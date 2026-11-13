"""Tests de los conectores con respuestas simuladas (sin red)."""
import pytest

from jobmarket import fetch


@pytest.fixture
def fake_get(monkeypatch):
    """Sustituye la descarga real por un payload fijo."""
    def _install(payload):
        monkeypatch.setattr(fetch, "_get", lambda url: payload)
    return _install


class TestRemoteOK:
    def test_parses_jobs(self, fake_get):
        fake_get([
            {"legal": "notice"},
            {"id": 1, "position": "QA Engineer", "company": "Acme",
             "location": "Remote", "tags": ["qa", "sql"],
             "description": "<p>Test cases</p>", "apply_url": "http://x"},
        ])
        jobs = fetch.remoteok()
        assert len(jobs) == 1
        assert jobs[0].title == "QA Engineer"
        assert jobs[0].source == "remoteok"
        assert "<p>" not in jobs[0].description

    def test_skips_entries_without_position(self, fake_get):
        fake_get([{"legal": "notice"}, {"id": 2, "company": "X"}])
        assert fetch.remoteok() == []

    def test_handles_non_list(self, fake_get):
        fake_get({"error": "rate limited"})
        assert fetch.remoteok() == []


class TestRemotive:
    def test_parses_jobs(self, fake_get):
        fake_get({"jobs": [{"id": 1, "title": "Support Agent", "company_name": "Beta",
                            "candidate_required_location": "LatAm", "category": "support",
                            "description": "Zendesk", "url": "http://y"}]})
        jobs = fetch.remotive(categories=("customer-support",))
        assert jobs[0].title == "Support Agent"
        assert jobs[0].location == "LatAm"


class TestJobicy:
    def test_parses_industry_and_level(self, fake_get):
        fake_get({"jobs": [{"id": 1, "jobTitle": "UX Designer", "companyName": "Gamma",
                            "jobGeo": "Remote", "jobIndustry": ["design"],
                            "jobLevel": "Senior", "jobDescription": "Figma"}]})
        jobs = fetch.jobicy(industries=("design",))
        assert "design" in jobs[0].category
        assert "Senior" in jobs[0].category


class TestArbeitnow:
    def test_parses_jobs(self, fake_get):
        fake_get({"data": [{"slug": "abc", "title": "Ops Coordinator",
                            "company_name": "Delta", "location": "Berlin",
                            "tags": ["ops"], "job_types": ["full-time"],
                            "description": "Inventory"}]})
        jobs = fetch.arbeitnow(pages=1)
        assert jobs[0].id == "abc"
        assert "full-time" in jobs[0].category

    def test_stops_when_page_is_empty(self, fake_get):
        fake_get({"data": []})
        assert fetch.arbeitnow(pages=5) == []


class TestHimalayas:
    def test_parses_location_restrictions(self, fake_get):
        fake_get({"jobs": [{"guid": "g1", "title": "QA Analyst", "companyName": "Epsilon",
                            "locationRestrictions": ["Worldwide", "Europe"],
                            "categories": ["qa"], "description": "Testing"}]})
        jobs = fetch.himalayas(pages=1)
        assert jobs[0].location == "Worldwide, Europe"


class TestFetchAll:
    def test_collects_and_reports_errors(self, monkeypatch):
        monkeypatch.setitem(fetch.SOURCES, "ok", lambda: [fetch._job(source="ok", title="T")])

        def boom():
            raise RuntimeError("caída")

        monkeypatch.setitem(fetch.SOURCES, "bad", boom)
        jobs, errores = fetch.fetch_all(["ok", "bad"])
        assert len(jobs) == 1
        assert "bad" in errores

    def test_unknown_source_reported(self):
        jobs, errores = fetch.fetch_all(["inventada"])
        assert jobs == []
        assert errores["inventada"] == "fuente desconocida"


class TestGetRetries:
    def test_raises_after_retries(self, monkeypatch):
        """Si la red falla siempre, se lanza FetchError en vez de colgarse."""
        import urllib.error

        def siempre_falla(*a, **k):
            raise urllib.error.URLError("sin red")

        monkeypatch.setattr(fetch.urllib.request, "urlopen", siempre_falla)
        monkeypatch.setattr(fetch.time, "sleep", lambda s: None)
        with pytest.raises(fetch.FetchError):
            fetch._get("http://ejemplo.com")
