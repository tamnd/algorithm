# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gallager-humblet-spira/. The authors are listed in prov/2BCNZB.jsonl.

import math
import random

from gallager_humblet_spira import ghs, kruskal, random_connected_graph

EXAMPLE = [(0, 1, 3), (1, 2, 1), (2, 3, 6), (3, 4, 2), (4, 5, 5), (0, 5, 4), (1, 4, 7), (2, 5, 8)]


def bound(n: int, m: int) -> float:
    return 5 * n * math.log2(n) + 2 * m


def test_example() -> None:
    st = ghs(6, EXAMPLE, schedule="unit")
    assert st["mst"] == {1, 2, 3, 4, 5}
    assert st["messages"] == 54
    assert st["by_type"] == {"Connect": 8, "Initiate": 12, "Test": 12, "Reject": 3, "Accept": 5, "Report": 12, "Change-root": 2}
    assert st["time"] == 19.0
    assert sorted(st["halted"]) == [4, 5]  # the ends of the final core, weight 5
    assert st["levels"] == [2] * 6


def test_two_nodes() -> None:
    st = ghs(2, [(0, 1, 7)])
    assert st["mst"] == {7}
    # Connect, Initiate and Report, each once in each direction
    assert st["by_type"] == {"Connect": 2, "Initiate": 2, "Report": 2}
    assert sorted(st["halted"]) == [0, 1]


def test_path_and_cycle() -> None:
    n = 8
    path = [(i, i + 1, 10 - i) for i in range(n - 1)]
    assert ghs(n, path)["mst"] == kruskal(n, path)
    cycle = path + [(n - 1, 0, 100)]
    st = ghs(n, cycle, schedule="unit")
    assert st["mst"] == kruskal(n, cycle) and 100 not in st["mst"]


def test_against_kruskal_random_schedules() -> None:
    rng = random.Random(2024)
    for trial in range(450):
        n = rng.randrange(2, 24)
        g = random_connected_graph(n, rng.randrange(0, n * (n - 1) // 2 - n + 2), rng)
        schedule = ("random", "unit", "slowlow")[trial % 3]
        wake = None if trial % 2 else rng.sample(range(n), rng.randrange(1, n + 1))
        st = ghs(n, g, seed=trial, wake=wake, schedule=schedule)
        assert st["mst"] == kruskal(n, g)
        assert st["messages"] <= bound(n, len(g))
        assert sorted(st["halted"]) != [] and len(st["halted"]) == 2
        assert max(st["levels"]) <= math.log2(n)
        # each message holds one weight, one level and a type: O(log n) bits
        assert st["max_bits"] <= 8 * math.ceil(math.log2(n + 1)) + 16


def test_time_when_all_wake() -> None:
    rng = random.Random(7)
    for trial in range(60):
        n = rng.randrange(2, 30)
        g = random_connected_graph(n, rng.randrange(0, 2 * n), rng)
        st = ghs(n, g, seed=trial, schedule=("random", "unit")[trial % 2])
        assert st["time"] <= 5 * n * math.log2(n)


def test_one_node_wakes() -> None:
    rng = random.Random(11)
    for trial in range(60):
        n = rng.randrange(2, 20)
        g = random_connected_graph(n, rng.randrange(0, n), rng)
        st = ghs(n, g, seed=trial, wake=[rng.randrange(n)])
        assert st["mst"] == kruskal(n, g)
        assert st["messages"] <= bound(n, len(g))
