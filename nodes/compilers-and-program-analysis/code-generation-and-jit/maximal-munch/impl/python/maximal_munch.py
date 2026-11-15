# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximal-munch/. The authors are listed in prov/FV9S4Q.jsonl.

"""Maximal munch instruction selection for expression trees.

A tree is written with tuples: ("CONST", k), ("VAR", x), ("MEM", a),
("ADD", a, b) or ("MUL", a, b). VAR is a variable in memory and MEM(a)
loads the word at the address a. Each instruction is a tree pattern with a
cost. In a pattern, "reg" is an operand in a register, ("CONST",) an
immediate constant and ("VAR",) a variable in memory. Registers are
unbounded virtual registers v0, v1, ...
"""

RULES = [
    ("li", ("CONST",), 1),
    ("ld", ("VAR",), 3),
    ("add", ("ADD", "reg", "reg"), 1),
    ("addi", ("ADD", "reg", ("CONST",)), 1),
    ("addm", ("ADD", "reg", ("VAR",)), 3),
    ("mul", ("MUL", "reg", "reg"), 3),
    ("ldr", ("MEM", "reg"), 3),
    ("ldo", ("MEM", ("ADD", "reg", ("CONST",))), 3),
    ("ldx", ("MEM", ("ADD", "reg", "reg")), 3),
    ("madd", ("ADD", ("MUL", "reg", "reg"), "reg"), 2),
]


def size(pat: object) -> int:
    """The number of tree nodes that the pattern covers."""
    if pat == "reg":
        return 0
    return 1 + sum(size(q) for q in pat[1:])


def match(pat: object, n: tuple) -> list | None:
    """Match pat at n. Return the leaves of the pattern, left to right, as
    (kind, node) pairs with kind "reg", "const" or "var", or None."""
    if pat == "reg":
        return [("reg", n)]
    if pat == ("CONST",):
        return [("const", n)] if n[0] == "CONST" else None
    if pat == ("VAR",):
        return [("var", n)] if n[0] == "VAR" else None
    if n[0] != pat[0]:
        return None
    out: list = []
    for p, child in zip(pat[1:], n[1:]):
        m = match(p, child)
        if m is None:
            return None
        out += m
    return out


def choose(n: tuple) -> tuple[int, list]:
    """The largest pattern that matches at n. A tie goes to the first one in the table."""
    best, leaves = -1, None
    for idx, (_, pat, _) in enumerate(RULES):  # @line L2
        m = match(pat, n)
        if m is not None and (best < 0 or size(pat) > size(RULES[best][1])):  # @line L3
            best, leaves = idx, m
    if best < 0:
        raise ValueError("no pattern matches at %r" % (n[0],))
    return best, leaves


def munch(n: tuple, code: list) -> str:
    """Append the code for n to code and return the register that holds n."""
    idx, leaves = choose(n)  # @line L1
    args = []
    for kind, h in leaves:  # @line L4
        if kind == "reg":
            args.append(munch(h, code))  # @line L5
        else:
            args.append(h[1])
    dst = "v%d" % len(code)
    code.append((idx, dst, args))  # @line L6
    return dst  # @line L7


def select(tree: tuple) -> tuple[list, int]:
    """Return (code, cost) of the maximal munch tiling of the tree."""
    code: list = []
    munch(tree, code)
    return code, sum(RULES[ins[0]][2] for ins in code)


def heap(a: int) -> int:
    """The word at address a."""
    return (31 * a + 7) % 97


def evaluate(t: tuple, env: dict[str, int]) -> int:
    """The value of the tree, computed directly."""
    op = t[0]
    if op == "CONST":
        return t[1]
    if op == "VAR":
        return env[t[1]]
    if op == "MEM":
        return heap(evaluate(t[1], env))
    a, b = evaluate(t[1], env), evaluate(t[2], env)
    return a + b if op == "ADD" else a * b


def run(code: list, env: dict[str, int]) -> int:
    """Run the code and return the value of the last instruction."""
    reg: dict[str, int] = {}
    for idx, dst, args in code:
        it = iter(args)

        def ev(p: object) -> int:
            if p == "reg":
                return reg[next(it)]
            if p == ("CONST",):
                return next(it)
            if p == ("VAR",):
                return env[next(it)]
            vals = [ev(q) for q in p[1:]]
            if p[0] == "MEM":
                return heap(vals[0])
            return vals[0] + vals[1] if p[0] == "ADD" else vals[0] * vals[1]

        reg[dst] = ev(RULES[idx][1])
    return reg[code[-1][1]]
