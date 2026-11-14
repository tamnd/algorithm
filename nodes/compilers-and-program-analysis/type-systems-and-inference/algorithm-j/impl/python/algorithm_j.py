# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/algorithm-j/. The authors are listed in prov/M228A9.jsonl.
"""Algorithm J of Milner on the toy lambda language of toylam.py.

J keeps one global substitution E in a union-find structure. A type
variable ("tv", n) is either a root (no entry in parent) or points to a
type in parent. find follows these links with path compression. Unification
links roots in place, with union by rank between two variables, so J never
builds or composes substitutions.

Generalization has two modes. With levels=False, J quantifies the variables
of the resolved type that are not free in the resolved environment, as in
Milner's paper. With levels=True, every variable carries the let depth at
which it was made, unification lowers levels, and J quantifies the
variables whose level is deeper than the current one (Remy's method). Both
give the same types.
"""

from toylam import normalize_type

INT = ("int",)
BOOL = ("bool",)
PRIM_TYPES = {"+": INT, "-": INT, "*": INT, "<": BOOL, "==": BOOL}


class TypeErrorHM(Exception):
    """The term has no type."""


class J:
    def __init__(self, levels=False):
        self.levels = levels
        self.parent = {}  # variable number -> the type it is linked to
        self.rank = {}
        self.level = {}
        self.depth = 0  # the let depth of the current point
        self.count = 0
        self.unions = 0  # links made by unification

    def new(self):
        n = self.count
        self.count += 1
        self.rank[n] = 0
        self.level[n] = self.depth
        return ("tv", n)

    def find(self, t):
        """The representative of t: a root variable or a type with a constructor on top."""
        path = []
        while t[0] == "tv" and t[1] in self.parent:
            path.append(t[1])
            t = self.parent[t[1]]
        for v in path[:-1]:
            self.parent[v] = t  # path compression
        return t

    def occurs_adjust(self, v, t, seen=None):
        """Fail if v occurs in t. Lower the levels of the variables of t to the level of v.

        seen holds the shared nodes already visited, so the walk is linear in the size of the DAG.
        """
        if seen is None:
            seen = {}
        t = self.find(t)
        if t[0] == "tv":
            if t[1] == v:
                raise TypeErrorHM("occurs check")
            if self.level[t[1]] > self.level[v]:
                self.level[t[1]] = self.level[v]
        elif t[0] == "fun" and id(t) not in seen:
            seen[id(t)] = t
            self.occurs_adjust(v, t[1], seen)
            self.occurs_adjust(v, t[2], seen)

    def unify(self, t1, t2, done=None):
        """Make t1 and t2 equal in the global substitution, or raise TypeErrorHM.

        done holds the pairs of shared nodes already unified in this call.
        """
        if done is None:
            done = {}
        t1, t2 = self.find(t1), self.find(t2)  # @line L9
        if t1 is t2 or (t1[0] != "fun" and t1 == t2):
            return
        if t1[0] == "tv" and t2[0] == "tv":  # @line L10
            a, b = t1[1], t2[1]
            if self.rank[a] > self.rank[b]:
                a, b = b, a
            self.parent[a] = ("tv", b)  # union by rank
            if self.rank[a] == self.rank[b]:
                self.rank[b] += 1
            self.level[b] = min(self.level[a], self.level[b])
            self.unions += 1
            return
        if t2[0] == "tv":
            t1, t2 = t2, t1
        if t1[0] == "tv":  # @line L11
            self.occurs_adjust(t1[1], t2)
            self.parent[t1[1]] = t2
            self.unions += 1
            return
        if t1[0] == "fun" and t2[0] == "fun":  # @line L12
            key = (id(t1), id(t2))
            if key in done:
                return
            done[key] = (t1, t2)
            self.unify(t1[1], t2[1], done)
            self.unify(t1[2], t2[2], done)
            return
        raise TypeErrorHM(f"cannot unify {t1[0]} with {t2[0]}")  # @line L13

    def resolve(self, t):
        """The type t with the global substitution applied in full."""
        t = self.find(t)
        if t[0] == "fun":
            return ("fun", self.resolve(t[1]), self.resolve(t[2]))
        return t

    def free_vars(self, t, out, seen=None):
        if seen is None:
            seen = {}
        t = self.find(t)
        if t[0] == "tv":
            out.add(t[1])
        elif t[0] == "fun" and id(t) not in seen:
            seen[id(t)] = t
            self.free_vars(t[1], out, seen)
            self.free_vars(t[2], out, seen)

    def generalize(self, env, t):
        if self.levels:
            vs = set()
            self.free_vars(t, vs)
            bound = tuple(sorted(v for v in vs if self.level[v] > self.depth))
        else:
            vs, envs = set(), set()
            self.free_vars(t, vs)
            for sc in env.values():
                fv = set()
                self.free_vars(sc[2], fv)
                envs |= fv - set(sc[1])
            bound = tuple(sorted(vs - envs))
        return ("forall", bound, t)

    def instantiate(self, sc):
        if not sc[1]:
            return sc[2]
        m = {v: self.new() for v in sc[1]}
        memo = {}  # shared nodes are copied once, so the copy is a DAG of the same size

        def copy(t):
            t = self.find(t)
            if t[0] == "tv":
                return m.get(t[1], t)
            if t[0] == "fun":
                hit = memo.get(id(t))
                if hit is not None:
                    return hit[1]
                c = ("fun", copy(t[1]), copy(t[2]))
                memo[id(t)] = (t, c)
                return c
            return t

        return copy(sc[2])

    def j(self, env, e):
        """Algorithm J: returns t; E(env) |- e : E(t) for the global E after the call."""
        tag = e[0]
        if tag == "var":  # @line L1
            if e[1] not in env:
                raise TypeErrorHM(f"unbound variable {e[1]}")
            return self.instantiate(env[e[1]])  # @line L2
        if tag == "lam":  # @line L3
            a = self.new()
            t1 = self.j({**env, e[1]: ("forall", (), a)}, e[2])
            return ("fun", a, t1)  # @line L4
        if tag == "app":  # @line L5
            t1 = self.j(env, e[1])
            t2 = self.j(env, e[2])
            b = self.new()
            self.unify(t1, ("fun", t2, b))  # @line L6
            return b
        if tag == "let":  # @line L7
            self.depth += 1
            t1 = self.j(env, e[2])
            self.depth -= 1
            sigma = self.generalize(env, t1)  # @line L8
            return self.j({**env, e[1]: sigma}, e[3])
        if tag == "fix":
            a, b = self.new(), self.new()
            t1 = self.j({**env, e[1]: ("forall", (), ("fun", a, b)), e[2]: ("forall", (), a)}, e[3])
            self.unify(b, t1)
            return ("fun", a, b)
        if tag == "int":
            return INT
        if tag == "bool":
            return BOOL
        if tag == "if":
            self.unify(self.j(env, e[1]), BOOL)
            t2 = self.j(env, e[2])
            t3 = self.j(env, e[3])
            self.unify(t2, t3)
            return t2
        if tag == "prim":
            self.unify(self.j(env, e[2]), INT)
            self.unify(self.j(env, e[3]), INT)
            return PRIM_TYPES[e[1]]
        raise ValueError(f"not a term: {e!r}")


def infer(e, levels=False):
    """The principal type of the closed term e, renamed to 0, 1, 2, ... Raises TypeErrorHM."""
    st = J(levels)
    t = st.j({}, e)
    return normalize_type(st.resolve(t))


def principal_type(e, levels=False):
    """The principal type of e, or None if e has no type."""
    try:
        return infer(e, levels)
    except TypeErrorHM:
        return None


def dag_size(e, levels=True):
    """The number of distinct nodes of the principal type of e in J's shared representation."""
    st = J(levels)
    t = st.j({}, e)
    seen = set()

    def walk(u):
        u = st.find(u)
        key = id(u) if u[0] == "fun" else u
        if key in seen:
            return
        seen.add(key)
        if u[0] == "fun":
            walk(u[1])
            walk(u[2])

    walk(t)
    return len(seen)
