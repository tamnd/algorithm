# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterative-policy-evaluation/. The authors are listed in prov/SYAD7P.jsonl.

"""Iterative policy evaluation: repeated Bellman expectation backups for a fixed policy.

P[s][a] is a list of pairs (p, t), the probability p of the next state t,
R[s][a] is the expected reward, and pi[s][a] is the probability that the
policy takes action a in state s. Numbers may be floats or Fractions.
"""


def iterative_policy_evaluation(P, R, gamma, pi, theta, in_place=True, v0=None, max_sweeps=None):
    """Return (V, k): the values after the last sweep and the number of sweeps.

    Precondition: 0 <= gamma < 1, or gamma = 1 with a policy that reaches an
    absorbing zero-reward state with probability 1 from each state; theta > 0.
    The loop stops after the first sweep whose largest change is below theta.
    For gamma < 1 the result is then within gamma theta / (1 - gamma) of V^pi
    in the max norm. in_place=True uses one array (each backup sees the newest
    values); in_place=False uses two arrays (a Jacobi sweep).
    One sweep costs O(sum over s and a with pi[s][a] > 0 of the size of P[s][a]).
    """
    n = len(P)
    V = [0 * gamma] * n if v0 is None else list(v0)  # @line L1
    k = 0
    while True:  # @line L2
        delta = 0  # @line L3
        W = V if in_place else list(V)
        for s in range(n):  # @line L4
            v = sum(  # @line L5
                pi[s][a] * (R[s][a] + gamma * sum(p * V[t] for p, t in P[s][a]))
                for a in range(len(P[s]))
                if pi[s][a]
            )
            delta = max(delta, abs(v - W[s]))  # @line L6
            W[s] = v  # @line L7
        V = W
        k += 1
        if delta < theta or (max_sweeps is not None and k >= max_sweeps):  # @line L8
            return V, k  # @line L9
