# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/myers-diff/. The authors are listed in prov/245ETE.jsonl.

import random

from myers_diff import diff, edit_distance_indel, furthest_points


def lcs_length(x: str, y: str) -> int:
    c = [[0] * (len(y) + 1) for _ in range(len(x) + 1)]
    for i in range(1, len(x) + 1):
        for j in range(1, len(y) + 1):
            if x[i - 1] == y[j - 1]:
                c[i][j] = c[i - 1][j - 1] + 1
            else:
                c[i][j] = max(c[i - 1][j], c[i][j - 1])
    return c[len(x)][len(y)]


def apply(ops: list) -> tuple[list, list]:
    old = [item for op, item in ops if op in "=-"]
    new = [item for op, item in ops if op in "=+"]
    return old, new


def test_example() -> None:
    a, b = "ABCABBA", "CBABAC"
    assert edit_distance_indel(a, b) == 5
    assert furthest_points(a, b)[2] == {-2: 2, 0: 2, 2: 3}
    ops = diff(a, b)
    assert "".join(op for op, _ in ops) == "--=+==-=+"
    assert apply(ops) == (list(a), list(b))


def test_edges() -> None:
    assert diff("", "") == []
    assert diff("abc", "abc") == [("=", "a"), ("=", "b"), ("=", "c")]
    assert edit_distance_indel("abc", "") == 3
    assert edit_distance_indel("", "abc") == 3
    assert edit_distance_indel("abc", "xyz") == 6
    assert edit_distance_indel("kitten", "sitting") == 5


def test_lines() -> None:
    old = ["def f():", "    return 1", ""]
    new = ["def f():", "    x = 1", "    return x", ""]
    ops = diff(old, new)
    assert apply(ops) == (old, new)
    assert sum(op != "=" for op, _ in ops) == 3


def test_random_against_lcs() -> None:
    rng = random.Random(1986)
    for _ in range(800):
        a = "".join(rng.choice("ABC") for _ in range(rng.randrange(14)))
        b = "".join(rng.choice("ABC") for _ in range(rng.randrange(14)))
        ops = diff(a, b)
        dist = len(a) + len(b) - 2 * lcs_length(a, b)
        assert edit_distance_indel(a, b) == dist
        assert sum(op != "=" for op, _ in ops) == dist
        old, new = apply(ops)
        assert "".join(old) == a and "".join(new) == b
