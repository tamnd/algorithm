# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/corner-stitching/. The authors are listed in prov/452WNT.jsonl.

import random

import pytest

from corner_stitching import Plane

W, H = 14, 12


def owner_grid(plane):
    """owner[x][y] is the tile that holds the unit cell [x, x+1) x [y, y+1).
    Every cell must be covered exactly once."""
    X0, Y0, X1, Y1 = plane.world
    owner = [[None] * (Y1 - Y0) for _ in range(X1 - X0)]
    for t in plane.tiles:
        assert t.x0 < t.x1 and t.y0 < t.y1
        for x in range(t.x0, t.x1):
            for y in range(t.y0, t.y1):
                assert owner[x - X0][y - Y0] is None, "tiles overlap"
                owner[x - X0][y - Y0] = t
    assert all(c is not None for col in owner for c in col), "a hole in the tiling"
    return owner


def canonical_space(solids, world):
    """Maximal horizontal strips of the free cells, by brute force over rows."""
    X0, Y0, X1, Y1 = world
    busy = set()
    for (a, b, c, d) in solids:
        for x in range(a, c):
            for y in range(b, d):
                busy.add((x, y))
    out, open_ = set(), {}
    for y in range(Y0, Y1 + 1):
        segs = set()
        if y < Y1:
            x = X0
            while x < X1:
                if (x, y) in busy:
                    x += 1
                    continue
                s = x
                while x < X1 and (x, y) not in busy:
                    x += 1
                segs.add((s, x))
        for seg in list(open_):
            if seg not in segs:
                out.add((seg[0], open_.pop(seg), seg[1], y))
        for seg in segs:
            open_.setdefault(seg, y)
    return out


def check(plane, solids):
    """Compare the whole structure with brute force."""
    X0, Y0, X1, Y1 = plane.world
    owner = owner_grid(plane)

    def at(x, y):
        if X0 <= x < X1 and Y0 <= y < Y1:
            return owner[x - X0][y - Y0]
        return None

    assert {t.rect() for t in plane.tiles if t.solid} == set(solids)
    assert {t.rect() for t in plane.tiles if not t.solid} == canonical_space(solids, plane.world)
    n_space = sum(1 for t in plane.tiles if not t.solid)
    assert n_space <= 3 * len(solids) + 1
    for t in plane.tiles:
        assert t.alive
        assert t.bl is at(t.x0, t.y0 - 1)
        assert t.lb is at(t.x0 - 1, t.y0)
        assert t.tr is at(t.x1 - 1, t.y1)
        assert t.rt is at(t.x1, t.y1 - 1)
    return at


def brute_neighbors(plane, t):
    tiles = plane.tiles
    top = [u for u in tiles if u.y0 == t.y1 and u.x0 < t.x1 and u.x1 > t.x0]
    right = [u for u in tiles if u.x0 == t.x1 and u.y0 < t.y1 and u.y1 > t.y0]
    bottom = [u for u in tiles if u.y1 == t.y0 and u.x0 < t.x1 and u.x1 > t.x0]
    left = [u for u in tiles if u.x1 == t.x0 and u.y0 < t.y1 and u.y1 > t.y0]
    return (
        sorted(top, key=lambda u: -u.x0),
        sorted(right, key=lambda u: -u.y0),
        sorted(bottom, key=lambda u: u.x0),
        sorted(left, key=lambda u: u.y0),
    )


def queries(plane, solids, at, rng):
    tiles = list(plane.tiles)
    for _ in range(30):
        x, y = rng.randrange(W), rng.randrange(H)
        assert plane.point_find(x, y, rng.choice(tiles)) is at(x, y)
    for _ in range(15):
        ax0, ax1 = sorted(rng.sample(range(W + 1), 2))
        ay0, ay1 = sorted(rng.sample(range(H + 1), 2))
        meets = [u for u in tiles if u.x0 < ax1 and u.x1 > ax0 and u.y0 < ay1 and u.y1 > ay0]
        got = plane.enumerate_area(ax0, ay0, ax1, ay1)
        assert len(got) == len(set(map(id, got))), "a tile was reported twice"
        assert set(map(id, got)) == set(map(id, meets))
        hit = plane.area_search(ax0, ay0, ax1, ay1)
        if any(u.solid for u in meets):
            assert hit is not None and hit.solid and hit in meets
        else:
            assert hit is None
    for t in rng.sample(tiles, min(6, len(tiles))):
        want = brute_neighbors(plane, t)
        got = (plane.top_neighbors(t), plane.right_neighbors(t),
               plane.bottom_neighbors(t), plane.left_neighbors(t))
        assert got == want


def test_empty_world():
    p = Plane(0, 0, W, H)
    at = check(p, [])
    assert len(p.tiles) == 1
    assert p.area_search(0, 0, W, H) is None
    queries(p, [], at, random.Random(1))


def test_page_example():
    # The example of the page: world [0, 10) x [0, 8), two solid tiles.
    p = Plane(0, 0, 10, 8)
    a = p.insert(2, 2, 5, 5)
    b = p.insert(6, 4, 9, 7)
    space = sorted(t.rect() for t in p.tiles if not t.solid)
    assert space == [(0, 0, 10, 2), (0, 2, 2, 5), (0, 5, 6, 7), (0, 7, 10, 8),
                     (5, 2, 10, 4), (5, 4, 6, 5), (9, 4, 10, 7)]
    assert a.tr.rect() == (0, 5, 6, 7) and a.rt.rect() == (5, 4, 6, 5)
    assert a.bl.rect() == (0, 0, 10, 2) and a.lb.rect() == (0, 2, 2, 5)
    check(p, [(2, 2, 5, 5), (6, 4, 9, 7)])
    start = p.point_find(0, 0)
    assert p.point_find(7, 5, start) is b
    assert p.area_search(5, 0, 6, 8) is None
    assert p.area_search(4, 6, 7, 8) is b
    p.delete(a)
    check(p, [(6, 4, 9, 7)])


def test_insert_rejects_overlap():
    p = Plane(0, 0, W, H)
    p.insert(3, 3, 6, 6)
    with pytest.raises(ValueError):
        p.insert(5, 5, 8, 8)
    check(p, [(3, 3, 6, 6)])


@pytest.mark.parametrize("seed", range(20))
def test_random_insert_delete(seed):
    rng = random.Random(seed)
    p = Plane(0, 0, W, H)
    solids = {}
    for step in range(150):
        if solids and rng.random() < 0.3:
            r = rng.choice(sorted(solids))
            p.delete(solids.pop(r))
        else:
            w, h = rng.randint(1, 5), rng.randint(1, 4)
            x, y = rng.randrange(W - w + 1), rng.randrange(H - h + 1)
            r = (x, y, x + w, y + h)
            free = all(r[2] <= s[0] or s[2] <= r[0] or r[3] <= s[1] or s[3] <= r[1] for s in solids)
            if free:
                solids[r] = p.insert(*r)
            else:
                with pytest.raises(ValueError):
                    p.insert(*r)
        at = check(p, list(solids))
        if step % 5 == 0:
            queries(p, list(solids), at, rng)


def test_unit_cells_dense():
    # Fill a checkerboard of unit squares, then remove them in random order.
    rng = random.Random(7)
    p = Plane(0, 0, 8, 8)
    solids = {}
    for x in range(8):
        for y in range(8):
            if (x + y) % 2 == 0:
                solids[(x, y, x + 1, y + 1)] = p.insert(x, y, x + 1, y + 1)
    check(p, list(solids))
    keys = sorted(solids)
    rng.shuffle(keys)
    for r in keys:
        p.delete(solids.pop(r))
        check(p, list(solids))
    assert len(p.tiles) == 1
