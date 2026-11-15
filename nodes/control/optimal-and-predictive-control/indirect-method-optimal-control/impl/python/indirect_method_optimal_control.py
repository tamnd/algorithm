# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/indirect-method-optimal-control/. The authors are listed in prov/NBHETY.jsonl.

"""Indirect method for optimal control by single shooting.

The maximum principle turns an optimal control problem into a two-point
boundary value problem for the state x and the costate lam:

    x' = H_lam,  lam' = -H_x,  x(0) = x0,  R(x(T), lam(T), T) = 0,

where the input u(x, lam) is already eliminated by the minimum condition.
Single shooting guesses the unknown initial costate s = lam(0) (and the final
time T if it is free), integrates the canonical equations forward with RK4,
and corrects the guess by Newton's method on the residual R.

Conventions:
- canon(t, z) returns z' for z = x + lam, one flat list with x first.
- residual(zT, T) returns a flat list with one entry for each unknown.
- With free_time = True the unknowns are s = lam(0) + [T], so T is last.
- The Newton Jacobian comes from forward differences with the step
  h * max(1, |s_j|).
"""

import ctlmat as cm
import ctlsim as cs

__all__ = ["integrate", "shooting_residual", "fd_jacobian", "single_shooting"]


def integrate(canon, z0, T, N):
    """Return the N + 1 points z(k T / N), k = 0..N, of z' = canon(t, z) by RK4."""
    if N < 1:
        raise ValueError("integrate: N must be at least 1")
    if not T > 0:
        raise ValueError("integrate: T must be positive")
    _, zs, _ = cs.simulate(lambda t, z, u: canon(t, z), [float(v) for v in z0], 0.0, T, T / N)
    return zs


def _split(s, n, T, free_time):
    """Split the unknowns into the initial costate and the final time."""
    want = n + 1 if free_time else n
    if len(s) != want:
        raise ValueError("expected %d unknowns, got %d" % (want, len(s)))
    if free_time:
        return [float(v) for v in s[:n]], float(s[n])
    if T is None:
        raise ValueError("T is required when the final time is fixed")
    return [float(v) for v in s], float(T)


def shooting_residual(canon, x0, residual, s, T=None, N=200, free_time=False):
    """Return R(z(T), T) for the trajectory that starts at (x0, lam(0))."""
    lam0, TT = _split(s, len(x0), T, free_time)
    zT = integrate(canon, list(x0) + lam0, TT, N)[-1]
    return [float(v) for v in residual(zT, TT)]


def fd_jacobian(phi, s, r=None, h=1e-7):
    """Return the forward difference Jacobian of phi at s (r = phi(s) if given)."""
    r = phi(s) if r is None else r
    cols = []
    for j in range(len(s)):
        step = h * max(1.0, abs(s[j]))
        sj = list(s)
        sj[j] += step
        rj = phi(sj)
        cols.append([(a - b) / step for a, b in zip(rj, r)])
    return cm.transpose(cols)


def single_shooting(canon, x0, residual, s0, T=None, N=200, free_time=False,
                    tol=1e-10, maxit=50, h=1e-7):
    """Solve the boundary value problem by single shooting and Newton's method.

    Returns (s, k): the unknowns s (lam(0), then T if free_time) with
    ||R|| <= tol, and the number k of Newton steps taken. Raises RuntimeError
    if maxit Newton steps do not reach the tolerance.
    """
    n = len(x0)
    s = [float(v) for v in s0]
    _split(s, n, T, free_time)

    def phi(v):
        return shooting_residual(canon, x0, residual, v, T, N, free_time)

    for k in range(maxit + 1):  # @line L1
        lam0, TT = _split(s, n, T, free_time)
        zT = integrate(canon, list(x0) + lam0, TT, N)[-1]  # @line L2
        r = [float(v) for v in residual(zT, TT)]  # @line L3
        if len(r) != len(s):
            raise ValueError("the residual must have one entry for each unknown")
        if cm.norm2(r) <= tol:  # @line L4
            return s, k
        if k == maxit:
            break
        J = fd_jacobian(phi, s, r, h)  # @line L5
        d = cm.solve(J, r)
        s = [a - b for a, b in zip(s, d)]  # @line L6
    raise RuntimeError("single_shooting: no convergence in %d Newton steps" % maxit)
