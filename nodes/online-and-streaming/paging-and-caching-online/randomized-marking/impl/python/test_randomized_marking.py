# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/randomized-marking/. The authors are listed in prov/6JHBAR.jsonl.

import random
from collections.abc import Hashable, Sequence
from fractions import Fraction

from randomized_marking import RandomizedMarking, expected_faults_exact, randomized_marking


def harmonic(k: int) -> Fraction:
    return sum((Fraction(1, i) for i in range(1, k + 1)), Fraction(0))


def opt_faults(sigma: Sequence[Hashable], k: int) -> int:
    """Optimal faults by search over all caches (small inputs only)."""
    best: dict[frozenset, int] = {frozenset(): 0}
    for p in sigma:
        new: dict[frozenset, int] = {}
        for c, f in best.items():
            if p in c:
                outs = [(c, f)]
            elif len(c) < k:
                outs = [(c | {p}, f + 1)]
            else:
                outs = [((c - {q}) | {p}, f + 1) for q in c]
            for c2, f2 in outs:
                if f2 < new.get(c2, f2 + 1):
                    new[c2] = f2
        best = new
    return min(best.values())


def phases(sigma: Sequence[Hashable], k: int) -> list[set[Hashable]]:
    out: list[set[Hashable]] = []
    for p in sigma:
        if not out or (p not in out[-1] and len(out[-1]) == k):
            out.append(set())
        out[-1].add(p)
    return out


def new_page_counts(sigma: Sequence[Hashable], k: int) -> list[int]:
    ph = phases(sigma, k)
    return [len(ph[0])] + [len(ph[i] - ph[i - 1]) for i in range(1, len(ph))] if ph else []


def test_worked_values() -> None:
    assert expected_faults_exact([1, 2, 3, 4, 1, 2], 3) == Fraction(29, 6)
    assert expected_faults_exact([1, 2, 3, 4, 1, 2, 5, 1, 2, 3], 3) == Fraction(23, 3)
    assert expected_faults_exact([1, 2, 3, 4, 5, 1, 2, 6, 3, 4], 3) == Fraction(29, 3)
    assert opt_faults([1, 2, 3, 4, 1, 2, 5, 1, 2, 3], 3) == 6
    assert harmonic(3) * 2 == Fraction(11, 3)


def test_edges() -> None:
    rng = random.Random(0)
    assert randomized_marking([], 2, rng) == 0
    assert randomized_marking([1, 1, 1], 1, rng) == 1
    assert randomized_marking([1, 2, 1, 2], 1, rng) == 4
    assert randomized_marking([1, 2, 1, 2, 1], 2, rng) == 2
    assert expected_faults_exact([1, 2, 1, 2], 1) == 4


def test_new_pages_first_formula() -> None:
    # Phase 2 requests m new pages, then the k - m stale pages once each.
    for k in range(1, 6):
        for m in range(1, k + 1):
            sigma = list(range(k)) + list(range(k, k + m)) + list(range(m, k))
            phase2 = expected_faults_exact(sigma, k) - k
            assert phase2 == m * (1 + harmonic(k) - harmonic(m))
            assert phase2 <= m * harmonic(k)


def test_within_2hk_of_opt() -> None:
    rng = random.Random(1)
    for _ in range(500):
        k = rng.randint(1, 3)
        sigma = [rng.randrange(rng.randint(1, k + 2)) for _ in range(rng.randint(0, 10))]
        e = expected_faults_exact(sigma, k)
        opt = opt_faults(sigma, k)
        ms = new_page_counts(sigma, k)
        assert 2 * opt >= sum(ms)
        assert e <= harmonic(k) * sum(ms)
        assert e <= 2 * harmonic(k) * opt
        assert e <= k * opt


def test_every_run_is_marking() -> None:
    rng = random.Random(2)
    for _ in range(500):
        k = rng.randint(1, 5)
        sigma = [rng.randrange(k + 3) for _ in range(rng.randint(0, 40))]
        c = RandomizedMarking(k, rng)
        seen: set[Hashable] = set()
        for p in sigma:
            if p not in seen and len(seen) == k:
                seen = set()
            v = c.request(p)
            assert v is None or v not in seen
            seen.add(p)
            assert seen <= c.cache and len(c.cache) <= k
            assert set(c.unmarked) == c.cache - seen
        assert c.faults <= k * len(phases(sigma, k))


def test_sample_mean_matches_exact() -> None:
    rng = random.Random(3)
    for sigma, k in (([1, 2, 3, 4, 1, 2, 5, 1, 2, 3], 3), ([0, 1, 2, 3, 4, 0, 1, 5, 2, 3, 0, 4], 4)):
        e = float(expected_faults_exact(sigma, k))
        runs = 20000
        mean = sum(randomized_marking(sigma, k, rng) for _ in range(runs)) / runs
        assert abs(mean - e) < 0.05


def test_cycle_against_deterministic() -> None:
    # On the cycle of k + 1 pages LRU faults on every request; marking with random choice does far better.
    k = 8
    sigma = [t % (k + 1) for t in range(9000)]
    f = randomized_marking(sigma, k, random.Random(4))
    assert f < len(sigma) / 2
    assert f <= 2 * float(harmonic(k)) * (len(sigma) / k + 1)
