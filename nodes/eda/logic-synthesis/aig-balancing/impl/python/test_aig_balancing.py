# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aig-balancing/. The authors are listed in prov/AX6R7V.jsonl.

import heapq
import random
from functools import lru_cache

from aig_balancing import Aig, balance, min_tree_depth, supergate_leaves


def chain(n: int) -> tuple[Aig, int]:
    g = Aig(n)
    x = 2 * n
    for i in range(n - 1, 0, -1):
        x = g.and_(2 * i, x)
    return g, x


def test_chain_example() -> None:
    g, o = chain(5)
    assert g.depth([o]) == 4 and len(g.cone([o])) == 4
    h, (p,) = balance(g, [o])
    assert h.depth([p]) == 3 and len(h.cone([p])) == 4
    assert h.simulate([p]) == g.simulate([o])
    # the pairs of the example: (a, b), (c, d), (e, ab), (cd, abe)
    assert [(h.fanin0[v], h.fanin1[v]) for v in range(6, 10)] == [(2, 4), (6, 8), (10, 12), (14, 16)]


def test_late_leaf_example() -> None:
    # o1 = (a & b) & (c & d) is shared; o2 = e & (f & o1) is a chain over a late leaf
    g = Aig(6)
    s = g.and_(g.and_(2, 4), g.and_(6, 8))
    o2 = g.and_(10, g.and_(12, s))
    refs_ok = g.depth([s, o2]) == 4
    assert refs_ok
    h, outs = balance(g, [s, o2])
    assert h.simulate(outs) == g.simulate([s, o2])
    assert h.depth(outs) == 3
    assert len(h.cone(outs)) == len(g.cone([s, o2])) == 5


def test_duplicate_and_opposite_leaves() -> None:
    g = Aig(3)
    ab = g.and_(2, 4)
    # (a & b) & (a & c): the leaf a appears twice
    o = g.and_(ab, g.and_(2, 6))
    h, (p,) = balance(g, [o])
    assert len(h.cone([p])) == 2 and h.simulate([p]) == g.simulate([o])
    # (a & b) & (!a & c) is 0
    q = g.and_(g.and_(2, 4), g.and_(3, 6))
    h2, (r,) = balance(g, [q])
    assert r == 0


def test_alternating_and_or_chain_is_unchanged() -> None:
    g = Aig(5)
    z = g.and_(8 ^ 1, 10 ^ 1) ^ 1  # d | e
    z = g.and_(6, z)  # c & (d | e)
    z = g.and_(4 ^ 1, z ^ 1) ^ 1  # b | ...
    o = g.and_(2, z)  # a & ...
    h, (p,) = balance(g, [o])
    assert h.depth([p]) == g.depth([o]) == 4
    assert len(h.cone([p])) == 4


@lru_cache(maxsize=None)
def brute_depth(levels: tuple[int, ...]) -> int:
    if len(levels) == 1:
        return levels[0]
    best = None
    k = len(levels)
    for mask in range(1, (1 << k) - 1):
        if mask & 1 == 0:
            continue
        a = tuple(sorted(levels[i] for i in range(k) if mask >> i & 1))
        b = tuple(sorted(levels[i] for i in range(k) if not mask >> i & 1))
        d = 1 + max(brute_depth(a), brute_depth(b))
        best = d if best is None else min(best, d)
    return best


def greedy_depth(levels: list[int]) -> int:
    heap = list(levels)
    heapq.heapify(heap)
    while len(heap) > 1:
        x = heapq.heappop(heap)
        y = heapq.heappop(heap)
        heapq.heappush(heap, 1 + max(x, y))
    return heap[0]


def test_greedy_pairing_is_optimal_against_all_trees() -> None:
    rng = random.Random(5)
    for _ in range(600):
        k = rng.randrange(1, 8)
        levels = tuple(sorted(rng.randrange(0, 4) for _ in range(k)))
        best = brute_depth(levels)
        assert greedy_depth(list(levels)) == best == min_tree_depth(list(levels))


def random_aig(rng: random.Random) -> tuple[Aig, list[int]]:
    n = rng.randrange(2, 7)
    g = Aig(n)
    lits = [2 * i for i in range(1, n + 1)]
    for _ in range(rng.randrange(3, 40)):
        if rng.random() < 0.5 and len(lits) > n:
            a = lits[-1]
        else:
            a = rng.choice(lits)
        b = rng.choice(lits)
        x = g.and_(a ^ (rng.random() < 0.25), b ^ (rng.random() < 0.25))
        if x > 1:
            lits.append(x)
    outs = [rng.choice(lits[n:] or lits) ^ rng.randrange(2) for _ in range(rng.randrange(1, 4))]
    return g, outs


def test_random_aigs_function_size_and_depth() -> None:
    rng = random.Random(99)
    for _ in range(700):
        g, outs = random_aig(rng)
        h, new = balance(g, outs)
        assert h.simulate(new) == g.simulate(outs)
        assert len(h.cone(new)) <= len(g.cone(outs))
        for o, p in zip(outs, new):
            assert h.level[p >> 1] <= g.level[o >> 1]
        # a second pass may find more, never less
        h2, new2 = balance(h, new)
        assert h2.depth(new2) <= h.depth(new)
        assert h2.simulate(new2) == g.simulate(outs)


def test_supergate_stops_at_shared_and_complemented_edges() -> None:
    g = Aig(4)
    ab = g.and_(2, 4)
    cd = g.and_(6, 8)
    top = g.and_(ab, cd ^ 1)
    refs = [0] * len(g.fanin0)
    for v in g.cone([top, ab]):
        refs[g.fanin0[v] >> 1] += 1
        refs[g.fanin1[v] >> 1] += 1
    refs[top >> 1] += 1
    refs[ab >> 1] += 1
    assert sorted(supergate_leaves(g, top >> 1, refs)) == sorted([ab, cd ^ 1])
