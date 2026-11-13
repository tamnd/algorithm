# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-principal-ideal-algorithm/. The authors are listed in prov/M8TEVB.jsonl.

import math
import random

from quantum_principal_ideal_algorithm import (
    canon,
    circuit_distribution,
    closed_form_distribution,
    cycle_around,
    distance_candidates,
    g_values,
    is_ideal,
    is_reduced,
    is_square,
    multiply,
    principal_cycle,
    principal_near,
    quantum_principal_ideal,
    reduce_ideal,
    reduced_power,
    regulator,
    step,
)
from qsim import sample

TOL = 1e-9
# class numbers of Q(sqrt(D)) for squarefree D = 2, 3 mod 4, from standard tables
CLASS_NUMBER = {3: 1, 6: 1, 7: 1, 10: 2, 11: 1, 14: 1, 15: 2, 19: 1, 22: 1, 23: 1, 26: 2, 30: 2, 31: 1, 34: 2, 46: 1, 79: 3, 82: 4, 94: 1}
# non-principal reduced ideals (P, Q) and the order of their class
ORDER = {(10, (0, 2)): 2, (15, (1, 2)): 2, (26, (0, 2)): 2, (30, (0, 2)): 2, (79, (1, 3)): 3, (79, (2, 3)): 3}


def reduced_ideals(D):
    s = math.isqrt(D)
    return sorted({(canon(D, P, Q) % Q, Q) for Q in range(1, 2 * s + 1) for P in range(Q) if is_ideal(D, P, Q) and is_reduced(D, P, Q)})


def scale(D):
    return round(4.3 / regulator(D), 3)


def brute_force_unit(D):
    """The least x + y sqrt(D) > 1 with x^2 - D y^2 = +-1."""
    y = 1
    while not (is_square(D * y * y + 1) or is_square(D * y * y - 1)):
        y += 1
    x = math.isqrt(D * y * y + 1) if is_square(D * y * y + 1) else math.isqrt(D * y * y - 1)
    return x, y


def brute_force_generator(D, I):
    """A generator x + y sqrt(D) of [Q, P + sqrt(D)] with 1 <= x + y sqrt(D) < eps, or None, by search over x^2 - D y^2 = +-Q."""
    P, Q = I
    ex, ey = brute_force_unit(D)
    eps = ex + ey * math.sqrt(D)
    best = None
    Y = math.ceil((eps + Q) / (2 * math.sqrt(D))) + 1  # |y| = |theta - theta'|/(2 sqrt(D)) with |theta'| = Q/theta <= Q
    for y in range(-Y, Y + 1):
        for n in (D * y * y + Q, D * y * y - Q):
            if n >= 0 and is_square(n):
                x = math.isqrt(n)
                for xx in (x, -x):
                    v = xx + y * math.sqrt(D)
                    if (xx - y * P) % Q == 0 and 1 - TOL <= v < eps - TOL and (best is None or v < best[0] + best[1] * math.sqrt(D)):
                        best = (xx, y)
    return best


def F(D, N, y):
    """The principal function: the reduced principal ideal with the largest distance <= y/N, and the offset."""
    R = regulator(D)
    best = None
    for Q, P, _, _, d in principal_cycle(D):
        dd = d + math.floor((y / N + 1e-9 - d) / R) * R
        if best is None or dd > best[2]:
            best = (Q, P, dd)
    return best[0], best[1], math.floor(y - N * best[2] + 1e-9)


def test_cycles_give_class_numbers_and_the_regulator():
    for D, h in CLASS_NUMBER.items():
        red, seen, cycles = reduced_ideals(D), set(), 0
        for I in red:
            if I in seen:
                continue
            cycles += 1
            P, Q = I
            while (P % Q, Q) not in seen:
                seen.add((P % Q, Q))
                P, Q, _ = step(D, P, Q)
        assert seen == set(red) and cycles == h
        x, y = brute_force_unit(D)
        assert abs(regulator(D) - math.log(x + y * math.sqrt(D))) < TOL


def test_multiply_gives_the_product_ideal():
    rng = random.Random(1)
    for D in [7, 10, 15, 19, 79, 82]:
        ideals = [(P, Q) for Q in range(1, 40) for P in range(Q) if is_ideal(D, P, Q)]
        for _ in range(150):
            (P1, Q1), (P2, Q2) = rng.choice(ideals), rng.choice(ideals)
            P, Q, w = multiply(D, (P1, Q1), (P2, Q2))
            assert is_ideal(D, P, Q) and w * w * Q == Q1 * Q2  # the index of w [Q, P + sqrt(D)] is the norm Q1 Q2
            for u, v in [(Q1 * Q2, 0), (Q1 * P2, Q1), (Q2 * P1, Q2), (P1 * P2 + D, P1 + P2)]:
                assert v % w == 0 and (u - (v // w) * w * P) % (w * Q) == 0  # each product lies in w [Q, P + sqrt(D)]


def test_reduction_and_distances_match_brute_force_generators():
    for D in [7, 14, 19, 23, 31, 46]:
        R = regulator(D)
        cyc = principal_cycle(D)
        for Q in range(1, 60):
            for P in range(Q):
                if not is_ideal(D, P, Q):
                    continue
                Pr, Qr, e = reduce_ideal(D, P, Q)
                assert is_reduced(D, Pr, Qr)
                gen = brute_force_generator(D, (P, Q))
                assert gen is not None  # the class number is 1
                delta = math.log(abs(gen[0] + gen[1] * math.sqrt(D))) + e
                J = [c for c in cyc if (c[1], c[0]) == (Pr % Qr, Qr)]
                assert len(J) == 1 and abs((J[0][4] - delta + R / 2) % R - R / 2) < 1e-9


def test_g_is_the_principal_function_shifted_by_the_distance():
    for D in [7, 14, 19, 23]:
        N = scale(D)
        for Q, P, _, _, d in principal_cycle(D):
            vals = g_values(D, (P, Q), N, 16, 32)
            assert all(vals[a][k] == F(D, N, k + a * N * d) for a in range(16) for k in range(32))
            assert len({v for row in vals for v in row}) <= 8


def test_rows_of_g_follow_the_class_of_I():
    for (D, I), m in ORDER.items():
        cycle_of = {}
        for J in reduced_ideals(D):
            if J in cycle_of:
                continue
            P, Q = J
            while (P % Q, Q) not in cycle_of:
                cycle_of[(P % Q, Q)] = J
                P, Q, _ = step(D, P, Q)
        vals = g_values(D, I, scale(D), 8, 32)
        cls = []
        for row in vals:
            cs = {cycle_of[(v[1], v[0])] for v in row}
            assert len(cs) == 1  # each row stays on one cycle, the class of I^a
            cls.append(cs.pop())
        assert all((cls[a] == cls[b]) == ((a - b) % m == 0) for a in range(8) for b in range(8))
        P, Q, _ = reduced_power(D, I, m)
        assert (Q, P % Q) in {(c[0], c[1]) for c in principal_cycle(D)}  # I^m is principal
        assert brute_force_generator(D, I) is None and brute_force_generator(D, (P % Q, Q)) is not None


def test_state_vector_matches_closed_form():
    for D, I, sizes in [(7, (1, 2), (4, 5, 3)), (19, (2, 5), (4, 5, 3)), (10, (0, 2), (3, 5, 4))]:
        assert sum(sizes) <= 12
        N = scale(D) if D != 7 else 1.5
        sv = circuit_distribution(D, I, N, *sizes)
        cf = closed_form_distribution(D, I, N, 1 << sizes[0], 1 << sizes[1])
        assert abs(sum(sv.values()) - 1) < TOL
        assert max(abs(sv.get(k, 0.0) - cf.get(k, 0.0)) for k in set(sv) | set(cf)) < TOL


def test_samples_locate_the_distance_far_better_than_guessing():
    # P(win): a candidate window of the sample holds the true distance. cover: the expected share of [0, R) the windows cover,
    # which is the success rate of windows placed at random.
    for D in [7, 14, 19, 23]:
        N, R = scale(D), regulator(D)
        for Q, P, _, _, d in principal_cycle(D):
            dist = closed_form_distribution(D, (P, Q), N)
            win = cover = 0.0
            for (b, c), p in dist.items():
                cands = distance_candidates(b, c, 16, 32, N, R)
                win += p * any(abs((d - t + R / 2) % R - R / 2) <= w for t, w in cands)
                cover += p * sum(2 * w for _, w in cands) / R
            assert win >= 0.3 and cover <= 0.16 and win >= 2.5 * cover


def test_quantum_principal_ideal_matches_brute_force():
    rng = random.Random(7)
    for D in [7, 10, 14, 15, 19, 23, 26, 30, 79]:
        N, R = scale(D), regulator(D)
        ideals = reduced_ideals(D)
        if D == 79:
            ideals = ideals[::3]
        for I in ideals:
            ref = brute_force_generator(D, I)
            dist = closed_form_distribution(D, I, N)
            for _ in range(3):
                gen, delta, rounds = quantum_principal_ideal(D, I, N, rng, dist=dist)
                assert (gen is None) == (ref is None)
                if gen is None:
                    assert rounds == 30
                    continue
                x, y = gen
                assert abs(x * x - D * y * y) == I[1] and (x - y * I[0]) % I[1] == 0  # x + y sqrt(D) lies in I with norm +-Q
                assert gen == ref and abs(delta - math.log(x + y * math.sqrt(D))) < TOL and 0 <= delta < R


def test_worked_example_7():
    D, I, N = 7, (1, 2), 1.5
    R = regulator(D)
    assert [(Q, P, x, y) for Q, P, x, y, _ in principal_cycle(D)] == [(1, 0, 1, 0), (3, 2, 2, 1), (2, 1, 3, 1), (3, 1, 5, 2)]
    assert [reduced_power(D, I, a)[:2] for a in range(3)] == [(2, 1), (1, 2), (2, 1)]
    assert abs(reduced_power(D, I, 2)[2] + math.log(2)) < TOL  # I^2 = (2)(8 + 3 sqrt(7)), reduced to (1) by the factor 1/2
    vals = g_values(D, I, N, 16, 32)
    assert vals[0][:6] == [(1, 0, 0), (1, 0, 1), (1, 0, 2), (2, 1, 0), (3, 1, 0), (1, 0, 0)]
    assert vals[1][:6] == [(2, 1, 0), (3, 1, 0), (1, 0, 0), (1, 0, 1), (3, 2, 0), (2, 1, 0)]
    dist = circuit_distribution(D, I, N)
    assert abs(dist[(0, 0)] - 0.1958) < 1e-4 and abs(dist[(10, 8)] - 0.1261) < 1e-4 and abs(dist[(6, 24)] - 0.1261) < 1e-4
    rng = random.Random(1)
    assert [sample(dist, rng) for _ in range(2)] == [(0, 0), (12, 16)]
    assert distance_candidates(0, 0, 16, 32, N, R) == []
    cands = distance_candidates(12, 16, 16, 32, N, R)
    assert [round(t, 4) for t, _ in cands] == [0.3333, 1.6667] and all(abs(w - 1 / 12) < TOL for _, w in cands)
    assert principal_near(D, cands[0][0], cands[0][1], principal_cycle(D), R) == []
    assert [(J[0], J[1]) for J in principal_near(D, cands[1][0], cands[1][1], principal_cycle(D), R)] == [(2, 1)]
    assert distance_candidates(10, 8, 16, 32, N, R) == distance_candidates(6, 24, 16, 32, N, R) == [(2 * 32 / 24 * 10 / 16, 32 / 192)]
    gen, delta, rounds = quantum_principal_ideal(D, I, N, random.Random(1), dist=dist)
    assert gen == (3, 1) and rounds == 2 and abs(delta - math.log(3 + math.sqrt(7))) < TOL
    walk = cycle_around(D, 2, 1, 0.0, 0.0, 2.0)
    assert [(Q, P) for Q, P, _ in walk] == [(1, 0), (3, 2), (2, 1), (3, 1)]
