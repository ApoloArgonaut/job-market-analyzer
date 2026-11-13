"""Tests de clasificación por perfil."""

from jobmarket.classify import (
    MIN_SCORE,
    TITLE_WEIGHT,
    Job,
    classify,
    classify_all,
    coverage_report,
    score_profiles,
)


def job(title: str, description: str = "", category: str = "", company: str = "Acme") -> Job:
    return Job(
        id="1", source="test", title=title, company=company,
        location="Remote", category=category, description=description,
    )


class TestScoreProfiles:
    def test_title_match_outweighs_description(self):
        en_titulo = score_profiles(job("QA Engineer", "we build things"))
        en_desc = score_profiles(job("Software Person", "you will do qa work"))
        assert en_titulo["QA"] > en_desc["QA"]

    def test_title_weight_is_applied(self):
        scores = score_profiles(job("QA Specialist"))
        assert scores["QA"] == TITLE_WEIGHT

    def test_no_match_returns_empty(self):
        assert score_profiles(job("Chef de cocina", "cocinar paella")) == {}


class TestClassify:
    def test_single_clear_profile(self):
        c = classify(job("Senior QA Engineer", "manual testing, test cases, jira"))
        assert c.primary == "QA"

    def test_unclassified_instead_of_guessing(self):
        """La versión anterior forzaba una etiqueta; aquí se admite 'sin clasificar'."""
        c = classify(job("Chef de cocina", "cocinar paella para clientes"))
        assert c.primary is None
        assert not c.is_classified

    def test_records_evidence(self):
        c = classify(job("QA Engineer", "test cases and jira"))
        assert "qa" in c.matched_on.get("title", [])

    def test_tie_breaks_deterministically(self):
        """Con puntuación idéntica, el resultado no debe cambiar entre ejecuciones."""
        j = job("Operations Coordinator", "operations coordinator")
        assert classify(j).primary == classify(j).primary

    def test_support_beats_ops_when_title_is_support(self):
        c = classify(job("Customer Support Specialist", "help desk tickets"))
        assert c.primary == "SUPPORT"

    def test_min_score_threshold_exists(self):
        assert MIN_SCORE > 0


class TestClassifyAll:
    def test_groups_by_primary(self):
        jobs = [
            job("QA Engineer", "testing"),
            job("QA Analyst", "test cases"),
            job("UX Designer", "figma"),
        ]
        grupos = classify_all(jobs)
        assert len(grupos["QA"]) == 2
        assert len(grupos["UX"]) == 1

    def test_omits_unclassified(self):
        grupos = classify_all([job("Chef", "paella")])
        assert grupos == {}

    def test_each_job_in_exactly_one_group(self):
        """Bug de la versión anterior: una vacante podía caer en dos perfiles."""
        jobs = [job("QA Engineer", "operations administrative support ux design")]
        grupos = classify_all(jobs)
        total = sum(len(v) for v in grupos.values())
        assert total == 1


class TestCoverageReport:
    def test_counts(self):
        jobs = [job("QA Engineer"), job("Chef", "paella"), job("UX Designer", "figma")]
        r = coverage_report(jobs)
        assert r == {"total": 3, "classified": 2, "unclassified": 1}

    def test_empty(self):
        assert coverage_report([]) == {"total": 0, "classified": 0, "unclassified": 0}
