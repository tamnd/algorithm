# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fiduccia-mattheyses/. The authors are listed in prov/K9FVJG.jsonl.

import random
from itertools import product

from fiduccia_mattheyses import cut_size, fiduccia_mattheyses


def gain_from_scratch(nets: list[list[int]], side: list[int], v: int) -> int:
    """Decrease of the cut when v alone changes side, recomputed from scratch."""
    after = side[:]
    after[v] = 1 - side[v]
    return cut_size(nets, side) - cut_size(nets, after)


def movable(side: list[int], v: int, lo: int, hi: int) -> bool:
    c0 = side.count(0)
    return lo <= (c0 - 1 if side[v] == 0 else c0 + 1) <= hi


def best_cut(nets: list[list[int]], n: int, lo: int, hi: int) -> int:
    return min(
        cut_size(nets, list(s)) for s in product((0, 1), repeat=n) if lo <= list(s).count(0) <= hi
    )


def check(nets: list[list[int]], n: int, side: list[int], lo: int, hi: int) -> list[int]:
    start_cut = cut_size(nets, side)
    pass_start_cuts: list[int] = []
    prev = {"tent": side[:], "locked": [False] * n}

    def on_step(v: int, g: int, tent: list[int], locked: list[bool], gain: list[int]) -> None:
        if sum(locked) == 1:
            before = tent[:]
            before[v] = 1 - tent[v]
            lock_before = [False] * n
            pass_start_cuts.append(cut_size(nets, before))
        else:
            before = prev["tent"]
            lock_before = prev["locked"]
        assert not lock_before[v] and before[v] != tent[v]
        # The recorded gain equals the change of the cut, recomputed from scratch.
        assert g == gain_from_scratch(nets, before, v)
        # The moved vertex keeps the balance and has the largest gain among
        # the free vertices that may move.
        assert movable(before, v, lo, hi)
        for u in range(n):
            if not lock_before[u] and movable(before, u, lo, hi):
                assert gain_from_scratch(nets, before, u) <= g
        # Every tentative partition is balanced.
        assert lo <= tent.count(0) <= hi
        # The bucket gains of the free vertices equal a recomputation.
        for u in range(n):
            if not locked[u]:
                assert gain[u] == gain_from_scratch(nets, tent, u)
        prev["tent"] = tent
        prev["locked"] = locked

    final = fiduccia_mattheyses(nets, n, side, lo, hi, on_step)
    assert len(final) == n and set(final) <= {0, 1}
    assert lo <= final.count(0) <= hi
    w = cut_size(nets, final)
    assert w <= start_cut
    if pass_start_cuts:
        assert pass_start_cuts[0] == start_cut
        assert all(p > q for p, q in zip(pass_start_cuts, pass_start_cuts[1:]))
        assert pass_start_cuts[-1] == w
    # No single balanced move improves the result.
    for v in range(n):
        if movable(final, v, lo, hi):
            assert gain_from_scratch(nets, final, v) <= 0
    assert w >= best_cut(nets, n, lo, hi)
    return final


def test_example_graph() -> None:
    a, b, c, d, e, f = range(6)
    nets = [[a, b], [a, c], [b, c], [c, d], [d, e], [d, f], [e, f], [b, e]]
    start = [0, 0, 1, 0, 1, 1]
    steps: list[tuple[int, int]] = []
    final = fiduccia_mattheyses(nets, 6, start, 2, 4, lambda v, g, t, l, gn: steps.append((v, g)))
    assert final == [0, 0, 0, 1, 1, 1]
    assert steps[:6] == [(d, 3), (c, 1), (b, -1), (f, -2), (a, 0), (e, -1)]
    assert [g for _, g in steps[6:]] == [-1, -1, 0, 0, 1, 1]
    assert cut_size(nets, final) == 2
    check(nets, 6, start, 2, 4)


def test_example_hypergraph() -> None:
    nets = [[0, 1, 2], [2, 3], [3, 4, 5], [1, 4], [0, 5]]
    final = check(nets, 6, [0, 1, 0, 1, 0, 1], 2, 4)
    assert cut_size(nets, final) == 2


def test_small_cases() -> None:
    assert fiduccia_mattheyses([], 0, [], 0, 0) == []
    assert fiduccia_mattheyses([[0, 1]], 2, [0, 1], 1, 1) == [0, 1]
    assert fiduccia_mattheyses([[0, 1]], 2, [0, 1], 0, 2) in ([0, 0], [1, 1])
    try:
        fiduccia_mattheyses([[0, 1]], 2, [0, 0], 1, 1)
    except ValueError:
        pass
    else:
        raise AssertionError("an unbalanced start must be rejected")


def test_random_against_scratch_and_brute_force() -> None:
    rng = random.Random(6271)
    for _ in range(700):
        n = rng.randint(1, 10)
        nets = []
        for _ in range(rng.randint(0, 14)):
            k = rng.randint(1, min(4, n))
            nets.append(rng.sample(range(n), k))
        if rng.random() < 0.3:
            nets = [e for e in nets if len(e) == 2]
        slack = rng.choice([0, 1, 1, 2, n])
        lo = max(0, n // 2 - slack)
        hi = min(n, (n + 1) // 2 + slack)
        size = rng.randint(lo, hi)
        zero = set(rng.sample(range(n), size))
        side = [0 if v in zero else 1 for v in range(n)]
        check(nets, n, side, lo, hi)


if __name__ == "__main__":
    test_example_graph()
    test_example_hypergraph()
    test_small_cases()
    test_random_against_scratch_and_brute_force()
    print("ok")
