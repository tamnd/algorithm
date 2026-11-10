# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/avr/. The authors are listed in prov/G3Q00A.jsonl.

import random
from fractions import Fraction

from avr import avr, edf_run, energy


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


def test_example():
    jobs = [(0, 4, 4), (1, 3, 3), (2, 2, 6)]
    h = Fraction(1, 2)
    assert avr(jobs) == [(0, 1, 1), (1, 2, 5 * h), (2, 3, 3), (3, 4, 3 * h), (4, 6, h)]
    assert energy(avr(jobs), 2) == 19
    assert energy(avr(jobs), 3) == Fraction(189, 4)
    assert yds_energy(jobs, 2) == Fraction(57, 4)
    assert yds_energy(jobs, 3) == Fraction(375, 16)
    assert edf_run(jobs, avr(jobs)) == [Fraction(10, 3), Fraction(13, 6), 6]


def test_single_job_is_optimal():
    jobs = [(2, 6, 5)]
    assert avr(jobs) == [(2, 5, 2)]
    for alpha in (2, 3):
        assert energy(avr(jobs), alpha) == yds_energy(jobs, alpha)


def test_feasible_and_ratio_on_random_inputs():
    rng = random.Random(1995)
    for alpha in (2, 3):
        bound = 2 ** (alpha - 1) * alpha ** alpha
        for _ in range(300):
            jobs = []
            for _ in range(rng.randint(1, 5)):
                r = rng.randint(0, 6)
                jobs.append((r, rng.randint(1, 6), r + rng.randint(1, 5)))
            pieces = avr(jobs)
            done = edf_run(jobs, pieces)
            assert all(c is not None and c <= d for c, (_, _, d) in zip(done, jobs))
            ratio = energy(pieces, alpha) / yds_energy(jobs, alpha)
            assert 1 <= ratio <= bound


def test_common_deadline_family_grows():
    # Job i is released at time i with deadline n and work about (n - i) ** (-1 / alpha).
    for alpha in (2, 3):
        last = 0
        for n in (2, 5, 10):
            jobs = [(i, Fraction((n - i) ** (-1 / alpha)).limit_denominator(10 ** 6), n) for i in range(n)]
            ratio = energy(avr(jobs), alpha) / yds_energy(jobs, alpha)
            assert last < ratio < alpha ** alpha
            last = ratio
        assert last > alpha ** alpha / 6
