# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/postorder-traversal/. The authors are listed in prov/M0CFJK.jsonl.


def postorder(children: list[list[int]], root: int = 0) -> list[int]:
    """Return the vertices of a rooted ordered tree in postorder.

    The tree has the vertices 0 .. n-1 and is not weighted. children[v] lists
    the children of v from left to right; root is the root. Precondition: the
    lists describe a tree rooted at root. An empty list of lists gives the
    empty order.

    The stack holds one (vertex, next child index) pair for each vertex on the
    path from the root, so there is no recursion. Time Theta(n), extra space
    O(h) for the height h.
    """
    if not children:
        return []
    out: list[int] = []  # @line L1
    stack = [[root, 0]]  # @line L2
    while stack:  # @line L3
        top = stack[-1]
        v, i = top  # @line L4
        if i < len(children[v]):  # @line L5
            top[1] = i + 1  # @line L6
            stack.append([children[v][i], 0])  # @line L7
        else:  # @line L8
            stack.pop()  # @line L9
            out.append(v)  # @line L10
    return out  # @line L11


def evaluate(children: list[list[int]], label: list[str], root: int = 0) -> int:
    """Evaluate an expression tree in postorder: a leaf holds an integer, an inner vertex '+' or '*'."""
    value = [0] * len(children)
    for v in postorder(children, root):
        if not children[v]:
            value[v] = int(label[v])
        elif label[v] == "+":
            value[v] = sum(value[c] for c in children[v])
        else:
            prod = 1
            for c in children[v]:
                prod *= value[c]
            value[v] = prod
    return value[root]
