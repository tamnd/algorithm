# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/combinatorial-extension/. The authors are listed in prov/J6984A.jsonl.

import math
import random

from combinatorial_extension import alignment_of, ce, ce_all, rmsd_of_alignment


def walk(n, rng, step=3.8):
    """A chain-like C-alpha trace: steps of 3.8 A, each within about 80 degrees of the last one."""
    pts = [(0.0, 0.0, 0.0)]
    d = (1.0, 0.0, 0.0)
    for _ in range(n - 1):
        while True:
            v = [rng.gauss(0, 1) for _ in range(3)]
            nv = math.sqrt(sum(c * c for c in v))
            v = [c / nv for c in v]
            if sum(x * y for x, y in zip(v, d)) > 0.2:
                break
        d = tuple(v)
        pts.append(tuple(pts[-1][k] + step * d[k] for k in range(3)))
    return pts


def turn(p, t):
    c, s = math.cos(t), math.sin(t)
    return (c * p[0] - s * p[1] + 5.0, s * p[0] + c * p[1] - 3.0, p[2] + 2.0)


def example_pair():
    """The page example: 32 residues, and a turned noisy copy with 4 residues inserted after residue 16."""
    a = walk(32, random.Random(3))
    h = a[15]
    ins = [(h[0] + 3.0, h[1] + 2.0, h[2] + 1.0), (h[0] + 5.0, h[1] + 4.5, h[2] - 1.0),
           (h[0] + 4.0, h[1] + 6.0, h[2] - 3.5), (h[0] + 1.0, h[1] + 5.0, h[2] - 4.0)]
    noise = random.Random(9)
    b = [tuple(c + noise.gauss(0, 0.3) for c in turn(p, 0.7)) for p in a[:16] + ins + a[16:]]
    return a, b


# ---------- an independent oracle, written from the equations of the paper ----------

def o_self(a, b, p, m):
    i, j = p
    return sum(abs(math.dist(a[i + k], a[i + l]) - math.dist(b[j + k], b[j + l]))
               for k in range(m) for l in range(m)) / m ** 2


def o_pair(a, b, p, q, m):
    offs = [(0, 0), (m - 1, m - 1)] + [(k, m - 1 - k) for k in range(1, m - 1)]
    return sum(abs(math.dist(a[p[0] + x], a[q[0] + y]) - math.dist(b[p[1] + x], b[q[1] + y]))
               for x, y in offs) / m


def o_d(a, b, p, q, m):
    return o_self(a, b, p, m) if p == q else o_pair(a, b, p, q, m)


def o_step_ok(p, q, m, gap):
    ga, gb = q[0] - p[0] - m, q[1] - p[1] - m
    return ga >= 0 and gb >= 0 and min(ga, gb) == 0 and max(ga, gb) <= gap


def o_mean10(a, b, path, q, m):
    return sum(o_pair(a, b, p, q, m) for p in path) / len(path)


def o_mean11(a, b, path, m):
    return sum(o_d(a, b, p, q, m) for p in path for q in path) / len(path) ** 2


def o_valid(a, b, path, m, gap, d0, d1):
    if any(o_self(a, b, p, m) >= d0 for p in path):
        return False
    for t in range(1, len(path)):
        if not o_step_ok(path[t - 1], path[t], m, gap):
            return False
        if o_mean10(a, b, path[:t], path[t], m) >= d1 or o_mean11(a, b, path[:t + 1], m) >= d1:
            return False
    return True


def o_afps(a, b, m):
    return [(i, j) for i in range(len(a) - m + 1) for j in range(len(b) - m + 1)]


def o_all_paths(a, b, m, gap, d0, d1):
    """Every path that passes (1) to (5), (9), (10) and (11) at each step, by plain enumeration."""
    afps = o_afps(a, b, m)
    out = []

    def rec(path):
        out.append(list(path))
        for q in afps:
            if q[0] > path[-1][0] and q[1] > path[-1][1] and o_valid(a, b, path + [q], m, gap, d0, d1):
                rec(path + [q])

    for p in afps:
        if o_self(a, b, p, m) < d0:
            rec([p])
    return out


def o_greedy(a, b, start, m, gap, d0, d1):
    """The 'best' strategy from one start, with no pruning."""
    path = [start]
    while True:
        cands = [q for q in o_afps(a, b, m) if o_step_ok(path[-1], q, m, gap)
                 and o_self(a, b, q, m) < d0 and o_mean10(a, b, path, q, m) < d1]
        if not cands:
            return path
        q = min(cands, key=lambda q: (o_mean10(a, b, path, q, m), q))
        if o_mean11(a, b, path + [q], m) >= d1:
            return path
        path.append(q)


def random_case(rng):
    m = rng.choice([2, 3, 4])
    n_a, n_b = rng.randint(m, 11), rng.randint(m, 11)
    a = walk(n_a, rng)
    if rng.random() < 0.5:
        b = walk(n_b, rng)
    else:  # a noisy copy of a with a few residues inserted or deleted
        b = [tuple(c + rng.gauss(0, 0.6) for c in p) for p in a]
        for _ in range(rng.randint(0, 2)):
            k = rng.randrange(len(b) + 1)
            if rng.random() < 0.5 and len(b) > m:
                del b[min(k, len(b) - 1)]
            else:
                b.insert(k, tuple(rng.uniform(-10, 10) for _ in range(3)))
        b = [turn(p, rng.uniform(0, 6.3)) for p in b]
    gap = rng.choice([0, 1, 2, 3, 30])
    d0 = rng.choice([0.5, 1.0, 3.0])
    d1 = rng.choice([0.5, 1.0, 2.0, 4.0])
    return a, b, m, gap, d0, d1


# ---------- tests ----------

def test_example_of_the_page() -> None:
    a, b = example_pair()
    path = ce(a, b)
    assert path == [(0, 0), (8, 8), (16, 20), (24, 28)]
    pairs = alignment_of(path, 8)
    assert pairs == [(i, i if i < 16 else i + 4) for i in range(32)]
    assert abs(rmsd_of_alignment(a, b, pairs) - 0.5196) < 1e-4
    assert len(ce_all(a, b)) == 4
    assert abs(o_mean11(a, b, path, 8) - 0.3504) < 1e-4


def test_edges() -> None:
    rng = random.Random(4)
    a = walk(20, rng)
    assert ce(a[:7], a) == [] and ce(a, a[:7]) == []
    assert ce(a, a) == [(0, 0), (8, 8)]  # an identical copy: two AFPs, D = 0 everywhere
    assert ce(a, [turn(p, 1.0) for p in a]) == [(0, 0), (8, 8)]
    far = [(40.0 * k, 0.0, 0.0) for k in range(8)]
    assert ce(far, a[:8]) == []  # no AFP passes (9)
    assert ce(a, a, m=4, d1=0.0) == [(0, 0)]  # (10) fails at once, so each path has one AFP


def test_rmsd_of_alignment() -> None:
    rng = random.Random(5)
    for _ in range(100):
        a = walk(rng.randint(3, 12), rng)
        t = rng.uniform(0, 6.3)
        b = [turn(p, t) for p in a]
        pairs = [(i, i) for i in range(len(a))]
        assert rmsd_of_alignment(a, b, pairs) < 1e-6
        c = [tuple(x + rng.gauss(0, 1.0) for x in p) for p in a]
        r = rmsd_of_alignment(a, c, pairs)
        plain = math.sqrt(sum(math.dist(p, q) ** 2 for p, q in zip(a, c)) / len(a))
        assert r <= plain + 1e-9  # the identity is one of the superpositions


def test_all_strategy_against_enumeration() -> None:
    rng = random.Random(1)
    for _ in range(500):
        a, b, m, gap, d0, d1 = random_case(rng)
        paths = o_all_paths(a, b, m, gap, d0, d1)
        got = ce_all(a, b, m, gap, d0, d1)
        if not paths:
            assert got == []
            continue
        longest = max(len(p) for p in paths)
        assert len(got) == longest
        assert o_valid(a, b, got, m, gap, d0, d1)
        least = min(o_mean11(a, b, p, m) for p in paths if len(p) == longest)
        assert abs(o_mean11(a, b, got, m) - least) < 1e-9


def test_best_strategy_against_oracle() -> None:
    rng = random.Random(2)
    shorter = 0
    for _ in range(500):
        a, b, m, gap, d0, d1 = random_case(rng)
        got = ce(a, b, m, gap, d0, d1)
        starts = [p for p in o_afps(a, b, m) if o_self(a, b, p, m) < d0]
        if not starts:
            assert got == []
            continue
        greedy = [o_greedy(a, b, s, m, gap, d0, d1) for s in starts]
        assert len(got) == max(len(g) for g in greedy)  # the pruning of L5 loses nothing
        assert got in greedy
        assert o_valid(a, b, got, m, gap, d0, d1)
        assert len(got) <= len(ce_all(a, b, m, gap, d0, d1))
        shorter += len(got) < len(ce_all(a, b, m, gap, d0, d1))
    assert shorter > 0  # the greedy strategy is not exact
