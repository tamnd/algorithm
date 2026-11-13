# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hallgren-pell-algorithm/. The authors are listed in prov/6ZS7YE.jsonl.

import math
import random
from fractions import Fraction

from hallgren_pell_algorithm import (
    brute_force_pell,
    circuit_distribution,
    closed_form_distribution,
    convergents,
    f_values,
    fundamental_unit,
    hallgren_pell,
    ideal_walk,
    is_square,
    label_codes,
    regulator_candidates,
)
from qsim import sample

TOL = 1e-9
Q = 256
# fundamental solutions of x^2 - D y^2 = 1 from standard tables, for D where brute force is slow
TABLE = {61: (1766319049, 226153980), 94: (2143295, 221064), 109: (158070671986249, 15140424455100)}


def scale_for(D):
    """N with N R = 8.5, so the 4-qubit target register holds every value of f_N."""
    return round(8.5 / fundamental_unit(D)[2], 3)


def pell_from_unit(D):
    x, y, _ = fundamental_unit(D)
    return (x * x + D * y * y, 2 * x * y) if x * x - D * y * y == -1 else (x, y)


def test_unit_from_the_cycle_matches_brute_force_and_tables():
    for D in range(2, 61):
        if not is_square(D):
            assert pell_from_unit(D) == brute_force_pell(D)
    for D, sol in TABLE.items():
        assert pell_from_unit(D) == sol


def test_walk_norms_distances_and_period():
    for D in [2, 3, 7, 13, 19, 31, 46]:
        x, y, R = fundamental_unit(D)
        walk = ideal_walk(D)
        items = [next(walk) for _ in range(40)]
        period = next(k for k in range(1, 40) if items[k][0] == 1)
        for k, (Qk, Pk, xk, yk, dk) in enumerate(items):
            assert xk * xk - D * yk * yk == (-1) ** k * Qk  # theta_k has norm (-1)^k Q_k
            assert (Qk == 1) == (k % period == 0)  # the ideal (1) only at multiples of the period
            if k + period < 40:
                assert items[k + period][:2] == (Qk, Pk)
                assert abs(items[k + period][4] - dk - R) < 1e-9
        assert all(items[k][4] < items[k + 1][4] for k in range(39))
        assert (items[period][2], items[period][3]) == (x, y)


def test_f_is_weakly_periodic():
    for D in [2, 7, 13, 46]:
        N = scale_for(D)
        S = N * fundamental_unit(D)[2]
        vals = f_values(D, N, Q)
        level = {}
        for k, v in enumerate(vals):
            level.setdefault(v, []).append(k)
        assert len(level) <= 16
        for ks in level.values():
            us = []
            for k in ks:
                u = round((k - ks[0]) / S)
                assert abs(k - ks[0] - u * S) < 1
                us.append(u)
            assert len(us) == len(set(us))  # at most one point of each level set per period


def test_state_vector_matches_closed_form():
    for D, N in [(7, 3.0), (2, scale_for(2)), (13, scale_for(13)), (46, scale_for(46))]:
        sv = circuit_distribution(D, N)
        cf = closed_form_distribution(D, N, Q)
        assert abs(sum(sv.values()) - 1) < TOL
        assert max(abs(sv.get(c, 0.0) - cf[c]) for c in cf) < TOL


def test_outcomes_concentrate_near_multiples_of_q_over_S():
    for D in [2, 7, 13, 46, 94]:
        N = scale_for(D)
        S = N * fundamental_unit(D)[2]
        cf = closed_form_distribution(D, N, Q)
        near = sum(p for c, p in cf.items() if any(abs(c - j * Q / S) <= 0.5 for j in range(1, int(S) + 1)))
        assert near > 0.2


def test_convergent_step_recovers_R_from_two_good_samples():
    # if |c_i - j_i q/S| <= 1 with gcd(j1, j2) = 1, 1 <= j_i <= J and q > (4J + 1) S, then j1/j2 is a
    # convergent of c1/c2 and the estimate j1 q/(N c1) is within 1/N of R
    for D in [7, 46]:
        N = scale_for(D)
        R = fundamental_unit(D)[2]
        S = N * R
        J = int((Q / S - 1) / 4)
        assert Q > (4 * J + 1) * S
        for j1 in range(1, J + 1):
            for j2 in range(1, J + 1):
                if math.gcd(j1, j2) != 1:
                    continue
                for c1 in range(math.ceil(j1 * Q / S - 1), math.floor(j1 * Q / S + 1) + 1):
                    for c2 in range(math.ceil(j2 * Q / S - 1), math.floor(j2 * Q / S + 1) + 1):
                        assert Fraction(j1, j2) in convergents(c1, c2)
                        t = j1 * Q / (N * c1)
                        assert abs(t - R) <= 1 / N
                        assert any(abs(u - R) <= 1 / N for u in regulator_candidates(c1, c2, Q, N, 10 * R))


def test_hallgren_pell_matches_brute_force_and_tables():
    rng = random.Random(7)
    for D in [2, 3, 5, 6, 7, 10, 11, 13, 14, 15, 19, 22, 29, 31, 46, 61, 94]:
        N = scale_for(D)
        _, _, R = fundamental_unit(D)
        ref = TABLE.get(D) or brute_force_pell(D)
        dist = closed_form_distribution(D, N, Q)
        for _ in range(20):
            sol, Rh, rounds = hallgren_pell(D, N, rng, dist=dist)
            assert sol == ref and sol[0] ** 2 - D * sol[1] ** 2 == 1
            assert abs(Rh - R) < 1e-12 and rounds <= 60


def test_other_scales():
    rng = random.Random(3)
    for D, N in [(7, 1.5), (7, 2.0), (13, 2.0)]:
        dist = closed_form_distribution(D, N, Q)
        for _ in range(20):
            sol, _, _ = hallgren_pell(D, N, rng, dist=dist)
            assert sol == brute_force_pell(D)


def test_worked_example_7():
    D, N = 7, 3.0
    assert [(Qk, Pk, xk, yk) for Qk, Pk, xk, yk, _ in [next(w) for w in [ideal_walk(7)] for _ in range(5)]] == [
        (1, 0, 1, 0),
        (3, 2, 2, 1),
        (2, 1, 3, 1),
        (3, 1, 5, 2),
        (1, 0, 8, 3),
    ]
    vals = f_values(D, N, Q)
    assert vals[:10] == [(1, 0, 0), (1, 0, 1), (1, 0, 2), (1, 0, 3), (1, 0, 4), (3, 2, 0), (2, 1, 0), (3, 1, 0), (3, 1, 1), (1, 0, 0)]
    assert len(label_codes(vals)) == 10
    dist = circuit_distribution(D, N)
    assert abs(dist[0] - 0.1076) < 1e-4 and abs(dist[31] - 0.0918) < 1e-4
    rng = random.Random(1)
    assert (sample(dist, rng), sample(dist, rng)) == (31, 195)
    assert convergents(31, 195) == [Fraction(0), Fraction(1, 6), Fraction(3, 19), Fraction(7, 44), Fraction(31, 195)]
    B = math.sqrt(Q / 3) / N
    ts = regulator_candidates(31, 195, Q, N, B + 1 / N)
    assert len(ts) == 1 and abs(ts[0] - 256 / 93) < 1e-12
    sol, R, rounds = hallgren_pell(D, N, random.Random(1), dist=dist)
    assert sol == (8, 3) and rounds == 1 and abs(R - math.log(8 + 3 * math.sqrt(7))) < 1e-12
