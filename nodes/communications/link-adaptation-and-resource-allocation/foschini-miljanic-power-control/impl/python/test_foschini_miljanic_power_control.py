# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/foschini-miljanic-power-control/. The authors are listed in prov/K8XR5H.jsonl.

import random

import pytest

from foschini_miljanic_power_control import (
    foschini_miljanic,
    foschini_miljanic_async,
    normalized_gain,
    sinr,
    solve_linear,
    spectral_radius,
    target_powers,
)

G = [[1.0, 0.1, 0.2], [0.2, 1.0, 0.1], [0.1, 0.1, 1.0]]
NOISE = [0.1, 0.1, 0.1]


def random_case(rng: random.Random, k: int, cross: float):
    g = [[rng.uniform(0.5, 1.5) if i == j else cross * rng.random() for j in range(k)] for i in range(k)]
    noise = [rng.uniform(0.05, 0.2) for _ in range(k)]
    gamma = [rng.uniform(0.5, 3.0) for _ in range(k)]
    return g, gamma, noise


def test_page_example() -> None:
    p_star = target_powers(G, [2.0] * 3, NOISE)
    assert p_star is not None
    assert all(abs(a - b) < 1e-12 for a, b in zip(p_star, [42 / 95, 43 / 95, 36 / 95]))
    p, _ = foschini_miljanic(G, [2.0] * 3, NOISE, [0.0] * 3, iters=1)
    assert all(abs(a - 0.2) < 1e-15 for a in p)
    p, _ = foschini_miljanic(G, [2.0] * 3, NOISE, p, iters=1)
    assert all(abs(a - b) < 1e-12 for a, b in zip(p, [0.32, 0.32, 0.28]))
    p, steps = foschini_miljanic(G, [2.0] * 3, NOISE, [0.0] * 3, tol=1e-9)
    assert steps < 60
    assert all(abs(a - b) < 1e-8 for a, b in zip(p, p_star))
    f, _ = normalized_gain(G, [2.0] * 3, NOISE)
    assert abs(spectral_radius(f) - 0.525473017) < 1e-8


def test_threshold_of_feasibility() -> None:
    f, _ = normalized_gain(G, [1.0] * 3, NOISE)
    gmax = 1.0 / spectral_radius(f)
    assert abs(gmax - 3.806091) < 1e-5
    assert target_powers(G, [0.999 * gmax] * 3, NOISE) is not None
    assert target_powers(G, [1.001 * gmax] * 3, NOISE) is None
    assert target_powers(G, [4.0] * 3, NOISE) is None


def test_fixed_point_meets_targets_with_equality() -> None:
    rng = random.Random(11)
    for _ in range(200):
        k = rng.randint(2, 6)
        g, gamma, noise = random_case(rng, k, 0.3)
        p_star = target_powers(g, gamma, noise)
        if p_star is None:
            continue
        s = sinr(g, noise, p_star)
        assert all(abs(a - b) <= 1e-9 * b for a, b in zip(s, gamma))
        p, _ = foschini_miljanic(g, gamma, noise, [rng.uniform(0, 10) for _ in range(k)], iters=20000, tol=1e-14)
        assert all(abs(a - b) <= 1e-8 * b for a, b in zip(p, p_star))


def test_monotone_from_zero_and_from_above() -> None:
    rng = random.Random(5)
    for _ in range(50):
        g, gamma, noise = random_case(rng, 4, 0.3)
        p_star = target_powers(g, gamma, noise)
        if p_star is None:
            continue
        p = [0.0] * 4
        q = [3.0 * v for v in p_star]
        for _ in range(100):
            p2, _ = foschini_miljanic(g, gamma, noise, p, iters=1)
            q2, _ = foschini_miljanic(g, gamma, noise, q, iters=1)
            assert all(b >= a - 1e-15 for a, b in zip(p, p2))
            assert all(b <= a + 1e-12 for a, b in zip(q, q2))
            assert all(a <= s + 1e-12 and s <= b + 1e-12 for a, s, b in zip(p2, p_star, q2))
            p, q = p2, q2


def test_least_powers() -> None:
    # Every power vector that meets all targets is at least p* in each entry.
    rng = random.Random(7)
    g, gamma, noise = G, [2.0] * 3, NOISE
    p_star = target_powers(g, gamma, noise)
    hits = 0
    for _ in range(20000):
        q = [rng.uniform(0.0, 2.0) for _ in range(3)]
        if all(s >= t for s, t in zip(sinr(g, noise, q), gamma)):
            hits += 1
            assert all(a >= b - 1e-12 for a, b in zip(q, p_star))
    assert hits > 100


def test_infeasible_diverges() -> None:
    gamma = [4.0] * 3
    p, _ = foschini_miljanic(G, gamma, NOISE, [0.0] * 3, iters=400)
    assert min(p) > 1e6
    rng = random.Random(3)
    for _ in range(100):
        g, gam, noise = random_case(rng, 3, 1.5)
        if target_powers(g, gam, noise) is None:
            f, _ = normalized_gain(g, gam, noise)
            assert spectral_radius(f) >= 1.0 - 1e-9


def test_rate_is_the_spectral_radius() -> None:
    gamma = [3.5] * 3
    p_star = target_powers(G, gamma, NOISE)
    f, _ = normalized_gain(G, gamma, NOISE)
    rho = spectral_radius(f)
    p = [0.0] * 3
    errs = []
    for _ in range(300):
        p, _ = foschini_miljanic(G, gamma, NOISE, p, iters=1)
        errs.append(max(abs(a - b) for a, b in zip(p, p_star)))
    ratio = errs[201] / errs[200]
    assert abs(ratio - rho) < 1e-3


@pytest.mark.parametrize("beta", [0.25, 0.5, 1.0])
def test_relaxed_and_asynchronous(beta: float) -> None:
    rng = random.Random(int(beta * 100))
    for _ in range(12):
        g, gamma, noise = random_case(rng, 5, 0.25)
        p_star = target_powers(g, gamma, noise)
        if p_star is None:
            continue
        p, _ = foschini_miljanic(g, gamma, noise, [1.0] * 5, beta=beta, iters=50000, tol=1e-14)
        assert all(abs(a - b) <= 1e-7 * b for a, b in zip(p, p_star))
        if beta == 1.0:
            q = foschini_miljanic_async(g, gamma, noise, [5.0] * 5, rng, 20000)
            assert all(abs(a - b) <= 1e-7 * b for a, b in zip(q, p_star))


def test_spectral_radius_two_links() -> None:
    # F = [[0, a], [b, 0]] has eigenvalues +- sqrt(ab); power iteration on F alone would oscillate.
    f = [[0.0, 0.3], [0.8, 0.0]]
    assert abs(spectral_radius(f) - (0.24) ** 0.5) < 1e-9
    assert solve_linear([[0.0, 0.0], [0.0, 1.0]], [1.0, 1.0]) is None
    with pytest.raises(ValueError):
        foschini_miljanic(G, [2.0] * 3, NOISE, [0.0] * 3, beta=0.0)
