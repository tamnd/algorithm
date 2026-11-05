# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/morris-traversal/. The authors are listed in prov/V880D8.jsonl.


def morris_traversal(left: list[int], right: list[int], root: int) -> list[int]:
    """Return the nodes of a binary tree in inorder, with O(1) extra space.

    The nodes are 0 .. n-1; left[x] and right[x] are the children of x, or -1 if the
    child is missing, and root is the root, or -1 for the empty tree. The function
    writes temporary threads into right and removes them again, so on return both
    lists are as they were. Time O(n); extra space O(1) besides the output list.
    """
    order: list[int] = []
    x = root  # @line L1
    while x != -1:  # @line L2
        if left[x] == -1:  # @line L3
            order.append(x)  # @line L4
            x = right[x]
        else:
            p = left[x]  # @line L5
            while right[p] != -1 and right[p] != x:
                p = right[p]
            if right[p] == -1:  # @line L6
                right[p] = x
                x = left[x]
            else:
                right[p] = -1  # @line L7
                order.append(x)
                x = right[x]
    return order  # @line L8
