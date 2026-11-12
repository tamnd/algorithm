# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dihedral-angle/. The authors are listed in prov/M9M4MB.jsonl.

"""Dihedral angles from four points, and backbone building from angles.

Angles are in degrees, in the range (-180, 180]. The sign follows the
IUPAC convention: looking along the bond p1 -> p2, the angle is positive
when the bond p0-p1 must turn clockwise to cover the bond p2-p3.
"""

from math import acos, atan2, cos, degrees, radians, sin, sqrt


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def scale(a, s):
    return (a[0] * s, a[1] * s, a[2] * s)


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def norm(a):
    return sqrt(dot(a, a))


def unit(a):
    return scale(a, 1.0 / norm(a))


def dihedral(p0, p1, p2, p3) -> float:
    """Return the dihedral angle p0-p1-p2-p3 in degrees.

    With b1 = p1 - p0, b2 = p2 - p1 and b3 = p3 - p2, the angle is
    atan2(|b2| b1 . (b2 x b3), (b1 x b2) . (b2 x b3)).
    Precondition: neither p0, p1, p2 nor p1, p2, p3 lie on one line.
    """
    b1, b2, b3 = sub(p1, p0), sub(p2, p1), sub(p3, p2)
    n1, n2 = cross(b1, b2), cross(b2, b3)
    y = norm(b2) * dot(b1, n2)
    x = dot(n1, n2)
    if x == 0 and y == 0:
        raise ValueError("three of the points lie on one line")
    ang = degrees(atan2(y, x))
    return 180.0 if ang == -180.0 else ang


def bond_angle(a, b, c) -> float:
    """Return the angle a-b-c in degrees."""
    u, v = sub(a, b), sub(c, b)
    t = dot(u, v) / (norm(u) * norm(v))
    return degrees(acos(max(-1.0, min(1.0, t))))


def place(a, b, c, length: float, angle: float, torsion: float):
    """Return d with |cd| = length, angle b-c-d = angle and dihedral a-b-c-d = torsion.

    This is the natural extension reference frame construction.
    """
    bc = unit(sub(c, b))
    n = unit(cross(sub(b, a), bc))
    m = cross(n, bc)
    th, ph = radians(angle), radians(torsion)
    # d - c in the frame (bc, m, n).
    dx = -length * cos(th)
    dy = length * sin(th) * cos(ph)
    dz = length * sin(th) * sin(ph)
    return add(c, add(scale(bc, dx), add(scale(m, dy), scale(n, dz))))


# Approximate ideal backbone geometry (lengths in angstroms, angles in degrees).
N_CA, CA_C, C_N = 1.458, 1.525, 1.329
ANG_N_CA_C, ANG_CA_C_N, ANG_C_N_CA = 111.2, 116.2, 121.7


def build_backbone(phi: list, psi: list, omega: list) -> list:
    """Return the atoms N, CA, C of each residue as a flat list.

    Residue i gets phi[i] and psi[i]; omega[i] is the peptide bond between
    residue i and residue i + 1. phi[0] and the last psi and omega have no
    effect on the atoms that are built.
    """
    n = len(phi)
    atoms = [(0.0, 0.0, 0.0), (N_CA, 0.0, 0.0)]
    t = radians(180.0 - ANG_N_CA_C)
    atoms.append((N_CA + CA_C * cos(t), CA_C * sin(t), 0.0))
    for i in range(n - 1):
        N0, CA0, C0 = atoms[3 * i], atoms[3 * i + 1], atoms[3 * i + 2]
        N1 = place(N0, CA0, C0, C_N, ANG_CA_C_N, psi[i])
        CA1 = place(CA0, C0, N1, N_CA, ANG_C_N_CA, omega[i])
        C1 = place(C0, N1, CA1, CA_C, ANG_N_CA_C, phi[i + 1])
        atoms.extend([N1, CA1, C1])
    return atoms


def backbone_dihedrals(atoms: list) -> list:
    """Return (phi, psi, omega) for each residue; None where an atom is missing.

    phi(i) = C(i-1) N(i) CA(i) C(i), psi(i) = N(i) CA(i) C(i) N(i+1),
    omega(i) = CA(i) C(i) N(i+1) CA(i+1).
    """
    n = len(atoms) // 3
    out = []
    for i in range(n):
        N, CA, C = atoms[3 * i], atoms[3 * i + 1], atoms[3 * i + 2]
        phi = dihedral(atoms[3 * i - 1], N, CA, C) if i > 0 else None
        psi = dihedral(N, CA, C, atoms[3 * i + 3]) if i + 1 < n else None
        omg = dihedral(CA, C, atoms[3 * i + 3], atoms[3 * i + 4]) if i + 1 < n else None
        out.append((phi, psi, omg))
    return out
