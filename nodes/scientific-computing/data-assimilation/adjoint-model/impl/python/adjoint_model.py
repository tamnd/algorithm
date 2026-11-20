# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adjoint-model/. The authors are listed in prov/D36VQ5.jsonl.

"""Tangent linear and adjoint models of Lorenz-96 with RK4 steps.

The forward model is x_{k+1} = M(x_k), one classical Runge-Kutta step of
dx_j/dt = (x_{j+1} - x_{j-2}) x_{j-1} - x_j + F with cyclic indices.

* tlm_step(x, dx) returns M'(x) dx, the tangent linear model.
* adj_step(x, lam) returns M'(x)^T lam, the adjoint model, written by
  reversing the statements of tlm_step line by line.
* gradient(...) returns the gradient of the 4D-Var cost with respect to the
  initial state by one forward sweep and one backward adjoint sweep.
"""


def tendency(x, F):
    """Return the Lorenz-96 tendency f(x)."""
    n = len(x)
    return [(x[(j + 1) % n] - x[j - 2]) * x[j - 1] - x[j] + F for j in range(n)]


def tlm_tendency(x, dx):
    """Return f'(x) dx."""
    n = len(x)
    return [
        (dx[(j + 1) % n] - dx[j - 2]) * x[j - 1] + (x[(j + 1) % n] - x[j - 2]) * dx[j - 1] - dx[j]
        for j in range(n)
    ]


def adj_tendency(x, lam):
    """Return f'(x)^T lam, the transpose of tlm_tendency, statement by statement."""
    n = len(x)
    out = [-v for v in lam]
    for j in range(n):
        out[(j + 1) % n] += lam[j] * x[j - 1]
        out[j - 2] -= lam[j] * x[j - 1]
        out[j - 1] += lam[j] * (x[(j + 1) % n] - x[j - 2])
    return out


def _axpy(a, x, y):
    return [a * u + v for u, v in zip(x, y)]


def step(x, F, h):
    """Return M(x), one RK4 step of length h."""
    k1 = tendency(x, F)
    k2 = tendency(_axpy(h / 2, k1, x), F)
    k3 = tendency(_axpy(h / 2, k2, x), F)
    k4 = tendency(_axpy(h, k3, x), F)
    return [a + h / 6 * (b + 2 * c + 2 * d + e) for a, b, c, d, e in zip(x, k1, k2, k3, k4)]


def _stages(x, F, h):
    k1 = tendency(x, F)
    z2 = _axpy(h / 2, k1, x)
    k2 = tendency(z2, F)
    z3 = _axpy(h / 2, k2, x)
    k3 = tendency(z3, F)
    z4 = _axpy(h, k3, x)
    return x, z2, z3, z4


def tlm_step(x, dx, F, h):
    """Return M'(x) dx: the derivative of one RK4 step in the direction dx."""
    z1, z2, z3, z4 = _stages(x, F, h)
    dk1 = tlm_tendency(z1, dx)
    dk2 = tlm_tendency(z2, _axpy(h / 2, dk1, dx))
    dk3 = tlm_tendency(z3, _axpy(h / 2, dk2, dx))
    dk4 = tlm_tendency(z4, _axpy(h, dk3, dx))
    return [a + h / 6 * (b + 2 * c + 2 * d + e) for a, b, c, d, e in zip(dx, dk1, dk2, dk3, dk4)]


def adj_step(x, lam, F, h):
    """Return M'(x)^T lam: the statements of tlm_step in reverse order, each transposed."""
    z1, z2, z3, z4 = _stages(x, F, h)
    a_dx = list(lam)
    a_dk1 = [h / 6 * v for v in lam]
    a_dk2 = [h / 3 * v for v in lam]
    a_dk3 = [h / 3 * v for v in lam]
    a_dk4 = [h / 6 * v for v in lam]
    a_in4 = adj_tendency(z4, a_dk4)  # dk4 = f'(z4)(dx + h dk3)
    a_dx = _axpy(1.0, a_in4, a_dx)
    a_dk3 = _axpy(h, a_in4, a_dk3)
    a_in3 = adj_tendency(z3, a_dk3)  # dk3 = f'(z3)(dx + h/2 dk2)
    a_dx = _axpy(1.0, a_in3, a_dx)
    a_dk2 = _axpy(h / 2, a_in3, a_dk2)
    a_in2 = adj_tendency(z2, a_dk2)  # dk2 = f'(z2)(dx + h/2 dk1)
    a_dx = _axpy(1.0, a_in2, a_dx)
    a_dk1 = _axpy(h / 2, a_in2, a_dk1)
    return _axpy(1.0, adj_tendency(z1, a_dk1), a_dx)  # dk1 = f'(z1) dx


def forward(x0, F, h, K):
    """Return the trajectory [x_0, ..., x_K]."""
    path = [list(x0)]
    for _ in range(K):
        path.append(step(path[-1], F, h))
    return path


def cost(x0, F, h, K, obs, idx, r):
    """Return J(x_0) = 1/2 sum over k in obs of |x_k[idx] - obs[k]|^2 / r."""
    path = forward(x0, F, h, K)
    total = 0.0
    for k, y in obs.items():
        total += sum((path[k][i] - yi) ** 2 for i, yi in zip(idx, y)) / (2 * r)
    return total


def gradient(x0, F, h, K, obs, idx, r):
    """Return grad J(x_0) by one forward sweep and one backward adjoint sweep.

    obs maps a step k (0 <= k <= K) to the observed values of the variables
    idx at x_k; the observation errors have variance r.
    """
    path = forward(x0, F, h, K)  # @line L1
    lam = [0.0] * len(x0)  # @line L2
    for k in range(K, -1, -1):  # @line L3
        if k in obs:  # @line L4
            for i, yi in zip(idx, obs[k]):
                lam[i] += (path[k][i] - yi) / r
        if k > 0:  # @line L5
            lam = adj_step(path[k - 1], lam, F, h)
    return lam  # @line L6
