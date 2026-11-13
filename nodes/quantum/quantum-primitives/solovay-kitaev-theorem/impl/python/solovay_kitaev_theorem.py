# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/solovay-kitaev-theorem/. The authors are listed in prov/ZW8FD1.jsonl.
"""The Solovay-Kitaev algorithm for one qubit, in the form of Dawson and Nielsen.

Gates are taken modulo global phase. A one-qubit unitary of determinant 1 is
U = a I - i (b X + c Y + d Z) with a^2 + b^2 + c^2 + d^2 = 1, stored as the unit quaternion
(a, b, c, d); then -iX, -iY, -iZ multiply like the quaternion units i, j, k. U and -U are the
same gate. The distance used is the phase-invariant operator-norm distance
    d(U, V) = min over phi of ||U - e^(i phi) V|| = sqrt(2 - |tr(U^dagger V)|) = sqrt(2 - 2 |<U, V>|),
where <U, V> is the dot product of the quaternions.

The base set is {H, T, T^dagger}. A word is a list of gate names in matrix-product order: the
word [g1, g2, g3] is the matrix g1 g2 g3, so g3 acts first.
"""

import math

Quat = tuple[float, float, float, float]

R2 = 1 / math.sqrt(2)
C8, S8 = math.cos(math.pi / 8), math.sin(math.pi / 8)
# i H = -i (-(X + Z)/sqrt 2) has determinant 1; e^(-i pi/8) T = cos(pi/8) I - i sin(pi/8) Z
GATES: dict[str, Quat] = {"H": (0.0, -R2, 0.0, -R2), "T": (C8, 0.0, 0.0, S8), "Tdg": (C8, 0.0, 0.0, -S8)}
INVERSE = {"H": "H", "T": "Tdg", "Tdg": "T"}


def qmul(p: Quat, q: Quat) -> Quat:
    a1, b1, c1, d1 = p
    a2, b2, c2, d2 = q
    return (a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2,
            a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2,
            a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2,
            a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2)


def qconj(p: Quat) -> Quat:
    """The inverse U^dagger of a unit quaternion."""
    return (p[0], -p[1], -p[2], -p[3])


def dist(p: Quat, q: Quat) -> float:
    dot = abs(p[0] * q[0] + p[1] * q[1] + p[2] * q[2] + p[3] * q[3])
    return math.sqrt(max(0.0, 2 - 2 * min(1.0, dot)))


def word_quat(word: list[str]) -> Quat:
    out: Quat = (1.0, 0.0, 0.0, 0.0)
    for g in word:
        out = qmul(out, GATES[g])
    return out


def inverse_word(word: list[str]) -> list[str]:
    return [INVERSE[g] for g in reversed(word)]


def _key(p: Quat) -> tuple:
    if next(v for v in p if abs(v) > 1e-9) < 0:
        p = (-p[0], -p[1], -p[2], -p[3])  # U and -U are the same gate
    return tuple(round(v, 7) for v in p)


def build_net(max_len: int) -> list[tuple[Quat, list[str]]]:
    """All distinct gates (modulo sign) that are words of length <= max_len over {H, T, T^dagger},
    each with a shortest word, by breadth-first search."""
    start: Quat = (1.0, 0.0, 0.0, 0.0)
    seen = {_key(start)}
    net = [(start, [])]
    frontier = [(start, [])]
    for _ in range(max_len):
        nxt = []
        for p, w in frontier:
            for g, q in GATES.items():
                if w and INVERSE[g] == w[-1]:
                    continue  # g cancels the last gate
                r = qmul(p, q)
                k = _key(r)
                if k not in seen:
                    seen.add(k)
                    nxt.append((r, w + [g]))
        net += nxt
        frontier = nxt
    return net


def basic_approximation(u: Quat, net: list[tuple[Quat, list[str]]]) -> tuple[Quat, list[str]]:
    """The nearest net element, by a linear scan."""
    a, b, c, d = u
    best = max(net, key=lambda e: abs(a * e[0][0] + b * e[0][1] + c * e[0][2] + d * e[0][3]))
    return best


def axis_angle(u: Quat) -> tuple[tuple[float, float, float], float]:
    """U = R_n(theta) = cos(theta/2) I - i sin(theta/2) n.sigma with theta in [0, pi] (U up to sign)."""
    a, b, c, d = u
    if a < 0:
        a, b, c, d = -a, -b, -c, -d
    s = math.sqrt(b * b + c * c + d * d)
    theta = 2 * math.atan2(s, a)
    if s < 1e-15:
        return (0.0, 0.0, 1.0), 0.0
    return (b / s, c / s, d / s), theta


def rotation(n: tuple[float, float, float], theta: float) -> Quat:
    s = math.sin(theta / 2)
    return (math.cos(theta / 2), s * n[0], s * n[1], s * n[2])


def group_commutator(u: Quat) -> tuple[Quat, Quat]:
    """Balanced V, W with V W V^dagger W^dagger = U (Dawson and Nielsen). Both are rotations by
    phi with sin(theta/2) = 2 sin^2(phi/2) sqrt(1 - sin^4(phi/2)), so phi is about sqrt(theta)."""
    n, theta = axis_angle(u)
    s = math.sqrt((1 - math.cos(theta / 2)) / 2)  # s = sin^2(phi/2)
    phi = 2 * math.asin(math.sqrt(s))
    v0 = rotation((1.0, 0.0, 0.0), phi)
    w0 = rotation((0.0, 1.0, 0.0), phi)
    c0 = qmul(qmul(v0, w0), qmul(qconj(v0), qconj(w0)))
    m, _ = axis_angle(c0)
    # a rotation S that maps the axis m of the commutator onto n
    cross = (m[1] * n[2] - m[2] * n[1], m[2] * n[0] - m[0] * n[2], m[0] * n[1] - m[1] * n[0])
    cn = math.sqrt(sum(x * x for x in cross))
    dot = max(-1.0, min(1.0, sum(x * y for x, y in zip(m, n))))
    if cn < 1e-15:
        sq: Quat = (1.0, 0.0, 0.0, 0.0) if dot > 0 else rotation((0.0, 0.0, 1.0), math.pi)
    else:
        sq = rotation((cross[0] / cn, cross[1] / cn, cross[2] / cn), math.acos(dot))
    v = qmul(qmul(sq, v0), qconj(sq))
    w = qmul(qmul(sq, w0), qconj(sq))
    return v, w


def solovay_kitaev(u: Quat, depth: int, net: list[tuple[Quat, list[str]]]) -> tuple[Quat, list[str]]:
    """An approximation of U as a word over {H, T, T^dagger}. Returns (the exact product of the word, the word).

    Depth 0 is the net lookup. Depth k makes 3 calls of depth k - 1, and the word length grows by
    a factor of 5 per level: U_k = V W V^dagger W^dagger U_(k-1).
    """
    if depth == 0:
        return basic_approximation(u, net)
    prev, w_prev = solovay_kitaev(u, depth - 1, net)
    delta = qmul(u, qconj(prev))
    v, w = group_commutator(delta)
    vq, wv = solovay_kitaev(v, depth - 1, net)
    wq, ww = solovay_kitaev(w, depth - 1, net)
    word = wv + ww + inverse_word(wv) + inverse_word(ww) + w_prev
    approx = qmul(qmul(qmul(vq, wq), qmul(qconj(vq), qconj(wq))), prev)
    return approx, word


def random_su2(rng) -> Quat:
    """A Haar-random element of SU(2): a uniform point on the 3-sphere."""
    v = [rng.gauss(0, 1) for _ in range(4)]
    s = math.sqrt(sum(x * x for x in v))
    return (v[0] / s, v[1] / s, v[2] / s, v[3] / s)


def to_matrix(u: Quat) -> list[list[complex]]:
    a, b, c, d = u
    return [[complex(a, -d), complex(-c, -b)], [complex(c, -b), complex(a, d)]]
