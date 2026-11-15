# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterative-modulo-scheduling/. The authors are listed in prov/PJN90C.jsonl.
import random

import pytest

import iterative_modulo_scheduling as ims

# acc = acc * c + x[i] * y[i], with i = i + 1
NAMES = ["lx", "ly", "m1", "m2", "a", "inc"]
RES = [[("mem", 0)], [("mem", 0)], [("mul", 0)], [("mul", 0)], [("alu", 0)], [("alu", 0)]]
EDGES = [
    (0, 3, 2, 0), (1, 3, 2, 0), (2, 4, 2, 0), (3, 4, 2, 0), (4, 2, 1, 1),
    (5, 0, 1, 1), (5, 1, 1, 1), (5, 5, 1, 1), (0, 5, 0, 0), (1, 5, 0, 0),
]
MACHINE = {"mem": 1, "mul": 1, "alu": 1}


def ceil_div(a, b):
    return -(-a // b)


def legal(n, res, edges, machine, ii, t):
    """Every edge holds and no slot of the modulo reservation table is over
    its number of units."""
    if sorted(t) != list(range(n)) or min(t.values(), default=0) < 0:
        return False
    for u, v, delay, dist in edges:
        if t[v] + ii * dist < t[u] + delay:
            return False
    use = {}
    for v in range(n):
        for r, off in res[v]:
            key = (r, (t[v] + off) % ii)
            use[key] = use.get(key, 0) + 1
    return all(c <= machine[key[0]] for key, c in use.items())


def flat_ok(n, res, edges, machine, ii, t, iters):
    """Run iters overlapped iterations, iteration i from cycle i * II, and
    check every unit in every cycle and every dependence between iterations."""
    start = {(v, i): i * ii + t[v] for v in range(n) for i in range(iters)}
    busy = {}
    for (v, i), s in start.items():
        for r, off in res[v]:
            busy[(r, s + off)] = busy.get((r, s + off), 0) + 1
    if any(c > machine[r] for (r, _), c in busy.items()):
        return False
    for u, v, delay, dist in edges:
        for i in range(iters - dist):
            if start[(v, i + dist)] < start[(u, i)] + delay:
                return False
    return True


def oracle_res_mii(n, res, machine):
    best = 0
    for r in machine:
        uses = sum(1 for v in range(n) for x, _ in res[v] if x == r)
        best = max(best, ceil_div(uses, machine[r]))
    return best


def oracle_rec_mii(n, edges):
    """max over simple cycles of ceil(delay / distance), by enumeration of
    the simple cycles from their least vertex."""
    out = [[] for _ in range(n)]
    for u, v, delay, dist in edges:
        out[u].append((v, delay, dist))
    best = 0

    def walk(start, x, on, delay, dist):
        nonlocal best
        for y, d1, d2 in out[x]:
            if y == start:
                assert dist + d2 >= 1
                best = max(best, ceil_div(delay + d1, dist + d2))
            elif y > start and y not in on:
                on.add(y)
                walk(start, y, on, delay + d1, dist + d2)
                on.discard(y)

    for s in range(n):
        walk(s, s, {s}, 0, 0)
    return best


def feasible(n, res, edges, machine, ii):
    """Exact test: is there any legal modulo schedule at ii? Enumerate the
    slots k(v) = t(v) mod ii that fit the table; then t(v) = k(v) + ii q(v)
    and the edges are difference constraints on the integers q(v)."""
    k = [0] * n
    use = {}

    def diff_ok():
        cons = [(u, v, ceil_div(delay - ii * dist - k[v] + k[u], ii)) for u, v, delay, dist in edges]
        q = [0] * n
        for _ in range(n + 1):
            changed = False
            for u, v, c in cons:
                if q[u] + c > q[v]:
                    q[v] = q[u] + c
                    changed = True
            if not changed:
                return True
        return False

    def rec(j):
        if j == n:
            return diff_ok()
        for x in range(ii):
            keys = [(r, (x + off) % ii) for r, off in res[j]]
            for key in keys:
                use[key] = use.get(key, 0) + 1
            if all(use[key] <= machine[key[0]] for key in keys):
                k[j] = x
                if rec(j + 1):
                    for key in keys:
                        use[key] -= 1
                    return True
            for key in keys:
                use[key] -= 1
        return False

    return rec(0)


def random_loop(rng, n):
    machine = {"mem": 1, "alu": rng.choice([1, 2]), "mul": 1}
    res = []
    for _ in range(n):
        r = rng.choice(["mem", "alu", "mul"])
        if r == "mul" and rng.random() < 0.3:
            res.append([("mul", 0), ("mul", 1)])
        else:
            res.append([(r, 0)])
    edges = []
    for _ in range(rng.randint(0, 2 * n)):
        u, v = rng.randrange(n), rng.randrange(n)
        dist = 0 if u < v and rng.random() < 0.6 else rng.randint(1, 3)
        edges.append((u, v, rng.randint(-1, 4), dist))
    return n, res, edges, machine


def test_example():
    n = len(NAMES)
    assert ims.res_mii(n, RES, MACHINE) == 2
    assert ims.rec_mii(n, EDGES) == 3
    assert ims.height_r(n, EDGES, 3) == [4, 4, 2, 2, 0, 2]
    log = []
    ii, t, mii = ims.modulo_schedule(n, RES, EDGES, MACHINE, log=log)
    assert (ii, mii) == (3, 3)
    assert {NAMES[v]: s for v, s in t.items()} == {"lx": 0, "ly": 1, "m1": 6, "m2": 4, "a": 8, "inc": 1}
    steps = [(NAMES[v], e, s, [NAMES[w] for w in out]) for v, e, s, out in log[1:]]
    assert steps == [
        ("lx", 0, 0, []), ("ly", 0, 1, []), ("m1", 0, 0, []), ("m2", 3, 4, []), ("inc", 1, 1, []),
        ("a", 6, 6, ["m1"]), ("m1", 4, 5, ["a"]), ("a", 7, 8, ["m1"]), ("m1", 6, 6, []),
    ]
    assert ims.stages(t, ii) == ({0: 0, 1: 0, 2: 2, 3: 1, 4: 2, 5: 0}, 3)
    assert legal(n, RES, EDGES, MACHINE, ii, t)
    assert flat_ok(n, RES, EDGES, MACHINE, ii, t, 6)
    assert not feasible(n, RES, EDGES, MACHINE, 2) and feasible(n, RES, EDGES, MACHINE, 3)


def test_random_loops_against_oracles():
    rng = random.Random(21)
    for _ in range(600):
        n, res, edges, machine = random_loop(rng, rng.randint(1, 7))
        rm = ims.res_mii(n, res, machine)
        cm = ims.rec_mii(n, edges)
        assert rm == oracle_res_mii(n, res, machine)
        assert cm == oracle_rec_mii(n, edges)
        ii, t, mii = ims.modulo_schedule(n, res, edges, machine)
        assert mii == max(1, rm, cm) and ii >= mii
        assert legal(n, res, edges, machine, ii, t)
        _, sc = ims.stages(t, ii)
        assert flat_ok(n, res, edges, machine, ii, t, sc + 3)


def test_mii_bounds_the_optimum():
    rng = random.Random(22)
    hit = 0
    for _ in range(150):
        n, res, edges, machine = random_loop(rng, rng.randint(1, 5))
        ii, t, mii = ims.modulo_schedule(n, res, edges, machine)
        best = next(x for x in range(1, ii + 1) if feasible(n, res, edges, machine, x))
        assert mii <= best <= ii
        if not feasible(n, res, edges, machine, mii):
            assert best > mii
        hit += ii == best
    assert hit >= 140


def test_small_budget_still_legal():
    rng = random.Random(23)
    worse = 0
    for _ in range(200):
        n, res, edges, machine = random_loop(rng, rng.randint(2, 7))
        ii, t, mii = ims.modulo_schedule(n, res, edges, machine, budget_ratio=1)
        assert ii >= mii and legal(n, res, edges, machine, ii, t)
        worse += ii > ims.modulo_schedule(n, res, edges, machine)[0]
    assert worse > 0


def test_self_conflicting_table():
    # a divide that holds the multiplier in cycles 0 and 2 cannot run at II = 2
    res = [[("mul", 0), ("mul", 2)], [("alu", 0)]]
    machine = {"mul": 1, "alu": 1}
    assert ims.res_mii(2, res, machine) == 2
    assert ims.iterative_schedule(2, res, [], machine, 2, 6) is None
    ii, t, _ = ims.modulo_schedule(2, res, [], machine)
    assert ii == 3 and legal(2, res, [], machine, 3, t)
    assert not feasible(2, res, [], machine, 2)


def test_rounding_up():
    # three loads on two memory ports: II = 1 would need three ports
    res = [[("mem", 0)]] * 3
    machine = {"mem": 2}
    assert ims.res_mii(3, res, machine) == 2
    assert not feasible(3, res, [], machine, 1)
    # a recurrence of delay 5 over distance 2 needs II = 3, not 2
    edges = [(0, 1, 3, 0), (1, 0, 2, 2)]
    assert ims.rec_mii(2, edges) == 3
    assert not feasible(2, [[("alu", 0)], [("alu", 0)]], edges, {"alu": 2}, 2)


def test_input_checks():
    with pytest.raises(ValueError):
        ims.modulo_schedule(2, [[("alu", 0)], [("alu", 0)]], [(0, 1, 1, 0), (1, 0, 1, 0)], {"alu": 1})
    with pytest.raises(ValueError):
        ims.modulo_schedule(1, [[("alu", 0)]], [(0, 0, 1, 0)], {"alu": 1})
    with pytest.raises(ValueError):
        ims.modulo_schedule(1, [[("fpu", 0)]], [], {"alu": 1})
    with pytest.raises(ValueError):
        ims.modulo_schedule(1, [[("alu", 0)]], [(0, 0, 1, -1)], {"alu": 1})
    assert ims.modulo_schedule(0, [], [], {"alu": 1}) == (1, {}, 1)
    ii, t, _ = ims.modulo_schedule(1, [[("alu", 0)]], [(0, 0, 4, 1)], {"alu": 1})
    assert (ii, t) == (4, {0: 0})
