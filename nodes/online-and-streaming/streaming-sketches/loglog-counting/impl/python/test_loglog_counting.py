# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/loglog-counting/. The authors are listed in prov/919CZB.jsonl.

import hashlib
import math
import random

from loglog_counting import ALPHA_INF, LogLog, alpha, rho_left


def keyed_hash(seed: int, width: int):
    key = seed.to_bytes(8, "little")

    def h(x: object) -> int:
        d = hashlib.blake2b(repr(x).encode(), digest_size=8, key=key).digest()
        return int.from_bytes(d, "little") & ((1 << width) - 1)

    return h


def test_rho_left() -> None:
    width = 8
    for w in range(1, 1 << width):
        bits = format(w, "08b")
        assert rho_left(w, width) == bits.index("1") + 1
    assert rho_left(0, width) == width + 1


def test_alpha_tends_to_alpha_inf() -> None:
    gamma = 0.5772156649015329
    assert abs(math.exp(-gamma) * math.sqrt(2) / 2 - ALPHA_INF) < 1e-5
    assert abs(alpha(1 << 12) - ALPHA_INF) < 1e-4
    # alpha_m increases towards alpha_inf; the relative gap is about 0.84 / m,
    # so at m = 64 it is about 1.3 percent, far below the standard error 1.30 / 8.
    assert alpha(16) < alpha(64) < alpha(1024) < ALPHA_INF + 1e-6
    assert abs(alpha(64) / ALPHA_INF - 1) < 0.015
    for m in (64, 256, 1024):
        assert abs(m * (1 - alpha(m) / ALPHA_INF) - 0.84) < 0.02


def test_worked_example() -> None:
    # b = 2: m = 4 registers, the top 2 of 32 hash bits pick the register.
    def top(j: int, w: int) -> int:
        return j << 30 | w

    table = {"a": top(0, 1 << 27), "b": top(1, 1 << 29), "c": top(2, 1 << 25), "d": top(0, 1 << 29), "e": top(3, 1 << 28)}
    s = LogLog(2, table.__getitem__)
    s.add_all("abcadeb")
    # rho of w in a 30-bit field: 1 << 27 -> 3, 1 << 29 -> 1, 1 << 25 -> 5, 1 << 28 -> 2.
    assert s.registers == [3, 1, 5, 2]
    assert abs(s.estimate() - alpha(4) * 4 * 2 ** (11 / 4)) < 1e-9


def test_duplicates_and_merge() -> None:
    h = keyed_hash(5, 32)
    rng = random.Random(6)
    for _ in range(30):
        xs = [rng.randrange(4000) for _ in range(rng.randrange(400))]
        ys = [rng.randrange(4000) for _ in range(rng.randrange(400))]
        a, b, u = LogLog(4, h), LogLog(4, h), LogLog(4, h)
        a.add_all(xs)
        b.add_all(ys)
        u.add_all(ys + xs + ys)
        assert a.merge(b).registers == u.registers


def test_standard_error_matches_130_over_sqrt_m() -> None:
    # Durand and Flajolet: asymptotically unbiased, standard error about 1.30 / sqrt(m).
    rng = random.Random(9)
    b, n, trials = 6, 2000, 200
    m = 1 << b
    errs = []
    for _ in range(trials):
        s = LogLog(b, lambda x: rng.getrandbits(32))
        s.add_all(range(n))
        errs.append(s.estimate() / n - 1)
    se = 1.30 / math.sqrt(m)
    rms = math.sqrt(sum(e * e for e in errs) / trials)
    mean = sum(errs) / trials
    # Tolerance: RMS within 25 percent of 1.30 / sqrt(m); mean within 4 standard errors.
    assert 0.75 * se <= rms <= 1.25 * se
    assert abs(mean) <= 4 * se / math.sqrt(trials)
