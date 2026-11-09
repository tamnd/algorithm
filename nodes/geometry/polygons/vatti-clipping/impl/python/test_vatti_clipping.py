# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vatti-clipping/. The authors are listed in prov/AT6FZP.jsonl.

import random
from fractions import Fraction

import pytest

from vatti_clipping import combine, filled, vatti_clip


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def edges_of(contours):
    out = []
    for c in contours:
        n = len(c)
        out += [(c[i], c[(i + 1) % n]) for i in range(n) if c[i] != c[(i + 1) % n]]
    return out


def on_boundary(contours, q):
    for a, b in edges_of(contours):
        if orient(a, b, q) == 0 and min(a[0], b[0]) <= q[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= q[1] <= max(a[1], b[1]):
            return True
    return False


def winding(contours, q):
    """Total winding number by signed crossings of the downward vertical ray (q off the boundary)."""
    w = 0
    for a, b in edges_of(contours):
        if a[0] <= q[0] < b[0] and orient(a, b, q) > 0:
            w += 1
        elif b[0] <= q[0] < a[0] and orient(a, b, q) < 0:
            w -= 1
    return w


def twice_area(contours):
    return sum(orient((0, 0), a, b) for a, b in edges_of(contours))


def crossing_xs(e, f):
    (a, b), (c, d) = e, f
    den = (b[0] - a[0]) * (d[1] - c[1]) - (b[1] - a[1]) * (d[0] - c[0])
    if den == 0:
        return []
    t = Fraction((c[0] - a[0]) * (d[1] - c[1]) - (c[1] - a[1]) * (d[0] - c[0]), den)
    u = Fraction((c[0] - a[0]) * (b[1] - a[1]) - (c[1] - a[1]) * (b[0] - a[0]), den)
    if 0 <= t <= 1 and 0 <= u <= 1:
        return [a[0] + t * (b[0] - a[0])]
    return []


def slab_measure(operands, keep):
    """Exact area of {q : keep(w_1, ..., w_k)}, w_j the winding number of operands[j], by vertical
    slabs between consecutive event x values, where the cross-section length is linear in x."""
    groups = [edges_of(ops) for ops in operands]
    alle = [e for g in groups for e in g]
    xs = {Fraction(p[0]) for e in alle for p in e}
    for i in range(len(alle)):
        for j in range(i + 1, len(alle)):
            xs.update(crossing_xs(alle[i], alle[j]))
    xs = sorted(xs)
    total = Fraction(0)
    for x0, x1 in zip(xs, xs[1:]):
        xm = (x0 + x1) / 2
        hits = []
        for k, g in enumerate(groups):
            for a, b in g:
                if min(a[0], b[0]) < xm < max(a[0], b[0]):
                    y = a[1] + (xm - a[0]) * Fraction(b[1] - a[1]) / (b[0] - a[0])
                    hits.append((y, k, 1 if b[0] > a[0] else -1))
        hits.sort()
        w = [0] * len(groups)
        length = Fraction(0)
        for idx in range(len(hits) - 1):
            y, k, s = hits[idx]
            w[k] += s
            if keep(*w):
                length += hits[idx + 1][0] - y
        total += (x1 - x0) * length
    return total


def check(subject, clip, op, rule, result, rng, size, samples=25):
    def keep(ws, wc):
        return combine(filled(ws, rule), filled(wc, rule), op)

    assert Fraction(twice_area(result), 2) == slab_measure([subject, clip], keep)
    for _ in range(samples):
        q = (Fraction(rng.randint(-2, 3 * size + 2), 3), Fraction(rng.randint(-2, 3 * size + 2), 3))
        if on_boundary(subject, q) or on_boundary(clip, q):
            continue
        assert winding(result, q) == (1 if keep(winding(subject, q), winding(clip, q)) else 0)


U = [[(0, 0), (6, 0), (6, 6), (4, 6), (4, 2), (2, 2), (2, 6), (0, 6)]]
BAR = [[(-1, 4), (7, 4), (7, 5), (-1, 5)]]
STAR = [[(0, 10), (-6, -8), (10, 3), (-10, 3), (6, -8)]]


def test_worked_example() -> None:
    assert twice_area(vatti_clip(U, BAR, "intersection")) == 8
    assert twice_area(vatti_clip(U, BAR, "union")) == 64
    assert twice_area(vatti_clip(U, BAR, "difference")) == 48
    assert twice_area(vatti_clip(U, BAR, "xor")) == 56
    union = vatti_clip(U, BAR, "union")
    assert sorted(twice_area([c]) for c in union) == [-8, 72]


def test_fill_rules_on_a_pentagram() -> None:
    box = [[(-20, -20), (20, -20), (20, 20), (-20, 20)]]
    rng = random.Random(1)
    for rule in ("nonzero", "evenodd"):
        res = vatti_clip(STAR, box, "intersection", rule)
        check(STAR, box, "intersection", rule, res, rng, 20)
    # Even-odd leaves the central pentagon out, nonzero keeps it.
    assert winding(vatti_clip(STAR, box, "intersection", "evenodd"), (0, 0)) == 0
    assert winding(vatti_clip(STAR, box, "intersection", "nonzero"), (0, 0)) == 1


def test_degenerate_inputs() -> None:
    sq = [[(0, 0), (4, 0), (4, 4), (0, 4)]]
    right = [[(4, 0), (8, 0), (8, 4), (4, 4)]]
    corner = [[(4, 4), (8, 4), (8, 8), (4, 8)]]
    assert twice_area(vatti_clip(sq, right, "union")) == 64
    assert len(vatti_clip(sq, right, "union")) == 1
    assert vatti_clip(sq, right, "intersection") == []
    assert twice_area(vatti_clip(sq, corner, "union")) == 64
    assert vatti_clip(sq, sq, "xor") == []
    assert twice_area(vatti_clip(sq, sq, "union")) == 32
    assert vatti_clip([], sq, "intersection") == []
    assert twice_area(vatti_clip([], sq, "union")) == 32
    assert vatti_clip([[(0, 0), (1, 1), (2, 2)]], sq, "intersection") == []
    with pytest.raises(ValueError):
        vatti_clip(sq, sq, "minus")
    rng = random.Random(2)
    for op in ("intersection", "union", "difference", "xor"):
        check(sq, right, op, "nonzero", vatti_clip(sq, right, op), rng, 8, 60)
        check(sq, corner, op, "nonzero", vatti_clip(sq, corner, op), rng, 8, 60)


def test_holes() -> None:
    ring = [[(0, 0), (9, 0), (9, 9), (0, 9)], [(3, 3), (3, 6), (6, 6), (6, 3)]]
    plug = [[(2, 4), (7, 4), (7, 5), (2, 5)]]
    rng = random.Random(3)
    for op in ("intersection", "union", "difference", "xor"):
        for rule in ("nonzero", "evenodd"):
            check(ring, plug, op, rule, vatti_clip(ring, plug, op, rule), rng, 9, 80)


def random_contours(rng, size):
    return [
        [(rng.randint(0, size), rng.randint(0, size)) for _ in range(rng.randint(3, 6))]
        for _ in range(rng.randint(1, 2))
    ]


def test_random_self_intersecting_inputs() -> None:
    rng = random.Random(1992)
    for trial in range(160):
        size = rng.choice([4, 8, 12])
        subject, clip = random_contours(rng, size), random_contours(rng, size)
        op = ("intersection", "union", "difference", "xor")[trial % 4]
        rule = ("nonzero", "evenodd")[trial // 4 % 2]
        check(subject, clip, op, rule, vatti_clip(subject, clip, op, rule), rng, size)
