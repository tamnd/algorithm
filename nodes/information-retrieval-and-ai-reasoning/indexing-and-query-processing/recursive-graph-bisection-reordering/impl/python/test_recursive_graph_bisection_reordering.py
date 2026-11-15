# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/recursive-graph-bisection-reordering/. The authors are listed in prov/7XKMDW.jsonl.

import itertools
import random

from irtoy import DOCS, tokenize
from recursive_graph_bisection_reordering import bisect_order, log_gap_cost, move_cost

EXAMPLE = [s.split() for s in [
    "sort merge", "sort array", "merge array", "hash key",
    "sort merge array", "hash table", "key table", "hash key table",
]]


def direct_cost(docs: list, order: list[int]) -> int:
    """Walk the positions in order and charge each term the bit length of the gap since its last position."""
    last: dict = {}
    total = 0
    for p, d in enumerate(order):
        for t in set(docs[d]):
            total += (p + 1 - last.get(t, 0)).bit_length()
            last[t] = p + 1
    return total


def best_cost(docs: list) -> int:
    return min(log_gap_cost(docs, p) for p in itertools.permutations(range(len(docs))))


def planted(rng: random.Random, k: int, per: int) -> list[set]:
    """k topics of per documents each, 8 terms per document, 20% of the terms from a shared vocabulary, shuffled."""
    docs = []
    for c in range(k):
        for _ in range(per):
            ts: set = set()
            while len(ts) < 8:
                ts.add(("shared", rng.randrange(30)) if rng.random() < 0.2 else (c, rng.randrange(30)))
            docs.append(ts)
    rng.shuffle(docs)
    return docs


def test_example() -> None:
    n = len(EXAMPLE)
    assert log_gap_cost(EXAMPLE, list(range(n))) == 32
    assert bisect_order(EXAMPLE, max_depth=1) == [0, 1, 2, 4, 3, 5, 6, 7]
    assert log_gap_cost(EXAMPLE, [0, 1, 2, 4, 3, 5, 6, 7]) == 29
    order = bisect_order(EXAMPLE)
    assert order == [0, 1, 4, 2, 3, 5, 7, 6]
    assert log_gap_cost(EXAMPLE, order) == 27 == best_cost(EXAMPLE)


def test_move_cost() -> None:
    assert move_cost(0, 0, 4, 4) == 0
    assert abs(move_cost(1, 1, 4, 4) - 2.0) < 1e-12
    assert abs(move_cost(2, 0, 4, 4) - 2 * 0.4150374992788438) < 1e-12


def test_toy_collection_is_a_case_where_it_loses() -> None:
    docs = [tokenize(DOCS[d]) for d in sorted(DOCS)]
    assert log_gap_cost(docs, list(range(8))) == 169
    assert log_gap_cost(docs, bisect_order(docs)) == 178
    assert log_gap_cost(docs, bisect_order(docs, iters=1)) == 164
    assert best_cost(docs) == 148


def test_output_is_a_permutation_and_cost_matches() -> None:
    rng = random.Random(20261122)
    for _ in range(200):
        n = rng.randint(0, 40)
        docs = [set(rng.sample(range(25), rng.randint(0, 7))) for _ in range(n)]
        before = [set(d) for d in docs]
        iters = rng.choice([0, 1, 5, 20])
        leaf = rng.choice([1, 2, 5])
        order = bisect_order(docs, iters=iters, leaf_size=leaf)
        assert sorted(order) == list(range(n))
        assert docs == before
        assert order == bisect_order(docs, iters=iters, leaf_size=leaf)
        for o in (order, list(range(n)), rng.sample(range(n), n)):
            assert log_gap_cost(docs, o) == direct_cost(docs, o)
        if iters == 0:
            assert order == list(range(n))


def test_depth_and_leaf_limits() -> None:
    rng = random.Random(5)
    for n in range(2, 30):
        docs = [set(rng.sample(range(10), 3)) for _ in range(n)]
        assert bisect_order(docs, max_depth=0) == list(range(n))
        assert bisect_order(docs, leaf_size=n) == list(range(n))
        half = (n + 1) // 2
        one = bisect_order(docs, max_depth=1)
        full = bisect_order(docs)
        # deeper levels only reorder documents inside the halves of the first level
        assert sorted(full[:half]) == sorted(one[:half]) and sorted(full[half:]) == sorted(one[half:])


def test_planted_topics_lower_the_cost() -> None:
    for seed in range(8):
        rng = random.Random(seed)
        docs = planted(rng, rng.choice([2, 4, 8]), rng.choice([8, 16]))
        n = len(docs)
        assert log_gap_cost(docs, bisect_order(docs)) < log_gap_cost(docs, list(range(n)))


def test_no_guarantee_on_random_input() -> None:
    rng = random.Random(1000)
    worse = 0
    for _ in range(100):
        n = rng.randint(2, 30)
        docs = [set(rng.sample(range(20), rng.randint(1, 6))) for _ in range(n)]
        if log_gap_cost(docs, bisect_order(docs)) > log_gap_cost(docs, list(range(n))):
            worse += 1
    assert worse > 0


def test_edge_cases() -> None:
    assert bisect_order([]) == [] and log_gap_cost([], []) == 0
    assert bisect_order([["a"]]) == [0] and log_gap_cost([["a"]], [0]) == 1
    assert sorted(bisect_order([[], [], []])) == [0, 1, 2]
    for kw in ({"leaf_size": 0}, {"iters": -1}):
        try:
            bisect_order([["a"]], **kw)
        except ValueError:
            pass
        else:
            raise AssertionError("bad parameter was accepted")
