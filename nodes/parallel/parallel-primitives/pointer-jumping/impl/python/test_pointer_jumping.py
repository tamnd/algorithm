# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pointer-jumping/. The authors are listed in prov/MB1XCY.jsonl.

import random

from pointer_jumping import Trace, ceil_log2, pointer_jump_rank, pointer_jump_roots


def random_lists(n: int, k: int, rng: random.Random) -> list[int | None]:
    """A successor array of n nodes cut into at most k disjoint lists, in random order."""
    order = list(range(n))
    rng.shuffle(order)
    cuts = set(rng.sample(range(1, n), min(k - 1, n - 1))) if n > 1 else set()
    nxt: list[int | None] = [None] * n
    for t in range(n - 1):
        if t + 1 not in cuts:
            nxt[order[t]] = order[t + 1]
    return nxt


def walk_rank(nxt: list[int | None]) -> list[int]:
    """Sequential reference: walk back from each tail along the predecessor links."""
    n = len(nxt)
    pred: list[int | None] = [None] * n
    for i, j in enumerate(nxt):
        if j is not None:
            pred[j] = i
    rank = [0] * n
    for t in range(n):
        if nxt[t] is None:
            d, v = 0, t
            while v is not None:
                rank[v] = d
                d, v = d + 1, pred[v]
    return rank


def test_example() -> None:
    # the list 3 -> 0 -> 6 -> 2 -> 5 -> 1 -> 7 -> 4
    nxt = [6, 7, 5, 0, None, 1, 2, 4]
    tr = Trace()
    assert pointer_jump_rank(nxt, tr) == [6, 2, 4, 7, 0, 3, 5, 1]
    assert tr.rounds == 3
    assert tr.work == 7 + 6 + 4


def test_edges() -> None:
    assert pointer_jump_rank([]) == []
    assert pointer_jump_rank([None]) == [0]
    assert pointer_jump_rank([1, None]) == [1, 0]
    assert pointer_jump_rank([None, None, None]) == [0, 0, 0]


def test_ceil_log2() -> None:
    for n in range(1, 2000):
        k = ceil_log2(n)
        assert 2**k >= n and (k == 0 or 2 ** (k - 1) < n)


def test_random_against_walk() -> None:
    rng = random.Random(1979)
    sizes = [0, 1, 2, 3, 4, 5, 7, 8, 9, 16, 17, 31, 32, 33, 64, 100, 128, 129]
    for _ in range(40):
        for n in sizes:
            nxt = random_lists(n, rng.randint(1, 4), rng)
            tr = Trace()
            assert pointer_jump_rank(nxt, tr) == walk_rank(nxt)
            assert tr.rounds == ceil_log2(n)


def test_single_list_work_closed_form() -> None:
    rng = random.Random(7)
    for n in list(range(1, 70)) + [255, 256, 257, 1000]:
        nxt = random_lists(n, 1, rng)
        tr = Trace()
        pointer_jump_rank(nxt, tr)
        k = ceil_log2(n)
        assert tr.work == n * k - (2**k - 1)


def test_exclusive_access() -> None:
    rng = random.Random(42)
    for n in [2, 3, 8, 13, 64, 77]:
        nxt = random_lists(n, rng.randint(1, 3), rng)
        tr = Trace()
        pointer_jump_rank(nxt, tr)
        for step in tr.substeps:
            owner: dict[tuple[str, int], int] = {}
            for proc, cell in step:
                assert owner.setdefault(cell, proc) == proc


def test_roots() -> None:
    rng = random.Random(5)
    for _ in range(300):
        n = rng.randint(1, 60)
        parent = [i if i == 0 or rng.random() < 0.1 else rng.randrange(i) for i in range(n)]
        ref = []
        depth = 0
        for i in range(n):
            v, d = i, 0
            while parent[v] != v:
                v, d = parent[v], d + 1
            ref.append(v)
            depth = max(depth, d)
        tr = Trace()
        assert pointer_jump_roots(parent, tr) == ref
        assert tr.rounds == ceil_log2(depth)
