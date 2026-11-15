# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/local-register-allocation/. The authors are listed in prov/A84DF7.jsonl.

"""Bottom-up local register allocation for one basic block of the toy IR.

The block has const, copy and op instructions and ends with ret. The machine
has k registers r0 .. r(k-1). Each name x also has a memory slot mem.x. The
parameters start in memory, so they are clean: memory has their value. A
value that an instruction computes is dirty until it is stored. A load
mem.x -> r costs LOAD_COST, and a store r -> mem.x costs store_cost.

The output is a toy IR program whose parameters are the memory slots of the
original parameters, and which uses only registers and memory slots.
"""

from toyir import Block, Program

LOAD_COST = 1
NEVER = float("inf")


def operands(ins: tuple, term: tuple) -> list:
    """The operands that an instruction reads; ins is None for the ret."""
    if ins is None:
        return [term[1]]
    if ins[0] == "op":
        return [ins[3], ins[4]]
    if ins[0] == "copy":
        return [ins[2]]
    if ins[0] == "const":
        return []
    raise ValueError("a local block has only const, copy and op: %r" % (ins,))


def steps(block: Block) -> list[tuple]:
    """The block as a list of register requests. A value is a pair (name,
    i): the name and the index of its definition, with i = -1 for a
    parameter. The steps are:
      ("use", u, pinned)  u must be in a register; pinned values must stay
      ("drop", u)         u has no later use, so its register is free
      ("def", x)          x needs a register; it is dirty
    """
    instrs = list(block.instrs) + [None]
    cur: dict[str, tuple] = {}
    reads: list[list] = []
    for i, ins in enumerate(instrs):
        vals: list = []
        for a in operands(ins, block.term):
            if isinstance(a, str) and cur.get(a, (a, -1)) not in vals:
                vals.append(cur.get(a, (a, -1)))
        reads.append(vals)
        if ins is not None:
            cur[ins[1]] = (ins[1], i)
    last: dict[tuple, int] = {}
    for i, vals in enumerate(reads):
        for v in vals:
            last[v] = i
    out: list[tuple] = []
    for i, vals in enumerate(reads):
        for t, v in enumerate(vals):
            out.append(("use", v, tuple(vals[:t])))
        for v in vals:
            if last[v] == i:
                out.append(("drop", v))
        if instrs[i] is not None:
            x = (instrs[i][1], i)
            out.append(("def", x))
            if x not in last:
                out.append(("drop", x))
    return out


def next_uses(st: list[tuple]) -> list[dict]:
    """For each step s, the step of the next use after s of each value."""
    res: list[dict] = [{} for _ in st]
    nxt: dict[tuple, int] = {}
    for s in range(len(st) - 1, -1, -1):
        res[s] = dict(nxt)
        if st[s][0] == "use":
            nxt[st[s][1]] = s
    return res


class Allocator:
    """Belady's rule: evict the value whose next use is furthest away."""

    def __init__(self, k: int, store_cost: int = 1) -> None:
        if k < 2:
            raise ValueError("an instruction can need two registers")
        self.k = k
        self.store_cost = store_cost

    def victim(self, reg: list, pinned: tuple, nxt: dict) -> int:
        """The register to free. A subclass can try another rule."""
        cand = [r for r in range(self.k) if reg[r] not in pinned]
        return max(cand, key=lambda r: (nxt.get(reg[r], NEVER), -r))  # @line L8

    def getreg(self, pinned: tuple, nxt: dict) -> int:
        if None in self.reg:  # @line L7
            return self.reg.index(None)
        r = self.victim(self.reg, pinned, nxt)
        v = self.reg[r]
        if v in self.dirty:  # @line L9
            self.code.append(("copy", "mem." + v[0], "r%d" % r))
            self.cost += self.store_cost
            self.dirty.discard(v)
        self.reg[r] = None  # @line L10
        return r

    def allocate(self, prog: Program) -> tuple[Program, int]:
        """Return the allocated program and its cost in loads and stores."""
        ((label, block),) = prog.blocks.items()
        st = steps(block)
        nu = next_uses(st)
        self.reg: list = [None] * self.k
        self.dirty: set = set()
        self.code: list = []
        self.cost = 0
        cur: dict[str, tuple] = {}
        where: dict[tuple, str] = {}  # the register of each operand of the current instruction
        for s, step in enumerate(st):  # @line L1
            if step[0] == "use":
                u = step[1]
                if u not in self.reg:  # @line L2
                    r = self.getreg(step[2], nu[s])  # @line L3
                    self.code.append(("copy", "r%d" % r, "mem." + u[0]))
                    self.cost += LOAD_COST
                    self.reg[r] = u
                where[u] = "r%d" % self.reg.index(u)
            elif step[0] == "drop":  # @line L4
                if step[1] in self.reg:
                    self.reg[self.reg.index(step[1])] = None
            else:
                x = step[1]
                ins = block.instrs[x[1]]

                def loc(a: object) -> object:
                    return where[cur.get(a, (a, -1))] if isinstance(a, str) else a

                r = self.getreg((), nu[s])  # @line L5
                dst = "r%d" % r
                if ins[0] == "const":
                    self.code.append(("const", dst, ins[2]))
                elif ins[0] == "copy":
                    self.code.append(("copy", dst, loc(ins[2])))
                else:
                    self.code.append(("op", dst, ins[2], loc(ins[3]), loc(ins[4])))
                self.reg[r] = x  # @line L6
                self.dirty.add(x)
                cur[x[0]] = x
                where = {}
        ret = block.term[1]
        if isinstance(ret, str):
            ret = where[cur.get(ret, (ret, -1))]
        params = ["mem." + p for p in prog.params]
        return Program(params, {label: Block(self.code, ("ret", ret))}), self.cost


def allocate(prog: Program, k: int, store_cost: int = 1) -> tuple[Program, int]:
    """Allocate the one block of prog to k registers with Belady's rule."""
    return Allocator(k, store_cost).allocate(prog)
