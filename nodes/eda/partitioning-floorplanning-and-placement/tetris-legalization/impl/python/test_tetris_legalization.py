# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tetris-legalization/. The authors are listed in prov/M7HMAC.jsonl.

import random
from fractions import Fraction
from itertools import permutations, product

import pytest

from tetris_legalization import displacement, tetris


def check_legal(x, y, w, K, S):
    n = len(x)
    for i in range(n):
        assert isinstance(x[i], int) and 0 <= x[i] and x[i] + w[i] <= S and y[i] in range(K)
    for i in range(n):
        for j in range(i + 1, n):
            if y[i] == y[j]:
                assert x[i] + w[i] <= x[j] or x[j] + w[j] <= x[i]


def best_one_row(xg, w, S):
    """Brute force: every order of the cells, and for each order every integer placement in that order."""
    n = len(xg)
    best = None
    for order in permutations(range(n)):
        for xs in product(range(S), repeat=n):
            if all(xs[k] + w[order[k]] <= xs[k + 1] for k in range(n - 1)) and xs[-1] + w[order[-1]] <= S:
                c = sum(abs(xs[k] - Fraction(xg[order[k]])) for k in range(n))
                if best is None or c < best:
                    best = c
    return best


def greedy_reference(xg, yg, w, K, S):
    """The same greedy rule, with each row scanned over every site at or after its frontier."""
    n = len(xg)
    frontier = [0] * K
    x, y = [0] * n, [0] * n
    for i in sorted(range(n), key=lambda i: (Fraction(xg[i]), i)):
        best = None
        for r in range(K):
            for pos in range(frontier[r], S - w[i] + 1):
                c = abs(pos - Fraction(xg[i])) + abs(r - Fraction(yg[i]))
                if best is None or c < best[0]:
                    best = (c, r, pos)
        if best is None:
            raise ValueError
        _, r, pos = best
        x[i], y[i] = pos, r
        frontier[r] = pos + w[i]
    return x, y


def test_legal_and_same_as_scanning_reference():
    rng = random.Random(2002)
    for _ in range(300):
        K, S = rng.randint(1, 4), rng.randint(3, 12)
        n = rng.randint(1, 10)
        w = [rng.randint(1, 3) for _ in range(n)]
        xg = [Fraction(rng.randint(-4, 4 * S), 4) for _ in range(n)]
        yg = [Fraction(rng.randint(-2, 4 * K), 4) for _ in range(n)]
        try:
            ref = greedy_reference(xg, yg, w, K, S)
        except ValueError:
            with pytest.raises(ValueError):
                tetris(xg, yg, w, K, S)
            continue
        got = tetris(xg, yg, w, K, S)
        check_legal(*got, w, K, S)
        assert displacement(*got, xg, yg) == displacement(*ref, xg, yg)


def test_never_better_than_the_best_one_row_placement():
    rng = random.Random(5)
    for _ in range(40):
        n = 4
        w = [rng.randint(1, 2) for _ in range(n)]
        S = sum(w) + rng.randint(0, 2)
        xg = [Fraction(rng.randint(0, 2 * S), 2) for _ in range(n)]
        try:
            x, y = tetris(xg, [0] * n, w, 1, S)
        except ValueError:
            continue
        assert displacement(x, y, xg, [0] * n) >= best_one_row(xg, w, S)


def test_page_examples():
    # three unit cells wanting x = 5: Tetris gives 5, 6, 7 (movement 3); the best is 4, 5, 6 (movement 2)
    x, _ = tetris([5, 5, 5], [0, 0, 0], [1, 1, 1], 1, 10)
    assert x == [5, 6, 7] and best_one_row([5, 5, 5], [1, 1, 1], 8) == 2
    # the frontier hides a free gap: a fits at 2, then b of width 2 finds no room, though [0, 2) is free
    with pytest.raises(ValueError):
        tetris([2, Fraction(5, 2)], [0, 0], [1, 2], 1, 4)
