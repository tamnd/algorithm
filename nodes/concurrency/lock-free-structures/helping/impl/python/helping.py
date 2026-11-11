# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/helping/. The authors are listed in prov/4QNG5W.jsonl.
"""Helping in the Michael and Scott queue.

An enqueue makes two changes: it links the new node after the last node
(the linearization point), and then it moves Tail to the new node. Between
the two steps, Tail lags one node behind. With help=True, any operation
that sees the lag moves Tail itself with a CAS, as in the 1996 paper. With
help=False, it only retries and waits for the enqueuer to move Tail.

If the enqueuer stops between its two steps, the version without help
blocks every other enqueue for ever, so it is not lock-free; the version
with help goes on.
"""

from explorer import World, solo

DUMMY = ("dummy", 0)


def nxt(node):
    return ("next", node)


def val(node):
    return ("val", node)


def enqueue(v, node, help):
    yield ("inv", "enq", v)
    yield ("write", val(node), v)
    yield ("write", nxt(node), None)
    while True:
        t = yield ("read", "Tail")
        n = yield ("read", nxt(t))
        if t == (yield ("read", "Tail")):
            if n is None:
                if (yield ("cas", nxt(t), None, node)):
                    yield ("cas", "Tail", t, node)
                    yield ("res", None)
                    return
            elif help:
                yield ("cas", "Tail", t, n)


def dequeue(help):
    yield ("inv", "deq", None)
    while True:
        h = yield ("read", "Head")
        t = yield ("read", "Tail")
        n = yield ("read", nxt(h))
        if h == (yield ("read", "Head")):
            if h == t:
                if n is None:
                    yield ("res", None)
                    return
                if help:
                    yield ("cas", "Tail", t, n)
            else:
                v = yield ("read", val(n))
                if (yield ("cas", "Head", h, n)):
                    yield ("res", v)
                    return


def program(pid, ops, help):
    for k, (name, arg) in enumerate(ops):
        if name == "enq":
            yield from enqueue(arg, (pid, k), help)
        else:
            yield from dequeue(help)


def setup_for(programs, help=True):
    def setup():
        mem = {"Head": DUMMY, "Tail": DUMMY, nxt(DUMMY): None}
        return mem, [program(p, ops, help) for p, ops in enumerate(programs)]

    return setup


def stop_after_link(help):
    """p0 enqueues and stops right after its link CAS; then p1 runs alone.

    Returns the outcome of p1's solo run: "done" or "loop".
    """
    w = World(setup_for([[("enq", "a")], [("enq", "b")]], help))
    while True:
        op = w.next[0]
        r = w.step(0)
        if op[0] == "cas" and op[1] != "Tail" and r:
            break
    outcome, _ = solo(w, 1, 200)
    return outcome
