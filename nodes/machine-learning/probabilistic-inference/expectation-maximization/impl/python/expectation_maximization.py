# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/expectation-maximization/. The authors are listed in prov/X3E38Q.jsonl.

"""The EM algorithm, with two instances: the genetic linkage multinomial of Dempster, Laird
and Rubin (1977) and the two coin mixture of Do and Batzoglou (2008)."""

import math


def em(theta, e_step, m_step, loglik, eps=1e-12, max_iter=1000):
    """Run EM from theta. Return (the last theta, the list of log likelihoods, one per iterate).

    e_step(theta) returns the expected sufficient statistics of the complete data under
    p(z | x, theta); m_step(stats) returns the theta that maximizes the expected complete
    log likelihood. loglik(theta) is the observed-data log likelihood.
    """
    history = [loglik(theta)]  # @line L1
    for _ in range(max_iter):  # @line L2
        stats = e_step(theta)  # @line L3
        theta = m_step(stats)  # @line L4
        history.append(loglik(theta))  # @line L5
        if history[-1] - history[-2] < eps:  # @line L6
            break
    return theta, history  # @line L7


# ---------------------------------------------------------------- genetic linkage

LINKAGE = (125, 18, 20, 34)  # Rao (1973), as used in Dempster, Laird and Rubin (1977)


def linkage_loglik(theta, y=LINKAGE):
    """Observed log likelihood, without the multinomial constant.

    The cell probabilities are (1/2 + theta/4, (1 - theta)/4, (1 - theta)/4, theta/4).
    """
    return (y[0] * math.log(0.5 + theta / 4) + (y[1] + y[2]) * math.log((1 - theta) / 4)
            + y[3] * math.log(theta / 4))


def linkage_e_step(theta, y=LINKAGE):
    """Split the first cell into 1/2 and theta/4; return the expected count of the theta/4 part."""
    return y[0] * (theta / 4) / (0.5 + theta / 4)


def linkage_m_step(x2, y=LINKAGE):
    """Complete data counts (x1, x2, y2, y3, y4) are binomial in theta: theta = (x2 + y4) / (x2 + y2 + y3 + y4)."""
    return (x2 + y[3]) / (x2 + y[1] + y[2] + y[3])


def linkage_em(theta0=0.5, eps=1e-12):
    return em(theta0, linkage_e_step, linkage_m_step, linkage_loglik, eps)


def linkage_mle(y=LINKAGE):
    """The exact maximizer: the positive root of n theta^2 - (y1 - 2 y2 - 2 y3 - y4) theta - 2 y4 = 0."""
    n = sum(y)
    b = y[0] - 2 * (y[1] + y[2]) - y[3]
    return (b + math.sqrt(b * b + 8 * n * y[3])) / (2 * n)


# ---------------------------------------------------------------- two coins

def _log_binom(h, n, p):
    return h * math.log(p) + (n - h) * math.log(1 - p)


def coins_loglik(theta, data):
    """theta = (lam, pa, pb): the chance of coin A, and the head probabilities of A and B.
    data is a list of (heads, tosses) for sets of tosses with one hidden coin each.
    The binomial coefficients are left out; they do not depend on theta."""
    lam, pa, pb = theta
    total = 0.0
    for h, n in data:
        la = math.log(lam) + _log_binom(h, n, pa)
        lb = math.log(1 - lam) + _log_binom(h, n, pb)
        mx = max(la, lb)
        total += mx + math.log(math.exp(la - mx) + math.exp(lb - mx))
    return total


def coins_e_step(theta, data):
    """Return the responsibilities r_i = P(coin A | set i) and the data."""
    lam, pa, pb = theta
    resp = []
    for h, n in data:
        la = math.log(lam) + _log_binom(h, n, pa)
        lb = math.log(1 - lam) + _log_binom(h, n, pb)
        resp.append(1.0 / (1.0 + math.exp(lb - la)))
    return resp, data


def coins_m_step(stats, learn_lambda=True, lam_fixed=0.5):
    """Weighted head frequencies; the mixing weight is the mean responsibility unless it is fixed."""
    resp, data = stats
    ha = sum(r * h for r, (h, n) in zip(resp, data))
    na = sum(r * n for r, (h, n) in zip(resp, data))
    hb = sum((1 - r) * h for r, (h, n) in zip(resp, data))
    nb = sum((1 - r) * n for r, (h, n) in zip(resp, data))
    lam = sum(resp) / len(resp) if learn_lambda else lam_fixed
    return (lam, ha / na, hb / nb)


def coins_em(theta0, data, learn_lambda=True, eps=1e-12, max_iter=1000):
    return em(theta0,
              lambda th: coins_e_step(th, data),
              lambda st: coins_m_step(st, learn_lambda, theta0[0]),
              lambda th: coins_loglik(th, data), eps, max_iter)


# Do and Batzoglou (2008), Figure 1: five sets of ten tosses.
DO_BATZOGLOU = [(5, 10), (9, 10), (8, 10), (4, 10), (7, 10)]
