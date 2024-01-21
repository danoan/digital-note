import argparse
from io import TextIOBase
from pathlib import Path
import sys

from pdf2image import convert_from_path
import pytesseract

SCRIPT_FOLDER = Path(__file__).parent.absolute()


def single(pdf_filepath: Path, temp_folder: Path, out_stream: TextIOBase):
    images = convert_from_path(pdf_filepath, output_folder=temp_folder, fmt="png")

    for image in images:
        out_stream.write(pytesseract.image_to_string(image))


def split(pdf_filepath: Path, temp_folder: Path):
    images = convert_from_path(pdf_filepath, output_folder=temp_folder, fmt="png")

    for i, image in enumerate(images):
        yield i, pytesseract.image_to_string(image)


def batch(pdf_folder: Path, temp_folder: Path, out_folder: Path):
    pdf_pattern = r"*.pdf"
    for pdf_filepath in pdf_folder.glob(pdf_pattern):
        basename = pdf_filepath.name
        with open(out_folder / f"{basename}.txt", "w") as f:
            single(pdf_filepath, temp_folder, f)


def __single__(pdf_filepath: Path, temp_folder: Path, **kwargs):
    temp_folder.mkdir(exist_ok=True)
    single(pdf_filepath, temp_folder, sys.stdout)


def __split__(pdf_filepath: Path, temp_folder: Path, out_folder: Path, **kwargs):
    temp_folder.mkdir(exist_ok=True)
    out_folder.mkdir(exist_ok=True)
    for i, page in split(pdf_filepath, temp_folder):
        basename = pdf_filepath.name
        with open(out_folder / f"{basename}-{i}.txt", "w") as f_out:
            f_out.write(page)


def __batch__(pdf_folder: Path, temp_folder: Path, out_folder: Path, **kwargs):
    temp_folder.mkdir(exist_ok=True)
    out_folder.mkdir(exist_ok=True)
    batch(pdf_folder, temp_folder, out_folder)


def main():
    parser = argparse.ArgumentParser("digital-note")

    subparsers = parser.add_subparsers()
    parser_single = subparsers.add_parser(
        "single", help="Digitalize a pdf file into a single text file."
    )
    parser_single.add_argument("pdf_filepath", type=Path)
    parser_single.add_argument(
        "--temp-folder", type=Path, default=SCRIPT_FOLDER / "temp-images"
    )
    parser_single.set_defaults(func=__single__, print_help=parser_single.print_help)

    parser_split = subparsers.add_parser(
        "split",
        help="Digitalize a pdf file and split each page into a separated text file.",
    )
    parser_split.add_argument("pdf_filepath", type=Path)
    parser_split.add_argument("out_folder", type=Path)
    parser_split.add_argument(
        "--temp-folder", type=Path, default=SCRIPT_FOLDER / "temp-images"
    )
    parser_split.set_defaults(func=__split__, print_help=parser_split.print_help)

    parser_batch = subparsers.add_parser(
        "batch", help="Digitalize several pdf files at once."
    )
    parser_batch.add_argument("pdf_folder", type=Path)
    parser_batch.add_argument("out_folder", type=Path)
    parser_batch.add_argument(
        "--temp-folder", type=Path, default=SCRIPT_FOLDER / "temp-images"
    )
    parser_batch.set_defaults(func=__batch__, print_help=parser_batch.print_help)

    args = parser.parse_args()
    if "func" in args:
        args.func(**vars(args))
    elif "print_help" in args:
        args.print_help()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
