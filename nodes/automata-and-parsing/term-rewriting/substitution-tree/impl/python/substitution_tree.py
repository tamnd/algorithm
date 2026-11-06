# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/substitution-tree/. The authors are listed in prov/6X13J0.jsonl.

"""Substitution trees (Graf, 1995): a term index whose nodes store substitutions.

Terms: a variable is a str, an application is a tuple (f, arg1, ..., argk),
and a constant is a 1-tuple such as ("a",). The tree renames variables:
stored terms use "#1", "#2", ... (in order of first occurrence), query terms
use "?" + name, and indicator variables, which only occur inside the tree,
are "*0", "*1", .... A stored term is the composition of the substitutions
on the path from the top to its leaf, applied to "*0".

All functions use explicit stacks, so very deep terms are fine.
"""

from typing import Any, Callable, Hashable, Union

Term = Union[str, tuple]
Subst = dict[str, Term]


def is_var(t: Term) -> bool:
    return isinstance(t, str)


def is_ivar(v: str) -> bool:
    return v[0] == "*"


def term_eq(s: Term, t: Term) -> bool:
    """Syntactic equality without recursion. O(min(|s|, |t|))."""
    stack = [(s, t)]
    while stack:
        a, b = stack.pop()
        if a is b:
            continue
        if isinstance(a, str) or isinstance(b, str):
            if a != b:
                return False
            continue
        if a[0] != b[0] or len(a) != len(b):
            return False
        stack.extend(zip(a[1:], b[1:]))
    return True


def rebuild(t: Term, leaf: Callable[[str], Term]) -> Term:
    """Copy t, replacing each variable v by leaf(v); variables are met left to right. O(|t|)."""
    out: list[Term] = []
    stack: list[tuple[Term, bool]] = [(t, False)]
    while stack:
        u, done = stack.pop()
        if isinstance(u, str):
            out.append(leaf(u))
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


def apply(t: Term, s: Subst) -> Term:
    """t with each variable v in s replaced by s[v], one pass. O(|t| + output)."""
    return rebuild(t, lambda v: s.get(v, v))


def normalize(t: Term) -> Term:
    """Rename the variables of t to #1, #2, ... by first occurrence. O(|t|)."""
    names: dict[str, str] = {}

    def leaf(v: str) -> str:
        if v not in names:
            names[v] = "#" + str(len(names) + 1)
        return names[v]

    return rebuild(t, leaf)


def match_pairs(pairs: list[tuple[Term, Term]], is_mvar: Callable[[str], bool]) -> Subst | None:
    """One-sided matching: bind the variables v of the left terms with is_mvar(v)
    so that each left term equals its right term; other variables are constants.
    Returns the bindings or None. O(total size) plus the equality tests."""
    b: Subst = {}
    stack = list(pairs)
    while stack:
        p, u = stack.pop()
        if isinstance(p, str):
            if is_mvar(p):
                if p in b:
                    if not term_eq(b[p], u):
                        return None
                else:
                    b[p] = u
            elif not (isinstance(u, str) and u == p):
                return None
            continue
        if isinstance(u, str) or p[0] != u[0] or len(p) != len(u):
            return None
        stack.extend(zip(p[1:], u[1:]))
    return b


def walk(t: Term, theta: Subst) -> Term:
    while isinstance(t, str) and t in theta:
        t = theta[t]
    return t


def occurs(v: str, t: Term, theta: Subst) -> bool:
    stack = [t]
    while stack:
        u = walk(stack.pop(), theta)
        if isinstance(u, str):
            if u == v:
                return True
        else:
            stack.extend(u[1:])
    return False


def unify(s: Term, t: Term, theta: Subst, trail: list[str], rigid: Callable[[str], bool]) -> bool:
    """Extend the triangular substitution theta to unify s and t, recording
    new bindings on trail. Variables v with rigid(v) are never bound.
    On failure, theta may hold partial bindings; the caller undoes the trail."""
    stack = [(s, t)]
    while stack:
        a, b = stack.pop()
        a = walk(a, theta)
        b = walk(b, theta)
        if isinstance(a, str) and isinstance(b, str) and a == b:
            continue
        if isinstance(a, str) and not rigid(a):
            if occurs(a, b, theta):
                return False
            theta[a] = b
            trail.append(a)
            continue
        if isinstance(b, str) and not rigid(b):
            if occurs(b, a, theta):
                return False
            theta[b] = a
            trail.append(b)
            continue
        if isinstance(a, str) or isinstance(b, str):
            return False
        if a[0] != b[0] or len(a) != len(b):
            return False
        stack.extend(zip(a[1:], b[1:]))
    return True


class Node:
    """A node: a substitution, children, and at a leaf the stored entries."""

    __slots__ = ("subst", "children", "entries")

    def __init__(self, subst: Subst, children: list["Node"] | None = None,
                 entries: list[tuple[Term, Any]] | None = None) -> None:
        self.subst = subst
        self.children = children if children is not None else []
        self.entries = entries if entries is not None else []


MODES = {
    "generalizations": lambda v: v[0] == "?",
    "instances": lambda v: v[0] == "#",
    "unifiable": lambda v: False,
}


class SubstitutionTree:
    """A substitution tree storing entries (term, value)."""

    def __init__(self) -> None:
        self.top = Node({})
        self.n = 0
        self._next = 1

    def _fresh(self) -> str:
        v = "*" + str(self._next)
        self._next += 1
        return v

    def _generalize(self, sigma: Subst, tau: Subst) -> tuple[Subst, Subst, Subst, bool]:
        """A common generalization mu of sigma and tau on dom(sigma), with
        mu alpha = sigma and mu beta = tau there. Where the two terms differ,
        mu keeps an indicator variable of sigma, or else gets a fresh one.
        Also reports whether some mu(x) is not an indicator variable.
        O(|sigma| + |tau|)."""
        mu: Subst = {}
        alpha: Subst = {}
        beta: Subst = {}
        nontrivial = False
        for x, s in sigma.items():
            u = tau[x]
            out: list[Term] = []
            stack: list[tuple[Term, Term, bool]] = [(s, u, False)]
            while stack:
                a, b, done = stack.pop()
                if done:
                    k = len(a) - 1
                    args = out[len(out) - k:] if k else []
                    del out[len(out) - k:]
                    out.append((a[0], *args))
                elif isinstance(a, str) and isinstance(b, str) and a == b:
                    out.append(a)
                elif (not isinstance(a, str) and not isinstance(b, str)
                      and a[0] == b[0] and len(a) == len(b)):
                    stack.append((a, b, True))
                    for p, q in reversed(list(zip(a[1:], b[1:]))):
                        stack.append((p, q, False))
                elif isinstance(a, str) and is_ivar(a):
                    beta[a] = b  # keep the open variable of sigma, bound below
                    out.append(a)
                else:
                    z = self._fresh()
                    alpha[z] = a
                    beta[z] = b
                    out.append(z)
            mu[x] = out[0]
            if not (isinstance(out[0], str) and is_ivar(out[0])):
                nontrivial = True
        return mu, alpha, beta, nontrivial

    def insert(self, term: Term, value: Any) -> None:
        """Store the entry (term, value). Each child of each visited node is
        tried once by matching and at most once by generalization, each in
        time linear in its substitution, so the cost is O(S + |term|), where S
        is the total size of the substitutions in the tree."""
        tau: Subst = {"*0": normalize(term)}  # @line L1
        node = self.top
        while tau:  # @line L2
            nxt = None
            for c in node.children:  # @line L3
                rho = match_pairs([(c.subst[x], tau[x]) for x in c.subst], is_ivar)
                if rho is not None:
                    nxt = (c, rho)
                    break
            if nxt is None:
                break
            c, rho = nxt
            tau = {x: u for x, u in tau.items() if x not in c.subst}  # @line L4
            tau.update(rho)
            node = c
        if not tau:  # @line L5
            node.entries.append((term, value))
            self.n += 1
            return
        for i, c in enumerate(node.children):  # @line L6
            mu, alpha, beta, nontrivial = self._generalize(c.subst, tau)
            if nontrivial and alpha:  # @line L7
                rest = {x: u for x, u in tau.items() if x not in mu}
                rest.update(beta)
                c.subst = alpha
                node.children[i] = Node(mu, [c, Node(rest, entries=[(term, value)])])  # @line L8
                self.n += 1
                return
        node.children.append(Node(dict(tau), entries=[(term, value)]))  # @line L9
        self.n += 1

    def retrieve(self, query: Term, mode: str = "unifiable") -> list[tuple[Term, Any]]:
        """Return the stored entries (term, value) whose term
        - is a generalization of query (term sigma = query), for mode "generalizations";
        - is an instance of query (query sigma = term), for mode "instances";
        - is unifiable with query after renaming apart, for mode "unifiable".
        The cost is one unification for each visited node; for generalizations
        every variable is bound to a subterm of the query, so a node with a
        substitution of size s costs O(s n) and the total is O(S n)."""
        rigid = MODES[mode]
        q = rebuild(query, lambda v: "?" + v)
        theta: Subst = {"*0": q}  # @line L10
        trail: list[str] = []
        out: list[tuple[Term, Any]] = []
        stack: list[tuple[str, Any]] = [("visit", c) for c in reversed(self.top.children)]
        while stack:  # @line L11
            op, x = stack.pop()
            if op == "undo":  # @line L12
                while len(trail) > x:
                    del theta[trail.pop()]
                continue
            mark = len(trail)
            ok = all(unify(v, s, theta, trail, rigid) for v, s in x.subst.items())  # @line L13
            if ok and x.children:  # @line L14
                stack.append(("undo", mark))
                stack.extend(("visit", c) for c in reversed(x.children))
                continue
            if ok:  # @line L15
                out.extend(x.entries)
            while len(trail) > mark:  # @line L16
                del theta[trail.pop()]
        return out

    def delete(self, term: Term, value: Any) -> bool:
        """Remove one copy of the entry (term, value); return whether it was there."""
        t = normalize(term)
        stack: list[tuple[Node, Subst, list[Node]]] = [(self.top, {"*0": t}, [self.top])]
        while stack:  # @line L17
            node, tau, path = stack.pop()
            if not tau:
                for k, (s, v) in enumerate(node.entries):  # @line L18
                    if v == value and term_eq(s, term):
                        del node.entries[k]
                        self.n -= 1
                        self._prune(path)
                        return True
                continue
            for c in node.children:
                rho = match_pairs([(c.subst[x], tau[x]) for x in c.subst], is_ivar)
                if rho is not None:
                    nt = {x: u for x, u in tau.items() if x not in c.subst}
                    nt.update(rho)
                    stack.append((c, nt, path + [c]))
        return False

    def _prune(self, path: list[Node]) -> None:
        leaf = path[-1]
        if leaf.entries:
            return
        parent = path[-2]
        parent.children.remove(leaf)  # @line L19
        if parent is self.top or len(parent.children) != 1:
            return
        child = parent.children[0]  # @line L20
        introduced: set[str] = set()
        for s in parent.subst.values():
            stack = [s]
            while stack:
                u = stack.pop()
                if isinstance(u, str):
                    if is_ivar(u):
                        introduced.add(u)
                else:
                    stack.extend(u[1:])
        merged = {x: apply(s, child.subst) for x, s in parent.subst.items()}  # @line L21
        merged.update({y: s for y, s in child.subst.items() if y not in introduced})
        grand = path[-3]
        grand.children[grand.children.index(parent)] = Node(merged, child.children, child.entries)

    def entries(self) -> list[tuple[Term, Any]]:
        """All stored entries. O(number of nodes + n)."""
        out: list[tuple[Term, Any]] = []
        stack = [self.top]
        while stack:
            x = stack.pop()
            out.extend(x.entries)
            stack.extend(x.children)
        return out

    def __len__(self) -> int:
        return self.n
