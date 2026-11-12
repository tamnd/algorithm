# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ephemeron/. The authors are listed in prov/DGVSB7.jsonl.

import random

from ephemeron import mark_with_ephemerons, mark_with_weak_pairs


def closed(s: set[int], edges, eph, roots) -> bool:
    if not set(roots) <= s:
        return False
    for x in s:
        if any(y not in s for y in edges.get(x, [])):
            return False
        if x in eph and eph[x][0] in s and eph[x][1] not in s:
            return False
    return True


def least_closed_set(n: int, edges, eph, roots) -> set[int]:
    """Brute force: the intersection of all closed sets of objects."""
    out = set(range(n))
    for mask in range(1 << n):
        s = {i for i in range(n) if mask >> i & 1}
        if closed(s, edges, eph, roots):
            out &= s
    return out


def random_heap(rng: random.Random, n: int):
    edges = {x: [rng.randrange(n) for _ in range(rng.randrange(3))] for x in range(n)}
    eph = {}
    for e in rng.sample(range(n), rng.randrange(n // 2 + 1)):
        eph[e] = (rng.randrange(n), rng.randrange(n))
        edges[e] = []
    roots = rng.sample(range(n), rng.randrange(1, min(n, 2) + 1))
    return edges, eph, roots


def test_against_brute_force_fixpoint() -> None:
    rng = random.Random(7)
    for _ in range(400):
        n = rng.randrange(1, 10)
        edges, eph, roots = random_heap(rng, n)
        live, cleared = mark_with_ephemerons(edges, eph, roots)
        assert live == least_closed_set(n, edges, eph, roots)
        assert cleared == sorted(e for e in eph if e in live and eph[e][0] not in live)
        assert live <= mark_with_weak_pairs(edges, eph, roots)


def test_value_refers_to_key() -> None:
    # 0 root, 1 table, 2 entry, 3 key, 4 value; the value refers to the key
    edges = {0: [1], 1: [2], 2: [], 3: [], 4: [3]}
    eph = {2: (3, 4)}
    assert mark_with_weak_pairs(edges, eph, [0]) == {0, 1, 2, 3, 4}  # the leak
    live, cleared = mark_with_ephemerons(edges, eph, [0])
    assert live == {0, 1, 2} and cleared == [2]
    edges[0].append(3)  # now the key has another path from a root
    live, cleared = mark_with_ephemerons(edges, eph, [0])
    assert live == {0, 1, 2, 3, 4} and cleared == []


def test_chain_needs_fixpoint() -> None:
    # e1 = (k1, k2), e2 = (k2, v); marking k1 late must release both values
    edges = {0: [5, 6], 5: [], 6: [], 1: [], 2: [], 3: [], 4: [1]}
    eph = {5: (1, 2), 6: (2, 3)}
    live, _ = mark_with_ephemerons(edges, eph, [0])
    assert live == {0, 5, 6}
    edges[0].append(4)
    live, cleared = mark_with_ephemerons(edges, eph, [0])
    assert live == {0, 1, 2, 3, 4, 5, 6} and cleared == []
