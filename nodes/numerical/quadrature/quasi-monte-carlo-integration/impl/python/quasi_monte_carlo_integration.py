# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quasi-monte-carlo-integration/. The authors are listed in prov/Y77BXY.jsonl.

import math
import random
from typing import Callable, List, Optional, Sequence, Tuple


def first_primes(s: int) -> List[int]:
    """The first s primes, by trial division (s is small in practice)."""
    primes: List[int] = []
    n = 2
    while len(primes) < s:
        if all(n % p for p in primes if p * p <= n):
            primes.append(n)
        n += 1
    return primes


def radical_inverse(i: int, base: int) -> float:
    """Van der Corput radical inverse: reflect the base-b digits of i.

    For i = sum d_k b^k returns sum d_k b^(-k-1), in [0, 1). Cost O(log_b i).
    """
    if i < 0 or base < 2:
        raise ValueError("need i >= 0 and base >= 2")
    # @line L10
    r, f = 0.0, 1.0 / base
    while i > 0:
        # @line L11
        i, d = divmod(i, base)
        r += f * d
        f /= base
    return r


def halton_point(i: int, primes: Sequence[int]) -> List[float]:
    """The i-th point of the Halton sequence in bases primes[0..s-1]."""
    return [radical_inverse(i, p) for p in primes]


def qmc_integrate(
    f: Callable[[Sequence[float]], float],
    lower: Sequence[float],
    upper: Sequence[float],
    n: int,
    replicates: int = 0,
    rng: Optional[random.Random] = None,
) -> Tuple[float, Optional[float]]:
    """Quasi-Monte Carlo integration of f over the box [lower, upper].

    Uses the Halton points with indices 1..n. With replicates = 0 the rule is
    deterministic and the second result is None. With replicates = R >= 1,
    each replicate adds an independent uniform shift modulo 1 (Cranley-
    Patterson rotation) using rng; the estimate is the mean of the R
    replicate values and, for R >= 2, the second result is its standard
    error. Each replicate is an unbiased estimate of the integral.

    Precondition: n >= 1, len(lower) == len(upper) >= 1, finite bounds, f
    integrable on the box. A bound with upper < lower contributes a minus
    sign to the volume. Cost: R n (or n) evaluations of f and O(R n s log n)
    other work.
    """
    s = len(lower)
    if n < 1 or s < 1 or len(upper) != s:
        raise ValueError("need n >= 1 and matching nonempty bounds")
    if replicates < 0:
        raise ValueError("replicates must be >= 0")
    if any(math.isinf(v) for v in list(lower) + list(upper)):
        raise ValueError("infinite bounds: map the domain to a box first")
    if replicates > 0 and rng is None:
        raise ValueError("a random generator is needed for shifted replicates")
    primes = first_primes(s)
    width = [upper[k] - lower[k] for k in range(s)]
    # @line L1
    vol = math.prod(width)
    values: List[float] = []
    # @line L2
    for _ in range(max(replicates, 1)):
        # @line L3
        shift = [rng.random() for _ in range(s)] if replicates > 0 else [0.0] * s
        # @line L4
        terms: List[float] = []
        # @line L5
        for i in range(1, n + 1):
            # @line L6
            u = [(h + d) % 1.0 for h, d in zip(halton_point(i, primes), shift)]
            # @line L7
            terms.append(f([lower[k] + u[k] * width[k] for k in range(s)]))
        # @line L8
        values.append(vol * math.fsum(terms) / n)
    # @line L9
    R = len(values)
    mean = math.fsum(values) / R
    if replicates < 2:
        return mean, None
    var = math.fsum((v - mean) ** 2 for v in values) / (R - 1)
    return mean, math.sqrt(var / R)


def star_discrepancy_1d(points: Sequence[float]) -> float:
    """Exact star discrepancy of points in [0, 1): 1/(2N) + max |x_(i) - (2i-1)/(2N)|."""
    x = sorted(points)
    N = len(x)
    if N == 0:
        raise ValueError("need at least one point")
    return 1.0 / (2 * N) + max(abs(xi - (2 * i + 1) / (2 * N)) for i, xi in enumerate(x))


def star_discrepancy_2d(points: Sequence[Sequence[float]]) -> float:
    """Exact star discrepancy of points in [0, 1)^2, in O(N^2) time.

    The supremum over anchored boxes [0, t) is attained, as a limit, at
    corners t whose coordinates are point coordinates or 1: from below with
    the closed count (too many points) or at the corner with the open count
    (too few). Two-dimensional prefix sums give both counts.
    """
    N = len(points)
    if N == 0:
        raise ValueError("need at least one point")
    xs = sorted(set([p[0] for p in points] + [1.0]))
    ys = sorted(set([p[1] for p in points] + [1.0]))
    xi = {v: k for k, v in enumerate(xs)}
    yi = {v: k for k, v in enumerate(ys)}
    cnt = [[0] * len(ys) for _ in xs]
    for p in points:
        cnt[xi[p[0]]][yi[p[1]]] += 1
    # C[a][b] = number of points with x < xs[a] and y < ys[b] (strict), a, b >= 0
    C = [[0] * (len(ys) + 1) for _ in range(len(xs) + 1)]
    for a in range(len(xs)):
        row = 0
        for b in range(len(ys)):
            row += cnt[a][b]
            C[a + 1][b + 1] = C[a][b + 1] + row
    D = 0.0
    for a, tx in enumerate(xs):
        for b, ty in enumerate(ys):
            v = tx * ty
            D = max(D, v - C[a][b] / N, C[a + 1][b + 1] / N - v)
    return D
