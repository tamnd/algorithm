# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rabin-randomized-byzantine-agreement/. The authors are listed in prov/93SCFK.jsonl.

"""Randomized binary Byzantine agreement with a dealer's common coin, after
Rabin (1983), in a synchronous form with n >= 8t + 1.

Thresholds: L = floor(n/2) + t + 1, H = L + t, G = L + 2t. In each round
every process sends its value; the common coin of the round picks the
threshold T in {L, H}; a process keeps the majority value if its tally
reaches T and takes 0 otherwise, and decides if the tally reaches G.

The dealer is modelled as unforgeable tokens: before the run it gives each
process a signed share of the coin of every round. A coin is rebuilt from
t + 1 valid shares, and a forged share is not a token, so it is ignored.
"""

import random


class Dealer:
    def __init__(self, n, t, seed):
        self.n, self.t = n, t
        self.rng = random.Random(seed)
        self.coins = {}
        self.tokens = set()

    def share(self, r, i):
        if r not in self.coins:
            self.coins[r] = self.rng.randrange(2)
        tok = ("share", r, i, self.coins[r])
        self.tokens.add(tok)
        return tok

    def reconstruct(self, r, shares):
        valid = {s for s in shares if s in self.tokens and s[1] == r}
        if len({s[2] for s in valid}) < self.t + 1:
            return None
        return valid.pop()[3]  # valid shares of one round all carry its coin


def thresholds(n, t):
    low = n // 2 + t + 1
    return low, low + t, low + 2 * t


def adversary(strategy, rng, n, t, honest, values, low, high, fixed):
    """Messages of the faulty processes to each honest process: a dict
    honest id -> list of values (one per faulty sender, None = silent)."""
    if strategy == "silent":
        return {i: [] for i in honest}
    if strategy == "random":
        return {i: [rng.choice((0, 1, None)) for _ in range(t)] for i in honest}
    if strategy == "wrong":
        ones = sum(values[i] for i in honest)
        minority = 0 if 2 * ones > len(honest) else 1
        return {i: [minority] * t for i in honest}
    # "straddle": keep the honest processes split around a threshold. The
    # faulty processes send 1 to some honest processes and 0 to the others,
    # so the tallies of 1 differ by t and some processes reach the threshold
    # while others do not. Without a coin the threshold is known; with the
    # coin the adversary must guess it.
    a = sum(values[i] for i in honest)
    target = fixed if fixed is not None else rng.choice((low, high))
    want = rng.choice((low - 1, high - 1)) if fixed is None else low - 1
    want = max(0, min(len(honest), want))
    if not (target - t <= a < target):
        return {i: [rng.choice((0, 1))] * t for i in honest}
    order = sorted(honest)
    return {i: [1 if k < want else 0] * t for k, i in enumerate(order)}


def run(n, t, faulty, strategy, inputs, seed=0, coin=True, max_rounds=200):
    """Run until every honest process has decided. (A real process runs one
    more round after it decides, so that the others can decide; here all
    have decided, so that round is not simulated.) With coin=False the
    threshold is always L. Returns a dict with the decisions, the round of
    each decision, the rounds run and the number of messages."""
    rng = random.Random(seed)
    dealer = Dealer(n, t, seed * 7919 + 1)
    low, high, good = thresholds(n, t)
    honest = [i for i in range(n) if i not in faulty]
    v = {i: inputs[i] for i in honest}
    decided, when = {}, {}
    messages = 0
    for r in range(1, max_rounds + 1):
        if decided and all(i in decided and when[i] < r for i in honest):
            return {"decisions": decided, "when": when, "rounds": r - 1, "messages": messages}
        fixed = None if coin else low
        bad = adversary(strategy, rng, n, t, honest, v, low, high, fixed)
        values = {i: [v[j] for j in honest] + bad[i] for i in honest}  # @line L1
        messages += n * (n - 1)
        shares = [dealer.share(r, i) for i in honest]
        forged = [("share", r, j, rng.randrange(2)) for j in faulty]
        messages += n * (n - 1)
        new = {}
        for i in honest:
            got = [x for x in values[i] if x is not None]
            ones = got.count(1)
            maj, tally = (1, ones) if 2 * ones > len(got) else (0, len(got) - ones)  # @line L2
            s = dealer.reconstruct(r, shares + forged) if coin else 0  # @line L3
            threshold = low if s == 0 else high  # @line L4
            new[i] = maj if tally >= threshold else 0  # @line L5
            if tally >= good and i not in decided:
                decided[i], when[i] = maj, r  # @line L6
        v = new
    return {"decisions": decided, "when": when, "rounds": None, "messages": messages}


def check(res, honest, inputs):
    """Agreement, validity and termination of one run; returns the errors."""
    errs = []
    d = res["decisions"]
    if res["rounds"] is None or set(d) != set(honest):
        errs.append("termination")
    if len(set(d.values())) > 1:
        errs.append("agreement")
    vals = {inputs[i] for i in honest}
    if len(vals) == 1 and set(d.values()) - vals:
        errs.append("validity")
    return errs


def mean_rounds(n, t, strategy, runs, coin=True):
    """Mean of the last decision round over seeded runs with random inputs."""
    total = 0
    for seed in range(runs):
        rng = random.Random(10_000 + seed)
        faulty = set(rng.sample(range(n), t))
        inputs = [rng.randrange(2) for _ in range(n)]
        res = run(n, t, faulty, strategy, inputs, seed=seed, coin=coin)
        assert check(res, [i for i in range(n) if i not in faulty], inputs) == []
        total += max(res["when"].values())
    return total / runs


if __name__ == "__main__":
    for strat in ("silent", "random", "wrong", "straddle"):
        print(strat, mean_rounds(17, 2, strat, 300))
