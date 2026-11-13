# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/polyomino-tiling-problem/. The authors are listed in prov/6M5XGW.jsonl.

import random

from polyomino_tiling_problem import (PENTOMINOES, brute_force, count_tilings, orientations,
                                      placements, rectangle, tilings)

DOMINO = {(0, 0), (0, 1)}
L_TROMINO = {(0, 0), (1, 0), (1, 1)}
I_TROMINO = {(0, 0), (0, 1), (0, 2)}
I_TETROMINO = {(0, 0), (0, 1), (0, 2), (0, 3)}
T_TETROMINO = {(0, 0), (0, 1), (0, 2), (1, 1)}
SQUARE = {(0, 0), (0, 1), (1, 0), (1, 1)}
SMALL = [{(0, 0)}, DOMINO, L_TROMINO, I_TROMINO, I_TETROMINO, T_TETROMINO, SQUARE]


def test_orientations() -> None:
    counts = {name: len(orientations(p)) for name, p in PENTOMINOES.items()}
    assert counts == {"F": 8, "I": 2, "L": 8, "N": 8, "P": 8, "T": 4, "U": 4,
                      "V": 4, "W": 4, "X": 1, "Y": 8, "Z": 4}
    assert sum(counts.values()) == 63
    assert len(orientations(PENTOMINOES["F"], reflect=False)) == 4


def test_known_counts() -> None:
    assert [count_tilings(rectangle(2, n), [DOMINO]) for n in range(1, 10)] == [1, 2, 3, 5, 8, 13, 21, 34, 55]
    assert count_tilings(rectangle(4, 4), [DOMINO]) == 36
    assert count_tilings(rectangle(2, 3), [L_TROMINO]) == 2
    assert count_tilings(rectangle(3, 3), [L_TROMINO]) == 0


def test_coloring_argument() -> None:
    # Color (r, c) by (r + c) mod 4; a straight tetromino covers each color once,
    # and the 6 by 6 board has 9, 10, 9 and 8 cells of the four colors.
    colors = [sum((r + c) % 4 == k for r, c in rectangle(6, 6)) for k in range(4)]
    assert colors == [9, 10, 9, 8]
    assert count_tilings(rectangle(6, 6), [I_TETROMINO]) == 0
    assert count_tilings(rectangle(4, 4), [I_TETROMINO]) == 2


def test_pentomino_subsets() -> None:
    pieces = [PENTOMINOES[k] for k in "LPUY"]
    got = tilings(rectangle(4, 5), pieces, once=True)
    assert got and got == brute_force(rectangle(4, 5), pieces, once=True)
    assert tilings(rectangle(5, 12), list(PENTOMINOES.values()), once=True, limit=1)


def test_against_brute_force() -> None:
    rng = random.Random(81)
    for _ in range(60):
        h, w = rng.randint(1, 3), rng.randint(1, 4)
        region = rectangle(h, w)
        for cell in rng.sample(sorted(region), rng.randint(0, min(2, len(region) - 1))):
            region.discard(cell)
        pieces = rng.sample(SMALL[1:], rng.randint(1, 3))
        if rng.random() < 0.2:
            pieces.append(SMALL[0])
        for once in (False, True):
            for reflect in (True, False):
                if len(placements(region, pieces, reflect)) > 40:
                    continue
                assert tilings(region, pieces, once, reflect) == brute_force(region, pieces, once, reflect)
