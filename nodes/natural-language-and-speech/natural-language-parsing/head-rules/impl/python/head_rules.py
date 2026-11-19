# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/head-rules/. The authors are listed in prov/EXAQEX.jsonl.

"""Head rules: pick the head child of each phrase and turn a tree into dependencies.

A tree is (label, children). A preterminal is (tag, word) with word a string.
An internal node is (label, list of trees). The table is the head table of
Collins (1999, appendix A) in the form used by the Stanford CollinsHeadFinder,
without its extra AUX and NX entries for the parent. Function tags such as the
"-SBJ" in "NP-SBJ" are removed before a label is looked up.

The words are numbered 1 to n from the left. to_dependencies returns the list
h with h[i] the head of word i, h[0] unused, and 0 for the word that heads the
whole sentence.
"""

from typing import Dict, List, Sequence, Tuple, Union

Tree = Tuple[str, Union[str, list]]

LEFT, RIGHT = "left", "right"

# label -> (direction, priority list). "left" scans the children from the left,
# "right" from the right, once for each label of the list in order.
COLLINS: Dict[str, Tuple[str, Tuple[str, ...]]] = {
    "ADJP": (LEFT, ("NNS", "QP", "NN", "$", "ADVP", "JJ", "VBN", "VBG", "ADJP", "JJR",
                    "NP", "JJS", "DT", "FW", "RBR", "RBS", "SBAR", "RB")),
    "ADVP": (RIGHT, ("RB", "RBR", "RBS", "FW", "ADVP", "TO", "CD", "JJR", "JJ", "IN",
                     "NP", "JJS", "NN")),
    "CONJP": (RIGHT, ("CC", "RB", "IN")),
    "FRAG": (RIGHT, ()),
    "INTJ": (LEFT, ()),
    "LST": (RIGHT, ("LS", ":")),
    "NAC": (LEFT, ("NN", "NNS", "NNP", "NNPS", "NP", "NAC", "EX", "$", "CD", "QP",
                   "PRP", "VBG", "JJ", "JJS", "JJR", "ADJP", "FW")),
    "PP": (RIGHT, ("IN", "TO", "VBG", "VBN", "RP", "FW")),
    "PRN": (LEFT, ()),
    "PRT": (RIGHT, ("RP",)),
    "QP": (LEFT, ("$", "IN", "NNS", "NN", "JJ", "RB", "DT", "CD", "NCD", "QP", "JJR",
                  "JJS")),
    "RRC": (RIGHT, ("VP", "NP", "ADVP", "ADJP", "PP")),
    "S": (LEFT, ("TO", "IN", "VP", "S", "SBAR", "ADJP", "UCP", "NP")),
    "SBAR": (LEFT, ("WHNP", "WHPP", "WHADVP", "WHADJP", "IN", "DT", "S", "SQ", "SINV",
                    "SBAR", "FRAG")),
    "SBARQ": (LEFT, ("SQ", "S", "SINV", "SBARQ", "FRAG")),
    "SINV": (LEFT, ("VBZ", "VBD", "VBP", "VB", "MD", "VP", "S", "SINV", "ADJP", "NP")),
    "SQ": (LEFT, ("VBZ", "VBD", "VBP", "VB", "MD", "VP", "SQ")),
    "UCP": (RIGHT, ()),
    "VP": (LEFT, ("TO", "VBD", "VBN", "MD", "VBZ", "VB", "VBG", "VBP", "VP", "ADJP",
                  "NN", "NNS", "NP")),
    "WHADJP": (LEFT, ("CC", "WRB", "JJ", "ADJP")),
    "WHADVP": (RIGHT, ("CC", "WRB")),
    "WHNP": (LEFT, ("WDT", "WP", "WP$", "WHADJP", "WHPP", "WHNP")),
    "WHPP": (RIGHT, ("IN", "TO", "FW")),
    "X": (RIGHT, ()),
}

# The NP rule of Collins: a list of (direction, label set) steps. Within one step
# the scan goes by position and stops at the first child whose label is in the set.
NP_STEPS = (
    (RIGHT, frozenset(("NN", "NNP", "NNPS", "NNS", "NX", "POS", "JJR"))),
    (LEFT, frozenset(("NP",))),
    (RIGHT, frozenset(("$", "ADJP", "PRN"))),
    (RIGHT, frozenset(("CD",))),
    (RIGHT, frozenset(("JJ", "JJS", "RB", "QP"))),
)


def base_label(label: str) -> str:
    """Return the label without function tags and indices: NP-SBJ-1 gives NP."""
    if label.startswith("-"):
        return label  # -NONE-, -LRB-, -RRB-
    for sep in "-=":
        k = label.find(sep)
        if k > 0:
            label = label[:k]
    return label


def _order(direction: str, m: int) -> range:
    return range(m) if direction == LEFT else range(m - 1, -1, -1)


def np_head(labels: Sequence[str]) -> int:
    """Return the 0-based index of the head child of an NP with these child labels."""
    m = len(labels)
    if labels[m - 1] == "POS":  # @line L15
        return m - 1
    for direction, wanted in NP_STEPS:  # @line L16
        for k in _order(direction, m):  # @line L17
            if labels[k] in wanted:  # @line L18
                return k
    return m - 1  # @line L19


def head_child(label: str, child_labels: Sequence[str], table=None) -> int:
    """Return the 0-based index of the head child of a node.

    label is the parent label and child_labels the labels of its children, in
    order. An unknown parent label scans from the left with an empty list, so
    its head is the leftmost child.
    """
    if table is None:
        table = COLLINS
    labels = [base_label(x) for x in child_labels]
    m = len(labels)
    if m == 0:
        raise ValueError("a node without children has no head child")
    if m == 1:  # @line L1
        return 0
    x = base_label(label)
    if x == "NP" and table is COLLINS:  # @line L2
        return np_head(labels)
    direction, priority = table.get(x, (LEFT, ()))  # @line L3
    order = _order(direction, m)  # @line L4
    for z in priority:  # @line L5
        for k in order:  # @line L6
            if labels[k] == z:  # @line L7
                return k
    return order[0]  # @line L8


def is_preterminal(t: Tree) -> bool:
    return isinstance(t[1], str)


def words(t: Tree) -> List[str]:
    """Return the words of t, left to right."""
    out: List[str] = []
    stack = [t]
    while stack:
        u = stack.pop()
        if is_preterminal(u):
            out.append(u[1])
        else:
            stack.extend(reversed(u[1]))
    return out


def to_dependencies(t: Tree, table=None) -> List[int]:
    """Return h with h[i] the head word of word i (1-based) and 0 for the root word.

    Each node passes up the head word of its head child. Every other child
    attaches its head word to that word. The walk is iterative, children first.
    """
    n = len(words(t))
    h = [0] * (n + 1)
    heads: List[int] = []  # lexical heads of the finished subtrees, left to right
    position = 0
    stack: List[Tuple[Tree, bool]] = [(t, False)]
    while stack:  # @line L9
        u, done = stack.pop()
        if is_preterminal(u):
            position += 1
            heads.append(position)  # @line L10
            continue
        kids = u[1]
        if not kids:
            raise ValueError("an internal node has no children")
        if not done:
            stack.append((u, True))
            for c in reversed(kids):
                stack.append((c, False))
            continue
        m = len(kids)
        child_heads = heads[len(heads) - m:]
        del heads[len(heads) - m:]
        c = head_child(u[0], [k[0] for k in kids], table)  # @line L11
        for k in range(m):  # @line L12
            if k != c:
                h[child_heads[k]] = child_heads[c]
        heads.append(child_heads[c])
    h[heads[0]] = 0  # @line L13
    return h  # @line L14


def read_tree(s: str) -> Tree:
    """Read a tree in Penn Treebank bracket form, such as (S (NP (NN dogs)) (VP (VBP bark)))."""
    tokens = s.replace("(", " ( ").replace(")", " ) ").split()
    pos = 0

    def parse() -> Tree:
        nonlocal pos
        if tokens[pos] != "(":
            raise ValueError("expected (")
        pos += 1
        label = tokens[pos]
        pos += 1
        if tokens[pos] not in ("(", ")"):
            word = tokens[pos]
            pos += 1
            if tokens[pos] != ")":
                raise ValueError("expected ) after a word")
            pos += 1
            return (label, word)
        kids = []
        while tokens[pos] == "(":
            kids.append(parse())
        if tokens[pos] != ")":
            raise ValueError("expected )")
        pos += 1
        return (label, kids)

    tree = parse()
    if pos != len(tokens):
        raise ValueError("text after the tree")
    return tree
