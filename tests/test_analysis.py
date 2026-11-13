"""Tests de análisis, persistencia e ingesta."""
from pathlib import Path

import pytest

from jobmarket.analysis import analyze_all, analyze_profile, market_gaps
from jobmarket.classify import Job
from jobmarket.store import profile_counts, read_csv, write_csv, write_sqlite


def make_job(title, description="", source="test", company="Acme", jid=None):
    return Job(
        id=jid or f"{title}-{company}", source=source, title=title,
        company=company, location="Remote", category="", description=description,
    )


class TestAnalyzeProfile:
    def test_counts_term_presence(self):
        jobs = [
            make_job("QA Engineer", "test cases and jira"),
            make_job("QA Analyst", "test cases"),
            make_job("QA Lead", "selenium automation"),
        ]
        stats = analyze_profile(jobs, "QA", min_count=1)
        por_termino = {t.term: t for t in stats.terms}
        assert por_termino["test_cases"].count == 2
        assert por_termino["test_cases"].pct == pytest.approx(66.7, abs=0.1)

    def test_reports_confidence_interval(self):
        jobs = [make_job(f"QA {i}", "test cases" if i % 2 == 0 else "selenium") for i in range(20)]
        stats = analyze_profile(jobs, "QA", min_count=1)
        t = next(x for x in stats.terms if x.term == "test_cases")
        assert t.count == 10
        assert t.ci_low < t.pct < t.ci_high

    def test_confidence_interval_is_tight_at_the_edges(self):
        """Con 20 de 20 el IC toca 100% por arriba: no es un error, es Wilson."""
        jobs = [make_job(f"QA {i}", "test cases") for i in range(20)]
        stats = analyze_profile(jobs, "QA", min_count=1)
        t = next(x for x in stats.terms if x.term == "test_cases")
        assert t.pct == 100.0
        assert t.ci_high == 100.0
        assert t.ci_low < 100.0

    def test_min_count_filters_noise(self):
        jobs = [make_job("QA Engineer", "jira")]
        stats = analyze_profile(jobs, "QA", min_count=3)
        assert all(t.count >= 3 for t in stats.terms)

    def test_default_min_count_is_three(self):
        """Con el umbral por defecto, un término que aparece una vez no se reporta."""
        jobs = [make_job("QA Engineer", "jira")]
        stats = analyze_profile(jobs, "QA")
        assert stats.terms == []

    def test_empty_profile(self):
        stats = analyze_profile([], "QA")
        assert stats.total == 0
        assert stats.terms == []

    def test_tracks_sources_per_term(self):
        jobs = [
            make_job("QA 1", "jira", source="remoteok"),
            make_job("QA 2", "jira", source="arbeitnow"),
        ]
        stats = analyze_profile(jobs, "QA", min_count=1)
        t = next(x for x in stats.terms if x.term == "jira")
        assert t.by_source == {"remoteok": 1, "arbeitnow": 1}


class TestAnalyzeAll:
    def test_groups_by_profile(self):
        jobs = [
            make_job("QA Engineer", "test cases"),
            make_job("UX Designer", "figma prototyping"),
        ]
        stats = analyze_all(jobs)
        assert "QA" in stats
        assert "UX" in stats

    def test_ignores_unclassified(self):
        stats = analyze_all([make_job("Chef", "paella")])
        assert stats == {}


class TestMarketGaps:
    def test_separates_missing_from_strengths(self):
        jobs = [make_job(f"QA {i}", "selenium jira test cases") for i in range(10)]
        brechas, fortalezas = market_gaps(jobs, "QA", have={"jira"})
        assert all(t.term != "jira" for t in brechas)
        assert any(t.term == "jira" for t in fortalezas)

    def test_limits_output(self):
        jobs = [make_job(f"QA {i}", "selenium cypress playwright jira postman") for i in range(10)]
        brechas, _ = market_gaps(jobs, "QA", have=set(), top=2)
        assert len(brechas) <= 2


class TestStore:
    def test_csv_roundtrip(self, tmp_path: Path):
        jobs = [make_job("QA Engineer", "testing"), make_job("UX Designer", "figma")]
        ruta = tmp_path / "v.csv"
        assert write_csv(jobs, ruta) == 2
        leidas = read_csv(ruta)
        assert len(leidas) == 2
        assert leidas[0].title == "QA Engineer"

    def test_sqlite_counts_by_profile(self, tmp_path: Path):
        jobs = [
            make_job("QA Engineer", "test cases"),
            make_job("QA Analyst", "test cases"),
            make_job("UX Designer", "figma"),
        ]
        db = tmp_path / "v.db"
        write_sqlite(jobs, db)
        conteo = profile_counts(db)
        assert conteo["QA"] == 2
        assert conteo["UX"] == 1

    def test_sqlite_survives_duplicate_ids(self, tmp_path: Path):
        jobs = [make_job("QA Engineer", jid="same"), make_job("QA Engineer", jid="same")]
        db = tmp_path / "v.db"
        write_sqlite(jobs, db)
        assert sum(profile_counts(db).values()) == 1
