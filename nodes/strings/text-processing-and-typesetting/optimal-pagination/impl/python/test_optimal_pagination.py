# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimal-pagination/. The authors are listed in prov/VBW9VJ.jsonl.

import math
import random
from fractions import Fraction

from optimal_pagination import (
    all_paginations,
    first_fit_pagination,
    optimal_pagination,
    pagination_cost,
    ref_counts,
)


def brute_force(lines, figures, refs, H, alpha, pi):
    best = math.inf
    for pages in all_paginations(len(lines), len(figures)):
        best = min(best, pagination_cost(lines, figures, refs, H, pages, alpha, pi))
    return best


def random_instance(rng, n_max, m_max):
    n = rng.randint(1, n_max)
    m = rng.randint(0, m_max)
    lines = [rng.randint(1, 3) for _ in range(n)]
    figures = [rng.randint(1, 5) for _ in range(m)]
    refs = sorted(rng.randint(1, n) for _ in range(m))
    H = rng.randint(3, 8)
    alpha = rng.choice([0, 1, 3, 10])
    pi = [rng.choice([0, 7])] + [rng.choice([0, 0, 5, 50]) for _ in range(n - 1)] + [rng.choice([0, 7])]
    return lines, figures, refs, H, alpha, pi


def test_ref_counts():
    assert ref_counts(5, [2, 2, 5]) == [0, 0, 2, 2, 2, 3]
    assert ref_counts(3, []) == [0, 0, 0, 0]


def test_example_of_the_page():
    lines, figures, refs, H, alpha = [1] * 8, [3], [4], 5, 5
    cost, pages = optimal_pagination(lines, figures, refs, H, alpha)
    assert (cost, pages) == (4, [(3, 0), (5, 1), (8, 1)])
    ff = first_fit_pagination(lines, figures, refs, H)
    assert ff == [(5, 0), (7, 1), (8, 1)]
    assert pagination_cost(lines, figures, refs, H, ff, alpha) == 5


def test_widow_penalty_moves_a_break():
    lines = [1, 1, 1, 1]
    assert optimal_pagination(lines, [], [], 3) == (0, [(3, 0), (4, 0)])
    pi = [0, 0, 0, 100, 0]
    assert optimal_pagination(lines, [], [], 3, pi=pi) == (1, [(2, 0), (4, 0)])


def test_infeasible_and_trivial_inputs():
    assert optimal_pagination([1, 1], [9], [1], 5) == (math.inf, None)
    assert optimal_pagination([7], [], [], 5) == (math.inf, None)
    assert optimal_pagination([2, 2], [], [], 5) == (0, [(2, 0)])
    assert optimal_pagination([], [], [], 5) == (0, [])


def test_bad_input_is_rejected():
    for args in (([1], [1], []), ([1], [1], [2]), ([1, 1], [1, 1], [2, 1]), ([-1], [], [])):
        try:
            optimal_pagination(*args, 5)
        except ValueError:
            continue
        raise AssertionError("bad input accepted")


def test_figure_never_before_its_reference():
    rng = random.Random(3)
    for _ in range(200):
        lines, figures, refs, H, alpha, pi = random_instance(rng, 9, 3)
        cost, pages = optimal_pagination(lines, figures, refs, H, alpha, pi)
        if pages is None:
            continue
        line_page, fig_page = {}, {}
        i = j = 0
        for k, (i2, j2) in enumerate(pages):
            for x in range(i + 1, i2 + 1):
                line_page[x] = k
            for t in range(j + 1, j2 + 1):
                fig_page[t] = k
            i, j = i2, j2
        for t, r in enumerate(refs, start=1):
            assert fig_page[t] >= line_page[r]


def test_against_brute_force():
    rng = random.Random(1)
    feasible = 0
    for _ in range(150):
        lines, figures, refs, H, alpha, pi = random_instance(rng, 7, 2)
        cost, pages = optimal_pagination(lines, figures, refs, H, alpha, pi)
        assert cost == brute_force(lines, figures, refs, H, alpha, pi)
        if pages is not None:
            feasible += 1
            assert pagination_cost(lines, figures, refs, H, pages, alpha, pi) == cost
    assert feasible >= 100


def test_fraction_heights():
    lines = [Fraction(1, 2)] * 6
    cost, pages = optimal_pagination(lines, [Fraction(3, 2)], [2], Fraction(2))
    assert cost == brute_force(lines, [Fraction(3, 2)], [2], Fraction(2), 1, [0] * 7)
    assert pagination_cost(lines, [Fraction(3, 2)], [2], Fraction(2), pages) == cost


def test_dp_is_never_worse_than_first_fit():
    rng = random.Random(2)
    better = 0
    for _ in range(300):
        lines, figures, refs, H, alpha, _ = random_instance(rng, 12, 3)
        cost, _ = optimal_pagination(lines, figures, refs, H, alpha)
        ff = first_fit_pagination(lines, figures, refs, H)
        if ff is None:
            continue
        fc = pagination_cost(lines, figures, refs, H, ff, alpha)
        assert cost <= fc
        better += cost < fc
    assert better > 0


def test_number_of_page_candidates():
    rng = random.Random(4)
    n, m, H = 400, 6, 10
    lines = [1] * n
    figures = [rng.randint(1, 4) for _ in range(m)]
    refs = sorted(rng.randint(1, n) for _ in range(m))
    stats = {}
    cost, pages = optimal_pagination(lines, figures, refs, H, 3, stats=stats)
    assert pages is not None
    assert stats["relax"] <= (n + 1) * (m + 1) * (H + 1) ** 2
    assert pagination_cost(lines, figures, refs, H, pages, 3) == cost
