# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/karp-miller-tree/. The authors are listed in prov/V1GHKA.jsonl.

"""The Karp-Miller coverability tree of a Petri net.

A net with P places is a list of transitions, each a pair (pre, post) of
tuples of P non-negative ints. A marking is a tuple of P values; an
omega-marking may also hold OMEGA (math.inf), which stands for "as many
tokens as you like". With math.inf, OMEGA - k = OMEGA + k = OMEGA.
"""

import math

OMEGA = math.inf

Marking = tuple[float, ...]
Net = list[tuple[tuple[int, ...], tuple[int, ...]]]


def _leq(a: Marking, b: Marking) -> bool:
    return all(x <= y for x, y in zip(a, b))


def karp_miller_tree(net: Net, m0: tuple[int, ...]) -> list[tuple[Marking, int, int]]:
    """Build the Karp-Miller tree of (net, m0).

    Return the nodes as a list of (label, parent index, transition index);
    the root is node 0 with parent -1 and transition -1. A node whose label
    equals the label of a proper ancestor is a leaf and is not expanded.
    Precondition: all vectors have the length of m0 and are non-negative.
    Cost: finite for every net (Dickson's lemma and Koenig's lemma), but the
    tree can be larger than any primitive recursive function of the net size.
    """
    nodes: list[tuple[Marking, int, int]] = [(tuple(m0), -1, -1)]  # @line L1
    work = [0]
    while work:  # @line L2
        x = work.pop()  # @line L3
        label = nodes[x][0]
        y = nodes[x][1]
        duplicate = False
        while y >= 0:  # @line L4
            if nodes[y][0] == label:
                duplicate = True
                break
            y = nodes[y][1]
        if duplicate:
            continue
        for t, (pre, post) in enumerate(net):  # @line L5
            if not _leq(pre, label):
                continue
            n = tuple(label[p] - pre[p] + post[p] for p in range(len(label)))  # @line L6
            m = list(n)
            y = x
            while y >= 0:  # @line L7
                ly = nodes[y][0]
                if _leq(ly, n) and ly != n:
                    for p in range(len(n)):  # @line L8
                        if ly[p] < n[p]:
                            m[p] = OMEGA
                y = nodes[y][1]
            nodes.append((tuple(m), x, t))  # @line L9
            work.append(len(nodes) - 1)
    return nodes  # @line L10


def coverable(net: Net, m0: tuple[int, ...], target: tuple[int, ...]) -> bool:
    """Is some marking reachable from m0 at least target in each place?"""
    return any(_leq(target, label) for label, _, _ in karp_miller_tree(net, m0))


def unbounded_places(net: Net, m0: tuple[int, ...]) -> set[int]:
    """The places that can hold an unbounded number of tokens."""
    return {p for label, _, _ in karp_miller_tree(net, m0) for p, v in enumerate(label) if v == OMEGA}
