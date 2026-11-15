"""Revisa que requisitos (R), reglas (BR) y criterios (AC) estén conectados, pareja por pareja.

Uso, desde la raíz del repo:  python scripts/verificar_trazabilidad.py
Sale con código 1 si encuentra huecos.

Qué comprueba:
- Cada R (menos R12, que se mide con coverage.py) y cada BR lo cita al menos un criterio.
- En la trazabilidad, los criterios de cada fila citan de verdad el requisito de esa fila.
- Las reglas (BR) de cada fila son exactamente las que citan los criterios de esa fila.
- Entre todas las filas de un requisito están todos los criterios que lo citan.
- Todo criterio aparece en la trazabilidad y no hay IDs que no existan.
"""
import re
import sys
from collections import defaultdict
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

    # Criterios: id -> (requisitos que cita, reglas que cita)
    ac = {}
    for m in re.finditer(r"^\| (AC\d\d) \| ([^|]*)\|", criterios, re.M):
        refs = m.group(2)
        ac[m.group(1)] = (set(re.findall(r"\bR\d\d\b", refs)), set(re.findall(r"\bBR\d\d\b", refs)))

    problemas = []
    citados_R = set().union(*(v[0] for v in ac.values())) if ac else set()
    citados_BR = set().union(*(v[1] for v in ac.values())) if ac else set()
    # R12 (cobertura) se verifica con la medición de coverage.py, no con un AC
    problemas += [f"R sin criterio que lo cite: {x}" for x in sorted(R - citados_R - {"R12"})]
    problemas += [f"BR sin criterio que la cite: {x}" for x in sorted(BR - citados_BR)]
    for a, (rs, bs) in sorted(ac.items()):
        for ref in sorted((rs - R) | (bs - BR)):
            problemas.append(f"{a} cita {ref}, que no existe")

    esperado = defaultdict(set)  # R -> criterios que lo citan
    for a, (rs, _) in ac.items():
        for r in rs:
            esperado[r].add(a)

    vistos = defaultdict(set)  # R -> criterios que aparecen en sus filas
    ac_en_traza = set()
    for m in re.finditer(r"^\| (R\d\d) \| ([^|]*)\| ([^|]*)\|", traza, re.M):
        r, col_br, col_ac = m.group(1), m.group(2), m.group(3)
        if r not in R:
            problemas.append(f"la trazabilidad usa {r}, que no existe")
            continue
        filas_ac = set(re.findall(r"AC\d\d", col_ac))
        filas_br = set(re.findall(r"BR\d\d", col_br))
        for a in sorted(filas_ac):
            if a not in ac:
                problemas.append(f"{r}: la trazabilidad cita {a}, que no existe")
            elif r not in ac[a][0]:
                problemas.append(f"{r}: {a} está en su fila pero ese criterio no cita {r}")
        validos = filas_ac & set(ac)
        de_los_criterios = set().union(*(ac[a][1] for a in validos)) if validos else set()
        for b in sorted(filas_br - de_los_criterios):
            problemas.append(f"{r}: {b} está en su fila pero ninguno de sus criterios la cita")
        for b in sorted(de_los_criterios - filas_br):
            problemas.append(f"{r}: sus criterios citan {b} pero falta en las reglas de la fila")
        vistos[r] |= filas_ac
        ac_en_traza |= filas_ac

    for r in sorted(R - {"R12"}):
        for a in sorted(esperado[r] - vistos[r]):
            problemas.append(f"{r}: falta {a} en la trazabilidad (ese criterio cita {r})")
    problemas += [f"AC que no está en la trazabilidad: {x}" for x in sorted(set(ac) - ac_en_traza)]

    print(f"R={len(R)} BR={len(BR)} AC={len(ac)}")
    if problemas:
        print("PROBLEMAS:")
        for p in problemas:
            print(" -", p)
        return 1
    print("OK: sin inconsistencias")
    return 0


if __name__ == "__main__":
    sys.exit(main())
