# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/markov-blanket/. The authors are listed in prov/7QYGND.jsonl.

import itertools
import random
from fractions import Fraction

from markov_blanket import blanket_dag, blanket_undirected, is_blanket, joint_bn, markov_boundaries


def random_dag(n, rng, p=0.5):
    order = list(range(n))
    rng.shuffle(order)
    return [(order[i], order[j]) for i in range(n) for j in range(i + 1, n) if rng.random() < p]


def random_cpt(n, edges, rng):
    cpt = []
    for v in range(n):
        k = sum(1 for _, b in edges if b == v)
        cpt.append({pa: Fraction(rng.randint(1, 9999), 10000) for pa in itertools.product((0, 1), repeat=k)})
    return cpt


def test_dag_blanket_is_a_blanket_and_the_unique_boundary():
    rng = random.Random(1988)
    for _ in range(120):
        n = rng.randint(2, 5)
        edges = random_dag(n, rng)
        pj = joint_bn(n, edges, random_cpt(n, edges, rng))
        for v in range(n):
            mb = blanket_dag(edges, v)
            assert is_blanket(pj, n, v, mb)
            # generic positive tables: the boundary is unique and equals the graph blanket
            assert markov_boundaries(pj, n, v) == [mb]


def test_co_parents_are_needed():
    # 0 -> 2 <- 1: the blanket of 0 is {1, 2}; the child alone is not enough.
    edges = [(0, 2), (1, 2)]
    rng = random.Random(7)
    pj = joint_bn(3, edges, random_cpt(3, edges, rng))
    assert blanket_dag(edges, 0) == {1, 2}
    assert not is_blanket(pj, 3, 0, {2})
    assert is_blanket(pj, 3, 0, {1, 2})


def test_markov_random_field_neighbours():
    rng = random.Random(1974)
    for _ in range(40):
        n = rng.randint(3, 5)
        adj = [set() for _ in range(n)]
        pot = {}
        for a, b in itertools.combinations(range(n), 2):
            if rng.random() < 0.5:
                adj[a].add(b)
                adj[b].add(a)
                pot[a, b] = {xy: Fraction(rng.randint(1, 999), 100) for xy in itertools.product((0, 1), repeat=2)}
        un = {x: Fraction(1) for x in itertools.product((0, 1), repeat=n)}
        for x in un:
            for (a, b), t in pot.items():
                un[x] *= t[x[a], x[b]]
        z = sum(un.values())
        pj = {x: p / z for x, p in un.items()}
        for v in range(n):
            nb = blanket_undirected(adj, v)
            assert is_blanket(pj, n, v, nb)
            assert markov_boundaries(pj, n, v) == [nb]


def test_boundary_not_unique_without_positivity():
    # X1 is an exact copy of X0, and X2 depends on X0.
    edges = [(0, 1), (0, 2)]
    cpt = [{(): Fraction(1, 2)}, {(0,): Fraction(0), (1,): Fraction(1)},
           {(0,): Fraction(1, 5), (1,): Fraction(4, 5)}]
    pj = joint_bn(3, edges, cpt)
    bs = markov_boundaries(pj, 3, 2)
    assert sorted(map(sorted, bs)) == [[0], [1]]
    # the graph blanket {0} is one of them, and its intersection with {1} is empty
    assert not is_blanket(pj, 3, 2, set())


def test_the_whole_rest_is_always_a_blanket():
    rng = random.Random(3)
    edges = random_dag(4, rng, 0.7)
    pj = joint_bn(4, edges, random_cpt(4, edges, rng))
    for v in range(4):
        assert is_blanket(pj, 4, v, {u for u in range(4) if u != v})
