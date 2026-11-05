# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brzozowski-minimization/. The authors are listed in prov/VRYA87.jsonl.

import itertools
import random

from brzozowski_minimization import brzozowski_minimize, determinize, reverse


def nfa_accepts(nfa, starts, finals, word) -> bool:
    s = set(starts)
    for a in word:
        s = {r for q in s for r in nfa[q][a]}
    return bool(s & set(finals))


def dfa_accepts(dfa, word) -> bool:
    q = dfa.start
    for a in word:
        q = dfa.delta[q][a]
    return q in dfa.finals


def words(sigma: int, max_len: int):
    for n in range(max_len + 1):
        yield from itertools.product(range(sigma), repeat=n)


def count_subsets(nfa, sigma, starts) -> int:
    """Number of reachable subsets of the NFA; a DFA with this many states accepts its language."""
    seen = {frozenset(starts)}
    stack = [frozenset(starts)]
    while stack:
        s = stack.pop()
        for a in range(sigma):
            t = frozenset(r for q in s for r in nfa[q][a])
            if t not in seen:
                seen.add(t)
                stack.append(t)
    return len(seen)


def brute_min_size(nfa, sigma, starts, finals, d: int) -> int:
    """Classes of prefixes x with |x| <= d - 1 by acceptance of xz for all z with |z| <= d - 2."""
    suffixes = list(words(sigma, max(0, d - 2)))
    rows = {}
    for x in words(sigma, d - 1):
        key = frozenset(nfa_run(nfa, starts, x))  # acceptance of xz depends on x only through this set
        if key not in rows:
            rows[key] = tuple(nfa_accepts(nfa, starts, finals, x + z) for z in suffixes)
    return len(set(rows.values()))


def nfa_run(nfa, starts, word) -> set[int]:
    s = set(starts)
    for a in word:
        s = {r for q in s for r in nfa[q][a]}
    return s


def check(nfa, sigma, starts, finals) -> None:
    m = brzozowski_minimize(nfa, sigma, starts, finals)
    k = len(m.delta)
    d = count_subsets(nfa, sigma, starts)
    # every class of a DFA with d states is reached by a word of length <= d - 1,
    # and two inequivalent states differ on a word of length <= d - 2
    assert k == brute_min_size(nfa, sigma, starts, finals, d)
    # two DFAs with d and k states that differ also differ on a word of length <= d + k - 2
    for w in words(sigma, d + k - 2):
        assert dfa_accepts(m, w) == nfa_accepts(nfa, starts, finals, w), w
    for row in m.delta:
        assert len(row) == sigma and all(0 <= r < k for r in row)


def test_example() -> None:
    # (a + b)* a b: 0 loops, 0 -a-> 1, 1 -b-> 2
    nfa = [[{0, 1}, {0}], [set(), {2}], [set(), set()]]
    d1, subsets1 = determinize(reverse(nfa, 2), 2, [2], [0])
    assert subsets1 == [frozenset({2}), frozenset(), frozenset({1}), frozenset({0})]
    assert d1.delta == [[1, 2], [1, 1], [3, 1], [3, 3]] and d1.finals == frozenset({3})
    m = brzozowski_minimize(nfa, 2, [0], [2])
    assert m.delta == [[1, 0], [1, 2], [1, 0]] and m.start == 0 and m.finals == frozenset({2})
    check(nfa, 2, [0], [2])


def test_dfa_with_unreachable_state() -> None:
    delta = [[1, 2], [3, 4], [4, 3], [5, 5], [5, 5], [5, 5], [6, 3]]
    nfa = [[(r,) for r in row] for row in delta]
    m = brzozowski_minimize(nfa, 2, [0], [3, 4, 6])
    assert len(m.delta) == 4
    for w in words(2, 6):
        assert dfa_accepts(m, w) == (len(w) == 2)


def test_edges() -> None:
    # empty language, Sigma*, no transitions at all, dead and unreachable states
    m = brzozowski_minimize([[(0,), (0,)]], 2, [0], [])
    assert len(m.delta) == 1 and not m.finals
    m = brzozowski_minimize([[(0,), (0,)]], 2, [0], [0])
    assert len(m.delta) == 1 and m.finals == frozenset({0})
    m = brzozowski_minimize([[set()]], 1, [0], [0])
    assert len(m.delta) == 2 and dfa_accepts(m, ()) and not dfa_accepts(m, (0,))
    m = brzozowski_minimize([[set()], [set()]], 1, [], [0, 1])
    assert len(m.delta) == 1 and not m.finals
    check([[{1}, {2}], [{1}, {1}], [{2}, {2}], [{3}, {0}]], 2, [0], [1])
    check([[{0, 1}], [{1}]], 1, [0], [0, 1])


def test_reversal_blowup() -> None:
    # DFA for "the n-th symbol is a" (n + 2 states); its reverse needs 2^n subsets
    for n in range(1, 7):
        delta = [[i + 1, i + 1] for i in range(n - 1)] + [[n, n + 1], [n, n], [n + 1, n + 1]]
        nfa = [[(r,) for r in row] for row in delta]
        d1, _ = determinize(reverse(nfa, 2), 2, [n], [0])
        assert len(d1.delta) == 2 ** n
        m = brzozowski_minimize(nfa, 2, [0], [n])
        assert len(m.delta) == n + 2


def random_nfa(rng: random.Random, n: int, sigma: int, p: float):
    return [[{r for r in range(n) if rng.random() < p} for _ in range(sigma)] for _ in range(n)]


def test_random_against_brute_force() -> None:
    rng = random.Random(1962)
    for t in range(600):
        sigma = rng.randint(1, 2)
        n = rng.randint(1, 4 if sigma == 1 else 3)
        mode = t % 6
        if mode == 5:
            # a complete DFA, possibly with unreachable and dead states
            nfa = [[{rng.randrange(n)} for _ in range(sigma)] for _ in range(n)]
            starts = [rng.randrange(n)]
        else:
            nfa = random_nfa(rng, n, sigma, rng.choice((0.2, 0.4, 0.6)))
            starts = [q for q in range(n) if rng.random() < 0.4] or [0]
        if mode == 0:
            finals = []
        elif mode == 1:
            finals = list(range(n))
            for q in range(n):
                for a in range(sigma):
                    nfa[q][a].add(q)  # Sigma* from every start
        else:
            finals = [q for q in range(n) if rng.random() < 0.4]
        check(nfa, sigma, starts, finals)
