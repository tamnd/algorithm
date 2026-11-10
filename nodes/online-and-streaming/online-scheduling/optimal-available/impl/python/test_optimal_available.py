# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimal-available/. The authors are listed in prov/4DSS0A.jsonl.

import random
from fractions import Fraction

from optimal_available import energy, optimal_available


def yds_energy(jobs, alpha):
    """Optimal energy by the YDS algorithm, in exact arithmetic."""
    rest = [(Fraction(r), Fraction(w), Fraction(d)) for r, w, d in jobs]
    total = Fraction(0)
    while rest:
        best = None
        for a in {r for r, _, _ in rest}:
            for b in {d for _, _, d in rest}:
                if b <= a:
                    continue
                work = sum(w for r, w, d in rest if a <= r and d <= b)
                if work > 0 and (best is None or work / (b - a) > best[0]):
                    best = (work / (b - a), a, b)
        g, a, b = best
        total += g ** alpha * (b - a)
        length = b - a

        def squeeze(t):
            return t if t <= a else (a if t < b else t - length)

        rest = [(squeeze(r), w, squeeze(d)) for r, w, d in rest if not (a <= r and d <= b)]
    return total


def avr_energy(jobs, alpha):
    """Energy of AVR, the sum of the densities of the open windows."""
    points = sorted({x for r, _, d in jobs for x in (r, d)})
    total = Fraction(0)
    for a, b in zip(points, points[1:]):
        s = sum(Fraction(w, d - r) for r, w, d in jobs if r <= a and b <= d)
        total += s ** alpha * (b - a)
    return total


def test_example():
    jobs = [(0, 4, 4), (1, 3, 3), (2, 2, 6)]
    pieces, done = optimal_available(jobs)
    assert pieces == [(0, 1, 1), (1, 2, 2), (2, 4, 2), (4, 6, 1)]
    assert done == [4, Fraction(5, 2), 6]
    assert energy(pieces, 2) == 15
    assert energy(pieces, 3) == 27
    assert energy(pieces, 2) / yds_energy(jobs, 2) == Fraction(20, 19)


def test_one_release_is_optimal():
    # With all jobs released together, OA is the YDS schedule.
    jobs = [(0, 3, 2), (0, 1, 5), (0, 4, 4)]
    for alpha in (2, 3):
        assert energy(optimal_available(jobs)[0], alpha) == yds_energy(jobs, alpha)


def test_feasible_and_ratio_on_random_inputs():
    rng = random.Random(2007)
    for alpha in (2, 3):
        for _ in range(300):
            jobs = []
            for _ in range(rng.randint(1, 5)):
                r = rng.randint(0, 6)
                jobs.append((r, rng.randint(1, 6), r + rng.randint(1, 5)))
            pieces, done = optimal_available(jobs)
            assert all(c <= d for c, (_, _, d) in zip(done, jobs))
            assert sum(s * (b - a) for a, b, s in pieces) == sum(w for _, w, _ in jobs)
            ratio = energy(pieces, alpha) / yds_energy(jobs, alpha)
            assert 1 <= ratio <= alpha ** alpha


def test_lower_bound_family():
    # Common deadline n; job i at time i with work about (n - i) ** (-1 / alpha).
    for alpha in (2, 3):
        last = 0
        for n in (2, 5, 10):
            jobs = [(i, Fraction((n - i) ** (-1 / alpha)).limit_denominator(10 ** 6), n) for i in range(n)]
            oa = energy(optimal_available(jobs)[0], alpha)
            assert oa == avr_energy(jobs, alpha)
            ratio = oa / yds_energy(jobs, alpha)
            assert last < ratio < alpha ** alpha
            last = ratio
