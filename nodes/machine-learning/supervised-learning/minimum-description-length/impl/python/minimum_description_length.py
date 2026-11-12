# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-description-length/. The authors are listed in prov/71J32F.jsonl.
"""Two-part MDL for choosing the number of bins of a histogram.

The data are n integers in {0, ..., N - 1}, N = 2^B. The model with K = 2^j equal bins (j = 0..B) is
coded in four parts, each an ideal code length in bits:

  1. j, uniform over the B + 1 choices:             log2(B + 1)
  2. the bin counts (n_1, ..., n_K), uniform over
     the C(n + K - 1, K - 1) compositions of n:      log2 C(n + K - 1, K - 1)
  3. the sequence of bin labels, given the counts:   log2 (n! / (n_1! ... n_K!))
  4. the position of each point inside its bin:      n log2 (N / K)

Parts 1 and 2 describe the model, parts 3 and 4 the data given the model. MDL picks the K with the
shortest total. The same total is -log2 of a probability, so the code satisfies Kraft with equality.
"""

import math
import random
from fractions import Fraction

LN2 = math.log(2)


def bin_counts(xs: list[int], n_values: int, k: int) -> list[int]:
    width = n_values // k
    c = [0] * k
    for x in xs:
        c[x // width] += 1
    return c


def log2_factorial(n: int) -> float:
    return math.lgamma(n + 1) / LN2


def code_parts(xs: list[int], b: int, k: int) -> tuple[float, float, float, float]:
    """The four parts of the two-part code length, in bits."""
    n, n_values = len(xs), 2 ** b
    c = bin_counts(xs, n_values, k)
    model_index = math.log2(b + 1)
    counts = log2_factorial(n + k - 1) - log2_factorial(k - 1) - log2_factorial(n)
    labels = log2_factorial(n) - sum(log2_factorial(v) for v in c)
    positions = n * math.log2(n_values / k)
    return model_index, counts, labels, positions


def code_length(xs: list[int], b: int, k: int) -> float:
    return sum(code_parts(xs, b, k))


def code_probability(xs: list[int], b: int, k: int) -> Fraction:
    """2^(-code_length), exactly: the probability that the code assigns to the sequence xs."""
    n, n_values = len(xs), 2 ** b
    c = bin_counts(xs, n_values, k)
    p = Fraction(1, b + 1)
    p *= Fraction(1, math.comb(n + k - 1, k - 1))
    p *= Fraction(math.prod(math.factorial(v) for v in c), math.factorial(n))
    return p * Fraction(k, n_values) ** n


def dirichlet_marginal(xs: list[int], b: int, k: int) -> Fraction:
    """Bayes marginal likelihood of xs under the K bin histogram with a uniform Dirichlet(1, ..., 1) prior
    on the bin probabilities, times the uniform prior 1/(B + 1) on the model: the Bayes evidence."""
    n, n_values = len(xs), 2 ** b
    c = bin_counts(xs, n_values, k)
    seq = Fraction(math.factorial(k - 1) * math.prod(math.factorial(v) for v in c), math.factorial(n + k - 1))
    return Fraction(1, b + 1) * seq * Fraction(k, n_values) ** n


def crude_mdl(xs: list[int], b: int, k: int) -> float:
    """The asymptotic form: n times the empirical entropy of the bins, plus (K - 1)/2 log2 n, plus positions."""
    n, n_values = len(xs), 2 ** b
    c = bin_counts(xs, n_values, k)
    ent = -sum(v * math.log2(v / n) for v in c if v)
    return ent + (k - 1) / 2 * math.log2(n) + n * math.log2(n_values / k)


def mdl_select(xs: list[int], b: int, length=code_length) -> tuple[int, dict[int, float]]:
    table = {2 ** j: length(xs, b, 2 ** j) for j in range(b + 1)}
    best = min(table, key=lambda k: (table[k], k))
    return best, table


def sample(n: int, b: int, weights: list[float], rng: random.Random) -> list[int]:
    """n draws from a step density: the range is cut into len(weights) equal blocks with these masses."""
    n_values = 2 ** b
    width = n_values // len(weights)
    out = []
    for _ in range(n):
        block = rng.choices(range(len(weights)), weights=weights)[0]
        out.append(block * width + rng.randrange(width))
    return out


def ideal_length(xs: list[int], b: int, weights: list[float]) -> float:
    """-log2 of the true probability of xs: what a code that knew the density would use."""
    width = 2 ** b // len(weights)
    total = sum(weights)
    return -sum(math.log2(weights[x // width] / total / width) for x in xs)


if __name__ == "__main__":
    b = 8
    for name, w in (("uniform", [1.0]), ("steps", [0.45, 0.05, 0.1, 0.4])):
        for n in (50, 200, 1000):
            xs = sample(n, b, w, random.Random(1))
            best, table = mdl_select(xs, b)
            cbest, _ = mdl_select(xs, b, crude_mdl)
            print(name, n, best, cbest, round(ideal_length(xs, b, w), 1),
                  {k: round(v, 1) for k, v in table.items()})
