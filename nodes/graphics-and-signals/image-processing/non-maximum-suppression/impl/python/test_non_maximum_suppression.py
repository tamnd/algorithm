# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/non-maximum-suppression/. The authors are listed in prov/9SMADY.jsonl.

import math
import random

from non_maximum_suppression import STEPS, non_maximum_suppression, sector


def reference(gx, gy):
    """Direct per-pixel rule: round the atan2 angle to a multiple of 45 degrees, then compare."""
    h, w = len(gx), len(gx[0])
    m = [[gx[y][x] ** 2 + gy[y][x] ** 2 for x in range(w)] for y in range(h)]
    out = [[0] * w for _ in range(h)]
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            if m[y][x] == 0:
                continue
            angle = math.degrees(math.atan2(gy[y][x], gx[y][x])) % 180.0
            k = round(angle / 45.0) % 4
            dx, dy = STEPS[k]
            if m[y][x] > m[y - dy][x - dx] and m[y][x] >= m[y + dy][x + dx]:
                out[y][x] = m[y][x]
    return out


def sobel(image):
    h, w = len(image), len(image[0])

    def at(x, y):
        return image[min(max(y, 0), h - 1)][min(max(x, 0), w - 1)]

    gx = [[(at(x + 1, y - 1) + 2 * at(x + 1, y) + at(x + 1, y + 1)) - (at(x - 1, y - 1) + 2 * at(x - 1, y) + at(x - 1, y + 1))
           for x in range(w)] for y in range(h)]
    gy = [[(at(x - 1, y + 1) + 2 * at(x, y + 1) + at(x + 1, y + 1)) - (at(x - 1, y - 1) + 2 * at(x, y - 1) + at(x + 1, y - 1))
           for x in range(w)] for y in range(h)]
    return gx, gy


def test_sector_table() -> None:
    assert sector(5, 0) == 0 and sector(-5, 0) == 0
    assert sector(0, 3) == 2 and sector(0, -3) == 2
    assert sector(5, 2) == 0  # 21.8 degrees
    assert sector(5, 3) == 1  # 31.0 degrees
    assert sector(2, 5) == 2  # 68.2 degrees
    assert sector(3, 5) == 1  # 59.0 degrees
    assert sector(-4, 4) == 3 and sector(4, -4) == 3 and sector(-4, -4) == 1


def test_sector_against_atan2() -> None:
    for gx in range(-40, 41):
        for gy in range(-40, 41):
            if gx == 0 and gy == 0:
                continue
            angle = math.degrees(math.atan2(gy, gx)) % 180.0
            assert sector(gx, gy) == round(angle / 45.0) % 4


def test_random_gradients_against_reference() -> None:
    rng = random.Random(31)
    for _ in range(300):
        h, w = rng.randint(1, 7), rng.randint(1, 7)
        gx = [[rng.randint(-6, 6) for _ in range(w)] for _ in range(h)]
        gy = [[rng.randint(-6, 6) for _ in range(w)] for _ in range(h)]
        assert non_maximum_suppression(gx, gy) == reference(gx, gy)


def test_sobel_of_random_images_against_reference() -> None:
    rng = random.Random(37)
    for _ in range(60):
        image = [[rng.choice((0, 0, 50, 200)) for _ in range(9)] for _ in range(8)]
        gx, gy = sobel(image)
        assert non_maximum_suppression(gx, gy) == reference(gx, gy)


def test_step_edge_single_response() -> None:
    image = [[0] * 4 + [100] * 4 for _ in range(6)]
    gx, gy = sobel(image)
    out = non_maximum_suppression(gx, gy)
    for y in range(1, 5):
        assert [x for x in range(8) if out[y][x]] == [3]


def test_plateaus() -> None:
    gy = [[0] * 7 for _ in range(3)]
    two = [[0] * 7, [1, 2, 5, 5, 2, 1, 0], [0] * 7]
    assert [x for x in range(7) if non_maximum_suppression(two, gy)[1][x]] == [2]
    three = [[0] * 7, [1, 2, 5, 5, 5, 1, 0], [0] * 7]
    assert [x for x in range(7) if non_maximum_suppression(three, gy)[1][x]] == [2]


def test_no_two_kept_neighbors_in_the_same_sector() -> None:
    rng = random.Random(41)
    for _ in range(200):
        gx = [[rng.randint(-5, 5) for _ in range(6)] for _ in range(6)]
        gy = [[rng.randint(-5, 5) for _ in range(6)] for _ in range(6)]
        out = non_maximum_suppression(gx, gy)
        for y in range(6):
            for x in range(6):
                if out[y][x]:
                    s = sector(gx[y][x], gy[y][x])
                    dx, dy = STEPS[s]
                    xx, yy = x + dx, y + dy
                    if 0 <= xx < 6 and 0 <= yy < 6 and sector(gx[yy][xx], gy[yy][xx]) == s:
                        assert out[yy][xx] == 0


def test_edges() -> None:
    assert non_maximum_suppression([], []) == []
    assert non_maximum_suppression([[3, 4]], [[0, 0]]) == [[0, 0]]
