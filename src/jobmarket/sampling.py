"""Muestreo estratificado con intervalos de confianza.

El bug de la versión anterior era `vacantes[:500]`: las primeras 500 filas del
CSV, que resultaban ser 84% de una sola fuente (Arbeitnow, Alemania). Eso no es
una muestra del mercado, es un sesgo con nombre de muestra.

Aquí el muestreo es estratificado por fuente y por perfil, con semilla fija
para que cualquiera pueda reproducir el resultado, y cada proporción lleva su
intervalo de Wilson para no reportar 3.4% como si fuera exacto.
"""
from __future__ import annotations

import math
import random
from collections import defaultdict
from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")


def wilson_interval(successes: int, total: int, z: float = 1.96) -> tuple[float, float]:
    """Intervalo de confianza de Wilson al 95% para una proporción.

    Se prefiere Wilson a la aproximación normal porque se comporta bien con
    proporciones pequeñas y extremas, que es justo el caso de "X% de las
    vacantes pide este término".
    """
    if total <= 0:
        return (0.0, 0.0)
    p = successes / total
    denom = 1 + z * z / total
    centro = (p + z * z / (2 * total)) / denom
    margen = (z * math.sqrt(p * (1 - p) / total + z * z / (4 * total * total))) / denom
    return (max(0.0, centro - margen), min(1.0, centro + margen))


def stratified_sample(
    items: Sequence[T],
    key,
    per_stratum: int,
    seed: int = 20260101,
    max_total: int | None = None,
) -> list[T]:
    """Toma hasta `per_stratum` elementos de cada estrato, de forma aleatoria.

    `key` es una función que devuelve el nombre del estrato para un elemento.
    La selección es determinista para una semilla dada.
    """
    rng = random.Random(seed)
    estratos: dict[str, list[T]] = defaultdict(list)
    for item in items:
        estratos[key(item)].append(item)

    salida: list[T] = []
    for nombre in sorted(estratos):
        grupo = estratos[nombre][:]
        rng.shuffle(grupo)
        salida.extend(grupo[:per_stratum])

    if max_total is not None and len(salida) > max_total:
        rng.shuffle(salida)
        salida = salida[:max_total]
    return salida


def sample_by_source(
    items: Sequence[T], per_source: int, seed: int = 20260101
) -> list[T]:
    """Atajo: estratifica por el atributo `source` del elemento."""
    return stratified_sample(
        items, key=lambda x: getattr(x, "source", "?"), per_stratum=per_source, seed=seed
    )


def describe_sample(items: Sequence[T]) -> dict[str, int]:
    """Cuenta elementos por fuente, para poder declararlo en el informe."""
    conteo: dict[str, int] = defaultdict(int)
    for item in items:
        conteo[getattr(item, "source", "?")] += 1
    return dict(sorted(conteo.items(), key=lambda kv: -kv[1]))


def proportion(numerator: int, denominator: int) -> dict[str, float]:
    """Devuelve proporción con su intervalo de Wilson, en porcentaje."""
    lo, hi = wilson_interval(numerator, denominator)
    pct = 100 * numerator / denominator if denominator else 0.0
    return {
        "pct": round(pct, 1),
        "ci_low": round(100 * lo, 1),
        "ci_high": round(100 * hi, 1),
    }
