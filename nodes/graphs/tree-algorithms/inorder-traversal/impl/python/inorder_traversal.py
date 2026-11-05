# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/inorder-traversal/. The authors are listed in prov/JDE4T3.jsonl.


def inorder(left: list[int], right: list[int], root: int) -> list[int]:
    """Return the nodes of a binary tree in inorder (left subtree, node, right subtree).

    The binary tree is rooted at `root` (or empty if root == -1), unweighted,
    and has the nodes 0 .. n-1. left[x] and right[x] are the children of x,
    or -1 for an empty subtree. The walk uses an explicit stack, so a tree of
    height 10^5 needs no deep recursion. Time Θ(n), extra space Θ(h).
    """
    n = len(left)
    if len(right) != n or not -1 <= root < n:
        raise ValueError("left and right must have the same length and root must be -1 or a node")
    stack: list[int] = []  # @line L1
    out: list[int] = []
    x = root
    pushes = 0
    while x != -1 or stack:  # @line L2
        while x != -1:  # @line L3
            pushes += 1  # @line L4
            if pushes > n:
                raise ValueError("the links do not form a binary tree")
            stack.append(x)
            x = left[x]
        x = stack.pop()  # @line L5
        out.append(x)  # @line L6
        x = right[x]  # @line L7
    return out  # @line L8


def inorder_keys(left: list[int], right: list[int], root: int, key: list) -> list:
    """Return the keys of the nodes in inorder; sorted if the tree is a binary search tree."""
    return [key[x] for x in inorder(left, right, root)]
