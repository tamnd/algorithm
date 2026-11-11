# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tunstall-coding/. The authors are listed in prov/D6TXZ9.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from tunstall_coding import (
    build_dictionary,
    decode,
    encode,
    expected_parse_length,
    inner_node_sum,
    word_prob,
)


def entropy(probs) -> float:
    return -sum(float(p) * math.log2(float(p)) for p in probs)


def random_probs(rng: random.Random, sigma: int) -> list[F]:
    raw = [rng.randint(1, 20) for _ in range(sigma)]
    return [F(x, sum(raw)) for x in raw]


def is_complete_and_proper(words, sigma: int) -> bool:
    """Prefix-free, and every inner node has all sigma children."""
    ws = set(words)
    inner = {w[:k] for w in ws for k in range(len(w))}
    if ws & inner:
        return False
    return all(u + (s,) in ws or u + (s,) in inner for u in inner for s in range(sigma))


def all_complete_dictionaries(sigma: int, size: int):
    """Every complete proper dictionary with `size` words, as sorted tuples."""
    seen = {tuple(sorted((s,) for s in range(sigma)))}
    frontier = set(seen)
    while frontier:
        nxt = set()
        for d in frontier:
            if len(d) + sigma - 1 > size:
                continue
            for x in d:
                new = tuple(sorted([w for w in d if w != x] + [x + (s,) for s in range(sigma)]))
                if new not in seen:
                    seen.add(new)
                    nxt.add(new)
        frontier = nxt
    return [d for d in seen if len(d) == size]


def test_worked_example() -> None:
    p = [F(7, 10), F(3, 10)]  # a = 0, b = 1
    words = build_dictionary(p, 3)
    names = ["".join("ab"[s] for s in w) for w in words]
    assert names == ["aaaaa", "aaaab", "aaab", "aab", "aba", "abb", "ba", "bb"]
    # E[L] = 1 + .7 + .49 + .343 + .2401 + .3 + .21, the inner nodes a, aa, aaa, aaaa, b, ab and the root.
    assert expected_parse_length(p, words) == F(32831, 10000)
    assert inner_node_sum(p, words) == F(32831, 10000)
    # aaaaa | aab | ba | abb | aaab: 17 symbols in 5 codewords of 3 bits.
    msg = [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1]
    assert encode(msg, words, 2) == [0, 3, 6, 5, 2]
    # A tail "aa" is completed to "aaaaa".
    assert encode([1, 1, 0, 0], words, 2) == [7, 0]
    assert decode([7, 0], words, 4) == [1, 1, 0, 0]


def test_expected_parse_length_is_the_inner_node_sum() -> None:
    rng = random.Random(1967)
    for _ in range(150):
        sigma = rng.randint(2, 5)
        p = random_probs(rng, sigma)
        bits = rng.randint(math.ceil(math.log2(sigma)), 7)
        words = build_dictionary(p, bits)
        assert sum(word_prob(p, w) for w in words) == 1
        assert is_complete_and_proper(words, sigma)
        assert 2**bits - sigma + 1 < len(words) <= 2**bits
        assert expected_parse_length(p, words) == inner_node_sum(p, words)


def test_round_trip() -> None:
    rng = random.Random(72)
    for _ in range(100):
        sigma = rng.randint(2, 6)
        p = random_probs(rng, sigma)
        bits = rng.randint(math.ceil(math.log2(sigma)), 6)
        words = build_dictionary(p, bits)
        msg = rng.choices(range(sigma), weights=[float(x) for x in p], k=rng.randint(0, 300))
        out = encode(msg, words, sigma)
        assert all(0 <= i < 2**bits for i in out)
        assert decode(out, words, len(msg)) == msg


def test_tunstall_maximizes_the_expected_parse_length() -> None:
    rng = random.Random(1972)
    # (sigma, B, the dictionary size that Tunstall reaches for 2^B)
    for sigma, bits, size in ((2, 2, 4), (2, 3, 8), (3, 3, 7), (4, 4, 16)):
        dicts = all_complete_dictionaries(sigma, size)
        for _ in range(4):
            p = random_probs(rng, sigma)
            words = build_dictionary(p, bits)
            assert len(words) == size
            best = max(expected_parse_length(p, d) for d in dicts)
            assert expected_parse_length(p, words) == best


def test_rate_tends_to_entropy() -> None:
    for p in ([F(7, 10), F(3, 10)], [F(1, 2), F(1, 4), F(1, 4)], [F(9, 10), F(1, 20), F(1, 20)]):
        h = entropy(p)
        pmin = float(min(p))
        gaps = []
        for bits in range(2, 11):
            words = build_dictionary(p, bits)
            rate = bits / float(expected_parse_length(p, words))
            # H(W) = H E[L] and log2 M + log2 pmin <= H(W) <= log2 M <= B.
            assert rate >= h - 1e-12
            low = math.log2(len(words)) + math.log2(pmin)
            if low > 0:
                assert rate <= h * bits / low + 1e-9
            gaps.append(rate - h)
        assert gaps[-1] < gaps[0]
        assert gaps[-1] < 0.25 * h


def test_inner_nodes_outweigh_leaves() -> None:
    rng = random.Random(3)
    for _ in range(50):
        sigma = rng.randint(2, 4)
        p = random_probs(rng, sigma)
        words = build_dictionary(p, 6)
        inner = {w[:k] for w in words for k in range(len(w))}
        assert min(word_prob(p, u) for u in inner) >= max(word_prob(p, w) for w in words)


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        build_dictionary([F(1)], 3)
    with pytest.raises(ValueError):
        build_dictionary([F(1, 2), F(1, 3)], 3)
    with pytest.raises(ValueError):
        build_dictionary([F(1, 5)] * 5, 2)
    # B = log2(sigma): the dictionary is the alphabet itself.
    assert build_dictionary([F(1, 4)] * 4, 2) == [(0,), (1,), (2,), (3,)]
