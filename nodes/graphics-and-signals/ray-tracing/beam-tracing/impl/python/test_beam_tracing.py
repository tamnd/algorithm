# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/beam-tracing/. The authors are listed in prov/WFNCHK.jsonl.

import random
from fractions import Fraction as Q

from beam_tracing import Beam, beam_path, cross, dot, reflect_point, sub, trace_beam, trace_ray

APEX = (Q(0), Q(0))
DL, DR = (Q(2), Q(-1)), (Q(2), Q(1))


def segments_meet(p, q, r, s):
    """True if the closed segments pq and rs share a point."""
    d1, d2, d3, d4 = cross(sub(q, p), sub(r, p)), cross(sub(q, p), sub(s, p)), cross(sub(s, r), sub(p, r)), cross(sub(s, r), sub(q, r))
    if ((d1 > 0) != (d2 > 0) or d1 == 0 or d2 == 0) and ((d3 > 0) != (d4 > 0) or d3 == 0 or d4 == 0):
        if d1 == d2 == 0:  # collinear: compare the projections
            m = sub(q, p)
            a = sorted((dot(sub(p, p), m), dot(sub(q, p), m)))
            b = sorted((dot(sub(r, p), m), dot(sub(s, p), m)))
            return a[0] <= b[1] and b[0] <= a[1]
        return True
    return False


def random_scene(rng, k):
    segs = []
    while len(segs) < k:
        p = (Q(rng.randint(10, 100), 10), Q(rng.randint(-60, 60), 10))
        q = (p[0] + Q(rng.randint(-25, 25), 10), p[1] + Q(rng.randint(-25, 25), 10))
        if p == q or q[0] <= Q(1, 2):
            continue
        if any(segments_meet(p, q, a, b) for a, b in segs):
            continue
        segs.append((p, q))
    mirrors = {i for i in range(k) if rng.random() < 0.5}
    return segs, mirrors


def fragment_bounds(beam):
    out = set()
    for _, a, b, _, _ in beam.fragments:
        out.update((a, b))
    for child in beam.children.values():
        out.update(fragment_bounds(child))
    return out


def test_beam_tree_matches_exactly_traced_rays():
    rng = random.Random(71)
    checked = reflected = 0
    for _ in range(12):
        segs, mirrors = random_scene(rng, 10)
        root = trace_beam(Beam(APEX, DL, DR), segs, mirrors, max_depth=3)
        bounds = fragment_bounds(root)
        for _ in range(25):
            s = Q(rng.randint(1, 9972), 9973)
            if s in bounds:
                continue
            d = root.direction(s)
            path = beam_path(root, s)
            assert path == trace_ray(APEX, d, segs, mirrors, 3)
            checked += 1
            reflected += len(path) > 1
    assert checked > 250 and reflected > 40


def test_fragments_are_disjoint_and_lie_on_their_segments():
    rng = random.Random(72)
    for _ in range(15):
        segs, mirrors = random_scene(rng, 8)
        root = trace_beam(Beam(APEX, DL, DR), segs, mirrors, max_depth=2)
        stack = [root]
        while stack:
            beam = stack.pop()
            spans = sorted((a, b) for _, a, b, _, _ in beam.fragments)
            for (a1, b1), (a2, b2) in zip(spans, spans[1:]):
                assert b1 <= a2
            for idx, a, b, pa, pb in beam.fragments:
                p, q = segs[idx]
                for x in (pa, pb):
                    assert cross(sub(q, p), sub(x, p)) == 0
                    assert 0 <= dot(sub(x, p), sub(q, p)) <= dot(sub(q, p), sub(q, p))
            stack.extend(beam.children.values())


def test_reflected_rays_come_from_the_virtual_apex():
    mirror = ((Q(4), Q(-3)), (Q(4), Q(3)))
    root = trace_beam(Beam(APEX, DL, DR), [mirror], {0}, max_depth=1)
    child = root.children[0]
    assert child.apex == (Q(8), Q(0)) == reflect_point(APEX, *mirror)
    for s in (Q(1, 7), Q(1, 2), Q(5, 6)):
        hit = beam_path(root, s)[0][1]
        d = root.direction(s)
        r = sub(d, (2 * d[0], 0))  # mirror x = 4 flips the x component
        v = sub(hit, child.apex)
        assert cross(r, v) == 0 and dot(r, v) > 0


def test_example_scene():
    segs = [((Q(3), Q(-1)), (Q(3), Q(1, 2))), ((Q(5), Q(-3)), (Q(5), Q(3))), ((Q(1), Q(-4)), (Q(1), Q(-6)))]
    root = trace_beam(Beam(APEX, DL, DR), segs, {1}, max_depth=1)
    frags = [(i, a, b, pa, pb) for i, a, b, pa, pb in root.fragments]
    assert frags == [
        (0, Q(1, 6), Q(2, 3), (3, -1), (3, Q(1, 2))),
        (1, Q(0), Q(1, 6), (5, Q(-5, 2)), (5, Q(-5, 3))),
        (1, Q(2, 3), Q(1), (5, Q(5, 6)), (5, Q(5, 2))),
    ]
    assert root.children[1].apex == root.children[2].apex == (Q(10), Q(0))
    lower = [(i, a, b, pa, pb) for i, a, b, pa, pb in root.children[1].fragments]
    assert lower == [(2, Q(2, 3), Q(1), (1, -4), (1, Q(-9, 2)))]
    assert root.children[2].fragments == []
