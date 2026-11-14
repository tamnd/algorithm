# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/monte-carlo-tolerance-analysis/. The authors are listed in prov/XCJC4F.jsonl.

"""Monte Carlo tolerance analysis.

Each part dimension is a random variable given by a spec (kind, nominal, T):

- ("normal", m, T): normal with mean m and standard deviation T / 3;
- ("uniform", m, T): uniform on [m - T, m + T].

The assembly function f maps a dict of dimensions to the output, or to None
when the parts do not assemble. The simulation draws N independent samples
with random.Random(seed), evaluates f exactly on each, and returns the sample
mean and variance of the output and the estimated reject rate, with its
standard error and two confidence intervals.
"""

import math
import random

Z95 = 1.959963984540054  # the 0.975 quantile of the standard normal


def draw(rng, spec):
    kind, m, T = spec
    if kind == "normal":
        return rng.gauss(m, T / 3.0)
    if kind == "uniform":
        return rng.uniform(m - T, m + T)
    raise ValueError("unknown distribution %r" % (kind,))


def wald_interval(rejects, n, z=Z95):
    p = rejects / n
    h = z * math.sqrt(p * (1 - p) / n)
    return max(0.0, p - h), min(1.0, p + h)


def wilson_interval(rejects, n, z=Z95):
    p = rejects / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    h = z / d * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return max(0.0, centre - h), min(1.0, centre + h)


def zero_reject_upper_bound(n, alpha=0.05):
    """Exact one-sided upper bound on p when no reject is seen in n samples."""
    return 1 - alpha ** (1.0 / n)


def simulate(f, specs, n, seed, lower=-math.inf, upper=math.inf):
    """Run n samples. specs is a dict name -> (kind, nominal, T).

    An output outside [lower, upper], or a sample that does not assemble,
    is a reject. Mean and variance are over the samples that assemble.
    """
    rng = random.Random(seed)
    names = sorted(specs)
    rejects = 0  # @line L1
    no_fit = 0
    count, mean, m2 = 0, 0.0, 0.0
    for _ in range(n):  # @line L2
        x = {name: draw(rng, specs[name]) for name in names}  # @line L3
        y = f(x)  # @line L4
        if y is None:  # @line L5
            no_fit += 1
            rejects += 1
            continue
        if y < lower or y > upper:  # @line L6
            rejects += 1
        count += 1  # @line L7
        d = y - mean
        mean += d / count
        m2 += d * (y - mean)
    p = rejects / n  # @line L8
    se = math.sqrt(p * (1 - p) / n)
    var = m2 / (count - 1) if count > 1 else float("nan")
    return {  # @line L9
        "n": n,
        "assembled": count,
        "no_fit": no_fit,
        "mean": mean,
        "var": var,
        "rejects": rejects,
        "p": p,
        "se": se,
        "wald": wald_interval(rejects, n),
        "wilson": wilson_interval(rejects, n),
        "upper_if_zero": zero_reject_upper_bound(n) if rejects == 0 else None,
    }
