# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/treedoc/. The authors are listed in prov/13DJ1S.jsonl.

import random

from treedoc import Treedoc


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


def run(seed: int, n: int, nops: int, dup: float = 0.2) -> list[Treedoc]:
    rng = random.Random(seed)
    reps = [Treedoc(i) for i in range(n)]
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
            reps[d].apply(payload[o])  # insert and delete are both idempotent
            hist[d].add(o)
            read(d)
    for i in range(n):
        assert reps[i].order() == reps[0].order()
        assert reps[i].value() == reps[0].value()
    assert acyclic(edges)
    return reps


def test_page_example() -> None:
    a, b = Treedoc(1), Treedoc(2)
    for op in (a.local_insert(0, "H"), a.local_insert(1, "i")):
        b.apply(op)
    assert a.order() == [(), ((1, (1, 1)),), ((1, (1, 1)), (1, (2, 1)))]
    x = a.local_insert(1, "e")  # H has a right child, so a left child of i
    y = b.local_insert(1, "o")  # the same path, another mini-node
    assert x[1] == ((1, (1, 1)), (1, (2, 1)), (0, (3, 1)))
    assert y[1] == ((1, (1, 1)), (1, (2, 1)), (0, (1, 2)))
    a.apply(y)
    b.apply(x)
    assert a.value() == b.value() == ["H", "o", "e", "i"]  # mini-nodes in dis order


def test_flatten_on_an_agreed_state() -> None:
    reps = run(7, 3, 80)
    for r in reps:
        r.flatten()
    assert all(r.order() == reps[0].order() for r in reps)
    assert not reps[0].dead
    depth = max(len(p) for p in reps[0].order())
    m = len(reps[0].value())
    assert 2 ** (depth - 1) <= 2 * m + 2  # balanced: depth about log2 of the size


def test_seeded_runs() -> None:
    for seed in range(60):
        run(seed, 2 + seed % 4, 40 + 5 * (seed % 20))


def test_larger_run() -> None:
    run(1000, 5, 300)
