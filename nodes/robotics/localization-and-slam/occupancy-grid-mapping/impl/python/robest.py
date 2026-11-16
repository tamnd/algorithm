# SPDX-License-Identifier: MIT
# Shared helper of the robotics pages of https://algorithm.tamnd.com/. The authors are listed in prov/.

"""Small estimation helpers for the localization and SLAM pages.

Vectors are lists of floats and matrices are lists of rows, as in rbm.py.
The notation follows Thrun, Burgard and Fox, Probabilistic Robotics (2005).

  wrap_angle(a)                       a wrapped to [-pi, pi)
  gauss_sample(rng, mean, cov)        one draw of N(mean, cov), by a Cholesky factor
  gauss_pdf(x, mean, cov)             the density of N(mean, cov) at x
  mahalanobis2(x, mean, cov)          (x - mean)^T cov^(-1) (x - mean)
  low_variance_resample(rng, w)       indices of a systematic (low variance) resample
  logodds(p), prob_from_logodds(l)    l = log(p / (1 - p)) and its inverse
  CHI2[(dof, level)]                  chi-square quantiles for gates, dof 1 to 3

gauss_pdf and mahalanobis2 also take plain numbers: then cov is a variance.
This module holds no filter, no SLAM back end and no planner.
"""

import math

import rbm

CHI2 = {
    (1, 0.95): 3.841,
    (1, 0.99): 6.635,
    (2, 0.95): 5.991,
    (2, 0.99): 9.210,
    (3, 0.95): 7.815,
    (3, 0.99): 11.345,
}

_TWO_PI = 2.0 * math.pi


def wrap_angle(a):
    """Return a + 2 pi k in [-pi, pi), with ((a + pi) mod 2 pi) - pi.

    An angle that is already in [-pi, pi) comes back unchanged, so that
    small angles keep all their digits.
    """
    if -math.pi <= a < math.pi:
        return float(a)
    w = math.fmod(a + math.pi, _TWO_PI)
    if w < 0.0:
        w += _TWO_PI
    w -= math.pi
    if w >= math.pi:  # rounding can give exactly pi
        w -= _TWO_PI
    return w


def _as_vector(x):
    if isinstance(x, (int, float)):
        return [float(x)], True
    return [float(v) for v in x], False


def _as_matrix(cov, scalar):
    if scalar:
        if isinstance(cov, (int, float)):
            return [[float(cov)]]
        return [[float(cov[0][0])]]
    return [[float(v) for v in row] for row in cov]


def gauss_sample(rng, mean, cov):
    """Draw x = mean + L z, with cov = L L^T and z standard normal.

    rng is a random.Random. cov must be symmetric positive definite.
    A number for mean (with a variance for cov) gives a number.
    """
    mu, scalar = _as_vector(mean)
    if scalar:
        var = float(cov) if isinstance(cov, (int, float)) else float(cov[0][0])
        if var < 0.0:
            raise ValueError("negative variance")
        return mu[0] + math.sqrt(var) * rng.gauss(0.0, 1.0)
    L = rbm.cholesky(_as_matrix(cov, False))
    z = [rng.gauss(0.0, 1.0) for _ in mu]
    return [mu[i] + sum(L[i][j] * z[j] for j in range(i + 1)) for i in range(len(mu))]


def mahalanobis2(x, mean, cov):
    """Return the squared Mahalanobis distance (x - mean)^T cov^(-1) (x - mean)."""
    xv, scalar = _as_vector(x)
    mv, _ = _as_vector(mean)
    if len(xv) != len(mv):
        raise ValueError("x and mean differ in size")
    d = [a - b for a, b in zip(xv, mv)]
    S = _as_matrix(cov, scalar)
    if len(d) == 1:
        return d[0] * d[0] / S[0][0]
    y = rbm.solve(S, d)
    return sum(a * b for a, b in zip(d, y))


def gauss_pdf(x, mean, cov):
    """Return the density of N(mean, cov) at x."""
    xv, scalar = _as_vector(x)
    S = _as_matrix(cov, scalar)
    k = len(xv)
    det = S[0][0] if k == 1 else rbm.det(S)
    if det <= 0.0:
        raise ValueError("covariance is not positive definite")
    m2 = mahalanobis2(xv, mean if not scalar else [mean], S)
    return math.exp(-0.5 * m2) / math.sqrt((_TWO_PI ** k) * det)


def low_variance_resample(rng, weights):
    """Return len(weights) indices drawn by the low variance sampler.

    This is systematic resampling (Thrun et al. 2005, Table 4.4): one
    uniform offset r in [0, 1/N), and the N points r + m / N select the
    indices through the cumulative weights. The weights need not sum to 1.
    """
    n = len(weights)
    if n == 0:
        return []
    total = float(sum(weights))
    if total <= 0.0 or any(w < 0.0 for w in weights):
        raise ValueError("weights must be nonnegative with a positive sum")
    r = rng.random() / n
    c = weights[0] / total
    i = 0
    out = []
    for m in range(n):
        u = r + m / n
        while u > c and i < n - 1:
            i += 1
            c += weights[i] / total
        out.append(i)
    return out


def logodds(p):
    """Return log(p / (1 - p)) for p in (0, 1)."""
    if not 0.0 < p < 1.0:
        raise ValueError("p must be in (0, 1)")
    return math.log(p / (1.0 - p))


def prob_from_logodds(l):
    """Return p = 1 - 1 / (1 + exp(l)), the inverse of logodds, without overflow."""
    if l >= 0.0:
        return 1.0 / (1.0 + math.exp(-l))
    e = math.exp(l)
    return e / (1.0 + e)
