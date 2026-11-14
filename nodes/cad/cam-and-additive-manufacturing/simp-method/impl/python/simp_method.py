# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simp-method/. The authors are listed in prov/KDKEWF.jsonl.

"""SIMP topology optimization with the optimality criteria update, after Sigmund (2001).

Each element e has a density x_e in [xmin, 1] and the Young's modulus
x_e^p E0 (solid isotropic material with penalization). The method minimizes
the compliance f^T u under the volume bound sum x_e <= f N. Each iteration
solves the finite element model, computes the sensitivities, smooths them with
the mesh-independency filter, and updates the densities with the optimality
criteria (OC) rule, with a bisection on the Lagrange multiplier.

The finite element part is in fem2d.py, a shared helper. Floats are used for
the densities and displacements; the tests state their tolerances.
"""

import math

from fem2d import element_energies, q4_stiffness, solve


def mbb_half_beam(nelx, nely):
    """Loads and supports of the half MBB beam: a unit load down at the top left,
    symmetry (no x motion) on the left edge, and a roller at the bottom right."""
    top_left = nely  # node (0, nely)
    force = {2 * top_left + 1: -1.0}
    fixed = [2 * j for j in range(nely + 1)]  # x dofs of the left edge
    fixed.append(2 * (nelx * (nely + 1)) + 1)  # y dof of node (nelx, 0)
    return force, fixed


def filter_weights(nelx, nely, rmin):
    """H_ef = max(0, rmin - dist(e, f)) for the neighbours f of each element e."""
    n = nelx * nely
    r = int(math.ceil(rmin))
    out = []
    for e in range(n):
        ex, ey = divmod(e, nely)
        row = []
        for fx in range(max(0, ex - r), min(nelx, ex + r + 1)):
            for fy in range(max(0, ey - r), min(nely, ey + r + 1)):
                h = rmin - math.hypot(ex - fx, ey - fy)
                if h > 0:
                    row.append((fx * nely + fy, h))
        out.append(row)
    return out


def filter_sensitivities(weights, x, dc):
    """dc~_e = sum_f H_ef x_f dc_f / (x_e sum_f H_ef)."""
    return [sum(h * x[f] * dc[f] for f, h in row) / (x[e] * sum(h for _, h in row))
            for e, row in enumerate(weights)]


def oc_trial(x, dc, lam, move, xmin, eta):
    """The OC fixed point step for the multiplier lam, inside the move limits."""
    return [max(xmin, xi - move, min(1.0, xi + move, xi * (max(0.0, -d) / lam) ** eta))  # @line L18
            for xi, d in zip(x, dc)]


def oc_update(x, dc, volfrac, move=0.2, xmin=1e-3, eta=0.5, tol=1e-9, steps=100):
    """The optimality criteria update with a bisection on the multiplier.

    The volume of oc_trial(lam) does not increase with lam. The loop keeps
    l2 feasible (volume at most volfrac N) and l1 infeasible or 0, and it
    returns the trial design at l2, so the result meets the volume bound.
    """
    bound = volfrac * len(x)
    l1, l2 = 0.0, 1.0  # @line L11
    while sum(oc_trial(x, dc, l2, move, xmin, eta)) > bound:  # @line L12
        l1, l2 = l2, 2 * l2
    for _ in range(steps):  # @line L13
        lam = (l1 + l2) / 2  # @line L14
        if sum(oc_trial(x, dc, lam, move, xmin, eta)) > bound:  # @line L15
            l1 = lam
        else:
            l2 = lam
        if l2 - l1 <= tol * l2:  # @line L16
            break
    return oc_trial(x, dc, l2, move, xmin, eta)  # @line L17


def compliance(nelx, nely, ke, x, p, force, fixed):
    u = solve(nelx, nely, ke, [xi ** p for xi in x], force, fixed)
    return sum(v * u[k] for k, v in force.items()), u


def simp(nelx, nely, volfrac, p=3, rmin=1.5, force=None, fixed=None, nu=0.3,
         maxit=60, tol=0.01, move=0.2, xmin=1e-3):
    """Return (x, history) with the final densities and the compliance of each iteration."""
    if force is None:
        force, fixed = mbb_half_beam(nelx, nely)
    ke = [[float(v) for v in row] for row in q4_stiffness(nu)]
    weights = filter_weights(nelx, nely, rmin)
    x = [float(volfrac)] * (nelx * nely)  # @line L1
    history = []
    for _ in range(maxit):  # @line L2
        c, u = compliance(nelx, nely, ke, x, p, force, fixed)  # @line L3
        history.append(c)  # @line L4
        energy = element_energies(nelx, nely, ke, u)
        dc = [-p * xi ** (p - 1) * en for xi, en in zip(x, energy)]  # @line L5
        dc = filter_sensitivities(weights, x, dc)  # @line L6
        xnew = oc_update(x, dc, volfrac, move, xmin)  # @line L7
        change = max(abs(a - b) for a, b in zip(xnew, x))  # @line L8
        x = xnew
        if change < tol:  # @line L9
            break
    return x, history  # @line L10


def show(x, nelx, nely):
    """Rows from top to bottom; '#' for x > 0.5."""
    return "\n".join("".join("#" if x[ex * nely + ey] > 0.5 else "." for ex in range(nelx))
                     for ey in range(nely - 1, -1, -1))


if __name__ == "__main__":
    x, hist = simp(24, 8, 0.5)
    print(show(x, 24, 8))
    print("iterations", len(hist), "first", round(hist[0], 3), "last", round(hist[-1], 3))
