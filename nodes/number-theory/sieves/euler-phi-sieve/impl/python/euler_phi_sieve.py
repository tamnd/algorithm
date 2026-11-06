# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/euler-phi-sieve/. The authors are listed in prov/1P82VA.jsonl.


def euler_phi_sieve(n: int) -> list[int]:
    """Return the list phi[0 .. n] with phi[m] = Euler's totient of m for m >= 1, and phi[0] = 0.

    Precondition: n >= 0.
    Cost: Theta(n log log n) word operations; the output list is the only table.
    """
    phi = list(range(n + 1))  # @line L1
    for p in range(2, n + 1):  # @line L2
        if phi[p] == p:  # @line L3
            for m in range(p, n + 1, p):  # @line L4
                phi[m] -= phi[m] // p  # @line L5
    return phi  # @line L6
