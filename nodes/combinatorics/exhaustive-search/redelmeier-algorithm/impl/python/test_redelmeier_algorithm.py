# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/redelmeier-algorithm/. The authors are listed in prov/R79V1G.jsonl.

import pytest

from redelmeier_algorithm import fixed_polyominoes, redelmeier_counts

# OEIS A001168, fixed polyominoes with n cells, n = 1, 2, ...
A001168 = [1, 2, 6, 19, 63, 216, 760, 2725, 9910, 36446]


def normalize(cells):
    mx = min(x for x, _ in cells)
    my = min(y for _, y in cells)
    return frozenset((x - mx, y - my) for x, y in cells)


def brute_force(n):
    """Fixed polyominoes by growth from all smaller ones, with a set to remove repeats."""
    level = {frozenset([(0, 0)])}
    out = [level]
    for _ in range(n - 1):
        nxt = set()
        for p in level:
            for x, y in p:
                for d in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if d not in p:
                        nxt.add(normalize(p | {d}))
        level = nxt
        out.append(level)
    return out


def test_counts_match_oeis() -> None:
    assert redelmeier_counts(10) == A001168


def test_against_brute_force() -> None:
    levels = brute_force(7)
    for k in range(1, 8):
        got = list(fixed_polyominoes(k))
        assert len(got) == len(set(got))
        assert {normalize(p) for p in got} == levels[k - 1]


def test_shape_of_output() -> None:
    for k in range(1, 7):
        for p in fixed_polyominoes(k):
            cells = set(p)
            assert len(cells) == k
            # The first cell in the order (y, x) is the origin.
            assert min(cells, key=lambda c: (c[1], c[0])) == (0, 0)
            # The cells are connected.
            seen, stack = {(0, 0)}, [(0, 0)]
            while stack:
                x, y = stack.pop()
                for d in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if d in cells and d not in seen:
                        seen.add(d)
                        stack.append(d)
            assert seen == cells


def test_edges() -> None:
    assert redelmeier_counts(0) == []
    assert redelmeier_counts(1) == [1]
    assert list(fixed_polyominoes(1)) == [((0, 0),)]
    assert sorted(fixed_polyominoes(2)) == [((0, 0), (0, 1)), ((0, 0), (1, 0))]
    with pytest.raises(ValueError):
        redelmeier_counts(-1)
    with pytest.raises(ValueError):
        list(fixed_polyominoes(0))
