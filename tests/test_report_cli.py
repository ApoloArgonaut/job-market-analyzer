"""Tests del generador de informe y del CLI."""
import json
from pathlib import Path

import pytest

from jobmarket.analysis import ProfileStats, TermStat
from jobmarket.classify import Job
from jobmarket.cli import main
from jobmarket.report import render_markdown, write_report
from jobmarket.store import write_csv


def stat(term="sql", count=10, total=100, pct=10.0, ci=(7.0, 14.0), sources=None):
    return TermStat(term=term, count=count, total=total, pct=pct,
                    ci_low=ci[0], ci_high=ci[1], by_source=sources or {"remoteok": count})


class TestRenderMarkdown:
    def test_contains_header_and_sample_size(self):
        md = render_markdown({}, sample_size=400, corpus_size=4239, sources={"remoteok": 400})
        assert "# Análisis de demanda" in md
        assert "400" in md
        assert "4239" in md

    def test_declares_method(self):
        md = render_markdown({}, 10, 100, {"x": 10})
        assert "Método" in md
        assert "Wilson" in md

    def test_lists_sources(self):
        md = render_markdown({}, 30, 100, {"remoteok": 20, "arbeitnow": 10})
        assert "| remoteok | 20 |" in md
        assert "| arbeitnow | 10 |" in md

    def test_renders_term_table(self):
        stats = {"QA": ProfileStats(profile="QA", total=100, classified=50, terms=[stat()])}
        md = render_markdown(stats, 50, 200, {"remoteok": 50})
        assert "| `sql` | 10/100 | 10.0% |" in md
        assert "7.0–14.0%" in md

    def test_profile_without_terms_is_skipped(self):
        stats = {"QA": ProfileStats(profile="QA", total=0, classified=0, terms=[])}
        md = render_markdown(stats, 0, 0, {})
        assert "## QA" not in md

    def test_limits_terms_per_profile(self):
        terms = [stat(term=f"t{i}") for i in range(50)]
        stats = {"QA": ProfileStats(profile="QA", total=100, classified=100, terms=terms)}
        md = render_markdown(stats, 100, 100, {"x": 100})
        assert md.count("| `t") == 25


class TestWriteReport:
    def test_creates_parent_dirs(self, tmp_path: Path):
        destino = tmp_path / "a" / "b" / "informe.md"
        write_report("# hola", destino)
        assert destino.read_text(encoding="utf-8") == "# hola"


@pytest.fixture
def corpus(tmp_path: Path) -> Path:
    jobs = []
    for i in range(20):
        jobs.append(Job(id=f"q{i}", source="remoteok" if i % 2 else "arbeitnow",
                        title=f"QA Engineer {i}", company=f"Co{i}", location="Remote",
                        category="", description="test cases jira selenium"))
    for i in range(10):
        jobs.append(Job(id=f"u{i}", source="remoteok", title=f"UX Designer {i}",
                        company=f"Design{i}", location="Remote", category="",
                        description="figma prototyping user research"))
    ruta = tmp_path / "vacantes.csv"
    write_csv(jobs, ruta)
    return ruta


class TestCli:
    def test_analyze_generates_report(self, corpus: Path, tmp_path: Path):
        salida = tmp_path / "informe.md"
        code = main(["analyze", "--input", str(corpus), "--out", str(salida), "--min-count", "1"])
        assert code == 0
        assert salida.exists()
        assert "QA" in salida.read_text(encoding="utf-8")

    def test_analyze_writes_json(self, corpus: Path, tmp_path: Path):
        salida = tmp_path / "informe.md"
        js = tmp_path / "out.json"
        code = main(["analyze", "--input", str(corpus), "--out", str(salida), "--json", str(js)])
        assert code == 0
        data = json.loads(js.read_text(encoding="utf-8"))
        assert "QA" in data
        assert data["QA"]["terms"][0]["term"]

    def test_missing_input_fails_cleanly(self, tmp_path: Path):
        code = main(["analyze", "--input", str(tmp_path / "nope.csv"),
                     "--out", str(tmp_path / "o.md")])
        assert code == 1

    def test_parser_requires_command(self):
        with pytest.raises(SystemExit):
            main([])

    def test_unknown_source_rejected(self):
        with pytest.raises(SystemExit):
            main(["fetch", "--sources", "invented"])
