# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/free-form-deformation/. The authors are listed in prov/5QACBN.jsonl.
import random
from fractions import Fraction as F

from free_form_deformation import Lattice, bernstein, de_casteljau_volume, det3


def unit_lattice(l=2, m=2, n=2):
    return Lattice((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), l, m, n)


def skew_lattice(l, m, n):
    return Lattice((1, -2, 3), (2, 1, 0), (F(1, 2), 3, 1), (0, 1, 4), l, m, n)


def rand_point_inside(lat, rng):
    s, t, u = (F(rng.randint(0, 64), 64) for _ in range(3))
    a, b, c = lat.axes
    return tuple(lat.x0[d] + s * a[d] + t * b[d] + u * c[d] for d in range(3))


def test_bernstein_partition_of_unity():
    for deg in range(6):
        for x in (F(0), F(1, 3), F(5, 7), F(1)):
            assert sum(bernstein(deg, x)) == 1


def test_local_coordinates_are_inverse_of_embedding():
    lat = skew_lattice(3, 2, 1)
    rng = random.Random(1)
    for _ in range(20):
        s, t, u = (F(rng.randint(-10, 10), 7) for _ in range(3))
        a, b, c = lat.axes
        x = tuple(lat.x0[d] + s * a[d] + t * b[d] + u * c[d] for d in range(3))
        assert lat.local(x) == (s, t, u)


def test_rest_lattice_is_exact_identity():
    rng = random.Random(2)
    for deg in ((1, 1, 1), (2, 2, 2), (3, 2, 1), (4, 1, 3)):
        lat = skew_lattice(*deg)
        for _ in range(10):
            x = rand_point_inside(lat, rng)
            assert lat.deform(x) == x


def test_affine_motion_of_lattice_is_reproduced_exactly():
    rng = random.Random(3)
    a = [[F(rng.randint(-5, 5), 3) for _ in range(3)] for _ in range(3)]
    b = [F(rng.randint(-5, 5), 2) for _ in range(3)]

    def aff(p):
        return tuple(sum(a[r][c] * p[c] for c in range(3)) + b[r] for r in range(3))

    lat = skew_lattice(3, 2, 2)
    lat.points = [[[aff(p) for p in row] for row in plane] for plane in lat.points]
    for _ in range(10):
        x = rand_point_inside(lat, rng)
        assert lat.deform(x) == aff(x)


def test_matches_de_casteljau():
    rng = random.Random(4)
    lat = unit_lattice(3, 2, 4)
    lat.points = [[[tuple(F(rng.randint(-20, 20), 5) for _ in range(3)) for _ in row] for row in plane] for plane in lat.points]
    for _ in range(10):
        s, t, u = (F(rng.randint(0, 30), 30) for _ in range(3))
        assert lat.evaluate(s, t, u) == de_casteljau_volume(lat.points, s, t, u)


def test_worked_example_center_point():
    lat = unit_lattice(2, 2, 2)
    lat.points[1][1][1] = (F(1, 2), F(1, 2), F(1))
    y = lat.deform((F(1, 2), F(1, 2), F(1, 2)))
    assert y == (F(1, 2), F(1, 2), F(9, 16))
    assert all(isinstance(v, F) for v in y)
    assert lat.deform((F(1, 4), F(1, 4), F(1, 4))) == (F(1, 4), F(1, 4), F(283, 1024))
    # Below the center the lattice is stretched along z: det J = 9/8 at (1/2, 1/2, 1/4).
    assert det3(lat.jacobian((F(1, 2), F(1, 2), F(1, 4)))) == F(9, 8)
    # The corner points of the lattice do not move.
    assert lat.deform((0, 0, 0)) == (0, 0, 0)
    assert lat.deform((1, 1, 1)) == (1, 1, 1)


def test_point_outside_does_not_move():
    lat = unit_lattice()
    lat.points[1][1][1] = (F(1, 2), F(1, 2), F(3))
    for x in ((F(-1, 10), F(1, 2), F(1, 2)), (2, 0, 0), (F(1, 2), F(1, 2), F(11, 10))):
        assert lat.deform(x) == x


def test_jacobian_matches_finite_differences():
    rng = random.Random(5)
    lat = skew_lattice(2, 3, 2)
    lat.points = [[[tuple(float(v) + rng.uniform(-0.3, 0.3) for v in p) for p in row] for row in plane] for plane in lat.points]
    h = 1e-6
    for _ in range(5):
        x = tuple(float(v) for v in rand_point_inside(lat, rng))
        s, t, u = lat.local(x)
        if not all(0.01 < c < 0.99 for c in (s, t, u)):
            continue
        j = lat.jacobian(x)
        for c in range(3):
            xp = list(x)
            xm = list(x)
            xp[c] += h
            xm[c] -= h
            fp, fm = lat.deform(xp), lat.deform(xm)
            for r in range(3):
                assert abs((fp[r] - fm[r]) / (2 * h) - j[r][c]) < 1e-6


def test_rest_jacobian_is_identity_and_affine_det_is_volume_ratio():
    lat = skew_lattice(2, 2, 2)
    x = rand_point_inside(lat, random.Random(6))
    j = lat.jacobian(x)
    assert j == [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    scale = (2, 3, F(1, 2))
    lat.points = [[[tuple(scale[d] * p[d] for d in range(3)) for p in row] for row in plane] for plane in lat.points]
    assert det3(lat.jacobian(x)) == 3
