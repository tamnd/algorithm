# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/grover-search/. The authors are listed in prov/XD74ZG.jsonl.

import math
import random

from grover_search import (
    grover_iteration,
    grover_search,
    grover_state,
    num_iterations,
    success_probability,
    uniform_state,
)

TOL = 1e-9


def marked_set(n_items: int, n_marked: int, seed: int) -> set[int]:
    return set(random.Random(seed).sample(range(n_items), n_marked))


def test_closed_form_every_n_and_m() -> None:
    # Every N up to 64, every M, and k from 0 to past the second peak.
    for n_items in range(1, 65):
        for n_marked in range(0, n_items + 1):
            marked = marked_set(n_items, n_marked, 1000 * n_items + n_marked)
            f = lambda x, s=marked: 1 if x in s else 0
            theta = math.asin(math.sqrt(n_marked / n_items))
            k_max = 3 if n_marked == 0 else 2 * num_iterations(n_items, n_marked) + 3
            state = uniform_state(n_items)
            for k in range(k_max + 1):
                p = sum(abs(state[x]) ** 2 for x in marked)
                assert abs(p - math.sin((2 * k + 1) * theta) ** 2) < TOL
                assert abs(sum(abs(a) ** 2 for a in state) - 1.0) < TOL
                grover_iteration(state, n_items, f)


def test_gate_form_equals_mean_form() -> None:
    for n in range(1, 7):
        n_items = 1 << n
        for n_marked in range(1, n_items + 1):
            marked = marked_set(n_items, n_marked, 7 * n_items + n_marked)
            f = lambda x, s=marked: 1 if x in s else 0
            for k in range(num_iterations(n_items, n_marked) + 3):
                a = grover_state(n_items, f, k, gates=True)
                b = grover_state(n_items, f, k, gates=False)
                assert max(abs(u - v) for u, v in zip(a, b)) < TOL


def test_optimal_count_and_its_bound() -> None:
    for n_items in range(1, 65):
        for n_marked in range(1, n_items + 1):
            k = num_iterations(n_items, n_marked)
            assert k <= math.pi / 4 * math.sqrt(n_items / n_marked)
            f = lambda x, m=n_marked: 1 if x < m else 0
            assert success_probability(n_items, f, k) >= 1 - n_marked / n_items - TOL


def test_page_example() -> None:
    f = lambda x: 1 if x == 5 else 0
    assert num_iterations(8, 1) == 2
    expected = [1 / 8, 25 / 32, 121 / 128, 169 / 512]
    for k, p in enumerate(expected):
        assert abs(success_probability(8, f, k) - p) < TOL


def test_overshoot() -> None:
    f = lambda x: 1 if x == 37 else 0
    p = [success_probability(64, f, k) for k in range(26)]
    assert p[6] > 0.99
    assert p[12] < 1e-3
    assert max(p[7:13]) == p[7]
    assert all(p[k + 1] < p[k] for k in range(6, 12))
    # Near 2 sqrt(N) iterations the success probability is below 9.5 percent.
    g = lambda x: 1 if x == 0 else 0
    assert success_probability(1024, g, round(math.sqrt(2 * 1024))) < 0.095


def test_quarter_marked_is_exact() -> None:
    for n_items in (4, 8, 16, 32, 64):
        f = lambda x, m=n_items // 4: 1 if x < m else 0
        assert num_iterations(n_items, n_items // 4) == 1
        assert abs(success_probability(n_items, f, 1) - 1.0) < TOL


def test_search_runs() -> None:
    rng = random.Random(2024)
    marked = {3, 40, 61}
    f = lambda x: 1 if x in marked else 0
    runs = 300
    hits = 0
    for _ in range(runs):
        x, queries = grover_search(64, f, 3, rng)
        assert queries == num_iterations(64, 3) + 1 == 4
        if x is not None:
            assert x in marked
            hits += 1
    p = success_probability(64, f, 3)
    # Hoeffding: the error of the mean of 300 runs is below 0.12 with probability above 1 - 2e-4.
    assert abs(hits / runs - p) < 0.12
    x, queries = grover_search(16, lambda x: 1, 16, rng)
    assert x is not None and queries == 1
