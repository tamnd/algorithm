# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/software-fault-isolation/. The authors are listed in prov/BDGPFB.jsonl.

"""Software fault isolation of stores on an abstract register machine.

The model has no real machine code. A module is a list of instructions on
registers that hold w-bit words. Its fault domain is the segment of addresses
whose upper w - m bits equal the segment identifier g. The rewriter puts a
sandboxing step before every store, the verifier checks the result, and the
interpreter runs a module with any initial registers, which models an
attacker who controls every value the module computes.

Instructions:
    ("li", r, k)          r <- k
    ("add", r, a, b)      r <- (a + b) mod 2**w
    ("load", r, a)        r <- mem[a]          (loads are not confined here)
    ("store", a, v)       mem[a] <- v
    ("sandbox", d, a)     d <- (a AND (2**m - 1)) OR (g * 2**m)
    ("check", d, a)       fault unless a >> m == g; then d <- a
    ("jnz", c, k)         if c != 0 then go to instruction k
    ("ijump", a)          go to instruction a, fault if a is not an index
    ("halt",)
"""

from collections.abc import Mapping, Sequence

Instr = tuple

_WRITES_FIRST = {"li", "add", "load", "sandbox", "check"}


class SFIError(Exception):
    """Raised by rewrite when the module already uses the dedicated register."""


def sandbox_address(a: int, g: int, m: int) -> int:
    """Force the address a into segment g: keep the low m bits, set the segment bits."""
    return (a & ((1 << m) - 1)) | (g << m)


def in_segment(a: int, g: int, m: int) -> bool:
    return a >> m == g


def rewrite(module: Sequence[Instr], d: str, mode: str = "mask") -> list[Instr]:
    """Insert a sandboxing step before each store that does not use d.

    mode "mask" is address sandboxing and mode "check" is segment matching.
    Direct jump targets are renumbered. Time O(n) for n instructions.
    Precondition: the module does not mention the dedicated register d.
    """
    if mode not in ("mask", "check"):
        raise ValueError("mode must be 'mask' or 'check'")
    for ins in module:
        if d in ins[1:]:
            raise SFIError(f"the module uses the dedicated register {d!r}")  # @line L1
    new_index: list[int] = []
    pos = 0
    for ins in module:
        new_index.append(pos)
        pos += 2 if ins[0] == "store" else 1
    out: list[Instr] = []
    for ins in module:  # @line L2
        if ins[0] == "store":  # @line L2
            _, a, v = ins
            if mode == "mask":
                out.append(("sandbox", d, a))  # @line L3
            else:
                out.append(("check", d, a))  # @line L4
            out.append(("store", d, v))  # @line L5
        elif ins[0] == "jnz":
            out.append(("jnz", ins[1], new_index[ins[2]] if ins[2] < len(module) else pos))
        else:
            out.append(ins)
    return out


def verify(module: Sequence[Instr], d: str) -> bool:
    """Accept only modules in which every store goes through d and only a
    sandboxing step writes d. Time O(n). This is the check a loader runs
    before it trusts a module, so it must not depend on the rewriter."""
    n = len(module)
    for ins in module:
        op = ins[0]
        if op in _WRITES_FIRST and ins[1] == d and op not in ("sandbox", "check"):
            return False  # @line L6
        if op == "store" and ins[1] != d:
            return False  # @line L7
        if op == "jnz" and not 0 <= ins[2] <= n:
            return False  # @line L7
    return True  # @line L8


def run(
    module: Sequence[Instr],
    regs: Mapping[str, int],
    g: int,
    m: int,
    w: int = 16,
    budget: int = 200,
) -> tuple[str, list[tuple[int, int]]]:
    """Run a module and return (status, stores), with stores as (address, value).

    status is "halt", "fault" or "budget". The memory starts as all zeros and
    a register that was never set reads 0. Time O(budget).
    """
    r = dict(regs)
    mem: dict[int, int] = {}
    stores: list[tuple[int, int]] = []
    word = (1 << w) - 1
    pc = 0
    n = len(module)
    for _ in range(budget):
        if not 0 <= pc < n:
            return "halt", stores
        ins = module[pc]
        op = ins[0]
        pc += 1
        if op == "li":
            r[ins[1]] = ins[2] & word
        elif op == "add":
            r[ins[1]] = (r.get(ins[2], 0) + r.get(ins[3], 0)) & word
        elif op == "load":
            r[ins[1]] = mem.get(r.get(ins[2], 0), 0)
        elif op == "store":
            a, v = r.get(ins[1], 0), r.get(ins[2], 0)
            mem[a] = v
            stores.append((a, v))
        elif op == "sandbox":
            r[ins[1]] = sandbox_address(r.get(ins[2], 0), g, m)
        elif op == "check":
            a = r.get(ins[2], 0)
            if not in_segment(a, g, m):
                return "fault", stores
            r[ins[1]] = a
        elif op == "jnz":
            if r.get(ins[1], 0) != 0:
                pc = ins[2]
        elif op == "ijump":
            t = r.get(ins[1], 0)
            if not 0 <= t < n:
                return "fault", stores
            pc = t
        elif op == "halt":
            return "halt", stores
        else:
            raise ValueError(f"unknown instruction {op!r}")
    return "budget", stores
