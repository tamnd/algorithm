# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/heaps-algorithm/. The authors are listed in prov/AEJSBV.jsonl.

import itertools
import math

from heaps_algorithm import heap_permutations, heaps_algorithm


def recursive_list(items: list[int]) -> list[tuple[int, ...]]:
    out: list[tuple[int, ...]] = []
    heaps_algorithm(list(items), lambda a: out.append(tuple(a)))
    return out


def sign(p: tuple[int, ...]) -> int:
    inv = sum(1 for i in range(len(p)) for j in range(i + 1, len(p)) if p[i] > p[j])
    return -1 if inv % 2 else 1


def test_example() -> None:
    got = recursive_list([1, 2, 3, 4])
    assert got[:12] == [
        (1, 2, 3, 4), (2, 1, 3, 4), (3, 1, 2, 4), (1, 3, 2, 4),
        (2, 3, 1, 4), (3, 2, 1, 4), (4, 2, 1, 3), (2, 4, 1, 3),
        (1, 4, 2, 3), (4, 1, 2, 3), (2, 1, 4, 3), (1, 2, 4, 3),
    ]
    assert got[-1] == (2, 3, 4, 1)


def test_edges() -> None:
    assert recursive_list([]) == [()]
    assert recursive_list([5]) == [(5,)]
    assert [tuple(p) for p in heap_permutations([])] == [()]
    assert [tuple(p) for p in heap_permutations([5])] == [(5,)]
    assert recursive_list([1, 2]) == [(1, 2), (2, 1)]


def test_all_permutations_once() -> None:
    for n in range(0, 8):
        got = recursive_list(list(range(n)))
        assert len(got) == math.factorial(n)
        assert set(got) == set(itertools.permutations(range(n)))


def test_one_transposition_per_step() -> None:
    for n in range(2, 8):
        got = recursive_list(list(range(n)))
        for p, q in zip(got, got[1:]):
            diff = [i for i in range(n) if p[i] != q[i]]
            assert len(diff) == 2
            i, j = diff
            assert p[i] == q[j] and p[j] == q[i]
            assert sign(p) == -sign(q)


def test_iterative_matches_recursive() -> None:
    for n in range(0, 8):
        it = [tuple(p) for p in heap_permutations(list(range(n)))]
        assert it == recursive_list(list(range(n)))


def test_last_permutation() -> None:
    for n in range(1, 9):
        first = tuple(range(n))
        last = recursive_list(list(first))[-1]
        diff = sum(1 for i in range(n) if first[i] != last[i])
        if n % 2 == 1 or n == 2:
            want = list(first)
            want[0], want[n - 1] = want[n - 1], want[0]
            assert last == tuple(want)
        else:
            assert diff == n


def test_wrong_parity_repeats() -> None:
    a = [1, 2, 3]
    out: list[tuple[int, ...]] = []

    def wrong(k: int) -> None:
        if k <= 1:
            out.append(tuple(a))
            return
        wrong(k - 1)
        for i in range(k - 1):
            if k % 2 == 1:
                a[i], a[k - 1] = a[k - 1], a[i]
            else:
                a[0], a[k - 1] = a[k - 1], a[0]
            wrong(k - 1)

    wrong(3)
    assert len(out) == 6 and len(set(out)) == 4
