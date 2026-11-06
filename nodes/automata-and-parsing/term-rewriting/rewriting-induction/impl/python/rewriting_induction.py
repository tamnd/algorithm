# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rewriting-induction/. The authors are listed in prov/35E48J.jsonl.

"""Rewriting induction (Reddy 1990) with the lexicographic path ordering.

Terms: a variable is a str, an application is a tuple (f, arg1, ..., argk),
and a constant is a 1-tuple such as ("0",). A rule or an equation is a pair
of terms. The rewrite system R must be a constructor system: the root of each
left side is a defined symbol, and its arguments are constructor terms.

Preconditions, as on the page: R is sufficiently complete (every ground term
f(c1, ..., cn) with f defined and ci ground constructor terms is reducible),
and its rules are oriented by the LPO for the precedence (this is checked).
A "disproved" answer also needs R to be ground confluent, which holds for
orthogonal constructor systems.

Matching, unification, rewriting and renaming use explicit stacks; the LPO
comparison is a memoized recursion of depth at most the sum of the depths.
"""

from dataclasses import dataclass, field
from itertools import count, product
from typing import Union

Term = Union[str, tuple]
Rule = tuple[Term, Term]


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


def symbols(t: Term) -> set[str]:
    out: set[str] = set()
    stack = [t]
    while stack:
        u = stack.pop()
        if not isinstance(u, str):
            out.add(u[0])
            stack.extend(u[1:])
    return out


def lpo_gt(s: Term, t: Term, prec: dict[str, int]) -> bool:
    """s >_lpo t, memoized on pairs of subterm occurrences: O(|s| |t| (|s| + |t|))."""
    memo: dict[tuple[int, int], bool] = {}

    def gt(s: Term, t: Term) -> bool:
        key = (id(s), id(t))
        if key in memo:
            return memo[key]
        if isinstance(t, str):
            r = not isinstance(s, str) and t in variables(s)
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
    """t sigma, for a sigma whose values are already fully applied. O(|t sigma|)."""
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
    """A sigma with p sigma = t, or None; the variables of t are treated as constants."""
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
            if a in variables(b):
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


def normal_form(t: Term, rules: list[Rule]) -> Term:
    """Rewrite at the first redex in preorder until none is left. Each step
    tries O(|t|) positions and all rules, with an O(|t|) match: O(|rules| |t|^2)."""
    while True:
        for p in positions(t):
            sub = subterm(t, p)
            for l, r in rules:
                sigma = match(l, sub)
                if sigma is not None:
                    t = replace(t, p, apply(r, sigma))
                    break
            else:
                continue
            break
        else:
            return t


def basic_position(t: Term, defined: set[str]) -> tuple[int, ...] | None:
    """The first position in preorder of a subterm f(c1, ..., cn) with f
    defined and every ci a constructor term, or None."""
    for p in positions(t):
        u = subterm(t, p)
        if u[0] in defined and not any(symbols(a) & defined for a in u[1:]):
            return p
    return None


_fresh = count()


def rename(rule: Rule) -> Rule:
    k = next(_fresh)
    names = {v: f"{v}_{k}" for v in variables(rule[0]) | variables(rule[1])}
    return apply(rule[0], names), apply(rule[1], names)


def ground_constructor_terms(constructors: dict[str, int], max_size: int) -> list[Term]:
    """All ground constructor terms with at most max_size symbols."""
    by: dict[int, list[Term]] = {}
    for n in range(1, max_size + 1):
        terms: list[Term] = []
        for c, k in constructors.items():
            if k == 0:
                if n == 1:
                    terms.append((c,))
                continue
            # split n - 1 symbols among k arguments
            def splits(total: int, parts: int):
                if parts == 1:
                    if total >= 1:
                        yield (total,)
                    return
                for first in range(1, total - parts + 2):
                    for rest in splits(total - first, parts - 1):
                        yield (first,) + rest
            for sizes in splits(n - 1, k):
                for args in product(*(by[s] for s in sizes)):
                    terms.append((c, *args))
        by[n] = terms
    return [t for n in by for t in by[n]]


@dataclass
class Result:
    """verdict is "proved", "disproved" or "unknown". For "disproved",
    witness is a ground equation, derived from the conjectures, whose sides
    are different constructor terms."""

    verdict: str
    hypotheses: list[Rule] = field(default_factory=list)
    steps: int = 0
    witness: Rule | None = None


def rewriting_induction(R: list[Rule], conjectures: list[Rule], constructors: dict[str, int],
                        prec: dict[str, int], max_steps: int = 200) -> Result:
    """Try to prove that every conjecture s = t holds for all ground instances,
    modulo R. Each step simplifies one equation with R and the hypotheses H,
    deletes it, or orients it into H and expands it at a basic subterm with
    every rule of R that unifies there. The cost of the run is not bounded in
    terms of the input; see the page for the cost of one step."""
    for l, r in R:
        if not lpo_gt(l, r, prec):
            raise ValueError(f"rule {l} -> {r} is not oriented by the LPO")
    defined = {l[0] for l, _ in R}
    E = list(conjectures)  # @line L1
    H: list[Rule] = []
    steps = 0
    while E:  # @line L2
        if steps == max_steps:  # @line L3
            return Result("unknown", H, steps)
        s, t = E.pop(0)  # @line L4
        steps += 1
        s, t = normal_form(s, R + H), normal_form(t, R + H)  # @line L5
        if s == t:  # @line L6
            continue
        if not (symbols(s) | symbols(t)) & defined:  # @line L7
            vs = sorted(variables(s) | variables(t))
            ground = ground_constructor_terms(constructors, 4)
            for vals in product(ground, repeat=len(vs)):
                theta = dict(zip(vs, vals))
                gs, gt_ = apply(s, theta), apply(t, theta)
                if gs != gt_:
                    return Result("disproved", H, steps, (gs, gt_))
            return Result("unknown", H, steps)
        if lpo_gt(t, s, prec):  # @line L8
            s, t = t, s
        p = basic_position(s, defined)
        if p is None or not lpo_gt(s, t, prec):  # @line L9
            return Result("unknown", H, steps)
        u = subterm(s, p)  # @line L10
        H.append((s, t))
        for rule in R:  # @line L11
            l, r = rename(rule)
            tau = unify(u, l)
            if tau is not None:
                E.append((apply(replace(s, p, r), tau), apply(t, tau)))
    return Result("proved", H, steps)  # @line L12
