# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dihedral-angle/. The authors are listed in prov/M9M4MB.jsonl.

import random
from math import acos, cos, degrees, isclose, radians, sin, sqrt

from dihedral_angle import (bond_angle, backbone_dihedrals, build_backbone, cross, dihedral, dot, norm,
                            place, sub)


def angle_diff(a, b):
    d = (a - b) % 360.0
    return min(d, 360.0 - d)


def known(theta):
    """Four points whose dihedral is theta by construction."""
    t = radians(theta)
    return (0.0, 1.0, 0.0), (0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (1.0, cos(t), sin(t))


def projection_dihedral(p0, p1, p2, p3):
    """Second method: project b1 and b3 onto the plane normal to b2, then acos and a sign."""
    b2 = sub(p2, p1)
    u = sub(p0, p1)
    v = sub(p3, p2)
    k = dot(b2, b2)
    up = sub(u, tuple(c * dot(u, b2) / k for c in b2))
    vp = sub(v, tuple(c * dot(v, b2) / k for c in b2))
    c = max(-1.0, min(1.0, dot(up, vp) / (norm(up) * norm(vp))))
    ang = degrees(acos(c))
    return ang if dot(cross(up, vp), b2) >= 0 else -ang


def random_rotation(rng):
    q = [rng.gauss(0, 1) for _ in range(4)]
    s = sqrt(sum(x * x for x in q))
    w, x, y, z = (c / s for c in q)
    return [[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
            [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
            [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]]


def move(p, R, t):
    return tuple(sum(R[i][j] * p[j] for j in range(3)) + t[i] for i in range(3))


def test_example() -> None:
    assert isclose(dihedral(*known(60.0)), 60.0)
    assert isclose(dihedral(*known(-60.0)), -60.0)
    assert dihedral(*known(180.0)) == 180.0
    assert abs(dihedral(*known(0.0))) < 1e-12


def test_known_angles_under_rigid_motions() -> None:
    rng = random.Random(1963)
    for _ in range(300):
        theta = rng.uniform(-179.9, 180.0)
        R = random_rotation(rng)
        t = [rng.uniform(-5, 5) for _ in range(3)]
        s = rng.uniform(0.2, 3.0)
        pts = [move(tuple(s * c for c in p), R, t) for p in known(theta)]
        assert angle_diff(dihedral(*pts), theta) < 1e-7
        # A mirror image flips the sign.
        mirror = [(-p[0], p[1], p[2]) for p in pts]
        assert angle_diff(dihedral(*mirror), -theta) < 1e-7
        # Reversing the order of the four points keeps the angle.
        assert angle_diff(dihedral(*pts[::-1]), theta) < 1e-7


def test_against_projection_method() -> None:
    rng = random.Random(4)
    for _ in range(300):
        pts = [tuple(rng.uniform(-3, 3) for _ in range(3)) for _ in range(4)]
        assert angle_diff(dihedral(*pts), projection_dihedral(*pts)) < 1e-6


def test_place_builds_the_requested_geometry() -> None:
    rng = random.Random(9)
    for _ in range(200):
        a, b, c = [tuple(rng.uniform(-3, 3) for _ in range(3)) for _ in range(3)]
        L, ang, tor = rng.uniform(1, 2), rng.uniform(60, 170), rng.uniform(-180, 180)
        d = place(a, b, c, L, ang, tor)
        assert isclose(norm(sub(d, c)), L, abs_tol=1e-9)
        assert isclose(bond_angle(b, c, d), ang, abs_tol=1e-6)
        assert angle_diff(dihedral(a, b, c, d), tor) < 1e-6


def test_backbone_round_trip() -> None:
    rng = random.Random(1)
    n = 8
    phi = [rng.uniform(-180, 180) for _ in range(n)]
    psi = [rng.uniform(-180, 180) for _ in range(n)]
    omega = [rng.choice([180.0, 0.0, rng.uniform(170, 190)]) for _ in range(n)]
    got = backbone_dihedrals(build_backbone(phi, psi, omega))
    for i, (f, p, o) in enumerate(got):
        if i > 0:
            assert angle_diff(f, phi[i]) < 1e-6
        if i + 1 < n:
            assert angle_diff(p, psi[i]) < 1e-6 and angle_diff(o, omega[i]) < 1e-6
    assert got[0][0] is None and got[-1][1] is None


def test_alpha_helix_ca_spacing() -> None:
    atoms = build_backbone([-57.0] * 12, [-47.0] * 12, [180.0] * 12)
    ca = [atoms[3 * i + 1] for i in range(12)]
    # Neighbouring CA atoms of a trans peptide are about 3.8 angstroms apart.
    for i in range(11):
        assert 3.7 < norm(sub(ca[i + 1], ca[i])) < 3.9
