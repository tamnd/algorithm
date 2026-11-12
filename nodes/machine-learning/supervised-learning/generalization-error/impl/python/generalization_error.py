# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalization-error/. The authors are listed in prov/3V7ENF.jsonl.
"""True risk, empirical risk and the generalization gap, with the Hoeffding and union bounds.

The experiment: the domain is {0, ..., N - 1}, x is uniform and the label y is a fair coin that does not
depend on x. So every classifier h has true risk L_D(h) = 1/2 under the zero-one loss. The class H holds
k fixed random classifiers. For one classifier fixed before the sample, Hoeffding's inequality bounds the
gap. For the classifier that empirical risk minimization picks, the same bound fails, and the union
bound over H restores it.
"""

import math
import random
from fractions import Fraction


def hoeffding_epsilon(n: int, delta: float) -> float:
    """The epsilon with P(|L_S(h) - L_D(h)| > epsilon) <= delta for one fixed h and a loss in [0, 1]."""
    return math.sqrt(math.log(2 / delta) / (2 * n))


def union_epsilon(n: int, delta: float, k: int) -> float:
    """The same for all h of a class of size k at once (Hoeffding plus the union bound)."""
    return math.sqrt(math.log(2 * k / delta) / (2 * n))


def binomial_cdf(n: int, t: int) -> Fraction:
    """P(Bin(n, 1/2) <= t), exactly."""
    return Fraction(sum(math.comb(n, i) for i in range(t + 1)), 2 ** n)


def prob_min_at_most(n: int, k: int, t: int) -> Fraction:
    """P(min of k independent Bin(n, 1/2) <= t), exactly."""
    return 1 - (1 - binomial_cdf(n, t)) ** k


def random_class(k: int, size: int, rng: random.Random) -> list[int]:
    """k classifiers on {0, ..., size - 1}; classifier j is the bit string h[j], h_j(x) = bit x of h[j]."""
    return [rng.getrandbits(size) for _ in range(k)]


def empirical_risks(h: list[int], xs: list[int], ys: list[int]) -> list[Fraction]:
    """L_S(h_j) under the zero-one loss, for each classifier."""
    n = len(xs)
    return [Fraction(sum(((hj >> x) & 1) != y for x, y in zip(xs, ys)), n) for hj in h]


def experiment(k: int, n: int, size: int, delta: float, trials: int, rng: random.Random) -> dict:
    """Fractions of trials where (a) the fixed h_0, (b) the ERM choice, (c) some h of H, has a gap above
    the bound named in the key. The true risk of every classifier is 1/2."""
    h = random_class(k, size, rng)
    e1, ek = hoeffding_epsilon(n, delta), union_epsilon(n, delta, k)
    fixed = erm = anyh = 0
    for _ in range(trials):
        xs = [rng.randrange(size) for _ in range(n)]
        ys = [rng.getrandbits(1) for _ in range(n)]
        risks = empirical_risks(h, xs, ys)
        fixed += abs(Fraction(1, 2) - risks[0]) > e1
        erm += Fraction(1, 2) - min(risks) > e1
        anyh += max(abs(Fraction(1, 2) - r) for r in risks) > ek
    return {"eps_fixed": e1, "eps_union": ek, "fixed": fixed / trials, "erm": erm / trials,
            "any_union": anyh / trials}


if __name__ == "__main__":
    print(experiment(200, 50, 1 << 12, 0.05, 400, random.Random(1)))
    t = math.ceil(50 * (0.5 - hoeffding_epsilon(50, 0.05))) - 1
    print(t, float(binomial_cdf(50, t)), float(prob_min_at_most(50, 200, t)))
