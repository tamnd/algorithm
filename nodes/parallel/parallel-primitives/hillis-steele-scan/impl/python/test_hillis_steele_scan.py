# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hillis-steele-scan/. The authors are listed in prov/H3KT7W.jsonl.

import itertools
import operator
import random

from hillis_steele_scan import hillis_steele_scan, in_place_scan_wrong, round_reads

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

SIZES = [0, 1, 2, 3, 4, 5, 7, 8, 9, 15, 16, 17, 31, 32, 33, 63, 64, 65, 100, 128, 200]


def test_example() -> None:
    out, work, rounds = hillis_steele_scan(operator.add, [3, 1, 7, 0, 4, 1, 6, 3])
    assert out == [3, 4, 11, 11, 15, 16, 22, 25]
    assert (work, rounds) == (17, 3)


def test_against_accumulate() -> None:
    rng = random.Random(1986)
    for op, gen in OPS:
        for n in SIZES:
            for _ in range(3):
                a = [gen(rng) for _ in range(n)]
                out, _, _ = hillis_steele_scan(op, a)
                assert out == list(itertools.accumulate(a, op))


def test_work_and_rounds_exact() -> None:
    for n in range(0, 700):
        _, work, rounds = hillis_steele_scan(operator.add, [1] * n)
        k = ceil_lg(n)
        assert rounds == k
        # n * ceil(lg n) applications, minus the 2^k - 1 skipped positions
        assert work == (n * k - (2**k - 1) if n > 0 else 0)
        if n >= 2:
            assert n * k - 2 * n < work <= n * k


def test_erew_substeps_have_distinct_reads() -> None:
    for n in (1, 2, 5, 8, 13, 64, 100):
        d = 1
        while d < n:
            first, second = round_reads(n, d)
            assert len(set(first)) == len(first)
            assert len(set(second)) == len(second)
            d *= 2


def test_in_place_update_is_wrong() -> None:
    a = [1, 1, 1, 1]
    assert hillis_steele_scan(operator.add, a)[0] == [1, 2, 3, 4]
    # After round d = 1 the in-place loop already holds the full prefix sums,
    # so round d = 2 adds x[0] and x[1] a second time.
    assert in_place_scan_wrong(operator.add, a) == [1, 2, 4, 6]
