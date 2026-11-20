# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vector-perturbation-precoding/. The authors are listed in prov/RSA6ZS.jsonl.

import itertools
import math
import random

import cbb
from vector_perturbation_precoding import closest_point, mod_tau, real_form, vp_precode, vp_receive

QPSK = [complex(a, b) for a in (-1, 1) for b in (-1, 1)]
QAM16 = [complex(a, b) for a in (-3, -1, 1, 3) for b in (-3, -1, 1, 3)]


def rand_h(rng: random.Random, k: int, m: int) -> list[list[complex]]:
    return [[cbb.cn(rng, 1.0) for _ in range(m)] for _ in range(k)]


def quad(a: list[list[complex]], u: list[complex]) -> float:
    return cbb.dot(u, cbb.matvec(a, u)).real


def test_example() -> None:
    h = [[1, 2], [0, 1]]
    s = [1 + 1j, -1 - 1j]
    x, l_vec, gamma = vp_precode(h, s, 4.0, 4.0)
    assert l_vec == [-1 - 1j, 0j]
    assert abs(gamma - 4.0) < 1e-12
    assert max(abs(a - b) for a, b in zip(x, [-1 - 1j, -1 - 1j])) < 1e-12
    y = cbb.matvec(h, x)
    assert max(abs(a - b) for a, b in zip(y, [-3 - 3j, -1 - 1j])) < 1e-12
    assert max(abs(vp_receive(v, gamma, 4.0, 4.0) - z) for v, z in zip(y, s)) < 1e-12
    # Zero forcing without the perturbation needs 5 times the power.
    assert abs(cbb.norm2(cbb.matvec(cbb.inv(h), s)) - 20.0) < 1e-12


def test_real_form() -> None:
    rng = random.Random(1)
    a = [[cbb.cn(rng, 1.0) for _ in range(3)] for _ in range(3)]
    a = cbb.matmul(a, cbb.herm(a))
    ar = real_form(a)
    for _ in range(20):
        u = [cbb.cn(rng, 1.0) for _ in range(3)]
        v = [z.real for z in u] + [z.imag for z in u]
        vt = sum(v[i] * ar[i][j] * v[j] for i in range(6) for j in range(6))
        assert abs(vt - quad(a, u)) < 1e-10


def test_search_against_brute_force() -> None:
    # The sphere search is exact over all integer vectors; a box search gives an upper bound.
    # When the search result lies in the box, the two must agree.
    rng = random.Random(2)
    tau = 4.0
    for k, box, trials in [(1, 3, 5), (2, 3, 4), (3, 2, 1)]:
        for _ in range(trials):
            h = rand_h(rng, k, k)
            s = [rng.choice(QPSK) for _ in range(k)]
            a = cbb.inv(cbb.matmul(h, cbb.herm(h)))
            _, l_vec, gamma = vp_precode(h, s, 1.0, tau)
            assert all(abs(z.real) <= box and abs(z.imag) <= box for z in l_vec)
            best = math.inf
            for c in itertools.product(range(-box, box + 1), repeat=2 * k):
                u = [s[i] + tau * complex(c[i], c[i + k]) for i in range(k)]
                best = min(best, quad(a, u))
            assert abs(gamma - best) < 1e-9 * best


def test_closest_point_small_real() -> None:
    # A real 2 by 2 lattice where the answer is known by hand.
    r = [[1.0, 2.0], [0.0, 1.0]]
    # ||R (v + tau l)||^2 with v = (0.4, 0) and tau = 1: l = (-1, ...) checks the coupling.
    lv, val = closest_point(r, [0.4, 0.0], 1.0)
    best = min(
        ((0.4 + a) + 2 * b) ** 2 + b**2 for a in range(-5, 6) for b in range(-5, 6)
    )
    assert abs(val - best) < 1e-12
    assert abs(((0.4 + lv[0]) + 2 * lv[1]) ** 2 + lv[1] ** 2 - best) < 1e-12


def test_power_and_zero_interference() -> None:
    rng = random.Random(3)
    tau = 8.0
    for k, m in [(2, 2), (3, 4), (4, 4), (6, 8)]:
        h = rand_h(rng, k, m)
        s = [rng.choice(QAM16) for _ in range(k)]
        pt = rng.uniform(0.5, 50.0)
        x, l_vec, gamma = vp_precode(h, s, pt, tau)
        assert abs(cbb.norm2(x) - pt) < 1e-9 * pt
        y = cbb.matvec(h, x)
        c = math.sqrt(pt / gamma)
        assert max(abs(y[i] - c * (s[i] + tau * l_vec[i])) for i in range(k)) < 1e-9
        # Without noise, the modulo receiver gives back the data exactly.
        assert max(abs(vp_receive(v, gamma, pt, tau) - z) for v, z in zip(y, s)) < 1e-9


def test_never_worse_than_zero_forcing() -> None:
    rng = random.Random(4)
    ratios = []
    for _ in range(30):
        h = rand_h(rng, 4, 4)
        s = [rng.choice(QPSK) for _ in range(4)]
        a = cbb.inv(cbb.matmul(h, cbb.herm(h)))
        _, _, gamma = vp_precode(h, s, 1.0, 4.0)
        gzf = quad(a, s)
        assert gamma <= gzf + 1e-9 * gzf
        ratios.append(gzf / gamma)
    # On K = M = 4 Rayleigh channels the power saving is large on average.
    assert sum(ratios) / len(ratios) > 2.0


def test_mod_tau() -> None:
    assert mod_tau(3 + 5j, 4.0) == -1 + 1j
    assert mod_tau(-2 + 1.999j, 4.0) == -2 + 1.999j
    assert mod_tau(2 + 0j, 4.0) == -2 + 0j
    for z in QAM16:
        assert mod_tau(z + 8 * (2 - 3j), 8.0) == z
