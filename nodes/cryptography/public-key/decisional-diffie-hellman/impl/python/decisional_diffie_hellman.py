# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/decisional-diffie-hellman/. The authors are listed in prov/AE1DRR.jsonl.
"""Two tools for the decisional Diffie-Hellman (DDH) problem.

legendre_ddh() decides DDH in the full group Z_p^* with advantage 1/2. It is
the reason why DDH-based schemes use a subgroup of prime order.

rerandomize() is the random self-reduction of Naor and Reingold (1997). It maps
any triple to a uniform Diffie-Hellman triple, or to a uniform triple that is
not a Diffie-Hellman triple, in a group of prime order q.

For study only. The code is not constant time and runs on toy groups.
"""

import random


def is_square(a: int, p: int) -> bool:
    """Euler's criterion for an odd prime p and 0 < a < p. Cost: one exponentiation."""
    return pow(a, (p - 1) // 2, p) == 1


def legendre_ddh(p: int, X: int, Y: int, Z: int) -> int:
    """Guess whether (X, Y, Z) = (g^x, g^y, g^(xy)) for a generator g of Z_p^*.

    Returns 1 for "Diffie-Hellman triple" and 0 for "random triple". On a real
    triple the answer is always 1; on a uniform triple it is 1 with
    probability 1/2. Cost: three exponentiations modulo p.
    """
    ex = is_square(X, p)  # @line L1
    ey = is_square(Y, p)  # @line L2
    ez = is_square(Z, p)  # @line L3
    return 1 if ez == (ex or ey) else 0  # @line L4


def rerandomize(p: int, q: int, g: int, X: int, Y: int, Z: int, rng: random.Random) -> tuple[int, int, int]:
    """Naor-Reingold random self-reduction in the subgroup of prime order q.

    With a in {1, ..., q - 1} and b, c in {0, ..., q - 1}:
    X' = X^a g^b, Y' = Y g^c, Z' = Z^a Y^b X^(ac) g^(bc).
    If Z = g^(xy), the output is a uniform Diffie-Hellman triple. Otherwise it
    is uniform among the triples that are not Diffie-Hellman triples.
    Cost: a constant number of exponentiations modulo p.
    """
    a = rng.randrange(1, q)
    b = rng.randrange(q)
    c = rng.randrange(q)
    return apply_map(p, q, g, X, Y, Z, a, b, c)


def apply_map(p: int, q: int, g: int, X: int, Y: int, Z: int, a: int, b: int, c: int) -> tuple[int, int, int]:
    """The map of rerandomize() for fixed a, b, c."""
    X2 = pow(X, a, p) * pow(g, b, p) % p
    Y2 = Y * pow(g, c, p) % p
    Z2 = pow(Z, a, p) * pow(Y, b, p) % p * pow(X, a * c % q, p) % p * pow(g, b * c % q, p) % p
    return X2, Y2, Z2
