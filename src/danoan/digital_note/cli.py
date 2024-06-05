from danoan.digital_note.core import api
from danoan.digital_note.commands import single, split, batch

import argparse
from pathlib import Path
import sys


SCRIPT_FOLDER = Path(__file__).parent.absolute()


def __split__(pdf_filepath: Path, temp_folder: Path, out_folder: Path, **kwargs):
    temp_folder.mkdir(exist_ok=True)
    out_folder.mkdir(exist_ok=True)
    for i, page in api.split(pdf_filepath, temp_folder):
        basename = pdf_filepath.name
        with open(out_folder / f"{basename}-{i}.txt", "w") as f_out:
            f_out.write(page)


def __batch__(pdf_folder: Path, temp_folder: Path, out_folder: Path, **kwargs):
    temp_folder.mkdir(exist_ok=True)
    out_folder.mkdir(exist_ok=True)
    api.batch(pdf_folder, temp_folder, out_folder)


def main():
    parser = argparse.ArgumentParser("digital-note")

    subparsers = parser.add_subparsers()

    list_of_commands = [single, split, batch]
    for command in list_of_commands:
        command.extend_parser(subparsers)

    args = parser.parse_args()
    if "func" in args:
        args.func(**vars(args))
    elif "subcommand_help" in args:
        args.subcommand_help()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
