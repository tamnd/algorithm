# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/loop-modeling/. The authors are listed in prov/BQJJ13.jsonl.

"""Loop closure by cyclic coordinate descent (CCD; Canutescu and Dunbrack 2003).

The backbone is the chain of atoms N, CA, C of each residue, with fixed bond
lengths and bond angles and a planar trans peptide bond (omega = 180 degrees).
Only the dihedral angles phi (about N-CA) and psi (about CA-C) of the loop
residues can change.

The loop starts at a fixed anchor residue. Its last residue is the moving
end: its three atoms N, CA, C must land on three target positions, which are
the atoms of the fixed residue on the other side of the gap. CCD visits the
rotatable bonds in turn. For each bond it rotates everything after the bond
by the angle that brings the moving atoms closest to their targets, which
has a closed form. Rotations about the bonds do not change any bond length
or bond angle, so the chain stays valid.
"""

import math
import random
from typing import List, Sequence, Tuple

Vec = Tuple[float, float, float]

# Ideal backbone geometry (angstrom and degrees), close to the Engh and Huber values.
B_N_CA, B_CA_C, B_C_N = 1.458, 1.525, 1.329
A_N_CA_C, A_CA_C_N, A_C_N_CA = 111.2, 116.2, 121.7
OMEGA = 180.0


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def scale(a, s):
    return (a[0] * s, a[1] * s, a[2] * s)


def dot(a, b) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def norm(a) -> float:
    return math.sqrt(dot(a, a))


def unit(a):
    return scale(a, 1.0 / norm(a))


def place(a: Vec, b: Vec, c: Vec, bond: float, angle_deg: float, torsion_deg: float) -> Vec:
    """The atom d with |cd| = bond, angle bcd = angle and dihedral abcd = torsion (NeRF)."""
    theta, tau = math.radians(angle_deg), math.radians(torsion_deg)
    bc = unit(sub(c, b))
    n = unit(cross(sub(b, a), bc))
    m = cross(n, bc)
    d2 = (-bond * math.cos(theta), bond * math.sin(theta) * math.cos(tau), bond * math.sin(theta) * math.sin(tau))
    return add(c, add(scale(bc, d2[0]), add(scale(m, d2[1]), scale(n, d2[2]))))


def dihedral(a: Vec, b: Vec, c: Vec, d: Vec) -> float:
    """The dihedral angle abcd in degrees, in (-180, 180]."""
    b1, b2, b3 = sub(b, a), sub(c, b), sub(d, c)
    n1, n2 = cross(b1, b2), cross(b2, b3)
    x = dot(n1, n2)
    y = dot(cross(n1, n2), unit(b2))
    return math.degrees(math.atan2(y, x))


def angle(a: Vec, b: Vec, c: Vec) -> float:
    u, v = sub(a, b), sub(c, b)
    return math.degrees(math.acos(max(-1.0, min(1.0, dot(u, v) / (norm(u) * norm(v))))))


def build_backbone(phis: Sequence[float], psis: Sequence[float]) -> List[Vec]:
    """Atoms N, CA, C of len(phis) residues, residue 0 in a fixed frame.

    phis[0] is not used, since the first N has no atom before it.
    """
    x: List[Vec] = [(0.0, 0.0, 0.0), (B_N_CA, 0.0, 0.0)]
    a = math.radians(180.0 - A_N_CA_C)
    x.append(add(x[1], (B_CA_C * math.cos(a), B_CA_C * math.sin(a), 0.0)))
    for k in range(1, len(phis)):
        n = place(x[-3], x[-2], x[-1], B_C_N, A_CA_C_N, psis[k - 1])
        ca = place(x[-2], x[-1], n, B_N_CA, A_C_N_CA, OMEGA)
        c = place(x[-1], n, ca, B_CA_C, A_N_CA_C, phis[k])
        x.extend([n, ca, c])
    return x


def rotate(p: Vec, origin: Vec, axis: Vec, theta: float) -> Vec:
    """Rotate p by theta radians about the line through origin with unit direction axis (Rodrigues)."""
    v = sub(p, origin)
    c, s = math.cos(theta), math.sin(theta)
    r = add(add(scale(v, c), scale(cross(axis, v), s)), scale(axis, dot(axis, v) * (1.0 - c)))
    return add(origin, r)


def ccd_angle(origin: Vec, axis: Vec, moving: Sequence[Vec], targets: Sequence[Vec]) -> float:
    """The rotation angle about the axis that minimizes the sum of |F_i - M_i|^2.

    With r_i the part of M_i - O at right angles to the axis and f_i = F_i - O,
    S(theta) = const - 2 (a cos theta + b sin theta), with a = sum f_i . r_i and
    b = sum f_i . (axis x r_i), so the best angle is atan2(b, a).
    """
    a = b = 0.0
    for m, f in zip(moving, targets):
        v = sub(m, origin)
        r = sub(v, scale(axis, dot(axis, v)))
        fv = sub(f, origin)
        a += dot(fv, r)
        b += dot(fv, cross(axis, r))
    return math.atan2(b, a)


def end_deviation(x: Sequence[Vec], targets: Sequence[Vec]) -> float:
    """RMS distance of the last three atoms from their targets."""
    m = x[-3:]
    return math.sqrt(sum(dot(sub(p, q), sub(p, q)) for p, q in zip(m, targets)) / 3.0)


def rotatable_bonds(n_res: int) -> List[Tuple[int, int]]:
    """Bonds (i, i + 1) about which the loop can turn: phi and psi of residues 1 .. n_res - 2.

    The first residue is the fixed anchor; the last residue is the moving end,
    which moves as one rigid block, so its own phi and psi do not count.
    """
    bonds = []
    for k in range(1, n_res - 1):
        bonds.append((3 * k, 3 * k + 1))      # phi: N_k - CA_k
        bonds.append((3 * k + 1, 3 * k + 2))  # psi: CA_k - C_k
    return bonds


def ccd_close(x: Sequence[Vec], targets: Sequence[Vec], tol: float = 0.01, max_sweeps: int = 5000,
              rng: random.Random = None):
    """Run CCD sweeps until the end deviation is at most tol. Returns (coordinates, sweeps, deviation).

    If rng is given, each sweep visits the bonds in a random order instead of from the anchor outward.
    """
    x = list(x)
    bonds = rotatable_bonds(len(x) // 3)
    sweeps = 0
    while end_deviation(x, targets) > tol and sweeps < max_sweeps:
        order = list(bonds)
        if rng is not None:
            rng.shuffle(order)
        for i, j in order:
            axis = unit(sub(x[j], x[i]))
            theta = ccd_angle(x[j], axis, x[-3:], targets)
            for t in range(j + 1, len(x)):
                x[t] = rotate(x[t], x[j], axis, theta)
        sweeps += 1
    return x, sweeps, end_deviation(x, targets)
