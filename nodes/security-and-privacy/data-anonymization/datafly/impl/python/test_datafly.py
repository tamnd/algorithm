# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/datafly/. The authors are listed in prov/JK6NEV.jsonl.
import random

from datafly import datafly

ROWS = [
    ("asian", "64/04/12", "F", "94142"),
    ("asian", "64/09/13", "F", "94141"),
    ("asian", "64/04/15", "F", "94139"),
    ("asian", "63/03/13", "M", "94139"),
    ("asian", "63/03/18", "M", "94139"),
    ("black", "64/09/27", "F", "94138"),
    ("black", "64/09/27", "F", "94139"),
    ("white", "64/09/27", "F", "94139"),
    ("white", "64/09/27", "F", "94141"),
]
RACES = ["asian", "black", "white"]
DOBS = sorted({r[1] for r in ROWS})
ZIPS = sorted({r[3] for r in ROWS})
HIER = [
    [{x: x for x in RACES}, {x: "person" for x in RACES}],
    [{x: x for x in DOBS}, {x: x[:5] for x in DOBS}, {x: x[:2] for x in DOBS}, {x: "*" for x in DOBS}],
    [{"F": "F", "M": "M"}, {"F": "*", "M": "*"}],
    [{z: z for z in ZIPS}, {z: z[:4] + "*" for z in ZIPS}, {z: z[:3] + "**" for z in ZIPS}, {z: "*" for z in ZIPS}],
]


def test_page_example() -> None:
    assert datafly(ROWS, HIER, 2) == ((1, 1, 0, 1), [0, 2])
    assert datafly(ROWS, HIER, 3) == ((1, 2, 0, 1), [3, 4])


def test_not_minimal() -> None:
    hier = [
        [{i: i for i in range(4)}, {i: i // 2 for i in range(4)}, {i: 0 for i in range(4)}],
        [{i: i for i in range(3)}, {i: 0 for i in range(3)}],
    ]
    rows = [(3, 0), (2, 2), (1, 0), (2, 1), (0, 0), (0, 0)]
    assert datafly(rows, hier, 2) == ((1, 1), [])
    # The vector (0, 1) is strictly lower and leaves only 2 = k rows to suppress.
    assert violators(rows, hier, (0, 1), 2) == [0, 2]


def test_edge_cases() -> None:
    assert datafly([], HIER, 2) == ((0, 0, 0, 0), [])
    assert datafly(ROWS[:1], HIER, 2) == ((0, 0, 0, 0), [0])
    assert datafly(ROWS, HIER, 1) == ((0, 0, 0, 0), [])
    same = [ROWS[0]] * 5
    assert datafly(same, HIER, 5) == ((0, 0, 0, 0), [])
    assert datafly(same, HIER, 6) == ((0, 0, 0, 0), [0, 1, 2, 3, 4])
    assert datafly(ROWS, HIER, 8) == ((1, 3, 1, 2), [])
    # With n <= k the stop test holds at once, and every row is suppressed.
    assert datafly(ROWS, HIER, 9) == ((0, 0, 0, 0), list(range(9)))


def violators(rows, hier, v, k):
    keys = [tuple(hier[a][v[a]][r[a]] for a in range(len(v))) for r in rows]
    return [i for i, key in enumerate(keys) if keys.count(key) < k]


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


def oracle(rows, hier, k):
    """Datafly from its definition, with the stop test and the choice written out again."""
    d = len(hier)
    v = [0] * d
    while len(violators(rows, hier, v, k)) > k:
        keys = [tuple(hier[a][v[a]][r[a]] for a in range(d)) for r in rows]
        best, best_count = 0, -1
        for a in range(d):
            count = len(set(key[a] for key in keys))
            if count > best_count:
                best, best_count = a, count
        v[best] += 1
    return tuple(v), violators(rows, hier, v, k)


def test_random_against_definition() -> None:
    rng = random.Random(1997)
    for _ in range(800):
        d = rng.randint(1, 4)
        sizes = [rng.randint(1, 5) for _ in range(d)]
        hier = [random_hierarchy(rng, r) for r in sizes]
        n = rng.randint(0, 20)
        rows = [tuple(rng.randrange(r) for r in sizes) for _ in range(n)]
        k = rng.randint(1, 5)
        v, s = datafly(rows, hier, k)
        assert (v, s) == oracle(rows, hier, k)
        assert len(s) <= k
        assert all(0 <= v[a] < len(hier[a]) for a in range(d))
        kept = [r for i, r in enumerate(rows) if i not in set(s)]
        keys = [tuple(hier[a][v[a]][r[a]] for a in range(d)) for r in kept]
        assert all(keys.count(key) >= k for key in keys)
