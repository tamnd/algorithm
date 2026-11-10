# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/karp-luby-estimator/. The authors are listed in prov/KKHPVT.jsonl.

import bisect
import math
import random
from typing import Callable, Hashable, Sequence

Element = Hashable
SampleFn = Callable[[int, random.Random], Element]
ContainsFn = Callable[[int, Element], bool]


def sample_count(m: int, eps: float, delta: float) -> int:
    """N = ceil(3 m ln(2 / delta) / eps^2) samples give relative error eps with probability 1 - delta."""
    if not (0 < eps < 1 and 0 < delta < 1):
        raise ValueError("need 0 < eps < 1 and 0 < delta < 1")
    return math.ceil(3 * m * math.log(2 / delta) / eps**2)


def _pick_set(prefix: list[int], rng: random.Random) -> int:
    """Index i with probability |A_i| / W, from the prefix sums of the sizes."""
    r = rng.randrange(prefix[-1])
    return bisect.bisect_right(prefix, r)


def karp_luby(
    sizes: Sequence[int],
    sample: SampleFn,
    contains: ContainsFn,
    eps: float,
    delta: float,
    rng: random.Random,
    n_samples: int | None = None,
) -> float:
    """Estimate |A_1 u ... u A_m| with the 0-1 estimator of Karp and Luby.

    sizes[i] = |A_i|, sample(i, rng) is a uniform element of A_i, and
    contains(j, x) tells whether x is in A_j. A sampled pair (i, x) counts
    when i is the first set that holds x. The result is within a factor
    1 +- eps of the true size with probability at least 1 - delta.
    """
    m = len(sizes)
    w = sum(sizes)  # @line L1
    if w == 0:
        return 0.0
    n = n_samples if n_samples is not None else sample_count(m, eps, delta)
    prefix = list(_accumulate(sizes))
    hits = 0
    for _ in range(n):  # @line L2
        i = _pick_set(prefix, rng)  # @line L3
        x = sample(i, rng)  # @line L4
        if not any(contains(j, x) for j in range(i)):  # @line L5
            hits += 1
    return w * hits / n  # @line L6


def coverage_estimate(
    sizes: Sequence[int],
    sample: SampleFn,
    contains: ContainsFn,
    n_samples: int,
    rng: random.Random,
) -> float:
    """The coverage estimator: the mean of W / c(x), where c(x) counts the sets that hold x."""
    m = len(sizes)
    w = sum(sizes)
    if w == 0:
        return 0.0
    prefix = list(_accumulate(sizes))
    total = 0.0
    for _ in range(n_samples):
        i = _pick_set(prefix, rng)
        x = sample(i, rng)
        c = sum(1 for j in range(m) if contains(j, x))
        total += w / c
    return total / n_samples


def _accumulate(values: Sequence[int]):
    s = 0
    for v in values:
        s += v
        yield s


# The DNF instance: clause i is a list of non-zero integers, v for x_v and -v for not x_v.


def dnf_oracles(clauses: Sequence[Sequence[int]], n_vars: int) -> tuple[list[int], SampleFn, ContainsFn]:
    """The sets A_i = assignments that satisfy clause i, as (sizes, sample, contains).

    An assignment is a tuple of n_vars bits. A clause with both x and not x
    is unsatisfiable and gets size 0.
    """
    fixed: list[dict[int, int] | None] = []
    for cl in clauses:
        f: dict[int, int] = {}
        ok = True
        for lit in cl:
            v, bit = abs(lit) - 1, 1 if lit > 0 else 0
            if f.get(v, bit) != bit:
                ok = False
            f[v] = bit
        fixed.append(f if ok else None)
    sizes = [0 if f is None else 2 ** (n_vars - len(f)) for f in fixed]

    def sample(i: int, rng: random.Random) -> tuple[int, ...]:
        f = fixed[i]
        assert f is not None
        return tuple(f[v] if v in f else rng.randrange(2) for v in range(n_vars))

    def contains(j: int, a: Element) -> bool:
        f = fixed[j]
        return f is not None and all(a[v] == bit for v, bit in f.items())  # type: ignore[index]

    return sizes, sample, contains


def dnf_count_brute_force(clauses: Sequence[Sequence[int]], n_vars: int) -> int:
    count = 0
    for bits in range(2**n_vars):
        a = [(bits >> v) & 1 for v in range(n_vars)]
        if any(all(a[abs(l) - 1] == (1 if l > 0 else 0) for l in cl) for cl in clauses):
            count += 1
    return count
