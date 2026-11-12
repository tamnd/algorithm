# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/covariance-model/. The authors are listed in prov/9XQKJ4.jsonl.

"""A covariance model (CM) built from a consensus structure, with CYK alignment.

The construction follows Eddy and Durbin (1994): a guide tree of nodes
(ROOT, MATP, MATL, MATR, BIF, BEGL, BEGR, END) is made from the consensus
secondary structure, and each node is expanded into states. State types:

    S  start           (no emission)
    P  pair emission   (emits x_i on the left and x_j on the right)
    L  left emission   (match ML or insert IL)
    R  right emission  (match MR or insert IR)
    D  delete          (no emission)
    B  bifurcation     (splits into two S states)
    E  end             (emits the empty string)

Scores are integers (log-odds in some unit). CYK finds the parse of the
highest total score. Subsequences are half-open: x[i:j].
"""

from typing import Callable, Optional

NEG = float("-inf")

# The states of each node type, in order. Split states come first.
NODE_STATES = {
    "ROOT": [("S", "S"), ("IL", "L"), ("IR", "R")],
    "MATP": [("MP", "P"), ("ML", "L"), ("MR", "R"), ("D", "D"), ("IL", "L"), ("IR", "R")],
    "MATL": [("ML", "L"), ("D", "D"), ("IL", "L")],
    "MATR": [("MR", "R"), ("D", "D"), ("IR", "R")],
    "BIF": [("B", "B")],
    "BEGL": [("S", "S")],
    "BEGR": [("S", "S"), ("IL", "L")],
    "END": [("E", "E")],
}
SPLIT = {"ROOT": 1, "MATP": 4, "MATL": 2, "MATR": 2, "BIF": 1, "BEGL": 1, "BEGR": 1, "END": 1}


def parse_structure(s: str) -> list:
    """Return pair[i] = partner of column i, or -1, for a dot-bracket string."""
    pair, stack = [-1] * len(s), []
    for i, c in enumerate(s):
        if c == "(":
            stack.append(i)
        elif c == ")":
            j = stack.pop()
            pair[i], pair[j] = j, i
    if stack:
        raise ValueError("unbalanced structure")
    return pair


def guide_tree(structure: str) -> list:
    """Return the guide tree nodes in preorder.

    Each node is a dict with keys type, cols (consensus columns it covers)
    and next (the child nodes: one for a chain node, two for BIF, none for END).
    """
    pair = parse_structure(structure)
    nodes: list = []
    tasks = [("ROOT", 0, len(structure), None)]  # (start type, a, b, (bif index, side))
    while tasks:
        start, a, b, link = tasks.pop()
        nodes.append({"type": start, "cols": (), "next": []})
        if link is not None:
            nodes[link[0]]["next"][link[1]] = len(nodes) - 1
        prev = len(nodes) - 1
        while True:
            if a == b:
                kind, cols = "END", ()
            elif pair[a] == b - 1:
                kind, cols = "MATP", (a, b - 1)
            elif pair[a] == -1:
                kind, cols = "MATL", (a,)
            elif pair[b - 1] == -1:
                kind, cols = "MATR", (b - 1,)
            else:
                kind, cols = "BIF", ()
            nodes.append({"type": kind, "cols": cols, "next": []})
            idx = len(nodes) - 1
            nodes[prev]["next"].append(idx)
            prev = idx
            if kind == "END":
                break
            if kind == "MATP":
                a, b = a + 1, b - 1
            elif kind == "MATL":
                a += 1
            elif kind == "MATR":
                b -= 1
            else:
                k = pair[a] + 1
                nodes[idx]["next"] = [None, None]
                tasks.append(("BEGR", k, b, (idx, 1)))
                tasks.append(("BEGL", a, k, (idx, 0)))
                break
    return nodes


class CM:
    """A covariance model: states, their children and their scores."""

    def __init__(self, structure: str, consensus: Optional[str] = None):
        self.structure = structure
        self.consensus = consensus
        self.nodes = guide_tree(structure)
        self.states: list = []  # dicts: name, type, node, children (list of int)
        first = []
        for n, node in enumerate(self.nodes):
            first.append(len(self.states))
            for name, typ in NODE_STATES[node["type"]]:
                self.states.append({"name": name, "type": typ, "node": n, "children": []})
        for n, node in enumerate(self.nodes):
            f, t = first[n], node["type"]
            if t == "BIF":
                self.states[f]["children"] = [first[node["next"][0]], first[node["next"][1]]]
                continue
            if t == "END":
                continue
            nxt = node["next"][0]
            nsplit = list(range(first[nxt], first[nxt] + SPLIT[self.nodes[nxt]["type"]]))
            names = [nm for nm, _ in NODE_STATES[t]]
            ins = [f + p for p, nm in enumerate(names) if nm in ("IL", "IR")]
            for p in range(SPLIT[t]):
                self.states[f + p]["children"] = ins + nsplit
            for p, nm in enumerate(names):
                v = f + p
                if nm == "IL":
                    self.states[v]["children"] = [w for w in ins if w >= v] + nsplit
                elif nm == "IR":
                    self.states[v]["children"] = [v] + nsplit
        self.trans: dict = {}  # (v, w) -> score
        self.emit: list = [dict() for _ in self.states]  # v -> {residue or pair: score}
        self.bifurcations = sum(1 for s in self.states if s["type"] == "B")

    def set_scores(self, trans: Callable[[int, int], int], emit: Callable[[int, str], int]) -> None:
        """Set every transition score t(v, w) and every emission score e(v, a)."""
        for v, s in enumerate(self.states):
            for w in s["children"]:
                if s["type"] != "B":
                    self.trans[(v, w)] = trans(v, w)
            if s["type"] == "P":
                for a in "ACGU":
                    for b in "ACGU":
                        self.emit[v][a + b] = emit(v, a + b)
            elif s["type"] in ("L", "R"):
                for a in "ACGU":
                    self.emit[v][a] = emit(v, a)


def toy_scores(cm: CM) -> None:
    """A small integer scoring scheme for examples.

    Match pair states score 3 for a Watson-Crick pair, 1 for G-U and -4
    otherwise, whatever the consensus letters. Match single states score
    1 for the consensus letter and -1 otherwise. Insert states score 0.
    A move into a delete or an insert state costs 3, staying in an insert
    state costs 1, and the other moves are free.
    """
    wc = {"AU", "UA", "GC", "CG"}
    gu = {"GU", "UG"}

    def emit(v: int, a: str) -> int:
        st = cm.states[v]
        node = cm.nodes[st["node"]]
        if st["name"] == "MP":
            return 3 if a in wc else (1 if a in gu else -4)
        if st["name"] in ("ML", "MR"):
            col = node["cols"][0] if st["name"] == "ML" else node["cols"][-1]
            return 1 if cm.consensus and cm.consensus[col] == a else -1
        return 0

    def trans(v: int, w: int) -> int:
        tw = cm.states[w]["name"]
        if tw in ("IL", "IR"):
            return -1 if v == w else -3
        if tw == "D":
            return -3
        return 0

    cm.set_scores(trans, emit)


def cyk(cm: CM, x: str) -> tuple:
    """Fill the CYK table: a[v][i][j] = best score of state v generating x[i:j].

    Returns (table, counts) where counts = (cells, split terms). The cost is
    Theta(M L^2) cells and Theta(M L^2 + B L^3) time, with M states, B
    bifurcation states and L = len(x).
    """
    L, M = len(x), len(cm.states)
    a = [[[NEG] * (L + 1) for _ in range(L + 1)] for _ in range(M)]
    cells = splits = 0
    for v in range(M - 1, -1, -1):  # @line L1
        st = cm.states[v]
        typ, ch, em = st["type"], st["children"], cm.emit[v]
        tr = [cm.trans.get((v, w), 0) for w in ch]
        av = a[v]
        for d in range(L + 1):  # @line L2
            for i in range(L - d + 1):  # @line L3
                j = i + d  # @line L4
                cells += 1
                best = NEG  # @line L11
                if typ == "E":
                    best = 0 if d == 0 else NEG  # @line L5
                elif typ == "B":
                    left, right = a[ch[0]], a[ch[1]]
                    for k in range(i, j + 1):  # @line L6
                        splits += 1
                        val = left[i][k] + right[k][j]
                        if val > best:
                            best = val
                elif typ in ("S", "D"):
                    for w, t in zip(ch, tr):  # @line L7
                        val = t + a[w][i][j]
                        if val > best:
                            best = val
                elif typ == "P":
                    if d >= 2:
                        e = em[x[i] + x[j - 1]]  # @line L8
                        for w, t in zip(ch, tr):
                            val = e + t + a[w][i + 1][j - 1]
                            if val > best:
                                best = val
                elif typ == "L":
                    if d >= 1:
                        e = em[x[i]]  # @line L9
                        for w, t in zip(ch, tr):
                            val = e + t + a[w][i + 1][j]
                            if val > best:
                                best = val
                else:  # R
                    if d >= 1:
                        e = em[x[j - 1]]  # @line L10
                        for w, t in zip(ch, tr):
                            val = e + t + a[w][i][j - 1]
                            if val > best:
                                best = val
                av[i][j] = best
    return a, (cells, splits)  # @line L12: the score is a[0][0][L]


def cyk_align(cm: CM, x: str) -> tuple:
    """Return (score, parse) of the best parse of the whole of x from the root.

    The parse is a list of (state, i, j) in preorder. Ties go to the first child.
    """
    a, _ = cyk(cm, x)
    L = len(x)
    score = a[0][0][L]
    if score == NEG:
        return score, []
    parse, stack = [], [(0, 0, L)]
    while stack:
        v, i, j = stack.pop()
        parse.append((v, i, j))
        st = cm.states[v]
        typ, ch = st["type"], st["children"]
        val = a[v][i][j]
        if typ == "E":
            continue
        if typ == "B":
            for k in range(i, j + 1):
                if a[ch[0]][i][k] + a[ch[1]][k][j] == val:
                    stack.append((ch[1], k, j))
                    stack.append((ch[0], i, k))
                    break
            continue
        if typ == "P":
            e, ii, jj = cm.emit[v][x[i] + x[j - 1]], i + 1, j - 1
        elif typ == "L":
            e, ii, jj = cm.emit[v][x[i]], i + 1, j
        elif typ == "R":
            e, ii, jj = cm.emit[v][x[j - 1]], i, j - 1
        else:
            e, ii, jj = 0, i, j
        for w in ch:
            if e + cm.trans[(v, w)] + a[w][ii][jj] == val:
                stack.append((w, ii, jj))
                break
    return score, parse


def cyk_scan(cm: CM, x: str, window: int) -> tuple:
    """Return (score, i, j) of the best local hit x[i:j] with j - i <= window."""
    a, _ = cyk(cm, x)
    best = (NEG, 0, 0)
    for i in range(len(x) + 1):
        for j in range(i, min(len(x), i + window) + 1):
            if a[0][i][j] > best[0]:
                best = (a[0][i][j], i, j)
    return best


def parse_pairs(cm: CM, parse: list) -> list:
    """Return the base pairs (i, j-1) emitted by P states in a parse."""
    return [(i, j - 1) for v, i, j in parse if cm.states[v]["type"] == "P"]
