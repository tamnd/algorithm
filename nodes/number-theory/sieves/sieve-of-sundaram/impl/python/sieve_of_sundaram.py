# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sieve-of-sundaram/. The authors are listed in prov/KQBYRB.jsonl.


def sieve_of_sundaram(n: int) -> list[int]:
    """Return the increasing list of all primes p <= n.

    Precondition: n is an integer (n < 2 gives the empty list).
    Cost: Theta(n log n) word operations and about n/2 bytes of flags.
    """
    if n < 2:  # @line L1
        return []
    k = (n - 1) // 2  # @line L2
    marked = bytearray(k + 1)  # @line L3: index 0 is unused
    i = 1  # @line L4
    while 2 * i + 2 * i * i <= k:  # @line L5
        j = i  # @line L6
        while i + j + 2 * i * j <= k:  # @line L7
            marked[i + j + 2 * i * j] = 1  # @line L8
            j += 1  # @line L9
        i += 1  # @line L10
    return [2] + [2 * x + 1 for x in range(1, k + 1) if not marked[x]]  # @line L11
