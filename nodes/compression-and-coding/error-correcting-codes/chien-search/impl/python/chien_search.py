# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chien-search/. The authors are listed in prov/GDVWFM.jsonl.
"""Chien search: the error positions of a BCH or Reed-Solomon decoder.

The error locator is Lambda(x) = prod_k (1 - X_k x) with X_k = alpha^(i_k), so
position i is in error exactly when Lambda(alpha^(-i)) = 0. Chien search
evaluates Lambda at alpha^0, alpha^(-1), ..., alpha^(-(n-1)) with one register
per coefficient; each step multiplies register j by the constant alpha^(-j).
"""

from gf import GF2m


def chien_search(field: GF2m, lam: list[int], n: int) -> list[int]:
    """Return the positions i in 0 .. n - 1 with Lambda(alpha^(-i)) = 0, in increasing order.

    Precondition: lam = [Lambda_0, ..., Lambda_nu] over `field`, and n <= 2^m - 1.
    Cost: n * nu multiplications by constants and n * nu additions; O(nu) space.
    """
    nu = len(lam) - 1
    t = [lam[j] for j in range(nu + 1)]  # @line L1: T_j <- Lambda_j
    step = [field.alpha(-j) for j in range(nu + 1)]  # the constants alpha^(-j)
    roots: list[int] = []  # @line L2
    for i in range(n):  # @line L3
        total = 0
        for j in range(nu + 1):
            total ^= t[j]
        if total == 0:  # @line L4: Lambda(alpha^(-i)) = T_0 + ... + T_nu
            roots.append(i)
        for j in range(1, nu + 1):  # @line L5
            t[j] = field.mul(t[j], step[j])
    return roots  # @line L6


def chien_search_direct(field: GF2m, lam: list[int], n: int) -> list[int]:
    """The same result by Horner's rule at each point: n * nu general multiplications."""
    return [i for i in range(n) if field.peval(lam, field.alpha(-i)) == 0]


def locate_errors(field: GF2m, lam: list[int], n: int) -> list[int] | None:
    """Chien search with the decoder check: None unless Lambda has deg Lambda distinct roots in range."""
    lam = field.trim(lam)
    if not lam or lam[0] == 0:
        return None
    roots = chien_search(field, lam, n)
    return roots if len(roots) == len(lam) - 1 else None
