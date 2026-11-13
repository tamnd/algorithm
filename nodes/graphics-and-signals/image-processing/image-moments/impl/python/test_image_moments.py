# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/image-moments/. The authors are listed in prov/Q8B269.jsonl.

import math
import random
from fractions import Fraction

from image_moments import (
    cell_raw_moments,
    central_moments,
    centroid,
    complex_central_moment,
    hu_moments,
    image_points,
    normalized_central_moment,
    orientation,
    principal_variances,
    raw_moments,
)

# An L of five pixels: a column of three and a foot of two to the right.
L_SHAPE = [
    [1, 0, 0],
    [1, 0, 0],
    [1, 1, 1],
]


def random_points(rng, n):
    return [(Fraction(rng.randint(-20, 20), rng.choice([1, 2, 3])), Fraction(rng.randint(-20, 20)), Fraction(rng.randint(1, 9))) for _ in range(n)]


def random_image(rng, h, w):
    img = [[rng.choice([0, 0, 1, 3, 7]) for _ in range(w)] for _ in range(h)]
    img[rng.randrange(h)][rng.randrange(w)] = 5
    return img


def direct_raw(points, p, q):
    return sum((w * x**p * y**q for x, y, w in points), Fraction(0))


def direct_central(points, p, q):
    n = sum(w for _, _, w in points)
    xc = sum(w * x for x, _, w in points) / n
    yc = sum(w * y for _, y, w in points) / n
    return sum((w * (x - xc) ** p * (y - yc) ** q for x, y, w in points), Fraction(0))


def exact_eta(mu, p, q):
    """eta_pq as a Fraction; needs mu_00 to be the square of an integer."""
    t = math.isqrt(int(mu[0, 0]))
    assert t * t == mu[0, 0]
    return mu[p, q] / Fraction(t) ** (p + q + 2)


def hu_from_eta(mu):
    """Hu's seven formulas written in the normalized central moments."""
    e = {pq: exact_eta(mu, *pq) for pq in mu if sum(pq) >= 2}
    n20, n02, n11 = e[2, 0], e[0, 2], e[1, 1]
    n30, n03, n21, n12 = e[3, 0], e[0, 3], e[2, 1], e[1, 2]
    a, b = n30 + n12, n21 + n03
    return [
        n20 + n02,
        (n20 - n02) ** 2 + 4 * n11**2,
        (n30 - 3 * n12) ** 2 + (3 * n21 - n03) ** 2,
        a**2 + b**2,
        (n30 - 3 * n12) * a * (a**2 - 3 * b**2) + (3 * n21 - n03) * b * (3 * a**2 - b**2),
        (n20 - n02) * (a**2 - b**2) + 4 * n11 * a * b,
        (3 * n21 - n03) * a * (a**2 - 3 * b**2) - (n30 - 3 * n12) * b * (3 * a**2 - b**2),
    ]


def transform(points, f):
    return [f(x, y, w) for x, y, w in points]


def test_moments_equal_direct_sums():
    rng = random.Random(1)
    for _ in range(50):
        pts = random_points(rng, rng.randint(1, 12))
        m = raw_moments(pts, 4)
        mu = central_moments(m)
        for p, q in m:
            assert m[p, q] == direct_raw(pts, p, q)
            assert mu[p, q] == direct_central(pts, p, q)
        assert mu[1, 0] == mu[0, 1] == 0 and mu[0, 0] == m[0, 0]


def test_cell_moments_are_integrals():
    # A solid a x b rectangle of unit squares: the integrals are known.
    for a, b in [(1, 1), (3, 2), (4, 5)]:
        img = [[1] * a for _ in range(b)]
        mu = central_moments(cell_raw_moments(img, 4))
        assert mu[0, 0] == a * b
        assert mu[2, 0] == Fraction(a**3 * b, 12) and mu[0, 2] == Fraction(a * b**3, 12)
        assert mu[1, 1] == mu[3, 0] == mu[2, 1] == 0
        assert mu[4, 0] == Fraction(a**5 * b, 80)
    # One cell differs from one point by the integral of t^2 over [-1/2, 1/2].
    rng = random.Random(2)
    img = random_image(rng, 3, 4)
    pm, cm = raw_moments(image_points(img), 2), cell_raw_moments(img, 2)
    assert cm[0, 0] == pm[0, 0] and cm[1, 0] == pm[1, 0] and cm[1, 1] == pm[1, 1]
    assert cm[2, 0] == pm[2, 0] + pm[0, 0] / 12


def test_hu_from_complex_moments_matches_hus_formulas():
    rng = random.Random(3)
    for _ in range(60):
        pts = random_points(rng, rng.randint(2, 10))
        # Add one point so that the total weight is a square and eta is rational.
        total = int(sum(w for _, _, w in pts))
        t = math.isqrt(total) + 1
        pts.append((Fraction(rng.randint(-20, 20)), Fraction(rng.randint(-20, 20)), Fraction(t * t - total)))
        mu = central_moments(raw_moments(pts, 3))
        assert hu_moments(mu) == hu_from_eta(mu)
        for p, q in mu:
            if p + q >= 2:
                assert math.isclose(normalized_central_moment(mu, p, q), exact_eta(mu, p, q), rel_tol=1e-12, abs_tol=1e-300)


def test_translation_and_scale_invariance_is_exact():
    rng = random.Random(4)
    for _ in range(40):
        pts = random_points(rng, rng.randint(2, 10))
        dx, dy = Fraction(rng.randint(-50, 50), 7), Fraction(rng.randint(-50, 50), 3)
        s = Fraction(rng.randint(1, 9), rng.randint(1, 4))
        mu = central_moments(raw_moments(pts, 4))
        moved = central_moments(raw_moments(transform(pts, lambda x, y, w: (x + dx, y + dy, w)), 4))
        assert moved == mu
        # Scaling the plane by s multiplies each area, so each weight, by s^2.
        scaled = central_moments(raw_moments(transform(pts, lambda x, y, w: (s * x + dx, s * y + dy, s * s * w)), 4))
        for p, q in mu:
            assert scaled[p, q] == s ** (p + q + 2) * mu[p, q]
            if (p + q) % 2 == 0 and p + q >= 2:
                assert normalized_central_moment(scaled, p, q) == normalized_central_moment(mu, p, q)
        assert hu_moments(scaled) == hu_moments(mu)


def test_rotation_invariance_is_exact_and_phi7_flips_under_reflection():
    rng = random.Random(5)
    c, s = Fraction(3, 5), Fraction(4, 5)
    for _ in range(40):
        pts = random_points(rng, rng.randint(2, 10))
        hu = hu_moments(central_moments(raw_moments(pts, 3)))
        turned = transform(pts, lambda x, y, w: (c * x - s * y, s * x + c * y, w))
        assert hu_moments(central_moments(raw_moments(turned, 3))) == hu
        mirrored = hu_moments(central_moments(raw_moments(transform(pts, lambda x, y, w: (-x, y, w)), 3)))
        assert mirrored[:6] == hu[:6] and mirrored[6] == -hu[6]
        # The set is not independent: phi_5 + i phi_7 = c_30 c_12^3 gives phi_3 phi_4^3 = phi_5^2 + phi_7^2.
        assert hu[2] * hu[3] ** 3 == hu[4] ** 2 + hu[6] ** 2
        # phi_2, phi_4 and phi_6 fix Im(c_20 c_12^2) only up to its sign.
        mu = central_moments(raw_moments(pts, 3))
        c20, c12 = complex_central_moment(mu, 2, 0), complex_central_moment(mu, 1, 2)
        im = (c20[1] * (c12[0] ** 2 - c12[1] ** 2) + c20[0] * 2 * c12[0] * c12[1]) / mu[0, 0] ** 7
        assert hu[1] * hu[3] ** 2 - hu[5] ** 2 == im**2


def test_pixel_images_under_replication_and_quarter_turns():
    rng = random.Random(6)
    for _ in range(20):
        img = random_image(rng, rng.randint(1, 4), rng.randint(1, 4))
        k = rng.randint(2, 3)
        big = [[v for v in row for _ in range(k)] for row in img for _ in range(k)]
        # Cells: replication is an exact scaling, so eta and Hu do not change.
        small_c, big_c = central_moments(cell_raw_moments(img, 3)), central_moments(cell_raw_moments(big, 3))
        assert hu_moments(big_c) == hu_moments(small_c)
        # Points: the block of k x k points adds a fixed spread inside each pixel.
        small_p, big_p = central_moments(raw_moments(image_points(img), 2)), central_moments(raw_moments(image_points(big), 2))
        m00 = small_p[0, 0]
        extra = Fraction(k * k - 1, 12 * k * k) / m00
        assert normalized_central_moment(big_p, 2, 0) == normalized_central_moment(small_p, 2, 0) + extra
        assert normalized_central_moment(big_p, 0, 2) == normalized_central_moment(small_p, 0, 2) + extra
        assert normalized_central_moment(big_p, 1, 1) == normalized_central_moment(small_p, 1, 1)
        # A quarter turn of the pixel grid is exact in both models.
        turned = [list(r) for r in zip(*img[::-1])]
        assert hu_moments(central_moments(raw_moments(image_points(turned), 3))) == hu_moments(central_moments(raw_moments(image_points(img), 3)))
        assert hu_moments(central_moments(cell_raw_moments(turned, 3))) == hu_moments(small_c)


def test_example():
    m = raw_moments(image_points(L_SHAPE), 3)
    assert (m[0, 0], m[1, 0], m[0, 1]) == (5, 3, 7)
    assert centroid(m) == (Fraction(3, 5), Fraction(7, 5))
    mu = central_moments(m)
    assert (mu[2, 0], mu[0, 2], mu[1, 1]) == (Fraction(16, 5), Fraction(16, 5), Fraction(9, 5))
    assert (mu[3, 0], mu[0, 3], mu[2, 1], mu[1, 2]) == (Fraction(54, 25), Fraction(-54, 25), Fraction(21, 25), Fraction(-21, 25))
    assert math.isclose(orientation(mu), math.pi / 4)
    big, small = principal_variances(mu)
    assert math.isclose(big, 1) and math.isclose(small, 7 / 25)
    hu = hu_moments(mu)
    assert hu[:4] == [Fraction(32, 125), Fraction(324, 15625), Fraction(27378, 1953125), Fraction(2178, 1953125)]
    assert hu[6] == 0  # The L is its own mirror image in the line x + y = 2.
    # As unit squares, each pixel adds 1/12 to mu_20 and mu_02 and nothing else up to order 3.
    cells = central_moments(cell_raw_moments(L_SHAPE, 3))
    assert cells[2, 0] == cells[0, 2] == Fraction(217, 60)
    assert all(cells[pq] == mu[pq] for pq in mu if pq not in ((2, 0), (0, 2)))
