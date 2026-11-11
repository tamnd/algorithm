# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/registers-have-consensus-number-one/. The authors are listed in prov/3WR03W.jsonl.
"""Attempts at 2-process consensus with read/write registers. All of them fail.

The theorem says that each attempt must fail agreement, validity or
wait-freedom in some run. The explorer finds such a run:

- write_then_read decides on what it saw. It is wait-free, and it fails
  agreement.
- wait_for_other waits until the other proposal is there. It agrees, and
  it is not wait-free: if the other process stops before its write, it
  reads for ever.
- one_round(f0, f1) is the whole family "write my input, read the other
  register once, decide f(input, value read)". protocol_family() checks
  all 64 x 64 pairs of decision functions and finds no correct one.
"""

import itertools

from explorer import Found, explore


def write_then_read(pid, x):
    yield ("write", ("prop", pid), x)
    r = yield ("read", ("prop", 1 - pid))
    return x if r is None else min(x, r)


def wait_for_other(pid, x):
    yield ("write", ("prop", pid), x)
    while True:
        r = yield ("read", ("prop", 1 - pid))
        if r is not None:
            return min(x, r)


def one_round(f):
    """The protocol: write, read once, decide f[(x, r)]."""

    def proto(pid, x):
        yield ("write", ("prop", pid), x)
        r = yield ("read", ("prop", 1 - pid))
        return f[(x, r)]

    return proto


def setup_for(protos, inputs):
    def setup():
        return {("prop", 0): None, ("prop", 1): None}, [protos[i](i, x) for i, x in enumerate(inputs)]

    return setup


def consensus_check(inputs):
    """Agreement and validity at every state (any state can be the last one before a crash)."""

    def check(w):
        dec = {w.ret[p] for p in range(len(inputs)) if w.done[p]}
        if len(dec) > 1:
            return "agreement fails"
        if dec and not dec <= set(inputs):
            return "validity fails"
        return None

    return check


INPUTS = [(0, 0), (0, 1), (1, 0), (1, 1)]


def verify(protos, max_depth=50):
    """Raise Found if some run on some input breaks agreement, validity or wait-freedom."""
    for inputs in INPUTS:
        try:
            explore(setup_for(protos, inputs), check=consensus_check(inputs), max_depth=max_depth)
        except Found as e:
            raise Found(f"{e.msg} on inputs {inputs}", e.schedule) from None


def all_functions():
    keys = [(x, r) for x in (0, 1) for r in (None, 0, 1)]
    for values in itertools.product((0, 1), repeat=len(keys)):
        yield dict(zip(keys, values))


def protocol_family():
    """Check every pair (f0, f1). Returns (pairs checked, a count of each failure kind)."""
    funcs = list(all_functions())
    kinds = {}
    pairs = 0
    for f0, f1 in itertools.product(funcs, funcs):
        pairs += 1
        try:
            verify([one_round(f0), one_round(f1)])
        except Found as e:
            kind = e.msg.split(" on ")[0]
            kinds[kind] = kinds.get(kind, 0) + 1
            continue
        kinds["correct"] = kinds.get("correct", 0) + 1
    return pairs, kinds
