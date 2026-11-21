# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-degree-anonymization/. The authors are listed in prov/X8DF57.jsonl.

import itertools
import random
from collections import Counter

import pytest

from k_degree_anonymization import anonymize_degrees, k_degree_anonymize

# vertices a..g are 0..6
EDGES = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 5), (3, 4)]


def degrees(n: int, edges: list[tuple[int, int]]) -> list[int]:
    deg = [0] * n
    for u, v in edges:
        deg[u] += 1
        deg[v] += 1
    return deg


def is_k_anonymous(values: list[int], k: int) -> bool:
    return all(c >= k for c in Counter(values).values())


def test_example() -> None:
    assert degrees(7, EDGES) == [4, 3, 2, 2, 2, 1, 0]
    assert anonymize_degrees([4, 3, 2, 2, 2, 1, 0], 2) == ([4, 4, 2, 2, 2, 1, 1], 2)
    assert k_degree_anonymize(7, EDGES, 2) == [(1, 6)]


def test_edges() -> None:
    assert anonymize_degrees([], 3) == ([], 0)
    assert k_degree_anonymize(0, [], 2) == []
    assert anonymize_degrees([3, 1, 0], 3) == ([3, 3, 3], 5)
    assert anonymize_degrees([2, 2, 1, 1], 1) == ([2, 2, 1, 1], 0)
    with pytest.raises(ValueError):
        anonymize_degrees([1, 1], 3)
    # a star on 4 vertices with k = 4 must become complete
    star = [(0, 1), (0, 2), (0, 3)]
    added = k_degree_anonymize(4, star, 4)
    assert added is not None and sorted(added) == [(1, 2), (1, 3), (2, 3)]
    # one edge on 3 vertices, k = 2: the best sequence (1, 1, 1) has an odd sum, so the answer is UNKNOWN,
    # although adding two edges gives the triangle, which is 2-degree anonymous
    assert anonymize_degrees([1, 1, 0], 2) == ([1, 1, 1], 1)
    assert k_degree_anonymize(3, [(0, 1)], 2) is None


def set_partitions(n: int) -> list[list[int]]:
    out: list[list[int]] = [[]]
    for _ in range(n):
        out = [s + [b] for s in out for b in range((max(s) + 2) if s else 1)]
    return out


PARTITIONS = {n: set_partitions(n) for n in range(1, 8)}


def brute_da(d: list[int], k: int) -> int:
    """Least L1 raise to a k-anonymous vector: every group of equal final values goes to its maximum."""
    best = None
    for labels in PARTITIONS[len(d)]:
        groups: dict[int, list[int]] = {}
        for b, x in zip(labels, d):
            groups.setdefault(b, []).append(x)
        if any(len(g) < k for g in groups.values()):
            continue
        c = sum(max(g) * len(g) - sum(g) for g in groups.values())
        best = c if best is None or c < best else best
    assert best is not None
    return best


def test_dp_against_brute_force() -> None:
    rng = random.Random(21)
    for _ in range(500):
        n = rng.randint(1, 7)
        k = rng.randint(1, n)
        d = sorted((rng.randint(0, n - 1) for _ in range(n)), reverse=True)
        out, cost = anonymize_degrees(d, k)
        assert cost == brute_da(d, k)
        assert cost == sum(x - y for x, y in zip(out, d))
        assert all(x >= y for x, y in zip(out, d))
        assert is_k_anonymous(out, k)


def test_graph_against_brute_force() -> None:
    rng = random.Random(22)
    found = 0
    for _ in range(300):
        n = rng.randint(1, 5)
        k = rng.randint(1, n)
        pairs = list(itertools.combinations(range(n), 2))
        edges = [e for e in pairs if rng.random() < 0.4]
        missing = [e for e in pairs if e not in edges]
        least = None
        for r in range(len(missing) + 1):
            for extra in itertools.combinations(missing, r):
                if is_k_anonymous(degrees(n, edges + list(extra)), k):
                    least = r
                    break
            if least is not None:
                break
        assert least is not None
        _, cost = anonymize_degrees(sorted(degrees(n, edges), reverse=True), k)
        assert 2 * least >= cost
        added = k_degree_anonymize(n, edges, k)
        if added is not None:
            found += 1
            assert len(set(added)) == len(added)
            assert not set(added) & set(edges)
            assert all(u != v for u, v in added)
            assert is_k_anonymous(degrees(n, edges + added), k)
            assert 2 * len(added) == cost == 2 * least
    assert found > 200
