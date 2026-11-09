# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/partial-order-reduction/. The authors are listed in prov/K3M7D5.jsonl.

"""Static partial-order reduction with ample sets (conditions C0 to C3).

A program is a list of threads. A thread is a list of instructions:
    ("w", x, c)     write the constant c to the shared variable x
    ("r", x)        copy x to the thread's register
    ("wr", x)       write the register to x
    ("lock", l)     take the lock l (enabled when l is free)
    ("unlock", l)   release l (enabled when this thread holds l)
    ("jmp", k)      go to instruction k (a local step; it makes loops)
A thread whose program counter equals the length of its list has ended.
A state is (pcs, vals, regs, owners), all tuples; variables start at 0 and
locks start free (-1).

A transition is identified by its thread: in each state a thread has at most
one next instruction. Two instructions of different threads are dependent when
they use the same lock, or the same variable with at least one write.

reduced_search builds the reduced state graph with a depth-first search. The
ample set of a state is {the next instruction of thread i} when that
instruction is enabled (C0), every instruction that another thread can still
reach is independent of it (C1), it writes no visible variable (C2), and its
successor is not on the search stack (C3). Otherwise the ample set is the set
of all enabled transitions. Cost: time and space linear in the size of the
reduced graph, times the cost of the static check (the program length).
"""

from collections.abc import Callable


def initial(prog, nvars: int, nlocks: int):
    n = len(prog)
    return (tuple([0] * n), tuple([0] * nvars), tuple([0] * n), tuple([-1] * nlocks))


def enabled(prog, s) -> list[int]:
    """The threads whose next instruction is enabled in s."""
    pcs, vals, regs, owners = s
    out = []
    for i, code in enumerate(prog):
        if pcs[i] == len(code):
            continue
        ins = code[pcs[i]]
        if ins[0] == "lock" and owners[ins[1]] != -1:
            continue
        if ins[0] == "unlock" and owners[ins[1]] != i:
            continue
        out.append(i)
    return out


def step(prog, s, i):
    """The state after thread i runs its next instruction (which must be enabled)."""
    pcs, vals, regs, owners = (list(x) for x in s)
    ins = prog[i][pcs[i]]
    pcs[i] += 1
    if ins[0] == "w":
        vals[ins[1]] = ins[2]
    elif ins[0] == "r":
        regs[i] = vals[ins[1]]
    elif ins[0] == "wr":
        vals[ins[1]] = regs[i]
    elif ins[0] == "lock":
        owners[ins[1]] = i
    elif ins[0] == "unlock":
        owners[ins[1]] = -1
    elif ins[0] == "jmp":
        pcs[i] = ins[1]
    return (tuple(pcs), tuple(vals), tuple(regs), tuple(owners))


def access(ins):
    """(reads, writes) of an instruction, as sets of ("v", x) and ("l", l)."""
    kind = ins[0]
    if kind == "w" or kind == "wr":
        return set(), {("v", ins[1])}
    if kind == "r":
        return {("v", ins[1])}, set()
    if kind in ("lock", "unlock"):
        return set(), {("l", ins[1])}
    return set(), set()


def dependent(a, b) -> bool:
    """Do two instructions of different threads conflict?"""
    ra, wa = access(a)
    rb, wb = access(b)
    return bool(wa & (rb | wb) or wb & ra)


def future(code, pc) -> list:
    """All instructions that a thread at pc can still run (follows jumps)."""
    seen, todo, out = set(), [pc], []
    while todo:
        k = todo.pop()
        if k in seen or k >= len(code):
            continue
        seen.add(k)
        ins = code[k]
        out.append(ins)
        todo.append(ins[1] if ins[0] == "jmp" else k + 1)
    return out


def full_search(prog, nvars: int, nlocks: int):
    """Plain exploration: (reachable states, deadlock states)."""
    s0 = initial(prog, nvars, nlocks)
    seen, todo, dead = {s0}, [s0], set()
    while todo:
        s = todo.pop()
        en = enabled(prog, s)
        if not en:
            dead.add(s)
        for i in en:
            t = step(prog, s, i)
            if t not in seen:
                seen.add(t)
                todo.append(t)
    return seen, dead


def ample(prog, s, en, on_stack, visible: set, proviso: bool) -> list[int]:
    """An ample set of s: a single thread that meets C1 to C3, or all of en."""
    pcs = s[0]
    for i in en:  # @line L7
        ins = prog[i][pcs[i]]
        if access(ins)[1] & {("v", x) for x in visible}:  # @line L8
            continue
        if any(
            dependent(ins, other)
            for j, code in enumerate(prog)
            if j != i
            for other in future(code, pcs[j])
        ):  # @line L9
            continue
        if proviso and step(prog, s, i) in on_stack:  # @line L10
            continue
        return [i]  # @line L11
    return en  # @line L12


def reduced_search(prog, nvars: int, nlocks: int, visible=(), proviso: bool = True):
    """Reduced exploration: (visited states, deadlock states)."""
    visible = set(visible)
    s0 = initial(prog, nvars, nlocks)
    seen = {s0}  # @line L1
    on_stack = {s0}
    en0 = enabled(prog, s0)
    stack = [(s0, iter(ample(prog, s0, en0, on_stack, visible, proviso)))]  # @line L2
    dead = set() if en0 else {s0}
    while stack:  # @line L3
        s, it = stack[-1]
        i = next(it, None)  # @line L4
        if i is None:
            stack.pop()
            on_stack.discard(s)
            continue
        t = step(prog, s, i)  # @line L5
        if t in seen:
            continue
        seen.add(t)  # @line L6
        on_stack.add(t)
        en = enabled(prog, t)
        if not en:
            dead.add(t)
        stack.append((t, iter(ample(prog, t, en, on_stack, visible, proviso))))
    return seen, dead


def partial_order_reduction(prog, nvars: int, nlocks: int, bad: Callable, visible=()):
    """Is a state with bad(vals) reachable? visible must hold the variables that bad reads."""
    seen, _ = reduced_search(prog, nvars, nlocks, visible)
    return any(bad(s[1]) for s in seen)
