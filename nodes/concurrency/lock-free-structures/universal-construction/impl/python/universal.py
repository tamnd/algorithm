# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/universal-construction/. The authors are listed in prov/TT2P8N.jsonl.
"""Herlihy's universal construction, in the form of Herlihy and Shavit
(The Art of Multiprocessor Programming, Chapter 6), for the explorer.

The object is a log: a list of nodes, one for each operation, that starts at
a sentinel TAIL. Each node has a one-shot consensus object that decides the
next node. A process appends its node by consensus, then computes its
response by applying the operations of the log, from the start, to a fresh
copy of the sequential object.

Shared words (cells of the explorer memory), for a node X:

    ("seq", X)        0 until X is in the log, then its position (TAIL is 1)
    ("next", X)       the node after X, once it is known
    ("dn", X)         the consensus object of X: the step ("decide", ("dn", X), v)
    ("head", i)       the last node in the log that process i knows
    ("announce", i)   the node of the operation of process i (wait-free form)

A missing cell reads as None, so a fresh node has seq 0 and no next node.
A node is the tuple ("N", pid, k, (name, arg)): the k-th operation of pid.
"""

from explorer import World

TAIL = ("N", -1, 0, None)


def initial_memory(n):
    mem = {("seq", TAIL): 1}
    for j in range(n):
        mem[("head", j)] = TAIL
        mem[("announce", j)] = TAIL
    return mem


def seq_of(x):
    s = yield ("read", ("seq", x))
    return s or 0


def max_head(n):
    """The node with the largest seq among the heads, and its seq."""
    best, bs = None, -1
    for j in range(n):
        h = yield ("read", ("head", j))
        s = yield from seq_of(h)
        if s > bs:
            best, bs = h, s
    return best, bs


def replay(node, obj):
    """Apply the log from the start up to node; return the response of node."""
    state = obj.init
    cur = yield ("read", ("next", TAIL))
    while True:
        name, arg = cur[3]
        state, r = obj.apply(state, name, arg, cur[1])
        if cur == node:
            return r
        cur = yield ("read", ("next", cur))


def append(before, bseq, after, i):
    """Record that after follows before (any process may do it, with the same values)."""
    yield ("write", ("next", before), after)
    yield ("write", ("seq", after), bseq + 1)
    yield ("write", ("head", i), after)


def lf_apply(i, n, node, obj):
    """The lock-free form: propose my own node at the end of the log until it wins."""
    iters = 0
    while (yield from seq_of(node)) == 0:
        iters += 1
        before, bseq = yield from max_head(n)
        after = yield ("decide", ("dn", before), node)
        yield from append(before, bseq, after, i)
    r = yield from replay(node, obj)
    return r, iters


def wf_apply(i, n, node, obj):
    """The wait-free form: announce my node; at position p, every process
    proposes the announced node of process p mod n if it is not in the log
    yet, and its own node otherwise."""
    yield ("write", ("announce", i), node)
    before, bseq = yield from max_head(n)
    yield ("write", ("head", i), before)
    iters = 0
    while (yield from seq_of(node)) == 0:
        iters += 1
        other = yield ("read", ("announce", (bseq + 1) % n))
        prefer = other if (yield from seq_of(other)) == 0 else node
        after = yield ("decide", ("dn", before), prefer)
        yield from append(before, bseq, after, i)
        before, bseq = after, bseq + 1
    yield ("write", ("head", i), node)
    r = yield from replay(node, obj)
    return r, iters


def program(i, n, ops, obj, wait_free=True):
    """Run the operations of process i. Returns the loop count of each one."""
    stats = []
    apply = wf_apply if wait_free else lf_apply
    for k, (name, arg) in enumerate(ops):
        node = ("N", i, k, (name, arg))
        yield ("inv", name, arg)
        r, iters = yield from apply(i, n, node, obj)
        yield ("res", r)
        stats.append(iters)
    return stats


def setup_for(programs, obj, wait_free=True):
    n = len(programs)

    def setup():
        return initial_memory(n), [program(i, n, ops, obj, wait_free) for i, ops in enumerate(programs)]

    return setup


def forever(i, n, obj, wait_free):
    """Process i enqueues 0, 1, 2, ... for ever."""
    apply = wf_apply if wait_free else lf_apply
    k = 0
    while True:
        node = ("N", i, k, ("enq", k))
        yield from apply(i, n, node, obj)
        k += 1


def race(obj, wait_free, n=2, head_start=0, rounds=2000):
    """Process 0 does one dequeue; processes 1 .. n-1 enqueue for ever.

    First the others run head_start steps each. Then the adversary runs
    process 0, except that just before process 0 calls decide on a consensus
    object that is still open, the others run (one step each, in turn) until
    that object is decided. So the others win every consensus they can win.
    Returns (process 0 done, its loop count or None, nodes of the others in
    the log).
    """

    def setup():
        progs = [program(0, n, [("deq", None)], obj, wait_free)]
        progs += [forever(j, n, obj, wait_free) for j in range(1, n)]
        return initial_memory(n), progs

    w = World(setup)
    for _ in range(head_start):
        for j in range(1, n):
            w.step(j)
    for _ in range(rounds):
        if w.done[0]:
            break
        op = w.next[0]
        if op[0] == "decide" and w.mem.get(op[1]) is None:
            while w.mem.get(op[1]) is None:
                for j in range(1, n):
                    w.step(j)
        else:
            w.step(0)
    others = len({r for _, op, r in w.trace if op[0] == "decide" and r[1] != 0})
    return w.done[0], (w.ret[0][0] if w.done[0] else None), others
