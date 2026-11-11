# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-mst/. The authors are listed in prov/59V4HH.jsonl.

import math
import random

from distributed_mst import budget, distributed_mst, kruskal, random_connected_graph

EXAMPLE = [(0, 1, 3), (1, 2, 1), (2, 3, 6), (3, 4, 2), (4, 5, 5), (0, 5, 4), (1, 4, 7), (2, 5, 8)]


def test_example() -> None:
    st = distributed_mst(6, EXAMPLE)
    assert st["mst"] == {1, 2, 3, 4, 5}
    # phase 1 joins the MOEs 3, 1, 2 and 4: fragments {0, 1, 2, 5} and {3, 4}
    assert st["fragments"] == [2, 1, 1]
    assert st["rounds"] == 3 * (3 * 6 + 2)


def test_against_kruskal() -> None:
    rng = random.Random(5)
    for _ in range(120):
        n = rng.randrange(2, 22)
        g = random_connected_graph(n, rng.randrange(0, 2 * n), rng)
        st = distributed_mst(n, g)
        assert st["mst"] == kruskal(n, g)
        phases = math.ceil(math.log2(n))
        assert st["rounds"] == phases * (3 * n + 2)
        # per phase: 2m ids, at most n - 1 up, n - 1 down, n connects, n - 1 floods
        assert st["messages"] <= phases * (2 * len(g) + 4 * n)
        assert st["max_bits"] <= budget(n)
        # the number of fragments at least halves in each phase
        prev = n
        for f in st["fragments"]:
            assert f <= max(1, prev // 2)
            prev = f
        assert st["fragments"][-1] == 1


def test_path_needs_log_phases() -> None:
    # on a path with increasing weights each fragment pairs up with a neighbour
    n = 16
    path = [(i, i + 1, i + 1) for i in range(n - 1)]
    st = distributed_mst(n, path)
    assert st["mst"] == set(range(1, n))
    assert st["fragments"][-1] == 1
