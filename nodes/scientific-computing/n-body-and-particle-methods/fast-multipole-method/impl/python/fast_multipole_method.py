# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-multipole-method/. The authors are listed in prov/2RM7MC.jsonl.
"""Fast multipole method of Greengard and Rokhlin for the 2D logarithmic kernel.

Charges q[i] sit at points z[i] (complex numbers) in the unit square
[0, 1) x [0, 1). The potential at charge j is

    u_j = sum over i != j of q_i log|z_j - z_i|,

the real part of the complex potential phi(z) = sum_i q_i log(z - z_i).
The field grad u is returned as the complex number conj(phi'(z)).

The tree is uniform: level l has 4^l boxes of side 2^-l, and the leaves are
at level L. Each box keeps p + 1 coefficients. The translation formulas are
those of Beatson and Greengard, "A short course on fast multipole methods",
Lemma 4.2 (P2M), Lemma 4.6 (M2M), Lemma 4.7 (M2L) and Lemma 4.8 (L2L).
"""

import cmath
import math
from math import comb
from typing import Optional, Sequence


def binomials(p: int) -> list[list[int]]:
    """Table C[n][k] = n choose k for 0 <= n, k <= 2p."""
    return [[comb(n, k) for k in range(2 * p + 1)] for n in range(2 * p + 1)]


def p2m(q: Sequence[float], z: Sequence[complex], center: complex, p: int) -> list[complex]:
    """Multipole coefficients about center: a_0 = sum q_i, a_k = -sum q_i (z_i - c)^k / k."""
    a = [0j] * (p + 1)
    for qi, zi in zip(q, z):
        d = zi - center
        a[0] += qi
        t = 1 + 0j
        for k in range(1, p + 1):
            t *= d
            a[k] -= qi * t / k
    return a


def eval_multipole(a: Sequence[complex], center: complex, w: complex) -> complex:
    """phi(w) = a_0 log(w - c) + sum_k a_k / (w - c)^k."""
    d = w - center
    s = 0j
    for k in range(len(a) - 1, 0, -1):
        s = (s + a[k]) / d
    return a[0] * cmath.log(d) + s


def m2m(a: Sequence[complex], z0: complex, C: list[list[int]]) -> list[complex]:
    """Shift a multipole expansion centered at z0 to the origin (Lemma 4.6).

    b_0 = a_0 and b_l = -a_0 z0^l / l + sum_{k=1}^{l} a_k z0^(l-k) C(l-1, k-1).
    The p + 1 new coefficients use only a_0, ..., a_p, so the shift is exact.
    """
    p = len(a) - 1
    pw = [1 + 0j] * (p + 1)
    for k in range(1, p + 1):
        pw[k] = pw[k - 1] * z0
    b = [0j] * (p + 1)
    b[0] = a[0]
    for l in range(1, p + 1):
        s = -a[0] * pw[l] / l
        for k in range(1, l + 1):
            s += a[k] * pw[l - k] * C[l - 1][k - 1]
        b[l] = s
    return b


def m2l(a: Sequence[complex], z0: complex, C: list[list[int]]) -> list[complex]:
    """Convert a multipole expansion centered at z0 into a local expansion about the origin (Lemma 4.7).

    b_0 = a_0 log(-z0) + sum_k (-1)^k a_k / z0^k and, for l >= 1,
    b_l = -a_0 / (l z0^l) + z0^(-l) sum_k (-1)^k a_k z0^(-k) C(l+k-1, k-1).
    """
    p = len(a) - 1
    inv = 1 / z0
    ip = [1 + 0j] * (p + 1)
    for k in range(1, p + 1):
        ip[k] = ip[k - 1] * inv
    t = [((-1) ** k) * a[k] * ip[k] for k in range(p + 1)]
    b = [0j] * (p + 1)
    b[0] = a[0] * cmath.log(-z0) + sum(t[1:])
    for l in range(1, p + 1):
        s = -a[0] / l
        for k in range(1, p + 1):
            s += t[k] * C[l + k - 1][k - 1]
        b[l] = s * ip[l]
    return b


def l2l(b: Sequence[complex], z0: complex) -> list[complex]:
    """Shift a local expansion sum_k b_k (w - z0)^k to the origin by Horner's scheme (Lemma 4.8). Exact."""
    a = list(b)
    p = len(a) - 1
    for j in range(p):
        for k in range(p - j - 1, p):
            a[k] -= z0 * a[k + 1]
    return a


def eval_local(b: Sequence[complex], center: complex, w: complex) -> tuple[complex, complex]:
    """Value and derivative of sum_l b_l (w - c)^l."""
    d = w - center
    v = 0j
    dv = 0j
    for k in range(len(b) - 1, -1, -1):
        dv = dv * d + v
        v = v * d + b[k]
    return v, dv


def box_center(ix: int, iy: int, level: int) -> complex:
    h = 1.0 / (1 << level)
    return complex((ix + 0.5) * h, (iy + 0.5) * h)


def interaction_list(ix: int, iy: int, level: int) -> list[tuple[int, int]]:
    """Children of the near neighbours of the parent that are not near neighbours of the box."""
    m = 1 << level
    px, py = ix // 2, iy // 2
    out = []
    for nx in range(2 * (px - 1), 2 * (px + 2)):
        for ny in range(2 * (py - 1), 2 * (py + 2)):
            if 0 <= nx < m and 0 <= ny < m and max(abs(nx - ix), abs(ny - iy)) > 1:
                out.append((nx, ny))
    return out


def _add(acc: list[complex], b: Sequence[complex]) -> None:
    for k in range(len(acc)):
        acc[k] += b[k]


def fmm(q: Sequence[float], z: Sequence[complex], p: int = 12, levels: Optional[int] = None, s: int = 8):
    """Potentials u_j and fields grad u_j (as complex numbers) of all charges.

    levels is the leaf level L (at least 2); by default L is chosen so that a
    leaf holds at most about s charges on average. Returns (u, field, stats),
    where stats counts the ordered pairs of the near field ("p2p") and the
    multipole-to-local translations ("m2l").
    """
    n = len(z)
    if levels is None:
        levels = max(2, math.ceil(math.log(n / s, 4))) if n > s else 2
    L = levels
    C = binomials(p)
    m = 1 << L
    leaf: dict[tuple[int, int], list[int]] = {}
    for i, zi in enumerate(z):
        key = (min(int(zi.real * m), m - 1), min(int(zi.imag * m), m - 1))
        leaf.setdefault(key, []).append(i)
    mult: list[dict] = [dict() for _ in range(L + 1)]
    for key, idx in leaf.items():  # @line L1
        mult[L][key] = p2m([q[i] for i in idx], [z[i] for i in idx], box_center(*key, L), p)
    for l in range(L - 1, 1, -1):  # @line L2
        for (cx, cy), a in mult[l + 1].items():
            key = (cx // 2, cy // 2)
            z0 = box_center(cx, cy, l + 1) - box_center(*key, l)
            _add(mult[l].setdefault(key, [0j] * (p + 1)), m2m(a, z0, C))
    local: list[dict] = [dict() for _ in range(L + 1)]
    n_m2l = 0
    for l in range(2, L + 1):
        for key, a in mult[l].items():  # @line L3
            for tgt in interaction_list(*key, l):
                if l == L and tgt not in leaf:
                    continue
                z0 = box_center(*key, l) - box_center(*tgt, l)
                _add(local[l].setdefault(tgt, [0j] * (p + 1)), m2l(a, z0, C))
                n_m2l += 1
        if l < L:
            for (px, py), b in local[l].items():  # @line L4
                for cx in (2 * px, 2 * px + 1):
                    for cy in (2 * py, 2 * py + 1):
                        z0 = box_center(px, py, l) - box_center(cx, cy, l + 1)
                        _add(local[l + 1].setdefault((cx, cy), [0j] * (p + 1)), l2l(b, z0))
    u = [0.0] * n
    field = [0j] * n
    n_p2p = 0
    for key, idx in leaf.items():
        b = local[L].get(key)
        c = box_center(*key, L)
        if b is not None:
            for j in idx:  # @line L5
                v, dv = eval_local(b, c, z[j])
                u[j] += v.real
                field[j] += dv.conjugate()
        ix, iy = key
        for nx in range(ix - 1, ix + 2):  # @line L6
            for ny in range(iy - 1, iy + 2):
                for i in leaf.get((nx, ny), ()):
                    for j in idx:
                        if i != j:
                            d = z[j] - z[i]
                            u[j] += q[i] * math.log(abs(d))
                            field[j] += q[i] / d.conjugate()
                            n_p2p += 1
    return u, field, {"p2p": n_p2p, "m2l": n_m2l}  # @line L7


def direct(q: Sequence[float], z: Sequence[complex]):
    """Direct summation over all ordered pairs: the reference."""
    n = len(z)
    u = [0.0] * n
    field = [0j] * n
    for j in range(n):
        for i in range(n):
            if i != j:
                d = z[j] - z[i]
                u[j] += q[i] * math.log(abs(d))
                field[j] += q[i] / d.conjugate()
    return u, field
