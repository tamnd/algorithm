# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tree-based-group-diffie-hellman/. The authors are listed in prov/B6HWGP.jsonl.
"""Tree-based Group Diffie-Hellman (TGDH) of Kim, Perrig and Tsudik (ACM CCS
2000; ACM TISSEC 2004), with the join and leave operations.

Each member sits at a leaf of a binary tree and holds a secret leaf key. The
key of an inner node is f(g^(k_left k_right)), and its blinded key g^k is
public. A member knows the keys on the path from its leaf to the root, and
the root key is the group key. On a join or a leave, one sponsor picks a new
leaf key and broadcasts the new blinded keys on its path; every other member
then recomputes the keys on its own path.

Simplifications: f(x) = x mod q, the insertion point of a join is the
shallowest rightmost leaf (the paper chooses the shallowest rightmost node,
which can be an inner node), and all messages are one shared public tree.
The protocol here is unauthenticated: it resists only a passive attacker.

The group is the subgroup of quadratic residues modulo the 1024-bit safe
prime of RFC 5054, Appendix A, with g = 4 of prime order q.

For study only. The code is not constant time, and it must not protect real
data.

Lines marked L1 to L9 match the pseudocode on the page.
"""

import secrets

P = int(
    "EEAF0AB9ADB38DD69C33F80AFA8FC5E86072618775FF3C0B9EA2314C"
    "9C256576D674DF7496EA81D3383B4813D692C6E0E0D5D8E250B98BE4"
    "8E495C1D6089DAD15DC7D7B46154D6B6CE8EF4AD69B15D4982559B29"
    "7BCF1885C529F566660E57EC68EDBC3C05726CC02FD4CBF4976EAA9A"
    "FD5138FE8376435B9FC61D2FC0EB06E3",
    16,
)
Q = (P - 1) // 2
G = 4


def f(x: int) -> int:
    """Map a group element to an exponent."""
    return x % Q or 1


class Node:
    def __init__(self, member=None):
        self.left = self.right = self.parent = None
        self.member = member          # set only at a leaf
        self.bk = None                # the blinded key g^k, public


class Member:
    def __init__(self, name: str, rng=secrets.randbelow):
        self.name, self.rng = name, rng
        self.k = 1 + rng(Q - 1)
        self.leaf = Node(self)
        self.leaf.bk = pow(G, self.k, P)                                # @line L3
        self.exps = 1

    def group_key(self, tree: "Tree") -> int:
        """Walk from the leaf to the root with the siblings' blinded keys."""
        k, node = self.k, self.leaf
        while node.parent is not None:
            k = f(pow(tree.sibling(node).bk, k, P))                     # @line L1
            self.exps += 1
            node = node.parent
        return k

    def refresh(self, tree: "Tree"):
        """The sponsor's step: a new leaf key, then new blinded keys on the path."""
        self.k = 1 + self.rng(Q - 1)                                    # @line L5
        self.leaf.bk = pow(G, self.k, P)
        self.exps += 1
        k, node = self.k, self.leaf
        while node.parent is not None:                                  # @line L6
            k = f(pow(tree.sibling(node).bk, k, P))
            node = node.parent
            self.exps += 1
            if node.parent is not None:                                 # the root's blinded key is never needed
                node.bk = pow(G, k, P)                                  # @line L2
                self.exps += 1


class Tree:
    def __init__(self, first: Member):
        self.root = first.leaf

    @staticmethod
    def sibling(node: Node) -> Node:
        p = node.parent
        return p.right if p.left is node else p.left

    def leaves(self, node=None):
        node = node or self.root
        if node.member is not None:
            return [node.member]
        return self.leaves(node.left) + self.leaves(node.right)

    def height(self, node=None) -> int:
        node = node or self.root
        if node.member is not None:
            return 0
        return 1 + max(self.height(node.left), self.height(node.right))

    def _replace(self, old: Node, new: Node):
        p = old.parent
        new.parent = p
        if p is None:
            self.root = new
        elif p.left is old:
            p.left = new
        else:
            p.right = new

    def join(self, new: Member) -> Member:
        """The new member broadcasts its blinded leaf key (L3). Returns the sponsor."""
        level, best = [self.root], None
        while best is None:                                             # @line L4: the shallowest rightmost leaf
            leaves = [n for n in level if n.member is not None]
            if leaves:
                best = leaves[-1]
            level = [c for n in level if n.member is None for c in (n.left, n.right)]
        inner = Node()
        self._replace(best, inner)
        inner.left, inner.right = best, new.leaf
        best.parent = new.leaf.parent = inner
        sponsor = best.member
        sponsor.refresh(self)
        return sponsor

    def leave(self, gone: Member) -> Member:
        """Remove the leaf, promote its sibling (L7). Returns the sponsor."""
        leaf = gone.leaf
        sib = self.sibling(leaf)
        self._replace(leaf.parent, sib)                                 # @line L7
        leaf.parent = None
        node = sib
        while node.member is None:                                      # @line L8: the rightmost leaf under the sibling
            node = node.right
        sponsor = node.member
        sponsor.refresh(self)
        return sponsor


def all_keys(tree: Tree):
    """Every member computes the group key."""
    return {m.name: m.group_key(tree) for m in tree.leaves()}         # @line L9
