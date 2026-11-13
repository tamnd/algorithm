# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/attributed-adjacency-graph/. The authors are listed in prov/5037C3.jsonl.

import random
import unittest

from attributed_adjacency_graph import (
    CONCAVE,
    CONVEX,
    TEMPLATES,
    box_cells,
    build_aag,
    match,
    match_brute_force,
    neighbors,
    prism,
    recognize,
    signed_volume6,
    voxel_brep,
)


def block(W=6, D=4, H=3):
    return box_cells(0, W, 0, D, 0, H)


def names(polys):
    return sorted(n for n, _, _ in recognize(polys, TEMPLATES)[2] if n is not None)


def unrecognized(polys):
    return [c for n, c, _ in recognize(polys, TEMPLATES)[2] if n is None]


# --- a brute-force AAG of a union of unit cubes ------------------------------


def brute_aag(cells):
    """Faces by flood fill of the exposed unit squares, labels by counting the cubes around each unit edge."""
    squares = {}  # key: frozenset of corners -> (axis, side, plane, (a, b)) with (a, b) the in-plane cell
    for (i, j, k) in cells:
        for axis in range(3):
            for side in (0, 1):
                nb = [i, j, k]
                nb[axis] += 1 if side else -1
                if tuple(nb) in cells:
                    continue
                c = [i, j, k]
                c[axis] += side
                u, w = (axis + 1) % 3, (axis + 2) % 3
                corners = []
                for du, dw in ((0, 0), (1, 0), (1, 1), (0, 1)):
                    p = list(c)
                    p[u] += du
                    p[w] += dw
                    corners.append(tuple(p))
                squares[frozenset(corners)] = (axis, side, c[axis], (c[u], c[w]))
    by_plane = {}
    for key, (axis, side, plane, ab) in squares.items():
        by_plane.setdefault((axis, side, plane), {})[ab] = key
    face_of = {}
    faces = []
    for plane, grid in by_plane.items():
        for ab, key in grid.items():
            if key in face_of:
                continue
            fid = len(faces)
            faces.append(set())
            stack = [ab]
            face_of[key] = fid
            while stack:
                a, b = stack.pop()
                faces[fid].add(grid[(a, b)])
                for nab in ((a + 1, b), (a - 1, b), (a, b + 1), (a, b - 1)):
                    if nab in grid and grid[nab] not in face_of:
                        face_of[grid[nab]] = fid
                        stack.append(nab)
    edge_faces = {}
    for key in squares:
        pts = sorted(key)
        for p in pts:
            for q in pts:
                if p < q and sum(abs(p[t] - q[t]) for t in range(3)) == 1:
                    edge_faces.setdefault((p, q), []).append(face_of[key])
    arcs = {}
    for (p, q), fs in edge_faces.items():
        if len(fs) != 2:
            return None  # a non-manifold edge
        a, b = fs
        if a == b:
            continue
        axis = next(t for t in range(3) if p[t] != q[t])
        u, w = (axis + 1) % 3, (axis + 2) % 3
        count = 0
        for du in (-1, 0):
            for dw in (-1, 0):
                c = list(p)
                c[u] += du
                c[w] += dw
                count += tuple(c) in cells
        if count == 2:
            return None
        lab = CONVEX if count == 1 else CONCAVE
        key = (min(a, b), max(a, b))
        arcs[key] = arcs.get(key, frozenset()) | {lab}
    return [frozenset(f) for f in faces], arcs


def canonical(polys, faces, arcs):
    """Faces as sets of square corner sets, so that two AAGs of the same cubes can be compared."""
    names_ = [frozenset(frozenset(polys[k]) for k in f) for f in faces]
    return set(names_), {frozenset((names_[a], names_[b])): lab for (a, b), lab in arcs.items()}


def brute_recognize(cells):
    faces, arcs = brute_aag(cells)
    adj = neighbors(len(faces), arcs)
    kept = {v for v in range(len(faces)) if any(lab != frozenset({CONVEX}) for lab in adj[v].values())}
    sub = [{w: lab for w, lab in adj[v].items() if w in kept} if v in kept else {} for v in range(len(faces))]
    out, seen = [], set()
    for v in sorted(kept):
        if v in seen:
            continue
        comp, stack = {v}, [v]
        while stack:
            for w in sub[stack.pop()]:
                if w not in comp:
                    comp.add(w)
                    stack.append(w)
        seen |= comp
        name = next((t["name"] for t in TEMPLATES if match_brute_force(t, comp, sub) is not None), None)
        out.append((name, frozenset(faces[x] for x in comp)))
    return out


class TestSingleFeatures(unittest.TestCase):
    def test_each_template_is_recognized(self):
        B = block()
        cases = {
            "step": B - box_cells(5, 6, 0, 4, 2, 3),
            "through slot": B - box_cells(2, 4, 0, 4, 2, 3),
            "blind slot": B - box_cells(2, 4, 0, 3, 2, 3),
            "blind step": B - box_cells(0, 2, 0, 2, 2, 3),
            "pocket": B - box_cells(2, 4, 1, 3, 1, 3),
            "through hole": B - box_cells(2, 3, 1, 2, 0, 3),
        }
        for name, cells in cases.items():
            polys = voxel_brep(cells)
            self.assertGreater(signed_volume6(polys), 0)
            self.assertEqual(names(polys), [name], name)
            self.assertEqual(unrecognized(polys), [], name)

    def test_plain_block_has_no_feature(self):
        faces, arcs, res = recognize(voxel_brep(block()), TEMPLATES)
        self.assertEqual(len(faces), 6)
        self.assertEqual(len(arcs), 12)
        self.assertTrue(all(lab == frozenset({CONVEX}) for lab in arcs.values()))
        self.assertEqual(res, [])

    def test_example_part(self):
        cells = block(10, 4, 3) - box_cells(3, 5, 0, 4, 2, 3) - box_cells(9, 10, 0, 4, 2, 3) - box_cells(6, 8, 1, 3, 1, 3)
        faces, arcs, res = recognize(voxel_brep(cells), TEMPLATES)
        self.assertEqual(len(faces), 17)
        self.assertEqual(sum(lab == frozenset({CONCAVE}) for lab in arcs.values()), 11)
        self.assertEqual(sorted(n for n, _, _ in res), ["pocket", "step", "through slot"])


class TestAgainstBruteForce(unittest.TestCase):
    def test_aag_of_random_parts(self):
        rng = random.Random(7)
        checked = rejected = 0
        for _ in range(120):
            W, D, H = rng.randint(3, 7), rng.randint(3, 6), rng.randint(2, 4)
            cells = block(W, D, H)
            for _ in range(rng.randint(1, 3)):
                x0, y0 = rng.randint(0, W - 1), rng.randint(0, D - 1)
                x1, y1 = rng.randint(x0 + 1, W), rng.randint(y0 + 1, D)
                cells -= box_cells(x0, x1, y0, y1, rng.randint(0, H - 1), H)
            if not cells:
                continue
            polys = voxel_brep(cells)
            ref = brute_aag(cells)
            if ref is None:
                with self.assertRaises(ValueError):
                    build_aag(polys)
                rejected += 1
                continue
            faces, arcs = build_aag(polys)
            # build_aag returns polygon indices; the brute force returns corner sets.
            got = canonical(polys, faces, arcs)
            want = ({frozenset(f) for f in ref[0]}, {frozenset((ref[0][a], ref[0][b])): lab for (a, b), lab in ref[1].items()})
            self.assertEqual(got, want)
            checked += 1
            mine = {(n, frozenset(frozenset(frozenset(polys[k]) for k in faces[x]) for x in c)) for n, c, _ in recognize(polys, TEMPLATES)[2]}
            theirs = set(brute_recognize(cells))
            self.assertEqual(mine, theirs)
        self.assertGreater(checked, 60)
        self.assertGreater(rejected, 0)

    def test_backtracking_matches_brute_force(self):
        rng = random.Random(11)
        labels = [frozenset({CONVEX}), frozenset({CONCAVE}), frozenset({CONVEX, CONCAVE})]
        for _ in range(400):
            k = rng.randint(1, 6)
            arcs = {}
            for a in range(k):
                for b in range(a + 1, k):
                    if rng.random() < 0.5:
                        arcs[(a, b)] = rng.choice(labels[:2] if rng.random() < 0.9 else labels)
            # a host graph that is either a relabeling of the template or a random graph of the same size
            nodes = list(range(10, 10 + k))
            if rng.random() < 0.5:
                perm = nodes[:]
                rng.shuffle(perm)
                host = {(min(perm[a], perm[b]), max(perm[a], perm[b])): lab for (a, b), lab in arcs.items()}
            else:
                host = {}
                for a in nodes:
                    for b in nodes:
                        if a < b and rng.random() < 0.5:
                            host[(a, b)] = rng.choice(labels[:2])
            adj = neighbors(10 + k, host)
            t = {"name": "t", "nodes": k, "arcs": arcs}
            m1, m2 = match(t, set(nodes), adj), match_brute_force(t, set(nodes), adj)
            self.assertEqual(m1 is None, m2 is None)
            if m1 is not None:
                for a in range(k):
                    for b in range(a + 1, k):
                        self.assertEqual(arcs.get((a, b)), adj[m1[a]].get(m1[b]))


class TestDegenerateInputs(unittest.TestCase):
    def test_crossing_slots_are_not_recognized(self):
        cells = block() - box_cells(2, 4, 0, 4, 2, 3) - box_cells(0, 6, 1, 3, 2, 3)
        res = recognize(voxel_brep(cells), TEMPLATES)[2]
        self.assertEqual(len(res), 1)
        self.assertIsNone(res[0][0])
        self.assertEqual(len(res[0][1]), 9)
        # A square hole drilled down from the floor of a slot joins the slot in one component.
        cells = block() - box_cells(1, 5, 0, 4, 2, 3) - box_cells(2, 4, 1, 3, 0, 2)
        res = recognize(voxel_brep(cells), TEMPLATES)[2]
        self.assertEqual([(n, len(c)) for n, c, _ in res], [(None, 7)])

    def test_v_groove_looks_like_a_step(self):
        groove = prism([(0, 0), (6, 0), (6, 3), (4, 3), (3, 1), (2, 3), (0, 3)], 4)
        self.assertGreater(signed_volume6(groove), 0)
        self.assertEqual(names(groove), ["step"])

    def test_split_faces_are_merged(self):
        plain = prism([(0, 0), (6, 0), (6, 3), (0, 3)], 4)
        split = prism([(0, 0), (2, 0), (6, 0), (6, 3), (0, 3)], 4)
        self.assertEqual(len(build_aag(plain)[0]), 6)
        self.assertEqual(len(build_aag(split)[0]), 6)

    def test_inside_out_swaps_the_labels(self):
        polys = voxel_brep(block() - box_cells(2, 4, 0, 4, 2, 3))
        rev = [list(reversed(P)) for P in polys]
        faces, arcs = canonical(polys, *build_aag(polys))
        faces2, flipped = canonical(rev, *build_aag(rev))
        swap = {CONVEX: CONCAVE, CONCAVE: CONVEX}
        self.assertEqual(faces, faces2)
        self.assertEqual(flipped, {e: frozenset(swap[x] for x in lab) for e, lab in arcs.items()})

    def test_bad_meshes_are_rejected(self):
        two = voxel_brep({(0, 0, 0), (1, 1, 0)})  # two cubes that share only an edge
        with self.assertRaises(ValueError):
            build_aag(two)
        with self.assertRaises(ValueError):
            build_aag(voxel_brep(block())[1:])  # an open mesh


if __name__ == "__main__":
    unittest.main()
