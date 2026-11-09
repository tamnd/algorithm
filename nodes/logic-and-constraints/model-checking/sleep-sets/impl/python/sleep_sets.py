# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sleep-sets/. The authors are listed in prov/DD26ZR.jsonl.

"""Sleep sets (Godefroid): skip transitions whose effect an earlier branch already covers.

The program model is the one of the partial-order reduction page: a list of
threads, each a list of instructions ("w", x, c), ("r", x), ("wr", x),
("lock", l), ("unlock", l). A transition is named by its thread. Two
instructions of different threads are dependent when they use the same lock,
or the same variable with at least one write.

sleep_set_search is a stateful depth-first search with sleep sets and a hash
table that stores, for each visited state, the transitions that were asleep
there and so were never taken from it. A later visit with a smaller sleep set
takes the ones that are now awake.

sleep_set_executions is the stateless version: it lists the maximal
executions that the search reaches, without a table of visited states.
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


def _wake(prog, s, sleep, i):
    """The sleep set after thread i moves from s: the members independent of i's step."""
    pcs = s[0]
    a = prog[i][pcs[i]]
    return {j for j in sleep if not dependent(prog[j][pcs[j]], a)}


def sleep_set_search(prog, nvars: int, nlocks: int):
    """Stateful search with sleep sets: (visited states, deadlock states, transitions taken)."""
    s0 = initial(prog, nvars, nlocks)
    asleep: dict = {}  # state -> transitions never taken from it
    visited, dead = set(), set()
    taken = 0
    stack = []

    def enter(s, sleep):
        if s in asleep:
            todo = [i for i in asleep[s] if i not in sleep]  # @line L2
            asleep[s] = asleep[s] & sleep  # @line L3
        else:
            visited.add(s)
            en = enabled(prog, s)
            if not en:
                dead.add(s)
            todo = [i for i in en if i not in sleep]  # @line L4
            asleep[s] = {i for i in en if i in sleep}  # @line L5
        stack.append((s, set(sleep), todo))

    enter(s0, set())  # @line L1
    while stack:
        s, sleep, todo = stack[-1]
        if not todo:
            stack.pop()
            continue
        i = todo.pop(0)  # @line L6
        taken += 1
        t = step(prog, s, i)  # @line L7
        new_sleep = _wake(prog, s, sleep, i)  # @line L8
        sleep.add(i)  # @line L9
        enter(t, new_sleep)  # @line L10
    return visited, dead, taken


def full_search(prog, nvars: int, nlocks: int):
    """Plain search: (reachable states, deadlock states, transitions taken)."""
    s0 = initial(prog, nvars, nlocks)
    seen, todo, dead, taken = {s0}, [s0], set(), 0
    while todo:
        s = todo.pop()
        en = enabled(prog, s)
        if not en:
            dead.add(s)
        for i in en:
            taken += 1
            t = step(prog, s, i)
            if t not in seen:
                seen.add(t)
                todo.append(t)
    return seen, dead, taken


def sleep_set_executions(prog, nvars: int, nlocks: int):
    """Stateless search with sleep sets: (maximal executions, number of blocked branches).

    An execution is the list of threads in the order they moved. A branch is
    blocked when some transition is enabled but all enabled ones are asleep.
    """
    s0 = initial(prog, nvars, nlocks)
    runs, blocked = [], 0
    stack = [(s0, set(), None, [])]
    while stack:
        s, sleep, todo, path = stack[-1]
        if todo is None:
            en = enabled(prog, s)
            if not en:
                runs.append(path)
                stack.pop()
                continue
            todo = [i for i in en if i not in sleep]
            if not todo:
                blocked += 1
            stack[-1] = (s, sleep, todo, path)
        if not todo:
            stack.pop()
            continue
        i = todo.pop(0)
        stack.append((step(prog, s, i), _wake(prog, s, sleep, i), None, path + [i]))
        sleep.add(i)
    return runs, blocked


def sleep_sets(prog, nvars: int, nlocks: int):
    """The deadlock states that the stateful sleep-set search finds."""
    return sleep_set_search(prog, nvars, nlocks)[1]
