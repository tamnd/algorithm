# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/off-policy-evaluation/. The authors are listed in prov/982C79.jsonl.

"""Off-policy evaluation estimators: direct method, importance sampling and doubly robust.

Bandit data are (x, a, r) triples logged by a behavior policy. pi(a, x) and mu_hat(a, x) give
action probabilities, q_hat(x, a) is a reward model. Sequential data are episodes of (s, a, r)
steps, and the sequential doubly robust estimator is the one of Jiang and Li (2016).
"""

from fractions import Fraction
from typing import Callable, Hashable, Sequence

Number = float | Fraction
Policy = Callable[[Hashable, Hashable], Number]
Model = Callable[[Hashable, Hashable], Number]


def direct_method(data: Sequence[tuple], pi: Policy, q_hat: Model, actions: Sequence) -> Number:
    """Mean over contexts of sum_a pi(a|x) q_hat(x, a). Ignores the logged actions and rewards."""
    return sum(sum(pi(b, x) * q_hat(x, b) for b in actions) for x, _, _ in data) / len(data)


def inverse_propensity(data: Sequence[tuple], pi: Policy, mu_hat: Policy) -> Number:
    """Mean of pi(a|x) / mu_hat(a|x) r: importance sampling for one step."""
    return sum(pi(a, x) / mu_hat(a, x) * r for x, a, r in data) / len(data)


def self_normalized_ips(data: Sequence[tuple], pi: Policy, mu_hat: Policy) -> Number:
    """Sum of w r over sum of w with w = pi / mu_hat: weighted importance sampling."""
    w = [pi(a, x) / mu_hat(a, x) for x, a, _ in data]
    total = sum(w)
    return sum(wi * r for wi, (_, _, r) in zip(w, data)) / total if total != 0 else 0 * total


def doubly_robust(data: Sequence[tuple], pi: Policy, mu_hat: Policy, q_hat: Model, actions: Sequence) -> Number:
    """Mean of sum_a pi(a|x) q_hat(x, a) + pi(a|x) / mu_hat(a|x) (r - q_hat(x, a)) (Dudik, Langford and Li 2011).

    Unbiased if mu_hat equals the true behavior policy or q_hat equals the true mean reward.
    """
    total = 0
    for x, a, r in data:
        baseline = sum(pi(b, x) * q_hat(x, b) for b in actions)
        total += baseline + pi(a, x) / mu_hat(a, x) * (r - q_hat(x, a))
    return total / len(data)


def sequential_doubly_robust(
    episodes: Sequence[Sequence[tuple]], pi: Policy, mu_hat: Policy, q_hat: Model, actions: Sequence, gamma: Number = 1
) -> Number:
    """Jiang and Li (2016): V_DR = V_hat(s) + rho (r + gamma V_DR' - Q_hat(s, a)), backward over each episode.

    V_hat(s) = sum_a pi(a|s) Q_hat(s, a). Returns the mean of V_DR at the start of the episodes.
    O(total steps times number of actions).
    """
    total = 0
    for episode in episodes:
        v_dr = 0
        for s, a, r in reversed(episode):
            v_hat = sum(pi(b, s) * q_hat(s, b) for b in actions)
            rho = pi(a, s) / mu_hat(a, s)
            v_dr = v_hat + rho * (r + gamma * v_dr - q_hat(s, a))
        total += v_dr
    return total / len(episodes)
