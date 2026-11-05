# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lstar-algorithm/. The authors are listed in prov/2BJ5ME.jsonl.

import itertools
import random
from collections import deque

from lstar_algorithm import lstar


def accepts(dfa, word) -> bool:
    delta, q, finals = dfa
    for a in word:
        q = delta[q][a]
    return q in finals


def words(sigma: int, max_len: int):
    for n in range(max_len + 1):
        yield from itertools.product(range(sigma), repeat=n)


def shortest_difference(target, hyp, sigma):
    # breadth-first search of the product; returns a shortest string accepted by exactly one
    start = (target[1], hyp[1])
    parent = {start: None}
    queue = deque([start])
    while queue:
        p, q = queue.popleft()
        if (p in target[2]) != (q in hyp[2]):
            word = []
            node = (p, q)
            while parent[node] is not None:
                node, a = parent[node]
                word.append(a)
            return tuple(reversed(word))
        for a in range(sigma):
            nxt = (target[0][p][a], hyp[0][q][a])
            if nxt not in parent:
                parent[nxt] = ((p, q), a)
                queue.append(nxt)
    return None


class Teacher:
    """Answers queries about a target DFA and counts them."""

    def __init__(self, target, sigma, rng=None, max_pad=0):
        self.target, self.sigma, self.rng, self.max_pad = target, sigma, rng, max_pad
        self.mq = 0
        self.eq = 0
        self.asked = set()
        self.sizes = []
        self.longest = 0

    def member(self, w):
        assert w not in self.asked, "a membership query was repeated"
        self.asked.add(w)
        self.mq += 1
        return accepts(self.target, w)

    def equivalent(self, hyp):
        self.eq += 1
        self.sizes.append(len(hyp[0]))
        c = shortest_difference(self.target, hyp, self.sigma)
        if c is not None and self.rng is not None and self.max_pad:
            # a longer counterexample: pad with a random suffix and keep it if it still differs
            for _ in range(10):
                pad = tuple(self.rng.randrange(self.sigma) for _ in range(self.rng.randint(0, self.max_pad)))
                pre = tuple(self.rng.randrange(self.sigma) for _ in range(self.rng.randint(0, self.max_pad)))
                w = pre + pad
                if accepts(self.target, w) != accepts(hyp, w):
                    c = w
                    break
        if c is not None:
            assert accepts(self.target, c) != accepts(hyp, c)
            self.longest = max(self.longest, len(c))
        return c


def brute_min_size(target, sigma) -> int:
    # reachable states, grouped by their answers on all words of length <= n - 1
    delta, start, finals = target
    n = len(delta)
    seen, stack = {start}, [start]
    while stack:
        q = stack.pop()
        for a in range(sigma):
            if delta[q][a] not in seen:
                seen.add(delta[q][a])
                stack.append(delta[q][a])
    test = list(words(sigma, max(0, n - 1)))
    sigs = set()
    for q in seen:
        sigs.add(tuple(accepts((delta, q, finals), w) for w in test))
    return len(sigs)


def check(target, sigma, rng=None, max_pad=0):
    teacher = Teacher(target, sigma, rng, max_pad)
    hyp = lstar(sigma, teacher.member, teacher.equivalent)
    n = brute_min_size(target, sigma)
    # two DFAs with n1 and n2 states that differ also differ on a word of length <= n1 + n2 - 2;
    # enumerate up to that bound when it is small, and search the product as well
    bound = min(len(hyp[0]) + len(target[0]) - 2, 9 if sigma <= 2 else 7)
    assert all(accepts(hyp, w) == accepts(target, w) for w in words(sigma, max(0, bound)))
    assert shortest_difference(target, hyp, sigma) is None
    assert len(hyp[0]) == n
    assert teacher.eq <= n
    assert all(x < y for x, y in zip(teacher.sizes, teacher.sizes[1:]))
    m = teacher.longest
    assert teacher.mq <= (sigma + 1) * (n + m * (n - 1)) * n
    return hyp, teacher


def even_even():
    # states (parity of a, parity of b): 0 = (0,0), 1 = (1,0), 2 = (0,1), 3 = (1,1)
    return ([[1, 2], [0, 3], [3, 0], [2, 1]], 0, {0})


def test_example() -> None:
    hyp, teacher = check(even_even(), 2)
    assert len(hyp[0]) == 4
    assert teacher.eq == 2
    assert teacher.sizes == [2, 4]
    assert teacher.mq == 19
    assert accepts(hyp, (0, 0, 1, 1)) and not accepts(hyp, (1, 0))


def test_first_counterexample() -> None:
    target = even_even()
    first = []

    def eq(h):
        c = shortest_difference(target, h, 2)
        first.append(c)
        return c

    lstar(2, lambda w: accepts(target, w), eq)
    assert first == [(1, 0), None]


def test_edges() -> None:
    empty = ([[0, 0]], 0, set())
    full = ([[0, 0]], 0, {0})
    assert len(check(empty, 2)[0][0]) == 1
    assert len(check(full, 2)[0][0]) == 1
    # one-letter alphabet: length divisible by 5
    hyp, _ = check(([[(q + 1) % 5] for q in range(5)], 0, {0}), 1)
    assert len(hyp[0]) == 5
    # an unreachable accepting state and two equivalent dead states
    hyp, _ = check(([[1, 2], [3, 3], [4, 4], [4, 3], [3, 4], [0, 0]], 0, {1, 5}), 2)
    assert len(hyp[0]) == 3
    # the n-th symbol from the end is a: 2^n states
    for k in range(1, 5):
        delta = [[((q << 1) | 1) & ((1 << k) - 1), (q << 1) & ((1 << k) - 1)] for q in range(1 << k)]
        hyp, _ = check((delta, 0, {q for q in range(1 << k) if q >> (k - 1) & 1}), 2)
        assert len(hyp[0]) == 1 << k


def random_dfa(rng, n, sigma):
    delta = [[rng.randrange(n) for _ in range(sigma)] for _ in range(n)]
    p = rng.choice([0.0, 0.3, 0.5, 1.0])
    finals = {q for q in range(n) if rng.random() < p}
    return delta, rng.randrange(n), finals


def test_random() -> None:
    rng = random.Random(1987)
    for t in range(700):
        sigma = rng.randint(1, 3)
        n = rng.randint(1, 6 if sigma <= 2 else 4)
        target = random_dfa(rng, n, sigma)
        check(target, sigma, rng, max_pad=rng.choice([0, 0, 4, 9]))
