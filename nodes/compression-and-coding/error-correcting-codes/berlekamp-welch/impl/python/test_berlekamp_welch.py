# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/berlekamp-welch/. The authors are listed in prov/7100GD.jsonl.

import itertools
import random

from berlekamp_welch import berlekamp_welch, poly_eval, solve_any
from gf import GF2m, GFp

F5 = GFp(5)
F7 = GFp(7)
F8 = GF2m(3, 0b1011)  # x^3 + x + 1
F16 = GF2m(4, 0b10011)  # x^4 + x + 1
F256 = GF2m(8, 0x11D)  # x^8 + x^4 + x^3 + x^2 + 1


def encode(f, msg: list[int], xs: list[int]) -> list[int]:
    return [poly_eval(f, msg, a) for a in xs]


def distance(a: list[int], b: list[int]) -> int:
    return sum(1 for x, y in zip(a, b) if x != y)


def test_worked_example_gf7() -> None:
    # f(x) = 1 + 2x at 0 .. 5 over GF(7) is 1 3 5 0 2 4; errors at positions 1 and 4
    xs = list(range(6))
    c = encode(F7, [1, 2], xs)
    assert c == [1, 3, 5, 0, 2, 4]
    y = [1, 6, 5, 0, 0, 4]
    assert berlekamp_welch(F7, xs, y, 2) == [1, 2]
    # the system has the unique solution E = (x - 1)(x - 4) = 4 + 2x + x^2, Q = E f = 4 + 3x + 5x^2 + 2x^3
    rows = [[1, a, a * a % 7, a ** 3 % 7, (-v) % 7, (-v * a) % 7] for a, v in zip(xs, y)]
    rhs = [v * a * a % 7 for a, v in zip(xs, y)]
    assert solve_any(F7, rows, rhs) == [4, 3, 5, 2, 4, 2]


def test_exhaustive_gf7() -> None:
    # n = 6, k = 2, e = 2 over GF(7): five messages, every pattern of at most 2 errors
    xs = list(range(6))
    for msg in ((0, 0), (1, 2), (6, 5), (3, 0), (0, 4)):
        c = encode(F7, list(msg), xs)
        for nu in range(3):
            for pos in itertools.combinations(range(6), nu):
                for vals in itertools.product(range(1, 7), repeat=nu):
                    y = list(c)
                    for i, v in zip(pos, vals):
                        y[i] = (y[i] + v) % 7
                    assert berlekamp_welch(F7, xs, y, 2) == list(msg)


def test_exhaustive_rs_7_3_gf8() -> None:
    # RS(7, 3) over GF(8) at the points alpha^0 .. alpha^6, e = 2, every pattern of at most 2 errors
    xs = [F8.alpha(i) for i in range(7)]
    msg = [3, 0, 5]
    c = encode(F8, msg, xs)
    for nu in range(3):
        for pos in itertools.combinations(range(7), nu):
            for vals in itertools.product(range(1, 8), repeat=nu):
                y = list(c)
                for i, v in zip(pos, vals):
                    y[i] ^= v
                assert berlekamp_welch(F8, xs, y, 3) == msg


def test_against_brute_force_nearest_codeword() -> None:
    # 600 random words over GF(5), n = 5: BW returns the codeword within distance e if there is one, else None
    rng = random.Random(1986)
    xs = list(range(5))
    for _ in range(600):
        k = rng.choice((1, 2, 3))
        e = (5 - k) // 2
        if rng.random() < 0.5:
            y = [rng.randrange(5) for _ in range(5)]
        else:
            y = encode(F5, [rng.randrange(5) for _ in range(k)], xs)
            for i in rng.sample(range(5), rng.randrange(0, e + 2)):
                y[i] = rng.randrange(5)
        close = [list(m) for m in itertools.product(range(5), repeat=k)
                 if distance(encode(F5, list(m), xs), y) <= e]
        assert len(close) <= 1
        assert berlekamp_welch(F5, xs, y, k) == (close[0] if close else None)


def test_random_gf16_and_gf256() -> None:
    rng = random.Random(4633470)
    cases = [(F16, 15, 7), (F16, 15, 11), (F16, 12, 5), (F256, 40, 20), (F256, 30, 29)]
    for f, n, k in cases:
        xs = [f.alpha(i) for i in range(n)]
        e = (n - k) // 2
        for _ in range(20):
            msg = [rng.randrange(f.q) for _ in range(k)]
            y = encode(f, msg, xs)
            nu = rng.randrange(0, e + 1)
            for i in rng.sample(range(n), nu):
                y[i] ^= rng.randrange(1, f.q)
            assert berlekamp_welch(f, xs, y, k) == msg


def test_beyond_e_is_detected_or_close() -> None:
    # with e + 1 errors the result is None or a different message within distance e
    rng = random.Random(5)
    xs = [F16.alpha(i) for i in range(15)]
    detected = 0
    for _ in range(200):
        msg = [rng.randrange(16) for _ in range(7)]
        y = encode(F16, msg, xs)
        for i in rng.sample(range(15), 5):
            y[i] ^= rng.randrange(1, 16)
        out = berlekamp_welch(F16, xs, y, 7)
        if out is None:
            detected += 1
        else:
            assert out != msg and distance(encode(F16, out, xs), y) <= 4
    assert detected > 150


def test_any_points_and_edges() -> None:
    # the points need not be powers of alpha; 0 is allowed
    xs = [0, 3, 1, 6, 2, 5, 4]
    c = encode(F7, [6, 0, 1], xs)
    y = list(c)
    y[0] = (y[0] + 1) % 7
    y[6] = (y[6] + 3) % 7
    assert berlekamp_welch(F7, xs, y, 3) == [6, 0, 1]
    # e = 0: plain interpolation, any word of length k is a codeword
    assert berlekamp_welch(F7, [1, 2, 3], [4, 4, 4], 3) == [4, 0, 0]
    # n = k + 1 gives e = 0: a single error is detected
    assert berlekamp_welch(F7, [1, 2, 3, 4], [1, 1, 1, 2], 3) is None
    # all zero word
    assert berlekamp_welch(F16, [F16.alpha(i) for i in range(15)], [0] * 15, 5) == [0] * 5
