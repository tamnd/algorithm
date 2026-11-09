# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/algorithm-x/. The authors are listed in prov/0R5E65.jsonl.

import itertools
import random

import pytest

from algorithm_x import algorithm_x, count_exact_covers, first_exact_cover


def brute_force(primary, options, secondary=()):
    """All exact covers, as sorted tuples of option indices, by trying every subset."""
    out = set()
    m = len(options)
    for r in range(m + 1):
        for sub in itertools.combinations(range(m), r):
            seen = []
            for j in sub:
                seen.extend(options[j])
            if len(seen) != len(set(seen)):
                continue
            if set(primary) <= set(seen):
                out.add(sub)
    return out


def test_knuth_example() -> None:
    opts = [["C", "E", "F"], ["A", "D", "G"], ["B", "C", "F"], ["A", "D"], ["B", "G"], ["D", "E", "G"]]
    sols = list(algorithm_x("ABCDEFG", opts))
    assert sols == [[3, 0, 4]]
    assert first_exact_cover("ABCDEFG", opts) == [0, 3, 4]


def test_edges() -> None:
    # No primary item: the empty selection is the only cover.
    assert list(algorithm_x([], [])) == [[]]
    assert list(algorithm_x([], [], secondary=["s"])) == [[]]
    # An item with no option: no cover.
    assert list(algorithm_x(["a"], [])) == []
    assert first_exact_cover(["a"], []) is None
    # Two equal options give two covers.
    assert sorted(map(sorted, algorithm_x(["a"], [["a"], ["a"]]))) == [[0], [1]]
    with pytest.raises(ValueError):
        list(algorithm_x(["a"], [["a", "a"]]))
    with pytest.raises(ValueError):
        list(algorithm_x(["a"], [["b"]]))
    with pytest.raises(ValueError):
        list(algorithm_x(["a", "a"], [["a"]]))
    with pytest.raises(ValueError):
        list(algorithm_x(["a"], [["s"]], secondary=["s"]))


def test_against_brute_force() -> None:
    rng = random.Random(7)
    nonempty = 0
    for _ in range(600):
        n = rng.randrange(0, 7)
        s = rng.randrange(0, 3)
        prim = list(range(n))
        sec = [f"s{i}" for i in range(s)]
        items = prim + sec
        m = rng.randrange(0, 13)
        opts = []
        for _ in range(m):
            if not prim:
                break
            k = rng.randrange(0, len(items))
            first = rng.choice(prim)
            rest = [x for x in items if x != first]
            opts.append([first] + rng.sample(rest, min(k, len(rest))))
        got = [tuple(sorted(c)) for c in algorithm_x(prim, opts, sec)]
        assert len(got) == len(set(got))
        assert set(got) == brute_force(prim, opts, sec)
        nonempty += bool(got)
    assert nonempty > 100


def queens(n: int) -> int:
    prim = [("r", i) for i in range(n)] + [("c", i) for i in range(n)]
    sec = [("a", i) for i in range(2 * n - 1)] + [("b", i) for i in range(2 * n - 1)]
    opts = [[("r", r), ("c", c), ("a", r + c), ("b", r - c + n - 1)] for r in range(n) for c in range(n)]
    return count_exact_covers(prim, opts, sec)


def test_queens_with_secondary_items() -> None:
    assert [queens(n) for n in range(1, 9)] == [1, 0, 0, 2, 10, 4, 40, 92]


def test_langford_pairs() -> None:
    def langford(n: int) -> int:
        prim = [("v", i) for i in range(1, n + 1)] + [("p", j) for j in range(1, 2 * n + 1)]
        opts = [
            [("v", i), ("p", j), ("p", j + i + 1)]
            for i in range(1, n + 1)
            for j in range(1, 2 * n + 1)
            if j + i + 1 <= 2 * n
        ]
        return count_exact_covers(prim, opts)

    # Each Langford pairing and its reverse: 2 * (0, 0, 1, 1, 0, 0, 26, 150).
    assert [langford(n) for n in range(1, 9)] == [0, 0, 2, 2, 0, 0, 52, 300]


def test_sudoku() -> None:
    puzzle = (
        "53..7...."
        "6..195..."
        ".98....6."
        "8...6...3"
        "4..8.3..1"
        "7...2...6"
        ".6....28."
        "...419..5"
        "....8..79"
    )
    prim = [(t, a, b) for t in "pRCB" for a in range(9) for b in range(9)]
    opts, meaning = [], []
    for r in range(9):
        for c in range(9):
            ch = puzzle[9 * r + c]
            digits = range(9) if ch == "." else [int(ch) - 1]
            for d in digits:
                box = 3 * (r // 3) + c // 3
                opts.append([("p", r, c), ("R", r, d), ("C", c, d), ("B", box, d)])
                meaning.append((r, c, d))
    sols = list(algorithm_x(prim, opts))
    assert len(sols) == 1
    grid = [[0] * 9 for _ in range(9)]
    for j in sols[0]:
        r, c, d = meaning[j]
        grid[r][c] = d + 1
    assert grid[0] == [5, 3, 4, 6, 7, 8, 9, 1, 2]
    for i in range(9):
        assert sorted(grid[i]) == list(range(1, 10))
        assert sorted(grid[r][i] for r in range(9)) == list(range(1, 10))


def test_branching_item_has_fewest_options() -> None:
    # Item "b" has one option, so the first choice must be that option.
    opts = [["a"], ["a", "c"], ["b", "c"], ["c"]]
    sols = list(algorithm_x(["a", "b", "c"], opts))
    assert sols == [[2, 0]]
