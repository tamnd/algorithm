# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/consensus-number/. The authors are listed in prov/FQYCHK.jsonl.
"""Wait-free consensus protocols from the consensus hierarchy.

Each protocol is a generator for the explorer in explorer.py. Process pid
proposes value and returns the value it decides. The two-process protocols
share a pattern: write my value to prop[pid], take one step on the shared
object, and use its answer to learn who was first. If I was first, I decide
my value; if not, the winner wrote its value before its step, so I read it.

The CAS protocol works for any n: the first CAS installs its value, and
every process reads the winner from the answer of its own CAS.
"""

from explorer import World, explore, solo


def tas2(pid, value):
    """Test-and-set, 2 processes. Consensus number 2."""
    yield ("write", ("prop", pid), value)
    if (yield ("tas", "t")) == 0:
        return value
    return (yield ("read", ("prop", 1 - pid)))


def faa2(pid, value):
    """Fetch-and-add, 2 processes. Consensus number 2."""
    yield ("write", ("prop", pid), value)
    if (yield ("faa", "c", 1)) == 0:
        return value
    return (yield ("read", ("prop", 1 - pid)))


def swap2(pid, value):
    """Swap, 2 processes. Consensus number 2. The word starts as None."""
    yield ("write", ("prop", pid), value)
    if (yield ("swap", "s", pid)) is None:
        return value
    return (yield ("read", ("prop", 1 - pid)))


def queue2(pid, value):
    """A queue that holds ("win", "lose"). Consensus number 2."""
    yield ("write", ("prop", pid), value)
    if (yield ("deq", "q")) == "win":
        return value
    return (yield ("read", ("prop", 1 - pid)))


def stack2(pid, value):
    """A stack that holds ("lose", "win"), with "win" on top. Consensus number 2."""
    yield ("write", ("prop", pid), value)
    if (yield ("pop", "st")) == "win":
        return value
    return (yield ("read", ("prop", 1 - pid)))


def cas_n(pid, value):
    """Compare-and-swap, any number of processes. Consensus number infinity.

    One step: CAS the word from None to my value. The answer is the old
    value. If it was None, I won; if not, it is the winner's value.
    """
    old = yield ("cmpxchg", "x", None, value)
    return value if old is None else old


def tas3_attempt(pid, value, n=3):
    """A natural try with test-and-set for 3 processes. It is wrong.

    A loser knows that it lost, but not which of the other two won. It
    guesses the lowest id that has written a proposal.
    """
    yield ("write", ("prop", pid), value)
    if (yield ("tas", "t")) == 0:
        return value
    for q in range(n):
        v = yield ("read", ("prop", q))
        if v is not None:
            return v
    return value


PROTOCOLS = {"tas": tas2, "faa": faa2, "swap": swap2, "queue": queue2, "stack": stack2, "cas": cas_n}


def setup_for(proto, values):
    def setup():
        mem = {"t": 0, "c": 0, "s": None, "q": ("win", "lose"), "st": ("lose", "win"), "x": None}
        return mem, [proto(i, v) for i, v in enumerate(values)]

    return setup


def agreement_check(values):
    """At every state: the decided values agree and were proposed.

    The check runs at every state, not only at the end, because any state
    can be the last one for a process that crashes there.
    """

    def check(w):
        dec = {w.ret[p] for p in range(len(values)) if w.done[p]}
        if len(dec) > 1:
            return f"disagreement {sorted(dec)}"
        if dec and not dec <= set(values):
            return f"decided a value nobody proposed: {dec}"
        return None

    return check


def verify(proto, values, max_depth=100):
    """Explore every interleaving. Raises Found on a broken property.

    Returns (states, finals, worst) where worst is the most steps any process
    takes in any run. Every run ends (explore checks for cycles and long
    runs), so the protocol is wait-free on this input.
    """
    setup = setup_for(proto, values)
    worst = [0]

    def check(w):
        worst[0] = max(worst[0], *w.steps)
        return agreement_check(values)(w)

    states, finals = explore(setup, check=check, max_depth=max_depth)
    return states, finals, worst[0]


def solo_from_start(proto, values, p):
    """Steps that process p takes alone from the start."""
    w = World(setup_for(proto, values))
    return solo(w, p, 50)
