# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linked-list-merge-sort/. The authors are listed in prov/NEN2CA.jsonl.

import itertools
import random

from linked_list_merge_sort import Node, linked_list_merge_sort, sort_list


def test_example() -> None:
    a = [5, 1, 4, 2, 8, 0, 3]
    assert linked_list_merge_sort(a) == 14
    assert a == [0, 1, 2, 3, 4, 5, 8]


def test_nodes_are_relinked_not_copied() -> None:
    nodes = [Node(k) for k in (3, 1, 2)]
    nodes[0].next, nodes[1].next = nodes[1], nodes[2]
    head, _ = sort_list(nodes[0])
    assert head is nodes[1] and head.next is nodes[2] and head.next.next is nodes[0]
    assert nodes[0].next is None


def test_edges() -> None:
    for a in ([], [1], [2, 1], [1, 2], [1, 1, 1], [3, 2, 1], [2**63 - 1, -(2**63)]):
        b = list(a)
        linked_list_merge_sort(b)
        assert b == sorted(a)


def test_all_permutations_and_comparison_bound() -> None:
    for n in range(1, 8):
        for p in itertools.permutations(range(n)):
            b = list(p)
            c = linked_list_merge_sort(b)
            assert b == list(range(n))
            assert c <= n * (n - 1).bit_length()


def test_stable() -> None:
    class Key:
        def __init__(self, k: int, tag: int) -> None:
            self.k, self.tag = k, tag

        def __lt__(self, other: "Key") -> bool:
            return self.k < other.k

    rng = random.Random(11)
    a = [Key(rng.randint(0, 5), i) for i in range(200)]
    linked_list_merge_sort(a)
    assert all((a[i].k, a[i].tag) < (a[i + 1].k, a[i + 1].tag) for i in range(199))


def test_random_against_sorted() -> None:
    rng = random.Random(1945)
    for _ in range(600):
        a = [rng.randint(-30, 30) for _ in range(rng.randint(0, 80))]
        b = list(a)
        linked_list_merge_sort(b)
        assert b == sorted(a)
