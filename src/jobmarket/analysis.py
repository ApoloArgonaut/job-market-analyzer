"""Análisis de demanda por término, con intervalos de confianza y control de sesgo.

Diferencia clave con la versión anterior: se reporta el tamaño de muestra real,
el intervalo de confianza al 95% y la desagregación por fuente, de modo que un
término que solo aparece en una bolsa de un país no se presente como tendencia
global.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, field

from .classify import Job, classify
from .lexicon import LEXICON
from .normalize import find_terms_overlapping, normalize
from .sampling import proportion


@dataclass(slots=True)
class TermStat:
    term: str
    count: int
    total: int
    pct: float
    ci_low: float
    ci_high: float
    by_source: dict[str, int] = field(default_factory=dict)



@dataclass(slots=True)
class ProfileStats:
    profile: str
    total: int
    classified: int
    terms: list[TermStat] = field(default_factory=list)


def _presence(texto: str) -> set[str]:
    """Términos canónicos presentes, sin contar los contenidos en otro más largo."""
    return find_terms_overlapping(texto, LEXICON)


def analyze_profile(jobs: list[Job], profile: str, min_count: int = 3) -> ProfileStats:
    """Calcula la frecuencia de cada término dentro de un perfil."""
    if not jobs:
        return ProfileStats(profile=profile, total=0, classified=0)

    presencia: Counter[str] = Counter()
    por_fuente: dict[str, Counter[str]] = defaultdict(Counter)
    validos = 0

    for job in jobs:
        texto = normalize(f"{job.title} {job.category} {job.description}")
        if not texto.strip():
            continue
        validos += 1
        encontrados = _presence(texto)
        presencia.update(encontrados)
        for t in encontrados:
            por_fuente[t][job.source] += 1

    stats = []
    for term, n in presencia.most_common():
        if n < min_count:
            continue
        p = proportion(n, validos)
        stats.append(
            TermStat(
                term=term,
                count=n,
                total=validos,
                pct=p["pct"],
                ci_low=p["ci_low"],
                ci_high=p["ci_high"],
                by_source=dict(por_fuente[term]),
            )
        )
    return ProfileStats(profile=profile, total=validos, classified=len(jobs), terms=stats)


def analyze_all(jobs: list[Job], min_count: int = 3) -> dict[str, ProfileStats]:
    """Agrupa por perfil primario y analiza cada grupo."""
    grupos: dict[str, list[Job]] = defaultdict(list)
    for job in jobs:
        c = classify(job)
        if c.primary:
            grupos[c.primary].append(job)
    return {p: analyze_profile(js, p, min_count) for p, js in sorted(grupos.items())}


def market_gaps(
    jobs: list[Job], profile: str, have: set[str], top: int = 15
) -> tuple[list[TermStat], list[TermStat]]:
    """Separa lo que piden y tienes de lo que piden y te falta.

    Devuelve (brechas, fortalezas): los términos más demandados que NO están en
    `have`, y los más demandados que sí están.
    """
    stats = analyze_profile(jobs, profile)
    brechas = [t for t in stats.terms if t.term not in have][:top]
    fortalezas = [t for t in stats.terms if t.term in have][:top]
    return brechas, fortalezas
