# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/preorder-traversal/. The authors are listed in prov/K1CRY0.jsonl.


def preorder(children: list[list[int]], root: int = 0) -> list[int]:
    """Return the vertices of a rooted ordered tree in preorder.

    The tree has the vertices 0 .. n-1 and is not weighted. children[v] lists
    the children of v from left to right; root is the root. Precondition: the
    lists describe a tree rooted at root (each vertex other than the root is in
    exactly one list, and every vertex is reachable from the root). An empty
    list of lists gives the empty order.

    The stack holds one (vertex, next child index) pair for each vertex on the
    path from the root, so there is no recursion. Time Theta(n), extra space
    O(h) for the height h.
    """
    if not children:
        return []
    out = [root]  # @line L1
    stack = [[root, 0]]  # @line L2
    while stack:  # @line L3
        top = stack[-1]
        v, i = top  # @line L4
        if i < len(children[v]):  # @line L5
            top[1] = i + 1  # @line L6
            c = children[v][i]  # @line L7
            out.append(c)  # @line L8
            stack.append([c, 0])  # @line L9
        else:
            stack.pop()  # @line L10
    return out  # @line L11


def children_from_parents(parent: list[int]) -> tuple[list[list[int]], int]:
    """Turn a parent array (parent[root] = -1) into child lists in increasing order, and the root."""
    children: list[list[int]] = [[] for _ in parent]
    root = -1
    for v, p in enumerate(parent):
        if p < 0:
            root = v
        else:
            children[p].append(v)
    return children, root
