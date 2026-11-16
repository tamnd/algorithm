# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/joint-probabilistic-data-association/. The authors are listed in prov/GVT723.jsonl.
"""Joint probabilistic data association (JPDA), the parametric form.

A known set of n tracks is updated with the m measurements of one frame. A
joint event gives each track at most one measurement inside its gate and each
measurement at most one track; the other measurements are clutter. The weight
of an event is the product of pD L_ij / lam over its pairs and of (1 - pD pG)
over its missed tracks, where L_ij is the Gaussian density of the innovation,
lam the clutter density, pD the detection probability and pG the gate
probability. The marginal probability beta_ij that measurement j belongs to
track i is the normalized sum of the weights of the events that hold the pair.
Each track is then updated with the PDA formulas. The events are enumerated, so
the cost grows exponentially with the size of a cluster of close tracks.
Matrices are lists of rows.
"""

import math

INF = float("inf")


def mat_mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(r) for r in zip(*a)]


def mat_add(a, b):
    return [[x + y for x, y in zip(r, s)] for r, s in zip(a, b)]


def mat_sub(a, b):
    return [[x - y for x, y in zip(r, s)] for r, s in zip(a, b)]


def mat_scale(a, f):
    return [[f * x for x in r] for r in a]


def inverse_and_det(a):
    """Inverse and determinant of a small nonsingular matrix by Gauss-Jordan elimination."""
    n = len(a)
    m = [list(map(float, r)) + [1.0 if i == j else 0.0 for j in range(n)] for i, r in enumerate(a)]
    det = 1.0
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        if abs(m[p][c]) < 1e-300:
            raise ValueError("singular matrix")
        if p != c:
            m[c], m[p] = m[p], m[c]
            det = -det
        piv = m[c][c]
        det *= piv
        m[c] = [x / piv for x in m[c]]
        for r in range(n):
            if r != c and m[r][c] != 0.0:
                f = m[r][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [r[n:] for r in m], det


def gaussian_density(nu, s):
    """Density of N(0, s) at the vector nu, and the squared Mahalanobis distance."""
    s_inv, det = inverse_and_det(s)
    col = [[x] for x in nu]
    d2 = mat_mul(mat_mul(transpose(col), s_inv), col)[0][0]
    return math.exp(-0.5 * d2) / math.sqrt((2 * math.pi) ** len(nu) * det), d2


def jpda_betas(lik, p_d, p_g, lam):
    """Association probabilities of JPDA by enumeration of the joint events (lines L3 to L5).

    lik[i][j] is the likelihood L_ij of measurement j for track i, or None
    outside the gate. Returns (beta, beta0, c, events): beta[i][j] is the
    probability that measurement j is from track i, beta0[i] the probability
    that track i has no measurement, c the sum of the event weights, and
    events the number of joint events.
    """
    n = len(lik)
    m = len(lik[0]) if n else 0
    miss = 1.0 - p_d * p_g
    acc = [[0.0] * m for _ in range(n)]
    total = [0.0]
    count = [0]
    chosen = [-1] * n
    used = [False] * m

    def visit(i, w):
        if i == n:
            total[0] += w
            count[0] += 1
            for t in range(n):
                if chosen[t] >= 0:
                    acc[t][chosen[t]] += w
            return
        chosen[i] = -1
        visit(i + 1, w * miss)  # track i is missed
        for j in range(m):  # @line L3
            if lik[i][j] is not None and not used[j]:
                used[j], chosen[i] = True, j
                visit(i + 1, w * p_d * lik[i][j] / lam)  # @line L4
                used[j], chosen[i] = False, -1

    visit(0, 1.0)
    c = total[0]  # @line L5
    beta = [[a / c for a in row] for row in acc]
    beta0 = [1.0 - sum(row) for row in beta]
    return beta, beta0, c, count[0]


def pda_update(x_pred, p_pred, z_hat, s, k, zs, beta_row, beta0):
    """PDA state and covariance update of one track (lines L6 and L7)."""
    nus = [[[z[a] - z_hat[a]] for a in range(len(z))] for z in zs]
    nu = [[0.0] for _ in z_hat]
    for b, v in zip(beta_row, nus):
        nu = mat_add(nu, mat_scale(v, b))
    x = mat_add(x_pred, mat_mul(k, nu))  # @line L6
    spread = mat_scale(mat_mul(nu, transpose(nu)), -1.0)
    for b, v in zip(beta_row, nus):
        spread = mat_add(spread, mat_scale(mat_mul(v, transpose(v)), b))
    kskt = mat_mul(mat_mul(k, s), transpose(k))
    p_c = mat_sub(p_pred, kskt)
    p = mat_add(mat_add(mat_scale(p_pred, beta0), mat_scale(p_c, 1.0 - beta0)), mat_mul(mat_mul(k, spread), transpose(k)))  # @line L7
    return x, p


def cv_model(q, r):
    """Constant velocity model in 2D with a time step of 1: F, Q, H, R."""
    f = [[1.0, 0.0, 1.0, 0.0], [0.0, 1.0, 0.0, 1.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
    qm = [[q / 3, 0.0, q / 2, 0.0], [0.0, q / 3, 0.0, q / 2], [q / 2, 0.0, q, 0.0], [0.0, q / 2, 0.0, q]]
    h = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0]]
    rm = [[r, 0.0], [0.0, r]]
    return f, qm, h, rm


def jpda_step(tracks, zs, model, p_d, p_g, lam, gamma):
    """One frame of JPDA for a fixed set of tracks, each a pair (x, P). Returns the new tracks."""
    f, q, h, r = model
    pred = []
    for x, p in tracks:  # @line L1
        xp = mat_mul(f, x)
        pp = mat_add(mat_mul(mat_mul(f, p), transpose(f)), q)
        ph = mat_mul(pp, transpose(h))
        s = mat_add(mat_mul(h, ph), r)
        s_inv, _ = inverse_and_det(s)
        z_hat = [row[0] for row in mat_mul(h, xp)]
        pred.append((xp, pp, z_hat, s, mat_mul(ph, s_inv)))
    lik = []
    for xp, pp, z_hat, s, k in pred:  # @line L2
        row = []
        for z in zs:
            dens, d2 = gaussian_density([a - b for a, b in zip(z, z_hat)], s)
            row.append(dens if d2 <= gamma else None)
        lik.append(row)
    beta, beta0, _, _ = jpda_betas(lik, p_d, p_g, lam)
    out = []
    for i, (xp, pp, z_hat, s, k) in enumerate(pred):
        out.append(pda_update(xp, pp, z_hat, s, k, zs, beta[i], beta0[i]))
    return out
