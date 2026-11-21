# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/samarati-algorithm/. The authors are listed in prov/FM4D27.jsonl.
import random
from itertools import product

from samarati_algorithm import samarati, suppressed_count

RACE = [
    {"asian": "asian", "black": "black", "white": "white"},
    {"asian": "person", "black": "person", "white": "person"},
]
ZIPS = ["94138", "94139", "94141", "94142"]
ZIP = [{z: z for z in ZIPS}, {z: z[:4] + "*" for z in ZIPS}, {z: z[:3] + "**" for z in ZIPS}]
TABLE = [
    ("asian", "94142"),
    ("asian", "94141"),
    ("asian", "94139"),
    ("asian", "94139"),
    ("asian", "94139"),
    ("black", "94138"),
    ("black", "94139"),
    ("white", "94139"),
    ("white", "94141"),
]


def test_page_example() -> None:
    h = [RACE, ZIP]
    assert suppressed_count(TABLE, h, (0, 0), 2) == 6
    assert suppressed_count(TABLE, h, (0, 1), 2) == 2
    assert suppressed_count(TABLE, h, (1, 0), 2) == 2
    assert suppressed_count(TABLE, h, (1, 1), 2) == 0
    assert samarati(TABLE, h, 2, 2) == (0, 1)
    assert suppressed_count(TABLE, h, (0, 2), 2) == 0
    assert samarati(TABLE, h, 2, 0) == (0, 2)
    assert samarati(TABLE, h, 2, 9) == (0, 0)


def test_edge_cases() -> None:
    h = [RACE, ZIP]
    assert samarati([], h, 3, 0) == (0, 0)
    assert samarati(TABLE[:1], h, 2, 0) is None
    assert samarati(TABLE[:1], h, 2, 1) == (0, 0)
    assert samarati(TABLE, h, 1, 0) == (0, 0)
    same = [("asian", "94139")] * 4
    assert samarati(same, h, 4, 0) == (0, 0)
    assert samarati(same, h, 5, 0) is None


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


def oracle(table, hierarchy, k, max_sup):
    heights = [len(x) - 1 for x in hierarchy]
    good = []
    for v in product(*(range(t + 1) for t in heights)):
        groups: dict = {}
        for row in table:
            key = tuple(hierarchy[a][v[a]][row[a]] for a in range(len(v)))
            groups[key] = groups.get(key, 0) + 1
        if sum(c for c in groups.values() if c < k) <= max_sup:
            good.append(v)
    if not good:
        return None
    best = min(sum(v) for v in good)
    return min(v for v in good if sum(v) == best)


def test_random_against_brute_force() -> None:
    rng = random.Random(20240601)
    for _ in range(600):
        d = rng.randint(1, 3)
        sizes = [rng.randint(1, 4) for _ in range(d)]
        hierarchy = [random_hierarchy(rng, r) for r in sizes]
        n = rng.randint(0, 12)
        table = [tuple(rng.randrange(r) for r in sizes) for _ in range(n)]
        k = rng.randint(1, 4)
        max_sup = rng.randint(0, 3)
        got = samarati(table, hierarchy, k, max_sup)
        want = oracle(table, hierarchy, k, max_sup)
        assert got == want
        if got is not None:
            for a in range(d):
                if got[a] > 0:
                    lower = got[:a] + (got[a] - 1,) + got[a + 1:]
                    assert suppressed_count(table, hierarchy, lower, k) > max_sup
