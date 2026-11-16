# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phd-filter/. The authors are listed in prov/9HR0MT.jsonl.
"""The Gaussian mixture probability hypothesis density filter (Vo and Ma, 2006).

The PHD D(x) of a multi-target state is a density on the single-target state
space whose integral over a region is the expected number of targets in it.
With linear Gaussian motion and measurement models, constant survival and
detection probabilities pS and pD, and a Gaussian mixture birth intensity, a
Gaussian mixture PHD stays a Gaussian mixture after the prediction and the
update. A component is a triple (w, m, P) of a weight, a mean (a list) and a
covariance (a list of rows). The clutter intensity kappa(z) is a function of
the measurement. Pruning and merging keep the number of components bounded.
"""

import math


def mat_mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(r) for r in zip(*a)]


def mat_add(a, b):
    return [[x + y for x, y in zip(r, s)] for r, s in zip(a, b)]


def mat_vec(a, v):
    return [sum(x * y for x, y in zip(r, v)) for r in a]


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


def quad(v, a_inv):
    """The quadratic form v^T A^-1 v."""
    return sum(v[i] * sum(a_inv[i][j] * v[j] for j in range(len(v))) for i in range(len(v)))


def gaussian(z, mean, cov):
    """The density N(z; mean, cov)."""
    inv, det = inverse_and_det(cov)
    nu = [a - b for a, b in zip(z, mean)]
    return math.exp(-0.5 * quad(nu, inv)) / math.sqrt((2 * math.pi) ** len(z) * det)


def predict(comps, f, q, p_s, birth):
    """Prediction of a Gaussian mixture PHD (lines L1 and L2)."""
    out = []
    ft = transpose(f)
    for w, m, p in comps:  # @line L1
        out.append((p_s * w, mat_vec(f, m), mat_add(mat_mul(mat_mul(f, p), ft), q)))
    out.extend(birth)  # @line L2
    return out


def update(comps, zs, h, r, p_d, kappa):
    """Update of a Gaussian mixture PHD with the measurements zs (lines L3 to L5)."""
    ht = transpose(h)
    d = len(comps[0][1]) if comps else 0
    parts = []
    for w, m, p in comps:  # @line L3
        ph = mat_mul(p, ht)
        s = mat_add(mat_mul(h, ph), r)
        s_inv, s_det = inverse_and_det(s)
        k = mat_mul(ph, s_inv)
        kh = mat_mul(k, h)
        p_upd = mat_add(p, [[-x for x in row] for row in mat_mul(kh, p)])
        p_upd = [[0.5 * (p_upd[i][j] + p_upd[j][i]) for j in range(d)] for i in range(d)]
        parts.append((mat_vec(h, m), s_inv, s_det, k, p_upd))
    out = [((1.0 - p_d) * w, m, p) for (w, m, p) in comps]  # @line L4
    for z in zs:  # @line L5
        terms = []
        for (w, m, p), (eta, s_inv, s_det, k, p_upd) in zip(comps, parts):
            nu = [a - b for a, b in zip(z, eta)]
            lik = math.exp(-0.5 * quad(nu, s_inv)) / math.sqrt((2 * math.pi) ** len(z) * s_det)
            terms.append((p_d * w * lik, [a + b for a, b in zip(m, mat_vec(k, nu))], p_upd))
        denom = kappa(z) + sum(t[0] for t in terms)
        out.extend((wz / denom, mz, pz) for wz, mz, pz in terms)
    return out


def prune_and_merge(comps, threshold=1e-5, merge_dist=4.0, max_comps=100):
    """Drop the components with a small weight, merge close ones, keep the largest (line L6)."""
    rest = [c for c in comps if c[0] > threshold]
    invs = [inverse_and_det(c[2])[0] for c in rest]
    alive = list(range(len(rest)))
    merged = []
    while alive:
        j = max(alive, key=lambda i: rest[i][0])
        mj = rest[j][1]
        group = [i for i in alive if quad([a - b for a, b in zip(rest[i][1], mj)], invs[i]) <= merge_dist]
        wt = sum(rest[i][0] for i in group)
        d = len(mj)
        mean = [sum(rest[i][0] * rest[i][1][a] for i in group) / wt for a in range(d)]
        cov = [[0.0] * d for _ in range(d)]
        for i in group:
            w, m, p = rest[i]
            dm = [a - b for a, b in zip(mean, m)]
            for a in range(d):
                for b in range(d):
                    cov[a][b] += w * (p[a][b] + dm[a] * dm[b])
        cov = [[x / wt for x in row] for row in cov]
        merged.append((wt, mean, cov))
        gs = set(group)
        alive = [i for i in alive if i not in gs]
    merged.sort(key=lambda c: -c[0])
    return merged[:max_comps]


def extract(comps):
    """The expected number of targets and the state estimates (line L7)."""
    n_hat = sum(c[0] for c in comps)  # @line L7
    states = []
    for w, m, _ in comps:
        if w > 0.5:
            states.extend([list(m)] * int(round(w)))
    return n_hat, states


def phd_step(comps, zs, model, p_s, p_d, kappa, birth, threshold=1e-5, merge_dist=4.0, max_comps=100):
    """One frame of the GM-PHD filter. Returns (components, expected number, state estimates)."""
    f, q, h, r = model
    comps = predict(comps, f, q, p_s, birth)
    comps = update(comps, zs, h, r, p_d, kappa)
    comps = prune_and_merge(comps, threshold, merge_dist, max_comps)  # @line L6
    n_hat, states = extract(comps)
    return comps, n_hat, states


def phd_density(comps, x):
    """The value of the Gaussian mixture PHD at the state x."""
    return sum(w * gaussian(x, m, p) for w, m, p in comps)


def cv_model(q, r):
    """Constant velocity model in 2D with a time step of 1: F, Q, H, R."""
    f = [[1.0, 0.0, 1.0, 0.0], [0.0, 1.0, 0.0, 1.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
    qm = [[q / 3, 0.0, q / 2, 0.0], [0.0, q / 3, 0.0, q / 2], [q / 2, 0.0, q, 0.0], [0.0, q / 2, 0.0, q]]
    h = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0]]
    rm = [[r, 0.0], [0.0, r]]
    return f, qm, h, rm
