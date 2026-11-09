# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/robinson-unification/. The authors are listed in prov/JGY442.jsonl.

"""Robinson's unification algorithm (1965) on tree terms.

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
    """Return t with each variable x in the domain of sigma replaced by sigma[x].

    The replacement is simultaneous. It uses an explicit stack, so deep terms
    do not hit the Python recursion limit. Cost: O(size of the result).
    """
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
    """Return True if the variable x occurs in t. Cost: O(size of t)."""
    stack = [t]
    while stack:
        u = stack.pop()
        if is_var(u):
            if u == x:
                return True
        else:
            stack.extend(u[1:])
    return False


def disagreement_pair(s: Term, t: Term) -> Optional[tuple[Term, Term]]:
    """Return the leftmost pair of subterms at which s and t first differ.

    The two terms are read together in preorder. The pair is taken at the
    first position where the symbols, the arities or the variables differ.
    Return None when s and t are identical.
    """
    stack = [(s, t)]
    while stack:
        u, v = stack.pop()
        if u == v:
            continue
        if is_var(u) or is_var(v) or u[0] != v[0] or len(u) != len(v):
            return u, v
        for a, b in zip(reversed(u[1:]), reversed(v[1:])):
            stack.append((a, b))
    return None


def robinson_unification(s: Term, t: Term) -> Optional[Subst]:
    """Return an idempotent most general unifier of s and t, or None.

    Precondition: s and t are finite terms in the representation above.
    The result sigma satisfies apply(s, sigma) == apply(t, sigma), and each
    unifier of s and t is an instance of sigma. Each binding step removes one
    variable, so there are at most n steps for n variables, but on tree terms
    the terms s sigma and t sigma can grow to size exponential in n.
    """
    sigma: Subst = {}  # @line L1
    s1, t1 = s, t
    while True:
        pair = disagreement_pair(s1, t1)  # @line L2
        if pair is None:
            return sigma  # @line L8
        u, v = pair  # @line L3
        if not is_var(u) and not is_var(v):
            return None  # @line L4
        if is_var(u):  # @line L5
            x, r = u, v
        else:
            x, r = v, u
        if occurs(x, r):
            return None  # @line L6
        bind = {x: r}  # @line L7
        sigma = {y: apply(w, bind) for y, w in sigma.items()}
        sigma[x] = r
        s1, t1 = apply(s1, bind), apply(t1, bind)
