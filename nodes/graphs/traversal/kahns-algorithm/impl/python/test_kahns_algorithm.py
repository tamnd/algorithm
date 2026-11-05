# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kahns-algorithm/. The authors are listed in prov/JVCQ4E.jsonl.

import random

from kahns_algorithm import kahns_algorithm


def is_topological(adj: list[list[int]], order: list[int]) -> bool:
    n = len(adj)
    if sorted(order) != list(range(n)):
        return False
    pos = [0] * n
    for i, v in enumerate(order):
        pos[v] = i
    return all(pos[u] < pos[v] for u in range(n) for v in adj[u])


def has_cycle(adj: list[list[int]]) -> bool:
    """Independent oracle: some vertex reaches itself by a nonempty path."""
    n = len(adj)
    for s in range(n):
        seen = [False] * n
        todo = list(adj[s])
        while todo:
            u = todo.pop()
            if u == s:
                return True
            if not seen[u]:
                seen[u] = True
                todo.extend(adj[u])
    return False


def test_example() -> None:
    adj = [[1, 3, 2], [2], [], [2, 4], [], [4, 6], []]
    assert kahns_algorithm(adj) == [0, 5, 1, 3, 6, 2, 4]


def test_example_with_cycle() -> None:
    adj = [[1, 3, 2], [2], [0], [2, 4], [], [4, 6], []]
    assert kahns_algorithm(adj) is None


def test_small_cases() -> None:
    assert kahns_algorithm([]) == []
    assert kahns_algorithm([[]]) == [0]
    assert kahns_algorithm([[0]]) is None
    assert kahns_algorithm([[], [], []]) == [0, 1, 2]
    assert kahns_algorithm([[1], [0]]) is None
    assert kahns_algorithm([[1, 1], []]) == [0, 1]
    assert kahns_algorithm([[1, 2], [3], [3], []]) == [0, 1, 2, 3]


def test_long_path() -> None:
    n = 100000
    adj = [[i + 1] for i in range(n - 1)] + [[]]
    assert kahns_algorithm(adj) == list(range(n))
    adj[-1] = [0]
    assert kahns_algorithm(adj) is None


def test_random_against_oracle() -> None:
    rng = random.Random(6271)
    for trial in range(600):
        n = rng.randint(0, 9)
        p = rng.random()
        if trial % 2 == 0:
            perm = list(range(n))
            rng.shuffle(perm)
            adj = [[] for _ in range(n)]
            for i in range(n):
                for j in range(i + 1, n):
                    if rng.random() < p:
                        adj[perm[i]].append(perm[j])
                        if rng.random() < 0.1:
                            adj[perm[i]].append(perm[j])
        else:
            adj = [[v for v in range(n) if rng.random() < p / 2] for _ in range(n)]
        for lst in adj:
            rng.shuffle(lst)
        got = kahns_algorithm(adj)
        if has_cycle(adj):
            assert got is None
        else:
            assert got is not None and is_topological(adj, got)
