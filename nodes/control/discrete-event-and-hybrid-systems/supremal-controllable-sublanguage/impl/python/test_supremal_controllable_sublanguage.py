# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/supremal-controllable-sublanguage/. The authors are listed in prov/1CMXJG.jsonl.

import random

from supremal_controllable_sublanguage import disabled_events, product, supremal_controllable


def step(a, q, e):
    return a["delta"].get((q, e))


def strings_of(a, events, length):
    """All strings s with |s| <= length in L(a), each with the state it reaches."""
    if a["init"] is None:
        return []
    out = [((), a["init"])]
    frontier = [((), a["init"])]
    for _ in range(length):
        nxt = []
        for s, q in frontier:
            for e in events:
                r = step(a, q, e)
                if r is not None:
                    nxt.append((s + (e,), r))
        out.extend(nxt)
        frontier = nxt
    return out


def run(a, s):
    q = a["init"]
    for e in s:
        if q is None:
            return None
        q = step(a, q, e)
    return q


def reach(states, succ, start):
    seen = {start} if start in states else set()
    stack = list(seen)
    while stack:
        x = stack.pop()
        for y in succ(x):
            if y in states and y not in seen:
                seen.add(y)
                stack.append(y)
    return seen


def brute_sup_states(g, h, unc, events):
    """The union of all sets X of product states whose restriction is trim and has no bad state."""
    a = product(h, g)
    order = sorted(a["states"], key=repr)
    succ = {x: [a["delta"][(x, e)] for e in events if (x, e) in a["delta"]] for x in order}
    pred = {x: [] for x in order}
    for x in order:
        for y in succ[x]:
            pred[y].append(x)
    best = set()
    for mask in range(1, 1 << len(order)):
        xs = {order[i] for i in range(len(order)) if mask >> i & 1}
        if a["init"] not in xs:
            continue
        if reach(xs, lambda x: succ[x], a["init"]) != xs:
            continue
        co = set()
        for m in xs & a["marked"]:
            co |= reach(xs, lambda x: pred[x], m)
        if co != xs:
            continue
        ok = True
        for x in xs:
            for e in unc:
                if (x[1], e) in g["delta"] and a["delta"].get((x, e)) not in xs:
                    ok = False
        if ok:
            best |= xs
    return best


def random_automaton(rng, n, events, p=0.55, pm=0.5):
    delta = {(q, e): rng.randrange(n) for q in range(n) for e in events if rng.random() < p}
    marked = {q for q in range(n) if rng.random() < pm} or {rng.randrange(n)}
    return {"init": 0, "delta": delta, "marked": marked}


def check_string_level(g, h, unc, sup, events, length):
    """L(sup) is in L(G), Lm(sup) is in Lm(H) & Lm(G), and L(sup) is controllable, on all strings up to `length`."""
    for s, q in strings_of(sup, events, length):
        gq, hq = run(g, s), run(h, s)
        assert gq is not None and hq is not None
        if q in sup["marked"]:
            assert gq in g["marked"] and hq in h["marked"]
        if len(s) < length:
            for e in unc:
                if step(g, gq, e) is not None:
                    assert step(sup, q, e) is not None


def nonblocking(sup):
    if sup["init"] is None:
        return True
    succ = {}
    for (x, _), y in sup["delta"].items():
        succ.setdefault(x, []).append(y)
    for x in sup["states"]:
        seen = reach(sup["states"], lambda z: succ.get(z, []), x)
        if not seen & sup["marked"]:
            return False
    return True


def factory():
    d = {}
    for m1 in "IW":
        for m2 in "IW":
            s = m1 + m2
            if m1 == "I":
                d[(s, "a1")] = "W" + m2
            else:
                d[(s, "b1")] = "I" + m2
            if m2 == "I":
                d[(s, "a2")] = m1 + "W"
            else:
                d[(s, "b2")] = m1 + "I"
    g = {"init": "II", "delta": d, "marked": {"II"}}
    h = {"init": 0, "delta": {(0, "b1"): 1, (1, "a2"): 0, (0, "a1"): 0, (1, "a1"): 1, (0, "b2"): 0, (1, "b2"): 1}, "marked": {0}}
    return g, h


def three_round():
    gd = {(0, "a"): 1, (1, "u"): 2, (2, "b"): 3, (3, "v"): 4, (4, "d"): 0, (0, "e"): 0, (1, "c"): 0}
    g = {"init": 0, "delta": gd, "marked": {0}}
    h = {"init": 0, "delta": {k: v for k, v in gd.items() if k[1] != "v"}, "marked": {0, 1, 2, 3, 4}}
    return g, h


def test_page_example_three_rounds():
    g, h = three_round()
    sup = supremal_controllable(g, h, {"u", "v"})
    assert sup["states"] == {(0, 0)}
    assert sup["delta"] == {((0, 0), "e"): (0, 0)}
    marked = [s for s, q in strings_of(sup, "abcdeuv", 8) if q in sup["marked"]]
    assert sorted(marked) == [("e",) * k for k in range(9)]


def test_one_round_without_retrim_is_not_enough():
    g, h = three_round()
    a = product(h, g)
    keep = {x for x in a["states"] if x != (3, 3) and x != (2, 2)}
    one_round = {"init": a["init"], "states": keep, "marked": a["marked"] & keep,
                 "delta": {(x, e): y for (x, e), y in a["delta"].items() if x in keep and y in keep}}
    s = ("a",)
    assert run(one_round, s) is not None and step(g, run(g, s), "u") is not None
    assert step(one_round, run(one_round, s), "u") is None


def test_factory_buffer():
    g, h = factory()
    sup = supremal_controllable(g, h, {"b1", "b2"})
    assert len(product(h, g)["states"]) == 8
    assert sup["states"] == {(0, "II"), (0, "IW"), (0, "WI"), (0, "WW"), (1, "II"), (1, "IW")}
    assert len(sup["delta"]) == 8
    dis = disabled_events(sup, g)
    assert dis[(1, "II")] == {"a1"} and dis[(1, "IW")] == {"a1"}
    assert dis[(0, "II")] == {"a2"} and dis[(0, "WI")] == {"a2"}
    assert nonblocking(sup)
    check_string_level(g, h, {"b1", "b2"}, sup, ["a1", "b1", "a2", "b2"], 8)


def test_empty_result():
    g = {"init": 0, "delta": {(0, "u"): 1, (1, "a"): 0}, "marked": {0, 1}}
    h = {"init": 0, "delta": {(0, "a"): 0}, "marked": {0}}
    sup = supremal_controllable(g, h, {"u"})
    assert sup["init"] is None and sup["states"] == set() and sup["delta"] == {}


def test_all_controllable_gives_trim_product():
    rng = random.Random(7)
    for _ in range(100):
        g = random_automaton(rng, 3, "abc")
        h = random_automaton(rng, 2, "abc")
        sup = supremal_controllable(g, h, set())
        a = product(h, g)
        assert sup["states"] == brute_sup_states(g, h, set(), "abc")
        assert sup["states"] <= a["states"]


def test_random_against_subset_brute_force():
    rng = random.Random(2024)
    events = ["a", "b", "c", "u"]
    unc = {"u"}
    strict = 0
    for _ in range(1500):
        g = random_automaton(rng, 3, events, p=0.6, pm=0.5)
        h = random_automaton(rng, 3, events, p=0.8, pm=0.6)
        sup = supremal_controllable(g, h, unc)
        assert sup["states"] == brute_sup_states(g, h, unc, events)
        assert nonblocking(sup)
        strict += 0 < len(sup["states"]) < len(product(h, g)["states"])
    assert strict >= 100


def test_random_two_uncontrollable_events():
    rng = random.Random(31)
    events = ["a", "b", "u", "v"]
    unc = {"u", "v"}
    for _ in range(500):
        g = random_automaton(rng, 3, events)
        h = random_automaton(rng, 2, events)
        sup = supremal_controllable(g, h, unc)
        assert sup["states"] == brute_sup_states(g, h, unc, events)
        assert nonblocking(sup)


def test_random_strings_up_to_length_8():
    rng = random.Random(99)
    events = ["a", "b", "u"]
    unc = {"u"}
    nonempty = 0
    for _ in range(60):
        g = random_automaton(rng, 3, events, p=0.5)
        h = random_automaton(rng, 3, events, p=0.6)
        sup = supremal_controllable(g, h, unc)
        check_string_level(g, h, unc, sup, events, 8)
        nonempty += sup["init"] is not None
    assert nonempty >= 10
