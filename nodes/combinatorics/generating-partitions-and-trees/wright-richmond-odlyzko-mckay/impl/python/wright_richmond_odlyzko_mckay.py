# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wright-richmond-odlyzko-mckay/. The authors are listed in prov/MPQVRK.jsonl.

from collections.abc import Iterator


def free_trees(n: int) -> Iterator[tuple[int, ...]]:
    """Yield every unlabeled free tree with n nodes once.

    Each tree is given as the canonical level sequence of its rooted version:
    the tree is rooted at its center, or, if it has two centers, at the center
    chosen by the rule of Wright, Richmond, Odlyzko and McKay. The sequences
    come in decreasing lexicographic order, from the path to the star.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return
    if n <= 2:
        yield tuple(range(n))
        return

    # 1-based arrays; index 0 is unused. Start with the path rooted at a center.
    half = n // 2
    L = [0] + list(range(0, half + 1)) + list(range(1, (n + 1) // 2))
    par = [0] * (n + 1)  # par[i]: parent of node i, and par[1] = 0
    top = [0] * (n + 1)  # top[i]: the child of the root whose subtree holds i
    mx = [0] * (n + 1)  # mx[i]: the largest level in top[i] .. i
    state = {"p": n, "s2": n + 1, "s3": n + 1}  # s2, s3: starts of T2 and T3

    def rebuild(lo: int) -> None:
        """Recompute par, top, mx, s2 and s3 for positions lo .. n."""
        for i in range(lo, n + 1):
            if L[i] == 0:
                par[i], top[i], mx[i] = 0, i, 0
                continue
            j = i - 1
            while L[j] >= L[i]:
                j = par[j]
            par[i] = j
            if L[i] == 1:
                top[i], mx[i] = i, 1
            else:
                top[i], mx[i] = top[i - 1], max(mx[i - 1], L[i])
        starts = [i for i in range(3, n + 1) if L[i] == 1][:2] + [n + 1, n + 1]
        state["s2"], state["s3"] = starts[0], starts[1]

    rebuild(1)

    def bh_next(p: int, shortcut: bool) -> bool:
        """The Beyer-Hedetniemi successor, starting the scan at p.

        Positions after p are treated as 1. It also keeps top, mx, s2 and s3.
        """
        while L[p] == 1:
            p -= 1
        if p <= 1:
            return False
        s2, s3 = state["s2"], state["s3"]
        if shortcut and L[p] == 2 and L[p - 1] == 1:
            L[p] = 1
            par[p] = par[p - 1]
            top[p], mx[p] = p, 1
            if s2 < p:
                s3 = min(s3, p)
            else:
                s2, s3 = p, (p + 1 if p < n else n + 1)
        else:
            if s2 >= p:
                s2 = s3 = n + 1
            elif s3 >= p:
                s3 = n + 1
            d = p - par[p]
            for i in range(p, n + 1):
                L[i] = L[i - d]
                if d + par[i - d] < p:
                    par[i] = par[i - d]
                else:
                    par[i] = d + par[i - d]
                if L[i] == 1:
                    top[i], mx[i] = i, 1
                    if s2 > n:
                        s2 = i
                    elif s3 > n:
                        s3 = i
                else:
                    top[i], mx[i] = top[i - 1], max(mx[i - 1], L[i])
            p = n
        state["p"], state["s2"], state["s3"] = p, s2, s3
        return True

    def valid() -> bool:
        """Test conditions (A), (B1), (B2), (C) and (D) on the current L."""
        s2, s3 = state["s2"], state["s3"]
        if s2 > n:  # (A) fails: the root has one child
            return False
        k = s2 - 2  # |T1|
        h1, h2 = mx[s2 - 1], mx[s3 - 1]
        if h1 == h2:  # (B1)
            return True
        if h1 != h2 + 1 or 2 * k > n:  # (B2) or (C) fails
            return False
        if 2 * k == n:  # (D): e(T1) is at most 0, 1 + e(T2), ..., 1 + e(Tm)
            for j in range(2, k + 1):
                a, b = L[1 + j] - 1, L[k + j]
                if a != b:
                    return a < b
        return True

    while True:
        yield tuple(L[1:])
        if not bh_next(state["p"], True):  # @line L1
            return
        if valid():  # @line L2
            continue
        k = state["s2"] - 2  # @line L3
        if not bh_next(k + 1, False):  # @line L4
            return
        if L[k + 1] > 1:  # @line L5
            h = mx[n]  # @line L6
            for j in range(1, h + 1):  # @line L7
                L[n - h + j] = j
            rebuild(n - h + 1)
            state["p"] = n
