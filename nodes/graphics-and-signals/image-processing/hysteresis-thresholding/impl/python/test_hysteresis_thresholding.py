# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hysteresis-thresholding/. The authors are listed in prov/97HN4Z.jsonl.

import random
from collections import deque

import pytest

from hysteresis_thresholding import hysteresis_threshold


def reference_bfs(strength, low, high):
    """Brute force: one separate breadth first search from each strong pixel, no shared state."""
    h, w = len(strength), len(strength[0])
    edge = [[False] * w for _ in range(h)]
    for sy in range(h):
        for sx in range(w):
            if strength[sy][sx] < high:
                continue
            seen = {(sx, sy)}
            queue = deque([(sx, sy)])
            while queue:
                x, y = queue.popleft()
                edge[y][x] = True
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        xx, yy = x + dx, y + dy
                        if (0 <= xx < w and 0 <= yy < h and (xx, yy) not in seen
                                and strength[yy][xx] >= low):
                            seen.add((xx, yy))
                            queue.append((xx, yy))
    return edge


def reference_labels(strength, low, high):
    """Brute force: label the components of the candidate set by repeated minimum label
    propagation until nothing changes, then keep the components that hold a strong pixel."""
    h, w = len(strength), len(strength[0])
    label = [[y * w + x if strength[y][x] >= low else -1 for x in range(w)] for y in range(h)]
    changed = True
    while changed:
        changed = False
        for y in range(h):
            for x in range(w):
                if label[y][x] < 0:
                    continue
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        xx, yy = x + dx, y + dy
                        if 0 <= xx < w and 0 <= yy < h and 0 <= label[yy][xx] < label[y][x]:
                            label[y][x] = label[yy][xx]
                            changed = True
    good = {label[y][x] for y in range(h) for x in range(w) if strength[y][x] >= high}
    return [[label[y][x] >= 0 and label[y][x] in good for x in range(w)] for y in range(h)]


def test_example() -> None:
    s = [
        [0, 3, 0, 0, 0, 0],
        [0, 0, 4, 9, 0, 0],
        [0, 0, 0, 0, 5, 0],
        [4, 0, 0, 0, 0, 4],
        [5, 0, 3, 0, 0, 0],
    ]
    got = hysteresis_threshold(s, 4, 8)
    want = {(2, 1), (3, 1), (4, 2), (5, 3)}
    assert {(x, y) for y in range(5) for x in range(6) if got[y][x]} == want


def test_against_brute_force() -> None:
    rng = random.Random(43)
    for _ in range(300):
        h, w = rng.randint(1, 9), rng.randint(1, 9)
        s = [[rng.choice((0, 0, 0, 2, 4, 6, 9)) for _ in range(w)] for _ in range(h)]
        low, high = sorted((rng.randint(1, 9), rng.randint(1, 9)))
        got = hysteresis_threshold(s, low, high)
        assert got == reference_bfs(s, low, high)
        assert got == reference_labels(s, low, high)


def test_bounds_between_single_thresholds() -> None:
    rng = random.Random(47)
    for _ in range(100):
        s = [[rng.random() for _ in range(8)] for _ in range(8)]
        got = hysteresis_threshold(s, 0.4, 0.8)
        for y in range(8):
            for x in range(8):
                if s[y][x] >= 0.8:
                    assert got[y][x]
                if got[y][x]:
                    assert s[y][x] >= 0.4


def test_equal_thresholds_is_plain_threshold() -> None:
    s = [[1, 5, 2], [7, 3, 9]]
    assert hysteresis_threshold(s, 5, 5) == [[False, True, False], [True, False, True]]


def test_diagonal_connection_and_edges() -> None:
    s = [[9, 0, 0], [0, 5, 0], [0, 0, 5]]
    assert hysteresis_threshold(s, 4, 8) == [[True, False, False], [False, True, False], [False, False, True]]
    assert hysteresis_threshold([], 1, 2) == []
    with pytest.raises(ValueError):
        hysteresis_threshold([[1]], 3, 2)
