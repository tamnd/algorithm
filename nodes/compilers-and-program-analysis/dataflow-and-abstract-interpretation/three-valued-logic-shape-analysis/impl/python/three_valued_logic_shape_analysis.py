# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/three-valued-logic-shape-analysis/. The authors are listed in prov/BGQ8GB.jsonl.
"""Shape analysis with three-valued logical structures, after Sagiv, Reps
and Wilhelm, for programs over singly linked cells with one field n.

Truth values are 0, 1 and HALF (unknown), with and = min, or = max and
not v = 1 - v (Kleene's logic). A structure has nodes 0 .. k-1 and:

    u[x][v]     x points to v                     (one predicate per variable)
    u["r:x"][v] v is reachable from x by n-steps  (zero steps included)
    u["c"][v]   v lies on a cycle of n
    n[v][w]     the field n of v is w
    sm[v]       0, or HALF if v may stand for more than one cell

All unary predicates are abstraction predicates: canonical abstraction
(blur) merges the nodes that agree on all of them. A program is a dict from
point to a list of (statement, successor point). Statements:

    ("null", x)           x = null
    ("new", x)            x = new cell
    ("copy", x, y)        x = y
    ("load", x, y)        x = y.n
    ("cut", x)            x.n = null
    ("link", x, y)        x.n = y
    ("assume", t, x[, y]) keep the states where the test holds, t one of
                          "null", "nonnull", "eq", "neq"

analyze(prog, vars_, entry) returns the set of canonical structures at each
point and the points where a null dereference may happen.
"""

HALF = 0.5


def join(a, b):
    return a if a == b else HALF


def leq(a, b):
    """The information order: a is at least as definite as b."""
    return a == b or b == HALF


def predicates(vars_):
    return tuple(vars_) + tuple("r:" + x for x in vars_) + ("c",)


class Struct:
    def __init__(self, preds, u, sm, n):
        self.preds = preds
        self.u = u
        self.sm = sm
        self.n = n

    def size(self):
        return len(self.sm)

    def copy(self):
        return Struct(self.preds, {p: list(vs) for p, vs in self.u.items()}, list(self.sm), [list(r) for r in self.n])

    def key(self):
        """A hashable form. After blur it is canonical, since blur sorts the
        nodes by their unary values and no two nodes share them."""
        vec = tuple(tuple(self.u[p][v] for p in self.preds) for v in range(self.size()))
        return (vec, tuple(self.sm), tuple(tuple(r) for r in self.n))


def thaw(preds, key):
    vec, sm, n = key
    u = {p: [vec[v][i] for v in range(len(vec))] for i, p in enumerate(preds)}
    return Struct(preds, u, list(sm), [list(r) for r in n])


def from_heap(vars_, env, nxt):
    """The two-valued structure of a concrete heap: env maps each variable
    to a cell or None, nxt maps each cell to its successor or None."""
    cells = sorted(nxt)
    idx = {c: i for i, c in enumerate(cells)}
    preds = predicates(vars_)
    k = len(cells)
    u = {p: [0] * k for p in preds}
    for x in vars_:
        c = env.get(x)
        seen = set()
        if c is not None:
            u[x][idx[c]] = 1
        while c is not None and c not in seen:
            seen.add(c)
            u["r:" + x][idx[c]] = 1
            c = nxt[c]
    for c in cells:
        d, steps = nxt[c], 0
        while d is not None and d != c and steps <= k:
            d, steps = nxt[d], steps + 1
        u["c"][idx[c]] = int(d == c)
    n = [[0] * k for _ in range(k)]
    for c in cells:
        if nxt[c] is not None:
            n[idx[c]][idx[nxt[c]]] = 1
    return Struct(preds, u, [0] * k, n)


def node_of(S, x):
    """The node that x points to, or None. Variables are always definite."""
    hits = [v for v in range(S.size()) if S.u[x][v] == 1]
    assert all(S.u[x][v] != HALF for v in range(S.size()))
    return hits[0] if hits else None


# ----------------------------------------------------------- the three steps


def blur(S):
    """Canonical abstraction: merge the nodes with equal unary values."""
    preds = S.preds
    vec = [tuple(S.u[p][v] for p in preds) for v in range(S.size())]
    keys = sorted(set(vec))
    g = {key: i for i, key in enumerate(keys)}
    m = len(keys)
    members = [[] for _ in range(m)]
    for v in range(S.size()):
        members[g[vec[v]]].append(v)
    u = {p: [keys[i][j] for i in range(m)] for j, p in enumerate(preds)}
    sm = [HALF if len(members[i]) > 1 or any(S.sm[v] == HALF for v in members[i]) else 0 for i in range(m)]
    n = [[None] * m for _ in range(m)]
    for v in range(S.size()):
        for w in range(S.size()):
            a, b = g[vec[v]], g[vec[w]]
            n[a][b] = S.n[v][w] if n[a][b] is None else join(n[a][b], S.n[v][w])
    return Struct(preds, u, sm, n)


def coerce(S, vars_):
    """Sharpen S with facts true of every heap, or return None if no heap
    fits it. The facts: a variable points to at most one cell, and its
    reachability set is empty exactly when it is null; a cell has at most
    one successor; the successor of a cell reachable from x is reachable
    from x; the successor of a cell on a cycle is on a cycle; a cell that
    is not on a cycle has no edge from itself or from a cell it reaches."""
    S = S.copy()
    k = S.size()
    changed = True
    while changed:
        changed = False
        for x in vars_:
            hits = [v for v in range(k) if S.u[x][v] == 1]
            rx = S.u["r:" + x]
            if len(hits) > 1:
                return None
            for v in range(k):
                if hits and v == hits[0]:
                    if S.sm[v] != 0:
                        S.sm[v] = 0
                        changed = True
                    if rx[v] == 0:
                        return None
                    if rx[v] == HALF:
                        rx[v] = 1
                        changed = True
                elif not hits and rx[v] != 0:
                    if rx[v] == 1:
                        return None
                    rx[v] = 0
                    changed = True
        for v in range(k):
            ones = [w for w in range(k) if S.n[v][w] == 1]
            if len(ones) > 1:
                return None
            if ones:
                w = ones[0]
                if S.sm[w] != 0:
                    S.sm[w] = 0
                    changed = True
                for w2 in range(k):
                    if w2 != w and S.n[v][w2] == HALF:
                        S.n[v][w2] = 0
                        changed = True
        for v in range(k):
            for w in range(k):
                if S.n[v][w] == 0:
                    continue
                bad = S.u["c"][v] == 1 and S.u["c"][w] == 0
                bad = bad or any(S.u["r:" + z][v] == 1 and S.u["r:" + z][w] == 0 for z in vars_)
                # An edge back to a cell that reaches v closes a cycle.
                bad = bad or (v == w and S.sm[v] == 0 and S.u["c"][v] == 0)
                bad = bad or (S.u["c"][w] == 0 and any(S.u[z][w] == 1 and S.u["r:" + z][v] == 1 for z in vars_))
                if bad:
                    if S.n[v][w] == 1:
                        return None
                    S.n[v][w] = 0
                    changed = True
    return S


def _split(S, w, u):
    """Copy the summary node w into a new node that is the one successor of
    u; w keeps the other cells."""
    T = S.copy()
    k = T.size()
    for p in T.preds:
        T.u[p].append(T.u[p][w])
    T.sm.append(0)
    for r in T.n:
        r.append(r[w])
    T.n.append(list(T.n[w]))
    T.n[k][k] = T.n[w][w]
    for j in range(k + 1):
        if j != k:
            T.n[u][j] = 0 if T.n[u][j] == HALF else T.n[u][j]
    T.n[u][k] = 1
    T.n[u][w] = 0
    return T


def focus_succ(S, u, vars_):
    """Structures that together stand for the same heaps as S, in each of
    which the n-successor of node u is definite."""
    S = coerce(S, vars_)
    if S is None:
        return []
    cand = [w for w in range(S.size()) if S.n[u][w] == HALF]
    if not cand:
        return [S]
    out = []
    none = S.copy()
    for w in cand:
        none.n[u][w] = 0
    out.append(none)
    for w in cand:
        whole = S.copy()
        for w2 in cand:
            whole.n[u][w2] = 0
        whole.n[u][w] = 1
        out.append(whole)
        if S.sm[w] == HALF:
            out.append(_split(S, w, u))
    return [T for T in (coerce(T, vars_) for T in out) if T is not None]


def _cut(S, x, vars_):
    """x.n = null on a structure where x is not null."""
    u = node_of(S, x)
    k = S.size()
    cu = S.u["c"][u]
    rx = S.u["r:" + x]
    xs = S.u[x]
    T = S.copy()
    for z in vars_:
        rz = S.u["r:" + z]
        for v in range(k):
            a = min(rz[u], rx[v], 1 - xs[v])
            # When u is not on a cycle, the cells after u are reachable from
            # z only through u. When it is, they may also come before u.
            T.u["r:" + z][v] = min(rz[v], 1 - min(a, 1 - cu), 1 - min(a, cu, HALF))
    for v in range(k):
        T.u["c"][v] = min(S.u["c"][v], 1 - min(cu, rx[v]))
    for w in range(k):
        T.n[u][w] = 0
    return T


def post(S, st, vars_):
    """The structures after statement st, and whether st may dereference
    null. Each result is focused, updated and coerced, not yet blurred."""
    kind = st[0]
    k = S.size()
    if kind == "assume":
        t, x = st[1], st[2]
        a = node_of(S, x)
        if t == "null":
            ok = a is None
        elif t == "nonnull":
            ok = a is not None
        else:
            b = node_of(S, st[3])
            ok = (a == b) == (t == "eq")
        return ([S] if ok else []), False
    if kind == "null":
        T = S.copy()
        T.u[st[1]] = [0] * k
        T.u["r:" + st[1]] = [0] * k
        return [T], False
    if kind == "new":
        x = st[1]
        T = S.copy()
        for p in T.preds:
            T.u[p].append(0)
        T.u[x] = [0] * k + [1]
        T.u["r:" + x] = [0] * k + [1]
        T.sm.append(0)
        for r in T.n:
            r.append(0)
        T.n.append([0] * (k + 1))
        return [T], False
    if kind == "copy":
        x, y = st[1], st[2]
        T = S.copy()
        T.u[x] = list(S.u[y])
        T.u["r:" + x] = list(S.u["r:" + y])
        return [T], False
    if kind == "load":
        x, y = st[1], st[2]
        u = node_of(S, y)
        if u is None:
            return [], True
        out = []
        for F in focus_succ(S, u, vars_):
            T = F.copy()
            T.u[x] = [F.n[u][v] for v in range(F.size())]
            T.u["r:" + x] = [max(min(F.u["r:" + y][v], 1 - F.u[y][v]), min(F.u[y][v], F.u["c"][v])) for v in range(F.size())]
            T = coerce(T, vars_)
            if T is not None:
                out.append(T)
        return out, False
    if kind == "cut":
        if node_of(S, st[1]) is None:
            return [], True
        T = coerce(_cut(S, st[1], vars_), vars_)
        return ([T] if T is not None else []), False
    if kind == "link":
        x, y = st[1], st[2]
        if node_of(S, x) is None:
            return [], True
        C = _cut(S, x, vars_)
        u = node_of(C, x)
        T = C.copy()
        ryu = C.u["r:" + y][u]
        for z in vars_:
            for v in range(k):
                T.u["r:" + z][v] = max(C.u["r:" + z][v], min(C.u["r:" + z][u], C.u["r:" + y][v]))
        for v in range(k):
            T.u["c"][v] = max(C.u["c"][v], min(ryu, C.u["r:" + y][v]))
            T.n[u][v] = max(C.n[u][v], C.u[y][v])
        T = coerce(T, vars_)
        return ([T] if T is not None else []), False
    raise ValueError("bad statement: %r" % (st,))


def analyze(prog, vars_, entry, start=0):
    """The least fixed point over sets of canonical structures. entry is a
    list of structures for the start point. Returns (A, errors): A maps each
    point to a set of keys (use thaw to read them), errors is the set of
    points whose statement may dereference null."""
    preds = predicates(vars_)
    A = {p: set() for p in prog}
    errors = set()
    work = []
    for S in entry:  # @line L1
        C = coerce(S, vars_)
        if C is not None:
            key = blur(C).key()
            if key not in A[start]:
                A[start].add(key)
                work.append((start, key))
    while work:  # @line L2
        p, key = work.pop()  # @line L3
        S = thaw(preds, key)
        for st, q in prog[p]:  # @line L4
            outs, err = post(S, st, vars_)  # @line L5
            if err:
                errors.add(p)  # @line L6
            for T in outs:  # @line L7
                new = blur(T).key()  # @line L8
                if new not in A[q]:  # @line L9
                    A[q].add(new)
                    work.append((q, new))
    return A, errors  # @line L10


# ------------------------------------------------------------- formulas


def evaluate(S, phi, env=None):
    """Kleene value of a formula on S. Formulas are tuples: ("p", name, v),
    ("n", v, w), ("eq", v, w), ("not", f), ("and", f, g), ("or", f, g),
    ("exists", v, f), ("forall", v, f), ("const", value); v and w are
    names of logical variables bound in env."""
    env = env or {}
    op = phi[0]
    if op == "const":
        return phi[1]
    if op == "p":
        return S.u[phi[1]][env[phi[2]]]
    if op == "n":
        return S.n[env[phi[1]]][env[phi[2]]]
    if op == "eq":
        a, b = env[phi[1]], env[phi[2]]
        if a != b:
            return 0
        return 1 if S.sm[a] == 0 else HALF
    if op == "not":
        return 1 - evaluate(S, phi[1], env)
    if op == "and":
        return min(evaluate(S, phi[1], env), evaluate(S, phi[2], env))
    if op == "or":
        return max(evaluate(S, phi[1], env), evaluate(S, phi[2], env))
    if op in ("exists", "forall"):
        vals = [evaluate(S, phi[2], dict(env, **{phi[1]: v})) for v in range(S.size())]
        if op == "exists":
            return max(vals, default=0)
        return min(vals, default=1)
    raise ValueError("bad formula: %r" % (phi,))
