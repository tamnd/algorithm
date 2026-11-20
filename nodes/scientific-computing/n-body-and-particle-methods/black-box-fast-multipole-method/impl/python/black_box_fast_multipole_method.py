# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/black-box-fast-multipole-method/. The authors are listed in prov/T616YW.jsonl.
"""Black-box fast multipole method of Fong and Darve, in 2D on a uniform tree.

Charges q[i] sit at points z[i] (complex numbers) of the unit square. The
output is u_j = sum over i != j of q_i K(z_j, z_i), for any kernel K that is
smooth away from x = y and is given as a function.

For two well separated boxes T and C, the kernel is replaced by its tensor
Chebyshev interpolant with n nodes in each of the four coordinates:

    K(x, y) ~ sum_m sum_m' S_T(m, x) K(xbar_m, ybar_m') S_C(m', y),

where xbar_m are the n^2 nodes of T, ybar_m' those of C, and
S(m, x) = S_n(xbar_m1, x1) S_n(xbar_m2, x2) with

    S_n(xbar, x) = 1/n + (2/n) sum_{k=1}^{n-1} T_k(xbar) T_k(x)

on [-1, 1] (the Lagrange polynomial of the Chebyshev node xbar). The
multipole weights of a box are W_C(m') = sum_i q_i S_C(m', y_i), and the
local values of a box are g_T(m) = sum K(xbar_m, ybar_m') W_C(m'). The
shifts between parent and child boxes are interpolation steps, which are
exact because S_parent(m, .) is a polynomial of degree n - 1.
"""

import math
from typing import Callable, Optional, Sequence

Kernel = Callable[[complex, complex], float]


def log_kernel(x: complex, y: complex) -> float:
    return math.log(abs(x - y))


def inverse_distance(x: complex, y: complex) -> float:
    return 1.0 / abs(x - y)


def cheb_nodes(n: int) -> list[float]:
    """The n Chebyshev nodes of the first kind, cos((2m - 1) pi / (2n)), m = 1..n."""
    return [math.cos((2 * m - 1) * math.pi / (2 * n)) for m in range(1, n + 1)]


def cheb_T(n: int, x: float) -> list[float]:
    """T_0(x), ..., T_{n-1}(x) by the three-term recurrence."""
    t = [1.0, x][:n]
    while len(t) < n:
        t.append(2 * x * t[-1] - t[-2])
    return t


def s_weights(n: int, nodes: Sequence[float], x: float) -> list[float]:
    """[S_n(xbar_m, x) for each node xbar_m], for x in [-1, 1]."""
    tx = cheb_T(n, x)
    out = []
    for xm in nodes:
        tm = cheb_T(n, xm)
        out.append(1.0 / n + (2.0 / n) * sum(tm[k] * tx[k] for k in range(1, n)))
    return out


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


def box_nodes(center: complex, w: float, nodes: Sequence[float]) -> list[complex]:
    """The n^2 tensor Chebyshev nodes of a box of side w, index m = m1 * n + m2."""
    return [center + 0.5 * w * complex(a, b) for a in nodes for b in nodes]


def p2m(q, z, idx, center: complex, w: float, n: int, nodes) -> list[float]:
    """W(m) = sum_i q_i S(m, y_i), with y_i mapped to [-1, 1]^2."""
    wt = [0.0] * (n * n)
    for i in idx:
        sx = s_weights(n, nodes, 2 * (z[i].real - center.real) / w)
        sy = s_weights(n, nodes, 2 * (z[i].imag - center.imag) / w)
        for m1 in range(n):
            a = q[i] * sx[m1]
            for m2 in range(n):
                wt[m1 * n + m2] += a * sy[m2]
    return wt


def child_shift(n: int, nodes) -> dict:
    """S1[a][m][m'] = S_n(xbar_m, (xbar_m' + 2a - 1) / 2): parent basis at the child nodes, a = 0 or 1."""
    return {a: [s_weights(n, nodes, (xm + 2 * a - 1) / 2) for xm in nodes] for a in (0, 1)}


def _shift_up(wc: Sequence[float], sa, sb, n: int) -> list[float]:
    """Parent weights from child weights: W_p(m1, m2) = sum S1[a][m'1][m1] S1[b][m'2][m2] W_c(m'1, m'2)."""
    tmp = [0.0] * (n * n)
    for k1 in range(n):
        for m2 in range(n):
            tmp[k1 * n + m2] = sum(sb[k2][m2] * wc[k1 * n + k2] for k2 in range(n))
    out = [0.0] * (n * n)
    for m1 in range(n):
        for m2 in range(n):
            out[m1 * n + m2] = sum(sa[k1][m1] * tmp[k1 * n + m2] for k1 in range(n))
    return out


def _shift_down(gp: Sequence[float], sa, sb, n: int) -> list[float]:
    """Child values from parent values: g_c(k1, k2) = sum S1[a][k1][m1] S1[b][k2][m2] g_p(m1, m2)."""
    tmp = [0.0] * (n * n)
    for m1 in range(n):
        for k2 in range(n):
            tmp[m1 * n + k2] = sum(sb[k2][m2] * gp[m1 * n + m2] for m2 in range(n))
    out = [0.0] * (n * n)
    for k1 in range(n):
        for k2 in range(n):
            out[k1 * n + k2] = sum(sa[k1][m1] * tmp[m1 * n + k2] for m1 in range(n))
    return out


def m2l_matrices(kernel: Kernel, level: int, nodes) -> dict:
    """[K(xbar_m, ybar_m')] for a target box at 0 and a source box at each offset of the interaction list."""
    w = 1.0 / (1 << level)
    tgt = box_nodes(0j, w, nodes)
    out = {}
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            if max(abs(dx), abs(dy)) > 1:
                src = box_nodes(complex(dx * w, dy * w), w, nodes)
                out[(dx, dy)] = [[kernel(x, y) for y in src] for x in tgt]
    return out


def bbfmm(q: Sequence[float], z: Sequence[complex], kernel: Kernel = log_kernel, n: int = 5,
          levels: Optional[int] = None, s: int = 8):
    """Potentials u_j = sum_{i != j} q_i K(z_j, z_i) with n Chebyshev nodes per coordinate.

    levels is the leaf level L (at least 2). Returns (u, stats) with the
    ordered pairs of the near field ("p2p") and the M2L products ("m2l").
    """
    nq = len(z)
    if levels is None:
        levels = max(2, math.ceil(math.log(nq / s, 4))) if nq > s else 2
    L = levels
    nodes = cheb_nodes(n)
    shift = child_shift(n, nodes)
    mats = {l: m2l_matrices(kernel, l, nodes) for l in range(2, L + 1)}
    m = 1 << L
    leaf: dict[tuple[int, int], list[int]] = {}
    for i, zi in enumerate(z):
        key = (min(int(zi.real * m), m - 1), min(int(zi.imag * m), m - 1))
        leaf.setdefault(key, []).append(i)
    mult: list[dict] = [dict() for _ in range(L + 1)]
    for key, idx in leaf.items():  # @line L1
        mult[L][key] = p2m(q, z, idx, box_center(*key, L), 1.0 / m, n, nodes)
    for l in range(L - 1, 1, -1):  # @line L2
        for (cx, cy), wc in mult[l + 1].items():
            acc = mult[l].setdefault((cx // 2, cy // 2), [0.0] * (n * n))
            up = _shift_up(wc, shift[cx % 2], shift[cy % 2], n)
            for k in range(n * n):
                acc[k] += up[k]
    local: list[dict] = [dict() for _ in range(L + 1)]
    n_m2l = 0
    for l in range(2, L + 1):
        for key, wc in mult[l].items():  # @line L3
            for tgt in interaction_list(*key, l):
                if l == L and tgt not in leaf:
                    continue
                mat = mats[l][(key[0] - tgt[0], key[1] - tgt[1])]
                acc = local[l].setdefault(tgt, [0.0] * (n * n))
                for k in range(n * n):
                    acc[k] += sum(a * b for a, b in zip(mat[k], wc))
                n_m2l += 1
        if l < L:
            for (px, py), gp in local[l].items():  # @line L4
                for a in (0, 1):
                    for b in (0, 1):
                        down = _shift_down(gp, shift[a], shift[b], n)
                        acc = local[l + 1].setdefault((2 * px + a, 2 * py + b), [0.0] * (n * n))
                        for k in range(n * n):
                            acc[k] += down[k]
    u = [0.0] * nq
    n_p2p = 0
    w = 1.0 / m
    for key, idx in leaf.items():
        g = local[L].get(key)
        c = box_center(*key, L)
        if g is not None:
            for j in idx:  # @line L5
                sx = s_weights(n, nodes, 2 * (z[j].real - c.real) / w)
                sy = s_weights(n, nodes, 2 * (z[j].imag - c.imag) / w)
                u[j] += sum(sx[m1] * sum(sy[m2] * g[m1 * n + m2] for m2 in range(n)) for m1 in range(n))
        ix, iy = key
        for nx in range(ix - 1, ix + 2):  # @line L6
            for ny in range(iy - 1, iy + 2):
                for i in leaf.get((nx, ny), ()):
                    for j in idx:
                        if i != j:
                            u[j] += q[i] * kernel(z[j], z[i])
                            n_p2p += 1
    return u, {"p2p": n_p2p, "m2l": n_m2l}  # @line L7


def direct(q: Sequence[float], z: Sequence[complex], kernel: Kernel = log_kernel) -> list[float]:
    """Direct summation over all ordered pairs: the reference."""
    nq = len(z)
    return [sum(q[i] * kernel(z[j], z[i]) for i in range(nq) if i != j) for j in range(nq)]
