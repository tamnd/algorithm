# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boundary-tags/. The authors are listed in prov/QY9E0Z.jsonl.

import random

import pytest

from boundary_tags import NIL, Heap, ScanHeap, blocks, check, first_fit


def run(h: Heap, ops):
    """Apply ops: ("m", n) mallocs n words, ("f", r) frees live block r mod count."""
    live = []
    for op, x in ops:
        if op == "m":
            p = h.malloc(x, first_fit)
            if p is not None:
                live.append(p)
        elif live:
            h.free(live.pop(x % len(live)))
        yield


def random_ops(rng: random.Random, steps: int, top: int):
    return [
        ("f", rng.randrange(1 << 30)) if rng.random() < 0.5 else ("m", rng.randint(1, top))
        for _ in range(steps)
    ]


def test_footer_names_the_block_below() -> None:
    h = Heap(64)
    ps = [h.malloc(n, first_fit) for n in (10, 2, 6, 2, 14, 2)]
    for p in ps[0::2]:
        h.free(p)
    bl = check(h)
    for (a, s, u), (b, _, _) in zip(bl, bl[1:]):
        assert h.mem[b - 1] == 2 * s + u and b - (h.mem[b - 1] >> 1) == a
    h.reads = 0
    h.free(ps[3])  # block (24, 4): reads its header, the header at 28 and the footer at 23
    assert h.reads == 3
    assert [(a, h.size(a)) for a in h.free_list()] == [(0, 12), (16, 28), (48, 16)]


def test_scan_reads_more_on_the_same_example() -> None:
    g = ScanHeap(64)
    ps = [g.malloc(n, first_fit) for n in (10, 2, 6, 2, 14, 2)]
    for p in ps[0::2]:
        g.free(p)
    g.reads = 0
    g.free(ps[3])  # header, upper header, then headers at 0, 12 and 16 to reach 16
    assert g.reads == 5
    assert [(a, g.size(a)) for a in g.free_list()] == [(0, 12), (16, 28), (48, 16)]


def naive_merge(bl):
    out = []
    for a, s, u in bl:
        if out and not u and not out[-1][2]:
            out[-1] = (out[-1][0], out[-1][1] + s, 0)
        else:
            out.append((a, s, u))
    return out


@pytest.mark.parametrize("order", ["addr", "lifo", "fifo"])
@pytest.mark.parametrize("seed", range(10))
def test_same_heap_as_address_scan(order: str, seed: int) -> None:
    rng = random.Random(seed)
    H = rng.randint(4, 600)
    ops = random_ops(rng, 300, 40)
    h, g = Heap(H, order), ScanHeap(H, order)
    for _ in zip(run(h, ops), run(g, ops)):
        assert h.mem == g.mem and (h.head, h.tail) == (g.head, g.tail)
        bl = check(h)
        assert bl == naive_merge(bl)


@pytest.mark.parametrize("seed", range(10))
def test_matches_naive_model(seed: int) -> None:
    """A model heap that frees by flipping a bit and merges by an address scan."""
    rng = random.Random(100 + seed)
    H = rng.randint(4, 600)
    h, model, live = Heap(H), [(0, H, 0)], []
    for _ in range(300):
        if live and rng.random() < 0.5:
            p = live.pop(rng.randrange(len(live)))
            h.free(p)
            model = naive_merge([(a, s, 0 if a == p - 1 else u) for a, s, u in model])
        else:
            n = rng.randint(1, 40)
            need = max(4, n + 2)
            got = None
            for i, (a, s, u) in enumerate(model):
                if not u and s >= need:
                    split = [(a, need, 1), (a + need, s - need, 0)] if s - need >= 4 else [(a, s, 1)]
                    model[i : i + 1] = split
                    got = a + 1
                    break
            assert h.malloc(n, first_fit) == got
            if got is not None:
                live.append(got)
        assert check(h) == model


def test_reads_on_a_trace() -> None:
    rng = random.Random(3)
    h, g, live, frees = Heap(1 << 14), ScanHeap(1 << 14), [], 0
    for _ in range(3000):
        if live and rng.random() < 0.45:
            p = live.pop(rng.randrange(len(live)))
            h.free(p)
            g.free(p)
            frees += 1
        else:
            n = rng.randint(1, 64)
            p = h.malloc(n, first_fit)
            assert g.malloc(n, first_fit) == p
            if p is not None:
                live.append(p)
    assert blocks(h) == blocks(g)
    assert h.reads <= 3 * frees
    assert (frees, len(live), len(blocks(h)), h.reads, g.reads) == (1373, 254, 328, 4092, 97573)


def test_errors() -> None:
    h = Heap(16)
    p = h.malloc(2, first_fit)
    h.free(p)
    with pytest.raises(ValueError):
        h.free(p)
    q = h.malloc(2, first_fit)
    h.malloc(2, first_fit)
    assert h.lower_free(q + 3) == NIL  # the block below is used
