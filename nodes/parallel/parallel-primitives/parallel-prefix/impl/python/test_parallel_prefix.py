# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-prefix/. The authors are listed in prov/98XS2A.jsonl.

import itertools
import operator
import random

from parallel_prefix import brent_kung, evaluate, kogge_stone, ladner_fischer, serial, sklansky

Mat = tuple[int, int, int, int]


def mat_mul(x: Mat, y: Mat) -> Mat:
    a, b, c, d = x
    e, f, g, h = y
    return (a * e + b * g, a * f + b * h, c * e + d * g, c * f + d * h)


def seg_op(x: tuple[bool, int], y: tuple[bool, int]) -> tuple[bool, int]:
    return (x[0] or y[0], y[1] if y[0] else x[1] + y[1])


def ceil_lg(n: int) -> int:
    return (n - 1).bit_length() if n > 0 else 0


OPS = [
    (operator.add, lambda r: r.randint(-50, 50)),
    (max, lambda r: r.randint(-50, 50)),
    (operator.add, lambda r: r.choice("abcde")),
    (mat_mul, lambda r: tuple(r.randint(-2, 2) for _ in range(4))),
    (seg_op, lambda r: (r.random() < 0.3, r.randint(-9, 9))),
]

SIZES = [0, 1, 2, 3, 4, 5, 7, 8, 9, 15, 16, 17, 31, 32, 33, 64, 100]


def circuits(n: int):
    yield "serial", serial(n)
    yield "sklansky", sklansky(n)
    yield "kogge-stone", kogge_stone(n)
    yield "brent-kung", brent_kung(n)
    for k in range(0, ceil_lg(n) + 1):
        yield f"lf{k}", ladner_fischer(n, k)


def test_all_circuits_compute_prefixes() -> None:
    rng = random.Random(1980)
    for op, gen in OPS:
        for n in SIZES:
            want_a = [gen(rng) for _ in range(n)]
            want = list(itertools.accumulate(want_a, op))
            for name, gates in circuits(n):
                out, _, _ = evaluate(op, gates, want_a)
                assert out == want, (name, n)


def test_exact_size_and_depth() -> None:
    for n in range(1, 300):
        k = ceil_lg(n)
        assert evaluate(operator.add, serial(n), [0] * n)[1:] == (n - 1, n - 1)
        assert evaluate(operator.add, kogge_stone(n), [0] * n)[1:] == (n * k - 2**k + 1, k)
    for k in range(1, 10):
        n = 2**k
        assert evaluate(operator.add, sklansky(n), [0] * n)[1:] == (n // 2 * k, k)
        assert evaluate(operator.add, brent_kung(n), [0] * n)[1:] == (2 * n - 2 - k, max(2 * k - 2, 1))


def test_ladner_fischer_bounds() -> None:
    # The example size C(P_0(9)) = 13 from the paper.
    assert evaluate(operator.add, ladner_fischer(9, 0), [0] * 9)[1] == 13
    for n in range(1, 300):
        lg = ceil_lg(n)
        for k in range(0, lg + 1):
            _, size, depth = evaluate(operator.add, ladner_fischer(n, k), [0] * n)
            assert depth <= k + lg
            assert size <= 2 * (1 + 2**-k) * n
        _, size0, depth0 = evaluate(operator.add, ladner_fischer(n, 0), [0] * n)
        assert depth0 == lg and size0 <= 4 * n


def test_general_lower_bounds() -> None:
    for n in range(2, 200):
        for _name, gates in circuits(n):
            _, size, depth = evaluate(operator.add, gates, [0] * n)
            assert size >= n - 1
            assert depth >= ceil_lg(n)
            assert size + depth >= 2 * n - 2  # Snir (1986)
