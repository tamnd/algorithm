# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hopcroft-tarjan-isomorphism/. The authors are listed in prov/NBDRZ3.jsonl.

import itertools
import random

from hopcroft_tarjan_isomorphism import (_Maps, map_isomorphism, mirror, refine,
                                         triconnected_planar_isomorphism)

Rotation = list[list[int]]
Face = tuple[int, int, int]

BIPYRAMID = [[1, 2, 3], [2, 0, 3, 4], [0, 1, 4, 3], [0, 2, 4, 1], [2, 1, 3]]
CHIRAL7 = [[1, 2, 5, 4], [2, 0, 4], [0, 1, 4, 3, 6, 5], [5, 6, 2, 4],
           [1, 0, 5, 3, 2], [0, 2, 6, 3, 4], [3, 5, 2]]


def rot_from_faces(n: int, faces: list[Face]) -> Rotation:
    succ: list[dict[int, int]] = [dict() for _ in range(n)]
    for f in faces:
        for i in range(3):
            succ[f[i]][f[(i + 1) % 3]] = f[(i + 2) % 3]
    rot = []
    for v in range(n):
        a0 = next(iter(succ[v]))
        out, a = [a0], succ[v][a0]
        while a != a0:
            out.append(a)
            a = succ[v][a]
        rot.append(out)
    return rot


def random_triangulation(rng: random.Random, n: int, flips: int) -> tuple[int, list[Face]]:
    """A random simple triangulation of the sphere: face splits, then edge flips."""
    faces = [(0, 1, 2), (0, 2, 3), (0, 3, 1), (1, 3, 2)]
    k = 4
    while k < n:
        a, b, c = faces.pop(rng.randrange(len(faces)))
        faces += [(a, b, k), (b, c, k), (c, a, k)]
        k += 1
    for _ in range(flips):
        rot = rot_from_faces(k, faces)
        f1 = rng.choice(faces)
        i = rng.randrange(3)
        a, b, c = f1[i], f1[(i + 1) % 3], f1[(i + 2) % 3]
        f2 = next(f for f in faces for j in range(3) if f[j] == b and f[(j + 1) % 3] == a)
        d = next(x for x in f2 if x not in (a, b))
        if len(rot[a]) <= 3 or len(rot[b]) <= 3 or d in rot[c]:
            continue
        faces.remove(f1)
        faces.remove(f2)
        faces += [(a, d, c), (d, b, c)]
    return k, faces


def dual(faces: list[Face]) -> Rotation:
    """The dual map: a 3-connected cubic planar graph."""
    edge_face = {}
    for i, f in enumerate(faces):
        for j in range(3):
            edge_face[(f[j], f[(j + 1) % 3])] = i
    return [[edge_face[(f[(j + 1) % 3], f[j])] for j in range(3)] for f in faces]


def relabel(rng: random.Random, rot: Rotation) -> Rotation:
    n = len(rot)
    p = list(range(n))
    rng.shuffle(p)
    out: Rotation = [[] for _ in range(n)]
    for v in range(n):
        lst = [p[x] for x in rot[v]]
        s = rng.randrange(len(lst))
        out[p[v]] = lst[s:] + lst[:s]
    return out


def edges(rot: Rotation) -> list[tuple[int, int]]:
    return [(u, v) for u in range(len(rot)) for v in rot[u] if u < v]


def is_isomorphism(phi: list[int], r1: Rotation, r2: Rotation) -> bool:
    e2 = {frozenset(e) for e in edges(r2)}
    return sorted(phi) == list(range(len(r1))) and len(edges(r1)) == len(e2) and \
        all(frozenset((phi[u], phi[v])) in e2 for u, v in edges(r1))


def brute_iso(r1: Rotation, r2: Rotation) -> bool:
    n = len(r1)
    if n != len(r2) or len(edges(r1)) != len(edges(r2)):
        return False
    return any(is_isomorphism(list(p), r1, r2) for p in itertools.permutations(range(n)))


def classes(r1: Rotation, r2: Rotation) -> list[int]:
    maps = _Maps(r1, r2)
    lab = maps.labels()
    keys = sorted(set(lab))
    block_of = [keys.index(x) for x in lab]
    blocks = [[d for d in range(len(lab)) if block_of[d] == i] for i in range(len(keys))]
    refine(maps, block_of, blocks, list(range(len(blocks))))
    return sorted(len(b) for b in blocks if b)


def test_page_example() -> None:
    p = [2, 0, 4, 1, 3]
    r2: Rotation = [[] for _ in range(5)]
    for v in range(5):
        r2[p[v]] = [p[x] for x in BIPYRAMID[v]]
    assert r2 == [[4, 2, 1, 3], [2, 4, 3, 0], [0, 4, 1], [4, 0, 1], [2, 0, 3, 1]]
    assert classes(BIPYRAMID, r2) == [12, 12, 12]
    assert map_isomorphism(BIPYRAMID, r2) == [2, 0, 4, 1, 3]
    assert map_isomorphism(BIPYRAMID, mirror(r2)) == [2, 1, 4, 0, 3]
    assert map_isomorphism(CHIRAL7, mirror(CHIRAL7)) is None
    phi = triconnected_planar_isomorphism(CHIRAL7, mirror(CHIRAL7))
    assert phi is not None and is_isomorphism(phi, CHIRAL7, CHIRAL7)


def test_edge_cases() -> None:
    k4 = rot_from_faces(4, [(0, 1, 2), (0, 2, 3), (0, 3, 1), (1, 3, 2)])
    assert classes(k4, k4) == [24]
    assert triconnected_planar_isomorphism(k4, mirror(k4)) is not None
    assert map_isomorphism(k4, BIPYRAMID) is None
    assert map_isomorphism([[]], [[]]) == [0]
    assert map_isomorphism([[1], [0]], [[1], [0]]) is not None


def test_small_against_brute_force() -> None:
    rng = random.Random(20261105)
    for trial in range(300):
        n = rng.randint(4, 7)
        k, f = random_triangulation(rng, n, rng.randint(0, 20))
        r1 = rot_from_faces(k, f)
        if trial % 2 == 0:
            r2 = relabel(rng, mirror(r1) if rng.random() < 0.5 else r1)
        else:
            k2, f2 = random_triangulation(rng, n, rng.randint(0, 20))
            r2 = relabel(rng, rot_from_faces(k2, f2))
        phi = triconnected_planar_isomorphism(r1, r2)
        assert (phi is not None) == brute_iso(r1, r2)
        if phi is not None:
            assert is_isomorphism(phi, r1, r2)


def test_cubic_duals_against_brute_force() -> None:
    rng = random.Random(77)
    for trial in range(200):
        n = rng.randint(4, 6)
        k, f = random_triangulation(rng, n, rng.randint(0, 20))
        r1 = dual(f)
        if trial % 2 == 0:
            r2 = relabel(rng, mirror(r1) if rng.random() < 0.5 else r1)
        else:
            _, f2 = random_triangulation(rng, n, rng.randint(0, 20))
            r2 = relabel(rng, dual(f2))
        phi = triconnected_planar_isomorphism(r1, r2)
        assert (phi is not None) == brute_iso(r1, r2)
        if phi is not None:
            assert is_isomorphism(phi, r1, r2)


def test_larger_relabelings() -> None:
    rng = random.Random(5)
    for _ in range(100):
        k, f = random_triangulation(rng, rng.randint(8, 30), 60)
        r1 = rot_from_faces(k, f)
        r2 = relabel(rng, mirror(r1))
        phi = triconnected_planar_isomorphism(r1, r2)
        assert phi is not None and is_isomorphism(phi, r1, r2)
