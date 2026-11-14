# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/petricks-method/. The authors are listed in prov/P7JR23.jsonl.

"""Petrick's method for the prime implicant table.

The table is a list of rows. Row r is the set of the column numbers
(prime implicants) that cover the minterm of row r. A product term of
the Petrick function is a frozenset of column numbers.
"""

from typing import Callable, Iterable

Term = frozenset[int]


def absorb(terms: Iterable[Term]) -> list[Term]:
    """Remove each term that contains another term (X + XY = X)."""
    out: list[Term] = []
    for t in sorted(set(terms), key=lambda t: (len(t), sorted(t))):
        if not any(s <= t for s in out):
            out.append(t)
    return out


def petrick_products(rows: list[set[int]]) -> list[Term]:
    """Multiply out the product of sums of the rows, with absorption.

    The result lists every inclusion-minimal set of columns that meets
    every row, each one time.
    """
    products: list[Term] = [frozenset()]  # @line L1: the empty product is 1
    for row in rows:  # @line L2
        if not row:
            return []  # @line L3: an empty sum is 0, so there is no cover
        step = []
        for t in products:  # @line L4
            if t & row:
                step.append(t)  # @line L5: X (X + Y) = X
            else:
                step.extend(t | {j} for j in row)  # @line L6
        products = absorb(step)  # @line L7
    return products


def cheapest(products: list[Term], weight: Callable[[int], tuple[int, int]]) -> Term:
    """The product of least total weight, ties broken by the sorted column list."""
    def total(t: Term) -> tuple[int, int]:
        a = b = 0
        for j in t:
            w = weight(j)
            a, b = a + w[0], b + w[1]
        return a, b
    return min(products, key=lambda t: (total(t), sorted(t)))  # @line L8


def literals(c: str) -> int:
    return sum(ch != "-" for ch in c)


def covers(c: str, m: int) -> bool:
    n = len(c)
    for i, ch in enumerate(c):
        bit = (m >> (n - 1 - i)) & 1
        if ch != "-" and int(ch) != bit:
            return False
    return True


def petricks_method(on: Iterable[int], primes: list[str]) -> list[str]:
    """A minimum cover of the on-set by the given primes, for the cost (cubes, literals)."""
    rows = [{j for j, p in enumerate(primes) if covers(p, m)} for m in sorted(set(on))]
    products = petrick_products(rows)
    if not products:
        raise ValueError("the primes do not cover the on-set")
    best = cheapest(products, lambda j: (1, literals(primes[j])))
    return sorted(primes[j] for j in best)
