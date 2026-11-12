---
tag: B23BP5
kind: algorithm
slug: soft-actor-critic
name: Soft actor-critic
area: machine-learning/reinforcement-learning
level: advanced
summary: "Off-policy actor-critic for the maximum entropy objective: twin soft Q critics, a stochastic actor trained with reparameterized actions, and a temperature tuned to a target entropy."
solves: [rl-control]
model: real-ram
complexity:
  vars: {n: the number of environment steps, M: the minibatch size, p: the number of actor parameters, q: the number of parameters of one critic, C: the replay capacity}
  time: {worst: "O(n M (p + q))"}
  space: {extra: "O(C + p + q)"}
properties: {deterministic: false, online: true, exact: false, recursive: false}
history:
  year: 2018
  people: [Tuomas Haarnoja, Aurick Zhou, Pieter Abbeel, Sergey Levine]
  note: "Haarnoja, Zhou, Abbeel and Levine derived soft policy iteration and turned it into an off-policy actor-critic; a second paper the same year added twin critics as the only critics and automatic temperature tuning."
prereqs: [maximum-entropy-rl, actor-critic, experience-replay]
see_also: [td3, ddpg, deterministic-policy-gradient, policy-iteration, double-q-learning, variational-autoencoder, log-sum-exp-trick, ppo]
sources:
  - paper: "Tuomas Haarnoja, Aurick Zhou, Pieter Abbeel and Sergey Levine, Soft actor-critic: off-policy maximum entropy deep reinforcement learning with a stochastic actor, Proceedings of the 35th International Conference on Machine Learning, PMLR 80, 2018, pages 1861 to 1870, arXiv:1801.01290"
    locator: Section 3.1 (maximum entropy objective), Section 4.1 (soft policy iteration, Lemma 1, Lemma 2, Theorem 1), Section 4.2 (the soft value, soft Q and policy objectives and the reparameterization trick), Algorithm 1, Appendix B (proofs), Appendix C (the tanh squashing correction)
  - paper: "Tuomas Haarnoja, Aurick Zhou, Kristian Hartikainen, George Tucker, Sehoon Ha, Jie Tan, Vikash Kumar, Henry Zhu, Abhishek Gupta, Pieter Abbeel and Sergey Levine, Soft actor-critic algorithms and applications, arXiv:1812.05905, 2018"
    locator: Section 5 (automatic entropy adjustment as a constrained problem and its dual), Section 6 (practical algorithm with two Q-functions and no value network), Algorithm 1, Appendix D (hyperparameters)
  - paper: "Tuomas Haarnoja, Haoran Tang, Pieter Abbeel and Sergey Levine, Reinforcement learning with deep energy-based policies, Proceedings of the 34th International Conference on Machine Learning, PMLR 70, 2017, arXiv:1702.08165"
    locator: Section 3 (soft Q-learning, the predecessor that samples from the energy-based policy)
  - paper: "Diederik P. Kingma and Max Welling, Auto-encoding variational Bayes, International Conference on Learning Representations, 2014, arXiv:1312.6114"
    locator: Section 2.4 (the reparameterization trick)
  - paper: "Scott Fujimoto, Herke van Hoof and David Meger, Addressing function approximation error in actor-critic methods, Proceedings of the 35th International Conference on Machine Learning, PMLR 80, 2018, arXiv:1802.09477"
    locator: Section 4.2 (clipped double Q-learning, the minimum of two critics)
---

Soft actor-critic (SAC) of Haarnoja, Zhou, Abbeel and Levine (2018) is an off-policy [actor-critic](/actor-critic/) method for the [maximum entropy](/maximum-entropy-rl/) objective $\mathbb{E}\big[\sum_t \gamma^t (r_t + \alpha \mathcal{H}(\pi(\cdot \mid s_t)))\big]$. It is the function approximation version of **soft policy iteration**, which alternates soft policy evaluation and the improvement $\pi_{\text{new}}(\cdot \mid s) \propto \exp(Q^{\pi_{\text{old}}}(s, \cdot) / \alpha)$ and converges to the soft optimal policy in the tabular case. In SAC, two critics learn the soft action value from a [replay buffer](/experience-replay/) with the target $r + \gamma(\min_j Q_{w'_j}(s', a') - \alpha \log \pi(a' \mid s'))$, where $a'$ is a fresh sample from the current policy. The actor is a Gaussian, squashed by tanh for bounded actions, trained to minimize $\mathbb{E}[\alpha \log \pi(a \mid s) - \min_j Q_{w_j}(s, a)]$ through the reparameterized action $a = \tanh(\mu_\phi(s) + \sigma_\phi(s) \xi)$. The later version also tunes $\alpha$ so that the policy entropy stays near a target. SAC is stable, sample efficient and needs little tuning, and is a standard method for continuous control.

## In plain words

SAC learns from stored experience, like DDPG and TD3, but its player acts at random on purpose. It is paid for reward and also for keeping its choices spread out. Two judges score actions, and the player believes the lower score. The player improves by moving its whole spread of actions toward the actions the judges like, while it keeps as much spread as the bonus asks for. A dial sets how much spread is worth. In the newer version the dial turns itself so that the spread stays near a chosen level.

## The problem

Off-policy deterministic methods such as [DDPG](/ddpg/) reuse data well but are brittle: they are sensitive to step sizes and noise scales, and their critics overestimate. On-policy methods such as [PPO](/ppo/) are stable but need fresh data for every update. SAC aims for both: off-policy reuse of data, and a stochastic policy whose exploration is part of the objective, not added noise. The objective is the [maximum entropy](/maximum-entropy-rl/) return with temperature $\alpha > 0$, in an MDP with continuous actions.

## The algorithm

**Soft policy iteration (tabular).** For a policy $\pi$, the soft Bellman operator is $(T^\pi Q)(s, a) = r(s, a) + \gamma\, \mathbb{E}_{s'}[V(s')]$ with $V(s') = \mathbb{E}_{a' \sim \pi}[Q(s', a') - \alpha \log \pi(a' \mid s')]$. Iterating $T^\pi$ gives $Q^\pi$ (Lemma 1 of the paper). The improvement step chooses, from a policy class $\Pi$, the policy that minimizes $\mathrm{KL}\big(\pi'(\cdot \mid s) \,\|\, \exp(Q^{\pi_{\text{old}}}(s, \cdot)/\alpha) / Z(s)\big)$; the result has $Q^{\pi_{\text{new}}} \ge Q^{\pi_{\text{old}}}$ (Lemma 2). Repeating both steps converges to the policy with the largest soft value in $\Pi$ (Theorem 1).

**SAC.** Replace both steps by stochastic gradient steps on minibatches. The actor is $a = \tanh(u)$ with $u = \mu_\phi(s) + \sigma_\phi(s) \xi$, $\xi \sim N(0, I)$, so that $\log \pi(a \mid s) = \log N(u; \mu_\phi(s), \sigma_\phi(s)^2) - \sum_i \log(1 - a_i^2)$.

```pseudo id=main
SAC(π_φ, Q_w1, Q_w2, α, H̄, γ, τ, M)
L1  for each environment step do
L2      sample ξ ~ N(0, I) and act with a ← tanh(μ_φ(s) + σ_φ(s) ξ)
L3      execute a, observe r and s′, and store (s, a, r, s′, done) in the replay buffer D
L4      sample a minibatch of M transitions from D
L5      a′_i ← a fresh sample from π_φ(· | s′_i), with its log density
L6      y_i ← r_i + γ (1 − done_i) (min_j Q_w′j(s′_i, a′_i) − α log π_φ(a′_i | s′_i))
L7      w_j ← w_j − η_Q ∇ (1/M) Σ_i (Q_wj(s_i, a_i) − y_i)² for j = 1, 2
L8      φ ← φ − η_π ∇_φ (1/M) Σ_i (α log π_φ(ã_i | s_i) − min_j Q_wj(s_i, ã_i)) with ã_i = a_φ(s_i, ξ_i), fresh ξ_i
L9      α ← α − η_α (1/M) Σ_i (−log π_φ(ã_i | s_i) − H̄)
L10     w′_j ← τ w_j + (1 − τ) w′_j for j = 1, 2
```

Line L8 is the KL projection of soft policy improvement: $\mathbb{E}_{a \sim \pi}[\alpha \log \pi(a \mid s) - Q(s, a)] = \alpha\, \mathrm{KL}(\pi(\cdot \mid s) \,\|\, e^{Q(s, \cdot)/\alpha} / Z(s)) - \alpha \log Z(s)$. Because $\tilde a$ is a differentiable function of $\phi$ and fixed noise, the gradient flows through the critic's action derivative, which has much lower variance than the likelihood ratio estimator of [REINFORCE](/reinforce/). Line L9 is a gradient step on $J(\alpha) = \mathbb{E}[-\alpha \log \pi(a \mid s) - \alpha \bar{\mathcal H}]$: $\alpha$ rises when the entropy is below the target $\bar{\mathcal H}$, usually $-\dim A$, and falls when it is above. Implementations often step on $\log \alpha$ in place of $\alpha$, which keeps it positive. The first version of SAC also learned a separate state value network and used the minimum of two critics; the second removed the value network and added line L9. The second paper used Adam with learning rate $3 \cdot 10^{-4}$, $\gamma = 0.99$, $\tau = 0.005$, minibatches of 256, a replay buffer of $10^6$ and one gradient step per environment step.

## Example

**Soft policy iteration.** In the two-state MDP of the [maximum entropy RL](/maximum-entropy-rl/) page ($P = [[[1/2, 1/4], [0, 3/4]], [[1/2, 0], [0, 0]]]$, $R = [[1, 0], [0, 3]]$, $\gamma = \tfrac12$) with $\alpha = 1$, start from the uniform policy.

| iteration | $\pi(a_0 \mid 0)$ | $\pi(a_1 \mid 1)$ | $Q(0, a_0)$ | $Q(0, a_1)$ | $Q(1, a_0)$ | $V(0)$ | $V(1)$ |
|---|---|---|---|---|---|---|---|
| 0 | 0.5 | 0.5 | 1.8224 | 0.9192 | 0.5160 | 2.0639 | 2.4511 |
| 1 | 0.7116 | 0.9230 | 1.9697 | 1.1570 | 0.5840 | 2.3360 | 3.0853 |
| 2 | 0.6927 | 0.9180 | 1.9700 | 1.1571 | 0.5843 | 2.3371 | 3.0855 |

Every $Q$ entry increases, as Lemma 2 says, and after two improvements the values agree to four places with the soft optimal values from soft value iteration. ($Q(1, a_1) = 3$ throughout, because that action ends the episode.)

**Function approximation.** On the scalar problem $s' = s + a$, $r = -(s^2 + a^2)$, $\gamma = 0.9$ of the [DDPG](/ddpg/) page, the soft optimal policy is Gaussian with mean $k^* s$, $k^* \approx -0.588$, and variance $\alpha / (2 \cdot 2.429)$, where $-2.429$ is the $a^2$ coefficient of the optimal $Q$. With a linear mean, a learned state-independent $\log \sigma$, quadratic twin critics, $\alpha = 0.1$, step sizes 0.02 and 0.03, $\tau = 0.05$ and no squashing, five seeds give $k$ between $-0.600$ and $-0.590$ and $\log \sigma$ between $-1.95$ and $-1.89$ after 6000 steps, against the optimum $\log \sigma^* \approx -1.94$. With automatic temperature and a target entropy equal to that of $N(0, 0.2^2)$, starting from $\alpha = 0.5$, three seeds give an $\alpha$ that settles between $0.192$ and $0.197$, close to the value $2 \cdot 2.429 \cdot 0.04 \approx 0.194$ that makes the soft optimal standard deviation 0.2.

## Correctness

The correctness proof covers the tabular theory that SAC approximates, and what each update line computes.

1. **Soft policy evaluation (Lemma 1).** $T^\pi$ is a $\gamma$-contraction in the maximum norm when the action set is finite, so its iterates converge to $Q^\pi$.
2. **Soft policy improvement (Lemma 2).** If $\pi_{\text{new}}$ minimizes the KL divergence to $\exp(Q^{\pi_{\text{old}}}/\alpha)/Z$ over a class that contains $\pi_{\text{old}}$, then $Q^{\pi_{\text{new}}} \ge Q^{\pi_{\text{old}}}$ everywhere.
3. **Soft policy iteration (Theorem 1).** With the class of all policies with full support, the iteration converges to a policy whose soft $Q$ is at least that of every such policy.
4. **Reparameterized actor step.** Line L8 is an unbiased estimate of the gradient of the KL projection objective for the current critic.
5. **Temperature step.** Line L9 is an unbiased gradient step on $J(\alpha)$, and its sign moves the entropy toward the target.

Like other deep RL methods, SAC with function approximation has no general convergence guarantee.

## Complexity

Per environment step, SAC samples one action, writes the buffer, and does one minibatch update with two critics, one actor step and one temperature step, each linear in its parameter count. For linear models this is $O(M (p + q))$ per step and $O(n M (p + q))$ in total; memory is $O(C + p + q)$. Unlike [TD3](/td3/), the actor is updated at every step, and each update samples fresh actions for both the target and the actor loss. Tabular soft policy evaluation by iteration costs $O(|S|^2 |A|)$ per sweep, and each improvement step costs $O(|S| |A|)$.

## Properties

- **Off-policy** with a stochastic actor; the replay data may come from any policy, because the critic target samples $a'$ from the current policy.
- **Exploration through the objective.** The policy stays as random as the temperature allows, and the temperature can be tuned automatically.
- **Pessimistic targets** from the minimum of two critics, as in [TD3](/td3/).
- **Low-variance actor gradients** from the reparameterization, the same estimator as in the [variational autoencoder](/variational-autoencoder/).
- **Randomized**: action sampling, target sampling and minibatches.

## Variants and improvements

- **SAC with a value network.** The first version also learned $V_\psi(s)$ with target $\mathbb{E}_{a \sim \pi}[\min_j Q_j(s, a) - \alpha \log \pi(a \mid s)]$ and bootstrapped the critics from a target copy of $V_\psi$.
- **Discrete actions.** With a finite action set, the expectations over $\pi$ can be computed exactly, so neither the target nor the actor needs reparameterization.
- **Soft Q-learning** (Haarnoja et al., 2017), the predecessor, learns only soft $Q$ and samples from $\exp(Q/\alpha)$ with an amortized sampler.
- **Ensembles and high update ratios.** REDQ and related methods use many critics and several gradient steps per environment step for better sample efficiency.
- **Offline RL.** Conservative Q-learning and similar methods add a penalty to a SAC critic so that it does not overvalue actions absent from a fixed dataset.

## When to use it

Use SAC for continuous control from off-policy data when samples are costly and robust behaviour across seeds matters; it is a common first choice in robotics. Compared with [TD3](/td3/), it usually explores better and gives a stochastic policy, at a slightly higher cost per update. If data is cheap and simulation is fast, [PPO](/ppo/) is simpler to scale in parallel; for discrete actions, [DQN](/dqn/) variants or the discrete version of SAC apply.

## Pitfalls

- **Missing squashing correction.** With tanh actions, the log density needs the term $-\sum_i \log(1 - a_i^2)$; without it the entropy, and so the temperature update, is wrong. Clip $1 - a^2$ away from 0.
- **Stale target action.** The target must sample $a'$ from the current policy at $s'$, not use the stored action.
- **Temperature scale.** With a fixed $\alpha$, the right value depends on the reward scale; automatic tuning with target entropy $-\dim A$ removes most of this tuning.
- **Unbounded $\log \sigma$.** Implementations clamp $\log \sigma$ to a range such as $[-20, 2]$ for numerical safety.
- **Time limits** must not be stored as terminal transitions.

## Implementations

## History

Maximum entropy objectives were used in inverse reinforcement learning (Ziebart et al., 2008) and in soft Q-learning (Haarnoja et al., 2017). Haarnoja, Zhou, Abbeel and Levine (ICML 2018) proved convergence of soft policy iteration in the tabular case and derived SAC from it, with a value network, two Q-functions and a reparameterized actor. Later in 2018, Haarnoja and coauthors published a second version that removes the value network, adopts the twin-critic minimum also studied in [TD3](/td3/), tunes the temperature automatically to a target entropy, and showed that SAC could learn to walk on a real quadruped robot.

## References
