# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/faceted-execution/. The authors are listed in prov/5EDZCZ.jsonl.

"""Faceted execution of a small while language with two levels, L and H.

Programs are nested tuples:

    expression: an int (a constant), a str (a variable), or (op, e1, e2)
                with op one of "+", "-", "*", "<", "=="
    command:    ("skip",)
                ("assign", x, e)
                ("seq", c1, c2)
                ("if", e, c1, c2)
                ("while", e, c)

Values are integers modulo MOD. A nonzero value is true. A faceted value
<V_H : V_L> is the pair Facet(high, low): an observer at H sees V_H and an
observer at L sees V_L. A plain int is a value that both observers see.
The program counter is None (no secret branch), "H" (a branch only the H
view takes) or "L" (a branch only the L view takes).
"""

from typing import NamedTuple, Optional, Union

Expr = Union[int, str, tuple]
Cmd = tuple

MOD = 256


class Facet(NamedTuple):
    high: int
    low: int


Value = Union[int, Facet]
FStore = dict[str, Value]


def make(high: int, low: int) -> Value:
    """Return <high : low>, or the plain int when the two views agree. Cost: O(1)."""
    return high if high == low else Facet(high, low)


def view(v: Value, side: str) -> int:
    """Return what the observer at side ("H" or "L") sees of v. Cost: O(1)."""
    if isinstance(v, Facet):
        return v.high if side == "H" else v.low
    return v


def project(store: FStore, side: str) -> dict[str, int]:
    """Return the plain store that the observer at side sees. Cost: O(size of store)."""
    return {x: view(v, side) for x, v in store.items()}


def _plain_eval(e: Expr, store: FStore, side: str) -> int:
    values: list[int] = []
    work: list[tuple[bool, Expr]] = [(False, e)]
    while work:
        done, f = work.pop()
        if done:
            b = values.pop()
            a = values.pop()
            op = f[0]
            if op == "+":
                values.append((a + b) % MOD)
            elif op == "-":
                values.append((a - b) % MOD)
            elif op == "*":
                values.append((a * b) % MOD)
            elif op == "<":
                values.append(int(a < b))
            elif op == "==":
                values.append(int(a == b))
            else:
                raise ValueError(f"unknown operator {op!r}")
        elif isinstance(f, int):
            values.append(f % MOD)
        elif isinstance(f, str):
            values.append(view(store[f], side))
        else:
            work.append((True, f))
            work.append((False, f[2]))
            work.append((False, f[1]))
    return values[0]


def evaluate(e: Expr, store: FStore) -> Value:
    """Return the faceted value of e: its value in each view, joined by make.

    Precondition: every variable of e is a key of store.
    Cost: O(size of e). Uses an explicit stack, no recursion.
    """
    return make(_plain_eval(e, store, "H"), _plain_eval(e, store, "L"))


def initial_store(s: dict[str, int], high: set[str], default: int = 0) -> FStore:
    """Give each variable in high the value <s(x) : default>. Cost: O(size of s)."""
    return {x: (make(v % MOD, default % MOD) if x in high else v % MOD) for x, v in s.items()}


def faceted_run(c: Cmd, store: FStore, fuel: int = 10_000) -> Optional[FStore]:
    """Run c once on a faceted store. Return the final store, or None after fuel steps.

    A branch on a value whose two views differ runs the taken arm of each
    view under the program counter of that view. An assignment under pc
    "H" changes only the H view of the target, and under "L" only the L
    view.
    Precondition: every variable of c is a key of store.
    Cost: at most fuel steps; a step costs O(1) plus two plain evaluations
    of its expression. The run takes at most the steps of the H view plus
    the steps of the L view.
    """
    sigma = dict(store)
    stack: list[tuple[Cmd, Optional[str]]] = [(c, None)]  # @line L1
    while stack:  # @line L2
        fuel -= 1
        if fuel < 0:
            return None
        d, pc = stack.pop()  # @line L3
        tag = d[0]
        if tag == "skip":
            continue
        if tag == "assign":  # @line L4
            v = evaluate(d[2], sigma)
            old = sigma[d[1]]
            if pc is None:
                sigma[d[1]] = v  # @line L5
            elif pc == "H":
                sigma[d[1]] = make(view(v, "H"), view(old, "L"))  # @line L6
            else:
                sigma[d[1]] = make(view(old, "H"), view(v, "L"))  # @line L7
        elif tag == "seq":  # @line L8
            stack.append((d[2], pc))
            stack.append((d[1], pc))
        elif tag in ("if", "while"):  # @line L9
            v = evaluate(d[1], sigma)
            th, tl = view(v, "H") != 0, view(v, "L") != 0
            if pc is None and th != tl:  # @line L10
                arms = [("L", tl), ("H", th)]  # @line L11
            else:
                arms = [(pc, tl if pc == "L" else th)]  # @line L12
            for p, taken in arms:
                if tag == "if":  # @line L13
                    stack.append((d[2] if taken else d[3], p))
                elif taken:  # @line L14
                    stack.append((d, p))
                    stack.append((d[2], p))
        else:
            raise ValueError(f"unknown command {tag!r}")
    return sigma  # @line L15
