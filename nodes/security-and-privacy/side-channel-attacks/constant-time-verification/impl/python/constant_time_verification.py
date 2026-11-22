# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/constant-time-verification/. The authors are listed in prov/B355TH.jsonl.

"""Constant-time verification by a product program, on a toy language.

The toy language works on the integers mod w. It has no real memory, no
real cache and no clock. A run gives a leakage trace of abstract events:

    ("br", b)        the decision b of a branch
    ("loop", n)      the iteration count n of a loop
    ("addr", a, i)   an access to cell i of the array a
    ("div", x, y)    the two operands of a division

Expressions are tuples:

    ("c", n)               the constant n mod w
    ("v", x)               the variable x (a variable that was not set is 0)
    ("ld", a, e)           the cell e of the array a
    ("div", e1, e2)        e1 div e2, and 0 when e2 is 0
    (op, e1, e2)           op is one of + - * & | ^ < ==

Statements are tuples, and a block is a list of statements:

    ("set", x, e)          x <- e
    ("st", a, i, e)        a[i] <- e
    ("if", c, b1, b2)      if c != 0 then b1 else b2
    ("rep", e, b)          repeat the block b e times
    ("assert", e)          only in product programs: e must not be 0

Every array has w cells, so every index is a valid cell, every program is
total and every run stops. The shadow copy of a variable or array x is
named x + "'".
"""

from collections.abc import Mapping, Sequence
from itertools import product as cartesian

Expr = tuple
Stmt = tuple
Block = list
Event = tuple

OPS = ("+", "-", "*", "&", "|", "^", "<", "==")


class AssertFailed(Exception):
    """An assert of a product program is false."""


def _binop(op: str, a: int, b: int, w: int) -> int:
    if op == "+":
        return (a + b) % w
    if op == "-":
        return (a - b) % w
    if op == "*":
        return (a * b) % w
    if op == "&":
        return (a & b) % w
    if op == "|":
        return (a | b) % w
    if op == "^":
        return (a ^ b) % w
    if op == "<":
        return 1 if a < b else 0
    if op == "==":
        return 1 if a == b else 0
    raise ValueError(f"unknown operator {op!r}")


def _eval(e: Expr, env: dict[str, int], arrs: dict[str, list[int]], w: int, trace: list[Event] | None) -> int:
    tag = e[0]
    if tag == "c":
        return e[1] % w
    if tag == "v":
        return env.get(e[1], 0)
    if tag == "ld":
        i = _eval(e[2], env, arrs, w, trace)
        if trace is not None:
            trace.append(("addr", e[1], i))
        return arrs[e[1]][i]
    a = _eval(e[1], env, arrs, w, trace)
    b = _eval(e[2], env, arrs, w, trace)
    if tag == "div":
        if trace is not None:
            trace.append(("div", a, b))
        return a // b if b else 0
    return _binop(tag, a, b, w)


def _exec(block: Block, env: dict[str, int], arrs: dict[str, list[int]], w: int, trace: list[Event] | None) -> None:
    for s in block:
        tag = s[0]
        if tag == "set":
            env[s[1]] = _eval(s[2], env, arrs, w, trace)
        elif tag == "st":
            i = _eval(s[2], env, arrs, w, trace)
            v = _eval(s[3], env, arrs, w, trace)
            if trace is not None:
                trace.append(("addr", s[1], i))
            arrs[s[1]][i] = v
        elif tag == "if":
            c = _eval(s[1], env, arrs, w, trace) != 0
            if trace is not None:
                trace.append(("br", c))
            _exec(s[2] if c else s[3], env, arrs, w, trace)
        elif tag == "rep":
            n = _eval(s[1], env, arrs, w, trace)
            if trace is not None:
                trace.append(("loop", n))
            for _ in range(n):
                _exec(s[2], env, arrs, w, trace)
        elif tag == "assert":
            if _eval(s[1], env, arrs, w, None) == 0:
                raise AssertFailed
        else:
            raise ValueError(f"unknown statement {tag!r}")


def run(prog: Block, inputs: Mapping[str, int], tables: Mapping[str, Sequence[int]], w: int = 4) -> tuple[dict[str, int], list[Event]]:
    """Run prog once and return the final variables and the leakage trace.

    Precondition: w >= 2, each input is in range(w), and each table has w
    cells with values in range(w). Cost: O(t) for a run of t steps.
    """
    env = dict(inputs)
    arrs = {a: list(t) for a, t in tables.items()}
    trace: list[Event] = []
    _exec(prog, env, arrs, w, trace)
    return env, trace


def _sh(e: Expr) -> Expr:
    """The shadow copy e' of the expression e."""
    tag = e[0]
    if tag == "c":
        return e
    if tag == "v":
        return ("v", e[1] + "'")
    if tag == "ld":
        return ("ld", e[1] + "'", _sh(e[2]))
    return (tag, _sh(e[1]), _sh(e[2]))


def _leak_terms(e: Expr) -> list[Expr]:
    """The subexpressions of e whose values the evaluation of e leaks."""
    tag = e[0]
    if tag in ("c", "v"):
        return []
    if tag == "ld":
        return _leak_terms(e[2]) + [e[2]]
    terms = _leak_terms(e[1]) + _leak_terms(e[2])
    if tag == "div":
        terms += [e[1], e[2]]
    return terms


def _guard(terms: list[Expr]) -> Expr:
    """The conjunction of l == l' over the terms l."""
    g: Expr = ("c", 1)
    for t in terms:  # @line L13
        g = ("&", g, ("==", t, _sh(t)))
    return g


def product(prog: Block) -> Block:
    """The output-insensitive product of prog with its shadow copy.

    Each statement is preceded by an assert that its leakage is the same in
    both copies. The product keeps the control structure of prog: it has one
    branch for each branch of prog and one loop for each loop of prog.
    Cost: O(n^2) time and size for a program of size n, and O(n) when the
    nesting depth of the expressions is bounded.
    """
    out: Block = []
    for s in prog:  # @line L12
        tag = s[0]
        if tag == "set":  # @line L7
            g = _guard(_leak_terms(s[2]))
            out += [("assert", g), s, ("set", s[1] + "'", _sh(s[2]))]
        elif tag == "st":  # @line L8
            g = _guard(_leak_terms(s[2]) + _leak_terms(s[3]) + [s[2]])
            out += [("assert", g), s, ("st", s[1] + "'", _sh(s[2]), _sh(s[3]))]
        elif tag == "if":  # @line L9
            c = s[1]
            same = ("==", ("==", c, ("c", 0)), ("==", _sh(c), ("c", 0)))
            g = ("&", _guard(_leak_terms(c)), same)  # @line L10
            out += [("assert", g), ("if", c, product(s[2]), product(s[3]))]
        elif tag == "rep":  # @line L11
            g = _guard(_leak_terms(s[1]) + [s[1]])
            out += [("assert", g), ("rep", s[1], product(s[2]))]
        else:
            raise ValueError(f"unknown statement {tag!r}")
    return out


def ct_verif(prog: Block, public: Sequence[str], secret: Sequence[str], tables: Mapping[str, Sequence[int]], w: int = 4) -> tuple[bool, tuple[dict[str, int], dict[str, int]] | None]:
    """Decide whether prog is constant time, with a witness pair if it is not.

    prog is constant time when any two runs whose public inputs are equal give
    the same leakage trace. The tables are public and equal in both runs.
    The check runs the product once for each start pair over range(w).

    Precondition: w >= 2, the names in public and secret are distinct, each
    table has w cells with values in range(w), and no name ends with "'".
    Cost: O(n^2) to build the product, then O(t) for each of the
    m = w^(p + 2s) start pairs, for p public and s secret inputs, where t is
    the number of steps of one run of the product.
    """
    if w < 2:
        raise ValueError("w must be at least 2")
    for t in tables.values():
        if len(t) != w:
            raise ValueError("each table must have w cells")
    q = product(prog)  # @line L1
    space = list(cartesian(range(w), repeat=len(secret)))
    for pv in cartesian(range(w), repeat=len(public)):  # @line L2
        for sv in space:
            for sv2 in space:
                a = dict(zip(public, pv)) | dict(zip(secret, sv))
                b = dict(zip(public, pv)) | dict(zip(secret, sv2))
                env = a | {x + "'": v for x, v in b.items()}
                arrs = {n: list(t) for n, t in tables.items()}
                arrs |= {n + "'": list(t) for n, t in tables.items()}
                try:
                    _exec(q, env, arrs, w, None)  # @line L3
                except AssertFailed:  # @line L4
                    return False, (a, b)  # @line L5
    return True, None  # @line L6


def cache_cost(trace: Sequence[Event], base: Mapping[str, int], sets: int = 2, ways: int = 1, line: int = 2, hit: int = 1, miss: int = 10) -> int:
    """The cost of the array accesses of a trace in an abstract LRU cache.

    The cache starts empty. It has the given number of sets and ways, and
    lines of line cells. Cell i of array a has the address base[a] + i, which
    goes to the set (address div line) mod sets. A hit costs hit units and a
    miss costs miss units. Other events cost nothing. The cost is a function
    of the sequence of addresses alone. Precondition: sets, ways and line are
    at least 1. Cost: O(k * ways) for k events.
    """
    content: list[list[int]] = [[] for _ in range(sets)]
    total = 0
    for ev in trace:
        if ev[0] != "addr":
            continue
        tag = (base[ev[1]] + ev[2]) // line
        lines = content[tag % sets]
        if tag in lines:
            total += hit
            lines.remove(tag)
        else:
            total += miss
            if len(lines) == ways:
                lines.pop(0)
        lines.append(tag)
    return total
