# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bit-plane-coding/. The authors are listed in prov/8GXKH4.jsonl.

import random

from bit_plane_coding import bit_planes, decode, encode, from_bit_planes, gray, gray_inverse, num_planes


def test_worked_example() -> None:
    v = [5, -3, 0, 12, -1]
    planes = num_planes(v)
    assert planes == 4
    s = encode(v, planes)
    assert "".join(map(str, s)) == "000100" + "100010" + "011000" + "110011"
    assert decode(s[:6], 5, planes)[0] == [0, 0, 0, 12, 0]
    assert decode(s[:12], 5, planes)[0] == [6, 0, 0, 14, 0]
    assert decode(s[:12], 5, planes, midpoint=False)[0] == [4, 0, 0, 12, 0]
    assert decode(s[:18], 5, planes)[0] == [5, -3, 0, 13, 0]
    assert decode(s, 5, planes)[0] == v


def laplacian_ints(rng: random.Random, n: int, scale: float) -> list:
    return [int(rng.expovariate(1 / scale)) * rng.choice((-1, 1)) for _ in range(n)]


def test_full_stream_is_lossless() -> None:
    rng = random.Random(1)
    for _ in range(200):
        v = laplacian_ints(rng, rng.randint(1, 40), rng.choice((1, 5, 50)))
        planes = num_planes(v)
        est, known = decode(encode(v, planes), len(v), planes)
        assert est == v and all(k == 0 for k in known) or planes == 0


def test_truncation_error_bound_at_each_plane() -> None:
    rng = random.Random(2)
    for _ in range(100):
        v = laplacian_ints(rng, 30, 20)
        planes = num_planes(v)
        s = encode(v, planes)
        # The prefix that ends each plane: count the bits written per plane.
        cut = 0
        for p in range(planes - 1, -1, -1):
            cut += sum(1 + (1 if (abs(x) >> p) & 1 and abs(x) >> (p + 1) == 0 else 0) for x in v)
            plain, known = decode(s[:cut], len(v), planes, midpoint=False)
            mid, _ = decode(s[:cut], len(v), planes)
            assert all(k == p for k in known)
            for x, a, b in zip(v, plain, mid):
                assert 0 <= abs(x) - abs(a) <= 2 ** p - 1 and (a == 0 or (a < 0) == (x < 0))
                if abs(x) >> p:  # significant: the midpoint halves the bound
                    assert abs(x - b) <= 2 ** (p - 1) if p > 0 else x == b
                else:
                    assert b == 0 and abs(x) <= 2 ** p - 1
            # Truncating at plane p is a dead-zone quantizer with step 2^p.
            assert [abs(a) >> p for a in plain] == [abs(x) // 2 ** p for x in v]


def test_every_prefix_decodes_within_bound() -> None:
    rng = random.Random(3)
    v = laplacian_ints(rng, 25, 30)
    planes = num_planes(v)
    s = encode(v, planes)
    prev_max = None
    for k in range(len(s) + 1):
        est, known = decode(s[:k], len(v), planes)
        for x, e, p in zip(v, est, known):
            if abs(x) >> p:
                assert abs(x - e) <= (2 ** (p - 1) if p > 0 else 0)
            else:
                assert e == 0 and abs(x) <= 2 ** p - 1
        bound = max(2 ** p - 1 for p in known)
        assert prev_max is None or bound <= prev_max  # the worst-case bound never grows
        prev_max = bound


def test_gray_code_planes() -> None:
    for a in range(1023):
        diff = gray(a) ^ gray(a + 1)
        assert diff and diff & (diff - 1) == 0  # neighbours differ in exactly one plane
        assert gray_inverse(gray(a)) == a
    ramp = list(range(256))
    changes = lambda planes: sum(r[i] != r[i + 1] for r in planes for i in range(len(r) - 1))
    assert changes(bit_planes(ramp, 8)) == 502
    assert changes(bit_planes(ramp, 8, use_gray=True)) == 255
    rng = random.Random(4)
    samples = [rng.randrange(256) for _ in range(100)]
    for g in (False, True):
        assert from_bit_planes(bit_planes(samples, 8, g), g) == samples
