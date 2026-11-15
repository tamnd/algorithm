# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/diagnoser-automaton/. The authors are listed in prov/8VN8F2.jsonl.

import itertools
import random

from diagnoser_automaton import diagnosable, diagnoser, has_uncertain_cycle, observe, verdict

N = frozenset()
F = frozenset({"F"})


def plant(edges, init=0):
    return {"init": init, "delta": {(x, e): y for x, e, y in edges}}


# The worked example of the page: the normal cycle a u b, and a fault after a.
EXAMPLE = plant([(0, "a", 1), (1, "u", 2), (2, "b", 0), (1, "f", 3), (3, "b", 4), (4, "c", 4)])
# Diagnosable, but the diagnoser has a cycle of uncertain states.
UNCERTAIN = plant([(1, "a", 1), (1, "f", 5), (5, "a", 2), (2, "b", 6), (6, "b", 6)], init=1)
# Not diagnosable: after the fault the plant shows a b a b ... as the normal plant does.
AMBIGUOUS = plant([(0, "a", 1), (1, "u", 2), (2, "b", 0), (1, "f", 3), (3, "b", 4), (4, "a", 5), (5, "b", 4)])


def brute_states(g, observable, faults, max_obs):
    """Group the strings of L(G) that end with an observable event (or are empty) by their projection."""
    out = {}
    for (x, e), y in g["delta"].items():
        out.setdefault(x, []).append((e, y))
    groups = {(): {(g["init"], N)}}
    stack = [(g["init"], N, ())]
    while stack:
        x, label, obs = stack.pop()
        for e, y in out.get(x, []):
            if e in observable:
                if len(obs) < max_obs:
                    groups.setdefault(obs + (e,), set()).add((y, label))
                    stack.append((y, label, obs + (e,)))
            else:
                stack.append((y, label | {faults[e]} if e in faults else label, obs))
    return groups


def oracle_verifier(g, observable, fault_events):
    """An independent twin plant: a cycle of states (x, faulty, y) with the flag set means not diagnosable."""
    out = {}
    for (x, e), y in g["delta"].items():
        out.setdefault(x, {})[e] = y
    start = (g["init"], False, g["init"])
    seen = {start}
    stack = [start]
    succ = {}
    while stack:
        x, f, y = v = stack.pop()
        nxt = []
        for e, x2 in out.get(x, {}).items():
            if e not in observable:
                nxt.append((x2, f or e in fault_events, y))
            elif e in out.get(y, {}):
                nxt.append((x2, f, out[y][e]))
        for e, y2 in out.get(y, {}).items():
            if e not in observable and e not in fault_events:
                nxt.append((x, f, y2))
        succ[v] = nxt
        for w in nxt:
            if w not in seen:
                seen.add(w)
                stack.append(w)
    nodes = {v for v in seen if v[1]}
    color = {}
    for root in nodes:
        if root in color:
            continue
        color[root] = 1
        it = [(root, iter(succ[root]))]
        while it:
            v, children = it[-1]
            for w in children:
                if w not in nodes:
                    continue
                if color.get(w) == 1:
                    return False
                if w not in color:
                    color[w] = 1
                    it.append((w, iter(succ[w])))
                    break
            else:
                color[v] = 2
                it.pop()
    return True


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


def test_page_example():
    d = diagnoser(EXAMPLE, {"a", "b", "c"}, {"f": "F"})
    q0 = frozenset({(0, N)})
    q1 = frozenset({(1, N)})
    q2 = frozenset({(0, N), (4, F)})
    q3 = frozenset({(4, F)})
    assert d["states"] == {q0, q1, q2, q3}
    assert d["delta"] == {(q0, "a"): q1, (q1, "b"): q2, (q2, "a"): q1, (q2, "c"): q3, (q3, "c"): q3}
    assert [verdict(q, "F") for q in (q0, q1, q2, q3)] == ["N", "N", "uncertain", "F"]
    assert observe(d, "abababc") == q3
    assert observe(d, "aa") is None
    assert diagnosable(EXAMPLE, {"a", "b", "c"}, {"f": "F"}, "F")


def test_uncertain_cycle_but_diagnosable():
    d = diagnoser(UNCERTAIN, {"a", "b"}, {"f": "F"})
    assert len(d["states"]) == 3
    assert has_uncertain_cycle(UNCERTAIN, {"a", "b"}, {"f": "F"}, "F")
    assert diagnosable(UNCERTAIN, {"a", "b"}, {"f": "F"}, "F")


def test_not_diagnosable():
    assert not diagnosable(AMBIGUOUS, {"a", "b"}, {"f": "F"}, "F")
    d = diagnoser(AMBIGUOUS, {"a", "b"}, {"f": "F"})
    assert verdict(observe(d, "abababab"), "F") == "uncertain"


def test_no_fault_event():
    g = plant([(0, "a", 1), (1, "u", 0)])
    d = diagnoser(g, {"a"}, {})
    assert all(verdict(q, "F") == "N" for q in d["states"])
    assert diagnosable(g, {"a"}, {}, "F")


def test_two_fault_types():
    g = plant([(0, "f1", 1), (0, "f2", 2), (1, "a", 3), (2, "a", 4), (3, "b", 3), (4, "c", 4)])
    faults = {"f1": 1, "f2": 2}
    d = diagnoser(g, {"a", "b", "c"}, faults)
    q = observe(d, "a")
    assert q == frozenset({(3, frozenset({1})), (4, frozenset({2}))})
    assert verdict(q, 1) == "uncertain" and verdict(observe(d, "ab"), 1) == "F"
    assert diagnosable(g, {"a", "b", "c"}, faults, 1) and diagnosable(g, {"a", "b", "c"}, faults, 2)


def test_states_against_brute_force():
    rng = random.Random(11)
    observable = ["a", "b"]
    for _ in range(300):
        g = random_plant(rng, 4, observable, ["u", "f"])
        d = diagnoser(g, set(observable), {"f": "F"})
        groups = brute_states(g, set(observable), {"f": "F"}, 4)
        for k in range(5):
            for word in itertools.product(observable, repeat=k):
                q = observe(d, word)
                if word in groups:
                    assert q == frozenset(groups[word])
                else:
                    assert q is None


def test_random_against_twin_plant():
    rng = random.Random(5)
    observable = ["a", "b"]
    counts = [0, 0]
    for _ in range(600):
        g = random_plant(rng, 4, observable, ["u", "f"])
        got = diagnosable(g, set(observable), {"f": "F"}, "F")
        assert got == oracle_verifier(g, set(observable), {"f"})
        counts[got] += 1
    assert min(counts) >= 50


def test_random_two_types_against_twin_plant():
    rng = random.Random(8)
    observable = ["a", "b"]
    faults = {"f": 1, "g": 2}
    for _ in range(300):
        g = random_plant(rng, 4, observable, ["f", "g", "u"])
        for kind, events in ((1, {"f"}), (2, {"g"})):
            assert diagnosable(g, set(observable), faults, kind) == oracle_verifier(g, set(observable), events)
