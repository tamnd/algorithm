# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/online-threshold-knapsack/. The authors are listed in prov/RRVVVX.jsonl.

import math
import random

from online_threshold_knapsack import (
    OnlineThresholdKnapsack,
    fractional_opt,
    guarantee,
    psi,
    threshold_knapsack,
)


def integrate(f, a: float, b: float, steps: int = 20000) -> float:
    h = (b - a) / steps
    return sum(f(a + (k + 0.5) * h) for k in range(steps)) * h


def test_threshold_function() -> None:
    for L, U in [(1.0, 2.0), (1.0, 10.0), (0.5, 50.0)]:
        c = 1 / (1 + math.log(U / L))
        assert psi(0.0, L, U) == L and psi(c, L, U) == L
        assert abs(psi(c + 1e-12, L, U) - L) < 1e-9
        assert abs(psi(1.0, L, U) - U) < 1e-9 * U
        zs = [k / 100 for k in range(101)]
        assert all(psi(a, L, U) <= psi(b, L, U) for a, b in zip(zs, zs[1:]))
        # the key identity: the area under psi up to Z equals c * psi(Z) for Z >= c
        for Z in [c, (c + 1) / 2, 1.0]:
            area = integrate(lambda z: psi(z, L, U), 0.0, Z)
            assert abs(area - c * psi(Z, L, U)) < 1e-6 * U


def test_example_from_page() -> None:
    items = [(0.1, d * 0.1) for d in [1, 1, 1, 2, 1.5, 5, 1.2, 3, 8, 10, 2.5, 9, 10, 10]]
    alg = OnlineThresholdKnapsack(1.0, 10.0)
    taken = [alg.arrive(w, v) for w, v in items]
    assert abs(alg.c - 0.3028) < 1e-4
    assert taken == [True, True, True, True, True, True, False, True, True, True, False, True, False, False]
    assert abs(alg.value - 4.15) < 1e-9 and abs(alg.z - 1.0) < 1e-9
    assert abs(fractional_opt(items) - 6.1) < 1e-9


def random_items(rng: random.Random, L: float, U: float, eps: float):
    items = []
    for _ in range(rng.randint(5, 400)):
        w = rng.uniform(eps / 10, eps)
        if rng.random() < 0.5:
            d = L * (U / L) ** rng.random()
        else:
            d = rng.choice([L, U, (L + U) / 2])
        items.append((w, d * w))
    if rng.random() < 0.5:
        items.sort(key=lambda it: it[1] / it[0])  # rising densities, the hard order
    return items


def test_ratio_on_random_inputs() -> None:
    rng = random.Random(8)
    for _ in range(400):
        L = rng.uniform(0.5, 2)
        U = L * rng.choice([1.0, 1.5, 2, 10, 100])
        eps = rng.choice([0.001, 0.01, 0.05])
        items = random_items(rng, L, U, eps)
        taken = threshold_knapsack(items, L, U)
        assert sum(items[i][0] for i in taken) <= 1 + 1e-9
        alg = sum(items[i][1] for i in taken)
        assert fractional_opt(items) <= guarantee(L, U, eps) * alg + 1e-9


def test_rising_density_adversary_is_tight() -> None:
    # batches of densities L r^k, each batch filling the capacity with items of size 1/m;
    # the adversary may stop after any batch, and the worst stop gives about 1 + ln(U/L)
    for ratio in [2.0, 10.0, 100.0]:
        L, U = 1.0, ratio
        N, m = 400, 400
        alg = OnlineThresholdKnapsack(L, U)
        worst = 0.0
        for k in range(N + 1):
            p = L * (U / L) ** (k / N)
            for _ in range(m):
                alg.arrive(1 / m, p / m)
            worst = max(worst, p / alg.value)
        target = 1 + math.log(U / L)
        assert worst <= guarantee(L, U, 1 / m)
        assert worst >= 0.97 * target


def test_lower_bound_for_any_fill_schedule() -> None:
    # for any non-decreasing fills f_0 <= ... <= f_N <= 1 on the batches,
    # max_k p_k / ALG_k >= 1 + N (1 - (L/U)^(1/N)); checked on random schedules
    rng = random.Random(3)
    L, U, N = 1.0, 10.0, 20
    ps = [L * (U / L) ** (k / N) for k in range(N + 1)]
    bound = 1 + N * (1 - (L / U) ** (1 / N))
    for _ in range(2000):
        cuts = sorted(rng.random() for _ in range(N + 1))
        top = rng.random() ** 0.2
        f = [top * c for c in cuts]
        value, prev, worst = 0.0, 0.0, 0.0
        for p, fk in zip(ps, f):
            value += p * (fk - prev)
            prev = fk
            worst = max(worst, p / value) if value > 0 else math.inf
        assert worst >= bound - 1e-9


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
    print("ok")
