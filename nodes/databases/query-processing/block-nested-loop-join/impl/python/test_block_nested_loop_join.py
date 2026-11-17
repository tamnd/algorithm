# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/block-nested-loop-join/. The authors are listed in prov/7N79ZS.jsonl.

import random
from collections import Counter

import pytest

from block_nested_loop_join import block_nested_loop_join, paginate


def reference(r_rows, s_rows, pred):
    return Counter(r + s for r in r_rows for s in s_rows if pred(r, s))


def rand_rel(rng, tag):
    return [(rng.randrange(5), f"{tag}{i}") for i in range(rng.randrange(0, 14))]


def test_example() -> None:
    # The worked example of the page: M = 5, N = 3, B = 4, so 2 + 2 + 1 pages per block.
    r = [(k, f"r{i}") for i, k in enumerate([1, 4, 2, 2, 5, 3, 1, 4, 6, 2])]
    s = [(k, f"s{i}") for i, k in enumerate([2, 4, 4, 7, 1, 2])]
    out, disk = block_nested_loop_join(paginate(r, 2), paginate(s, 2), 0, 0, 4)
    assert disk.reads == 5 + 3 * 3
    assert Counter(out) == reference(r, s, lambda a, b: a[0] == b[0])
    assert len(out) == 12


def test_edges() -> None:
    out, disk = block_nested_loop_join([], paginate([(1,)], 1), 0, 0, 3)
    assert out == [] and disk.reads == 0
    out, disk = block_nested_loop_join(paginate([(1,), (1,)], 1), [], 0, 0, 3)
    assert out == [] and disk.reads == 2
    with pytest.raises(ValueError):
        block_nested_loop_join([], [], 0, 0, 2)
    # All keys equal: the output is the full product.
    r, s = [(0, i) for i in range(7)], [(0, -i) for i in range(5)]
    out, _ = block_nested_loop_join(paginate(r, 2), paginate(s, 2), 0, 0, 3)
    assert len(out) == 35


def test_against_reference() -> None:
    rng = random.Random(21)
    for _ in range(700):
        r, s = rand_rel(rng, "r"), rand_rel(rng, "s")
        pr, ps, b = rng.randrange(1, 4), rng.randrange(1, 4), rng.randrange(3, 8)
        rp, sp = paginate(r, pr), paginate(s, ps)
        m, n = len(rp), len(sp)
        cost = m + -(-m // (b - 2)) * n
        out, disk = block_nested_loop_join(rp, sp, 0, 0, b)
        assert Counter(out) == reference(r, s, lambda x, y: x[0] == y[0])
        assert disk.reads == cost
        theta = lambda x, y: x[0] < y[0]
        out, disk = block_nested_loop_join(rp, sp, 0, 0, b, pred=theta)
        assert Counter(out) == reference(r, s, theta)
        assert disk.reads == cost


def test_cost_formula_exact() -> None:
    # M = 1000 and N = 500 in the units of the page, B = 102: blocks of 100 pages.
    r = [(i % 50, i) for i in range(1000)]
    s = [(i % 70, i) for i in range(500)]
    _, disk = block_nested_loop_join(paginate(r, 1), paginate(s, 1), 0, 0, 102)
    assert disk.reads == 1000 + 10 * 500 == 6000
    _, disk = block_nested_loop_join(paginate(s, 1), paginate(r, 1), 0, 0, 102)
    assert disk.reads == 500 + 5 * 1000 == 5500
