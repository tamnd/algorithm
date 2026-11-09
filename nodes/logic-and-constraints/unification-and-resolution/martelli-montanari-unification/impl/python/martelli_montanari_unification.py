# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/martelli-montanari-unification/. The authors are listed in prov/RV98XJ.jsonl.

"""Martelli-Montanari unification by transformation rules, and the
almost-linear variant on a term DAG with union-find.

A term is a variable (a Python str) or a tuple (symbol, arg1, ..., argk).
A constant is a tuple with one item, for example ("a",).
A substitution is a dict from variable names to terms.
"""

from typing import Optional, Union

Term = Union[str, tuple]
Subst = dict[str, Term]


def is_var(t: Term) -> bool:
    return isinstance(t, str)


def apply(t: Term, sigma: Subst) -> Term:
    """Simultaneous substitution with an explicit stack. Cost: O(size of result)."""
    if not sigma:
        return t
    out: list[Term] = []
    stack: list[tuple[Term, bool]] = [(t, False)]
    while stack:
        u, done = stack.pop()
        if is_var(u):
            out.append(sigma.get(u, u))
        elif done:
            k = len(u) - 1
            args = out[len(out) - k:] if k else []
            del out[len(out) - k:]
            out.append((u[0], *args))
        else:
            stack.append((u, True))
            for a in reversed(u[1:]):
                stack.append((a, False))
    return out[0]


def occurs(x: str, t: Term) -> bool:
    stack = [t]
    while stack:
        u = stack.pop()
        if is_var(u):
            if u == x:
                return True
        else:
            stack.extend(u[1:])
    return False


def martelli_montanari_unification(equations: list[tuple[Term, Term]]) -> Optional[Subst]:
    """Solve a list of equations (s, t) by the rules of Martelli and Montanari.

    Return an idempotent most general unifier of all the equations, or None
    when they have no unifier. The rules are delete, decompose, clash,
    orient, occurs check and eliminate. On tree terms the solved part can
    grow to exponential size; see unify_union_find for the DAG version.
    """
    solved: Subst = {}  # @line L1
    todo = list(reversed(equations))
    while todo:  # @line L2
        s, t = todo.pop()  # @line L3
        if s == t:
            continue  # @line L4
        if not is_var(s) and not is_var(t):
            if s[0] != t[0] or len(s) != len(t):
                return None  # @line L5
            for a, b in zip(reversed(s[1:]), reversed(t[1:])):  # @line L6
                todo.append((a, b))
            continue
        if not is_var(s):
            s, t = t, s  # @line L7
        if occurs(s, t):
            return None  # @line L8
        bind = {s: t}  # @line L9
        todo = [(apply(a, bind), apply(b, bind)) for a, b in todo]
        solved = {y: apply(w, bind) for y, w in solved.items()}
        solved[s] = t
    return solved  # @line L10


class _UnionFind:
    """Disjoint sets over node ids, with union by rank and path compression."""

    def __init__(self) -> None:
        self.parent: list[int] = []
        self.rank: list[int] = []

    def add(self) -> int:
        self.parent.append(len(self.parent))
        self.rank.append(0)
        return len(self.parent) - 1

    def find(self, a: int) -> int:
        root = a
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[a] != root:
            self.parent[a], a = root, self.parent[a]
        return root

    def union(self, a: int, b: int) -> int:
        """Join the sets of the roots a and b and return the new root."""
        if self.rank[a] < self.rank[b]:
            a, b = b, a
        self.parent[b] = a
        if self.rank[a] == self.rank[b]:
            self.rank[a] += 1
        return a


def unify_union_find(s: Term, t: Term) -> Optional[Subst]:
    """Unify s and t on a term DAG with union-find, then check for cycles.

    The terms are stored once in a DAG with shared subterms (hash consing).
    Each class of the union-find keeps one function node as its schema.
    Merging stops on a clash. The occurs check is one depth-first search
    over the classes at the end. The DAG part takes O(N alpha(N)) time for
    N nodes; the returned dict is the expanded idempotent most general
    unifier, which can be exponentially larger than the DAG.
    """
    table: dict[tuple, int] = {}
    sym: list = []
    kids: list[tuple[int, ...]] = []
    uf = _UnionFind()

    def intern(term: Term) -> int:
        stack: list[tuple[Term, bool]] = [(term, False)]
        out: list[int] = []
        while stack:
            u, done = stack.pop()
            if not is_var(u) and not done:
                stack.append((u, True))
                for a in reversed(u[1:]):
                    stack.append((a, False))
                continue
            if is_var(u):
                key: tuple = ("var", u)
            else:
                k = len(u) - 1
                args = tuple(out[len(out) - k:]) if k else ()
                del out[len(out) - k:]
                key = ("app", u[0], args)
            if key not in table:
                table[key] = uf.add()
                sym.append(key[1])
                kids.append(key[2] if key[0] == "app" else ())
            out.append(table[key])
        return out[0]

    def is_fun(i: int) -> bool:
        return table.get(("var", sym[i])) != i

    root_s, root_t = intern(s), intern(t)
    schema = {i: i for i in range(len(sym)) if is_fun(i)}
    pairs = [(root_s, root_t)]
    while pairs:
        a, b = pairs.pop()
        a, b = uf.find(a), uf.find(b)
        if a == b:
            continue
        fa, fb = schema.get(a), schema.get(b)
        if fa is not None and fb is not None:
            if sym[fa] != sym[fb] or len(kids[fa]) != len(kids[fb]):
                return None
            pairs.extend(zip(kids[fa], kids[fb]))
        r = uf.union(a, b)
        keep = fa if fa is not None else fb
        schema.pop(a, None)
        schema.pop(b, None)
        if keep is not None:
            schema[r] = keep

    # Occurs check: the graph of classes must be acyclic.
    color: dict[int, int] = {}
    for start in {uf.find(i) for i in range(len(sym))}:
        if start in color:
            continue
        color[start] = 1
        stack = [(start, iter(kids[schema[start]] if start in schema else ()))]
        while stack:
            c, it = stack[-1]
            nxt = next(it, None)
            if nxt is None:
                color[c] = 2
                stack.pop()
                continue
            d = uf.find(nxt)
            if color.get(d) == 1:
                return None
            if d not in color:
                color[d] = 1
                stack.append((d, iter(kids[schema[d]] if d in schema else ())))

    # Expand each class to a tree term: the schema, or a chosen variable.
    name: dict[int, str] = {}
    for i in range(len(sym)):
        if not is_fun(i):
            name.setdefault(uf.find(i), sym[i])
    memo: dict[int, Term] = {}

    def expand(c: int) -> Term:
        stack = [(c, False)]
        while stack:
            d, done = stack.pop()
            if d in memo:
                continue
            if d not in schema:
                memo[d] = name[d]
                continue
            ks = [uf.find(k) for k in kids[schema[d]]]
            if done:
                memo[d] = (sym[schema[d]], *[memo[k] for k in ks])
            else:
                stack.append((d, True))
                stack.extend((k, False) for k in ks if k not in memo)
        return memo[c]

    sigma: Subst = {}
    for i in range(len(sym)):
        if not is_fun(i):
            value = expand(uf.find(i))
            if value != sym[i]:
                sigma[sym[i]] = value
    return sigma
