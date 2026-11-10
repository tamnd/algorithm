# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hyperloglog/. The authors are listed in prov/ZE356T.jsonl.

import hashlib
import math
import random

from hyperloglog import TWO_32, HyperLogLog, alpha, corrected_estimate, raw_estimate, rho_left


def keyed_hash(seed: int, width: int):
    key = seed.to_bytes(8, "little")

    def h(x: object) -> int:
        d = hashlib.blake2b(repr(x).encode(), digest_size=8, key=key).digest()
        return int.from_bytes(d, "little") & ((1 << width) - 1)

    return h


def test_alpha_and_rho() -> None:
    assert (alpha(16), alpha(32), alpha(64)) == (0.673, 0.697, 0.709)
    assert abs(alpha(1 << 16) - 0.7213) < 1e-4
    for w in range(1, 1 << 8):
        assert rho_left(w, 8) == format(w, "08b").index("1") + 1
    assert rho_left(0, 8) == 9


def test_worked_example() -> None:
    # b = 4: m = 16 registers, the top 4 of 32 hash bits pick the register.
    def top(j: int, w: int) -> int:
        return j << 28 | w

    table = {"a": top(0, 1 << 25), "b": top(5, 1 << 27), "c": top(9, 1 << 20), "d": top(0, 1 << 26)}
    s = HyperLogLog(4, table.__getitem__)
    s.add_all("abcadb")
    # rho in a 28-bit field: 1 << 25 -> 3, 1 << 27 -> 1, 1 << 20 -> 8, 1 << 26 -> 2.
    want = [0] * 16
    want[0], want[5], want[9] = 3, 1, 8
    assert s.registers == want
    z = 13 + 2**-3 + 2**-1 + 2**-8
    assert abs(s.raw() - 0.673 * 256 / z) < 1e-9
    # The raw value is below 5m/2 = 40 and 13 registers are 0: linear counting.
    assert abs(s.estimate() - 16 * math.log(16 / 13)) < 1e-12


def test_large_range_correction() -> None:
    regs = [24] * 16
    e = raw_estimate(regs)
    assert e > TWO_32 / 30
    got = corrected_estimate(regs)
    assert abs(got - (-TWO_32 * math.log(1 - e / TWO_32))) < 1e-3
    assert got > e
    mid = [10] * 64
    assert corrected_estimate(mid) == raw_estimate(mid)


def test_duplicates_and_merge() -> None:
    h = keyed_hash(3, 32)
    rng = random.Random(4)
    for _ in range(30):
        xs = [rng.randrange(5000) for _ in range(rng.randrange(500))]
        ys = [rng.randrange(5000) for _ in range(rng.randrange(500))]
        a, b, u = HyperLogLog(5, h), HyperLogLog(5, h), HyperLogLog(5, h)
        a.add_all(xs)
        b.add_all(ys)
        u.add_all(xs + ys + ys)
        assert a.merge(b).registers == u.registers
        assert a.merge(b).estimate() == u.estimate()


def errors(b: int, n: int, trials: int, seed: int, raw: bool) -> list[float]:
    rng = random.Random(seed)
    out = []
    for _ in range(trials):
        s = HyperLogLog(b, lambda x: rng.getrandbits(32))
        s.add_all(range(n))
        out.append((s.raw() if raw else s.estimate()) / n - 1)
    return out


def test_standard_error_matches_104_over_sqrt_m() -> None:
    # FFGM Theorem 1 (fully random hash): standard error about 1.04 / sqrt(m),
    # here m = 64 (beta_64 = 1.054) and n = 4000, in the range without corrections.
    b, n, trials = 6, 4000, 200
    m = 1 << b
    errs = errors(b, n, trials, seed=5, raw=True)
    se = 1.054 / math.sqrt(m)
    rms = math.sqrt(sum(e * e for e in errs) / trials)
    mean = sum(errs) / trials
    # Tolerance: RMS within 25 percent of beta_m / sqrt(m); mean within 4 standard errors.
    assert 0.75 * se <= rms <= 1.25 * se
    assert abs(mean) <= 4 * se / math.sqrt(trials)


def test_small_range_correction_helps() -> None:
    # n = 40 with m = 64: the raw estimate has a large positive bias, linear counting does not.
    b, n, trials = 6, 40, 200
    raw = errors(b, n, trials, seed=6, raw=True)
    cor = errors(b, n, trials, seed=6, raw=False)
    assert sum(raw) / trials > 0.3
    assert abs(sum(cor) / trials) < 0.03
    assert math.sqrt(sum(e * e for e in cor) / trials) < 0.13
