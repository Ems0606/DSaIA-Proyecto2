"""Revisa que requisitos (R), reglas (BR) y criterios (AC) estén conectados.

Uso, desde la raíz del repo:  python scripts/verificar_trazabilidad.py
Sale con código 1 si encuentra huecos.
"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def leer(ruta):
    return (RAIZ / ruta).read_text(encoding="utf-8")


def main():
    req = leer("specs/requirements.md")
    reglas = leer("specs/business-rules.md")
    criterios = leer("specs/acceptance-criteria.md")
    traza = leer("docs/traceability.md")

    R = set(re.findall(r"^\| (R\d\d) \|", req, re.M))
    BR = set(re.findall(r"^\| (BR\d\d) \|", reglas, re.M))
    AC = set(re.findall(r"^\| (AC\d\d) \|", criterios, re.M))
    refs = " ".join(re.findall(r"^\| AC\d\d \| ([^|]*)\|", criterios, re.M))
    traza_R = set(re.findall(r"^\| (R\d\d) \|", traza, re.M))
    traza_AC = set(re.findall(r"AC\d\d", traza))
    traza_BR = set(re.findall(r"BR\d\d", traza))

    problemas = []
    # R12 (cobertura) se verifica con la medición de coverage.py, no con un AC
    problemas += [f"R sin criterio que lo cite: {x}" for x in sorted(R - set(re.findall(r"\bR\d\d\b", refs)) - {"R12"})]
    problemas += [f"BR sin criterio que la cite: {x}" for x in sorted(BR - set(re.findall(r"BR\d\d", refs)))]
    problemas += [f"R sin fila en la trazabilidad: {x}" for x in sorted(R - traza_R)]
    problemas += [f"AC que no está en la trazabilidad: {x}" for x in sorted(AC - traza_AC)]
    problemas += [f"AC de la trazabilidad que no existe: {x}" for x in sorted(traza_AC - AC)]
    problemas += [f"BR de la trazabilidad que no existe: {x}" for x in sorted(traza_BR - BR)]
    for ref in sorted(set(re.findall(r"\b(?:R|BR)\d\d\b", refs)) - R - BR):
        problemas.append(f"un criterio cita {ref}, que no existe")

    print(f"R={len(R)} BR={len(BR)} AC={len(AC)}")
    if problemas:
        print("PROBLEMAS:")
        for p in problemas:
            print(" -", p)
        return 1
    print("OK: sin inconsistencias")
    return 0


if __name__ == "__main__":
    sys.exit(main())
