# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/variational-network-mri/. The authors are listed in prov/THXH29.jsonl.

"""The variational network (Hammernik et al. 2018) as an unrolled gradient scheme.

The network is given. This module does not train it. A stage t is a pair
(reg_t, lam_t): reg_t is a function that maps an image u to the image
sum_i K_i^T phi'_i(K_i u), and lam_t >= 0 weights the data term. The
forward pass is

    u_0 = A^* f,   u_{t+1} = u_t - reg_t(u_t) - lam_t A^*(A u_t - f).

An image is an n1 x n2 complex image, stored row-major as one list. The
operator A maps u to the coil k-space M F_u (c_j u) on the full grid, with
the unitary 2D DFT F_u, a 0/1 mask M and coil maps c_j (one coil, c = 1, if
no maps are given).

Fields of experts terms: a filter is a pair of real kernels (k_re, k_im),
each a dict {(di, dj): weight} on periodic offsets, and

    (K u)(p) = sum_o k_re[o] Re u(p + o) + k_im[o] Im u(p + o),

a real image, as in Hammernik et al. Its adjoint for the real inner product
Re <u, v> maps a real image z to sum_o (k_re[o] + i k_im[o]) z(p - o).
With a potential phi and its derivative dphi, foe_regularizer builds reg_t
and foe_energy evaluates sum_i sum_p phi_i((K_i u)(p)).
"""

import math

from imgkit import dft2, idft2, unflatten


# ------------------------------------------------------------------ the data term


def _fu2(img, n1, n2):
    s = 1.0 / math.sqrt(n1 * n2)
    return [v * s for row in dft2(unflatten(img, n1, n2)) for v in row]


def _fu2h(k, n1, n2):
    s = math.sqrt(n1 * n2)
    return [v * s for row in idft2(unflatten(k, n1, n2)) for v in row]


def make_operator(mask, n1, n2, coils=None):
    """The pair (A, A^*) for one frame, as functions."""
    maps = coils or [None]

    def apply_a(u):
        out = []
        for cmap in maps:
            img = u if cmap is None else [c * v for c, v in zip(cmap, u)]
            out.append([v if m else 0j for v, m in zip(_fu2(img, n1, n2), mask)])
        return out

    def apply_ah(data):
        acc = [0j] * (n1 * n2)
        for cmap, k in zip(maps, data):
            img = _fu2h([v if m else 0j for v, m in zip(k, mask)], n1, n2)
            if cmap is None:
                acc = [a + v for a, v in zip(acc, img)]
            else:
                acc = [a + c.conjugate() * v for a, c, v in zip(acc, cmap, img)]
        return acc

    return apply_a, apply_ah


# ------------------------------------------------------------------ fields of experts


def filter_apply(kernel, u, n1, n2):
    """(K u)(p) = sum_o k_re[o] Re u(p + o) + k_im[o] Im u(p + o), periodic."""
    k_re, k_im = kernel
    out = [0.0] * (n1 * n2)
    for i in range(n1):
        for j in range(n2):
            s = 0.0
            for (di, dj), w in k_re.items():
                s += w * u[((i + di) % n1) * n2 + (j + dj) % n2].real
            for (di, dj), w in k_im.items():
                s += w * u[((i + di) % n1) * n2 + (j + dj) % n2].imag
            out[i * n2 + j] = s
    return out


def filter_adjoint(kernel, z, n1, n2):
    """K^T z for the real inner product: sum_o (k_re[o] + i k_im[o]) z(p - o)."""
    k_re, k_im = kernel
    out = [0j] * (n1 * n2)
    for i in range(n1):
        for j in range(n2):
            v = z[i * n2 + j]
            if v == 0:
                continue
            for (di, dj), w in k_re.items():
                q = ((i + di) % n1) * n2 + (j + dj) % n2
                out[q] += w * v
            for (di, dj), w in k_im.items():
                q = ((i + di) % n1) * n2 + (j + dj) % n2
                out[q] += 1j * w * v
    return out


def forward_differences():
    """Four filters: forward differences along rows and columns of Re u and of Im u."""
    dx = {(0, 0): -1.0, (0, 1): 1.0}
    dy = {(0, 0): -1.0, (1, 0): 1.0}
    return [(dx, {}), (dy, {}), ({}, dx), ({}, dy)]


def foe_regularizer(kernels, dphis, n1, n2):
    """The function u -> sum_i K_i^T dphi_i(K_i u)."""

    def reg(u):
        acc = [0j] * (n1 * n2)
        for kernel, dphi in zip(kernels, dphis):
            z = [dphi(v) for v in filter_apply(kernel, u, n1, n2)]
            acc = [a + b for a, b in zip(acc, filter_adjoint(kernel, z, n1, n2))]
        return acc

    return reg


def foe_energy(u, kernels, phis, n1, n2):
    """sum_i sum_p phi_i((K_i u)(p))."""
    return sum(sum(phi(v) for v in filter_apply(kernel, u, n1, n2)) for kernel, phi in zip(kernels, phis))


# ------------------------------------------------------------------ the network


def variational_network(f, stages, apply_a, apply_ah, history=None):
    """Run the given stages [(reg_t, lam_t), ...] on the data f.

    If history is a list, u_0, ..., u_T are appended to it.
    """
    u = apply_ah(f)  # @line L1
    if history is not None:
        history.append(u)
    for reg, lam in stages:  # @line L2
        r = reg(u)  # @line L3
        resid = [[a - b for a, b in zip(ac, fc)] for ac, fc in zip(apply_a(u), f)]  # @line L4
        g = apply_ah(resid)
        u = [x - rr - lam * gg for x, rr, gg in zip(u, r, g)]  # @line L5
        if history is not None:
            history.append(u)
    return u  # @line L6
