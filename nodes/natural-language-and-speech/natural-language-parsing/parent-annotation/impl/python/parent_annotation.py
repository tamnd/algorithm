# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parent-annotation/. The authors are listed in prov/SJCKA7.jsonl.

"""Parent annotation of treebank trees, its inverse, and treebank rule estimates.

A tree is (label, word) for a preterminal, with word a string, and
(label, [children]) for any other node. annotate() gives every phrasal node
the label "X^P", where P is the original label of its parent, or root_parent
for the root. Preterminals are kept unchanged unless tags=True. strip() cuts
every label at the first separator, so strip(annotate(t)) == t whenever no
label of t contains the separator. Both walks use an explicit stack: the
children of a node are pushed in reverse, so they are popped, and appended
to the copy of their parent, from left to right.
"""

from collections import Counter
from fractions import Fraction
from typing import Dict, Iterable, List, Tuple, Union

Tree = Tuple[str, Union[str, list]]
Rule = Tuple[str, Tuple[str, ...]]


def is_preterminal(t: Tree) -> bool:
    return isinstance(t[1], str)


def _check_labels(t: Tree, sep: str) -> None:
    stack = [t]
    while stack:
        u = stack.pop()
        if sep in u[0]:
            raise ValueError("label %r already contains the separator %r" % (u[0], sep))
        if not is_preterminal(u):
            stack.extend(u[1])


def annotate(t: Tree, root_parent: str = "ROOT", sep: str = "^", tags: bool = False) -> Tree:
    """Return a copy of t in which each phrasal node X with parent label P is X^P."""
    _check_labels(t, sep)
    out: List[Tree] = []
    stack = [(t, root_parent, out)]  # @line L1
    while stack:  # @line L2
        u, p, dest = stack.pop()  # @line L3
        if is_preterminal(u):  # @line L4
            dest.append((u[0] + sep + p, u[1]) if tags else u)
            continue
        kids: List[Tree] = []
        dest.append((u[0] + sep + p, kids))  # @line L5
        for c in reversed(u[1]):  # @line L6
            stack.append((c, u[0], kids))
    return out[0]  # @line L7


def strip(t: Tree, sep: str = "^") -> Tree:
    """Return a copy of t with every label cut at the first separator."""
    out: List[Tree] = []
    stack = [(t, out)]
    while stack:  # @line L8
        u, dest = stack.pop()
        label = u[0].split(sep, 1)[0]
        if is_preterminal(u):
            dest.append((label, u[1]))
            continue
        kids: List[Tree] = []
        dest.append((label, kids))
        for c in reversed(u[1]):
            stack.append((c, kids))
    return out[0]


def rules(t: Tree) -> List[Rule]:
    """The rules of t, phrasal and lexical, in preorder."""
    out: List[Rule] = []
    stack = [t]
    while stack:
        u = stack.pop()
        if is_preterminal(u):
            out.append((u[0], (u[1],)))
        else:
            out.append((u[0], tuple(c[0] for c in u[1])))
            stack.extend(reversed(u[1]))
    return out


def treebank_pcfg(trees: Iterable[Tree]) -> Dict[Rule, Fraction]:
    """Relative frequency estimates q(A -> alpha) = count(A -> alpha) / count(A)."""
    counts: Counter = Counter()
    for t in trees:
        counts.update(rules(t))
    lhs: Counter = Counter()
    for (a, _), c in counts.items():
        lhs[a] += c
    return {r: Fraction(c, lhs[r[0]]) for r, c in counts.items()}


def tree_probability(t: Tree, q: Dict[Rule, Fraction]) -> Fraction:
    """The product of q over the rules of t (0 if a rule is missing)."""
    p = Fraction(1)
    for r in rules(t):
        p *= q.get(r, Fraction(0))
    return p


def read_tree(s: str) -> Tree:
    """Read a tree in bracket form, such as (S (NP (PRP she)) (VP (VBD left)))."""
    tokens = s.replace("(", " ( ").replace(")", " ) ").split()
    out: List[Tree] = []
    stack: List[Tree] = []
    pos = 0
    while pos < len(tokens):
        if out and not stack:
            raise ValueError("text after the tree")
        tok = tokens[pos]
        dest = stack[-1][1] if stack else out
        if tok == "(":
            if pos + 1 >= len(tokens) or tokens[pos + 1] in ("(", ")"):
                raise ValueError("a bracket needs a label")
            label = tokens[pos + 1]
            if pos + 2 < len(tokens) and tokens[pos + 2] not in ("(", ")"):
                if pos + 3 >= len(tokens) or tokens[pos + 3] != ")":
                    raise ValueError("expected ) after a word")
                dest.append((label, tokens[pos + 2]))
                pos += 4
            else:
                node: Tree = (label, [])
                dest.append(node)
                stack.append(node)
                pos += 2
        elif tok == ")":
            if not stack or not stack[-1][1]:
                raise ValueError("unbalanced ) or a phrase with no children")
            stack.pop()
            pos += 1
        else:
            raise ValueError("unexpected word %r" % tok)
    if stack or len(out) != 1:
        raise ValueError("unbalanced brackets or empty input")
    return out[0]
