# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/median-filter/. The authors are listed in prov/HHPV82.jsonl.

import random

from median_filter import median_filter_1d, median_filter_2d


def clamp(i, n):
    return min(max(i, 0), n - 1)


def brute_1d(x, m):
    n = len(x)
    return [sorted(x[clamp(k + j, n)] for j in range(-m, m + 1))[m] for k in range(n)]


def brute_2d(img, m):
    rows, cols = len(img), len(img[0])
    out = []
    for r in range(rows):
        row = []
        for c in range(cols):
            vals = sorted(img[clamp(r + a, rows)][clamp(c + b, cols)] for a in range(-m, m + 1) for b in range(-m, m + 1))
            row.append(vals[(len(vals) - 1) // 2])
        out.append(row)
    return out


def test_1d_against_sort() -> None:
    rng = random.Random(10101)
    for _ in range(300):
        n = rng.randint(1, 40)
        m = rng.randint(0, 6)
        x = [rng.randint(-5, 5) for _ in range(n)]
        assert median_filter_1d(x, m) == brute_1d(x, m)


def test_2d_against_sort() -> None:
    rng = random.Random(10102)
    for _ in range(60):
        rows, cols = rng.randint(1, 9), rng.randint(1, 9)
        m = rng.randint(0, 3)
        levels = rng.choice([2, 4, 16, 256])
        img = [[rng.randrange(levels) for _ in range(cols)] for _ in range(rows)]
        assert median_filter_2d(img, m, levels) == brute_2d(img, m)


def test_example() -> None:
    x = [2, 80, 6, 3, 1, 4, 0, 5]
    assert median_filter_1d(x, 1) == [2, 6, 6, 3, 3, 1, 4, 5]


def test_step_edge_preserved() -> None:
    for m in range(1, 5):
        for edge in range(1, 20):
            x = [0] * edge + [9] * (20 - edge)
            assert median_filter_1d(x, m) == x
    img = [[0] * 4 + [200] * 4 for _ in range(8)]
    assert median_filter_2d(img, 1) == img
    assert median_filter_2d(img, 2) == img


def test_impulses_removed() -> None:
    """A burst of at most m equal outliers inside a flat run is removed."""
    for m in range(1, 5):
        for width in range(1, m + 1):
            x = [3] * 30
            for i in range(12, 12 + width):
                x[i] = 250
            assert median_filter_1d(x, m) == [3] * 30
    img = [[10] * 7 for _ in range(7)]
    img[3][3] = 255
    img[0][6] = 0
    assert median_filter_2d(img, 1) == [[10] * 7 for _ in range(7)]


def test_monotone_signal_unchanged() -> None:
    rng = random.Random(10103)
    for _ in range(50):
        x = sorted(rng.randint(0, 100) for _ in range(rng.randint(1, 30)))
        assert median_filter_1d(x, rng.randint(0, 5)) == x


def test_not_linear() -> None:
    x, y = [0, 0, 1], [1, 0, 0]
    s = [a + b for a, b in zip(x, y)]
    mx, my, ms = median_filter_1d(x, 1), median_filter_1d(y, 1), median_filter_1d(s, 1)
    assert mx == [0, 0, 1] and my == [1, 0, 0] and ms == [1, 1, 1]
    assert ms != [a + b for a, b in zip(mx, my)]  # at the middle: med(1, 1, 1) = 1 but 0 + 0 = 0


def test_idempotent_after_root() -> None:
    """Repeated filtering stops changing: the result is a root signal."""
    rng = random.Random(10104)
    for _ in range(50):
        x = [rng.randint(0, 9) for _ in range(30)]
        y = x
        for _ in range(30):
            z = median_filter_1d(y, 1)
            if z == y:
                break
            y = z
        assert median_filter_1d(y, 1) == y
