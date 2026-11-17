# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/closed-form-matting/. The authors are listed in prov/YQKAHR.jsonl.

"""Closed-form matting of Levin, Lischinski and Weiss (CVPR 2006).

Pixel p = v * w + u is (u, v). img[v][u] is a gray value (a number) or a
color (a list of 3 numbers). The matting Laplacian L sums, over every 3 x 3
window w_k that lies inside the image,

    L_ij += delta_ij - (1 + (I_i - mu_k)^T (Sigma_k + eps / |w_k| Id)^-1 (I_j - mu_k)) / |w_k|

for the pixels i, j of the window, with the mean mu_k and the covariance
Sigma_k (divided by |w_k|) of the window. The matte minimizes alpha^T L alpha
with alpha fixed on the scribbled pixels. L is dense here, so the code suits
small images only.
"""

from cvla import inv, solve, zeros

WINDOW_RADIUS = 1


def pixel_vectors(img):
    """The pixels in the order p = v * w + u, each as a list of channels."""
    out = []
    for row in img:
        for x in row:
            out.append([float(c) for c in x] if isinstance(x, (list, tuple)) else [float(x)])
    return out


def windows(h, w, r=WINDOW_RADIUS):
    """The pixel lists of all (2r+1) x (2r+1) windows inside the image."""
    out = []
    for v in range(r, h - r):
        for u in range(r, w - r):
            out.append([(v + dv) * w + (u + du) for dv in range(-r, r + 1) for du in range(-r, r + 1)])
    return out


def window_stats(vec, win):
    """The mean vector and the covariance matrix (divided by |w|) of a window."""
    c = len(vec[0])
    m = len(win)
    mu = [sum(vec[i][a] for i in win) / m for a in range(c)]
    cov = [[sum((vec[i][a] - mu[a]) * (vec[i][b] - mu[b]) for i in win) / m for b in range(c)] for a in range(c)]
    return mu, cov


def matting_laplacian(img, eps):
    """The dense N x N matting Laplacian of equations 5 (gray) and 12 (color)."""
    h, w = len(img), len(img[0])
    vec = pixel_vectors(img)
    c = len(vec[0])
    n = h * w
    lap = zeros(n, n)  # @line L1
    for win in windows(h, w):  # @line L2
        m = len(win)
        mu, cov = window_stats(vec, win)  # @line L3
        reg = [[cov[a][b] + (eps / m if a == b else 0.0) for b in range(c)] for a in range(c)]
        minv = inv(reg)  # @line L4
        cen = [[vec[i][a] - mu[a] for a in range(c)] for i in win]
        proj = [[sum(minv[a][b] * x[b] for b in range(c)) for a in range(c)] for x in cen]
        for ii, i in enumerate(win):
            for jj, j in enumerate(win):
                q = sum(cen[ii][a] * proj[jj][a] for a in range(c))
                lap[i][j] += (1.0 if i == j else 0.0) - (1.0 + q) / m  # @line L5
    return lap


def solve_matte(lap, scribbles):
    """Minimize alpha^T L alpha subject to alpha_i = s_i for i in scribbles (equation 13)."""
    n = len(lap)
    alpha = [0.0] * n
    free = [p for p in range(n) if p not in scribbles]  # @line L6
    for p, s in scribbles.items():
        alpha[p] = float(s)
    if free:
        luu = [[lap[i][j] for j in free] for i in free]
        rhs = [-sum(lap[i][p] * s for p, s in scribbles.items()) for i in free]
        xu = solve(luu, rhs)  # @line L7
        for r, p in enumerate(free):
            alpha[p] = xu[r]
    return alpha  # @line L8


def closed_form_matting(img, scribbles, eps=1e-4):
    """The alpha matte of img from scribbles {pixel: 0 or 1 (or any value)}."""
    return solve_matte(matting_laplacian(img, eps), scribbles)


def quadratic_form(lap, x):
    return sum(x[i] * sum(lap[i][j] * x[j] for j in range(len(x))) for i in range(len(x)))


def cost_j(img, alpha, eps):
    """min over (a_k, b_k) of the cost J(alpha, a, b) of equations 3 and 10,
    computed window by window from the normal equations of the least squares."""
    h, w = len(img), len(img[0])
    vec = pixel_vectors(img)
    c = len(vec[0])
    total = 0.0
    for win in windows(h, w):
        rows = [vec[i] + [1.0] for i in win]
        ata = [[sum(r[a] * r[b] for r in rows) + (eps if a == b and a < c else 0.0)
                for b in range(c + 1)] for a in range(c + 1)]
        atb = [sum(r[a] * alpha[i] for r, i in zip(rows, win)) for a in range(c + 1)]
        coef = solve(ata, atb)
        res = sum((alpha[i] - sum(coef[a] * r[a] for a in range(c + 1))) ** 2 for r, i in zip(rows, win))
        total += res + eps * sum(coef[a] ** 2 for a in range(c))
    return total


def composite(alpha, fg, bg):
    """I_i = alpha_i F_i + (1 - alpha_i) B_i for flat lists of numbers or of colors."""
    out = []
    for a, f, b in zip(alpha, fg, bg):
        if isinstance(f, (list, tuple)):
            out.append([a * x + (1 - a) * y for x, y in zip(f, b)])
        else:
            out.append(a * f + (1 - a) * b)
    return out
