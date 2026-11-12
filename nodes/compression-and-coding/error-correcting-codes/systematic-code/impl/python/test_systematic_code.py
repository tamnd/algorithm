# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/systematic-code/. The authors are listed in prov/9C8353.jsonl.

import random
from itertools import product
from math import comb

from systematic_code import encode, information_sets, is_information_set, rref, systematic_form

G74 = [[1, 0, 0, 0, 1, 1, 0], [0, 1, 0, 0, 0, 1, 1], [0, 0, 1, 0, 1, 1, 1], [0, 0, 0, 1, 1, 0, 1]]


def span(g, q):
    k, n = len(g), len(g[0])
    return {tuple(sum(m[i] * g[i][j] for i in range(k)) % q for j in range(n)) for m in product(range(q), repeat=k)}


def test_no_systematic_form_on_first_positions():
    g = [[1, 1, 0, 0], [0, 0, 1, 1]]
    assert not is_information_set(g, (0, 1))
    assert information_sets(g) == [(0, 2), (0, 3), (1, 2), (1, 3)]
    gs, perm = systematic_form(g)
    assert perm == [0, 2, 1, 3]
    assert gs == [[1, 0, 1, 0], [0, 1, 0, 1]]
    assert encode([1, 0], gs, perm) == [1, 1, 0, 0]
    assert encode([0, 1], gs, perm) == [0, 0, 1, 1]


def test_hamming_information_sets():
    assert len(information_sets(G74)) == 28 and comb(7, 4) == 35


def test_scrambled_generator_same_code():
    # A non-systematic generator of the Hamming code: row reduction gives back G74.
    g = [[1, 1, 0, 0, 1, 0, 1], [0, 1, 1, 0, 1, 0, 0], [1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 1, 1, 0, 1]]
    assert span(g, 2) == span(G74, 2)
    gs, perm = systematic_form(g)
    assert perm == list(range(7)) and gs == G74


def test_random_codes():
    rng = random.Random(44)
    done = 0
    while done < 200:
        q = rng.choice([2, 2, 3, 5])
        n = rng.randint(1, 8 if q == 2 else 5)
        k = rng.randint(1, n)
        g = [[rng.randrange(q) for _ in range(n)] for _ in range(k)]
        if len(rref(g, q)[1]) < k:
            continue
        gs, perm = systematic_form(g, q)
        assert [row[:k] for row in gs] == [[int(i == j) for j in range(k)] for i in range(k)]
        assert is_information_set(g, tuple(sorted(perm[:k])), q)
        code = span(g, q)
        words = set()
        for m in product(range(q), repeat=k):
            c = encode(list(m), gs, perm, q)
            assert tuple(c) in code
            assert [c[j] for j in perm[:k]] == list(m)
            words.add(tuple(c))
        assert words == code
        if is_information_set(g, tuple(range(k)), q):
            assert perm == list(range(n))
        done += 1
