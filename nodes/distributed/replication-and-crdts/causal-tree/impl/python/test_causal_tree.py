# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/causal-tree/. The authors are listed in prov/B5EAJ4.jsonl.

import random

from causal_tree import ROOT, Atom, CausalTree


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


def rga_order(atoms: list[Atom]) -> list:
    """Replay the character atoms with the RGA rule: after the cause, skip larger ids."""
    seq: list = [ROOT]
    for a in sorted(atoms, key=lambda a: a.id):  # id order is a causal order
        if a.kind != "char":
            continue
        p = seq.index(a.cause) + 1
        while p < len(seq) and seq[p] > a.id:
            p += 1
        seq.insert(p, a.id)
    return seq[1:]


def run(seed: int, n: int, nops: int, dup: float = 0.2) -> CausalTree:
    rng = random.Random(seed)
    reps = [CausalTree(i) for i in range(n)]
    payload: list[Atom] = []
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
            reps[d].apply(payload[o])  # add() ignores an atom it already has
            hist[d].add(o)
            read(d)
    for i in range(n):
        assert reps[i].order() == reps[0].order()
        assert reps[i].value() == reps[0].value()
    assert acyclic(edges)
    assert reps[0].order() == rga_order(payload)  # the same order as RGA with these ids
    return reps[0]


def test_page_example() -> None:
    a, b = CausalTree(0), CausalTree(1)
    for x in [a.local_insert(0, "H"), a.local_insert(1, "i")]:
        b.apply(x)
    x = a.local_insert(1, "e")  # id (3, 0), cause H
    y = b.local_insert(1, "o")  # id (3, 1), cause H
    a.apply(y)
    b.apply(x)
    assert a.children[(1, 0)] == [(3, 1), (3, 0), (2, 0)]
    assert a.value() == b.value() == ["H", "o", "e", "i"]
    d = b.local_delete(1)  # delete atom (4, 1), cause (3, 1)
    a.apply(d)
    assert a.value() == ["H", "e", "i"] and d.cause == (3, 1)


def test_seeded_runs() -> None:
    for seed in range(60):
        run(seed, 2 + seed % 4, 40 + 5 * (seed % 20))


def test_larger_run() -> None:
    run(1000, 5, 250)
