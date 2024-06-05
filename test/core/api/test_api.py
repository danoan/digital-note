from danoan.digital_note.core import api

import io
from pathlib import Path
import shutil
import tempfile

SCRIPT_FOLDER = Path(__file__).parent
INPUT_FOLDER = SCRIPT_FOLDER / "input"
EXPECTED_FOLDER = SCRIPT_FOLDER / "expected"


def compare_lines(t1: str, t2: str):
    for t1_line, t2_line in zip(t1.splitlines(), t2.splitlines()):
        assert t1_line == t2_line


def test_single():
    pdf_filepath = INPUT_FOLDER / "botafogo.pdf"
    ss = io.StringIO()
    with tempfile.TemporaryDirectory() as temp_dir:
        api.single(pdf_filepath, Path(temp_dir), ss)

    ss.seek(0, io.SEEK_SET)
    with open(EXPECTED_FOLDER / "botafogo.txt") as f:
        compare_lines(f.read(), ss.getvalue())


def test_split():
    pdf_filepath = INPUT_FOLDER / "jekyll_hyde.pdf"
    with tempfile.TemporaryDirectory() as temp_dir:
        digitizations = list(api.split(pdf_filepath, Path(temp_dir)))
        assert len(digitizations) == 3

    expected_filepaths = [
        EXPECTED_FOLDER / "jekyll_hyde.pdf-0.txt",
        EXPECTED_FOLDER / "jekyll_hyde.pdf-1.txt",
        EXPECTED_FOLDER / "jekyll_hyde.pdf-2.txt",
    ]

    for index, expected_filepath in enumerate(expected_filepaths):
        with open(expected_filepath) as f:
            compare_lines(digitizations[index][1], f.read())


def test_batch():
    pdf_filepath_1 = INPUT_FOLDER / "botafogo.pdf"
    pdf_filepath_2 = INPUT_FOLDER / "jekyll_hyde.pdf"

    with tempfile.TemporaryDirectory() as pdf_dir, tempfile.TemporaryDirectory() as temp_folder, tempfile.TemporaryDirectory() as out_folder:
        shutil.copy2(pdf_filepath_1, pdf_dir)
        shutil.copy2(pdf_filepath_2, pdf_dir)

        api.batch(Path(pdf_dir), Path(temp_folder), Path(out_folder))

        assert (Path(out_folder) / f"{pdf_filepath_1.name}.txt").exists()
        assert (Path(out_folder) / f"{pdf_filepath_2.name}.txt").exists()
