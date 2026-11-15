# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lamport-hyperplane-method/. The authors are listed in prov/RCRHT9.jsonl.

import random
from fractions import Fraction
from itertools import product

from lamport_hyperplane_method import (
    box,
    check_time_function,
    fewest_fronts,
    hyperplane_matrix,
    inverse_map,
    lex_positive,
    scan,
    time_function,
    wavefronts,
)

# A nest: k, constraints, and statements. A statement is (write, reads);
# an access is (array, offsets) and touches array[i + offsets].


def points_of(constraints, k, bounds):
    """Brute-force list of the integer points of the space, in lexicographic order."""
    pts = []
    for i in product(*[range(lo, hi + 1) for lo, hi in bounds]):
        if all(sum(a * x for a, x in zip(ai, i)) + b >= 0 for ai, b in constraints):
            pts.append(i)
    return pts


def elem(acc, i):
    return (acc[0], tuple(x + o for x, o in zip(i, acc[1])))


def instances(points, stmts):
    """Statement instances in the original order: (iteration, statement index)."""
    return [(i, s) for i in points for s in range(len(stmts))]


def true_dependences(points, stmts):
    """All pairs (source, sink) of instances that touch one element, one of them a write."""
    inst = instances(points, stmts)
    deps = []
    for x in range(len(inst)):
        i, s = inst[x]
        w1 = elem(stmts[s][0], i)
        r1 = {elem(r, i) for r in stmts[s][1]}
        for y in range(x + 1, len(inst)):
            j, t = inst[y]
            w2 = elem(stmts[t][0], j)
            r2 = {elem(r, j) for r in stmts[t][1]}
            if w1 == w2 or w1 in r2 or w2 in r1:
                deps.append((inst[x], inst[y]))
    return deps


def start_value(e):
    name, idx = e
    return (ord(name) % 7 + 3 * sum((p + 2) * v for p, v in enumerate(idx))) % 101


def run(order, stmts):
    """Run the iterations in the given order; each iteration runs its statements in text order."""
    mem = {}
    for i in order:
        for s, (w, reads) in enumerate(stmts):
            vals = [mem.get(elem(r, i), start_value(elem(r, i))) for r in reads]
            mem[elem(w, i)] = (sum((n + 1) * v for n, v in enumerate(vals)) * 3 + s + 1) % 1000003
    return mem


def random_nest(rnd, k):
    bounds = [(rnd.randint(0, 2), 0) for _ in range(k)]
    bounds = [(lo, lo + rnd.randint(1, 3)) for lo, _ in bounds]
    cons = box(bounds)
    if k >= 2 and rnd.random() < 0.4:
        # A triangular space: i_1 - i_0 + c >= 0.
        a = [0] * k
        a[0], a[1] = -1, 1
        cons.append((tuple(a), rnd.randint(0, 2)))
    stmts = []
    for _ in range(rnd.randint(1, 2)):
        arr = rnd.choice("AB")
        w = (arr, tuple(0 for _ in range(k)))
        reads = []
        for _ in range(rnd.randint(1, 3)):
            reads.append((rnd.choice("AB"), tuple(rnd.randint(-2, 1) for _ in range(k))))
        stmts.append((w, reads))
    return bounds, cons, stmts


def distances_of(deps):
    out = set()
    for (i, _), (j, _) in deps:
        d = tuple(b - a for a, b in zip(i, j))
        if any(d):
            out.add(d)
    return sorted(out)


def det(m):
    m = [[Fraction(x) for x in row] for row in m]
    n, s = len(m), Fraction(1)
    for c in range(n):
        p = next((r for r in range(c, n) if m[r][c] != 0), None)
        if p is None:
            return Fraction(0)
        if p != c:
            m[c], m[p] = m[p], m[c]
            s = -s
        s *= m[c][c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return s


def test_stencil_example():
    # A[i][j] = A[i-1][j] + A[i][j-1] + A[i-1][j+1] has distances (1,0), (0,1), (1,-1).
    D = [(1, 0), (0, 1), (1, -1)]
    pi = time_function(D)
    assert pi == [2, 1]
    fr = wavefronts(box([(1, 4), (1, 5)]), 2, pi)
    assert len(fr) == 11
    assert [t for t, _ in fr] == list(range(3, 14))
    assert fr[0][1] == [(1, 1)]
    assert sorted(p for _, f in fr for p in f) == points_of(box([(1, 4), (1, 5)]), 2, [(1, 4), (1, 5)])


def test_construction_on_random_distances():
    rnd = random.Random(11)
    for _ in range(400):
        k = rnd.randint(1, 4)
        D = []
        for _ in range(rnd.randint(1, 5)):
            while True:
                d = tuple(rnd.randint(-3, 3) for _ in range(k))
                if lex_positive(d):
                    break
            D.append(d)
        pi = time_function(D)
        assert pi[-1] == 1 and all(p >= 0 for p in pi)
        assert check_time_function(pi, D)
        # Each entry is as small as the construction allows: lowering one outer
        # entry by 1 breaks some distance that leads at that level.
        for l in range(k - 1):
            if pi[l] > 0:
                q = list(pi)
                q[l] -= 1
                leading_here = [d for d in D if d[l] != 0 and not any(d[:l])]
                assert not check_time_function(q, leading_here)
        T = hyperplane_matrix(pi)
        assert abs(det(T)) == 1
        for _ in range(5):
            y = tuple(rnd.randint(-5, 5) for _ in range(k))
            i = inverse_map(pi, y)
            assert tuple(sum(a * x for a, x in zip(row, i)) for row in T) == y


def test_rejects_bad_distances():
    for D in ([(0, 0)], [(-1, 2)], [(0, -1)]):
        try:
            time_function(D)
        except ValueError:
            pass
        else:
            raise AssertionError("accepted %r" % (D,))


def test_scan_matches_brute_force():
    rnd = random.Random(5)
    for _ in range(150):
        k = rnd.randint(1, 3)
        bounds, cons, _ = random_nest(rnd, k)
        assert list(scan(cons, k)) == points_of(cons, k, bounds)


def check_schedule(fronts, points, deps):
    """Fronts cover every point once, and every dependence goes to a later front."""
    flat = [p for _, f in fronts for p in f]
    assert sorted(flat) == sorted(points) and len(flat) == len(set(flat))
    ts = [t for t, _ in fronts]
    assert ts == sorted(set(ts))
    when = {p: t for t, f in fronts for p in f}
    ok_order = all(when[i] < when[j] or i == j for (i, _), (j, _) in deps)
    no_inner = all(when[i] != when[j] or i == j for (i, _), (j, _) in deps)
    return ok_order and no_inner


def test_random_nests_legal_and_parallel_fronts():
    rnd = random.Random(2024)
    tried = 0
    while tried < 120:
        k = rnd.randint(1, 3)
        bounds, cons, stmts = random_nest(rnd, k)
        points = points_of(cons, k, bounds)
        if not points:
            continue
        tried += 1
        deps = true_dependences(points, stmts)
        D = distances_of(deps)
        pi = time_function(D, k)
        fronts = wavefronts(cons, k, pi)
        for t, f in fronts:
            assert all(sum(p * x for p, x in zip(pi, i)) == t for i in f)
        # Legality and no dependence between two points of one front.
        assert check_schedule(fronts, points, deps)
        # Running each front in a random order gives the original final state.
        want = run(points, stmts)
        for rep in range(3):
            order = []
            for _, f in fronts:
                g = list(f)
                rnd.shuffle(g)
                order.extend(g)
            assert run(order, stmts) == want
        # The brute-force best pi never needs more fronts than the construction.
        best = fewest_fronts(D, points, 3)
        assert best is not None and best[0] <= len(fronts)
        assert check_time_function(best[1], D)


def test_checker_rejects_a_bad_time_function():
    # Columns of the stencil (pi = (0, 1)) put (1, 2) and (2, 1) in one front,
    # though (2, 1) reads A[1][2].
    stmts = [(("A", (0, 0)), [("A", (-1, 0)), ("A", (0, -1)), ("A", (-1, 1))])]
    cons = box([(1, 3), (1, 3)])
    points = points_of(cons, 2, [(1, 3), (1, 3)])
    deps = true_dependences(points, stmts)
    assert distances_of(deps) == [(0, 1), (1, -1), (1, 0)]
    bad = {}
    for i in points:
        bad.setdefault(i[1], []).append(i)
    fronts = sorted(bad.items())
    assert not check_schedule(fronts, points, deps)
    order = [p for _, f in fronts for p in f]
    assert run(order, stmts) != run(points, stmts)


if __name__ == "__main__":
    test_stencil_example()
    test_construction_on_random_distances()
    test_rejects_bad_distances()
    test_scan_matches_brute_force()
    test_random_nests_legal_and_parallel_fronts()
    test_checker_rejects_a_bad_time_function()
    print("ok")
