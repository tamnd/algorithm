# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slitherlink-problem/. The authors are listed in prov/0NPZ8T.jsonl.

import functools
import random

from slitherlink_problem import all_loops, cell_edges, edges_of, is_single_loop, is_solution, solve

loops_of = functools.lru_cache(maxsize=None)(all_loops)


def key(edge_set):
    return frozenset(edge_set)


def edge_brute_force(clues):
    """All solutions by trying every subset of the edges."""
    h, w = len(clues), len(clues[0])
    edges = edges_of(h, w)
    out = set()
    for mask in range(1 << len(edges)):
        chosen = {edges[i] for i in range(len(edges)) if mask >> i & 1}
        if is_solution(clues, chosen):
            out.add(key(chosen))
    return out


def full_clues(h, w, loop):
    return [[sum(e in loop for e in cell_edges(r, c)) for c in range(w)] for r in range(h)]


def test_loop_counts() -> None:
    # The cell-set enumeration agrees with the edge-subset enumeration.
    for h, w in ((1, 1), (1, 2), (2, 2)):
        edges = edges_of(h, w)
        by_edges = {key({edges[i] for i in range(len(edges)) if m >> i & 1})
                    for m in range(1 << len(edges))
                    if is_single_loop({edges[i] for i in range(len(edges)) if m >> i & 1})}
        assert by_edges == {key(s) for s in all_loops(h, w)}
    assert [len(all_loops(n, n)) for n in (1, 2, 3)] == [1, 13, 213]
    assert len(all_loops(2, 3)) == 40


def test_known_puzzle() -> None:
    clues = [[None, 0, None, None],
             [None, None, None, None],
             [2, None, 3, None],
             [None, None, None, 1]]
    sols = solve(clues)
    assert len(sols) == 1
    expected = {((1, 0), (1, 1)), ((1, 0), (2, 0)), ((1, 1), (2, 1)), ((2, 0), (3, 0)),
                ((2, 1), (3, 1)), ((2, 2), (2, 3)), ((2, 2), (3, 2)), ((2, 3), (3, 3)),
                ((3, 0), (4, 0)), ((3, 1), (3, 2)), ((3, 3), (4, 3)), ((4, 0), (4, 1)),
                ((4, 1), (4, 2)), ((4, 2), (4, 3))}
    assert sols[0] == expected
    # The answer is unique among all 9349 loops of the 4 by 4 board.
    assert [s for s in loops_of(4, 4) if is_solution(clues, s)] == [expected]


def test_solver_against_edge_brute_force() -> None:
    rng = random.Random(21)
    for h, w, trials in ((1, 2, 10), (2, 2, 20), (2, 3, 1)):
        loops = loops_of(h, w)
        for _ in range(trials):
            full = full_clues(h, w, rng.choice(loops))
            clues = [[v if rng.random() < 0.5 else None for v in row] for row in full]
            if rng.random() < 0.2:
                clues[rng.randrange(h)][rng.randrange(w)] = rng.randint(0, 3)
            expected = edge_brute_force(clues)
            assert {key(s) for s in solve(clues)} == expected


def test_solver_against_loop_enumeration() -> None:
    rng = random.Random(22)
    for h, w in ((3, 3), (3, 4), (4, 4)):
        loops = loops_of(h, w)
        for _ in range(4):
            full = full_clues(h, w, rng.choice(loops))
            clues = [[v if rng.random() < 0.4 else None for v in row] for row in full]
            expected = {key(s) for s in loops if is_solution(clues, s)}
            assert {key(s) for s in solve(clues)} == expected
