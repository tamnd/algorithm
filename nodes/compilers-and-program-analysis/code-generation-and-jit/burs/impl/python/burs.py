# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/burs/. The authors are listed in prov/VPX7R8.jsonl.

"""A bottom-up rewrite system (BURS) code generator.

A tree is written with tuples: ("CONST", k), ("VAR", x), ("MEM", a),
("ADD", a, b) or ("MUL", a, b). The machine is a list of tree patterns
with costs. In a pattern, "reg" is an operand in a register, ("CONST",) an
immediate constant and ("VAR",) a variable in memory. Registers are
unbounded virtual registers v0, v1, ...

The patterns become a tree grammar with rules of depth one. All dynamic
programming happens when the tables are built. Labeling a tree is then one
table lookup per node.
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
ARITY = {"CONST": 0, "VAR": 0, "MEM": 1, "ADD": 2, "MUL": 2}


def normalize(rules: list) -> tuple[list, list]:
    """Turn the patterns into base rules (lhs, op, kids, cost, pattern) and
    chain rules (lhs, rhs, cost, pattern). A helper nonterminal stands for
    each inner node of a pattern; its rule costs 0."""
    base = [("con", "CONST", (), 0, None), ("var", "VAR", (), 0, None)]
    chain = []
    count = [0]

    def nt(p: object) -> str:
        if p == "reg":
            return "reg"
        if p == ("CONST",):
            return "con"
        if p == ("VAR",):
            return "var"
        count[0] += 1
        name = "h%d" % count[0]
        base.append((name, p[0], tuple(nt(q) for q in p[1:]), 0, None))
        return name

    for idx, (_, pat, cost) in enumerate(rules):
        if pat == ("CONST",):
            chain.append(("reg", "con", cost, idx))
        elif pat == ("VAR",):
            chain.append(("reg", "var", cost, idx))
        else:
            base.append(("reg", pat[0], tuple(nt(q) for q in pat[1:]), cost, idx))
    return base, chain


class Burs:
    """The tables of a BURS code generator for one set of patterns."""

    def __init__(self, rules: list = RULES) -> None:
        self.rules = rules
        self.base, self.chain = normalize(rules)
        self.states: list[tuple] = []
        self.index: dict[tuple, int] = {}
        self.table: dict[tuple, int] = {}
        self.build()

    def close(self, cost: dict[str, tuple]) -> tuple:
        # Apply chain rules until no cost falls, then subtract the minimum.
        changed = True
        while changed:  # @line L4
            changed = False
            for k, (lhs, rhs, c, _) in enumerate(self.chain):
                if rhs in cost and (lhs not in cost or cost[rhs][0] + c < cost[lhs][0]):
                    cost[lhs] = (cost[rhs][0] + c, ("chain", k))
                    changed = True
        low = min(c for c, _ in cost.values())  # @line L5
        return tuple(sorted((x, c - low, r) for x, (c, r) in cost.items()))

    def transition(self, op: str, kids: tuple) -> tuple:
        # The state of a node with this operator and these child states.
        cost: dict[str, tuple] = {}
        kid_cost = [{x: c for x, c, _ in self.states[s]} for s in kids]
        for k, (lhs, bop, nts, c, _) in enumerate(self.base):  # @line L2
            if bop != op or any(x not in kc for x, kc in zip(nts, kid_cost)):
                continue
            total = c + sum(kc[x] for x, kc in zip(nts, kid_cost))  # @line L3
            if lhs not in cost or total < cost[lhs][0]:
                cost[lhs] = (total, ("base", k))
        return self.close(cost)

    def add_state(self, s: tuple) -> int:
        if s not in self.index:
            self.index[s] = len(self.states)
            self.states.append(s)
        return self.index[s]

    def build(self) -> None:
        # The worklist: compute every transition from known states until no new state appears.
        for op, a in ARITY.items():  # @line L1
            if a == 0:
                self.table[(op,)] = self.add_state(self.transition(op, ()))
        done = 0
        while done < len(self.states):  # @line L6
            done = len(self.states)
            for op, a in ARITY.items():
                if a == 1:
                    for s in range(done):
                        if (op, s) not in self.table:
                            self.table[(op, s)] = self.add_state(self.transition(op, (s,)))
                elif a == 2:
                    for s in range(done):
                        for t in range(done):
                            if (op, s, t) not in self.table:
                                self.table[(op, s, t)] = self.add_state(self.transition(op, (s, t)))

    def label(self, t: tuple) -> tuple:
        """Return the tree with a state number on each node: (op, value, state, kids)."""
        if t[0] in ("CONST", "VAR"):
            return (t[0], t[1], self.table[(t[0],)], [])
        kids = [self.label(c) for c in t[1:]]  # @line L7
        return (t[0], None, self.table[(t[0],) + tuple(k[2] for k in kids)], kids)  # @line L8

    def reduce(self, n: tuple, goal: str, code: list, names: list) -> object:
        """Emit the code for n derived from the nonterminal goal. Return the
        virtual register, constant or variable that holds the result."""
        entry = {x: r for x, _, r in self.states[n[2]]}[goal]  # @line L9
        kind, k = entry
        if kind == "chain":
            lhs, rhs, cost, idx = self.chain[k]  # @line L10
            arg = self.reduce(n, rhs, code, names)
            return self.emit(idx, [arg], code, names)
        lhs, op, nts, cost, idx = self.base[k]  # @line L11
        if op in ("CONST", "VAR"):
            return n[1]
        args: list = []
        for child, x in zip(n[3], nts):  # @line L12
            sub = self.reduce(child, x, code, names)
            args += sub if isinstance(sub, list) else [sub]
        if idx is None:
            return args  # a helper: its operands go to the instruction above
        return self.emit(idx, args, code, names)

    def emit(self, idx: int, args: list, code: list, names: list) -> str:
        dst = "v%d" % len(names)
        names.append(dst)
        code.append((idx, dst, args))
        return dst

    def generate(self, t: tuple) -> tuple[list, int]:
        """Return (code, cost). The cost is the least cost of a tiling."""
        n = self.label(t)
        code: list = []
        self.reduce(n, "reg", code, [])
        return code, sum(self.rules[ins[0]][2] for ins in code)


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


def run(code: list, env: dict[str, int], rules: list = RULES) -> int:
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

        reg[dst] = ev(rules[idx][1])
    return reg[code[-1][1]]
