# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-streaming-matching/. The authors are listed in prov/ZQCPTZ.jsonl.

import random

from greedy_streaming_matching import GreedyMatching, greedy_matching, is_maximal, maximum_matching_size

STREAM = [(2, 3), (1, 2), (3, 4), (5, 6), (4, 5), (1, 6)]


def test_worked_example() -> None:
    g = GreedyMatching()
    taken = [g.process(u, v) for u, v in STREAM]
    assert taken == [True, False, False, True, False, False]
    assert g.matching == [(2, 3), (5, 6)]
    g.check_invariant()
    assert is_maximal(g.matching, STREAM)
    assert maximum_matching_size(STREAM) == 3  # the 6-cycle has a perfect matching


def test_ratio_one_half_is_tight() -> None:
    path = [(2, 3), (1, 2), (3, 4)]
    assert greedy_matching(path) == [(2, 3)]
    assert maximum_matching_size(path) == 2
    # k disjoint copies keep the ratio exactly 1/2
    k = 5
    stream = []
    for c in range(k):
        a, b, x, y = 4 * c + 1, 4 * c + 2, 4 * c + 3, 4 * c + 4
        stream += [(b, x), (a, b), (x, y)]
    assert len(greedy_matching(stream)) == k and maximum_matching_size(stream) == 2 * k


def test_edges() -> None:
    assert greedy_matching([]) == []
    assert greedy_matching([(1, 2)]) == [(1, 2)]
    assert greedy_matching([(1, 2), (2, 1), (1, 2)]) == [(1, 2)]  # repeats are ignored
    star = [(0, i) for i in range(1, 8)]
    assert greedy_matching(star) == [(0, 1)] and maximum_matching_size(star) == 1
    try:
        GreedyMatching().process(3, 3)
        raise AssertionError("self-loop accepted")
    except ValueError:
        pass


def test_random_graphs_against_brute_force() -> None:
    rng = random.Random(2005)
    for _ in range(600):
        n = rng.randint(1, 9)
        p = rng.choice([0.2, 0.4, 0.7])
        edges = [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < p]
        rng.shuffle(edges)
        edges = [(v, u) if rng.random() < 0.5 else (u, v) for u, v in edges]
        g = GreedyMatching()
        for u, v in edges:
            g.process(u, v)
        g.check_invariant()
        opt = maximum_matching_size(edges)
        assert is_maximal(g.matching, edges)
        assert 2 * len(g.matching) >= opt >= len(g.matching)
        assert len(g.matching) <= n // 2


def test_every_order_of_one_graph() -> None:
    # All 720 orders of the 6-cycle: greedy gets 2 or 3 edges, never fewer than OPT / 2.
    import itertools

    sizes = {len(greedy_matching(order)) for order in itertools.permutations(STREAM)}
    assert sizes == {2, 3}
