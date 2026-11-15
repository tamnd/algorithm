# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/copy-and-patch-compilation/. The authors are listed in prov/KRGC64.jsonl.
"""Copy-and-patch compilation of the toy IR.

The target is a small word machine. Its code is a list of integers, and it
has two registers r0 and r1 and an array of slots, one per variable.

    TICK            use one unit of fuel, or stop with ("fuel",)
    LDS r s         r = slot[s]
    LDI r k         r = k
    STS s r         slot[s] = r
    ALU i           r0 = r0 OPS[i] r1, or stop with ("trap",)
    JMP a           go to address a
    BR r a b        go to a if r != 0, else to b
    RET r           stop with ("ret", r)

A stencil is a piece of machine code made once, before any program is
compiled, with holes: words whose value is not known yet, listed by offset
and name like relocations in an object file. The compiler picks one stencil
for each IR instruction, by its kind, its operator and whether each operand
is a variable or a constant. It places the stencils one after the other,
copies their words into the code buffer, and writes the operands and the
addresses into the holes. TICK is there so that the compiled code uses fuel
exactly like toyir.run; a real system has no such instruction.
"""

from dataclasses import dataclass

import toyir

TICK, LDS, LDI, STS, ALU, JMP, BR, RET = range(1, 9)
NAMES = {TICK: "TICK", LDS: "LDS", LDI: "LDI", STS: "STS", ALU: "ALU", JMP: "JMP", BR: "BR", RET: "RET"}
SIZE = {TICK: 1, LDS: 3, LDI: 3, STS: 3, ALU: 2, JMP: 2, BR: 4, RET: 2}


@dataclass(frozen=True)
class Stencil:
    """Machine code with holes. code has a 0 at each hole; holes is a tuple
    of (offset, name) pairs."""

    name: str
    code: tuple
    holes: tuple

    def __len__(self):
        return len(self.code)


def assemble(name, items):
    """Make a stencil from machine instructions, where a str operand is a
    hole with that name."""
    code, holes = [], []
    for ins in items:
        if len(ins) != SIZE[ins[0]]:
            raise ValueError("bad instruction %r in stencil %s" % (ins, name))
        for w in ins:
            if isinstance(w, str):
                holes.append((len(code), w))
                code.append(0)
            else:
                code.append(w)
    return Stencil(name, tuple(code), tuple(holes))


def _load(r, kind, hole):
    # kind "v": the operand is a variable, so load its slot; "i": a constant.
    return (LDS, r, hole) if kind == "v" else (LDI, r, hole)


def build_stencils():
    """The stencil library. Keys are (instruction kind, ...variant)."""
    lib = {}
    lib[("const",)] = assemble("const", [(TICK,), (LDI, 0, "a"), (STS, "x", 0)])
    for ka in "vi":
        lib[("copy", ka)] = assemble("copy_" + ka, [(TICK,), _load(0, ka, "a"), (STS, "x", 0)])
        lib[("br", ka)] = assemble("br_" + ka, [(TICK,), _load(0, ka, "a"), (BR, 0, "t", "f")])
        lib[("ret", ka)] = assemble("ret_" + ka, [(TICK,), _load(0, ka, "a"), (RET, 0)])
        # The first half of an edge copy: read a phi operand into a temporary.
        lib[("phi", ka)] = assemble("phi_" + ka, [(TICK,), _load(0, ka, "a"), (STS, "x", 0)])
        for kb in "vi":
            for i, op in enumerate(toyir.OPS):
                lib[("op", op, ka, kb)] = assemble(
                    "op%s_%s%s" % (op, ka, kb),
                    [(TICK,), _load(0, ka, "a"), _load(1, kb, "b"), (ALU, i), (STS, "x", 0)],
                )
    lib[("jump",)] = assemble("jump", [(TICK,), (JMP, "t")])
    # A jump to the stencil placed right after it: the jump is left out.
    lib[("jump-next",)] = assemble("jump_next", [(TICK,)])
    # The second half of an edge copy: move a temporary into the phi variable.
    lib[("move",)] = assemble("move", [(LDS, 0, "a"), (STS, "x", 0)])
    lib[("goto",)] = assemble("goto", [(JMP, "t")])
    return lib


STENCILS = build_stencils()


@dataclass
class Compiled:
    code: list
    nslots: int
    nparams: int
    names: list  # slot number -> variable name
    placements: list  # (address, stencil, {hole name: value}) in address order

    def run(self, args, fuel=10000):
        return execute(self, args, fuel)


def _kind(a):
    return "i" if isinstance(a, int) else "v"


def _check(prog):
    pr = toyir.preds(prog)
    for label, b in prog.blocks.items():
        seen_other = False
        for ins in b.instrs:
            k = ins[0]
            if k not in ("const", "copy", "op", "phi"):
                raise ValueError("copy-and-patch: unsupported instruction %r" % (ins,))
            if k == "phi":
                if seen_other:
                    raise ValueError("phi after a non-phi instruction in %r" % label)
                if label == prog.entry:
                    raise ValueError("phi in the entry block")
                for p in pr[label]:
                    if p not in ins[2]:
                        raise ValueError("phi %s has no operand for %r" % (ins[1], p))
            else:
                seen_other = True
            if k == "op" and ins[2] not in toyir.OPS:
                raise ValueError("bad operator: %r" % (ins[2],))


def compile_program(prog, lib=STENCILS):
    """Compile prog in two passes. Pass 1 picks a stencil for each
    instruction and gives it an address. Pass 2 copies the stencils into
    the code buffer and patches the holes. Returns a Compiled."""
    _check(prog)
    labels = list(prog.blocks)

    # Slots: parameters first, then every other name in order of appearance.
    slot = {}
    for p in prog.params:
        if p in slot:
            raise ValueError("duplicate parameter %r" % p)
        slot[p] = len(slot)
    for b in prog.blocks.values():
        for ins in b.instrs:
            for a in [toyir.defs(ins)] + toyir.uses(ins):
                slot.setdefault(a, len(slot))
        for a in toyir.term_uses(b.term):
            slot.setdefault(a, len(slot))
    nphi = max((sum(1 for ins in b.instrs if ins[0] == "phi") for b in prog.blocks.values()), default=0)
    temps = []
    for i in range(nphi):
        t = "%%t%d" % i  # cannot clash: % is not allowed in a toy IR name
        temps.append(t)
        slot[t] = len(slot)

    def phis(label):
        return [ins for ins in prog.blocks[label].instrs if ins[0] == "phi"]

    def target(src, dst):
        # Where a branch from src to dst goes: the edge stub if dst has phis.
        return ("edge", src, dst) if phis(dst) else ("block", dst)

    def operand(a):
        return ("imm", a) if isinstance(a, int) else ("slot", a)

    # Pass 1: selection and layout. Each piece is (stencil, {hole: value}),
    # where a value is ("slot", name), ("imm", k) or ("addr", place).
    pieces = []
    addr = {}
    pc = 0

    def place(key, holes):
        nonlocal pc
        st = lib[key]
        pieces.append((pc, st, holes))
        pc += len(st)

    stubs = []
    for n, label in enumerate(labels):
        b = prog.blocks[label]
        addr[("block", label)] = pc
        for ins in b.instrs:
            k = ins[0]
            if k == "phi":
                continue
            if k == "const":
                place(("const",), {"x": ("slot", ins[1]), "a": ("imm", ins[2])})
            elif k == "copy":
                place(("copy", _kind(ins[2])), {"x": ("slot", ins[1]), "a": operand(ins[2])})
            else:
                key = ("op", ins[2], _kind(ins[3]), _kind(ins[4]))
                place(key, {"x": ("slot", ins[1]), "a": operand(ins[3]), "b": operand(ins[4])})
        t = b.term
        if t[0] == "jump":
            to = target(label, t[1])
            nxt = labels[n + 1] if n + 1 < len(labels) else None
            if to == ("block", nxt):
                place(("jump-next",), {})
            else:
                place(("jump",), {"t": ("addr", to)})
            if to[0] == "edge" and to not in stubs:
                stubs.append(to)
        elif t[0] == "br":
            t1, t2 = target(label, t[2]), target(label, t[3])
            place(("br", _kind(t[1])), {"a": operand(t[1]), "t": ("addr", t1), "f": ("addr", t2)})
            for to in (t1, t2):
                if to[0] == "edge" and to not in stubs:
                    stubs.append(to)
        elif t[0] == "ret":
            place(("ret", _kind(t[1])), {"a": operand(t[1])})
        else:
            raise ValueError("bad terminator: %r" % (t,))

    # Edge stubs: read all phi operands into temporaries, then move them.
    for e in stubs:
        _, src, dst = e
        addr[e] = pc
        ps = phis(dst)
        for i, ins in enumerate(ps):
            a = ins[2][src]
            place(("phi", _kind(a)), {"x": ("slot", temps[i]), "a": operand(a)})
        for i, ins in enumerate(ps):
            place(("move",), {"x": ("slot", ins[1]), "a": ("slot", temps[i])})
        place(("goto",), {"t": ("addr", ("block", dst))})

    # Pass 2: copy and patch.
    code = [0] * pc
    placements = []
    for at, st, holes in pieces:
        code[at:at + len(st)] = st.code
        values = {}
        for off, name in st.holes:
            kind, v = holes[name]
            if kind == "slot":
                w = slot[v]
            elif kind == "imm":
                w = v
            else:
                w = addr[v]
            code[at + off] = w
            values[name] = w
        placements.append((at, st, values))
    names = [None] * len(slot)
    for name, s in slot.items():
        names[s] = name
    return Compiled(code, len(slot), len(prog.params), names, placements)


# ------------------------------------------------------------------ the machine


class _Trap(Exception):
    pass


_SIMPLE = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "&": lambda a, b: a & b,
    "|": lambda a, b: a | b,
    "^": lambda a, b: a ^ b,
    "<": lambda a, b: int(a < b),
    "<=": lambda a, b: int(a <= b),
    "==": lambda a, b: int(a == b),
    "!=": lambda a, b: int(a != b),
}


def _alu(op, a, b):
    if op in _SIMPLE:
        return _SIMPLE[op](a, b)
    if op == "/" or op == "%":
        # Division truncates toward zero, and the remainder has the sign of a.
        if b == 0:
            raise _Trap()
        q = abs(a) // abs(b)
        if (a < 0) != (b < 0):
            q = -q
        return q if op == "/" else a - b * q
    if b < 0 or b > 63:
        raise _Trap()
    return a << b if op == "<<" else a >> b


_UNSET = object()


def execute(c, args, fuel=10000):
    """Run compiled code. Returns ("ret", v), ("trap",) or ("fuel",)."""
    if len(args) != c.nparams:
        raise ValueError("expected %d arguments" % c.nparams)
    code = c.code
    slots = list(args) + [_UNSET] * (c.nslots - c.nparams)
    r = [0, 0]
    pc = 0
    while True:
        o = code[pc]
        if o == TICK:
            if fuel <= 0:
                return ("fuel",)
            fuel -= 1
            pc += 1
        elif o == LDS:
            v = slots[code[pc + 2]]
            if v is _UNSET:
                raise toyir.UndefinedName(c.names[code[pc + 2]])
            r[code[pc + 1]] = v
            pc += 3
        elif o == LDI:
            r[code[pc + 1]] = code[pc + 2]
            pc += 3
        elif o == STS:
            slots[code[pc + 1]] = r[code[pc + 2]]
            pc += 3
        elif o == ALU:
            try:
                r[0] = _alu(toyir.OPS[code[pc + 1]], r[0], r[1])
            except _Trap:
                return ("trap",)
            pc += 2
        elif o == JMP:
            pc = code[pc + 1]
        elif o == BR:
            pc = code[pc + 2] if r[code[pc + 1]] != 0 else code[pc + 3]
        elif o == RET:
            return ("ret", r[code[pc + 1]])
        else:
            raise ValueError("bad opcode %r at %d" % (o, pc))


def run(prog, args, fuel=10000):
    """Compile prog and run it, with the same result format as toyir.run."""
    return compile_program(prog).run(args, fuel)


def disassemble(c):
    """One line per machine instruction, with its address."""
    out = []
    code = c.code
    pc = 0
    while pc < len(code):
        o = code[pc]
        n = SIZE[o]
        out.append("%3d  %s %s" % (pc, NAMES[o], " ".join(str(w) for w in code[pc + 1:pc + n])))
        pc += n
    return [line.rstrip() for line in out]


EXAMPLE = """
# params: n
B0:
  s = 0
  i = 0
  jump B1
B1:
  c = i < n
  br c B2 B3
B2:
  s = s + i
  i = i + 1
  jump B1
B3:
  ret s
"""


def example():
    """The worked example of the page: the sum 0 + 1 + ... + (n - 1)."""
    prog = toyir.parse(EXAMPLE)
    return prog, compile_program(prog)


if __name__ == "__main__":
    prog, c = example()
    for at, st, values in c.placements:
        print(at, st.name, values)
    print("\n".join(disassemble(c)))
    print(len(c.code), c.names, c.run([4]), toyir.run(prog, [4]))
