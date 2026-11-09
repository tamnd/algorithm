# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wright-richmond-odlyzko-mckay/. The authors are listed in prov/MPQVRK.jsonl.

import random

import pytest

from wright_richmond_odlyzko_mckay import free_trees

# OEIS A000055, t_0 .. t_18.
A000055 = [1, 1, 1, 1, 2, 3, 6, 11, 23, 47, 106, 235, 551, 1301, 3159, 7741, 19320, 48629, 123867]


def rooted_counts(m: int) -> list[int]:
    """a_0 .. a_m, the numbers of rooted trees, by Otter's recurrence."""
    a = [0, 1]
    for n in range(1, m):
        s = 0
        for k in range(1, n + 1):
            s += sum(d * a[d] for d in range(1, k + 1) if k % d == 0) * a[n - k + 1]
        a.append(s // n)
    return a


def free_count(n: int, a: list[int]) -> int:
    """Otter's formula: t_n = a_n - (sum_{i+j=n} a_i a_j - [n even] a_{n/2}) / 2."""
    if n == 0:
        return 1
    pairs = sum(a[i] * a[n - i] for i in range(1, n))
    if n % 2 == 0:
        pairs -= a[n // 2]
    return a[n] - pairs // 2


def canonical(seq: tuple[int, ...]) -> tuple[int, ...]:
    """Sort the child subtrees of every node in decreasing order."""

    def build(i: int) -> tuple[tuple[int, ...], int]:
        d = seq[i]
        j = i + 1
        kids = []
        while j < len(seq) and seq[j] > d:
            block, j = build(j)
            kids.append(block)
        kids.sort(reverse=True)
        return (d,) + tuple(x for b in kids for x in b), j

    return build(0)[0]


def rooted_version(adj: list[list[int]]) -> tuple[int, ...]:
    """Oracle: root the free tree at its center, with the rule for two centers."""
    n = len(adj)
    if n == 0:
        return ()

    def code(r: int, banned: int) -> tuple[int, ...]:
        seq = []
        stack = [(r, -1, 0)]
        while stack:
            v, parent, d = stack.pop()
            seq.append(d)
            for w in reversed(adj[v]):
                if w != parent and w != banned:
                    stack.append((w, v, d + 1))
        return canonical(tuple(seq))

    deg = [len(x) for x in adj]
    alive = set(range(n))
    leaves = [v for v in alive if deg[v] <= 1]
    while len(alive) > 2:
        new = []
        for v in leaves:
            alive.discard(v)
            for w in adj[v]:
                if w in alive:
                    deg[w] -= 1
                    if deg[w] == 1:
                        new.append(w)
        leaves = new
    centers = sorted(alive)
    if len(centers) == 1:
        return code(centers[0], -1)
    u, v = centers
    tu, tv = code(u, v), code(v, u)
    root = u if (len(tv), tv) < (len(tu), tu) else v
    return code(root, -1)


def from_levels(seq: tuple[int, ...]) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in seq]
    stack: list[int] = []
    for i, x in enumerate(seq):
        del stack[x:]
        if stack:
            adj[i].append(stack[-1])
            adj[stack[-1]].append(i)
        stack.append(i)
    return adj


def from_pruefer(code: list[int], n: int) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    degree = [1] * n
    for x in code:
        degree[x] += 1
    for x in code:
        leaf = min(v for v in range(n) if degree[v] == 1)
        adj[leaf].append(x)
        adj[x].append(leaf)
        degree[leaf] -= 1
        degree[x] -= 1
    u, v = [w for w in range(n) if degree[w] == 1]
    adj[u].append(v)
    adj[v].append(u)
    return adj


def all_rooted(n: int) -> set[tuple[int, ...]]:
    """All rooted trees with n nodes, from all C_{n-1} level sequences."""
    if n == 0:
        return set()
    out = set()

    def extend(seq: list[int]) -> None:
        if len(seq) == n:
            out.add(canonical(tuple(seq)))
            return
        for x in range(1, seq[-1] + 2):
            seq.append(x)
            extend(seq)
            seq.pop()

    extend([0])
    return out


def test_small() -> None:
    assert list(free_trees(0)) == []
    assert list(free_trees(1)) == [(0,)]
    assert list(free_trees(2)) == [(0, 1)]
    assert list(free_trees(3)) == [(0, 1, 1)]
    assert list(free_trees(4)) == [(0, 1, 2, 1), (0, 1, 1, 1)]
    with pytest.raises(ValueError):
        list(free_trees(-1))


def test_example_n7() -> None:
    got = ["".join(map(str, t)) for t in free_trees(7)]
    assert got == [
        "0123123",
        "0123122",
        "0123121",
        "0122212",
        "0122122",
        "0122121",
        "0122111",
        "0121212",
        "0121211",
        "0121111",
        "0111111",
    ]


def test_against_oracle() -> None:
    for n in range(0, 11):
        expected = sorted({rooted_version(from_levels(t)) for t in all_rooted(n)}, reverse=True)
        if n == 0:
            expected = []
        assert list(free_trees(n)) == expected


def test_counts() -> None:
    a = rooted_counts(18)
    for n in range(0, 19):
        assert free_count(n, a) == A000055[n]
    # The generator lists no tree for n = 0, although t_0 = 1 by convention.
    for n in range(1, 17):
        assert sum(1 for _ in free_trees(n)) == A000055[n]


def test_order_and_validity() -> None:
    for n in range(3, 14):
        prev = None
        for t in free_trees(n):
            assert rooted_version(from_levels(t)) == t
            assert prev is None or t < prev
            prev = t


def test_random_trees_are_listed() -> None:
    rng = random.Random(11)
    n = 12
    listed = set(free_trees(n))
    assert len(listed) == A000055[n]
    for _ in range(300):
        code = [rng.randrange(n) for _ in range(n - 2)]
        assert rooted_version(from_pruefer(code, n)) in listed
