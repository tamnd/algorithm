# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reverse-linked-list/. The authors are listed in prov/X89XHB.jsonl.

import random

from reverse_linked_list import Node, from_iterable, reverse, to_list


def nodes_of(head: Node[int] | None) -> list[Node[int]]:
    out = []
    while head is not None:
        out.append(head)
        head = head.next
    return out


def test_example() -> None:
    head = from_iterable([1, 2, 3, 4, 5])
    assert to_list(reverse(head)) == [5, 4, 3, 2, 1]


def test_edges() -> None:
    assert reverse(None) is None
    one = Node(7)
    assert reverse(one) is one and one.next is None
    two = from_iterable([1, 2])
    r = reverse(two)
    assert to_list(r) == [2, 1]
    assert two is not None and two.next is None  # the old head is now the tail
    assert to_list(reverse(from_iterable([3, 3, 3]))) == [3, 3, 3]


def test_in_place_and_twice() -> None:
    head = from_iterable(range(10))
    before = nodes_of(head)
    r = reverse(head)
    after = nodes_of(r)
    assert after == before[::-1]  # the same node objects, no new node
    assert all(a is b for a, b in zip(after, before[::-1]))
    assert to_list(reverse(r)) == list(range(10))


def test_long_list_no_recursion() -> None:
    n = 200_000
    assert to_list(reverse(from_iterable(range(n)))) == list(range(n - 1, -1, -1))


def test_random_against_slicing() -> None:
    rng = random.Random(1027)
    for _ in range(600):
        a = [rng.randint(-10**18, 10**18) for _ in range(rng.randint(0, 40))]
        assert to_list(reverse(from_iterable(a))) == a[::-1]
