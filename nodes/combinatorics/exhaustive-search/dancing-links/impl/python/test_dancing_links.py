# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dancing-links/. The authors are listed in prov/48VR35.jsonl.

import itertools
import random

import pytest

from dancing_links import DancingLinks, dancing_links_exact_covers

KNUTH = [["C", "E", "F"], ["A", "D", "G"], ["B", "C", "F"], ["A", "D"], ["B", "G"], ["D", "E", "G"]]


def brute_force(primary, options):
    out = []
    for r in range(len(options) + 1):
        for sub in itertools.combinations(range(len(options)), r):
            seen = [x for j in sub for x in options[j]]
            if len(seen) == len(set(seen)) and set(primary) <= set(seen):
                out.append(list(sub))
    return sorted(out)


def test_initial_structure() -> None:
    d = DancingLinks("ABCDEFG", KNUTH)
    assert d.active_items() == list("ABCDEFG")
    assert d.active_options("A") == [1, 3]
    assert d.active_options("D") == [1, 3, 5]
    assert [d.length[d.item(c)] for c in "ABCDEFG"] == [2, 2, 2, 3, 2, 2, 3]


def test_cover_and_uncover_example() -> None:
    d = DancingLinks("ABCDEFG", KNUTH)
    before = d.state()
    d.cover(d.item("A"))
    assert d.active_items() == list("BCDEFG")
    # Options 1 and 3 hold A, so they leave the columns of D and G.
    assert d.active_options("D") == [5]
    assert d.active_options("G") == [4, 5]
    assert d.length[d.item("D")] == 1
    d.uncover(d.item("A"))
    assert d.state() == before


def test_lifo_restores_every_state() -> None:
    rng = random.Random(3)
    for _ in range(200):
        n = rng.randrange(1, 7)
        items = list(range(n))
        opts = [rng.sample(items, rng.randrange(1, n + 1)) for _ in range(rng.randrange(0, 9))]
        d = DancingLinks(items, opts)
        states = [d.state()]
        covered = []
        for _ in range(rng.randrange(0, n + 1)):
            act = d.active_items()
            if not act:
                break
            i = d.item(rng.choice(act))
            d.cover(i)
            covered.append(i)
            states.append(d.state())
            # A covered item leaves the list, and no active column holds an
            # option that contains it.
            for name in d.active_items():
                for j in d.active_options(name):
                    assert d.names[i - 1] not in opts[j]
        while covered:
            assert d.state() == states.pop()
            d.uncover(covered.pop())
        assert d.state() == states.pop()


def test_solve_knuth_example() -> None:
    assert dancing_links_exact_covers("ABCDEFG", KNUTH) == [[0, 3, 4]]


def test_solve_against_brute_force() -> None:
    rng = random.Random(11)
    found = 0
    for _ in range(500):
        n = rng.randrange(0, 7)
        items = list(range(n))
        opts = []
        if n:
            opts = [rng.sample(items, rng.randrange(1, n + 1)) for _ in range(rng.randrange(0, 12))]
        got = dancing_links_exact_covers(items, opts)
        assert sorted(got) == brute_force(items, opts)
        found += bool(got)
    assert found > 100


def test_secondary_items_and_queens() -> None:
    def queens(n: int) -> int:
        prim = [("r", i) for i in range(n)] + [("c", i) for i in range(n)]
        sec = [("a", i) for i in range(2 * n - 1)] + [("b", i) for i in range(2 * n - 1)]
        opts = [[("r", r), ("c", c), ("a", r + c), ("b", r - c + n - 1)] for r in range(n) for c in range(n)]
        return sum(1 for _ in DancingLinks(prim, opts, sec).solve())

    assert [queens(n) for n in range(1, 9)] == [1, 0, 0, 2, 10, 4, 40, 92]


def test_solve_leaves_structure_unchanged() -> None:
    d = DancingLinks("ABCDEFG", KNUTH)
    before = d.state()
    assert len(list(d.solve())) == 1
    assert d.state() == before


def test_edges() -> None:
    assert dancing_links_exact_covers([], []) == [[]]
    assert dancing_links_exact_covers(["a"], []) == []
    assert dancing_links_exact_covers(["a"], [["a"], ["a"]]) == [[0], [1]]
    with pytest.raises(ValueError):
        DancingLinks(["a"], [["a", "a"]])
    with pytest.raises(ValueError):
        DancingLinks(["a"], [["s"]], ["s"])
    with pytest.raises(ValueError):
        DancingLinks(["a", "a"], [])
