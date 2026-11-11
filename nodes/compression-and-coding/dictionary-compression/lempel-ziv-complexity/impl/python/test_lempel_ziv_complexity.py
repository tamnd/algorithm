# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lempel-ziv-complexity/. The authors are listed in prov/EXZCS6.jsonl.

import math
import random

from lempel_ziv_complexity import (
    components,
    kaspar_schuster,
    lz76_complexity,
    min_history,
    normalized,
    upper_bound,
)


def _all_three(t) -> int:
    a, b, c = lz76_complexity(t), kaspar_schuster(t), min_history(t)
    assert a == b == c, (t, a, b, c)
    return a


def test_page_examples() -> None:
    assert components("0001101001000101") == ["0", "001", "10", "100", "1000", "101"]
    assert components("010011101101100") == ["0", "1", "00", "11", "101", "101100"]
    assert components("0101010101") == ["0", "1", "01010101"]
    assert components("abcabcabd") == ["a", "b", "c", "abcabd"]
    for t in ("0001101001000101", "010011101101100", "abcabcabd"):
        assert _all_three(t) == len(components(t))


def test_edges() -> None:
    assert components("") == [] and _all_three("") == 0
    assert _all_three("0") == 1
    assert _all_three("01") == 2
    for n in range(2, 60):
        assert components("0" * n) == ["0", "0" * (n - 1)]
        assert _all_three("0" * n) == 2
    # A text with n distinct symbols has n components.
    assert _all_three("abcdefgh") == 8
    assert lz76_complexity(bytes(range(100))) == 100
    assert kaspar_schuster(list(range(100))) == 100


def test_components_join_and_each_is_new() -> None:
    rng = random.Random(1976)
    for _ in range(400):
        t = "".join(rng.choice("01") for _ in range(rng.randrange(1, 60)))
        parts = components(t)
        assert "".join(parts) == t
        start = 0
        for k, p in enumerate(parts):
            end = start + len(p)
            # All but the last symbol occurs earlier (overlap allowed).
            assert t.find(p[:-1], 0, end - 1) >= 0
            # The whole component is new, unless it is the last one.
            if k < len(parts) - 1:
                assert t.find(p, 0, end - 1) < 0
            start = end


def test_random_three_ways_agree() -> None:
    rng = random.Random(1987)
    for _ in range(1200):
        alphabet = rng.choice(["01", "abc", "acgt"])
        _all_three("".join(rng.choice(alphabet) for _ in range(rng.randrange(35))))


def test_repetitive() -> None:
    rng = random.Random(42)
    for _ in range(200):
        unit = "".join(rng.choice("01") for _ in range(rng.randrange(1, 6)))
        t = (unit * 30)[: rng.randrange(1, 80)]
        c = _all_three(t)
        # With period p, everything from position p on is a copy of the text
        # p symbols back, so at most one component starts at or after p.
        assert c <= lz76_complexity(t[:len(unit)]) + 1


def _lz_factors(t) -> list:
    """Greedy factors with no extra symbol: the longest earlier copy, or one new symbol."""
    out, i = [], 0
    while i < len(t):
        length = 0
        while i + length < len(t) and t.find(t[i:i + length + 1], 0, i + length) >= 0:
            length += 1
        length = max(1, length)
        out.append(t[i:i + length])
        i += length
    return out


def _lz78(t) -> list:
    seen, out, i = {""}, [], 0
    while i < len(t):
        j = i + 1
        while j <= len(t) and t[i:j] in seen:
            j += 1
        seen.add(t[i:j])
        out.append(t[i:j])
        i = j
    return out


def test_non_examples_and_related_counts() -> None:
    t = "0001101001000101"
    assert _lz78(t) == ["0", "00", "1", "10", "100", "1000", "101"]
    assert _lz_factors(t) == ["0", "00", "1", "1", "01", "001", "0001", "01"]
    rng = random.Random(78)
    for _ in range(400):
        t = "".join(rng.choice("01") for _ in range(rng.randrange(1, 70)))
        c, z = lz76_complexity(t), len(_lz_factors(t))
        assert c <= z <= 2 * c
        assert c <= len(_lz78(t))


def test_kaspar_schuster_long() -> None:
    rng = random.Random(7)
    for p in (0.5, 0.2):
        t = "".join("1" if rng.random() < p else "0" for _ in range(2000))
        assert kaspar_schuster(t) == lz76_complexity(t)


def test_normalized_and_bound() -> None:
    assert normalized("") == 0.0 and normalized("1") == 1.0
    # Bernoulli sources, n = 16000, fixed seeds. The normalized complexity
    # approaches the entropy rate only slowly; at this n it lies within 0.05
    # of it, and above it for p = 1/2.
    for p, seed in ((0.5, 16000), (0.1, 16000)):
        rng = random.Random(seed)
        n = 16000
        t = "".join("1" if rng.random() < p else "0" for _ in range(n))
        h = -(p * math.log2(p) + (1 - p) * math.log2(1 - p))
        value = normalized(t)
        assert abs(value - h) < 0.05
        assert lz76_complexity(t) < upper_bound(n)
    rng = random.Random(3)
    for n in (64, 256, 1000, 4000):
        t = "".join(rng.choice("01") for _ in range(n))
        assert lz76_complexity(t) < upper_bound(n)
