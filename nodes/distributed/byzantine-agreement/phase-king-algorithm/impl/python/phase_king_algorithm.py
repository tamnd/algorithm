# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phase-king-algorithm/. The authors are listed in prov/VHXE8S.jsonl.

"""The phase king algorithm for binary Byzantine agreement, n > 3t.

This is the three-round version (Berman, Garay and Perry 1989, as written
in Wattenhofer's lecture notes): t + 1 phases, each with a value round, a
propose round and a king round. The run is a lock-step synchronous
simulation: in each round every process sends, then every process
receives, then every process computes. Faulty processes are Byzantine
and rushing: a seeded strategy picks each of their messages after it has
seen what the honest processes send in that round. Messages are oral
(no signatures), and the channels show the receiver the true sender.
"""

import random
from typing import Callable, Optional

# A strategy is called as strategy(kind, phase, sender, receiver, view, rng)
# and returns the value to send, or None for no message. kind is "value",
# "propose" or "king". view holds the honest state of the round.
Strategy = Callable[[str, int, int, int, dict, random.Random], Optional[int]]


def king_of(phase: int) -> int:
    """The king of phase 1 is process 0, of phase 2 process 1, and so on."""
    return phase - 1


def run(n: int, t: int, inputs: list[int], faulty: set[int], strategy: Strategy, seed: int = 0) -> dict:
    """Run t + 1 phases. Returns the decisions of the honest processes and the costs."""
    assert len(inputs) == n and len(faulty) <= t
    rng = random.Random(seed)
    honest = [p for p in range(n) if p not in faulty]
    x = {p: inputs[p] for p in honest}  # @line L1
    messages = 0
    rounds = 0
    log = []
    for phase in range(1, t + 2):  # @line L2
        # round 1: every process broadcasts value(x)
        view = {"x": dict(x), "phase": phase}
        got = {p: [] for p in honest}  # (sender, value) pairs
        for s in range(n):
            for r in honest:
                v = x[s] if s in x else strategy("value", phase, s, r, view, rng)  # @line L3
                if v is not None:
                    got[r].append((s, v))
        messages += n * len(honest)  # each honest process sends to all n
        rounds += 1
        # round 2: propose y if value(y) came at least n - t times
        prop = {}
        for p in honest:
            c = [0, 0]
            for _, v in got[p]:
                c[v] += 1
            prop[p] = next((y for y in (0, 1) if c[y] >= n - t), None)  # @line L4
        view = {"x": dict(x), "prop": dict(prop), "phase": phase}
        pgot = {p: [0, 0] for p in honest}
        for s in range(n):
            for r in honest:
                v = prop[s] if s in prop else strategy("propose", phase, s, r, view, rng)  # @line L5
                if v is not None:
                    pgot[r][v] += 1
        messages += n * sum(1 for p in honest if prop[p] is not None)
        for p in honest:
            for z in (0, 1):
                if pgot[p][z] > t:
                    x[p] = z  # @line L6
        rounds += 1
        # round 3: the king broadcasts its x; keep x only with n - t propose(x)
        k = king_of(phase)
        view = {"x": dict(x), "pgot": {p: list(c) for p, c in pgot.items()}, "phase": phase}
        kept = {}
        king_value = x.get(k)  # @line L7
        if k in x:
            messages += n
        for p in honest:
            if k in x:
                w = king_value
            else:
                w = strategy("king", phase, k, p, view, rng)
            if w is None:
                w = 0  # a missing king message is read as 0
            kept[p] = pgot[p][x[p]] >= n - t  # @line L8
            if not kept[p]:
                x[p] = w  # @line L9
        rounds += 1
        counts = {p: [sum(1 for _, v in got[p] if v == b) for b in (0, 1)] for p in honest}
        log.append({"phase": phase, "king": k, "values": counts, "prop": dict(prop), "pgot": {p: list(c) for p, c in pgot.items()}, "x": dict(x), "kept": kept})
    return {"decision": dict(x), "rounds": rounds, "messages": messages, "log": log}  # @line L10


def check(inputs: list[int], faulty: set[int], res: dict) -> list[str]:
    """The safety properties: agreement, and strong validity for binary values."""
    bad = []
    d = res["decision"]
    if len(set(d.values())) > 1:
        bad.append("agreement")
    hv = {inputs[p] for p in d}
    if len(hv) == 1 and set(d.values()) != hv:
        bad.append("validity")
    return bad


# ---- Byzantine strategies --------------------------------------------------

def silent(kind, phase, s, r, view, rng):
    return None


def random_values(kind, phase, s, r, view, rng):
    return rng.choice([0, 1, None])


def equivocate(kind, phase, s, r, view, rng):
    """Send 0 to the receivers with an even index and 1 to the others."""
    return r % 2


def oppose(kind, phase, s, r, view, rng):
    """Push each receiver away from its own current value."""
    return 1 - view["x"][r]


def make_split(group_a: set[int]) -> Strategy:
    """The attack for n = 3t: tell group A 0 and everyone else 1, in every
    round, also as king. With n > 3t it cannot work; with n = 3t it keeps
    the two groups apart for ever."""
    def strat(kind, phase, s, r, view, rng):
        return 0 if r in group_a else 1
    return strat


def king_attack(kind, phase, s, r, view, rng):
    """As king, send each receiver the value that it does not hold; else oppose."""
    return 1 - view["x"][r]


STRATEGIES = {"silent": silent, "random": random_values, "equivocate": equivocate, "oppose": oppose, "king": king_attack}


if __name__ == "__main__":
    res = run(4, 1, [0, 1, 1, 0], {3}, equivocate, 1)
    print(res["decision"], res["rounds"], res["messages"])
