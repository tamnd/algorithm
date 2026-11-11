# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/yata/. The authors are listed in prov/Y6F20Y.jsonl.

import random

from yata import Yata


def acyclic(edges: set[tuple]) -> bool:
    succ: dict = {}
    indeg: dict = {}
    for a, b in edges:
        succ.setdefault(a, []).append(b)
        indeg[b] = indeg.get(b, 0) + 1
        indeg.setdefault(a, 0)
    todo = [v for v, d in indeg.items() if d == 0]
    seen = 0
    while todo:
        v = todo.pop()
        seen += 1
        for w in succ.get(v, []):
            indeg[w] -= 1
            if indeg[w] == 0:
                todo.append(w)
    return seen == len(indeg)


def run(seed: int, n: int, nops: int, dup: float = 0.2) -> list:
    rng = random.Random(seed)
    reps = [Yata(i) for i in range(n)]
    payload: list = []
    deps: list[frozenset[int]] = []
    hist: list[set[int]] = [set() for _ in range(n)]
    net: list[tuple[int, int]] = []
    edges: set[tuple] = set()

    def read(i: int) -> None:
        reps[i].check_invariant()
        v = reps[i].value()
        edges.update(zip(v, v[1:]))

    made = 0
    while made < nops or net:
        ready = [k for k, (d, o) in enumerate(net) if deps[o] <= hist[d]]
        if made < nops and (not ready or rng.random() < 0.5):
            i = rng.randrange(n)
            vis = reps[i].value()
            if vis and rng.random() < 0.25:
                j = rng.randrange(len(vis))
                op = reps[i].local_delete(j)
                assert reps[i].value() == vis[:j] + vis[j + 1:]
            else:
                j = rng.randrange(len(vis) + 1)
                val = f"{i}.{made}"
                op = reps[i].local_insert(j, val)
                assert reps[i].value() == vis[:j] + [val] + vis[j:]
            payload.append(op)
            deps.append(frozenset(hist[i]))
            hist[i].add(len(payload) - 1)
            net.extend((d, len(payload) - 1) for d in range(n) if d != i)
            made += 1
            read(i)
        else:
            k = rng.choice(ready)
            d, o = net[k]
            if rng.random() >= dup:
                net.pop(k)
            reps[d].apply(payload[o])  # a second copy of an item is ignored
            hist[d].add(o)
            read(d)
    for i in range(n):
        assert reps[i].order() == reps[0].order()
        assert reps[i].value() == reps[0].value()
    assert acyclic(edges)
    return reps[0].value()


def test_page_example() -> None:
    a, b, c = Yata(1), Yata(2), Yata(3)
    for op in [a.local_insert(0, "H"), a.local_insert(1, "i")]:
        b.apply(op)
        c.apply(op)
    x = a.local_insert(1, "e")  # origin H, right origin i
    y = b.local_insert(1, "o")  # the same origins
    z = c.local_insert(1, "u")  # the same origins
    for r, ops in ((a, (y, z)), (b, (z, x)), (c, (x, y))):
        for op in ops:
            r.apply(op)
    assert a.value() == b.value() == c.value() == ["H", "e", "o", "u", "i"]  # client id order


def test_forward_typing_does_not_interleave() -> None:
    a, b = Yata(1), Yata(2)
    oa = [a.local_insert(i, ch) for i, ch in enumerate("abc")]
    ob = [b.local_insert(i, ch) for i, ch in enumerate("xyz")]
    for op in ob:
        a.apply(op)
    for op in oa:
        b.apply(op)
    assert "".join(a.value()) == "".join(b.value()) == "abcxyz"


def test_back_to_front_typing_does_not_interleave() -> None:
    a, b = Yata(1), Yata(2)
    oa = [a.local_insert(0, ch) for ch in "cba"]
    ob = [b.local_insert(0, ch) for ch in "zyx"]
    for op in ob:
        a.apply(op)
    for op in oa:
        b.apply(op)
    assert "".join(a.value()) == "".join(b.value()) == "abcxyz"


def test_seeded_runs() -> None:
    for seed in range(80):
        run(seed, 2 + seed % 4, 40 + 5 * (seed % 20))


def test_larger_run() -> None:
    run(1000, 5, 300)
