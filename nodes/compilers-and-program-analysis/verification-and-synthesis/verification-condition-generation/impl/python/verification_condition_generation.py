# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/verification-condition-generation/. The authors are listed in prov/7VA8XP.jsonl.
"""Verification condition generation for a small while language.

Expressions are tuples:
  ("int", c), ("bool", b), ("var", x),
  (op, a, b) for op in + - * < <= == and or =>,
  ("not", a), ("ite", c, a, b) and ("let", x, e, body).
Statements are tuples:
  ("skip",), ("assign", x, e), ("seq", s1, s2), ("if", b, s1, s2),
  ("while", b, inv, body), ("assert", p), ("assume", p).

vcgen(pre, stmt, post) returns the list of verification conditions of the
page: first pre => wp(stmt, post), then the side conditions of the loops.
Each is meant to hold in every state. compact_vc(pre, stmt, post) builds the
Flanagan-Saxe style VC of a loop-free statement: assignments become
single-assignment versions bound by let, joins become ite merges, and the
postcondition is named by a let at each join, so its size is polynomial.

There is no SMT solver here. valid_on_box checks a formula in every state of
a box of integers. This is a bounded check, not a proof of validity.
"""

import itertools

_ARITH = {"+": lambda a, b: a + b, "-": lambda a, b: a - b, "*": lambda a, b: a * b}
_CMP = {"<": lambda a, b: a < b, "<=": lambda a, b: a <= b, "==": lambda a, b: a == b}
_BOOL = ("and", "or", "=>")

TRUE = ("bool", True)


def evaluate(e: tuple, env: dict):
    """The value of e in the state env (a dict from names to ints). Cost:
    O(size of e), where a let counts its bound expression once."""
    tag = e[0]
    if tag == "int" or tag == "bool":
        return e[1]
    if tag == "var":
        return env[e[1]]
    if tag in _ARITH:
        return _ARITH[tag](evaluate(e[1], env), evaluate(e[2], env))
    if tag in _CMP:
        return _CMP[tag](evaluate(e[1], env), evaluate(e[2], env))
    if tag == "and":
        return evaluate(e[1], env) and evaluate(e[2], env)
    if tag == "or":
        return evaluate(e[1], env) or evaluate(e[2], env)
    if tag == "=>":
        return (not evaluate(e[1], env)) or evaluate(e[2], env)
    if tag == "not":
        return not evaluate(e[1], env)
    if tag == "ite":
        return evaluate(e[2], env) if evaluate(e[1], env) else evaluate(e[3], env)
    if tag == "let":
        inner = dict(env)
        inner[e[1]] = evaluate(e[2], env)
        return evaluate(e[3], inner)
    raise ValueError("unknown expression %r" % (tag,))


def subst(e: tuple, x: str, r: tuple) -> tuple:
    """e with every free occurrence of the variable x replaced by r. The
    bound names of let are fresh in this module, so no capture occurs.
    Cost: O(size of the result)."""
    tag = e[0]
    if tag == "var":
        return r if e[1] == x else e
    if tag == "int" or tag == "bool":
        return e
    if tag == "let":
        body = e[3] if e[1] == x else subst(e[3], x, r)
        return ("let", e[1], subst(e[2], x, r), body)
    return (tag,) + tuple(subst(a, x, r) for a in e[1:])


def size(e: tuple) -> int:
    """The number of nodes of e as a tree. Cost: O(size of e)."""
    if e[0] in ("int", "bool", "var"):
        return 1
    return 1 + sum(size(a) for a in e[1:] if isinstance(a, tuple))


def dag_size(e: tuple) -> int:
    """The number of distinct subterms of e, the size of e as a DAG with
    shared subterms. Cost: O(size of e) set operations."""
    seen = set()
    stack = [e]
    while stack:
        t = stack.pop()
        if t in seen:
            continue
        seen.add(t)
        if t[0] not in ("int", "bool", "var"):
            stack.extend(a for a in t[1:] if isinstance(a, tuple))
    return len(seen)


def wp(s: tuple, q: tuple, side: list) -> tuple:
    """The weakest precondition of s for q, with each loop replaced by its
    invariant. The side conditions of the loops are appended to side.
    Cost: O(size of the result), which can be exponential in the size of s."""
    tag = s[0]  # @line L3
    if tag == "skip":
        return q  # @line L4
    if tag == "assign":
        return subst(q, s[1], s[2])  # @line L5
    if tag == "assert":
        return ("and", s[1], q)  # @line L6
    if tag == "assume":
        return ("=>", s[1], q)  # @line L7
    if tag == "seq":
        return wp(s[1], wp(s[2], q, side), side)  # @line L8
    if tag == "if":
        b = s[1]  # @line L9
        return ("and", ("=>", b, wp(s[2], q, side)), ("=>", ("not", b), wp(s[3], q, side)))
    if tag == "while":
        b, inv, body = s[1], s[2], s[3]  # @line L10
        side.append(("=>", ("and", inv, b), wp(body, inv, side)))  # @line L11
        side.append(("=>", ("and", inv, ("not", b)), q))  # @line L12
        return inv  # @line L13
    raise ValueError("unknown statement %r" % (tag,))


def vcgen(pre: tuple, s: tuple, post: tuple) -> list:
    """The verification conditions of {pre} s {post}: the main condition
    pre => wp(s, post), then the side conditions of every loop. If all of
    them hold in every state, every run of s from a state of pre that stops
    passes its asserts and ends in post (partial correctness)."""
    side = []  # @line L1
    main = ("=>", pre, wp(s, post, side))  # @line L2
    return [main] + side


def valid_on_box(f: tuple, names, lo: int, hi: int):
    """Check f in every state that maps names into [lo, hi]. Return None if
    f holds in all of them, or the first state where it fails. This is a
    bounded check, not a proof. Cost: (hi - lo + 1)^len(names) evaluations."""
    names = list(names)
    for vals in itertools.product(range(lo, hi + 1), repeat=len(names)):
        env = dict(zip(names, vals))
        if not evaluate(f, env):
            return env
    return None


def run(s: tuple, env: dict, fuel: int = 10000, heads=None):
    """Execute s from the state env. Return ("ok", final state),
    ("fail", None) when an assert is false, ("blocked", None) when an assume
    is false, or ("out", None) when fuel runs out. Each loop test uses one
    unit of fuel. If heads is a list, every state at a loop head is
    appended to it."""
    env = dict(env)
    budget = [fuel]

    def go(t):
        tag = t[0]
        if tag == "skip":
            return "ok"
        if tag == "assign":
            env[t[1]] = evaluate(t[2], env)
            return "ok"
        if tag == "assert":
            return "ok" if evaluate(t[1], env) else "fail"
        if tag == "assume":
            return "ok" if evaluate(t[1], env) else "blocked"
        if tag == "seq":
            r = go(t[1])
            return go(t[2]) if r == "ok" else r
        if tag == "if":
            return go(t[2]) if evaluate(t[1], env) else go(t[3])
        if tag == "while":
            while True:
                if budget[0] <= 0:
                    return "out"
                budget[0] -= 1
                if heads is not None:
                    heads.append(dict(env))
                if not evaluate(t[1], env):
                    return "ok"
                r = go(t[3])
                if r != "ok":
                    return r
        raise ValueError("unknown statement %r" % (tag,))

    r = go(s)
    return (r, dict(env) if r == "ok" else None)


def assigned(s: tuple) -> set:
    """The variables that s assigns."""
    tag = s[0]
    if tag == "assign":
        return {s[1]}
    if tag == "seq" or tag == "if":
        return assigned(s[-2]) | assigned(s[-1])
    if tag == "while":
        return assigned(s[3])
    return set()


def compact_vc(pre: tuple, s: tuple, post: tuple) -> tuple:
    """A VC of {pre} s {post} for a loop-free s, equal to pre => wp(s, post)
    in every state. It is built in two passes, after Flanagan and Saxe.

    Pass 1 makes s passive. Each assignment x := e gets a fresh version x#k
    defined by e over the current versions. At a join, each variable whose
    versions differ gets a version defined by ite(g, left, right), where g
    names the branch condition. The definitions become nested lets.
    Pass 2 computes wp of the passive statement, which needs no substitution,
    and names the postcondition with a let at each join. The result has
    size O(|s| + |pre| + |post| + m), where m is the number of merged
    versions, at most the number of variables times the number of ifs."""
    counter = itertools.count(1)
    defs = []

    def rename(e, sigma):
        for x, v in sigma.items():
            if v != x:
                e = subst(e, x, ("var", v))
        return e

    def passify(t, sigma):
        tag = t[0]
        if tag == "skip":
            return ("skip",), sigma
        if tag == "assign":
            v = "%s#%d" % (t[1], next(counter))
            defs.append((v, rename(t[2], sigma)))
            out = dict(sigma)
            out[t[1]] = v
            return ("skip",), out
        if tag == "assert" or tag == "assume":
            return (tag, rename(t[1], sigma)), sigma
        if tag == "seq":
            a, s1 = passify(t[1], sigma)
            b, s2 = passify(t[2], s1)
            return ("seq", a, b), s2
        if tag == "if":
            g = "g#%d" % next(counter)
            defs.append((g, rename(t[1], sigma)))
            a, sa = passify(t[2], sigma)
            b, sb = passify(t[3], sigma)
            out = dict(sigma)
            for x in sorted(sigma):
                if sa[x] != sb[x]:
                    v = "%s#%d" % (x, next(counter))
                    defs.append((v, ("ite", ("var", g), ("var", sa[x]), ("var", sb[x]))))
                    out[x] = v
            left = ("seq", ("assume", ("var", g)), a)
            right = ("seq", ("assume", ("not", ("var", g))), b)
            return ("choice", left, right), out
        raise ValueError("compact_vc needs a loop-free statement, got %r" % (tag,))

    def pwp(t, q):
        tag = t[0]
        if tag == "skip":
            return q
        if tag == "assert":
            return ("and", t[1], q)
        if tag == "assume":
            return ("=>", t[1], q)
        if tag == "seq":
            return pwp(t[1], pwp(t[2], q))
        if tag == "choice":
            if q[0] in ("var", "bool"):
                return ("and", pwp(t[1], q), pwp(t[2], q))
            n = "q#%d" % next(counter)
            name = ("var", n)
            return ("let", n, q, ("and", pwp(t[1], name), pwp(t[2], name)))
        raise ValueError(tag)

    names = _free_vars(pre) | _free_vars(post) | _stmt_vars(s)
    sigma0 = {x: x for x in names}
    passive, sigma = passify(s, sigma0)
    f = ("=>", pre, pwp(passive, rename(post, sigma)))
    for v, e in reversed(defs):
        f = ("let", v, e, f)
    return f


def _free_vars(e: tuple) -> set:
    tag = e[0]
    if tag == "var":
        return {e[1]}
    if tag in ("int", "bool"):
        return set()
    if tag == "let":
        return _free_vars(e[2]) | (_free_vars(e[3]) - {e[1]})
    out = set()
    for a in e[1:]:
        out |= _free_vars(a)
    return out


def _stmt_vars(s: tuple) -> set:
    tag = s[0]
    if tag == "assign":
        return {s[1]} | _free_vars(s[2])
    if tag in ("assert", "assume"):
        return _free_vars(s[1])
    if tag == "seq":
        return _stmt_vars(s[1]) | _stmt_vars(s[2])
    if tag == "if":
        return _free_vars(s[1]) | _stmt_vars(s[2]) | _stmt_vars(s[3])
    if tag == "while":
        return _free_vars(s[1]) | _free_vars(s[2]) | _stmt_vars(s[3])
    return set()
