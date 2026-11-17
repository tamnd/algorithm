# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/epidemic-data-augmentation-mcmc/. The authors are listed in prov/YHHCY9.jsonl.
"""Data augmentation MCMC for the Markov SIR epidemic with observed removals.

Model: N people, infection rate beta S I / N, removal rate gamma per case.
The epidemic is over, and the removal times r_1, ..., r_n of the n people
who were ever infected are known. Their infection times i_1, ..., i_n are
not. The earliest infection is the initial case; it has a flat prior on
(-inf, its removal time). The priors are beta ~ Gamma(a_beta, rate b_beta)
and gamma ~ Gamma(a_gamma, rate b_gamma).

The sampler keeps the infection times as extra unknowns. Given them, beta
and gamma have gamma full conditionals (Gibbs steps). Given beta and gamma,
one infection time at a time gets a Metropolis-Hastings step that proposes
r_j - Exp(gamma).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Sequence, Tuple


@dataclass
class Prior:
    a_beta: float = 1.0
    b_beta: float = 1.0  # rate
    a_gamma: float = 1.0
    b_gamma: float = 1.0  # rate


def pressure_integral(inf: Sequence[float], rem: Sequence[float], n_pop: int) -> float:
    """A = integral of S(t) I(t) dt, as a sum over pairs (case j, person k).

    Case j can infect person k from i_j until min(r_j, i_k); a person who is
    never infected has i_k = inf and adds r_j - i_j for every case j.
    """
    n = len(inf)
    total = 0.0
    for j in range(n):
        for k in range(n):
            if k != j:
                total += max(0.0, min(rem[j], inf[k]) - inf[j])
        total += (n_pop - n) * (rem[j] - inf[j])
    return total


def pair_terms(j: int, inf: Sequence[float], rem: Sequence[float], n_pop: int) -> float:
    """The terms of pressure_integral that involve case j, as infector or as
    the person infected. A changes by the change of this sum when only i_j
    moves, which costs O(n) in place of O(n^2)."""
    n = len(inf)
    total = (n_pop - n) * (rem[j] - inf[j])
    for k in range(n):
        if k != j:
            total += max(0.0, min(rem[j], inf[k]) - inf[j])
            total += max(0.0, min(rem[k], inf[j]) - inf[k])
    return total


def log_infection_term(inf: Sequence[float], rem: Sequence[float]) -> float:
    """The sum of log I(i_j-) over all cases but the first, or -inf if some
    case was infected while nobody was infectious. One sweep over the 2n
    sorted event times, O(n log n)."""
    events = sorted([(t, 1) for t in inf] + [(t, -1) for t in rem])
    count, total, first = 0, 0.0, True
    for _, kind in events:
        if kind == 1:
            if not first:
                if count == 0:
                    return -math.inf
                total += math.log(count)
            first = False
        count += kind
    return total


def log_likelihood(inf, rem, n_pop: int, beta: float, gamma: float) -> float:
    """log of the density of the complete epidemic (infection and removal
    times) given beta and gamma."""
    if any(i >= r for i, r in zip(inf, rem)):
        return -math.inf
    li = log_infection_term(inf, rem)
    if li == -math.inf:
        return li
    n = len(inf)
    a = pressure_integral(inf, rem, n_pop)
    d = sum(r - i for i, r in zip(inf, rem))
    return ((n - 1) * math.log(beta / n_pop) + li - beta * a / n_pop
            + n * math.log(gamma) - gamma * d)


def initial_infection_times(rem: Sequence[float], gap: float = 1.0) -> List[float]:
    """A valid start: everyone infected before the first removal, in the order
    of the removals, so each later case finds the earlier ones infectious."""
    first = min(rem)
    order = sorted(range(len(rem)), key=lambda j: rem[j])
    inf = [0.0] * len(rem)
    for rank, j in enumerate(order):
        inf[j] = first - gap * (len(rem) - rank) / len(rem)
    return inf


def run(rng, rem: Sequence[float], n_pop: int, prior: Prior, iterations: int,
        updates_per_iteration: int | None = None) -> Tuple[List[float], List[float], List[List[float]]]:
    """The sampler. Returns the chains of beta, gamma and the infection times.

    Draw order per iteration: rng.gammavariate for beta, rng.gammavariate for
    gamma, then for each infection-time update rng.randrange (which case),
    rng.expovariate (the proposal) and rng.random (the acceptance).
    """
    n = len(rem)
    if n < 1 or n > n_pop:
        raise ValueError("need 1 <= n <= N")
    k_updates = n if updates_per_iteration is None else updates_per_iteration
    inf = initial_infection_times(rem)  # @line L1
    a = pressure_integral(inf, rem, n_pop)
    li = log_infection_term(inf, rem)
    betas, gammas, infs = [], [], []
    for _ in range(iterations):  # @line L2
        d = sum(r - i for i, r in zip(inf, rem))
        beta = rng.gammavariate(prior.a_beta + n - 1, 1.0 / (prior.b_beta + a / n_pop))  # @line L3
        gamma = rng.gammavariate(prior.a_gamma + n, 1.0 / (prior.b_gamma + d))  # @line L4
        for _ in range(k_updates):
            j = rng.randrange(n)  # @line L5
            new = list(inf)
            new[j] = rem[j] - rng.expovariate(gamma)  # @line L6
            u = rng.random()
            li_new = log_infection_term(new, rem)
            if li_new == -math.inf:
                continue  # the proposed epidemic is impossible: reject
            a_new = a - pair_terms(j, inf, rem, n_pop) + pair_terms(j, new, rem, n_pop)
            log_ratio = (li_new - li) - beta * (a_new - a) / n_pop
            if math.log(1.0 - u) < log_ratio:  # @line L7
                inf, a, li = new, a_new, li_new
        betas.append(beta)  # @line L8
        gammas.append(gamma)
        infs.append(list(inf))
    return betas, gammas, infs


def simulate_labeled(rng, n_pop: int, beta: float, gamma: float,
                     initial: int = 1) -> Tuple[List[float], List[float]]:
    """A complete labelled Markov SIR epidemic from `initial` cases at time 0.

    Returns the infection and removal times of the people who were infected.
    Draw order per event: rng.expovariate (the time), rng.random (the type),
    then rng.randrange (which case is removed; the infected person is the
    next label, since the labels of susceptibles are exchangeable).
    """
    t = 0.0
    inf = [0.0] * initial
    rem = [math.inf] * initial
    active = list(range(initial))
    s = n_pop - initial
    while active:
        i = len(active)
        a_inf = beta * s * i / n_pop
        a0 = a_inf + gamma * i
        t += rng.expovariate(a0)
        if rng.random() * a0 < a_inf:
            inf.append(t)
            rem.append(math.inf)
            active.append(len(inf) - 1)
            s -= 1
        else:
            k = active.pop(rng.randrange(len(active)))
            rem[k] = t
    return inf, rem
