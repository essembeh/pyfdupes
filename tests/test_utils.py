from pathlib import Path

from pyfdupes.fdupes import find_duplicates


def test_fdupes(data_folder: Path):
    duplicates = find_duplicates([data_folder])
    assert len(duplicates) == 5

    files = {files[0].name: files for files in duplicates}
    assert len(files) == 5
    assert len(files["lorem"]) == 2
    assert len(files["ipsum"]) == 2
    assert len(files["dolor"]) == 3
    assert len(files["sit"]) == 2
    assert len(files["amet"]) == 2
