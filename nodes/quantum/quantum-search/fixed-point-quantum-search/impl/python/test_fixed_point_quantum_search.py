# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fixed-point-quantum-search/. The authors are listed in prov/33JPWY.jsonl.

import math
import random

from fixed_point_quantum_search import (
    choose_depth,
    fixed_point_search,
    pi3_state,
    width,
    ylc_length,
    ylc_phases,
    ylc_predicted,
    ylc_search,
    ylc_success,
)
from qsim import norm

TOL = 1e-9


def marked_f(n_items: int, n_marked: int, seed: int):
    marked = set(random.Random(seed).sample(range(n_items), n_marked))
    return marked, (lambda x, s=marked: 1 if x in s else 0)


def grover_probability(n_items: int, n_marked: int, k: int) -> float:
    theta = math.asin(math.sqrt(n_marked / n_items))
    return math.sin((2 * k + 1) * theta) ** 2


def test_pi3_formula_and_monotone() -> None:
    # Success after depth n is 1 - (1 - lam)^(3^n), with (3^n - 1) / 2 queries,
    # and it never decreases with the depth, for every N and M checked.
    for n_items in (1, 2, 3, 4, 5, 8, 16):
        for n_marked in range(0, n_items + 1):
            marked, f = marked_f(n_items, n_marked, 7 * n_items + n_marked)
            lam = n_marked / n_items
            last = -1.0
            for depth in range(4):
                state, queries = pi3_state(n_items, f, depth)
                p = sum(abs(state[x]) ** 2 for x in marked)
                assert queries == (3 ** depth - 1) // 2
                assert abs(norm(state) - 1.0) < TOL
                assert abs(p - (1.0 - (1.0 - lam) ** (3 ** depth))) < TOL
                assert p >= last - TOL
                last = p


def test_pi3_example_table() -> None:
    # N = 8, one marked item: the table on the page.
    f = lambda x: 1 if x == 5 else 0
    expected = [0.125, 0.330078125, 0.6993422, 0.9728220]
    for depth, want in enumerate(expected):
        state, _ = pi3_state(8, f, depth)
        assert abs(abs(state[5]) ** 2 - want) < 1e-6
    # Grover's plain iteration overshoots on the same input.
    assert grover_probability(8, 1, 3) < 0.34


def test_choose_depth() -> None:
    assert choose_depth(1 / 8, 0.05) == 3
    for w_min in (0.5, 0.1, 0.01):
        for eps in (0.1, 0.01):
            d = choose_depth(w_min, eps)
            assert (1 - w_min) ** (3 ** d) <= eps
            assert d == 0 or (1 - w_min) ** (3 ** (d - 1)) > eps


def test_seeded_pi3_runs() -> None:
    rng = random.Random(2024)
    runs = 300
    hits = 0
    for _ in range(runs):
        marked, f = marked_f(16, 3, rng.randrange(10 ** 6))
        x, queries = fixed_point_search(16, f, 3 / 16, 0.05, rng)
        assert queries == 13 + 1
        if x is not None:
            assert x in marked
            hits += 1
    # Each run fails with probability (13/16)^27 < 0.004. Hoeffding,
    # 300 runs, failure 1e-3: tolerance sqrt(ln(1000) / 600) < 0.108.
    assert hits / runs >= 0.996 - 0.108


def test_ylc_matches_closed_form() -> None:
    for n_items in (2, 4, 7, 8, 16, 32):
        for n_marked in range(0, n_items + 1):
            _, f = marked_f(n_items, n_marked, 11 * n_items + n_marked)
            lam = n_marked / n_items
            for length in (1, 3, 5, 7, 9, 13):
                for delta in (0.9, 0.5, 0.1):
                    p = ylc_success(n_items, f, length, delta)
                    assert abs(p - ylc_predicted(length, delta, lam)) < 1e-8


def test_ylc_delta_one_is_grover() -> None:
    for n_items in (8, 16, 64):
        for n_marked in (1, 2, 3):
            _, f = marked_f(n_items, n_marked, n_items + n_marked)
            for length in (3, 5, 7, 9):
                alpha, beta = ylc_phases(length, 1.0 - 1e-15)
                assert all(abs(abs(a) - math.pi) < 1e-6 for a in alpha + beta)
                p = ylc_success(n_items, f, length, 1.0 - 1e-15)
                assert abs(p - grover_probability(n_items, n_marked, (length - 1) // 2)) < 1e-6


def test_ylc_guarantee() -> None:
    # For every lam >= w, P_L >= 1 - delta^2, in simulation.
    for n_items in (16, 32, 64):
        for delta in (0.5, math.sqrt(0.1)):
            for w_min in (1.0 / n_items, 4.0 / n_items):
                length = ylc_length(w_min, delta)
                assert width(length, delta) <= w_min
                assert length == 1 or width(length - 2, delta) > w_min
                for n_marked in range(1, n_items + 1):
                    if n_marked / n_items < w_min:
                        continue
                    _, f = marked_f(n_items, n_marked, 3 * n_items + n_marked)
                    assert ylc_success(n_items, f, length, delta) >= 1.0 - delta ** 2 - TOL


def test_ylc_width_and_length() -> None:
    for delta in (0.9, 0.5, 0.1, 0.01):
        last = 2.0
        for length in range(1, 201, 2):
            w = width(length, delta)
            assert w < last
            last = w
        for w_min in (0.5, 0.1, 0.01, 0.001):
            # L >= ln(2 / delta) / sqrt(w) suffices.
            assert ylc_length(w_min, delta) <= math.log(2.0 / delta) / math.sqrt(w_min) + 2


def test_ylc_against_grover_overshoot() -> None:
    # N = 64: 6 Grover iterations are tuned for M = 1. With M = 4 the success
    # is 0.0204. The YLC search with L = 15 (7 queries) keeps >= 0.9 for all M.
    delta = math.sqrt(0.1)
    length = ylc_length(1.0 / 64, delta)
    assert length == 15
    for n_marked in range(1, 65):
        _, f = marked_f(64, n_marked, 500 + n_marked)
        assert ylc_success(64, f, length, delta) >= 0.9 - TOL
    assert grover_probability(64, 4, 6) < 0.021


def test_seeded_ylc_runs() -> None:
    rng = random.Random(77)
    runs = 300
    hits = 0
    for _ in range(runs):
        marked, f = marked_f(32, 5, rng.randrange(10 ** 6))
        x, _ = ylc_search(32, f, 1.0 / 32, 0.5, rng)
        if x is not None:
            assert x in marked
            hits += 1
    assert hits / runs >= 0.75 - 0.108
