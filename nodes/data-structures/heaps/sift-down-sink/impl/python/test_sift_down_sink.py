# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sift-down-sink/. The authors are listed in prov/RCFB8N.jsonl.

import random

import pytest

from sift_down_sink import del_max, heapsort, sink


def is_max_heap(pq: list[int]) -> bool:
    n = len(pq) - 1
    return all(not pq[k // 2] < pq[k] for k in range(2, n + 1))


def counting(a: list[int]) -> tuple[list[int], object, object]:
    calls = [0]

    def less(i: int, j: int) -> bool:
        calls[0] += 1
        return a[i - 1] < a[j - 1]

    def exch(i: int, j: int) -> None:
        a[i - 1], a[j - 1] = a[j - 1], a[i - 1]

    return calls, less, exch


def test_example_construction() -> None:
    a = [5, 1, 9, 3, 7, 6, 2, 8, 4]
    calls, less, exch = counting(a)
    for k in range(len(a) // 2, 0, -1):
        sink(less, exch, k, len(a))  # type: ignore[arg-type]
    assert a == [9, 8, 6, 4, 7, 5, 2, 3, 1]
    assert calls[0] == 12


def test_example_heapsort() -> None:
    a = [5, 1, 9, 3, 7, 6, 2, 8, 4]
    heapsort(a)
    assert a == [1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_del_max() -> None:
    pq = [None, 9, 8, 6, 4, 7, 5, 2, 3, 1]
    assert del_max(pq) == 9  # type: ignore[arg-type]
    assert pq[1:] == [8, 7, 6, 4, 1, 5, 2, 3]
    assert is_max_heap(pq)  # type: ignore[arg-type]


def test_edges() -> None:
    with pytest.raises(IndexError):
        del_max([None])  # type: ignore[list-item]
    pq = [None, 4]
    assert del_max(pq) == 4 and pq == [None]  # type: ignore[arg-type]
    for a in ([], [1], [2, 1], [1, 1, 1], [3, 2, 1], [1, 2, 3]):
        b = list(a)
        heapsort(b)
        assert b == sorted(a)


def test_random_against_sorted() -> None:
    rng = random.Random(2024)
    for _ in range(600):
        a = [rng.randint(-40, 40) for _ in range(rng.randint(0, 50))]
        b = list(a)
        heapsort(b)
        assert b == sorted(a)


def test_random_del_max() -> None:
    rng = random.Random(5)
    for _ in range(300):
        items = [rng.randint(0, 30) for _ in range(rng.randint(1, 40))]
        a = list(items)
        calls, less, exch = counting(a)
        for k in range(len(a) // 2, 0, -1):
            sink(less, exch, k, len(a))  # type: ignore[arg-type]
        assert calls[0] < 2 * len(a)
        pq = [None] + a
        out = []
        while len(pq) > 1:
            out.append(del_max(pq))  # type: ignore[arg-type]
            assert is_max_heap(pq)  # type: ignore[arg-type]
        assert out == sorted(items, reverse=True)
