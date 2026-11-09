# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sleep-sets/. The authors are listed in prov/DD26ZR.jsonl.

import random

from sleep_sets import (
    dependent,
    enabled,
    full_search,
    initial,
    sleep_set_executions,
    sleep_set_search,
    sleep_sets,
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
    """Every maximal execution, by brute force."""
    out = []
    stack = [(initial(prog, nvars, nlocks), [])]
    while stack:
        s, path = stack.pop()
        en = enabled(prog, s)
        if not en:
            out.append(path)
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
    full, dead, taken = full_search(EXAMPLE, 3, 0)
    visited, sdead, staken = sleep_set_search(EXAMPLE, 3, 0)
    assert len(full) == 11 and len(dead) == 2 and taken == 13
    assert visited == full and sdead == dead
    assert staken == 10
    runs, blocked = sleep_set_executions(EXAMPLE, 3, 0)
    assert len(all_executions(EXAMPLE, 3, 0)) == 6
    assert runs == [[0, 0, 1, 1], [1, 1, 0, 0]] and blocked == 1


def test_random_against_full_search() -> None:
    rng = random.Random(1991)
    saved = 0
    for _ in range(700):
        prog = random_program(rng)
        full, dead, taken = full_search(prog, 3, 2)
        visited, sdead, staken = sleep_set_search(prog, 3, 2)
        assert sdead == dead
        assert sleep_sets(prog, 3, 2) == dead
        assert visited == full  # sleep sets alone keep every state
        assert staken <= taken
        saved += taken - staken
    assert saved > 0


def test_stateless_one_execution_per_trace() -> None:
    rng = random.Random(1996)
    for _ in range(500):
        prog = random_program(rng)
        every = all_executions(prog, 3, 2)
        runs, _ = sleep_set_executions(prog, 3, 2)
        want = {trace(prog, p) for p in every}
        got = [trace(prog, p) for p in runs]
        assert set(got) == want
        assert len(got) == len(want)


def test_single_thread_and_empty() -> None:
    assert sleep_set_search([[]], 1, 0)[2] == 0
    prog = [[("w", 0, 1), ("r", 0)]]
    visited, dead, taken = sleep_set_search(prog, 1, 0)
    assert len(visited) == 3 and taken == 2 and len(dead) == 1
