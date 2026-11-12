# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generational-collector-pause-tradeoff/. The authors are listed in prov/RPKRXJ.jsonl.

"""An exact model of minor collection pauses, work and promotion.

The mutator allocates one object per time unit. Lifetimes are independent,
with survival function S(a) = P(lifetime > a). A minor collection runs after
every N allocations. An object of age a (a allocations after its birth) is
alive at a collection if its lifetime is greater than a. A young object that
survives T collections is promoted at the T-th; before that it is copied
inside the young generation. The collector keeps exactly the objects that
are alive, so the model has no nepotism.

With P(n) = S(0) + S(1) + ... + S(n-1), in the steady state each minor
collection copies P(T*N) objects in expectation and promotes
P(T*N) - P((T-1)*N) of them.
"""

from fractions import Fraction
from typing import Callable, Union

Num = Union[int, float, Fraction]
Survival = Callable[[int], Num]


def geometric(mean: int, exact: bool = True) -> Survival:
    q = 1 - Fraction(1, mean) if exact else 1.0 - 1.0 / mean
    return lambda a: q ** a


def mixture(parts: list[tuple[Num, Survival]]) -> Survival:
    return lambda a: sum(w * s(a) for w, s in parts)


def finite(dist: dict[int, Fraction]) -> Survival:
    """dist maps a lifetime to its probability."""
    return lambda a: sum((p for life, p in dist.items() if life > a), Fraction(0))


def p_sum(s: Survival, n: int) -> Num:
    """P(n), the expected number of the last n allocated objects still alive."""
    return sum((s(a) for a in range(n)), Fraction(0))  # a float survival gives a float


def geometric_p(mean: int, n: int) -> float:
    """P(n) for a geometric lifetime of the given mean, in closed form."""
    return mean * (1.0 - (1.0 - 1.0 / mean) ** n)


def copied_per_collection(s: Survival, n: int, t: int) -> Num:
    """The expected pause work: objects copied or promoted at one collection."""
    return p_sum(s, t * n)


def promoted_per_collection(s: Survival, n: int, t: int) -> Num:
    return p_sum(s, t * n) - p_sum(s, (t - 1) * n)


def promotion_rate(s: Survival, n: int, t: int) -> Num:
    """Promoted objects per allocated object."""
    return promoted_per_collection(s, n, t) / n


def cost_per_allocation(s: Survival, n: int, t: int, fixed: Num, per_copy: Num) -> Num:
    """Minor collection work per allocated object: (fixed + per_copy * P(TN)) / N."""
    return (fixed + per_copy * copied_per_collection(s, n, t)) / n


def simulate(lifetimes: list[int], n: int, t: int) -> list[tuple[int, int]]:
    """Run the policy on given lifetimes. Object k is born at time k; the
    j-th collection (j = 1, 2, ...) runs after allocation j*n - 1. Return
    (copied, promoted) for each collection that has all its windows full."""
    out = []
    collections = len(lifetimes) // n
    for j in range(1, collections + 1):
        copied = promoted = 0
        for k in range(max(0, (j - t) * n), j * n):  # older objects are no longer young
            age = j * n - 1 - k
            seen = j - k // n  # this is the object's seen-th collection
            if 1 <= seen <= t and lifetimes[k] > age:
                copied += 1
                if seen == t:
                    promoted += 1
        out.append((copied, promoted))
    return out
