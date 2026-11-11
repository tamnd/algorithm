# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/join-semilattice/. The authors are listed in prov/QS5856.jsonl.

"""Join-semilattices as values with a join function, and checks of their laws.

Each example is a function join(x, y). The order is derived from the join:
x <= y exactly when join(x, y) == y. The checks take a finite sample of
elements and test the laws on all pairs and triples of the sample.
"""

from itertools import product
from typing import Callable, Hashable, Iterable, Sequence, TypeVar

T = TypeVar("T")
Join = Callable[[T, T], T]


# Examples ------------------------------------------------------------------

def max_join(x: int, y: int) -> int:
    """A chain: the integers ordered by <=."""
    return x if x >= y else y


def union_join(x: frozenset, y: frozenset) -> frozenset:
    """Sets ordered by inclusion."""
    return x | y


def vector_join(x: tuple[int, ...], y: tuple[int, ...]) -> tuple[int, ...]:
    """Vectors of naturals with the pointwise max (the state of a g-counter)."""
    if len(x) != len(y):
        raise ValueError("vectors of different lengths")
    return tuple(a if a >= b else b for a, b in zip(x, y))


def map_join(x: dict[str, int], y: dict[str, int]) -> dict[str, int]:
    """Finite maps to integers; a missing key is the bottom element 0."""
    return {k: max(x.get(k, 0), y.get(k, 0)) for k in x.keys() | y.keys()}


def lex_join(x: tuple[int, frozenset], y: tuple[int, frozenset]) -> tuple[int, frozenset]:
    """Lexicographic pair: a chain first, a join-semilattice second."""
    if x[0] > y[0]:
        return x
    if y[0] > x[0]:
        return y
    return (x[0], x[1] | y[1])


def lcm_join(x: int, y: int) -> int:
    """Positive integers ordered by divisibility."""
    a, b = x, y
    while b:
        a, b = b, a % b
    return x // a * y


# Non-examples --------------------------------------------------------------

def plus_merge(x: int, y: int) -> int:
    """Addition: associative and commutative, not idempotent."""
    return x + y


def second_merge(x: int, y: int) -> int:
    """Keep the argument that arrived last: associative and idempotent, not commutative."""
    return y


def average_merge(x: float, y: float) -> float:
    """The mean: commutative and idempotent, not associative."""
    return (x + y) / 2


# Law checks ----------------------------------------------------------------

def _eq(a: object, b: object) -> bool:
    return a == b


def is_associative(join: Join, sample: Sequence[T]) -> bool:
    return all(_eq(join(join(a, b), c), join(a, join(b, c))) for a, b, c in product(sample, repeat=3))


def is_commutative(join: Join, sample: Sequence[T]) -> bool:
    return all(_eq(join(a, b), join(b, a)) for a, b in product(sample, repeat=2))


def is_idempotent(join: Join, sample: Sequence[T]) -> bool:
    return all(_eq(join(a, a), a) for a in sample)


def is_semilattice(join: Join, sample: Sequence[T]) -> bool:
    """The ACI laws on all pairs and triples of the sample."""
    return is_associative(join, sample) and is_commutative(join, sample) and is_idempotent(join, sample)


def leq(join: Join, x: T, y: T) -> bool:
    """The order derived from a join: x <= y iff x join y = y."""
    return _eq(join(x, y), y)


def is_least_upper_bound(join: Join, sample: Sequence[T]) -> bool:
    """For x, y in the sample, join(x, y) is an upper bound of both, and it is
    below every upper bound of x and y that is in the sample."""
    for x, y in product(sample, repeat=2):
        z = join(x, y)
        if not (leq(join, x, z) and leq(join, y, z)):
            return False
        for u in sample:
            if leq(join, x, u) and leq(join, y, u) and not leq(join, z, u):
                return False
    return True


def is_partial_order(rel: Callable[[T, T], bool], sample: Sequence[T]) -> bool:
    refl = all(rel(a, a) for a in sample)
    anti = all(not (rel(a, b) and rel(b, a)) or _eq(a, b) for a, b in product(sample, repeat=2))
    trans = all(not (rel(a, b) and rel(b, c)) or rel(a, c) for a, b, c in product(sample, repeat=3))
    return refl and anti and trans


def is_monotone_inflationary(f: Callable[[T], T], join: Join, sample: Sequence[T]) -> bool:
    """x <= f(x), and x <= y implies f(x) <= f(y)."""
    infl = all(leq(join, x, f(x)) for x in sample)
    mono = all(not leq(join, x, y) or leq(join, f(x), f(y)) for x, y in product(sample, repeat=2))
    return infl and mono


def absorption(join: Join, meet: Join, sample: Sequence[T]) -> bool:
    """x join (x meet y) = x and x meet (x join y) = x."""
    return all(_eq(join(x, meet(x, y)), x) and _eq(meet(x, join(x, y)), x) for x, y in product(sample, repeat=2))


def join_all(join: Join, bottom: T, items: Iterable[T]) -> T:
    """The join of a finite set; the result does not depend on the order or on repeats."""
    acc = bottom
    for x in items:
        acc = join(acc, x)
    return acc


def minimal_upper_bounds(elements: Sequence[Hashable], below: set[tuple[Hashable, Hashable]], x: Hashable, y: Hashable) -> list[Hashable]:
    """For a finite poset given by its strict order pairs, the minimal upper bounds of x and y."""

    def le(a: Hashable, b: Hashable) -> bool:
        return a == b or (a, b) in below

    ub = [u for u in elements if le(x, u) and le(y, u)]
    return [u for u in ub if not any(v != u and le(v, u) for v in ub)]


# A poset with no join for a and b: a, b < c and a, b < d, c and d incomparable.
BOWTIE_ELEMENTS = ["a", "b", "c", "d"]
BOWTIE_BELOW = {("a", "c"), ("a", "d"), ("b", "c"), ("b", "d")}
