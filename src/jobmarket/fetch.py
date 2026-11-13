"""Ingesta desde APIs públicas de empleo.

Cada fuente vive en su propio conector, con reintentos y sin dependencias
externas (solo stdlib). El resultado siempre es una lista de `Job`.
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from collections.abc import Callable, Iterable

from .classify import Job
from .normalize import strip_html

UA = {"User-Agent": "jobmarket-analyzer/1.0 (+https://github.com/ApoloArgonaut)"}
TIMEOUT = 45
RETRIES = 3
BACKOFF = 2.0


class FetchError(RuntimeError):
    """Error recuperable al consultar una fuente."""


def _get(url: str) -> dict | list:
    """GET con reintentos exponenciales. Lanza FetchError si se agota."""
    ultimo: Exception | None = None
    for intento in range(RETRIES):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                return json.loads(resp.read().decode("utf-8", "replace"))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError) as exc:
            ultimo = exc
            if intento < RETRIES - 1:
                time.sleep(BACKOFF ** intento)
    raise FetchError(f"{url}: {ultimo}") from ultimo


def _job(**kw) -> Job:
    """Normaliza los campos comunes a todos los conectores."""
    return Job(
        id=str(kw.get("id") or ""),
        source=kw["source"],
        title=strip_html(kw.get("title") or ""),
        company=strip_html(kw.get("company") or ""),
        location=strip_html(kw.get("location") or ""),
        category=strip_html(kw.get("category") or ""),
        description=strip_html(kw.get("description") or ""),
        url=kw.get("url") or "",
        posted_at=kw.get("posted_at") or "",
    )


def remoteok() -> list[Job]:
    data = _get("https://remoteok.com/api")
    if not isinstance(data, list):
        return []
    return [
        _job(
            id=j.get("id"),
            source="remoteok",
            title=j.get("position"),
            company=j.get("company"),
            location=j.get("location"),
            category=" ".join(j.get("tags") or []),
            description=j.get("description"),
            url=j.get("apply_url") or j.get("url"),
            posted_at=j.get("date"),
        )
        for j in data
        if isinstance(j, dict) and j.get("position")
    ]


DEFAULT_REMOTIVE = ("software-dev", "customer-support", "design", "product", "data")


def remotive(categories: tuple[str, ...] = DEFAULT_REMOTIVE) -> list[Job]:
    salida: list[Job] = []
    for cat in categories:
        try:
            data = _get(f"https://remotive.com/api/remote-jobs?category={cat}&limit=2000")
        except FetchError:
            continue
        for j in data.get("jobs", []) if isinstance(data, dict) else []:
            salida.append(
                _job(
                    id=j.get("id"),
                    source="remotive",
                    title=j.get("title"),
                    company=j.get("company_name"),
                    location=j.get("candidate_required_location"),
                    category=j.get("category"),
                    description=j.get("description"),
                    url=j.get("url"),
                    posted_at=j.get("publication_date"),
                )
            )
        time.sleep(1)
    return salida


DEFAULT_JOBICY = ("supporting", "admin", "design", "creative", "business", "management")


def jobicy(industries: tuple[str, ...] = DEFAULT_JOBICY) -> list[Job]:
    salida: list[Job] = []
    for ind in industries:
        try:
            data = _get(f"https://jobicy.com/api/v2/remote-jobs?count=100&industry={ind}")
        except FetchError:
            continue
        for j in data.get("jobs", []) if isinstance(data, dict) else []:
            salida.append(
                _job(
                    id=j.get("id"),
                    source="jobicy",
                    title=j.get("jobTitle"),
                    company=j.get("companyName"),
                    location=j.get("jobGeo"),
                    category=" ".join(j.get("jobIndustry") or []) + " " + str(j.get("jobLevel") or ""),
                    description=j.get("jobDescription") or j.get("jobExcerpt"),
                    url=j.get("url"),
                    posted_at=j.get("pubDate"),
                )
            )
        time.sleep(1)
    return salida


def arbeitnow(pages: int = 8) -> list[Job]:
    salida: list[Job] = []
    for p in range(1, pages + 1):
        try:
            data = _get(f"https://www.arbeitnow.com/api/job-board-api?page={p}")
        except FetchError:
            break
        for j in data.get("data", []) if isinstance(data, dict) else []:
            salida.append(
                _job(
                    id=j.get("slug"),
                    source="arbeitnow",
                    title=j.get("title"),
                    company=j.get("company_name"),
                    location=j.get("location"),
                    category=" ".join(j.get("tags") or []) + " " + " ".join(j.get("job_types") or []),
                    description=j.get("description"),
                    url=j.get("url"),
                    posted_at=str(j.get("created_at") or ""),
                )
            )
        time.sleep(1)
    return salida


def himalayas(pages: int = 12) -> list[Job]:
    salida: list[Job] = []
    for i in range(pages):
        try:
            data = _get(f"https://himalayas.app/jobs/api?limit=100&offset={i * 100}")
        except FetchError:
            break
        jobs = data.get("jobs") if isinstance(data, dict) else None
        if not jobs:
            break
        for j in jobs:
            salida.append(
                _job(
                    id=j.get("guid") or j.get("id"),
                    source="himalayas",
                    title=j.get("title"),
                    company=j.get("companyName"),
                    location=", ".join(j.get("locationRestrictions") or []) or j.get("location"),
                    category=" ".join(j.get("categories") or []),
                    description=j.get("description"),
                    url=j.get("applicationLink") or j.get("guid"),
                    posted_at=str(j.get("pubDate") or ""),
                )
            )
        time.sleep(1)
    return salida


#: Conectores disponibles por nombre, para el CLI.
SOURCES: dict[str, Callable[..., list[Job]]] = {
    "remoteok": remoteok,
    "remotive": remotive,
    "jobicy": jobicy,
    "arbeitnow": arbeitnow,
    "himalayas": himalayas,
}


def fetch_all(names: Iterable[str] | None = None) -> tuple[list[Job], dict[str, str]]:
    """Ejecuta los conectores indicados y devuelve (vacantes, errores)."""
    seleccion = list(names) if names else list(SOURCES)
    vacantes: list[Job] = []
    errores: dict[str, str] = {}
    for nombre in seleccion:
        fn = SOURCES.get(nombre)
        if fn is None:
            errores[nombre] = "fuente desconocida"
            continue
        try:
            lote = fn()
            vacantes.extend(lote)
            print(f"  {nombre:<12} {len(lote):>5} vacantes")
        except Exception as exc:  # noqa: BLE001 - una fuente caída no debe tumbar todo
            errores[nombre] = str(exc)
            print(f"  {nombre:<12} ERROR: {exc}")
    return vacantes, errores
