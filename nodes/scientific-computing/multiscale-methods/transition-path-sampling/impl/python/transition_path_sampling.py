# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/transition-path-sampling/. The authors are listed in prov/MA0G4J.jsonl.
"""Transition path sampling (Dellago, Bolhuis, Csajka and Chandler 1998).

A path is a list x[0..N] of states of a Markov chain at successive time
steps. The transition path ensemble gives the path x the weight

    pi(x[0]) p(x[0], x[1]) ... p(x[N-1], x[N]) h_A(x[0]) h_B(x[N]),

where pi is the equilibrium distribution, p the transition probability,
and h_A, h_B the indicators of the two stable states. This module samples
the ensemble by Metropolis Monte Carlo in path space with two moves:

- one-way shooting: pick a time slice k, then either regenerate the part
  after k with the forward dynamics, or the part before k with the
  backward dynamics;
- shifting: drop s states at one end and grow s new states at the other.

step(x, rng) is one step of the dynamics. back(x, rng) is one step of the
time reversed dynamics, the chain with p_back(y, x) = pi(x) p(x, y) / pi(y);
for a reversible chain it is the same as step. With these moves the
generation probability cancels the path weight, and a trial path is
accepted if and only if it starts in A and ends in B.
"""

from typing import Callable, Optional


def transition_path_sampling(path, step: Callable, in_a: Callable, in_b: Callable, rng, n_moves: int,
                             back: Optional[Callable] = None, max_shift: int = 2,
                             observe: Optional[Callable] = None):
    """Run n_moves path moves from a reactive path.

    Returns (path, samples, accepted, work): the last path, the list of
    observe(path) after every move (the path itself if observe is None),
    the number of accepted moves, and the number of dynamics steps made.
    """
    if back is None:
        back = step
    x = list(path)
    if not (in_a(x[0]) and in_b(x[-1])):
        raise ValueError("transition_path_sampling: the initial path must go from A to B")
    n = len(x) - 1
    samples, accepted, work = [], 0, 0
    for _ in range(n_moves):                                            # @line L1
        if rng.random() < 0.5:                                          # @line L2
            k = rng.randrange(n + 1)                                    # @line L3
            if rng.random() < 0.5:
                trial = x[:k + 1]
                for _ in range(n - k):
                    trial.append(step(trial[-1], rng))
                work += n - k
            else:
                head = [x[k]]
                for _ in range(k):
                    head.append(back(head[-1], rng))
                trial = head[::-1] + x[k + 1:]
                work += k
        else:
            s = rng.randrange(1, max_shift + 1)                         # @line L4
            if rng.random() < 0.5:
                trial = x[s:]
                for _ in range(s):
                    trial.append(step(trial[-1], rng))
            else:
                head = [x[0]]
                for _ in range(s):
                    head.append(back(head[-1], rng))
                trial = head[::-1] + x[1:n - s + 1]
            work += s
        if in_a(trial[0]) and in_b(trial[-1]):                          # @line L5
            x = trial
            accepted += 1
        samples.append(observe(x) if observe else list(x))              # @line L6
    return x, samples, accepted, work                                   # @line L7
