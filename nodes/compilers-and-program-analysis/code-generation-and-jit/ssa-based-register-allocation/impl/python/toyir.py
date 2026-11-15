# SPDX-License-Identifier: MIT
# Shared helper of the compilers and program analysis pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""The toy IR: three-address code in basic blocks.

A program is Program(params, blocks). blocks is a dict from label to
Block(instrs, term), kept in insertion order, and the first label is the
entry. Instructions are tuples:

    ("const", x, k)          x = k
    ("copy", x, a)           x = y
    ("op", x, op, a, b)      x = a op b
    ("phi", x, {pred: a})    x = phi [pred: a, ...]
    ("addr", p, x)           p = &x
    ("load", x, p)           x = *p
    ("store", p, a)          *p = a
    ("alloc", p)             p = alloc
    ("call", x, f, args)     x = call f(a, b)   (args is a list)

Terminators are ("jump", L), ("br", a, L1, L2) and ("ret", a). An operand a
is a str (a name) or an int. The text form of a copy of an int is the text
form of a constant, so parse always gives ("const", x, k) for "x = k".
"""

from dataclasses import dataclass, field
import re

OPS = ("+", "-", "*", "/", "%", "&", "|", "^", "<<", ">>", "<", "<=", "==", "!=")


@dataclass
class Block:
    instrs: list = field(default_factory=list)
    term: tuple = ("ret", 0)


@dataclass
class Program:
    params: list
    blocks: dict

    @property
    def entry(self):
        return next(iter(self.blocks))


class UndefinedName(Exception):
    """A name was read before any definition."""


# ---------------------------------------------------------------- text form

_NAME = r"[A-Za-z_][A-Za-z0-9_.]*"
_INT = r"-?[0-9]+"


def _operand(tok):
    if re.fullmatch(_INT, tok):
        return int(tok)
    if re.fullmatch(_NAME, tok):
        return tok
    raise ValueError("bad operand: %r" % tok)


def _name(tok):
    if not re.fullmatch(_NAME, tok):
        raise ValueError("bad name: %r" % tok)
    return tok


def _parse_instr(line):
    toks = line.split()
    if toks[0] == "jump" and len(toks) == 2:
        return "term", ("jump", _name(toks[1]))
    if toks[0] == "br" and len(toks) == 4:
        return "term", ("br", _operand(toks[1]), _name(toks[2]), _name(toks[3]))
    if toks[0] == "ret" and len(toks) == 2:
        return "term", ("ret", _operand(toks[1]))
    lhs, eq, rhs = line.partition("=")
    if not eq:
        raise ValueError("bad line: %r" % line)
    lhs, rhs = lhs.strip(), rhs.strip()
    if lhs.startswith("*"):
        return "instr", ("store", _name(lhs[1:].strip()), _operand(rhs))
    x = _name(lhs)
    if rhs.startswith("phi"):
        body = rhs[3:].strip()
        if not (body.startswith("[") and body.endswith("]")):
            raise ValueError("bad phi: %r" % line)
        args = {}
        inner = body[1:-1].strip()
        if inner:
            for part in inner.split(","):
                pred, colon, a = part.partition(":")
                if not colon:
                    raise ValueError("bad phi: %r" % line)
                args[_name(pred.strip())] = _operand(a.strip())
        return "instr", ("phi", x, args)
    if rhs.startswith("call "):
        m = re.fullmatch(r"call\s+(" + _NAME + r")\s*\((.*)\)", rhs)
        if not m:
            raise ValueError("bad call: %r" % line)
        inner = m.group(2).strip()
        args = [_operand(a.strip()) for a in inner.split(",")] if inner else []
        return "instr", ("call", x, m.group(1), args)
    if rhs == "alloc":
        return "instr", ("alloc", x)
    if rhs.startswith("&"):
        return "instr", ("addr", x, _name(rhs[1:].strip()))
    if rhs.startswith("*"):
        return "instr", ("load", x, _name(rhs[1:].strip()))
    parts = rhs.split()
    if len(parts) == 1:
        a = _operand(parts[0])
        if isinstance(a, int):
            return "instr", ("const", x, a)
        return "instr", ("copy", x, a)
    if len(parts) == 3 and parts[1] in OPS:
        return "instr", ("op", x, parts[1], _operand(parts[0]), _operand(parts[2]))
    raise ValueError("bad instruction: %r" % line)


def parse(text):
    """Parse the text form. A line "# params: a, b" gives the parameters;
    without it, the parameters are the names that are read and never
    defined, in the order of their first use."""
    params = None
    blocks = {}
    cur = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#"):
            m = re.fullmatch(r"#\s*params:(.*)", line)
            if m:
                inner = m.group(1).strip()
                params = [_name(p.strip()) for p in inner.split(",")] if inner else []
            continue
        if line.endswith(":") and re.fullmatch(_NAME, line[:-1]):
            label = line[:-1]
            if label in blocks:
                raise ValueError("duplicate label: %r" % label)
            cur = label
            blocks[label] = Block([], None)
            continue
        if cur is None:
            raise ValueError("instruction outside a block: %r" % line)
        if blocks[cur].term is not None:
            raise ValueError("instruction after the terminator in %r" % cur)
        kind, item = _parse_instr(line)
        if kind == "term":
            blocks[cur].term = item
        else:
            blocks[cur].instrs.append(item)
    for label, b in blocks.items():
        if b.term is None:
            raise ValueError("block %r has no terminator" % label)
    if not blocks:
        raise ValueError("empty program")
    prog = Program([], blocks)
    if params is None:
        params = _free_names(prog)
    prog.params = params
    return prog


def _free_names(prog):
    defined = set()
    for b in prog.blocks.values():
        for ins in b.instrs:
            d = defs(ins)
            if d is not None:
                defined.add(d)
    out = []
    for b in prog.blocks.values():
        for ins in b.instrs:
            for a in uses(ins):
                if a not in defined and a not in out:
                    out.append(a)
        for a in term_uses(b.term):
            if a not in defined and a not in out:
                out.append(a)
    return out


def _show_instr(ins):
    k = ins[0]
    if k == "const":
        return "%s = %d" % (ins[1], ins[2])
    if k == "copy":
        return "%s = %s" % (ins[1], ins[2])
    if k == "op":
        return "%s = %s %s %s" % (ins[1], ins[3], ins[2], ins[4])
    if k == "phi":
        return "%s = phi [%s]" % (ins[1], ", ".join("%s: %s" % (p, a) for p, a in ins[2].items()))
    if k == "addr":
        return "%s = &%s" % (ins[1], ins[2])
    if k == "load":
        return "%s = *%s" % (ins[1], ins[2])
    if k == "store":
        return "*%s = %s" % (ins[1], ins[2])
    if k == "alloc":
        return "%s = alloc" % ins[1]
    if k == "call":
        return "%s = call %s(%s)" % (ins[1], ins[2], ", ".join(str(a) for a in ins[3]))
    raise ValueError("bad instruction: %r" % (ins,))


def _show_term(t):
    if t[0] == "jump":
        return "jump %s" % t[1]
    if t[0] == "br":
        return "br %s %s %s" % (t[1], t[2], t[3])
    if t[0] == "ret":
        return "ret %s" % (t[1],)
    raise ValueError("bad terminator: %r" % (t,))


def show(prog):
    lines = ["# params: " + ", ".join(prog.params)]
    for label, b in prog.blocks.items():
        lines.append(label + ":")
        for ins in b.instrs:
            lines.append("  " + _show_instr(ins))
        lines.append("  " + _show_term(b.term))
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------- names and graph


def defs(ins):
    """The name an instruction defines, or None for a store."""
    return None if ins[0] == "store" else ins[1]


def uses(ins):
    """The names an instruction reads, in order (phi operands included)."""
    k = ins[0]
    if k == "const" or k == "alloc" or k == "addr":
        ops = []
    elif k == "copy":
        ops = [ins[2]]
    elif k == "op":
        ops = [ins[3], ins[4]]
    elif k == "phi":
        ops = list(ins[2].values())
    elif k == "load":
        ops = [ins[2]]
    elif k == "store":
        ops = [ins[1], ins[2]]
    elif k == "call":
        ops = list(ins[3])
    else:
        raise ValueError("bad instruction: %r" % (ins,))
    return [a for a in ops if isinstance(a, str)]


def term_uses(t):
    if t[0] == "br" or t[0] == "ret":
        return [t[1]] if isinstance(t[1], str) else []
    return []


def succs(prog, label):
    """Successor labels of a block, without repeats, in terminator order."""
    t = prog.blocks[label].term
    if t[0] == "jump":
        return [t[1]]
    if t[0] == "br":
        return [t[2]] if t[2] == t[3] else [t[2], t[3]]
    return []


def edges(prog):
    return [(a, b) for a in prog.blocks for b in succs(prog, a)]


def preds(prog):
    """Dict from label to the list of predecessor labels, in block order."""
    out = {label: [] for label in prog.blocks}
    for a, b in edges(prog):
        out[b].append(a)
    return out


def is_acyclic(prog):
    color = {label: 0 for label in prog.blocks}
    for root in prog.blocks:
        if color[root]:
            continue
        color[root] = 1
        stack = [(root, iter(succs(prog, root)))]
        while stack:
            v, it = stack[-1]
            w = next(it, None)
            if w is None:
                color[v] = 2
                stack.pop()
            elif color[w] == 1:
                return False
            elif color[w] == 0:
                color[w] = 1
                stack.append((w, iter(succs(prog, w))))
    return True


def paths(prog):
    """Every path from the entry to a ret block, as a list of labels.
    The CFG must be acyclic."""
    if not is_acyclic(prog):
        raise ValueError("paths needs an acyclic CFG")
    out = []

    def walk(path):
        last = path[-1]
        s = succs(prog, last)
        if not s:
            out.append(list(path))
        for w in s:
            path.append(w)
            walk(path)
            path.pop()

    walk([prog.entry])
    return out


# ------------------------------------------------------------------ running


class _Trap(Exception):
    pass


class _Fuel(Exception):
    pass


def _binop(op, a, b):
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("arithmetic on a pointer")
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/" or op == "%":
        if b == 0:
            raise _Trap()
        q = abs(a) // abs(b)
        if (a < 0) != (b < 0):
            q = -q
        return q if op == "/" else a - b * q
    if op == "&":
        return a & b
    if op == "|":
        return a | b
    if op == "^":
        return a ^ b
    if op == "<<" or op == ">>":
        if b < 0 or b > 63:
            raise _Trap()
        return a << b if op == "<<" else a >> b
    if op == "<":
        return int(a < b)
    if op == "<=":
        return int(a <= b)
    if op == "==":
        return int(a == b)
    if op == "!=":
        return int(a != b)
    raise ValueError("bad operator: %r" % op)


class _Frame:
    """One activation: its program, its variables and its position."""

    def __init__(self, prog, args, fid):
        if len(args) != len(prog.params):
            raise ValueError("expected %d arguments" % len(prog.params))
        self.prog = prog
        self.env = dict(zip(prog.params, args))
        self.fid = fid
        self.label = prog.entry
        self.prev = None
        self.pc = 0  # 0 means: the phis of the block have not run yet
        self.dest = None  # the name that receives the value of a pending call

    def val(self, a):
        if isinstance(a, int):
            return a
        if a not in self.env:
            raise UndefinedName(a)
        return self.env[a]


def _run(prog, args, fuel, funcs):
    """Run with an explicit stack of frames, so deep recursion in the toy
    program does not use Python recursion."""
    heap = {}
    envs = {}
    stack = []
    fr = _Frame(prog, args, 0)
    envs[0] = fr.env
    nframes = 1

    def tick():
        nonlocal fuel
        if fuel <= 0:
            raise _Fuel()
        fuel -= 1

    while True:
        block = fr.prog.blocks[fr.label]
        instrs = block.instrs
        if fr.pc == 0:
            # Phis at the top of the block read all operands first, then assign.
            incoming = []
            i = 0
            while i < len(instrs) and instrs[i][0] == "phi":
                tick()
                ins = instrs[i]
                if fr.prev not in ins[2]:
                    raise ValueError("phi %s has no operand for %r" % (ins[1], fr.prev))
                incoming.append((ins[1], fr.val(ins[2][fr.prev])))
                i += 1
            for x, v in incoming:
                fr.env[x] = v
            fr.pc = i if i > 0 else -1
        start = fr.pc if fr.pc > 0 else 0
        called = False
        env = fr.env
        for j in range(start, len(instrs)):
            ins = instrs[j]
            tick()
            k = ins[0]
            if k == "const":
                env[ins[1]] = ins[2]
            elif k == "copy":
                env[ins[1]] = fr.val(ins[2])
            elif k == "op":
                env[ins[1]] = _binop(ins[2], fr.val(ins[3]), fr.val(ins[4]))
            elif k == "addr":
                env[ins[1]] = ("var", fr.fid, ins[2])
            elif k == "alloc":
                cell = ("heap", len(heap))
                heap[cell] = None
                env[ins[1]] = cell
            elif k == "load":
                p = fr.val(ins[2])
                if p[0] == "var":
                    if p[2] not in envs[p[1]]:
                        raise UndefinedName(p[2])
                    env[ins[1]] = envs[p[1]][p[2]]
                else:
                    if heap[p] is None:
                        raise UndefinedName(repr(p))
                    env[ins[1]] = heap[p]
            elif k == "store":
                p = fr.val(ins[1])
                if p[0] == "var":
                    envs[p[1]][p[2]] = fr.val(ins[2])
                else:
                    heap[p] = fr.val(ins[2])
            elif k == "call":
                if funcs is None or ins[2] not in funcs:
                    raise ValueError("unknown function %r" % ins[2])
                vals = [fr.val(a) for a in ins[3]]
                fr.pc = j + 1
                fr.dest = ins[1]
                stack.append(fr)
                fr = _Frame(funcs[ins[2]], vals, nframes)
                envs[nframes] = fr.env
                nframes += 1
                called = True
                break
            elif k == "phi":
                raise ValueError("phi after a non-phi instruction")
            else:
                raise ValueError("bad instruction: %r" % (ins,))
        if called:
            continue
        tick()
        t = block.term
        if t[0] == "jump" or t[0] == "br":
            if t[0] == "jump":
                nxt = t[1]
            else:
                nxt = t[2] if fr.val(t[1]) != 0 else t[3]
            fr.prev, fr.label, fr.pc = fr.label, nxt, 0
            continue
        v = fr.val(t[1])
        if not stack:
            return ("ret", v), fuel
        fr = stack.pop()
        fr.env[fr.dest] = v


def run(prog, args, fuel=10000, funcs=None):
    """Run prog on args. Returns ("ret", v), ("trap",) or ("fuel",).
    Each instruction, phi and terminator uses one unit of fuel. funcs is an
    optional dict from function name to Program, used by call; deep
    recursion in the toy program is fine, because the frames are kept on an
    explicit stack."""
    try:
        out, _ = _run(prog, list(args), fuel, funcs)
        return out
    except _Trap:
        return ("trap",)
    except _Fuel:
        return ("fuel",)


# ------------------------------------------------------------ random programs

_SAFE = ("+", "-", "*", "&", "|", "^", "<", "<=", "==", "!=")
_CONST_RIGHT = ("/", "%", "<<", ">>")


def random_program(rng, nvars, nblocks, acyclic):
    """A random program with blocks B0 .. B(nblocks-1) and variables
    x0 .. x(nvars-1). x0 and x1 are the parameters; the entry defines the
    others, so no run reads an undefined name. A division by a variable can
    trap. Every block is reachable from
    B0 and B0 has no predecessor. With acyclic=False, each loop has its own
    counter c that is set to 0 in B0 and never reset, and the back edge is
    taken only while c < m and c < 4, where m is the first parameter. So the
    whole run takes each back edge at most 3 times."""
    nvars = max(nvars, 1)
    nblocks = max(nblocks, 1)
    xs = ["x%d" % i for i in range(nvars)]
    params = xs[:2]
    labels = ["B%d" % i for i in range(nblocks)]

    def operand():
        if rng.random() < 0.25:
            return rng.randint(-3, 9)
        return rng.choice(xs)

    def instr():
        x = rng.choice(xs)
        r = rng.random()
        if r < 0.15:
            return ("const", x, rng.randint(-5, 9))
        if r < 0.25:
            return ("copy", x, rng.choice(xs))
        if r < 0.3:
            # A division by a variable may trap.
            return ("op", x, rng.choice(("/", "%")), rng.choice(xs), rng.choice(xs))
        if r < 0.4:
            op = rng.choice(_CONST_RIGHT)
            k = rng.randint(1, 5)
            return ("op", x, op, rng.choice(xs), k)
        return ("op", x, rng.choice(_SAFE), operand(), operand())

    blocks = {}
    has_pred = [False] * nblocks
    has_pred[0] = True
    for i in range(nblocks):
        instrs = [instr() for _ in range(rng.randint(1, 3))]
        if i == 0:
            instrs = [("const", x, rng.randint(-5, 9)) for x in xs[len(params):]] + instrs
        if i == nblocks - 1:
            term = ("ret", rng.choice(xs))
        elif has_pred[i + 1] and rng.random() < 0.2:
            term = ("ret", rng.choice(xs))
        else:
            first = i + 1 if not has_pred[i + 1] else rng.randrange(i + 1, nblocks)
            if rng.random() < 0.5:
                term = ("jump", labels[first])
                has_pred[first] = True
            else:
                second = rng.randrange(i + 1, nblocks)
                if second == first:
                    term = ("jump", labels[first])
                else:
                    term = ("br", rng.choice(xs), labels[first], labels[second])
                    has_pred[second] = True
                has_pred[first] = True
        blocks[labels[i]] = Block(instrs, term)

    if not acyclic and nblocks > 1:
        nloops = rng.randint(1, max(1, nblocks // 3))
        for k in range(nloops):
            latches = [lab for lab in labels[1:] if blocks[lab].term[0] == "jump"]
            if not latches:
                break
            t = rng.choice(latches)
            h = labels[rng.randint(1, labels.index(t))]
            c, m, w1, w2, w = "c%d" % k, "m%d" % k, "t%d" % k, "u%d" % k, "w%d" % k
            blocks[labels[0]].instrs[0:0] = [("const", c, 0), ("copy", m, params[0])]
            out = blocks[t].term[1]
            blocks[t].instrs += [
                ("op", c, "+", c, 1),
                ("op", w1, "<", c, m),
                ("op", w2, "<", c, 4),
                ("op", w, "&", w1, w2),
            ]
            blocks[t].term = ("br", w, h, out)
    return Program(list(params), blocks)
