# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimistic-hedge/. The authors are listed in prov/259HJ8.jsonl.
"""Optimistic Hedge (optimistic multiplicative weights) on k actions with losses in [0, 1].

After it sees the loss vector l of a round, the learner multiplies the weight of action a by
exp(-eta (2 l(a) - m(a))), where m is the loss vector of the round before (0 before the
first round), and normalizes. This is Hedge on the cumulative losses plus one extra copy of
the last loss, used as a prediction of the next one. Arithmetic is in float.
"""

import math


class OptimisticHedge:
    """An online learner. Call distribution() to get the current x, then update(loss)."""

    def __init__(self, k, eta):
        if k < 1 or eta <= 0:
            raise ValueError("need k >= 1 and eta > 0")
        self.eta = eta
        self.x = [1.0 / k] * k  # @line L1
        self.z = [0.0] * k
        self.m = [0.0] * k  # @line L2

    def distribution(self):
        return list(self.x)

    def update(self, loss):
        eta = self.eta
        # The weights are kept as logarithms z(a), so that no weight underflows; x is the softmax of z.
        for a in range(len(self.z)):  # @line L5
            self.z[a] -= eta * (2 * loss[a] - self.m[a])  # @line L6
        top = max(self.z)
        w = [math.exp(e - top) for e in self.z]
        total = sum(w)
        self.x = [v / total for v in w]  # @line L7
        self.m = list(loss)  # @line L8


def play(k, T, eta, adversary):
    """Run optimistic Hedge for T rounds against adversary(t, x), which returns the loss vector
    of round t and may look at the current distribution x. Return the distributions and losses."""
    learner = OptimisticHedge(k, eta)
    xs, losses = [], []
    for t in range(T):  # @line L3
        x = learner.distribution()
        loss = adversary(t, x)  # @line L4
        learner.update(loss)
        xs.append(x)
        losses.append(list(loss))
    return xs, losses


def regret(xs, losses):
    """Return sum_t x_t . l_t minus the least total loss of a fixed action."""
    if not xs:
        return 0.0
    k = len(xs[0])
    mine = sum(sum(a * b for a, b in zip(x, l)) for x, l in zip(xs, losses))
    return mine - min(sum(l[a] for l in losses) for a in range(k))


def rvu_bound(xs, losses, eta):
    """Return ln k / eta + eta sum_t |l_t - l_{t-1}|_inf^2 - (1 / (8 eta)) sum_{t >= 2} |x_t - x_{t-1}|_1^2,
    with l_0 = 0: the RVU bound on the regret of optimistic Hedge."""
    k = len(xs[0])
    prev = [0.0] * k
    var = 0.0
    for l in losses:
        var += max(abs(a - b) for a, b in zip(l, prev)) ** 2
        prev = l
    move = sum(sum(abs(a - b) for a, b in zip(x, y)) ** 2 for x, y in zip(xs[1:], xs))
    return math.log(k) / eta + eta * var - move / (8 * eta)


def self_play(game, T, eta):
    """Let every player of a finite game (sizes, pay), as in the helper agtgame, run optimistic
    Hedge on its expected losses (max u_i - u_i(a, x_-i)) / range_i. Return the list of the
    profiles of distributions and the list of the loss vectors of each player."""
    sizes, pay = game
    n = len(sizes)
    hi = [float(max(pay[s][i] for s in pay)) for i in range(n)]
    span = [hi[i] - float(min(pay[s][i] for s in pay)) or 1.0 for i in range(n)]
    learners = [OptimisticHedge(k, eta) for k in sizes]
    payf = {s: [float(v) for v in u] for s, u in pay.items()}
    hist_x, hist_l = [], []
    for _ in range(T):
        xs = [L.distribution() for L in learners]
        losses = []
        for i in range(n):
            d = [0.0] * sizes[i]
            for s, u in payf.items():
                w = 1.0
                for j, a in enumerate(s):
                    if j != i:
                        w *= xs[j][a]
                d[s[i]] += w * u[i]
            losses.append([(hi[i] - v) / span[i] for v in d])
        for L, l in zip(learners, losses):
            L.update(l)
        hist_x.append(xs)
        hist_l.append(losses)
    return hist_x, hist_l
