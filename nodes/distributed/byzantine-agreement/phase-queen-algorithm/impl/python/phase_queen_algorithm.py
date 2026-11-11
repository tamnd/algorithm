# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phase-queen-algorithm/. The authors are listed in prov/P9R1W2.jsonl.

"""The phase queen algorithm for binary Byzantine agreement, n > 4t.

Berman and Garay (1989): t + 1 phases of two rounds. In round 1 every
process broadcasts its value; in round 2 the queen of the phase
broadcasts the majority value it saw. A process keeps its own majority
only if it saw it more than n/2 + t times; else it takes the queen's value.

The run is a lock-step synchronous simulation with oral messages and a
static, rushing Byzantine adversary given by a seeded strategy.
"""

import random
from typing import Callable, Optional

# strategy(kind, phase, sender, receiver, view, rng) -> bit or None;
# kind is "value" or "queen".
Strategy = Callable[[str, int, int, int, dict, random.Random], Optional[int]]


def queen_of(phase: int) -> int:
    """The queen of phase 1 is process 0, of phase 2 process 1, and so on."""
    return phase - 1


def run(n: int, t: int, inputs: list[int], faulty: set[int], strategy: Strategy, seed: int = 0) -> dict:
    """Run t + 1 phases. Returns the honest decisions, the costs and a log."""
    assert len(inputs) == n and len(faulty) <= t
    rng = random.Random(seed)
    honest = [p for p in range(n) if p not in faulty]
    x = {p: inputs[p] for p in honest}  # @line L1
    messages = rounds = 0
    log = []
    for phase in range(1, t + 2):  # @line L2
        view = {"x": dict(x), "phase": phase, "n": n}
        cnt = {p: [0, 0] for p in honest}
        for s in range(n):
            for r in honest:
                v = x[s] if s in x else strategy("value", phase, s, r, view, rng)  # @line L3
                if v is not None:
                    cnt[r][v] += 1
        messages += n * len(honest)
        rounds += 1
        maj, mult = {}, {}
        for p in honest:
            maj[p] = 1 if cnt[p][1] > cnt[p][0] else 0  # @line L4
            mult[p] = cnt[p][maj[p]]
        q = queen_of(phase)
        view = {"x": dict(x), "maj": dict(maj), "mult": dict(mult), "phase": phase, "n": n}
        if q in x:
            messages += n  # @line L5
        new = {}
        for p in honest:
            if 2 * mult[p] > n + 2 * t:  # mult > n/2 + t
                new[p] = maj[p]  # @line L6
            else:
                w = maj[q] if q in x else strategy("queen", phase, q, p, view, rng)
                new[p] = 0 if w is None else w  # @line L7
        x = new
        rounds += 1
        log.append({"phase": phase, "queen": q, "counts": {p: list(c) for p, c in cnt.items()}, "maj": maj, "mult": mult, "x": dict(x)})
    return {"decision": dict(x), "rounds": rounds, "messages": messages, "log": log}  # @line L8


def check(inputs: list[int], faulty: set[int], res: dict) -> list[str]:
    """Agreement, and strong validity for binary values."""
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
    """Send 0 to receivers with an even index and 1 to the others."""
    return r % 2


def oppose(kind, phase, s, r, view, rng):
    """Push each receiver away from its own value."""
    return 1 - view["x"][r]


def weaken(kind, phase, s, r, view, rng):
    """Vote against the honest majority, so that honest counts fall to the
    threshold, and as queen send each receiver the bit it does not hold."""
    if kind == "value":
        ones = sum(view["x"].values())
        return 0 if 2 * ones >= len(view["x"]) else 1
    return 1 - view["maj"][r]


STRATEGIES = {"silent": silent, "random": random_values, "equivocate": equivocate, "oppose": oppose, "weaken": weaken}


def last_queen_attack(kind, phase, s, r, view, rng):
    """The attack for n = 4t when the last queen is faulty. In round 1 the
    faulty processes send the opposite of the common honest value, so each
    honest count is n - t = n/2 + t, which is not above the threshold. As
    the last queen, send 0 to even receivers and 1 to odd ones."""
    if kind == "value":
        return 1 - view["x"][r]
    return r % 2


if __name__ == "__main__":
    res = run(5, 1, [1, 0, 1, 1, 0], {4}, weaken, 0)
    print(res["decision"], res["rounds"], res["messages"])
