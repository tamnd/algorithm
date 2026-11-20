# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shake-constraint-algorithm/. The authors are listed in prov/3AE47X.jsonl.

import math
import random

import pytest

from shake_constraint_algorithm import bond_error, shake, shake_verlet_step


def perturbed(x, rng, size):
    return [[c + rng.uniform(-size, size) for c in p] for p in x]


def solve_dense(a, b):
    """Gaussian elimination with partial pivoting, the reference linear solver."""
    n = len(b)
    m = [list(row) + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(m[r][c]))
        m[c], m[piv] = m[piv], m[c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            for k in range(c, n + 1):
                m[r][k] -= f * m[c][k]
    out = [0.0] * n
    for r in range(n - 1, -1, -1):
        out[r] = (m[r][n] - sum(m[r][k] * out[k] for k in range(r + 1, n))) / m[r][r]
    return out


def newton_reference(x_old, x_unc, w, bonds):
    """Solve all constraint equations at once by Newton's method on the multipliers."""
    nc = len(bonds)
    g = [0.0] * nc

    def positions(g):
        x = [list(p) for p in x_unc]
        for (i, j, _), gc in zip(bonds, g):
            for a in range(3):
                r = x_old[i][a] - x_old[j][a]
                x[i][a] += w[i] * gc * r
                x[j][a] -= w[j] * gc * r
        return x

    for _ in range(50):
        x = positions(g)
        res = [sum((x[i][a] - x[j][a]) ** 2 for a in range(3)) - d * d for i, j, d in bonds]
        if max(abs(v) for v in res) < 1e-15:
            break
        jac = [[0.0] * nc for _ in range(nc)]
        for c, (i, j, _) in enumerate(bonds):
            s = [x[i][a] - x[j][a] for a in range(3)]
            for e, (k, l, _) in enumerate(bonds):
                r = [x_old[k][a] - x_old[l][a] for a in range(3)]
                coef = (w[k] if k == i else 0.0) - (w[k] if k == j else 0.0) - (w[l] if l == i else 0.0) + (w[l] if l == j else 0.0)
                jac[c][e] = 2.0 * coef * sum(s[a] * r[a] for a in range(3))
        step = solve_dense(jac, [-v for v in res])
        g = [a + b for a, b in zip(g, step)]
    return positions(g)


def test_single_bond_matches_the_quadratic_root() -> None:
    x_old = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]
    x_unc = [[0.05, 0.1, -0.02], [1.2, -0.05, 0.03]]
    w = [1.0, 0.25]
    x, _ = shake(x_old, x_unc, w, [(0, 1, 1.0)])
    # |s + c g r|^2 = d^2 is a quadratic in g; take the root of smaller size
    s = [x_unc[0][a] - x_unc[1][a] for a in range(3)]
    r = [-1.0, 0.0, 0.0]
    c = w[0] + w[1]
    qa, qb, qc = c * c, 2 * c * sum(u * v for u, v in zip(s, r)), sum(u * u for u in s) - 1.0
    roots = [(-qb + sg * math.sqrt(qb * qb - 4 * qa * qc)) / (2 * qa) for sg in (1, -1)]
    g = min(roots, key=abs)
    exact0 = [x_unc[0][a] + w[0] * g * r[a] for a in range(3)]
    assert math.dist(x[0], exact0) < 1e-12


def test_coupled_bonds_match_a_newton_solve() -> None:
    rng = random.Random(3)
    # a branched molecule: a centre bonded to three atoms, plus one bond between two of them
    x_old = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [-0.3, 0.95, 0.0], [-0.3, -0.4, 0.87], [1.5, 0.9, 0.0]]
    bonds = [(0, 1, 1.0), (0, 2, math.dist(x_old[0], x_old[2])), (0, 3, math.dist(x_old[0], x_old[3])), (1, 4, math.dist(x_old[1], x_old[4])), (2, 4, math.dist(x_old[2], x_old[4]))]
    w = [1 / 16, 1.0, 1.0, 1 / 12, 0.5]
    x_unc = perturbed(x_old, rng, 0.05)
    x, sweeps = shake(x_old, x_unc, w, bonds)
    assert bond_error(x, bonds) < 1e-11
    ref = newton_reference(x_old, x_unc, w, bonds)
    assert max(math.dist(a, b) for a, b in zip(x, ref)) < 1e-10
    assert sweeps > 2  # the bonds are coupled, so one sweep is not enough


def test_corrections_keep_the_centre_of_mass() -> None:
    rng = random.Random(4)
    x_old = [[float(k), 0.3 * (k % 2), 0.0] for k in range(5)]
    bonds = [(k, k + 1, math.dist(x_old[k], x_old[k + 1])) for k in range(4)]
    m = [1.0, 12.0, 14.0, 1.0, 16.0]
    w = [1 / v for v in m]
    x_unc = perturbed(x_old, rng, 0.04)
    x, _ = shake(x_old, x_unc, w, bonds)
    for a in range(3):
        assert abs(sum(mi * p[a] for mi, p in zip(m, x)) - sum(mi * p[a] for mi, p in zip(m, x_unc))) < 1e-12


def test_fixed_atom_does_not_move() -> None:
    x_old = [[0.0, 0.0, 0.0], [0.0, -1.0, 0.0]]
    x_unc = [[0.0, 0.0, 0.0], [0.2, -1.05, 0.0]]
    x, _ = shake(x_old, x_unc, [0.0, 1.0], [(0, 1, 1.0)])
    assert x[0] == [0.0, 0.0, 0.0]
    assert abs(math.dist(x[0], x[1]) - 1.0) < 1e-12


def chain_force(x):
    # springs between atoms two apart in a rigid chain of four, and a soft wall in z
    f = [[0.0] * 3 for _ in x]
    for i, j in ((0, 2), (1, 3), (0, 3)):
        s = [x[i][a] - x[j][a] for a in range(3)]
        r = math.sqrt(sum(c * c for c in s))
        mag = -2.0 * (r - 1.6)
        for a in range(3):
            f[i][a] += mag * s[a] / r
            f[j][a] -= mag * s[a] / r
    return f


def chain_energy(x, v, m):
    e = sum(0.5 * mi * sum(c * c for c in vi) for mi, vi in zip(m, v))
    for i, j in ((0, 2), (1, 3), (0, 3)):
        e += (math.dist(x[i], x[j]) - 1.6) ** 2
    return e


def run_chain(h: float, t_end: float) -> tuple[float, float]:
    m = [1.0, 2.0, 2.0, 1.0]
    w = [1 / v for v in m]
    x0 = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.5, 0.85, 0.1], [2.4, 1.1, -0.3]]
    bonds = [(k, k + 1, math.dist(x0[k], x0[k + 1])) for k in range(3)]
    # start at rest: x_(-1) = x_0 is a consistent start with zero velocity
    xs = [x0, shake_verlet_step(x0, x0, w, chain_force, h, bonds)]
    xs[1] = [[0.5 * (a + b) for a, b in zip(p, q)] for p, q in zip(x0, xs[1])]
    xs[1], _ = shake(x0, xs[1], w, bonds)
    steps = int(round(t_end / h))
    worst = 0.0
    energies = []
    for _ in range(steps):
        xs.append(shake_verlet_step(xs[-2], xs[-1], w, chain_force, h, bonds))
        worst = max(worst, bond_error(xs[-1], bonds))
        v = [[(a - b) / (2 * h) for a, b in zip(p, q)] for p, q in zip(xs[-1], xs[-3])]
        energies.append(chain_energy(xs[-2], v, m))
        xs = xs[-2:]
    return max(energies) - min(energies), worst


def test_bonds_hold_and_energy_stays_bounded() -> None:
    spread_h, worst = run_chain(0.02, 20.0)
    assert worst < 1e-11
    spread_h2, _ = run_chain(0.01, 20.0)
    assert spread_h < 0.05
    assert 2.5 < spread_h / spread_h2 < 6.0  # second order: halving h divides the fluctuation by about 4


def test_divergence_is_reported() -> None:
    with pytest.raises(RuntimeError):
        x_old = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [2.0, 0.0, 0.0]]
        x_unc = [[0.0, 0.0, 0.0], [1.0, 0.3, 0.0], [2.0, 0.0, 0.0]]
        shake(x_old, x_unc, [1.0, 1.0, 1.0], [(0, 1, 1.0), (1, 2, 1.0), (0, 2, 1.9)], max_sweeps=20)
