# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/strictness-analysis/. The authors are listed in prov/GYNYB7.jsonl.
"""Mycroft's strictness analysis on the first-order fragment of toylam.py.

The input is one function, written as a toylam term:

    ("fix", f, x1, ("lam", x2, ... ("lam", xk, body)))   a recursive function
    ("lam", x1, ... ("lam", xk, body))                   a function with no recursion

The body may use the parameters, int and bool constants, the operators of
toylam, if, let, and full calls f e1 ... ek of the function itself. It may not
contain lambdas, fix terms or partial calls. The parameters are passed lazily
(call by name or call by need): an argument is only computed when it is used.

The abstract value 0 means "surely undefined" (the computation loops or fails)
and 1 means "may be defined". The analysis computes the least fixed point of
the abstract function f# : {0,1}^k -> {0,1} by Kleene iteration on its table,
and says f is strict in x_i when f#(1, ..., 1, 0, 1, ..., 1) = 0, with the 0
in place i. Then f e1 ... ek is undefined whenever e_i is undefined, so e_i
can be computed before the call.

Cost: with n the size of the body, at most 2^k + 1 rounds of 2^k evaluations
of the body, each O(n) time, so O((2^k + 1) 2^k n) time and O(2^k + n) space.
No function recurses on the term: the body is compiled once to postfix code.
"""

from itertools import product

CONST, VAR, AND, IF, BIND, UNBIND, CALL = range(7)


class FirstOrderFunction:
    """A parsed function: its name (None if not recursive), parameters and postfix code."""

    def __init__(self, name: str | None, params: list[str], code: list[tuple]):
        self.name = name
        self.params = params
        self.code = code


def parse_function(term: tuple) -> FirstOrderFunction:
    """Check that term is in the first-order fragment and compile its body.

    Raises ValueError otherwise. O(n) time, iterative.
    """
    if term[0] == "fix":
        name, params, body = term[1], [term[2]], term[3]
    elif term[0] == "lam":
        name, params, body = None, [term[1]], term[2]
    else:
        raise ValueError("a function must be a fix or a lam term")
    while body[0] == "lam":
        params.append(body[1])
        body = body[2]
    if len(set(params)) != len(params) or name in params:
        raise ValueError("the parameters and the name must be distinct")
    k = len(params)
    scope = {x: 1 for x in params}
    code: list[tuple] = []
    todo: list[tuple] = [("visit", body)]
    while todo:
        kind, item = todo.pop()
        if kind == "emit":
            code.append(item)
            if item[0] == UNBIND:
                scope[item[1]] -= 1
            continue
        if kind == "enter":
            scope[item] = scope.get(item, 0) + 1
            continue
        e = item
        tag = e[0]
        if tag in ("int", "bool"):
            code.append((CONST,))
        elif tag == "var":
            if scope.get(e[1], 0) == 0:
                raise ValueError(f"free or higher-order use of {e[1]!r}")
            code.append((VAR, e[1]))
        elif tag == "prim":
            todo += [("emit", (AND,)), ("visit", e[3]), ("visit", e[2])]
        elif tag == "if":
            todo += [("emit", (IF,)), ("visit", e[3]), ("visit", e[2]), ("visit", e[1])]
        elif tag == "let":
            if e[1] == name:
                raise ValueError("a let may not hide the function name")
            todo += [("emit", (UNBIND, e[1])), ("visit", e[3]), ("enter", e[1]),
                     ("emit", (BIND, e[1])), ("visit", e[2])]
        elif tag == "app":
            args = []
            head = e
            while head[0] == "app":
                args.append(head[2])
                head = head[1]
            if head != ("var", name) or name is None or len(args) != k:
                raise ValueError("only full calls of the function itself are allowed")
            todo.append(("emit", (CALL, k)))
            todo += [("visit", a) for a in args]  # args is reversed, so the first runs first
        else:
            raise ValueError(f"{tag} is not in the first-order fragment")
    return FirstOrderFunction(name, params, code)


def abstract_eval(fn: FirstOrderFunction, point: tuple[int, ...], table: dict) -> int:
    """ABS(body, {x_i -> point_i}, table): the abstract value of the body, O(n) time."""
    env = dict(zip(fn.params, point))
    stack: list[int] = []
    saved: list[int | None] = []
    for op in fn.code:
        t = op[0]
        if t == CONST:
            stack.append(1)  # @line L9
        elif t == VAR:
            stack.append(env[op[1]])  # @line L10
        elif t == AND:
            b = stack.pop()
            stack.append(stack.pop() & b)  # @line L11
        elif t == IF:
            e3 = stack.pop()
            e2 = stack.pop()
            stack.append(stack.pop() & (e2 | e3))  # @line L12
        elif t == BIND:
            saved.append(env.get(op[1]))  # @line L13
            env[op[1]] = stack.pop()  # @line L13
        elif t == UNBIND:
            old = saved.pop()
            if old is None:
                del env[op[1]]
            else:
                env[op[1]] = old
        else:
            k = op[1]
            args = tuple(stack[len(stack) - k:])
            del stack[len(stack) - k:]
            stack.append(table[args])  # @line L14
    return stack.pop()


def kleene_step(fn: FirstOrderFunction, table: dict) -> dict:
    """One round: the table F(T) with F(T)[v] = ABS(body, v, T)."""
    return {v: abstract_eval(fn, v, table) for v in table}  # @line L3


def analyse(term: tuple) -> tuple[dict, list[bool], int]:
    """Return (table of the least fixed point f#, strict flags per parameter, rounds)."""
    fn = parse_function(term)
    k = len(fn.params)
    table = {v: 0 for v in product((0, 1), repeat=k)}  # @line L1
    rounds = 0
    while True:  # @line L2
        new = kleene_step(fn, table)  # @line L3
        rounds += 1
        stable = new == table  # @line L4
        table = new  # @line L5
        if stable:  # @line L6
            break
    strict = []
    for i in range(k):  # @line L7
        probe = tuple(0 if j == i else 1 for j in range(k))
        strict.append(table[probe] == 0)  # @line L7
    return table, strict, rounds  # @line L8
