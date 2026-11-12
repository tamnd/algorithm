# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/prioritized-sweeping/. The authors are listed in prov/NRKTQX.jsonl.

"""Prioritized sweeping (Moore and Atkeson 1993; Peng and Williams 1993).

Value backups are ordered by the size of the Bellman error, kept in a max
priority queue (a binary heap with lazy deletion). When V(s) changes, only the
predecessors of s, the states with an action that can lead to s, get new
priorities.

prioritized_sweeping plans on a known model: P[s][a] is a list of pairs
(p, t), the probability p of the next state t, and R[s][a] is the expected
reward. OnlinePrioritizedSweeping learns a count model from real transitions
and runs a few prioritized backups after each one, as in Moore and Atkeson.
"""

import heapq


def _sweep(V, qvals, pred, heap, prio, theta, limit=None):
    """Run backups from the queue until it is empty or limit backups are done.

    Invariant: prio[s] is the current Bellman error of s if it exceeds theta,
    and s is absent from prio otherwise. Heap entries that disagree with prio
    are stale and are skipped. Return the number of backups.
    """
    done = 0
    while heap and (limit is None or done < limit):  # @line L3
        neg, s = heapq.heappop(heap)  # @line L4
        if prio.get(s) != -neg:
            continue  # a stale entry
        del prio[s]
        V[s] = max(qvals(s, V))  # @line L5
        done += 1
        for p in pred[s]:  # @line L6
            e = abs(max(qvals(p, V)) - V[p])  # @line L7
            if e > theta:  # @line L8
                prio[p] = e
                heapq.heappush(heap, (-e, p))
            else:
                prio.pop(p, None)
    return done


def prioritized_sweeping(P, R, gamma, theta, v0=None):
    """Return (V, backups). At return every Bellman error |(TV)(s) - V(s)| is <= theta.

    Preconditions: 0 <= gamma < 1, theta > 0. Then |V - V*| <= theta / (1 - gamma).
    """
    n = len(P)

    def qvals(s, V):
        return [R[s][a] + gamma * sum(p * V[t] for p, t in P[s][a]) for a in range(len(P[s]))]

    V = [0.0] * n if v0 is None else list(v0)  # @line L1
    pred = [set() for _ in range(n)]
    for s in range(n):
        for a in range(len(P[s])):
            for p, t in P[s][a]:
                if p > 0:
                    pred[t].add(s)
    heap, prio = [], {}
    for s in range(n):  # @line L2
        e = abs(max(qvals(s, V)) - V[s])
        if e > theta:
            prio[s] = e
            heapq.heappush(heap, (-e, s))
    backups = _sweep(V, qvals, pred, heap, prio, theta)
    return V, backups  # @line L9


class OnlinePrioritizedSweeping:
    """Learn a count model from transitions (s, a, r, t) and plan with prioritized sweeping.

    The model of an action is its empirical next-state distribution and its mean
    reward. Actions that were never tried are left out of the maximum; a state
    with no tried action has value 0.
    """

    def __init__(self, n_states, n_actions, gamma, theta, backups_per_step):
        self.n, self.k, self.gamma, self.theta = n_states, n_actions, gamma, theta
        self.limit = backups_per_step
        self.N = [[0] * n_actions for _ in range(n_states)]
        self.C = [[{} for _ in range(n_actions)] for _ in range(n_states)]
        self.Rsum = [[0.0] * n_actions for _ in range(n_states)]
        self.V = [0.0] * n_states
        self.pred = [set() for _ in range(n_states)]
        self.heap, self.prio = [], {}
        self.backups = 0

    def qvals(self, s, V):
        out = []
        for a in range(self.k):
            m = self.N[s][a]
            if m:
                exp = sum(c * V[t] for t, c in self.C[s][a].items()) / m
                out.append(self.Rsum[s][a] / m + self.gamma * exp)
        return out or [0.0]

    def observe(self, s, a, r, t):
        """Add one real transition to the model, then run up to backups_per_step backups."""
        self.N[s][a] += 1
        self.C[s][a][t] = self.C[s][a].get(t, 0) + 1
        self.Rsum[s][a] += r
        self.pred[t].add(s)
        e = abs(max(self.qvals(s, self.V)) - self.V[s])
        if e > self.theta:
            self.prio[s] = e
            heapq.heappush(self.heap, (-e, s))
        self.backups += _sweep(self.V, self.qvals, self.pred, self.heap, self.prio, self.theta, self.limit)

    def flush(self):
        """Run backups until no Bellman error of the learned model exceeds theta."""
        self.backups += _sweep(self.V, self.qvals, self.pred, self.heap, self.prio, self.theta)

    def greedy(self, s):
        best, act = None, 0
        for a in range(self.k):
            if self.N[s][a]:
                q = self.Rsum[s][a] / self.N[s][a] + self.gamma * sum(
                    c * self.V[t] for t, c in self.C[s][a].items()
                ) / self.N[s][a]
                if best is None or q > best:
                    best, act = q, a
        return act
