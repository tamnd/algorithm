# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fisher-vector/. The authors are listed in prov/WR6YRW.jsonl.
"""The Fisher vector of a set of local descriptors under a diagonal Gaussian mixture.

The mixture has K components with weights w[k] (positive, sum 1), means
mu[k] and standard deviations sigma[k] (lists of D floats, all positive).
For descriptors x_1..x_T the Fisher vector is the gradient of the average
log-likelihood with respect to the means and the standard deviations (and,
as an option, the soft-max weight parameters), each component scaled by the
diagonal approximation of the inverse square root of the Fisher information,
as in Sanchez, Perronnin, Mensink and Verbeek (IJCV 2013, Eq. 16 to 19).
Then the signed power rho and an L2 normalization are applied.
Layout of the output: for each k, the D mean entries, then the D sigma
entries; with include_weights=True the K weight entries come first.
Standard library only. Cost: O(T K D) time and O(K D) extra space.
"""

import math

LOG_2PI = math.log(2.0 * math.pi)


def log_gauss(x, mean, std):
    """Log density of a diagonal Gaussian at x."""
    s = 0.0
    for xi, mi, si in zip(x, mean, std):
        z = (xi - mi) / si
        s += LOG_2PI + 2.0 * math.log(si) + z * z
    return -0.5 * s


def log_mixture_terms(x, w, mu, sigma):
    """The K values log(w_k) + log N(x; mu_k, sigma_k)."""
    return [math.log(w[k]) + log_gauss(x, mu[k], sigma[k]) for k in range(len(w))]


def log_sum_exp(values):
    m = max(values)
    return m + math.log(sum(math.exp(v - m) for v in values))


def posteriors(x, w, mu, sigma, hard=False):
    """Soft assignments gamma(k) of x; with hard=True, a one-hot vector at the largest one."""
    a = log_mixture_terms(x, w, mu, sigma)
    if hard:
        k = max(range(len(a)), key=lambda j: (a[j], -j))
        return [1.0 if j == k else 0.0 for j in range(len(a))]
    m = log_sum_exp(a)
    return [math.exp(v - m) for v in a]


def log_likelihood(xs, w, mu, sigma):
    """The sum over the descriptors of log u(x), u the mixture density."""
    return sum(log_sum_exp(log_mixture_terms(x, w, mu, sigma)) for x in xs)


def raw_gradients(xs, w, mu, sigma):
    """Unnormalized gradients of log_likelihood (Sanchez et al. 2013, Section 2.2).

    Returns (g_alpha, g_mu, g_sigma): the gradient with respect to the soft-max
    parameters alpha (w = softmax(alpha)), the means and the standard deviations.
    """
    K, D = len(w), len(mu[0])
    g_alpha = [0.0] * K
    g_mu = [[0.0] * D for _ in range(K)]
    g_sigma = [[0.0] * D for _ in range(K)]
    for x in xs:
        gam = posteriors(x, w, mu, sigma)
        for k in range(K):
            g_alpha[k] += gam[k] - w[k]
            for i in range(D):
                d = x[i] - mu[k][i]
                s = sigma[k][i]
                g_mu[k][i] += gam[k] * d / (s * s)
                g_sigma[k][i] += gam[k] * (d * d / (s * s * s) - 1.0 / s)
    return g_alpha, g_mu, g_sigma


def fisher_vector(xs, w, mu, sigma, rho=0.5, normalize=True, include_weights=False, hard=False):
    """The Fisher vector of the descriptors xs (a flat list).

    rho = 1 and normalize = False give the plain normalized gradient. With
    hard = True the posteriors are replaced by a one-hot assignment.
    """
    K, D, T = len(w), len(mu[0]), len(xs)
    S0 = [0.0] * K  # @line L1
    S1 = [[0.0] * D for _ in range(K)]
    S2 = [[0.0] * D for _ in range(K)]
    for x in xs:  # @line L2
        gam = posteriors(x, w, mu, sigma, hard)  # @line L3
        for k in range(K):  # @line L4
            g = gam[k]
            if g == 0.0:
                continue
            S0[k] += g
            for i in range(D):
                z = (x[i] - mu[k][i]) / sigma[k][i]
                S1[k][i] += g * z
                S2[k][i] += g * (z * z - 1.0)
    if T == 0:
        out = [0.0] * ((K if include_weights else 0) + 2 * K * D)
        return out
    out = []
    if include_weights:
        out.extend((S0[k] - T * w[k]) / (T * math.sqrt(w[k])) for k in range(K))  # @line L5
    for k in range(K):
        out.extend(S1[k][i] / (T * math.sqrt(w[k])) for i in range(D))  # @line L6
        out.extend(S2[k][i] / (T * math.sqrt(2.0 * w[k])) for i in range(D))  # @line L7
    out = [float(t) for t in out]  # @line L8
    if rho != 1.0:  # @line L9
        out = [math.copysign(abs(t) ** rho, t) if t != 0 else 0.0 for t in out]
    if normalize:  # @line L10
        s = math.sqrt(sum(t * t for t in out))
        if s > 0.0:
            out = [t / s for t in out]
    return out  # @line L11
