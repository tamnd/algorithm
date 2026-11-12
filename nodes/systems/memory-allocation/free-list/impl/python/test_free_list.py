# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/free-list/. The authors are listed in prov/G56SEJ.jsonl.

import random

import pytest

from free_list import MIN_BLOCK, NIL, Heap, check, first_fit


class Model:
    """Naive model: the block list and the free list as Python lists."""

    def __init__(self, H: int, order: str) -> None:
        self.b = [[0, H, 0]]
        self.order = order
        self.fl = [0]

    def link(self, a: int) -> None:
        if self.order == "lifo":
            self.fl.insert(0, a)
        elif self.order == "fifo":
            self.fl.append(a)
        else:
            self.fl = sorted(self.fl + [a])

    def malloc(self, n: int) -> int | None:
        need = max(MIN_BLOCK, n + 2)
        size = {a: s for a, s, _ in self.b}
        fits = [a for a in self.fl if size[a] >= need]
        if not fits:
            return None
        a = fits[0]
        i = next(j for j, x in enumerate(self.b) if x[0] == a)
        s = self.b[i][1]
        if s - need >= MIN_BLOCK:
            self.b[i:i + 1] = [[a, need, 1], [a + need, s - need, 0]]
            self.fl[self.fl.index(a)] = a + need
        else:
            self.b[i][2] = 1
            self.fl.remove(a)
        return a + 1

    def free(self, p: int) -> None:
        i = next(k for k, x in enumerate(self.b) if x[0] == p - 1)
        self.b[i][2] = 0
        if i + 1 < len(self.b) and not self.b[i + 1][2]:
            self.fl.remove(self.b[i + 1][0])
            self.b[i][1] += self.b.pop(i + 1)[1]
        if i > 0 and not self.b[i - 1][2]:
            self.fl.remove(self.b[i - 1][0])
            self.b[i - 1][1] += self.b.pop(i)[1]
            i -= 1
        self.link(self.b[i][0])


def backward(h: Heap) -> list[int]:
    out, a = [], h.tail
    while a != NIL:
        out.append(a)
        a = h.prv(a)
    return out[::-1]


def test_example_orders() -> None:
    got = {}
    for order in ("addr", "lifo", "fifo"):
        h = Heap(64, order)
        ps = [h.malloc(n, first_fit) for n in (10, 2, 6, 2, 14, 2)]
        out = [h.free_list()]
        for p in ps[0::2]:
            h.free(p)
            out.append(h.free_list())
        p = h.malloc(6, first_fit)
        out.append((p, h.free_list()))
        h.free(p)
        out.append(h.free_list())
        check(h)
        got[order] = out
    assert got == {
        "addr": [[48], [0, 48], [0, 16, 48], [0, 16, 28, 48], (1, [8, 16, 28, 48]), [0, 16, 28, 48]],
        "lifo": [[48], [0, 48], [16, 0, 48], [28, 16, 0, 48], (29, [36, 16, 0, 48]), [28, 16, 0, 48]],
        "fifo": [[48], [48, 0], [48, 0, 16], [48, 0, 16, 28], (49, [56, 0, 16, 28]), [0, 16, 28, 48]],
    }


def test_links_live_inside_the_blocks() -> None:
    h = Heap(64)
    ps = [h.malloc(n, first_fit) for n in (10, 2, 6, 2, 14, 2)]
    for p in ps[0::2]:
        h.free(p)
    assert (h.head, h.tail) == (0, 48)
    assert [(h.nxt(a), h.prv(a)) for a in (0, 16, 28, 48)] == [(16, NIL), (28, 0), (48, 16), (NIL, 28)]


def test_empty_list() -> None:
    h = Heap(4)
    assert h.malloc(2, first_fit) == 1
    assert h.free_list() == [] and h.head == h.tail == NIL
    h.free(1)
    assert h.free_list() == [0] and h.head == h.tail == 0


@pytest.mark.parametrize("order", ["addr", "lifo", "fifo"])
@pytest.mark.parametrize("seed", range(12))
def test_against_model(order: str, seed: int) -> None:
    rng = random.Random(seed)
    H = rng.randint(4, 400)
    h, m = Heap(H, order), Model(H, order)
    live: list[int] = []
    for _ in range(300):
        if live and rng.random() < 0.45:
            p = live.pop(rng.randrange(len(live)))
            h.free(p)
            m.free(p)
        else:
            n = rng.randint(1, 40)
            p = h.malloc(n, first_fit)
            assert p == m.malloc(n)
            if p is not None:
                live.append(p)
        assert check(h) == [tuple(x) for x in m.b]
        assert h.free_list() == backward(h) == m.fl


def test_lifo_link_is_constant_time() -> None:
    """Address-ordered links walk the list; LIFO links never do."""
    steps = {}
    for order in ("addr", "lifo"):
        rng = random.Random(4)
        h, live = Heap(1 << 12, order), []
        for _ in range(2000):
            if live and rng.random() < 0.5:
                h.free(live.pop(rng.randrange(len(live))))
            else:
                p = h.malloc(rng.randint(1, 30), first_fit_free)
                if p is not None:
                    live.append(p)
        steps[order] = h.probes
    assert steps["lifo"] == 0 and steps["addr"] > 0


def first_fit_free(h: Heap, need: int) -> int:
    """First fit that does not count its probes, so h.probes counts link steps only."""
    a = h.head
    while a != NIL and h.size(a) < need:
        a = h.nxt(a)
    return a
