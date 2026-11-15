# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/finite-horizon-lqr/. The authors are listed in prov/6S5J80.jsonl.

"""Finite-horizon linear quadratic regulator.

Discrete time. The plant is x_(k+1) = A x_k + B u_k for k = 0, ..., N - 1,
and the cost is

    J = sum_(k=0)^(N-1) (x_k^T Q x_k + u_k^T R u_k) + x_N^T Q_f x_N,

with Q >= 0, Q_f >= 0 and R > 0. The backward recursion

    P_N = Q_f,
    K_k = (R + B^T P_(k+1) B)^(-1) B^T P_(k+1) A,
    P_k = Q + A^T P_(k+1) A - A^T P_(k+1) B K_k,

gives the optimal feedback u_k = -K_k x_k and the optimal cost x_0^T P_0 x_0.
With int or Fraction data every step is exact.

Continuous time. The plant is x' = A x + B u on [0, T], and the cost is the
integral of x^T Q x + u^T R u plus x(T)^T Q_f x(T). The Riccati differential
equation

    -P'(t) = A^T P + P A - P B R^(-1) B^T P + Q,    P(T) = Q_f,

is integrated backward from T with the classical RK4 method and a fixed
step. The optimal feedback is u(t) = -R^(-1) B^T P(t) x(t).
"""

from ctlmat import add, mul, scale, solve, sub, transpose

__all__ = ["riccati_backward", "lqr_cost", "riccati_ode", "rde_rhs"]


def _sym(p):
    """Return (P + P^T) / 2 for a float matrix; exact matrices are returned as they are."""
    return [[(p[i][j] + p[j][i]) / 2 if isinstance(p[i][j], float) else p[i][j]
             for j in range(len(p))] for i in range(len(p))]


def riccati_backward(A, B, Q, R, Qf, N):
    """Return (Ps, Ks): Ps[k] = P_k for k = 0, ..., N and Ks[k] = K_k for k < N."""
    if N < 0:
        raise ValueError("the horizon N must be at least 0")
    at, bt = transpose(A), transpose(B)
    Ps = [None] * (N + 1)
    Ks = [None] * N
    p = [list(row) for row in Qf]  # @line L1
    Ps[N] = p
    for k in range(N - 1, -1, -1):  # @line L2
        pb = mul(p, B)
        s = add(R, mul(bt, pb))  # @line L3
        kk = solve(s, mul(transpose(pb), A))  # @line L4
        p = sub(add(Q, mul(at, mul(p, A))), mul(at, mul(pb, kk)))  # @line L5
        Ps[k] = _sym(p)
        Ks[k] = kk
        p = Ps[k]
    return Ps, Ks  # @line L6


def lqr_cost(A, B, Q, R, Qf, xs, us):
    """Return the cost J of the trajectory xs (N + 1 states) and inputs us (N inputs)."""
    def quad(m, v):
        return sum(v[i] * m[i][j] * v[j] for i in range(len(v)) for j in range(len(v)))
    total = 0
    for x, u in zip(xs, us):
        total += quad(Q, x) + quad(R, u)
    return total + quad(Qf, xs[-1])


def rde_rhs(A, B, Q, R, P):
    """Return A^T P + P A - P B R^(-1) B^T P + Q, which is -P'(t)."""
    pb = mul(P, B)
    return add(add(mul(transpose(A), P), mul(P, A)),
               sub(Q, mul(pb, solve(R, transpose(pb)))))


def riccati_ode(A, B, Q, R, Qf, T, steps):
    """Integrate the Riccati differential equation backward from P(T) = Qf.

    Uses `steps` RK4 steps of size T / steps. Returns (ts, Ps) with
    ts[j] = j T / steps and Ps[j] approximately P(ts[j]), so Ps[0] is P(0).
    The cost of the optimal control from x(0) = x_0 is x_0^T P(0) x_0.
    """
    if steps < 1 or T <= 0:
        raise ValueError("T must be positive and steps at least 1")
    h = T / steps
    p = [[float(v) for v in row] for row in Qf]
    Ps = [None] * (steps + 1)
    Ps[steps] = p

    def f(m):
        return rde_rhs(A, B, Q, R, m)

    for j in range(steps, 0, -1):
        # In backward time tau = T - t the equation is dP/dtau = f(P).
        k1 = f(p)
        k2 = f(add(p, scale(h / 2, k1)))
        k3 = f(add(p, scale(h / 2, k2)))
        k4 = f(add(p, scale(h, k3)))
        inc = add(add(k1, scale(2, k2)), add(scale(2, k3), k4))
        p = _sym(add(p, scale(h / 6, inc)))
        Ps[j - 1] = p
    return [j * h for j in range(steps + 1)], Ps
