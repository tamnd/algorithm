# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/matroid-greedy-algorithm/. The authors are listed in prov/4BS62B.jsonl.

import itertools
import random

from matroid_greedy_algorithm import matroid_greedy_algorithm


def graphic(edges):
    def indep(xs):
        parent = {}

        def find(v):
            while parent.get(v, v) != v:
                v = parent[v]
            return v

        for k in xs:
            u, v = edges[k][0], edges[k][1]
            a, b = find(u), find(v)
            if a == b:
                return False
            parent[a] = b
        return True

    return indep


def gf2(vectors):
    def indep(xs):
        basis = []
        for k in xs:
            v = vectors[k]
            for b in basis:
                v = min(v, v ^ b)
            if v == 0:
                return False
            basis.append(v)
            basis.sort(reverse=True)
        return True

    return indep


def uniform(k):
    return lambda xs: len(xs) <= k


def partition(block, cap):
    def indep(xs):
        count = {}
        for x in xs:
            count[block[x]] = count.get(block[x], 0) + 1
        return all(c <= cap[b] for b, c in count.items())

    return indep


def best_basis_weight(elements, weight, indep):
    best = None
    for r in range(len(elements), -1, -1):
        for xs in itertools.combinations(elements, r):
            if indep(frozenset(xs)):
                w = sum(weight(x) for x in xs)
                best = w if best is None or w > best else best
        if best is not None:
            return best
    return 0


def test_example() -> None:
    edges = {
        "a": (1, 2, 7), "b": (1, 3, 5), "c": (2, 3, 8), "d": (2, 4, 6),
        "e": (3, 4, 9), "f": (3, 5, 4), "g": (4, 5, 6), "h": (1, 5, 3),
    }
    got = matroid_greedy_algorithm(list(edges), lambda k: edges[k][2], graphic(edges))
    assert got == ["e", "c", "a", "g"]
    assert sum(edges[k][2] for k in got) == 30


def test_edges() -> None:
    assert matroid_greedy_algorithm([], lambda x: x, uniform(3)) == []
    assert matroid_greedy_algorithm([1, 2, 3], lambda x: x, uniform(0)) == []
    assert matroid_greedy_algorithm([1, 2, 3], lambda x: x, uniform(5)) == [3, 2, 1]
    # negative weights are still taken when a basis needs them
    assert matroid_greedy_algorithm([-5, -1, -3], lambda x: x, uniform(2)) == [-1, -3]
    # ties keep input order
    w = {"x": 1, "y": 1, "z": 1}
    assert matroid_greedy_algorithm(["z", "x", "y"], w.get, uniform(2)) == ["z", "x"]


def test_linear_and_partition_examples() -> None:
    vec = {"a": 0b110, "b": 0b011, "c": 0b101, "d": 0b111, "e": 0b100}
    w = {"a": 5, "b": 7, "c": 6, "d": 2, "e": 4}
    assert matroid_greedy_algorithm(list(vec), w.get, gf2(vec)) == ["b", "c", "e"]
    block = {"a": 1, "b": 1, "c": 1, "d": 2, "e": 2, "f": 2, "g": 3, "h": 3}
    val = {"a": 9, "b": 7, "c": 4, "d": 8, "e": 6, "f": 5, "g": 3, "h": 2}
    got = matroid_greedy_algorithm(list(block), val.get, partition(block, {1: 1, 2: 2, 3: 1}))
    assert sorted(got) == ["a", "d", "e", "g"]


def test_not_a_matroid_can_fail() -> None:
    # matchings on the path u1 - v1 - u2 - v2 are not a matroid
    edges = {"p": ("u1", "v1"), "q": ("u2", "v1"), "s": ("u2", "v2")}
    w = {"p": 2, "q": 3, "s": 2}

    def matching(xs):
        ends = [v for x in xs for v in edges[x]]
        return len(ends) == len(set(ends))

    got = matroid_greedy_algorithm(list(edges), w.get, matching)
    assert sum(w[x] for x in got) == 3
    assert best_basis_weight(list(edges), w.get, matching) == 4


def random_case(rng):
    kind = rng.randrange(4)
    n = rng.randint(0, 7)
    elems = list(range(n))
    if kind == 0:
        indep = uniform(rng.randint(0, n))
    elif kind == 1:
        block = {x: rng.randrange(3) for x in elems}
        indep = partition(block, {b: rng.randint(0, 2) for b in range(3)})
    elif kind == 2:
        edges = {x: (rng.randrange(5), rng.randrange(5)) for x in elems}
        indep = graphic(edges)
    else:
        vecs = {x: rng.randrange(16) for x in elems}
        indep = gf2(vecs)
    weights = {x: rng.randint(-10, 10) for x in elems}
    return elems, weights, indep


def test_random_against_brute_force() -> None:
    rng = random.Random(20251104)
    for _ in range(800):
        elems, weights, indep = random_case(rng)
        got = matroid_greedy_algorithm(elems, weights.get, indep)
        assert indep(frozenset(got))
        assert all(not indep(frozenset(got) | {x}) for x in elems if x not in got)
        assert sum(weights[x] for x in got) == best_basis_weight(elems, weights.get, indep)
        # Gale optimality: k-th heaviest dominates every independent set
        gw = [weights[x] for x in got]
        assert gw == sorted(gw, reverse=True)
        for r in range(len(got) + 1):
            for xs in itertools.combinations(elems, r):
                if indep(frozenset(xs)):
                    xw = sorted((weights[x] for x in xs), reverse=True)
                    assert all(a >= b for a, b in zip(gw, xw))
