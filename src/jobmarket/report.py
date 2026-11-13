"""Generación del informe en Markdown."""
from __future__ import annotations

from datetime import date
from pathlib import Path

from .analysis import ProfileStats


def _tabla_terminos(stats: ProfileStats, limite: int = 25) -> list[str]:
    lineas = [
        "| Término | Ofertas | % | IC 95% | Fuentes |",
        "|---|---:|---:|---|---|",
    ]
    for t in stats.terms[:limite]:
        fuentes = ", ".join(f"{k} ({v})" for k, v in sorted(t.by_source.items(), key=lambda kv: -kv[1])[:3])
        lineas.append(
            f"| `{t.term}` | {t.count}/{t.total} | {t.pct}% | "
            f"{t.ci_low}–{t.ci_high}% | {fuentes} |"
        )
    return lineas


def render_markdown(
    stats: dict[str, ProfileStats],
    sample_size: int,
    corpus_size: int,
    sources: dict[str, int],
) -> str:
    hoy = date.today().isoformat()
    out = [
        "# Análisis de demanda del mercado laboral",
        "",
        f"*Generado el {hoy} · muestra de **{sample_size}** vacantes sobre un corpus de **{corpus_size}**.*",
        "",
        "## Método",
        "",
        "Cada vacante se clasifica en un perfil primario ponderando las señales del",
        "título (peso 3) y de la descripción (peso 1). Los términos se detectan con",
        "coincidencia por límite de palabra sobre alias explícitos, de modo que `sql`",
        "no cuenta como aparición en `mysql` ni en `postgresql`.",
        "",
        "El porcentaje indica en cuántas ofertas del perfil aparece el término.",
        "El intervalo del 95% (método de Wilson) dice cuánta incertidumbre hay:",
        "un término con 4% y un IC de 2–7% no es lo mismo que uno con 4% y 3.8–4.2%.",
        "",
        "### Muestra por fuente",
        "",
        "| Fuente | Vacantes en la muestra |",
        "|---|---:|",
    ]
    for fuente, n in sorted(sources.items(), key=lambda kv: -kv[1]):
        out.append(f"| {fuente} | {n} |")

    out += ["", "## Perfiles", "", "| Perfil | Ofertas clasificadas |", "|---|---:|"]
    for perfil, s in sorted(stats.items(), key=lambda kv: -kv[1].classified):
        out.append(f"| {perfil} | {s.classified} |")

    for perfil, s in sorted(stats.items(), key=lambda kv: -kv[1].classified):
        if not s.terms:
            continue
        out += ["", f"## {perfil} — {s.classified} ofertas", "", *_tabla_terminos(s), ""]

    return "\n".join(out)


def write_report(markdown: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(markdown, encoding="utf-8")
