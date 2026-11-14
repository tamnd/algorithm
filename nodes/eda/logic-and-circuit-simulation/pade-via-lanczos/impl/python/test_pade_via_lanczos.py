# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pade-via-lanczos/. The authors are listed in prov/JW00K7.jsonl.

import math
import random
from fractions import Fraction as Fr

import pytest

import sim3dense
from pade_via_lanczos import (
    Breakdown,
    awe,
    exact_moments,
    lu_factor,
    lu_solve,
    lu_solve_transposed,
    model_eval,
    model_moments,
    pvl,
    rational_eval,
    rlc_line,
    transfer,
)


def two_node():
    """1 S from node 1 to ground and from node 1 to node 2, 1 F from each node
    to ground, 1 A into node 1, output node 2: G = [[2, -1], [-1, 1]], C = I."""
    G = [[Fr(2), Fr(-1)], [Fr(-1), Fr(1)]]
    C = [[Fr(1), Fr(0)], [Fr(0), Fr(1)]]
    return G, C, [Fr(1), Fr(0)], [Fr(0), Fr(1)]


def test_hand_example():
    G, C, b, l = two_node()
    assert exact_moments(G, C, b, l, 0, 5) == [1, -3, 8, -21, 55]
    m0, T = pvl(G, C, b, l, Fr(0), 1)
    assert (m0, T) == (1, [[-3]])
    assert model_moments(m0, T, 3) == [1, -3, 9]  # two moments match, the third does not
    m0, T = pvl(G, C, b, l, Fr(0), 2)
    assert T == [[-3, -1], [1, 0]]
    for s in (Fr(0), Fr(1), Fr(-1, 2), Fr(7, 3)):
        assert model_eval(m0, T, 0, s) == 1 / (s * s + 3 * s + 1)  # exact for q = n


def random_circuit(rng, n):
    G = [[Fr(rng.randint(-3, 3)) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] += 3 * n
    C = [[Fr(rng.randint(-2, 2)) for _ in range(n)] for _ in range(n)]
    b = [Fr(rng.randint(-2, 2)) for _ in range(n)]
    l = [Fr(rng.randint(-2, 2)) for _ in range(n)]
    b[0], l[-1] = Fr(1), Fr(1)  # nonzero
    return G, C, b, l


def test_exact_arithmetic_matches_2q_moments():
    rng = random.Random(91)
    short = more = 0
    for _ in range(40):
        n = rng.randint(3, 6)
        G, C, b, l = random_circuit(rng, n)
        s0 = Fr(rng.randint(-1, 2))
        ref = exact_moments(G, C, b, l, s0, 2 * n + 1)
        for q in range(1, n + 1):
            m0, T = pvl(G, C, b, l, s0, q)  # no breakdown occurs with this seed
            got = model_moments(m0, T, 2 * q + 1)
            assert got[: 2 * q] == ref[: 2 * q]
            if q == n:
                assert got[2 * q] == ref[2 * q]  # the full model matches every moment
            else:
                short += 1
                more += got[2 * q] != ref[2 * q]
    assert short == 141 and more == short  # moment 2q is missed in every case


def test_same_model_as_awe_in_exact_arithmetic():
    rng = random.Random(92)
    for _ in range(20):
        n = rng.randint(3, 6)
        G, C, b, l = random_circuit(rng, n)
        for q in range(1, n):
            try:
                m0, T = pvl(G, C, b, l, Fr(0), q)
                num, den = awe(exact_moments(G, C, b, l, 0, 2 * q), q)
            except (Breakdown, sim3dense.SingularMatrixError):
                break
            for sig in (Fr(1, 7), Fr(-2, 5), Fr(3)):
                try:
                    want = rational_eval(num, den, sig)
                except ZeroDivisionError:
                    continue
                assert model_eval(m0, T, 0, sig) == want


def test_q_equal_n_reproduces_the_transfer_function():
    rng = random.Random(93)
    for _ in range(10):
        n = rng.randint(2, 5)
        G, C, b, l = random_circuit(rng, n)
        try:
            m0, T = pvl(G, C, b, l, Fr(0), n)
        except Breakdown:
            continue
        for s in (Fr(1, 3), Fr(2), Fr(-1, 5)):
            Y = [[G[i][j] + s * C[i][j] for j in range(n)] for i in range(n)]
            want = sum(a * x for a, x in zip(l, sim3dense.solve(Y, b)))
            assert model_eval(m0, T, 0, s) == want


def test_breakdown_is_reported():
    G = [[Fr(1), Fr(0)], [Fr(0), Fr(1)]]
    C = [[Fr(1), Fr(1)], [Fr(0), Fr(1)]]
    with pytest.raises(Breakdown):
        pvl(G, C, [Fr(1), Fr(0)], [Fr(0), Fr(1)], Fr(0), 2)  # l^T r = 0


def test_transposed_solve_reuses_the_factors():
    rng = random.Random(94)
    for _ in range(20):
        n = rng.randint(1, 8)
        K = [[Fr(rng.randint(-5, 5)) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            K[i][i] += 11
        w = [Fr(rng.randint(-5, 5)) for _ in range(n)]
        fac = lu_factor(K)
        assert lu_solve(fac, w) == sim3dense.solve(K, w)
        assert lu_solve_transposed(fac, w) == sim3dense.solve(sim3dense.transpose(K), w)


def rc_line(n, r, c, rs, rload):
    N = n + 1
    G = [[0.0] * N for _ in range(N)]
    C = [[0.0] * N for _ in range(N)]
    for k in range(n):
        g = 1 / r
        G[k][k] += g
        G[k + 1][k + 1] += g
        G[k][k + 1] -= g
        G[k + 1][k] -= g
        C[k + 1][k + 1] += c
    G[0][0] += 1 / rs
    G[N - 1][N - 1] += 1 / rload
    b = [0.0] * N
    b[0] = 1.0
    l = [0.0] * N
    l[-1] = 1.0
    return G, C, b, l


def errors(G, C, b, l, s0, fs, qs):
    exact = [transfer(G, C, b, l, 2j * math.pi * f) for f in fs]
    peak = max(abs(h) for h in exact)
    mom = exact_moments(G, C, b, l, s0, 2 * max(qs))
    out = {}
    for q in qs:
        m0, T = pvl(G, C, b, l, s0, q)
        e_pvl = max(abs(model_eval(m0, T, s0, 2j * math.pi * f) - h) for f, h in zip(fs, exact)) / peak
        num, den = awe(mom, q)
        e_awe = max(abs(rational_eval(num, den, 2j * math.pi * f - s0) - h) for f, h in zip(fs, exact)) / peak
        out[q] = (e_pvl, e_awe)
    return out


def test_rc_line_pvl_converges_and_awe_stalls():
    fs = [10 ** (6 + 4 * i / 120) for i in range(121)]
    e = errors(*rc_line(60, 10.0, 10e-15, 50.0, 1e6), 0.0, fs, [2, 4, 8, 12])
    assert e[2][0] == pytest.approx(e[2][1], rel=1e-6)  # the same model while the moments are accurate
    assert e[4][0] < 1e-4 and e[8][0] < 1e-12 and e[12][0] < 1e-12
    assert e[8][1] > 1e-9 and e[12][1] > 1e-9  # explicit moments lose the later directions


def test_rlc_line_with_a_real_expansion_point():
    G, C, b, l = rlc_line(20, 2.0, 1e-9, 1e-12, 25.0, 50.0)
    fs = [1e8 + (3e9 - 1e8) * i / 120 for i in range(121)]
    e = errors(G, C, b, l, 2 * math.pi * 1e9, fs, [20, 30])
    assert e[20][0] < 1e-6 and e[30][0] < 1e-10
    assert e[20][1] > 1e-3
