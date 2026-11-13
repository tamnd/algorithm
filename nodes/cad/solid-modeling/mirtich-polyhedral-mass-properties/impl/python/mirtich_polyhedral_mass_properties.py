# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mirtich-polyhedral-mass-properties/. The authors are listed in prov/JVZRYG.jsonl.

"""Mirtich's exact volume, centroid and inertia tensor of a polyhedron.

A polyhedron is a list of faces. Each face is a list of at least three
vertices (x, y, z) that lie in one plane, in counterclockwise order when the
face is seen from outside the solid (the outward normal follows the
right-hand rule). The faces must form a closed surface. With int or Fraction
coordinates every result is an exact Fraction.
"""

from fractions import Fraction
from typing import NamedTuple, Sequence

Num = int | Fraction
Point = tuple[Num, Num, Num]


class VolumeIntegrals(NamedTuple):
    t0: Fraction                                  # integral of 1 (the volume)
    t1: tuple[Fraction, Fraction, Fraction]       # integrals of x, y, z
    t2: tuple[Fraction, Fraction, Fraction]       # integrals of x^2, y^2, z^2
    tp: tuple[Fraction, Fraction, Fraction]       # integrals of xy, yz, zx


def _sub(p: Point, q: Point) -> tuple[Num, Num, Num]:
    return (p[0] - q[0], p[1] - q[1], p[2] - q[2])


def _cross(u: Sequence[Num], v: Sequence[Num]) -> tuple[Num, Num, Num]:
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


def face_normal(face: Sequence[Point]) -> tuple[Num, Num, Num]:
    """Newell's normal: exact, outward, of length twice the face area for a planar face."""
    nx = ny = nz = 0
    k = len(face)
    for i in range(k):
        p, q = face[i], face[(i + 1) % k]
        nx += (p[1] - q[1]) * (p[2] + q[2])
        ny += (p[2] - q[2]) * (p[0] + q[0])
        nz += (p[0] - q[0]) * (p[1] + q[1])
    return (nx, ny, nz)


def projection_integrals(face: Sequence[Point], a: int, b: int) -> dict[str, Fraction]:
    """Integrals over the projection of the face to the (a, b) plane, by Green's theorem.

    Returns P1, Pa, Pb, Paa, Pab, Pbb, Paaa, Paab, Pabb, Pbbb: the integrals of
    1, alpha, beta, alpha^2, ... over the projected region, signed by the
    orientation of the projected boundary.
    """
    p1 = pa = pb = paa = pab = pbb = paaa = paab = pabb = pbbb = Fraction(0)
    k = len(face)
    for i in range(k):
        a0, b0 = face[i][a], face[i][b]
        a1, b1 = face[(i + 1) % k][a], face[(i + 1) % k][b]
        da, db = a1 - a0, b1 - b0
        a0_2, a1_2, b0_2, b1_2 = a0 * a0, a1 * a1, b0 * b0, b1 * b1
        a0_3, a1_3, b0_3, b1_3 = a0_2 * a0, a1_2 * a1, b0_2 * b0, b1_2 * b1
        c1 = a1 + a0
        ca = a1 * c1 + a0_2
        caa = a1 * ca + a0_3
        caaa = a1 * caa + a0_3 * a0
        cb = b1 * (b1 + b0) + b0_2
        cbb = b1 * cb + b0_3
        cbbb = b1 * cbb + b0_3 * b0
        cab = 3 * a1_2 + 2 * a1 * a0 + a0_2
        kab = a1_2 + 2 * a1 * a0 + 3 * a0_2
        caab = a0 * cab + 4 * a1_3
        kaab = a1 * kab + 4 * a0_3
        cabb = 4 * b1_3 + 3 * b1_2 * b0 + 2 * b1 * b0_2 + b0_3
        kabb = b1_3 + 2 * b1_2 * b0 + 3 * b1 * b0_2 + 4 * b0_3
        p1 += db * c1
        pa += db * ca
        paa += db * caa
        paaa += db * caaa
        pb += da * cb
        pbb += da * cbb
        pbbb += da * cbbb
        pab += db * (b1 * cab + b0 * kab)
        paab += db * (b1 * caab + b0 * kaab)
        pabb += da * (a1 * cabb + a0 * kabb)
    return {
        "P1": p1 / 2, "Pa": pa / 6, "Paa": paa / 12, "Paaa": paaa / 20,
        "Pb": pb / -6, "Pbb": pbb / -12, "Pbbb": pbbb / -20,
        "Pab": pab / 24, "Paab": paab / 60, "Pabb": pabb / -60,
    }


def volume_integrals(faces: Sequence[Sequence[Point]]) -> VolumeIntegrals:
    """Exact T0, T1, T2 and TP of a closed, outward oriented polyhedral surface.

    Cost: Theta(total number of face vertices) arithmetic operations.
    """
    t0 = Fraction(0)  # @line L1
    t1 = [Fraction(0)] * 3
    t2 = [Fraction(0)] * 3
    tp = [Fraction(0)] * 3
    for face in faces:  # @line L2
        n = face_normal(face)  # @line L3
        w = -(n[0] * face[0][0] + n[1] * face[0][1] + n[2] * face[0][2])
        c = max(range(3), key=lambda i: abs(n[i]))  # @line L4
        a, b = (c + 1) % 3, (c + 2) % 3
        if n[c] == 0:
            raise ValueError("a face has a zero normal")
        P = projection_integrals(face, a, b)  # @line L5
        na, nb, nc = n[a], n[b], n[c]
        k1 = Fraction(1) / nc  # @line L6
        k2, k3, k4 = k1 * k1, k1 * k1 * k1, k1 * k1 * k1 * k1
        fa = k1 * P["Pa"]
        fb = k1 * P["Pb"]
        fc = -k2 * (na * P["Pa"] + nb * P["Pb"] + w * P["P1"])
        faa = k1 * P["Paa"]
        fbb = k1 * P["Pbb"]
        fcc = k3 * (na * na * P["Paa"] + 2 * na * nb * P["Pab"] + nb * nb * P["Pbb"]
                    + w * (2 * (na * P["Pa"] + nb * P["Pb"]) + w * P["P1"]))
        faaa = k1 * P["Paaa"]
        fbbb = k1 * P["Pbbb"]
        fccc = -k4 * (na ** 3 * P["Paaa"] + 3 * na * na * nb * P["Paab"]
                      + 3 * na * nb * nb * P["Pabb"] + nb ** 3 * P["Pbbb"]
                      + 3 * w * (na * na * P["Paa"] + 2 * na * nb * P["Pab"] + nb * nb * P["Pbb"])
                      + w * w * (3 * (na * P["Pa"] + nb * P["Pb"]) + w * P["P1"]))
        faab = k1 * P["Paab"]
        fbbc = -k2 * (na * P["Pabb"] + nb * P["Pbbb"] + w * P["Pbb"])
        fcca = k3 * (na * na * P["Paaa"] + 2 * na * nb * P["Paab"] + nb * nb * P["Pabb"]
                     + w * (2 * (na * P["Paa"] + nb * P["Pab"]) + w * P["Pa"]))
        t0 += n[0] * (fa if a == 0 else fb if b == 0 else fc)  # @line L7
        t1[a] += na * faa
        t1[b] += nb * fbb
        t1[c] += nc * fcc
        t2[a] += na * faaa
        t2[b] += nb * fbbb
        t2[c] += nc * fccc
        tp[a] += na * faab
        tp[b] += nb * fbbc
        tp[c] += nc * fcca
    return VolumeIntegrals(  # @line L8
        t0,
        (t1[0] / 2, t1[1] / 2, t1[2] / 2),
        (t2[0] / 3, t2[1] / 3, t2[2] / 3),
        (tp[0] / 2, tp[1] / 2, tp[2] / 2),
    )


class MassProperties(NamedTuple):
    mass: Fraction
    center: tuple[Fraction, Fraction, Fraction]
    inertia: tuple[tuple[Fraction, Fraction, Fraction], ...]  # about the center of mass


def mass_properties(faces: Sequence[Sequence[Point]], density: Num = 1) -> MassProperties:
    """Mass, center of mass and inertia tensor about the center of mass, for a uniform density."""
    T = volume_integrals(faces)
    if T.t0 == 0:
        raise ValueError("the volume is zero")
    m = density * T.t0  # @line L9
    r = tuple(x / T.t0 for x in T.t1)
    ixx = density * (T.t2[1] + T.t2[2]) - m * (r[1] ** 2 + r[2] ** 2)
    iyy = density * (T.t2[2] + T.t2[0]) - m * (r[2] ** 2 + r[0] ** 2)
    izz = density * (T.t2[0] + T.t2[1]) - m * (r[0] ** 2 + r[1] ** 2)
    ixy = -(density * T.tp[0] - m * r[0] * r[1])
    iyz = -(density * T.tp[1] - m * r[1] * r[2])
    izx = -(density * T.tp[2] - m * r[2] * r[0])
    inertia = ((ixx, ixy, izx), (ixy, iyy, iyz), (izx, iyz, izz))
    return MassProperties(Fraction(m), (r[0], r[1], r[2]), inertia)
