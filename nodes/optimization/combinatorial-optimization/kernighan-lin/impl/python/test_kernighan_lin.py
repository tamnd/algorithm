# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kernighan-lin/. The authors are listed in prov/NEYJA8.jsonl.

import random
from itertools import combinations

from kernighan_lin import cut_weight, kernighan_lin


def d_from_scratch(c: list[list[int]], side: list[int], v: int) -> int:
    """External minus internal weight of v, recomputed from the definition."""
    return sum((c[v][u] if side[u] != side[v] else -c[v][u]) for u in range(len(c)) if u != v)


def swap_gain(c: list[list[int]], side: list[int], x: int, y: int) -> int:
    """Decrease of the cut when x and y change sides, recomputed from scratch."""
    after = side[:]
    after[x], after[y] = side[y], side[x]
    return cut_weight(c, side) - cut_weight(c, after)


def best_bisection(c: list[list[int]], size: int) -> int:
    n = len(c)
    best = None
    for s in combinations(range(n), size):
        side = [1] * n
        for v in s:
            side[v] = 0
        w = cut_weight(c, side)
        best = w if best is None or w < best else best
    return best


def graph(edges: list[tuple[int, int, int]], n: int) -> list[list[int]]:
    c = [[0] * n for _ in range(n)]
    for u, v, w in edges:
        c[u][v] += w
        c[v][u] += w
    return c


def check(c: list[list[int]], a: list[int]) -> tuple[list[int], list[int]]:
    n = len(c)
    side = [1] * n
    for v in a:
        side[v] = 0
    start_cut = cut_weight(c, side)
    pass_start_cuts: list[int] = []
    prev = {"tent": side[:], "locked": [False] * n}

    def on_step(tent: list[int], d: list[int], locked: list[bool], x: int, y: int, g: int) -> None:
        if sum(locked) == 2:
            # First swap of a pass: the state before it is the real partition.
            before = tent[:]
            before[x], before[y] = 0, 1
            lock_before = [False] * n
            pass_start_cuts.append(cut_weight(c, before))
        else:
            before = prev["tent"]
            lock_before = prev["locked"]
        assert before[x] == 0 and before[y] == 1
        assert not lock_before[x] and not lock_before[y]
        # The gain equals the change of the cut, recomputed from scratch.
        assert g == swap_gain(c, before, x, y)
        # The chosen pair is a best unlocked pair.
        for u in range(n):
            for v in range(n):
                if before[u] == 0 and before[v] == 1 and not lock_before[u] and not lock_before[v]:
                    assert swap_gain(c, before, u, v) <= g
        # The tentative sides keep their sizes.
        assert tent.count(0) == before.count(0)
        # The updated D values equal a recomputation from scratch.
        for v in range(n):
            if not locked[v]:
                assert d[v] == d_from_scratch(c, tent, v)
        prev["tent"] = tent
        prev["locked"] = locked

    A, B = kernighan_lin(c, a, on_step)
    final = [1] * n
    for v in A:
        final[v] = 0
    # A partition with the same side sizes as the start.
    assert sorted(A + B) == list(range(n))
    assert len(A) == len(a)
    w = cut_weight(c, final)
    assert w <= start_cut
    # Every pass but the last lowers the cut, and the last one changes nothing.
    if pass_start_cuts:
        assert pass_start_cuts[0] == start_cut
        assert all(p > q for p, q in zip(pass_start_cuts, pass_start_cuts[1:]))
        assert pass_start_cuts[-1] == w
    # The result is a local optimum for single swaps.
    for x in A:
        for y in B:
            assert swap_gain(c, final, x, y) <= 0
    # It is never better than the optimum.
    assert w >= best_bisection(c, len(a))
    return A, B


def test_example() -> None:
    a, b, cc, d, e, f = range(6)
    c = graph([(a, b, 1), (a, cc, 1), (b, cc, 1), (cc, d, 1), (d, e, 1), (d, f, 1), (e, f, 1), (b, e, 1)], 6)
    steps: list[tuple[int, int, int]] = []
    A, B = kernighan_lin(c, [a, b, d], lambda t, dd, l, x, y, g: steps.append((x, y, g)))
    assert (A, B) == ([0, 1, 2], [3, 4, 5])
    assert steps[:3] == [(d, cc, 4), (a, e, -3), (b, f, -1)]
    assert [g for _, _, g in steps[3:]] == [-2, 0, 2]
    assert cut_weight(c, [0, 0, 0, 1, 1, 1]) == 2
    check(c, [a, b, d])


def test_small_cases() -> None:
    assert kernighan_lin([[0]], []) == ([], [0])
    assert kernighan_lin([[0, 1], [1, 0]], [0]) == ([0], [1])
    c = graph([(0, 1, 5), (2, 3, 5), (0, 2, 1), (1, 3, 1)], 4)
    A, _ = kernighan_lin(c, [0, 2])
    assert cut_weight(c, [0 if v in A else 1 for v in range(4)]) == 2
    check(c, [0, 2])


def test_full_pass_gains_add_to_zero() -> None:
    # With equal sides a full pass swaps every vertex, so its gains add up to 0.
    rng = random.Random(77)
    for _ in range(50):
        n = 2 * rng.randint(1, 4)
        c = [[0] * n for _ in range(n)]
        for u in range(n):
            for v in range(u + 1, n):
                c[u][v] = c[v][u] = rng.randint(0, 4)
        gains: list[int] = []

        def on_step(t, d, l, x, y, g):
            if sum(l) == 2:
                gains.clear()
            gains.append(g)
            if all(l):
                assert sum(gains) == 0

        kernighan_lin(c, list(range(n // 2)), on_step)


def test_random_against_scratch_and_brute_force() -> None:
    rng = random.Random(4127)
    for _ in range(600):
        n = rng.randint(2, 9)
        p = rng.random()
        wmax = rng.choice([1, 1, 3, 9])
        c = [[0] * n for _ in range(n)]
        for u in range(n):
            for v in range(u + 1, n):
                if rng.random() < p:
                    c[u][v] = c[v][u] = rng.randint(1, wmax)
        size = n // 2 if rng.random() < 0.8 else rng.randint(0, n)
        a = rng.sample(range(n), size)
        check(c, a)


if __name__ == "__main__":
    test_example()
    test_small_cases()
    test_full_pass_gains_add_to_zero()
    test_random_against_scratch_and_brute_force()
    print("ok")
