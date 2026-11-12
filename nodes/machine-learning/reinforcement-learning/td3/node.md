---
tag: K6H73Z
kind: algorithm
slug: td3
name: Twin delayed deep deterministic policy gradient
aliases:
- TD3
- twin delayed DDPG
area: machine-learning/reinforcement-learning
level: advanced
summary: "DDPG with three changes: the target takes the minimum of two critics, the actor and targets update once every d critic steps, and the target action gets clipped noise."
solves: [rl-control]
model: real-ram
complexity:
  vars: {n: the number of environment steps, M: the minibatch size, p: the number of actor parameters, q: the number of parameters of one critic, C: the replay capacity}
  time: {worst: "O(n M (p + q))"}
  space: {extra: "O(C + p + q)"}
properties: {deterministic: false, online: true, exact: false, recursive: false}
history:
  year: 2018
  people: [Scott Fujimoto, Herke van Hoof, David Meger]
  note: "Fujimoto, van Hoof and Meger showed that the overestimation bias of Q-learning also affects deterministic actor-critic methods, and fixed DDPG with a pessimistic twin critic, delayed policy updates and target smoothing."
prereqs: [ddpg, double-q-learning]
see_also: [deterministic-policy-gradient, soft-actor-critic, double-dqn, actor-critic, experience-replay, dqn, adam, ppo]
sources:
  - paper: "Scott Fujimoto, Herke van Hoof and David Meger, Addressing function approximation error in actor-critic methods, Proceedings of the 35th International Conference on Machine Learning, PMLR 80, 2018, pages 1587 to 1596, arXiv:1802.09477"
    locator: Section 4.1 (overestimation in actor-critic), Section 4.2 (clipped double Q-learning, the target with the minimum of two critics), Section 5.2 (delayed policy updates), Section 5.3 (target policy smoothing), Algorithm 1, Section 6 (experiments and hyperparameters), supplementary material (convergence of clipped double Q-learning in the finite case)
  - paper: "Hado van Hasselt, Double Q-learning, Advances in Neural Information Processing Systems 23, 2010, pages 2613 to 2621"
    locator: the overestimation of the maximum of noisy estimates and the two-estimator fix
  - paper: "Timothy P. Lillicrap, Jonathan J. Hunt, Alexander Pritzel, Nicolas Heess, Tom Erez, Yuval Tassa, David Silver and Daan Wierstra, Continuous control with deep reinforcement learning, International Conference on Learning Representations, 2016, arXiv:1509.02971"
    locator: Algorithm 1 (the DDPG algorithm that TD3 modifies)
  - paper: "Tuomas Haarnoja, Aurick Zhou, Kristian Hartikainen, George Tucker, Sehoon Ha, Jie Tan, Vikash Kumar, Henry Zhu, Abhishek Gupta, Pieter Abbeel and Sergey Levine, Soft actor-critic algorithms and applications, arXiv:1812.05905, 2018"
    locator: Section 5 (the use of two Q-functions with the minimum, taken from TD3)
---

Twin delayed deep deterministic policy gradient (TD3) of Fujimoto, van Hoof and Meger (2018) is [DDPG](/ddpg/) with three changes that reduce the errors of the critic and their effect on the actor. **Clipped double Q-learning:** two critics $Q_{w_1}, Q_{w_2}$ are learned, and both regress on the target $y = r + \gamma \min_{j = 1, 2} Q_{w'_j}(s', \tilde a)$, which counters the overestimation that a maximum over noisy estimates causes ([double Q-learning](/double-q-learning/)). **Delayed policy updates:** the actor and all target networks change once every $d$ critic updates, so that the critic's error shrinks before the actor follows it. **Target policy smoothing:** the target action is $\tilde a = \mu_{\theta'}(s') + \mathrm{clip}(\varepsilon, -c, c)$ with Gaussian $\varepsilon$, so that the target averages the critic over nearby actions and the actor cannot exploit a narrow peak. The actor is still trained by the [deterministic policy gradient](/deterministic-policy-gradient/), on the first critic. TD3 is much more reliable than DDPG on continuous control benchmarks, and its twin critics were adopted by [soft actor-critic](/soft-actor-critic/).

## In plain words

DDPG has a judge that scores actions and a player that follows the judge. The judge makes errors, and the player seeks out actions the judge scores too high, so errors grow. TD3 trains two judges and always believes the more pessimistic one when it builds its learning targets. It lets the judges learn for a few steps before the player moves, so the player follows better advice. And when it asks what the next action is worth, it asks about a few nearby actions, not one exact point, so a single lucky spike in the score cannot fool it.

## The problem

The setting is that of [DDPG](/ddpg/): continuous actions, off-policy learning from a replay buffer, a deterministic actor and a learned critic. In [Q-learning](/q-learning/), the maximum over noisy estimates is biased upward; this is the problem that [double Q-learning](/double-q-learning/) and [double DQN](/double-dqn/) address. Fujimoto et al. showed that a deterministic actor that climbs $\nabla_a Q_w$ causes the same bias, because the actor chooses actions where the critic is too high, and that bootstrapping then spreads the error to other states. Double DQN's fix of evaluating the target with a second network helps little here, because the target and the learned actor change slowly and stay close. The task is to keep DDPG's structure and remove this bias and the variance that feeds it.

## The algorithm

Initialize the actor $\mu_\theta$, two critics with different weights $w_1 \ne w_2$, and target copies $\theta', w'_1, w'_2$.

```pseudo id=main
TD3(μ_θ, Q_w1, Q_w2, γ, τ, σ, σ̃, c, d, M)
L1  for each environment step t do
L2      a ← μ_θ(s) + ε with ε ~ N(0, σ²), clipped to the action bounds
L3      execute a, observe r and s′, and store (s, a, r, s′, done) in the replay buffer D
L4      sample a minibatch of M transitions from D
L5      ã_i ← μ_θ′(s′_i) + clip(ε̃_i, −c, c) with ε̃_i ~ N(0, σ̃²)
L6      y_i ← r_i + γ (1 − done_i) min(Q_w′1(s′_i, ã_i), Q_w′2(s′_i, ã_i))
L7      w_j ← w_j − η_Q ∇ (1/M) Σ_i (Q_wj(s_i, a_i) − y_i)² for j = 1, 2
L8      if this is the k-th critic update and k mod d = 0 then
L9          θ ← θ + η_μ (1/M) Σ_i ∇_θ μ_θ(s_i) ∇_a Q_w1(s_i, a)|_{a = μ_θ(s_i)}
L10         w′_j ← τ w_j + (1 − τ) w′_j for j = 1, 2, and θ′ ← τ θ + (1 − τ) θ′
```

Lines L5 and L6 are the smoothed, clipped double target; both critics regress on the same $y$, so they differ only through their initialization and the noise of learning. The smoothed action is also clipped to the action bounds in practice. The paper used $\sigma = 0.1$ for exploration, $\tilde\sigma = 0.2$ and $c = 0.5$ for smoothing, $d = 2$, $\tau = 0.005$, Adam with learning rate $10^{-3}$ and minibatches of 100. Exploration noise is plain Gaussian; the Ornstein-Uhlenbeck noise of DDPG gave no benefit.

## Example

**One target.** With $\gamma = \tfrac12$, target actor $\mu'(s) = -\tfrac12 s$, target critics $Q'_1(s, a) = -s^2 - a^2$ and $Q'_2(s, a) = -2 s^2 + 1$, and a transition with $r = 1$ and $s' = 2$: the target action is $\tilde a = -1$ when $\tilde\varepsilon = 0$, the critics give $-5$ and $-7$, and $y = 1 + \tfrac12 \cdot (-7) = -\tfrac52$. DDPG with critic 1 alone would use $y = -\tfrac32$. With $\mu'(1) = 2$ and $c = \tfrac12$, the noise draws $3$, $-3$, $\tfrac1{10}$ give target actions $\tfrac52$, $\tfrac32$, $\tfrac{21}{10}$: the action never moves more than $c$.

**Bias of the minimum.** If two independent unbiased estimates of a value $q$ have errors uniform on $\{-1, 0, 1\}$, the expected maximum is $q + \tfrac49$ and the expected minimum is $q - \tfrac49$. TD3 accepts the small underestimate, which the actor does not exploit, in place of an overestimate, which it does.

**Learning.** On the scalar problem $s' = s + a$, $r = -(s^2 + a^2)$, $\gamma = 0.9$ of the [DDPG](/ddpg/) page, with the optimal gain $k^* \approx -0.588$, a linear actor, quadratic critics with a constant feature, step sizes 0.03, $\tau = 0.05$, $d = 2$, $\sigma = \tilde\sigma = 0.1$ and $c = 0.25$, five seeds give gains between $-0.61$ and $-0.52$ after 6000 steps. The constant feature matters: smoothing adds $w_3 \mathbb{E}[\mathrm{clip}(\tilde\varepsilon)^2]$ to the target of a critic $w_3 a^2 + \ldots$, and without a constant term the critic must absorb that offset into its other weights.

## Correctness

TD3 has no convergence guarantee with function approximation; the paper proves convergence of clipped double Q-learning only in the finite tabular case. The correctness proof shows what each change computes.

1. **No upward bias from the minimum.** $\mathbb{E}[\min(Q'_1, Q'_2)] \le \min(\mathbb{E} Q'_1, \mathbb{E} Q'_2)$. So if either target critic is unbiased or too low at $(s', \tilde a)$, the target is not too high in expectation.
2. **Smoothing.** Given $s'$, the expected target is $r + \gamma\, \mathbb{E}_{\tilde\varepsilon}[\min_j Q'_j(s', \mu'(s') + \mathrm{clip}(\tilde\varepsilon, -c, c))]$, an average of the critic over actions within $c$ of the target actor's action.
3. **Delay.** After $k$ critic updates, the actor and the targets have changed exactly $\lfloor k / d \rfloor$ times, each time after $d$ fresh critic updates.
4. **Actor step.** The actor update is the deterministic policy gradient with $Q_{w_1}$ as critic, as in DDPG.

## Complexity

Per environment step, TD3 does one actor evaluation, one buffer write, and one minibatch update with two critics; every $d$ steps it also does an actor update and three soft updates. For linear models with $p$ actor parameters and $q$ parameters per critic, this is $O(M (p + q))$ per step, so $O(n M (p + q))$ for $n$ steps, about twice the critic work of DDPG and $1/d$ of its actor work. Memory is $O(C + p + q)$ for the buffer and six parameter vectors.

## Properties

- **Off-policy and online**, like DDPG.
- **Pessimistic targets.** The minimum of two critics trades overestimation for a mild underestimation.
- **Smoother value targets** through target policy smoothing, which acts like a regularizer that makes similar actions have similar values.
- **Randomized.** Exploration noise, target noise and minibatch sampling.

## Variants and improvements

- **Soft actor-critic.** A stochastic actor with entropy regularization, and TD3's minimum of two critics ([soft actor-critic](/soft-actor-critic/)).
- **More critics.** Ensembles with a minimum over a random subset (REDQ) or with truncated mixtures (TQC) tune the amount of pessimism.
- **TD3 with behaviour cloning.** For offline reinforcement learning, TD3+BC adds a term that keeps the actor near the actions in the dataset.
- **Double DQN style target.** Evaluating the target actor's action with the other critic, without the minimum, was tested in the paper and was weaker ([double DQN](/double-dqn/)).

## When to use it

Use TD3 as a strong, simple baseline for continuous control with off-policy data when a deterministic policy is acceptable. It is a direct replacement for [DDPG](/ddpg/) and usually needs less tuning. [Soft actor-critic](/soft-actor-critic/) is often a little better when exploration is hard or when a stochastic policy is useful; for discrete actions use [DQN](/dqn/) variants.

## Pitfalls

- **Identical twins.** If both critics start with the same weights and see the same data, they stay identical and the minimum does nothing; initialize them independently.
- **Actor on the minimum.** The paper trains the actor on $Q_{w_1}$; using the minimum of both in the actor loss is a variant with different behaviour, not the original algorithm.
- **Noise scale versus action scale.** $\sigma$, $\tilde\sigma$ and $c$ are in action units; rescale them when the action range is not $[-1, 1]$.
- **Underestimation.** In some tasks the minimum makes the critic too pessimistic, which slows exploration; ensembles with tuned pessimism address this.
- **Time limits** must not be stored as terminal transitions, as in DDPG.

## Implementations

## History

Van Hasselt (2010) showed that Q-learning overestimates values because it takes a maximum over noisy estimates, and proposed [double Q-learning](/double-q-learning/); [double DQN](/double-dqn/) (2016) carried the idea to deep networks. Fujimoto, van Hoof and Meger (ICML 2018) showed that the same bias arises in deterministic actor-critic methods, proposed TD3, and reported that it beat DDPG, PPO, TRPO, ACKTR and soft actor-critic on the MuJoCo tasks they tested. Soft actor-critic adopted the twin critic minimum in its later version (Haarnoja et al., 2018).

## References
