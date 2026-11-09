# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binary-reflected-gray-code/. The authors are listed in prov/73K11Q.jsonl.


def binary_reflected_gray_code(n: int) -> list[int]:
    """Return the binary reflected Gray code of length n as a list of 2**n integers.

    Entry k is the string a_{n-1} ... a_0 stored as the integer sum(a_j * 2**j).
    The list is 0 Gamma_{n-1}, then 1 Gamma_{n-1} reversed.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    g = [0]  # @line L1
    for i in range(n):  # @line L2
        top = 1 << i
        for j in range(len(g) - 1, -1, -1):  # @line L3: the bound is fixed here
            g.append(g[j] + top)  # @line L4
    return g  # @line L5


def as_strings(codes: list[int], n: int) -> list[str]:
    """Write each code as an n-character string of 0 and 1, bit n-1 first."""
    if n == 0:
        return ["" for _ in codes]
    return [format(c, "0" + str(n) + "b") for c in codes]
