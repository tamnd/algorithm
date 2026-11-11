# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cas-has-infinite-consensus-number/. The authors are listed in prov/MGMTMQ.jsonl.
"""Wait-free consensus for any number of processes with one CAS word.

The word starts as None (the value bottom, which is not an input). The
first CAS from None installs its input; every later CAS fails and leaves
the word as it is. So every process learns the winner.

Two forms of the primitive:

- cmpxchg returns the old value: one step per process.
- a CAS that returns only True or False needs one read afterwards.
"""

from explorer import explore, random_run


def cas_decide(pid, v):
    """One cmpxchg step."""
    old = yield ("cmpxchg", "x", None, v)
    return v if old is None else old


def bool_cas_decide(pid, v):
    """A boolean CAS, then a read of the word."""
    if (yield ("cas", "x", None, v)):
        return v
    return (yield ("read", "x"))


def setup_for(proto, inputs):
    def setup():
        return {"x": None}, [proto(i, v) for i, v in enumerate(inputs)]

    return setup


def consensus_check(inputs):
    """Agreement and validity at every state. Any state may be the last one
    for a process that crashes there, so checking every state covers crashes."""

    def check(w):
        dec = {w.ret[p] for p in range(len(inputs)) if w.done[p]}
        if len(dec) > 1:
            return "agreement fails"
        if dec and not dec <= set(inputs):
            return "validity fails"
        return None

    return check


def verify(proto, inputs):
    """Every interleaving. Returns (states, finals, most steps of one process)."""
    worst = [0]
    check = consensus_check(inputs)

    def c(w):
        worst[0] = max(worst[0], *w.steps)
        return check(w)

    states, finals = explore(setup_for(proto, inputs), check=c, max_depth=50)
    return states, finals, worst[0]


def random_with_crashes(proto, n, seed):
    """A random schedule where about a third of the processes crash, before
    their first step or after it.

    Returns the set of decided values, and whether every process that did
    not crash decided.
    """
    crash = {p: (seed + p) % 2 for p in range(n) if (p * 7 + seed) % 3 == 0}
    w = random_run(setup_for(proto, [f"v{i}" for i in range(n)]), seed, crash=crash)
    dec = {w.ret[p] for p in range(n) if w.done[p]}
    live_decided = all(w.done[p] for p in range(n) if p not in crash)
    return dec, live_decided
