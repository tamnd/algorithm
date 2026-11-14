# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aalen-johansen-estimator/. The authors are listed in prov/ZVA82Z.jsonl.

import math
import random
from fractions import Fraction

from aalen_johansen_estimator import (
    Subject, competing_risks_subjects, cumulative_incidence, evaluate, kaplan_meier, transition_matrices,
)


def random_data(rng, n, K, censor=0.3, ties=True):
    times = [rng.randint(1, 9) if ties else rng.random() for _ in range(n)]
    causes = [0 if rng.random() < censor else rng.randint(1, K) for _ in range(n)]
    return times, causes


def grid(times):
    return sorted(set(times)) + [min(times) - 1, max(times) + 1]


def test_one_cause_is_one_minus_kaplan_meier() -> None:
    rng = random.Random(1)
    for _ in range(50):
        times, causes = random_data(rng, rng.randint(1, 15), 1)
        rows = cumulative_incidence(times, causes, 1)
        km = kaplan_meier(times, causes)
        assert [r.time for r in rows] == [t for t, _ in km]
        for r, (_, S) in zip(rows, km):
            assert r.cif[0] == 1 - S
            assert r.surv == S


def test_incidences_and_survival_sum_to_one() -> None:
    rng = random.Random(2)
    for _ in range(50):
        K = rng.randint(1, 4)
        times, causes = random_data(rng, rng.randint(1, 20), K)
        rows = cumulative_incidence(times, causes, K)
        for t in grid(times):
            assert evaluate(rows, t) + sum(evaluate(rows, t, k) for k in range(1, K + 1)) == 1


def test_one_minus_cause_specific_km_overstates() -> None:
    rng = random.Random(3)
    strict = 0
    for _ in range(50):
        K = rng.randint(2, 3)
        times, causes = random_data(rng, rng.randint(2, 20), K)
        rows = cumulative_incidence(times, causes, K)
        for k in range(1, K + 1):
            km = kaplan_meier(times, [int(c == k) for c in causes])
            for t in grid(times):
                S_k = Fraction(1)
                for u, s in km:
                    if u <= t:
                        S_k = s
                F = evaluate(rows, t, k)
                assert 1 - S_k >= F
                strict += 1 - S_k > F
    assert strict > 0


def test_no_censoring_gives_empirical_proportions() -> None:
    rng = random.Random(4)
    for _ in range(30):
        K = rng.randint(1, 3)
        n = rng.randint(1, 20)
        times, causes = random_data(rng, n, K, censor=0.0)
        rows = cumulative_incidence(times, causes, K)
        for t in grid(times):
            for k in range(1, K + 1):
                assert evaluate(rows, t, k) == Fraction(sum(1 for y, c in zip(times, causes) if y <= t and c == k), n)
            assert evaluate(rows, t) == Fraction(sum(1 for y in times if y > t), n)


def test_multistate_form_equals_cumulative_incidence() -> None:
    rng = random.Random(5)
    for _ in range(40):
        K = rng.randint(1, 3)
        times, causes = random_data(rng, rng.randint(1, 18), K)
        rows = cumulative_incidence(times, causes, K)
        mats = transition_matrices(competing_risks_subjects(times, causes), K + 1)
        assert [t for t, _ in mats] == [r.time for r in rows]
        for (t, P), r in zip(mats, rows):
            assert P[0][0] == r.surv
            assert tuple(P[0][1:]) == r.cif


def illness_death(rng, n, censor):
    """States 0 healthy, 1 ill, 2 dead; integer times so that ties occur."""
    subs = []
    for _ in range(n):
        t, state, moves = 0, 0, []
        while state != 2:
            t += rng.randint(1, 4)
            state = rng.choice([1, 2]) if state == 0 else 2
            moves.append((t, state))
        end = moves[-1][0]
        if censor and rng.random() < censor:
            end = rng.randint(0, end)
            moves = [m for m in moves if m[0] <= end]
        subs.append(Subject(0, tuple(moves), end))
    return subs


def state_at(sub, t):
    s = sub.start
    for u, h in sub.moves:
        if u <= t:
            s = h
    return s


def test_illness_death_without_censoring_is_empirical() -> None:
    rng = random.Random(6)
    for _ in range(20):
        n = rng.randint(1, 15)
        subs = illness_death(rng, n, 0.0)
        for t, P in transition_matrices(subs, 3):
            for h in range(3):
                assert P[0][h] == Fraction(sum(1 for sub in subs if state_at(sub, t) == h), n)


def test_rows_sum_to_one_with_censoring() -> None:
    rng = random.Random(7)
    for _ in range(30):
        subs = illness_death(rng, rng.randint(1, 20), 0.4)
        for _, P in transition_matrices(subs, 3):
            for row in P:
                assert sum(row) == 1
            assert P[2] == [0, 0, 1]
            assert all(v >= 0 for row in P for v in row)


def test_exponential_competing_risks_by_simulation() -> None:
    # Cause-specific hazards 1 and 0.5, censoring rate 0.3; F_1(t) = (2/3)(1 - e^(-1.5 t)).
    rng = random.Random(8)
    n = 2000
    times, causes = [], []
    for _ in range(n):
        a, b, c = rng.expovariate(1.0), rng.expovariate(0.5), rng.expovariate(0.3)
        y = min(a, b, c)
        times.append(y)
        causes.append(0 if y == c else (1 if y == a else 2))
    rows = cumulative_incidence(times, causes, 2)
    for t in [0.2, 0.5, 1.0, 2.0]:
        F1 = (2 / 3) * (1 - math.exp(-1.5 * t))
        F2 = (1 / 3) * (1 - math.exp(-1.5 * t))
        se = math.sqrt(F1 * (1 - F1) / n) * 1.5
        assert abs(float(evaluate(rows, t, 1)) - F1) < 4 * se
        assert abs(float(evaluate(rows, t, 2)) - F2) < 4 * se


def test_hand_example_and_input_checks() -> None:
    times = [1, 2, 2, 3, 4, 5]
    causes = [1, 2, 0, 1, 0, 2]
    rows = cumulative_incidence(times, causes)
    assert [r.time for r in rows] == [1, 2, 3, 5]
    assert [r.cif for r in rows] == [
        (Fraction(1, 6), Fraction(0)),
        (Fraction(1, 6), Fraction(1, 6)),
        (Fraction(7, 18), Fraction(1, 6)),
        (Fraction(7, 18), Fraction(11, 18)),
    ]
    assert [r.surv for r in rows] == [Fraction(5, 6), Fraction(2, 3), Fraction(4, 9), Fraction(0)]
    for bad in [([], []), ([1], [-1]), ([1, 2], [1])]:
        try:
            cumulative_incidence(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("bad input accepted")
