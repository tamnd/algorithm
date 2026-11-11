# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fetch-and-add/. The authors are listed in prov/FAZZ48.jsonl.
"""Fetch-and-add: two-process consensus, a failed three-process attempt, and tickets.

Each process is a generator for the explorer in explorer.py. A step
("faa", a, d) adds d to the word a and returns the old value, in one
atomic step.
"""


def consensus2(pid, value):
    """Wait-free consensus for processes 0 and 1 with one FAA word and two registers."""
    yield ("write", ("prop", pid), value)      # announce my value
    r = yield ("faa", "x", 1)                  # who came first?
    if r == 0:
        return value                           # I came first: my value wins
    other = yield ("read", ("prop", 1 - pid))  # the other came first, and it wrote first
    return other


def consensus3_attempt(pid, value, n=3):
    """A natural try for three processes. It is wrong.

    The first FAA still wins, but a later process does not know which of
    the others was first. It guesses the lowest id that has proposed.
    """
    yield ("write", ("prop", pid), value)
    r = yield ("faa", "x", 1)
    if r == 0:
        return value
    for q in range(n):
        v = yield ("read", ("prop", q))
        if v is not None:
            return v
    return value


def ticket(pid):
    """Take one ticket from a shared counter."""
    t = yield ("faa", "next", 1)
    return t


def consensus_setup(proto, values):
    """A setup function: process i runs proto(i, values[i])."""

    def setup():
        return {"x": 0}, [proto(i, v) for i, v in enumerate(values)]

    return setup


def agreement_check(values):
    """A check for the explorer: in every state, decided values agree and are inputs."""

    def check(w):
        dec = {w.ret[p] for p in range(len(values)) if w.done[p]}
        if len(dec) > 1:
            return f"disagreement {sorted(dec)}"
        if dec and not dec <= set(values):
            return f"decided a value nobody proposed: {dec}"
        return None

    return check
