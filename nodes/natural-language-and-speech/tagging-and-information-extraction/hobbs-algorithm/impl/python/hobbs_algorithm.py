# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hobbs-algorithm/. The authors are listed in prov/3QNB55.jsonl.

"""The naive algorithm of Hobbs (1978) for resolving a pronoun.

The input is the parse tree of the sentence that holds the pronoun, the parse
trees of the earlier sentences (most recent last), and the NP node of the
pronoun. The trees follow Hobbs's grammar: S, NP, VP, PP, Det and Nominal
(his N-bar) nodes, with a Nominal child under each NP that has a noun head.

The algorithm proposes NP nodes in a fixed order. The first proposed NP that
agrees with the pronoun in gender, number and person is the answer. The
search is a heuristic: it has no guarantee of finding the right antecedent.
"""

from collections import deque
from typing import Dict, Iterator, List, Optional, Sequence


class Node:
    """A parse tree node. An NP may carry agreement features and a word for display."""

    def __init__(self, label: str, children: Sequence["Node"] = (), word: str = "",
                 gender: Optional[str] = None, number: Optional[str] = None,
                 person: Optional[int] = None):
        self.label = label
        self.children = list(children)
        self.word = word
        self.feats = {"gender": gender, "number": number, "person": person}

    def __repr__(self) -> str:
        return "%s(%s)" % (self.label, self.text())

    def text(self) -> str:
        if self.word:
            return self.word
        return " ".join(c.text() for c in self.children)


def parents(root: Node) -> Dict[int, Node]:
    """Map id(node) to the parent node, for every node below root."""
    out = {}
    stack = [root]
    while stack:
        n = stack.pop()
        for c in n.children:
            out[id(c)] = n
            stack.append(c)
    return out


def agrees(a: Node, b: Node) -> bool:
    """True if no feature is set on both nodes with different values."""
    for k in ("gender", "number", "person"):
        x, y = a.feats[k], b.feats[k]
        if x is not None and y is not None and x != y:
            return False
    return True


def bfs(root: Node, stop_below=lambda n: False) -> Iterator[Node]:
    """Breadth-first, left-to-right walk from root (excluded); do not expand nodes with stop_below."""
    q = deque(root.children)
    while q:
        n = q.popleft()
        yield n
        if not stop_below(n):
            q.extend(n.children)


def side_of_path(x: Node, path: List[Node], left: bool, stop_np_s: bool = False) -> Iterator[Node]:
    """Walk the branches below x to the left (or right) of the path, breadth first, left to right.

    path[0] is x and path[-1] is the node the path ends at. Path nodes are walked
    through but not yielded, and the end node is not expanded. Each yielded node
    comes with nothing else; callers test its label.
    """
    on_path = {id(n): k for k, n in enumerate(path)}
    q = deque([x])
    while q:
        n = q.popleft()
        k = on_path.get(id(n))
        if k is not None:
            if k == len(path) - 1:
                continue
            nxt = path[k + 1]
            pos = next(i for i, c in enumerate(n.children) if c is nxt)
            if left:
                q.extend(n.children[:pos])
                q.append(nxt)
            else:
                q.append(nxt)
                q.extend(n.children[pos + 1:])
            continue
        yield n
        if not (stop_np_s and n.label in ("NP", "S")):
            q.extend(n.children)


def up_to_np_or_s(node: Node, par: Dict[int, Node]) -> Optional[List[Node]]:
    """Go up from node to the first NP or S above it. Return the path from that node down to node."""
    path = [node]
    n = node
    while id(n) in par:
        n = par[id(n)]
        path.append(n)
        if n.label in ("NP", "S"):
            return path[::-1]
    return None


def proposals(pron_np: Node, tree: Node, earlier: Sequence[Node]) -> Iterator[Node]:
    """Yield the NP nodes in the order the naive algorithm proposes them (no agreement test)."""
    par = parents(tree)
    path = up_to_np_or_s(pron_np, par)  # @line L1
    if path is None:
        raise ValueError("the pronoun NP has no NP or S above it")
    x = path[0]  # @line L2
    for n in side_of_path(x, path, left=True):  # @line L3
        if n.label == "NP":
            m = par[id(n)]
            between = False
            while m is not x:
                if m.label in ("NP", "S"):
                    between = True
                    break
                m = par[id(m)]
            if between:
                yield n
    while True:
        if x is tree:  # @line L4
            for t in reversed(earlier):
                for n in bfs(t):
                    if n.label == "NP":
                        yield n
            return
        path = up_to_np_or_s(x, par)  # @line L5
        if path is None:
            raise ValueError("the root of the tree is not an S node")
        x = path[0]
        if x.label == "NP" and path[1].label != "Nominal":  # @line L6
            yield x
        for n in side_of_path(x, path, left=True):  # @line L7
            if n.label == "NP":
                yield n
        if x.label == "S":  # @line L8
            for n in side_of_path(x, path, left=False, stop_np_s=True):
                if n.label == "NP":
                    yield n
        # @line L9: go back to step 4


def resolve(pron_np: Node, tree: Node, earlier: Sequence[Node] = ()) -> Optional[Node]:
    """Return the first proposed NP that agrees with the pronoun, or None."""
    for n in proposals(pron_np, tree, earlier):
        if n is not pron_np and agrees(n, pron_np):  # @line L10
            return n
    return None
