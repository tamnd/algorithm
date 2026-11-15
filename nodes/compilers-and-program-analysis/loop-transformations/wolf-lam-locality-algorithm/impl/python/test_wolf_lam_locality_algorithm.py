# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wolf-lam-locality-algorithm/. The authors are listed in prov/SBSZSV.jsonl.

import random
from collections import OrderedDict
from fractions import Fraction
from itertools import combinations, permutations, product

from wolf_lam_locality_algorithm import (
    count_classes,
    in_image,
    make_band,
    mat_vec,
    nest_cost,
    rank,
    reuse_spaces,
    spatial,
    tiled_order,
    transformed,
    unit,
    wolf_lam,
)

# A nest is a box of iterations and a list of statements (write, reads).
# An access is (array, H, c) and touches array[H i + c].


def elem(acc, i):
    arr, H, c = acc
    return (arr, tuple(sum(a * x for a, x in zip(row, i)) + o for row, o in zip(H, c)))


def points_of(bounds):
    return list(product(*[range(lo, hi + 1) for lo, hi in bounds]))


def true_dependences(points, stmts):
    """All pairs of statement instances, in original order, that touch one element with a write."""
    inst = [(i, s) for i in points for s in range(len(stmts))]
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
                deps.append((i, j))
    return deps


def distances_of(deps):
    return sorted({tuple(b - a for a, b in zip(i, j)) for i, j in deps if i != j})


def start_value(e):
    name, idx = e
    return (ord(name) % 7 + 3 * sum((p + 2) * v for p, v in enumerate(idx))) % 101


def run(order, stmts):
    mem = {}
    for i in order:
        for s, (w, reads) in enumerate(stmts):
            vals = [mem.get(elem(r, i), start_value(elem(r, i))) for r in reads]
            mem[elem(w, i)] = (sum((n + 1) * v for n, v in enumerate(vals)) * 3 + s + 1) % 1000003
    return mem


def random_row(rnd, k):
    j = rnd.randrange(k)
    row = [0] * k
    row[j] = 1
    if k > 1 and rnd.random() < 0.2:
        l = rnd.choice([x for x in range(k) if x != j])
        row[l] = rnd.choice((1, -1))
    return row


def random_access(rnd, k, arr):
    dims = rnd.randint(1, 2)
    H = [random_row(rnd, k) for _ in range(dims)]
    c = tuple(rnd.randint(-1, 1) for _ in range(dims))
    return (arr, H, c)


def random_nest(rnd, k):
    bounds = [(0, rnd.randint(1, 3)) for _ in range(k)]
    stmts = []
    for _ in range(rnd.randint(1, 2)):
        w = random_access(rnd, k, rnd.choice("AB"))
        reads = [random_access(rnd, k, rnd.choice("AB")) for _ in range(rnd.randint(1, 3))]
        stmts.append((w, reads))
    return bounds, stmts


def accesses_of(stmts):
    out = []
    for w, reads in stmts:
        out.append(w)
        out.extend(reads)
    return out


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


def lex_pos(v):
    for x in v:
        if x != 0:
            return x > 0
    return False


def order_keeps(order, deps):
    pos = {p: n for n, p in enumerate(order)}
    return all(pos[i] < pos[j] for i, j in deps if i != j)


def misses(order, accesses, ncols, line, cache_lines):
    """LRU misses when every array is n x ncols, row-major, and a line holds `line` elements."""
    cache = OrderedDict()
    base = {}
    count = 0
    for i in order:
        for acc in accesses:
            name, idx = elem(acc, i)
            b = base.setdefault(name, len(base) * 1000000)
            addr = b + (idx[0] * ncols + idx[1] if len(idx) == 2 else idx[0])
            key = addr // line
            if key in cache:
                cache.move_to_end(key)
            else:
                count += 1
                cache[key] = True
                if len(cache) > cache_lines:
                    cache.popitem(last=False)
    return count


# ---------------------------------------------------------------- examples from the page

COLUMN = [("A", [[0, 1], [1, 0]], (0, 0))]
SOR_H = [[0, 1, 0], [0, 0, 1]]
SOR = [("A", SOR_H, c) for c in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]]
SOR_D = [(0, 1, 0), (0, 0, 1), (1, 0, 0), (1, -1, 0), (1, 0, -1)]
MATMUL = [
    ("C", [[1, 0, 0], [0, 1, 0]], (0, 0)),
    ("A", [[1, 0, 0], [0, 0, 1]], (0, 0)),
    ("B", [[0, 0, 1], [0, 1, 0]], (0, 0)),
]


def test_column_traversal_is_interchanged():
    best = wolf_lam(COLUMN, [], 2, line=8, s=100)
    assert best["I"] == (0,)
    assert best["cost"] == Fraction(1, 8)
    assert best["T"] == [[0, 1], [1, 0]]
    pts = points_of([(0, 63), (0, 63)])
    order = tiled_order(pts, best["T"], best["m"], 8)
    assert misses(pts, COLUMN, 64, 8, 16) == 4096
    assert misses(order, COLUMN, 64, 8, 16) == 512


def test_sor_costs_and_skew():
    l, s = 8, 100
    assert nest_cost(SOR, (2,), 3, l, s) == Fraction(3, l)
    assert nest_cost(SOR, (1, 2), 3, l, s) == Fraction(1, l)
    assert nest_cost(SOR, (0, 1, 2), 3, l, s) == Fraction(1, l * s)
    assert make_band(SOR_D, (0,), 3) is None
    best = wolf_lam(SOR, SOR_D, 3, l, s)
    assert best["I"] == (0, 1, 2)
    T = best["T"]
    assert T == [[1, 0, 0], [1, 1, 0], [2, 1, 1]]
    assert all(min(transformed(T, d)) >= 0 for d in SOR_D)
    # The SOR nest itself: brute-force legality and equal final arrays.
    stmts = [(SOR[0], SOR)]
    pts = points_of([(0, 2), (1, 4), (1, 4)])
    deps = true_dependences(pts, stmts)
    assert set(SOR_D) <= set(distances_of(deps))
    for B in (2, 3):
        order = tiled_order(pts, T, 3, B)
        assert order_keeps(order, deps)
        assert run(order, stmts) == run(pts, stmts)
        # Tiling the same band without the skew breaks a dependence and the result.
        bad = tiled_order(pts, [[1, 0, 0], [0, 1, 0], [0, 0, 1]], 3, B)
        assert not order_keeps(bad, deps)
        assert run(bad, stmts) != run(pts, stmts)
    # Fewer misses than the original order on a larger grid.
    pts = points_of([(0, 7), (1, 30), (1, 30)])
    order = tiled_order(pts, T, 3, 8)
    assert misses(order, SOR, 32, 8, 32) < misses(pts, SOR, 32, 8, 32)


def test_matmul_costs():
    l, s = 8, 100
    assert nest_cost(MATMUL, (1, 2), 3, l, s) == Fraction(2, l * s) + Fraction(1, l)
    assert nest_cost(MATMUL, (0, 1, 2), 3, l, s) == Fraction(3, l * s)
    best = wolf_lam(MATMUL, [(0, 0, 1)], 3, l, s)
    assert best["I"] == (0, 1, 2) and best["m"] == 3
    pts = points_of([(0, 15), (0, 15), (0, 15)])
    order = tiled_order(pts, best["T"], 3, 4)
    acc = MATMUL + [MATMUL[0]]
    assert misses(pts, acc, 16, 8, 16) == 4160
    assert misses(order, acc, 16, 8, 16) == 416


# ---------------------------------------------------------------- reuse spaces against brute force

def test_reuse_spaces_match_brute_force():
    rnd = random.Random(7)
    for _ in range(200):
        k = rnd.randint(1, 3)
        _, H, _ = random_access(rnd, k, "A")
        R_ST, R_SS = reuse_spaces(H, k)
        assert len(R_ST) == k - rank(H, k)
        assert all(not any(mat_vec(H, b)) for b in R_ST)
        assert all(not any(mat_vec(spatial(H), b)) for b in R_SS)
        for r in product(range(-2, 3), repeat=k):
            same_elem = all(sum(a * x for a, x in zip(row, r)) == 0 for row in H)
            same_row = all(sum(a * x for a, x in zip(row, r)) == 0 for row in H[:-1])
            assert same_elem == (rank(R_ST + [r], k) == len(R_ST))
            assert same_row == (rank(R_SS + [r], k) == len(R_SS))


def test_group_classes_match_brute_force():
    rnd = random.Random(8)
    for _ in range(150):
        k = rnd.randint(1, 3)
        dims = rnd.randint(1, 2)
        # Subscripts that are loop indices plus constants.
        H = []
        for _ in range(dims):
            row = [0] * k
            row[rnd.randrange(k)] = 1
            H.append(row)
        offs = sorted({tuple(rnd.randint(-2, 2) for _ in range(dims)) for _ in range(rnd.randint(1, 4))})
        I = tuple(j for j in range(k) if rnd.random() < 0.5)
        L = [unit(j, k) for j in I]
        # Brute force: c1 ~ c2 when some integer r on the loops of I gives H r = c1 - c2.
        rs = []
        for vals in product(range(-4, 5), repeat=len(I)):
            r = [0] * k
            for j, v in zip(I, vals):
                r[j] = v
            rs.append(tuple(sum(a * x for a, x in zip(row, r)) for row in H))
        reach = set(rs)
        parent = {c: c for c in offs}

        def find(c):
            while parent[c] != c:
                c = parent[c]
            return c

        for a, b in combinations(offs, 2):
            diff = tuple(x - y for x, y in zip(a, b))
            assert (diff in reach) == in_image(H, L, diff, k)
            if diff in reach:
                parent[find(a)] = find(b)
        assert count_classes(H, offs, L, k) == len({find(c) for c in offs})


# ---------------------------------------------------------------- legality on random nests

def test_random_nests_legal_and_same_result():
    rnd = random.Random(2025)
    for _ in range(70):
        k = rnd.randint(1, 3)
        bounds, stmts = random_nest(rnd, k)
        pts = points_of(bounds)
        deps = true_dependences(pts, stmts)
        D = distances_of(deps)
        assert all(lex_pos(d) for d in D)
        want = run(pts, stmts)
        best = wolf_lam(accesses_of(stmts), D, k)
        assert best is not None
        for I in [best["I"]] + [I for n in range(k + 1) for I in combinations(range(k), n)]:
            band = make_band(D, I, k)
            if band is None:
                continue
            T, m = band
            assert m == len(I) and abs(det(T)) == 1
            for d in D:
                y = transformed(T, d)
                outer, inner = y[:k - m], y[k - m:]
                assert lex_pos(outer) or (not any(outer) and min(inner) >= 0 and any(inner))
            for B in (1, 2, 3):
                order = tiled_order(pts, T, m, B)
                assert sorted(order) == pts
                assert order_keeps(order, deps)
                assert run(order, stmts) == want


def test_band_found_when_a_signed_permutation_is_legal():
    rnd = random.Random(31)
    for _ in range(300):
        k = rnd.randint(1, 3)
        D = []
        for _ in range(rnd.randint(1, 4)):
            while True:
                d = tuple(rnd.randint(-2, 2) for _ in range(k))
                if lex_pos(d):
                    break
            D.append(d)
        for n in range(k + 1):
            for I in combinations(range(k), n):
                legal = False
                for perm in permutations(range(k)):
                    if sorted(perm[k - n:]) != list(I):
                        continue
                    for signs in product((1, -1), repeat=k):
                        if all(lex_pos([sg * d[j] for sg, j in zip(signs, perm)]) for d in D):
                            legal = True
                assert (make_band(D, I, k) is not None) == legal


if __name__ == "__main__":
    test_column_traversal_is_interchanged()
    test_sor_costs_and_skew()
    test_matmul_costs()
    test_reuse_spaces_match_brute_force()
    test_group_classes_match_brute_force()
    test_random_nests_legal_and_same_result()
    test_band_found_when_a_signed_permutation_is_legal()
    print("ok")
