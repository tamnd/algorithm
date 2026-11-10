# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/flajolet-martin-algorithm/. The authors are listed in prov/YQ5W45.jsonl.

import hashlib
import itertools
import math
import random
from math import comb

from flajolet_martin_algorithm import (
    PHI,
    FMSketch,
    GF2AffineHash,
    ams_f0,
    ams_median,
    fm_count,
    lowest_zero,
    rho,
)


def keyed_hash(seed: int, width: int):
    key = seed.to_bytes(8, "little")

    def h(x: object) -> int:
        d = hashlib.blake2b(repr(x).encode(), digest_size=8, key=key).digest()
        return int.from_bytes(d, "little") & ((1 << width) - 1)

    return h


EXAMPLE = {"a": 0b01101100, "b": 0b10010001, "c": 0b00101010, "d": 0b10110000, "e": 0b01010011, "f": 0b10100110}


def test_rho_and_lowest_zero() -> None:
    for y in range(1, 1 << 10):
        want = next(i for i in range(10) if y >> i & 1)
        assert rho(y, 10) == want
    assert rho(0, 10) == 10
    for b in range(1 << 10):
        assert lowest_zero(b) == next(i for i in range(11) if not b >> i & 1)


def test_worked_example() -> None:
    stream = list("abcadebf")
    s = FMSketch(EXAMPLE.__getitem__, 8)
    for x in stream:
        s.add(x)
    assert s.bitmap == 0b10111
    assert s.big_r() == 3
    assert abs(fm_count(stream, EXAMPLE.__getitem__, 8) - 8 / PHI) < 1e-12
    assert abs(8 / PHI - 10.342) < 1e-3


def test_duplicates_do_not_change_the_state() -> None:
    h = keyed_hash(1, 32)
    a, b = FMSketch(h, 32), FMSketch(h, 32)
    for x in range(500):
        a.add(x)
    for x in list(range(500)) * 3:
        b.add(x)
    assert a.bitmap == b.bitmap


def test_merge_equals_sketch_of_union() -> None:
    h = keyed_hash(2, 32)
    rng = random.Random(3)
    for _ in range(50):
        xs = [rng.randrange(5000) for _ in range(rng.randrange(300))]
        ys = [rng.randrange(5000) for _ in range(rng.randrange(300))]
        a, b, u = FMSketch(h, 32), FMSketch(h, 32), FMSketch(h, 32)
        for x in xs:
            a.add(x)
        for y in ys:
            b.add(y)
        for z in xs + ys:
            u.add(z)
        assert a.merge(b).bitmap == u.bitmap


def test_mean_of_r_is_log2_phi_n() -> None:
    # Flajolet and Martin: E[R] = log2(PHI n) + small oscillation, sd(R) about 1.12.
    rng = random.Random(4)
    n, runs = 1000, 1000
    rs = []
    for _ in range(runs):
        bitmap = 0
        for _ in range(n):
            bitmap |= 1 << rho(rng.getrandbits(32), 32)
        rs.append(lowest_zero(bitmap))
    mean = sum(rs) / runs
    sd = math.sqrt(sum((r - mean) ** 2 for r in rs) / (runs - 1))
    assert abs(mean - math.log2(PHI * n)) <= 4 * 1.13 / math.sqrt(runs)
    assert 0.95 <= sd <= 1.30


def test_gf2_family_is_pairwise_independent() -> None:
    bits = 3
    counts: dict[tuple[int, int, int, int], int] = {}
    for cols in itertools.product(range(8), repeat=bits):
        for b in range(8):
            h = GF2AffineHash(bits, random.Random(0))
            h.columns, h.offset = list(cols), b
            for x, y in itertools.permutations(range(8), 2):
                key = (x, y, h(x), h(y))
                counts[key] = counts.get(key, 0) + 1
    # 2^12 functions, 64 output pairs: each (x, y, u, v) occurs 2^12 / 64 = 64 times.
    assert len(counts) == 56 * 64
    assert set(counts.values()) == {64}


def test_ams_constant_factor_bounds() -> None:
    rng = random.Random(5)
    bits, d, runs = 16, 200, 1000
    items = rng.sample(range(1 << bits), d)
    high = low = 0
    for _ in range(runs):
        est = ams_f0(items, GF2AffineHash(bits, rng))
        high += est >= 3 * d
        low += est <= d / 3
    bound = math.sqrt(2) / 3
    tol = 3 * math.sqrt(bound * (1 - bound) / runs)
    assert high / runs <= bound + tol
    assert low / runs <= bound + tol
    assert ams_f0([], GF2AffineHash(bits, rng)) == 0.0


def test_ams_median_failure_rate() -> None:
    rng = random.Random(6)
    bits, d, t, runs = 16, 100, 9, 300
    items = rng.sample(range(1 << bits), d)
    bad = 0
    for _ in range(runs):
        est = ams_median(items, [GF2AffineHash(bits, rng) for _ in range(t)])
        bad += not d / 3 < est < 3 * d
    q = math.sqrt(2) / 3
    one_side = sum(comb(t, k) * q**k * (1 - q) ** (t - k) for k in range(t // 2 + 1, t + 1))
    bound = 2 * one_side
    assert bad / runs <= bound + 3 * math.sqrt(bound * (1 - bound) / runs)
