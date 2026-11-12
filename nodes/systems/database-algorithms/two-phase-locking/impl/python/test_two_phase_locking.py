# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-phase-locking/. The authors are listed in prov/JSBTG5.jsonl.

import random

from two_phase_locking import run_2pl


def conflict(p, q) -> bool:
    return p[1] != q[1] and p[2] == q[2] and "w" in (p[0], q[0])


def graph(s) -> dict[int, set[int]]:
    g: dict[int, set[int]] = {p[1]: set() for p in s}
    for i, p in enumerate(s):
        for q in s[i + 1 :]:
            if conflict(p, q):
                g[p[1]].add(q[1])
    return g


def acyclic(g) -> bool:
    indeg = {v: 0 for v in g}
    for v in g:
        for w in g[v]:
            indeg[w] += 1
    ready = [v for v in g if indeg[v] == 0]
    seen = 0
    while ready:
        v = ready.pop()
        seen += 1
        for w in g[v]:
            indeg[w] -= 1
            if indeg[w] == 0:
                ready.append(w)
    return seen == len(g)


def conflict_equivalent(s1, s2) -> bool:
    def pairs(s):
        tagged, count = [], {}
        for p in s:
            count[p[1]] = count.get(p[1], 0) + 1
            tagged.append((p, count[p[1]]))
        return {(a, b) for i, a in enumerate(tagged) for b in tagged[i + 1 :] if conflict(a[0], b[0])}

    return sorted(s1) == sorted(s2) and pairs(s1) == pairs(s2)


def random_programs(rng: random.Random) -> dict:
    return {
        t: [(rng.choice("rw"), rng.choice("xyz")) for _ in range(rng.randint(1, 4))]
        for t in range(1, rng.randint(2, 5) + 1)
    }


def test_trace_example() -> None:
    progs = {1: [("r", "x"), ("w", "x"), ("w", "y")], 2: [("r", "x"), ("w", "z")]}
    out = run_2pl(progs, script=[1, 1, 1, 2, 2, 1, 2])
    assert out["schedule"] == [
        ("r", 1, "x"), ("w", 1, "x"), ("w", 1, "y"), ("r", 2, "x"), ("w", 2, "z"),
        ("c", 1, None), ("c", 2, None),
    ]
    assert out["events"] == [
        ("lock", 1, "x", "S"), ("lock", 1, "x", "X"), ("lock", 1, "y", "X"),
        ("unlock", 1, "x"), ("unlock", 1, "y"),
        ("lock", 2, "x", "S"), ("lock", 2, "z", "X"), ("unlock", 2, "x"), ("unlock", 2, "z"),
    ]
    assert out["lock_point"] == {1: 3, 2: 5}


def test_deadlock_example() -> None:
    progs = {1: [("r", "x"), ("w", "y")], 2: [("r", "y"), ("w", "x")]}
    out = run_2pl(progs, script=[1, 2, 1, 2])
    assert out["aborts"] == 1
    assert out["schedule"][:3] == [("r", 1, "x"), ("r", 2, "y"), ("a", 2, None)]
    assert out["committed"] == [("r", 1, "x"), ("w", 1, "y"), ("r", 2, "y"), ("w", 2, "x")]


def test_random_runs_are_conflict_serializable_in_lock_point_order() -> None:
    rng = random.Random(77)
    total_aborts = 0
    for _ in range(800):
        progs = random_programs(rng)
        out = run_2pl(progs, rng=rng, p_release=rng.choice([0.0, 0.3, 1.0]))
        s = out["committed"]
        assert acyclic(graph(s))
        order = sorted(progs, key=out["lock_point"].__getitem__)
        serial = [p for t in order for p in s if p[1] == t]
        assert conflict_equivalent(s, serial)
        for t in progs:
            assert [(op, x) for op, u, x in s if u == t] == progs[t]
        total_aborts += out["aborts"]
    assert total_aborts > 0


def test_two_phase_rule_holds_in_each_attempt() -> None:
    rng = random.Random(8)
    for _ in range(300):
        progs = random_programs(rng)
        out = run_2pl(progs, rng=rng)
        state = {t: "growing" for t in progs}
        for e in out["events"]:
            t = e[1]
            if e[0] == "abort":
                state[t] = "growing"
            elif e[0] == "unlock":
                state[t] = "shrinking"
            else:
                assert state[t] == "growing"
