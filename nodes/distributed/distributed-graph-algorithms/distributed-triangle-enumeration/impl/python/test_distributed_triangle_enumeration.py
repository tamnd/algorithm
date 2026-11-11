# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-triangle-enumeration/. The authors are listed in prov/7GRAF4.jsonl.

import math
import random
from collections import Counter

from distributed_triangle_enumeration import (
    brute_triangles,
    clique_triangles,
    cube_root,
    schedule,
)

EXAMPLE = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3), (4, 5), (5, 7), (4, 7), (3, 4)]


def round_bound(n: int) -> int:
    """2 ceil((ceil(1.5 s (s + 1) / n) + 1) / B), with s = ceil(n / q): O(n^(1/3) / log n)."""
    q = cube_root(n)
    s = -(-n // q)
    b = max(1, math.ceil(math.log2(n)))
    cap = -(-(3 * s * (s + 1) // 2) // n) + 1
    return 2 * -(-cap // b)


def check(n: int, edges: list[tuple[int, int]]) -> dict:
    st = clique_triangles(n, edges)
    listed = [tri for tri, _ in st["triangles"]]
    assert len(listed) == len(set(listed))  # each triangle once
    assert set(listed) == brute_triangles(n, edges)  # and all of them
    q = st["q"]
    for (x, y, z), t in st["triangles"]:
        assert t == (x % q) * q * q + (y % q) * q + z % q  # by the node of its triple
    m1, m2 = st["max_load"]
    assert m1 <= st["cap"] and m2 <= st["cap"]
    assert st["total_rounds"] <= round_bound(n)
    return st


def test_example() -> None:
    st = check(8, EXAMPLE)
    assert sorted(st["triangles"]) == [((0, 1, 2), 2), ((0, 1, 3), 3), ((0, 2, 3), 1), ((1, 2, 3), 5), ((4, 5, 7), 3)]
    assert (st["q"], st["B"], st["cap"], st["rounds"]) == (2, 3, 4, (1, 2))


def test_random_graphs_match_brute_force() -> None:
    rng = random.Random(2)
    for _ in range(60):
        n = rng.randrange(1, 45)
        p = rng.choice([0.1, 0.3, 0.6, 0.9])
        check(n, [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < p])


def test_node_loads() -> None:
    # each node sends and receives at most 1.5 s (s + 1) bits, with s = ceil(n / q)
    for n in list(range(2, 70)) + [100, 125]:
        q = cube_root(n)
        s = -(-n // q)
        out: Counter = Counter()
        inn: Counter = Counter()
        for (x, t), pairs in schedule(n).items():
            out[x] += len(pairs)
            inn[t] += len(pairs)
        assert max(out.values(), default=0) <= 1.5 * s * (s + 1)
        assert max(inn.values(), default=0) <= 1.5 * s * (s + 1)


def test_rounds_on_complete_graphs() -> None:
    # the schedule does not depend on the input, so neither do the rounds
    for n in (27, 64, 125):
        complete = [(u, v) for u in range(n) for v in range(u + 1, n)]
        st = check(n, complete)
        assert len(st["triangles"]) == math.comb(n, 3)
        assert st["total_rounds"] <= round_bound(n)
        assert st["rounds"] == clique_triangles(n, [])["rounds"]
