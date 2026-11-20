# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lincs-algorithm/. The authors are listed in prov/F7HF6T.jsonl.
"""LINCS: the linear constraint solver of Hess, Bekker, Berendsen and Fraaije (1997).

Each constraint c = (i, j, d) asks |x_i - x_j| = d. Let B be the C x 3N
matrix whose row c holds the unit vector n_c of the old bond i - j at atom i
and -n_c at atom j, and W the diagonal of inverse masses. The constraint
forces act along the old bonds, so the new positions are
x = x_unc - W B^T lambda. Asking B x = p for a target p gives

    B W B^T lambda = B x_unc - p.

With S = diag(1 / sqrt(w_i + w_j)), B W B^T = S^-1 (I - A) S^-1, where A is
zero on the diagonal and couples constraints that share an atom. LINCS
replaces (I - A)^-1 by the truncated series I + A + ... + A^order. The
first solve uses p = d. Because the old directions are fixed, a rotated bond
ends up too long, so each correction pass sets p_c = sqrt(d^2 - q_c^2), with
q_c the part of the bond normal to n_c, and solves again.

The series converges only when the spectral radius of A is below 1. For a
triangle of constraints it tends to 1 as the triangle becomes flat.

Cost: Theta(C (order + 1)) per solve, with a fixed number of operations per
constraint and no sweep to convergence, so it runs well in parallel.
"""

import math

Vec = list[float]
Bond = tuple[int, int, float]


def coupling(x_old: list[Vec], inv_mass: list[float], bonds: list[Bond]):
    """Directions n_c, scale factors S_c and the sparse coupling matrix A as lists of (d, A_cd)."""
    dirs, scale = [], []
    for i, j, _ in bonds:  # @line L1
        r = [x_old[i][a] - x_old[j][a] for a in range(3)]
        length = math.sqrt(r[0] * r[0] + r[1] * r[1] + r[2] * r[2])
        dirs.append([c / length for c in r])
        scale.append(1.0 / math.sqrt(inv_mass[i] + inv_mass[j]))
    by_atom: dict[int, list[tuple[int, float]]] = {}
    for c, (i, j, _) in enumerate(bonds):
        by_atom.setdefault(i, []).append((c, 1.0))
        by_atom.setdefault(j, []).append((c, -1.0))
    coup: list[list[tuple[int, float]]] = [[] for _ in bonds]
    for atom, members in by_atom.items():  # @line L2
        for c, sc in members:
            for d, sd in members:
                if c != d:
                    nd = sum(p * q for p, q in zip(dirs[c], dirs[d]))
                    coup[c].append((d, -sc * sd * inv_mass[atom] * nd * scale[c] * scale[d]))
    return dirs, scale, coup


def series_solve(coup, rhs: list[float], order: int) -> list[float]:
    """Approximate (I - A)^-1 rhs by rhs + A rhs + ... + A^order rhs."""
    sol, term = list(rhs), list(rhs)
    for _ in range(order):  # @line L4
        term = [sum(a * term[d] for d, a in row) for row in coup]
        sol = [s + t for s, t in zip(sol, term)]
    return sol


def _project(x, inv_mass, bonds, dirs, scale, coup, target, order) -> None:
    rhs = []
    for c, (i, j, _) in enumerate(bonds):  # @line L3
        proj = sum(dirs[c][a] * (x[i][a] - x[j][a]) for a in range(3))
        rhs.append(scale[c] * (proj - target[c]))
    sol = series_solve(coup, rhs, order)
    for c, (i, j, _) in enumerate(bonds):  # @line L5
        lam = scale[c] * sol[c]
        for a in range(3):
            x[i][a] -= inv_mass[i] * lam * dirs[c][a]
            x[j][a] += inv_mass[j] * lam * dirs[c][a]


def lincs(
    x_old: list[Vec], x_unc: list[Vec], inv_mass: list[float], bonds: list[Bond],
    order: int = 4, n_iter: int = 1,
) -> list[Vec]:
    """Constrain x_unc with the LINCS expansion of the given order and n_iter rotation corrections."""
    dirs, scale, coup = coupling(x_old, inv_mass, bonds)
    x = [list(p) for p in x_unc]
    _project(x, inv_mass, bonds, dirs, scale, coup, [d for _, _, d in bonds], order)
    for _ in range(n_iter):  # @line L6
        target = []
        for c, (i, j, d) in enumerate(bonds):
            s = [x[i][a] - x[j][a] for a in range(3)]
            along = sum(dirs[c][a] * s[a] for a in range(3))
            normal2 = sum(v * v for v in s) - along * along
            target.append(math.sqrt(max(0.0, d * d - normal2)))
        _project(x, inv_mass, bonds, dirs, scale, coup, target, order)
    return x  # @line L7


def spectral_radius(coup, iters: int = 500) -> float:
    """Largest |eigenvalue| of the symmetric coupling matrix A by power iteration on A^2."""
    v = [1.0 + 0.1 * c for c in range(len(coup))]
    rho = 0.0
    for _ in range(iters):
        w = [sum(a * v[d] for d, a in row) for row in coup]
        w = [sum(a * w[d] for d, a in row) for row in coup]
        norm = math.sqrt(sum(c * c for c in w))
        if norm == 0.0:
            return 0.0
        rho = math.sqrt(norm / math.sqrt(sum(c * c for c in v)))
        v = [c / norm for c in w]
    return rho
