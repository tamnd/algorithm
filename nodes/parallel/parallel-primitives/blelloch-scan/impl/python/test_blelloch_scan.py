# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blelloch-scan/. The authors are listed in prov/GXQF52.jsonl.

import itertools
import math
import operator
import random

from blelloch_scan import Stats, blelloch_scan, down_sweep_swapped

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
    (operator.add, 0, lambda r: r.randint(-50, 50)),
    (max, -math.inf, lambda r: r.randint(-50, 50)),
    (operator.add, "", lambda r: r.choice("abcde")),
    (mat_mul, (1, 0, 0, 1), lambda r: tuple(r.randint(-2, 2) for _ in range(4))),
    (seg_op, (False, 0), lambda r: (r.random() < 0.3, r.randint(-9, 9))),
]

SIZES = [0, 1, 2, 3, 4, 5, 7, 8, 9, 15, 16, 17, 31, 32, 33, 63, 64, 65, 100, 128, 200]


def exclusive(op, e, a):
    pre = list(itertools.accumulate(a, op, initial=e))
    return pre[:-1], pre[-1]


def test_example() -> None:
    st = Stats()
    out, total = blelloch_scan(operator.add, 0, [3, 1, 7, 0, 4, 1, 6, 3], st)
    assert out == [0, 3, 4, 11, 11, 15, 16, 22]
    assert total == 25
    assert (st.work, st.rounds, st.chain) == (14, 6, 5)


def test_against_accumulate() -> None:
    rng = random.Random(1990)
    for op, e, gen in OPS:
        for n in SIZES:
            for _ in range(3):
                a = [gen(rng) for _ in range(n)]
                assert blelloch_scan(op, e, a) == exclusive(op, e, a)


def test_work_and_span_exact() -> None:
    for n in range(0, 700):
        st = Stats()
        blelloch_scan(operator.add, 0, list(range(n)), st)
        k = ceil_lg(n)
        m = 2**k
        assert st.work == (2 * (m - 1) if n > 0 else 0)
        assert st.rounds == 2 * k
        assert st.chain == (2 * k - 1 if n >= 2 else 0)
        if n >= 1:
            assert st.work < 4 * n


def test_swapped_down_sweep_fails_for_strings() -> None:
    a = list("abcd")
    assert blelloch_scan(operator.add, "", a)[0] == ["", "a", "ab", "abc"]
    assert down_sweep_swapped(operator.add, "", a) == ["", "a", "ab", "cab"]
    # For a commutative operator the swapped version is still right.
    assert down_sweep_swapped(operator.add, 0, [3, 1, 7, 0]) == [0, 3, 4, 11]
