# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boyce-codd-normal-form/. The authors are listed in prov/W6NDNV.jsonl.
"""Tests for Boyce-Codd normal form (BCNF).

An attribute set is a frozenset of strings. A functional dependency (FD) X -> Y is a pair
(X, Y) of attribute sets. The closure of X under F is computed by the usual fixpoint.
"""

from itertools import combinations

Attrs = frozenset
FD = tuple[frozenset, frozenset]


def parse_fds(text: str) -> list[FD]:
    """Parse "AB->C, C->A" into FDs with one-letter attributes."""
    out = []
    for part in text.split(","):
        lhs, rhs = part.strip().split("->")
        out.append((frozenset(lhs.strip()), frozenset(rhs.strip())))
    return out


def closure(x: frozenset, fds: list[FD]) -> frozenset:
    """Return the closure X+ of X under fds. Cost O(|F|^2 * n) set operations in this simple form."""
    result = set(x)
    changed = True
    while changed:
        changed = False
        for lhs, rhs in fds:
            if lhs <= result and not rhs <= result:
                result |= rhs
                changed = True
    return frozenset(result)


def bcnf_violation(schema: frozenset, fds: list[FD]) -> FD | None:
    """Test a full schema R against its own FD set F.

    Precondition: every FD of fds uses only attributes of schema.
    Checks only the FDs of F: X -> Y with Y not inside X, and X+ not all of R, is a violation.
    Cost: |F| closures, so polynomial.
    """
    for lhs, rhs in fds:
        if not rhs <= lhs and not schema <= closure(lhs, fds):
            return (lhs, rhs - lhs)
    return None


def is_bcnf(schema: frozenset, fds: list[FD]) -> bool:
    """True when the schema with its own FD set is in BCNF."""
    return bcnf_violation(schema, fds) is None


def projected_violation(sub: frozenset, fds: list[FD]) -> FD | None:
    """Test a subschema S of R against the projection of F onto S.

    Tries each subset X of S (exponential in |S|): X -> (X+ & S) - X is a violation when it is
    nontrivial and X is not a superkey of S. The decision problem is coNP-complete in general.
    """
    attrs = sorted(sub)
    for size in range(len(attrs) + 1):
        for xs in combinations(attrs, size):
            x = frozenset(xs)
            c = closure(x, fds)
            gained = (c & sub) - x
            if gained and not sub <= c:
                return (x, gained)
    return None


def is_bcnf_projection(sub: frozenset, fds: list[FD]) -> bool:
    """True when the subschema sub is in BCNF under the projection of fds onto sub."""
    return projected_violation(sub, fds) is None
