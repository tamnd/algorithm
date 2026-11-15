# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lqg-control/. The authors are listed in prov/WY53ER.jsonl.

"""Linear quadratic Gaussian (LQG) control in continuous time.

Plant: x' = A x + B u + w, y = C x + v, with x in R^n, u in R^m, y in R^p.
The noises w and v are white, zero mean and uncorrelated, with intensities
W >= 0 and V > 0. The cost is the average

    J = lim_(T -> inf) (1/T) E integral_0^T (x^T Q x + u^T R u) dt,

with Q >= 0 and R > 0. No cross terms are used.

The LQG controller is u = -K xhat with the observer

    xhat' = A xhat + B u + L (y - C xhat),

where K = R^-1 B^T P from the CARE A^T P + P A - P B R^-1 B^T P + Q = 0
and L = S C^T V^-1 from the filter Riccati equation
A S + S A^T - S C^T V^-1 C S + W = 0. Both are the stabilizing solutions.

The Riccati equations are solved by the matrix sign function of the
Hamiltonian matrix, followed by two Newton (Kleinman) steps that remove the
rounding error of the least squares step. Lyapunov equations are solved
with a Kronecker product, which is fine for the small n of the examples.
"""

from ctlmat import add, block, det, eye, inv, kron, mul, scale, solve, sub, trace, transpose, unvec, vec

__all__ = ["lyap", "care", "filter_are", "lqg", "closed_loop", "lqg_cost", "optimal_cost"]


def lyap(F, M):
    """Return X with F X + X F^T + M = 0 (F must have no eigenvalue pair summing to 0)."""
    n = len(F)
    big = add(kron(eye(n), F), kron(F, eye(n)))
    x = solve(big, [-v for v in vec(M)])
    X = unvec(x, n, n)
    return [[(X[i][j] + X[j][i]) / 2 for j in range(n)] for i in range(n)]


def _sign(Z, tol, max_iter):
    n = len(Z)
    for _ in range(max_iter):
        Zi = inv(Z)
        d = abs(det(Z)) ** (-1.0 / n)  # determinant scaling for faster convergence
        Zn = scale(0.5, add(scale(d, Z), scale(1.0 / d, Zi)))
        diff = max(abs(a - b) for ra, rb in zip(Zn, Z) for a, b in zip(ra, rb))
        size = max(abs(a) for r in Zn for a in r)
        Z = Zn
        if diff <= tol * size:
            break
    else:
        raise ArithmeticError("sign iteration did not converge (eigenvalue on the imaginary axis?)")
    return Z


def care(A, B, Q, R, tol=1e-13, max_iter=100):
    """Return the stabilizing solution P of A^T P + P A - P B R^-1 B^T P + Q = 0."""
    n = len(A)
    A = [[float(v) for v in r] for r in A]
    G = mul(mul(B, inv(R)), transpose(B))
    G = [[float(v) for v in r] for r in G]
    Q = [[float(v) for v in r] for r in Q]
    H = block([[A, scale(-1.0, G)], [scale(-1.0, Q), scale(-1.0, transpose(A))]])  # @line L6
    Wm = _sign(H, tol, max_iter)  # @line L7
    W11 = [r[:n] for r in Wm[:n]]
    W12 = [r[n:] for r in Wm[:n]]
    W21 = [r[:n] for r in Wm[n:]]
    W22 = [r[n:] for r in Wm[n:]]
    M = W12 + add(W22, eye(n))  # (W + I) [I; P] = 0 gives M P = rhs
    rhs = scale(-1.0, add(W11, eye(n)) + W21)
    Mt = transpose(M)
    P = solve(mul(Mt, M), mul(Mt, rhs))  # @line L8
    P = [[(P[i][j] + P[j][i]) / 2 for j in range(n)] for i in range(n)]
    for _ in range(2):  # @line L9
        Ak = sub(A, mul(G, P))
        P = lyap(transpose(Ak), add(Q, mul(mul(P, G), P)))
    return P


def filter_are(A, C, W, V, **kw):
    """Return the stabilizing solution S of A S + S A^T - S C^T V^-1 C S + W = 0 (by duality)."""
    return care(transpose(A), transpose(C), W, V, **kw)


def lqg(A, B, C, Q, R, W, V):
    """Return (K, L, P, S) of the LQG controller u = -K xhat."""
    P = care(A, B, Q, R)  # @line L1
    K = mul(mul(inv(R), transpose(B)), P)  # @line L2
    S = filter_are(A, C, W, V)  # @line L3
    L = mul(mul(S, transpose(C)), inv(V))  # @line L4
    return K, L, P, S  # @line L5


def controller(A, B, C, K, L):
    """Return (Ac, Bc, Cc): xhat' = Ac xhat + Bc y, u = -Cc xhat."""
    Ac = sub(sub(A, mul(B, K)), mul(L, C))
    return Ac, L, K


def closed_loop(A, B, C, K, L, gain=None):
    """Return the 2n by 2n matrix of (x, xhat) when u = -gain K xhat (gain is an m by m matrix, I if None)."""
    m = len(B[0])
    Gm = gain if gain is not None else eye(m)
    BGK = mul(mul(B, Gm), K)
    Ac, _, _ = controller(A, B, C, K, L)
    return block([[A, scale(-1, BGK)], [mul(L, C), Ac]])


def lqg_cost(A, B, C, Q, R, W, V, K, L):
    """Return the average cost J of the loop with gains K and L, from a Lyapunov equation.

    The closed-loop matrix must be Hurwitz. The noise (w, v) enters (x, xhat)
    through [[I, 0], [0, L]], and J = trace(Q X11) + trace(K^T R K X22) with
    X the stationary covariance of (x, xhat).
    """
    n, p = len(A), len(C)
    Acl = closed_loop(A, B, C, K, L)
    Bn = block([[eye(n), [[0] * p for _ in range(n)]], [[[0] * n for _ in range(n)], L]])
    N = block([[W, [[0] * p for _ in range(n)]], [[[0] * n for _ in range(p)], V]])
    X = lyap(Acl, mul(mul(Bn, N), transpose(Bn)))
    X11 = [r[:n] for r in X[:n]]
    X22 = [r[n:] for r in X[n:]]
    KRK = mul(mul(transpose(K), R), K)
    return trace(mul(Q, X11)) + trace(mul(KRK, X22))


def optimal_cost(B, R, W, K, P, S):
    """Return trace(P W) + trace(S K^T R K), the optimal LQG cost."""
    return trace(mul(P, W)) + trace(mul(S, mul(mul(transpose(K), R), K)))
