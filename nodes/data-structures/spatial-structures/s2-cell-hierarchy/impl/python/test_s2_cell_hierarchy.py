# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/s2-cell-hierarchy/. The authors are listed in prov/MMDM7B.jsonl.
import random

import pytest

from s2_cell_hierarchy import (MAX_LEVEL, MAX_SIZE, children, contains, face, face_uv_to_xyz,
                               from_face_ij, from_latlng, from_token, ij_bounds, is_valid,
                               latlng_to_xyz, level, lsb, parent, range_max, range_min,
                               st_to_ij, st_to_uv, to_face_ij, token, uv_to_st, xyz_to_face_uv)

FACE = [(f << 61) | (1 << 60) for f in range(6)]


def test_page_example():
    c = from_latlng(40.7128, -74.0060)  # New York
    assert face(c) == 4 and level(c) == 30
    assert token(c).startswith("89c25")
    assert [token(parent(c, k)) for k in (0, 1, 2)] == ["9", "8c", "89"]
    assert token(from_latlng(0, 0)) == "1000000000000001"
    kids = children(parent(c, 0))
    assert [token(x) for x in kids] == ["84", "8c", "94", "9c"]
    assert contains(kids[1], c) and not contains(kids[0], c)


def test_faces_and_tokens():
    assert [token(x) for x in FACE] == ["1", "3", "5", "7", "9", "b"]
    for x in FACE:
        assert level(x) == 0 and is_valid(x)
        assert from_token(token(x)) == x
    assert not is_valid(0) and not is_valid(2)
    with pytest.raises(ValueError):
        children(from_latlng(1, 2))
    with pytest.raises(ValueError):
        parent(FACE[0], 1)


def corners(c):
    f, i0, j0, s = ij_bounds(c)
    out = set()
    for di in (0, s):
        for dj in (0, s):
            p = face_uv_to_xyz(f, st_to_uv((i0 + di) / MAX_SIZE), st_to_uv((j0 + dj) / MAX_SIZE))
            n = sum(a * a for a in p) ** 0.5
            out.add(tuple(round(a / n, 9) for a in p))
    return out


def test_hilbert_order_is_continuous():
    lev = 3
    cells = []
    for f in range(6):
        c = parent(range_min(FACE[f]), lev)
        for _ in range(4 ** lev):
            cells.append(c)
            c += 2 * lsb(c)
    for a, b in zip(cells, cells[1:] + cells[:1]):
        assert len(corners(a) & corners(b)) == 2  # consecutive cells share an edge


def test_random_against_brute_force():
    rng = random.Random(5)
    for trial in range(600):
        lat, lng = rng.uniform(-90, 90), rng.uniform(-180, 180)
        leaf = from_latlng(lat, lng)
        f, u, v = xyz_to_face_uv(latlng_to_xyz(lat, lng))
        i, j = st_to_ij(uv_to_st(u)), st_to_ij(uv_to_st(v))
        assert to_face_ij(leaf)[:3] == (f, i, j)
        assert from_face_ij(f, i, j) == leaf
        lev = rng.randint(0, MAX_LEVEL)
        c = parent(leaf, lev)
        assert level(c) == lev and contains(c, leaf) and is_valid(c)
        # descend from the face by children, choosing by (i, j): same cell
        d = FACE[f]
        for _ in range(lev):
            for k in children(d):
                _, i0, j0, s = ij_bounds(k)
                if i0 <= i < i0 + s and j0 <= j < j0 + s:
                    d = k
                    break
        assert d == c
        if lev < MAX_LEVEL:
            ks = children(c)
            assert all(parent(k, lev) == c for k in ks)
            assert range_min(ks[0]) == range_min(c) and range_max(ks[3]) == range_max(c)
            assert sum(contains(k, leaf) for k in ks) == 1
        assert from_token(token(c)) == c
