"""Tests de muestreo e intervalos de confianza."""
import pytest

from jobmarket.sampling import (
    describe_sample,
    proportion,
    sample_by_source,
    stratified_sample,
    wilson_interval,
)


class TestWilsonInterval:
    def test_known_value(self):
        """50 de 100 al 95%: el IC de Wilson es aproximadamente 40.4–59.6%."""
        lo, hi = wilson_interval(50, 100)
        assert 0.40 < lo < 0.41
        assert 0.59 < hi < 0.60

    def test_small_proportion_stays_positive(self):
        lo, _ = wilson_interval(1, 1000)
        assert lo >= 0.0

    def test_perfect_proportion_capped_at_one(self):
        _, hi = wilson_interval(100, 100)
        assert hi <= 1.0

    def test_zero_total(self):
        assert wilson_interval(0, 0) == (0.0, 0.0)

    def test_interval_narrows_with_more_data(self):
        ancho_pequeno = wilson_interval(5, 50)
        ancho_grande = wilson_interval(500, 5000)
        assert (ancho_grande[1] - ancho_grande[0]) < (ancho_pequeno[1] - ancho_pequeno[0])


class TestStratifiedSample:
    def test_takes_from_every_stratum(self):
        items = [{"s": "a", "i": i} for i in range(100)] + [{"s": "b", "i": i} for i in range(5)]
        muestra = stratified_sample(items, key=lambda x: x["s"], per_stratum=10)
        fuentes = {x["s"] for x in muestra}
        assert fuentes == {"a", "b"}
        assert sum(1 for x in muestra if x["s"] == "b") == 5  # solo hay 5

    def test_caps_per_stratum(self):
        items = [{"s": "a", "i": i} for i in range(100)]
        muestra = stratified_sample(items, key=lambda x: x["s"], per_stratum=10)
        assert len(muestra) == 10

    def test_deterministic_for_same_seed(self):
        items = [{"s": "a", "i": i} for i in range(100)]
        a = stratified_sample(items, key=lambda x: x["s"], per_stratum=20, seed=42)
        b = stratified_sample(items, key=lambda x: x["s"], per_stratum=20, seed=42)
        assert a == b

    def test_different_seed_different_sample(self):
        items = [{"s": "a", "i": i} for i in range(100)]
        a = stratified_sample(items, key=lambda x: x["s"], per_stratum=20, seed=1)
        b = stratified_sample(items, key=lambda x: x["s"], per_stratum=20, seed=2)
        assert a != b

    def test_respects_max_total(self):
        items = [{"s": c, "i": i} for c in "abcde" for i in range(100)]
        muestra = stratified_sample(items, key=lambda x: x["s"], per_stratum=50, max_total=100)
        assert len(muestra) == 100

    def test_empty(self):
        assert stratified_sample([], key=lambda x: x["s"], per_stratum=10) == []


class TestSampleBySource:
    def test_uses_source_attribute(self):
        class Item:
            def __init__(self, source):
                self.source = source

        items = [Item("remoteok") for _ in range(50)] + [Item("arbeitnow") for _ in range(3)]
        muestra = sample_by_source(items, per_source=10)
        assert len(muestra) == 13

    def test_prevents_single_source_dominance(self):
        """El bug original: 84% de la muestra venía de una sola fuente."""
        class Item:
            def __init__(self, source):
                self.source = source

        items = [Item("arbeitnow") for _ in range(4000)] + [Item("remoteok") for _ in range(1000)]
        muestra = sample_by_source(items, per_source=400)
        fuentes = describe_sample(muestra)
        proporcion_arbeitnow = fuentes["arbeitnow"] / len(muestra)
        assert proporcion_arbeitnow == pytest.approx(0.5, abs=0.05)

    def test_caps_even_when_one_source_is_huge(self):
        """Con una fuente 40x mayor, el tope por estrato sigue mandando."""
        class Item:
            def __init__(self, source):
                self.source = source

        items = [Item("arbeitnow") for _ in range(4000)] + [Item("remoteok") for _ in range(100)]
        muestra = sample_by_source(items, per_source=400)
        fuentes = describe_sample(muestra)
        assert fuentes["arbeitnow"] <= 400
        assert fuentes["remoteok"] == 100


class TestDescribeSample:
    def test_counts_by_source(self):
        class Item:
            def __init__(self, source):
                self.source = source

        items = [Item("a"), Item("a"), Item("b")]
        assert describe_sample(items) == {"a": 2, "b": 1}

    def test_sorted_descending(self):
        class Item:
            def __init__(self, source):
                self.source = source

        items = [Item("b")] + [Item("a") for _ in range(5)]
        assert list(describe_sample(items)) == ["a", "b"]


class TestProportion:
    def test_returns_pct_and_ci(self):
        p = proportion(25, 100)
        assert p["pct"] == 25.0
        assert p["ci_low"] < 25.0 < p["ci_high"]

    def test_zero_denominator(self):
        p = proportion(0, 0)
        assert p["pct"] == 0.0
