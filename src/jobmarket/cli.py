"""CLI del analizador de mercado laboral."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .analysis import analyze_all
from .fetch import SOURCES, fetch_all
from .report import render_markdown, write_report
from .sampling import describe_sample, sample_by_source
from .store import profile_counts, read_csv, write_csv, write_sqlite

DATA = Path("data")
DEFAULT_CSV = DATA / "vacantes.csv"
DEFAULT_DB = DATA / "vacantes.db"
DEFAULT_REPORT = Path("reports") / "informe-mercado.md"


def cmd_fetch(args: argparse.Namespace) -> int:
    print(f"Consultando {len(args.sources) if args.sources else 'todas las'} fuentes…")
    jobs, errores = fetch_all(args.sources)
    if not jobs:
        print("No se recuperó ninguna vacante.", file=sys.stderr)
        return 1

    # Deduplicar por (título, empresa) normalizados.
    vistos: set[tuple[str, str]] = set()
    unicos = []
    for job in jobs:
        clave = (job.title.lower().strip(), job.company.lower().strip())
        if not job.title or clave in vistos:
            continue
        vistos.add(clave)
        unicos.append(job)

    write_csv(unicos, Path(args.out))
    write_sqlite(unicos, DEFAULT_DB)
    print(f"\n{len(jobs)} recogidas · {len(unicos)} únicas -> {args.out}")
    if errores:
        print(f"Fuentes con error: {', '.join(errores)}")
    return 0


def cmd_analyze(args: argparse.Namespace) -> int:
    ruta = Path(args.input)
    if not ruta.exists():
        print(f"No existe {ruta}. Ejecuta primero: jobmarket fetch", file=sys.stderr)
        return 1

    corpus = read_csv(ruta)
    if args.per_source > 0:
        muestra = sample_by_source(corpus, per_source=args.per_source, seed=args.seed)
    else:
        muestra = corpus
    print(f"corpus: {len(corpus)} · analizadas: {len(muestra)}")

    stats = analyze_all(muestra, min_count=args.min_count)
    cubiertas = sum(s.classified for s in stats.values())
    print(f"clasificadas en algún perfil: {cubiertas} ({100 * cubiertas / max(len(muestra), 1):.1f}%)")

    md = render_markdown(
        stats,
        sample_size=len(muestra),
        corpus_size=len(corpus),
        sources=describe_sample(muestra),
    )
    write_report(md, Path(args.out))
    print(f"informe -> {args.out}")

    if args.json:
        payload = {
            perfil: {
                "classified": s.classified,
                "terms": [
                    {"term": t.term, "count": t.count, "pct": t.pct, "ci": [t.ci_low, t.ci_high]}
                    for t in s.terms[:40]
                ],
            }
            for perfil, s in stats.items()
        }
        Path(args.json).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"json -> {args.json}")
    return 0


def cmd_stats(args: argparse.Namespace) -> int:
    if not DEFAULT_DB.exists():
        print("No hay base de datos. Ejecuta: jobmarket fetch", file=sys.stderr)
        return 1
    for perfil, n in profile_counts(DEFAULT_DB).items():
        print(f"  {perfil:<16}{n:>6}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="jobmarket",
        description="Analiza la demanda real del mercado laboral remoto: qué piden las ofertas, por perfil.",
    )
    sub = p.add_subparsers(dest="command", required=True)

    f = sub.add_parser("fetch", help="Descarga vacantes de las APIs públicas")
    f.add_argument("--sources", nargs="*", choices=list(SOURCES), default=None)
    f.add_argument("--out", default=str(DEFAULT_CSV))
    f.set_defaults(func=cmd_fetch)

    a = sub.add_parser("analyze", help="Genera el informe de demanda por perfil")
    a.add_argument("--input", default=str(DEFAULT_CSV))
    a.add_argument("--out", default=str(DEFAULT_REPORT))
    a.add_argument("--json", default="")
    a.add_argument("--per-source", type=int, default=0,
                   help="Vacantes por fuente (0 = corpus completo, por defecto)")
    a.add_argument("--seed", type=int, default=20260101)
    a.add_argument("--min-count", type=int, default=3, help="Mínimo de apariciones para reportar un término")
    a.set_defaults(func=cmd_analyze)

    s = sub.add_parser("stats", help="Cuenta vacantes por perfil en la base")
    s.set_defaults(func=cmd_stats)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
