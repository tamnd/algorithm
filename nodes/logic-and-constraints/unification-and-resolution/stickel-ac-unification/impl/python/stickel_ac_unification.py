# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stickel-ac-unification/. The authors are listed in prov/JEGV8S.jsonl.

"""Stickel's AC-unification for one associative-commutative symbol with
variables and free constants (elementary AC-unification with constants).

A term is a variable (a Python str), a constant (a tuple with one item, for
example ("a",)), or (op, s, t) for the AC symbol op, "+" by default.
A substitution is a dict from variable names to terms.
"""

from collections import Counter
from itertools import product
from typing import Union

Term = Union[str, tuple]
Subst = dict[str, Term]


def flatten(t: Term, op: str = "+") -> Counter:
    """The multiset of the arguments of t below the AC symbol op."""
    out: Counter = Counter()
    stack = [t]
    while stack:
        u = stack.pop()
        if not isinstance(u, str) and u[0] == op:
            stack.extend(u[1:])
        else:
            out[u] += 1
    return out


def build(args: list[Term], op: str = "+") -> Term:
    """Build the sum of a nonempty list of terms, nested to the right."""
    result = args[-1]
    for a in reversed(args[:-1]):
        result = (op, a, result)
    return result


def _key(t: Term) -> tuple:
    return (0, t) if isinstance(t, str) else (1, t[0])


def diophantine_basis(a: list[int], b: list[int]) -> list[tuple[int, ...]]:
    """The minimal nonzero solutions (x, y) in nonnegative integers of
    sum a[i] x[i] = sum b[j] y[j], as tuples x + y.

    It uses Huet's bound: in a minimal solution each x[i] <= max(b) and
    each y[j] <= max(a). Cost: O((max(b) + 1)^len(a) (max(a) + 1)^len(b)),
    which is fine for the small systems that AC problems give.
    """
    ma, mb = max(a), max(b)
    sols = []
    for xs in product(range(mb + 1), repeat=len(a)):
        lhs = sum(ai * xi for ai, xi in zip(a, xs))
        for ys in product(range(ma + 1), repeat=len(b)):
            if lhs == sum(bj * yj for bj, yj in zip(b, ys)) and lhs > 0:
                sols.append(xs + ys)
    sols.sort(key=sum)
    basis: list[tuple[int, ...]] = []
    for v in sols:
        if not any(all(p <= q for p, q in zip(w, v)) for w in basis):
            basis.append(v)
    return basis


def stickel_ac_unification(s: Term, t: Term, op: str = "+") -> list[Subst]:
    """Return a complete set of AC-unifiers of s and t.

    Each unifier maps the variables of s and t to sums of new variables
    z1, z2, ... and constants. Every AC-unifier of s and t is, modulo AC,
    an instance of one of them. The list is empty when s and t have no
    AC-unifier. The set is complete but not always minimal.
    """
    left, right = flatten(s, op), flatten(t, op)  # @line L1
    common = left & right
    left, right = left - common, right - common
    if not left and not right:
        return [{}]  # @line L2
    if not left or not right:
        return []
    cols = sorted(left, key=_key) + sorted(right, key=_key)  # @line L3
    coef = [left[c] for c in sorted(left, key=_key)] + [right[c] for c in sorted(right, key=_key)]
    basis = diophantine_basis(coef[: len(left)], coef[len(left):])  # @line L4
    used = {v for v in cols if isinstance(v, str)}
    names: list[str] = []
    i = 1
    while len(names) < len(basis):
        if f"z{i}" not in used:
            names.append(f"z{i}")
        i += 1
    unifiers: list[Subst] = []  # @line L5
    for mask in range(1, 1 << len(basis)):  # @line L6
        chosen = [k for k in range(len(basis)) if mask >> k & 1]
        total = [sum(basis[k][c] for k in chosen) for c in range(len(cols))]
        if 0 in total:
            continue  # @line L7
        if any(total[c] != 1 for c in range(len(cols)) if not isinstance(cols[c], str)):
            continue  # @line L8
        value: dict[str, Term] = {}  # @line L9
        clash = False
        for c, col in enumerate(cols):
            if not isinstance(col, str):
                (k,) = [k for k in chosen if basis[k][c] == 1]
                if value.setdefault(names[k], col) != col:  # @line L10
                    clash = True
        if clash:
            continue
        sigma: Subst = {}
        for c, col in enumerate(cols):  # @line L11
            if isinstance(col, str):
                parts: list[Term] = []
                for k in chosen:
                    parts.extend([value.get(names[k], names[k])] * basis[k][c])
                sigma[col] = build(parts, op)
        unifiers.append(sigma)  # @line L12
    return unifiers  # @line L13
