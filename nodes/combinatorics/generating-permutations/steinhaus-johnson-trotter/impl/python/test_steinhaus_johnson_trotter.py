# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/steinhaus-johnson-trotter/. The authors are listed in prov/0D9QST.jsonl.

import itertools
import math
import random

from steinhaus_johnson_trotter import plain_changes, steinhaus_johnson_trotter


def run(n: int) -> list[tuple[int, ...]]:
    return [tuple(p) for p in steinhaus_johnson_trotter(list(range(1, n + 1)))]


def recursive_list(n: int) -> list[tuple[int, ...]]:
    if n <= 1:
        return [tuple(range(1, n + 1))]
    out: list[tuple[int, ...]] = []
    for t, p in enumerate(recursive_list(n - 1)):
        places = range(n - 1, -1, -1) if t % 2 == 0 else range(n)
        for i in places:
            out.append(p[:i] + (n,) + p[i:])
    return out


def inversions(p: tuple[int, ...]) -> int:
    return sum(1 for i in range(len(p)) for j in range(i + 1, len(p)) if p[i] > p[j])


def test_example() -> None:
    want = [
        "1234", "1243", "1423", "4123", "4132", "1432", "1342", "1324",
        "3124", "3142", "3412", "4312", "4321", "3421", "3241", "3214",
        "2314", "2341", "2431", "4231", "4213", "2413", "2143", "2134",
    ]
    assert run(4) == [tuple(int(c) for c in s) for s in want]
    assert run(3) == [(1, 2, 3), (1, 3, 2), (3, 1, 2), (3, 2, 1), (2, 3, 1), (2, 1, 3)]


def test_edges() -> None:
    assert run(0) == [()]
    assert run(1) == [(1,)]
    assert run(2) == [(1, 2), (2, 1)]
    assert list(plain_changes(0)) == []
    assert list(plain_changes(1)) == []
    assert list(plain_changes(2)) == [0]


def test_all_permutations_once() -> None:
    for n in range(0, 9):
        got = run(n)
        assert len(got) == math.factorial(n)
        assert set(got) == set(itertools.permutations(range(1, n + 1)))


def test_matches_recursive_definition() -> None:
    for n in range(0, 8):
        assert run(n) == recursive_list(n)


def test_adjacent_exchange_and_cycle() -> None:
    for n in range(2, 8):
        got = run(n)
        for p, q in zip(got + got[:1], got[1:] + got[:1]):
            diff = [i for i in range(n) if p[i] != q[i]]
            assert len(diff) == 2 and diff[1] == diff[0] + 1
            assert abs(inversions(p) - inversions(q)) == 1
        assert got[-1] == (2, 1) + tuple(range(3, n + 1))


def test_move_counts() -> None:
    for n in range(2, 8):
        got = run(n)
        moves = [0] * (n + 1)
        for p, q in zip(got, got[1:]):
            i = next(i for i in range(n) if p[i] != q[i])
            moves[max(p[i], p[i + 1])] += 1
        for m in range(2, n + 1):
            assert moves[m] == (m - 1) * math.factorial(m - 1)


def test_plain_changes_replay() -> None:
    for n in range(0, 8):
        a = list(range(1, n + 1))
        seen = [tuple(a)]
        for p in plain_changes(n):
            a[p], a[p + 1] = a[p + 1], a[p]
            seen.append(tuple(a))
        assert seen == run(n)


def test_random_items() -> None:
    rng = random.Random(20261109)
    for _ in range(30):
        n = rng.randint(0, 6)
        items = [rng.choice("abcdefgh") + str(i) for i in range(n)]
        got = [tuple(p) for p in steinhaus_johnson_trotter(items)]
        assert got[0] == tuple(items)
        assert sorted(got) == sorted(itertools.permutations(items))
        idx = run(n)
        assert got == [tuple(items[v - 1] for v in p) for p in idx]
