# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lipton-tarjan-separator/. The authors are listed in prov/YCV3MB.jsonl.

import itertools
import random

import pytest

from lipton_tarjan_separator import lipton_tarjan_separator

Rotation = dict[int, list[int]]


def check(rot: Rotation) -> tuple[list[int], list[int], list[int]]:
    """Run the algorithm and verify the output independently."""
    a, b, s = lipton_tarjan_separator(rot)
    n = len(rot)
    assert sorted(a + b + s) == sorted(rot)
    side_b = set(b)
    for u in a:
        for w in rot[u]:
            assert w not in side_b
    assert 3 * len(a) <= 2 * n and 3 * len(b) <= 2 * n
    assert len(s) * len(s) <= 8 * n
    return a, b, s


def fan(n: int) -> Rotation:
    rot: Rotation = {0: list(range(n - 1, 0, -1))}
    for i in range(1, n):
        rot[i] = [j for j in (i + 1, i - 1) if 1 <= j < n] + [0]
    return rot


def grid(k: int, first: int = 0) -> Rotation:
    """The k x k grid; neighbours counterclockwise: right, up, left, down."""
    rot: Rotation = {}
    cells = [(i, j) for i in range(k) for j in range(k)]
    cells.sort(key=lambda c: c != divmod(first, k))
    for i, j in cells:
        around = []
        for di, dj in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            if 0 <= i + di < k and 0 <= j + dj < k:
                around.append((i + di) * k + j + dj)
        rot[i * k + j] = around
    return rot


def stacked(rng: random.Random, n: int) -> Rotation:
    """A random stacked triangulation with n >= 3 vertices."""
    rot: Rotation = {0: [1, 2], 1: [2, 0], 2: [0, 1]}
    faces = [(0, 1, 2), (0, 2, 1)]
    for v in range(3, n):
        i = rng.randrange(len(faces))
        x, y, z = faces[i]
        faces[i] = (x, y, v)
        faces += [(y, z, v), (z, x, v)]
        for p, q in ((x, y), (y, z), (z, x)):
            rot[p].insert(rot[p].index(q) + 1, v)
        rot[v] = [x, y, z]
    return rot


def random_planar(rng: random.Random, n: int) -> Rotation:
    rot = stacked(rng, n) if n >= 3 else {v: [] for v in range(n)}
    if n == 2 and rng.random() < 0.5:
        rot = {0: [1], 1: [0]}
    for _ in range(rng.randint(0, 2 * n)):
        v = rng.randrange(n)
        if rot[v]:
            w = rng.choice(rot[v])
            rot[v].remove(w)
            rot[w].remove(v)
    perm = list(range(n))
    rng.shuffle(perm)
    return {perm[v]: [perm[w] for w in rot[v]] for v in rng.sample(range(n), n)}


def least_separator(rot: Rotation) -> int:
    """Brute force: the least size of a separator with sides of at most 2n/3."""
    vs = list(rot)
    n = len(vs)
    for size in range(n + 1):
        for s in itertools.combinations(vs, size):
            seen = set(s)
            parts = []
            for v in vs:
                if v in seen:
                    continue
                seen.add(v)
                stack, count = [v], 0
                while stack:
                    u = stack.pop()
                    count += 1
                    for w in rot[u]:
                        if w not in seen:
                            seen.add(w)
                            stack.append(w)
                parts.append(count)
            sums = {0}
            for c in parts:
                sums |= {x + c for x in sums}
            total = sum(parts)
            if any(3 * x <= 2 * n and 3 * (total - x) <= 2 * n for x in sums):
                return size
    return n


def test_page_example() -> None:
    rot = fan(11)
    assert rot[0] == [10, 9, 8, 7, 6, 5, 4, 3, 2, 1] and rot[5] == [6, 4, 0] and rot[1] == [2, 0]
    assert lipton_tarjan_separator(rot) == ([4, 5, 6, 7, 8, 9], [1, 2], [0, 3, 10])


def test_small_cases() -> None:
    assert lipton_tarjan_separator({}) == ([], [], [])
    assert lipton_tarjan_separator({7: []}) == ([], [], [7])
    assert lipton_tarjan_separator({0: [1], 1: [0]}) == ([1], [], [0])
    k4 = {0: [1, 2, 3], 1: [2, 0, 3], 2: [0, 1, 3], 3: [0, 2, 1]}
    a, b, s = check(k4)
    assert s == [1, 2, 3] and a == [0]  # the level of the neighbours of 0
    star = {0: [1, 2, 3, 4, 5], 1: [0], 2: [0], 3: [0], 4: [0], 5: [0]}
    assert check(star)[2] == [1, 2, 3, 4, 5]  # the median level, not the least separator
    path = {i: [j for j in (i - 1, i + 1) if 0 <= j < 9] for i in range(9)}
    check(path)
    isolated = {v: [] for v in range(5)}
    assert check(isolated)[2] == []


def test_grid_from_center() -> None:
    a, b, s = check(grid(3, first=4))
    assert s == [1, 3, 5, 7] and a == [0, 2, 4] and b == [6, 8]
    for k in range(2, 30):
        check(grid(k))


def test_k5_and_k33_are_rejected() -> None:
    k5 = {v: [w for w in range(5) if w != v] for v in range(5)}
    with pytest.raises(ValueError):
        lipton_tarjan_separator(k5)
    k33 = {v: ([3, 4, 5] if v < 3 else [0, 1, 2]) for v in range(6)}
    with pytest.raises(ValueError):
        lipton_tarjan_separator(k33)
    toroidal_k4 = {0: [1, 2, 3], 1: [0, 2, 3], 2: [0, 1, 3], 3: [0, 1, 2]}
    with pytest.raises(ValueError):
        lipton_tarjan_separator(toroidal_k4)


def test_fans_use_the_cycle_step() -> None:
    for n in range(11, 200, 7):
        a, b, s = check(fan(n))
        assert 0 in s and len(s) == 3


def test_random_against_oracle() -> None:
    rng = random.Random(2024)
    for trial in range(600):
        n = rng.randint(0, 9) if trial < 200 else rng.randint(9, 160)
        rot = random_planar(rng, n)
        a, b, s = check(rot)
        if n <= 9:
            assert least_separator(rot) <= len(s)


def test_disjoint_unions() -> None:
    rng = random.Random(7)
    for _ in range(100):
        parts = [stacked(rng, rng.randint(3, 40)) for _ in range(rng.randint(1, 4))]
        rot: Rotation = {}
        for part in parts:
            base = len(rot)
            for v, around in part.items():
                rot[base + v] = [base + w for w in around]
        check(rot)


def test_large_inputs() -> None:
    rng = random.Random(1)
    a, b, s = check(stacked(rng, 20000))
    assert len(s) <= 400
    check(fan(5000))
    check(grid(100))
