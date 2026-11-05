# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/level-order-traversal/. The authors are listed in prov/F8MRDB.jsonl.

from collections import deque


def level_order_traversal(left: list[int], right: list[int], root: int) -> list[int]:
    """Return the nodes of a binary tree in level order.

    The nodes are 0 .. n-1; left[x] and right[x] are the children of x, or -1 if the
    child is missing, and root is the root, or -1 for the empty tree. Nodes come by
    increasing depth, and from left to right within a depth. Time O(n), extra space
    O(w) for the largest number w of nodes at one depth.
    """
    if root == -1:  # @line L1
        return []
    queue: deque[int] = deque([root])  # @line L2
    order: list[int] = []
    while queue:  # @line L3
        x = queue.popleft()  # @line L4
        order.append(x)  # @line L5
        if left[x] != -1:  # @line L6
            queue.append(left[x])
        if right[x] != -1:  # @line L7
            queue.append(right[x])
    return order
