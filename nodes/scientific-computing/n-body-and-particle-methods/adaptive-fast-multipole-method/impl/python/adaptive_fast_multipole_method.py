# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adaptive-fast-multipole-method/. The authors are listed in prov/B4084E.jsonl.
"""Adaptive fast multipole method of Carrier, Greengard and Rokhlin for the 2D logarithmic kernel.

Charges q[i] sit at distinct points z[i] (complex numbers) of the unit square
[0, 1) x [0, 1). The potential at charge j is

    u_j = sum over i != j of q_i log|z_j - z_i|,

and the field grad u_j is returned as a complex number, conj(phi'(z_j)).

A box is split when it holds more than s charges, so the leaves are at many
levels. Empty boxes are dropped. A box is a key (level, ix, iy). Each leaf b
has four lists, with the names of Ying, Biros and Zorin:

    U(b)  the leaves adjacent to b, b included          (direct sum)
    V(b)  the children of the colleagues of the parent
          of b that are not adjacent to b (any box b)   (multipole to local)
    W(b)  the descendants of colleagues of b that are
          not adjacent to b but whose parent is         (multipole to target)
    X(b)  the boxes c with b in W(c)                    (source to local)

Colleagues are adjacent boxes of the same level. The expansions are the
complex Laurent and Taylor series of Beatson and Greengard, Section 4.
"""

import cmath
import math
from math import comb
from typing import Sequence

Box = tuple[int, int, int]


def binomials(p: int) -> list[list[int]]:
    """Table C[n][k] = n choose k for 0 <= n, k <= 2p."""
    return [[comb(n, k) for k in range(2 * p + 1)] for n in range(2 * p + 1)]


def box_center(b: Box) -> complex:
    l, ix, iy = b
    h = 1.0 / (1 << l)
    return complex((ix + 0.5) * h, (iy + 0.5) * h)


def adjacent(a: Box, b: Box) -> bool:
    """True if the closed squares of a and b share at least one point."""
    la, ax, ay = a
    lb, bx, by = b
    top = max(la, lb)
    sa = 1 << (top - la)
    sb = 1 << (top - lb)
    return (ax * sa <= (bx + 1) * sb and bx * sb <= (ax + 1) * sa
            and ay * sa <= (by + 1) * sb and by * sb <= (ay + 1) * sa)


def build_tree(z: Sequence[complex], s: int, max_level: int = 30):
    """Split every box with more than s charges. Returns (members, children)."""
    members: dict[Box, list[int]] = {(0, 0, 0): list(range(len(z)))}
    children: dict[Box, list[Box]] = {}
    stack = [(0, 0, 0)]
    while stack:
        b = stack.pop()
        l = b[0]
        idx = members[b]
        if len(idx) <= s or l >= max_level:
            children[b] = []
            continue
        m = 1 << (l + 1)
        parts: dict[Box, list[int]] = {}
        for i in idx:
            key = (l + 1, min(int(z[i].real * m), m - 1), min(int(z[i].imag * m), m - 1))
            parts.setdefault(key, []).append(i)
        children[b] = sorted(parts)
        for key, sub in parts.items():
            members[key] = sub
            stack.append(key)
    return members, children


def colleagues(b: Box, children: dict) -> list[Box]:
    """Boxes of the tree at the level of b that are adjacent to b, b included."""
    l, ix, iy = b
    return [(l, ix + dx, iy + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (l, ix + dx, iy + dy) in children]


def build_lists(children: dict):
    """The U, W lists of every leaf, the V list of every box and the X lists."""
    U: dict[Box, list[Box]] = {}
    V: dict[Box, list[Box]] = {}
    W: dict[Box, list[Box]] = {}
    X: dict[Box, list[Box]] = {b: [] for b in children}
    for b in children:
        l, ix, iy = b
        V[b] = []
        if l >= 2:
            for col in colleagues((l - 1, ix >> 1, iy >> 1), children):
                for ch in children[col]:
                    if max(abs(ch[1] - ix), abs(ch[2] - iy)) > 1:
                        V[b].append(ch)
    for b in children:
        if children[b]:
            continue
        l, ix, iy = b
        u = [b]
        w = []
        for k in range(l - 1, -1, -1):
            anc = (k, ix >> (l - k), iy >> (l - k))
            for col in colleagues(anc, children):
                if not children[col] and adjacent(col, b):
                    u.append(col)
        stack = [col for col in colleagues(b, children) if col != b]
        while stack:
            c = stack.pop()
            if not children[c]:
                u.append(c)
                continue
            for ch in children[c]:
                if adjacent(ch, b):
                    stack.append(ch)
                else:
                    w.append(ch)
        U[b] = u
        W[b] = w
        for d in w:
            X[d].append(b)
    return U, V, W, X


def p2m(q, z, idx, center: complex, p: int) -> list[complex]:
    """a_0 = sum q_i and a_k = -sum q_i (z_i - c)^k / k."""
    a = [0j] * (p + 1)
    for i in idx:
        d = z[i] - center
        a[0] += q[i]
        t = 1 + 0j
        for k in range(1, p + 1):
            t *= d
            a[k] -= q[i] * t / k
    return a


def m2m(a: Sequence[complex], z0: complex, C) -> list[complex]:
    """Shift a multipole expansion centered at z0 to the origin (exact)."""
    p = len(a) - 1
    pw = [1 + 0j] * (p + 1)
    for k in range(1, p + 1):
        pw[k] = pw[k - 1] * z0
    b = [a[0]] + [0j] * p
    for l in range(1, p + 1):
        s = -a[0] * pw[l] / l
        for k in range(1, l + 1):
            s += a[k] * pw[l - k] * C[l - 1][k - 1]
        b[l] = s
    return b


def m2l(a: Sequence[complex], z0: complex, C) -> list[complex]:
    """Local expansion about the origin of a multipole expansion centered at z0."""
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


def p2l(q, z, idx, center: complex, p: int) -> list[complex]:
    """Local expansion about center of far charges: b_0 = sum q log(c - z_i), b_l = -sum q / (l (z_i - c)^l)."""
    b = [0j] * (p + 1)
    for i in idx:
        d = z[i] - center
        b[0] += q[i] * cmath.log(-d)
        inv = 1 / d
        t = 1 + 0j
        for l in range(1, p + 1):
            t *= inv
            b[l] -= q[i] * t / l
    return b


def l2l(b: Sequence[complex], z0: complex) -> list[complex]:
    """Shift a local expansion sum_k b_k (w - z0)^k to the origin by Horner's scheme (exact)."""
    a = list(b)
    p = len(a) - 1
    for j in range(p):
        for k in range(p - j - 1, p):
            a[k] -= z0 * a[k + 1]
    return a


def eval_multipole(a: Sequence[complex], center: complex, w: complex) -> tuple[complex, complex]:
    """Value and derivative of a_0 log(w - c) + sum_k a_k / (w - c)^k."""
    d = w - center
    inv = 1 / d
    v = 0j
    dv = 0j
    for k in range(len(a) - 1, 0, -1):
        v = (v + a[k]) * inv
        dv = (dv + k * a[k]) * inv
    return a[0] * cmath.log(d) + v, a[0] * inv - dv * inv


def eval_local(b: Sequence[complex], center: complex, w: complex) -> tuple[complex, complex]:
    """Value and derivative of sum_l b_l (w - c)^l."""
    d = w - center
    v = 0j
    dv = 0j
    for k in range(len(b) - 1, -1, -1):
        dv = dv * d + v
        v = v * d + b[k]
    return v, dv


def _add(acc: list[complex], b: Sequence[complex]) -> None:
    for k in range(len(acc)):
        acc[k] += b[k]


def adaptive_fmm(q: Sequence[float], z: Sequence[complex], p: int = 12, s: int = 10, max_level: int = 30):
    """Potentials u_j and fields grad u_j (as complex numbers) of all charges.

    Returns (u, field, stats); stats counts the ordered pairs of the near field
    ("p2p"), the translations of the V list ("m2l"), the W list evaluations
    ("m2p", box and target pairs) and the X list expansions ("p2l", box pairs).
    """
    n = len(z)
    u = [0.0] * n
    field = [0j] * n
    stats = {"p2p": 0, "m2l": 0, "m2p": 0, "p2l": 0}
    if n == 0:
        return u, field, stats
    C = binomials(p)
    members, children = build_tree(z, s, max_level)  # @line L1
    U, V, W, X = build_lists(children)  # @line L2
    order = sorted(children, key=lambda b: b[0])
    mult: dict[Box, list[complex]] = {}
    for b in reversed(order):  # @line L3
        c = box_center(b)
        if not children[b]:
            mult[b] = p2m(q, z, members[b], c, p)
        else:
            acc = [0j] * (p + 1)
            for ch in children[b]:
                _add(acc, m2m(mult[ch], box_center(ch) - c, C))
            mult[b] = acc
    local: dict[Box, list[complex]] = {}
    for b in order:
        c = box_center(b)
        acc = [0j] * (p + 1)
        for src in V[b]:  # @line L4
            _add(acc, m2l(mult[src], box_center(src) - c, C))
            stats["m2l"] += 1
        for src in X[b]:
            _add(acc, p2l(q, z, members[src], c, p))
            stats["p2l"] += 1
        l, ix, iy = b
        if l > 0:
            parent = (l - 1, ix >> 1, iy >> 1)
            _add(acc, l2l(local[parent], box_center(parent) - c))  # @line L5
        local[b] = acc
    for b in order:
        if children[b]:
            continue
        c = box_center(b)
        for j in members[b]:  # @line L6
            v, dv = eval_local(local[b], c, z[j])
            for src in W[b]:
                mv, mdv = eval_multipole(mult[src], box_center(src), z[j])
                v += mv
                dv += mdv
                stats["m2p"] += 1
            u[j] += v.real
            field[j] += dv.conjugate()
        for src in U[b]:  # @line L7
            for i in members[src]:
                for j in members[b]:
                    if i != j:
                        d = z[j] - z[i]
                        u[j] += q[i] * math.log(abs(d))
                        field[j] += q[i] / d.conjugate()
                        stats["p2p"] += 1
    return u, field, stats


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
