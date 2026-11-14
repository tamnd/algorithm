# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/abc-rejection-sampling/. The authors are listed in prov/1PE36P.jsonl.
"""The ABC rejection algorithm (Tavare et al. 1997; Pritchard et al. 1999).

Draw theta from the prior, simulate a data set y from the model at theta, and keep
theta when the summaries S(y) lie within eps of the observed summaries s_obs.
The kept values are an exact sample from the eps-posterior

    pi_eps(theta) proportional to pi(theta) P_theta(rho(S(Y), s_obs) <= eps).

With eps = 0, discrete data and a sufficient summary, that is the exact posterior.

Cost: each proposal costs one prior draw and one simulation. The expected number of
proposals per accepted value is 1 / P(rho(S(Y), s_obs) <= eps) under the prior
predictive, which grows like eps^(-q) for q continuous summaries.
"""

import random
from typing import Callable


def abc_step(
    prior_draw: Callable,
    simulate: Callable,
    summary: Callable,
    s_obs,
    distance: Callable,
    eps: float,
    rng,
) -> tuple:
    """One proposal: returns (theta, accepted). Lines L3 to L5."""
    theta = prior_draw(rng)  # @line L3
    y = simulate(theta, rng)  # @line L4
    return theta, distance(summary(y), s_obs) <= eps  # @line L5


def abc_rejection(
    prior_draw: Callable,
    simulate: Callable,
    summary: Callable,
    s_obs,
    distance: Callable,
    eps: float,
    n_accept: int,
    rng: random.Random,
    max_sims: int = 10**8,
) -> tuple[list, int]:
    """Run proposals until n_accept values are kept or max_sims proposals are made.

    Returns (accepted values, number of proposals).
    Precondition: prior_draw(rng) draws from a proper prior; simulate(theta, rng) draws a
    data set from f(. | theta); distance(a, b) >= 0. The kept values are independent.
    """
    accepted = []  # @line L1
    sims = 0
    while len(accepted) < n_accept and sims < max_sims:  # @line L2
        sims += 1
        theta, ok = abc_step(prior_draw, simulate, summary, s_obs, distance, eps, rng)
        if ok:
            accepted.append(theta)  # @line L6
    return accepted, sims  # @line L7


class ScriptedRNG:
    """A stand-in for random.Random whose randrange(k) returns scripted values.

    Used to enumerate every random path of a discrete sampler with exact probabilities.
    When the script runs out it raises NeedChoice(k), so the caller can branch.
    """

    class NeedChoice(Exception):
        def __init__(self, k: int):
            super().__init__(k)
            self.k = k

    def __init__(self, script: list):
        self.script = script
        self.pos = 0

    def randrange(self, k: int) -> int:
        if self.pos == len(self.script):
            raise ScriptedRNG.NeedChoice(k)
        v = self.script[self.pos][0]
        self.pos += 1
        return v


def exact_accept_law(run_step: Callable) -> dict:
    """Exact law of one call run_step(rng) -> (theta, accepted) over all random paths.

    run_step must use only rng.randrange. Returns {theta: P(theta and accepted)} as
    Fractions; their sum is the acceptance probability. Paths are enumerated depth first.
    """
    from fractions import Fraction

    law: dict = {}
    stack = [[]]  # each script is a list of (value, range)
    while stack:
        script = stack.pop()
        try:
            theta, ok = run_step(ScriptedRNG(script))
        except ScriptedRNG.NeedChoice as need:
            for v in range(need.k):
                stack.append(script + [(v, need.k)])
            continue
        if ok:
            p = Fraction(1)
            for _, k in script:
                p /= k
            law[theta] = law.get(theta, Fraction(0)) + p
    return law
