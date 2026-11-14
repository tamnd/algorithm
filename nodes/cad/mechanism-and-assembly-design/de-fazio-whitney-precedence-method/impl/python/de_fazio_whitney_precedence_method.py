# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/de-fazio-whitney-precedence-method/. The authors are listed in prov/RRPKFP.jsonl.
"""The De Fazio-Whitney question method for linear assembly sequences.

For each liaison i = {u, v} the method asks two questions:
  Q1: which liaisons must be done before liaison i can be done?  -> pre[i]
  Q2: which liaisons must not be done yet when liaison i is done? -> post[i]
Each answer is a monotone logical formula over the liaisons. A state is the
set of liaisons made so far. A step may add several liaisons at once, and it
passes when pre[i] holds and post[i] does not, in the state before the step,
for every liaison i that it makes.

Here an oracle answers the questions from the geometry of a product of
axis-aligned boxes, under this model: linear and monotone (one new part per
step, placed parts never move), connected (the new part touches a placed
part, and all its liaisons with placed parts are made in that step), and a
part goes in by one translation from infinity; it can come in along -d
when it could leave the placed parts along d, for some d in the motion set.
"""

from assembly_boxes import AXES6, blocks, face_contact

TRUE = ("and", ())
FALSE = ("or", ())


def var(i):
    return ("var", i)


def f_and(items):
    items = tuple(items)
    if FALSE in items:
        return FALSE
    items = tuple(x for x in items if x != TRUE)
    return items[0] if len(items) == 1 else ("and", items)


def f_or(items):
    items = tuple(items)
    if TRUE in items:
        return TRUE
    items = tuple(x for x in items if x != FALSE)
    return items[0] if len(items) == 1 else ("or", items)


def evaluate(f, state):
    """The value of formula f when exactly the liaisons in state are made."""
    tag = f[0]
    if tag == "var":
        return f[1] in state
    if tag == "and":
        return all(evaluate(g, state) for g in f[1])
    if tag == "or":
        return any(evaluate(g, state) for g in f[1])
    raise ValueError("answers are monotone formulas")


def show(f, names=None):
    """The formula as text, with liaison i written l<i+1> unless names given."""
    tag = f[0]
    if f == TRUE:
        return "true"
    if f == FALSE:
        return "false"
    if tag == "var":
        return names[f[1]] if names else "l%d" % (f[1] + 1)
    sep = " and " if tag == "and" else " or "
    return "(" + sep.join(show(g, names) for g in f[1]) + ")"


def liaisons_of(boxes):
    """The contact liaisons as a list of pairs (u, v) with u < v."""
    n = len(boxes)
    return [(u, v) for u in range(n) for v in range(u + 1, n)
            if face_contact(boxes[u], boxes[v]) is not None]


def answer_questions(boxes, liaisons, motions=AXES6):
    """The answers to Q1 and Q2 for every liaison, from the geometry."""
    n = len(boxes)
    at = [[k for k, (u, v) in enumerate(liaisons) if w in (u, v)] for w in range(n)]

    def present(w):  # part w is placed, when at least two parts are placed
        return f_or(var(k) for k in at[w])

    pre, post = [], []
    for (u, v) in liaisons:  # @line L1
        alone = any(not blocks(boxes[v], boxes[u], d) or not blocks(boxes[u], boxes[v], d)
                    for d in motions)
        pre.append(TRUE if alone else FALSE)  # @line L2
        terms = []
        for a, b in ((u, v), (v, u)):  # b comes in next to a
            # b is stuck when, for every d, some blocker of b along d is present
            stuck = f_and(f_or(present(w) for w in range(n)
                               if w != b and blocks(boxes[b], boxes[w], d))
                          for d in motions)
            terms.append(f_and((present(a), stuck)))
        post.append(f_or(terms))  # @line L3
    return pre, post


def generate(n, liaisons, pre, post):
    """The diagram of liaison states and its start states.

    A state is a frozenset of liaison indices. Returns (starts, arcs) where
    arcs maps a state to the list of states one passing step away.
    """
    adj = [0] * n
    for (u, v) in liaisons:
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    full = frozenset(range(len(liaisons)))
    reach = 1
    while True:
        grow = reach
        for p in range(n):
            if reach >> p & 1:
                grow |= adj[p]
        if grow == reach:
            break
        reach = grow
    if reach != (1 << n) - 1:
        return [], {}, full          # a product in pieces has no sequence

    def made(q):
        return frozenset(k for k, (u, v) in enumerate(liaisons) if q >> u & 1 and q >> v & 1)

    def passes(x, delta):
        return all(evaluate(pre[i], x) and not evaluate(post[i], x) for i in delta)

    starts = []
    for k, (u, v) in enumerate(liaisons):  # @line L4
        q = 1 << u | 1 << v
        if passes(frozenset(), made(q)):
            starts.append((made(q), q))
    arcs = {}
    todo = list(starts)
    seen = {}
    while todo:  # @line L5
        x, q = todo.pop()
        if x in arcs:
            continue
        arcs[x] = []
        for p in range(n):  # @line L6
            if q >> p & 1 or not adj[p] & q:
                continue
            q2 = q | 1 << p
            y = made(q2)
            delta = y - x  # @line L7
            if passes(x, delta):  # @line L8
                arcs[x].append(y)  # @line L9
                if y not in seen:
                    seen[y] = q2
                    todo.append((y, q2))
    start_states = sorted({x for x, _ in starts}, key=sorted)
    return start_states, arcs, full


def count_sequences(n, liaisons, pre, post):
    """The number of liaison sequences, by counting paths in the diagram."""
    if n == 1:
        return 1
    starts, arcs, full = generate(n, liaisons, pre, post)
    memo = {}

    def paths(x):  # @line L10
        if x == full:
            return 1
        if x not in memo:
            memo[x] = sum(paths(y) for y in arcs.get(x, ()))
        return memo[x]

    return sum(paths(x) for x in starts)


def sequences(n, liaisons, pre, post):
    """Every liaison sequence as a tuple of states, from the first to the full one."""
    if n == 1:
        return [()]
    starts, arcs, full = generate(n, liaisons, pre, post)
    out = []

    def walk(x, path):
        if x == full:
            out.append(tuple(path))
            return
        for y in arcs.get(x, ()):
            walk(y, path + [y])

    for x in starts:
        walk(x, [x])
    return out
