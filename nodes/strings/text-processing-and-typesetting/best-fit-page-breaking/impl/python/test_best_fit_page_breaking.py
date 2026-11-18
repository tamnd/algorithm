# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/best-fit-page-breaking/. The authors are listed in prov/81895S.jsonl.

import math
import random

from boxglue import FILL, INF_PENALTY, Box, Glue, Penalty, all_breakings, is_forced, is_legal_break, tex_badness
from best_fit_page_breaking import (
    AWFUL_BAD,
    DEPLORABLE,
    Page,
    break_cost,
    breaking_cost,
    lines,
    optimal_breaking,
    page_badness,
    page_builder,
)


def simulate(items, goal, max_depth=None):
    """The page builder item by item, with running totals as in TeX, no prefix sums."""
    m = len(items)
    breaks, costs = [], []
    a = -1
    while True:
        i = a + 1
        while i < m and not isinstance(items[i], Box):
            i += 1  # glue, kerns and penalties at the top of a page are discarded
        if i >= m:
            return breaks, costs
        total, depth = 0, 0
        stretch, shrink = [0, 0, 0, 0], 0
        least, best = AWFUL_BAD, None
        for k in range(i, m):
            x = items[k]
            if k > i and is_legal_break(items, k):
                p = x.penalty if isinstance(x, Penalty) else 0
                c = break_cost(page_badness(total, tuple(stretch), shrink, goal), p)
                if c <= least:
                    least, best = c, k
                if c == AWFUL_BAD or p <= -INF_PENALTY:
                    break
            if isinstance(x, Box):
                total += depth + x.height
                depth = x.depth
                if max_depth is not None and depth > max_depth:
                    total += depth - max_depth
                    depth = max_depth
            elif isinstance(x, Glue):
                total += depth + x.width
                depth = 0
                stretch[x.stretch_order] += x.stretch
                shrink += x.shrink
        breaks.append(best)
        costs.append(least)
        a = best


def random_list(rng, n):
    items = []
    for i in range(n):
        if i > 0:
            if rng.random() < 0.3:
                items.append(Penalty(0, rng.choice([-200, 50, 150, 300, INF_PENALTY])))
            items.append(Glue(rng.randint(0, 3), rng.randint(0, 4), rng.randint(0, 2)))
        items.append(Box(0, rng.randint(5, 15), rng.randint(0, 3)))
    items.append(Glue(0, 1, 0, stretch_order=FILL))
    items.append(Penalty(0, -INF_PENALTY))
    return items


def test_break_cost_rules():
    assert break_cost(50, 100) == 150
    assert break_cost(20, -500) == -480
    assert break_cost(0, 0) == 0
    assert break_cost(10000, 0) == DEPLORABLE
    assert break_cost(10000, -INF_PENALTY) == -INF_PENALTY
    assert break_cost(37, -INF_PENALTY) == -INF_PENALTY
    assert break_cost(AWFUL_BAD, 0) == AWFUL_BAD
    assert break_cost(AWFUL_BAD, -INF_PENALTY) == AWFUL_BAD
    assert break_cost(50, 100, 25) == 175
    assert break_cost(50, 100, INF_PENALTY) == AWFUL_BAD


def test_page_badness_rules():
    assert page_badness(22, (8, 0, 0, 0), 0, 44) == tex_badness(22, 8)
    assert page_badness(22, (8, 1, 0, 0), 0, 44) == 0
    assert page_badness(44, (0, 0, 0, 0), 0, 44) == 0
    assert page_badness(20, (0, 0, 0, 0), 5, 44) == 10000
    assert page_badness(46, (0, 0, 0, 0), 3, 44) == tex_badness(2, 3)
    assert page_badness(48, (9, 9, 0, 0), 3, 44) == AWFUL_BAD


def test_example_of_the_page():
    # four lines of height 10 and two of height 20, glue 2 plus 8 minus 1, page goal 44
    items = lines([10, 10, 10, 10, 20, 20], Glue(2, 8, 1))
    assert page_badness(34, (16, 0, 0, 0), 2, 44) == 24
    assert page_badness(46, (24, 0, 0, 0), 3, 44) == 30
    assert page_badness(32, (8, 0, 0, 0), 1, 44) == 336
    breaks, costs = page_builder(items, 44)
    assert breaks == [5, 9, 12]
    assert costs == [24, 336, -INF_PENALTY]
    assert breaking_cost(items, breaks, 44) == 360
    assert optimal_breaking(items, 44) == (30, (7, 12))


def test_a_later_break_wins_a_tie():
    items = [Box(0, 10), Glue(2), Box(0, 10), Glue(0), Penalty(0, 0), Box(0, 10), Glue(0, 1, 0, stretch_order=FILL), Penalty(0, -INF_PENALTY)]
    breaks, costs = page_builder(items, 22)
    assert breaks == [4, 7]
    assert costs == [0, -INF_PENALTY]


def test_discards_at_the_top_of_a_page():
    items = [Box(0, 10), Glue(2), Box(0, 10), Penalty(0, -INF_PENALTY), Glue(5), Penalty(0, 50), Glue(7), Box(0, 10), Glue(0, 1, 0, stretch_order=FILL), Penalty(0, -INF_PENALTY)]
    pg = Page(items)
    assert pg.first_box(3) == 7
    assert pg.total(7, 8)[0] == 10
    breaks, costs = page_builder(items, 22)
    assert breaks == [3, 9]
    assert costs == [-INF_PENALTY, -INF_PENALTY]


def test_depth_of_the_last_box():
    items = [Box(0, 8, 3), Glue(2), Box(0, 8, 3), Glue(0, 1, 0, stretch_order=FILL), Penalty(0, -INF_PENALTY)]
    assert Page(items).total(0, 3)[0] == 21
    assert Page(items).total(0, 4)[0] == 24
    assert Page(items, max_depth=1).total(0, 3)[0] == 23
    assert Page(items, max_depth=5).total(0, 3)[0] == 21


def test_overfull_page_is_taken_when_nothing_fits():
    items = lines([30, 10], Glue(2))
    breaks, costs = page_builder(items, 20)
    assert breaks == [1, 4]
    assert costs[0] == AWFUL_BAD
    assert breaking_cost(items, breaks, 20) == AWFUL_BAD


def test_infinite_shrink_is_rejected():
    items = [Box(0, 10), Glue(2, 0, 1, shrink_order=FILL), Box(0, 10), Penalty(0, -INF_PENALTY)]
    try:
        page_builder(items, 20)
    except ValueError:
        return
    raise AssertionError("infinite shrink was accepted")


def test_builder_against_item_by_item_simulation():
    rng = random.Random(1)
    for _ in range(400):
        items = random_list(rng, rng.randint(1, 12))
        goal = rng.randint(15, 60)
        md = rng.choice([None, 0, 1, 2])
        assert page_builder(items, goal, md) == simulate(items, goal, md)


def test_builder_never_beats_the_optimum_and_is_a_breaking():
    rng = random.Random(2)
    worse = 0
    for _ in range(300):
        items = random_list(rng, rng.randint(1, 7))
        goal = rng.randint(15, 50)
        breaks, _ = page_builder(items, goal)
        gc = breaking_cost(items, breaks, goal)
        oc, ob = optimal_breaking(items, goal)
        if gc == AWFUL_BAD:
            continue
        full = set(all_breakings(items))
        assert tuple(breaks) in full or tuple(breaks) + (len(items) - 1,) in full
        assert all(is_legal_break(items, b) for b in breaks)
        assert oc <= gc
        worse += oc < gc
    assert worse > 0


def test_forced_breaks_are_always_taken():
    rng = random.Random(4)
    for _ in range(200):
        items = random_list(rng, rng.randint(1, 10))
        k = rng.randrange(len(items) - 1)
        if isinstance(items[k], Glue) and k > 0 and isinstance(items[k - 1], Box):
            items[k] = Penalty(0, -INF_PENALTY)
        breaks, _ = page_builder(items, rng.randint(15, 60))
        tops = [-1] + breaks
        for b, x in enumerate(items):
            if is_forced(x):
                # either the page ends there, or the penalty is at the top of a page and is discarded
                a = max(t for t in tops if t < b)
                assert b in breaks or not any(isinstance(y, Box) for y in items[a + 1 : b])


def test_number_of_tests_per_page_is_bounded():
    rng = random.Random(5)
    h, goal = 10, 120
    items = lines([h] * 3000, Glue(2, 3, 0), [rng.choice([0, 0, 150]) for _ in range(2999)])
    stats = {}
    breaks, costs = page_builder(items, goal, stats=stats)
    assert all(c < AWFUL_BAD for c in costs)
    assert stats["tests"] <= len(breaks) * (goal // h + 2)
    assert not math.isinf(breaking_cost(items, breaks, goal))
