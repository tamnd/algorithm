# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/majority-inverter-graph/. The authors are listed in prov/AVZMQ8.jsonl.

import itertools
import random

from majority_inverter_graph import Mig, maj3


def M(x: int, y: int, z: int) -> int:
    return 1 if x + y + z >= 2 else 0


def points(k: int):
    return itertools.product((0, 1), repeat=k)


def test_axioms_on_all_assignments() -> None:
    for x, y, z in points(3):
        # commutativity
        assert M(x, y, z) == M(y, x, z) == M(z, y, x)
        # majority
        assert M(x, x, z) == x and M(x, 1 - x, z) == z
        # inverter propagation
        assert 1 - M(x, y, z) == M(1 - x, 1 - y, 1 - z)
        # AND and OR
        assert M(x, y, 0) == (x & y) and M(x, y, 1) == (x | y)
    for x, y, z, u in points(4):
        # associativity
        assert M(x, u, M(y, u, z)) == M(z, u, M(y, u, x))
        # complementary associativity
        assert M(x, u, M(y, 1 - u, z)) == M(x, u, M(y, x, z))
    for x, y, z, u, v in points(5):
        # distributivity
        assert M(x, y, M(u, v, z)) == M(M(x, y, u), M(x, y, v), z)


def test_relevance_for_every_function_of_three_inputs() -> None:
    # M(x, y, z) = M(x, y, z with x replaced by not y), for every z(x, y, w)
    for table in range(256):
        def z(x: int, y: int, w: int) -> int:
            return (table >> (4 * x + 2 * y + w)) & 1
        for x, y, w in points(3):
            assert M(x, y, z(x, y, w)) == M(x, y, z(1 - y, y, w))


def test_substitution_on_random_functions() -> None:
    rng = random.Random(3)
    for _ in range(500):
        tx, ty, tz = (rng.randrange(256) for _ in range(3))

        def f(v: int, u: int, w: int) -> int:
            def ev(t: int) -> int:
                return (t >> (4 * v + 2 * u + w)) & 1
            return M(ev(tx), ev(ty), ev(tz))

        for v, u, w in points(3):
            lhs = f(v, u, w)
            rhs = M(v, M(1 - v, f(u, u, w), u), M(1 - v, f(1 - u, u, w), 1 - u))
            assert lhs == rhs


def test_normal_form_merges_axiom_sides() -> None:
    g = Mig(3)
    x, y, z = 2, 4, 6
    m = g.maj(x, y, z)
    assert g.maj(y, x, z) == g.maj(z, y, x) == m
    assert g.maj(x, x, z) == x and g.maj(x, x ^ 1, z) == z
    assert g.maj(x ^ 1, y ^ 1, z ^ 1) == m ^ 1
    assert g.num_nodes() == 1
    for v in range(g.n + 1, len(g.fanins)):
        a, b, c = g.fanins[v]
        assert a < b < c and (a & 1) + (b & 1) + (c & 1) <= 1


def test_associativity_and_distributivity_as_graphs() -> None:
    g = Mig(5)
    x, y, z, u, v = (2 * i for i in range(1, 6))
    left = g.maj(x, u, g.maj(y, u, z))
    right = g.maj(z, u, g.maj(y, u, x))
    assert g.simulate([left]) == g.simulate([right])
    d1 = g.maj(x, y, g.maj(u, v, z))
    d2 = g.maj(g.maj(x, y, u), g.maj(x, y, v), z)
    assert g.simulate([d1]) == g.simulate([d2])


def test_full_adder_example() -> None:
    g = Mig(3)
    a, b, c = 2, 4, 6
    carry = g.maj(a, b, c)
    s = g.maj(carry ^ 1, c, g.maj(a, b, c ^ 1))
    assert g.num_nodes() == 3
    assert g.simulate([s, carry]) == [150, 232]
    assert g.depth([s, carry]) == 2


def test_depth_example() -> None:
    g = Mig(7)
    x, u, y, p, q, r, t = (2 * i for i in range(1, 8))
    z = g.maj(p, q, g.maj(r, t, g.and_(p, r)))
    f = g.maj(x, u, g.maj(y, u, z))
    f2 = g.maj(z, u, g.maj(y, u, x))
    assert (g.depth([z]), g.depth([f]), g.depth([f2])) == (3, 5, 4)
    assert g.simulate([f]) == g.simulate([f2])


def random_formula(rng: random.Random, n: int, depth: int):
    if depth == 0 or rng.random() < 0.2:
        return ("x", rng.randrange(1, n + 1), rng.randrange(2))
    op = rng.choice(["maj", "and", "or"])
    k = 3 if op == "maj" else 2
    return (op, [random_formula(rng, n, depth - 1) for _ in range(k)], rng.randrange(2))


def evaluate(f, x) -> int:
    if f[0] == "x":
        return x[f[1] - 1] ^ f[2]
    v = [evaluate(h, x) for h in f[1]]
    if f[0] == "maj":
        r = M(*v)
    elif f[0] == "and":
        r = v[0] & v[1]
    else:
        r = v[0] | v[1]
    return r ^ f[2]


def build(g: Mig, f) -> int:
    if f[0] == "x":
        return g.input(f[1]) ^ f[2]
    args = [build(g, h) for h in f[1]]
    r = g.maj(*args) if f[0] == "maj" else (g.and_(*args) if f[0] == "and" else g.or_(*args))
    return r ^ f[2]


def test_random_formulas_against_truth_tables() -> None:
    rng = random.Random(17)
    for _ in range(600):
        n = rng.randrange(1, 6)
        g = Mig(n)
        forms = [random_formula(rng, n, rng.randrange(1, 5)) for _ in range(3)]
        outs = [build(g, f) for f in forms]
        for f, t in zip(forms, g.simulate(outs)):
            for m, x in enumerate(points(n)):
                assert (t >> m) & 1 == evaluate(f, x)
        size = g.num_nodes()
        assert [build(g, f) for f in forms] == outs and g.num_nodes() == size
        keys = list(g.fanins[g.n + 1:])
        assert len(keys) == len(set(keys))


def test_bitwise_majority() -> None:
    assert maj3(0b1100, 0b1010, 0b0110) == 0b1110
