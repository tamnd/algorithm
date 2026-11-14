# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/breslow-estimator/. The authors are listed in prov/NMKKND.jsonl.

import math
import random
from fractions import Fraction

from breslow_estimator import breslow, cox_snell_residuals, evaluate, risk_scores, survival

# Gehan (1965) leukemia remission data: 6-MP arm, then placebo arm (x = 1).
MP_T = [6, 6, 6, 6, 7, 9, 10, 10, 11, 13, 16, 17, 19, 20, 22, 23, 25, 32, 32, 34, 35]
MP_D = [1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0]
PL_T = [1, 1, 2, 2, 3, 4, 4, 5, 5, 8, 8, 8, 8, 11, 11, 12, 12, 15, 17, 22, 23]
T = MP_T + PL_T
D = MP_D + [1] * 21
X = [0] * 21 + [1] * 21


def random_data(rng, n, ties=True):
    times = [rng.randint(1, 8) if ties else rng.random() for _ in range(n)]
    events = [1 if rng.random() < 0.7 else 0 for _ in range(n)]
    return times, events


def nelson_aalen(times, events):
    out = []
    H = Fraction(0)
    for t in sorted(set(y for y, e in zip(times, events) if e)):
        d = sum(1 for y, e in zip(times, events) if e and y == t)
        n = sum(1 for y in times if y >= t)
        H += Fraction(d, n)
        out.append((t, H))
    return out


def direct(times, events, scores, ties):
    """H0-hat by a fresh sum over the risk set at each event time, O(n) per time."""
    out, H = [], Fraction(0)
    for t in sorted(set(y for y, e in zip(times, events) if e)):
        S = sum(Fraction(w) for y, w in zip(times, scores) if y >= t)
        dead = [Fraction(w) for y, e, w in zip(times, events, scores) if e and y == t]
        d, Dsum = len(dead), sum(dead)
        if ties == "breslow":
            H += Fraction(d) / S
        else:
            H += sum(1 / (S - Fraction(r, d) * Dsum) for r in range(d))
        out.append((t, H))
    return out


def full_loglik(times, events, scores, jumps):
    """Log full likelihood with a baseline hazard that jumps only at event times.

    sum_j d_j log(lam_j) + sum_i delta_i log(w_i) - sum_i w_i Lambda0(y_i).
    """
    ts = sorted(jumps)
    total = 0.0
    for t in ts:
        d = sum(1 for y, e in zip(times, events) if e and y == t)
        total += d * math.log(jumps[t])
    for y, e, w in zip(times, events, scores):
        if e:
            total += math.log(w)
        total -= w * sum(jumps[t] for t in ts if t <= y)
    return total


def test_beta_zero_gives_nelson_aalen_exactly() -> None:
    rng = random.Random(1)
    for _ in range(40):
        times, events = random_data(rng, rng.randint(1, 15))
        if not any(events):
            continue
        steps = breslow(times, events, [1] * len(times))
        assert [(s.time, s.cum_hazard) for s in steps] == nelson_aalen(times, events)
        # Efron at beta = 0 does not reduce to Nelson-Aalen when there are ties.
        efron = breslow(times, events, [1] * len(times), "efron")
        for a, b in zip(steps, efron):
            assert b.increment >= a.increment
            assert (b.increment == a.increment) == (a.events == 1)


def test_matches_direct_summation_with_rational_scores() -> None:
    rng = random.Random(2)
    for _ in range(40):
        n = rng.randint(1, 14)
        times, events = random_data(rng, n)
        if not any(events):
            continue
        scores = [Fraction(rng.randint(1, 9), rng.randint(1, 5)) for _ in range(n)]
        for ties in ("breslow", "efron"):
            steps = breslow(times, events, scores, ties)
            assert [(s.time, s.cum_hazard) for s in steps] == direct(times, events, scores, ties)


def test_efron_increment_formula_by_hand() -> None:
    # Three subjects at risk with scores 1, 2, 3; the last two die together.
    steps = breslow([1, 2, 2], [0, 1, 1], [1, 2, 3], "efron")
    S, Dsum = 5, 5
    assert steps[0].increment == Fraction(1, S) + 1 / (S - Fraction(1, 2) * Dsum)
    assert steps[0].increment == Fraction(1, 5) + Fraction(2, 5)
    assert breslow([1, 2, 2], [0, 1, 1], [1, 2, 3])[0].increment == Fraction(2, 5)


def test_cox_snell_residuals_sum_to_number_of_events_for_any_scores() -> None:
    rng = random.Random(3)
    for _ in range(40):
        n = rng.randint(1, 14)
        times, events = random_data(rng, n)
        if not any(events):
            continue
        scores = [Fraction(rng.randint(1, 20), rng.randint(1, 7)) for _ in range(n)]
        steps = breslow(times, events, scores)
        r = cox_snell_residuals(times, steps, scores)
        assert sum(r) == sum(events)
        # Hence the martingale residuals delta_i - r_i sum to 0.
        assert sum(e - ri for e, ri in zip(events, r)) == 0


def test_profile_maximum_of_the_full_likelihood() -> None:
    rng = random.Random(4)
    for _ in range(20):
        n = rng.randint(2, 12)
        times, events = random_data(rng, n)
        if not any(events):
            continue
        scores = [Fraction(rng.randint(1, 9), rng.randint(1, 4)) for _ in range(n)]
        steps = breslow(times, events, scores)
        # The derivative d_j / lam_j - sum_{y_i >= t_j} w_i is exactly 0 at every jump.
        for s in steps:
            at_risk = sum(w for y, w in zip(times, scores) if y >= s.time)
            assert Fraction(s.events) / s.increment - at_risk == 0
        jumps = {s.time: float(s.increment) for s in steps}
        w = [float(v) for v in scores]
        best = full_loglik(times, events, w, jumps)
        for _ in range(10):
            other = {t: lam * math.exp(rng.uniform(-0.3, 0.3)) for t, lam in jumps.items()}
            assert full_loglik(times, events, w, other) < best + 1e-12


def test_variance_term_and_step_function() -> None:
    steps = breslow([1, 2, 2, 3, 5], [1, 1, 0, 1, 0], [1, 1, 1, 1, 1])
    assert [s.cum_hazard for s in steps] == [Fraction(1, 5), Fraction(1, 5) + Fraction(1, 4), Fraction(1, 5) + Fraction(1, 4) + Fraction(1, 2)]
    assert steps[-1].var == Fraction(1, 25) + Fraction(1, 16) + Fraction(1, 4)
    assert evaluate(steps, 0.5) == 0
    assert evaluate(steps, 2.5) == Fraction(9, 20)
    assert evaluate(steps, 100) == Fraction(19, 20)
    assert abs(survival(steps, 2, 2.0) - math.exp(-0.9)) < 1e-15


def _cox_fit_one_covariate(times, events, x):
    """Newton on the Breslow log partial likelihood for one covariate."""
    b = 0.0
    for _ in range(50):
        U = I = 0.0
        for t in sorted(set(y for y, e in zip(times, events) if e)):
            S0 = S1 = S2 = 0.0
            for y, xi in zip(times, x):
                if y >= t:
                    w = math.exp(b * xi)
                    S0 += w
                    S1 += w * xi
                    S2 += w * xi * xi
            dead = [xi for y, e, xi in zip(times, events, x) if e and y == t]
            U += sum(dead) - len(dead) * S1 / S0
            I += len(dead) * (S2 / S0 - (S1 / S0) ** 2)
        step = U / I
        b += step
        if abs(step) < 1e-13:
            break
    return b


def test_gehan_leukemia_baseline() -> None:
    b = _cox_fit_one_covariate(T, D, X)
    assert abs(b - 1.509191) < 1e-5
    w = risk_scores([[x] for x in X], [b])
    steps = breslow(T, D, w)
    assert len(steps) == 17
    assert sum(s.events for s in steps) == 30
    # Baseline (6-MP arm) at the first event time: 2 / (21 + 21 e^b).
    assert abs(steps[0].cum_hazard - 2 / (21 + 21 * math.exp(b))) < 1e-15
    assert abs(sum(cox_snell_residuals(T, steps, w)) - 30) < 1e-11
    # The fitted survival at t = 10 for each arm.
    s0 = survival(steps, 10, 1.0)
    s1 = survival(steps, 10, math.exp(b))
    assert abs(s1 - s0 ** math.exp(b)) < 1e-14
    assert 0.0 < s1 < s0 < 1.0


def test_float_and_fraction_agree_and_input_checks() -> None:
    rng = random.Random(5)
    times, events = random_data(rng, 30, ties=False)
    events[0] = 1
    scores = [rng.uniform(0.2, 5.0) for _ in range(30)]
    a = breslow(times, events, scores)
    b = breslow(times, events, [Fraction(s) for s in scores])
    for u, v in zip(a, b):
        assert abs(u.cum_hazard - float(v.cum_hazard)) < 1e-12 * max(1.0, float(v.cum_hazard))
    for bad in [([], [], []), ([1], [2], [1]), ([1], [1], [0]), ([1, 2], [1], [1, 1])]:
        try:
            breslow(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("bad input accepted")
