"""Modelo de dominio y clasificación de vacantes por perfil.

Corrige el bug de la versión anterior, donde una vacante podía quedar en dos
perfiles a la vez con la misma fuerza y donde el 48.9% quedaba sin clasificar
porque el `elif` cortaba la evaluación.
"""
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field

from .lexicon import ROLE_PROFILES
from .normalize import contains, normalize


@dataclass(slots=True)
class Job:
    id: str
    source: str
    title: str
    company: str
    location: str
    category: str
    description: str
    url: str = ""
    posted_at: str = ""

    def __post_init__(self) -> None:
        self.title = (self.title or "").strip()
        self.company = (self.company or "").strip()
        self.location = (self.location or "").strip()

    @property
    def text(self) -> str:
        """Texto normalizado del título + categoría, para clasificar."""
        return normalize(f"{self.title} {self.category}")

    @property
    def body(self) -> str:
        """Descripción normalizada, recortada para no penalizar rendimiento."""
        return normalize(self.description)[:8000]


@dataclass(slots=True)
class Classification:
    """Resultado de clasificar una vacante.

    `primary` es el perfil de mayor puntuación, o None si ninguno alcanza el
    umbral. `scores` guarda todas las puntuaciones para poder auditar.
    """

    primary: str | None
    scores: dict[str, float] = field(default_factory=dict)
    matched_on: dict[str, list[str]] = field(default_factory=dict)

    @property
    def is_classified(self) -> bool:
        return self.primary is not None


#: Peso del título frente a la descripción. Una coincidencia en el título vale
#: mucho más que una mención suelta en un párrafo de 4.000 caracteres.
TITLE_WEIGHT = 3.0
DESC_WEIGHT = 1.0
#: Umbral mínimo para considerar que una vacante pertenece a un perfil.
MIN_SCORE = 1.0


def score_profiles(job: Job) -> dict[str, float]:
    """Puntúa cada perfil según coincidencias en título y descripción."""
    titulo = job.text
    cuerpo = job.body
    salida: dict[str, float] = {}
    for perfil, senales in ROLE_PROFILES.items():
        puntos = 0.0
        for senal in senales:
            if contains(titulo, senal):
                puntos += TITLE_WEIGHT
            elif contains(cuerpo, senal):
                puntos += DESC_WEIGHT
        if puntos:
            salida[perfil] = puntos
    return salida


def classify(job: Job) -> Classification:
    """Asigna el perfil con mayor puntuación, documentando la evidencia."""
    scores = score_profiles(job)
    if not scores:
        return Classification(primary=None)

    ordenados = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
    mejor, puntos = ordenados[0]
    if puntos < MIN_SCORE:
        return Classification(primary=None, scores=scores)

    evidencia: dict[str, list[str]] = {}
    titulo = job.text
    cuerpo = job.body
    for senal in ROLE_PROFILES[mejor]:
        if contains(titulo, senal):
            evidencia.setdefault("title", []).append(senal)
        elif contains(cuerpo, senal):
            evidencia.setdefault("description", []).append(senal)

    return Classification(primary=mejor, scores=scores, matched_on=evidencia)


def classify_all(jobs: Iterable[Job]) -> dict[str, list[Job]]:
    """Agrupa vacantes por perfil primario. Omite las no clasificadas."""
    grupos: dict[str, list[Job]] = {}
    for job in jobs:
        c = classify(job)
        if c.primary:
            grupos.setdefault(c.primary, []).append(job)
    return grupos


def coverage_report(jobs: Iterable[Job]) -> dict[str, int]:
    """Cuenta clasificadas frente a no clasificadas (auditoría rápida)."""
    total = clasificadas = 0
    for job in jobs:
        total += 1
        if classify(job).is_classified:
            clasificadas += 1
    return {"total": total, "classified": clasificadas, "unclassified": total - clasificadas}
