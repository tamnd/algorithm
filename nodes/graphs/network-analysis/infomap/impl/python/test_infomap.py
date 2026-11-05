# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/infomap/. The authors are listed in prov/R7CYRH.jsonl.

import random
from fractions import Fraction
from itertools import combinations
from math import isclose, log2

from infomap import infomap, map_equation


def exact_power(n, edges, groups):
    """2^(2W L(M)) from the definition, as an exact fraction of integers."""
    deg = [0] * n
    for u, v, w in edges:
        deg[u] += w
        deg[v] += w
    where = {v: i for i, g in enumerate(groups) for v in g}
    cut = [0] * len(groups)
    for u, v, w in edges:
        if where[u] != where[v]:
            cut[where[u]] += w
            cut[where[v]] += w
    tot = [sum(deg[v] for v in g) for g in groups]
    big = sum(cut)
    num = big**big
    den = 1
    for c, t in zip(cut, tot):
        num *= (c + t) ** (c + t)
        den *= c ** (2 * c)
    for d in deg:
        den *= d**d
    return Fraction(num, den)


def reference(n, edges):
    """The same rules on blocks of original vertices, each score computed from the definition."""
    if not edges:
        return [[v] for v in range(n)], []
    linked = set()
    for u, v, _ in edges:
        linked.add((u, v))
        linked.add((v, u))
    blocks = [[v] for v in range(n)]
    levels = []
    while True:
        k = len(blocks)
        comm = list(range(k))
        moved = improved = False
        improved = True
        while improved:
            improved = False
            for b in range(k):
                old = comm[b]
                near = {
                    comm[c]
                    for c in range(k)
                    if c != b and any((x, y) in linked for x in blocks[b] for y in blocks[c])
                }

                def score(target):
                    trial = comm[:]
                    trial[b] = target
                    groups = {}
                    for c in range(k):
                        groups.setdefault(trial[c], []).extend(blocks[c])
                    return exact_power(n, edges, list(groups.values()))

                best, best_s = old, score(old)
                for c in sorted(near):
                    if c != old and score(c) < best_s:
                        best, best_s = c, score(c)
                comm[b] = best
                if best != old:
                    improved = moved = True
        if not moved:
            return sorted(sorted(p) for p in blocks), levels
        order = []
        for b in range(k):
            if comm[b] not in order:
                order.append(comm[b])
        blocks = [sum((blocks[b] for b in range(k) if comm[b] == c), []) for c in order]
        levels.append(sorted(sorted(p) for p in blocks))


def all_partitions(items):
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for p in all_partitions(rest):
        for i in range(len(p)):
            yield p[:i] + [[first] + p[i]] + p[i + 1 :]
        yield [[first]] + p


def random_weighted(rng, n, p):
    return [(u, v, rng.choice([1, 1, 1, 2, 3])) for u, v in combinations(range(n), 2) if rng.random() < p]


EXAMPLE = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (4, 6), (5, 6)]


def test_example():
    edges = [(u, v, 1) for u, v in EXAMPLE]
    modules, levels = infomap(7, edges)
    assert modules == [[0, 1, 2, 3], [4, 5, 6]]
    assert levels == [[[0, 1, 2, 3], [4, 5, 6]]]
    assert isclose(map_equation(7, edges, modules), 2.44444, abs_tol=5e-5)
    assert isclose(map_equation(7, edges, [list(range(7))]), 2.77995, abs_tol=5e-5)
    assert isclose(map_equation(7, edges, [[v] for v in range(7)]), 4.77995, abs_tol=5e-5)


def test_edge_cases():
    assert infomap(0, []) == ([], [])
    assert infomap(3, []) == ([[0], [1], [2]], [])
    assert infomap(2, [(0, 1, 1)])[0] == [[0, 1]]
    assert infomap(4, [(0, 1, 1), (2, 3, 1)])[0] == [[0, 1], [2, 3]]
    assert infomap(4, [(u, v, 1) for u, v in combinations(range(4), 2)])[0] == [[0, 1, 2, 3]]
    try:
        infomap(2, [(1, 1, 1)])
    except ValueError:
        pass
    else:
        raise AssertionError("a self-loop must be refused")


def test_formula_matches_exact_form():
    rng = random.Random(1)
    for _ in range(200):
        n = rng.randint(1, 8)
        edges = random_weighted(rng, n, 0.5)
        if not edges:
            continue
        two_w = 2 * sum(w for _, _, w in edges)
        labels = [rng.randrange(3) for _ in range(n)]
        groups = [[v for v in range(n) if labels[v] == c] for c in range(3)]
        groups = [g for g in groups if g]
        x = exact_power(n, edges, groups)
        exact = (log2(x.numerator) - log2(x.denominator)) / two_w
        assert isclose(map_equation(n, edges, groups), exact, abs_tol=1e-9)


def test_random_against_reference():
    rng = random.Random(20080129)
    for _ in range(300):
        n = rng.randint(0, 8)
        edges = random_weighted(rng, n, rng.choice([0.2, 0.4, 0.6]))
        assert infomap(n, edges) == reference(n, edges)


def test_levels_lower_the_codelength():
    rng = random.Random(118)
    for _ in range(150):
        n = rng.randint(1, 7)
        edges = random_weighted(rng, n, 0.45)
        if not edges:
            continue
        modules, levels = infomap(n, edges)
        xs = [exact_power(n, edges, [[v] for v in range(n)])] + [exact_power(n, edges, p) for p in levels]
        assert all(a > b for a, b in zip(xs, xs[1:]))
        best = min(exact_power(n, edges, p) for p in all_partitions(list(range(n))))
        assert exact_power(n, edges, modules) >= best


if __name__ == "__main__":
    test_example()
    test_edge_cases()
    test_formula_matches_exact_form()
    test_random_against_reference()
    test_levels_lower_the_codelength()
    print("ok")
