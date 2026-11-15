# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/eigensystem-realization-algorithm/. The authors are listed in prov/8Q2BQ4.jsonl.

import cmath
import math
import random

from ctlmat import charpoly, mul, polyroots, transpose
from eigensystem_realization_algorithm import continuous_poles, era, hankel, jacobi_svd, markov_parameters


def _close(a, b, tol):
    return all(abs(x - y) <= tol for ra, rb in zip(a, b) for x, y in zip(ra, rb))


def _modal_system(h):
    # two lightly damped modes: (omega, zeta) = (2, 0.05) and (5, 0.02), period h
    A = [[0.0] * 4 for _ in range(4)]
    for b, (omega, zeta) in enumerate([(2.0, 0.05), (5.0, 0.02)]):
        z = cmath.exp(complex(-zeta * omega, omega * math.sqrt(1 - zeta * zeta)) * h)
        A[2 * b][2 * b], A[2 * b][2 * b + 1] = z.real, z.imag
        A[2 * b + 1][2 * b], A[2 * b + 1][2 * b + 1] = -z.imag, z.real
    B = [[1.0], [0.0], [1.0], [0.0]]
    C = [[1.0, 0.0, 0.5, 0.0], [0.0, 1.0, 0.0, 1.0]]
    D = [[0.0], [0.0]]
    return A, B, C, D


def _max_eig_error(A, A0):
    eig = polyroots(charpoly(A))
    true = polyroots(charpoly(A0))
    return max(min(abs(e - t) for t in true) for e in eig)


def test_svd_known_factors():
    U, s, V = jacobi_svd([[3.0, 0.0], [4.0, 5.0]])
    assert abs(s[0] - 3 * math.sqrt(5)) < 1e-12
    assert abs(s[1] - math.sqrt(5)) < 1e-12
    back = mul(mul(U, [[s[0], 0.0], [0.0, s[1]]]), transpose(V))
    assert _close(back, [[3.0, 0.0], [4.0, 5.0]], 1e-12)


def test_svd_random_matrices():
    rng = random.Random(3)
    for _ in range(20):
        r, c = rng.randint(1, 7), rng.randint(1, 7)
        a = [[rng.uniform(-1, 1) for _ in range(c)] for _ in range(r)]
        U, s, V = jacobi_svd(a)
        k = min(r, c)
        assert all(s[i] >= s[i + 1] for i in range(k - 1))
        S = [[s[i] if i == j else 0.0 for j in range(k)] for i in range(k)]
        assert _close(mul(mul(U, S), transpose(V)), a, 1e-12)
        eye = [[1.0 if i == j else 0.0 for j in range(k)] for i in range(k)]
        assert _close(mul(transpose(U), U), eye, 1e-12)
        assert _close(mul(transpose(V), V), eye, 1e-12)


def test_exact_data_recovers_the_system():
    h = 0.1
    A0, B0, C0, D0 = _modal_system(h)
    N = 10
    hk = markov_parameters(A0, B0, C0, D0, 2 * N)
    A, B, C, D, s = era(hk, N)
    # the order is chosen by the singular values: four are nonzero
    assert len(A) == 4
    assert s[4] < 1e-12 * s[0]
    far = markov_parameters(A, B, C, D, 3 * N)
    true = markov_parameters(A0, B0, C0, D0, 3 * N)
    for k in range(3 * N + 1):
        assert _close(far[k], true[k], 1e-10)
    assert _max_eig_error(A, A0) < 1e-10
    # modal parameters from s = ln(lambda) / h
    poles = continuous_poles(polyroots(charpoly(A)), h)
    pairs = sorted((abs(z), -z.real / abs(z)) for z in poles if z.imag > 0)
    assert abs(pairs[0][0] - 2.0) < 1e-9 and abs(pairs[0][1] - 0.05) < 1e-9
    assert abs(pairs[1][0] - 5.0) < 1e-9 and abs(pairs[1][1] - 0.02) < 1e-9


def test_result_is_balanced():
    A0, B0, C0, D0 = _modal_system(0.1)
    N = 10
    hk = markov_parameters(A0, B0, C0, D0, 2 * N)
    A, B, C, D, s = era(hk, N)
    n = len(A)
    obs = []
    ctr_blocks = []
    for k in range(N):
        Ak = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
        for _ in range(k):
            Ak = mul(Ak, A)
        obs.extend(mul(C, Ak))
        ctr_blocks.append(mul(Ak, B))
    ctr = [sum((blk[i] for blk in ctr_blocks), []) for i in range(n)]
    sigma = [[s[i] if i == j else 0.0 for j in range(n)] for i in range(n)]
    assert _close(mul(transpose(obs), obs), sigma, 1e-9)
    assert _close(mul(ctr, transpose(ctr)), sigma, 1e-9)


def test_noisy_data_gives_close_eigenvalues():
    # measurement: noise with standard deviation 0.01 on every Markov parameter
    A0, B0, C0, D0 = _modal_system(0.1)
    N = 10
    hk = markov_parameters(A0, B0, C0, D0, 2 * N)
    for seed in range(1, 6):
        rng = random.Random(seed)
        hn = [[[v + (rng.gauss(0.0, 0.01) if k > 0 else 0.0) for v in row] for row in hk[k]]
              for k in range(len(hk))]
        A, B, C, D, s = era(hn, N, n=4)
        # a clear gap after the fourth singular value
        assert s[3] > 10 * s[4]
        assert _max_eig_error(A, A0) < 0.02


def test_order_above_rank_is_rejected():
    hk = markov_parameters([[0.5]], [[1.0]], [[1.0]], [[0.0]], 6)
    try:
        era(hk, 3, n=2)
    except ValueError:
        return
    assert False, "an order above the rank of H must be rejected"


def test_hankel_layout():
    hk = [[[float(k)]] for k in range(7)]
    assert hankel(hk, 3, 3) == [[1.0, 2.0, 3.0], [2.0, 3.0, 4.0], [3.0, 4.0, 5.0]]
    assert hankel(hk, 3, 3, shift=1)[0] == [2.0, 3.0, 4.0]
