# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/and-inverter-graph/. The authors are listed in prov/PGBE80.jsonl.

import itertools
import random

from and_inverter_graph import Aig


def test_full_adder_example() -> None:
    g = Aig(3)
    a, b, c = g.input(1), g.input(2), g.input(3)
    t = g.xor(a, b)
    s = g.xor(t, c)
    before = g.num_ands()
    carry = g.or_(g.and_(a, b), g.and_(t, c))
    assert (t, s) == (12, 18)
    assert before == 6
    assert g.num_ands() == 7
    assert carry == 21
    assert g.simulate([a, b, c, s, carry]) == [240, 204, 170, 150, 232]
    assert max(g.levels()) == 4


def test_trivial_rules() -> None:
    g = Aig(2)
    a, b = g.input(1), g.input(2)
    assert g.and_(a, 0) == 0
    assert g.and_(1, a) == a
    assert g.and_(a, a) == a
    assert g.and_(a, a ^ 1) == 0
    assert g.num_ands() == 0
    x = g.and_(a, b)
    assert g.and_(b, a) == x
    assert g.or_(a, 1) == 1
    assert g.num_ands() == 1


def test_hashing_is_not_canonical() -> None:
    g = Aig(3)
    a, b, c = g.input(1), g.input(2), g.input(3)
    left = g.and_(g.and_(a, b), c)
    right = g.and_(a, g.and_(b, c))
    assert left != right
    assert g.simulate([left]) == g.simulate([right])


def test_no_two_nodes_share_fanins() -> None:
    rng = random.Random(7)
    g = Aig(4)
    lits = [0, 1] + [g.input(i) ^ c for i in range(1, 5) for c in (0, 1)]
    for _ in range(300):
        x = g.and_(rng.choice(lits) ^ rng.randrange(2), rng.choice(lits) ^ rng.randrange(2))
        lits.append(x)
    pairs = list(zip(g.fanin0[g.n + 1:], g.fanin1[g.n + 1:]))
    assert len(pairs) == len(set(pairs))
    for v in range(g.n + 1, len(g.fanin0)):
        a, b = g.fanin0[v], g.fanin1[v]
        assert 2 <= a < b and (a >> 1) < v and (b >> 1) < v and a ^ 1 != b
        assert g.table[(a, b)] == v


def random_formula(rng: random.Random, n: int, depth: int):
    if depth == 0 or rng.random() < 0.2:
        return ("x", rng.randrange(1, n + 1), rng.randrange(2))
    op = rng.choice(["and", "or", "xor", "mux"])
    k = 3 if op == "mux" else 2
    return (op, [random_formula(rng, n, depth - 1) for _ in range(k)], rng.randrange(2))


def evaluate(f, x: tuple[int, ...]) -> int:
    if f[0] == "x":
        return x[f[1] - 1] ^ f[2]
    vals = [evaluate(h, x) for h in f[1]]
    if f[0] == "and":
        v = vals[0] & vals[1]
    elif f[0] == "or":
        v = vals[0] | vals[1]
    elif f[0] == "xor":
        v = vals[0] ^ vals[1]
    else:
        v = vals[1] if vals[0] else vals[2]
    return v ^ f[2]


def build(g: Aig, f) -> int:
    if f[0] == "x":
        return g.input(f[1]) ^ f[2]
    args = [build(g, h) for h in f[1]]
    if f[0] == "and":
        v = g.and_(*args)
    elif f[0] == "or":
        v = g.or_(*args)
    elif f[0] == "xor":
        v = g.xor(*args)
    else:
        v = g.mux(*args)
    return v ^ f[2]


def test_random_formulas_against_truth_tables() -> None:
    rng = random.Random(2024)
    for trial in range(600):
        n = rng.randrange(1, 6)
        g = Aig(n)
        forms = [random_formula(rng, n, rng.randrange(1, 5)) for _ in range(3)]
        outs = [build(g, f) for f in forms]
        tables = g.simulate(outs)
        for f, t in zip(forms, tables):
            for m, x in enumerate(itertools.product((0, 1), repeat=n)):
                assert (t >> m) & 1 == evaluate(f, x)
        # building the same formulas again adds no node
        size = g.num_ands()
        assert [build(g, f) for f in forms] == outs
        assert g.num_ands() == size


def test_equal_tables_after_rebuild_in_fresh_graph() -> None:
    rng = random.Random(11)
    for _ in range(200):
        n = rng.randrange(2, 5)
        f = random_formula(rng, n, 4)
        g1, g2 = Aig(n), Aig(n)
        assert g1.simulate([build(g1, f)]) == g2.simulate([build(g2, f)])
