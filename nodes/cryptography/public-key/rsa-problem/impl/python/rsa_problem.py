# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rsa-problem/. The authors are listed in prov/07Z52Q.jsonl.
"""Reductions around the RSA problem.

The RSA problem is: given N, e and c, find m with m^e = c mod N. This file
holds the two reductions that the page states and proves:

* factoring gives the private exponent, so it solves the RSA problem;
* the private exponent gives the factorization, by the probabilistic
  algorithm of Miller (1976), as in Fact 1 of Boneh's survey of 1999;
* the RSA problem is random self reducible, so the worst case and the
  average case over c are equally hard.

For study only. The code is not constant time and must not be used to protect
real data. It runs on toy parameters, with keys that this file or the test
file makes.
"""

import math
import secrets

Factors = tuple[int, int]


def private_exponent_from_factors(e: int, p: int, q: int) -> int:
    """The private exponent of the key (p, q, e), reduced modulo lambda(N).
    Cost: one extended Euclidean algorithm on numbers of the size of N."""
    lam = (p - 1) * (q - 1) // math.gcd(p - 1, q - 1)
    if math.gcd(e, lam) != 1:
        raise ValueError("e is not invertible modulo lambda(N)")
    return pow(e, -1, lam)


def solve_with_factors(n: int, e: int, c: int, p: int, q: int) -> int:
    """Solve one instance of the RSA problem with the factorization of N.
    This is the reduction `factoring implies RSA': the only extra work is one
    inversion and one modular exponentiation."""
    if p * q != n:
        raise ValueError("p * q must equal N")
    d = private_exponent_from_factors(e, p, q)
    return pow(c, d, n)


def factor_from_exponents(
    n: int, e: int, d: int, rounds: int = 64, randbelow=secrets.randbelow
) -> Factors | None:
    """Factor N from a public and a private exponent pair with e*d = 1 mod lambda(N).

    Method: write e*d - 1 = 2^s * t with t odd. For a random base a, the chain
    a^t, a^(2t), ..., a^(2^s t) ends at 1 modulo N when gcd(a, N) = 1. A square
    root of 1 in the chain that is neither 1 nor N - 1 is a nontrivial square
    root of 1, and then gcd(x - 1, N) is p or q. Each base works with
    probability at least 1/2, so the failure probability after `rounds` bases is
    at most 2^(-rounds). Returns (p, q) with p < q, or None.
    Cost: O(rounds * log(e*d)) modular multiplications.
    """
    k = e * d - 1
    if k <= 0 or k % 2 != 0:
        raise ValueError("e*d - 1 must be a positive even number")
    s, t = 0, k
    while t % 2 == 0:
        t //= 2
        s += 1
    for _ in range(rounds):  # @line L1
        a = 2 + randbelow(n - 3)  # @line L2
        g = math.gcd(a, n)  # @line L3
        if 1 < g < n:  # @line L3
            return (min(g, n // g), max(g, n // g))
        x = pow(a, t, n)  # @line L4
        for _ in range(s):  # @line L5
            y = x * x % n  # @line L6
            if y == 1:  # @line L7
                if x != 1 and x != n - 1:  # @line L8
                    f = math.gcd(x - 1, n)  # @line L9
                    if 1 < f < n:
                        return (min(f, n // f), max(f, n // f))  # @line L10
                break
            x = y  # @line L11
    return None  # @line L12


def blind_instance(n: int, e: int, c: int, r: int) -> int:
    """The random self reduction of the RSA problem: c' = c * r^e mod N for a
    random r that is invertible modulo N. The new instance is uniform when c is
    fixed and r is uniform among the invertible residues."""
    if math.gcd(r, n) != 1:
        raise ValueError("r must be invertible modulo N")
    return c * pow(r, e, n) % n


def unblind_solution(n: int, m_blinded: int, r: int) -> int:
    """Undo blind_instance: if m' is the e-th root of c * r^e then m' / r is the
    e-th root of c."""
    return m_blinded * pow(r, -1, n) % n


def solve_with_average_case_oracle(n: int, e: int, c: int, oracle, randbelow=secrets.randbelow) -> int:
    """Solve a fixed instance with an oracle that answers random instances only.
    One blinded query is enough, so the worst case over c is as easy as the
    average case. `oracle` maps a ciphertext to its e-th root modulo N."""
    while True:
        r = 1 + randbelow(n - 1)
        if math.gcd(r, n) == 1:
            break
    return unblind_solution(n, oracle(blind_instance(n, e, c, r)), r)
