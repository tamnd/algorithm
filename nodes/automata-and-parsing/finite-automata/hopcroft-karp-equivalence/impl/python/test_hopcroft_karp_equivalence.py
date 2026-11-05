# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hopcroft-karp-equivalence/. The authors are listed in prov/R0H62M.jsonl.

import itertools
import random

from hopcroft_karp_equivalence import DisjointSet, hopcroft_karp_equivalent


def accepts(delta, start, finals, word) -> bool:
    q = start
    for a in word:
        q = delta[q][a]
    return q in finals


def words(sigma: int, max_len: int):
    for n in range(max_len + 1):
        yield from itertools.product(range(sigma), repeat=n)


def brute_equivalent(d1, s1, f1, d2, s2, f2) -> bool:
    # two DFAs with n1 and n2 states that differ also differ on a word of length <= n1 + n2 - 2
    sigma = len(d1[0])
    bound = max(0, len(d1) + len(d2) - 2)
    return all(accepts(d1, s1, f1, w) == accepts(d2, s2, f2, w) for w in words(sigma, bound))


def check(d1, s1, f1, d2, s2, f2) -> bool:
    eq, w = hopcroft_karp_equivalent(d1, s1, f1, d2, s2, f2)
    assert eq == brute_equivalent(d1, s1, f1, d2, s2, f2)
    if eq:
        assert w is None
    else:
        assert accepts(d1, s1, f1, w) != accepts(d2, s2, f2, w)
        assert len(w) <= len(d1) + len(d2) - 2
    return eq


def counter(m: int, finals) -> list[list[int]]:
    # count the a's modulo m over {a, b}
    return [[(q + 1) % m, q] for q in range(m)]


def test_examples() -> None:
    assert hopcroft_karp_equivalent(counter(2, None), 0, {0}, counter(3, None), 0, {0}) == (False, (0, 0))
    assert hopcroft_karp_equivalent(counter(2, None), 0, {0}, counter(4, None), 0, {0, 2}) == (True, None)


def test_edges() -> None:
    empty, full = ([[0, 0]], 0, set()), ([[0, 0]], 0, {0})
    assert check(*empty, *empty)
    assert check(*full, *full)
    assert not check(*empty, *full)
    # unreachable accepting state does not matter
    assert check([[0], [1]], 0, {1}, [[0]], 0, set())
    # dead states: "exactly one symbol" with and without a dead sink of size 2
    assert check([[1], [2], [2]], 0, {1}, [[1], [2], [3], [2]], 0, {1})
    # one-letter alphabet, the tight family for the length of a counterexample
    for m in range(2, 7):
        cycle = [[(q + 1) % m] for q in range(m)]
        chain = [[min(q + 1, m)] for q in range(m + 1)]
        fchain = {k for k in range(m) if k % m == m - 1}
        eq, w = hopcroft_karp_equivalent(cycle, 0, {m - 1}, chain, 0, fchain)
        assert not eq and len(w) == 2 * m - 1


def test_disjoint_set() -> None:
    ds = DisjointSet(6)
    ds.union(0, 1)
    ds.union(2, 3)
    ds.union(1, 3)
    assert ds.find(0) == ds.find(2) and ds.find(4) != ds.find(0)


def random_dfa(rng: random.Random, n: int, sigma: int):
    return [[rng.randrange(n) for _ in range(sigma)] for _ in range(n)]


def split_copy(rng: random.Random, delta, start, finals):
    """An equivalent DFA with each state doubled and the copies chosen at random."""
    n = len(delta)
    d2 = [[delta[q % n][a] + n * rng.randrange(2) for a in range(len(delta[0]))] for q in range(2 * n)]
    return d2, start, {q for q in range(2 * n) if q % n in finals}


def test_random_against_brute_force() -> None:
    rng = random.Random(1971)
    equal = 0
    for t in range(800):
        sigma = rng.randint(1, 3)
        n1 = rng.randint(1, 4)
        d1 = random_dfa(rng, n1, sigma)
        s1 = rng.randrange(n1)
        mode = t % 5
        if mode == 0:
            f1 = set()
        elif mode == 1:
            f1 = set(range(n1))
        else:
            f1 = {q for q in range(n1) if rng.random() < 0.5}
        if t % 2 == 0 and n1 <= 3:
            d2, s2, f2 = split_copy(rng, d1, s1, f1)
        else:
            n2 = rng.randint(1, 4)
            d2 = random_dfa(rng, n2, sigma)
            s2 = rng.randrange(n2)
            f2 = set() if mode == 0 else {q for q in range(n2) if rng.random() < 0.5}
        if sigma == 3 and len(d1) + len(d2) > 7:
            continue
        equal += check(d1, s1, f1, d2, s2, f2)
    assert equal >= 100
