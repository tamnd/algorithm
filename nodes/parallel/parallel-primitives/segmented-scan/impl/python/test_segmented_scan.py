# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/segmented-scan/. The authors are listed in prov/KQTVZW.jsonl.

import itertools
import math
import operator
import random

from segmented_scan import (
    Stats,
    exclusive_without_care,
    flags_from_lengths,
    seg_op,
    segmented_scan,
)

Mat = tuple[int, int, int, int]


def mat_mul(x: Mat, y: Mat) -> Mat:
    a, b, c, d = x
    e, f, g, h = y
    return (a * e + b * g, a * f + b * h, c * e + d * g, c * f + d * h)


def segments(flags, a):
    """Split a into its segments."""
    out = []
    for i, x in enumerate(a):
        if i == 0 or flags[i]:
            out.append([])
        out[-1].append(x)
    return out


def reference(op, e, flags, a):
    inc, exc = [], []
    for seg in segments(flags, a):
        pre = list(itertools.accumulate(seg, op, initial=e))
        inc += pre[1:]
        exc += pre[:-1]
    return inc, exc


OPS = [
    (operator.add, 0, lambda r: r.randint(-50, 50)),
    (max, -math.inf, lambda r: r.randint(-50, 50)),
    (operator.add, "", lambda r: r.choice("abcde")),
    (mat_mul, (1, 0, 0, 1), lambda r: tuple(r.randint(-2, 2) for _ in range(4))),
]

SIZES = [0, 1, 2, 3, 4, 5, 7, 8, 9, 15, 16, 17, 31, 32, 33, 64, 100, 200]


def test_example() -> None:
    a = [3, 1, 7, 0, 4, 1, 6, 3]
    f = [True, False, True, False, False, True, False, False]
    inc, exc = segmented_scan(operator.add, 0, f, a)
    assert inc == [3, 4, 7, 7, 11, 1, 7, 10]
    assert exc == [0, 3, 0, 7, 7, 0, 1, 7]


def test_against_reference() -> None:
    rng = random.Random(1980)
    for op, e, gen in OPS:
        for n in SIZES:
            for density in (0.0, 0.1, 0.5, 1.0):
                a = [gen(rng) for _ in range(n)]
                f = [rng.random() < density for _ in range(n)]
                assert segmented_scan(op, e, f, a) == reference(op, e, f, a)


def test_operator_is_associative_by_brute_force() -> None:
    domains = [
        (operator.add, 0, [-1, 0, 1, 2]),
        (max, -math.inf, [-math.inf, 0, 1, 5]),
        (operator.add, "", ["", "a", "b", "ab"]),
        (operator.sub, 0, [0, 1, 3]),  # not associative: must fail
    ]
    for op, e, values in domains:
        s = seg_op(op)
        dom = [(f, v) for f in (False, True) for v in values]
        assoc = all(s(s(x, y), z) == s(x, s(y, z)) for x in dom for y in dom for z in dom)
        assert assoc == (op is not operator.sub)
        if assoc:
            for x in dom:
                assert s((False, e), x) == x and s(x, (False, e)) == x


def test_segmented_operator_is_not_commutative() -> None:
    s = seg_op(operator.add)
    assert s((True, 1), (False, 2)) == (True, 3)
    assert s((False, 2), (True, 1)) == (True, 1)


def test_exclusive_needs_care_at_segment_starts() -> None:
    a = [3, 1, 7, 0]
    f = [True, False, True, False]
    assert segmented_scan(operator.add, 0, f, a)[1] == [0, 3, 0, 7]
    assert exclusive_without_care(operator.add, 0, f, a) == [0, 3, 4, 7]


def test_work_and_rounds() -> None:
    for n in range(1, 300):
        st = Stats()
        segmented_scan(operator.add, 0, [False] * n, list(range(n)), st)
        k = (n - 1).bit_length()
        assert st.work == 2 * (2**k - 1) + n
        assert st.rounds == 2 * k + 1


def test_flags_from_lengths() -> None:
    assert flags_from_lengths([2, 3, 1]) == [True, False, True, False, False, True]
    assert flags_from_lengths([0, 2, 0, 1]) == [True, False, True]
