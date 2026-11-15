# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/local-value-numbering/. The authors are listed in prov/CJTBEP.jsonl.
"""Local value numbering on the toy IR.

lvn_block(instrs) rewrites the instructions of one basic block and returns a
new list of the same length: the i-th instruction of the result replaces the
i-th instruction of the input. An operation becomes a constant when both
operands are known constants and it cannot trap, a copy or a constant when a
safe algebraic identity applies, and a copy of a name that still holds the
value when the same operation on the same value numbers was computed before
in the block. Every other instruction is kept. lvn(prog) applies lvn_block
to every block and returns a new program.
"""

from collections import deque

import toyir

COMMUTATIVE = ("+", "*", "&", "|", "^", "==", "!=")


def evaluate(op, a, b):
    """The value of a op b in the toy IR, or None if the operation traps.
    Division truncates toward zero, as on the target; Python's // does not."""
    if op in ("/", "%"):
        if b == 0:
            return None
        q = abs(a) // abs(b)
        if (a < 0) != (b < 0):
            q = -q
        return q if op == "/" else a - b * q
    if op in ("<<", ">>"):
        if b < 0 or b > 63:
            return None
        return a << b if op == "<<" else a >> b
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "&":
        return a & b
    if op == "|":
        return a | b
    if op == "^":
        return a ^ b
    if op == "<":
        return int(a < b)
    if op == "<=":
        return int(a <= b)
    if op == "==":
        return int(a == b)
    if op == "!=":
        return int(a != b)
    raise ValueError("bad operator: %r" % op)


def _identity(op, a, b, va, vb, ka, kb):
    """A safe algebraic identity for a op b. Returns ("name", a), ("name", b),
    ("const", k) or None. ka and kb are the known constants of the operands,
    or None. No identity removes a trap: x / x and 0 / x are not touched."""
    same = va == vb
    if op == "+":
        if kb == 0:
            return ("name", a)
        if ka == 0:
            return ("name", b)
    elif op == "-":
        if kb == 0:
            return ("name", a)
        if same:
            return ("const", 0)
    elif op == "*":
        if kb == 0 or ka == 0:
            return ("const", 0)
        if kb == 1:
            return ("name", a)
        if ka == 1:
            return ("name", b)
    elif op == "/":
        if kb == 1:
            return ("name", a)
    elif op == "%":
        if kb == 1 or kb == -1:
            return ("const", 0)
    elif op in ("<<", ">>"):
        if kb == 0:
            return ("name", a)
    elif op == "&":
        if kb == 0 or ka == 0:
            return ("const", 0)
        if same or kb == -1:
            return ("name", a)
        if ka == -1:
            return ("name", b)
    elif op == "|":
        if same or kb == 0:
            return ("name", a)
        if ka == 0:
            return ("name", b)
    elif op == "^":
        if same:
            return ("const", 0)
        if kb == 0:
            return ("name", a)
        if ka == 0:
            return ("name", b)
    elif op in ("==", "<="):
        if same:
            return ("const", 1)
    elif op in ("!=", "<"):
        if same:
            return ("const", 0)
    return None


class _Numbering:
    """The maps of one block: name -> VN, constant -> VN, VN -> constant,
    expression key -> VN, and VN -> the names that were given it."""

    def __init__(self):
        self.vn = {}
        self.const_vn = {}
        self.vn_const = {}
        self.table = {}
        self.holders = {}
        self.count = 0

    def fresh(self):
        self.count += 1
        return self.count

    def of_const(self, k):
        if k not in self.const_vn:  # @line L21
            v = self.fresh()
            self.const_vn[k] = v
            self.vn_const[v] = k
        return self.const_vn[k]  # @line L22

    def of(self, a):
        if isinstance(a, int):  # @line L20
            return self.of_const(a)
        if a not in self.vn:  # @line L23
            # First read in the block: the value the name has on entry.
            self.bind(a, self.fresh())
        return self.vn[a]  # @line L24

    def bind(self, x, v):
        self.vn[x] = v
        if v not in self.holders:
            self.holders[v] = deque()
        self.holders[v].append(x)

    def holder(self, v):
        """A name that holds value number v now, or None. Names that were
        redefined since they got v are dropped from the front of the list,
        so each name is passed over at most once per definition."""
        hs = self.holders.get(v)
        while hs and self.vn.get(hs[0]) != v:
            hs.popleft()
        return hs[0] if hs else None


def lvn_block(instrs):
    num = _Numbering()  # @line L1
    out = []
    for ins in instrs:  # @line L2
        kind = ins[0]
        new = ins
        if kind == "store":  # @line L3
            out.append(ins)
            continue
        if kind == "const":  # @line L4
            v = num.of_const(ins[2])
        elif kind == "copy":  # @line L5
            v = num.of(ins[2])
        elif kind == "op":  # @line L6
            x, op, a, b = ins[1], ins[2], ins[3], ins[4]
            va, vb = num.of(a), num.of(b)  # @line L7
            ka, kb = num.vn_const.get(va), num.vn_const.get(vb)
            r = None
            if ka is not None and kb is not None:  # @line L8
                r = evaluate(op, ka, kb)
            if r is not None:
                new = ("const", x, r)  # @line L9
                v = num.of_const(r)
            else:
                ident = _identity(op, a, b, va, vb, ka, kb)  # @line L10
                if ident is not None and isinstance(ident[1], int):
                    ident = ("const", ident[1])
                if ident is not None and ident[0] == "const":  # @line L11
                    new = ("const", x, ident[1])
                    v = num.of_const(ident[1])
                elif ident is not None:
                    new = ("copy", x, ident[1])
                    v = num.of(ident[1])
                else:
                    if op in COMMUTATIVE and vb < va:  # @line L12
                        va, vb = vb, va
                    key = (op, va, vb)
                    if key in num.table:  # @line L13
                        v = num.table[key]
                        h = num.holder(v)  # @line L14
                        if h is not None:
                            new = ("copy", x, h)
                    else:
                        v = num.fresh()  # @line L15
                        num.table[key] = v  # @line L16
        else:
            # phi, load, call, alloc, addr: a value this pass cannot name.
            v = num.fresh()  # @line L17
        out.append(new)
        num.bind(ins[1], v)  # @line L18
    return out  # @line L19


def lvn(prog):
    blocks = {}
    for label, blk in prog.blocks.items():
        blocks[label] = toyir.Block(lvn_block(blk.instrs), blk.term)
    return toyir.Program(list(prog.params), blocks)
