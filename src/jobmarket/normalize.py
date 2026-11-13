"""Normalización de texto y emparejamiento de términos por límite de palabra.

El bug central del proyecto anterior era `"sql" in texto`, que devuelve True
para "mysql" y "postgresql". Aquí cada término canónico tiene alias explícitos
y se compara con límites de palabra, nunca por subcadena.
"""
from __future__ import annotations

import re
import unicodedata
from functools import lru_cache

from .lexicon import CONTEXT_TERMS

_ESPACIOS = re.compile(r"\s+")
_ETIQUETAS = re.compile(r"<[^>]+>")
_ENTIDADES = [
    ("&nbsp;", " "), ("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"),
    ("&quot;", '"'), ("&#39;", "'"), ("&apos;", "'"), ("&mdash;", "—"),
    ("&ndash;", "–"), ("&hellip;", "…"), ("&rsquo;", "'"), ("&lsquo;", "'"),
]


def strip_html(texto: str) -> str:
    """Quita etiquetas HTML y normaliza entidades sin usar BeautifulSoup."""
    if not texto:
        return ""
    for ent, val in _ENTIDADES:
        texto = texto.replace(ent, val)
    texto = _ETIQUETAS.sub(" ", texto)
    texto = re.sub(r"&#\d+;", " ", texto)
    return _ESPACIOS.sub(" ", texto).strip()


def normalize(texto: str) -> str:
    """Minúsculas, sin acentos, espacios colapsados. Idempotente."""
    if not texto:
        return ""
    t = unicodedata.normalize("NFKD", texto.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return _ESPACIOS.sub(" ", t).strip()


@lru_cache(maxsize=4096)
def _patron(alias: str) -> re.Pattern[str]:
    """Compila un alias con límites alfanuméricos, no con \\b.

    \\b falla con términos como "ci/cd" o "c++". Se exige que el carácter
    anterior y el posterior no sean letras ni dígitos, lo que sí permite
    puntuación alrededor ("(qa)", "sql.", "react/typescript").

    Se admite una "s" final opcional para que "test case" cubra "test cases"
    sin necesidad de duplicar cada alias en plural. Los alias que ya terminan
    en "s" no la aceptan, para no generar "qa ss".
    """
    escapado = re.escape(alias)
    plural = "" if alias.endswith("s") else "s?"
    return re.compile(rf"(?<![a-z0-9]){escapado}{plural}(?![a-z0-9])", re.IGNORECASE)


def contains(normalized_text: str, alias: str) -> bool:
    """True si el alias aparece como palabra completa."""
    if not normalized_text or not alias:
        return False
    return _patron(normalize(alias)).search(normalized_text) is not None


def find_terms(normalized_text: str, lexicon: dict[str, tuple[str, ...]]) -> set[str]:
    """Devuelve los términos canónicos presentes en el texto.

    Un término cuenta si cualquiera de sus alias aparece como palabra completa.
    Antes de ejecutar la regex se hace una comprobación de subcadena barata:
    si el alias no aparece ni como subcadena, no puede aparecer como palabra.
    Eso reduce el trabajo en textos largos de minutos a segundos.
    """
    if not normalized_text:
        return set()
    return {
        canonico
        for canonico, alias in lexicon.items()
        if any(a in normalized_text and _patron(a).search(normalized_text) for a in alias)
    }


def find_terms_overlapping(
    normalized_text: str, lexicon: dict[str, tuple[str, ...]]
) -> set[str]:
    """Términos presentes, suprimiendo los que están contenidos en otro más largo.

    Sin esto, una oferta que dice "bug reporting" cuenta también como
    "reporting", y una que dice "test plan" cuenta como "test" y "plan" si
    existieran como términos. El término más largo gana y el corto se descarta
    solo cuando *todas* sus apariciones caen dentro de una más larga.
    """
    if not normalized_text:
        return set()

    apariciones: dict[str, list[tuple[int, int]]] = {}
    for canonico, alias in lexicon.items():
        if canonico in CONTEXT_TERMS:
            continue
        tramos: list[tuple[int, int]] = []
        for a in alias:
            if a not in normalized_text:
                continue
            tramos.extend((m.start(), m.end()) for m in _patron(a).finditer(normalized_text))
        if tramos:
            apariciones[canonico] = tramos

    if not apariciones:
        return set()

    # Longitud del término más largo que aparece en cada posición.
    cubierto_por_largo: dict[str, bool] = {}
    for corto, tramos_cortos in apariciones.items():
        todas_dentro = True
        for inicio, fin in tramos_cortos:
            dentro = any(
                otro != corto
                and fin - inicio < f2 - i2
                and i2 <= inicio
                and fin <= f2
                for otro, tramos_largos in apariciones.items()
                for i2, f2 in tramos_largos
            )
            if not dentro:
                todas_dentro = False
                break
        cubierto_por_largo[corto] = todas_dentro

    return {t for t in apariciones if not cubierto_por_largo[t]}


def count_terms(normalized_text: str, lexicon: dict[str, tuple[str, ...]]) -> dict[str, int]:
    """Cuenta ocurrencias por término canónico (suma de sus alias)."""
    salida: dict[str, int] = {}
    if not normalized_text:
        return salida
    for canonico, alias in lexicon.items():
        n = sum(len(_patron(a).findall(normalized_text)) for a in alias)
        if n:
            salida[canonico] = n
    return salida


def slug(texto: str) -> str:
    """Identificador estable para deduplicar títulos."""
    return re.sub(r"[^a-z0-9]+", " ", normalize(texto)).strip()
