"""Persistencia: CSV canónico y base SQLite para consultas.

La versión anterior tenía un CSV de 21 MB y ningún índice; cualquier análisis
recorría el archivo completo. Aquí el CSV es solo el formato de intercambio y
SQLite es la fuente de consulta, con índices sobre perfil y fuente.
"""
from __future__ import annotations

import csv
import sqlite3
from collections.abc import Iterable
from pathlib import Path

from .classify import Job, classify

FIELDS = ("id", "source", "title", "company", "location", "category", "description", "url", "posted_at")

SCHEMA = """
CREATE TABLE IF NOT EXISTS jobs (
    id          TEXT PRIMARY KEY,
    source      TEXT NOT NULL,
    title       TEXT NOT NULL,
    company     TEXT,
    location    TEXT,
    category    TEXT,
    description TEXT,
    url         TEXT,
    posted_at   TEXT,
    profile     TEXT
);
CREATE INDEX IF NOT EXISTS idx_jobs_profile ON jobs(profile);
CREATE INDEX IF NOT EXISTS idx_jobs_source  ON jobs(source);
CREATE INDEX IF NOT EXISTS idx_jobs_company ON jobs(company);
"""


def write_csv(jobs: Iterable[Job], path: Path) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        writer.writeheader()
        for job in jobs:
            writer.writerow({k: getattr(job, k) for k in FIELDS})
            n += 1
    return n


def read_csv(path: Path) -> list[Job]:
    """Lee un CSV de vacantes, aceptando el esquema inglés y el legacy en español."""
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        columnas = set(reader.fieldnames or [])
        legacy = "titulo" in columnas or "fuente" in columnas
        salida: list[Job] = []
        for row in reader:
            if legacy:
                salida.append(
                    Job(
                        id=(row.get("id") or "").strip(),
                        source=(row.get("fuente") or "").strip(),
                        title=(row.get("titulo") or "").strip(),
                        company=(row.get("empresa") or "").strip(),
                        location=(row.get("ubicacion") or "").strip(),
                        category=(row.get("categoria") or "").strip(),
                        description=(row.get("descripcion") or "").strip(),
                        url=(row.get("url") or "").strip(),
                        posted_at=(row.get("fecha") or "").strip(),
                    )
                )
            else:
                salida.append(Job(**{k: (row.get(k) or "") for k in FIELDS}))
        return salida


def write_sqlite(jobs: Iterable[Job], path: Path) -> int:
    """Escribe las vacantes con su perfil ya calculado."""
    path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(path)
    try:
        con.executescript(SCHEMA)
        filas = []
        for job in jobs:
            c = classify(job)
            filas.append(
                (job.id or f"{job.source}:{job.title}:{job.company}", job.source, job.title,
                 job.company, job.location, job.category, job.description, job.url,
                 job.posted_at, c.primary)
            )
        con.executemany(
            "INSERT OR REPLACE INTO jobs "
            "(id, source, title, company, location, category, description, url, posted_at, profile) "
            "VALUES (?,?,?,?,?,?,?,?,?,?)",
            filas,
        )
        con.commit()
        return len(filas)
    finally:
        con.close()


def connect(path: Path) -> sqlite3.Connection:
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    return con


def profile_counts(path: Path) -> dict[str, int]:
    con = connect(path)
    try:
        rows = con.execute(
            "SELECT COALESCE(profile,'(sin clasificar)') AS p, COUNT(*) AS n "
            "FROM jobs GROUP BY p ORDER BY n DESC"
        ).fetchall()
        return {r["p"]: r["n"] for r in rows}
    finally:
        con.close()
