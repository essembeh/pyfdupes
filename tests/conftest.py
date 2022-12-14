from pathlib import Path

import pytest


def mkfile(folder: Path, filename: str) -> Path:
    out = folder / filename
    assert not out.exists()
    out.parent.mkdir(exist_ok=True, parents=True)
    out.write_text(filename)
    return out


@pytest.fixture
def data_folder(tmp_path) -> Path:
    mkfile(tmp_path / "a", "lorem")
    mkfile(tmp_path / "a", "ipsum")
    mkfile(tmp_path / "a", "dolor")
    mkfile(tmp_path / "a", "sit")
    mkfile(tmp_path / "a", "amet")

    mkfile(tmp_path / "b", "lorem")
    mkfile(tmp_path / "b", "ipsum")
    mkfile(tmp_path / "b", "dolor")

    mkfile(tmp_path / "c", "dolor")
    mkfile(tmp_path / "c", "sit")
    mkfile(tmp_path / "c", "amet")

    return tmp_path
