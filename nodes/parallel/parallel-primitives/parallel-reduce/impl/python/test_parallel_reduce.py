# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-reduce/. The authors are listed in prov/7TMWGJ.jsonl.

import functools
import math
import operator
import random

from parallel_reduce import parallel_reduce, reduce_rounds

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
    ("sum", operator.add, 0, lambda r: r.randint(-50, 50)),
    ("max", max, -math.inf, lambda r: r.randint(-50, 50)),
    ("concat", operator.add, "", lambda r: r.choice("abcde")),
    ("matrix", mat_mul, (1, 0, 0, 1), lambda r: tuple(r.randint(-2, 2) for _ in range(4))),
    ("segmented", seg_op, (False, 0), lambda r: (r.random() < 0.3, r.randint(-9, 9))),
]

SIZES = [0, 1, 2, 3, 4, 5, 7, 8, 9, 15, 16, 17, 31, 32, 33, 64, 100, 127, 128, 129, 1000]


def test_example() -> None:
    a = [3, 1, 7, 0, 4, 1, 6, 3]
    assert parallel_reduce(operator.add, 0, a) == (25, 7, 3)
    assert reduce_rounds(operator.add, 0, a) == (25, 7, 3)
    assert parallel_reduce(operator.add, "", list("abcde"))[0] == "abcde"


def test_against_sequential_fold() -> None:
    rng = random.Random(7)
    for _name, op, e, gen in OPS:
        for n in SIZES:
            for _ in range(3):
                a = [gen(rng) for _ in range(n)]
                want = functools.reduce(op, a, e)
                v1, w1, s1 = parallel_reduce(op, e, a)
                v2, w2, s2 = reduce_rounds(op, e, a)
                assert v1 == want and v2 == want


def test_work_and_span_exact() -> None:
    for n in range(0, 600):
        a = list(range(n))
        _, w, s = parallel_reduce(operator.add, 0, a)
        _, w2, r2 = reduce_rounds(operator.add, 0, a)
        assert w == max(n - 1, 0) and w2 == w
        assert s == ceil_lg(n) and r2 == ceil_lg(n)


def test_float_sum_depends_on_tree() -> None:
    a = [1e16] + [1.0] * 8
    sequential = functools.reduce(operator.add, a, 0.0)
    tree, _, _ = parallel_reduce(operator.add, 0.0, a)
    assert sequential == 1e16
    assert tree == 1e16 + 6
    assert math.fsum(a) == 1e16 + 8
    assert (0.1 + 0.2) + 0.3 != 0.1 + (0.2 + 0.3)


def test_not_associative_operator_gives_tree_value() -> None:
    a = [8, 4, 2, 1]
    assert functools.reduce(operator.sub, a) == 1
    assert parallel_reduce(operator.sub, 0, a)[0] == (8 - 4) - (2 - 1) == 3
