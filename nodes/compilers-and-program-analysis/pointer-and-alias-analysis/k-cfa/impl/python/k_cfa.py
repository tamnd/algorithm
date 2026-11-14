# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-cfa/. The authors are listed in prov/WSCAQ1.jsonl.
"""k-CFA: control flow analysis of a higher-order program with the last k
call sites as the context of each binding.

label(term) numbers the nodes of a toylam term in preorder, as on the 0-CFA
page, and links each variable to its binder (label, name).

k_cfa(term, k) returns (nodes, C, R). A contour is a tuple of at most k
application labels, the most recent last. An abstract closure is (lam, ce)
where ce is a sorted tuple of (name, contour) pairs for the free variables of
the function lam. C[(t, d)] is the set of closures that node t may evaluate
to in contour d, and R[(b, d)] the set of closures bound to binder b in
contour d. The solver keeps a set of tasks (t, ce, d), one for each way in
which node t may be evaluated, and applies the rule of every task, round
after round, until nothing changes. The number of contours is at most n^k,
and the number of closures can be exponential in n, so k >= 1 is exponential
in the worst case.
"""


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
            nodes.append(None)
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


def free_names(nodes):
    """The free variable names of each node. Children have larger labels."""
    fv = [frozenset()] * len(nodes)
    for t in range(len(nodes) - 1, -1, -1):
        node = nodes[t]
        tag = node[0]
        if tag == "var":
            fv[t] = frozenset([node[1]])
        elif tag == "lam":
            fv[t] = fv[node[2]] - {node[1]}
        elif tag == "fix":
            fv[t] = fv[node[3]] - {node[1], node[2]}
        elif tag == "let":
            fv[t] = fv[node[2]] | (fv[node[3]] - {node[1]})
        elif tag == "app":
            fv[t] = fv[node[1]] | fv[node[2]]
        elif tag == "if":
            fv[t] = fv[node[1]] | fv[node[2]] | fv[node[3]]
        elif tag == "prim":
            fv[t] = fv[node[2]] | fv[node[3]]
    return fv


def k_cfa(term, k):
    nodes = label(term)
    fv = free_names(nodes)
    C, R = {}, {}
    tasks = {}  # an ordered set of (t, ce, d)
    changed = [False]

    def task(t, ce, d):
        key = (t, tuple(sorted((x, c) for x, c in ce.items() if x in fv[t])), d)  # @line L16
        if key not in tasks:
            tasks[key] = None
            changed[0] = True

    def add(table, key, items):
        s = table.setdefault(key, set())
        if not items <= s:
            s |= items
            changed[0] = True

    def rule(t, ce, d):
        node = nodes[t]
        tag = node[0]
        if tag == "var":
            if node[2] is not None:
                add(C, (t, d), R.get((node[2], ce[node[1]]), set()))  # @line L6
        elif tag in ("lam", "fix"):
            add(C, (t, d), {(t, tuple(sorted(ce.items())))})  # @line L7
        elif tag == "let":
            t1, t2 = node[2], node[3]
            task(t1, ce, d)  # @line L8
            add(R, ((t, node[1]), d), C.get((t1, d), set()))
            task(t2, {**ce, node[1]: d}, d)
            add(C, (t, d), C.get((t2, d), set()))
        elif tag in ("if", "prim"):
            kids = node[1:] if tag == "if" else node[2:]
            for u in kids:
                task(u, ce, d)  # @line L9
            if tag == "if":
                add(C, (t, d), C.get((node[2], d), set()) | C.get((node[3], d), set()))
        elif tag == "app":
            t1, t2 = node[1], node[2]
            task(t1, ce, d)  # @line L10
            task(t2, ce, d)
            for lam, ce2 in list(C.get((t1, d), ())):  # @line L11
                d2 = (d + (t,))[-k:] if k > 0 else ()  # @line L12
                fun = nodes[lam]
                inner = dict(ce2)
                if fun[0] == "lam":
                    x, body = fun[1], fun[2]
                else:
                    x, body = fun[2], fun[3]
                    add(R, ((lam, fun[1]), d2), {(lam, ce2)})  # @line L13
                    inner[fun[1]] = d2
                add(R, ((lam, x), d2), C.get((t2, d), set()))
                inner[x] = d2
                task(body, inner, d2)  # @line L14
                add(C, (t, d), C.get((body, d2), set()))  # @line L15

    task(0, {}, ())  # @line L1
    while changed[0]:  # @line L2 @line L4
        changed[0] = False
        for t, ce, d in list(tasks):  # @line L3
            rule(t, dict(ce), d)
    return nodes, C, R  # @line L5


def project(table):
    """Forget the contours and environments: a dict from each label or binder
    to the set of function labels."""
    out = {}
    for (key, _), closures in table.items():
        if closures:
            out.setdefault(key, set()).update(lam for lam, _ in closures)
    return out


def call_graph(nodes, C):
    """The pairs (application label, function label) of the result."""
    flat = project(C)
    return {(t, lam) for t, node in enumerate(nodes) if node[0] == "app" for lam in flat.get(node[1], ())}
