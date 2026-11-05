# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/topological-sort/. The authors are listed in prov/KDXVF9.jsonl.

import random

from topological_sort import topological_sort


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


def reverse_postorder(adj: list[list[int]]) -> list[int]:
    """The textbook recursive DFS, used as the oracle for the exact order."""
    n = len(adj)
    seen = [False] * n
    out: list[int] = []

    def visit(u: int) -> None:
        seen[u] = True
        for v in adj[u]:
            if not seen[v]:
                visit(v)
        out.append(u)

    for u in range(n):
        if not seen[u]:
            visit(u)
    return out[::-1]


def test_example() -> None:
    adj = [[1, 3, 2], [2], [], [2, 4], [], [4, 6], []]
    assert topological_sort(adj) == [5, 6, 0, 3, 4, 1, 2]


def test_example_with_cycle() -> None:
    adj = [[1, 3, 2], [2], [0], [2, 4], [], [4, 6], []]
    assert topological_sort(adj) is None


def test_small_cases() -> None:
    assert topological_sort([]) == []
    assert topological_sort([[]]) == [0]
    assert topological_sort([[0]]) is None
    assert topological_sort([[], [], []]) == [2, 1, 0]
    assert topological_sort([[1], [0]]) is None
    diamond = [[1, 2], [3], [3], []]
    assert topological_sort(diamond) == [0, 2, 1, 3]
    assert topological_sort([[1], [], [1]]) == [2, 0, 1]


def test_long_path() -> None:
    n = 100000
    adj = [[i + 1] for i in range(n - 1)] + [[]]
    assert topological_sort(adj) == list(range(n))
    adj[-1] = [0]
    assert topological_sort(adj) is None


def test_random_against_oracles() -> None:
    rng = random.Random(5150)
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
        else:
            adj = [[v for v in range(n) if rng.random() < p / 2] for _ in range(n)]
        for lst in adj:
            rng.shuffle(lst)
        got = topological_sort(adj)
        if has_cycle(adj):
            assert got is None
        else:
            assert got is not None and is_topological(adj, got)
            assert got == reverse_postorder(adj)
