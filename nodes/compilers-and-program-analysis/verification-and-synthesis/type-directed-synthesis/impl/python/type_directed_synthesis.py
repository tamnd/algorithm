# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/type-directed-synthesis/. The authors are listed in prov/3WFWA4.jsonl.
"""Type-directed synthesis of recursive functions on the toy lambda language.

The goal type is int -> int or int -> int -> int, and the specification is a
list of examples (args, out). The synthesizer works top-down by the type:

- At a function type it introduces fix f x -> fun y -> ..., so the body has
  the arguments in scope, and each example becomes a world: the values of
  the arguments and the wanted output.
- At int it first guesses an E-term (variables, 0, 1, + - * and a recursive
  call) that gives the wanted output in every world. E-terms are built
  bottom-up by size, one per distinct vector of values over the worlds.
- If no E-term fits, it refines: it splits the worlds by "x < 1" (the match
  of a natural number on zero and successor), or by a guessed bool E-term
  (< and == of int E-terms), and solves each part.

The recursive call is f (x - 1) a2 ... and is allowed only in the branch where
x < 1 is false. Its value in a world is read from the examples, so the
examples must be trace complete: every call that the wanted program makes on
an example input must be an example too. The outer loop deepens the size of
E-terms k and the number of nested splits d.
"""

from toylam import show  # noqa: F401  (re-exported for callers)

ARGS = ("x", "y", "z")


def var(n):
    return ("var", n)


def num(k):
    return ("int", k)


def rec_call(arity, rest):
    """The term f (x - 1) a2 ... an."""
    t = ("app", var("f"), ("prim", "-", var("x"), num(1)))
    for a in rest:
        t = ("app", t, a)
    return t


def guard():
    return ("prim", "<", var("x"), num(1))


def wrap(arity, body):
    """fix f x -> fun y -> ... -> body, a term of type int -> ... -> int."""
    for name in reversed(ARGS[1:arity]):
        body = ("lam", name, body)
    return ("fix", "f", "x", body)


def _bank(worlds, k, allow_rec, arity, table, memo):
    """The kept int and bool E-terms of size at most k, with their vectors."""
    key = (worlds, k, allow_rec)
    if key in memo:
        return memo[key]
    ints = {}   # size -> list of (term, vector)
    bools = []  # list of (term, vector)
    seen_i, seen_b = set(), set()

    def add_int(s, t, vec):
        if vec not in seen_i:  # observational equivalence over the worlds
            seen_i.add(vec)
            ints.setdefault(s, []).append((t, vec))

    for s in range(1, k + 1):
        if s == 1:
            for i in range(arity):
                add_int(1, var(ARGS[i]), tuple(w[i] for w in worlds))
            add_int(1, num(0), tuple(0 for _ in worlds))
            add_int(1, num(1), tuple(1 for _ in worlds))
        if allow_rec:
            for parts in _arg_tuples(ints, arity - 1, s - 2):
                vec = []
                for j, w in enumerate(worlds):
                    vals = (w[0] - 1,) + tuple(v[j] for _, v in parts)
                    vec.append(None if None in vals else table.get(vals))
                add_int(s, rec_call(arity, [t for t, _ in parts]), tuple(vec))
        for s1 in range(1, s - 1):
            for p, u in list(ints.get(s1, ())):
                for q, v in list(ints.get(s - 1 - s1, ())):
                    for op in ("+", "-", "*"):
                        vec = tuple(None if a is None or b is None else
                                    (a + b if op == "+" else a - b if op == "-" else a * b)
                                    for a, b in zip(u, v))
                        add_int(s, ("prim", op, p, q), vec)
                    for op in ("<", "=="):
                        vec = tuple(None if a is None or b is None else
                                    (a < b if op == "<" else a == b)
                                    for a, b in zip(u, v))
                        if None not in vec and vec not in seen_b:
                            seen_b.add(vec)
                            bools.append((("prim", op, p, q), vec))
    memo[key] = (ints, bools)
    return ints, bools


def _arg_tuples(ints, n, total):
    """All tuples of n kept int E-terms whose sizes add up to total."""
    if n == 0:
        if total == 0:
            yield ()
        return
    for s in range(1, total - n + 2):
        for t in list(ints.get(s, ())):
            for rest in _arg_tuples(ints, n - 1, total - s):
                yield (t,) + rest


def _refine(worlds, k, d, m, ctx):
    """A body of type int that fits all worlds, or None.

    worlds is a tuple of (args, out); m is "none" before the split on x < 1,
    "base" in its true branch and "step" in its false branch.
    """
    arity, table, memo = ctx
    args = tuple(a for a, _ in worlds)
    target = tuple(o for _, o in worlds)
    ints, bools = _bank(args, k, m == "step", arity, table, memo)
    for s in range(1, k + 1):  # @line L7
        for t, vec in ints.get(s, ()):
            if vec == target:
                return t  # @line L8
    if d == 0:  # @line L9
        return None
    if m == "none":  # @line L10
        w0 = tuple(w for w in worlds if w[0][0] < 1)
        w1 = tuple(w for w in worlds if w[0][0] >= 1)
        if w1:  # with no world in w0, any term fits the base branch
            e0 = _refine(w0, k, d - 1, "base", ctx)
            e1 = _refine(w1, k, d - 1, "step", ctx) if e0 is not None else None
            if e1 is not None:
                return ("if", guard(), e0, e1)  # @line L11
    for c, vec in bools:  # @line L12
        wt = tuple(w for w, b in zip(worlds, vec) if b)
        wf = tuple(w for w, b in zip(worlds, vec) if not b)
        if not wt or not wf:
            continue
        et = _refine(wt, k, d - 1, m, ctx)  # @line L13
        ef = _refine(wf, k, d - 1, m, ctx) if et is not None else None
        if ef is not None:
            return ("if", c, et, ef)  # @line L14
    return None  # @line L15


def synthesize(arity, examples, max_size=7, max_splits=2):
    """A term fix f x -> ... of type int -> ... -> int that meets the examples, or None.

    examples is a list of (args, out) with args a tuple of arity ints.
    """
    table = {tuple(a): o for a, o in examples}  # @line L1
    worlds = tuple((tuple(a), o) for a, o in examples)
    ctx = (arity, table, {})
    for k in range(1, max_size + 1):  # @line L2
        for d in range(0, max_splits + 1):  # @line L3
            body = _refine(worlds, k, d, "none", ctx)  # @line L4
            if body is not None:
                return wrap(arity, body)  # @line L5
    return None  # @line L6
