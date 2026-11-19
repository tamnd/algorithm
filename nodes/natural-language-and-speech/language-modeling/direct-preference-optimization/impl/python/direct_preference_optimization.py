# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/direct-preference-optimization/. The authors are listed in prov/ZDWMJ1.jsonl.

"""Direct preference optimization (DPO): the loss and its gradient.

The input is m preference pairs. For pair i the network gives four sequence
log probabilities (natural log, summed over the tokens of a response):

    a_w = log pi_theta(y_w | x)    the trained policy on the preferred response
    a_l = log pi_theta(y_l | x)    the trained policy on the other response
    b_w = log pi_ref(y_w | x)      the frozen reference policy
    b_l = log pi_ref(y_l | x)

With z = beta ((a_w - b_w) - (a_l - b_l)) the loss of the batch is

    L = (1 / m) sum_i -log sigmoid(z_i),

and dL/da_w = -beta sigmoid(-z) / m, dL/da_l = +beta sigmoid(-z) / m. The
gradient with respect to the network weights is the chain rule through
a_w and a_l, which the training framework does.

-log sigmoid(z) is computed as log_add(0, -z), so it does not overflow for
large |z|.

The tabular part has one prompt and K responses, a policy pi = softmax(theta)
over them, and a reference pi_ref. It is used to check that the minimizer of
the population DPO loss under Bradley-Terry preferences is
pi_ref exp(r / beta) / Z, the optimum of the KL-regularized objective.

The code takes the four sequence log probabilities as given. It does not
train a network and does not load weights.
"""

import math
from typing import List, Sequence, Tuple

from nlslog import log_add, log_normalize

Pair = Tuple[float, float, float, float]  # (a_w, b_w, a_l, b_l)


def sigmoid(z: float) -> float:
    """Return 1 / (1 + exp(-z)) without overflow."""
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    e = math.exp(z)
    return e / (1.0 + e)


def neg_log_sigmoid(z: float) -> float:
    """Return -log sigmoid(z) = log(1 + exp(-z)) = log_add(0, -z)."""
    return log_add(0.0, -z)


def implicit_reward(logp: float, logp_ref: float, beta: float) -> float:
    """Return beta (log pi - log pi_ref), the reward that the policy implies up to a term in x."""
    return beta * (logp - logp_ref)


def dpo_loss(pairs: Sequence[Pair], beta: float) -> Tuple[float, List[Tuple[float, float]]]:
    """Return (L, grads), where grads[i] = (dL/da_w, dL/da_l) for pair i."""
    if beta <= 0:
        raise ValueError("beta must be positive")
    m = len(pairs)
    if m == 0:
        raise ValueError("need at least one pair")
    total = []  # @line L1
    grads = []
    for a_w, b_w, a_l, b_l in pairs:  # @line L2
        z = beta * ((a_w - b_w) - (a_l - b_l))  # @line L3
        total.append(neg_log_sigmoid(z))  # @line L4
        q = sigmoid(-z)  # @line L5
        grads.append((-beta * q / m, beta * q / m))  # @line L6
    return math.fsum(total) / m, grads  # @line L7


def reward_model_loss(r_w: float, r_l: float) -> float:
    """Return the Bradley-Terry loss -log sigmoid(r_w - r_l) of a reward model."""
    return neg_log_sigmoid(r_w - r_l)


# ------------------------------------------------------------ tabular policy


def log_policy(theta: Sequence[float]) -> List[float]:
    """Return log softmax(theta)."""
    return log_normalize(list(theta))


def optimal_policy(ref: Sequence[float], reward: Sequence[float], beta: float) -> List[float]:
    """Return pi*(y) = pi_ref(y) exp(r(y) / beta) / Z, computed in log space."""
    logs = [math.log(p) + r / beta for p, r in zip(ref, reward)]
    return [math.exp(v) for v in log_normalize(logs)]


def log_partition(ref: Sequence[float], reward: Sequence[float], beta: float) -> float:
    """Return log Z = log sum_y pi_ref(y) exp(r(y) / beta)."""
    logs = [math.log(p) + r / beta for p, r in zip(ref, reward)]
    z = logs[0]
    for v in logs[1:]:
        z = log_add(z, v)
    return z


def kl_objective(pi: Sequence[float], ref: Sequence[float], reward: Sequence[float], beta: float) -> float:
    """Return E_pi[r] - beta KL(pi || pi_ref), the objective of RLHF for one prompt."""
    er = math.fsum(p * r for p, r in zip(pi, reward))
    kl = math.fsum(p * math.log(p / q) for p, q in zip(pi, ref) if p > 0)
    return er - beta * kl


def bradley_terry_pairs(reward: Sequence[float]) -> List[Tuple[int, int, float]]:
    """Return (w, l, weight) for every ordered pair: an unordered pair is drawn uniformly,
    and w is preferred to l with probability sigmoid(r_w - r_l) (Bradley-Terry)."""
    K = len(reward)
    n_pairs = K * (K - 1) // 2
    out = []
    for i in range(K):
        for j in range(K):
            if i != j:
                out.append((i, j, sigmoid(reward[i] - reward[j]) / n_pairs))
    return out


def tabular_dpo_loss(theta: Sequence[float], log_ref: Sequence[float], weighted_pairs, beta: float) -> Tuple[float, List[float]]:
    """Return the weighted DPO loss of a softmax policy and its gradient with respect to theta.

    weighted_pairs holds (w, l, weight). Since d log pi(y) / d theta_j = [y = j] - pi_j,
    the pi_j terms cancel in log pi(w) - log pi(l), and dz/dtheta_j = beta ([w = j] - [l = j]).
    """
    lp = log_policy(theta)
    terms = []
    grad = [0.0] * len(theta)
    for w, l, weight in weighted_pairs:
        z = beta * ((lp[w] - log_ref[w]) - (lp[l] - log_ref[l]))
        terms.append(weight * neg_log_sigmoid(z))
        q = sigmoid(-z)
        grad[w] -= weight * beta * q
        grad[l] += weight * beta * q
    return math.fsum(terms), grad


def fit_tabular(log_ref: Sequence[float], weighted_pairs, beta: float, steps: int = 3000, lr: float = 1.0) -> List[float]:
    """Run gradient descent on theta, starting at theta = log_ref. Return pi_theta."""
    theta = list(log_ref)
    for _ in range(steps):
        _, g = tabular_dpo_loss(theta, log_ref, weighted_pairs, beta)
        theta = [t - lr * gi for t, gi in zip(theta, g)]
    return [math.exp(v) for v in log_policy(theta)]
