---
tag: QCDBQ4
kind: algorithm
slug: conservative-q-learning
name: Conservative Q-learning
aliases:
- CQL
- CQL(H)
area: machine-learning/reinforcement-learning
level: research
summary: "Offline Q-learning that adds alpha (logsumexp_a Q(s,a) - Q(s,a_data)) to the Bellman loss, pushing down values of actions absent from the data so the learned value is a lower bound."
solves: [offline-reinforcement-learning]
model: real-ram
complexity:
  vars: {K: the number of outer iterations, G: the gradient steps per iteration, N: the number of transitions, S: the number of states, A: the number of actions}
  time: {worst: "O(K (N + G S A))"}
  space: {extra: "O(S A)"}
properties: {deterministic: true, online: false, exact: false, recursive: false}
history:
  year: 2020
  people: [Aviral Kumar, Aurick Zhou, George Tucker, Sergey Levine]
  note: "Kumar, Zhou, Tucker and Levine introduced CQL at NeurIPS 2020, with lower-bound theorems for its value estimates."
prereqs: [offline-reinforcement-learning, fitted-q-iteration]
see_also: [q-learning, dqn, deadly-triad, off-policy-evaluation, soft-actor-critic, log-sum-exp-trick, imitation-learning]
sources:
  - paper: "Aviral Kumar, Aurick Zhou, George Tucker and Sergey Levine, Conservative Q-learning for offline reinforcement learning, Advances in Neural Information Processing Systems 33 (NeurIPS 2020), arXiv:2006.04779"
    locator: "Section 3.1 (equation 1 and Theorem 3.1, the pointwise lower bound; equation 2 and Theorem 3.2, the lower bound on the value), Section 3.2 (equation 3, CQL(R), and equation 4, CQL(H); Theorems 3.3 and 3.4), Section 3.3 (safe policy improvement), Algorithm 1"
  - paper: "Sergey Levine, Aviral Kumar, George Tucker and Justin Fu, Offline reinforcement learning, tutorial, review, and perspectives on open problems, arXiv:2005.01643, 2020"
    locator: the section on distributional shift and the section on policy constraints and conservative methods
  - paper: "Scott Fujimoto, David Meger and Doina Precup, Off-policy deep reinforcement learning without exploration, Proceedings of the 36th International Conference on Machine Learning (ICML), PMLR 97, 2019, pages 2052 to 2062"
    locator: extrapolation error and batch-constrained Q-learning (BCQ)
  - paper: "Aviral Kumar, Justin Fu, George Tucker and Sergey Levine, Stabilizing off-policy Q-learning via bootstrapping error reduction, Advances in Neural Information Processing Systems 32 (NeurIPS 2019)"
    locator: bootstrapping error from out-of-distribution actions, and BEAR
---

Conservative Q-learning (CQL; Kumar, Zhou, Tucker and Levine, 2020) is a Q-learning method for [offline reinforcement learning](/offline-reinforcement-learning/), where the agent learns from a fixed dataset $D$ and cannot collect more. Plain offline Q-learning, such as [fitted Q-iteration](/fitted-q-iteration/), computes targets $r + \gamma \max_{a'} Q(s', a')$ that can pick actions the data never tried, whose values nothing has corrected. These values are often too high, and the greedy policy goes for them. CQL adds a penalty to the regression loss that pushes Q-values down over all actions and up on the actions in the data. The variant CQL(H) (equation 4 of the paper) minimizes

$$\alpha\, \mathbb{E}_{s \sim D}\Big[\log \sum_a \exp Q(s, a) - \mathbb{E}_{a \sim \hat\pi_\beta(\cdot \mid s)} Q(s, a)\Big] + \tfrac12\, \mathbb{E}_{(s, a, s') \sim D}\Big[\big(Q(s, a) - \hat{\mathcal B} \hat Q^k(s, a)\big)^2\Big],$$

where $\hat\pi_\beta$ is the behavior policy of the data and $\hat{\mathcal B}$ the empirical Bellman operator. The paper proves that, with the right form of the penalty, the learned value is a lower bound on the true value of the learned policy.

## In plain words

Learning only from old records is risky. The records show what happened after some actions. For actions nobody tried, the method has to guess, and a guess that is too optimistic looks like the best choice. The agent then picks exactly the actions it knows least about.

CQL makes the guesses pessimistic. During training it pushes all action values down, and pushes the values of the recorded actions back up. Actions that the records support keep realistic values. Actions that the records do not support end up low, so the agent does not pick them. A weight $\alpha$ sets how strong the push is.

## The problem

The input is a dataset $D$ of $N$ transitions $(s, a, r, s', \text{done})$ from an unknown MDP, collected by some behavior policy $\pi_\beta$, and a discount $\gamma < 1$. The output is a policy, ideally with high return. No new data can be collected. This is the [offline reinforcement learning](/offline-reinforcement-learning/) problem. Its main difficulty is *distribution shift*: a learned policy visits actions and states that $D$ does not cover, and the [deadly triad](/deadly-triad/) of bootstrapping, function approximation and off-policy data makes errors on those actions grow instead of shrink.

## The algorithm

The tabular form of CQL(H) with the max backup, the Q-learning variant of Algorithm 1 in the paper. $n(s, a)$ counts the transitions at $(s, a)$, $n(s) = \sum_a n(s, a)$, and $\sigma(s, \cdot)$ is the softmax of $Q(s, \cdot)$, which is the gradient of $\log \sum_a \exp Q(s, a)$.

```pseudo id=main
CQL-H(D, γ, α, K, G, η)
L1  Q ← 0 on all pairs
L2  for k ← 1 to K do
L3      ȳ(s, a) ← mean of r + γ (1 − done) max_a′ Q(s′, a′) over the transitions at (s, a) in D
L4      repeat G times
L5          σ(s, ·) ← softmax Q(s, ·) for each s
L6          g(s, a) ← (1/N) [α n(s) σ(s, a) − α n(s, a) + n(s, a) (Q(s, a) − ȳ(s, a))]
L7          Q ← Q − η g
L8  return Q and its greedy policy
```

Line L6 is the exact gradient of the loss above, with the empirical distribution of $D$ for $s$ and for $\hat\pi_\beta$, and with the targets $\bar y$ frozen during the inner loop. For a pair with $n(s, a) = 0$, $g(s, a) = \alpha n(s) \sigma(s, a) / N > 0$, so line L7 lowers its value at every step. Nothing pulls it back up.

**With function approximation.** The paper's version for large problems replaces the table by a network and line L7 by $G$ minibatch steps, like [DQN](/dqn/). For continuous actions it adds a policy trained like [soft actor-critic](/soft-actor-critic/), and estimates the log-sum-exp by importance sampling over sampled actions. It can also choose $\alpha$ automatically by a dual (Lagrange) step that keeps the penalty term near a target $\tau$.

**The family.** Equation 3 of the paper, CQL(R), takes a minimization over a distribution $\mu$ regularized by $\mathcal R(\mu)$. With $\mathcal R$ the entropy, the inner maximization over $\mu$ gives the log-sum-exp, which is CQL(H); with a KL divergence to a prior $\rho$, it gives CQL($\rho$). Equation 2 is the policy evaluation form, which uses $\mathbb{E}_{a \sim \mu}$ in place of the log-sum-exp for a fixed policy $\mu = \pi$.

## Example

The corridor has states 0 to 3 and three actions: right (from state 3 it ends the episode), stay, and left. Every step costs 1, and $\gamma = 0.9$. The data has, in each state, four transitions of "right" and one of "stay", and no "left". So $N = 20$, and "left" is never in the data.

With $\alpha = 1$, $K = 100$, $G = 50$, $\eta = 2$, CQL(H) gives these values, rounded, next to the exact $Q^\pi$ of its greedy policy $\pi$ (always right, which is optimal):

| state | CQL right | CQL stay | CQL left | $Q^\pi$ right | $Q^\pi$ stay | $Q^\pi$ left |
|---|---|---|---|---|---|---|
| 0 | $-3.193$ | $-4.206$ | $-10.67$ | $-3.439$ | $-4.095$ | $-4.095$ |
| 1 | $-2.530$ | $-3.576$ | $-10.03$ | $-2.710$ | $-3.439$ | $-4.095$ |
| 2 | $-1.783$ | $-2.868$ | $-9.30$ | $-1.900$ | $-2.710$ | $-3.439$ |
| 3 | $-0.944$ | $-2.072$ | $-8.48$ | $-1.000$ | $-1.900$ | $-2.710$ |

The missing action "left" is far below its true value in every state. Tabular fitted Q-iteration on the same data never updates "left", so it stays at its initial value 0, above its true value of $-2.71$ to $-4.10$. Then every target $r + \gamma \max_{a'} Q(s', a')$ uses that 0, all seen values become $-1$, and the greedy policy is "left" in every state. That policy never reaches the end and has true value $-1/(1 - 0.9) = -10$, against $-3.439$ for the optimal policy from state 0.

The table also shows that CQL(H) with the max backup is not a pointwise lower bound: the frequent action "right" ends up a little *above* $Q^\pi$, because the penalty pushes it up by about $\alpha (1 - n(s)\sigma / n(s, a))$. The lower-bound theorems below are for the evaluation forms.

## Correctness

The paper's guarantees are about the fixed points of the tabular updates, with the empirical Bellman operator $\hat{\mathcal B}^\pi$ close to $\mathcal B^\pi$ with probability $1 - \delta$ (a concentration term in $1 / \sqrt{n(s, a)}$).

1. **Theorem 3.1 (pointwise bound).** For the evaluation update of equation 1, which only pushes down under a distribution $\mu$, the fixed point satisfies $\hat Q^\pi \le Q^\pi$ at every $(s, a)$ for $\alpha$ large enough. If $\hat{\mathcal B}^\pi = \mathcal B^\pi$, any $\alpha > 0$ is enough.
2. **Theorem 3.2 (value bound).** For equation 2, which also pushes up on the data, with $\mu = \pi$ and $\hat\pi_\beta(a \mid s) > 0$, the value satisfies $\hat V^\pi(s) = \mathbb{E}_{\pi(a \mid s)}[\hat Q^\pi(s, a)] \le V^\pi(s)$ for all $s$ in $D$, for $\alpha$ large enough; any $\alpha > 0$ is enough if $\hat{\mathcal B}^\pi = \mathcal B^\pi$. The single values $\hat Q^\pi(s, a)$ need not be below $Q^\pi(s, a)$.
3. **Theorems 3.3 and 3.4.** When the policy changes slowly between iterations, CQL(H) with policy updates also gives lower-bounded values, and the penalty widens the gap between in-data and out-of-data actions.

The proof page proves Theorem 3.2 in the exact case $\hat{\mathcal B}^\pi = \mathcal B^\pi$, with the closed form of the gap, and the facts used in the example: the penalty gradient on a missing action is positive, and tabular FQI never moves a missing action. The implementation checks Theorem 3.2 on 40 random MDPs with exact backups and finds, as the theorem allows, pairs where $\hat Q^\pi(s, a) > Q^\pi(s, a)$.

## Complexity

In the tabular form, line L3 costs $O(N + S A)$ and each inner step $O(S A)$, so $K$ iterations cost $O(K (N + G S A))$ time, with $O(S A)$ space for the tables and counts. With a network, each gradient step costs one minibatch of forward and backward passes plus, for continuous actions, the sampled actions for the log-sum-exp; the paper reports a modest overhead over [soft actor-critic](/soft-actor-critic/).

## Properties

- **Offline.** Uses only $D$; never acts.
- **Pessimistic on unseen actions.** Values of actions outside the data drop without bound in the tabular case, at a rate that slows as their softmax weight shrinks.
- **A lower bound in expectation, not pointwise.** CQL(H) can raise the values of frequent data actions above their true values.
- **One hyperparameter that matters.** $\alpha$ trades conservatism against fitting the Bellman targets; too large and the policy copies the behavior policy, too small and it acts like plain offline Q-learning.

## Variants and improvements

- **CQL-Lagrange.** Tunes $\alpha$ by gradient ascent on a dual variable so that the penalty term stays near a threshold $\tau$.
- **CQL($\rho$).** Uses a KL penalty to a prior $\rho$, such as the previous policy, in place of the entropy.
- **Cal-QL** (Nakamoto and others, 2023) keeps the CQL values above those of a reference policy so that later online fine-tuning starts well.
- **Other pessimistic methods.** [Offline reinforcement learning](/offline-reinforcement-learning/) also has policy constraint methods (BCQ, BEAR, TD3+BC) and in-sample methods such as implicit Q-learning, which never query unseen actions.

## When to use it

Use CQL when you have a fixed dataset, no simulator, and a policy must do better than the one that made the data. It works with discrete actions (with a [DQN](/dqn/) backbone) and continuous actions (with a soft actor-critic backbone). If the data comes from one expert, [imitation learning](/imitation-learning/) is simpler and often as good. If you can collect new data safely, online methods are better.

## Pitfalls

- **Choosing $\alpha$ without online tests.** Offline, you cannot measure the policy's return directly. [Off-policy evaluation](/off-policy-evaluation/) estimates are themselves noisy. The paper's Lagrange version helps, but the threshold $\tau$ is still a choice.
- **Reading the values as accurate.** The values are biased low on purpose. Do not use them as estimates of the policy's return.
- **Narrow data.** If the data covers one action per state, CQL can do little more than copy it.
- **Log-sum-exp overflow.** Compute it with the [log-sum-exp trick](/log-sum-exp-trick/); the softmax at line L5 subtracts the maximum first.

## Implementations

## History

Fujimoto, Meger and Precup (2019) named the problem *extrapolation error* and proposed BCQ, which keeps the policy near the data. Kumar, Fu, Tucker and Levine (2019) analyzed the same effect as bootstrapping error and proposed BEAR, which constrains the policy's support. Kumar, Zhou, Tucker and Levine (2020) moved the constraint from the policy to the values: CQL learns a lower bound on the value and lets the policy be greedy with respect to it. On the D4RL benchmarks it improved on earlier offline methods, by factors of 2 to 5 in final return on some of the harder tasks.

## References
