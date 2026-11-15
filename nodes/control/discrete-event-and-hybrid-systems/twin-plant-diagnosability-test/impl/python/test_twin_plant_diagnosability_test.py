# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/twin-plant-diagnosability-test/. The authors are listed in prov/4TC48W.jsonl.

import random

from twin_plant_diagnosability_test import build_verifier, diagnosable, diagnosable_jiang, witness


def plant(edges, init=0):
    return {"init": init, "delta": {(x, e): y for x, e, y in edges}}


# The worked example of the page: normal cycle a u b; after the fault the plant repeats b a.
AMBIGUOUS = plant([(0, "a", 1), (1, "u", 2), (2, "b", 0), (1, "f", 3), (3, "b", 4), (4, "a", 5), (5, "b", 4)])
# The same plant, but after the fault it shows c forever.
DIAGNOSABLE = plant([(0, "a", 1), (1, "u", 2), (2, "b", 0), (1, "f", 3), (3, "b", 4), (4, "c", 4)])
# Diagnosable, although its diagnoser has a cycle of uncertain states.
UNCERTAIN = plant([(1, "a", 1), (1, "f", 5), (5, "a", 2), (2, "b", 6), (6, "b", 6)], init=1)


def run(g, s):
    q = g["init"]
    for e in s:
        q = g["delta"].get((q, e))
        if q is None:
            return None
    return q


def oracle_diagnoser(g, observable, fault_events):
    """Independent test by the diagnoser of Sampath et al.: no indeterminate cycle means diagnosable."""
    out = {}
    for (x, e), y in g["delta"].items():
        out.setdefault(x, {})[e] = y
    memo = {}

    def jumps(pair):
        if pair in memo:
            return memo[pair]
        res = {}
        seen = {pair}
        stack = [pair]
        while stack:
            x, f = stack.pop()
            for e, y in out.get(x, {}).items():
                if e in observable:
                    res.setdefault(e, set()).add((y, f))
                else:
                    p = (y, f or e in fault_events)
                    if p not in seen:
                        seen.add(p)
                        stack.append(p)
        memo[pair] = res
        return res

    q0 = frozenset({(g["init"], False)})
    dstates, dnext, stack = {q0}, {}, [q0]
    while stack:
        q = stack.pop()
        for e in observable:
            r = set()
            for p in q:
                r |= jumps(p).get(e, set())
            if r:
                r = frozenset(r)
                dnext[(q, e)] = r
                if r not in dstates:
                    dstates.add(r)
                    stack.append(r)
    nodes = {(q, a, b) for q in dstates for a in q for b in q if a[1] and not b[1]}
    succ = {v: [] for v in nodes}
    for q, a, b in nodes:
        for e in observable:
            if (q, e) in dnext:
                for a2 in jumps(a).get(e, ()):
                    for b2 in jumps(b).get(e, ()):
                        if not b2[1]:
                            succ[(q, a, b)].append((dnext[(q, e)], a2, b2))
    indeg = {v: 0 for v in nodes}
    for v in nodes:
        for w in succ[v]:
            indeg[w] += 1
    ready = [v for v in nodes if indeg[v] == 0]
    gone = 0
    while ready:
        v = ready.pop()
        gone += 1
        for w in succ[v]:
            indeg[w] -= 1
            if indeg[w] == 0:
                ready.append(w)
    return gone == len(nodes)


def random_plant(rng, n, observable, unobservable):
    edges = {}
    for x in range(n):
        for e in observable:
            if rng.random() < 0.45:
                edges[(x, e)] = rng.randrange(n)
        for e in unobservable:
            if x < n - 1 and rng.random() < 0.35:
                edges[(x, e)] = rng.randrange(x + 1, n)
        if not any(k[0] == x for k in edges):
            edges[(x, rng.choice(observable))] = rng.randrange(n)
    return {"init": 0, "delta": edges}


def check_witness(g, observable, faults, wit, reps=4):
    p1, c1, p2, c2 = wit
    assert len(c1) >= 1
    for k in range(reps):
        s1, s2 = p1 + c1 * k, p2 + c2 * k
        assert run(g, s1) is not None and run(g, s2) is not None
        assert any(e in faults for e in s1)
        assert not any(e in faults for e in s2)
        assert [e for e in s1 if e in observable] == [e for e in s2 if e in observable]
        tail = s1[min(i for i, e in enumerate(s1) if e in faults) + 1:]
        assert len(tail) >= k * len(c1)


def test_page_example_not_diagnosable():
    obs = {"a", "b", "c"}
    v0, states, edges = build_verifier(AMBIGUOUS, obs, {"f"})
    assert v0 == (0, False, 0)
    assert len(states) == 10
    assert sum(len(x) for x in edges.values()) == 13
    assert {v for v in states if v[1]} == {(3, True, 1), (3, True, 2), (4, True, 0), (5, True, 1), (5, True, 2)}
    assert not diagnosable(AMBIGUOUS, obs, {"f"})
    wit = witness(AMBIGUOUS, obs, {"f"})
    assert wit == (("a", "f", "b", "a"), ("b", "a"), ("a", "u", "b", "a"), ("u", "b", "a"))
    check_witness(AMBIGUOUS, obs, {"f"}, wit)
    v0, states, edges = build_verifier(DIAGNOSABLE, obs, {"f"})
    assert len(states) == 8 and sum(len(x) for x in edges.values()) == 10
    assert edges[(4, True, 0)] == []


def test_unobservable_cycle_breaks_the_test():
    # Pitfall: with an unobservable cycle in the normal part, copy 2 can loop alone while copy 1 waits after the fault.
    g = plant([(0, "f", 1), (0, "u", 2), (2, "u", 2), (1, "a", 1), (2, "b", 2)])
    v0, states, edges = build_verifier(g, {"a", "b"}, {"f"})
    assert ((1, True, 2), (None, "u")) in edges[(1, True, 2)]
    assert not diagnosable(g, {"a", "b"}, {"f"})
    # Yet every long run after the fault shows a and every normal run shows only b, so the fault is diagnosable.


def test_page_example_diagnosable():
    obs = {"a", "b", "c"}
    assert diagnosable(DIAGNOSABLE, obs, {"f"})
    assert witness(DIAGNOSABLE, obs, {"f"}) is None
    assert diagnosable_jiang(DIAGNOSABLE, obs, {"f"})
    assert not diagnosable_jiang(AMBIGUOUS, obs, {"f"})


def test_uncertain_diagnoser_cycle_is_diagnosable():
    assert diagnosable(UNCERTAIN, {"a", "b"}, {"f"})


def test_no_fault_and_fault_free_plant():
    g = plant([(0, "a", 1), (1, "u", 0)])
    assert diagnosable(g, {"a"}, set())
    assert diagnosable(g, {"a"}, {"f"})


def test_fault_without_observation_after_it():
    g = plant([(0, "a", 0), (0, "f", 1), (1, "a", 1)])
    assert not diagnosable(g, {"a"}, {"f"})
    check_witness(g, {"a"}, {"f"}, witness(g, {"a"}, {"f"}))


def test_random_against_diagnoser_and_jiang():
    rng = random.Random(17)
    observable = ["a", "b"]
    counts = [0, 0]
    for _ in range(600):
        g = random_plant(rng, 4, observable, ["u", "f"])
        got = diagnosable(g, set(observable), {"f"})
        assert got == oracle_diagnoser(g, set(observable), {"f"})
        assert got == diagnosable_jiang(g, set(observable), {"f"})
        if not got:
            check_witness(g, set(observable), {"f"}, witness(g, set(observable), {"f"}))
        counts[got] += 1
    assert min(counts) >= 50


def test_verifier_size_bound():
    rng = random.Random(23)
    for _ in range(200):
        n = rng.randrange(2, 7)
        g = random_plant(rng, n, ["a", "b", "c"], ["u", "f"])
        v0, states, edges = build_verifier(g, {"a", "b", "c"}, {"f"})
        assert len(states) <= 2 * n * n
        assert all(len(x) <= 5 + 2 for x in edges.values())
        assert sum(len(x) for x in edges.values()) <= 4 * n * n * 5
        flagged = [v for v in states if v[1]]
        assert len(flagged) <= n * n
        # The flag never goes back to False, so a cycle through a flagged state stays flagged.
        assert all(not v[1] or all(w[1] for w, _ in edges[v]) for v in states)
