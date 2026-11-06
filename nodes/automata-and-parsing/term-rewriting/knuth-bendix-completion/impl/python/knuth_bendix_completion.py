# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/knuth-bendix-completion/. The authors are listed in prov/WM035M.jsonl.

"""Knuth-Bendix completion with simplification, collapse and composition.

A term is a variable, written as a str, or an application, written as a tuple
(f, t1, ..., tn) whose first item is the function symbol; a constant a is
("a",). An equation or a rule is a pair (s, t) of terms. Positions are tuples
of 1-based argument indexes.

complete(equations, greater, max_steps) returns one of
    ("success", rules)    rules is convergent and has the same equational
                          theory as the equations,
    ("fail", (s, t))      the normalized equation s = t cannot be oriented,
    ("give up", rules)    max_steps iterations of the main loop were used.

greater(s, t) must be a reduction ordering; lpo(precedence) builds the
lexicographic path ordering. All functions use explicit stacks, so deep terms
do not hit the recursion limit.
"""

import heapq
from itertools import count
from typing import Callable, Optional, Union

Term = Union[str, tuple]
Pair = tuple[Term, Term]
Order = Callable[[Term, Term], bool]


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


def size(t: Term) -> int:
    n = 0
    stack = [t]
    while stack:
        u = stack.pop()
        n += 1
        if not is_var(u):
            stack.extend(u[1:])
    return n


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


def rename(t: Term, names: dict[str, str]) -> Term:
    return substitute(t, {x: y for x, y in names.items()})


_NAMES = ["x", "y", "z", "u", "v", "w"]


def canonical(pair: Pair) -> Pair:
    """Rename the variables of a pair to x, y, z, u, v, w, x7, x8, ..."""
    s, t = pair
    seen = variables(("=", s, t))
    names = {v: (_NAMES[i] if i < len(_NAMES) else f"x{i + 1}") for i, v in enumerate(seen)}
    return rename(s, names), rename(t, names)


# ---------- rewriting ----------

def reducible(t: Term, rules: list[Pair]) -> bool:
    for _, u in subterms(t):
        if not is_var(u):
            for l, _ in rules:
                if match(l, u) is not None:
                    return True
    return False


def normalize(t: Term, rules: list[Pair]) -> Term:
    """Innermost normal form of t. The rules must terminate."""
    by_root: dict[str, list[Pair]] = {}
    for l, r in rules:
        by_root.setdefault(l[0], []).append((l, r))
    tasks: list[tuple] = [(0, t, None)]
    vals: list[Term] = []
    while tasks:
        kind, u, env = tasks.pop()
        if kind == 0:  # evaluate u under env, whose values are normal forms
            if is_var(u):
                vals.append(env[u] if env is not None and u in env else u)
            else:
                tasks.append((1, u, len(u) - 1))
                for a in reversed(u[1:]):
                    tasks.append((0, a, env))
        else:  # build u[0] over the top values and try the rules at the root
            n = env
            args = vals[len(vals) - n:] if n else []
            del vals[len(vals) - n:]
            s = (u[0],) + tuple(args)
            for l, r in by_root.get(s[0], ()):
                tau = match(l, s)
                if tau is not None:
                    tasks.append((0, r, tau))
                    break
            else:
                vals.append(s)
    return vals[0]


def critical_pairs(rule1: Pair, rule2: Pair, same: bool = False) -> list[Pair]:
    """Critical pairs from overlapping rule2 into non-variable positions of
    rule1. If same is true, the root overlap is skipped."""
    v1, v2 = variables(rule1[0]), variables(rule2[0])
    l1 = rename(rule1[0], {x: f"_a{i}" for i, x in enumerate(v1)})
    r1 = rename(rule1[1], {x: f"_a{i}" for i, x in enumerate(v1)})
    l2 = rename(rule2[0], {x: f"_b{i}" for i, x in enumerate(v2)})
    r2 = rename(rule2[1], {x: f"_b{i}" for i, x in enumerate(v2)})
    out = []
    for p, u in subterms(l1):
        if is_var(u) or (same and p == ()):
            continue
        sigma = unify(u, l2)
        if sigma is None:
            continue
        top = substitute(l1, sigma)
        out.append(canonical((replace(top, p, substitute(r2, sigma)), substitute(r1, sigma))))
    return out


def all_critical_pairs(rules: list[Pair]) -> list[Pair]:
    out = []
    for i, a in enumerate(rules):
        for j, b in enumerate(rules):
            out.extend(critical_pairs(a, b, same=(i == j)))
    return out


# ---------- the lexicographic path ordering ----------

def lpo(precedence: dict[str, int]) -> Order:
    """s >lpo t for the precedence f > g iff precedence[f] > precedence[g].
    Symbols missing from the precedence are incomparable with all others.
    Pairs of subterms are memoized, so the time is polynomial."""

    def greater(s: Term, t: Term) -> bool:
        ids: dict[tuple, int] = {}
        nodes: list[tuple] = []
        varsets: list[frozenset] = []

        def intern(term: Term) -> int:
            out: list[int] = []
            stack: list[tuple[bool, Term]] = [(False, term)]
            while stack:
                done, u = stack.pop()
                if is_var(u):
                    key: tuple = ("?", u)
                    vs = frozenset([u])
                elif not done:
                    stack.append((True, u))
                    for a in reversed(u[1:]):
                        stack.append((False, a))
                    continue
                else:
                    n = len(u) - 1
                    kids = tuple(out[len(out) - n:]) if n else ()
                    del out[len(out) - n:]
                    key = (u[0], kids)
                    vs = frozenset().union(*(varsets[k] for k in kids)) if kids else frozenset()
                if key not in ids:
                    ids[key] = len(nodes)
                    nodes.append(key)
                    varsets.append(vs)
                out.append(ids[key])
            return out[0]

        a0, b0 = intern(s), intern(t)
        memo: dict[tuple[int, int], bool] = {}

        def frame(a: int, b: int):
            fa, ka = nodes[a]
            fb, kb = nodes[b]
            if fa == "?":
                return False
            if fb == "?":
                return kb in varsets[a] and a != b
            for c in ka:
                if c == b:
                    return True
                if (yield (c, b)):
                    return True
            pf, pg = precedence.get(fa), precedence.get(fb)
            if fa != fb and pf is not None and pg is not None and pf > pg:
                for c in kb:
                    if not (yield (a, c)):
                        return False
                return True
            if fa == fb and len(ka) == len(kb):
                k = 0
                while k < len(ka) and ka[k] == kb[k]:
                    k += 1
                if k == len(ka) or not (yield (ka[k], kb[k])):
                    return False
                for c in kb:
                    if not (yield (a, c)):
                        return False
                return True
            return False

        stack = [((a0, b0), frame(a0, b0))]
        val = None
        while stack:
            key, gen = stack[-1]
            try:
                q = gen.send(val)
            except StopIteration as stop:
                memo[key] = bool(stop.value)
                val = memo[key]
                stack.pop()
                continue
            if q in memo:
                val = memo[q]
            else:
                stack.append((q, frame(*q)))
                val = None
        return memo[(a0, b0)]

    return greater


# ---------- completion ----------

def complete(equations: list[Pair], greater: Order, max_steps: int = 1000):
    """Knuth-Bendix completion; see the module docstring for the result."""
    tick = count()
    pending: list = []

    def push(s: Term, t: Term) -> None:
        heapq.heappush(pending, (size(s) + size(t), next(tick), s, t))

    for s, t in equations:  # @line L1
        push(s, t)
    rules: list[Pair] = []
    steps = 0
    while True:  # @line L2
        if not pending:  # @line L3
            for u, v in all_critical_pairs(rules):
                if not term_eq(normalize(u, rules), normalize(v, rules)):
                    push(u, v)
            if not pending:
                return "success", rules
        steps += 1  # @line L4
        if steps > max_steps:
            return "give up", rules
        _, _, s, t = heapq.heappop(pending)  # @line L5
        s, t = normalize(s, rules), normalize(t, rules)
        if term_eq(s, t):  # @line L6
            continue
        if greater(s, t):  # @line L7
            rho = canonical((s, t))
        elif greater(t, s):
            rho = canonical((t, s))
        else:
            return "fail", (s, t)
        kept = []  # @line L8
        for g, d in rules:
            if reducible(g, [rho]):
                push(g, d)
            else:
                kept.append((g, d))
        for i, (g, d) in enumerate(kept):  # @line L9
            others = kept[:i] + kept[i + 1:] + [rho]
            kept[i] = (g, normalize(d, others))
        rules = kept + [rho]  # @line L10
        for rule in rules:
            for u, v in critical_pairs(rho, rule, same=rule is rho):
                push(u, v)
            if rule is not rho:
                for u, v in critical_pairs(rule, rho):
                    push(u, v)
