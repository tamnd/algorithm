# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interpolative-coding/. The authors are listed in prov/TZXH8F.jsonl.

import math
import random

import pytest

from interpolative_coding import (
    BitReader,
    BitWriter,
    bic_encode,
    decode,
    encode,
    minimal_length,
    plain_width,
    read_minimal,
    trace,
    write_minimal,
)

# Pibiri and Venturini, Techniques for inverted index compression (arXiv:1908.10598v2),
# Section 3.5 and Fig. 4, copied by hand. S = [3, 4, 7, 13, 14, 15, 21, 25, 36, 38, 54, 62],
# l = 0, h = 62 = S[n]; the first n - 1 elements are coded. Pre-order written values
# and their plain binary codeword lengths:
PV_S = [3, 4, 7, 13, 14, 15, 21, 25, 36, 38, 54]
PV_VALUES = [10, 5, 3, 0, 5, 18, 5, 3, 1, 15]
PV_LENGTHS = [6, 4, 3, 2, 3, 6, 5, 4, 5, 5]


def recursive_oracle(s: list[int], lo: int, hi: int, out: list[tuple[int, int]]) -> None:
    """The recursive form, as in the survey, 1-indexed middle m = ceil(n/2):
    write S[m] - l - m + 1 with range h - l - n + 1."""
    n = len(s)
    if n == 0 or hi - lo + 1 == n:
        return
    m = (n + 1) // 2
    out.append((s[m - 1] - lo - m + 1, hi - lo - n + 1))
    recursive_oracle(s[: m - 1], lo, s[m - 1] - 1, out)
    recursive_oracle(s[m:], s[m - 1] + 1, hi, out)


def test_survey_figure_4() -> None:
    t = trace(PV_S, 0, 62)
    assert [row[3] for row in t] == PV_VALUES
    assert [plain_width(row[4]) for row in t] == PV_LENGTHS
    # The element 14 has l = h = 14 and costs 0 bits: it writes nothing.
    assert 14 not in [row[2] for row in t]
    for code in ("plain", "minimal"):
        data, nbits = encode(PV_S, 0, 62, code)
        assert decode(len(PV_S), 0, 62, data, nbits, code) == PV_S
    assert encode(PV_S, 0, 62, "plain")[1] == sum(PV_LENGTHS) == 43
    assert encode(PV_S, 0, 62, "minimal")[1] == 38


def test_minimal_binary() -> None:
    for r in range(0, 300):
        words = []
        for v in range(r + 1):
            w = BitWriter()
            write_minimal(w, v, r)
            data, nbits = w.getvalue()
            assert nbits == minimal_length(v, r)
            assert read_minimal(BitReader(data, nbits), r) == v
            words.append("".join(str((data[i >> 3] >> (7 - (i & 7))) & 1) for i in range(nbits)))
        if r == 0:
            continue
        # Prefix-free and complete: the Kraft sum is exactly 1.
        assert all(not b.startswith(a) for a in words for b in words if a != b)
        assert math.fsum(2.0 ** -len(x) for x in words) == 1.0
        k = math.ceil(math.log2(r + 1))
        assert {len(x) for x in words} <= {k - 1, k}
        # The short codewords sit in the middle of the range.
        short = [v for v in range(r + 1) if len(words[v]) == k - 1]
        if short:
            assert short == list(range(short[0], short[-1] + 1))
            assert abs((short[0] + short[-1]) - r) <= 1


def test_dense_run_costs_zero_bits() -> None:
    assert encode(list(range(100, 1100)), 100, 1099)[1] == 0
    assert encode(list(range(0, 50)), 0, 49, "plain")[1] == 0
    # A run inside a longer list: only the nodes on the two edges of the run
    # write a value; every subtree pinned on both sides by run elements is free.
    s = [5] + list(range(1000, 1200)) + [5000]
    t = trace(s, 0, 6000)
    assert len(t) == 15
    assert decode(len(s), 0, 6000, *encode(s, 0, 6000)) == s


def test_random_against_recursive_oracle() -> None:
    rng = random.Random(97)
    for _ in range(500):
        u = rng.randrange(1, 3000)
        n = rng.randrange(0, min(u, 200) + 1)
        if rng.random() < 0.3:
            start = rng.randrange(0, u - n + 1)
            s = sorted(set(range(start, start + n)) | set(rng.sample(range(u), rng.randrange(0, 5))))
        else:
            s = sorted(rng.sample(range(u), n))
        lo = rng.randrange(0, (s[0] if s else 0) + 1)
        hi = (s[-1] if s else lo) + rng.randrange(0, 50)
        ref: list[tuple[int, int]] = []
        recursive_oracle(s, lo, hi, ref)
        assert [(row[3], row[4]) for row in trace(s, lo, hi)] == ref
        for code in ("plain", "minimal"):
            data, nbits = encode(s, lo, hi, code)
            assert decode(len(s), lo, hi, data, nbits, code) == s
        assert encode(s, lo, hi, "plain")[1] == sum(plain_width(r) for _, r in ref)
        assert encode(s, lo, hi, "minimal")[1] == sum(minimal_length(v, r) for v, r in ref)


def test_stack_depth_is_logarithmic() -> None:
    for n in (1, 2, 3, 7, 8, 100, 1000, 5000):
        s = list(range(0, 3 * n, 3))
        depth = bic_encode(s, 0, 3 * n, BitWriter())
        assert depth <= math.floor(math.log2(n)) + 2


def test_edge_cases() -> None:
    assert encode([], 0, 10) == (b"", 0)
    assert decode(0, 0, 10, b"", 0) == []
    assert decode(1, 7, 7, b"", 0) == [7]
    assert decode(1, 0, 1000, *encode([999], 0, 1000)) == [999]
    with pytest.raises(ValueError):
        encode([3, 3], 0, 10)
    with pytest.raises(ValueError):
        encode([3, 11], 0, 10)
    data, nbits = encode([1, 500, 900], 0, 1000)
    with pytest.raises(EOFError):
        decode(3, 0, 1000, data, nbits - 1)
