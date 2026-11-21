# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incognito/. The authors are listed in prov/KC05HR.jsonl.
import random
from itertools import product

from incognito import incognito

RACES = ["asian", "black", "white"]
STATUS = ["single", "married", "divorced", "widow"]
HIER = [
    [{x: x for x in RACES}, {x: "person" for x in RACES}],
    [{"F": "F", "M": "M"}, {"F": "*", "M": "*"}],
    [
        {x: x for x in STATUS},
        {x: ("never_married" if x == "single" else "been_married") for x in STATUS},
        {x: "*" for x in STATUS},
    ],
]
ROWS = [
    ("asian", "F", "divorced"),
    ("asian", "F", "divorced"),
    ("asian", "F", "married"),
    ("asian", "M", "married"),
    ("asian", "M", "married"),
    ("black", "F", "single"),
    ("black", "F", "single"),
    ("white", "F", "single"),
    ("white", "F", "widow"),
]


def test_page_example() -> None:
    full, minimal = incognito(ROWS, HIER, 2)
    assert minimal == [(0, 0, 2), (1, 0, 1)]
    assert full == [(0, 0, 2), (0, 1, 2), (1, 0, 1), (1, 0, 2), (1, 1, 1), (1, 1, 2)]


def test_edge_cases() -> None:
    all_vectors = sorted(product(range(2), range(2), range(3)))
    assert incognito([], HIER, 3) == (all_vectors, [(0, 0, 0)])
    assert incognito(ROWS, HIER, 1) == (all_vectors, [(0, 0, 0)])
    assert incognito(ROWS[:1], HIER, 2) == ([], [])
    assert incognito(ROWS, HIER, 9) == ([(1, 1, 2)], [(1, 1, 2)])
    one = [[{0: 0, 1: 1, 2: 2}, {0: 0, 1: 0, 2: 1}, {0: 0, 1: 0, 2: 0}]]
    assert incognito([(0,), (1,), (2,), (2,)], one, 2) == ([(1,), (2,)], [(1,)])


def random_hierarchy(rng: random.Random, r: int) -> list[dict[int, int]]:
    """A chain of coarser and coarser partitions of range(r), ending in one block."""
    block = list(range(r))
    levels = [dict(enumerate(block))]
    while len(set(block)) > 1:
        labels = sorted(set(block))
        rng.shuffle(labels)
        cut = rng.randint(2, len(labels))
        merged = set(labels[:cut])
        new_label = min(merged)
        block = [new_label if b in merged else b for b in block]
        levels.append(dict(enumerate(block)))
    return levels


def brute_force(rows, hier, k):
    tops = [len(x) - 1 for x in hier]
    good = []
    for v in product(*(range(t + 1) for t in tops)):
        groups: dict = {}
        for row in rows:
            key = tuple(hier[a][v[a]][row[a]] for a in range(len(v)))
            groups[key] = groups.get(key, 0) + 1
        if all(c >= k for c in groups.values()):
            good.append(v)
    minimal = []
    for v in good:
        below = [w for w in good if w != v and all(w[a] <= v[a] for a in range(len(v)))]
        if not below:
            minimal.append(v)
    return sorted(good), sorted(minimal)


def test_random_against_brute_force() -> None:
    rng = random.Random(2005)
    for _ in range(500):
        d = rng.randint(1, 4)
        sizes = [rng.randint(1, 4) for _ in range(d)]
        hier = [random_hierarchy(rng, r) for r in sizes]
        n = rng.randint(0, 14)
        rows = [tuple(rng.randrange(r) for r in sizes) for _ in range(n)]
        k = rng.randint(1, 4)
        assert incognito(rows, hier, k) == brute_force(rows, hier, k)
