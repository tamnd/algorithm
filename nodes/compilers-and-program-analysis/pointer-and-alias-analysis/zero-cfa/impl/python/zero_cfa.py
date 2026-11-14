# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zero-cfa/. The authors are listed in prov/JG6AT6.jsonl.
"""0-CFA: the functions that each expression of a higher-order program may
evaluate to, with one abstract binding per variable.

label(term) numbers the nodes of a toylam term in preorder and links each
variable to its binder. A node is a tuple whose children are labels:

    ("var", x, b)        b is the binder (label, name), or None if x is free
    ("lam", x, body)     binds (label, x)
    ("fix", f, x, body)  binds (label, f) and (label, x)
    ("app", t1, t2)
    ("let", x, t1, t2)   binds (label, x)
    ("if", t1, t2, t3)   ("prim", op, t1, t2)   ("int", k)   ("bool", b)

zero_cfa(term) returns (nodes, C, R). C[l] is the set of labels of the lam
and fix nodes that node l may evaluate to, and R[b] the same for the binder
b. Only code that can run is analysed: the body of a function is visited
when some reachable call may call it. The solver is a worklist over the
sets C[l] and R[b] that sends only the new elements along each edge.
Cost: O(n^3) for a term of n nodes.
"""

from collections import deque


def label(term):
    nodes = []
    stack = [(term, {}, None, 0)]  # (term, scope, parent label, child slot)
    while stack:
        t, scope, parent, slot = stack.pop()
        here = len(nodes)
        tag = t[0]
        if tag == "var":
            nodes.append(("var", t[1], scope.get(t[1])))
        elif tag in ("int", "bool"):
            nodes.append(t)
        else:
            nodes.append(None)  # filled when the children have labels
        if parent is not None:
            node = list(nodes[parent])
            node[slot] = here
            nodes[parent] = tuple(node)
        if tag == "lam":
            nodes[here] = ("lam", t[1], None)
            stack.append((t[2], {**scope, t[1]: (here, t[1])}, here, 2))
        elif tag == "fix":
            nodes[here] = ("fix", t[1], t[2], None)
            inner = {**scope, t[1]: (here, t[1]), t[2]: (here, t[2])}
            stack.append((t[3], inner, here, 3))
        elif tag == "app":
            nodes[here] = ("app", None, None)
            stack.append((t[2], scope, here, 2))
            stack.append((t[1], scope, here, 1))
        elif tag == "let":
            nodes[here] = ("let", t[1], None, None)
            stack.append((t[3], {**scope, t[1]: (here, t[1])}, here, 3))
            stack.append((t[2], scope, here, 2))
        elif tag == "if":
            nodes[here] = ("if", None, None, None)
            for slot2 in (3, 2, 1):
                stack.append((t[slot2], scope, here, slot2))
        elif tag == "prim":
            nodes[here] = ("prim", t[1], None, None)
            stack.append((t[3], scope, here, 3))
            stack.append((t[2], scope, here, 2))
    return nodes


def param(node, lab):
    """The binder of the parameter and the body label of a lam or fix node."""
    if node[0] == "lam":
        return (lab, node[1]), node[2]
    return (lab, node[2]), node[3]


def zero_cfa(term):
    nodes = label(term)  # @line L1
    val, delta, succ = {}, {}, {}  # @line L2
    watch = {}  # ("C", t1) -> the applications whose operator is t1
    reached = set()
    work = deque()

    def propagate(n, d):
        d = d - val.setdefault(n, set())  # @line L20
        if d:
            val[n] |= d  # @line L21
            if n not in delta:  # n is in the worklist exactly when it has a delta
                delta[n] = set()
                work.append(n)
            delta[n] |= d

    def add_edge(a, b):
        if b not in succ.setdefault(a, set()):  # @line L19
            succ[a].add(b)
            propagate(b, val.get(a, set()))

    def call(t, lam):
        node = nodes[lam]
        if node[0] == "fix":
            propagate(("R", (lam, node[1])), {lam})  # @line L15
        binder, body = param(node, lam)
        add_edge(("C", nodes[t][2]), ("R", binder))  # @line L16
        add_edge(("C", body), ("C", t))  # @line L17
        reach(body)  # @line L18

    def reach(root):
        todo = [root]
        while todo:
            t = todo.pop()
            if t in reached:  # @line L9
                continue
            reached.add(t)
            node = nodes[t]
            tag = node[0]
            if tag in ("lam", "fix"):
                propagate(("C", t), {t})  # @line L10
            elif tag == "var":
                if node[2] is not None:
                    add_edge(("R", node[2]), ("C", t))  # @line L11
            elif tag == "let":
                add_edge(("C", node[2]), ("R", (t, node[1])))  # @line L12
                add_edge(("C", node[3]), ("C", t))
                todo += [node[2], node[3]]
            elif tag == "if":
                add_edge(("C", node[2]), ("C", t))  # @line L13
                add_edge(("C", node[3]), ("C", t))
                todo += [node[1], node[2], node[3]]
            elif tag == "prim":
                todo += [node[2], node[3]]
            elif tag == "app":
                op = ("C", node[1])
                watch.setdefault(op, []).append(t)  # @line L14
                for lam in list(val.get(op, ())):
                    call(t, lam)
                todo += [node[1], node[2]]

    reach(0)  # @line L3
    while work:  # @line L4
        n = work.popleft()
        d = delta.pop(n)  # @line L5
        for t in list(watch.get(n, ())):
            for lam in d:
                call(t, lam)  # @line L6
        for m in list(succ.get(n, ())):
            propagate(m, d)  # @line L7
    cache = {lab: val.get(("C", lab), set()) for lab in range(len(nodes))}
    env = {key[1]: s for key, s in val.items() if key[0] == "R" and s}
    return nodes, cache, env  # @line L8


def call_graph(nodes, cache):
    """The pairs (application label, function label) of the result."""
    return {(t, lam) for t, node in enumerate(nodes) if node[0] == "app" for lam in cache[node[1]]}
