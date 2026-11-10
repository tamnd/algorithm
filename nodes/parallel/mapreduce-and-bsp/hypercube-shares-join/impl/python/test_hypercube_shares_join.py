# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hypercube-shares-join/. The authors are listed in prov/38S9XN.jsonl.

import math
import random
from collections import Counter

from hypercube_shares_join import (best_integer_shares, chain_shares, communication, shares_join,
                                   triangle_shares, triangles_brute_force)

TRI = [(1, ("A", "B")), (1, ("B", "C")), (1, ("C", "A"))]


def triangle_query(r_rel, s_rel, t_rel):
    return [(("A", "B"), r_rel), (("B", "C"), s_rel), (("C", "A"), t_rel)]


def random_edges(rng, n_vertices, m, zipf=False):
    if zipf:
        w = [1 / i for i in range(1, n_vertices + 1)]
        return [tuple(rng.choices(range(n_vertices), weights=w, k=2)) for _ in range(m)]
    return [(rng.randrange(n_vertices), rng.randrange(n_vertices)) for _ in range(m)]


def test_lagrange_shares_of_the_triangle():
    x, cost = triangle_shares(10**6, 10**6, 10**6, 1000)
    assert all(math.isclose(v, 10) for v in x.values()) and math.isclose(cost, 3 * 10**7)
    for r, s, t, k in [(1, 1, 1, 64), (8, 1, 1, 64), (5, 7, 11, 1000)]:
        x, cost = triangle_shares(r, s, t, k)
        assert math.isclose(math.prod(x.values()), k)
        assert math.isclose(communication([(r, ("A", "B")), (s, ("B", "C")), (t, ("C", "A"))], x), cost)
        _, best_int = best_integer_shares([(r, ("A", "B")), (s, ("B", "C")), (t, ("C", "A"))], ["A", "B", "C"], k)
        assert cost <= best_int + 1e-9
    assert best_integer_shares(TRI, ["A", "B", "C"], 64) == ({"A": 4, "B": 4, "C": 4}, 12)


def test_lagrange_shares_of_the_chain():
    rels = [(10, ("A", "B")), (7, ("B", "C")), (10, ("C", "D"))]
    x, cost = chain_shares(10, 7, 10, 16)
    assert x == {"A": 1.0, "B": 4.0, "C": 4.0, "D": 1.0} and cost == 7 + 80
    assert best_integer_shares(rels, ["A", "B", "C", "D"], 16) == ({"A": 1, "B": 4, "C": 4, "D": 1}, 87)


def test_communication_and_replication_match_the_formula_exactly():
    rng = random.Random(41)
    for shares in [{"A": 3, "B": 3, "C": 3}, {"A": 2, "B": 4, "C": 1}, {"A": 1, "B": 1, "C": 1}]:
        rels = [random_edges(rng, 30, rng.randrange(0, 80)) for _ in range(3)]
        out, st = shares_join(triangle_query(*rels), shares)
        want = communication([(len(rels[0]), ("A", "B")), (len(rels[1]), ("B", "C")),
                              (len(rels[2]), ("C", "A"))], shares)
        assert st.pairs_sent == want == sum(st.reducer_input)
        assert len(st.reducer_input) == math.prod(shares.values())


def test_triangle_output_matches_brute_force():
    rng = random.Random(42)
    for _ in range(40):
        n, m = rng.choice([(1, 5), (5, 30), (40, 150)])
        rels = [random_edges(rng, n, m, zipf=rng.random() < 0.5) for _ in range(3)]
        shares = rng.choice([{"A": 2, "B": 2, "C": 2}, {"A": 3, "B": 1, "C": 2}, {"A": 1, "B": 1, "C": 1}])
        out, _ = shares_join(triangle_query(*rels), shares)
        assert Counter(out) == Counter(triangles_brute_force(*rels))


def test_empty_and_one_key():
    out, st = shares_join(triangle_query([], [(1, 2)], [(2, 1)]), {"A": 2, "B": 2, "C": 2})
    assert out == [] and st.pairs_sent == 2 * 2  # two tuples, each copied along the one attribute it lacks
    loop = [(0, 0)] * 3
    out, st = shares_join(triangle_query(loop, loop, loop), {"A": 2, "B": 2, "C": 2})
    assert len(out) == 27 and st.pairs_sent == 18 and st.largest_reducer_input == 9


def test_page_example_numbers():
    rng = random.Random(7)
    edges = list({(rng.randrange(300), rng.randrange(300)) for _ in range(3100)})[:3000]
    out, st = shares_join(triangle_query(edges, edges, edges), {"A": 3, "B": 3, "C": 3})
    assert len(out) == 982 and st.pairs_sent == 27000
    assert (st.largest_reducer_input, min(st.reducer_input)) == (1277, 805)
    out_deg = Counter(a for a, _ in edges)
    assert sum(out_deg[b] for _, b in edges) == 29912  # paths of length two, the size of R join S


def test_each_triangle_is_found_at_exactly_one_reducer():
    rng = random.Random(43)
    edges = list(set(random_edges(rng, 60, 600)))
    shares = {"A": 3, "B": 3, "C": 3}
    out, st = shares_join(triangle_query(edges, edges, edges), shares)
    assert len(out) == len(set(out)) == len(triangles_brute_force(edges, edges, edges))
    assert st.pairs_sent == 3 * len(edges) * 3
