# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sieve-of-eratosthenes/. The authors are listed in prov/F0W4PP.jsonl.


def sieve_of_eratosthenes(n: int) -> list[int]:
    """Return the increasing list of all primes p <= n.

    Precondition: n is an integer (n < 2 gives the empty list).
    Cost: Theta(n log log n) word operations and n + 1 bytes of flags.
    """
    if n < 2:  # @line L1
        return []
    is_prime = bytearray([1]) * (n + 1)  # @line L2
    is_prime[0] = 0
    is_prime[1] = 0
    p = 2  # @line L3
    while p * p <= n:  # @line L4
        if is_prime[p]:  # @line L5
            for m in range(p * p, n + 1, p):  # @line L6
                is_prime[m] = 0  # @line L7
        p += 1  # @line L8
    return [m for m in range(2, n + 1) if is_prime[m]]  # @line L9


def prime_flags(n: int) -> bytearray:
    """Return a table T of n + 1 bytes (empty for n < 0) with T[m] = 1 exactly when m is prime.

    Precondition: n is an integer. Cost: Theta(n log log n) word operations.
    """
    table = bytearray(max(n + 1, 0))
    for p in sieve_of_eratosthenes(n):
        table[p] = 1
    return table
