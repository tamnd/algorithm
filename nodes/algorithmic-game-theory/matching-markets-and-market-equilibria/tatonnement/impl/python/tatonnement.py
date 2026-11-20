# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tatonnement/. The authors are listed in prov/ZA6PKF.jsonl.
"""Discrete tatonnement: move each price in the direction of its excess demand.

A market is given by an excess demand function z(p) -> list of floats, one per good, and the
supply s_j of each good. The multiplicative rule p_j <- p_j (1 + step * min(z_j / s_j, 1)) keeps
prices positive for 0 < step < 1. The additive rule p <- p + step * z is the Euler scheme of the
continuous process dp/dt = z(p) of Arrow, Block and Hurwicz. All arithmetic is floating point;
convergence means max_j |z_j| / s_j <= tol.
"""


def tatonnement(excess, p0, step, rounds, tol, supply=None):
    """Run the multiplicative rule. Return (p, t, converged), where t is the number of updates."""
    m = len(p0)
    s = supply or [1.0] * m
    p = [float(q) for q in p0]  # @line L1
    for t in range(rounds):  # @line L2
        z = excess(p)  # @line L3
        if max(abs(z[j]) / s[j] for j in range(m)) <= tol:  # @line L4
            return p, t, True
        p = [p[j] * (1 + step * min(z[j] / s[j], 1.0)) for j in range(m)]  # @line L5
    z = excess(p)
    return p, rounds, max(abs(z[j]) / s[j] for j in range(m)) <= tol  # @line L6


def tatonnement_additive(excess, p0, step, rounds):
    """Run the additive rule p <- p + step * z(p) and return the list of all price vectors."""
    path = [[float(q) for q in p0]]
    for _ in range(rounds):
        p = path[-1]
        z = excess(p)
        path.append([p[j] + step * z[j] for j in range(len(p))])
    return path


# Excess demand functions of some markets with one unit of each good.

def fisher_cobb_douglas(a, budgets):
    """Fisher market, buyer i spends the share a[i][j] of her budget on good j."""
    def z(p):
        return [sum(a[i][j] * budgets[i] for i in range(len(a))) / p[j] - 1 for j in range(len(p))]
    return z


def fisher_ces(a, budgets, rho):
    """Fisher market with CES utilities (sum_j a_ij x_ij^rho)^(1 / rho), 0 != rho < 1.
    For 0 < rho < 1 the goods are gross substitutes."""
    sigma = 1 / (1 - rho)

    def z(p):
        out = [-1.0] * len(p)
        for i, row in enumerate(a):
            denom = sum(row[k] ** sigma * p[k] ** (1 - sigma) for k in range(len(p)) if row[k] > 0)
            for j in range(len(p)):
                if row[j] > 0:
                    out[j] += budgets[i] * row[j] ** sigma * p[j] ** (-sigma) / denom
        return out
    return z


def fisher_linear(u, budgets):
    """Fisher market with linear utilities, where each buyer has a single best good. The demand is
    not a function at prices where a buyer is indifferent, so those prices raise an error."""
    def z(p):
        out = [-1.0] * len(p)
        for i, row in enumerate(u):
            bang = [row[j] / p[j] for j in range(len(p))]
            best = max(bang)
            top = [j for j in range(len(p)) if bang[j] == best]
            if len(top) > 1:
                raise ValueError("buyer %d has several best goods" % i)
            out[top[0]] += budgets[i] / p[top[0]]
        return out
    return z


def scarf(p):
    """Scarf's exchange economy: consumer j owns one unit of good j and wants goods j and j + 1 in
    equal amounts (indices mod 3). The equilibrium prices are the multiples of (1, 1, 1)."""
    m = len(p)
    return [p[j - 1] / (p[j - 1] + p[j]) - p[(j + 1) % m] / (p[j] + p[(j + 1) % m]) for j in range(m)]
