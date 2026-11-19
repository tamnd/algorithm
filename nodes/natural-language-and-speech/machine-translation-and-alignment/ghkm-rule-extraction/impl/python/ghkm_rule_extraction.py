# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ghkm-rule-extraction/. The authors are listed in prov/6NN595.jsonl.

"""Minimal GHKM rule extraction (Galley, Hopkins, Knight and Marcu 2004).

Input: a parse tree of the target sentence e (its leaves are the target
positions 1..l), the source sentence f = f_1..f_m, and word alignment links
(j, i) that join source position j to target position i.

span(n) is the set of source positions aligned to the leaves under node n.
complement_span(n) is the set of source positions aligned to the leaves
outside the subtree of n. A node n is a frontier node if span(n) is not empty
and the closure [min span(n), max span(n)] holds no position of
complement_span(n). Each frontier node gives one minimal rule: its left side is
the tree fragment from n down to the next frontier nodes (which become
variables) or to the words; its right side is the source words of the closure,
with the closure of each variable node replaced by the variable.

An unaligned source word goes to the lowest frontier node whose closure holds
it. The root is given the whole source sentence [1, m].
"""

from dataclasses import dataclass, field
from typing import Union


@dataclass(eq=False)
class Node:
    label: str
    kids: list = field(default_factory=list)  # Node or int (target position)


@dataclass
class Rule:
    node: Node
    lhs: str
    rhs: tuple[str, ...]
    variables: list[Node]


def parse(text: str) -> tuple[Node, list[str]]:
    """Parse '(S (NP (PRP he)) (VP (VB go)))'. Leaves become positions 1..l."""
    tokens = text.replace("(", " ( ").replace(")", " ) ").split()
    words: list[str] = []
    pos = 0

    def node() -> Node:
        nonlocal pos
        assert tokens[pos] == "("
        n = Node(tokens[pos + 1])
        pos += 2
        while tokens[pos] != ")":
            if tokens[pos] == "(":
                n.kids.append(node())
            else:
                words.append(tokens[pos])
                n.kids.append(len(words))
                pos += 1
        pos += 1
        return n

    root = node()
    if pos != len(tokens):
        raise ValueError("text after the tree")
    return root, words


def tree_string(n: Node, words: list[str]) -> str:
    return n.label + "(" + " ".join(words[k - 1] if isinstance(k, int) else tree_string(k, words) for k in n.kids) + ")"


def preorder(n: Node) -> list[Node]:
    out = [n]
    for k in n.kids:
        if isinstance(k, Node):
            out.extend(preorder(k))
    return out


def frontier_nodes(root: Node, m: int, links: set[tuple[int, int]]) -> tuple[set[Node], dict, dict]:
    """Return (frontier set, span, complement_span)."""
    src: dict[int, set[int]] = {}
    for j, i in links:
        if not 1 <= j <= m:
            raise ValueError(f"source position {j} out of range")
        src.setdefault(i, set()).add(j)

    span: dict[Node, set[int]] = {}

    def kid_span(k: Union[Node, int]) -> set[int]:
        return src.get(k, set()) if isinstance(k, int) else span[k]

    for n in reversed(preorder(root)):  # @line L1
        span[n] = set().union(*[kid_span(k) for k in n.kids])
    comp: dict[Node, set[int]] = {root: set()}
    for n in preorder(root):  # @line L2
        for a, k in enumerate(n.kids):
            if isinstance(k, Node):
                comp[k] = comp[n].union(*[kid_span(b) for c, b in enumerate(n.kids) if c != a])
    frontier = set()
    for n in preorder(root):  # @line L3
        s = span[n]
        if s and not any(min(s) <= j <= max(s) for j in comp[n]):
            frontier.add(n)
    return frontier, span, comp


def extract_minimal_rules(root: Node, words: list[str], f: list[str], links: set[tuple[int, int]]) -> list[Rule]:
    m = len(f)
    for j, i in links:
        if not 1 <= i <= len(words):
            raise ValueError(f"target position {i} out of range")
    frontier, span, _ = frontier_nodes(root, m, links)
    rules = []
    for n in preorder(root):  # @line L4
        if n not in frontier:
            continue
        variables: list[Node] = []

        def fragment(x: Node) -> str:  # @line L5
            parts = []
            for k in x.kids:
                if isinstance(k, int):
                    parts.append(words[k - 1])
                elif k in frontier:
                    parts.append(f"x{len(variables)}:{k.label}")
                    variables.append(k)
                else:
                    parts.append(fragment(k))
            return x.label + "(" + " ".join(parts) + ")"

        lhs = fragment(n)
        lo, hi = (1, m) if n is root else (min(span[n]), max(span[n]))  # @line L6
        starts = {min(span[v]): (v_idx, max(span[v])) for v_idx, v in enumerate(variables)}
        rhs: list[str] = []
        j = lo
        while j <= hi:  # @line L7
            if j in starts:
                v_idx, end = starts[j]
                rhs.append(f"x{v_idx}")
                j = end + 1
            else:
                rhs.append(f[j - 1])
                j += 1
        rules.append(Rule(n, lhs, tuple(rhs), variables))  # @line L8
    return rules  # @line L9


def derive(rule_of: dict, n: Node, words: list[str]) -> tuple[str, list[str]]:
    """Apply the rules from node n down: return (tree string, source words)."""
    rule = rule_of[n]
    lhs, sub = rule.lhs, []
    for v_idx, v in enumerate(rule.variables):
        t, s = derive(rule_of, v, words)
        lhs = lhs.replace(f"x{v_idx}:{v.label}", t, 1)
        sub.append(s)
    out: list[str] = []
    for sym in rule.rhs:
        if sym.startswith("x") and sym[1:].isdigit():
            out.extend(sub[int(sym[1:])])
        else:
            out.append(sym)
    return lhs, out


def brute_force_frontier(root: Node, m: int, links: set[tuple[int, int]]) -> set[Node]:
    """A node is a frontier node if it covers at least one aligned word and every
    source word between its first and last aligned source words is aligned only
    to leaves under the node (or not aligned at all)."""
    out = set()
    for n in preorder(root):
        under = set()
        stack = [n]
        while stack:
            x = stack.pop()
            for k in x.kids:
                if isinstance(k, int):
                    under.add(k)
                else:
                    stack.append(k)
        js = {j for j, i in links if i in under}
        if not js:
            continue
        if all(i in under for j, i in links if min(js) <= j <= max(js)):
            out.add(n)
    return out
