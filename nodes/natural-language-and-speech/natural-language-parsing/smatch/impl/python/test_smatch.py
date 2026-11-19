# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/smatch/. The authors are listed in prov/SMYWR9.jsonl.

from fractions import Fraction
from itertools import permutations
from math import comb, perm
import random

from smatch import (
    all_mappings,
    climb,
    corpus_smatch,
    match_count,
    parse_penman,
    smart_init,
    smatch,
    smatch_brute_force,
    smatch_hill_climb,
)

# The example of Cai and Knight 2013, section 2.
GOLD = parse_penman("(a / want-01 :ARG0 (b / boy) :ARG1 (c / go-01 :ARG0 b))")
TEST = parse_penman("(x / want-01 :ARG0 (y / boy) :ARG1 (z / football))")


def rand_graph(rng, nv, ne, concepts, roles, pre):
    vs = [pre + str(i) for i in range(nv)]
    t = [("instance", v, rng.choice(concepts)) for v in vs]
    for _ in range(ne):
        t.append((rng.choice(roles), rng.choice(vs), rng.choice(vs)))
    if rng.random() < 0.5:
        t.append(("polarity", rng.choice(vs), "-"))
    return sorted(set(t))


def test_reader():
    assert sorted(GOLD) == sorted([
        ("instance", "a", "want-01"),
        ("instance", "b", "boy"),
        ("instance", "c", "go-01"),
        ("ARG0", "a", "b"),
        ("ARG1", "a", "c"),
        ("ARG0", "c", "b"),
    ])
    assert len(TEST) == 5


def test_reader_inverse_role_and_constant():
    g = parse_penman('(b / boy :ARG0-of (w / want-01) :name (n / name :op1 "Ed") :polarity -)', "p.")
    assert ("ARG0", "p.w", "p.b") in g
    assert ("op1", "p.n", "Ed") in g
    assert ("polarity", "p.b", "-") in g


def test_paper_table_of_six_mappings():
    want = {
        ("a", "b", "c"): 4,
        ("a", "c", "b"): 1,
        ("b", "a", "c"): 0,
        ("b", "c", "a"): 0,
        ("c", "a", "b"): 0,
        ("c", "b", "a"): 2,
    }
    for images, m in want.items():
        assert match_count(TEST, GOLD, dict(zip("xyz", images))) == m


def test_paper_score():
    p, r, f = smatch(TEST, GOLD, exact=True)
    assert (p, r, f) == (Fraction(4, 5), Fraction(2, 3), Fraction(8, 11))
    assert round(float(f), 2) == 0.73
    assert smatch(TEST, GOLD) == (p, r, f)


def test_identical_graphs_score_one():
    g2 = parse_penman("(a / want-01 :ARG0 (b / boy) :ARG1 (c / go-01 :ARG0 b))", "g.")
    assert smatch(GOLD, g2, exact=True)[2] == 1
    assert smatch(GOLD, g2)[2] == 1


def test_symmetric_match_count():
    rng = random.Random(1)
    for _ in range(30):
        a = rand_graph(rng, 3, 3, ["p", "q"], ["r", "s"], "t")
        b = rand_graph(rng, 4, 4, ["p", "q"], ["r", "s"], "g")
        assert smatch_brute_force(a, b)[0] == smatch_brute_force(b, a)[0]


def test_number_of_mappings():
    # Injective partial maps from m variables to n variables.
    for m in range(4):
        for n in range(4):
            got = sum(1 for _ in all_mappings(["t" + str(i) for i in range(m)], ["g" + str(i) for i in range(n)]))
            assert got == sum(comb(m, k) * perm(n, k) for k in range(min(m, n) + 1))
    got = sum(1 for _ in all_mappings(list("abcde"), list("ABCDE")))
    assert got == 1546


def test_hill_climbing_stuck_at_local_maximum():
    test = [("instance", "t0", "p"), ("instance", "t1", "q"), ("r", "t0", "t1")]
    gold = [("instance", "g0", "q"), ("instance", "g1", "q"), ("r", "g0", "g1")]
    start = smart_init(test, gold)
    assert start == {"t0": None, "t1": "g0"}
    assert climb(test, gold, start)[0] == 1
    assert smatch_brute_force(test, gold)[0] == 2
    assert match_count(test, gold, {"t0": "g0", "t1": "g1"}) == 2


def test_hill_climbing_never_exceeds_brute_force():
    rng = random.Random(2)
    for trial in range(60):
        a = rand_graph(rng, 5, rng.randint(3, 7), ["p", "q", "r"], ["r", "s"], "t")
        b = rand_graph(rng, rng.randint(3, 5), rng.randint(3, 7), ["p", "q", "r"], ["r", "s"], "g")
        opt, best_map = smatch_brute_force(a, b)
        got, mapping = smatch_hill_climb(a, b, restarts=1, seed=trial)
        assert got <= opt
        assert match_count(a, b, mapping) == got
        assert match_count(a, b, best_map) == opt


def test_restarts_reach_the_optimum():
    rng = random.Random(5)
    cases = []
    for _ in range(120):
        a = rand_graph(rng, 4, rng.randint(2, 6), ["p", "q", "r"], ["r", "s"], "t")
        b = rand_graph(rng, rng.randint(3, 5), rng.randint(2, 6), ["p", "q", "r"], ["r", "s"], "g")
        cases.append((a, b, smatch_brute_force(a, b)[0]))
    stuck_without = sum(smatch_hill_climb(a, b, restarts=0, seed=7)[0] < opt for a, b, opt in cases)
    stuck_with = sum(smatch_hill_climb(a, b, restarts=20, seed=7)[0] < opt for a, b, opt in cases)
    assert stuck_without > 0
    assert stuck_with == 0


def test_corpus_score_sums_counts():
    g2 = parse_penman("(w / want-01 :ARG0 (b / boy))", "g.")
    t2 = parse_penman("(w / want-01 :ARG0 (b / girl))", "t.")
    p, r, f = corpus_smatch([(TEST, GOLD), (t2, g2)], exact=True)
    # Matches 4 + 2, test triples 5 + 3, gold triples 6 + 3.
    assert (p, r, f) == (Fraction(6, 8), Fraction(6, 9), Fraction(12, 17))
    mean_f = (smatch(TEST, GOLD, exact=True)[2] + smatch(t2, g2, exact=True)[2]) / 2
    assert mean_f != f


def test_empty_graph():
    assert smatch([], GOLD, exact=True) == (0, 0, 0)


def has_subgraph(h_edges, nh, g_edges, ng):
    gset = set(g_edges) | {(v, u) for u, v in g_edges}
    for images in permutations(range(ng), nh):
        if all((images[u], images[v]) in gset for u, v in h_edges):
            return True
    return False


def graph_to_amr(edges, n, pre):
    t = [("instance", pre + str(v), "node") for v in range(n)]
    for u, v in edges:
        t.append(("edge", pre + str(u), pre + str(v)))
        t.append(("edge", pre + str(v), pre + str(u)))
    return t


def test_reduction_from_subgraph_isomorphism():
    # H is a subgraph of G iff the best match count is |V(H)| + 2 |E(H)|.
    rng = random.Random(9)
    seen = {True: 0, False: 0}
    for _ in range(40):
        nh, ng = 3, 4
        all_h = [(u, v) for u in range(nh) for v in range(u + 1, nh)]
        all_g = [(u, v) for u in range(ng) for v in range(u + 1, ng)]
        h = [e for e in all_h if rng.random() < 0.6]
        g = [e for e in all_g if rng.random() < 0.5]
        best, _ = smatch_brute_force(graph_to_amr(h, nh, "h"), graph_to_amr(g, ng, "g"))
        answer = has_subgraph(h, nh, g, ng)
        assert (best == nh + 2 * len(h)) == answer
        seen[answer] += 1
    assert seen[True] > 0 and seen[False] > 0
    triangle = [(0, 1), (1, 2), (0, 2)]
    four_cycle = [(0, 1), (1, 2), (2, 3), (0, 3)]
    assert smatch_brute_force(graph_to_amr(triangle, 3, "h"), graph_to_amr(four_cycle, 4, "g"))[0] < 9
