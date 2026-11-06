# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/narrowing/. The authors are listed in prov/4TKTY0.jsonl.

"""Breadth-first narrowing: solve s = t modulo a term rewriting system.

A term is a variable, written as a str, or an application, written as a tuple
(f, t1, ..., tn) whose first item is the function symbol; a constant a is
("a",). A rule is a pair (l, r) of terms. Positions are tuples of 1-based
argument indexes. Variable names that start with "_" are reserved for the
fresh copies of rule variables.

narrow(s, t, rules, depth) returns the answers of all narrowing derivations of
length at most depth from the goal s = t, in breadth-first order, without
repetitions. An answer is a dict from each variable of s and t to a term.
Every answer theta is sound: s theta and t theta rewrite to a common term. If
the rules are confluent and terminating, the answers are also complete: every
normalized solution is an instance of an answer found with a large enough
depth (Hullot 1980). All functions use explicit stacks.
"""

from collections import deque
from itertools import count
from typing import Optional, Union

Term = Union[str, tuple]
Rule = tuple[Term, Term]


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


def variables(t: Term) -> list[str]:
    """The variables of t in left-to-right order of first occurrence."""
    out: list[str] = []
    seen: set[str] = set()
    stack = [t]
    while stack:
        u = stack.pop()
        if is_var(u):
            if u not in seen:
                seen.add(u)
                out.append(u)
        else:
            stack.extend(reversed(u[1:]))
    return out


def substitute(t: Term, sigma: dict[str, Term]) -> Term:
    """t sigma. Bound values are inserted as they are, without copying."""
    out: list[Term] = []
    stack: list[tuple[bool, Term]] = [(False, t)]
    while stack:
        done, u = stack.pop()
        if done:
            n = len(u) - 1
            args = out[len(out) - n:] if n else []
            del out[len(out) - n:]
            out.append((u[0],) + tuple(args))
        elif is_var(u):
            out.append(sigma.get(u, u))
        else:
            stack.append((True, u))
            for a in reversed(u[1:]):
                stack.append((False, a))
    return out[0]


def _walk(t: Term, sigma: dict[str, Term]) -> Term:
    while is_var(t) and t in sigma:
        t = sigma[t]
    return t


def _occurs(x: str, t: Term, sigma: dict[str, Term]) -> bool:
    stack = [t]
    while stack:
        u = _walk(stack.pop(), sigma)
        if is_var(u):
            if u == x:
                return True
        else:
            stack.extend(u[1:])
    return False


def _resolve(t: Term, sigma: dict[str, Term]) -> Term:
    """Apply a triangular substitution completely."""
    out: list[Term] = []
    stack: list[tuple[bool, Term]] = [(False, t)]
    while stack:
        done, u = stack.pop()
        if done:
            n = len(u) - 1
            args = out[len(out) - n:] if n else []
            del out[len(out) - n:]
            out.append((u[0],) + tuple(args))
            continue
        u = _walk(u, sigma)
        if is_var(u):
            out.append(u)
        else:
            stack.append((True, u))
            for a in reversed(u[1:]):
                stack.append((False, a))
    return out[0]


def unify(s: Term, t: Term) -> Optional[dict[str, Term]]:
    """A most general unifier of s and t, fully applied, or None."""
    sigma: dict[str, Term] = {}
    stack = [(s, t)]
    while stack:
        a, b = stack.pop()
        a, b = _walk(a, sigma), _walk(b, sigma)
        if is_var(a) and is_var(b) and a == b:
            continue
        if is_var(b) and not is_var(a):
            a, b = b, a
        if is_var(a):
            if _occurs(a, b, sigma):
                return None
            sigma[a] = b
            continue
        if len(a) != len(b) or a[0] != b[0]:
            return None
        stack.extend(zip(a[1:], b[1:]))
    return {x: _resolve(x, sigma) for x in sigma}


def subterms(t: Term) -> list[tuple[tuple[int, ...], Term]]:
    """All (position, subterm) pairs of t in preorder."""
    out = []
    stack: list[tuple[tuple[int, ...], Term]] = [((), t)]
    while stack:
        p, u = stack.pop()
        out.append((p, u))
        if not is_var(u):
            for i in range(len(u) - 1, 0, -1):
                stack.append((p + (i,), u[i]))
    return out


def replace(t: Term, p: tuple[int, ...], s: Term) -> Term:
    """t[s]_p, rebuilding only the path to p."""
    path = []
    u = t
    for i in p:
        path.append((u, i))
        u = u[i]
    for node, i in reversed(path):
        s = node[:i] + (s,) + node[i + 1:]
    return s


def show(t: Term) -> str:
    """A string form of t, built without recursion."""
    out: list[str] = []
    stack: list[Union[str, Term]] = [t]
    while stack:
        u = stack.pop()
        if isinstance(u, str):
            out.append(u)
        elif len(u) == 1:
            out.append(u[0])
        else:
            stack.append(")")
            for i in range(len(u) - 1, 0, -1):
                stack.append(u[i])
                if i > 1:
                    stack.append(",")
            stack.append(u[0] + "(")
    return "".join(out)


def _tidy(answer: dict[str, Term]) -> dict[str, Term]:
    """Rename the fresh variables of an answer to _1, _2, ... in order."""
    names: dict[str, str] = {}
    for x in answer:
        for v in variables(answer[x]):
            if v.startswith("_") and v not in names:
                names[v] = "_" + str(len(names) + 1)
    return {x: substitute(u, names) for x, u in answer.items()}


def narrow(s: Term, t: Term, rules: list[Rule], depth: int,
           max_answers: Optional[int] = None) -> list[dict[str, Term]]:
    """Answers of the narrowing derivations from s = t of length <= depth."""
    goal_vars = variables(("=", s, t))
    queue = deque([(("=", s, t), {x: x for x in goal_vars}, 0)])  # @line L1
    answers: list[dict[str, Term]] = []
    seen: set[str] = set()
    fresh = count(1)
    while queue:  # @line L2
        goal, sigma, d = queue.popleft()  # @line L3
        mu = unify(goal[1], goal[2])  # @line L4
        if mu is not None:
            answer = _tidy({x: substitute(sigma[x], mu) for x in goal_vars})
            key = "|".join(show(answer[x]) for x in goal_vars)
            if key not in seen:
                seen.add(key)
                answers.append(answer)
                if max_answers is not None and len(answers) >= max_answers:
                    return answers
        if d >= depth:  # @line L5
            continue
        for p, u in subterms(goal):  # @line L6
            if not p or is_var(u):
                continue
            for l, r in rules:  # @line L7
                k = next(fresh)
                names = {x: "_" + str(k) + x for x in variables(l)}
                l2, r2 = substitute(l, names), substitute(r, names)
                tau = unify(u, l2)  # @line L8
                if tau is None:
                    continue
                child = substitute(replace(goal, p, r2), tau)  # @line L9
                queue.append((child, {x: substitute(v, tau) for x, v in sigma.items()}, d + 1))
    return answers  # @line L10
