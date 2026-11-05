# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wagner-fischer-algorithm/. The authors are listed in prov/ZX8DFX.jsonl.

import random
from collections import deque

from wagner_fischer_algorithm import alignment, edit_distance, edit_table


def bfs_distance(x: str, y: str, alphabet: str) -> int:
    """Shortest number of unit edit operations from x to y, by breadth-first search."""
    limit = max(len(x), len(y)) + 1
    seen = {x: 0}
    queue = deque([x])
    while queue:
        s = queue.popleft()
        if s == y:
            return seen[s]
        nxt = []
        for i in range(len(s)):
            nxt.append(s[:i] + s[i + 1 :])
            for c in alphabet:
                if c != s[i]:
                    nxt.append(s[:i] + c + s[i + 1 :])
        if len(s) < limit:
            for i in range(len(s) + 1):
                for c in alphabet:
                    nxt.append(s[:i] + c + s[i:])
        for t in nxt:
            if t not in seen:
                seen[t] = seen[s] + 1
                queue.append(t)
    raise AssertionError("unreachable")


def check_alignment(x: str, y: str) -> None:
    cols = alignment(x, y)
    assert "".join(a for a, _ in cols) == x
    assert "".join(b for _, b in cols) == y
    assert all(a != "" or b != "" for a, b in cols)
    assert sum(a != b for a, b in cols) == edit_distance(x, y)


def test_example() -> None:
    d = edit_table("kitten", "sitting")
    assert d[6] == [6, 6, 5, 4, 3, 3, 2, 3]
    assert d[3] == [3, 3, 2, 1, 2, 3, 4, 5]
    assert edit_distance("kitten", "sitting") == 3
    assert alignment("kitten", "sitting") == [
        ("k", "s"), ("i", "i"), ("t", "t"), ("t", "t"), ("e", "i"), ("n", "n"), ("", "g"),
    ]


def test_edges() -> None:
    assert edit_distance("", "") == 0
    assert edit_distance("", "abc") == 3
    assert edit_distance("abc", "") == 3
    assert edit_distance("abc", "abc") == 0
    assert edit_distance("ab", "ba") == 2
    assert edit_distance("sunday", "saturday") == 3
    assert edit_distance("intention", "execution") == 5
    assert alignment("", "") == []
    for x, y in [("", "ab"), ("ab", ""), ("a", "b"), ("abc", "abc")]:
        check_alignment(x, y)


def test_random_against_bfs() -> None:
    rng = random.Random(1974)
    for alphabet in ("ab", "acgt"):
        for _ in range(300):
            top = 5 if alphabet == "ab" else 4
            x = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, top)))
            y = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, top)))
            d = edit_distance(x, y)
            assert d == bfs_distance(x, y, alphabet)
            assert d == edit_table(x, y)[len(x)][len(y)] == edit_distance(y, x)
            check_alignment(x, y)


def test_random_longer() -> None:
    rng = random.Random(7)
    for alphabet in ("ab", "acgt"):
        for _ in range(300):
            x = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 20)))
            y = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 20)))
            d = edit_distance(x, y)
            assert abs(len(x) - len(y)) <= d <= max(len(x), len(y))
            check_alignment(x, y)
            z = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 20)))
            assert edit_distance(x, z) <= d + edit_distance(y, z)
