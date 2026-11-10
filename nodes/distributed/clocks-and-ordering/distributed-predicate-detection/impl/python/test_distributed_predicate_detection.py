# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-predicate-detection/. The authors are listed in prov/E1GYTY.jsonl.

import random

from distributed_predicate_detection import (
    definitely,
    definitely_brute,
    possibly,
    possibly_brute,
    runs,
    sat_instance,
    satisfiable,
)

# The page example. p0: e1 sets x = 1 and sends m0; e2 receives m1 and sets x = 0.
# p1: e1 receives m0 and sets y = 1; e2 sends m1; e3 sets y = 0.
WITH_REPLY = [
    [("send", 0, 1), ("recv", 1, 1)],
    [("recv", 0, 0), ("send", 1, 0), ("int",)],
]
X = [0, 1, 0]
Y = [0, 1, 1, 0]


def phi(cut):
    return X[cut[0]] == 1 and Y[cut[1]] == 1


def test_page_example() -> None:
    assert len({c for r in runs(WITH_REPLY) for c in r}) == 7
    assert possibly(WITH_REPLY, phi) and definitely(WITH_REPLY, phi)
    # Without the reply, p0 can set x = 0 before p1 sets y = 1.
    no_reply = [[("send", 0, 1), ("int",)], [("recv", 0, 0), ("int",), ("int",)]]
    assert possibly(no_reply, phi) and not definitely(no_reply, phi)


def random_computation(n, steps, rng):
    comp = [[] for _ in range(n)]
    transit = []
    mid = 0
    for _ in range(steps):
        i = rng.randrange(n)
        mine = [x for x in transit if x[2] == i]
        r = rng.random()
        if mine and r < 0.4:
            x = rng.choice(mine)
            transit.remove(x)
            comp[i].append(("recv", x[0], x[1]))
        elif r < 0.8:
            dst = rng.choice([j for j in range(n) if j != i])
            comp[i].append(("send", mid, dst))
            transit.append((mid, i, dst))
            mid += 1
        else:
            comp[i].append(("int",))
    return comp


def test_against_run_enumeration() -> None:
    seen = {(a, b) for a in (False, True) for b in (False, True)}
    got = set()
    for seed in range(300):
        rng = random.Random(seed)
        n = rng.randrange(2, 4)
        comp = random_computation(n, rng.randrange(2, 9), rng)
        vals = [[rng.randrange(3) for _ in range(len(p) + 1)] for p in comp]
        target = rng.randrange(3 * n)
        f = lambda c, vals=vals, target=target: sum(vals[i][c[i]] for i in range(len(c))) == target
        p, d = possibly(comp, f), definitely(comp, f)
        assert p == possibly_brute(comp, f)
        assert d == definitely_brute(comp, f)
        assert p or not d  # definitely implies possibly
        got.add((p, d))
    assert got == seen - {(False, True)}


def test_sat_reduction() -> None:
    for seed in range(200):
        rng = random.Random(seed)
        k = rng.randrange(1, 6)
        cnf = [[rng.choice([1, -1]) * rng.randrange(1, k + 1) for _ in range(3)] for _ in range(rng.randrange(1, 9))]
        comp, f = sat_instance(cnf, k)
        assert possibly(comp, f) == satisfiable(cnf, k)


def test_unsat_reduction() -> None:
    from distributed_predicate_detection import unsat_instance

    both = set()
    for seed in range(150):
        rng = random.Random(seed)
        k = rng.randrange(1, 4)
        cnf = [[rng.choice([1, -1]) * rng.randrange(1, k + 1) for _ in range(rng.randrange(1, 4))] for _ in range(rng.randrange(1, 7))]
        comp, f = unsat_instance(cnf, k)
        d = definitely(comp, f)
        assert d == (not satisfiable(cnf, k))
        if k <= 2:  # at most 5! runs
            assert d == definitely_brute(comp, f)
        both.add(d)
    assert both == {False, True}
