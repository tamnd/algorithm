# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/truncated-hierarchical-b-spline/. The authors are listed in prov/EY36RH.jsonl.

import random
from fractions import Fraction as F

from truncated_hierarchical_b_spline import THB, bspline, rank


def example(p=2):
    """Three levels on [0, 4]^2: Omega^1 = [0, 2]^2 and Omega^2 = [0, 1]^2."""
    T = THB(4, p, 3)
    T.refine(1, [(a, b) for a in range(2) for b in range(2)])
    T.refine(2, [(a, b) for a in range(2) for b in range(2)])
    return T


def random_thb(rng, p):
    T = THB(4, p, 3)
    T.refine(1, rng.sample(sorted(T.omega[0]), 7))
    T.refine(2, rng.sample(sorted(T.omega[1]), 9))
    return T


def pts(rng, k):
    return [(F(rng.randint(0, 400), 100), F(rng.randint(0, 400), 100)) for _ in range(k)]


def cases():
    rng = random.Random(5)
    yield example(2)
    yield example(3)
    for p in (2, 3):
        for _ in range(2):
            yield random_thb(rng, p)


def reference_value(T, l, B, x, y):
    """Truncate by the definition and evaluate each level with its own knots.

    The function is B minus, for each finer level k, the dropped terms of its
    expansion in level k, each evaluated by Cox-de Boor on the knots of level k.
    """
    def ev(level, c):
        kn = T.knots[level]
        return sum(v * bspline(kn, i, T.p, x) * bspline(kn, j, T.p, y) for (i, j), v in c.items())

    value = ev(l, {B: F(1)})
    c = {B: F(1)}
    for k in range(l + 1, T.L):
        c = T.lift(c, k - 1)
        dropped = {g: v for g, v in c.items() if T.inside(k, g, k)}
        value -= ev(k, dropped)
        c = {g: v for g, v in c.items() if g not in dropped}
    return value


def test_one_level_gives_the_tensor_b_splines():
    T = THB(3, 2, 1)
    basis = T.basis()
    assert len(basis) == 25
    for (l, B), c in basis.items():
        assert c == {B: 1}


def test_example_counts_match_kraft():
    T = example()
    levels = [sum(1 for l, _ in T.basis() if l == k) for k in range(3)]
    assert levels == [32, 12, 16]


def test_partition_of_unity_exactly():
    rng = random.Random(6)
    for T in cases():
        total = {}
        for c in T.basis().values():
            for g, v in c.items():
                total[g] = total.get(g, F(0)) + v
        n = T.size(T.L - 1)
        assert total == {(a, b): F(1) for a in range(n) for b in range(n)}
        for x, y in pts(rng, 3):
            assert T.evaluate(total, x, y) == 1


def test_coefficients_of_a_level_0_spline_are_preserved():
    rng = random.Random(9)
    for T in cases():
        n = T.size(0)
        s0 = {(i, j): F(rng.randint(-9, 9)) for i in range(n) for j in range(n)}
        level = [s0]
        for k in range(T.L - 1):
            level.append(T.lift(level[-1], k))
        total = {}
        for (l, B), c in T.basis().items():
            w = level[l].get(B, F(0))
            for g, v in c.items():
                total[g] = total.get(g, F(0)) + w * v
        total = {g: v for g, v in total.items() if v}
        assert total == {g: v for g, v in level[-1].items() if v}


def test_coefficients_are_nonnegative_and_supports_shrink():
    smaller = 0
    for T in cases():
        for (l, B), c in T.basis().items():
            plain = T.plain(l, B)
            assert all(v > 0 for v in c.values())
            assert set(c) <= set(plain)
            assert all(c[g] <= plain[g] for g in c)
            smaller += set(c) != set(plain)
    assert smaller > 0


def test_same_span_as_the_hierarchical_basis_and_independent():
    for T in cases():
        basis = T.basis()
        thb = [c for c in basis.values()]
        hb = [T.plain(l, B) for l, B in basis]
        r = rank(thb)
        assert r == len(basis)
        assert rank(thb + hb) == r


def test_refinement_gives_nested_spaces():
    rng = random.Random(7)
    T = random_thb(rng, 2)
    old = list(T.basis().values())
    for _ in range(3):
        level = rng.choice([1, 2])
        T.refine(level, rng.sample(sorted(T.omega[level - 1]), 2))
        new = list(T.basis().values())
        assert rank(new) == len(new)
        assert rank(new + old) == len(new)
        old = new


def test_values_against_level_by_level_reference():
    rng = random.Random(8)
    T = example()
    basis = T.basis()
    keys = sorted(basis)
    for l, B in rng.sample(keys, 12) + [(0, (2, 2)), (1, (3, 3))]:
        for x, y in pts(rng, 3) + [(F(1, 2), F(1, 2)), (F(3, 2), F(5, 4))]:
            assert T.evaluate(basis[(l, B)], x, y) == reference_value(T, l, B, x, y)


def test_truncated_function_in_the_example():
    T = example()
    basis = T.basis()
    c = basis[(0, (2, 2))]
    # the level 0 B-spline with support [0, 3]^2 loses its part inside [0, 2]^2
    assert T.evaluate(c, F(1, 2), F(1, 2)) == 0
    assert T.evaluate(c, F(5, 2), F(5, 2)) == T.evaluate(T.plain(0, (2, 2)), F(5, 2), F(5, 2))
    assert T.evaluate(c, F(3, 2), F(3, 2)) < T.evaluate(T.plain(0, (2, 2)), F(3, 2), F(3, 2))
