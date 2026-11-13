# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sokoban-problem/. The authors are listed in prov/N70HNE.jsonl.

import random

from sokoban_problem import bfs_moves, bfs_pushes, iddfs_moves, parse, replay, solved, zero_one_pushes

EXAMPLE = """\
########
##  #  #
#  $@# #
#   . ##
#      #
########"""

CORRIDOR = """\
#######
#@ $ .#
#######"""

CORNER = """\
#####
#@  #
# $ #
#  .#
#####"""

DEAD = """\
#####
#$ .#
# @ #
#####"""


def random_level(rng, boxes):
    h, w = rng.randint(3, 4), rng.randint(3, 5)
    cells = [(r, c) for r in range(h) for c in range(w)]
    walls = set(rng.sample(cells, rng.randint(0, h * w // 4)))
    free = [x for x in cells if x not in walls]
    if len(free) < 2 * boxes + 1:
        return None
    pick = rng.sample(free, 2 * boxes + 1)
    box, goal, player = set(pick[:boxes]), set(pick[boxes:2 * boxes]), pick[-1]
    rows = ['#' * (w + 2)]
    for r in range(h):
        line = '#'
        for c in range(w):
            x = (r, c)
            if x in walls:
                line += '#'
            elif x == player:
                line += '+' if x in goal else '@'
            elif x in box:
                line += '*' if x in goal else '$'
            else:
                line += '.' if x in goal else ' '
        rows.append(line + '#')
    rows.append('#' * (w + 2))
    return '\n'.join(rows)


def check_solution(level, solution):
    state = replay(level, solution)
    assert state is not None and solved(level, state)


def test_small_levels() -> None:
    lv = parse(CORRIDOR)
    assert bfs_moves(lv) == 'rRR' and bfs_pushes(lv) == 2
    lv = parse(CORNER)
    m = bfs_moves(lv)
    check_solution(lv, m)
    assert len(m) == len(iddfs_moves(lv)) and bfs_pushes(lv) == zero_one_pushes(lv) == 2
    lv = parse(DEAD)
    assert bfs_moves(lv) is None and bfs_pushes(lv) is None and zero_one_pushes(lv) is None


def test_moves_and_pushes_disagree() -> None:
    lv = parse(EXAMPLE)
    m = bfs_moves(lv)
    check_solution(lv, m)
    assert len(m) == 8 and sum(ch.isupper() for ch in m) == 4
    assert bfs_pushes(lv) == zero_one_pushes(lv) == 2
    check_solution(lv, 'dlluurDldR')  # 2 pushes, 10 moves


def test_bfs_against_independent_searches() -> None:
    rng = random.Random(3)
    checked = 0
    while checked < 60:
        text = random_level(rng, rng.randint(1, 2))
        if text is None:
            continue
        lv = parse(text)
        m = bfs_moves(lv)
        p = bfs_pushes(lv)
        assert p == zero_one_pushes(lv), text
        if m is None:
            assert p is None
            continue
        check_solution(lv, m)
        assert p <= sum(ch.isupper() for ch in m)
        if len(m) <= 12:
            assert len(iddfs_moves(lv, 12)) == len(m), text
        checked += 1
