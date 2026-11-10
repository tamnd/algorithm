# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ullman-yannakakis/. The authors are listed in prov/BAM5EM.jsonl.

import math
import random

from ullman_yannakakis import Cost, ullman_yannakakis


def closure_by_search(n: int, edges: list[tuple[int, int]]) -> list[int]:
    """Sequential reference: one search with an explicit stack from each vertex."""
    out: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        out[u].append(v)
    rows = []
    for s in range(n):
        seen = 1 << s
        stack = [s]
        while stack:
            u = stack.pop()
            for v in out[u]:
                if not seen >> v & 1:
                    seen |= 1 << v
                    stack.append(v)
        rows.append(seen)
    return rows


def family(rng: random.Random) -> list[tuple[int, list[tuple[int, int]]]]:
    out: list[tuple[int, list[tuple[int, int]]]] = []
    for n in (1, 2, 7, 30):
        out.append((n, []))
        out.append((n, [(i, i + 1) for i in range(n - 1)]))  # directed path
        out.append((n, [(i, (i + 1) % n) for i in range(n)]))  # directed cycle
        out.append((n, [(0, i) for i in range(1, n)]))  # out-star
        out.append((n, [(i, j) for i in range(n) for j in range(n) if i != j]))  # complete
    for _ in range(110):
        n = rng.randint(1, 40)
        p = rng.choice([0.02, 0.05, 0.1, 0.3])
        out.append((n, [(i, j) for i in range(n) for j in range(n) if i != j and rng.random() < p]))
    return out


def test_example() -> None:
    edges = [(i, i + 1) for i in range(7)]  # the path 0 -> 1 -> ... -> 7
    full = [((1 << 8) - 1) ^ ((1 << v) - 1) for v in range(8)]
    c = Cost()
    assert ullman_yannakakis(8, edges, 3, cost=c, fixed=[2, 5]) == full
    assert (c.bfs_rounds, c.squarings) == (3, 1)
    # the sample {4} misses the window 0, 1, 2: vertex 0 does not see 4 to 7
    rows = ullman_yannakakis(8, edges, 3, fixed=[4])
    assert rows[0] == 0b1111 and rows[1:] == full[1:]


def test_against_search() -> None:
    rng = random.Random(19)
    runs = 0
    for n, edges in family(rng):
        want = closure_by_search(n, edges)
        for t in (1, 2, 3, 5, max(n, 1)):
            got = ullman_yannakakis(n, edges, t, random.Random(rng.random()))
            assert got == want
            low = ullman_yannakakis(n, edges, t, random.Random(rng.random()), c=0.3)
            assert all(g & ~w == 0 for g, w in zip(low, want))  # never a false pair
            runs += 1
    assert runs >= 500


def test_rounds_on_long_paths() -> None:
    # a directed path plus n/8 random arcs, t = ceil(2 sqrt n), c = 4: the closure is exact,
    # the number of rounds (BFS rounds plus squarings) is at most t + log2 n + 1, which is
    # below 3 sqrt n, and the sample has at most twice its mean size c n ln n / t
    rng = random.Random(20)
    for n in (64, 256, 1024):
        t = math.ceil(2 * math.sqrt(n))
        edges = [(i, i + 1) for i in range(n - 1)] + [(rng.randrange(n), rng.randrange(n)) for _ in range(n // 8)]
        c = Cost()
        got = ullman_yannakakis(n, edges, t, random.Random(rng.random()), cost=c)
        assert got == closure_by_search(n, edges)
        rounds = c.bfs_rounds + c.squarings
        assert rounds <= t + math.log2(n) + 1 <= 3 * math.sqrt(n)
        assert c.sample <= 2 * 4 * n * math.log(n) / t
