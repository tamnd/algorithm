# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/houdini-algorithm/. The authors are listed in prov/8FP30Z.jsonl.
"""The Houdini algorithm on a single loop of a small while language.

Expressions are tuples: ("int", c), ("var", x), (op, a, b) for op in
+ - * < <= == != and or, ("not", a) and ("ite", c, a, b).

A Loop has a list of variable names, a precondition init, a guard and a
body. The body is a list of assignments (x, e) run in order, so it is
deterministic; use ite for a branch.

houdini(candidates, prove) is the algorithm. prove(h) gets a tuple of
candidate indices and returns None when the conjunction of those candidates
is inductive, or a counterexample: ("init", s), a state of the
precondition that falsifies the conjunction, or ("step", s, t), a state s
that satisfies the conjunction and the guard and whose successor t does not.

box_prover(loop, candidates, lo, hi) is the prover of the page. It has no
SMT solver: it tries every state of the box [lo, hi]^k in a fixed order and
returns the first counterexample. "Inductive" then means inductive on the
box, a bounded check, not a proof.
"""

import itertools

_OPS = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "<": lambda a, b: a < b,
    "<=": lambda a, b: a <= b,
    "==": lambda a, b: a == b,
    "!=": lambda a, b: a != b,
}


def evaluate(e: tuple, env: dict):
    """The value of e in the state env. Cost: O(size of e)."""
    tag = e[0]
    if tag == "int":
        return e[1]
    if tag == "var":
        return env[e[1]]
    if tag in _OPS:
        return _OPS[tag](evaluate(e[1], env), evaluate(e[2], env))
    if tag == "and":
        return evaluate(e[1], env) and evaluate(e[2], env)
    if tag == "or":
        return evaluate(e[1], env) or evaluate(e[2], env)
    if tag == "not":
        return not evaluate(e[1], env)
    if tag == "ite":
        return evaluate(e[2], env) if evaluate(e[1], env) else evaluate(e[3], env)
    raise ValueError("unknown expression %r" % (tag,))


class Loop:
    """while guard do body, entered from the states of init."""

    __slots__ = ("names", "init", "guard", "body")

    def __init__(self, names, init, guard, body):
        self.names = list(names)
        self.init = init
        self.guard = guard
        self.body = list(body)

    def step(self, s: dict) -> dict:
        """The state after one turn of the body from s."""
        t = dict(s)
        for x, e in self.body:
            t[x] = evaluate(e, t)
        return t


def houdini(candidates, prove):
    """Return (h, calls): h is the tuple of indices of the largest subset of
    candidates whose conjunction prove accepts, calls is the number of calls
    to prove. Precondition: prove answers for a fixed notion of
    "inductive" that is closed under union of candidate sets, and each
    counterexample it returns is genuine. Cost: at most c + 1 calls to
    prove, where c = len(candidates), and O(c) evaluations per call."""
    h = list(range(len(candidates)))  # @line L1
    calls = 0
    while True:  # @line L2
        calls += 1
        cex = prove(tuple(h))  # @line L3
        if cex is None:
            return tuple(h), calls  # @line L4
        if cex[0] == "init":
            s = cex[1]  # @line L5
            h = [i for i in h if evaluate(candidates[i], s)]
        else:
            t = cex[2]  # @line L6
            h = [i for i in h if evaluate(candidates[i], t)]


def box_states(names, lo: int, hi: int):
    """Every state of the box [lo, hi]^k, in lexicographic order."""
    for vals in itertools.product(range(lo, hi + 1), repeat=len(names)):
        yield dict(zip(names, vals))


def box_prover(loop: Loop, candidates, lo: int, hi: int):
    """A prover for houdini that checks initiation and consecution in every
    state of the box and returns the first counterexample. Each call costs
    O((hi - lo + 1)^k) evaluations of the candidates. It also counts its
    calls in the attribute calls."""
    states = list(box_states(loop.names, lo, hi))

    def holds(h, s):
        return all(evaluate(candidates[i], s) for i in h)

    def prove(h):
        prove.calls += 1
        for s in states:
            if evaluate(loop.init, s) and not holds(h, s):
                return ("init", s)
        for s in states:
            if holds(h, s) and evaluate(loop.guard, s):
                t = loop.step(s)
                if not holds(h, t):
                    return ("step", s, t)
        return None

    prove.calls = 0
    return prove


def inductive_on_box(loop: Loop, candidates, h, lo: int, hi: int) -> bool:
    """Whether the conjunction of the candidates in h is inductive on the box:
    every state of the box in init satisfies it, and every state of the box
    that satisfies it and the guard has a successor that satisfies it."""
    return box_prover(loop, candidates, lo, hi)(tuple(h)) is None
