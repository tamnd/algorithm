# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rush-hour-problem/. The authors are listed in prov/72JECE.jsonl.

import random

from rush_hour_problem import bfs, component_size, dijkstra_steps, iddfs_moves, parse, replay, solved

TRUCK = ['..B...',
         '..B...',
         'AAB...',
         '......',
         '......',
         '......']

EXAMPLE = ['MMKD.C',
           'IIKD.C',
           'J..AAC',
           'J.HHB.',
           'LEEEB.',
           'LGGGFF']

STUCK = ['..B...',
         '..B...',
         'AAB...',
         '..C...',
         '..C...',
         '..C...']


def random_board(rng, n, cars):
    grid = [['.'] * n for _ in range(n)]
    exit_row = (n - 1) // 2
    c0 = rng.randint(0, n - 3)
    grid[exit_row][c0] = grid[exit_row][c0 + 1] = 'A'
    k = 0
    for _ in range(200):
        if k == cars:
            break
        length = rng.choice([2, 2, 3])
        horizontal = rng.random() < 0.5
        r, c = rng.randrange(n), rng.randrange(n)
        cells = [(r, c + i) if horizontal else (r + i, c) for i in range(length)]
        if any(x >= n or y >= n or grid[x][y] != '.' for x, y in cells):
            continue
        if horizontal and r == exit_row:
            continue
        for x, y in cells:
            grid[x][y] = 'BCDEFGHIJKLMNOP'[k]
        k += 1
    return [''.join(row) for row in grid]


def test_truck_example() -> None:
    board = parse(TRUCK)
    assert bfs(board) == (2, [('B', 3), ('A', 4)])
    assert bfs(board, unit_steps=True)[0] == 7 == dijkstra_steps(board)


def test_stuck() -> None:
    board = parse(STUCK)
    assert bfs(board) is None and iddfs_moves(board, 6) is None and dijkstra_steps(board) is None


def test_example_board() -> None:
    board = parse(EXAMPLE)
    moves, path = bfs(board)
    assert moves == 12 == iddfs_moves(board, 12)
    assert solved(board, replay(board, path))
    assert bfs(board, unit_steps=True)[0] == 17 == dijkstra_steps(board)
    assert component_size(board) == 1935


def test_bfs_against_independent_searches() -> None:
    rng = random.Random(4)
    for _ in range(150):
        board = parse(random_board(rng, rng.choice([4, 5]), rng.randint(2, 7)))
        res = bfs(board)
        steps = bfs(board, unit_steps=True)
        assert (res is None) == (steps is None)
        if res is None:
            assert dijkstra_steps(board) is None
            continue
        assert solved(board, replay(board, res[1]))
        assert iddfs_moves(board, res[0]) == res[0]
        assert steps[0] == dijkstra_steps(board)
        assert res[0] <= steps[0]
