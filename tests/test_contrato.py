import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import contrato  # noqa: E402

MODELO = Path(__file__).resolve().parent.parent / "contrato"


def copia(tmp_path, nome="c"):
    destino = tmp_path / nome
    shutil.copytree(MODELO, destino)
    (destino / "VERSOES.json").write_text("{}\n", encoding="utf-8")
    return destino


def test_firmar_e_verificar(tmp_path):
    c = copia(tmp_path)
    assert contrato.verificar(c, None) == 1                 # nada firmado
    assert contrato.registar(c, 1) == 0
    assert contrato.verificar(c, None) == 0
    assert contrato.registar(c, 2) == 2                     # sem mudanças não há versão nova
    assert contrato.registar(c, 1) == 2                     # versões só sobem


def test_mudanca_sem_versao_falha(tmp_path):
    c = copia(tmp_path)
    contrato.registar(c, 1)
    (c / "openapi.yaml").write_text("mudou\n", encoding="utf-8")
    assert contrato.verificar(c, None) == 1
    assert contrato.registar(c, 2) == 0 and contrato.verificar(c, None) == 0


def test_finais_de_linha_nao_contam(tmp_path):
    c = copia(tmp_path)
    contrato.registar(c, 1)
    f = c / "openapi.yaml"
    f.write_bytes(f.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
    assert contrato.verificar(c, None) == 0


def test_copia_desactualizada_contra_a_partilhada(tmp_path):
    partilhada, local = copia(tmp_path, "p"), copia(tmp_path, "l")
    contrato.registar(partilhada, 1)
    contrato.registar(local, 1)
    assert contrato.verificar(local, partilhada) == 0
    (partilhada / "openapi.yaml").write_text("v2\n", encoding="utf-8")
    contrato.registar(partilhada, 2)
    assert contrato.verificar(local, partilhada) == 1
