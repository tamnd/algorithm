# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pruefer-decoding/. The authors are listed in prov/BS0MJQ.jsonl.

from collections.abc import Iterator, Sequence


def pruefer_decode(code: Sequence[int]) -> list[tuple[int, int]]:
    """Return the edges of the labeled tree on {1, ..., n} with the given Prüfer code.

    The code has length n - 2 and entries in 1..n, so n = len(code) + 2.
    Edge i (0-based, i < n - 2) joins the leaf removed at step i + 1 of the
    encoder to code[i]; the last edge joins the final leaf to n.
    """
    n = len(code) + 2
    for v in code:
        if not 1 <= v <= n:
            raise ValueError("code entries must lie in 1..n")
    deg = [0] + [1] * n  # @line L1
    for v in code:  # @line L2
        deg[v] += 1
    ptr = 1  # @line L3
    while deg[ptr] != 1:
        ptr += 1
    leaf = ptr  # @line L4
    edges: list[tuple[int, int]] = []
    for v in code:  # @line L5
        edges.append((leaf, v))  # @line L6
        deg[v] -= 1  # @line L7
        if deg[v] == 1 and v < ptr:  # @line L8
            leaf = v
        else:
            ptr += 1  # @line L9
            while deg[ptr] != 1:
                ptr += 1
            leaf = ptr  # @line L10
    edges.append((leaf, n))  # @line L11
    return edges  # @line L12


def labeled_trees(n: int) -> Iterator[list[tuple[int, int]]]:
    """Yield every tree on {1, ..., n}, as an edge list, by decoding all n^(n-2) codes.

    The codes are taken in lexicographic order, so the trees come in the
    order of their Prüfer codes. For n = 1 the single tree has no edge.
    """
    if n < 1:
        raise ValueError("n must be at least 1")
    if n == 1:
        yield []
        return
    code = [1] * (n - 2)
    while True:
        yield pruefer_decode(code)
        i = n - 3
        while i >= 0 and code[i] == n:
            code[i] = 1
            i -= 1
        if i < 0:
            return
        code[i] += 1
