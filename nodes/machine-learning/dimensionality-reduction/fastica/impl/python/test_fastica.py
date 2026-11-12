# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fastica/. The authors are listed in prov/6J62KD.jsonl.

import math
import random

import pytest

from fastica import (
    amari_index,
    fastica_deflation,
    fastica_symmetric,
    nonlinearity,
    one_unit_update,
    population_kurtosis_step,
    symmetric_decorrelation,
    whiten,
)

TOL = 0.98  # every recovered source must have |correlation| above this with one true source


def laplace(rng: random.Random) -> float:
    u = rng.random() - 0.5
    return -math.copysign(1.0, u) * math.log(1.0 - 2.0 * abs(u)) / math.sqrt(2.0)


def uniform(rng: random.Random) -> float:
    return rng.uniform(-math.sqrt(3.0), math.sqrt(3.0))


def binary(rng: random.Random) -> float:
    return rng.choice([-1.0, 1.0])


def make(rng: random.Random, n: int, makers: list, a: list) -> tuple[list, list]:
    srcs = [[mk(rng) for mk in makers] for _ in range(n)]
    xs = [[sum(a[i][j] * s[j] for j in range(len(makers))) for i in range(len(a))] for s in srcs]
    return srcs, xs


def abs_corr(u: list, v: list) -> float:
    n = len(u)
    mu, mv = sum(u) / n, sum(v) / n
    cuv = sum((a - mu) * (b - mv) for a, b in zip(u, v))
    cuu = sum((a - mu) ** 2 for a in u)
    cvv = sum((b - mv) ** 2 for b in v)
    return abs(cuv) / math.sqrt(cuu * cvv)


def check_recovery(unmix: list, xs: list, srcs: list) -> None:
    d = len(srcs[0])
    outs = [[sum(b * x for b, x in zip(row, xt)) for xt in xs] for row in unmix]
    cols = [[s[j] for s in srcs] for j in range(d)]
    matched = []
    for out in outs:
        cors = [abs_corr(out, c) for c in cols]
        best = max(range(d), key=lambda j: cors[j])
        assert cors[best] > TOL
        matched.append(best)
    assert sorted(matched) == list(range(len(outs)))  # a permutation: each source found once


def matmul(p: list, q: list) -> list:
    return [[sum(p[i][k] * q[k][j] for k in range(len(q))) for j in range(len(q[0]))] for i in range(len(p))]


@pytest.mark.parametrize("g_name", ["pow3", "logcosh", "exp"])
def test_deflation_recovers_uniform_and_laplace(g_name: str) -> None:
    rng = random.Random(10)
    a = [[1.0, 0.7], [0.5, 1.0]]
    srcs, xs = make(rng, 3000, [uniform, laplace], a)
    unmix, counts = fastica_deflation(xs, 2, random.Random(11), g_name)
    check_recovery(unmix, xs, srcs)
    assert amari_index(matmul(unmix, a)) < 0.05
    assert max(counts) < 200


def test_symmetric_recovers_three_sources() -> None:
    rng = random.Random(12)
    a = [[1.0, 2.0, 0.5], [0.3, 1.0, 1.0], [1.5, 0.2, 1.0]]
    srcs, xs = make(rng, 3000, [uniform, laplace, binary], a)
    unmix, it = fastica_symmetric(xs, 3, random.Random(13), "logcosh")
    check_recovery(unmix, xs, srcs)
    assert amari_index(matmul(unmix, a)) < 0.05
    assert it < 200


def test_outputs_are_white() -> None:
    rng = random.Random(14)
    _, xs = make(rng, 1000, [uniform, laplace, binary], [[1, 1, 0], [0, 1, 1], [1, 0, 1]])
    unmix, _ = fastica_deflation(xs, 3, random.Random(15), "logcosh")
    n = len(xs)
    mean = [sum(x[j] for x in xs) / n for j in range(3)]
    outs = [[sum(b * (x[j] - mean[j]) for j, b in enumerate(row)) for x in xs] for row in unmix]
    for i in range(3):
        for j in range(3):
            assert sum(a * b for a, b in zip(outs[i], outs[j])) / n == pytest.approx(1.0 if i == j else 0.0, abs=1e-8)


def test_converged_vector_is_a_fixed_point() -> None:
    rng = random.Random(16)
    _, xs = make(rng, 2000, [uniform, laplace], [[2.0, 1.0], [1.0, 1.0]])
    z, v = whiten(xs)
    unmix, _ = fastica_deflation(xs, 1, random.Random(17), "logcosh")
    # Recover w in whitened coordinates: unmix = w^T V, and V is invertible.
    v_inv = inverse(v)
    w = [sum(unmix[0][j] * v_inv[j][k] for j in range(2)) for k in range(2)]
    g, dg = nonlinearity("logcosh")
    w_plus = one_unit_update(z, w, g, dg)
    norm = math.sqrt(sum(x * x for x in w_plus))
    assert abs(sum(a * b for a, b in zip(w, w_plus))) / norm == pytest.approx(1.0, abs=1e-8)


def inverse(m: list) -> list:
    (a, b), (c, d) = m
    det = a * d - b * c
    return [[d / det, -b / det], [-c / det, a / det]]


def test_symmetric_decorrelation_gives_orthonormal_rows() -> None:
    rng = random.Random(18)
    w = symmetric_decorrelation([[rng.gauss(0, 1) for _ in range(4)] for _ in range(4)])
    for i in range(4):
        for j in range(4):
            assert sum(a * b for a, b in zip(w[i], w[j])) == pytest.approx(1.0 if i == j else 0.0, abs=1e-10)


def test_population_iteration_converges_cubically() -> None:
    # In source coordinates the kurtosis step is w_i <- kappa_i w_i^3 (then normalize).
    # With u_i = sqrt(|kappa_i|) |w_i|, the ratios u_i / u_1 are cubed at every step.
    kappa = [3.0, -1.2, -2.0, 1.0]
    w = [0.6, 0.5, 0.45, 0.4]
    s = math.sqrt(sum(x * x for x in w))
    w = [x / s for x in w]
    for _ in range(4):
        u = [math.sqrt(abs(k)) * abs(x) for k, x in zip(kappa, w)]
        w2 = population_kurtosis_step(kappa, w)
        u2 = [math.sqrt(abs(k)) * abs(x) for k, x in zip(kappa, w2)]
        for i in range(1, 4):
            assert u2[i] / u2[0] == pytest.approx((u[i] / u[0]) ** 3, rel=1e-9)
        w = w2
    assert abs(w[0]) == pytest.approx(1.0, abs=1e-12)
    errors = []
    w = [x / s for x in [0.6, 0.5, 0.45, 0.4]]
    for _ in range(3):
        w = population_kurtosis_step(kappa, w)
        errors.append(math.sqrt(1.0 - w[0] ** 2))
    # Cubic convergence: the error at least roughly cubes (error ratio e_{t+1} / e_t^3 bounded).
    assert errors[2] < 10 * errors[1] ** 3


def test_population_step_matches_sample_step() -> None:
    # On a large sample of independent whitened sources the pow3 update is close to kappa_i w_i^3.
    rng = random.Random(19)
    srcs = [[uniform(rng), binary(rng)] for _ in range(40000)]
    g, dg = nonlinearity("pow3")
    w = [0.8, 0.6]
    w_plus = one_unit_update(srcs, w, g, dg)
    assert w_plus[0] == pytest.approx(-1.2 * 0.8 ** 3, abs=0.05)
    assert w_plus[1] == pytest.approx(-2.0 * 0.6 ** 3, abs=0.05)
