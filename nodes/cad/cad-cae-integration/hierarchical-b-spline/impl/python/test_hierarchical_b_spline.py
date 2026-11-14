# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hierarchical-b-spline/. The authors are listed in prov/4MZ00N.jsonl.

import random
from fractions import Fraction as F

from hierarchical_b_spline import Hierarchy, bspline, open_knots, rank


def all_basis(knots, p, x):
    """Reference: every B-spline of degree p at x by the triangular Cox-de Boor table."""
    n = len(knots) - p - 1
    if x == knots[-1]:
        return [F(int(i == n - 1)) for i in range(n)]
    N = [F(int(knots[i] <= x < knots[i + 1])) for i in range(len(knots) - 1)]
    for d in range(1, p + 1):
        N = [
            ((x - knots[i]) / (knots[i + d] - knots[i]) * N[i] if knots[i + d] > knots[i] else 0)
            + ((knots[i + d + 1] - x) / (knots[i + d + 1] - knots[i + 1]) * N[i + 1] if knots[i + d + 1] > knots[i + 1] else 0)
            for i in range(len(N) - 1)
        ]
    return N


def example(p=2):
    """Three levels on [0, 4]^2: Omega^1 = [0, 2]^2 and Omega^2 = [0, 1]^2."""
    H = Hierarchy(4, p, 3)
    H.refine(1, [(a, b) for a in range(2) for b in range(2)])
    H.refine(2, [(a, b) for a in range(2) for b in range(2)])
    return H


def random_hierarchy(rng, p):
    H = Hierarchy(4, p, 3)
    H.refine(1, rng.sample(sorted(H.omega[0]), 7))
    H.refine(2, rng.sample(sorted(H.omega[1]), 9))
    return H


def pts(rng, k):
    return [(F(rng.randint(0, 400), 100), F(rng.randint(0, 400), 100)) for _ in range(k)]


def test_one_level_is_the_tensor_b_spline_basis():
    H = Hierarchy(3, 2, 1)
    basis = H.basis()
    assert len(basis) == 25
    rng = random.Random(1)
    for x, y in pts(rng, 10):
        if x > 3 or y > 3:
            continue
        Nx, Ny = all_basis(H.knots[0], 2, x), all_basis(H.knots[0], 2, y)
        for _, (i, j) in basis:
            assert H.evaluate({(0, (i, j)): 1}, x, y) == Nx[i] * Ny[j]


def test_two_scale_relation_against_direct_evaluation():
    rng = random.Random(2)
    for p in (2, 3):
        H = Hierarchy(4, p, 2)
        fine = H.knots[1]
        for i, row in enumerate(H.R[0]):
            for _ in range(5):
                x = F(rng.randint(0, 400), 100)
                assert bspline(H.knots[0], i, p, x) == sum(c * bspline(fine, j, p, x) for j, c in row.items())
                assert all(c > 0 for c in row.values())


def test_kraft_selection_on_the_example():
    H = example()
    basis = H.basis()
    by_level = [sum(1 for l, _ in basis if l == k) for k in range(3)]
    # level 0: the 36 B-splines minus the 4 whose support [i-2, i+1] lies in [0, 2]
    assert by_level == [32, 12, 16]
    assert rank([H.finest(l, B) for l, B in basis]) == len(basis)


def test_basis_is_independent_and_contains_each_level_on_its_domain():
    rng = random.Random(3)
    for p in (2, 3):
        H = random_hierarchy(rng, p)
        basis = H.basis()
        vecs = [H.finest(l, B) for l, B in basis]
        r = rank(vecs)
        assert r == len(basis)
        for l in range(3):
            for i in range(H.size(l)):
                for j in range(H.size(l)):
                    if H.inside(l, (i, j), l):
                        assert rank(vecs + [H.finest(l, (i, j))]) == r


def test_enlarging_the_domains_gives_nested_spaces():
    rng = random.Random(4)
    H = random_hierarchy(rng, 2)
    old = [H.finest(l, B) for l, B in H.basis()]
    for _ in range(3):
        level = rng.choice([1, 2])
        H.refine(level, rng.sample(sorted(H.omega[level - 1]), 2))
        new = [H.finest(l, B) for l, B in H.basis()]
        assert rank(new) == len(new)
        assert rank(new + old) == len(new)
        old = new


def test_no_partition_of_unity_but_constants_are_in_the_space():
    H = example()
    basis = H.basis()
    total = {}
    for l, B in basis:
        for k, c in H.finest(l, B).items():
            total[k] = total.get(k, F(0)) + c
    ones = {(a, b): F(1) for a in range(H.size(2)) for b in range(H.size(2))}
    assert total != ones  # the plain sum is not 1
    assert H.evaluate({b: 1 for b in basis}, F(1, 2), F(1, 2)) > 1
    vecs = [H.finest(l, B) for l, B in basis]
    assert rank(vecs + [ones]) == len(vecs)  # but 1 is in the span
