# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zhang-shasha-algorithm/. The authors are listed in prov/Y3PPPP.jsonl.

from typing import Callable, Hashable, Optional


def _postorder(children: list[list[int]], root: int) -> tuple[list[int], list[int]]:
    """Return (order, lml): the nodes in postorder, and for position k
    (1-based) the 1-based position of the leftmost leaf of that node.
    Uses an explicit stack, so deep trees are safe."""
    order: list[int] = []
    pos: dict[int, int] = {}
    lml: list[int] = [0]
    stack = [(root, 0)]
    while stack:
        v, k = stack.pop()
        if k < len(children[v]):
            stack.append((v, k + 1))
            stack.append((children[v][k], 0))
            continue
        order.append(v)
        pos[v] = len(order)
        if children[v]:
            lml.append(lml[pos[children[v][0]]])
        else:
            lml.append(pos[v])
    return order, lml


def _keyroots(lml: list[int]) -> list[int]:
    """The keyroots in increasing order: for each leftmost leaf, the
    highest postorder position that has it."""
    best: dict[int, int] = {}
    for i in range(1, len(lml)):
        best[lml[i]] = i
    return sorted(best.values())


def tree_edit_distance(
    children1: list[list[int]],
    labels1: list[Hashable],
    children2: list[list[int]],
    labels2: list[Hashable],
    delete: Optional[Callable[[Hashable], float]] = None,
    insert: Optional[Callable[[Hashable], float]] = None,
    rename: Optional[Callable[[Hashable, Hashable], float]] = None,
    root1: int = 0,
    root2: int = 0,
) -> float:
    """Tree edit distance of two ordered, labelled, rooted trees (Zhang-Shasha).

    Tree t has the nodes 0 .. n_t - 1 with n_t >= 1; children_t[v] lists the
    children of v from left to right, and labels_t[v] is its label. The
    trees are not weighted. By default every deletion and insertion costs 1,
    and a rename costs 0 for equal labels and 1 otherwise.
    Time O(n1 n2 min(depth1, leaves1) min(depth2, leaves2)), space O(n1 n2).
    """
    if delete is None:
        delete = lambda a: 1  # noqa: E731
    if insert is None:
        insert = lambda b: 1  # noqa: E731
    if rename is None:
        rename = lambda a, b: 0 if a == b else 1  # noqa: E731
    o1, l1 = _postorder(children1, root1)  # @line L1
    o2, l2 = _postorder(children2, root2)
    n1, n2 = len(o1), len(o2)
    dl = [0] + [delete(labels1[v]) for v in o1]
    ins = [0] + [insert(labels2[w]) for w in o2]
    lab1 = [None] + [labels1[v] for v in o1]
    lab2 = [None] + [labels2[w] for w in o2]
    k1 = _keyroots(l1)  # @line L2
    k2 = _keyroots(l2)
    td = [[0.0] * (n2 + 1) for _ in range(n1 + 1)]
    fd = [[0.0] * (n2 + 1) for _ in range(n1 + 1)]
    for i in k1:  # @line L3
        li = l1[i]
        for j in k2:  # @line L4
            lj = l2[j]
            fd[li - 1][lj - 1] = 0  # @line L5
            for i1 in range(li, i + 1):  # @line L6
                fd[i1][lj - 1] = fd[i1 - 1][lj - 1] + dl[i1]
            row = fd[li - 1]
            for j1 in range(lj, j + 1):  # @line L7
                row[j1] = row[j1 - 1] + ins[j1]
            for i1 in range(li, i + 1):  # @line L8
                cur, prev = fd[i1], fd[i1 - 1]
                d_i1 = dl[i1]
                tree_i = l1[i1] == li
                for j1 in range(lj, j + 1):  # @line L9
                    a = prev[j1] + d_i1
                    b = cur[j1 - 1] + ins[j1]
                    if tree_i and l2[j1] == lj:  # @line L10
                        c = prev[j1 - 1] + rename(lab1[i1], lab2[j1])
                        best = min(a, b, c)  # @line L11
                        cur[j1] = best
                        td[i1][j1] = best  # @line L12
                    else:
                        c = fd[l1[i1] - 1][l2[j1] - 1] + td[i1][j1]
                        cur[j1] = min(a, b, c)  # @line L13
    return td[n1][n2]  # @line L14
