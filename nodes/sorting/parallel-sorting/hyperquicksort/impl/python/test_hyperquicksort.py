# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hyperquicksort/. The authors are listed in prov/J95TFF.jsonl.

import random

import pytest

from hyperquicksort import flatten, hyperquicksort


EXAMPLE = [[42, 7, 93, 25], [60, 12, 88, 3], [54, 31, 76, 19], [65, 8, 47, 99]]


def test_example() -> None:
    out = hyperquicksort(EXAMPLE)
    assert out == [[3, 7, 8, 12, 19], [25], [31, 42, 47, 54], [60, 65, 76, 88, 93, 99]]


def test_edges() -> None:
    assert hyperquicksort([[]]) == [[]]
    assert hyperquicksort([[3, 1, 2]]) == [[1, 2, 3]]
    assert hyperquicksort([[], [], [2, 1], []]) == [[1], [], [2], []]
    with pytest.raises(ValueError):
        hyperquicksort([[1], [2], [3]])


def test_imbalance_on_two_processors() -> None:
    out = hyperquicksort([list(range(8)), list(range(8, 16))])
    assert [len(x) for x in out] == [4, 12]
    assert flatten(out) == list(range(16))


def test_random_inputs() -> None:
    rng = random.Random(7)
    for _ in range(200):
        p = 1 << rng.randint(0, 4)
        lists = [[rng.randint(0, 50) for _ in range(rng.randint(0, 12))] for _ in range(p)]
        out = hyperquicksort(lists)
        keys = sorted(x for lst in lists for x in lst)
        assert flatten(out) == keys
        for q in range(p):
            assert out[q] == sorted(out[q])
