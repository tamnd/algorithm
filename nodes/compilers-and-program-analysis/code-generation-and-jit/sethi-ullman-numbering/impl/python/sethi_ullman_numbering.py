# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sethi-ullman-numbering/. The authors are listed in prov/HKPTPW.jsonl.

"""Sethi-Ullman labels and code generation for expression trees.

An expression is a variable name (a str) or a tuple (op, left, right) with
op in "+", "-", "*". The same variable can occur at many leaves, but each
leaf is a separate node of the tree.

The machine has registers R0 .. R(k-1) and four instructions:
    ("load", i, x)          Ri <- x          x is a variable or a temporary
    ("op", o, i, j, l)      Ri <- Rj o Rl
    ("opm", o, i, j, x)     Ri <- Rj o x     the right operand is in memory
    ("store", t, i)         t <- Ri
The left operand of an operation is always a register.
"""

from typing import Union

Expr = Union[str, tuple]

OPS = {"+": lambda a, b: a + b, "-": lambda a, b: a - b, "*": lambda a, b: a * b}


def is_leaf(e: Expr) -> bool:
    return isinstance(e, str)


def annotate(e: Expr, memory_operands: bool = True, is_left: bool = True) -> tuple:
    """Return a copy of e where each node carries its label.

    A leaf becomes ("leaf", x, label). An inner node becomes
    (op, left, right, label). With memory_operands=False each leaf gets 1,
    which gives the Ershov numbers of a machine with no memory operands.
    """
    if is_leaf(e):
        if is_left or not memory_operands:  # @line L1
            return ("leaf", e, 1)
        return ("leaf", e, 0)  # @line L2
    a = annotate(e[1], memory_operands, True)  # @line L3
    b = annotate(e[2], memory_operands, False)
    la, lb = a[-1], b[-1]
    if la == lb:  # @line L4
        return (e[0], a, b, la + 1)
    return (e[0], a, b, max(la, lb))  # @line L5


def label(e: Expr, memory_operands: bool = True) -> int:
    """The label of the root: the fewest registers that evaluate e without stores."""
    return annotate(e, memory_operands)[-1]


def generate(e: Expr, k: int) -> tuple[list[tuple], int]:
    """Return (code, number of stores) that leaves the value of e in R0.

    The code uses only R0 .. R(k-1). It stores to temporaries only when the
    label of e is larger than k.
    """
    if k < 1:
        raise ValueError("need at least one register")
    code: list[tuple] = []
    temps = [0]

    def gen(n: tuple, i: int) -> None:
        # Put the value of n in Ri. Use only Ri .. R(k-1).
        r = k - i
        if n[0] == "leaf":
            code.append(("load", i, n[1]))  # @line L6
            return
        op, a, b = n[0], n[1], n[2]
        if b[0] == "leaf":
            gen(a, i)  # @line L7
            code.append(("opm", op, i, i, b[1]))
        elif a[-1] >= r and b[-1] >= r:  # @line L8
            gen(b, i)  # @line L9
            t = "t%d" % temps[0]
            temps[0] += 1
            code.append(("store", t, i))
            gen(a, i)  # @line L10
            code.append(("opm", op, i, i, t))
        elif a[-1] >= b[-1]:
            gen(a, i)  # @line L11
            gen(b, i + 1)
            code.append(("op", op, i, i, i + 1))
        else:
            gen(b, i)  # @line L12
            gen(a, i + 1)
            code.append(("op", op, i, i + 1, i))

    gen(annotate(e, True), 0)
    return code, temps[0]


def evaluate(e: Expr, env: dict[str, int]) -> int:
    """Evaluate e directly."""
    if is_leaf(e):
        return env[e]
    return OPS[e[0]](evaluate(e[1], env), evaluate(e[2], env))


def run(code: list[tuple], env: dict[str, int], k: int) -> int:
    """Run the code on a machine with k registers and return R0."""
    reg: dict[int, int] = {}
    mem = dict(env)
    for ins in code:
        if ins[0] == "load":
            _, i, x = ins
            assert 0 <= i < k
            reg[i] = mem[x]
        elif ins[0] == "op":
            _, o, i, j, l = ins
            assert 0 <= i < k
            reg[i] = OPS[o](reg[j], reg[l])
        elif ins[0] == "opm":
            _, o, i, j, x = ins
            assert 0 <= i < k
            reg[i] = OPS[o](reg[j], mem[x])
        else:
            _, t, i = ins
            assert t not in env
            mem[t] = reg[i]
    return reg[0]
