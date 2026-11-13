# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nurikabe-problem/. The authors are listed in prov/69KGGJ.jsonl.

import random

from nurikabe_problem import brute_force, is_solution, solve


def key(shade):
    return tuple(tuple(row) for row in shade)


def random_board(rng, h, w):
    """Clues from a random valid shading, so the board has a solution."""
    while True:
        shade = [[1 if rng.random() < 0.55 else 0 for _ in range(w)] for _ in range(h)]
        board = [[0] * w for _ in range(h)]
        # Put the clue of each white component on one of its cells.
        seen = set()
        for r0 in range(h):
            for c0 in range(w):
                if shade[r0][c0] or (r0, c0) in seen:
                    continue
                comp = [(r0, c0)]
                seen.add((r0, c0))
                i = 0
                while i < len(comp):
                    r, c = comp[i]
                    i += 1
                    for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                        if 0 <= nr < h and 0 <= nc < w and not shade[nr][nc] and (nr, nc) not in seen:
                            seen.add((nr, nc))
                            comp.append((nr, nc))
                r, c = rng.choice(comp)
                board[r][c] = len(comp)
        if is_solution(board, shade):
            return board, shade


def test_known_puzzle() -> None:
    board = [[0, 0, 0, 0, 0],
             [1, 0, 1, 0, 0],
             [0, 0, 0, 0, 7],
             [0, 0, 2, 0, 0],
             [0, 0, 0, 0, 0]]
    expected = [[1, 1, 1, 0, 0],
                [0, 1, 0, 1, 0],
                [1, 1, 1, 1, 0],
                [1, 0, 0, 1, 0],
                [1, 1, 1, 0, 0]]
    assert solve(board) == [expected]


def test_rules() -> None:
    # A 2 by 2 pool of sea is not allowed.
    board = [[1, 0, 0], [0, 0, 0], [0, 0, 1]]
    assert not is_solution(board, [[0, 1, 1], [1, 1, 1], [1, 1, 0]])
    # Two islands may not touch, and the sea must be connected.
    assert not is_solution([[1, 1]], [[0, 0]])
    assert is_solution([[1, 0, 1]], [[0, 1, 0]])
    assert not is_solution([[0, 3, 0]], [[1, 0, 1]])


def test_solver_against_brute_force_small() -> None:
    rng = random.Random(11)
    for _ in range(60):
        h, w = rng.randint(1, 3), rng.randint(1, 4)
        board, shade = random_board(rng, h, w)
        expected = {key(s) for s in brute_force(board)}
        assert key(shade) in expected
        assert {key(s) for s in solve(board)} == expected


def test_solver_against_brute_force_4x4() -> None:
    rng = random.Random(12)
    for _ in range(4):
        board, shade = random_board(rng, 4, 4)
        expected = {key(s) for s in brute_force(board)}
        assert {key(s) for s in solve(board)} == expected


def test_unsolvable_boards() -> None:
    rng = random.Random(13)
    for _ in range(30):
        h, w = rng.randint(2, 3), rng.randint(2, 3)
        board = [[rng.choice((0, 0, 0, 1, 2, 3)) for _ in range(w)] for _ in range(h)]
        if not any(v for row in board for v in row):
            continue
        assert {key(s) for s in solve(board)} == {key(s) for s in brute_force(board)}
