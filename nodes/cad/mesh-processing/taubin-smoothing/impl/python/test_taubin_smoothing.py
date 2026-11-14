# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/taubin-smoothing/. The authors are listed in prov/Y17GAM.jsonl.

import random
from fractions import Fraction as Fr

from mp2mesh import boundary_vertices, grid_mesh, icosphere, neighbours, signed_volume
from taubin_smoothing import pass_band, taubin_graph, taubin_smoothing, transfer

LAM, MU = Fr(33, 100), Fr(-34, 100)

# The hexagon modes cos(pi m i / 3), m = 0, 1, 2, 3, have the frequencies k = 1 - cos(pi m / 3).
HEX_MODES = {
    0: ([1, 1, 1, 1, 1, 1], Fr(0)),
    1: ([1, Fr(1, 2), Fr(-1, 2), -1, Fr(-1, 2), Fr(1, 2)], Fr(1, 2)),
    2: ([1, Fr(-1, 2), Fr(-1, 2), 1, Fr(-1, 2), Fr(-1, 2)], Fr(3, 2)),
    3: ([1, -1, 1, -1, 1, -1], Fr(2)),
}


def cycle(n):
    return [[(i - 1) % n, (i + 1) % n] for i in range(n)]


# ---- brute force: the product of the two step matrices, as dense matrices ----


def step_matrix(nb, f, fixed):
    n = len(nb)
    S = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        if i in fixed or not nb[i]:
            S[i][i] = Fr(1)
            continue
        S[i][i] = 1 - f
        for j in nb[i]:
            S[i][j] += f / len(nb[i])
    return S


def matmul(A, B):
    n = len(A)
    return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


def matrix_taubin(points, nb, lam, mu, passes, fixed):
    T = matmul(step_matrix(nb, mu, fixed), step_matrix(nb, lam, fixed))
    x = [list(p) for p in points]
    d = len(points[0])
    for _ in range(passes):
        x = [[sum(T[i][j] * x[j][k] for j in range(len(x))) for k in range(d)] for i in range(len(x))]
    return [tuple(r) for r in x]


def test_hexagon_modes_are_scaled_by_the_transfer_function() -> None:
    assert transfer(Fr(1, 2), LAM, MU) == Fr(19539, 20000)
    assert transfer(Fr(3, 2), LAM, MU) == Fr(15251, 20000)
    assert transfer(Fr(2), LAM, MU) == Fr(357, 625)
    for m, (v, k) in HEX_MODES.items():
        x = [(Fr(c),) for c in v]
        for passes in (1, 2, 3):
            y = taubin_graph(x, cycle(6), LAM, MU, passes)
            g = transfer(k, LAM, MU) ** passes
            assert y == [(g * c[0],) for c in x]


def test_example_trace() -> None:
    x = [(Fr(c),) for c in HEX_MODES[1][0]]
    assert taubin_graph(x, cycle(6), LAM, 0, 1)[0] == (Fr(167, 200),)
    assert taubin_graph(x, cycle(6), LAM, MU, 1)[0] == (Fr(19539, 20000),)
    x = [(Fr(c),) for c in HEX_MODES[3][0]]
    assert taubin_graph(x, cycle(6), LAM, 0, 1)[0] == (Fr(17, 50),)
    assert taubin_graph(x, cycle(6), LAM, MU, 1)[0] == (Fr(357, 625),)


def test_against_matrix_product() -> None:
    rng = random.Random(17)
    for _ in range(12):
        p, f = grid_mesh(rng.randrange(1, 4), rng.randrange(1, 4))
        p = [(Fr(a) + Fr(rng.randrange(-2, 3), 8), Fr(b) + Fr(rng.randrange(-2, 3), 8), Fr(rng.randrange(-4, 5), 8))
             for a, b, _ in p]
        lam = Fr(rng.randrange(1, 9), 10)
        mu = -lam - Fr(rng.randrange(1, 5), 100)
        k = rng.randrange(1, 3)
        nb = neighbours(len(p), f)
        fixed = boundary_vertices(f)
        assert taubin_smoothing(p, f, lam, mu, k) == matrix_taubin(p, nb, lam, mu, k, fixed)
        assert taubin_smoothing(p, f, lam, mu, k, fixed=()) == matrix_taubin(p, nb, lam, mu, k, set())


def test_border_fixed() -> None:
    rng = random.Random(4)
    p, f = grid_mesh(4, 3)
    p = [(Fr(a), Fr(b), Fr(rng.randrange(-4, 5), 8)) for a, b, _ in p]
    x = taubin_smoothing(p, f, passes=4)
    for v in boundary_vertices(f):
        assert x[v] == p[v]


def test_pass_band() -> None:
    kpb = pass_band(LAM, MU)
    assert kpb == Fr(50, 561)
    assert transfer(kpb, LAM, MU) == 1 and transfer(0, LAM, MU) == 1
    for i in range(1, 201):
        k = Fr(i, 100)
        g = transfer(k, LAM, MU)
        if k < kpb:
            assert 1 < g < Fr(10003, 10000)          # a slight gain on the lowest frequencies
        else:
            assert -1 < g < 1                         # damped, and stable up to k = 2


def test_shrinks_much_less_than_laplacian() -> None:
    p, f = icosphere(2)
    v0 = signed_volume(p, f)
    x = taubin_smoothing(p, f, 0.33, -0.34, 10)
    assert 0.99 < signed_volume(x, f) / v0 < 1.02    # measured: 1.0064
    nb = neighbours(len(p), f)
    y = taubin_graph(p, nb, 0.33, 0.0, 20)           # 20 plain Laplacian steps, the same work
    assert signed_volume(y, f) / v0 < 0.5            # measured: 0.409


def test_high_frequency_noise_is_removed() -> None:
    n = 12
    rng = random.Random(9)
    base = [(Fr(rng.randrange(-8, 9), 8),) for _ in range(n)]
    smooth = taubin_graph(base, cycle(n), LAM, MU, 0)
    alt = [(Fr((-1) ** i, 10),) for i in range(n)]
    x = [(a[0] + b[0],) for a, b in zip(base, alt)]
    y = taubin_graph(x, cycle(n), LAM, MU, 3)
    z = taubin_graph(smooth, cycle(n), LAM, MU, 3)
    # linearity: the result is the smoothed base plus the alternating mode times f(2)^3
    g = transfer(Fr(2), LAM, MU) ** 3
    assert y == [(a[0] + g * b[0],) for a, b in zip(z, alt)]


def test_bad_parameters() -> None:
    p, f = grid_mesh(1, 1)
    for lam, mu in ((Fr(1, 3), Fr(-1, 3)), (Fr(-1, 3), Fr(-1, 2)), (Fr(1, 3), Fr(1, 2))):
        try:
            taubin_smoothing(p, f, lam, mu)
        except ValueError:
            continue
        raise AssertionError("bad parameters were accepted")
