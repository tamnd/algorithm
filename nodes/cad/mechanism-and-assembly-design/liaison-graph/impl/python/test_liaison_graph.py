# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/liaison-graph/. The authors are listed in prov/RHWBG9.jsonl.

import random
from fractions import Fraction

from assembly_boxes import face_contact, random_boxes, is_valid_assembly
from liaison_graph import LiaisonGraph, build

# ---- independent references ----


def all_pairs(boxes):
    """The pairwise test on every pair, with no sweep."""
    out = {}
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            c = face_contact(boxes[i], boxes[j])
            if c is not None:
                out[(i, j)] = ("contact",) + c
    return out


def voxel_faces(boxes, size):
    """Count unit faces between different boxes on a voxel grid."""
    owner = {}
    for idx, b in enumerate(boxes):
        for x in range(b[0], b[3]):
            for y in range(b[1], b[4]):
                for z in range(b[2], b[5]):
                    owner[(x, y, z)] = idx
    out = {}
    for (x, y, z), a in owner.items():
        for k in range(3):
            q = [x, y, z]
            q[k] += 1
            b = owner.get(tuple(q))
            if b is None or b == a:
                continue
            i, j, s = (a, b, 1) if a < b else (b, a, -1)
            key = (i, j)
            prev = out.get(key, ("contact", k, s, 0))
            assert prev[1] == k and prev[2] == s
            out[key] = ("contact", k, s, prev[3] + 1)
    return out


def connected_by_bfs(n, pairs, mask):
    parts = [i for i in range(n) if mask >> i & 1]
    if not parts:
        return False
    seen = {parts[0]}
    stack = [parts[0]]
    while stack:
        u = stack.pop()
        for (i, j) in pairs:
            for a, b in ((i, j), (j, i)):
                if a == u and mask >> b & 1 and b not in seen:
                    seen.add(b)
                    stack.append(b)
    return len(seen) == len(parts)


EXAMPLE = [
    (0, 0, 0, 4, 2, 1),   # 0 base plate
    (0, 0, 1, 1, 2, 3),   # 1 left post
    (3, 0, 1, 4, 2, 3),   # 2 right post
    (1, 0, 1, 3, 2, 2),   # 3 block
    (0, 0, 3, 4, 2, 4),   # 4 top plate
]

# ---- tests ----


def test_example():
    g = build(EXAMPLE)
    assert g.liaisons() == [(0, 1), (0, 2), (0, 3), (1, 3), (1, 4), (2, 3), (2, 4)]
    assert g.label[(0, 3)] == ("contact", 2, 1, 4)
    assert g.label[(1, 3)] == ("contact", 0, 1, 2)
    assert g.neighbours(3) == [0, 1, 2]
    assert g.cut(0b01000) == [(0, 3), (1, 3), (2, 3)]
    assert g.is_connected(0b11110)
    assert not g.is_connected(0b11000)
    assert len(g.connected_subsets()) == 27
    assert g.label[(2, 3)] == ("contact", 0, -1, 2)


def test_sweep_matches_all_pairs():
    rng = random.Random(1)
    for trial in range(300):
        n = rng.randint(1, 30)
        boxes = random_boxes(rng, n, size=8, max_side=3, connected=trial % 2 == 0)
        assert is_valid_assembly(boxes)
        g = build(boxes)
        assert g.label == all_pairs(boxes)


def test_contacts_match_voxel_faces():
    rng = random.Random(2)
    for _ in range(200):
        n = rng.randint(2, 12)
        boxes = random_boxes(rng, n, size=5, max_side=3, connected=False)
        assert build(boxes).label == voxel_faces(boxes, 5)


def test_edge_and_corner_touch_are_not_liaisons():
    a = (0, 0, 0, 1, 1, 1)
    edge = (1, 1, 0, 2, 2, 1)
    corner = (1, 1, 1, 2, 2, 2)
    face = (1, 0, 0, 2, 1, 1)
    g = build([a, edge, corner, face])
    assert (0, 1) not in g.label and (0, 2) not in g.label
    assert g.label[(0, 3)] == ("contact", 0, 1, 1)


def test_fraction_coordinates():
    h = Fraction(1, 2)
    boxes = [(0, 0, 0, h, 1, 1), (h, Fraction(1, 3), 0, 1, 1, 1)]
    g = build(boxes)
    assert g.label[(0, 1)] == ("contact", 0, 1, Fraction(2, 3))


def test_connected_subsets_against_all_subsets():
    rng = random.Random(3)
    for _ in range(150):
        n = rng.randint(1, 9)
        boxes = random_boxes(rng, n, size=5, max_side=2, connected=rng.random() < 0.7)
        g = build(boxes)
        pairs = g.liaisons()
        brute = sorted(m for m in range(1, 1 << n) if connected_by_bfs(n, pairs, m))
        got = g.connected_subsets()
        assert len(got) == len(set(got))
        assert sorted(got) == brute
        for m in range(1 << n):
            assert g.is_connected(m) == connected_by_bfs(n, pairs, m)


def test_counts_on_simple_graphs():
    for n in range(1, 9):
        chain = LiaisonGraph(n)
        for i in range(n - 1):
            chain.add_liaison(i, i + 1, ("fastener",))
        assert len(chain.connected_subsets()) == n * (n + 1) // 2
        star = LiaisonGraph(n)
        for i in range(1, n):
            star.add_liaison(0, i, ("fastener",))
        assert len(star.connected_subsets()) == 2 ** (n - 1) + n - 1
        full = LiaisonGraph(n)
        for i in range(n):
            for j in range(i + 1, n):
                full.add_liaison(i, j, ("fastener",))
        assert len(full.connected_subsets()) == 2 ** n - 1


def test_fastener_liaison():
    g = build([(0, 0, 0, 1, 1, 1), (2, 0, 0, 3, 1, 1)])
    assert g.liaisons() == []
    g.add_liaison(1, 0, ("fastener", "bolt"))
    assert g.liaisons() == [(0, 1)] and g.is_connected(0b11)
