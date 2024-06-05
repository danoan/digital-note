from danoan.digital_note.core import api

import argparse
from pathlib import Path
import tempfile


def __batch__(pdf_folder: Path, temp_folder: Path, out_folder: Path, **kwargs):
    """
    Digitalize several pdf files at once.
    """
    out_folder.mkdir(exist_ok=True)
    if temp_folder:
        temp_folder = temp_folder
        temp_folder.mkdir(exist_ok=True)
    else:
        temp_dir = tempfile.TemporaryDirectory()
        temp_folder = Path(temp_dir.name)

    api.batch(pdf_folder, temp_folder, out_folder)
    if temp_dir:
        temp_dir.cleanup()


def extend_parser(subparser_action=None):
    command_name = "batch"
    description = __batch__.__doc__
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

    parser.add_argument("pdf_folder", type=Path)
    parser.add_argument("out_folder", type=Path)
    parser.add_argument("--temp-folder", type=Path, default=None)
    parser.set_defaults(func=__batch__, print_help=parser.print_help)
