# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/actor-critic/. The authors are listed in prov/2ZBR0P.jsonl.

"""One-step actor-critic: a tabular softmax actor and a linear TD(0) critic.

An MDP is (P, R): P[s][a][t] is the probability of the next state t, the
missing mass of a row is the probability that the episode ends, and R[s][a] is
the reward. The actor is pi(a|s) = exp(theta[s][a]) / sum_b exp(theta[s][b]).
The critic is V_w(s) = sum_i w[i] phi[s][i], and V_w(end) = 0.

step works with Fractions as well as floats, so that its mean over all
episodes can be compared exactly with the true gradient.

Cost per time step: O(A + F) arithmetic operations, F the number of critic
features. Memory: O(S A + F) for the parameters.
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


def value(w, phi, s):
    """V_w(s); s is None at the end of the episode."""
    if s is None:
        return 0 * w[0]
    return sum(wi * fi for wi, fi in zip(w, phi[s]))


def step(theta, w, phi, pi, s, a, r, s_next, gamma, I, eta_theta, eta_w):
    """One update from the transition (s, a, r, s_next); pi is the policy that chose a. Returns delta."""
    delta = r + gamma * value(w, phi, s_next) - value(w, phi, s)  # @line L5
    for i in range(len(w)):
        w[i] += eta_w * delta * phi[s][i]  # @line L6
    for b in range(len(theta[s])):
        theta[s][b] += eta_theta * I * delta * ((1 if a == b else 0) - pi[s][b])  # @line L7
    return delta


def actor_critic(P, R, gamma, mu, theta, w, phi, eta_theta, eta_w, episodes, rng, max_steps=1000):
    """Run one-step actor-critic; return (theta, w)."""
    theta = [row[:] for row in theta]
    w = list(w)
    n = len(P)
    for _ in range(episodes):  # @line L1
        s, I = rng.choices(range(n), weights=mu)[0], 1.0  # @line L2
        for _ in range(max_steps):  # @line L3
            if s is None:
                break
            pi = softmax(theta)
            a = rng.choices(range(len(pi[s])), weights=pi[s])[0]  # @line L4
            u, acc, s_next = rng.random(), 0.0, None
            for t in range(n):
                acc += P[s][a][t]
                if u < acc:
                    s_next = t
                    break
            step(theta, w, phi, pi, s, a, R[s][a], s_next, gamma, I, eta_theta, eta_w)
            I, s = gamma * I, s_next  # @line L8
    return theta, w
