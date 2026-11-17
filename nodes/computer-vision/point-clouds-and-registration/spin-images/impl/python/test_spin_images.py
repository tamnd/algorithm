# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spin-images/. The authors are listed in prov/9YPF70.jsonl.

import math
import random

import pytest

from spin_images import correlation, spin_coordinates, spin_image


def unit(v):
    length = math.sqrt(sum(x * x for x in v))
    return [x / length for x in v]


def rotation(rng):
    w, x, y, z = unit([rng.gauss(0, 1) for _ in range(4)])
    return (
        (1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)),
        (2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)),
        (2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)),
    )


def axis_rotation(axis, angle):
    """Rodrigues' rotation about a unit axis."""
    x, y, z = axis
    c, s, t = math.cos(angle), math.sin(angle), 1 - math.cos(angle)
    return (
        (t * x * x + c, t * x * y - s * z, t * x * z + s * y),
        (t * x * y + s * z, t * y * y + c, t * y * z - s * x),
        (t * x * z - s * y, t * y * z + s * x, t * z * z + c),
    )


def apply(R, v, t=(0.0, 0.0, 0.0)):
    return [sum(R[r][c] * v[c] for c in range(3)) + t[r] for r in range(3)]


def surface(rng, n):
    pts, nrm = [], []
    for _ in range(n):
        x, y = rng.uniform(-2, 2), rng.uniform(-2, 2)
        pts.append([x, y, 0.2 * x * x - 0.1 * y * y + 0.05 * x * y])
        nrm.append(unit([-(0.4 * x + 0.05 * y), -(-0.2 * y + 0.05 * x), 1.0]))
    return pts, nrm


def close(a, b, tol=1e-9):
    return all(abs(u - v) < tol for ra, rb in zip(a, b) for u, v in zip(ra, rb))


def example():
    pts = [[0, 0, 0], [1, 0, 0], [0, 1.5, 0.5], [-2.4, 0, -1], [3, 4, 0], [0.5, 0, 0]]
    nrm = [[0, 0, 1], [0, 0, 1], [0, 0, 1], unit([1, 0, 1]), [0, 0, 1], [0, 0, -1]]
    return pts, nrm


def test_example() -> None:
    pts, nrm = example()
    img = spin_image(pts, nrm, (0, 0, 0), (0, 0, 1), 1.0, 5, 60.0)
    expected = [
        [0, 0, 0, 0, 0],
        [0, 0.25, 0.25, 0, 0],
        [1, 1.25, 0.25, 0, 0],
        [0, 0, 0.6, 0.4, 0],
        [0, 0, 0, 0, 0],
    ]
    assert close(img, expected)
    al, be = spin_coordinates((0, 0, 0), (0, 0, 1), (-2.4, 0, -1))
    assert abs(al - 2.4) < 1e-12 and be == -1


def test_weights_sum_to_the_accepted_points() -> None:
    rng = random.Random(71)
    pts, nrm = surface(rng, 300)
    for i in range(10):
        img = spin_image(pts, nrm, pts[i], nrm[i], 0.25, 9, 60.0)
        accepted = 0
        for x, nx in zip(pts, nrm):
            if sum(a * b for a, b in zip(nrm[i], nx)) < math.cos(math.radians(60)):
                continue
            al, be = spin_coordinates(pts[i], nrm[i], x)
            if al <= 2.0 and abs(be) <= 1.0:
                accepted += 1
        assert abs(sum(map(sum, img)) - accepted) < 1e-9
        assert min(min(row) for row in img) >= 0


def oracle(points, normals, p, n, b, w, angle):
    """Tent-function form of bilinear binning, cell by cell."""
    bmax, amax = (w - 1) * b / 2, (w - 1) * b
    img = [[0.0] * w for _ in range(w)]
    for x, nx in zip(points, normals):
        if sum(u * v for u, v in zip(n, nx)) < math.cos(math.radians(angle)):
            continue
        d = [x[k] - p[k] for k in range(3)]
        be = sum(n[k] * d[k] for k in range(3))
        al = math.sqrt(max(0.0, sum(t * t for t in d) - be * be))
        if al > amax or abs(be) > bmax:
            continue
        for r in range(w):
            for c in range(w):
                wr = max(0.0, 1 - abs((bmax - be) / b - r))
                wc = max(0.0, 1 - abs(al / b - c))
                img[r][c] += wr * wc
    return img


def test_matches_oracle() -> None:
    rng = random.Random(72)
    pts, nrm = surface(rng, 200)
    for i in range(8):
        a = spin_image(pts, nrm, pts[i], nrm[i], 0.3, 8, 70.0)
        b = oracle(pts, nrm, pts[i], nrm[i], 0.3, 8, 70.0)
        assert close(a, b)


def test_rigid_motion_invariance() -> None:
    rng = random.Random(73)
    pts, nrm = surface(rng, 250)
    R = rotation(rng)
    t = (3.0, -1.0, 2.0)
    mp = [apply(R, p, t) for p in pts]
    mn = [apply(R, m) for m in nrm]
    for i in range(8):
        a = spin_image(pts, nrm, pts[i], nrm[i], 0.25, 10, 60.0)
        b = spin_image(mp, mn, mp[i], mn[i], 0.25, 10, 60.0)
        assert close(a, b)


def test_rotation_about_the_normal_moves_only_the_cloud() -> None:
    # Rotating the cloud about the normal line of p, with p and n fixed,
    # does not change the image of p.
    rng = random.Random(74)
    pts, nrm = surface(rng, 250)
    p, n = pts[0], nrm[0]
    R = axis_rotation(n, 1.234)
    mp = [[a + b for a, b in zip(apply(R, [q[k] - p[k] for k in range(3)]), p)] for q in pts]
    mn = [apply(R, m) for m in nrm]
    assert close(spin_image(pts, nrm, p, n, 0.3, 9), spin_image(mp, mn, p, n, 0.3, 9))


def test_flipping_the_normal_reverses_the_rows() -> None:
    rng = random.Random(75)
    pts, nrm = surface(rng, 200)
    p, n = pts[3], nrm[3]
    a = spin_image(pts, nrm, p, n, 0.3, 9, 180.0)
    b = spin_image(pts, nrm, p, [-v for v in n], 0.3, 9, 180.0)
    assert close(a, b[::-1])


def test_support() -> None:
    pts, nrm = example()
    # Point 5 has an opposite normal: a support angle of 180 degrees takes it.
    wide = spin_image(pts, nrm, (0, 0, 0), (0, 0, 1), 1.0, 5, 180.0)
    narrow = spin_image(pts, nrm, (0, 0, 0), (0, 0, 1), 1.0, 5, 60.0)
    assert abs(sum(map(sum, wide)) - sum(map(sum, narrow)) - 1) < 1e-12
    assert abs(wide[2][0] - narrow[2][0] - 0.5) < 1e-12
    # Point 4 has alpha = 5 > alpha_max = 4. A width of 7 gives alpha_max = 6 and takes it.
    big = spin_image(pts, nrm, (0, 0, 0), (0, 0, 1), 1.0, 7, 60.0)
    assert abs(sum(map(sum, big)) - 5) < 1e-12


def test_correlation() -> None:
    rng = random.Random(76)
    pts, nrm = surface(rng, 200)
    a = spin_image(pts, nrm, pts[0], nrm[0], 0.3, 8)
    assert abs(correlation(a, a) - 1) < 1e-12
    assert abs(correlation(a, [[2 * v + 1 for v in row] for row in a]) - 1) < 1e-12
    assert correlation(a, [[0.0] * 8 for _ in range(8)]) is None
    with pytest.raises(ValueError):
        correlation(a, [[0.0]])


def test_edges() -> None:
    assert spin_image([], [], (0, 0, 0), (0, 0, 1), 1.0, 3) == [[0.0] * 3 for _ in range(3)]
    with pytest.raises(ValueError):
        spin_image([], [], (0, 0, 0), (0, 0, 1), 0.0, 3)
    with pytest.raises(ValueError):
        spin_image([], [], (0, 0, 0), (0, 0, 1), 1.0, 1)
