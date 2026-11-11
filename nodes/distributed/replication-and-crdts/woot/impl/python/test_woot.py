# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/woot/. The authors are listed in prov/D9EX5G.jsonl.

import random

from woot import Woot


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
    """Random edits; the network reorders freely (no causal delivery) and duplicates."""
    rng = random.Random(seed)
    reps = [Woot(i) for i in range(n)]
    payload: list = []
    net: list[tuple[int, int]] = []
    edges: set[tuple] = set()

    def read(i: int) -> None:
        reps[i].check_invariant()
        v = reps[i].value()
        edges.update(zip(v, v[1:]))

    made = 0
    while made < nops or net:
        if made < nops and (not net or rng.random() < 0.5):
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
            net.extend((d, len(payload) - 1) for d in range(n) if d != i)
            made += 1
            read(i)
        else:
            k = rng.randrange(len(net))
            d, o = net[k]
            if rng.random() >= dup:
                net.pop(k)
            reps[d].apply(payload[o])
            read(d)
    for i in range(n):
        assert not reps[i].pool
        assert reps[i].order() == reps[0].order()
        assert reps[i].value() == reps[0].value()
    assert acyclic(edges)
    return reps[0].value()


def test_page_example() -> None:
    a, b, c = Woot(1), Woot(2), Woot(3)
    ops = [a.local_insert(0, "a"), a.local_insert(1, "b")]
    for op in ops:
        b.apply(op)
        c.apply(op)
    x = a.local_insert(1, "1")  # between a and b, id (1, 3)
    y = b.local_insert(1, "2")  # between a and b, id (2, 1)
    z = c.local_insert(1, "3")  # between a and b, id (3, 1)
    a.apply(z)
    a.apply(y)
    c.apply(y)
    c.apply(x)
    b.apply(x)
    b.apply(z)
    assert a.value() == b.value() == c.value() == ["a", "1", "2", "3", "b"]


def test_out_of_order_delivery_waits_in_the_pool() -> None:
    a, b = Woot(1), Woot(2)
    o1 = a.local_insert(0, "x")
    o2 = a.local_insert(1, "y")  # its prev is x
    o3 = a.local_delete(0)
    b.apply(o3)
    b.apply(o2)
    assert b.value() == [] and len(b.pool) == 2
    b.apply(o1)
    b.apply(o1)  # a duplicate is ignored
    assert b.value() == a.value() == ["y"] and not b.pool


def test_no_interleaving_on_simple_runs() -> None:
    for word_a, word_b, front in (("abc", "xyz", False), ("cba", "zyx", True)):
        a, b = Woot(1), Woot(2)
        oa = [a.local_insert(0 if front else i, ch) for i, ch in enumerate(word_a)]
        ob = [b.local_insert(0 if front else i, ch) for i, ch in enumerate(word_b)]
        for op in ob:
            a.apply(op)
        for op in oa:
            b.apply(op)
        assert "".join(a.value()) == "".join(b.value()) == "abcxyz"


def test_seeded_runs() -> None:
    for seed in range(60):
        run(seed, 2 + seed % 4, 40 + 5 * (seed % 20))


def test_larger_run() -> None:
    run(1000, 5, 250)
