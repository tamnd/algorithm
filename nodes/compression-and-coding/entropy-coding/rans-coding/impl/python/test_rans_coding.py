# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rans-coding/. The authors are listed in prov/08A5D1.jsonl.

import math
import random

import pytest

from rans_coding import (
    L, M, counts_of, cumulative, decode, decode_get, empirical_entropy, encode, encode_put,
    length_bound, model_cost, normalize_frequencies, slot_table, _Reader,
)


def test_example() -> None:
    # The worked example of the page: "abac" with f(a) = 2048, f(b) = f(c) = 1024.
    data = b"abac"
    freq = normalize_frequencies(counts_of(data))
    assert (freq[ord("a")], freq[ord("b")], freq[ord("c")]) == (2048, 1024, 1024)
    code = encode(data, freq)
    assert code.hex() == "0000000200380008"
    assert decode(code, 4, freq) == data


def test_put_and_get_are_inverse() -> None:
    rng = random.Random(3)
    counts = [rng.randint(0, 50) for _ in range(256)]
    counts[0] = 1
    freq = normalize_frequencies(counts)
    cum = cumulative(freq)
    sym = slot_table(freq, cum)
    for _ in range(3000):
        s = rng.choice([t for t in range(256) if freq[t]])
        x = rng.randrange(L, 256 * L)
        out: list[int] = []
        y = encode_put(x, freq[s], cum[s], out)
        # The new state stays in [L, 256 L), so it fits in 32 bits.
        assert L <= y < 256 * L
        got, back = decode_get(y, freq, cum, sym, _Reader(bytes(reversed(out))))
        assert (got, back) == (s, x)


def test_normalize() -> None:
    rng = random.Random(8)
    for _ in range(200):
        counts = [rng.choice([0, 0, 1, rng.randint(1, 10 ** rng.randint(0, 6))]) for _ in range(256)]
        if not any(counts):
            counts[5] = 1
        freq = normalize_frequencies(counts)
        assert sum(freq) == M
        assert all((f >= 1) == (c >= 1) for f, c in zip(freq, counts))
    with pytest.raises(ValueError):
        normalize_frequencies([0] * 256)


def test_edges() -> None:
    for data in (b"a", b"ab", b"abc", b"z" * 1000, bytes(range(256))):
        freq = normalize_frequencies(counts_of(data))
        assert decode(encode(data, freq), len(data), freq) == data
    freq = normalize_frequencies(counts_of(b"ab"))
    assert decode(encode(b"", freq), 0, freq) == b""
    with pytest.raises(ValueError):
        encode(b"c", freq)
    with pytest.raises(ValueError):
        decode(encode(b"abba", freq)[:-1], 4, freq)


def test_random_roundtrip_and_bound() -> None:
    rng = random.Random(2014)
    for _ in range(200):
        k = rng.randint(1, 256)
        weights = [rng.random() ** 4 for _ in range(k)]
        n = rng.randint(1, 600)
        data = bytes(rng.choices(range(k), weights=weights, k=n))
        freq = normalize_frequencies(counts_of(data))
        code = encode(data, freq)
        assert decode(code, n, freq) == data
        assert 8 * len(code) <= length_bound(data, freq)


def test_size_near_empirical_entropy() -> None:
    rng = random.Random(1402)
    for weights in ([8, 4, 2, 1, 1], [30, 1], [1] * 256, [rng.random() for _ in range(40)]):
        data = bytes(rng.choices(range(len(weights)), weights=weights, k=20000))
        freq = normalize_frequencies(counts_of(data))
        size = 8 * len(encode(data, freq))
        h0 = len(data) * empirical_entropy(data)
        # The table quantization costs the relative entropy of the counts and
        # the frequencies; here it is below 0.01 bit per symbol.
        assert model_cost(data, freq) <= h0 + 0.01 * len(data)
        assert h0 - 1 <= size <= h0 + 0.012 * len(data) + 64
    # A source with entropy 0 still costs at least the two 32-bit states.
    data = b"q" * 5000
    assert 8 * len(encode(data, normalize_frequencies(counts_of(data)))) == 64
    assert math.isclose(empirical_entropy(data), 0.0, abs_tol=1e-12)
