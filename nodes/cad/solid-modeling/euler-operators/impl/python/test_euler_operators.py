# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/euler-operators/. The authors are listed in prov/23HY3M.jsonl.

import random
import unittest
from fractions import Fraction

from euler_operators import EulerError, Model, is_lone, twin, walk

# change in (V, E, F, L, S, H) of each operator
TABLE = {
    "mvsf": (1, 0, 1, 1, 1, 0),
    "kvsf": (-1, 0, -1, -1, -1, 0),
    "mev": (1, 1, 0, 0, 0, 0),
    "kev": (-1, -1, 0, 0, 0, 0),
    "mef": (0, 1, 1, 1, 0, 0),
    "kef": (0, -1, -1, -1, 0, 0),
    "kemr": (0, -1, 0, 1, 0, 0),
    "mekr": (0, 1, 0, -1, 0, 0),
    "kfmrh": ((0, 0, -1, 0, 0, 1), (0, 0, -1, 0, -1, 0)),
    "mfkrh": ((0, 0, 1, 0, 0, -1), (0, 0, 1, 0, 1, 0)),
}
KEYS = ("V", "E", "F", "L", "S", "H")


def euler_poincare(c):
    return c["V"] - c["E"] + c["F"] - (c["L"] - c["F"]) - 2 * (c["S"] - c["H"])


def recount(m):
    """Count by a scan of the loops, with shells by union-find (the brute force)."""
    loops = []  # (face index, list of (vertex id, edge or None))
    faces = list(m.faces)
    index = {f: i for i, f in enumerate(faces)}
    for f in faces:
        for loop in f.loops():
            seq = []
            h = loop.he
            while True:
                seq.append((h.vertex.id, h.edge))
                h = h.next
                if h is loop.he:
                    break
            loops.append((index[f], seq))
    parent = list(range(len(faces)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    edge_faces = {}
    for fi, seq in loops:
        for _, e in seq:
            if e is not None:
                edge_faces.setdefault(e, []).append(fi)
    for fs in edge_faces.values():
        assert len(fs) == 2
        parent[find(fs[0])] = find(fs[1])
    roots = {find(i) for i in range(len(faces))}
    per = {r: [set(), set(), 0, 0] for r in roots}  # vertices, edges, faces, loops
    for fi, seq in loops:
        p = per[find(fi)]
        p[3] += 1
        for vid, e in seq:
            p[0].add(vid)
            if e is not None:
                p[1].add(e)
    for i in range(len(faces)):
        per[find(i)][2] += 1
    genus = 0
    for vs, es, nf, nl in per.values():
        chi = len(vs) - len(es) + nf - (nl - nf)
        assert chi <= 2 and chi % 2 == 0, chi
        genus += (2 - chi) // 2
    return {
        "V": len({vid for _, seq in loops for vid, _ in seq}),
        "E": len(edge_faces),
        "F": len(faces),
        "L": len(loops),
        "S": len(roots),
        "H": genus,
    }


def signature(m):
    """The faces as sorted lists of loops, each loop its least rotation of
    (vertex id, lone) pairs. Outer loops and rings are not told apart."""

    def loop_sig(loop):
        seq = []
        h = loop.he
        while True:
            seq.append((h.vertex.id, is_lone(h)))
            h = h.next
            if h is loop.he:
                break
        return min(tuple(seq[i:] + seq[:i]) for i in range(len(seq)))

    return tuple(sorted(tuple(sorted(loop_sig(lp) for lp in f.loops())) for f in m.faces))


def delta(before, after):
    return tuple(after[k] - before[k] for k in KEYS)


class Tracker:
    """Apply operators, and after each one check the structure, the brute-force
    counts, the change table and the Euler-Poincare formula."""

    def __init__(self, test, m):
        self.t = test
        self.m = m
        self.c = m.check()

    def do(self, name, *args, **kw):
        res = getattr(self.m, name)(*args, **kw)
        c = self.m.check()
        self.t.assertEqual(c, recount(self.m))
        d = delta(self.c, c)
        want = TABLE[name]
        if isinstance(want[0], tuple):
            self.t.assertIn(d, want)
        else:
            self.t.assertEqual(d, want)
        self.t.assertEqual(euler_poincare(c), 0)
        self.c = c
        return res


def he(m, f, u, w=None):
    """The half-edge of face f that starts at vertex u (and ends at w)."""
    found = []
    for loop in f.loops():
        h = loop.he
        while True:
            if h.vertex.id == u and (w is None or (not is_lone(h) and h.next.vertex.id == w)):
                found.append(h)
            h = h.next
            if h is loop.he:
                break
    assert len(found) == 1, (u, w, len(found))
    return found[0]


def face_with(m, u, w):
    """The face that has the half-edge from u to w."""
    out = [f for f in m.faces for lp in f.loops() for h in walk(lp.he) if h.vertex.id == u and h.next.vertex.id == w]
    assert len(out) == 1
    return out[0]


def build_box(tr, lo, hi, inward=False):
    """A box by mvsf, 3 mev, mef, 4 mev, 4 mef. Returns the vertex ids
    (bottom 0..3, top 4..7) and the undo list. With inward, x and y are swapped
    in every point, a reflection, so the box is oriented inward."""
    m = tr.m
    (x0, y0, z0), (x1, y1, z1) = lo, hi
    pts = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    if inward:
        pts = [(p[1], p[0], p[2]) for p in pts]
    undo = []
    f = tr.do("mvsf", pts[0])
    v = [f.outer.he.vertex.id]
    undo.append(("kvsf", f))
    h = f.outer.he
    for i in (1, 2, 3):
        a = tr.do("mev", h, pts[i])
        v.append(a.next.vertex.id)
        undo.append(("kev", a))
        h = twin(a)  # starts at the new vertex
    a = tr.do("mef", he(m, f, v[3]), he(m, f, v[0]))  # closes the bottom
    undo.append(("kef", a))
    top = a.loop.face
    for i in range(4):
        a = tr.do("mev", he(m, top, v[i], v[(i + 1) % 4]), pts[4 + i])
        v.append(a.next.vertex.id)
        undo.append(("kev", a))
    for i in range(4):
        h1 = he(m, top, v[4 + i], v[i])
        nxt = 4 + (i + 1) % 4
        h2 = he(m, top, v[nxt], v[(i + 1) % 4]) if i < 3 else he(m, top, v[4], v[5])
        a = tr.do("mef", h1, h2)
        undo.append(("kef", a))
    return v, pts, undo


def undo_all(tr, undo):
    """Apply the inverses in reverse order. An argument that is a list of one
    item is read when it is used, and an entry with a third item stores its
    result there (kemr deletes an edge, so its inverse makes a new one)."""
    for entry in reversed(undo):
        name, arg = entry[0], entry[1]
        args = arg if isinstance(arg, tuple) else (arg,)
        args = tuple(x[0] if isinstance(x, list) else x for x in args)
        res = tr.do(name, *args)
        if len(entry) == 3:
            entry[2][0] = res


def loops_xyz(m):
    """Each face as a list of loops of points."""
    out = []
    for f in m.faces:
        out.append([[h.vertex.point for h in walk(lp.he)] for lp in f.loops()])
    return out


def volume(m):
    """The signed volume by the divergence theorem, exact (Newell normals)."""
    total = Fraction(0)
    for loops in loops_xyz(m):
        q = loops[0][0]
        for pts in loops:
            n = [0, 0, 0]
            for i in range(len(pts)):
                a, b = pts[i], pts[(i + 1) % len(pts)]
                n[0] += a[1] * b[2] - a[2] * b[1]
                n[1] += a[2] * b[0] - a[0] * b[2]
                n[2] += a[0] * b[1] - a[1] * b[0]
            total += q[0] * n[0] + q[1] * n[1] + q[2] * n[2]
    return total / 6


def planar(m):
    for loops in loops_xyz(m):
        pts = loops[0]
        n = [0, 0, 0]
        for i in range(len(pts)):
            a, b = pts[i], pts[(i + 1) % len(pts)]
            n[0] += a[1] * b[2] - a[2] * b[1]
            n[1] += a[2] * b[0] - a[0] * b[2]
            n[2] += a[0] * b[1] - a[1] * b[0]
        q = pts[0]
        for lp in loops:
            for p in lp:
                if sum(n[k] * (p[k] - q[k]) for k in range(3)) != 0:
                    return False
    return True


def build_frame(tr):
    """The square frame [0,3]^2 x [0,1] with the hole (1,2)^2 x [0,1]."""
    m = tr.m
    v, pts, undo = build_box(tr, (0, 0, 0), (3, 3, 1))
    top = face_with(m, v[4], v[5])
    bottom = face_with(m, v[3], v[2])
    a = tr.do("mev", he(m, top, v[4], v[5]), (1, 1, 1))  # the bridge
    bridge = a
    bridge_ref = [a]
    undo.append(("kev", bridge_ref))
    w = [a.next.vertex.id]
    h = twin(a)
    for p in ((2, 1, 1), (2, 2, 1), (1, 2, 1)):
        a = tr.do("mev", h, p)
        undo.append(("kev", a))
        w.append(a.next.vertex.id)
        h = twin(a)
    a = tr.do("mef", he(m, top, w[0], w[1]), he(m, top, w[3]))  # the inner square face
    undo.append(("kef", a))
    inner = twin(a).loop.face
    h1, h2 = tr.do("kemr", bridge)  # the ring of the top face
    undo.append(("mekr", (h1, h2), bridge_ref))
    low = []
    for i, p in enumerate(((1, 1, 0), (2, 1, 0), (2, 2, 0), (1, 2, 0))):
        a = tr.do("mev", he(m, inner, w[i], w[(i + 1) % 4]), p)
        undo.append(("kev", a))
        low.append(a.next.vertex.id)
    for i in range(4):
        h1 = he(m, inner, low[i], w[i])
        h2 = he(m, inner, low[(i + 1) % 4], w[(i + 1) % 4]) if i < 3 else he(m, inner, low[0], low[1])
        a = tr.do("mef", h1, h2)
        undo.append(("kef", a))
    ring = tr.do("kfmrh", bottom, inner)  # the hole
    undo.append(("mfkrh", ring))
    return undo


class EulerOperatorTests(unittest.TestCase):
    def test_cube(self):
        tr = Tracker(self, Model())
        v, pts, undo = build_box(tr, (0, 0, 0), (1, 1, 1))
        self.assertEqual(tr.c, {"V": 8, "E": 12, "F": 6, "L": 6, "S": 1, "H": 0})
        self.assertEqual(volume(tr.m), 1)
        self.assertTrue(planar(tr.m))
        got = sorted(sorted(lp[0]) for lp in loops_xyz(tr.m))
        want = []
        for axis in range(3):
            for c in (0, 1):
                want.append(sorted(p for p in pts if p[axis] == c))
        self.assertEqual(got, sorted(want))
        undo_all(tr, undo)
        self.assertEqual(tr.c, {k: 0 for k in KEYS})

    def test_cube_with_through_hole(self):
        tr = Tracker(self, Model())
        undo = build_frame(tr)
        self.assertEqual(tr.c, {"V": 16, "E": 24, "F": 10, "L": 12, "S": 1, "H": 1})
        self.assertEqual(volume(tr.m), 8)
        self.assertTrue(planar(tr.m))
        rings = [f for f in tr.m.faces if f.rings]
        self.assertEqual(len(rings), 2)
        undo_all(tr, undo)
        self.assertEqual(tr.c, {k: 0 for k in KEYS})

    def test_cavity(self):
        tr = Tracker(self, Model())
        build_box(tr, (0, 0, 0), (3, 3, 3))
        build_box(tr, (1, 1, 1), (2, 2, 2), inward=True)
        self.assertEqual(tr.c, {"V": 16, "E": 24, "F": 12, "L": 12, "S": 2, "H": 0})
        self.assertEqual(volume(tr.m), 26)

    def test_one_vertex_cases(self):
        tr = Tracker(self, Model())
        f = tr.do("mvsf")
        a = tr.do("mef", f.outer.he, f.outer.he)  # a sphere cut by one closed edge
        self.assertEqual(tr.c, {"V": 1, "E": 1, "F": 2, "L": 2, "S": 1, "H": 0})
        tr.do("kef", a)
        g = tr.do("mvsf")
        ring = tr.do("kfmrh", f, g)  # a vertex moved into a face of another shell
        self.assertEqual(tr.c, {"V": 2, "E": 0, "F": 1, "L": 2, "S": 1, "H": 0})
        tr.do("mfkrh", ring)
        self.assertEqual(tr.c["S"], 2)

    def test_preconditions(self):
        m = Model()
        tr = Tracker(self, m)
        undo = build_frame(tr)
        before = signature(m)
        top_ring = next(f for f in m.faces if f.rings)
        cube_edge = next(iter(m.edges)).he1
        with self.assertRaises(EulerError):
            m.kev(cube_edge)  # both ends have degree 3
        with self.assertRaises(EulerError):
            m.kemr(cube_edge)  # two different loops
        with self.assertRaises(EulerError):
            m.mekr(top_ring.outer.he, top_ring.outer.he.next)  # one loop
        with self.assertRaises(EulerError):
            m.mfkrh(top_ring.outer)  # not a ring
        with self.assertRaises(EulerError):
            m.kfmrh(next(f for f in m.faces if not f.rings), top_ring)  # f2 has a ring
        with self.assertRaises(EulerError):
            m.kvsf(top_ring)
        with self.assertRaises(EulerError):
            m.mef(top_ring.outer.he, top_ring.rings[0].he)  # two loops
        self.assertEqual(signature(m), before)
        undo_all(tr, undo)

    def test_random_sequences(self):
        rng = random.Random(20261114)
        seen = {"H": 0, "S": 0}
        used = set()
        rounds = 0
        for run in range(40):
            m = Model()
            tr = Tracker(self, m)
            for step in range(250):
                name, args = self.pick(rng, m)
                used.add(name)
                before = signature(m)
                pre = self.context(name, args)
                res = tr.do(name, *args)
                seen["H"] = max(seen["H"], tr.c["H"])
                seen["S"] = max(seen["S"], tr.c["S"])
                if rng.random() < 0.4:
                    inv = self.inverse(name, res, pre)
                    if inv is not None:
                        tr.do(*inv)
                        self.assertEqual(signature(m), before)
                        rounds += 1
        self.assertEqual(used, set(TABLE))
        self.assertGreaterEqual(seen["H"], 2)
        self.assertGreaterEqual(seen["S"], 3)
        self.assertGreater(rounds, 3000)

    @staticmethod
    def context(name, args):
        """What the inverse needs to know from before the operator."""
        if name == "kev":
            w = twin(args[0]).vertex
            return (w.point, w.id)
        if name == "kef":
            a = args[0]
            b = twin(a)
            # mef puts no rings in the new face, and with h1 = h2 its new face is (b)
            return not b.loop.face.rings and not (a.next is a and b.next is not b)
        if name == "mfkrh":
            return args[0].face
        return None

    @staticmethod
    def inverse(name, res, pre):
        if name == "mvsf":
            return ("kvsf", res)
        if name == "kvsf":
            return ("mvsf", res.point, res.id)
        if name == "mev":
            return ("kev", res)
        if name == "kev":
            return ("mev", res, pre[0], pre[1])
        if name == "mef":
            return ("kef", res)
        if name == "kef":
            return ("mef", *res) if pre else None
        if name == "kemr":
            return ("mekr", *res)
        if name == "mekr":
            return ("kemr", res)
        if name == "kfmrh":
            return ("mfkrh", res)
        if name == "mfkrh":
            return ("kfmrh", pre, res)
        return None

    @staticmethod
    def pick(rng, m):
        hes = [h for lp in m.loops for h in ([lp.he] if is_lone(lp.he) else walk(lp.he))]
        real = [h for h in hes if not is_lone(h)]
        size = len(hes)
        options = []
        options.append(("mvsf", ()))
        if hes and size < 60:
            options.append(("mev", (rng.choice(hes),)))
            lp = rng.choice(list(m.loops))
            hs = [lp.he] if is_lone(lp.he) else walk(lp.he)
            options.append(("mef", (rng.choice(hs), rng.choice(hs))))
        kev = [h for h in real if h.next is twin(h)]
        if kev:
            options.append(("kev", (rng.choice(kev),)))
        kef = [h for h in real if h.loop.face is not twin(h).loop.face]
        if kef:
            options.append(("kef", (rng.choice(kef),)))
        kemr = [h for h in real if h.loop is twin(h).loop]
        if kemr:
            options.append(("kemr", (rng.choice(kemr),)))
        multi = [f for f in m.faces if f.rings]
        if multi:
            f = rng.choice(multi)
            l1, l2 = rng.sample(f.loops(), 2)
            h1 = l1.he if is_lone(l1.he) else rng.choice(walk(l1.he))
            h2 = l2.he if is_lone(l2.he) else rng.choice(walk(l2.he))
            options.append(("mekr", (h1, h2)))
            options.append(("mfkrh", (rng.choice(f.rings),)))
        singles = [f for f in m.faces if not f.rings]
        if len(m.faces) >= 2 and singles:
            f2 = rng.choice(singles)
            f1 = rng.choice([f for f in m.faces if f is not f2])
            options.append(("kfmrh", (f1, f2)))
        lone = [f for f in m.faces if not f.rings and is_lone(f.outer.he)]
        if lone:
            options.append(("kvsf", (rng.choice(lone),)))
        if size >= 60:
            options = [o for o in options if o[0] not in ("mvsf",)] or options
        return rng.choice(options)


if __name__ == "__main__":
    unittest.main()
