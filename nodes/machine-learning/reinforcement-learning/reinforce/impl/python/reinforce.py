# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reinforce/. The authors are listed in prov/QVNG1R.jsonl.

"""REINFORCE (Williams 1992) with a tabular softmax policy and an optional baseline.

An MDP is (P, R): P[s][a][t] is the probability of the next state t, the
missing mass of a row is the probability that the episode ends, and R[s][a] is
the reward. pi(a|s) = exp(theta[s][a]) / sum_b exp(theta[s][b]), and
d log pi(a|s) / d theta[s][b] = 1[a = b] - pi(b|s).

episode_update works with Fractions as well as floats, so that its mean over
all episodes can be compared exactly with the true gradient.

Cost per episode of length T: O(T A) arithmetic operations for the update,
plus the sampling. Memory: O(S A) parameters and the episode.
"""

import math
import random


def softmax(theta):
    out = []
    for row in theta:
        m = max(row)
        e = [math.exp(x - m) for x in row]
        z = sum(e)
        out.append([x / z for x in e])
    return out


def sample_episode(P, R, pi, mu, rng, horizon):
    """Run pi from S_0 ~ mu; return [(S_t, A_t, R_(t+1)), ...] for at most horizon steps."""
    n = len(P)
    s = rng.choices(range(n), weights=mu)[0]
    episode = []
    for _ in range(horizon):
        a = rng.choices(range(len(pi[s])), weights=pi[s])[0]
        episode.append((s, a, R[s][a]))
        u, acc, nxt = rng.random(), 0.0, None
        for t in range(n):
            acc += P[s][a][t]
            if u < acc:
                nxt = t
                break
        if nxt is None:  # the episode ends
            break
        s = nxt
    return episode


def episode_update(pi, episode, gamma, baseline=None):
    """g = sum_t gamma^t (G_t - b(S_t)) grad log pi(A_t | S_t), returned as g[s][b]."""
    n, k = len(pi), len(pi[0])
    zero = 0 * pi[0][0]
    g = [[zero] * k for _ in range(n)]  # @line L3
    G = zero  # @line L4
    for t in range(len(episode) - 1, -1, -1):  # @line L5
        s, a, r = episode[t]
        G = r + gamma * G  # @line L6
        b = baseline[s] if baseline is not None else 0
        w = gamma ** t * (G - b)
        for j in range(k):
            g[s][j] += w * ((1 if a == j else 0) - pi[s][j])  # @line L7
    return g


def reinforce(P, R, gamma, mu, theta, eta, episodes, rng, horizon=1000, baseline_rate=None):
    """Run REINFORCE for a number of episodes; return (theta, baseline).

    With baseline_rate set, b(s) is a table that moves toward the observed
    returns G_t with that step size, after the policy update of each episode.
    """
    theta = [row[:] for row in theta]
    b = [0.0] * len(P) if baseline_rate is not None else None
    for _ in range(episodes):  # @line L1
        pi = softmax(theta)
        episode = sample_episode(P, R, pi, mu, rng, horizon)  # @line L2
        g = episode_update(pi, episode, gamma, b)
        for s in range(len(theta)):
            for j in range(len(theta[s])):
                theta[s][j] += eta * g[s][j]  # @line L8
        if b is not None:
            G = 0.0
            for s, _, r in reversed(episode):
                G = r + gamma * G
                b[s] += baseline_rate * (G - b[s])  # @line L9
    return theta, b
