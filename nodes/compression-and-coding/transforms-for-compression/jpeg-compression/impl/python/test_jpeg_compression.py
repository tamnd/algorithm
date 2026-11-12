# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jpeg-compression/. The authors are listed in prov/2JBQT3.jsonl.

"""Tests for the baseline greyscale JPEG coder.

There is no JPEG codec in the Python standard library, so no independent
decoder checks the files. The tests check the Huffman codes generated from
BITS and HUFFVAL against codewords copied by hand from Annex K, the marker
layout, byte stuffing, the error bound proved on the page, and a worked
block whose bits were checked by hand.
"""

import math
import random

from jpeg_compression import (
    AC_LUMINANCE_BITS,
    AC_LUMINANCE_VALUES,
    DC_LUMINANCE_BITS,
    DC_LUMINANCE_VALUES,
    K1_LUMINANCE,
    ZIGZAG,
    BitReader,
    BitWriter,
    category,
    decode,
    encode,
    encoder_table,
    extend,
    extra_bits,
    fdct,
    idct,
    quantize,
    scaled_table,
)

# Table K.3 (T.81, K.3.1, page 149): DC luminance codes by category, copied by hand.
TABLE_K3 = ["00", "010", "011", "100", "101", "110", "1110", "11110", "111110", "1111110", "11111110", "111111110"]

# Table K.5, sheet 1 (T.81, K.3.2, page 150): some AC luminance codes, copied by hand.
TABLE_K5 = {
    0x00: "1010", 0x01: "00", 0x02: "01", 0x03: "100", 0x04: "1011", 0x05: "11010",
    0x06: "1111000", 0x07: "11111000", 0x08: "1111110110", 0x11: "1100", 0x12: "11011",
    0x13: "1111001", 0x21: "11100", 0x31: "111010",
}


def bitstring(code: int, length: int) -> str:
    return format(code, "0%db" % length)


def psnr(a, b) -> float:
    n = len(a) * len(a[0])
    m = sum((x - y) ** 2 for ra, rb in zip(a, b) for x, y in zip(ra, rb)) / n
    return math.inf if m == 0 else 10 * math.log10(255 * 255 / m)


def psnr_bound(table) -> float:
    """PSNR lower bound from the page: block MSE <= ((sqrt(sum Q^2) / 2 + 4)^2) / 64."""
    mse = (0.5 * math.sqrt(sum(q * q for q in table)) + 4) ** 2 / 64
    return 10 * math.log10(255 * 255 / mse)


def images():
    rng = random.Random(1)
    return {
        "gradient": [[(8 * r + 4 * c) % 256 for c in range(32)] for r in range(32)],
        "smooth": [[int(128 + 100 * math.sin(r / 5) * math.cos(c / 7)) for c in range(32)] for r in range(32)],
        "checkerboard": [[255 if (r // 4 + c // 4) % 2 else 0 for c in range(16)] for r in range(16)],
        "random": [[rng.randrange(256) for _ in range(16)] for _ in range(16)],
        "odd size": [[min(255, 10 * r + 3 * c + rng.randrange(20)) for c in range(21)] for r in range(13)],
        "one pixel": [[77]],
    }


def test_annex_c_codes_match_annex_k() -> None:
    dc = encoder_table(DC_LUMINANCE_BITS, DC_LUMINANCE_VALUES)
    assert [bitstring(*dc[s]) for s in range(12)] == TABLE_K3
    ac = encoder_table(AC_LUMINANCE_BITS, AC_LUMINANCE_VALUES)
    assert len(ac) == 162 == sum(AC_LUMINANCE_BITS)
    for symbol, code in TABLE_K5.items():
        assert bitstring(*ac[symbol]) == code
    # A prefix code that is complete except for the all-ones word of each length.
    assert sum(2.0 ** -s for _, s in ac.values()) == 1 - 2.0 ** -16
    words = sorted(bitstring(*c) for c in ac.values())
    assert not any(b.startswith(a) for a, b in zip(words, words[1:]))


def test_categories_and_extra_bits() -> None:
    assert [category(v) for v in (0, 1, -1, 2, -3, 4, 1023, -2047)] == [0, 1, 1, 2, 2, 3, 10, 11]
    assert bitstring(extra_bits(-3, 2), 2) == "00" and bitstring(extra_bits(3, 2), 2) == "11"
    assert bitstring(extra_bits(-17, 5), 5) == "01110"
    for v in range(-2047, 2048):
        s = category(v)
        assert extend(extra_bits(v, s), s) == v


def test_dct_is_orthonormal() -> None:
    rng = random.Random(4)
    block = [rng.uniform(-128, 127) for _ in range(64)]
    coef = fdct(block)
    assert max(abs(a - b) for a, b in zip(idct(coef), block)) < 1e-9
    assert abs(sum(c * c for c in coef) - sum(s * s for s in block)) < 1e-6
    assert abs(fdct([10.0] * 64)[0] - 80) < 1e-12


def test_byte_stuffing_and_padding() -> None:
    w = BitWriter()
    w.write(0xFF, 8)
    w.write(0b101, 3)
    data = w.flush()
    assert data == bytes([0xFF, 0x00, 0b10111111])
    r = BitReader(data, 0)
    assert r.bits(8) == 0xFF and r.bits(3) == 0b101


def test_worked_block() -> None:
    img = [[100 + 6 * x + 3 * y + (20 if x >= 4 else 0) for x in range(8)] for y in range(8)]
    coef = fdct([s - 128 for row in img for s in row])
    sq = [quantize(coef[i], K1_LUMINANCE[i]) for i in range(64)]
    assert sq[:8] == [7, -17, 0, 1, 0, -1, 0, 0] and sq[8] == -5 and not any(sq[9:])
    zz = [sq[z] for z in ZIGZAG]
    assert [(k, v) for k, v in enumerate(zz) if v] == [(0, 7), (1, -17), (2, -5), (6, 1), (15, -1)]
    data = encode(img)
    # DC 100 111, then 11010 01110, 100 010, 111010 1, 111111000 0, EOB 1010, and five 1-bits.
    assert data[-8:] == bytes.fromhex("9f4e8bafe15fffd9")
    out = decode(data)
    assert out[0] == [98, 110, 109, 118, 145, 154, 153, 166]
    assert max(abs(a - b) for ra, rb in zip(img, out) for a, b in zip(ra, rb)) == 6
    assert sum((a - b) ** 2 for ra, rb in zip(img, out) for a, b in zip(ra, rb)) == 680  # MSE 10.625


def test_marker_layout() -> None:
    data = encode(images()["gradient"])
    pos, markers = 2, [data[1]]
    while markers[-1] != 0xDA:
        markers.append(data[pos + 1])
        pos += 2 + int.from_bytes(data[pos + 2:pos + 4], "big")
    assert markers == [0xD8, 0xE0, 0xDB, 0xC0, 0xC4, 0xC4, 0xDA]  # SOI APP0 DQT SOF0 DHT DHT SOS
    entropy = data[pos:-2]
    assert data[-2:] == b"\xff\xd9"  # EOI
    assert b"\xff\x00" in entropy  # this image needs stuffing
    assert all(entropy[i + 1] == 0 for i in range(len(entropy) - 1) if entropy[i] == 0xFF)
    assert entropy[-1] != 0xFF
    # The DQT payload is the table in zigzag order.
    dqt = data.index(b"\xff\xdb")
    assert list(data[dqt + 5:dqt + 69]) == [K1_LUMINANCE[z] for z in ZIGZAG]


def test_round_trip_meets_error_bound() -> None:
    for quality in (None, 25, 90, 100):
        table = K1_LUMINANCE if quality is None else scaled_table(quality)
        bound = psnr_bound(table)
        per_sample = 0.5 * math.sqrt(sum(q * q for q in table)) + 0.5
        for name, img in images().items():
            out = decode(encode(img, table))
            assert len(out) == len(img) and len(out[0]) == len(img[0]), name
            if len(img) % 8 == 0 and len(img[0]) % 8 == 0:
                assert psnr(img, out) >= bound, (quality, name)
            assert max(abs(a - b) for ra, rb in zip(img, out) for a, b in zip(ra, rb)) <= per_sample
    assert abs(psnr_bound(scaled_table(100)) - 48.1308) < 1e-4  # all steps 1
    assert scaled_table(50) == K1_LUMINANCE


def test_quality_100_extremes_and_constant() -> None:
    # The block that gives the largest AC coefficient, 1020 at (0, 4), needs size 10.
    img = [[255 if math.cos((2 * x + 1) * 4 * math.pi / 16) > 0 else 0 for x in range(8)] for _ in range(8)]
    coef = fdct([s - 128 for row in img for s in row])
    assert abs(coef[4] - 1020) < 1e-9
    assert decode(encode(img, scaled_table(100))) == img
    flat = [[100] * 24 for _ in range(16)]
    assert decode(encode(flat)) == flat


def test_coefficient_error_at_most_half_step() -> None:
    rng = random.Random(9)
    for _ in range(50):
        block = [rng.randrange(256) - 128 for _ in range(64)]
        coef = fdct(block)
        for f, q in zip(coef, K1_LUMINANCE):
            assert abs(quantize(f, q) * q - f) <= q / 2 + 1e-9


def test_decoder_skips_comment_and_app_segments() -> None:
    img = images()["smooth"]
    data = encode(img)
    com = b"\xff\xfe" + (2 + 5).to_bytes(2, "big") + b"hello"
    app1 = b"\xff\xe1" + (2 + 3).to_bytes(2, "big") + b"abc"
    assert decode(data[:2] + com + app1 + data[2:]) == decode(data)
