# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/join-index/. The authors are listed in prov/8DK147.jsonl.

import random
from collections import Counter
from math import ceil

import pytest

from join_index import JoinIndex


def reference(ji):
    return Counter(r + s for r in ji.r.values() for s in ji.s.values() if r[0] == s[0])


def test_example() -> None:
    ji = JoinIndex(0, 0, per_page=2, pairs_per_page=4)
    for k in [10, 20, 10, 30]:
        ji.insert_r((k, "r"))
    for k in [20, 10, 40]:
        ji.insert_s((k, "s"))
    assert ji.pairs() == {(0, 1), (1, 0), (2, 1)}
    ji.check_invariant()
    out, ios = ji.join()
    assert Counter(out) == reference(ji)
    # 1 page of pairs, R pages 0 and 1, S page 0.
    assert ios == 1 + 2 + 1
    ji.delete_s(1)
    assert ji.pairs() == {(1, 0)}
    ji.insert_r((40, "r"))
    assert ji.pairs() == {(1, 0), (4, 2)}
    ji.check_invariant()


def test_edges() -> None:
    ji = JoinIndex(0, 0)
    assert ji.join() == ([], 0)
    with pytest.raises(KeyError):
        ji.delete_r(0)
    with pytest.raises(ValueError):
        JoinIndex(0, 0, per_page=0)
    rid = ji.insert_r((1,))
    ji.delete_r(rid)
    with pytest.raises(KeyError):
        ji.delete_r(rid)
    ji.check_invariant()


def test_random_operations_against_model() -> None:
    rng = random.Random(91)
    for _ in range(60):
        ji = JoinIndex(0, 0, per_page=rng.randrange(1, 4), pairs_per_page=rng.randrange(1, 5))
        for _ in range(rng.randrange(1, 60)):
            op = rng.random()
            if op < 0.3:
                ji.insert_r((rng.randrange(5), rng.randrange(100)))
            elif op < 0.6:
                ji.insert_s((rng.randrange(5), rng.randrange(100)))
            elif op < 0.8 and ji.r:
                ji.delete_r(rng.choice(sorted(ji.r)))
            elif ji.s:
                ji.delete_s(rng.choice(sorted(ji.s)))
            ji.check_invariant()
            out, ios = ji.join()
            assert Counter(out) == reference(ji)
            pairs = ji.pairs()
            want = (ceil(len(pairs) / ji.pairs_per_page)
                    + len({rid // ji.per_page for rid, _ in pairs})
                    + len({sid // ji.per_page for _, sid in pairs}))
            assert ios == want


def test_matches_of_r() -> None:
    ji = JoinIndex(0, 1)
    a = ji.insert_r((7, "a"))
    b = ji.insert_r((8, "b"))
    x = ji.insert_s(("x", 7))
    y = ji.insert_s(("y", 7))
    assert ji.matches_of_r(a) == {x, y} and ji.matches_of_r(b) == set()
