# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deferred-merge-embedding/. The authors are listed in prov/RDEGA7.jsonl.

import random
from fractions import Fraction
from itertools import product

from deferred_merge_embedding import dme, l1, wirelength


def check_tree(root, sinks):
    """Exact zero skew, edges at least the distance, sinks at their points."""
    delays = {}

    def walk(v, acc):
        if v.sink is not None:
            assert v.pt == (sinks[v.sink][0], sinks[v.sink][1])
            delays[v.sink] = acc
        for k in v.kids:
            assert k.edge >= l1(v.pt, k.pt)
            walk(k, acc + k.edge)

    walk(root, Fraction(0))
    assert set(delays) == set(range(len(sinks)))
    assert set(delays.values()) == {root.t}


def random_topology(rng, items):
    if len(items) == 1:
        return items[0]
    k = rng.randint(1, len(items) - 1)
    return (random_topology(rng, items[:k]), random_topology(rng, items[k:]))


def internal_nodes(topo, out):
    if isinstance(topo, tuple):
        out.append(topo)
        internal_nodes(topo[0], out)
        internal_nodes(topo[1], out)
    return out


def brute_cost(sinks, topo, step):
    """Least wire of a zero-skew tree on the topology over all placements of
    the internal nodes on a grid of the bounding box. For fixed points the
    least cost sets each delay t(v) = max over children of t(c) + d(v, c),
    since the cost 2 t(root) + sum of the other internal t(v) grows with every
    t(v). Clamping the points into the box never makes a distance longer."""
    xs = [p[0] for p in sinks]
    ys = [p[1] for p in sinks]
    gx = [Fraction(min(xs)) + step * i for i in range(int((max(xs) - min(xs)) / step) + 1)]
    gy = [Fraction(min(ys)) + step * i for i in range(int((max(ys) - min(ys)) / step) + 1)]
    grid = [(x, y) for x in gx for y in gy]
    nodes = internal_nodes(topo, [])
    best = None
    for pick in product(grid, repeat=len(nodes)):
        pos = {id(t): p for t, p in zip(nodes, pick)}

        def solve(t):
            if not isinstance(t, tuple):
                return sinks[t], Fraction(0), Fraction(0)
            p = pos[id(t)]
            (pa, ta, ca), (pb, tb, cb) = solve(t[0]), solve(t[1])
            tv = max(ta + l1(p, pa), tb + l1(p, pb))
            return p, tv, ca + cb + (tv - ta) + (tv - tb)

        cost = solve(topo)[2]
        best = cost if best is None else min(best, cost)
    return best


def test_zero_skew_exact(rng=random.Random(45)):
    for _ in range(200):
        n = rng.randint(1, 9)
        sinks = [(rng.randint(0, 20), rng.randint(0, 20)) for _ in range(n)]
        order = list(range(n))
        rng.shuffle(order)
        topo = random_topology(rng, order)
        root = dme(sinks, topo)
        check_tree(root, sinks)
        src = (rng.randint(0, 20), rng.randint(0, 20))
        root2 = dme(sinks, topo, source=src)
        check_tree(root2, sinks)
        assert wirelength(root2) == wirelength(root)


def test_least_wire_against_grid(rng=random.Random(2718)):
    equal = 0
    cases = 0
    for _ in range(24):
        n = rng.choice([3, 3, 4])
        sinks = [(rng.randint(0, 2), rng.randint(0, 2)) for _ in range(n)]
        topo = ((0, 1), 2) if n == 3 else rng.choice([((0, 1), (2, 3)), (((0, 1), 2), 3)])
        root = dme(sinks, topo)
        check_tree(root, sinks)
        step = Fraction(1, 4) if n == 3 else Fraction(1, 2)
        grid_best = brute_cost(sinks, topo, step)
        assert wirelength(root) <= grid_best
        cases += 1
        equal += wirelength(root) == grid_best
    # DME is never worse than a grid placement, and on these small boxes the
    # best grid placement is as good as DME, so the two values are equal
    assert equal == cases


def test_example_of_the_page():
    sinks = [(1, 3), (0, 1), (2, 0), (3, 2)]
    root = dme(sinks, ((0, 1), (2, 3)))
    check_tree(root, sinks)
    left, right = root.kids
    h = Fraction(1, 2)
    assert (left.t, right.t, root.t) == (3 * h, 3 * h, 2)
    assert root.pt == (3 * h, 3 * h) and left.pt == (1, 3 * h) and right.pt == (2, 3 * h)
    assert (left.edge, right.edge) == (h, h)
    assert wirelength(root) == 7
    assert brute_cost(sinks, ((0, 1), (2, 3)), h) == 7
