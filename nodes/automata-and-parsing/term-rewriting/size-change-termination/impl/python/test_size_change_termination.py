# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/size-change-termination/. The authors are listed in prov/WBRKWD.jsonl.

import random

from size_change_termination import Graph, compose, make_graph, size_change_terminates


def descending_cycle(g: Graph) -> bool:
    """True if the arcs of a graph f -> f contain a cycle through a strict arc.

    Brute force: i -> j is on a cycle iff j reaches i, by plain search.
    """
    succ: dict[int, set[int]] = {}
    for i, j, _ in g.arcs:
        succ.setdefault(i, set()).add(j)

    def reaches(a: int, b: int) -> bool:
        seen, stack = {a}, [a]
        while stack:
            u = stack.pop()
            if u == b:
                return True
            for v in succ.get(u, ()):
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        return False

    return any(s and reaches(j, i) for i, j, s in g.arcs)


def closed_walks(graphs: list[Graph], max_len: int):
    """Yield (walk, composed graph) for every closed walk of length <= max_len."""
    stack = [((i,), g) for i, g in enumerate(graphs)]
    while stack:
        walk, g = stack.pop()
        if g.src == g.dst:
            yield walk, g
        if len(walk) < max_len:
            for i, h in enumerate(graphs):
                if h.src == g.dst:
                    stack.append((walk + (i,), compose(g, h)))


def check(graphs: list[Graph], max_len: int = 6) -> bool:
    res = size_change_terminates(graphs)
    if res.terminates:
        # Every periodic call sequence w^omega must have a descending thread.
        for walk, g in closed_walks(graphs, max_len):
            assert descending_cycle(g), walk
    else:
        assert res.witness is not None and res.walk is not None
        g = graphs[res.walk[0]]
        g = make_graph(g.src, g.dst, g.arcs)
        for i in res.walk[1:]:
            g = compose(g, graphs[i])
        assert g == res.witness
        assert g.src == g.dst and compose(g, g) == g
        assert not descending_cycle(g)
    return res.terminates


def G(src, dst, *arcs) -> Graph:
    return make_graph(src, dst, arcs)


def test_ackermann() -> None:
    graphs = [
        G("ack", "ack", (0, 0, True)),
        G("ack", "ack", (0, 0, False), (1, 1, True)),
        G("ack", "ack", (0, 0, True)),
    ]
    assert check(graphs)


def test_page_example() -> None:
    # p(m, n, r): r > 0 calls p(m, r - 1, n); n > 0 calls p(r, n - 1, m).
    g1 = G("p", "p", (0, 0, False), (2, 1, True), (1, 2, False))
    g2 = G("p", "p", (2, 0, False), (1, 1, True), (0, 2, False))
    assert check([g1, g2])
    res = size_change_terminates([g1, g2])
    assert res.terminates


def test_swap_loops() -> None:
    res = size_change_terminates([G("f", "f", (0, 1, False), (1, 0, False))])
    assert not res.terminates
    assert res.witness == G("f", "f", (0, 0, False), (1, 1, False))
    assert check([G("f", "f", (0, 1, True), (1, 0, False))])


def test_mutual_recursion() -> None:
    # f(x) calls g(x - 1); g(y) calls f(y): every cycle goes through the decrease.
    assert check([G("f", "g", (0, 0, True)), G("g", "f", (0, 0, False))])
    assert not check([G("f", "g", (0, 0, False)), G("g", "f", (0, 0, False))])


def test_edges() -> None:
    assert size_change_terminates([]).terminates
    assert size_change_terminates([G("f", "g", (0, 0, False))]).terminates
    res = size_change_terminates([G("f", "f")])
    assert not res.terminates and res.walk == (0,)


def test_random_against_walks() -> None:
    rng = random.Random(7)
    seen = {True: 0, False: 0}
    for _ in range(600):
        names = ["f", "g"][: rng.randint(1, 2)]
        arity = {f: rng.randint(1, 3) for f in names}
        graphs = []
        for _ in range(rng.randint(1, 3)):
            a, b = rng.choice(names), rng.choice(names)
            arcs = [
                (i, j, rng.random() < 0.4)
                for i in range(arity[a])
                for j in range(arity[b])
                if rng.random() < 0.4
            ]
            graphs.append(make_graph(a, b, arcs))
        seen[check(graphs)] += 1
    assert seen[True] > 50 and seen[False] > 50
