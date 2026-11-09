# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/decision-diagram/. The authors are listed in prov/YY3W21.jsonl.

import operator
import random

from decision_diagram import DD


def check_reduced(d: DD) -> None:
    seen = set()
    for u, (i, rest) in enumerate(d.nodes):
        if i == d.n:
            key = ("value", rest)
        else:
            assert len(set(rest)) > 1, "a node has all children equal"
            assert all(d.var(c) > i for c in rest), "the order is broken"
            assert all(c < u for c in rest)
            key = rest
        assert (i, key) not in seen, "two nodes are equal"
        seen.add((i, key))


def random_dom(rng: random.Random) -> list[int]:
    while True:
        dom = [rng.randint(2, 3) for _ in range(rng.randint(1, 6))]
        size = 1
        for x in dom:
            size *= x
        if size <= 400:
            return dom


def test_example() -> None:
    # x_0 in {0, 1, 2}, x_1 in {0, 1}; f = x_0 + x_1 and g = max(x_0, x_1).
    d = DD([3, 2])
    f = d.build([0, 1, 2, 1, 2, 3])
    g = d.build([0, 1, 2, 1, 1, 2])
    assert d.size(f) == 1 + 3 + 4  # one root, three nodes on x_1, four values
    s = d.apply(operator.add, f, g)
    assert d.table(s) == [0, 2, 4, 2, 3, 5]
    assert d.apply(operator.eq, f, f) == d.terminal(True)
    check_reduced(d)


def test_boolean_case_matches_bdd_sizes() -> None:
    d = DD([2] * 4)
    parity = d.build([bin(a).count("1") & 1 for a in range(16)])
    assert d.size(parity) == 2 * 4 + 1
    pairs = d.build([int((a & 3) == 3 or (a >> 2 & 3) == 3) for a in range(16)])
    assert d.size(pairs) == 2 * 2 + 2


def test_apply_against_tables() -> None:
    rng = random.Random(2000)
    ops = [operator.add, operator.mul, max, min, operator.eq, operator.sub]
    for _ in range(60):
        dom = random_dom(rng)
        d = DD(dom)
        size = len(d.table(d.terminal(0)))
        t1 = [rng.randint(0, 3) for _ in range(size)]
        t2 = [rng.randint(0, 3) for _ in range(size)]
        f, g = d.build(t1), d.build(t2)
        assert d.table(f) == t1 and d.table(g) == t2
        for op in ops:
            r = d.apply(op, f, g)
            assert d.table(r) == [op(a, b) for a, b in zip(t1, t2)]
        check_reduced(d)


def test_canonical_across_construction_orders() -> None:
    rng = random.Random(1993)
    for _ in range(40):
        dom = random_dom(rng)
        d = DD(dom)
        size = len(d.table(d.terminal(0)))
        t = [rng.randint(0, 2) for _ in range(size)]
        direct = d.build(t)
        # Sum of value * indicator over all points, added in a random order.
        points = list(range(size))
        rng.shuffle(points)
        acc = d.terminal(0)
        for a in points:
            ind = d.build([t[a] if b == a else 0 for b in range(size)])
            acc = d.apply(operator.add, acc, ind)
        assert acc == direct
        check_reduced(d)


def test_terminals_and_constant() -> None:
    d = DD([3, 3])
    c = d.build([7] * 9)
    assert c == d.terminal(7) and d.size(c) == 1
    assert d.evaluate(c, [2, 1]) == 7
