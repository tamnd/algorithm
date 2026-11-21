# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/no-sensitive-upgrade/. The authors are listed in prov/V9BYDH.jsonl.

"""A no-sensitive-upgrade (NSU) monitor for a small while language.

Programs are nested tuples:

    expression: an int (a constant), a str (a variable), or (op, e1, e2)
                with op one of "+", "-", "*", "<", "=="
    command:    ("skip",)
                ("assign", x, e)
                ("seq", c1, c2)
                ("if", e, c1, c2)
                ("while", e, c)

Values are integers modulo MOD. A nonzero value is true. A label is a
frozenset of category names, ordered by inclusion; the empty set is the
public level L. Each variable carries a label that changes at run time.
"""

from typing import Optional, Union

Label = frozenset
Expr = Union[int, str, tuple]
Cmd = tuple
Store = dict[str, int]
Labels = dict[str, Label]

MOD = 256
BOTTOM: Label = frozenset()


def evaluate(e: Expr, s: Store, lab: Labels) -> tuple[int, Label]:
    """Return the value of e in the store s and the join of the labels it reads.

    Precondition: every variable of e is a key of s and of lab.
    Cost: O(size of e). Uses an explicit stack, no recursion.
    """
    values: list[int] = []
    level: Label = BOTTOM
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
            level = level | lab[f]
        else:
            work.append((True, f))
            work.append((False, f[2]))
            work.append((False, f[1]))
    return values[0], level


def nsu_run(c: Cmd, s: Store, lab: Labels, fuel: int = 10_000) -> tuple[str, Optional[Store], Optional[Labels]]:
    """Run c under the no-sensitive-upgrade monitor.

    Returns ("ok", store, labels) when the run ends, ("stop", None, None)
    when the monitor stops the run, and ("diverge", None, None) when the
    run takes more than fuel steps. The inputs are not changed.
    Each work item carries its own program counter label, so the label of
    a branch ends when its last command ends.
    Precondition: every variable of c is a key of s and of lab.
    Cost: O(1) lattice operations per step plus the cost of the
    expressions; at most fuel steps.
    """
    s = dict(s)
    lab = dict(lab)
    stack: list[tuple[Cmd, Label]] = [(c, BOTTOM)]  # @line L1
    while stack:  # @line L2
        fuel -= 1
        if fuel < 0:
            return ("diverge", None, None)
        d, pc = stack.pop()  # @line L3
        tag = d[0]
        if tag == "skip":
            continue
        if tag == "assign":  # @line L4
            x = d[1]
            if not pc <= lab[x]:  # @line L5
                return ("stop", None, None)
            v, le = evaluate(d[2], s, lab)  # @line L6
            s[x] = v
            lab[x] = le | pc  # @line L7
        elif tag == "seq":  # @line L8
            stack.append((d[2], pc))
            stack.append((d[1], pc))
        elif tag == "if":  # @line L9
            v, le = evaluate(d[1], s, lab)
            stack.append((d[2] if v != 0 else d[3], pc | le))  # @line L10
        elif tag == "while":  # @line L11
            v, le = evaluate(d[1], s, lab)
            if v != 0:
                q = pc | le  # @line L12
                stack.append((d, q))
                stack.append((d[2], q))
        else:
            raise ValueError(f"unknown command {tag!r}")
    return ("ok", s, lab)  # @line L13


def observe(store: Store, lab: Labels, level: Label = BOTTOM) -> tuple[tuple[str, object], ...]:
    """Return what an observer at the given level sees of a final store.

    The observer sees the value of each variable whose label is below its
    level, and a "*" for every other variable.
    Cost: O(number of variables).
    """
    return tuple((x, store[x] if lab[x] <= level else "*") for x in sorted(store))
