# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bayes-ball/. The authors are listed in prov/FBZXXF.jsonl.

import itertools
import random
from fractions import Fraction

from bayes_ball import bayes_ball, d_separated


def all_dags(n):
    pairs = list(itertools.combinations(range(n), 2))
    for choice in itertools.product(range(3), repeat=len(pairs)):
        edges = [(a, b) if c == 1 else (b, a) for (a, b), c in zip(pairs, choice) if c]
        if acyclic(n, edges):
            yield edges


def acyclic(n, edges):
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
    return seen == n


def descendants(edges, v):
    out, stack = set(), [v]
    while stack:
        u = stack.pop()
        for a, b in edges:
            if a == u and b not in out:
                out.add(b)
                stack.append(b)
    return out


def brute_force(n, edges, xs, ys, zs):
    """d-separation by the definition over all simple paths of the skeleton."""
    es = set(edges)
    desc = [descendants(edges, v) for v in range(n)]
    nbr = [set() for _ in range(n)]
    for a, b in edges:
        nbr[a].add(b)
        nbr[b].add(a)
    for x in xs:
        stack = [[x]]
        while stack:
            path = stack.pop()
            v = path[-1]
            if len(path) >= 3:
                a, m = path[-3], path[-2]
                if (a, m) in es and (v, m) in es:
                    if m not in zs and not (desc[m] & zs):
                        continue
                elif m in zs:
                    continue
            if v in ys:
                return False
            stack.extend(path + [w] for w in nbr[v] if w not in path)
    return True


def subsets(items):
    for r in range(len(items) + 1):
        yield from itertools.combinations(items, r)


def test_worked_example():
    # A=0, B=1, C=2, D=3, E=4 with A->B, A->C, B->D, C->D, D->E; J = {B}, K = {A, E}.
    edges = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)]
    r = bayes_ball(5, edges, {1}, {0, 4})
    assert r.bottom == {1, 2, 3}
    assert r.top == {1, 2, 3, 4}
    assert r.visited == {0, 1, 2, 3, 4}
    assert r.requisite_observation() == {0, 4}
    assert not d_separated(5, edges, {1}, {2}, {0, 4})
    assert d_separated(5, edges, {1}, {2}, {0})


def test_all_dags_up_to_four_nodes():
    for n in range(1, 5):
        for edges in all_dags(n):
            for x, y in itertools.permutations(range(n), 2):
                rest = [v for v in range(n) if v not in (x, y)]
                for z in subsets(rest):
                    zs = set(z)
                    assert d_separated(n, edges, {x}, {y}, zs) == brute_force(n, edges, {x}, {y}, zs)


def test_sample_of_five_node_dags():
    rng = random.Random(1998)
    dags = list(all_dags(5))
    for edges in rng.sample(dags, 400):
        for x, y in itertools.combinations(range(5), 2):
            rest = [v for v in range(5) if v not in (x, y)]
            for z in subsets(rest):
                zs = set(z)
                assert d_separated(5, edges, {x}, {y}, zs) == brute_force(5, edges, {x}, {y}, zs)


def random_cpts(n, parents, rng):
    cpt = []
    for v in range(n):
        table = {}
        for pa in itertools.product((0, 1), repeat=len(parents[v])):
            table[pa] = Fraction(rng.randint(1, 9), 10)
        cpt.append(table)
    return cpt


def conditional(n, parents, cpt, J, K, kvals):
    """P(J = . | K = kvals) as a dict, by summing the joint."""
    num = {}
    for x in itertools.product((0, 1), repeat=n):
        if any(x[k] != kvals[i] for i, k in enumerate(K)):
            continue
        p = Fraction(1)
        for v in range(n):
            q = cpt[v][tuple(x[u] for u in parents[v])]
            p *= q if x[v] == 1 else 1 - q
        key = tuple(x[j] for j in J)
        num[key] = num.get(key, 0) + p
    total = sum(num.values())
    return {k: v / total for k, v in num.items()}


def test_tables_off_the_top_marks_do_not_matter():
    rng = random.Random(3)
    for _ in range(60):
        n = rng.randint(2, 5)
        order = list(range(n))
        rng.shuffle(order)
        edges = [(order[i], order[j]) for i in range(n) for j in range(i + 1, n) if rng.random() < 0.5]
        parents = [[u for u, w in edges if w == v] for v in range(n)]
        roles = [rng.randrange(3) for _ in range(n)]
        J = [v for v in range(n) if roles[v] == 0] or [0]
        K = [v for v in range(n) if roles[v] == 1 and v not in J]
        res = bayes_ball(n, edges, set(J), set(K))
        cpt = random_cpts(n, parents, rng)
        for kvals in itertools.product((0, 1), repeat=len(K)):
            before = conditional(n, parents, cpt, J, K, kvals)
            other = random_cpts(n, parents, rng)
            changed = [other[v] if v not in res.top else cpt[v] for v in range(n)]
            assert conditional(n, parents, changed, J, K, kvals) == before


def test_each_mark_is_set_at_most_once():
    rng = random.Random(9)
    for _ in range(100):
        n = rng.randint(1, 30)
        edges = [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < 0.2]
        K = {v for v in range(n) if rng.random() < 0.3}
        J = {v for v in range(n) if v not in K and rng.random() < 0.2}
        r = bayes_ball(n, edges, J, K)
        assert r.bottom.isdisjoint(K)
        assert J <= r.bottom
