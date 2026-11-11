# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/enumerative-coding/. The authors are listed in prov/HHYSRG.jsonl.

import itertools
import math
import random
from fractions import Fraction
from math import comb

import pytest

from enumerative_coding import (code_length, cover_rank, decode, encode, multinomial, rank, rank_multiset,
                                type_counter, unrank, unrank_multiset)


def test_page_example() -> None:
    x = [int(c) for c in "0001000000100000"]
    assert rank(x) == (2, comb(12, 2) + comb(5, 1)) == (2, 71)
    assert unrank(16, 2, 71) == x
    code = encode(x)
    assert len(code) == 5 + 7 == code_length(16, 2)
    assert decode(code, 16) == x
    assert [rank(list(map(int, s)))[1] for s in ("0011", "0101", "0110", "1001", "1010", "1100")] == list(range(6))


@pytest.mark.parametrize("n", range(0, 13))
def test_bijection_by_enumeration(n: int) -> None:
    seen: dict[int, list[int]] = {k: [] for k in range(n + 1)}
    for x in itertools.product((0, 1), repeat=n):  # lexicographic order
        k, r = rank(x)
        assert k == sum(x)
        seen[k].append(r)
        assert unrank(n, k, r) == list(x)
        assert decode(encode(x), n) == list(x)
    for k in range(n + 1):
        # Ranks in lexicographic order are exactly 0, 1, ..., C(n, k) - 1.
        assert seen[k] == list(range(comb(n, k)))


def _h(p: float) -> float:
    return 0.0 if p in (0.0, 1.0) else -p * math.log2(p) - (1 - p) * math.log2(1 - p)


def test_length_bounds() -> None:
    for n in range(1, 300, 7):
        for k in range(0, n + 1):
            nh = n * _h(k / n)
            lg_c = math.log2(comb(n, k))
            assert nh - math.log2(n + 1) - 1e-9 <= lg_c <= nh + 1e-9
            assert code_length(n, k) <= nh + math.log2(n + 1) + 2
    rng = random.Random(1973)
    x = [1 if rng.random() < 0.1 else 0 for _ in range(4000)]
    code = encode(x)
    assert decode(code, len(x)) == x
    k = sum(x)
    assert len(code) <= len(x) * _h(k / len(x)) + math.log2(len(x) + 1) + 2


def test_laplace_equivalence() -> None:
    # The sequential Laplace estimator gives every sequence the probability 1 / ((n + 1) C(n, k)).
    for x in itertools.product((0, 1), repeat=7):
        p = Fraction(1)
        ones = 0
        for i, b in enumerate(x):
            p *= Fraction(ones + 1 if b else i - ones + 1, i + 2)
            ones += b
        assert p == Fraction(1, (len(x) + 1) * comb(len(x), sum(x)))


def test_cover_general_form_and_multiset() -> None:
    n = 9
    for k in range(n + 1):
        count = type_counter(n, [n - k, k])
        for x in itertools.combinations(range(n), k):
            bits = [1 if i in x else 0 for i in range(n)]
            assert cover_rank(bits, 2, count) == rank(bits)[1]
    counts = [2, 1, 3]
    seqs = sorted(set(itertools.permutations([0, 0, 1, 2, 2, 2])))
    assert len(seqs) == multinomial(counts) == 60
    for r, s in enumerate(seqs):
        assert rank_multiset(list(s), 3) == (counts, r)
        assert unrank_multiset(counts, r) == list(s)


def test_errors() -> None:
    with pytest.raises(ValueError):
        unrank(5, 2, comb(5, 2))
    with pytest.raises(ValueError):
        rank([0, 2])
    assert encode([]) == [] and decode([], 0) == []
