# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pcsa/. The authors are listed in prov/1T1SSZ.jsonl.

import hashlib
import math
import random

from pcsa import PCSA, PHI, lowest_zero, rho


def keyed_hash(seed: int, width: int):
    key = seed.to_bytes(8, "little")

    def h(x: object) -> int:
        d = hashlib.blake2b(repr(x).encode(), digest_size=8, key=key).digest()
        return int.from_bytes(d, "little") & ((1 << width) - 1)

    return h


def test_rho_and_lowest_zero() -> None:
    for y in range(1, 1 << 9):
        assert rho(y, 9) == next(i for i in range(9) if y >> i & 1)
    assert rho(0, 9) == 9
    for b in range(1 << 9):
        assert lowest_zero(b) == next(i for i in range(10) if not b >> i & 1)


def test_worked_example() -> None:
    # m = 4 bitmaps; the low 2 bits of the hash pick the bitmap.
    table = {"a": 0b0100, "b": 0b1001, "c": 0b1010, "d": 0b0111, "e": 0b1100, "f": 0b1011}
    s = PCSA(4, table.__getitem__, hash_bits=8)
    s.add_all("abcadebf")
    # a: j=0, w=1 -> bit 0 ; e: j=0, w=3 -> bit 0 ; b: j=1, w=2 -> bit 1
    # c: j=2, w=2 -> bit 1 ; d: j=3, w=1 -> bit 0 ; f: j=3, w=2 -> bit 1
    assert s.bitmaps == [0b1, 0b10, 0b10, 0b11]
    assert [lowest_zero(b) for b in s.bitmaps] == [1, 0, 0, 2]
    assert abs(s.estimate() - 4 / PHI * 2 ** (3 / 4)) < 1e-12


def test_duplicates_and_merge() -> None:
    h = keyed_hash(7, 64)
    rng = random.Random(8)
    for _ in range(30):
        xs = [rng.randrange(4000) for _ in range(rng.randrange(400))]
        ys = [rng.randrange(4000) for _ in range(rng.randrange(400))]
        a, b, u = PCSA(16, h), PCSA(16, h), PCSA(16, h)
        a.add_all(xs)
        b.add_all(ys)
        u.add_all(xs + ys + xs)
        assert a.merge(b).bitmaps == u.bitmaps


def relative_errors(m: int, n: int, trials: int, seed: int) -> list[float]:
    # A fresh random table per trial: each distinct item gets independent random bits.
    rng = random.Random(seed)
    out = []
    for _ in range(trials):
        s = PCSA(m, lambda x: rng.getrandbits(64))
        s.add_all(range(n))
        out.append(s.estimate() / n - 1)
    return out


def test_standard_error_matches_078_over_sqrt_m() -> None:
    # Flajolet and Martin: standard error about 0.78 / sqrt(m) once n is large against m.
    m, n, trials = 32, 2000, 200
    errs = relative_errors(m, n, trials, seed=11)
    se = 0.78 / math.sqrt(m)
    rms = math.sqrt(sum(e * e for e in errs) / trials)
    mean = sum(errs) / trials
    # Tolerance: the sample RMS of 200 runs is within 25 percent of the true value
    # with wide margin; the mean is within 4 standard errors of the mean.
    assert 0.75 * se <= rms <= 1.25 * se
    assert abs(mean) <= 4 * se / math.sqrt(trials) + 0.31 / m
