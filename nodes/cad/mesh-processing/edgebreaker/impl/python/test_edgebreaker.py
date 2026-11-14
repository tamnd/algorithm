# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/edgebreaker/. The authors are listed in prov/5F4MY3.jsonl.

import random

import pytest

from edgebreaker import decode, encode, from_bits, right_loop_lengths, to_bits

TET = [(0, 2, 1), (0, 1, 3), (1, 2, 3), (2, 0, 3)]
OCTA = [(0, 2, 4), (2, 1, 4), (1, 3, 4), (3, 0, 4), (2, 0, 5), (1, 2, 5), (3, 1, 5), (0, 3, 5)]
ICO = [(0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11), (1, 5, 9), (5, 11, 4),
       (11, 10, 2), (10, 7, 6), (7, 1, 8), (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8),
       (3, 8, 9), (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1)]


def bipyramid(n):
    """n side vertices 0..n-1, apex n and n+1."""
    faces = []
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n))
        faces.append((j, i, n + 1))
    return faces


def subdivide(faces):
    """Split each triangle into four."""
    nv = 1 + max(x for t in faces for x in t)
    mid = {}

    def m(a, b):
        nonlocal nv
        key = (min(a, b), max(a, b))
        if key not in mid:
            mid[key] = nv
            nv += 1
        return mid[key]

    out = []
    for a, b, c in faces:
        ab, bc, ca = m(a, b), m(b, c), m(c, a)
        out += [(a, ab, ca), (ab, b, bc), (ca, bc, c), (ab, bc, ca)]
    return out


def random_flips(faces, k, rng):
    """k random edge flips that keep the mesh simplicial (no double edge, every degree at least 3)."""
    faces = [list(t) for t in faces]
    done = 0
    for _ in range(50 * k):
        if done == k:
            break
        where = {}
        nbr = {}
        for f, t in enumerate(faces):
            for i in range(3):
                where[(t[i], t[(i + 1) % 3])] = (f, t[(i + 2) % 3])
                nbr.setdefault(t[i], set()).add(t[(i + 1) % 3])
        a, b = rng.choice(sorted(where))
        f, c = where[(a, b)]
        g, d = where[(b, a)]
        if d in nbr[c] or len(nbr[a]) <= 3 or len(nbr[b]) <= 3:
            continue
        faces[f] = [c, a, d]
        faces[g] = [d, b, c]
        done += 1
    return [tuple(t) for t in faces]


def canon(t):
    k = t.index(min(t))
    return t[k:] + t[:k]


def relabel(faces, rng):
    """The same mesh with random vertex ids, a random face order and random rotations of each face."""
    ids = sorted({x for t in faces for x in t})
    new = list(range(100, 100 + len(ids)))
    rng.shuffle(new)
    lab = dict(zip(ids, new))
    out = []
    for t in faces:
        r = rng.randrange(3)
        t = tuple(lab[x] for x in t)
        out.append(t[r:] + t[:r])
    rng.shuffle(out)
    return out


def meshes():
    rng = random.Random(7)
    out = [("pillow", [(0, 1, 2), (0, 2, 1)]), ("tet", TET), ("octa", OCTA), ("ico", ICO), ("tet1", subdivide(TET)),
           ("octa1", subdivide(OCTA)), ("ico1", subdivide(ICO))]
    out += [("bipyramid%d" % n, bipyramid(n)) for n in (3, 4, 5, 9)]
    for i in range(6):
        base = [OCTA, ICO, subdivide(OCTA)][i % 3]
        out.append(("flipped%d" % i, random_flips(base, 10 + 15 * i, rng)))
    return out


def check_round_trip(faces, start):
    symbols, order, tri_order = encode(faces, start)
    got = decode(symbols)
    index = {v: i for i, v in enumerate(order)}
    assert sorted(order) == sorted({x for t in faces for x in t})
    # Same mesh up to vertex order: the relabelled input is exactly the decoded list, face by face.
    want = [tuple(index[x] for x in faces[f]) for f in tri_order]
    assert [canon(t) for t in got] == [canon(t) for t in want]
    assert sorted(tri_order) == list(range(len(faces)))
    return symbols


def test_decode_inverts_encode_from_every_start():
    for name, faces in meshes():
        for start in range(len(faces)):
            check_round_trip(faces, start)


def test_round_trip_after_random_relabelling():
    rng = random.Random(11)
    for name, faces in meshes():
        for _ in range(5):
            g = relabel(faces, rng)
            check_round_trip(g, rng.randrange(len(g)))


def test_counts_and_bit_bound():
    for name, faces in meshes():
        t = len(faces)
        v = len({x for f in faces for x in f})
        assert v - 3 * t // 2 + t == 2
        for start in range(len(faces)):
            symbols, _, _ = encode(faces, start)
            assert len(symbols) == t - 1
            assert symbols.count("C") == v - 3
            assert symbols.count("E") == symbols.count("S") + 1
            bits = to_bits(symbols)
            assert len(bits) == 2 * t - 1
            assert from_bits(bits) == symbols


def test_all_five_symbols_occur():
    seen = set()
    for name, faces in meshes():
        for start in range(len(faces)):
            seen |= set(encode(faces, start)[0])
    assert seen == set("CLRSE")


def slow_lengths(symbols):
    """Brute force: for each S, scan forward until its right branch has one more E than S."""
    out = {}
    for i, s in enumerate(symbols):
        if s != "S":
            continue
        bal, j = 1, i
        while bal:
            j += 1
            bal += {"S": 1, "E": -1}.get(symbols[j], 0)
        part = symbols[i + 1:j + 1]
        # Each C adds one edge to the loop, L and R remove one, S adds one, E removes three.
        size = 0
        for x in reversed(part):
            size += {"C": -1, "L": 1, "R": 1, "S": -1, "E": 3}[x]
        out[i] = size
    return out


def test_loop_lengths_match_a_slow_scan():
    for name, faces in meshes():
        for start in range(0, len(faces), 3):
            symbols, order, tri_order = encode(faces, start)
            lengths = right_loop_lengths(symbols)
            assert lengths == slow_lengths(symbols)
            assert sorted(lengths) == [i for i, s in enumerate(symbols) if s == "S"]
            assert all(n >= 3 for n in lengths.values())


def test_rejects_meshes_that_are_not_spheres():
    with pytest.raises(ValueError):
        encode(TET[:3])  # a disk with a boundary
    torus = []
    m, n = 3, 4
    for i in range(m):
        for j in range(n):
            a, b = i * n + j, i * n + (j + 1) % n
            c, d = ((i + 1) % m) * n + j, ((i + 1) % m) * n + (j + 1) % n
            torus += [(a, b, d), (a, d, c)]
    with pytest.raises(ValueError):
        encode(torus)
    # Two octahedra glued at two opposite vertices: V - E + F = 10 - 24 + 16 = 2, but not a sphere.
    other = {0: 0, 1: 1, 2: 6, 3: 7, 4: 8, 5: 9}
    pinched = OCTA + [tuple(other[x] for x in f) for f in OCTA]
    with pytest.raises(ValueError):
        encode(pinched)
    with pytest.raises(ValueError):
        encode([(0, 0, 1)] + TET)
    with pytest.raises(ValueError):
        decode("CCE")  # too short for its loops
    with pytest.raises(ValueError):
        decode("CRSE")  # an S without the E of its second loop
