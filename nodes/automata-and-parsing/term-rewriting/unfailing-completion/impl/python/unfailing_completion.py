# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unfailing-completion/. The authors are listed in prov/FECHPF.jsonl.

"""Unfailing (ordered) completion with the lexicographic path ordering.

Terms: a variable is a str, an application is a tuple (f, arg1, ..., argk),
and a constant is a 1-tuple such as ("a",). An equation is a pair (s, t) of
terms. The order is the lexicographic path ordering (LPO) for a precedence,
given as a dict from symbols to integers (larger is bigger); with distinct
ranks for all symbols, the LPO is total on ground terms.

Rewriting and the main loop use explicit stacks; the LPO comparison is
recursive, with depth at most the sum of the depths of the two terms.
"""

import heapq
from dataclasses import dataclass, field
from typing import Union

Term = Union[str, tuple]
Equation = tuple[Term, Term]


def is_var(t: Term) -> bool:
    return isinstance(t, str)


def variables(t: Term) -> set[str]:
    out: set[str] = set()
    stack = [t]
    while stack:
        u = stack.pop()
        if isinstance(u, str):
            out.add(u)
        else:
            stack.extend(u[1:])
    return out


def occurs(v: str, t: Term) -> bool:
    return v in variables(t)


def lpo_gt(s: Term, t: Term, prec: dict[str, int]) -> bool:
    """s >_lpo t. Memoized on pairs of subterm occurrences, so there are at
    most |s| |t| distinct calls, each with O(|s| + |t|) work for the
    equality and occurrence tests: O(|s| |t| (|s| + |t|)) time in all."""
    memo: dict[tuple[int, int], bool] = {}

    def gt(s: Term, t: Term) -> bool:
        key = (id(s), id(t))
        if key in memo:
            return memo[key]
        if isinstance(t, str):
            r = not isinstance(s, str) and occurs(t, s)
        elif isinstance(s, str):
            r = False
        elif any(si == t or gt(si, t) for si in s[1:]):
            r = True
        elif prec[s[0]] > prec[t[0]]:
            r = all(gt(s, tj) for tj in t[1:])
        elif s[0] == t[0] and len(s) == len(t) and all(gt(s, tj) for tj in t[1:]):
            r = False
            for a, b in zip(s[1:], t[1:]):
                if a != b:
                    r = gt(a, b)
                    break
        else:
            r = False
        memo[key] = r
        return r

    return gt(s, t)


def apply(t: Term, sigma: dict[str, Term]) -> Term:
    """t sigma, where the values of sigma are already fully applied. O(|t sigma|)."""
    out: list[Term] = []
    stack: list[tuple[Term, bool]] = [(t, False)]
    while stack:
        u, done = stack.pop()
        if isinstance(u, str):
            out.append(sigma.get(u, u))
        elif done:
            k = len(u) - 1
            args = out[len(out) - k:] if k else []
            del out[len(out) - k:]
            out.append((u[0], *args))
        else:
            stack.append((u, True))
            stack.extend((a, False) for a in reversed(u[1:]))
    return out[0]


def match(p: Term, t: Term) -> dict[str, Term] | None:
    """A substitution sigma with p sigma = t, or None; variables of t are constants."""
    sigma: dict[str, Term] = {}
    stack = [(p, t)]
    while stack:
        a, b = stack.pop()
        if isinstance(a, str):
            if a in sigma:
                if sigma[a] != b:
                    return None
            else:
                sigma[a] = b
        elif isinstance(b, str) or a[0] != b[0] or len(a) != len(b):
            return None
        else:
            stack.extend(zip(a[1:], b[1:]))
    return sigma


def unify(s: Term, t: Term) -> dict[str, Term] | None:
    """A most general unifier, fully applied, or None."""
    sigma: dict[str, Term] = {}
    stack = [(s, t)]
    while stack:
        a, b = stack.pop()
        a, b = apply(a, sigma), apply(b, sigma)
        if a == b:
            continue
        if isinstance(b, str) and not isinstance(a, str):
            a, b = b, a
        if isinstance(a, str):
            if occurs(a, b):
                return None
            sigma = {x: apply(u, {a: b}) for x, u in sigma.items()}
            sigma[a] = b
        elif a[0] != b[0] or len(a) != len(b):
            return None
        else:
            stack.extend(zip(a[1:], b[1:]))
    return sigma


def positions(t: Term) -> list[tuple[int, ...]]:
    """The non-variable positions of t, in preorder."""
    out: list[tuple[int, ...]] = []
    stack: list[tuple[Term, tuple[int, ...]]] = [(t, ())]
    while stack:
        u, p = stack.pop()
        if isinstance(u, str):
            continue
        out.append(p)
        for i in range(len(u) - 1, 0, -1):
            stack.append((u[i], p + (i,)))
    return out


def subterm(t: Term, p: tuple[int, ...]) -> Term:
    for i in p:
        t = t[i]
    return t


def replace(t: Term, p: tuple[int, ...], r: Term) -> Term:
    path = []
    for i in p:
        path.append(t)
        t = t[i]
    for u, i in zip(reversed(path), reversed(p)):
        r = u[:i] + (r,) + u[i + 1:]
    return r


def orientations(e: Equation, prec: dict[str, int]) -> list[Equation]:
    """The directions in which an equation may be used: one if it is
    oriented by the LPO, else both."""
    s, t = e
    if lpo_gt(s, t, prec):
        return [(s, t)]
    if lpo_gt(t, s, prec):
        return [(t, s)]
    return [(s, t), (t, s)]


def usable(eqs: list[Equation], prec: dict[str, int]) -> list[tuple[Term, Term, bool]]:
    """The directions u -> v of the equations that ordered rewriting may use,
    with a flag telling whether u > v holds already, so no test is needed.
    A direction is skipped if u is a variable or v has a variable not in u."""
    out = []
    for e in eqs:
        dirs = orientations(e, prec)
        for u, v in dirs:
            if not is_var(u) and variables(v) <= variables(u):
                out.append((u, v, len(dirs) == 1))
    return out


def rewrite_once(t: Term, dirs: list[tuple[Term, Term, bool]], prec: dict[str, int]) -> Term | None:
    """One ordered rewrite step: at the first position p in preorder and with the
    first usable direction u -> v, if t|p = u sigma and u sigma > v sigma."""
    for p in positions(t):
        sub = subterm(t, p)
        for u, v, oriented in dirs:
            sigma = match(u, sub)
            if sigma is None:
                continue
            r = apply(v, sigma)
            if oriented or lpo_gt(sub, r, prec):
                return replace(t, p, r)
    return None


def normal_form(t: Term, eqs: list[Equation], prec: dict[str, int]) -> Term:
    """Ordered rewriting to a normal form; terminates since each step decreases t in the LPO."""
    dirs = usable(eqs, prec)
    while True:
        r = rewrite_once(t, dirs, prec)
        if r is None:
            return t
        t = r


def rename(e: Equation, suffix: str) -> Equation:
    names: dict[str, Term] = {}
    for v in variables(e[0]) | variables(e[1]):
        names[v] = v + suffix
    return apply(e[0], names), apply(e[1], names)


def ordered_critical_pairs(e1: Equation, e2: Equation, prec: dict[str, int]) -> list[Equation]:
    """The ordered critical pairs of e2 into e1: for each usable direction
    u1 = v1 of e1 and u2 = v2 of e2 (renamed apart), each non-variable position
    p of u1 and mgu sigma of u1|p and u2, the pair (u1 sigma[v2 sigma]_p, v1 sigma),
    unless v1 sigma > u1 sigma or v2 sigma > u2 sigma."""
    out: list[Equation] = []
    for u1, v1 in orientations(e1, prec):
        for u2, v2 in orientations(rename(e2, "'"), prec):
            for p in positions(u1):
                sigma = unify(subterm(u1, p), u2)
                if sigma is None:
                    continue
                a, b = apply(u1, sigma), apply(v1, sigma)
                c = apply(v2, sigma)
                if lpo_gt(b, a, prec) or lpo_gt(c, apply(u2, sigma), prec):
                    continue
                out.append((replace(a, p, c), b))
    return out


def size(t: Term) -> int:
    n = 0
    stack = [t]
    while stack:
        u = stack.pop()
        n += 1
        if not isinstance(u, str):
            stack.extend(u[1:])
    return n


def canonical(e: Equation) -> Equation:
    """e with its variables renamed v1, v2, ... by first occurrence, so that
    two equations are variants iff their canonical forms are equal."""
    names: dict[str, Term] = {}
    stack = [e[1], e[0]]
    while stack:
        u = stack.pop()
        if isinstance(u, str):
            if u not in names:
                names[u] = "v" + str(len(names) + 1)
        else:
            stack.extend(reversed(u[1:]))
    return apply(e[0], names), apply(e[1], names)


@dataclass
class Result:
    """saturated is True if the final equations were checked to have no
    ordered critical pair with different normal forms; then ordered rewriting
    with them decides the ground word problem of E."""

    saturated: bool
    equations: list[Equation] = field(default_factory=list)
    steps: int = 0


def unfailing_completion(E: list[Equation], prec: dict[str, int], max_steps: int = 500) -> Result:
    """Unfailing completion with the LPO for prec, in the given-equation style.

    Each step takes a smallest pending equation (oldest first among equal
    sizes), simplifies it by ordered rewriting with the active equations, and,
    unless it becomes trivial or a variant of an active equation, adds it,
    sends back to pending the active equations that it simplifies, and adds
    its ordered critical pairs with the active equations. When nothing is
    pending, all ordered critical pairs of the active set are recomputed; if
    they all have equal normal forms the result is saturated. Gives up after
    max_steps steps. Each step costs a critical pair computation against all
    active equations, so the time is not bounded in terms of |E|."""
    active: list[Equation] = []  # @line L1
    heap: list[tuple[int, int, Equation]] = []
    count = 0

    def push(e: Equation) -> None:
        nonlocal count
        heapq.heappush(heap, (size(e[0]) + size(e[1]), count, e))
        count += 1

    dirs_cache: list = [None]

    def nf(t: Term) -> Term:
        if dirs_cache[0] is None:
            dirs_cache[0] = usable(active, prec)
        while True:
            r = rewrite_once(t, dirs_cache[0], prec)
            if r is None:
                return t
            t = r

    for e in E:
        push(e)
    steps = 0
    while steps < max_steps:  # @line L2
        if not heap:  # @line L3
            open_pairs = [cp for a in active for b in active
                          for cp in ordered_critical_pairs(a, b, prec)
                          if nf(cp[0]) != nf(cp[1])]
            if not open_pairs:
                return Result(True, active, steps)  # @line L4
            for cp in open_pairs:
                push(cp)
            continue
        _, _, (s, t) = heapq.heappop(heap)  # @line L5
        steps += 1
        s, t = nf(s), nf(t)  # @line L6
        c = canonical((s, t))
        if s == t or any(c == canonical(a) or c == canonical((a[1], a[0])) for a in active):  # @line L7
            continue
        if lpo_gt(t, s, prec):  # @line L8
            s, t = t, s
        e = (s, t)
        keep: list[Equation] = []
        dirs = usable([e], prec)
        for a in active:  # @line L9
            if rewrite_once(a[0], dirs, prec) is not None or rewrite_once(a[1], dirs, prec) is not None:
                push(a)
            else:
                keep.append(a)
        active = keep + [e]  # @line L10
        dirs_cache[0] = None
        for other in active:  # @line L11
            for cp in ordered_critical_pairs(e, other, prec) + ordered_critical_pairs(other, e, prec):
                push(cp)
    return Result(False, active, steps)  # @line L12


def equal(s: Term, t: Term, result: Result, prec: dict[str, int]) -> bool:
    """Decide s = t modulo E for ground s and t, if result is saturated."""
    return normal_form(s, result.equations, prec) == normal_form(t, result.equations, prec)
