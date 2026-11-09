# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stalmarck-algorithm/. The authors are listed in prov/JF7B8D.jsonl.

import itertools
import random

from stalmarck_algorithm import FALSE, TRUE, Equiv, Stats, build, intersect, saturate, simple_rules, stalmarck


def satisfiable(clauses: list[list[int]], n: int) -> bool:
    for bits in itertools.product([False, True], repeat=n):
        if all(any(bits[abs(a) - 1] == (a > 0) for a in c) for c in clauses):
            return True
    return False


def random_cnf(rng: random.Random, n: int, m: int) -> list[list[int]]:
    out = []
    for _ in range(m):
        w = rng.choice([1, 2, 2, 3, 3, 3])
        out.append([v if rng.random() < 0.5 else -v for v in rng.sample(range(1, n + 1), min(w, n))])
    return out


def pigeonhole(p: int, h: int) -> list[list[int]]:
    var = lambda i, j: i * h + j + 1
    cs = [[var(i, j) for j in range(h)] for i in range(p)]
    cs += [[-var(a, j), -var(b, j)] for j in range(h) for a in range(p) for b in range(a + 1, p)]
    return cs


def check(clauses, n):
    model, k = stalmarck(clauses, n)
    assert (model is not None) == satisfiable(clauses, n)
    if model is not None:
        assert all(any(model[abs(a)] == (a > 0) for a in c) for c in clauses)
    return model, k


def test_against_brute_force() -> None:
    rng = random.Random(1989)
    for _ in range(120):
        n = rng.randint(1, 8)
        check(random_cnf(rng, n, rng.randint(1, 5 * n)), n)
    for _ in range(12):  # larger n, near the 3-SAT threshold
        n = rng.randint(9, 12)
        f = [[v if rng.random() < 0.5 else -v for v in rng.sample(range(1, n + 1), 3)]
             for _ in range(round(4.3 * n))]
        check(f, n)


def test_soundness_of_each_saturation() -> None:
    """Every equivalence that k-saturation derives holds in every model of F."""
    rng = random.Random(5)
    for _ in range(40):
        n = rng.randint(2, 6)
        f = random_cnf(rng, n, rng.randint(2, 3 * n))
        triplets, roots, size = build(f, n)
        e = Equiv(size)
        for r in roots:
            e.union(r, TRUE)
        used = {abs(d) for c in f for d in c}
        for k in (0, 1, 2):
            s = saturate(triplets, e, k, n, used, Stats())
            for bits in itertools.product([False, True], repeat=n):
                if not all(any(bits[abs(a) - 1] == (a > 0) for a in c) for c in f):
                    continue
                assert not s.bad
                for v in sorted(used):
                    root, p = s.find(v)
                    if root == 0:
                        assert bits[v - 1] == (p == 0)
                for u, v in itertools.combinations(sorted(used), 2):
                    (ru, pu), (rv, pv) = s.find(u), s.find(v)
                    if ru == rv:
                        assert (bits[u - 1] ^ bits[v - 1]) == (pu ^ pv)


def test_intersection_keeps_common_equivalences() -> None:
    a, b = Equiv(5), Equiv(5)
    a.union(2, 4)      # x1 == x2
    a.union(6, 0)      # x3 == TRUE
    b.union(2, 4)      # x1 == x2
    b.union(6, 1)      # x3 == FALSE
    b.union(8, 3)      # x4 == not x1
    c = intersect(a, b)
    assert c.same(2, 4) and not c.same(6, 0) and not c.same(6, 1) and not c.same(8, 3)


def test_page_example() -> None:
    # Every clause has two literals, so 0-saturation finds nothing, and one dilemma on x1 refutes F.
    f = [[1, 2], [1, -2], [-1, 3], [-1, -3]]
    stats = Stats()
    model, k = stalmarck(f, 3, stats)
    assert model is None and k == 1 and stats.dilemmas == 1
    # The two branches agree on x1 == x2, x2 == -x3 and x4 == TRUE; 0-saturation finds none of them.
    g = [[-1, 2], [-2, 1], [1, 3], [-1, -3], [4, -2], [4, 2]]
    model, k = stalmarck(g, 4)
    assert k == 0 and model == {1: True, 2: True, 3: False, 4: True}
    triplets, roots, size = build(g, 4)
    e = Equiv(size)
    for r in roots:
        e.union(r, TRUE)
    simple_rules(triplets, e)
    assert not e.same(4, 6 + 1)
    s = saturate(triplets, e, 1, 4, {1, 2, 3, 4}, Stats())
    assert s.same(2, 4) and s.same(4, 7) and s.same(8, TRUE)


def test_pigeonhole_needs_depth() -> None:
    model, k = check(pigeonhole(3, 2), 6)
    assert model is None and k >= 1
    model, k = check(pigeonhole(3, 3), 9)
    assert model is not None
