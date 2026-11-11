# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/feldman-micali-byzantine-agreement/. The authors are listed in prov/P7QJJH.jsonl.

"""The reduction of Feldman and Micali (STOC 1988, SIAM J. Comput. 1997):
synchronous binary Byzantine agreement for n >= 3t + 1 from graded
consensus and a common coin, in constant expected rounds.

The coin is an oracle here. Feldman and Micali build it from verifiable
secret sharing and gradecast; this file does not. The modes are:
  "ideal"     a fair bit that all honest processes see, drawn after the
              messages of the iteration (the adversary cannot predict it);
  "weak"      with probability 1/2 an ideal common bit, otherwise the
              adversary chooses each process's bit (a coin that is common
              only with constant probability, as Feldman and Micali's is);
  "predicted" the adversary knows the bit in advance and picks it.
"""

import random

BOT = None  # the empty proposal


def adversary_round(strategy, rng, t, honest, sent, target, k_reach):
    """The messages of the t faulty processes to each honest process in one
    round: honest id -> list of values. `sent` maps each honest process to
    what it sent this round."""
    if strategy == "silent":
        return {i: [] for i in honest}
    if strategy == "random":
        return {i: [rng.choice((0, 1, BOT)) for _ in range(t)] for i in honest}
    if strategy == "equivocate":
        return {i: [k % 2] * t for k, i in enumerate(sorted(honest))}
    if strategy == "mirror":  # each honest process hears its own value back
        return {i: [sent[i]] * t for i in honest}
    # "split": give `target` to the first k_reach honest processes only.
    order = sorted(honest)
    return {i: ([target] * t if k < k_reach else [1 - target if target in (0, 1) else BOT] * t) for k, i in enumerate(order)}


def counts(msgs):
    c = {}
    for x in msgs:
        if x is not BOT:
            c[x] = c.get(x, 0) + 1
    return c


def run(n, t, faulty, strategy, inputs, seed=0, coin="ideal", max_iters=100):
    """Iterate until every honest process has decided. Returns decisions,
    the iteration of each decision, the iterations and rounds run, and the
    number of messages (the coin's own messages are not counted)."""
    rng = random.Random(seed)
    honest = sorted(i for i in range(n) if i not in faulty)
    v = {i: inputs[i] for i in honest}
    decided, when = {}, {}
    messages = 0
    for it in range(1, max_iters + 1):
        if decided and all(i in decided and when[i] < it for i in honest):
            return {"decisions": decided, "when": when, "iterations": it - 1, "rounds": 2 * (it - 1), "messages": messages}
        # The split attack: aim at the value held by more honest processes,
        # make exactly one honest process propose it, and give grade 1 to
        # a chosen number of honest processes.
        ones = sum(v[i] for i in honest)
        target = 1 if 2 * ones >= len(honest) else 0
        need = n - t - sum(1 for i in honest if v[i] == target)
        # Round 1: values. A process proposes w if it sees n - t copies.
        bad = adversary_round(strategy, rng, t, honest, v, target, 1 if 0 <= need <= t else 0)
        x = {}
        for i in honest:
            c = counts([v[j] for j in honest] + bad[i])  # @line L1
            w = [a for a, k in c.items() if k >= n - t]
            x[i] = w[0] if w else BOT
        messages += n * (n - 1)
        # Round 2: proposals and grades.
        k_reach = rng.randint(t + 1, max(t + 1, n - 2 * t - 1))
        bad = adversary_round(strategy, rng, t, honest, x, target, k_reach)
        y, g = {}, {}
        for i in honest:
            c = counts([x[j] for j in honest] + bad[i])  # @line L2
            w, cw = max(c.items(), key=lambda p: (p[1], p[0])) if c else (BOT, 0)
            if cw >= n - t:
                y[i], g[i] = w, 2  # @line L3
            elif cw >= t + 1:
                y[i], g[i] = w, 1
            else:
                y[i], g[i] = v[i], 0
        messages += n * (n - 1)
        # The coin, revealed only now.
        if coin == "ideal":
            s = rng.randrange(2)  # @line L4
            bits = {i: s for i in honest}
        elif coin == "weak":
            s = rng.randrange(2)
            common = rng.random() < 0.5
            bits = {i: (s if common else 1 - target) for i in honest}
        else:  # "predicted": the adversary picks the bit that hurts most
            bits = {i: 1 - target for i in honest}
        for i in honest:
            v[i] = y[i] if g[i] >= 1 else bits[i]  # @line L5
            if g[i] == 2 and i not in decided:
                decided[i], when[i] = y[i], it  # @line L6
    return {"decisions": decided, "when": when, "iterations": None, "rounds": None, "messages": messages}


def check(res, honest, inputs):
    errs = []
    d = res["decisions"]
    if res["iterations"] is None or set(d) != set(honest):
        errs.append("termination")
    if len(set(d.values())) > 1:
        errs.append("agreement")
    vals = {inputs[i] for i in honest}
    if len(vals) == 1 and set(d.values()) - vals:
        errs.append("validity")
    return errs


def mean_iterations(n, t, strategy, runs, coin="ideal", inputs=None):
    total = 0
    for seed in range(runs):
        rng = random.Random(20_000 + seed)
        faulty = set(rng.sample(range(n), t))
        inp = inputs or [rng.randrange(2) for _ in range(n)]
        res = run(n, t, faulty, strategy, inp, seed=seed, coin=coin)
        assert check(res, [i for i in range(n) if i not in faulty], inp) == []
        total += max(res["when"].values())
    return total / runs


if __name__ == "__main__":
    for coin in ("ideal", "weak"):
        for strat in ("silent", "random", "equivocate", "mirror", "split"):
            print(coin, strat, mean_iterations(10, 3, strat, 300, coin=coin))
