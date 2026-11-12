---
tag: CP12JX
kind: algorithm
slug: ddpg
name: Deep deterministic policy gradient
aliases:
- DDPG
- deep DPG
area: machine-learning/reinforcement-learning
level: advanced
summary: "Off-policy actor-critic for continuous actions: a critic learned by Q-learning targets from replay, a deterministic actor moved along grad_a Q, slowly tracking target networks and noisy exploration."
solves: [rl-control]
model: real-ram
complexity:
  vars: {n: the number of environment steps, M: the minibatch size, p: the number of actor parameters, q: the number of critic parameters, C: the replay capacity}
  time: {worst: "O(n M (p + q))"}
  space: {extra: "O(C + p + q)"}
properties: {deterministic: false, online: true, exact: false, recursive: false}
history:
  year: 2015
  people: [Timothy P. Lillicrap, Jonathan J. Hunt, Alexander Pritzel, Nicolas Heess, Tom Erez, Yuval Tassa, David Silver, Daan Wierstra]
  note: "Lillicrap et al. combined the deterministic policy gradient with the replay buffer and target networks of DQN, and learned more than 20 simulated physics tasks, some from pixels, with one set of hyperparameters (arXiv 2015, ICLR 2016)."
prereqs: [deterministic-policy-gradient, dqn, experience-replay]
see_also: [td3, soft-actor-critic, actor-critic, double-q-learning, q-learning, adam, ppo, stochastic-gradient-descent]
sources:
  - paper: "Timothy P. Lillicrap, Jonathan J. Hunt, Alexander Pritzel, Nicolas Heess, Tom Erez, Yuval Tassa, David Silver and Daan Wierstra, Continuous control with deep reinforcement learning, International Conference on Learning Representations, 2016, arXiv:1509.02971"
    locator: Section 3 (the critic loss, the actor update, replay, soft target updates, batch normalization and Ornstein-Uhlenbeck exploration), Algorithm 1, Section 7 (experiment details and hyperparameters)
  - paper: "David Silver, Guy Lever, Nicolas Heess, Thomas Degris, Daan Wierstra and Martin Riedmiller, Deterministic policy gradient algorithms, Proceedings of the 31st International Conference on Machine Learning, PMLR 32(1), 2014, pages 387 to 395"
    locator: Section 3.1 Theorem 1 and Section 4.2 (off-policy deterministic actor-critic)
  - paper: doi:10.1038/nature14236
    title: "Volodymyr Mnih et al., Human-level control through deep reinforcement learning, Nature 518, 2015, pages 529 to 533"
    locator: Methods (experience replay and the target network)
  - paper: doi:10.1103/PhysRev.36.823
    title: "George E. Uhlenbeck and Leonard S. Ornstein, On the theory of the Brownian motion, Physical Review 36(5), 1930, pages 823 to 841"
    locator: the mean-reverting Gaussian process used for exploration noise
  - paper: "Scott Fujimoto, Herke van Hoof and David Meger, Addressing function approximation error in actor-critic methods, Proceedings of the 35th International Conference on Machine Learning, PMLR 80, 2018, pages 1587 to 1596, arXiv:1802.09477"
    locator: Section 4 (overestimation bias in DDPG) and Section 5 (target networks and delayed updates)
---

Deep deterministic policy gradient (DDPG) of Lillicrap et al. (2016) is an off-policy [actor-critic](/actor-critic/) method for continuous actions. A critic $Q_w(s, a)$ learns action values from a replay buffer, with the same tools that made [DQN](/dqn/) stable: [experience replay](/experience-replay/) and target networks. A deterministic actor $\mu_\theta(s)$ is trained by the [deterministic policy gradient](/deterministic-policy-gradient/): it moves its action in the direction $\nabla_a Q_w(s, a)$ that the critic says improves the value. Where DQN needs $\max_a Q(s', a)$, which is an optimization problem in a continuous action space, DDPG uses the actor's action $\mu(s')$ instead. Exploration comes from noise added to the actor's action, and the target networks follow the learned ones slowly by *soft updates* $w' \leftarrow \tau w + (1 - \tau) w'$. DDPG learned many simulated control tasks, some from pixels, but it is sensitive to hyperparameters and overestimates values; [TD3](/td3/) and [soft actor-critic](/soft-actor-critic/) fix much of this.

## In plain words

DDPG has two parts. A judge learns to score any action in any situation by how much reward follows. A player picks one exact action in each situation, and keeps nudging its choice in the direction the judge scores higher. The judge learns from a memory of past moves, mixed up so that consecutive moves do not mislead it. To stop the judge from chasing its own changing guesses, it compares itself with slow copies of the judge and the player, which drift toward the current ones a little at each step. To discover new actions, the player adds random wobble to its moves while it practises.

## The problem

The setting is [reinforcement learning control](/rl-control/) in a [Markov decision process](/markov-decision-process/) with a continuous action space $\mathbb{R}^n$, discount $\gamma$, and unknown dynamics that can only be sampled. The goal is a deterministic policy $\mu_\theta$ that maximizes the expected return. [Q-learning](/q-learning/) needs $\max_a Q(s, a)$ at every update, which is expensive or impossible over a continuous action set, and on-policy gradient methods need fresh data for every update. DDPG learns from old data and avoids the maximization.

## The algorithm

The actor is $\mu_\theta$, the critic $Q_w$, their targets $\mu_{\theta'}$ and $Q_{w'}$, initialized as copies. $\mathcal{N}_t$ is exploration noise, in the paper an Ornstein-Uhlenbeck process $x_{t+1} = x_t + \theta_{\text{OU}}(m - x_t) + \sigma \varepsilon_t$ with $\theta_{\text{OU}} = 0.15$ and $\sigma = 0.2$, which gives temporally correlated noise.

```pseudo id=main
DDPG(μ_θ, Q_w, γ, τ, M)
L1  for each environment step t do
L2      a ← μ_θ(s) + 𝒩_t
L3      execute a, observe r and s′, and store (s, a, r, s′, done) in the replay buffer D
L4      sample a minibatch of M transitions (s_i, a_i, r_i, s′_i, done_i) from D
L5      y_i ← r_i + γ (1 − done_i) Q_w′(s′_i, μ_θ′(s′_i))
L6      w ← w − η_Q ∇_w (1/M) Σ_i (Q_w(s_i, a_i) − y_i)²
L7      θ ← θ + η_μ (1/M) Σ_i ∇_θ μ_θ(s_i) ∇_a Q_w(s_i, a)|_{a = μ_θ(s_i)}
L8      w′ ← τ w + (1 − τ) w′ and θ′ ← τ θ + (1 − τ) θ′
```

Line L5 is the [Q-learning](/q-learning/) target with the target actor's action in place of the maximum, and the target networks in place of the learned ones. Line L6 is a semi-gradient step: $y_i$ is held fixed. Line L7 is the [deterministic policy gradient](/deterministic-policy-gradient/) with the critic in place of $Q^\mu$, at states from the replay buffer instead of the actor's own state distribution, which makes it the off-policy form. In a network, it is computed by backpropagating $Q_w(s, \mu_\theta(s))$ into $\theta$ with $w$ held fixed. Line L8 is the soft target update; with $\tau = 1$ it is DQN's hard copy. The paper used Adam with learning rates $10^{-4}$ (actor) and $10^{-3}$ (critic), $\gamma = 0.99$, $\tau = 0.001$, minibatches of 64, a replay buffer of $10^6$ transitions, and batch normalization of the low-dimensional inputs. When an episode stops because of a time limit, not a terminal state, the transition is stored with $\text{done} = 0$, so that the target still bootstraps.

## Example

Take the scalar linear quadratic problem $s' = s + a$, $r = -(s^2 + a^2)$, $\gamma = 0.9$, start states uniform in $[-1, 1]$ and episodes of 10 steps. The optimal policy is linear, $a = k^* s$, with $V^*(s) = -P s^2$ where $0.9 P^2 - 0.8 P - 1 = 0$, so $P \approx 1.588$ and $k^* = -0.9 P / (1 + 0.9 P) \approx -0.588$. The optimal action values are $Q^*(s, a) \approx -2.430 s^2 - 2.859 s a - 2.430 a^2$.

Run DDPG with the linear actor $\mu(s) = k s$, the quadratic critic $Q_w(s, a) = w_1 s^2 + w_2 s a + w_3 a^2$, step sizes 0.02, $\tau = 0.05$, minibatches of 32 and Ornstein-Uhlenbeck noise with $\sigma = 0.1$, from $k = -0.2$. After 3000 steps, six seeds give $k$ between $-0.71$ and $-0.48$; after 6000 steps, between $-0.67$ and $-0.60$. With one seed, the critic after 6000 steps is $(-2.94, -2.22, -1.76)$. That is far from $Q^*$, but its greedy action $-w_2 s / (2 w_3) \approx -0.63 s$ agrees with the actor. The actor only follows $\nabla_a Q_w$ at its own actions, so it needs the critic's slope there, not its values.

The soft update with $\tau = 0.05$ makes the target an exponential moving average: after $k$ updates with fixed learned weights, $w'_k = w + 0.95^k (w'_0 - w)$, so the target closes half the gap in about 14 updates.

## Correctness

DDPG has no convergence guarantee with function approximation; it combines off-policy learning, bootstrapping and nonlinear approximation. The correctness proof shows what each line computes.

1. **Actor step.** With $Q_w = Q^\mu$, the expected actor update over states with law $\rho$ is $\int \nabla_\theta \mu_\theta(s) \nabla_a Q^\mu(s, a)|_{a = \mu_\theta(s)} \rho(ds)$. For $\rho$ the normalized discounted visitation of $\mu$, this is $(1 - \gamma) \nabla J(\mu_\theta)$ by the deterministic policy gradient theorem; for the replay distribution it is the off-policy deterministic gradient of Silver et al.
2. **Critic step.** For fixed targets, line L6 is a gradient step on a least squares regression of $Q_w(s_i, a_i)$ onto $y_i$. With exact fitting and frozen target networks, the critic computes the Bellman operator of $\mu_{\theta'}$ applied to $Q_{w'}$ at the replayed pairs.
3. **Soft target update.** After $k$ updates, $w'_k = (1 - \tau)^k w'_0 + \sum_{j=1}^{k} \tau (1 - \tau)^{k-j} w_j$, an exponential moving average of the learned weights whose coefficients sum to 1.
4. **Exploration noise.** The Ornstein-Uhlenbeck recursion has mean $m + (1 - \theta_{\text{OU}})^t (x_0 - m)$ and, for $0 < \theta_{\text{OU}} < 2$, the stationary variance $\sigma^2 / (1 - (1 - \theta_{\text{OU}})^2)$, with correlation $1 - \theta_{\text{OU}}$ between consecutive steps.

## Complexity

Each environment step does one actor evaluation, one buffer write and one minibatch update. For linear models with $p$ actor and $q$ critic parameters, the update costs $O(M (p + q))$: $M$ target evaluations, $M$ critic gradients and $M$ actor gradients. So $n$ steps cost $O(n M (p + q))$, and memory is $O(C + p + q)$ for a buffer of capacity $C$ plus four parameter vectors. For networks, $p$ and $q$ become the costs of forward and backward passes. Sampling from a list-based buffer is $O(M)$ per minibatch.

## Properties

- **Off-policy.** Any stored transition can be reused, regardless of the policy that collected it.
- **Deterministic actor.** The learned policy outputs one action; exploration is added only during training.
- **Online.** One gradient update per environment step, with constant memory beyond the buffer.
- **Biased critic.** The target uses $Q_{w'}$ at the actor's action, which the actor pushes toward the critic's overestimates.
- **Randomized.** Exploration noise and minibatch sampling.

## Variants and improvements

- **TD3.** Twin critics with a minimum in the target, delayed actor updates and target policy smoothing ([TD3](/td3/)).
- **Soft actor-critic.** A stochastic actor with an entropy bonus and twin critics ([soft actor-critic](/soft-actor-critic/)).
- **Distributed distributional DDPG (D4PG).** Distributional critics, $n$-step returns, prioritized replay and many actors.
- **Exploration.** Uncorrelated Gaussian noise works as well as Ornstein-Uhlenbeck noise on most benchmarks, and parameter space noise is another option.
- **NAF.** Normalized advantage functions use a critic quadratic in the action, so the maximum is in closed form and no separate actor is needed.

## When to use it

Use DDPG for continuous control when samples are costly and an off-policy method is needed, and when a deterministic policy is acceptable. In practice, prefer [TD3](/td3/) or [soft actor-critic](/soft-actor-critic/), which keep the same structure and are much more robust. For discrete actions, use [DQN](/dqn/) or its successors instead.

## Pitfalls

- **Overestimation.** The actor climbs the critic's errors, and the target bootstraps from them; values can grow without bound. TD3's twin critics address this.
- **Brittle hyperparameters.** Learning rates, $\tau$, the noise scale and reward scale strongly affect results; small changes can make training diverge.
- **Time limits.** Marking time-limit ends as terminal makes the critic learn a wrong, time-dependent value.
- **Action bounds.** With bounded actions, a tanh output layer keeps the actor inside the bounds, but the gradient vanishes near the bounds; clip the noisy action, not the actor output, to the bounds.
- **Exploration.** Noise that is too small never finds better actions; noise that is too large fills the buffer with useless data.

## Implementations

## History

The [deterministic policy gradient](/deterministic-policy-gradient/) theorem of Silver et al. (2014) gave an actor-critic update without an integral over actions, and [DQN](/dqn/) (Mnih et al., 2015) showed that replay and target networks stabilize Q-learning with deep networks. Lillicrap, Hunt, Pritzel, Heess, Erez, Tassa, Silver and Wierstra combined the two in DDPG (arXiv 2015, ICLR 2016) and solved more than 20 simulated physics tasks, including cartpole swing-up, reaching, legged locomotion and driving, several of them directly from pixels. Fujimoto, van Hoof and Meger (2018) showed that DDPG overestimates values and proposed [TD3](/td3/).

## References
