# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/proth-test/. The authors are listed in prov/ACSTC1.jsonl.

"""Proth's test for Proth numbers n = k * 2^m + 1 with k odd and k < 2^m.

proth_test(n) returns (True, a) if n is prime and (False, evidence) if not,
where a is a base with Jacobi symbol (a/n) = -1 and a^((n-1)/2) = -1 mod n.
The answer is exact: no error on any Proth number. A number that is not a
Proth number raises ValueError.

Cost: integers of arbitrary precision with bit length l. One modular
exponentiation, O(l^3) bit operations with schoolbook arithmetic, plus A
Jacobi symbols of O(l^2) each, where A is the least base a >= 2 with
(a/n) != 1. All loops are iterative.
"""

import math


def proth_split(n: int) -> tuple[int, int]:
    """(k, m) with n - 1 = k * 2^m and k odd, for odd n >= 3."""
    k, m = n - 1, 0
    while k % 2 == 0:
        k //= 2
        m += 1
    return k, m


def is_proth_number(n: int) -> bool:
    if n < 3 or n % 2 == 0:
        return False
    k, m = proth_split(n)
    return k < 2**m


def jacobi(a: int, n: int) -> int:
    """Jacobi symbol (a/n) for odd n >= 1, by quadratic reciprocity."""
    a %= n
    result = 1
    while a != 0:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5):
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a %= n
    return result if n == 1 else 0


def proth_test(n: int) -> tuple[bool, dict]:
    if not is_proth_number(n):  # @line L1
        raise ValueError("n is not a Proth number k * 2^m + 1 with k odd and k < 2^m")
    r = math.isqrt(n)
    if r * r == n:  # @line L2
        return False, {"square_root": r}
    a = 2  # @line L3
    while jacobi(a, n) == 1:  # @line L4
        a += 1
    if jacobi(a, n) == 0:  # @line L5
        return False, {"factor": math.gcd(a, n)}
    x = pow(a, (n - 1) // 2, n)  # @line L6
    if x == n - 1:  # @line L7
        return True, {"base": a}
    return False, {"base": a, "residue": x}  # @line L8
