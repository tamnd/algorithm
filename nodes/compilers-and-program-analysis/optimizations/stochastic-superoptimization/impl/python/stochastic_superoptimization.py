# SPDX-License-Identifier: MIT
"""Stochastic superoptimization (STOKE) on toy straight-line programs.

A machine has nregs registers of w bits. The inputs are in r0, r1, ...,
the other registers start at 0, and the output is r0 at the end. A program
is a list of L slots; a slot is None (unused) or an instruction in toy IR
form:

    ("op", d, op, a, b)   rd = ra op rb, op one of + - & | ^ << >>
    ("copy", d, a)        rd = ra

Registers are numbered 0 .. nregs-1, and an operand is a register number
or ("k", c) for a constant c. All arithmetic is modulo 2**w; a shift by w
or more gives 0.

search is the Metropolis-Hastings search of Schkufza, Sharma and Aiken:
the cost of a program is the number of wrong output bits on the tests
plus its number of instructions, moves change one random part of the
program, and a move is accepted with the Metropolis-Hastings rule. A
program that is right on all tests and shorter than the best so far is
checked on every input; if the check fails, an input where it differs
becomes a new test.
"""

import math
import random
from itertools import product

OPS = ("+", "-", "&", "|", "^", "<<", ">>")


class Machine:
    """The machine model: word size w, nregs registers, ninputs inputs,
    the binary operators ops and the constants that may be operands."""

    def __init__(self, w=4, nregs=4, ninputs=2, ops=OPS, consts=(1,)):
        self.w = w
        self.mask = (1 << w) - 1
        self.nregs = nregs
        self.ninputs = ninputs
        self.ops = tuple(ops)
        self.operands = list(range(nregs)) + [("k", c) for c in consts]
        # Every instruction, for the instruction move.
        self.instrs = [("op", d, op, a, b) for op in self.ops for d in range(nregs)
                       for a in self.operands for b in self.operands]
        self.instrs += [("copy", d, a) for d in range(nregs) for a in self.operands if a != d]

    def all_inputs(self):
        return list(product(range(1 << self.w), repeat=self.ninputs))


def _val(regs, a):
    return a[1] if isinstance(a, tuple) else regs[a]


def _apply(m, op, x, y):
    if op == "+":
        return (x + y) & m.mask
    if op == "-":
        return (x - y) & m.mask
    if op == "&":
        return x & y
    if op == "|":
        return x | y
    if op == "^":
        return x ^ y
    if op == "<<":
        return (x << y) & m.mask if y < m.w else 0
    if op == ">>":
        return x >> y if y < m.w else 0
    raise ValueError("unknown operator %r" % (op,))


def run(m, prog, inputs):
    """The value of r0 after prog runs on the given inputs."""
    regs = [0] * m.nregs
    for i, x in enumerate(inputs):
        regs[i] = x & m.mask
    for ins in prog:
        if ins is None:
            continue
        if ins[0] == "op":
            regs[ins[1]] = _apply(m, ins[2], _val(regs, ins[3]), _val(regs, ins[4]))
        else:
            regs[ins[1]] = _val(regs, ins[2])
    return regs[0]


def perf(prog):
    """The number of instructions that are used: every one costs one cycle."""
    return sum(1 for ins in prog if ins is not None)


def eq(m, prog, tests):
    """The number of wrong bits of the output, over the tests. tests is a
    list of (inputs, expected output)."""
    return sum(bin(run(m, prog, x) ^ want).count("1") for x, want in tests)


def cost(m, prog, tests):
    return eq(m, prog, tests) + perf(prog)


def counterexample(m, prog, target):
    """An input where prog and target differ, or None when they agree on
    every input (an exhaustive check over all 2**(w*ninputs) inputs)."""
    for x in m.all_inputs():
        if run(m, prog, x) != run(m, target, x):
            return x
    return None


def acceptance(beta, c, c_new, hastings=1.0):
    """The Metropolis-Hastings acceptance probability of a move from a
    program of cost c to one of cost c_new, where hastings is the ratio
    q(new -> old) / q(old -> new) of the proposal probabilities."""
    d = c_new - c
    if d <= 0 and hastings >= 1:
        return 1.0
    return min(1.0, hastings * math.exp(-beta * d))


def propose(m, prog, rng, p_unused):
    """One random move. Returns (the new program, the move name, the
    Hastings ratio q(new -> old) / q(old -> new) of this move)."""
    L = len(prog)
    new = list(prog)
    kind = rng.choice(("opcode", "operand", "swap", "instruction"))
    i = rng.randrange(L)
    ins = prog[i]
    if kind == "opcode":
        # Another operator for a binary instruction: symmetric.
        if ins is not None and ins[0] == "op":
            op = rng.choice([o for o in m.ops if o != ins[2]])
            new[i] = ("op", ins[1], op, ins[3], ins[4])
        return new, kind, 1.0
    if kind == "operand":
        # Another value for one of the operand places: symmetric.
        if ins is not None:
            places = [1, 3, 4] if ins[0] == "op" else [1, 2]
            k = rng.choice(places)
            pool = list(range(m.nregs)) if k == 1 else m.operands
            choice = rng.choice([v for v in pool if v != ins[k]])
            cand = list(ins)
            cand[k] = choice
            cand = tuple(cand)
            if cand[0] == "copy" and cand[1] == cand[2]:
                return list(prog), kind, 1.0  # not an instruction of the set
            new[i] = cand
        return new, kind, 1.0
    if kind == "swap":
        j = rng.randrange(L)
        new[i], new[j] = new[j], new[i]
        return new, kind, 1.0
    # Instruction move: unused with probability p_unused, otherwise a
    # uniformly random instruction. The proposal is not symmetric, so the
    # Hastings ratio is P(old slot) / P(new slot).
    new[i] = None if rng.random() < p_unused else rng.choice(m.instrs)

    def p(s):
        return p_unused if s is None else (1 - p_unused) / len(m.instrs)
    return new, kind, p(prog[i]) / p(new[i])


def mh_step(m, R, c, tests, beta, rng, p_unused, hastings=True):
    """One step of the chain from program R of cost c. With hastings=False
    the proposal is treated as symmetric (plain Metropolis rule)."""
    R2, _, h = propose(m, R, rng, p_unused)  # @line L4
    c2 = cost(m, R2, tests)  # @line L5
    if rng.random() < acceptance(beta, c, c2, h if hastings else 1.0):  # @line L6
        return R2, c2
    return R, c


class Result:
    def __init__(self, best, tests, accepted, verified, counterexamples, steps):
        self.best = best                    # the shortest verified program found
        self.tests = tests                  # the final test set
        self.accepted = accepted            # (step, program) for each verified improvement
        self.verified = verified            # number of exhaustive checks
        self.counterexamples = counterexamples  # (step, input added as a test, the program it refuted)
        self.steps = steps


def search(m, target, tests, L, steps, beta=4.0, seed=0, p_unused=0.2, start=None):
    """STOKE: Metropolis-Hastings over programs of L slots.

    target is the program to optimize and tests its initial test inputs.
    The chain starts from start (default: target padded to L slots).
    Returns a Result whose best program is equivalent to target on every
    input.
    """
    rng = random.Random(seed)
    tests = [(tuple(x), run(m, target, x)) for x in tests]
    pad = list(target) + [None] * (L - len(target))
    R = list(start) if start is not None else pad
    c = cost(m, R, tests)  # @line L1
    best, accepted, verified, cex = [ins for ins in target if ins is not None], [], 0, []  # @line L2
    for step in range(1, steps + 1):  # @line L3
        R, c = mh_step(m, R, c, tests, beta, rng, p_unused)
        if c == perf(R) and perf(R) < perf(best):  # @line L7
            verified += 1
            x = counterexample(m, R, target)
            if x is None:
                best = [ins for ins in R if ins is not None]  # @line L8
                accepted.append((step, best))
            else:
                tests.append((x, run(m, target, x)))  # @line L9
                cex.append((step, x, [ins for ins in R if ins is not None]))
                c = cost(m, R, tests)
    return Result(best, tests, accepted, verified, cex, steps)  # @line L10


def shortest_by_enumeration(m, target, max_len):
    """The shortest program equivalent to target, by trying all programs of
    length 0, 1, 2, ... (Massalin's exhaustive search), or None."""
    inputs = m.all_inputs()
    want = [run(m, target, x) for x in inputs]
    for n in range(max_len + 1):
        for prog in product(m.instrs, repeat=n):
            if all(run(m, prog, x) == y for x, y in zip(inputs, want)):
                return list(prog)
    return None


def _operand_text(a):
    return str(a[1]) if isinstance(a, tuple) else "r%d" % a


def show(prog):
    """The program in toy IR text, one instruction per line."""
    lines = []
    for ins in prog:
        if ins is None:
            continue
        if ins[0] == "op":
            lines.append("r%d = %s %s %s" % (ins[1], _operand_text(ins[3]), ins[2], _operand_text(ins[4])))
        else:
            lines.append("r%d = %s" % (ins[1], _operand_text(ins[2])))
    return "\n".join(lines)
