# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/diff3/. The authors are listed in prov/8YT0S8.jsonl.

import random

from diff3 import (CHANGED_A, CHANGED_B, CONFLICT, FALSE_CONFLICT, STABLE, UNCHANGED, diff3_merge, diff3_output,
                   diff3_parse)
from txdiff import lcs_matching

# Figure 1 of Khanna, Kunal and Pierce, with the matchings of GNU diff3.
A1, O1, B1 = [1, 4, 5, 2, 3, 6], [1, 2, 3, 4, 5, 6], [1, 2, 4, 5, 3, 6]
MA1 = [(0, 0), (1, 3), (2, 4), (5, 5)]
MB1 = [(0, 0), (1, 1), (3, 2), (4, 3), (5, 5)]


def test_figure_1() -> None:
    chunks = diff3_parse(A1, O1, B1, MA1, MB1)
    assert [(c.kind, c.a, c.o, c.b) for c in chunks] == [
        (STABLE, [1], [1], [1]),
        (CHANGED_A, [4, 5], [], []),
        (STABLE, [2], [2], [2]),
        (CONFLICT, [3], [3, 4, 5], [4, 5, 3]),
        (STABLE, [6], [6], [6]),
    ]
    assert diff3_output(chunks) == ([1, 4, 5, 2, 3, 6], [1, 4, 5, 2, 3, 4, 5, 6], [1, 4, 5, 2, 4, 5, 3, 6])
    merged, conflicts = diff3_merge(A1, O1, B1, MA1, MB1)
    assert conflicts == 1
    assert merged == [1, 4, 5, 2, "<<<<<<< A", 3, "||||||| O", 3, 4, 5, "=======", 4, 5, 3, ">>>>>>> B", 6]


def test_the_matching_changes_the_result() -> None:
    # The helper takes another longest matching of O and A: 1, 4, 5, 6 instead of 1, 2, 3, 6.
    ma = lcs_matching(O1, A1)
    assert ma == [(0, 0), (3, 1), (4, 2), (5, 5)] and len(ma) == len(MA1)
    chunks = diff3_parse(A1, O1, B1, ma, MB1)
    assert [c.kind for c in chunks] == [STABLE, CONFLICT, STABLE, CONFLICT, STABLE]
    assert chunks[2].o == [4, 5]
    assert diff3_merge(A1, O1, B1, ma, MB1)[1] == 2


def test_not_idempotent() -> None:
    # Figure 4: each pair of files has one maximum matching, and a second run changes the result.
    a, o, b = [1, 2, 4, 6, 8], [1, 2, 3, 4, 5, 5, 5, 6, 7, 8], [1, 4, 5, 5, 5, 6, 2, 3, 4, 8]
    first = diff3_output(diff3_parse(a, o, b))
    assert first == ([1, 2, 4, 6, 8], [1, 2, 3, 4, 6, 7, 8], [1, 4, 6, 2, 3, 4, 8])
    second = diff3_output(diff3_parse(*first))
    assert second == ([1, 4, 6, 2, 4, 6, 8], [1, 4, 6, 2, 4, 6, 7, 8], [1, 4, 6, 2, 4, 8])


def test_locality() -> None:
    # Figure 3: A edits the start and B edits the end, yet there is a conflict for every n.
    for n in (1, 3, 6):
        o2 = [1, 2] * n
        a, o, b = [1, 2] + o2 + [1, 2], o2 + [1, 2], o2 + [3]
        assert lcs_matching(o, a) == [(k, k) for k in range(2 * n + 2)]  # the matching of the paper
        chunks = diff3_parse(a, o, b)
        assert [(c.kind, c.a, c.o, c.b) for c in chunks] == [(STABLE, o2, o2, o2), (CONFLICT, [1, 2, 1, 2], [1, 2], [3])]
        # Theorem 4.1.1: a line that occurs once in each file, in the middle part, removes the conflict.
        o2 = [1, 2] * n + [9] + [1, 2] * n
        a, o, b = [1, 2] + o2 + [1, 2], o2 + [1, 2], o2 + [3]
        assert diff3_merge(a, o, b) == ([1, 2] + o2 + [3], 0)


def test_page_examples() -> None:
    o = ["a", "b", "c"]
    assert diff3_merge(["a", "x", "b", "c"], o, ["a", "b", "c", "y"]) == (["a", "x", "b", "c", "y"], 0)
    merged, conflicts = diff3_merge(["a", "p", "c"], o, ["a", "q", "c"])
    assert conflicts == 1
    assert merged == ["a", "<<<<<<< A", "p", "||||||| O", "b", "=======", "q", ">>>>>>> B", "c"]
    # The same change on both sides is a false conflict, and the merge takes it.
    chunks = diff3_parse(["a", "z", "c"], o, ["a", "z", "c"])
    assert [c.kind for c in chunks] == [STABLE, FALSE_CONFLICT, STABLE]
    assert diff3_merge(["a", "z", "c"], o, ["a", "z", "c"]) == (["a", "z", "c"], 0)
    # A deletion on one side and no change on the other.
    assert diff3_merge(["a", "c"], o, o) == (["a", "c"], 0)
    assert [c.kind for c in diff3_parse(o, o, ["a", "c"])] == [STABLE, CHANGED_B, STABLE]
    assert diff3_merge([], [], []) == ([], 0)


def test_bad_matching() -> None:
    for ma in ([(1, 0)], [(0, 0), (0, 1)], [(3, 3)]):
        try:
            diff3_parse(["x", "y"], ["x", "y"], ["x", "y"], ma, None)
        except ValueError:
            continue
        raise AssertionError(f"{ma} was accepted")


def _edit(rng: random.Random, s: list[str]) -> list[str]:
    t = list(s)
    for _ in range(rng.randint(0, 3)):
        k = rng.randint(0, len(t))
        if t and rng.random() < 0.5:
            del t[min(k, len(t) - 1)]
        else:
            t.insert(k, rng.choice("abcxy"))
    return t


def _check_parse(a: list[str], o: list[str], b: list[str], ma: list[tuple[int, int]],
                 mb: list[tuple[int, int]]) -> None:
    chunks = diff3_parse(a, o, b, ma, mb)
    assert sum((c.a for c in chunks), []) == a
    assert sum((c.o for c in chunks), []) == o
    assert sum((c.b for c in chunks), []) == b
    triples = set()
    pa = po = pb = 0
    for k, c in enumerate(chunks):
        assert c.a or c.o or c.b
        if c.kind == STABLE:
            assert c.a == c.o == c.b
            triples |= {(po + t, pa + t, pb + t) for t in range(len(c.o))}
            # Each stable chunk is as large as possible: the next chunk is not stable.
            assert k + 1 == len(chunks) or chunks[k + 1].kind != STABLE
        pa, po, pb = pa + len(c.a), po + len(c.o), pb + len(c.b)
    a_of, b_of = dict(ma), dict(mb)
    both = {(x, a_of[x], b_of[x]) for x in a_of if x in b_of}
    assert both <= triples  # property (I) of a diff3 parse


def test_random_parses() -> None:
    rng = random.Random(8)
    for _ in range(400):
        o = [rng.choice("abc") for _ in range(rng.randint(0, 7))]
        a, b = _edit(rng, o), _edit(rng, o)
        ma, mb = lcs_matching(o, a), lcs_matching(o, b)
        _check_parse(a, o, b, ma, mb)
        assert UNCHANGED not in [c.kind for c in diff3_parse(a, o, b, ma, mb)]
        # Any increasing matchings give a parse, also ones that are not maximum.
        sub_a = [p for p in ma if rng.random() < 0.6]
        sub_b = [p for p in mb if rng.random() < 0.6]
        _check_parse(a, o, b, sub_a, sub_b)
        for x, y in ((sub_a, sub_b), (ma, mb)):
            # One side unchanged: the merge is the other side.
            assert diff3_merge(o, o, b, None, y) == (b, 0)
            assert diff3_merge(a, o, o, x, None) == (a, 0)
            # The same change on both sides with the same matching: the merge is that change.
            assert diff3_merge(a, o, a, x, x) == (a, 0)
