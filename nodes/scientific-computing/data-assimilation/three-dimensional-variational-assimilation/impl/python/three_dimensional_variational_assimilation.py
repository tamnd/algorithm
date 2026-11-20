# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/three-dimensional-variational-assimilation/. The authors are listed in prov/BZ95E9.jsonl.

"""Three-dimensional variational assimilation (3D-Var).

Notation of Ide, Courtier, Ghil and Lorenc (1997): background x^b in R^n
with error covariance B, observations y^o in R^p with error covariance R,
and an observation operator h from R^n to R^p, possibly nonlinear, with
Jacobian H(x). The analysis minimizes

    J(x) = 1/2 (x - x^b)^T B^-1 (x - x^b) + 1/2 (y^o - h(x))^T R^-1 (y^o - h(x)).

The minimizer here is incremental Gauss-Newton: each outer loop linearizes h
at the current x and solves the quadratic problem for the increment with the
conjugate gradient method. B^-1 and R^-1 are applied with Cholesky factors
and never formed. For a linear h one outer loop gives the exact minimizer,
which equals the optimal interpolation and Kalman analysis.
"""

import scimat


def conjugate_gradient(apply_a, b, tol=1e-14, max_iter=None):
    """Solve A z = b for symmetric positive definite A given as a function.

    Stop when |r| <= tol |b|, or after max_iter steps (default 2 len(b)).
    """
    n = len(b)
    if max_iter is None:
        max_iter = 2 * n
    z = [0.0] * n
    r = [float(v) for v in b]
    q = list(r)
    rr = scimat.dot(r, r)
    stop = (tol * scimat.norm2(b)) ** 2
    for _ in range(max_iter):
        if rr <= stop:
            break
        aq = apply_a(q)
        alpha = rr / scimat.dot(q, aq)
        z = [zi + alpha * qi for zi, qi in zip(z, q)]
        r = [ri - alpha * ai for ri, ai in zip(r, aq)]
        rr_new = scimat.dot(r, r)
        q = [ri + (rr_new / rr) * qi for ri, qi in zip(r, q)]
        rr = rr_new
    return z


def cost(x, xb, B, yo, h, R):
    """Return J(x)."""
    LB, LR = scimat.cholesky(B), scimat.cholesky(R)
    e = scimat.sub(x, xb)
    r = scimat.sub(yo, h(x))
    return 0.5 * scimat.dot(e, scimat.cholesky_solve(LB, e)) + 0.5 * scimat.dot(r, scimat.cholesky_solve(LR, r))


def gradient(x, xb, B, yo, h, jac, R):
    """Return grad J(x) = B^-1 (x - x^b) - H(x)^T R^-1 (y^o - h(x))."""
    LB, LR = scimat.cholesky(B), scimat.cholesky(R)
    e = scimat.sub(x, xb)
    r = scimat.sub(yo, h(x))
    Ht = scimat.transpose(jac(x))
    return scimat.sub(scimat.cholesky_solve(LB, e), scimat.matvec(Ht, scimat.cholesky_solve(LR, r)))


def var3d(xb, B, yo, h, jac, R, max_outer=30, tol=1e-12):
    """Return (x^a, iterates): the 3D-Var analysis and the list of outer iterates.

    h(x) returns the model equivalents of the observations and jac(x) the
    p by n Jacobian of h at x. The outer loop stops when the increment is
    below tol (1 + |x|) or after max_outer loops.
    """
    LB, LR = scimat.cholesky(B), scimat.cholesky(R)
    x = [float(v) for v in xb]  # @line L1
    iterates = [list(x)]
    for _ in range(max_outer):  # @line L2
        d = scimat.sub(yo, h(x))  # @line L3
        Hl = jac(x)  # @line L4
        Ht = scimat.transpose(Hl)

        def apply_a(v):  # @line L5
            return scimat.add(scimat.cholesky_solve(LB, v), scimat.matvec(Ht, scimat.cholesky_solve(LR, scimat.matvec(Hl, v))))

        e = scimat.sub(x, xb)
        g = scimat.sub(scimat.cholesky_solve(LB, e), scimat.matvec(Ht, scimat.cholesky_solve(LR, d)))  # @line L6
        dx = conjugate_gradient(apply_a, [-v for v in g])  # @line L7
        x = scimat.add(x, dx)  # @line L8
        iterates.append(list(x))
        if scimat.norm2(dx) <= tol * (1.0 + scimat.norm2(x)):  # @line L9
            break
    return x, iterates  # @line L10


def linear_operator(H):
    """Return (h, jac) for the linear observation operator given by the matrix H."""
    return (lambda x: scimat.matvec(H, x)), (lambda x: H)
