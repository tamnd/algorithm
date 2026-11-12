# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nearest-codeword-problem/. The authors are listed in prov/XEFEQH.jsonl.

import random
from itertools import product

from nearest_codeword_problem import (
    coset_weight,
    has_perfect_matching,
    nearest_codeword,
    solve_and_kernel,
    three_dm_to_coset_weight,
)

G74 = [[1, 0, 0, 0, 1, 1, 0], [0, 1, 0, 0, 0, 1, 1], [0, 0, 1, 0, 1, 1, 1], [0, 0, 0, 1, 1, 0, 1]]


def test_page_example():
    c, d = nearest_codeword(G74, (1, 1, 1, 1, 1, 1, 0))
    assert d == 1 and c == (1, 1, 1, 1, 1, 1, 1)
    # A [5, 2, 3] code and a word at distance 2 from it.
    c, d = nearest_codeword([[1, 0, 1, 1, 0], [0, 1, 0, 1, 1]], (1, 1, 0, 0, 0))
    assert d == 2


def test_3dm_examples():
    yes = [(0, 0, 0), (1, 1, 1), (0, 1, 1), (1, 0, 1)]
    no = [(0, 0, 0), (0, 1, 1), (1, 1, 0)]
    for triples, want in [(yes, True), (no, False)]:
        h, s, w = three_dm_to_coset_weight(2, triples)
        assert has_perfect_matching(2, triples) == want
        assert (coset_weight(h, s, w) is not None) == want


def test_reduction_random():
    rng = random.Random(8)
    seen = {True: 0, False: 0}
    for _ in range(400):
        q = rng.randint(1, 3)
        allt = list(product(range(q), repeat=3))
        t = rng.randint(1, min(len(allt), 7))
        triples = rng.sample(allt, t)
        h, s, w = three_dm_to_coset_weight(q, triples)
        want = has_perfect_matching(q, triples)
        e = coset_weight(h, s, w)
        assert (e is not None) == want
        if e is not None:
            chosen = [triples[j] for j in range(len(triples)) if e[j]]
            assert len(chosen) == q
        seen[want] += 1
    assert seen[True] > 20 and seen[False] > 20


def test_syndrome_form_equals_generator_form():
    rng = random.Random(12)
    for _ in range(150):
        r, n = rng.randint(1, 5), rng.randint(2, 9)
        h = [[rng.randrange(2) for _ in range(n)] for _ in range(r)]
        s = tuple(rng.randrange(2) for _ in range(r))
        res = solve_and_kernel(h, s)
        brute = [v for v in product(range(2), repeat=n) if tuple(sum(a * b for a, b in zip(row, v)) % 2 for row in h) == s]
        if res is None:
            assert brute == []
            continue
        y, g = res
        lightest = min(sum(v) for v in brute)
        if g:
            _, d = nearest_codeword(g, y)
        else:
            d = sum(y)
        assert d == lightest
        e = coset_weight(h, s, n)
        assert e is not None and sum(e) == lightest
