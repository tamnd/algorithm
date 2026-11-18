# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adaptive-scalable-texture-compression/. The authors are listed in prov/XB2HVD.jsonl.

"""Tests of the ASTC subset: the BISE layout and round trip, the
unquantization tables, the block modes, and the decoding of one-partition
LDR blocks with the color endpoint modes 8 and 12."""

import random
from fractions import Fraction
from math import ceil, log2

from adaptive_scalable_texture_compression import (
    COLOR_RANGES,
    DECODE_TABLE,
    ERROR_COLOR,
    FOOTPRINTS,
    MODE_OF,
    WEIGHT_RANGES,
    bits_per_texel,
    decode_block,
    decode_block_mode,
    endpoints,
    infill,
    interpolate,
    ise_bits,
    ise_decode,
    ise_encode,
    ise_params,
    ise_rate,
    pack_block,
    unquant_color,
    unquant_weight,
)

ALL_RANGES = sorted(set(COLOR_RANGES) | set(WEIGHT_RANGES.values()))


def test_rates_and_layout():
    assert bits_per_texel(4, 4) == 8 and bits_per_texel(12, 12) == Fraction(8, 9)
    assert bits_per_texel(6, 6) == Fraction(32, 9)
    assert ise_rate(11) == 2 + Fraction(8, 5) and ise_rate(9) == 1 + Fraction(7, 3)
    for mx in ALL_RANGES:
        kind, n = ise_params(mx)
        # The rate is at most 1% above the information content log2(mx + 1).
        assert log2(mx + 1) <= ise_rate(mx) <= 1.01 * log2(mx + 1) + 1e-12
        for count in range(1, 70):
            extra = {"bits": 0, "trit": ceil(8 * count / 5), "quint": ceil(7 * count / 3)}[kind]
            assert ise_bits(count, mx) == count * n + extra


def test_packed_fields_cover_every_tuple():
    trits, quints = DECODE_TABLE["trit"], DECODE_TABLE["quint"]
    assert len(trits) == 256 and len(set(trits)) == 3 ** 5
    assert len(quints) == 128 and len(set(quints)) == 5 ** 3


def test_trit_group_bit_positions():
    # Five values in 0..47 (n = 4): m0 T[1:0] m1 T[3:2] m2 T[4] m3 T[6:5] m4 T[7].
    rng = random.Random(1)
    for _ in range(200):
        vals = [rng.randrange(48) for _ in range(5)]
        stream, length = ise_encode(vals, 47)
        assert length == 28
        for j, start in enumerate((0, 6, 12, 17, 23)):
            assert (stream >> start) & 15 == vals[j] & 15
        t = ((stream >> 4) & 3) | ((stream >> 10) & 3) << 2 | ((stream >> 16) & 1) << 4 \
            | ((stream >> 21) & 3) << 5 | ((stream >> 27) & 1) << 7
        assert DECODE_TABLE["trit"][t] == tuple(v >> 4 for v in vals)


def test_round_trip_all_ranges_and_partial_groups():
    rng = random.Random(2)
    for mx in ALL_RANGES:
        for count in range(1, 40):
            vals = [rng.randrange(mx + 1) for _ in range(count)]
            stream, length = ise_encode(vals, mx)
            assert stream < 1 << length
            assert ise_decode(stream, count, mx) == vals
            # Bits past the end are read as zero, whatever the block holds there.
            noise = rng.getrandbits(64) << length
            assert ise_decode(stream | noise, count, mx) == vals


def test_round_trip_every_short_trit_and_quint_group():
    for mx, size in ((2, 5), (5, 5), (4, 3), (9, 3)):
        kind, n = ise_params(mx)
        for count in range(1, size + 1):
            for high in range(3 ** count if kind == "trit" else 5 ** count):
                digits, h = [], high
                for _ in range(count):
                    digits.append(h % (3 if kind == "trit" else 5))
                    h //= 3 if kind == "trit" else 5
                vals = [d << n | (j & ((1 << n) - 1)) for j, d in enumerate(digits)]
                stream, length = ise_encode(vals, mx)
                assert ise_decode(stream, count, mx) == vals


def test_unquantization_tables():
    for mx in COLOR_RANGES:
        u = [unquant_color(v, mx) for v in range(mx + 1)]
        assert len(set(u)) == mx + 1 and min(u) == 0 and max(u) == 255
        kind, n = ise_params(mx)
        if kind != "bits":  # flipping the lowest bit mirrors the value
            assert all(unquant_color(v ^ 1, mx) == 255 - unquant_color(v, mx) for v in range(mx + 1))
    for mx in sorted(set(WEIGHT_RANGES.values())):
        u = sorted(unquant_weight(v, mx) for v in range(mx + 1))
        assert len(set(u)) == mx + 1 and u[0] == 0 and u[-1] == 64
        # The levels are close to even: every gap is within 3 of 64 / mx.
        assert all(abs((b - a) - 64 / mx) < 3 for a, b in zip(u, u[1:]))
    # The quantized order is not the order of the values.
    assert [unquant_weight(v, 11) for v in range(4)] == [0, 64, 17, 47]


def test_block_modes():
    infos = [decode_block_mode(m) for m in range(2048)]
    assert sum(1 for x in infos if x == "void") == 4
    for info in infos:
        if isinstance(info, tuple):
            w, h, wmax, dual = info
            assert 2 <= w <= 12 and 2 <= h <= 12 and wmax in WEIGHT_RANGES.values()
    for (w, h, wmax), mode in MODE_OF.items():
        assert decode_block_mode(mode) == (w, h, wmax, 0)
    assert (4, 4, 11) in MODE_OF and (8, 8, 1) in MODE_OF and (6, 10, 3) in MODE_OF
    assert max(w * h for w, h, _ in MODE_OF) == 81  # 9 x 9, more than the 64 weights allowed


def test_infill_identity_and_constants():
    rng = random.Random(3)
    for bw, bh in FOOTPRINTS:
        w = [rng.randrange(65) for _ in range(bw * bh)]
        assert all(infill(w, bw, bh, bw, bh, s, t) == w[t * bw + s] for t in range(bh) for s in range(bw))
        for n in range(2, bw + 1):
            for m in range(2, bh + 1):
                c = rng.randrange(65)
                assert all(infill([c] * (n * m), n, m, bw, bh, s, t) == c
                           for t in range(bh) for s in range(bw))
                g = [rng.randrange(65) for _ in range(n * m)]
                assert infill(g, n, m, bw, bh, 0, 0) == g[0]
                assert infill(g, n, m, bw, bh, bw - 1, bh - 1) == g[-1]


def test_interpolation_ends():
    for e0 in range(0, 256, 15):
        for e1 in range(0, 256, 17):
            assert interpolate(e0, e1, 0) == 257 * e0 and interpolate(e0, e1, 64) == 257 * e1
            row = [interpolate(e0, e1, i) for i in range(65)]
            assert row == sorted(row) or row == sorted(row, reverse=True)


def test_decode_matches_the_fields():
    rng = random.Random(4)
    cases = [((4, 4), (4, 4)), ((6, 6), (3, 5)), ((8, 8), (5, 4)), ((12, 12), (6, 6)), ((10, 5), (10, 5))]
    for (bw, bh), (n, m) in cases:
        for wmax in sorted(set(WEIGHT_RANGES.values())):
            if (n, m, wmax) not in MODE_OF or not 24 <= ise_bits(n * m, wmax) <= 96:
                continue
            for cem in (8, 12):
                try:
                    probe = pack_block(n, m, wmax, cem, [0] * (2 * (cem // 4 + 1)), [0] * (n * m))
                except ValueError:
                    continue
                cmax = probe[1]
                colors = [rng.randrange(cmax + 1) for _ in range(2 * (cem // 4 + 1))]
                weights = [rng.randrange(wmax + 1) for _ in range(n * m)]
                block, _ = pack_block(n, m, wmax, cem, colors, weights)
                e0, e1 = endpoints(cem, [unquant_color(c, cmax) for c in colors])
                w = [unquant_weight(x, wmax) for x in weights]
                out = decode_block(block, bw, bh)
                for t in range(bh):
                    for s in range(bw):
                        i = infill(w, n, m, bw, bh, s, t)
                        want = tuple((257 * a * (64 - i) + 257 * b * i + 32) // 64 for a, b in zip(e0, e1))
                        assert out[t * bw + s] == want


def test_blue_contraction_and_constant_blocks():
    assert endpoints(8, [40, 200, 100, 220, 50, 60]) == ((40, 100, 50, 255), (200, 220, 60, 255))
    assert endpoints(8, [200, 40, 220, 100, 60, 50]) == ((45, 75, 50, 255), (130, 140, 60, 255))
    assert endpoints(12, [200, 40, 220, 100, 60, 50, 7, 9]) == ((45, 75, 50, 9), (130, 140, 60, 7))
    block, cmax = pack_block(4, 4, 11, 8, [40, 200, 100, 220, 50, 60], [0] * 16)
    assert cmax == 255
    assert decode_block(block, 4, 4) == [(40 * 257, 100 * 257, 50 * 257, 65535)] * 16
    block, _ = pack_block(4, 4, 11, 8, [40, 200, 100, 220, 50, 60], [1] * 16)  # 1 means 64
    assert decode_block(block, 4, 4) == [(200 * 257, 220 * 257, 60 * 257, 65535)] * 16


def test_error_blocks_and_random_access():
    block, _ = pack_block(8, 8, 1, 8, [10, 20, 30, 40, 50, 60], [0, 1] * 32)
    assert decode_block(block, 8, 8)[0] != ERROR_COLOR
    assert decode_block(block, 6, 6) == [ERROR_COLOR] * 36  # the grid is larger than the block
    bits = int.from_bytes(block, "little") & ~0x7FF  # mode 0 is reserved
    assert decode_block(bits.to_bytes(16, "little"), 8, 8) == [ERROR_COLOR] * 64
    # A block decodes alone: the same 16 bytes give the same texels.
    assert decode_block(bytes(block), 8, 8) == decode_block(block, 8, 8)
