# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/suffix-tree-from-suffix-array/. The authors are listed in prov/Q1HEHJ.jsonl.

SENTINEL = "\0"


class Node:
    """A suffix tree node. depth is the string depth; start is the start of a suffix below it.

    The label of the edge into the node is text[start + parent.depth : start + depth].
    leaf is the suffix number for a leaf and -1 for an internal node.
    """

    __slots__ = ("depth", "start", "leaf", "children")

    def __init__(self, depth: int, start: int, leaf: int = -1) -> None:
        self.depth = depth
        self.start = start
        self.leaf = leaf
        self.children: list[Node] = []


def suffix_array(t: str) -> list[int]:
    """A simple suffix array, for the tests and the examples."""
    return sorted(range(len(t)), key=lambda i: t[i:])


def lcp_array(t: str, sa: list[int]) -> list[int]:
    """Kasai's algorithm: lcp[i] is the longest common prefix of the suffixes sa[i-1] and sa[i]; lcp[0] = 0."""
    n = len(t)
    rank = [0] * n
    for i, p in enumerate(sa):
        rank[p] = i
    lcp = [0] * n
    h = 0
    for p in range(n):
        if rank[p] > 0:
            q = sa[rank[p] - 1]
            while p + h < n and q + h < n and t[p + h] == t[q + h]:
                h += 1
            lcp[rank[p]] = h
            if h > 0:
                h -= 1
        else:
            h = 0
    return lcp


def suffix_tree_from_sa(t: str, sa: list[int], lcp: list[int]) -> Node:
    """Build the suffix tree of t from its suffix array and LCP array in O(n) time.

    t must end with a symbol that occurs nowhere else, so that every suffix ends at a leaf.
    """
    n = len(t)
    root = Node(0, 0)
    stack = [root]  # @line L1
    for i in range(n):
        h, last = lcp[i], None  # @line L2
        while stack[-1].depth > h:  # @line L3
            last = stack.pop()
        top = stack[-1]
        if top.depth < h:  # @line L4
            assert last is not None
            u = Node(h, last.start)
            top.children[-1] = u
            u.children.append(last)
            stack.append(u)
            top = u
        v = Node(n - sa[i], sa[i], sa[i])  # @line L5
        top.children.append(v)
        stack.append(v)
    return root  # @line L6


def build(s: str) -> tuple[str, Node]:
    """Append the sentinel to s and build its suffix tree through the suffix array."""
    if SENTINEL in s:
        raise ValueError("the text must not contain the sentinel")
    t = s + SENTINEL
    sa = suffix_array(t)
    return t, suffix_tree_from_sa(t, sa, lcp_array(t, sa))


def edge_label(t: str, parent: Node, child: Node) -> str:
    return t[child.start + parent.depth: child.start + child.depth]


def check_invariant(t: str, root: Node) -> None:
    """Every internal node but the root branches, children are sorted by their first symbol,
    and each leaf spells its suffix."""
    leaves = 0
    stack: list[tuple[Node, str]] = [(root, "")]
    while stack:
        x, path = stack.pop()
        assert len(path) == x.depth
        if x.leaf >= 0:
            assert not x.children and path == t[x.leaf:]
            leaves += 1
            continue
        assert x is root or len(x.children) >= 2, "unary internal node"
        firsts = [edge_label(t, x, c)[0] for c in x.children]
        assert firsts == sorted(firsts) and len(set(firsts)) == len(firsts)
        for c in x.children:
            assert c.depth > x.depth and t.startswith(path, c.start)
            stack.append((c, path + edge_label(t, x, c)))
    assert leaves == len(t)
