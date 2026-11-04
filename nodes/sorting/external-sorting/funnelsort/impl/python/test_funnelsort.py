# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/funnelsort/. The authors are listed in prov/VCKGXK.jsonl.

import random

from funnelsort import Node, build_funnel, fill, funnelsort


class Rec:
    def __init__(self, key: int, pos: int) -> None:
        self.key, self.pos = key, pos

    def __lt__(self, other: "Rec") -> bool:
        return self.key < other.key


def inner_nodes(v: Node) -> list[Node]:
    if v.left is None:
        return []
    return [v] + inner_nodes(v.left) + inner_nodes(v.right)


def test_example() -> None:
    f = [21, 4, 17, 9, 26, 1, 12, 23, 6, 15, 19, 3, 25, 8, 11, 14, 2, 20, 27, 5, 10, 16, 24, 7, 13, 18, 22]
    funnelsort(f)
    assert f == list(range(1, 28))


def test_edges() -> None:
    for f in ([], [1], [2, 1], [3, 3, 3], list(range(9, 0, -1))):
        want = sorted(f)
        funnelsort(f)
        assert f == want


def test_buffer_sizes() -> None:
    for k in (2, 3, 4, 5, 8, 9, 16, 30, 64):
        root = build_funnel([[i] for i in range(k)])
        nodes = inner_nodes(root)
        assert all(v.cap >= 1 for v in nodes[1:])
        root.cap = k
        fill(root)
        assert list(root.buf) == list(range(k))
    root = build_funnel([[i] for i in range(16)])
    # k = 16 is a 4-funnel on top of four 4-funnels; the middle buffers hold 16^(3/2) = 64 items
    assert root.left.left.cap == 64 and root.left.left.left.cap == 8


def test_stable() -> None:
    rng = random.Random(7)
    for _ in range(100):
        n = rng.randint(0, 400)
        f = [Rec(rng.randint(0, 5), i) for i in range(n)]
        funnelsort(f)
        assert [(r.key, r.pos) for r in f] == sorted((r.key, r.pos) for r in f)


def test_random_against_sorted() -> None:
    rng = random.Random(1999)
    for _ in range(600):
        n = rng.randint(0, 700)
        f = [rng.randint(-50, 50) for _ in range(n)]
        want = sorted(f)
        funnelsort(f)
        assert f == want
