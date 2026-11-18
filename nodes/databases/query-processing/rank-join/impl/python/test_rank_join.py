# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rank-join/. The authors are listed in prov/TEN8RX.jsonl.

import operator
import random
from collections import Counter

import pytest

from dbrel import Relation, evaluate
from rank_join import rank_join

FUNCS = (operator.add, lambda x, y: 2 * x + y, min, max, lambda x, y: x * y)


def oracle(left, right):
    """The bag join by dbrel, as a Counter of (key, score_l, id_l, score_r, id_r)."""
    db = {"L": Relation(("k", "sl", "il"), left), "R": Relation(("k", "sr", "ir"), right)}
    res = evaluate(("join", ("scan", "L"), ("scan", "R")), db).reorder(("k", "sl", "il", "sr", "ir"))
    return Counter(res.rows)


def flat(out):
    return Counter((l[0], l[1], l[2], r[1], r[2]) for _, l, r in out)


def test_example() -> None:
    left = [("a", 10, 0), ("b", 8, 1), ("c", 5, 2), ("a", 3, 3), ("b", 1, 4)]
    right = [("b", 9, 0), ("a", 7, 1), ("c", 6, 2), ("b", 2, 3)]
    out, stats = rank_join(left, right, 2)
    assert [s for s, _, _ in out] == [17, 17] and stats["depth"] == [2, 2]
    assert stats["thresholds"] == [19, 19, 19, 17]
    out, stats = rank_join(left, right, 3)
    assert [s for s, _, _ in out] == [17, 17, 11] and stats["depth"] == [5, 4]
    assert stats["thresholds"] == [19, 19, 19, 17, 17, 16, 16, 12, float("-inf")]


def test_paper_thresholds() -> None:
    # Scores of Ilyas et al.: reading 3 + 3 gives T = 108, the HRJN* rule
    # reads 2 + 4 and gives T = 105. No keys match, so nothing is output.
    left = [(f"l{i}", s, i) for i, s in enumerate([100, 50, 25, 10, 1])]
    right = [(f"r{i}", s, i) for i, s in enumerate([10, 9, 8, 5, 1])]
    _, alt = rank_join(left, right, None, strategy="alternate")
    _, ada = rank_join(left, right, None, strategy="adaptive")
    assert alt["thresholds"][5] == 108 and ada["thresholds"][5] == 105
    assert alt["thresholds"][:6] == [110, 110, 110, 109, 109, 108]
    assert ada["thresholds"][:6] == [110, 110, 110, 109, 108, 105]


def test_random_against_oracle() -> None:
    rng = random.Random(11)
    for trial in range(150):
        dom = rng.choice([3, 4, 5])
        keys = list(range(dom)) + [None]
        left = sorted(((rng.choice(keys), rng.randrange(10), i) for i in range(rng.randrange(0, 25))),
                      key=lambda t: -t[1])
        right = sorted(((rng.choice(keys), rng.randrange(10), i) for i in range(rng.randrange(0, 25))),
                       key=lambda t: -t[1])
        f = FUNCS[trial % len(FUNCS)]
        want = oracle(left, right)
        ranked = sorted((f(sl, sr) for (_, sl, _, sr, _), c in want.items() for _ in range(c)), reverse=True)
        for strategy in ("alternate", "adaptive"):
            full, _ = rank_join(left, right, None, f, strategy)
            assert flat(full) == want
            assert [s for s, _, _ in full] == ranked
            for k in (1, 2, 5):
                out, stats = rank_join(left, right, k, f, strategy)
                assert [s for s, _, _ in out] == ranked[:k]
                assert not flat(out) - want
                assert all(s == f(l[1], r[1]) for s, l, r in out)
                assert stats["depth"][0] <= len(left) and stats["depth"][1] <= len(right)


def test_edges() -> None:
    assert rank_join([], [("a", 1, 0)], 3)[0] == []
    assert rank_join([("a", 1, 0)], [], 3)[0] == []
    assert rank_join([("a", 1, 0)], [("a", 2, 0)], 0)[0] == []
    out, _ = rank_join([("a", 1, 0)], [("a", 2, 0)], 5)
    assert out == [(3, ("a", 1, 0), ("a", 2, 0))]
    same_l = [("x", 5 - i, i) for i in range(4)]
    same_r = [("x", 5 - i, i) for i in range(3)]
    out, _ = rank_join(same_l, same_r, None)
    assert len(out) == 12 and out[0][0] == 10
    assert rank_join([(None, 3, 0)], [(None, 3, 0)], None)[0] == []
    with pytest.raises(ValueError):
        rank_join([("a", 1, 0), ("a", 2, 1)], [("a", 1, 0)], 1)


def test_early_stop_on_correlated_input() -> None:
    # When high scores join, the operator reads only a prefix of each input.
    left = [(i % 4, 200 - i, i) for i in range(200)]
    right = [(i % 4, 200 - i, i) for i in range(200)]
    out, stats = rank_join(left, right, 3)
    assert [s for s, _, _ in out] == [400, 398, 396]
    assert max(stats["depth"]) <= 10
