# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/irving-stable-roommates/. The authors are listed in prov/Q2A2ZX.jsonl.

import random

from irving_stable_roommates import irving_stable_roommates


def acceptable(prefs, a, b):
    return b in prefs[a] and a in prefs[b]


def prefers(prefs, a, b, mate_a):
    """True if a prefers b to its partner mate_a (None means single)."""
    if mate_a is None:
        return True
    return prefs[a].index(b) < prefs[a].index(mate_a)


def is_stable(prefs, mate):
    n = len(prefs)
    for x in range(n):
        y = mate[x]
        if y is not None:
            assert mate[y] == x and acceptable(prefs, x, y)
    for a in range(n):
        for b in range(a + 1, n):
            if mate[a] == b or not acceptable(prefs, a, b):
                continue
            if prefers(prefs, a, b, mate[a]) and prefers(prefs, b, a, mate[b]):
                return False
    return True


def all_matchings(prefs):
    """Every matching that uses only mutually acceptable pairs."""
    n = len(prefs)
    mate = [None] * n

    def rec(x):
        while x < n and mate[x] is not None:
            x += 1
        if x == n:
            yield list(mate)
            return
        yield from rec(x + 1)  # x stays single
        for y in prefs[x]:
            if y > x and mate[y] is None and acceptable(prefs, x, y):
                mate[x], mate[y] = y, x
                yield from rec(x + 1)
                mate[x] = mate[y] = None

    yield from rec(0)


def has_stable(prefs):
    return any(is_stable(prefs, m) for m in all_matchings(prefs))


def check(prefs):
    got = irving_stable_roommates(prefs)
    if got is None:
        assert not has_stable(prefs)
    else:
        assert is_stable(prefs, got)
    return got


def test_empty_instance():
    assert irving_stable_roommates([]) == []
    assert irving_stable_roommates([[]]) == [None]
    assert irving_stable_roommates([[], []]) == [None, None]


def test_one_pair_and_one_sided_list():
    assert irving_stable_roommates([[1], [0]]) == [1, 0]
    # 0 lists 1 but 1 does not list 0: they cannot be matched
    assert irving_stable_roommates([[1], []]) == [None, None]


def test_no_stable_matching():
    # A, B, C each rank the next one first; D is last for everybody
    prefs = [[1, 2, 3], [2, 0, 3], [0, 1, 3], [0, 1, 2]]
    assert irving_stable_roommates(prefs) is None
    assert not has_stable(prefs)


def test_odd_cycle_three_agents():
    # three agents in a cycle: one is single, and some pair always blocks
    prefs = [[1, 2], [2, 0], [0, 1]]
    assert irving_stable_roommates(prefs) is None
    # with agreed tastes a stable matching exists and one agent is single
    prefs = [[1, 2], [0, 2], [0, 1]]
    assert irving_stable_roommates(prefs) == [1, 0, None]


def test_two_stable_matchings():
    # A:B,D,C  B:C,D,A  C:A,D,B  D:C,B,A
    prefs = [[1, 3, 2], [2, 3, 0], [0, 3, 1], [2, 1, 0]]
    mate = check(prefs)
    assert mate in ([1, 0, 3, 2], [2, 3, 0, 1])


def test_worked_example():
    prefs = [[1, 3, 2], [2, 3, 0], [0, 3, 1], [2, 1, 0]]
    assert irving_stable_roommates(prefs) == [2, 3, 0, 1]


def test_bipartite_instance_gives_a_stable_marriage():
    # men 0..2, women 3..5, cyclic preferences: always solvable
    prefs = [[3, 4, 5], [4, 5, 3], [5, 3, 4], [1, 2, 0], [2, 0, 1], [0, 1, 2]]
    mate = check(prefs)
    assert mate is not None and None not in mate


def test_long_chain_no_recursion_limit():
    # agents 0..n-1, each prefers the next one, then the previous one
    n = 2000
    prefs = [[y for y in (x + 1, x - 1) if 0 <= y < n] for x in range(n)]
    mate = irving_stable_roommates(prefs)
    assert mate is not None
    assert all(mate[mate[x]] == x for x in range(n) if mate[x] is not None)


def test_random_against_brute_force():
    rng = random.Random(20261105)
    solved = unsolved = 0
    for _ in range(1500):
        n = rng.randint(0, 8)
        p = rng.random()
        prefs = []
        for x in range(n):
            others = [y for y in range(n) if y != x and rng.random() < p + 0.2]
            rng.shuffle(others)
            prefs.append(others)
        if check(prefs) is None:
            unsolved += 1
        else:
            solved += 1
    assert solved > 100 and unsolved > 100


def test_random_complete_lists():
    rng = random.Random(7)
    for _ in range(300):
        n = 2 * rng.randint(1, 4)
        prefs = []
        for x in range(n):
            others = [y for y in range(n) if y != x]
            rng.shuffle(others)
            prefs.append(others)
        mate = check(prefs)
        if mate is not None:
            assert None not in mate


def test_bad_input():
    for bad in ([[0]], [[1, 1], [0]], [[2], [0]]):
        try:
            irving_stable_roommates(bad)
        except ValueError:
            continue
        raise AssertionError("expected ValueError")
