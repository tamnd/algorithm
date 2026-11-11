# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lseq/. The authors are listed in prov/DDRN05.jsonl.

import random

from lseq import LSeq, base_at, bits


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


def run(seed: int, n: int, nops: int, boundary: int, dup: float = 0.2) -> list:
    rng = random.Random(seed)
    reps = [LSeq(i, boundary=boundary, seed=seed) for i in range(n)]
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
            if o not in hist[d]:
                reps[d].apply(payload[o])
                hist[d].add(o)
            read(d)
    for i in range(n):
        assert reps[i].order() == reps[0].order()
        assert reps[i].value() == reps[0].value()
    assert acyclic(edges)
    return reps[0].value()


def test_bases_double() -> None:
    assert [base_at(i) for i in range(4)] == [32, 64, 128, 256]
    assert bits(((1, 0, 0), (1, 0, 0))) == 5 + 6


def test_strategy_is_fixed_per_depth() -> None:
    doc = LSeq(0, seed=4)
    for k in range(300):
        doc.local_insert(len(doc.pos), k)
    assert set(doc.strategy) == set(range(max(len(x) for x in doc.pos)))


def test_concurrent_typing_can_interleave() -> None:
    found = 0
    for seed in range(20):
        a, b = LSeq(1, seed=seed), LSeq(2, seed=seed + 100)
        oa = [a.local_insert(i, ch) for i, ch in enumerate("abcd")]
        ob = [b.local_insert(i, ch) for i, ch in enumerate("wxyz")]
        for op in ob:
            a.apply(op)
        for op in oa:
            b.apply(op)
        s = "".join(a.value())
        assert s == "".join(b.value())
        found += s not in ("abcdwxyz", "wxyzabcd")
    assert found > 0


def test_identifier_growth_stays_small() -> None:
    for mode in ("append", "prepend", "random"):
        rng = random.Random(2)
        doc = LSeq(0, seed=1)
        for k in range(2000):
            m = len(doc.pos)
            doc.local_insert(m if mode == "append" else 0 if mode == "prepend" else rng.randint(0, m), k)
        avg = sum(len(x) for x in doc.pos) / 2000
        assert avg < 12, (mode, avg)


def test_seeded_runs() -> None:
    for seed in range(60):
        run(seed, 2 + seed % 4, 40 + 5 * (seed % 20), 1 + seed % 10)


def test_larger_run() -> None:
    run(1000, 5, 300, 10)
