from danoan.digital_note.core import api

import argparse
from pathlib import Path
import tempfile


def __split__(pdf_filepath: Path, temp_folder: Path, out_folder: Path, **kwargs):
    """
    Digitalize a pdf file and split each page into a separated text file.
    """
    out_folder.mkdir(exist_ok=True)
    if temp_folder:
        temp_folder.mkdir(exist_ok=True)
    else:
        temp_dir = tempfile.TemporaryDirectory()
        temp_folder = Path(temp_dir.name)

    for i, page in api.split(pdf_filepath, temp_folder):
        basename = pdf_filepath.name
        with open(out_folder / f"{basename}-{i}.txt", "w") as f_out:
            f_out.write(page)

    if temp_dir:
        temp_dir.cleanup()


def extend_parser(subparser_action=None):
    command_name = "split"
    description = __split__.__doc__
    help = description.split(".")[0] if description else ""

    if subparser_action:
        parser = subparser_action.add_parser(
            command_name,
            description=description,
            help=help,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
    else:
        parser = argparse.ArgumentParser(
            command_name,
            description=description,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )

    parser.add_argument("pdf_filepath", type=Path)
    parser.add_argument("out_folder", type=Path)
    parser.add_argument("--temp-folder", type=Path, default=None)
    parser.set_defaults(func=__split__, print_help=parser.print_help)
