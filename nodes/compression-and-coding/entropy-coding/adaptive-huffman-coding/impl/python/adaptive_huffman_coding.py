# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adaptive-huffman-coding/. The authors are listed in prov/E86180.jsonl.

"""Adaptive (dynamic) Huffman coding: algorithm FGK and Vitter's algorithm.

Encoder and decoder keep the same tree and update it after each symbol.
The symbols are bytes. A symbol seen for the first time is sent as the
codeword of the NYT node (not yet transmitted, weight 0) followed by its
8 raw bits.

The nodes are numbered 0, 1, 2, ... from the bottom: `order[k]` is the
node with number k, and the root has the largest number. The two nodes
with numbers 2j and 2j + 1 are siblings. A node number is a fixed place
in the tree: when nodes change numbers, they change places, with their
subtrees.
"""


class _Node:
    __slots__ = ("weight", "parent", "left", "right", "symbol", "num")

    def __init__(self, weight=0, parent=None, symbol=None):
        self.weight = weight
        self.parent = parent
        self.left = None
        self.right = None
        self.symbol = symbol
        self.num = 0

    def is_leaf(self) -> bool:
        return self.left is None


class _Tree:
    def __init__(self, vitter: bool):
        self.vitter = vitter
        self.nyt = _Node()
        self.root = self.nyt
        self.order = [self.nyt]
        self.leaf = {}

    # ---- places in the tree -------------------------------------------
    def _slot(self, node):
        p = node.parent
        return (p, p is not None and p.right is node)

    def _put(self, node, slot, num):
        p, right = slot
        node.parent = p
        if p is not None:
            if right:
                p.right = node
            else:
                p.left = node
        node.num = num
        self.order[num] = node

    def _rotate(self, i, j):
        """Move the node at number i to number j > i; the nodes at numbers
        i + 1 .. j move down by one. Each node takes the place of the
        number it gets."""
        slots = [self._slot(self.order[k]) for k in range(i, j + 1)]
        moving = [self.order[k] for k in range(i + 1, j + 1)] + [self.order[i]]
        for k, node in enumerate(moving):
            self._put(node, slots[k], i + k)

    def _swap(self, a, b):
        sa, sb = self._slot(a), self._slot(b)
        na, nb = a.num, b.num
        self._put(a, sb, nb)
        self._put(b, sa, na)

    # ---- codes --------------------------------------------------------
    def path(self, node) -> str:
        bits = []
        while node.parent is not None:
            bits.append("1" if node.parent.right is node else "0")
            node = node.parent
        return "".join(reversed(bits))

    def _split_nyt(self, symbol):
        """The NYT node becomes an inner node with a new NYT (left) and a
        new leaf for the symbol (right), both of weight 0."""
        old = self.nyt
        new_nyt = _Node(0, old)
        leaf = _Node(0, old, symbol)
        old.left, old.right = new_nyt, leaf
        self.order[0:0] = [new_nyt, leaf]
        for k, node in enumerate(self.order):
            node.num = k
        self.nyt = new_nyt
        self.leaf[symbol] = leaf
        return old, leaf

    # ---- FGK ----------------------------------------------------------
    def _update_fgk(self, symbol):
        # The caller has split the NYT node already for a new symbol.
        q = self.leaf[symbol]  # @line L5
        while q is not None:  # @line L6
            # The leader: the highest-numbered node of the same weight,
            # but never the parent of q. A linear scan finds it here;
            # a list of blocks finds it in O(1) time.
            k = q.num  # @line L7
            while k + 1 < len(self.order) and self.order[k + 1].weight == q.weight:
                k += 1
            if self.order[k] is q.parent:
                k -= 1
            if k != q.num:  # @line L8
                self._swap(q, self.order[k])
            q.weight += 1  # @line L9
            q = q.parent  # @line L10

    # ---- Vitter (algorithm Lambda) ------------------------------------
    def _slide_and_increment(self, p):
        w = p.weight
        leaf = p.is_leaf()
        old_parent = p.parent
        # The block just after p: inner nodes of weight w (p a leaf), or
        # leaves of weight w + 1 (p an inner node).
        k = p.num
        while k + 1 < len(self.order):
            nxt = self.order[k + 1]
            if leaf and not nxt.is_leaf() and nxt.weight == w:
                k += 1
            elif not leaf and nxt.is_leaf() and nxt.weight == w + 1:
                k += 1
            else:
                break
        if k > p.num:
            self._rotate(p.num, k)
        p.weight += 1
        return p.parent if leaf else old_parent

    def _leader_of_leaf_block(self, q):
        k = q.num
        while (
            k + 1 < len(self.order)
            and self.order[k + 1].weight == q.weight
            and self.order[k + 1].is_leaf()
        ):
            k += 1
        return self.order[k]

    def _update_vitter(self, symbol, inner=None):
        # `inner` is the old NYT node when the caller has just split it
        # for a new symbol.
        leaf_to_increment = None
        if inner is not None:
            q, leaf_to_increment = inner, self.leaf[symbol]
        else:
            q = self.leaf[symbol]
            leader = self._leader_of_leaf_block(q)
            if leader is not q:
                self._swap(q, leader)
            if q.parent is not None and q.parent.left is self.nyt:
                leaf_to_increment = q
                q = q.parent
        while q is not None:
            q = self._slide_and_increment(q)
        if leaf_to_increment is not None:
            self._slide_and_increment(leaf_to_increment)

    def update(self, symbol):
        """Count one more occurrence of the symbol. A new symbol first
        gets a leaf by a split of the NYT node."""
        inner = None
        if symbol not in self.leaf:
            inner, _ = self._split_nyt(symbol)
        if self.vitter:
            self._update_vitter(symbol, inner)
        else:
            self._update_fgk(symbol)


def encode(data: bytes, vitter: bool = True) -> str:
    """Encode bytes with algorithm FGK (vitter=False) or Vitter's
    algorithm (vitter=True). The result is a string of '0' and '1'."""
    t = _Tree(vitter)  # @line L1
    out = []
    for s in data:  # @line L2
        if s in t.leaf:  # @line L3
            out.append(t.path(t.leaf[s]))
        else:  # @line L4
            out.append(t.path(t.nyt))
            out.append(format(s, "08b"))
        t.update(s)
    return "".join(out)


def decode(bits: str, count: int, vitter: bool = True) -> bytes:
    t = _Tree(vitter)
    out = bytearray()
    pos = 0
    for _ in range(count):
        node = t.root
        while not node.is_leaf():
            node = node.right if bits[pos] == "1" else node.left
            pos += 1
        if node is t.nyt:
            s = int(bits[pos : pos + 8], 2)
            pos += 8
        else:
            s = node.symbol
        out.append(s)
        t.update(s)
    if pos != len(bits):
        raise ValueError("extra bits after the last symbol")
    return bytes(out)


def check_tree(t: _Tree) -> None:
    """Raise AssertionError unless the tree has the sibling property and,
    for Vitter's algorithm, the order 'leaves of weight w before inner
    nodes of weight w'."""
    order = t.order
    assert order[-1] is t.root
    for k, node in enumerate(order):
        assert node.num == k
        if node.is_leaf():
            assert node.right is None
        else:
            assert node.weight == node.left.weight + node.right.weight
            assert node.left.parent is node and node.right.parent is node
    for k in range(len(order) - 1):
        assert order[k].weight <= order[k + 1].weight
    for k in range(0, len(order) - 1, 2):
        a, b = order[k], order[k + 1]
        assert a.parent is b.parent and a.parent.num > b.num
    if t.vitter:
        for k in range(len(order) - 1):
            a, b = order[k], order[k + 1]
            if a.weight == b.weight:
                assert a.is_leaf() or not b.is_leaf()
