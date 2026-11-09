# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/local-model-checking/. The authors are listed in prov/SYAG8V.jsonl.

"""Local model checking of the alternation-free modal mu-calculus.

The method follows the local fixed-point algorithm of Liu and Smolka (1998) on a
dependency graph that is built on demand. A vertex is a pair (s, f) of a state
and a subformula. A hyperedge of (s, f) is a tuple of target vertices: (s, f)
is true in the least solution exactly when all targets of one of its hyperedges
are true. Only the vertices that the search reaches are built.

A formula is a nested tuple in positive normal form:
    ("true",), ("false",), ("ap", p), ("nap", p)   p holds / p does not hold
    ("and", f, g), ("or", f, g)
    ("dia", f)   some successor satisfies f
    ("box", f)   every successor satisfies f
    ("mu", X, f), ("nu", X, f), ("var", X)
Preconditions: the formula is closed, each variable is bound once, and the
formula is alternation-free: no fixed-point subformula has a free variable that
a fixed point of the other kind binds. Positive normal form makes every
variable occur positively.

A model is a dict with succ (state -> list of states) and label (state -> set of
atomic propositions).

Cost: one call for a mu formula phi takes O(|M| |phi|) time for the vertices and
hyperedges it builds, where |M| counts states and transitions; each nested nu
subformula is solved by a dual call, with its results cached per state.
"""


def dual(f: tuple) -> tuple:
    """The positive normal form of the negation of f (a variable stays a variable)."""
    op = f[0]
    if op == "true":
        return ("false",)
    if op == "false":
        return ("true",)
    if op == "ap":
        return ("nap", f[1])
    if op == "nap":
        return ("ap", f[1])
    if op == "and":
        return ("or", dual(f[1]), dual(f[2]))
    if op == "or":
        return ("and", dual(f[1]), dual(f[2]))
    if op == "dia":
        return ("box", dual(f[1]))
    if op == "box":
        return ("dia", dual(f[1]))
    if op == "mu":
        return ("nu", f[1], dual(f[2]))
    if op == "nu":
        return ("mu", f[1], dual(f[2]))
    if op == "var":
        return f
    raise ValueError(f"unknown operator {op!r}")


def _binders(f: tuple) -> dict:
    """Map each variable name to its binding fixed-point subformula."""
    out = {}
    stack = [f]
    while stack:
        g = stack.pop()
        if g[0] in ("mu", "nu"):
            out[g[1]] = g
            stack.append(g[2])
        elif g[0] in ("and", "or"):
            stack.extend((g[1], g[2]))
        elif g[0] in ("dia", "box"):
            stack.append(g[1])
    return out


class LocalChecker:
    """Answers queries "does state s satisfy phi" and builds only what they need."""

    def __init__(self, model: dict):
        self.model = model
        self.cache: dict = {}
        self.vertices = 0  # the number of dependency-graph vertices built so far

    def holds(self, s, phi: tuple) -> bool:
        key = (s, phi)
        if key not in self.cache:
            if phi[0] == "nu":
                self.cache[key] = not self._local(s, dual(phi))
            else:
                self.cache[key] = self._local(s, phi)
        return self.cache[key]

    def _edges(self, v, binder):
        """The hyperedges of the vertex v = (s, f): a list of tuples of vertices."""
        s, f = v
        op = f[0]
        if op == "true":
            return [()]
        if op == "false":
            return []
        if op == "ap":
            return [()] if f[1] in self.model["label"][s] else []
        if op == "nap":
            return [] if f[1] in self.model["label"][s] else [()]
        if op == "and":
            return [((s, f[1]), (s, f[2]))]
        if op == "or":
            return [((s, f[1]),), ((s, f[2]),)]
        if op == "dia":
            return [((t, f[1]),) for t in self.model["succ"][s]]
        if op == "box":
            return [tuple((t, f[1]) for t in self.model["succ"][s])]
        if op == "mu":
            return [((s, f[2]),)]
        if op == "var":
            return [((s, binder[f[1]]),)]
        if op == "nu":  # closed, by alternation-freedom: solve it on its own
            return [()] if self.holds(s, f) else []
        raise ValueError(f"unknown operator {op!r}")

    def _local(self, s0, phi: tuple) -> bool:
        """Liu-Smolka local algorithm for the least solution at the vertex (s0, phi)."""
        binder = _binders(phi)
        v0 = (s0, phi)
        value = {v0: 0}  # @line L1
        deps: dict = {v0: []}
        edges = {v0: self._edges(v0, binder)}
        self.vertices += 1
        ptr: dict = {}
        # The work list is a stack. Hyperedges go on it in reverse order, so that the
        # first hyperedge of a vertex is tried first: depth-first, left to right.
        work = [(v0, i) for i in reversed(range(len(edges[v0])))]  # @line L2
        while work:  # @line L3
            v, i = work.pop()  # @line L4
            if value[v] == 1:  # @line L5
                continue
            targets = edges[v][i]
            k = ptr.get((v, i), 0)
            while k < len(targets) and value.get(targets[k]) == 1:  # @line L6
                k += 1
            ptr[(v, i)] = k
            if k == len(targets):  # @line L7
                value[v] = 1  # @line L8
                if v == v0:
                    return True
                work.extend(deps[v])  # @line L9
                continue
            u = targets[k]  # @line L10
            if u not in value:  # @line L11
                value[u] = 0  # @line L12
                deps[u] = [(v, i)]
                edges[u] = self._edges(u, binder)
                self.vertices += 1
                work.extend((u, j) for j in reversed(range(len(edges[u]))))  # @line L13
            else:
                deps[u].append((v, i))  # @line L14
        return False  # @line L15


def local_model_checking(model: dict, s, phi: tuple) -> bool:
    """Does the state s of the model satisfy the closed alternation-free formula phi?"""
    return LocalChecker(model).holds(s, phi)
