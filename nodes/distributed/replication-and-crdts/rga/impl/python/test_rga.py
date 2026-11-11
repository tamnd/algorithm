# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rga/. The authors are listed in prov/WZ1GQT.jsonl.

import random

from rga import RGA


def acyclic(edges: set[tuple]) -> bool:
    """True when the 'comes before' edges have a topological order (one list order)."""
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
    reps = [RGA(n, i) for i in range(n)]
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
            if o not in hist[d]:  # at-most-once on top of a duplicating network
                reps[d].apply(payload[o])
                hist[d].add(o)
            read(d)
    for i in range(n):
        assert reps[i].order() == reps[0].order()
        assert reps[i].value() == reps[0].value()
    assert acyclic(edges)  # one list order explains every read: the strong list spec
    return reps[0].value()


def test_page_example() -> None:
    a, b = RGA(2, 0), RGA(2, 1)
    ops = [a.local_insert(0, "H"), a.local_insert(1, "i")]
    for op in ops:
        b.apply(op)
    x = a.local_insert(1, "e")  # a types between H and i
    y = b.local_insert(1, "o")  # b types at the same place
    assert x[2].key() == (0, 3, 0) and y[2].key() == (0, 3, 1)
    a.apply(y)
    b.apply(x)
    assert a.value() == b.value() == ["H", "o", "e", "i"]  # larger timestamp nearer the reference
    z = a.local_delete(2)
    b.apply(z)
    assert a.value() == b.value() == ["H", "o", "i"]
    assert len(a.order()) == 4  # the tombstone stays


def test_forward_typing_does_not_interleave() -> None:
    a, b = RGA(2, 0), RGA(2, 1)
    oa = [a.local_insert(i, c) for i, c in enumerate("abc")]
    ob = [b.local_insert(i, c) for i, c in enumerate("xyz")]
    for op in ob:
        a.apply(op)
    for op in oa:
        b.apply(op)
    assert "".join(a.value()) == "".join(b.value()) in ("abcxyz", "xyzabc")


def test_back_to_front_typing_interleaves() -> None:
    # Each replica types its word from the last letter to the first, always at the head.
    a, b = RGA(2, 0), RGA(2, 1)
    oa = [a.local_insert(0, c) for c in "cba"]
    ob = [b.local_insert(0, c) for c in "zyx"]
    for op in ob:
        a.apply(op)
    for op in oa:
        b.apply(op)
    assert "".join(a.value()) == "".join(b.value()) == "xaybzc"


def test_seeded_runs() -> None:
    for seed in range(60):
        run(seed, 2 + seed % 4, 40 + 5 * (seed % 20))


def test_larger_run() -> None:
    assert len(run(1000, 5, 300)) > 0
