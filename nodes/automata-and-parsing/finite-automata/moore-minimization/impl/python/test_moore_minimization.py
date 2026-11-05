# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/moore-minimization/. The authors are listed in prov/7CHN37.jsonl.

import itertools
import random

from moore_minimization import moore_minimize, reachable


def accepts(delta, start, finals, word) -> bool:
    q = start
    for a in word:
        q = delta[q][a]
    return q in finals


def words(sigma: int, max_len: int):
    for n in range(max_len + 1):
        yield from itertools.product(range(sigma), repeat=n)


def brute_min_size(delta, start, finals) -> int:
    """Count reachable states with distinct acceptance on all words of length <= n."""
    n, sigma = len(delta), len(delta[0])
    ws = list(words(sigma, n))
    return len({tuple(accepts(delta, q, finals, w) for w in ws) for q in reachable(delta, start)})


def check(delta, start, finals) -> None:
    m, cls = moore_minimize(delta, start, finals)
    n, sigma = len(delta), len(delta[0])
    assert len(m.delta) == brute_min_size(delta, start, finals)
    # two DFAs with n and k states that differ also differ on a word of length <= n + k - 2
    for w in words(sigma, max(0, n + len(m.delta) - 2)):
        assert accepts(delta, start, finals, w) == accepts(m.delta, m.start, m.finals, w)
    for q, c in cls.items():
        for a in range(sigma):
            assert m.delta[c][a] == cls[delta[q][a]]


def test_example() -> None:
    delta = [[1, 2], [3, 4], [4, 3], [5, 5], [5, 5], [5, 5], [6, 3]]
    m, cls = moore_minimize(delta, 0, {3, 4, 6})
    assert m.delta == [[1, 1], [2, 2], [3, 3], [3, 3]]
    assert m.start == 0 and m.finals == frozenset({2})
    assert cls == {0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: 3}
    check(delta, 0, {3, 4, 6})


def test_edges() -> None:
    # empty language, Sigma*, one state, unreachable and dead states
    m, _ = moore_minimize([[0, 0]], 0, set())
    assert len(m.delta) == 1 and not m.finals
    m, _ = moore_minimize([[0, 0]], 0, {0})
    assert len(m.delta) == 1 and m.finals == frozenset({0})
    m, _ = moore_minimize([[1], [0], [2]], 0, {2})
    assert len(m.delta) == 1 and not m.finals
    m, _ = moore_minimize([[1, 1], [0, 0]], 0, {0, 1})
    assert len(m.delta) == 1 and m.finals == frozenset({0})
    for delta, f in (([[1], [2], [2]], {1}), ([[1, 2], [2, 2], [2, 2]], {1}), ([[0]], set())):
        check(delta, 0, f)


def test_worst_case_rounds() -> None:
    # the chain 0 -> 1 -> ... -> n-1 with F = {n-1} is already minimal
    for n in range(1, 9):
        delta = [[min(i + 1, n - 1)] for i in range(n)]
        m, _ = moore_minimize(delta, 0, {n - 1})
        assert len(m.delta) == n


def test_random_against_brute_force() -> None:
    rng = random.Random(7377)
    for t in range(600):
        sigma = rng.randint(1, 3)
        n = rng.randint(1, 6 if sigma < 3 else 5)
        delta = [[rng.randrange(n) for _ in range(sigma)] for _ in range(n)]
        mode = t % 5
        if mode == 0:
            finals = set()
        elif mode == 1:
            finals = set(range(n))
        else:
            finals = {q for q in range(n) if rng.random() < 0.4}
        check(delta, rng.randrange(n), finals)
