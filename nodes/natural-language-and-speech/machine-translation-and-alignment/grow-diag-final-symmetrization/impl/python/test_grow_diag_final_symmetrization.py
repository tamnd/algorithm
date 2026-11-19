# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/grow-diag-final-symmetrization/. The authors are listed in prov/00FY52.jsonl.

import random

import pytest

from grow_diag_final_symmetrization import (
    NEIGHBOURS_DIAG,
    grow_diag_final,
    grow_diag_final_and,
    links_from_alignment,
    links_from_reverse,
)


def reference(a1, a2, m, l, diag=True, final=True, final_and=False, outer_j=False):
    """A second, plain version of the Moses pseudocode: sets only, and the
    alignment status of a word is found by a scan of the current set."""
    union = a1 | a2
    A = set(a1 & a2)

    def src_free(j):
        return all(p[0] != j for p in A)

    def tgt_free(i):
        return all(p[1] != i for p in A)

    def cells():
        if outer_j:
            return [(j, i) for j in range(1, m + 1) for i in range(1, l + 1)]
        return [(j, i) for i in range(1, l + 1) for j in range(1, m + 1)]

    nb = NEIGHBOURS_DIAG if diag else NEIGHBOURS_DIAG[:4]
    changed = True
    while changed:
        changed = False
        for j, i in cells():
            if (j, i) in A:
                for di, dj in nb:
                    p = (j + dj, i + di)
                    if p in union and (src_free(p[0]) or tgt_free(p[1])):
                        A.add(p)
                        changed = True
    if final:
        for b in (a1, a2):
            for j, i in cells():
                if (j, i) in b:
                    if final_and:
                        ok = src_free(j) and tgt_free(i)
                    else:
                        ok = src_free(j) or tgt_free(i)
                    if ok:
                        A.add((j, i))
    return A


def random_pair(rng, m, l, null=0.2):
    a = [0 if rng.random() < null else rng.randint(1, l) for _ in range(m)]
    b = [0 if rng.random() < null else rng.randint(1, m) for _ in range(l)]
    return links_from_alignment(a), links_from_reverse(b)


def test_worked_example() -> None:
    # f = ich gehe nicht nach hause, e = i do not go home
    a1 = links_from_alignment([1, 4, 3, 5, 5])
    a2 = links_from_reverse([1, 2, 3, 2, 5])
    assert a1 & a2 == {(1, 1), (2, 4), (3, 3), (5, 5)}
    assert grow_diag_final(a1, a2, 5, 5, diag=False, final=False) == a1 & a2 | {(4, 5)}
    assert grow_diag_final(a1, a2, 5, 5, final=False) == a1 & a2 | {(2, 2), (4, 5)}
    assert grow_diag_final(a1, a2, 5, 5) == a1 | a2


def test_variants_differ() -> None:
    a1 = links_from_alignment([2, 4, 3, 1, 4])
    a2 = links_from_reverse([5, 1, 1, 2, 1])
    inter = {(1, 2), (2, 4)}
    assert a1 & a2 == inter
    assert grow_diag_final(a1, a2, 5, 5, diag=False, final=False) == inter | {(1, 3)}
    gd = grow_diag_final(a1, a2, 5, 5, final=False)
    assert gd == inter | {(1, 3), (1, 5), (3, 3)}
    assert grow_diag_final_and(a1, a2, 5, 5) == gd | {(4, 1)}
    assert grow_diag_final(a1, a2, 5, 5) == gd | {(4, 1), (5, 4)}
    assert (a1 | a2) - grow_diag_final(a1, a2, 5, 5) == {(5, 1)}


def test_loop_order_matters() -> None:
    a1 = links_from_alignment([3, 2, 1, 1])
    a2 = links_from_reverse([4, 4, 1])
    out = grow_diag_final(a1, a2, 4, 3, final=False)
    assert out == {(1, 3), (2, 2), (3, 1), (4, 1), (4, 2)}
    assert out == reference(a1, a2, 4, 3, final=False)
    # with the source positions in the outer loop, (4, 2) is not added
    assert reference(a1, a2, 4, 3, final=False, outer_j=True) == out - {(4, 2)}


def test_against_reference() -> None:
    rng = random.Random(17)
    for _ in range(400):
        m, l = rng.randint(1, 7), rng.randint(1, 7)
        a1, a2 = random_pair(rng, m, l)
        for kw in ({}, {"diag": False}, {"final": False}, {"final_and": True}):
            assert grow_diag_final(a1, a2, m, l, **kw) == reference(a1, a2, m, l, **kw)


def test_bounds_and_coverage() -> None:
    rng = random.Random(23)
    for _ in range(400):
        m, l = rng.randint(1, 8), rng.randint(1, 8)
        a1, a2 = random_pair(rng, m, l)
        union = a1 | a2
        out = grow_diag_final(a1, a2, m, l)
        assert a1 & a2 <= out <= union
        # every word with a link in either direction is aligned at the end
        assert {j for j, _ in union} == {j for j, _ in out}
        assert {i for _, i in union} == {i for _, i in out}
        # grow-diag-final-and starts from the same grown set; it is not always a subset of
        # grow-diag-final, because a link that one final step adds can block another
        gd = grow_diag_final(a1, a2, m, l, final=False)
        gdfa = grow_diag_final_and(a1, a2, m, l)
        assert gd <= gdfa <= union
        assert gd <= out


def test_fixed_point_of_growing() -> None:
    rng = random.Random(29)
    for _ in range(300):
        m, l = rng.randint(1, 8), rng.randint(1, 8)
        a1, a2 = random_pair(rng, m, l)
        out = grow_diag_final(a1, a2, m, l, final=False)
        src = {j for j, _ in out}
        tgt = {i for _, i in out}
        for j, i in out:
            for di, dj in NEIGHBOURS_DIAG:
                p = (j + dj, i + di)
                if p in a1 | a2:
                    assert p[0] in src and p[1] in tgt


def test_edges() -> None:
    assert grow_diag_final(set(), set(), 3, 3) == set()
    a = {(1, 1), (2, 2)}
    assert grow_diag_final(a, a, 2, 2) == a
    # one direction only: the final step adds all of it here
    assert grow_diag_final({(1, 2), (2, 1)}, set(), 2, 2) == {(1, 2), (2, 1)}
    with pytest.raises(ValueError):
        grow_diag_final({(0, 1)}, set(), 2, 2)
    assert links_from_alignment([0, 2, 1]) == {(2, 2), (3, 1)}
    assert links_from_reverse([3, 0]) == {(3, 1)}
