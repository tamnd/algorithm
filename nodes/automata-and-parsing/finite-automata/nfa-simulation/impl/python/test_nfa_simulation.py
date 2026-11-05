# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nfa-simulation/. The authors are listed in prov/B4QP59.jsonl.

import itertools
import random

from nfa_simulation import EPS, close, nfa_simulation


def words(alphabet, max_len):
    for k in range(max_len + 1):
        for t in itertools.product(alphabet, repeat=k):
            yield "".join(t)


def oracle(delta, start, accepting, w):
    """Search the configurations (state, position), with epsilon-moves."""
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


def oracle_set(delta, start, w):
    """The set of states in which some run on w ends, by the same search."""
    seen = {(start, 0)}
    stack = [(start, 0)]
    while stack:
        q, i = stack.pop()
        nxt = [(r, i) for r in delta.get((q, EPS), ())]
        if i < len(w):
            nxt += [(r, i + 1) for r in delta.get((q, w[i]), ())]
        for c in nxt:
            if c not in seen:
                seen.add(c)
                stack.append(c)
    return frozenset(q for q, i in seen if i == len(w))


EXAMPLE = {
    (0, EPS): [1, 3],
    (1, "a"): [1],
    (1, EPS): [2],
    (2, "b"): [2],
    (3, "a"): [4],
    (4, "b"): [3],
}


def test_example_from_the_page():
    tr = []
    assert nfa_simulation(EXAMPLE, 0, {2, 3}, "abab", tr)
    assert tr == [frozenset(s) for s in ({0, 1, 2, 3}, {1, 2, 4}, {2, 3}, {4}, {3})]
    tr = []
    assert nfa_simulation(EXAMPLE, 0, {2, 3}, "aab", tr)
    assert tr == [frozenset(s) for s in ({0, 1, 2, 3}, {1, 2, 4}, {1, 2}, {2})]
    tr = []
    assert not nfa_simulation(EXAMPLE, 0, {2, 3}, "bab", tr)
    assert tr == [frozenset(s) for s in ({0, 1, 2, 3}, {2}, set())]
    assert not nfa_simulation(EXAMPLE, 0, {2, 3}, "aba")
    for w in words("ab", 8):
        expected = (w == "a" * w.count("a") + "b" * w.count("b")) or w == "ab" * (len(w) // 2)
        assert nfa_simulation(EXAMPLE, 0, {2, 3}, w) == expected


def test_ends_in_abb():
    d = {(0, "a"): [0, 1], (0, "b"): [0], (1, "b"): [2], (2, "b"): [3]}
    for w in words("ab", 9):
        assert nfa_simulation(d, 0, {3}, w) == w.endswith("abb")


def test_many_runs_but_small_sets():
    d = {(0, "a"): [0, 1], (1, "a"): [0, 1]}
    tr = []
    assert not nfa_simulation(d, 0, set(), "a" * 20 + "c", tr)
    assert tr[1:21] == [frozenset({0, 1})] * 20 and tr[21] == frozenset()


def test_edge_cases():
    # empty language, no transitions, the empty word
    assert not nfa_simulation({}, 0, set(), "")
    assert nfa_simulation({}, 0, {0}, "")
    assert not nfa_simulation({}, 0, {0}, "a")
    # Sigma* with one state
    full = {(0, "a"): [0], (0, "b"): [0]}
    for w in words("ab", 6):
        assert nfa_simulation(full, 0, {0}, w)
    # unreachable accepting state and a dead state
    d = {(0, "a"): [1], (1, "a"): [1], (1, "b"): [1], (2, "a"): [2]}
    for w in words("ab", 6):
        assert nfa_simulation(d, 0, {2}, w) is False
    # an epsilon-cycle
    cyc = {(0, EPS): [1], (1, EPS): [0], (1, "a"): [2], (2, EPS): [0]}
    for w in words("ab", 6):
        assert nfa_simulation(cyc, 0, {0}, w) == (set(w) <= {"a"})
    # a long chain of epsilon-moves needs no recursion
    n = 5000
    chain = {(i, EPS): [i + 1] for i in range(n)}
    chain[(n, "a")] = [0]
    assert close([0], chain) == set(range(n + 1))
    assert nfa_simulation(chain, 0, {n}, "aaa")
    # an iterator as the word
    assert nfa_simulation(full, 0, {0}, iter("abba"))


def random_nfa(rng, n, alphabet, p_edge, p_eps, p_final):
    delta = {}
    for q in range(n):
        for a in alphabet:
            targets = [r for r in range(n) if rng.random() < p_edge]
            if targets:
                delta[(q, a)] = targets
        eps = [r for r in range(n) if rng.random() < p_eps]
        if eps:
            delta[(q, EPS)] = eps
    final = {q for q in range(n) if rng.random() < p_final}
    return delta, final


def test_random_against_brute_force():
    rng = random.Random(20261106)
    for trial in range(700):
        n = rng.randint(1, 6)
        alphabet = "ab" if trial % 3 else "abc"
        p_eps = 0.0 if trial % 2 else rng.choice([0.1, 0.25])
        delta, final = random_nfa(rng, n, alphabet, rng.choice([0.1, 0.3, 0.5]), p_eps, rng.choice([0.0, 0.3, 1.0]))
        for w in words(alphabet, 5 if alphabet == "ab" else 4):
            tr = []
            got = nfa_simulation(delta, 0, final, w, tr)
            assert got == oracle(delta, 0, final, w)
            if len(tr) == len(w) + 1:
                assert tr[-1] == oracle_set(delta, 0, w)
