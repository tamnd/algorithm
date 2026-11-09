# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dynamic-partial-order-reduction/. The authors are listed in prov/EKPZ7C.jsonl.

import random

from dynamic_partial_order_reduction import (
    dependent,
    dynamic_partial_order_reduction,
    enabled,
    initial,
    step,
)


def random_program(rng):
    prog = []
    for _ in range(rng.randint(2, 3)):
        code = []
        for _ in range(rng.randint(1, 3)):
            r = rng.random()
            if r < 0.35:
                code.append(("w", rng.randrange(3), rng.randint(1, 2)))
            elif r < 0.55:
                code.append(("r", rng.randrange(3)))
            elif r < 0.65:
                code.append(("wr", rng.randrange(3)))
            elif r < 0.85:
                code.append(("lock", rng.randrange(2)))
            else:
                code.append(("unlock", rng.randrange(2)))
        prog.append(code)
    return prog


def all_executions(prog, nvars, nlocks):
    """Every maximal execution and its final state, by brute force."""
    out = []
    stack = [(initial(prog, nvars, nlocks), [])]
    while stack:
        s, path = stack.pop()
        en = enabled(prog, s)
        if not en:
            out.append((path, s))
        for i in en:
            stack.append((step(prog, s, i), path + [i]))
    return out


def trace(prog, path):
    """The Mazurkiewicz trace of an execution: its events and the order of dependent pairs."""
    count = [0] * len(prog)
    events = []
    for i in path:
        events.append((i, count[i]))
        count[i] += 1
    pairs = set()
    for a in range(len(events)):
        for b in range(a + 1, len(events)):
            (i, p), (j, q) = events[a], events[b]
            if i != j and dependent(prog[i][p], prog[j][q]):
                pairs.add((events[a], events[b]))
    return frozenset(events), frozenset(pairs)


EXAMPLE = [[("w", 0, 1), ("w", 1, 1)], [("w", 2, 1), ("r", 0)]]


def test_example() -> None:
    terminal, runs = dynamic_partial_order_reduction(EXAMPLE, 3, 0)
    every = all_executions(EXAMPLE, 3, 0)
    assert len(every) == 6
    # Without sleep sets the second run is redundant: same trace as the first.
    assert runs == [[0, 0, 1, 1], [1, 0, 0, 1], [1, 1, 0, 0]]
    assert trace(EXAMPLE, runs[0]) == trace(EXAMPLE, runs[1])
    assert terminal == {s for _, s in every}
    assert len(terminal) == 2


def test_independent_threads_one_run() -> None:
    prog = [[("w", i, 1), ("w", i, 2)] for i in range(4)]
    terminal, runs = dynamic_partial_order_reduction(prog, 4, 0)
    assert len(runs) == 1 and len(terminal) == 1
    assert len(all_executions(prog, 4, 0)) == 2520  # 8! / (2!)^4


def test_all_writers_conflict() -> None:
    # n threads that each write x once: all n! orders are distinct traces.
    for n in (2, 3, 4):
        prog = [[("w", 0, i + 1)] for i in range(n)]
        terminal, runs = dynamic_partial_order_reduction(prog, 1, 0)
        assert len(runs) == [1, 1, 2, 6, 24][n]
        assert len(terminal) == n


def test_random_against_full_exploration() -> None:
    rng = random.Random(2005)
    explored = total = 0
    for _ in range(800):
        prog = random_program(rng)
        every = all_executions(prog, 3, 2)
        terminal, runs = dynamic_partial_order_reduction(prog, 3, 2)
        assert terminal == {s for _, s in every}
        want = {trace(prog, p) for p, _ in every}
        got = {trace(prog, p) for p in runs}
        assert got == want
        assert len(want) <= len(runs) <= len(every)
        assert len(set(map(tuple, runs))) == len(runs)
        explored += len(runs)
        total += len(every)
    assert explored < total


def test_single_thread_and_empty() -> None:
    assert dynamic_partial_order_reduction([[]], 1, 0)[1] == [[]]
    terminal, runs = dynamic_partial_order_reduction([[("w", 0, 1), ("r", 0)]], 1, 0)
    assert runs == [[0, 0]] and len(terminal) == 1
