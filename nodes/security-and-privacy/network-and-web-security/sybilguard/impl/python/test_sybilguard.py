# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sybilguard/. The authors are listed in prov/QFN0T8.jsonl.

import random

from sybilguard import own_routes, registries, route, routing_tables, verify

# The worked example: honest A..F, Sybil X, Y, Z, one attack edge F-X.
EDGES = ["AB", "AC", "BC", "BD", "CE", "DE", "DF", "EF", "FX", "XY", "XZ", "YZ"]
HONEST = set("ABCDEF")


def build(edges) -> dict:
    adj: dict = {}
    for a, b in edges:
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    return {v: sorted(n) for v, n in sorted(adj.items())}


def test_example() -> None:
    adj = build(EDGES)
    perm = routing_tables(adj, random.Random(4))
    assert [adj["F"][perm["F"][i]] for i in range(3)] == ["X", "E", "D"]  # from D, E, X
    w = 3
    reg = registries(adj, perm, w, HONEST, {("X", "F"): ["X", "Y", "Z"]})
    assert reg[("X", "F")] == ["X", "Y", "Z"]
    assert reg[("F", "D")] == ["F", "X", "Y"]
    assert reg[("D", "E")] == ["D", "F", "X"]
    polluted = sum(1 for t in reg.values() for e in t if e not in HONEST)
    assert polluted == 3 + 2 + 1
    assert {e for t in reg.values() for e in t} - HONEST == {"X", "Y", "Z"}  # g * w = 3 names
    assert own_routes(adj, perm, "A", w) == [["B", "D", "F"], ["C", "A", "B"]]
    assert own_routes(adj, perm, "E", w) == [["C", "E", "D"], ["D", "B", "C"], ["F", "E", "C"]]
    assert verify(adj, perm, w, reg, "A", "E", own_routes(adj, perm, "E", w), HONEST)
    assert verify(adj, perm, w, reg, "A", "Z", [["F"]], HONEST)  # one route of two accepts
    assert not verify(adj, perm, w, reg, "A", "Z", [sorted(HONEST)], HONEST)
    assert not verify(adj, perm, w, reg, "A", "W", [["F"]], HONEST)  # W is in no registry


def test_edge_cases() -> None:
    adj = build(["AB"])
    perm = routing_tables(adj, random.Random(0))
    assert route(adj, perm, "A", 0, 4) == ["B", "A", "B", "A"]
    reg = registries(adj, perm, 1)
    assert reg == {("A", "B"): ["A"], ("B", "A"): ["B"]}
    # With w = 1 the routes A->B and B->A share no node, so A rejects its only friend.
    assert not verify(adj, perm, 1, reg, "A", "B", own_routes(adj, perm, "B", 1))
    reg = registries(adj, perm, 2)
    assert reg == {("A", "B"): ["A", "B"], ("B", "A"): ["B", "A"]}
    assert verify(adj, perm, 2, reg, "A", "B", own_routes(adj, perm, "B", 2))
    assert not verify(adj, perm, 2, reg, "A", "C", [["B"]])
    # A route on a triangle with the identity table goes round and round.
    adj = build(["AB", "BC", "CA"])
    perm = {"A": [1, 0], "B": [1, 0], "C": [1, 0]}
    assert route(adj, perm, "A", 0, 4) == ["B", "C", "A", "B"]


def random_graph(rng: random.Random, n: int, lo: int = 0, extra: int = 2) -> list[tuple[int, int]]:
    edges = {(lo + v, lo + rng.randrange(v)) for v in range(1, n)}
    for _ in range(extra * n):
        a, b = rng.randrange(n), rng.randrange(n)
        if a != b:
            edges.add((lo + max(a, b), lo + min(a, b)))
    return sorted(edges)


def test_back_traceable() -> None:
    """Every slot (directed edge, hop) is used by exactly one honest route, and the registries match it."""
    rng = random.Random(2006)
    for _ in range(500):
        n = rng.randrange(2, 12)
        adj = build(random_graph(rng, n))
        perm = routing_tables(adj, rng)
        w = rng.randrange(1, 7)
        owner: dict = {}
        for s in adj:
            for j in range(len(adj[s])):
                nodes = [s] + route(adj, perm, s, j, w)
                hops = list(zip(nodes, nodes[1:]))
                for i, e in enumerate(hops):
                    assert (e, i) not in owner
                    owner[(e, i)] = s
                first_repeat = next((i for i, e in enumerate(hops) if e in hops[:i]), None)
                if first_repeat is not None:  # a loop closes only on the first edge
                    assert hops[first_repeat] == hops[0]
        assert len(owner) == w * sum(len(a) for a in adj.values())
        reg = registries(adj, perm, w)
        for (p, x), table in reg.items():
            assert table == [owner[((p, x), i)] for i in range(w)]


def two_regions(rng: random.Random, nh: int, ns: int, g: int) -> tuple[dict, set, list]:
    edges = random_graph(rng, nh) + random_graph(rng, ns, nh)
    attack: set = set()
    while len(attack) < g:
        attack.add((rng.randrange(nh), nh + rng.randrange(ns)))
    return build(edges + sorted(attack)), set(range(nh)), sorted(attack)


def test_sybil_bound() -> None:
    """Whatever the adversary sends, at most g * w Sybil names reach honest registries,
    and a verifier with fewer than half of its routes escaping accepts no other Sybil name."""
    rng = random.Random(2008)
    for _ in range(100):
        nh, ns, g = rng.randrange(4, 16), rng.randrange(2, 8), rng.randrange(1, 4)
        adj, honest, attack = two_regions(rng, nh, ns, g)
        perm = routing_tables(adj, rng)
        w = rng.randrange(1, 6)
        names = [("sybil", i) for i in range(4 * w * g + 4)]
        forged = {(s, h): rng.sample(names, rng.randrange(0, 2 * w)) for h, s in attack}
        reg = registries(adj, perm, w, honest, forged)
        seen = {e for t in reg.values() for e in t if e not in honest}
        assert len(seen) <= g * w
        assert seen <= {e for t in forged.values() for e in t[:w]}
        for v in honest:
            routes = own_routes(adj, perm, v, w)
            if 2 * sum(any(y not in honest for y in r) for r in routes) >= len(routes):
                continue
            for name in rng.sample(names, 6):
                claims = [[[x]] for x in adj] + [[list(adj)]]
                if any(verify(adj, perm, w, reg, v, name, c, honest) for c in claims):
                    assert name in seen


def test_honest_acceptance_measurement() -> None:
    """On random honest graphs of 60 nodes most honest pairs accept each other (a measurement)."""
    rng = random.Random(267)
    ok = total = 0
    for _ in range(3):
        adj = build(random_graph(rng, 60, extra=2))
        perm = routing_tables(adj, rng)
        w = 16
        reg = registries(adj, perm, w)
        routes = {s: own_routes(adj, perm, s, w) for s in adj}
        for v in adj:
            for s in rng.sample(sorted(adj), 10):
                if s != v:
                    ok += verify(adj, perm, w, reg, v, s, routes[s])
                    total += 1
    assert ok / total > 0.8
