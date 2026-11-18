# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/semistructured-merge/. The authors are listed in prov/30FJFE.jsonl.
"""Semistructured merge, after Apel, Liebig, Brandl, Lengauer and Kästner (ESEC/FSE 2011).

A program is a tree of nodes. A node has a kind and a name. A nonterminal node,
such as a class, has children whose order does not matter; a terminal node, such
as a method, has a body of text lines. The merge matches children by (kind, name),
merges matched nonterminals again, and merges the bodies of matched terminals
with a line-based three-way merge. The tree part is superimposition; deletions are
handled by the rules of merge_node.
"""

from collections.abc import Sequence
from typing import NamedTuple, Optional

from txdiff import lcs_matching


class Node(NamedTuple):
    kind: str
    name: str
    children: tuple["Node", ...] = ()
    body: Optional[tuple[str, ...]] = None  # None for a nonterminal node

    @property
    def key(self) -> tuple[str, str]:
        return (self.kind, self.name)

    @property
    def terminal(self) -> bool:
        return self.body is not None


class Conflict(NamedTuple):
    path: tuple[str, ...]  # the names from the root to the node
    reason: str  # "lines", "added on both sides", "deleted in A, changed in B" or "deleted in B, changed in A"


def line_merge(a: Sequence[str], o: Sequence[str], b: Sequence[str],
               names: tuple[str, str, str] = ("A", "O", "B")) -> tuple[list[str], int]:
    """Return the line-based three-way merge of a and b with base o, and its number of conflicts.

    This is the chunk rule of diff3, with longest matchings of o with a and of o with b.
    """
    a_of, b_of = dict(lcs_matching(o, a)), dict(lcs_matching(o, b))
    out: list[str] = []
    conflicts = 0
    lo = la = lb = 0
    for x in [x for x in range(len(o)) if x in a_of and x in b_of] + [len(o)]:
        ja, jb = (a_of[x], b_of[x]) if x < len(o) else (len(a), len(b))
        pa, po, pb = list(a[la:ja]), list(o[lo:x]), list(b[lb:jb])
        if po == pb or pa == pb:
            out += pa  # changed in A only, or the same change on both sides, or no change
        elif po == pa:
            out += pb  # changed in B only
        else:
            conflicts += 1
            out += [f"<<<<<<< {names[0]}", *pa, f"||||||| {names[1]}", *po, "=======", *pb, f">>>>>>> {names[2]}"]
        if x < len(o):
            out.append(o[x])  # a line that all three files keep
        lo, la, lb = x + 1, ja + 1, jb + 1
    return out, conflicts


def merge_node(a: Node, o: Optional[Node], b: Node,
               path: tuple[str, ...] = ()) -> tuple[Node, list[Conflict]]:
    """Merge two nodes with the same key, given their base o, which is None if both sides added the node."""
    if a.key != b.key or (o is not None and o.key != a.key) or a.terminal != b.terminal:
        raise ValueError("the nodes do not match")
    path = path + (a.name,)
    if a.terminal:  # @line L1
        body, k = line_merge(a.body, o.body if o is not None and o.terminal else (), b.body)
        reason = "lines" if o is not None else "added on both sides"
        return a._replace(body=tuple(body)), [Conflict(path, reason)] * k
    in_a = {c.key: c for c in a.children}
    in_o = {c.key: c for c in o.children} if o is not None else {}
    in_b = {c.key: c for c in b.children}
    keys = [c.key for c in a.children] + [c.key for c in b.children if c.key not in in_a]  # @line L2
    children: list[Node] = []
    conflicts: list[Conflict] = []
    for key in keys:  # @line L3
        x, y, z = in_a.get(key), in_o.get(key), in_b.get(key)
        if x is not None and z is not None:  # @line L4
            child, more = merge_node(x, y, z, path)
            children.append(child)
            conflicts += more
        elif y is None:  # @line L5
            children.append(x if x is not None else z)  # added on one side
        else:
            kept, side = (x, "B") if x is not None else (z, "A")
            if kept != y:  # @line L6
                children.append(kept)  # deleted on one side, changed on the other: keep it and report
                other = "A" if side == "B" else "B"
                conflicts.append(Conflict(path + (kept.name,), f"deleted in {side}, changed in {other}"))
            # Otherwise the node is unchanged on one side and deleted on the other, so it is dropped.
    return a._replace(children=tuple(children)), conflicts  # @line L7


def semistructured_merge(a: Node, o: Node, b: Node) -> tuple[Node, list[Conflict]]:
    """Merge the trees a and b of two revisions with the tree o of their base; return the tree and the conflicts."""
    return merge_node(a, o, b)


def to_lines(node: Node, depth: int = 0) -> list[str]:
    """Print a tree as lines: a nonterminal as "kind name {", its children and "}", a terminal as its body."""
    pad = "    " * depth
    if node.terminal:
        return [pad + line if line else line for line in node.body]
    out = [f"{pad}{node.kind} {node.name} {{"]
    for child in node.children:
        out += to_lines(child, depth + 1)
    return out + [pad + "}"]
