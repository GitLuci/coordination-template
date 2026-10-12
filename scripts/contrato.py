"""Versões do contrato FE/BE: firma (registar) e verifica que nada mudou sem nova versão.

    python scripts/contrato.py registar --versao 2    # firma o estado actual de contrato/ como v2
    python scripts/contrato.py verificar             # falha se contrato/ mudou desde a última versão firmada
    python scripts/contrato.py verificar --contra ../coordenacao-x/contrato   # e se difere da cópia partilhada

O sha256 cobre o schema e os exemplos (tudo em contrato/ menos VERSOES.json e ALTERACOES.md), com os finais de linha
normalizados, para Windows e Linux darem o mesmo valor. Só a biblioteca padrão.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent / "contrato"
FORA = {"VERSOES.json", "ALTERACOES.md", "README.md"}


def sha(pasta: Path) -> str:
    h = hashlib.sha256()
    for f in sorted(p for p in pasta.rglob("*") if p.is_file() and p.name not in FORA):
        h.update(f.relative_to(pasta).as_posix().encode() + b"\0")
        h.update(f.read_bytes().replace(b"\r\n", b"\n") + b"\0")
    return h.hexdigest()


def versoes(pasta: Path) -> dict[str, str]:
    f = pasta / "VERSOES.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}


def registar(pasta: Path, versao: int) -> int:
    v = versoes(pasta)
    if v and versao <= max(map(int, v)):
        print(f"a versão tem de ser maior do que {max(map(int, v))}", file=sys.stderr)
        return 2
    actual = sha(pasta)
    if v and actual == v[max(v, key=int)]:
        print("o contrato não mudou desde a última versão firmada", file=sys.stderr)
        return 2
    v[str(versao)] = actual
    (pasta / "VERSOES.json").write_text(json.dumps(v, indent=2) + "\n", encoding="utf-8")
    print(f"contrato v{versao} firmado ({actual[:12]}). Regista a linha em ALTERACOES.md e avisa os devs.")
    return 0


def verificar(pasta: Path, contra: Path | None) -> int:
    v = versoes(pasta)
    if not v:
        print("nenhuma versão firmada: `registar --versao 1` primeiro", file=sys.stderr)
        return 1
    ultima = max(v, key=int)
    actual = sha(pasta)
    if actual != v[ultima]:
        print(f"o contrato mudou desde a v{ultima} sem nova versão firmada (pede ao coordenador)", file=sys.stderr)
        return 1
    if contra is not None:
        partilhado = versoes(contra)
        if not partilhado:
            print(f"{contra}: sem versões firmadas", file=sys.stderr)
            return 1
        ultima_p = max(partilhado, key=int)
        if ultima_p != ultima or sha(contra) != actual:
            print(f"esta cópia está na v{ultima}; a partilhada está na v{ultima_p}: actualiza a cópia", file=sys.stderr)
            return 1
    print(f"contrato v{ultima} ok")
    return 0


def main(argv=None) -> int:
    a = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    a.add_argument("--pasta", type=Path, default=RAIZ, help="pasta do contrato (omissão: contrato/ do repositório)")
    sub = a.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("registar")
    r.add_argument("--versao", type=int, required=True)
    c = sub.add_parser("verificar")
    c.add_argument("--contra", type=Path, help="a pasta do contrato partilhada (repositórios separados)")
    args = a.parse_args(argv)
    if args.cmd == "registar":
        return registar(args.pasta, args.versao)
    return verificar(args.pasta, args.contra)


if __name__ == "__main__":
    sys.exit(main())
