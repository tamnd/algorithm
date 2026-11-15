# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/string-transformation-synthesis/. The authors are listed in prov/NBNPFH.jsonl.
"""String transformation synthesis in the style of FlashFill, on a small language.

The language:
    program   Concat(f1, ..., fn), a tuple of atoms, n >= 1
    atom      ("const", s)            the non-empty string s
              ("sub", p1, p2)         the input from position p1 up to position p2
    position  ("cpos", k)             k >= 0: index k; k < 0: index len + 1 + k
              ("pos", r1, r2, c)      the c-th index t where a run of token r1 ends
                                      and a run of token r2 starts; c in +-1..+-3,
                                      negative c counts from the right
Tokens are "D" (digits), "L" (letters), "S" (spaces) and "E" (the empty token,
which matches at every index); r1 and r2 are not both "E". A run is a maximal
block of characters of one token. A substring is defined only when both
positions are defined and p1 < p2, so every atom gives a non-empty string, and
a program is undefined when one of its atoms is undefined.

synthesize(examples) builds one DAG for each example, over the indices of the
output, with all atoms that produce each piece of the output. It intersects
the DAGs and returns the cheapest program, or None. The cost is the tuple
(number of characters in constants, number of atoms, sum of position costs),
compared in this order. A position costs 1 for CPos(0) and CPos(-1), 2 for a
token position, 3 for CPos(k) with k > 0 and 4 for CPos(k) with k < -1.
"""

TOKENS = ("D", "L", "S", "E")
COUNTS = (1, 2, 3, -1, -2, -3)


def token_of(ch):
    if ch.isdigit():
        return "D"
    if ch.isalpha():
        return "L"
    if ch == " ":
        return "S"
    return None


def _ends_run(s, t, tok):
    if tok == "E":
        return True
    return t > 0 and token_of(s[t - 1]) == tok and (t == len(s) or token_of(s[t]) != tok)


def _starts_run(s, t, tok):
    if tok == "E":
        return True
    return t < len(s) and token_of(s[t]) == tok and (t == 0 or token_of(s[t - 1]) != tok)


def eval_pos(p, s):
    """The index that position p denotes in s, or None."""
    if p[0] == "cpos":
        k = p[1]
        t = k if k >= 0 else len(s) + 1 + k
        return t if 0 <= t <= len(s) else None
    _, r1, r2, c = p
    ms = [t for t in range(len(s) + 1) if _ends_run(s, t, r1) and _starts_run(s, t, r2)]
    if c > 0:
        return ms[c - 1] if c <= len(ms) else None
    return ms[c] if -c <= len(ms) else None


def eval_atom(f, s):
    if f[0] == "const":
        return f[1]
    a, b = eval_pos(f[1], s), eval_pos(f[2], s)
    if a is None or b is None or a >= b:
        return None
    return s[a:b]


def run(program, s):
    """The output of the program on s, or None if it is undefined."""
    out = []
    for f in program:
        r = eval_atom(f, s)
        if r is None:
            return None
        out.append(r)
    return "".join(out)


def positions(max_len):
    """All position expressions that can be defined on a string of length <= max_len."""
    ps = [("cpos", k) for k in range(-(max_len + 1), max_len + 1)]
    for r1 in TOKENS:
        for r2 in TOKENS:
            if r1 == "E" and r2 == "E":
                continue
            for c in COUNTS:
                ps.append(("pos", r1, r2, c))
    return ps


def pos_cost(p):
    if p[0] == "cpos":
        if p[1] in (0, -1):
            return 1
        return 3 if p[1] > 0 else 4
    return 2


def atom_cost(f):
    """(characters in constants, atoms, position cost); tuples compare in this order."""
    if f[0] == "const":
        return (len(f[1]), 1, 0)
    return (0, 1, pos_cost(f[1]) + pos_cost(f[2]))


def add_cost(a, b):
    return tuple(x + y for x, y in zip(a, b))


def program_cost(program):
    c = (0, 0, 0)
    for f in program:
        c = add_cost(c, atom_cost(f))
    return c


def position_sets(s):
    """For each index t of s, the set of position expressions that denote t."""
    sets = {t: set() for t in range(len(s) + 1)}
    for p in positions(len(s)):
        t = eval_pos(p, s)
        if t is not None:
            sets[t].add(p)
    return {t: frozenset(v) for t, v in sets.items()}


def example_dag(s, out):
    """The labels W[(i, j)] of the DAG of one example: (constants, substring choices)."""
    pset = position_sets(s)
    w = {}
    for i in range(len(out)):  # @line L8
        for j in range(i + 1, len(out) + 1):
            piece = out[i:j]
            subs = []
            for a in range(len(s) - (j - i) + 1):
                if s[a:a + j - i] == piece:  # @line L10
                    subs.append((pset[a], pset[a + j - i]))  # @line L11
            w[(i, j)] = (frozenset([piece]), tuple(subs))  # @line L9
    return w  # @line L12


def intersect_labels(x, y):
    consts = x[0] & y[0]
    subs = []
    for a1, a2 in x[1]:
        for b1, b2 in y[1]:
            c1 = a1 & b1
            if c1:
                c2 = a2 & b2
                if c2:
                    subs.append((c1, c2))
    return (consts, tuple(subs))


def label_empty(lab):
    return not lab[0] and not lab[1]


def label_count(lab):
    return len(lab[0]) + sum(len(p1) * len(p2) for p1, p2 in lab[1])


def best_atom(lab):
    """The cheapest atom of a label, with its cost."""
    best = None
    for c in sorted(lab[0]):
        cand = (atom_cost(("const", c)), ("const", c))
        if best is None or cand < best:
            best = cand
    for p1s, p2s in lab[1]:
        p1 = min(p1s, key=lambda p: (pos_cost(p), p))
        p2 = min(p2s, key=lambda p: (pos_cost(p), p))
        f = ("sub", p1, p2)
        cand = (atom_cost(f), f)
        if best is None or cand < best:
            best = cand
    return best


def product_edges(dags, outs, u):
    """The edges of the product DAG that leave the state u, with their labels."""
    k = len(dags)
    res = []

    def go(j, label, w):
        if j == k:
            res.append((tuple(w), label))
            return
        for nxt in range(u[j] + 1, len(outs[j]) + 1):
            lab = dags[j][(u[j], nxt)]
            lab = lab if label is None else intersect_labels(label, lab)  # @line L5
            if not label_empty(lab):
                go(j + 1, lab, w + [nxt])

    go(0, None, [])
    return res


def product_dag(examples):
    """The reachable part of the intersection of the example DAGs."""
    dags = [example_dag(s, o) for s, o in examples]  # @line L1
    outs = [o for _, o in examples]
    start = tuple(0 for _ in examples)  # @line L2
    goal = tuple(len(o) for o in outs)
    edges = {}
    seen = {start}
    frontier = [start]
    while frontier:  # @line L3
        u = frontier.pop()
        edges[u] = product_edges(dags, outs, u)  # @line L4
        for w, _ in edges[u]:
            if w not in seen:
                seen.add(w)
                frontier.append(w)
    return start, goal, edges


def synthesize(examples):
    """The cheapest program consistent with all examples, or None."""
    if any(o == "" for _, o in examples):
        return None
    start, goal, edges = product_dag(examples)
    order = sorted(edges, key=sum)  # every edge raises the sum of the indices
    best = {start: ((0, 0, 0), ())}
    for u in order:
        if u not in best:
            continue
        cu, pu = best[u]
        for w, lab in edges[u]:
            ca, f = best_atom(lab)
            cand = (add_cost(cu, ca), pu + (f,))
            if w not in best or cand < best[w]:  # @line L6
                best[w] = cand
    if goal not in best:
        return None
    return best[goal][1]  # @line L7


def count_programs(examples, max_atoms):
    """The number of programs with at most max_atoms atoms consistent with all examples."""
    if any(o == "" for _, o in examples):
        return 0
    start, goal, edges = product_dag(examples)
    order = sorted(edges, key=sum)
    ways = {start: {0: 1}}
    for u in order:
        for w, lab in edges[u]:
            c = label_count(lab)
            for n, v in ways.get(u, {}).items():
                if n < max_atoms:
                    d = ways.setdefault(w, {})
                    d[n + 1] = d.get(n + 1, 0) + v * c
    return sum(ways.get(goal, {}).values())


def show(program):
    parts = []
    for f in program:
        if f[0] == "const":
            parts.append(f"ConstStr({f[1]!r})")
        else:
            parts.append(f"SubStr({_show_pos(f[1])}, {_show_pos(f[2])})")
    return "Concat(" + ", ".join(parts) + ")"


def _show_pos(p):
    if p[0] == "cpos":
        return f"CPos({p[1]})"
    return f"Pos({p[1]}, {p[2]}, {p[3]})"
