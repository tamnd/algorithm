# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/block-diagonalization/. The authors are listed in prov/VCA1WD.jsonl.

import math
import random

import cbb
from block_diagonalization import bd_precoder, null_space, rate_from_gains, sum_rate


def rand_h(rng: random.Random, n: int, m: int) -> list[list[complex]]:
    return [[cbb.cn(rng, 1.0) for _ in range(m)] for _ in range(n)]


def max_abs(a: list[list[complex]]) -> float:
    return max((abs(x) for row in a for x in row), default=0.0)


EXAMPLE = [[[1, 0, 0], [0, 1, 0]], [[1, 1, 1]]]


def test_example() -> None:
    w, u, s, p = bd_precoder(EXAMPLE, 3.0, 1.0)
    assert abs(s[0][0] - 1.0) < 1e-12 and abs(s[0][1] - 1 / math.sqrt(3)) < 1e-12
    assert abs(s[1][0] - 1.0) < 1e-12
    assert abs(p[0][0] - 1.5) < 1e-12 and abs(p[0][1]) < 1e-12 and abs(p[1][0] - 1.5) < 1e-12
    assert abs(rate_from_gains(s, p, 1.0) - 2 * math.log2(2.5)) < 1e-12
    assert abs(sum_rate(EXAMPLE, w, 1.0) - 2 * math.log2(2.5)) < 1e-10


def test_zero_interference_and_power() -> None:
    rng = random.Random(1)
    for m, sizes in [(4, (2, 2)), (6, (1, 2, 3)), (8, (2, 2, 2, 2)), (5, (2, 1))]:
        hs = [rand_h(rng, n, m) for n in sizes]
        pt = rng.uniform(0.5, 50.0)
        w, _, _, _ = bd_precoder(hs, pt, 1.0)
        assert abs(sum(cbb.norm2(wk) for wk in w if wk[0]) - pt) < 1e-9 * pt
        for j, hj in enumerate(hs):
            for k, wk in enumerate(w):
                if j != k and wk[0]:
                    assert max_abs(cbb.matmul(hj, wk)) < 1e-9


def test_null_space_is_orthonormal() -> None:
    rng = random.Random(2)
    a = rand_h(rng, 3, 5)
    v0 = null_space(a, 5)
    assert len(v0[0]) == 2
    assert max_abs(cbb.sub(cbb.matmul(cbb.herm(v0), v0), cbb.eye(2))) < 1e-12
    assert max_abs(cbb.matmul(a, v0)) < 1e-12


def test_rate_two_ways() -> None:
    # The rate from the gains equals the log det rate with the other users treated as noise.
    rng = random.Random(3)
    for m, sizes in [(4, (2, 2)), (6, (2, 3, 1))]:
        hs = [rand_h(rng, n, m) for n in sizes]
        w, _, s, p = bd_precoder(hs, 10.0, 0.5)
        assert abs(rate_from_gains(s, p, 0.5) - sum_rate(hs, w, 0.5)) < 1e-9


def test_single_antenna_users_give_zero_forcing_gains() -> None:
    # With N_k = 1 the gain of user k is 1 / [(H H^H)^(-1)]_kk, the zero-forcing gain.
    rng = random.Random(4)
    h = rand_h(rng, 3, 4)
    _, _, s, _ = bd_precoder([[row] for row in h], 1.0, 1.0)
    gi = cbb.inv(cbb.matmul(h, cbb.herm(h)))
    for k in range(3):
        assert abs(s[k][0] ** 2 - 1.0 / gi[k][k].real) < 1e-10


def test_water_filling_kkt() -> None:
    rng = random.Random(5)
    hs = [rand_h(rng, 2, 6) for _ in range(3)]
    n0 = 2.0
    _, _, s, p = bd_precoder(hs, 4.0, n0)
    inv = [n0 / (x * x) for sk in s for x in sk]
    pw = [x for pk in p for x in pk]
    mu = max(i + q for i, q in zip(inv, pw) if q > 0)
    for i, q in zip(inv, pw):
        if q > 0:
            assert abs(i + q - mu) < 1e-9
        else:
            assert i >= mu - 1e-9


def test_grid_search_over_powers() -> None:
    # On the example, no split of the power over the three streams beats BD.
    w, _, s, p = bd_precoder(EXAMPLE, 3.0, 1.0)
    g = [x * x for sk in s for x in sk]
    best = rate_from_gains(s, p, 1.0)
    grid = 0.0
    steps = 150
    for a in range(steps + 1):
        for b in range(steps + 1 - a):
            q = [3.0 * a / steps, 3.0 * b / steps, 3.0 * (steps - a - b) / steps]
            grid = max(grid, sum(math.log2(1 + gi * qi) for gi, qi in zip(g, q)))
    assert grid <= best + 1e-12
    assert best - grid < 1e-3


def test_beats_random_null_space_precoders() -> None:
    # BD is the best precoder with zero interference: random precoders in the same null spaces do not beat it.
    rng = random.Random(6)
    m, sizes, pt = 4, (2, 2), 6.0
    hs = [rand_h(rng, n, m) for n in sizes]
    w, _, s, p = bd_precoder(hs, pt, 1.0)
    best = rate_from_gains(s, p, 1.0)
    bases = []
    for k in range(2):
        others = [row for j, hj in enumerate(hs) if j != k for row in hj]
        bases.append(null_space(others, m))
    for _ in range(200):
        ws = [cbb.matmul(v0, rand_h(rng, len(v0[0]), 2)) for v0 in bases]
        c = math.sqrt(pt / sum(cbb.norm2(x) for x in ws))
        ws = [cbb.scale(c, x) for x in ws]
        assert sum_rate(hs, ws, 1.0) <= best + 1e-9


def test_too_few_antennas() -> None:
    rng = random.Random(7)
    # The 3 antennas of user 1 fill the whole space, so user 2 has no null space.
    hs = [rand_h(rng, 3, 3), rand_h(rng, 1, 3)]
    try:
        bd_precoder(hs, 1.0, 1.0)
    except ValueError:
        return
    raise AssertionError("expected ValueError")
