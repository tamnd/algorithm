# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aho-johnson-code-generation/. The authors are listed in prov/10CJ5M.jsonl.

"""Aho-Johnson dynamic programming code generation for expression trees.

A tree is written with tuples: ("CONST", k), ("VAR", x), ("MEM", a),
("ADD", a, b) or ("MUL", a, b). VAR is a variable in memory. MEM(a) loads
the word at the address a. Each instruction of the machine is a tree
pattern with a cost. In a pattern, "reg" is an operand in a register,
("CONST",) is an immediate constant and ("VAR",) is an operand in memory:
a variable, or a temporary that holds a stored subtree. The machine has r
registers and a store instruction t <- Ri of cost STORE_COST.
"""

from itertools import permutations

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
LD = 1
STORE_COST = 3
INF = float("inf")


class Node:
    """One node of the tree. Two nodes are never shared."""

    __slots__ = ("op", "val", "kids")

    def __init__(self, op: str, val: object, kids: list["Node"]) -> None:
        self.op, self.val, self.kids = op, val, kids


def build(t: tuple) -> Node:
    if t[0] in ("CONST", "VAR"):
        return Node(t[0], t[1], [])
    return Node(t[0], None, [build(c) for c in t[1:]])


def heap(a: int) -> int:
    """The word at address a."""
    return (31 * a + 7) % 97


def match(pat: object, n: Node) -> list | None:
    """Match pat at n. Return the leaves of the pattern, left to right, as
    (kind, node) pairs with kind "reg", "const" or "mem", or None."""
    if pat == "reg":
        return [("reg", n)]
    if pat == ("CONST",):
        return [("const", n)] if n.op == "CONST" else None
    if pat == ("VAR",):
        return [("mem", n)]
    if n.op != pat[0]:
        return None
    out: list = []
    for p, child in zip(pat[1:], n.kids):
        m = match(p, child)
        if m is None:
            return None
        out += m
    return out


class Generator:
    """The dynamic program on one tree, and the code that it chooses."""

    def __init__(self, tree: tuple, r: int) -> None:
        if r < 2:
            raise ValueError("this machine needs at least two registers")
        self.r = r
        self.root = build(tree)
        self.cost: dict[Node, list[float]] = {}
        self.choice: dict[Node, list] = {}
        self.label(self.root)

    def label(self, n: Node) -> None:
        r = self.r
        for child in n.kids:  # @line L1
            self.label(child)
        c = [INF] * (r + 1)
        ch: list = [None] * (r + 1)
        for idx, (_, pat, cost) in enumerate(RULES):  # @line L2
            if pat == ("VAR",) and n.op != "VAR":
                continue  # a reload, handled at line L9
            leaves = match(pat, n)
            if leaves is None:
                continue
            regs = [i for i, (k, _) in enumerate(leaves) if k == "reg"]
            base = cost  # @line L3
            for k, h in leaves:
                if k == "mem" and h.op != "VAR":
                    base += self.cost[h][0]
            for order in permutations(regs):  # @line L4
                for j in range(max(1, len(order)), r + 1):
                    total = base + sum(self.cost[leaves[i][1]][j - t] for t, i in enumerate(order))  # @line L5
                    if total < c[j]:  # @line L6
                        c[j] = total
                        ch[j] = (idx, leaves, order)
        if n.op == "VAR":  # @line L7
            c[0], ch[0] = 0, ("var",)
        else:
            c[0], ch[0] = c[r] + STORE_COST, ("store",)  # @line L8
        for j in range(1, r + 1):  # @line L9
            if c[0] + RULES[LD][2] < c[j]:
                c[j], ch[j] = c[0] + RULES[LD][2], ("reload",)
        self.cost[n] = c
        self.choice[n] = ch

    def generate(self) -> list[tuple]:
        """Return the code. An instruction is (rule, Ri, args) or ("store", t, Ri)."""
        self.code: list[tuple] = []
        self.temp: dict[Node, str] = {}
        self.jobs(self.root, self.r)  # @line L10
        self.emit(self.root, ["R%d" % i for i in range(self.r)])  # @line L11
        return self.code

    def run_job(self, n: Node) -> None:
        # Compute n with all registers free, then store it.
        self.jobs(n, self.r)
        self.emit(n, ["R%d" % i for i in range(self.r)])
        t = "t%d" % len(self.temp)
        self.temp[n] = t
        self.code.append(("store", t, "R0"))

    def jobs(self, n: Node, j: int) -> None:
        # Emit first every subtree that the plan of (n, j) keeps in memory.
        ch = self.choice[n][j]
        if ch[0] == "reload":
            self.run_job(n)
            return
        _, leaves, order = ch
        for k, h in leaves:
            if k == "mem" and h.op != "VAR":
                self.run_job(h)
        for t, i in enumerate(order):
            self.jobs(leaves[i][1], j - t)

    def emit(self, n: Node, regs: list[str]) -> None:
        # Leave n in regs[0]. The stored subtrees are already in memory.
        ch = self.choice[n][len(regs)]
        if ch[0] == "reload":
            self.code.append((LD, regs[0], [self.temp[n]]))
            return
        idx, leaves, order = ch
        args: list = [None] * len(leaves)
        for t, i in enumerate(order):
            self.emit(leaves[i][1], regs[t:])
            args[i] = regs[t]
        for i, (k, h) in enumerate(leaves):
            if k == "const":
                args[i] = h.val
            elif k == "mem":
                args[i] = h.val if h.op == "VAR" else self.temp[h]
        self.code.append((idx, regs[0], args))


def generate(tree: tuple, r: int) -> tuple[list[tuple], float]:
    """Return (code, cost) of an optimal program for the tree with r registers."""
    g = Generator(tree, r)
    return g.generate(), g.cost[g.root][r]


def code_cost(code: list[tuple]) -> int:
    return sum(STORE_COST if ins[0] == "store" else RULES[ins[0]][2] for ins in code)


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


def run(code: list[tuple], env: dict[str, int], r: int) -> int:
    """Run the code on the machine with r registers and return R0."""
    reg: dict[str, int] = {}
    mem = dict(env)
    for ins in code:
        if ins[0] == "store":
            mem[ins[1]] = reg[ins[2]]
            continue
        idx, dst, args = ins
        assert int(dst[1:]) < r
        it = iter(args)

        def ev(p: object) -> int:
            if p == "reg":
                return reg[next(it)]
            if p == ("CONST",):
                return next(it)
            if p == ("VAR",):
                return mem[next(it)]
            vals = [ev(q) for q in p[1:]]
            if p[0] == "MEM":
                return heap(vals[0])
            return vals[0] + vals[1] if p[0] == "ADD" else vals[0] * vals[1]

        reg[dst] = ev(RULES[idx][1])
    return reg["R0"]
