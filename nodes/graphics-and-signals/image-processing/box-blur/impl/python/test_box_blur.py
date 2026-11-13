# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/box-blur/. The authors are listed in prov/ES8PJ7.jsonl.

import random
from fractions import Fraction as F

from box_blur import BORDERS, border_index, box_blur, box_sum

EXAMPLE = [
    [10, 10, 10, 80, 80],
    [10, 10, 90, 80, 80],
    [10, 10, 10, 80, 80],
]


def direct_sum(image, r, border):
    """The direct 2D sum over the (2r+1) x (2r+1) window, O(r^2) per pixel."""
    h, w = len(image), len(image[0])
    out = []
    for y in range(h):
        row = []
        for x in range(w):
            s = 0
            for v in range(-r, r + 1):
                for u in range(-r, r + 1):
                    j, i = border_index(y + v, h, border), border_index(x + u, w, border)
                    if i is not None and j is not None:
                        s += image[j][i]
            row.append(s)
        out.append(row)
    return out


def test_example_sums_and_means() -> None:
    sums = box_sum(EXAMPLE, 1, "clamp")
    assert sums == [[90, 170, 380, 590, 720]] * 3
    means = box_blur(EXAMPLE, 1, "clamp")
    assert means[1] == [F(10), F(170, 9), F(380, 9), F(590, 9), F(80)]
    assert box_sum(EXAMPLE, 1, "zero")[0] == [40, 140, 280, 420, 320]


def test_border_index() -> None:
    assert [border_index(i, 3, "clamp") for i in range(-2, 5)] == [0, 0, 0, 1, 2, 2, 2]
    assert [border_index(i, 3, "mirror") for i in range(-3, 6)] == [2, 1, 0, 0, 1, 2, 2, 1, 0]
    assert [border_index(i, 3, "wrap") for i in range(-2, 5)] == [1, 2, 0, 1, 2, 0, 1]
    assert [border_index(i, 3, "zero") for i in range(-1, 4)] == [None, 0, 1, 2, None]


def test_edges() -> None:
    assert box_sum([], 2) == []
    assert box_sum([[]], 2) == []
    assert box_sum([[7]], 0) == [[7]]
    assert box_sum([[7]], 2, "clamp") == [[175]]
    assert box_sum([[7]], 2, "zero") == [[7]]
    assert box_blur([[5] * 4] * 3, 3, "mirror") == [[F(5)] * 4] * 3
    try:
        box_sum([[1]], -1)
    except ValueError:
        pass
    else:
        raise AssertionError("a negative radius must be rejected")


def test_radius_zero_is_identity() -> None:
    rng = random.Random(11)
    img = [[rng.randint(0, 255) for _ in range(6)] for _ in range(4)]
    for b in BORDERS:
        assert box_sum(img, 0, b) == img


def test_random_against_direct_sum() -> None:
    rng = random.Random(2024)
    for trial in range(600):
        h, w = rng.randint(1, 6), rng.randint(1, 6)
        r = rng.randint(0, 7)
        border = BORDERS[trial % 4]
        img = [[rng.randint(-255, 255) for _ in range(w)] for _ in range(h)]
        assert box_sum(img, r, border) == direct_sum(img, r, border)


def test_fraction_means_against_direct() -> None:
    rng = random.Random(77)
    for _ in range(100):
        h, w, r = rng.randint(1, 5), rng.randint(1, 5), rng.randint(0, 3)
        img = [[F(rng.randint(0, 40), rng.randint(1, 5)) for _ in range(w)] for _ in range(h)]
        want = [[F(s) / (2 * r + 1) ** 2 for s in row] for row in direct_sum(img, r, "mirror")]
        assert box_blur(img, r, "mirror") == want


def test_float_drift_is_small() -> None:
    rng = random.Random(5)
    img = [[rng.random() for _ in range(40)] for _ in range(3)]
    fast = box_blur(img, 4, "clamp")
    slow = direct_sum(img, 4, "clamp")
    for a, b in zip(fast, slow):
        for p, q in zip(a, b):
            assert abs(p - q / 81) < 1e-12
