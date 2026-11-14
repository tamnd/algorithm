# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/karnaugh-map/. The authors are listed in prov/KAW0FH.jsonl.

import itertools
import random

from karnaugh_map import cell, cube_of, grid, groups, read_cover, rectangles


def cube_cells(c: str) -> frozenset[int]:
    n = len(c)
    return frozenset(m for m in range(2 ** n) if all(ch == "-" or int(ch) == (m >> (n - 1 - i)) & 1 for i, ch in enumerate(c)))


def all_cubes(n: int) -> list[str]:
    return ["".join(t) for t in itertools.product("01-", repeat=n)]


def brute_primes(n: int, on: set[int], dc: set[int]) -> set[frozenset[int]]:
    imps = [cube_cells(c) for c in all_cubes(n) if cube_cells(c) <= on | dc]
    return {g for g in imps if not any(g < h for h in imps) and g & on}


def brute_min_cost(n: int, on: set[int], dc: set[int]) -> tuple[int, int]:
    primes = sorted(brute_primes(n, on, dc), key=sorted)
    lits = [sum(ch != "-" for ch in cube_of(n, g)) for g in primes]
    for k in range(len(primes) + 1):
        costs = [sum(lits[j] for j in s) for s in itertools.combinations(range(len(primes)), k)
                 if on <= set().union(*(primes[j] for j in s))]
        if costs:
            return (k, min(costs))
    raise AssertionError("no cover")


def cost(cover: list[str]) -> tuple[int, int]:
    return len(cover), sum(ch != "-" for c in cover for ch in c)


def test_layout_is_gray() -> None:
    for n in (2, 3, 4):
        rows, cols = (2, 2) if n == 2 else (2, 4) if n == 3 else (4, 4)
        seen = {cell(n, r, c) for r in range(rows) for c in range(cols)}
        assert seen == set(range(2 ** n))
        for r in range(rows):
            for c in range(cols):
                for r2, c2 in (((r + 1) % rows, c), (r, (c + 1) % cols)):
                    if (r2, c2) != (r, c):
                        assert bin(cell(n, r, c) ^ cell(n, r2, c2)).count("1") == 1


def test_grid_text() -> None:
    assert grid(4, {0, 2, 8, 10}, {5}) == ["1001", "0x00", "0000", "1001"]


def test_rectangles_are_the_cubes() -> None:
    for n in (2, 3, 4):
        rects = rectangles(n)
        assert len(set(rects)) == 3 ** n
        assert {cube_of(n, g) for g in rects} == set(all_cubes(n))
        for g in rects:
            assert cube_cells(cube_of(n, g)) == g


def test_corners_are_one_group() -> None:
    # The four corners of a 4-variable map form x2' x4'.
    assert read_cover(4, {0, 2, 8, 10}) == ["-0-0"]


def test_groups_are_the_primes() -> None:
    rng = random.Random(31)
    for n in (2, 3, 4):
        for _ in range(150):
            on = {m for m in range(2 ** n) if rng.random() < 0.45}
            dc = {m for m in range(2 ** n) if m not in on and rng.random() < 0.2}
            assert set(groups(n, on, dc)) == brute_primes(n, on, dc)


def test_reading_is_a_valid_cover() -> None:
    rng = random.Random(32)
    for n in (2, 3, 4):
        for _ in range(150):
            on = {m for m in range(2 ** n) if rng.random() < 0.45}
            dc = {m for m in range(2 ** n) if m not in on and rng.random() < 0.2}
            cover = read_cover(n, on, dc)
            got = set().union(*(cube_cells(c) for c in cover)) if cover else set()
            assert on <= got <= on | dc
            assert cost(cover) >= brute_min_cost(n, on, dc)


def test_reading_is_minimum_on_all_three_variable_functions() -> None:
    # On three variables the reading is minimum for every function; on four it can fail.
    for bits in range(2 ** 8):
        on = {m for m in range(8) if bits >> m & 1}
        assert cost(read_cover(3, on)) == brute_min_cost(3, on, set())
