# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/a3c/. The authors are listed in prov/VZH9DA.jsonl.

"""A3C: asynchronous advantage actor-critic, simulated in one process.

Several workers share the parameters theta (a tabular softmax actor) and w (a
linear critic, V_w(s) = sum_i w[i] phi[s][i]). A schedule fixes the order in
which workers act. The first time a worker appears it reads the shared
parameters, runs up to t_max steps of its own copy of the MDP with them and
computes its gradient; the next time it appears it adds that gradient to the
shared parameters, which other workers may have changed in between. So the
gradient can be stale, as with real threads that update without locks.

An MDP is (P, R, mu): P[s][a][t] is the probability of the next state t, the
missing mass of a row is the probability that the episode ends, and mu is the
start distribution.

Cost: O(t_max (A + F)) arithmetic operations per read and per write, for A
actions and F critic features. Memory: O(t_max) per worker for its segment and
O(S A + F) per worker for its copy of the parameters.
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


def rollout(P, R, mu, pi, s, t_max, rng):
    """Run pi from s (or from a fresh start if s is None) for at most t_max steps or to the end.

    Returns (states, actions, rewards, last state, ended).
    """
    if s is None:
        s = rng.choices(range(len(P)), weights=mu)[0]
    states, actions, rewards = [], [], []
    for _ in range(t_max):
        a = rng.choices(range(len(pi[s])), weights=pi[s])[0]
        states.append(s)
        actions.append(a)
        rewards.append(R[s][a])
        u, acc, nxt = rng.random(), 0.0, None
        for t in range(len(P)):
            acc += P[s][a][t]
            if u < acc:
                nxt = t
                break
        if nxt is None:
            return states, actions, rewards, None, True
        s = nxt
    return states, actions, rewards, s, False


def worker_gradient(theta, w, phi, segment, gamma, beta):
    """Summed gradients (d_theta, d_w) of one segment, with the worker's copy (theta, w)."""
    states, actions, rewards, last, ended = segment
    pi = softmax(theta)
    d_theta = [[0.0] * len(row) for row in theta]  # @line L3
    d_w = [0.0] * len(w)
    G = 0.0 if ended else value(w, phi, last)  # @line L5
    for i in range(len(states) - 1, -1, -1):
        s, a = states[i], actions[i]
        G = rewards[i] + gamma * G  # @line L6
        adv = G - value(w, phi, s)
        H = -sum(p * math.log(p) for p in pi[s])
        for b in range(len(theta[s])):
            d_theta[s][b] += adv * ((1 if a == b else 0) - pi[s][b]) - beta * pi[s][b] * (math.log(pi[s][b]) + H)  # @line L7
        for k in range(len(w)):
            d_w[k] += adv * phi[s][k]  # @line L8
    return d_theta, d_w


def random_schedule(n_workers, reads, rng):
    """A random interleaving in which each worker alternates read and write, reads times in total."""
    out, pending, done = [], [False] * n_workers, 0
    while done < reads or any(pending):
        i = rng.randrange(n_workers)
        if not pending[i] and done >= reads:
            continue
        if not pending[i]:
            done += 1
        pending[i] = not pending[i]
        out.append(i)
    return out


def a3c(P, R, mu, gamma, theta, w, phi, n_workers, t_max, schedule, eta, rng, beta=0.0, c_v=0.5, log=None):
    """Run the workers in the order of schedule; return the shared (theta, w).

    If log is a list, each read appends (worker, theta copy, w copy, segment).
    """
    theta = [row[:] for row in theta]
    w = list(w)
    rngs = [random.Random(rng.randrange(2 ** 32)) for _ in range(n_workers)]
    env = [None] * n_workers
    grads = [None] * n_workers
    k = 0
    while k < len(schedule):  # @line L1
        i = schedule[k]
        if grads[i] is None:
            th_i, w_i = [row[:] for row in theta], list(w)  # @line L2
            seg = rollout(P, R, mu, softmax(th_i), env[i], t_max, rngs[i])  # @line L4
            env[i] = seg[3]
            grads[i] = worker_gradient(th_i, w_i, phi, seg, gamma, beta)
            if log is not None:
                log.append((i, th_i, w_i, seg))
        else:
            d_theta, d_w = grads[i]
            for s in range(len(theta)):
                for b in range(len(theta[s])):
                    theta[s][b] += eta * d_theta[s][b]  # @line L9
            for j in range(len(w)):
                w[j] += eta * c_v * d_w[j]
            grads[i] = None
        k += 1
        if k >= len(schedule):  # @line L10
            break
    return theta, w
