# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generic-naming-scheme/. The authors are listed in prov/5S5Z62.jsonl.

import random
import unittest
from itertools import permutations

from generic_naming_scheme import Part, name_edges, name_vertices, resolve_edge, resolve_vertex


def isomorphism_images(p1: Part, p2: Part):
    """Brute force: every map of the cycles of p1 onto the cycles of p2, with
    a rotation of each cycle, that preserves all labels. Returns, for each
    edge of p1, the set of its images, or None if there is no such map."""
    if len(p1.cycles) != len(p2.cycles):
        return None
    images = {e: set() for e in p1.edges}
    found = False
    for perm in permutations(range(len(p2.cycles))):
        rots = []
        for c1, c2 in enumerate(perm):
            a, b = p1.cycles[c1], p2.cycles[c2]
            if len(a) != len(b):
                break
            ok = [s for s in range(len(b)) if all(b[(i + s) % len(b)] == a[i] for i in range(len(a)))]
            if not ok:
                break
            rots.append(ok)
        else:
            found = True
            for c1, c2 in enumerate(perm):
                L = len(p1.cycles[c1])
                for i in range(L):
                    for s in rots[c1]:
                        images[(c1, i)].add((c2, (i + s) % L))
    return images if found else None


def distinct(base, ops):
    """Only the same side of copies in one pattern may share a coordinate."""
    owners = {}
    for k, op in enumerate([[base]] + list(ops)):
        for r in op:
            for axis, v, side in (("x", r[0], 0), ("x", r[2], 1), ("y", r[1], 0), ("y", r[3], 1)):
                if owners.setdefault((axis, v), (k, side)) != (k, side):
                    return False
    return True


def perturb(rng, base, ops):
    """A parameter change: every coordinate value moves by at most 3, so
    the topology may or may not change."""
    rects = [base] + [r for op in ops for r in op]
    vals = {v for r in rects for v in r}
    while True:
        m = {v: v + rng.randint(-3, 3) for v in vals}
        nb = (m[base[0]], m[base[1]], m[base[2]], m[base[3]])
        nops = [[(m[a], m[b], m[c], m[d]) for a, b, c, d in op] for op in ops]
        if all(r[0] < r[2] and r[1] < r[3] for r in [nb] + [r for op in nops for r in op]) \
                and distinct(nb, nops):
            return nb, nops


def random_history(rng, nops, shape=None):
    """A base rectangle and nops cut operations; each is one rectangle or a
    pattern of 2 or 3 copies shifted along x or y. With shape given, the
    same number of copies per operation is kept."""
    while True:
        W, H = rng.randint(12, 30), rng.randint(8, 20)
        base = (0, 0, W, H)
        ops = []
        for k in range(nops):
            copies = shape[k] if shape else rng.choice([1, 1, 2, 3])
            w, h = rng.randint(1, 8), rng.randint(1, 8)
            if rng.random() < 0.3:      # a through cut, across the whole part
                if rng.random() < 0.5:
                    h = H + 2 * rng.randint(1, 3) + 1
                else:
                    w = W + 2 * rng.randint(1, 3) + 1
            x0, y0 = rng.randint(-4, W - 1), rng.randint(-4, H - 1)
            if h > H:
                y0 = -rng.randint(1, h - H - 1)
            if w > W:
                x0 = -rng.randint(1, w - W - 1)
            dx, dy = (rng.randint(w + 1, w + 6), 0) if rng.random() < 0.5 else (0, rng.randint(h + 1, h + 6))
            if w > W:
                dx, dy = 0, rng.randint(h + 1, h + 6)
            if h > H:
                dx, dy = rng.randint(w + 1, w + 6), 0
            ops.append([(x0 + i * dx, y0 + i * dy, x0 + i * dx + w, y0 + i * dy + h) for i in range(copies)])
        if distinct(base, ops):
            return base, ops


def remap(rng, base, ops):
    """A parameter change that keeps the order of all x and all y values."""
    rects = [base] + [r for op in ops for r in op]
    xv = sorted({r[0] for r in rects} | {r[2] for r in rects})
    yv = sorted({r[1] for r in rects} | {r[3] for r in rects})
    nx = dict(zip(xv, sorted(rng.sample(range(-60, 160), len(xv)))))
    ny = dict(zip(yv, sorted(rng.sample(range(-60, 160), len(yv)))))
    new = [[(nx[a], ny[b], nx[c], ny[d]) for a, b, c, d in op] for op in [[base]] + list(ops)]
    return new[0][0], new[1:]


def cell_area(p: Part) -> int:
    return sum((p.xs[i + 1] - p.xs[i]) * (p.ys[j + 1] - p.ys[j]) for i, j in p.cells)


class TestHandCases(unittest.TestCase):
    def test_slot_splits_the_top(self):
        p = Part((0, 0, 10, 6), [(4, 3, 6, 8)])
        self.assertEqual(len(p.cycles), 1)
        self.assertEqual(len(p.cycles[0]), 8)
        tops = [e for e in p.edges if p.label(e) == ("base", "top")]
        self.assertEqual(len(tops), 2)
        names = name_edges(p)
        self.assertEqual(sorted(names[e][0] for e in tops), [1, 1])
        self.assertEqual(max(n[0] for n in names.values()), 1)
        # resize everything: the names still find the same pieces
        q = Part((0, 0, 20, 9), [(5, 4, 12, 15)])
        for e in tops:
            (f,) = resolve_edge(names[e], q)
            self.assertEqual(p.edge_geom[e[0]][e[1]], q.edge_geom[f[0]][f[1]])  # same grid position
        # make the cut a pocket: the top is whole again, and the split names fail
        r = Part((0, 0, 10, 6), [(4, 3, 6, 5)])
        self.assertEqual(len(r.cycles), 2)
        for e in tops:
            self.assertEqual(resolve_edge(names[e], r), set())
        self.assertEqual(len(resolve_edge((0, r.window(tops[0], 0)), r)), 1)

    def test_cut_through_splits_the_part(self):
        p = Part((0, 0, 10, 6), [(4, -1, 6, 8)])
        self.assertEqual(sorted(len(c) for c in p.cycles), [4, 4])
        names = name_edges(p)
        self.assertTrue(all(len(resolve_edge(n, p)) == 1 for n in names.values()))

    def test_pattern_gives_symmetric_pieces(self):
        # three through slots of one pattern: the two middle pieces have the
        # same labels all round, so their edges cannot be told apart
        ops = [[(4, -1, 5, 11), (9, -1, 10, 11), (14, -1, 15, 11)]]
        p = Part((0, 0, 20, 10), ops)
        self.assertEqual(sorted(len(c) for c in p.cycles), [4, 4, 4, 4])
        names = name_edges(p)
        counts = sorted(len(resolve_edge(n, p)) for n in names.values())
        self.assertEqual(counts, [1] * 8 + [2] * 8)
        self.assertTrue(all(n[0] == 4 for n in names.values() if len(resolve_edge(n, p)) == 2))
        q = Part((0, 0, 30, 12), [[(3, -2, 9, 13), (11, -2, 12, 13), (20, -2, 26, 13)]])
        images = isomorphism_images(p, q)
        for e, n in names.items():
            self.assertEqual(resolve_edge(n, q), images[e])


class TestAgainstBruteForce(unittest.TestCase):
    def test_model_is_consistent(self):
        rng = random.Random(1)
        for _ in range(150):
            base, cuts = random_history(rng, rng.randint(0, 3))
            p = Part(base, cuts)
            self.assertEqual(p.area(), cell_area(p))
            for c in p.cycles:
                for i in range(len(c)):
                    self.assertNotEqual(c[i], c[i - 1])  # each edge is maximal

    def test_names_survive_order_preserving_changes(self):
        rng = random.Random(2)
        checked = 0
        for _ in range(150):
            base, cuts = random_history(rng, rng.randint(0, 3))
            p = Part(base, cuts)
            q = Part(*remap(rng, base, cuts))
            images = isomorphism_images(p, q)
            self.assertIsNotNone(images)
            en = name_edges(p)
            for e, n in en.items():
                got = resolve_edge(n, q)
                self.assertEqual(got, images[e])
                self.assertIn(e, got)                 # the same grid edge
                if len(resolve_edge(n, p)) == 1:
                    self.assertEqual(got, {e})
                checked += 1
            for v, n in name_vertices(p, en).items():
                # an isomorphism maps the vertex after edge a to the vertex after its image
                want = {(x, (x[0], (x[1] + 1) % len(q.cycles[x[0]]))) for x in images[v[0]]}
                self.assertEqual(resolve_vertex(n, q), want)
                checked += 1
        self.assertGreater(checked, 500)

    def test_names_against_isomorphisms_after_any_change(self):
        """Every coordinate moves by up to 3, which may change the order of
        the coordinates and the topology. When the labelled boundaries are
        isomorphic, resolution returns exactly the images under all
        isomorphisms. Otherwise nothing is claimed; the test only counts
        these cases, to show that the edits do change the topology."""
        rng = random.Random(3)
        checked = iso = changed = 0
        for _ in range(250):
            ncuts = rng.randint(1, 3)
            base, cuts = random_history(rng, ncuts)
            p = Part(base, cuts)
            q = Part(*perturb(rng, base, cuts))
            images = isomorphism_images(p, q)
            if images is None:
                changed += 1
                continue
            iso += 1
            en = name_edges(p)
            for e, n in en.items():
                self.assertEqual(resolve_edge(n, q), images[e])
                checked += 1
        self.assertGreater(iso, 50)
        self.assertGreater(changed, 10)
        self.assertGreater(checked, 500)


if __name__ == "__main__":
    unittest.main()
