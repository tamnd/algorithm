# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/logoot/. The authors are listed in prov/AHQMT3.jsonl.

import random

from logoot import Logoot, alloc


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


def run(seed: int, n: int, nops: int, base: int, dup: float = 0.2) -> list:
    rng = random.Random(seed)
    reps = [Logoot(i, base=base, seed=seed) for i in range(n)]
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


def test_alloc_is_between() -> None:
    rng = random.Random(3)
    p = ((5, 1, 1),)
    q = ((6, 2, 1),)
    x = alloc(p, q, 100, 10, 3, 7, rng)  # no free digit at level 1, so go one level down
    assert p < x < q and len(x) == 2 and x[0] == p[0]
    p = ((5, 1, 1), (7, 1, 2))
    q = ((5, 2, 1), (3, 2, 2))  # same first digit, different sites
    x = alloc(p, q, 100, 10, 3, 8, rng)
    assert p < x < q
    for _ in range(2000):  # random pairs
        a = tuple((rng.randint(0, 3), rng.randint(0, 2), rng.randint(0, 2)) for _ in range(rng.randint(1, 3)))
        b = tuple((rng.randint(0, 3), rng.randint(0, 2), rng.randint(0, 2)) for _ in range(rng.randint(1, 3)))
        a, b = min(a, b), max(a, b)
        if a == b or b[-1][0] == 0 or a[: len(b)] == b:
            continue
        assert a < alloc(a, b, 4, 2, 9, 9, rng) < b


def test_page_example() -> None:
    a, b = Logoot(1, base=100, seed=5), Logoot(2, base=100, seed=5)
    for op in (a.local_insert(0, "H"), a.local_insert(1, "i")):
        b.apply(op)
    x = a.local_insert(1, "e")
    y = b.local_insert(1, "o")
    a.apply(y)
    b.apply(x)
    assert a.value() == b.value()
    assert a.order() == b.order()
    assert sorted(a.value()) == ["H", "e", "i", "o"]


def test_concurrent_typing_can_interleave() -> None:
    found = 0
    for seed in range(20):
        a, b = Logoot(1, seed=seed), Logoot(2, seed=seed)
        oa = [a.local_insert(i, ch) for i, ch in enumerate("abcd")]
        ob = [b.local_insert(i, ch) for i, ch in enumerate("wxyz")]
        for op in ob:
            a.apply(op)
        for op in oa:
            b.apply(op)
        s = "".join(a.value())
        assert s == "".join(b.value())
        found += s not in ("abcdwxyz", "wxyzabcd")
    assert found > 0  # character-by-character interleaving happens


def test_identifier_growth() -> None:
    def avg_depth(mode: str, n: int) -> float:
        doc = Logoot(0, base=2**10, boundary=10, seed=1)
        for k in range(n):
            doc.local_insert(len(doc.pos) if mode == "append" else 0, k)
        return sum(len(x) for x in doc.pos) / n

    assert avg_depth("append", 2000) < 8
    assert avg_depth("prepend", 2000) > 100  # boundary+ only: typing at the front grows linearly


def test_seeded_runs() -> None:
    for seed in range(60):
        run(seed, 2 + seed % 4, 40 + 5 * (seed % 20), 16 if seed % 2 else 2**10)


def test_larger_run() -> None:
    run(1000, 5, 300, 8)
