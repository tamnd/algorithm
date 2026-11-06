# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/innermost-reduction/. The authors are listed in prov/KTF62M.jsonl.

"""Leftmost-innermost reduction of first-order terms.

A term is a variable, written as a str, or an application, written as a tuple
(f, t1, ..., tn) whose first item is the function symbol; a constant a is
("a",). A rule is a pair (l, r) of terms where l is not a variable and every
variable of r occurs in l. Positions are tuples of 1-based argument indexes.

All functions use explicit stacks, so deep terms do not hit the recursion limit.
Terms built by a rule share the subterms bound to its variables.
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
    """Return sigma with pattern sigma = term, or None. Non-linear patterns
    need equal subterms at all occurrences of a variable."""
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


def check_rules(rules: list[Rule]) -> None:
    for i, (l, r) in enumerate(rules):
        if is_var(l):
            raise ValueError(f"rule {i}: the left side is a variable")
        if not variables(r) <= variables(l):
            raise ValueError(f"rule {i}: a variable of the right side is not on the left side")


def _position(link: Optional[tuple]) -> Position:
    out: list[int] = []
    while link is not None:
        link, i = link
        out.append(i)
    return tuple(reversed(out))


def innermost_normalize(
    t: Term,
    rules: list[Rule],
    max_steps: Optional[int] = None,
    trace: Optional[list[tuple[Position, int]]] = None,
) -> tuple[Optional[Term], int]:
    """Reduce t by leftmost-innermost steps, with the first matching rule.

    Returns (normal form, number of steps), or (None, max_steps) when the
    bound is reached before a normal form. When trace is a list, each step
    is appended to it as (position, rule index).
    """
    check_rules(rules)
    # A position is kept as a linked list (parent, index), with None for the
    # root, so that moving one level down costs O(1).
    steps = 0  # @line L1
    # A task is ("eval", u, sigma, p): normalize u sigma at position p, where the
    # values of sigma are normal forms; or ("build", f, n, p).
    tasks: list[tuple] = [("eval", t, None, None)]
    vals: list[Term] = []
    while tasks:  # @line L2
        task = tasks.pop()  # @line L3
        if task[0] == "eval":
            _, u, sigma, p = task
            if is_var(u):  # @line L4
                vals.append(sigma[u] if sigma is not None and u in sigma else u)
            else:  # @line L5
                n = len(u) - 1
                tasks.append(("build", u[0], n, p))
                for i in range(n, 0, -1):
                    tasks.append(("eval", u[i], sigma, (p, i)))
        else:
            _, f, n, p = task
            args = vals[len(vals) - n:] if n else []  # @line L6
            del vals[len(vals) - n:]
            s = (f, *args)
            found = None
            for idx, (l, r) in enumerate(rules):  # @line L7
                tau = match(l, s)
                if tau is not None:
                    found = (idx, r, tau)
                    break
            if found is None:  # @line L8
                vals.append(s)
            elif max_steps is not None and steps >= max_steps:  # @line L9
                return None, steps
            else:
                idx, r, tau = found
                steps += 1  # @line L10
                if trace is not None:
                    trace.append((_position(p), idx))
                tasks.append(("eval", r, tau, p))
    return vals.pop(), steps  # @line L11
