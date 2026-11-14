# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tsay-zero-skew/. The authors are listed in prov/J8K07F.jsonl.

import random
from fractions import Fraction

from tsay_zero_skew import Node, l1, merge, wirelength, zero_skew_tree


def elmore_to_sinks(root, r, c):
    """Elmore delay from the root to every sink as the sum of R_ik C_k over
    the pi model of all wires, with no use of the subtree summaries."""
    nodes, parent_path = [], {}
    cap = {}
    stack = [(root, ())]
    while stack:
        v, path = stack.pop()
        nodes.append(v)
        parent_path[id(v)] = path  # resistances of the edges from the root
        cap[id(v)] = cap.get(id(v), Fraction(0)) + (v.cap if v.sink is not None else 0)
        for k, length in v.kids:
            cap[id(v)] += c * length / 2
            cap[id(k)] = c * length / 2
            stack.append((k, path + ((id(k), r * length),)))
    out = {}
    for s in nodes:
        if s.sink is None:
            continue
        ps = dict(parent_path[id(s)])
        total = Fraction(0)
        for k in nodes:
            common = sum(res for e, res in parent_path[id(k)] if e in ps)
            total += common * cap[id(k)]
        out[s.sink] = total
    return out


def random_topology(rng, items):
    if len(items) == 1:
        return items[0]
    k = rng.randint(1, len(items) - 1)
    return (random_topology(rng, items[:k]), random_topology(rng, items[k:]))


def merges_elongate(node, r, c):
    """Does some merge of the tree need a wire longer than the distance?"""
    if not node.kids:
        return False
    (a, la), (b, lb) = node.kids
    return la + lb != l1(a.pt, b.pt) or merges_elongate(a, r, c) or merges_elongate(b, r, c)


def test_zero_skew_exact(rng=random.Random(80701)):
    exact_cases = 0
    for _ in range(150):
        n = rng.randint(1, 7)
        sinks = [((rng.randint(0, 12), rng.randint(0, 12)), rng.randint(1, 4)) for _ in range(n)]
        order = list(range(n))
        rng.shuffle(order)
        topo = random_topology(rng, order)
        r, c = Fraction(rng.randint(1, 3)), Fraction(rng.randint(1, 3))
        root = zero_skew_tree(sinks, topo, r, c)
        delays = elmore_to_sinks(root, r, c)
        assert set(delays) == set(range(n))
        for s in delays:
            if merges_elongate(root, r, c):
                assert abs(delays[s] - root.t) < Fraction(1, 10**40)
            else:
                assert delays[s] == root.t
        if not merges_elongate(root, r, c):
            exact_cases += 1
            # without elongation each merge uses exactly the distance between the roots
            def check(v):
                if v.kids:
                    (a, la), (b, lb) = v.kids
                    assert la + lb == l1(a.pt, b.pt)
                    assert l1(v.pt, a.pt) == la and l1(v.pt, b.pt) == lb
                    check(a)
                    check(b)
            check(root)
        assert wirelength(root) >= 0
    assert exact_cases > 50


def test_tap_point_against_grid(rng=random.Random(12)):
    # the skew at a tap s along the wire grows strictly with s, so a grid search
    # sees one sign change, at the tap of Tsay's formula
    for _ in range(200):
        r, c = Fraction(rng.randint(1, 3)), Fraction(rng.randint(1, 3))
        a = Node((Fraction(rng.randint(0, 9)), Fraction(rng.randint(0, 9))), Fraction(rng.randint(1, 9)), Fraction(rng.randint(0, 60)), [])
        b = Node((Fraction(rng.randint(0, 9)), Fraction(rng.randint(0, 9))), Fraction(rng.randint(1, 9)), Fraction(rng.randint(0, 60)), [])
        L = l1(a.pt, b.pt)
        if L == 0:
            continue
        m = merge(a, b, r, c)
        (_, la), (_, lb) = m.kids

        def skew(s):
            return (a.t + r * s * (c * s / 2 + a.cap)) - (b.t + r * (L - s) * (c * (L - s) / 2 + b.cap))

        grid = [L * Fraction(j, 64) for j in range(65)]
        signs = [skew(s) for s in grid]
        assert all(x < y for x, y in zip(signs, signs[1:]))
        if la + lb == L:
            assert skew(la) == 0
            assert all((s < la) == (skew(s) < 0) for s in grid if s != la)
        else:
            assert all(x > 0 for x in signs) or all(x < 0 for x in signs)


def test_exact_elongation():
    r = c = Fraction(1)
    a = Node((Fraction(0), Fraction(0)), Fraction(1), Fraction(4), [])
    b = Node((Fraction(1), Fraction(0)), Fraction(1), Fraction(0), [])
    m = merge(a, b, r, c)
    (_, la), (_, lb) = m.kids
    assert (la, lb, m.pt, m.t) == (0, 2, (0, 0), 4)
    assert m.cap == 1 + 1 + 2


def test_example_of_the_page():
    sinks = [((5, 7), 3), ((2, 0), 2), ((6, 2), 1), ((6, 8), 2)]
    r, c = Fraction(1), Fraction(1)
    root = zero_skew_tree(sinks, ((0, 1), (2, 3)), r, c)
    (left, ll), (right, lr) = root.kids
    assert left.pt == (2, Fraction(16, 3)) and left.t == Fraction(224, 9) and left.cap == 15
    assert right.pt == (6, Fraction(16, 3)) and right.t == Fraction(80, 9) and right.cap == 9
    assert (ll, lr, root.pt, root.t, root.cap) == (1, 3, (3, Fraction(16, 3)), Fraction(727, 18), 28)
    assert wirelength(root) == 20
    delays = elmore_to_sinks(root, r, c)
    assert set(delays.values()) == {Fraction(727, 18)}
