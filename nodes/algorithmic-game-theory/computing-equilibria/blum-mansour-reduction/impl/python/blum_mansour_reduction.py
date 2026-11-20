# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blum-mansour-reduction/. The authors are listed in prov/FWT8FT.jsonl.
"""The Blum-Mansour reduction from swap regret to external regret, with Hedge copies.

There are k actions and losses in [0, 1]. The learner keeps k copies of Hedge. In each
round, copy j proposes a distribution q_j; the learner plays a distribution p with p = p Q,
where row j of Q is q_j, and after it sees the loss vector it gives copy j the scaled loss
vector p(j) * loss. The swap regret of the learner is at most the sum of the external
regrets of the copies. Arithmetic is in float.
"""

import math


class Hedge:
    """Hedge (exponential weights) on k actions with a fixed learning rate eta > 0."""

    def __init__(self, k, eta):
        if k < 1 or eta <= 0:
            raise ValueError("need k >= 1 and eta > 0")
        self.eta = eta
        self.cum = [0.0] * k  # cumulative loss of each action

    def distribution(self):
        low = min(self.cum)  # shift for numerical safety; it cancels in the ratio
        w = [math.exp(-self.eta * (c - low)) for c in self.cum]
        total = sum(w)
        return [x / total for x in w]

    def update(self, loss):
        for a, v in enumerate(loss):
            self.cum[a] += v


def stationary(Q):
    """Return the distribution p with p = p Q for a row-stochastic k by k matrix Q with
    positive entries (then p is unique). Gaussian elimination with partial pivoting."""
    k = len(Q)
    # Equations: sum_j p_j (Q[j][i] - [i == j]) = 0 for i < k - 1, and sum_j p_j = 1.
    M = [[Q[j][i] - (1.0 if i == j else 0.0) for j in range(k)] + [0.0] for i in range(k - 1)]
    M.append([1.0] * k + [1.0])
    for col in range(k):
        piv = max(range(col, k), key=lambda r: abs(M[r][col]))
        M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        for r in range(k):
            if r != col and M[r][col] != 0.0:
                f = M[r][col] / pv
                M[r] = [a - f * b for a, b in zip(M[r], M[col])]
    p = [max(M[i][k] / M[i][i], 0.0) for i in range(k)]
    total = sum(p)
    return [x / total for x in p]


class BlumMansour:
    """A no-swap-regret learner on k actions built from k copies of Hedge."""

    def __init__(self, k, eta):
        self.k = k
        self.copies = [Hedge(k, eta) for _ in range(k)]  # @line L1
        self.p = None
        self.Q = None

    def distribution(self):
        rows = [c.distribution() for c in self.copies]  # @line L3
        self.Q = rows  # @line L4
        self.p = stationary(self.Q)  # @line L5
        return self.p

    def update(self, loss):
        for j, c in enumerate(self.copies):  # @line L7
            c.update([self.p[j] * v for v in loss])


def run(k, T, eta, adversary):
    """Run the learner for T rounds. adversary(t, p) returns the loss vector of round t; it
    may look at the current distribution p. Return the lists of the distributions played,
    the loss vectors and the matrices Q."""
    learner = BlumMansour(k, eta)
    ps, losses, Qs = [], [], []
    for t in range(T):  # @line L2
        p = learner.distribution()
        loss = adversary(t, p)  # @line L6
        learner.update(loss)
        ps.append(p)
        losses.append(loss)
        Qs.append(learner.Q)
    return ps, losses, Qs


def swap_regret(ps, losses):
    """Return max over maps delta of sum_t sum_j p_t(j) (loss_t(j) - loss_t(delta(j))).
    The maximum splits over j: each j is sent to the action with the least weighted loss."""
    k = len(ps[0]) if ps else 0
    total = 0.0
    for j in range(k):
        here = sum(p[j] * l[j] for p, l in zip(ps, losses))
        best = min(sum(p[j] * l[a] for p, l in zip(ps, losses)) for a in range(k))
        total += here - best
    return total


def external_regret(ps, losses):
    """Return sum_t p_t . loss_t minus the least total loss of a fixed action."""
    k = len(ps[0]) if ps else 0
    here = sum(sum(x * v for x, v in zip(p, l)) for p, l in zip(ps, losses))
    return here - min(sum(l[a] for l in losses) for a in range(k)) if ps else 0.0


def regret_bound(k, T, eta):
    """The bound k ln k / eta + eta T / 2 on the swap regret after T rounds (losses in [0, 1])."""
    return k * math.log(k) / eta + eta * T / 2
