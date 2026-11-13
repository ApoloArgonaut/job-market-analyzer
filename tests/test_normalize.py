"""Tests de normalización y emparejamiento de términos.

El caso central: `sql` no debe coincidir dentro de `mysql` ni `postgresql`.
"""
import pytest

from jobmarket.normalize import contains, count_terms, find_terms, normalize, slug, strip_html


class TestNormalize:
    def test_lowercases_and_strips_accents(self):
        assert normalize("Análisis de DATOS") == "analisis de datos"

    def test_collapses_whitespace(self):
        assert normalize("  hola   mundo\n\t") == "hola mundo"

    def test_idempotent(self):
        once = normalize("Diseño UX/UI")
        assert normalize(once) == once

    def test_empty(self):
        assert normalize("") == ""
        assert normalize(None) == ""

    def test_slug(self):
        assert slug("QA Engineer (Remote)") == "qa engineer remote"


class TestStripHtml:
    def test_removes_tags(self):
        assert strip_html("<p>Hola <b>mundo</b></p>") == "Hola mundo"

    def test_decodes_entities(self):
        assert strip_html("A &amp; B") == "A & B"
        assert strip_html("&nbsp;x") == "x"

    def test_handles_none(self):
        assert strip_html(None) == ""


class TestContains:
    @pytest.mark.parametrize("texto,alias", [
        ("we use mysql daily", "mysql"),
        ("postgresql experience required", "postgresql"),
        ("strong sql skills", "sql"),
        ("sql, python and excel", "sql"),
        ("(sql)", "sql"),
    ])
    def test_matches_real_occurrences(self, texto, alias):
        assert contains(normalize(texto), alias)

    @pytest.mark.parametrize("texto", [
        "we use mysql daily",
        "postgresql experience required",
        "nosql databases",
        "mysqli extension",
    ])
    def test_does_not_match_sql_inside_other_words(self, texto):
        """El bug original: 'sql' in 'mysql' devolvía True."""
        assert not contains(normalize(texto), "sql")

    def test_respects_word_boundaries(self):
        assert not contains(normalize("qaeda"), "qa")
        assert contains(normalize("qa engineer"), "qa")

    def test_handles_slash_terms(self):
        assert contains(normalize("ci/cd pipelines"), "ci/cd")

    def test_handles_parentheses(self):
        assert contains(normalize("(remote)"), "remote")

    def test_empty_inputs(self):
        assert not contains("", "sql")
        assert not contains("sql", "")


class TestFindTerms:
    LEXICON = {
        "sql": ("sql", "mysql", "postgresql"),
        "python": ("python",),
        "qa": ("qa", "quality assurance"),
    }

    def test_finds_multiple(self):
        found = find_terms(normalize("Python, SQL and QA experience"), self.LEXICON)
        assert found == {"sql", "python", "qa"}

    def test_alias_maps_to_canonical(self):
        found = find_terms(normalize("strong postgresql background"), self.LEXICON)
        assert found == {"sql"}

    def test_no_false_positive(self):
        found = find_terms(normalize("we use mysql"), self.LEXICON)
        assert found == {"sql"}  # mysql es alias de sql, no una aparición suelta

    def test_empty(self):
        assert find_terms("", self.LEXICON) == set()


class TestCountTerms:
    LEXICON = {"python": ("python",), "sql": ("sql",)}

    def test_counts_occurrences(self):
        counts = count_terms(normalize("python python sql"), self.LEXICON)
        assert counts == {"python": 2, "sql": 1}

    def test_missing_term_absent(self):
        assert count_terms(normalize("python"), self.LEXICON) == {"python": 1}
