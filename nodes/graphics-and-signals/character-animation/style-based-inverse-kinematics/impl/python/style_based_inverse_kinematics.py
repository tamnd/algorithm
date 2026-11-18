# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/style-based-inverse-kinematics/. The authors are listed in prov/1FCH43.jsonl.
"""Style-based inverse kinematics (Grochow, Martin, Hertzmann and Popovic 2004).

A scaled Gaussian process latent variable model (SGPLVM) maps a latent
point x (dimension d) to a pose y (dimension D) with the kernel

    k(x, x') = alpha exp(-(gamma / 2) |x - x'|^2) + delta(x, x') / beta.

For the training latents X and poses Y (centered by their mean mu), the
model gives a mean and a variance at any x:

    f(x) = mu + Y^T K^(-1) k(x),   s2(x) = k(x, x) - k(x)^T K^(-1) k(x).

The inverse kinematics objective is the negative log likelihood of a pose,

    L_IK(x, y) = |W (y - f(x))|^2 / (2 s2(x)) + (D / 2) ln s2(x) + |x|^2 / 2,

plus a soft constraint (lam / 2) |g(y) - p|^2 on the end effector position
g(y). Both x and y are unknowns. The code minimizes the sum by BFGS with
a backtracking line search, using the analytic gradient. The paper uses
SQP and L-BFGS.

The latent points and the hyperparameters are inputs. The paper learns
them from the motion capture data by maximizing the likelihood of the
model; that step is not part of this file. The chain is a planar arm with
the joint angles y and the link lengths in LENGTHS.
"""

import math

from anim import dot, solve

LENGTHS = (1.0, 0.8, 0.6)


def kernel(a, b, alpha, gamma):
    """Return the RBF part alpha exp(-(gamma / 2) |a - b|^2)."""
    return alpha * math.exp(-0.5 * gamma * sum((x - y) ** 2 for x, y in zip(a, b)))


class SGPLVM:
    """A trained model: latents X, poses Y, hyperparameters and scaling W."""

    def __init__(self, latents, poses, alpha=1.0, gamma=1.0, beta=100.0, scale=None):
        self.x = [list(p) for p in latents]
        n, dim = len(poses), len(poses[0])
        self.mu = [sum(p[k] for p in poses) / n for k in range(dim)]
        self.y = [[p[k] - self.mu[k] for k in range(dim)] for p in poses]
        self.alpha, self.gamma, self.beta = alpha, gamma, beta
        self.w = list(scale) if scale is not None else [1.0] * dim
        kmat = [[kernel(a, b, alpha, gamma) + (1.0 / beta if i == j else 0.0) for j, b in enumerate(self.x)] for i, a in enumerate(self.x)]
        eye = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
        self.kinv = solve(kmat, eye)  # K^(-1), once
        self.kinv_y = [[sum(self.kinv[i][j] * self.y[j][k] for j in range(n)) for k in range(dim)] for i in range(n)]

    def predict(self, x):
        """Return (f, s2, df, ds2): the mean, the variance and their gradients in x."""
        n, dim, d = len(self.x), len(self.mu), len(x)
        kx = [kernel(x, xj, self.alpha, self.gamma) for xj in self.x]
        dk = [[-self.gamma * (x[c] - xj[c]) * kv for c in range(d)] for xj, kv in zip(self.x, kx)]
        f = [self.mu[k] + sum(self.kinv_y[j][k] * kx[j] for j in range(n)) for k in range(dim)]
        df = [[sum(self.kinv_y[j][k] * dk[j][c] for j in range(n)) for c in range(d)] for k in range(dim)]
        a = [sum(self.kinv[i][j] * kx[j] for j in range(n)) for i in range(n)]
        s2 = self.alpha + 1.0 / self.beta - dot(kx, a)
        ds2 = [-2.0 * sum(a[j] * dk[j][c] for j in range(n)) for c in range(d)]
        return f, s2, df, ds2


def end_effector(y):
    """Return the end position of the planar chain and its Jacobian (2 by D)."""
    th = 0.0
    px = py = 0.0
    pts = []
    for ang, ln in zip(y, LENGTHS):
        th += ang
        px += ln * math.cos(th)
        py += ln * math.sin(th)
        pts.append((th, ln))
    jac = [[0.0] * len(y) for _ in range(2)]
    for i in range(len(y)):
        for th_k, ln in pts[i:]:
            jac[0][i] -= ln * math.sin(th_k)
            jac[1][i] += ln * math.cos(th_k)
    return (px, py), jac


def objective(model, z, target, lam):
    """Return (E, gradient) for z = (x, y) with the soft constraint of weight lam."""
    d = len(model.x[0])
    x, y = z[:d], z[d:]
    dim = len(y)
    f, s2, df, ds2 = model.predict(x)
    r = [model.w[k] * (y[k] - f[k]) for k in range(dim)]
    rr = dot(r, r)
    e = rr / (2.0 * s2) + 0.5 * dim * math.log(s2) + 0.5 * dot(x, x)  # @line L4
    gx = [0.0] * d
    gy = [model.w[k] * r[k] / s2 for k in range(dim)]
    for c in range(d):
        gx[c] = -sum(model.w[k] * r[k] * df[k][c] for k in range(dim)) / s2
        gx[c] += (-rr / (2.0 * s2 * s2) + 0.5 * dim / s2) * ds2[c] + x[c]
    if lam:
        p, jac = end_effector(y)  # @line L5
        res = (p[0] - target[0], p[1] - target[1])
        e += 0.5 * lam * dot(res, res)
        for k in range(dim):
            gy[k] += lam * (jac[0][k] * res[0] + jac[1][k] * res[1])
    return e, gx + gy


def style_ik(model, target, x0, y0=None, lam=1e3, max_iter=500, gtol=1e-9):
    """Return (x, y, history) minimizing L_IK(x, y) + (lam / 2) |g(y) - target|^2.

    The start is x0 and y0 = f(x0) if y0 is None. The minimizer is BFGS
    with a backtracking (Armijo) line search; history holds E after each
    accepted step. With lam = 0 there is no constraint and target is unused.
    """
    d = len(x0)
    if y0 is None:
        y0 = model.predict(list(x0))[0]
    z = list(x0) + list(y0)  # @line L1
    nz = len(z)
    h = [[1.0 if i == j else 0.0 for j in range(nz)] for i in range(nz)]  # inverse Hessian estimate
    e, g = objective(model, z, target, lam)  # @line L2
    history = [e]
    for _ in range(max_iter):  # @line L3
        if math.sqrt(dot(g, g)) <= gtol:  # @line L8
            break
        p = [-sum(h[i][j] * g[j] for j in range(nz)) for i in range(nz)]  # @line L6
        slope = dot(p, g)
        if slope >= 0.0:
            h = [[1.0 if i == j else 0.0 for j in range(nz)] for i in range(nz)]
            p = [-x for x in g]
            slope = -dot(g, g)
        step = 1.0
        while True:
            z2 = [a + step * b for a, b in zip(z, p)]
            e2, g2 = objective(model, z2, target, lam)
            if e2 <= e + 1e-4 * step * slope:
                break
            step *= 0.5
            if step < 1e-16:
                return z[:d], z[d:], history
        s = [a - b for a, b in zip(z2, z)]
        yv = [a - b for a, b in zip(g2, g)]
        sy = dot(s, yv)
        if sy > 1e-14 * math.sqrt(dot(s, s) * dot(yv, yv)):  # BFGS update of the inverse Hessian
            hy = [sum(h[i][j] * yv[j] for j in range(nz)) for i in range(nz)]
            yhy = dot(yv, hy)
            for i in range(nz):
                for j in range(nz):
                    h[i][j] += (sy + yhy) * s[i] * s[j] / (sy * sy) - (hy[i] * s[j] + s[i] * hy[j]) / sy
        z, e, g = z2, e2, g2  # @line L7
        history.append(e)
        if max(abs(x) for x in s) <= 1e-13 * (1.0 + max(abs(x) for x in z)):
            break  # the steps are below the rounding level of z
    return z[:d], z[d:], history  # @line L9
