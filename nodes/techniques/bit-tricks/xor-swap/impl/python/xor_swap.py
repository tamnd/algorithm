# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/xor-swap/. The authors are listed in prov/G8X0J3.jsonl.


def xor_swap(a: list[int], i: int, j: int) -> None:
    """Exchange a[i] and a[j] in place with three XORs and no temporary.

    The items are integers. Python's ^ acts on the infinite two's complement
    form, so the swap is also correct for negative integers and for words of
    any width. When i == j nothing changes. Cost: O(1) word operations.
    """
    if i == j:  # @line L1
        return
    a[i] ^= a[j]  # @line L2
    a[j] ^= a[i]  # @line L3
    a[i] ^= a[j]  # @line L4


def xor_swap_unguarded(a: list[int], i: int, j: int) -> None:
    """The same three XORs without the test of line L1 (zeroes a[i] when i == j)."""
    a[i] ^= a[j]
    a[j] ^= a[i]
    a[i] ^= a[j]
