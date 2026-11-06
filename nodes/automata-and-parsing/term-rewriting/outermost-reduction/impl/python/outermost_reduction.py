# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/outermost-reduction/. The authors are listed in prov/1DTK3Q.jsonl.

"""Leftmost-outermost reduction of first-order terms.

A term is a variable, written as a str, or an application, written as a tuple
(f, t1, ..., tn) whose first item is the function symbol; a constant a is
("a",). A rule is a pair (l, r) of terms where l is not a variable and every
variable of r occurs in l. Positions are tuples of 1-based argument indexes.

All functions use explicit stacks, so deep terms do not hit the recursion limit.
"""

from typing import Optional, Union

Term = Union[str, tuple]
Rule = tuple[Term, Term]
Position = tuple[int, ...]


def is_var(t: Term) -> bool:
    return isinstance(t, str)


def variables(t: Term) -> set[str]:
    out: set[str] = set()
    stack = [t]
    while stack:
        u = stack.pop()
        if is_var(u):
            out.add(u)
        else:
            stack.extend(u[1:])
    return out


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


def match(pattern: Term, term: Term) -> Optional[dict[str, Term]]:
    """Return sigma with pattern sigma = term, or None."""
    sigma: dict[str, Term] = {}
    stack = [(pattern, term)]
    while stack:
        p, t = stack.pop()
        if is_var(p):
            if p in sigma:
                if not term_eq(sigma[p], t):
                    return None
            else:
                sigma[p] = t
        elif is_var(t) or len(p) != len(t) or p[0] != t[0]:
            return None
        else:
            stack.extend(zip(p[1:], t[1:]))
    return sigma


def substitute(t: Term, sigma: dict[str, Term]) -> Term:
    """t sigma, built bottom-up with an explicit stack. Bound values are shared."""
    out: list[Term] = []
    stack: list[tuple[Term, bool]] = [(t, False)]
    while stack:
        u, done = stack.pop()
        if is_var(u):
            out.append(sigma.get(u, u))
        elif done:
            n = len(u) - 1
            args = out[len(out) - n:] if n else []
            del out[len(out) - n:]
            out.append((u[0], *args))
        else:
            stack.append((u, True))
            for a in reversed(u[1:]):
                stack.append((a, False))
    return out[0]


def check_rules(rules: list[Rule]) -> None:
    for i, (l, r) in enumerate(rules):
        if is_var(l):
            raise ValueError(f"rule {i}: the left side is a variable")
        if not variables(r) <= variables(l):
            raise ValueError(f"rule {i}: a variable of the right side is not on the left side")


def leftmost_outermost_redex(t: Term, rules: list[Rule]):
    """Search t in preorder for the first position where some rule matches.
    Returns (path, rule index, contractum) or None, where path lists the pairs
    (term, argument index) from the root down to the redex. During the search
    a path is a linked list (parent link, term, index), so a push costs O(1)."""
    stack: list[tuple[Term, Optional[tuple]]] = [(t, None)]
    while stack:
        u, path = stack.pop()
        for idx, (l, r) in enumerate(rules):
            tau = match(l, u)
            if tau is not None:
                pairs = []
                while path is not None:
                    path, parent, i = path
                    pairs.append((parent, i))
                pairs.reverse()
                return pairs, idx, substitute(r, tau)
        if not is_var(u):
            for i in range(len(u) - 1, 0, -1):
                stack.append((u[i], (path, u, i)))
    return None


def outermost_normalize(
    t: Term,
    rules: list[Rule],
    max_steps: Optional[int] = None,
    trace: Optional[list[tuple[Position, int]]] = None,
) -> tuple[Optional[Term], int]:
    """Reduce t by leftmost-outermost steps, with the first matching rule.

    Returns (normal form, number of steps), or (None, max_steps) when the
    bound is reached before a normal form. When trace is a list, each step
    is appended to it as (position, rule index).
    """
    check_rules(rules)
    steps = 0  # @line L1
    while True:  # @line L2
        found = leftmost_outermost_redex(t, rules)  # @line L3
        if found is None:  # @line L4
            return t, steps
        if max_steps is not None and steps >= max_steps:  # @line L5
            return None, steps
        path, idx, v = found
        for parent, i in reversed(path):  # @line L6
            v = parent[:i] + (v,) + parent[i + 1:]
        t = v
        steps += 1  # @line L7
        if trace is not None:
            trace.append((tuple(i for _, i in path), idx))
