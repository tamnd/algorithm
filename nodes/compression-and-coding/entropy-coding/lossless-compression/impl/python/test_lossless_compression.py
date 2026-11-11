# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lossless-compression/. The authors are listed in prov/DRHZ6Y.jsonl.

import math
import random

import pytest

from lossless_compression import (COMPRESSORS, GENERATORS, entropy0, order0_compress, order0_decompress, run)

N = 10000
SEED = 1948


@pytest.fixture(scope="module")
def results() -> dict[str, tuple[bytes, float, dict[str, int]]]:
    out = {}
    for kind, gen in GENERATORS.items():
        data, info = gen(N, SEED)
        out[kind] = (data, info, run(data))  # run() checks every round trip
    return out


def test_roundtrip_edges() -> None:
    rng = random.Random(5)
    cases = [b"", b"x", bytes(range(256)), b"\x00" * 70000, bytes(rng.randrange(256) for _ in range(3000))]
    for data in cases:
        assert run(data)  # raises on a failed round trip
        assert order0_decompress(order0_compress(data)) == data


def test_random_data_does_not_shrink(results) -> None:
    data, _, sizes = results["random"]
    for name, size in sizes.items():
        assert size >= len(data), name


def test_no_compressor_beats_the_source_by_much(results) -> None:
    # For any injective code, Pr[length < information - c bits] <= (max length in bytes + 1) 2^-c.
    for kind, (_, info, sizes) in results.items():
        for name, size in sizes.items():
            assert 8 * size >= info - 64, (kind, name)


def test_order0_is_near_the_order0_entropy(results) -> None:
    for kind, (data, _, sizes) in results.items():
        n = len(data)
        # Laplace mixture: n H0 + lg C(n + 255, 255), plus the coder overhead and the 4-byte header.
        model_cost = math.log2(math.comb(n + 255, 255))
        assert 8 * sizes["order0"] <= entropy0(data) + model_cost + 2 + 8 + 32 + n * 1e-4 + 1, kind


def test_results_order_as_theory_predicts(results) -> None:
    _, _, skew = results["skewed"]
    # Memoryless data: an order-0 model is the right model, and it beats the dictionary and BWT coders.
    assert skew["order0"] < min(skew["zlib"], skew["bz2"], skew["lzma"])
    data, info, markov = results["markov"]
    # Markov text: coders that use context beat order 0, which cannot go below n H0.
    assert max(markov["bz2"], markov["lzma"], markov["zlib"]) < markov["order0"]
    assert 8 * markov["order0"] >= entropy0(data) - 8 * 255 * math.log2(len(data))
    assert info < entropy0(data)
    _, _, runs = results["runs"]
    # Long runs: dictionary and BWT coders win by a factor of ten or more.
    assert 10 * max(runs["zlib"], runs["bz2"], runs["lzma"]) < runs["order0"]


def test_entropy0() -> None:
    assert entropy0(b"") == 0
    assert entropy0(b"aaaa") == 0
    assert entropy0(b"abab") == pytest.approx(4.0)
    assert entropy0(bytes(range(256))) == pytest.approx(256 * 8)
    assert set(COMPRESSORS) == {"zlib", "bz2", "lzma", "order0"}
