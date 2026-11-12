# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/d-separation/. The authors are listed in prov/WVXXR3.jsonl.

import itertools
import random
from fractions import Fraction

from d_separation import d_separated, d_separated_moral, independent, joint


def all_dags(n):
    pairs = list(itertools.combinations(range(n), 2))
    for choice in itertools.product(range(3), repeat=len(pairs)):
        edges = [(a, b) if c == 1 else (b, a) for (a, b), c in zip(pairs, choice) if c]
        indeg = [0] * n
        for _, v in edges:
            indeg[v] += 1
        stack = [v for v in range(n) if indeg[v] == 0]
        seen = 0
        while stack:
            u = stack.pop()
            seen += 1
            for a, b in edges:
                if a == u:
                    indeg[b] -= 1
                    if indeg[b] == 0:
                        stack.append(b)
        if seen == n:
            yield edges


def random_cpt(n, edges, rng):
    cpt = []
    for v in range(n):
        k = sum(1 for _, b in edges if b == v)
        # values from a fine grid, so that an accidental cancellation has a tiny chance
        cpt.append({pa: Fraction(rng.randint(1, 9999), 10000) for pa in itertools.product((0, 1), repeat=k)})
    return cpt


def queries(n):
    for x, y in itertools.combinations(range(n), 2):
        rest = [v for v in range(n) if v not in (x, y)]
        for r in range(len(rest) + 1):
            for z in itertools.combinations(rest, r):
                yield {x}, {y}, set(z)


def test_three_node_patterns():
    chain, fork, collider = [(0, 1), (1, 2)], [(1, 0), (1, 2)], [(0, 1), (2, 1)]
    for edges in (chain, fork):
        assert not d_separated(3, edges, {0}, {2}, set())
        assert d_separated(3, edges, {0}, {2}, {1})
    assert d_separated(3, collider, {0}, {2}, set())
    assert not d_separated(3, collider, {0}, {2}, {1})
    # a descendant of the collider in Z also opens it
    assert not d_separated(4, collider + [(1, 3)], {0}, {2}, {3})


def test_worked_example():
    # A=0, B=1, C=2, D=3, E=4 with A->B, A->C, B->D, C->D, D->E.
    e = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)]
    assert d_separated(5, e, {1}, {2}, {0})
    assert not d_separated(5, e, {1}, {2}, {0, 4})
    assert d_separated(5, e, {0}, {4}, {3})


def test_soundness_and_generic_completeness_on_all_dags_with_four_nodes():
    rng = random.Random(1990)
    for n in (3, 4):
        for edges in all_dags(n):
            pj = joint(n, edges, random_cpt(n, edges, rng))
            for xs, ys, zs in queries(n):
                assert independent(pj, xs, ys, zs) == d_separated(n, edges, xs, ys, zs)


def test_soundness_on_five_node_dags():
    rng = random.Random(1988)
    dags = list(all_dags(5))
    for edges in rng.sample(dags, 80):
        pj = joint(5, edges, random_cpt(5, edges, rng))
        for xs, ys, zs in queries(5):
            if d_separated(5, edges, xs, ys, zs):
                assert independent(pj, xs, ys, zs)


def test_unfaithful_parameters_break_only_the_converse():
    # A -> B -> C and A -> C with tables that cancel: A and C are independent,
    # but they are adjacent, so not d-separated.
    edges = [(0, 1), (1, 2), (0, 2)]
    h = Fraction(1, 2)
    cpt = [{(): h}, {(0,): Fraction(1, 4), (1,): Fraction(3, 4)},
           {(0, 0): Fraction(1, 4), (0, 1): Fraction(3, 4), (1, 0): Fraction(3, 4), (1, 1): Fraction(1, 4)}]
    pj = joint(3, edges, cpt)
    assert independent(pj, {0}, {2}, set())
    assert not d_separated(3, edges, {0}, {2}, set())


def test_moral_ancestral_graph_criterion_agrees():
    for n in range(2, 5):
        for edges in all_dags(n):
            for xs, ys, zs in queries(n):
                assert d_separated_moral(n, edges, xs, ys, zs) == d_separated(n, edges, xs, ys, zs)
    rng = random.Random(4)
    for _ in range(300):
        n = rng.randint(2, 7)
        order = list(range(n))
        rng.shuffle(order)
        edges = [(order[i], order[j]) for i in range(n) for j in range(i + 1, n) if rng.random() < 0.4]
        lab = [rng.randrange(4) for _ in range(n)]
        xs, ys, zs = ({v for v in range(n) if lab[v] == k} for k in range(3))
        if xs and ys:
            assert d_separated_moral(n, edges, xs, ys, zs) == d_separated(n, edges, xs, ys, zs)
