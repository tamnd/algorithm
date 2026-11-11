# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linearizability/. The authors are listed in prov/68Z96K.jsonl.
"""Linearizability: the example histories of the page, and a random history maker.

The checker itself is in lincheck.py. This module holds the histories that
the page discusses, so that the tests can check each claim of the page.
"""

from lincheck import Objects, Queue

# p0 enqueues x and p1 enqueues y at overlapping times, then p0 dequeues y.
# The two enqueues overlap, so either order is allowed.
OVERLAP = [
    ("inv", 0, "enq", "x"),
    ("inv", 1, "enq", "y"),
    ("res", 1, None),
    ("res", 0, None),
    ("inv", 0, "deq", None),
    ("res", 0, "y"),
]

# enq(x) ends before enq(y) starts, and then deq returns y. Real time forces
# x to be first, so this is not linearizable. Each process alone sees a
# legal order (y, then x, then the deq of p0), so it is sequentially
# consistent.
SC_NOT_LIN = [
    ("inv", 0, "enq", "x"),
    ("res", 0, None),
    ("inv", 1, "enq", "y"),
    ("res", 1, None),
    ("inv", 0, "deq", None),
    ("res", 0, "y"),
]

# A write of 1 ends, and then a read returns the old value 0.
STALE_READ = [
    ("inv", 0, "write", 1),
    ("res", 0, None),
    ("inv", 1, "read", None),
    ("res", 1, 0),
]

# Sequential consistency is not local. Two queues p and q. Each projection is
# sequentially consistent, but the whole history is not.
NOT_LOCAL = [
    ("inv", 0, ("p", "enq"), "x"),
    ("res", 0, None),
    ("inv", 1, ("q", "enq"), "y"),
    ("res", 1, None),
    ("inv", 0, ("q", "enq"), "x"),
    ("res", 0, None),
    ("inv", 1, ("p", "enq"), "y"),
    ("res", 1, None),
    ("inv", 0, ("p", "deq"), None),
    ("res", 0, "y"),
    ("inv", 1, ("q", "deq"), None),
    ("res", 1, "x"),
]

TWO_QUEUES = Objects({"p": Queue(), "q": Queue()})

# p0 starts enq(x) and never responds. p1 dequeues x. The pending enq must be
# placed before the deq, and that is allowed.
PENDING_SEEN = [
    ("inv", 0, "enq", "x"),
    ("inv", 1, "deq", None),
    ("res", 1, "x"),
]

# The same, but p1 dequeues nothing. The pending enq is left out.
PENDING_UNSEEN = [
    ("inv", 0, "enq", "x"),
    ("inv", 1, "deq", None),
    ("res", 1, None),
]


def random_history(rng, nproc=3, nops=5, objects=("p", "q"), values=("a", "b")):
    """A random history of queue operations on several queues.

    Responses are random too, so most histories are not linearizable.
    The result is used to test locality: the history is linearizable if
    and only if each projection on one object is.
    """
    hist, open_, started = [], {}, 0
    while started < nops or open_:
        p = rng.randrange(nproc)
        if p in open_:
            obj, m = open_.pop(p)
            if m == "enq":
                hist.append(("res", p, None))
            else:
                hist.append(("res", p, rng.choice((None,) + values)))
        elif started < nops:
            obj, m = rng.choice(objects), rng.choice(("enq", "deq"))
            arg = rng.choice(values) if m == "enq" else None
            hist.append(("inv", p, (obj, m), arg))
            open_[p] = (obj, m)
            started += 1
    return hist


def single(history):
    """Map (obj, m) names to m, for one object."""
    out = []
    for e in history:
        out.append(e[:2] + (e[2][1],) + e[3:] if e[0] == "inv" else e)
    return out
