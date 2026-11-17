# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nested-loop-join/. The authors are listed in prov/V6PA3X.jsonl.

import random
from collections import Counter

import pytest

from nested_loop_join import equi, nested_loop_join, paginate


def reference(r_rows, s_rows, pred):
    return Counter(r + s for r in r_rows for s in s_rows if pred(r, s))


def rand_rel(rng, tag):
    n = rng.randrange(0, 13)
    return [(rng.randrange(5), f"{tag}{i}") for i in range(n)]


def test_example() -> None:
    r = [(1, "a"), (2, "b"), (2, "c"), (3, "d")]
    s = [(2, "x"), (3, "y"), (2, "z")]
    rp, sp = paginate(r, 2), paginate(s, 2)
    out, disk = nested_loop_join(rp, sp, equi(0, 0), "tuple")
    assert Counter(out) == Counter([(2, "b", 2, "x"), (2, "b", 2, "z"), (2, "c", 2, "x"),
                                    (2, "c", 2, "z"), (3, "d", 3, "y")])
    assert disk.reads == 2 + 4 * 2
    out, disk = nested_loop_join(rp, sp, equi(0, 0), "page")
    assert len(out) == 5 and disk.reads == 2 + 2 * 2


def test_empty_inputs() -> None:
    for mode in ("tuple", "page"):
        out, disk = nested_loop_join([], paginate([(1,)], 1), equi(0, 0), mode)
        assert out == [] and disk.reads == 0
        out, disk = nested_loop_join(paginate([(1,), (2,)], 1), [], equi(0, 0), mode)
        assert out == [] and disk.reads == 2
    with pytest.raises(ValueError):
        nested_loop_join([], [], equi(0, 0), "block")


def test_against_reference() -> None:
    rng = random.Random(14)
    preds = [equi(0, 0), lambda r, s: r[0] < s[0], lambda r, s: abs(r[0] - s[0]) <= 1]
    for _ in range(600):
        r, s = rand_rel(rng, "r"), rand_rel(rng, "s")
        pr, ps = rng.randrange(1, 4), rng.randrange(1, 4)
        pred = rng.choice(preds)
        want = reference(r, s, pred)
        for mode in ("tuple", "page"):
            out, disk = nested_loop_join(paginate(r, pr), paginate(s, ps), pred, mode)
            assert Counter(out) == want
            m, n = len(paginate(r, pr)), len(paginate(s, ps))
            assert disk.reads == (m + len(r) * n if mode == "tuple" else m + m * n)


def test_cost_formula_exact() -> None:
    # M = 6 pages of p = 4 tuples, N = 5 pages: M + p M N = 126 and M + M N = 36.
    r = [(i % 7, i) for i in range(24)]
    s = [(i % 5, i) for i in range(15)]
    out_t, d_t = nested_loop_join(paginate(r, 4), paginate(s, 3), equi(0, 0), "tuple")
    out_p, d_p = nested_loop_join(paginate(r, 4), paginate(s, 3), equi(0, 0), "page")
    assert d_t.reads == 126 and d_p.reads == 36
    assert Counter(out_t) == Counter(out_p)
    # Swapping the roles: S outer, M = 5, N = 6: page mode costs 5 + 30 = 35 < 36.
    _, d_swap = nested_loop_join(paginate(s, 3), paginate(r, 4), equi(0, 0), "page")
    assert d_swap.reads == 35
