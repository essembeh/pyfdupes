import shlex
from typing import List, Tuple
from unittest import mock

import pytest

from pyfdupes import __name__ as prog
from pyfdupes import __version__ as version
from pyfdupes import cli


def run(capsys, args: str) -> Tuple[int, List[str], List[str]]:
    with pytest.raises(SystemExit) as error:
        with mock.patch("sys.argv", [prog] + shlex.split(args)):
            cli.run()
    captured = capsys.readouterr()
    return (
        error.value.code,
        captured.out.splitlines(),
        captured.err.splitlines(),
    )  # pyright: reportGeneralTypeIssues=false


def assert_no_error(
    rc: int, out: List[str], err: List[str]
) -> Tuple[int, List[str], List[str]]:
    assert rc == 0
    assert len(out) > 0
    assert len(err) == 0
    return rc, out, err


def test_help(capsys):
    assert_no_error(*run(capsys, "--help"))


def test_version(capsys):
    _rc, out, _err = assert_no_error(*run(capsys, "--version"))
    assert len(out) == 1
    assert version in out[0]


def test_nodelete(capsys, data_folder):
    rc, out, err = run(capsys, f"--quiet {data_folder}")
    assert rc == 0
    assert len(out) == 1
    assert len(err) == 0

    assert (data_folder / "a" / "lorem").exists()
    assert (data_folder / "a" / "ipsum").exists()
    assert (data_folder / "a" / "dolor").exists()
    assert (data_folder / "a" / "sit").exists()
    assert (data_folder / "a" / "amet").exists()

    assert (data_folder / "b" / "lorem").exists()
    assert (data_folder / "b" / "ipsum").exists()
    assert (data_folder / "b" / "dolor").exists()

    assert (data_folder / "c" / "dolor").exists()
    assert (data_folder / "c" / "sit").exists()
    assert (data_folder / "c" / "amet").exists()


def test_delete(capsys, data_folder):
    rc, out, err = run(capsys, f"--quiet -k {data_folder}/b {data_folder} --rm")
    assert rc == 0
    assert len(out) > 0
    assert len(err) == 0

    assert not (data_folder / "a" / "lorem").exists()
    assert not (data_folder / "a" / "ipsum").exists()
    assert not (data_folder / "a" / "dolor").exists()
    assert (data_folder / "a" / "sit").exists()
    assert (data_folder / "a" / "amet").exists()

    assert (data_folder / "b" / "lorem").exists()
    assert (data_folder / "b" / "ipsum").exists()
    assert (data_folder / "b" / "dolor").exists()

    assert not (data_folder / "c" / "dolor").exists()
    assert (data_folder / "c" / "sit").exists()
    assert (data_folder / "c" / "amet").exists()


def test_delete_first(capsys, data_folder):
    rc, out, err = run(capsys, f"--quiet -1 -k {data_folder} --rm")
    assert rc == 0
    assert len(out) > 0
    assert len(err) == 0

    assert (data_folder / "a" / "lorem").exists()
    assert (data_folder / "a" / "ipsum").exists()
    assert (data_folder / "a" / "dolor").exists()
    assert (data_folder / "a" / "sit").exists()
    assert (data_folder / "a" / "amet").exists()

    assert not (data_folder / "b" / "lorem").exists()
    assert not (data_folder / "b" / "ipsum").exists()
    assert not (data_folder / "b" / "dolor").exists()

    assert not (data_folder / "c" / "dolor").exists()
    assert not (data_folder / "c" / "sit").exists()
    assert not (data_folder / "c" / "amet").exists()


def test_nodelete_first(capsys, data_folder):
    rc, out, err = run(capsys, f"--quiet -1 {data_folder} --rm")
    assert rc == 0
    assert len(out) > 0
    assert len(err) == 0

    assert (data_folder / "a" / "lorem").exists()
    assert (data_folder / "a" / "ipsum").exists()
    assert (data_folder / "a" / "dolor").exists()
    assert (data_folder / "a" / "sit").exists()
    assert (data_folder / "a" / "amet").exists()

    assert (data_folder / "b" / "lorem").exists()
    assert (data_folder / "b" / "ipsum").exists()
    assert (data_folder / "b" / "dolor").exists()

    assert (data_folder / "c" / "dolor").exists()
    assert (data_folder / "c" / "sit").exists()
    assert (data_folder / "c" / "amet").exists()
