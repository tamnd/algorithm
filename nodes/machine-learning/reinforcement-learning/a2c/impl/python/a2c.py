# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/a2c/. The authors are listed in prov/S26G9H.jsonl.

"""A2C: synchronous n-step advantage actor-critic over N copies of an MDP.

An MDP is (P, R, mu): P[s][a][t] is the probability of the next state t, the
missing mass of a row is the probability that the episode ends (the copy then
restarts from mu), and R[s][a] is the reward. The actor is a tabular softmax,
pi(a|s) proportional to exp(theta[s][a]); the critic is linear,
V_w(s) = sum_i w[i] phi[s][i].

One update costs O(N n (A + F)) arithmetic operations for N copies, n steps,
A actions and F critic features. Memory: O(N n) for the batch and O(S A + F)
for the parameters.
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
    return sum(wi * fi for wi, fi in zip(w, phi[s]))


def env_step(P, R, mu, s, a, rng):
    """One step of a copy: (reward, next state, done); after done the next state is a fresh start."""
    u, acc = rng.random(), 0.0
    for t in range(len(P)):
        acc += P[s][a][t]
        if u < acc:
            return R[s][a], t, False
    return R[s][a], rng.choices(range(len(P)), weights=mu)[0], True


def n_step_returns(rewards, dones, bootstrap, gamma):
    """G_t = R_(t+1) + gamma (1 - D_(t+1)) G_(t+1), with G_n = bootstrap; rewards[t] = R_(t+1)."""
    G = bootstrap  # @line L5
    out = [None] * len(rewards)
    for t in range(len(rewards) - 1, -1, -1):
        G = rewards[t] + (0 if dones[t] else gamma * G)  # @line L6
        out[t] = G
    return out


def gradients(theta, w, phi, pi, batch, beta):
    """Ascent directions for the actor and the critic from a batch of (s, a, G).

    g_theta = mean of (G - V_w(s)) grad log pi(a|s) + beta grad H(pi(.|s)),
    g_w = mean of (G - V_w(s)) grad V_w(s). beta must be 0 for Fractions.
    """
    zero = 0 * w[0]
    g_theta = [[zero] * len(row) for row in theta]
    g_w = [zero] * len(w)
    m = len(batch)
    for s, a, G in batch:
        adv = G - value(w, phi, s)  # @line L7
        H = -sum(p * math.log(p) for p in pi[s]) if beta else 0
        for b in range(len(theta[s])):
            ent = -pi[s][b] * (math.log(pi[s][b]) + H) if beta else 0
            g_theta[s][b] += (adv * ((1 if a == b else 0) - pi[s][b]) + beta * ent) / m  # @line L8
        for i in range(len(w)):
            g_w[i] += adv * phi[s][i] / m  # @line L9
    return g_theta, g_w


def a2c(P, R, mu, gamma, theta, w, phi, n_envs, n, updates, eta, rng, beta=0.0, c_v=0.5):
    """Run A2C for a number of updates; return (theta, w)."""
    theta = [row[:] for row in theta]
    w = list(w)
    S = [rng.choices(range(len(P)), weights=mu)[0] for _ in range(n_envs)]  # @line L1
    for _ in range(updates):  # @line L2
        pi = softmax(theta)
        batch = []
        segments = [([], [], [], []) for _ in range(n_envs)]
        for _ in range(n):  # @line L3
            for i in range(n_envs):
                a = rng.choices(range(len(pi[S[i]])), weights=pi[S[i]])[0]
                r, s2, done = env_step(P, R, mu, S[i], a, rng)  # @line L4
                for lst, x in zip(segments[i], (S[i], a, r, done)):
                    lst.append(x)
                S[i] = s2
        for i in range(n_envs):
            states, actions, rewards, dones = segments[i]
            G = n_step_returns(rewards, dones, value(w, phi, S[i]), gamma)
            batch += list(zip(states, actions, G))
        g_theta, g_w = gradients(theta, w, phi, pi, batch, beta)
        for s in range(len(theta)):
            for b in range(len(theta[s])):
                theta[s][b] += eta * g_theta[s][b]  # @line L10
        for i in range(len(w)):
            w[i] += eta * c_v * g_w[i]
    return theta, w
