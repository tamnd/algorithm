# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dependency-preserving-decomposition/. The authors are listed in prov/HRYHGM.jsonl.
"""Test whether a decomposition preserves a set of functional dependencies.

Attribute sets are frozensets of names, and an FD X -> Y is a pair (X, Y).
"""

from itertools import combinations

FD = tuple[frozenset, frozenset]


def closure(x: frozenset, fds: list[FD]) -> frozenset:
    """X+ under fds."""
    result = set(x)
    changed = True
    while changed:
        changed = False
        for lhs, rhs in fds:
            if lhs <= result and not rhs <= result:
                result |= rhs
                changed = True
    return frozenset(result)


def closure_under_projections(x: frozenset, fds: list[FD], parts: list[frozenset]) -> frozenset:
    """The closure of X under the union G of the projections of F on the parts.

    Repeat Z := Z | ((Z & Ri)+ & Ri) until Z is stable. G is never built.
    Cost: at most n rounds of k closures, for n attributes and k parts.
    """
    z = frozenset(x)
    changed = True
    while changed:
        changed = False
        for part in parts:
            add = closure(z & part, fds) & part
            if not add <= z:
                z = z | add
                changed = True
    return z


def preserves(fds: list[FD], parts: list[frozenset]) -> bool:
    """True when the projections of fds on parts together imply every FD of fds. Polynomial."""
    return all(rhs <= closure_under_projections(lhs, fds, parts) for lhs, rhs in fds)


def projected_fds(fds: list[FD], part: frozenset) -> list[FD]:
    """The projection of fds on part, built by brute force over all subsets X of part.

    Each X gives X -> (X+ & part) - X when that set is not empty. Cost: 2^|part| closures.
    """
    out = []
    attrs = sorted(part)
    for size in range(len(attrs) + 1):
        for xs in combinations(attrs, size):
            x = frozenset(xs)
            y = (closure(x, fds) & part) - x
            if y:
                out.append((x, y))
    return out


def preserves_brute_force(fds: list[FD], parts: list[frozenset]) -> bool:
    """The definition: build G as the union of the projections, and test G |= F."""
    g = [fd for part in parts for fd in projected_fds(fds, part)]
    return all(rhs <= closure(lhs, g) for lhs, rhs in fds)
