# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/abacus-legalization/. The authors are listed in prov/4DKME3.jsonl.

import random
from fractions import Fraction
from itertools import product

import pytest

from abacus_legalization import abacus, cell_positions, movement, place_row


def qp_brute_force(order, xg, w, e, S):
    """Exact optimum of min sum e_i (x_i - xg_i)^2 with the order kept, no overlap, inside [0, S].
    The optimum is the minimizer for its own set of tight constraints, so enumerate all of them:
    every split of the order into blocks of abutting cells, and a pin of the first block to 0
    and of the last block to S. Keep the best feasible candidate."""
    n = len(order)
    best = None
    for cuts in product([0, 1], repeat=n - 1):
        blocks, cur = [], [order[0]]
        for k in range(1, n):
            if cuts[k - 1]:
                blocks.append(cur)
                cur = [order[k]]
            else:
                cur.append(order[k])
        blocks.append(cur)
        for pin_left, pin_right in product([False, True], repeat=2):
            xs = {}
            ok = True
            for b_idx, blk in enumerate(blocks):
                width = sum(w[i] for i in blk)
                off, offs = 0, []
                for i in blk:
                    offs.append(off)
                    off += w[i]
                left = pin_left and b_idx == 0
                right = pin_right and b_idx == len(blocks) - 1
                if left and right and width != S:
                    ok = False
                    break
                if left:
                    X = Fraction(0)
                elif right:
                    X = Fraction(S - width)
                else:
                    X = sum(e[i] * (Fraction(xg[i]) - o) for i, o in zip(blk, offs)) / sum(e[i] for i in blk)
                for i, o in zip(blk, offs):
                    xs[i] = X + o
            if not ok:
                continue
            feasible = all(xs[order[k]] + w[order[k]] <= xs[order[k + 1]] for k in range(n - 1))
            feasible = feasible and xs[order[0]] >= 0 and xs[order[-1]] + w[order[-1]] <= S
            if feasible:
                cost = sum(e[i] * (xs[i] - xg[i]) ** 2 for i in order)
                if best is None or cost < best[0]:
                    best = (cost, xs)
    return best


def check_legal(x, y, w, K, S):
    n = len(x)
    for i in range(n):
        assert isinstance(x[i], int) and 0 <= x[i] and x[i] + w[i] <= S
        assert y[i] in range(K)
    for i in range(n):
        for j in range(i + 1, n):
            if y[i] == y[j]:
                assert x[i] + w[i] <= x[j] or x[j] + w[j] <= x[i]


def test_place_row_is_the_exact_qp_optimum_for_5_cells():
    rng = random.Random(2008)
    for _ in range(400):
        n = 5
        w = [rng.randint(1, 3) for _ in range(n)]
        S = sum(w) + rng.randint(0, 6)
        xg = [Fraction(rng.randint(-4, 4 * S), 4) for _ in range(n)]
        e = [Fraction(rng.randint(1, 4)) for _ in range(n)]
        order = list(range(n)) if rng.random() < 0.5 else sorted(range(n), key=lambda i: xg[i])
        clusters = place_row(order, xg, w, e, 0, S)
        xs = cell_positions(clusters, w)
        cost = sum(e[i] * (xs[i] - xg[i]) ** 2 for i in order)
        bcost, bxs = qp_brute_force(order, xg, w, e, S)
        assert cost == bcost
        assert xs == bxs  # unique, since the objective is strictly convex


def test_page_example_row():
    w = [2, 1, 2, 1, 2]
    xg = [1, 2, Fraction(5, 2), 7, 7]
    e = [1] * 5
    clusters = place_row(range(5), xg, w, e, 0, 9)
    xs = cell_positions(clusters, w)
    assert [xs[i] for i in range(5)] == [Fraction(1, 6), Fraction(13, 6), Fraction(19, 6), 6, 7]
    assert [c.cells for c in clusters] == [[0, 1, 2], [3, 4]]
    assert sum((xs[i] - xg[i]) ** 2 for i in range(5)) == Fraction(13, 6)
    x, y = abacus(xg, [0] * 5, w, 1, 9)
    assert x == [0, 2, 3, 6, 7] and movement(x, y, xg, [0] * 5) == Fraction(9, 4)


def test_abacus_is_legal_and_keeps_order():
    rng = random.Random(4)
    for _ in range(150):
        K = rng.randint(1, 4)
        S = rng.randint(4, 12)
        n = rng.randint(1, K * S // 2)
        w = [rng.randint(1, 3) for _ in range(n)]
        while sum(w) > K * S - 3 * K and n > 1:
            w.pop()
            n -= 1
        xg = [Fraction(rng.randint(-8, 4 * S + 8), 4) for _ in range(n)]
        yg = [Fraction(rng.randint(-2, 4 * K + 2), 4) for _ in range(n)]
        try:
            x, y = abacus(xg, yg, w, K, S)
        except ValueError:
            continue  # no row had room for some cell
        check_legal(x, y, w, K, S)
        for r in range(K):
            row = [i for i in range(n) if y[i] == r]
            assert sorted(row, key=lambda i: (xg[i], i)) == sorted(row, key=lambda i: x[i])


def test_one_row_rounding_close_to_integer_optimum():
    # the rounded result is legal and its cost is at least the best integer placement in the same order
    rng = random.Random(9)
    for _ in range(100):
        n = 4
        w = [rng.randint(1, 2) for _ in range(n)]
        S = sum(w) + rng.randint(0, 3)
        xg = [Fraction(rng.randint(0, 4 * S), 4) for _ in range(n)]
        x, y = abacus(xg, [0] * n, w, 1, S)
        check_legal(x, y, w, 1, S)
        order = sorted(range(n), key=lambda i: (xg[i], i))
        best = None
        for xs in product(range(S), repeat=n):
            if all(xs[k] + w[order[k]] <= xs[k + 1] for k in range(n - 1)) and xs[-1] + w[order[-1]] <= S:
                c = sum((xs[k] - xg[order[k]]) ** 2 for k in range(n))
                best = c if best is None or c < best else best
        assert movement(x, y, xg, [0] * n) >= best
        cont = qp_brute_force(order, xg, w, [1] * n, S)[0]
        assert best >= cont


def test_no_room():
    with pytest.raises(ValueError):
        abacus([0, 0, 0], [0, 0, 0], [2, 2, 2], 1, 5)
