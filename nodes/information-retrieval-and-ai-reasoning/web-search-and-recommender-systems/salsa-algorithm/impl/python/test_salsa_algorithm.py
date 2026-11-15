# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/salsa-algorithm/. The authors are listed in prov/XD0VVF.jsonl.

import random
from fractions import Fraction

import pytest

from salsa_algorithm import authority_matrix, authority_step, clean_links, hub_step, salsa, salsa_power

# The example of the page: hubs 0 to 3 link to authorities 9 and 10, hubs 4 to 8 link to 11, and 0 also links to 11.
BLOCK = [(q, p) for q in range(4) for p in (9, 10)]
STAR = [(q, 11) for q in range(4, 9)]
CONNECTED = BLOCK + STAR + [(0, 11)]


def random_graph(rng: random.Random, n: int, prob: float) -> list[tuple[int, int]]:
    return [(q, p) for q in range(n) for p in range(n) if q != p and rng.random() < prob]


def components(n: int, arcs: list[tuple[int, int]]) -> list[set[int]]:
    """Authority sets of the connected components of the bipartite graph, by a plain search."""
    adj: dict[tuple[str, int], set[tuple[str, int]]] = {}
    for q, p in arcs:
        adj.setdefault(("h", q), set()).add(("a", p))
        adj.setdefault(("a", p), set()).add(("h", q))
    seen: set[tuple[str, int]] = set()
    comps = []
    for v in sorted(adj):
        if v in seen:
            continue
        stack, comp = [v], set()
        seen.add(v)
        while stack:
            u = stack.pop()
            if u[0] == "a":
                comp.add(u[1])
            for w in adj[u]:
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
        comps.append(comp)
    return comps


def stationary(pa: dict[tuple[int, int], Fraction], nodes: list[int]) -> list[Fraction]:
    """Solve pi P = pi with sum(pi) = 1 exactly, by Gaussian elimination."""
    k = len(nodes)
    rows = [[(pa.get((nodes[i], nodes[j]), Fraction(0)) - (1 if i == j else 0)) for i in range(k)] + [Fraction(0)] for j in range(k)]
    rows[-1] = [Fraction(1)] * k + [Fraction(1)]
    for c in range(k):
        piv = next(r for r in range(c, k) if rows[r][c] != 0)
        rows[c], rows[piv] = rows[piv], rows[c]
        for r in range(k):
            if r != c and rows[r][c] != 0:
                f = rows[r][c] / rows[c][c]
                rows[r] = [x - f * y for x, y in zip(rows[r], rows[c])]
    return [rows[i][k] / rows[i][i] for i in range(k)]


def test_example_connected() -> None:
    h, a = salsa(12, CONNECTED, exact=True)
    assert [a[p] for p in (9, 10, 11)] == [Fraction(2, 7), Fraction(2, 7), Fraction(3, 7)]
    assert h[0] == Fraction(3, 14) and h[1] == h[2] == h[3] == Fraction(1, 7)
    assert all(h[q] == Fraction(1, 14) for q in range(4, 9))
    hp, ap, _ = salsa_power(12, CONNECTED)
    assert all(abs(float(x) - y) < 1e-9 for x, y in zip(a + h, ap + hp))


def test_example_two_components() -> None:
    h, a = salsa(12, BLOCK + STAR, exact=True)
    assert [a[p] for p in (9, 10, 11)] == [Fraction(1, 3)] * 3
    assert all(h[q] == Fraction(1, 9) for q in range(9))


def test_closed_form_matches_power_iteration() -> None:
    rng = random.Random(2)
    for _ in range(80):
        n = rng.randrange(1, 10)
        edges = random_graph(rng, n, rng.choice([0.15, 0.3, 0.6]))
        h, a = salsa(n, edges)
        hp, ap, _ = salsa_power(n, edges)
        assert all(abs(x - y) < 1e-9 for x, y in zip(h + a, hp + ap))


def test_closed_form_is_exactly_stationary() -> None:
    rng = random.Random(4)
    for _ in range(80):
        n = rng.randrange(1, 10)
        edges = random_graph(rng, n, 0.3)
        arcs = clean_links(n, edges)
        h, a = salsa(n, edges, exact=True)
        assert authority_step(n, arcs, a) == a
        assert hub_step(n, arcs, h) == h
        if arcs:
            assert sum(a) == 1 and sum(h) == 1


def test_connected_component_gives_in_degree() -> None:
    # On a connected bipartite graph the unique stationary distribution of P_A is in(p) / m.
    rng = random.Random(9)
    done = 0
    while done < 30:
        n = rng.randrange(2, 9)
        arcs = clean_links(n, random_graph(rng, n, 0.45))
        comps = components(n, arcs)
        if len(comps) != 1:
            continue
        done += 1
        auths = sorted(comps[0])
        pa = authority_matrix(n, arcs)
        for i in auths:
            assert sum(pa.get((i, j), Fraction(0)) for j in auths) == 1
            assert pa[(i, i)] > 0
        pi = stationary(pa, auths)
        inn = {p: sum(1 for _, x in arcs if x == p) for p in auths}
        assert pi == [Fraction(inn[p], len(arcs)) for p in auths]
        _, a = salsa(n, arcs, exact=True)
        assert [a[p] for p in auths] == pi


def test_component_mass_is_preserved() -> None:
    rng = random.Random(6)
    for _ in range(40):
        n = rng.randrange(2, 10)
        arcs = clean_links(n, random_graph(rng, n, 0.2))
        auths = sorted({p for _, p in arcs})
        if not auths:
            continue
        x = [Fraction(1, len(auths)) if p in auths else Fraction(0) for p in range(n)]
        for _ in range(3):
            x = authority_step(n, arcs, x)
        _, a = salsa(n, arcs, exact=True)
        for comp in components(n, arcs):
            share = Fraction(len(comp), len(auths))
            assert sum(x[p] for p in comp) == share
            assert sum(a[p] for p in comp) == share


def test_links_are_cleaned_and_empty_graph() -> None:
    assert clean_links(3, [(0, 1), (0, 1), (2, 2)]) == [(0, 1)]
    assert salsa(3, [(0, 1), (0, 1), (2, 2)], exact=True) == salsa(3, [(0, 1)], exact=True)
    assert salsa(3, [], exact=True) == ([0, 0, 0], [0, 0, 0])
    with pytest.raises(ValueError):
        salsa(2, [(0, 5)])
