# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/discrimination-tree/. The authors are listed in prov/R1941B.jsonl.

"""A discrimination tree: a trie over the preorder symbols of terms.

A term is a variable, written as a str, or an application, written as a tuple
(f, t1, ..., tn) whose first item is the function symbol; a constant a is
("a",). The tree stores patterns, such as the left sides of rewrite rules,
each with a value. The key of a pattern is its preorder sequence of symbols,
where a function symbol f with n arguments is the pair (f, n) and every
variable is the same symbol STAR. So the tree forgets which variables are
equal: f(x, x) and f(x, y) have the same key.

retrieve(t) returns the entries whose pattern, with each variable occurrence
renamed apart, matches t. For a linear pattern this is the same as "the
pattern matches t". match(t) filters these candidates with a full matcher, so
it returns exactly the entries whose pattern matches t, also for non-linear
patterns. Variables of the query t are treated as constants that only a STAR
edge can consume. All functions use explicit stacks, so deep terms are safe.
"""

from typing import Any, Optional, Union

Term = Union[str, tuple]
STAR = "*"
_QVAR = object()  # tags the symbol of a query variable


def is_var(t: Term) -> bool:
    return isinstance(t, str)


def term_eq(s: Term, t: Term) -> bool:
    """Syntactic equality, without recursion."""
    stack = [(s, t)]
    while stack:
        u, v = stack.pop()
        if u is v:
            continue
        if is_var(u) or is_var(v):
            if u != v:
                return False
            continue
        if len(u) != len(v) or u[0] != v[0]:
            return False
        stack.extend(zip(u[1:], v[1:]))
    return True


def key(t: Term) -> list:
    """The preorder symbols of a pattern, with STAR for each variable."""
    out: list = []
    stack = [t]
    while stack:
        u = stack.pop()
        if is_var(u):
            out.append(STAR)
        else:
            out.append((u[0], len(u) - 1))
            stack.extend(reversed(u[1:]))
    return out


def flatten(t: Term) -> tuple[list, list[int]]:
    """The preorder symbols of a query and the skip array.

    A query variable x becomes the symbol (_QVAR, x), which no pattern key
    contains. skip[i] is the index just after the subterm that starts at i.
    """
    syms: list = []
    stack = [t]
    while stack:
        u = stack.pop()
        if is_var(u):
            syms.append((_QVAR, u))
        else:
            syms.append((u[0], len(u) - 1))
            stack.extend(reversed(u[1:]))
    n = len(syms)
    size = [1] * n
    for i in range(n - 1, -1, -1):
        s = syms[i]
        if s[0] is not _QVAR:
            j = i + 1
            for _ in range(s[1]):
                j += size[j]
            size[i] = j - i
    return syms, [i + size[i] for i in range(n)]


def match(pattern: Term, t: Term) -> Optional[dict[str, Term]]:
    """The matcher sigma with pattern sigma = t, or None. Variables of t are constants."""
    sigma: dict[str, Term] = {}
    stack = [(pattern, t)]
    while stack:
        p, u = stack.pop()
        if is_var(p):
            if p in sigma:
                if not term_eq(sigma[p], u):
                    return None
            else:
                sigma[p] = u
        elif is_var(u) or len(p) != len(u) or p[0] != u[0]:
            return None
        else:
            stack.extend(zip(p[1:], u[1:]))
    return sigma


class _Node:
    __slots__ = ("next", "vals")

    def __init__(self) -> None:
        self.next: dict[Any, "_Node"] = {}
        self.vals: list[tuple[Term, Any]] = []


class DiscriminationTree:
    """A set of (pattern, value) entries indexed by the preorder key of the pattern."""

    def __init__(self) -> None:
        self.root = _Node()
        self.n = 0

    def __len__(self) -> int:
        return self.n

    def insert(self, pattern: Term, value: Any) -> None:
        x = self.root  # @line L1
        for a in key(pattern):  # @line L2
            if a not in x.next:  # @line L3
                x.next[a] = _Node()
            x = x.next[a]  # @line L4
        x.vals.append((pattern, value))  # @line L5
        self.n += 1

    def retrieve(self, t: Term) -> list[tuple[Term, Any]]:
        """The entries whose pattern, made linear, matches t (a superset of the matches)."""
        syms, skip = flatten(t)  # @line L6
        n = len(syms)
        out: list[tuple[Term, Any]] = []
        stack = [(self.root, 0)]  # @line L7
        while stack:  # @line L8
            x, i = stack.pop()  # @line L9
            if i == n:  # @line L10
                out.extend(x.vals)
                continue
            star = x.next.get(STAR)
            if star is not None:  # @line L11
                stack.append((star, skip[i]))
            a = syms[i]
            if a[0] is not _QVAR and a in x.next:  # @line L12
                stack.append((x.next[a], i + 1))
        return out  # @line L13

    def match(self, t: Term) -> list[tuple[Any, dict[str, Term]]]:
        """The values of the entries whose pattern matches t, each with its matcher."""
        out = []  # @line L14
        for pattern, value in self.retrieve(t):  # @line L15
            sigma = match(pattern, t)  # @line L16
            if sigma is not None:
                out.append((value, sigma))
        return out  # @line L17

    def delete(self, pattern: Term, value: Any) -> bool:
        """Remove one entry (pattern, value). Return False if there is none."""
        k = key(pattern)
        path = [self.root]  # @line L18
        x = self.root
        for a in k:  # @line L19
            x = x.next.get(a)  # @line L20
            if x is None:
                return False
            path.append(x)
        for j, (p, v) in enumerate(x.vals):  # @line L21
            if v == value and term_eq(p, pattern):
                del x.vals[j]
                break
        else:
            return False
        self.n -= 1
        for i in range(len(path) - 1, 0, -1):  # @line L22
            if path[i].vals or path[i].next:  # @line L23
                break
            del path[i - 1].next[k[i - 1]]  # @line L24
        return True  # @line L25

    def node_count(self) -> int:
        count = 0
        stack = [self.root]
        while stack:
            x = stack.pop()
            count += 1
            stack.extend(x.next.values())
        return count
