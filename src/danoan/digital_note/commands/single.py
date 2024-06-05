from danoan.digital_note.core import api

import argparse
from pathlib import Path
import tempfile
from typing import Optional
import sys


def __single__(pdf_filepath: Path, temp_folder: Optional[Path], **kwargs):
    """
    Digitalize a pdf file into a single text file.
    """
    if temp_folder:
        temp_folder = temp_folder
        temp_folder.mkdir(exist_ok=True)
    else:
        temp_dir = tempfile.TemporaryDirectory()
        temp_folder = Path(temp_dir.name)

    api.single(pdf_filepath, temp_folder, sys.stdout)


def extend_parser(subparser_action=None):
    command_name = "single"
    description = __single__.__doc__
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
    parser.add_argument("--temp-folder", type=Path, default=None)
    parser.set_defaults(func=__single__, print_help=parser.print_help)
