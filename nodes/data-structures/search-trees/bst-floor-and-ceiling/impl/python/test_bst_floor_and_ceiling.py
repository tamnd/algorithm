# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bst-floor-and-ceiling/. The authors are listed in prov/85F3S3.jsonl.

import bisect
import random

from bst_floor_and_ceiling import ceiling, floor, insert

EXAMPLE = [50, 30, 70, 20, 40, 60, 80, 35, 45, 65]


def build(keys):
    root = None
    for k in keys:
        root = insert(root, k)
    return root


def test_example() -> None:
    root = build(EXAMPLE)
    assert floor(root, 62) == 60 and ceiling(root, 62) == 65
    assert floor(root, 45) == 45 and ceiling(root, 45) == 45
    assert floor(root, 10) is None and ceiling(root, 10) == 20
    assert floor(root, 90) == 80 and ceiling(root, 90) is None
    assert floor(root, 49) == 45 and ceiling(root, 49) == 50
    assert floor(root, 36) == 35 and ceiling(root, 36) == 40


def test_edges() -> None:
    assert floor(None, 1) is None and ceiling(None, 1) is None
    root = build([5])
    assert floor(root, 5) == 5 and floor(root, 4) is None and floor(root, 6) == 5
    assert ceiling(root, 4) == 5 and ceiling(root, 6) is None


def test_chain() -> None:
    root = build(list(range(0, 6000, 2)))
    assert floor(root, 5999) == 5998 and ceiling(root, 1) == 2


def test_random_against_bisect() -> None:
    rng = random.Random(3301)
    for _ in range(600):
        keys = [rng.randint(0, 80) for _ in range(rng.randint(0, 30))]
        root = build(keys)
        s = sorted(set(keys))
        for q in range(-2, 84):
            i = bisect.bisect_right(s, q)
            assert floor(root, q) == (s[i - 1] if i else None)
            j = bisect.bisect_left(s, q)
            assert ceiling(root, q) == (s[j] if j < len(s) else None)
