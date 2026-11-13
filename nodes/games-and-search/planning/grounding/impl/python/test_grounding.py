# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/grounding/. The authors are listed in prov/E2ANZJ.jsonl.

import random
from itertools import product

from grounding import (
    applicable,
    ground_brute,
    ground_join,
    ground_reachable,
    move_actions,
    reachable,
    schema,
    static_predicates,
)

LOGISTICS = [
    schema("drive", [("?t", "truck"), ("?from", "location"), ("?to", "location")],
           pre=[("at", "?t", "?from"), ("road", "?from", "?to")], add=[("at", "?t", "?to")], delete=[("at", "?t", "?from")]),
    schema("load", [("?p", "package"), ("?t", "truck"), ("?l", "location")],
           pre=[("at", "?p", "?l"), ("at", "?t", "?l")], add=[("in", "?p", "?t")], delete=[("at", "?p", "?l")]),
    schema("unload", [("?p", "package"), ("?t", "truck"), ("?l", "location")],
           pre=[("in", "?p", "?t"), ("at", "?t", "?l")], add=[("at", "?p", "?l")], delete=[("in", "?p", "?t")]),
]

MOVE = [
    schema("move", [("?b", "block"), ("?x", "block"), ("?y", "block")],
           pre=[("on", "?b", "?x"), ("clear", "?b"), ("clear", "?y")], add=[("on", "?b", "?y"), ("clear", "?x")],
           delete=[("on", "?b", "?x"), ("clear", "?y")], distinct=[("?b", "?x"), ("?b", "?y"), ("?x", "?y")]),
    schema("move-to-table", [("?b", "block"), ("?x", "block")],
           pre=[("on", "?b", "?x"), ("clear", "?b")], add=[("ontable", "?b"), ("clear", "?x")], delete=[("on", "?b", "?x")],
           distinct=[("?b", "?x")]),
    schema("move-from-table", [("?b", "block"), ("?x", "block")],
           pre=[("ontable", "?b"), ("clear", "?b"), ("clear", "?x")], add=[("on", "?b", "?x")], delete=[("ontable", "?b"), ("clear", "?x")],
           distinct=[("?b", "?x")]),
]


def ring(locs):
    k = len(locs)
    return {("road", locs[i], locs[(i + 1) % k]) for i in range(k)} | {("road", locs[(i + 1) % k], locs[i]) for i in range(k)}


def as_set(actions):
    return {(a.name, a.pre, a.add, a.delete) for a in actions}


def test_static_predicates():
    assert static_predicates(LOGISTICS) == {"road"}
    assert static_predicates(MOVE) == set()


def test_exact_counts_logistics():
    objects = {"truck": ["t1", "t2"], "location": ["l1", "l2", "l3", "l4"], "package": ["p1", "p2", "p3"]}
    init = ring(objects["location"]) | {("at", "t1", "l1"), ("at", "t2", "l3"), ("at", "p1", "l1"), ("at", "p2", "l2"), ("at", "p3", "l4")}
    all_tuples = sum(len(list(product(*(objects[t] for _, t in s.params)))) for s in LOGISTICS)
    assert all_tuples == 2 * 4 * 4 + 2 * (3 * 2 * 4)  # 80
    brute = ground_brute(LOGISTICS, objects, init)
    join = ground_join(LOGISTICS, objects, init)
    assert len(brute) == len(join) == 2 * 8 + 2 * (3 * 2 * 4)  # 64: 2 trucks times 8 directed roads, plus loads and unloads
    assert as_set(brute) == as_set(join)
    assert len(as_set(join)) == len(join)


def test_join_equals_brute_on_random_road_maps():
    rng = random.Random(99)
    for _ in range(30):
        locs = [f"l{i}" for i in range(rng.randint(2, 5))]
        roads = {("road", a, b) for a in locs for b in locs if a != b and rng.random() < 0.4}
        objects = {"truck": ["t1", "t2"][: rng.randint(1, 2)], "location": locs, "package": ["p1", "p2"]}
        init = roads | {("at", t, rng.choice(locs)) for t in objects["truck"]} | {("at", p, rng.choice(locs)) for p in objects["package"]}
        brute = ground_brute(LOGISTICS, objects, init)
        join = ground_join(LOGISTICS, objects, init)
        assert as_set(brute) == as_set(join)
        assert len(join) == len(objects["truck"]) * len(roads) + 2 * len(objects["package"]) * len(objects["truck"]) * len(locs)


def test_lifted_move_domain_matches_hand_grounding():
    for n in range(1, 6):
        blocks = "abcde"[:n]
        objects = {"block": list(blocks)}
        lifted = ground_join(MOVE, objects, set())
        assert len(lifted) == n * (n - 1) * (n - 2) + 2 * n * (n - 1) == n * n * (n - 1)
        assert {(a.pre, a.add, a.delete) for a in lifted} == {(a.pre, a.add, a.delete) for a in move_actions(blocks)}
        assert as_set(lifted) == as_set(ground_brute(MOVE, objects, set()))


def test_relaxed_reachability_keeps_every_applicable_action():
    objects = {"truck": ["t1", "t2"], "location": ["l1", "l2", "l3", "l4"], "package": ["p1", "p2"]}
    roads = {("road", "l1", "l2"), ("road", "l2", "l1"), ("road", "l3", "l4"), ("road", "l4", "l3")}
    init = frozenset(roads | {("at", "t1", "l1"), ("at", "t2", "l3"), ("at", "p1", "l1"), ("at", "p2", "l4")})
    join = ground_join(LOGISTICS, objects, init)
    kept = ground_reachable(LOGISTICS, objects, init)
    assert len(join) == 2 * 4 + 2 * (2 * 2 * 4)  # 40
    assert len(kept) == 12
    states = reachable(init, join)
    used = {a.name for a in join if any(applicable(s, a) for s in states)}
    assert used <= {a.name for a in kept}
    assert used == {a.name for a in kept}
