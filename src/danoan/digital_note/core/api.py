from pathlib import Path
from io import TextIOBase

from pdf2image import convert_from_path
import pytesseract


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
