# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dynamic-partial-order-reduction/. The authors are listed in prov/EKPZ7C.jsonl.

"""Dynamic partial-order reduction (Flanagan and Godefroid, POPL 2005).

The program model is the one of the partial-order reduction page, without
jumps, so that every execution is finite (the state space is acyclic):
a list of threads, each a list of instructions ("w", x, c), ("r", x),
("wr", x), ("lock", l), ("unlock", l). Process p's next instruction in a state
is next(s, p); it may be disabled (a lock that another thread holds).

The search is stateless: it keeps only the current execution, with the state,
the backtrack set and the done set of each prefix. After each step it looks
for the last earlier event that is dependent with the next instruction of
each thread and does not happen before that thread; it adds a backtrack point
there. "May be co-enabled" is taken as always true, which is safe: it can only
add backtrack points.

Cost: per explored step, O(d^2 + n d) time for d the length of the current
execution and n the number of threads (the happens-before sets are built
directly); the number of explored executions is at least the number of
Mazurkiewicz traces of maximal executions and at most the number of all
maximal executions. The recursion depth is the length of the program.
"""


def initial(prog, nvars: int, nlocks: int):
    n = len(prog)
    return (tuple([0] * n), tuple([0] * nvars), tuple([0] * n), tuple([-1] * nlocks))


def enabled(prog, s) -> list[int]:
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
    return (tuple(pcs), tuple(vals), tuple(regs), tuple(owners))


def access(ins):
    if ins[0] in ("w", "wr"):
        return set(), {("v", ins[1])}
    if ins[0] == "r":
        return {("v", ins[1])}, set()
    return set(), {("l", ins[1])}


def dependent(a, b) -> bool:
    ra, wa = access(a)
    rb, wb = access(b)
    return bool(wa & (rb | wb) or wb & ra)


def dynamic_partial_order_reduction(prog, nvars: int, nlocks: int):
    """Return (terminal states, explored maximal executions as lists of threads)."""
    states = [initial(prog, nvars, nlocks)]
    events: list = []  # (thread, instruction) of each step of the current execution
    hb: list = []  # hb[j]: indices of the earlier events that happen before event j
    backtrack: list = []
    done: list = []
    terminal, runs = set(), []

    def happens_before_thread(i, p):
        """Does event i happen before the next step of thread p (i ->_S p)?"""
        if events[i][0] == p:
            return True
        return any(events[j][0] == p and i in hb[j] for j in range(i + 1, len(events)))

    def explore():
        s = states[-1]
        pcs = s[0]
        for p, code in enumerate(prog):  # @line L1
            if pcs[p] == len(code):
                continue
            nxt = code[pcs[p]]
            for i in range(len(events) - 1, -1, -1):  # @line L2
                q, ins = events[i]
                if q != p and dependent(ins, nxt) and not happens_before_thread(i, p):
                    pre_en = enabled(prog, states[i])  # @line L3
                    if p in pre_en:
                        backtrack[i].add(p)  # @line L4
                    else:
                        backtrack[i].update(pre_en)  # @line L5
                    break
        en = enabled(prog, s)
        if not en:
            terminal.add(s)
            runs.append([q for q, _ in events])
            return
        backtrack.append({en[0]})  # @line L6
        done.append(set())
        k = len(states) - 1
        while backtrack[k] - done[k]:  # @line L7
            p = min(backtrack[k] - done[k])
            done[k].add(p)  # @line L8
            ins = prog[p][pcs[p]]
            j = len(events)
            before = set()
            for i, (q, other) in enumerate(events):
                if q == p or dependent(other, ins):
                    before.add(i)
                    before |= hb[i]
            events.append((p, ins))
            hb.append(before)
            states.append(step(prog, s, p))
            explore()  # @line L9
            states.pop()
            events.pop()
            hb.pop()
            assert len(events) == j
        backtrack.pop()
        done.pop()

    explore()
    return terminal, runs
