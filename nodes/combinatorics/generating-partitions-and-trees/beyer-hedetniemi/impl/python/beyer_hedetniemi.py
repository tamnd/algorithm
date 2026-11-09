# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/beyer-hedetniemi/. The authors are listed in prov/VB34EV.jsonl.

from collections.abc import Iterator


def rooted_trees(n: int, parents: bool = False) -> Iterator:
    """Yield every unlabeled rooted tree with n nodes once, as its canonical level sequence.

    The sequences come in decreasing lexicographic order, from the path
    (0, 1, ..., n - 1) to the star (0, 1, ..., 1). If parents is True, yield
    pairs (levels, par) where par[i] is the 1-based preorder position of the
    parent of node i + 1, and 0 for the root.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return
    # 1-based arrays; index 0 is unused. Start with the path.
    L = list(range(-1, n))  # L[i] = i - 1
    par = list(range(-1, n))  # par[i] = i - 1, and par[1] = 0
    p = n
    while True:
        if parents:
            yield tuple(L[1:]), tuple(par[1:])
        else:
            yield tuple(L[1:])
        while L[p] == 1:  # @line L1
            p -= 1
        if p <= 1:  # @line L2
            return
        if L[p] == 2 and L[p - 1] == 1:  # @line L3
            L[p] = 1  # @line L4
            par[p] = par[p - 1]
        else:  # @line L5
            d = p - par[p]  # @line L6
            for i in range(p, n + 1):  # @line L7
                L[i] = L[i - d]  # @line L8
                if d + par[i - d] < p:  # @line L9
                    par[i] = par[i - d]
                else:
                    par[i] = d + par[i - d]
            p = n  # @line L10
