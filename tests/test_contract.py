import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import contract  # noqa: E402

TEMPLATE = Path(__file__).resolve().parent.parent / "contract"


def copy(tmp_path, name="c"):
    dest = tmp_path / name
    shutil.copytree(TEMPLATE, dest)
    (dest / "VERSIONS.json").write_text("{}\n", encoding="utf-8")
    return dest


def test_sign_and_verify(tmp_path):
    c = copy(tmp_path)
    assert contract.verify(c, None) == 1                    # nothing signed
    assert contract.register(c, 1) == 0
    assert contract.verify(c, None) == 0
    assert contract.register(c, 2) == 2                     # no changes, so no new version
    assert contract.register(c, 1) == 2                     # versions only go up


def test_change_without_version_fails(tmp_path):
    c = copy(tmp_path)
    contract.register(c, 1)
    (c / "openapi.yaml").write_text("changed\n", encoding="utf-8")
    assert contract.verify(c, None) == 1
    assert contract.register(c, 2) == 0 and contract.verify(c, None) == 0


def test_line_endings_dont_count(tmp_path):
    c = copy(tmp_path)
    contract.register(c, 1)
    f = c / "openapi.yaml"
    f.write_bytes(f.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
    assert contract.verify(c, None) == 0


def test_outdated_copy_against_the_shared_one(tmp_path):
    shared, local = copy(tmp_path, "s"), copy(tmp_path, "l")
    contract.register(shared, 1)
    contract.register(local, 1)
    assert contract.verify(local, shared) == 0
    (shared / "openapi.yaml").write_text("v2\n", encoding="utf-8")
    contract.register(shared, 2)
    assert contract.verify(local, shared) == 1
