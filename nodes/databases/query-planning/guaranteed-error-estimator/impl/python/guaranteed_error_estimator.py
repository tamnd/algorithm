# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/guaranteed-error-estimator/. The authors are listed in prov/32XY8A.jsonl.
"""The guaranteed-error estimator (GEE) of Charikar, Chaudhuri, Motwani and Narasayya (PODS 2000).

The input is a column of n rows. GEE reads a uniform random sample of r
rows and estimates the number D of distinct values in the column. Let f_j
be the number of values that occur exactly j times in the sample. Then

    GEE = sqrt(n / r) * f_1 + sum over j >= 2 of f_j.

A value seen two or more times is counted once. A value seen once stands
for itself and for sqrt(n / r) - 1 values that the sample missed. The
estimate always lies between d, the number of distinct values in the
sample, and sqrt(n / r) * d.
"""

import math
from collections import Counter
from random import Random
from typing import Dict, Hashable, List, Sequence


def frequency_profile(sample: Sequence[Hashable]) -> Dict[int, int]:
    """Return {j: f_j}, where f_j is the number of values seen exactly j times."""
    counts = Counter(sample)  # @line L2
    profile: Dict[int, int] = {}
    for j in counts.values():  # @line L3
        profile[j] = profile.get(j, 0) + 1
    return profile


def gee_from_profile(profile: Dict[int, int], n: int, r: int) -> float:
    """GEE for a sample of r rows from n rows with frequency profile `profile`."""
    if not 1 <= r <= n:
        raise ValueError("the sample size r must satisfy 1 <= r <= n")
    if sum(j * f for j, f in profile.items()) != r:
        raise ValueError("the profile does not describe r rows")
    scale = math.sqrt(n / r)
    f1 = profile.get(1, 0)
    rest = sum(f for j, f in profile.items() if j >= 2)
    return scale * f1 + rest  # @line L4


def gee(sample: Sequence[Hashable], n: int) -> float:
    """GEE for a sample (a list of values) drawn from a column of n rows."""
    return gee_from_profile(frequency_profile(sample), n, len(sample))


def draw_sample(column: Sequence[Hashable], r: int, rng: Random) -> List[Hashable]:
    """A uniform random sample of r rows, without replacement."""
    return rng.sample(list(column), r)  # @line L1


def estimate_distinct(column: Sequence[Hashable], r: int, rng: Random) -> float:
    """Draw r rows of the column at random and return the GEE estimate."""
    return gee(draw_sample(column, r, rng), len(column))


def ratio_error(estimate: float, true: float) -> float:
    """max(estimate / true, true / estimate), for positive values."""
    if estimate <= 0 or true <= 0:
        raise ValueError("the ratio error needs positive values")
    return max(estimate / true, true / estimate)


def lower_bound(n: int, r: int, gamma: float) -> float:
    """The ratio error sqrt((n - r) / (2 r) * ln(1 / gamma)) of the lower bound.

    Charikar et al. show that every estimator that examines at most r of n
    rows has at least this ratio error on some input, with probability at
    least gamma, for each gamma > e^(-r).
    """
    if not (math.exp(-r) < gamma < 1):
        raise ValueError("gamma must satisfy e^(-r) < gamma < 1")
    return math.sqrt((n - r) / (2 * r) * math.log(1 / gamma))
