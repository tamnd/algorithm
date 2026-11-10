# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/von-neumann-debiasing/. The authors are listed in prov/0S9GAW.jsonl.

"""Von Neumann's trick and Peres's iterated version.

The input is a list of bits that are independent and have the same unknown
probability p of being 1, with 0 < p < 1. Both functions return bits that are
independent and exactly unbiased, given the number of bits returned.
"""


def von_neumann_debiasing(bits: list[int]) -> list[int]:
    """Read the bits in pairs: 01 gives 0, 10 gives 1, 00 and 11 give nothing."""
    out = []  # @line L1
    for i in range(0, len(bits) - 1, 2):  # @line L2
        a, b = bits[i], bits[i + 1]
        if a != b:  # @line L3
            out.append(a)
    return out  # @line L4


def peres_debiasing(bits: list[int], depth: int = 64) -> list[int]:
    """Peres's iterated procedure, cut off after `depth` levels of recursion.

    Psi(x) = vN(x) ++ Psi(u) ++ Psi(v), where u holds the XOR of each pair and
    v holds one bit of each equal pair. The recursion runs on an explicit stack
    in the same output order. Depth 1 is von Neumann's trick.
    """
    out: list[int] = []
    stack: list[tuple[list[int], int]] = [(list(bits), depth)]
    while stack:
        x, level = stack.pop()
        if level <= 0 or len(x) < 2:  # @line L5
            continue
        u, v = [], []
        for i in range(0, len(x) - 1, 2):
            a, b = x[i], x[i + 1]
            if a != b:
                out.append(a)  # the von Neumann part of line L8
                u.append(1)  # @line L6
            else:
                u.append(0)
                v.append(a)  # @line L7
        stack.append((v, level - 1))  # @line L8: Psi(v) is popped after the whole of Psi(u)
        stack.append((u, level - 1))
    return out
