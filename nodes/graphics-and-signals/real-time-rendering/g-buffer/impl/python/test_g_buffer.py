# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/g-buffer/. The authors are listed in prov/P04D18.jsonl.

"""Tests of the octahedral normal encoding and of the example texel layout."""

import math
import random

from g_buffer import (
    decode_normal,
    encode_normal,
    encode_normal_best,
    normalize,
    oct_decode,
    oct_encode,
    pack_texel,
    unpack_texel,
)


def random_unit(rng: random.Random) -> tuple[float, float, float]:
    while True:
        v = (rng.gauss(0.0, 1.0), rng.gauss(0.0, 1.0), rng.gauss(0.0, 1.0))
        if v[0] * v[0] + v[1] * v[1] + v[2] * v[2] > 1e-6:
            return normalize(v)


def angle_deg(a, b) -> float:
    d = a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
    return math.degrees(math.acos(max(-1.0, min(1.0, d))))


def close(a, b, tol: float = 1e-12) -> bool:
    return all(abs(x - y) <= tol for x, y in zip(a, b))


def test_axes_and_corners() -> None:
    assert oct_encode((0.0, 0.0, 1.0)) == (0.0, 0.0)
    assert oct_encode((1.0, 0.0, 0.0)) == (1.0, 0.0)
    assert oct_encode((0.0, -1.0, 0.0)) == (0.0, -1.0)
    # The south pole goes to a corner; all four corners decode to it.
    assert oct_encode((0.0, 0.0, -1.0)) == (1.0, 1.0)
    for u, v in ((1.0, 1.0), (-1.0, 1.0), (1.0, -1.0), (-1.0, -1.0)):
        assert close(oct_decode(u, v), (0.0, 0.0, -1.0))


def test_round_trip_float() -> None:
    rng = random.Random(7)
    for _ in range(3000):
        n = random_unit(rng)
        u, v = oct_encode(n)
        assert -1.0 <= u <= 1.0 and -1.0 <= v <= 1.0
        assert close(oct_decode(u, v), n)


def test_round_trip_on_signed_zeros_and_equator() -> None:
    for n in ((0.0, 0.6, -0.8), (0.6, 0.0, -0.8), (-0.6, -0.0, -0.8), (0.6, 0.8, 0.0), (-0.8, 0.6, -0.0)):
        assert close(oct_decode(*oct_encode(n)), normalize(n))


def test_square_to_sphere_to_square() -> None:
    """On the open square the map is one to one, so encode(decode(p)) = p."""
    rng = random.Random(8)
    for _ in range(3000):
        u, v = rng.uniform(-0.999, 0.999), rng.uniform(-0.999, 0.999)
        p = oct_encode(oct_decode(u, v))
        assert abs(p[0] - u) < 1e-12 and abs(p[1] - v) < 1e-12


def test_decode_is_unit() -> None:
    rng = random.Random(9)
    for _ in range(2000):
        d = oct_decode(rng.uniform(-1.0, 1.0), rng.uniform(-1.0, 1.0))
        assert abs(d[0] ** 2 + d[1] ** 2 + d[2] ** 2 - 1.0) < 1e-12


def test_quantized_error_measured() -> None:
    """Measured largest angle errors on 4000 random directions. These are
    measurements on this sample, not proved bounds."""
    rng = random.Random(10)
    worst = {8: 0.0, 16: 0.0}
    worst_best = {8: 0.0, 16: 0.0}
    for _ in range(4000):
        n = random_unit(rng)
        for bits in (8, 16):
            worst[bits] = max(worst[bits], angle_deg(n, decode_normal(encode_normal(n, bits), bits)))
            worst_best[bits] = max(worst_best[bits], angle_deg(n, decode_normal(encode_normal_best(n, bits), bits)))
    assert worst[8] < 1.0 and worst[16] < 0.005
    assert worst_best[8] <= worst[8] and worst_best[16] <= worst[16]


def test_texel_round_trip() -> None:
    rng = random.Random(11)
    for _ in range(500):
        albedo = (rng.random(), rng.random(), rng.random())
        n = random_unit(rng)
        rough, metal = rng.random(), rng.random()
        words = pack_texel(albedo, n, rough, metal)
        assert all(0 <= w < 1 << 32 for w in words)
        a2, n2, r2, m2 = unpack_texel(words)
        assert all(abs(x - y) <= 0.5 / 255.0 + 1e-12 for x, y in zip(albedo, a2))
        assert abs(rough - r2) <= 0.5 / 255.0 + 1e-12
        assert abs(metal - m2) <= 0.5 / 255.0 + 1e-12
        assert angle_deg(n, n2) < 0.005
        again = pack_texel(a2, n2, r2, m2)
        assert again[0] == words[0] and again[2] == words[2]
