# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/t-closeness/. The authors are listed in prov/4AARD3.jsonl.

from collections import Counter
from collections.abc import Hashable, Sequence
from fractions import Fraction

Row = Sequence[Hashable]


def distribution(values: Sequence[Hashable], domain: Sequence[Hashable]) -> list[Fraction]:
    """Return the distribution of the values over the domain, as exact fractions.

    Precondition: values is not empty and each value is in the domain. Cost: O(len(values) + len(domain)).
    """
    count = Counter(values)
    if set(count) - set(domain):
        raise ValueError("a value is not in the domain")
    return [Fraction(count[v], len(values)) for v in domain]


def emd_ordered(p: Sequence[Fraction], w: Sequence[Fraction]) -> Fraction:
    """Earth mover's distance under the ordered distance |i - j| / (m - 1).

    Precondition: p and w are distributions over the same m ordered values. Cost: O(m).
    """
    m = len(p)
    if m < 2:
        return Fraction(0)
    run = Fraction(0)  # @line L4
    d = Fraction(0)
    for i in range(m - 1):  # @line L5
        run += p[i] - w[i]  # @line L6
        d += abs(run)  # @line L7
    return d / (m - 1)


def emd_equal(p: Sequence[Fraction], w: Sequence[Fraction]) -> Fraction:
    """Earth mover's distance under the equal distance; this is the total variation distance. Cost: O(m)."""
    return sum((abs(a - b) for a, b in zip(p, w)), Fraction(0)) / 2


def is_t_close(
    table: Sequence[Row],
    qi: Sequence[int],
    s: int,
    t: Fraction | int,
    domain: Sequence[Hashable],
    ground: str = "ordered",
) -> bool:
    """Return True if every block of the table is within distance t of the whole table.

    domain lists the values of column s, in increasing order for the ordered
    distance. ground is "ordered" or "equal". An empty table is t-close.
    Cost: O(n + g m) for n rows, g blocks and m values, with exact fractions.
    """
    if not table:
        return True
    dist = emd_ordered if ground == "ordered" else emd_equal
    w = distribution([row[s] for row in table], domain)  # @line L1
    groups: dict[tuple[Hashable, ...], list[Hashable]] = {}
    for row in table:
        groups.setdefault(tuple(row[j] for j in qi), []).append(row[s])
    for values in groups.values():  # @line L2
        p = distribution(values, domain)  # @line L3
        if dist(p, w) > t:  # @line L8
            return False
    return True  # @line L9
