# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/subset-construction/. The authors are listed in prov/19CF15.jsonl.

import itertools
import random

from subset_construction import EPS, close, subset_construction


def words(alphabet, max_len):
    for k in range(max_len + 1):
        for t in itertools.product(alphabet, repeat=k):
            yield "".join(t)


def nfa_accepts(delta, start, accepting, w):
    """Oracle: search the configurations (state, position), with epsilon-moves."""
    seen = {(start, 0)}
    stack = [(start, 0)]
    while stack:
        q, i = stack.pop()
        if i == len(w) and q in accepting:
            return True
        nxt = [(r, i) for r in delta.get((q, EPS), ())]
        if i < len(w):
            nxt += [(r, i + 1) for r in delta.get((q, w[i]), ())]
        for c in nxt:
            if c not in seen:
                seen.add(c)
                stack.append(c)
    return False


def dfa_accepts(table, final, w):
    s = 0
    for a in w:
        s = table[s][a]
    return s in final


def check(alphabet, delta, start, accepting, n_states, max_len=6):
    subsets, table, final = subset_construction(alphabet, delta, start, accepting)
    assert len(subsets) == len(set(subsets)) <= 2**n_states
    for i, s in enumerate(subsets):
        assert close(s, delta) == s
        assert set(table[i]) == set(alphabet)
        assert (i in final) == bool(s & set(accepting))
    for w in words(alphabet, max_len):
        assert dfa_accepts(table, final, w) == nfa_accepts(delta, start, set(accepting), w), w
    return subsets, table, final


def test_example():
    # a*b* union (ab)*, with epsilon-moves
    delta = {(0, EPS): [1, 3], (1, "a"): [1], (1, EPS): [2], (2, "b"): [2], (3, "a"): [4], (4, "b"): [3]}
    subsets, table, final = check("ab", delta, 0, {2, 3}, 5, 8)
    assert subsets == [
        frozenset({0, 1, 2, 3}),
        frozenset({1, 2, 4}),
        frozenset({2}),
        frozenset({1, 2}),
        frozenset({2, 3}),
        frozenset(),
        frozenset({4}),
        frozenset({3}),
    ]
    assert final == {0, 1, 2, 3, 4, 7}
    assert table[1] == {"a": 3, "b": 4} and table[7] == {"a": 6, "b": 5}


def test_nth_from_end_needs_all_subsets():
    for n in range(1, 7):
        delta = {(0, "a"): [0, 1], (0, "b"): [0]}
        for i in range(1, n):
            delta[(i, "a")] = [i + 1]
            delta[(i, "b")] = [i + 1]
        subsets, _, _ = check("ab", delta, 0, {n}, n + 1, 7)
        assert len(subsets) == 2**n


def test_edges():
    # empty language: no accepting state
    subsets, table, final = check("ab", {(0, "a"): [1], (1, "b"): [0]}, 0, set(), 2)
    assert final == set()
    # Sigma*: one accepting state with loops
    subsets, table, final = check("ab", {(0, "a"): [0], (0, "b"): [0]}, 0, {0}, 1)
    assert len(subsets) == 1 and final == {0}
    # no transitions at all: the dead state appears
    subsets, table, final = check("ab", {}, 0, {0}, 1)
    assert subsets == [frozenset({0}), frozenset()]
    # unreachable states and a dead state
    delta = {(0, "a"): [1], (1, "a"): [1], (2, "b"): [0], (3, "a"): [3], (3, "b"): [3]}
    subsets, _, _ = check("ab", delta, 0, {1, 2}, 4)
    assert all(2 not in s and 3 not in s for s in subsets)
    # a cycle of epsilon-moves
    delta = {(0, EPS): [1], (1, EPS): [2], (2, EPS): [0], (2, "a"): [3]}
    subsets, _, _ = check("ab", delta, 0, {3}, 4)
    assert subsets[0] == frozenset({0, 1, 2})
    # a long chain of epsilon-moves (no recursion limit)
    k = 5000
    delta = {(i, EPS): [i + 1] for i in range(k)}
    assert close([0], delta) == frozenset(range(k + 1))


def test_random_against_brute_force():
    rng = random.Random(1959)
    for trial in range(600):
        n = rng.randint(1, 5)
        alphabet = "ab" if trial % 3 else "abc"
        delta = {}
        for q in range(n):
            for a in list(alphabet) + [EPS]:
                p = 0.15 if a == EPS else 0.35
                targets = [r for r in range(n) if rng.random() < p]
                if targets:
                    delta[(q, a)] = targets
        accepting = {q for q in range(n) if rng.random() < 0.35}
        check(alphabet, delta, rng.randrange(n), accepting, n, 5)
