# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/secure-multi-execution/. The authors are listed in prov/5EGZEC.jsonl.

"""Secure multi-execution (SME) of a small while language.

Programs are nested tuples:

    expression: an int (a constant), a str (a variable), or (op, e1, e2)
                with op one of "+", "-", "*", "<", "=="
    command:    ("skip",)
                ("assign", x, e)
                ("seq", c1, c2)
                ("if", e, c1, c2)
                ("while", e, c)

Values are integers modulo MOD. A nonzero value is true. A level is a
frozenset of category names, ordered by inclusion. The inputs of a run
are the initial values of the variables, and the outputs are the final
values; the output on a variable x is visible at level gamma[x].
"""

from typing import Optional, Union

Level = frozenset
Expr = Union[int, str, tuple]
Cmd = tuple
Store = dict[str, int]

MOD = 256


def evaluate(e: Expr, s: Store) -> int:
    """Return the value of e in the store s.

    Precondition: every variable of e is a key of s.
    Cost: O(size of e). Uses an explicit stack, no recursion.
    """
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
            values.append(s[f])
        else:
            work.append((True, f))
            work.append((False, f[2]))
            work.append((False, f[1]))
    return values[0]


def run(c: Cmd, s: Store, fuel: int = 10_000) -> Optional[Store]:
    """Run c on a copy of s. Return the final store, or None after fuel steps.

    Precondition: every variable of c is a key of s.
    Cost: at most fuel steps, each O(1) plus the cost of its expression.
    """
    s = dict(s)
    work: list[Cmd] = [c]
    while work:
        fuel -= 1
        if fuel < 0:
            return None
        d = work.pop()
        tag = d[0]
        if tag == "skip":
            continue
        if tag == "assign":
            s[d[1]] = evaluate(d[2], s)
        elif tag == "seq":
            work.append(d[2])
            work.append(d[1])
        elif tag == "if":
            work.append(d[2] if evaluate(d[1], s) != 0 else d[3])
        elif tag == "while":
            if evaluate(d[1], s) != 0:
                work.append(d)
                work.append(d[2])
        else:
            raise ValueError(f"unknown command {tag!r}")
    return s


def sme(c: Cmd, s: Store, gamma: dict[str, Level], default: int = 0, fuel: int = 10_000) -> dict[str, Optional[int]]:
    """Run c once per level and give each output from the copy of its level.

    The copy at level k sees the true input of x when gamma[x] <= k, and
    the default value otherwise. The output on x comes from the copy at
    level gamma[x]; it is None when that copy does not end within fuel
    steps. The copies run one after the other, lowest level first.
    Precondition: the keys of gamma are the keys of s and hold every
    variable of c.
    Cost: one run of c per distinct level, so at most k times the cost of
    one run for k levels.
    """
    levels = sorted(set(gamma.values()), key=len)  # @line L1
    finals: dict[Level, Optional[Store]] = {}
    for k in levels:  # @line L2
        sk = {x: (s[x] if gamma[x] <= k else default) for x in s}  # @line L3
        finals[k] = run(c, sk, fuel)  # @line L4
    out: dict[str, Optional[int]] = {}
    for x in s:  # @line L5
        t = finals[gamma[x]]  # @line L6
        out[x] = None if t is None else t[x]  # @line L7
    return out  # @line L8
