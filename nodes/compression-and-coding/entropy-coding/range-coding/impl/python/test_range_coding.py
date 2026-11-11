# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/range-coding/. The authors are listed in prov/3GVCEG.jsonl.

import lzma
import math
import random

from range_coding import (
    PROB_INIT, RangeDecoder, RangeEncoder, decode_bits, decode_bytes, decode_lzma_literals,
    encode_bits, encode_bytes, model_cost_bytes,
)


def test_example() -> None:
    # The worked example of the page: the bits 0 0 1 0 with one adaptive probability.
    code = encode_bits([0, 0, 1, 0], 1, [0, 0, 0, 0])
    assert code[0] == 0  # the LZMA encoder always writes a zero byte first
    assert code.hex() == "002307bbc1"
    assert decode_bits(code, 1, [0, 0, 0, 0]) == [0, 0, 1, 0]


def test_probability_update() -> None:
    probs = [PROB_INIT]
    enc = RangeEncoder()
    enc.encode_bit(probs, 0, 0)
    assert probs[0] == 1024 + (1024 >> 5) == 1056
    enc.encode_bit(probs, 0, 1)
    assert probs[0] == 1056 - (1056 >> 5) == 1023
    # The probability stays in [31, 2017]: 2048 - 2017 = 31 and 31 >> 5 == 0.
    p = [PROB_INIT]
    for _ in range(500):
        enc.encode_bit(p, 0, 0)
    assert p[0] == 2017
    for _ in range(500):
        enc.encode_bit(p, 0, 1)
    assert p[0] == 31


def test_edges() -> None:
    for bits in ([], [0], [1], [0] * 5000, [1] * 5000, [0, 1] * 2000):
        ctx = [0] * len(bits)
        code = encode_bits(bits, 1, ctx)
        assert decode_bits(code, 1, ctx) == bits
        dec = RangeDecoder(code)
        p = [PROB_INIT]
        for _ in bits:
            dec.decode_bit(p, 0)
        assert dec.finished_ok()


def test_random_bits_with_contexts() -> None:
    rng = random.Random(1979)
    for _ in range(300):
        n = rng.randint(0, 400)
        k = rng.randint(1, 8)
        p1 = [rng.random() for _ in range(k)]
        ctx = [rng.randrange(k) for _ in range(n)]
        bits = [1 if rng.random() < p1[c] else 0 for c in ctx]
        code = encode_bits(bits, k, ctx)
        assert decode_bits(code, k, ctx) == bits


def test_carry_propagation() -> None:
    # Long runs of 1 bits with a probability that favours 0 push low up and
    # make carries through cached 0xFF bytes.
    rng = random.Random(5)
    for _ in range(50):
        bits = [1 if rng.random() < 0.97 else 0 for _ in range(3000)]
        code = encode_bits(bits, 1, [0] * len(bits))
        assert decode_bits(code, 1, [0] * len(bits)) == bits


def test_direct_bits() -> None:
    rng = random.Random(11)
    values = [(rng.getrandbits(w), w) for w in [rng.randint(1, 26) for _ in range(200)]]
    enc = RangeEncoder()
    probs = [PROB_INIT]
    for v, w in values:
        enc.encode_direct_bits(v, w)
        enc.encode_bit(probs, 0, v & 1)
    code = enc.finish()
    dec = RangeDecoder(code)
    probs = [PROB_INIT]
    for v, w in values:
        assert dec.decode_direct_bits(w) == v
        assert dec.decode_bit(probs, 0) == v & 1


def test_bytes_roundtrip_and_size() -> None:
    rng = random.Random(42)
    for data in (b"", b"x", b"abracadabra" * 50, bytes(rng.randrange(256) for _ in range(3000)),
                 bytes(rng.choices(b"ab", weights=[9, 1], k=4000))):
        code = encode_bytes(data)
        assert decode_bytes(code, len(data)) == data
    # The length theorem of the proof: the output is at most the model cost (the
    # sum of -lg p over the 8 n decisions) plus 40 bits plus lg(1/(1 - 2^-13))
    # bits per decision for the truncation of range / 2^11.
    loss = -math.log2(1 - 2 ** -13)
    for data in (bytes(rng.choices(b"ab", weights=[9, 1], k=4000)), bytes(rng.randrange(256) for _ in range(2000)),
                 b"z" * 3000):
        cost = model_cost_bytes(data)
        size = len(encode_bytes(data)) * 8
        assert cost - 1 <= size <= cost + 40 + 8 * len(data) * loss
    # The shift-5 estimator pays for its short memory: on the skewed source it
    # is above n h(0.1), but well below 8 bits per byte.
    data = bytes(rng.choices(b"ab", weights=[9, 1], k=4000))
    h = -(0.9 * math.log2(0.9) + 0.1 * math.log2(0.1))
    assert 4000 * h < len(encode_bytes(data)) * 8 < 4000


def test_decodes_a_raw_lzma1_stream_from_liblzma() -> None:
    # A permutation of the 256 byte values has no repeated byte, so no match and
    # no short rep is possible, and the LZMA encoder must emit 256 literals. The
    # stream comes from the xz library through Python's lzma module.
    rng = random.Random(2024)
    for _ in range(3):
        perm = list(range(256))
        rng.shuffle(perm)
        data = bytes(perm)
        raw = lzma.compress(data, format=lzma.FORMAT_RAW, filters=[{"id": lzma.FILTER_LZMA1, "preset": 6}])
        assert raw[0] == 0
        assert decode_lzma_literals(raw, len(data)) == data
    # Distinct letters in a short text: also all literals.
    text = b"the quick brown fox"
    data = bytes(dict.fromkeys(text))
    raw = lzma.compress(data, format=lzma.FORMAT_RAW, filters=[{"id": lzma.FILTER_LZMA1, "preset": 6}])
    assert decode_lzma_literals(raw, len(data)) == data
