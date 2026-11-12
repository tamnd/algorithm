---
tag: S26G9H
kind: algorithm
slug: a2c
name: Advantage actor-critic
aliases:
- A2C
- synchronous advantage actor-critic
area: machine-learning/reinforcement-learning
level: advanced
summary: "Actor-critic that runs N copies of the environment for n steps with the same policy, builds n-step returns bootstrapped from V_w, and takes one gradient step on the whole batch."
solves: [rl-control]
model: real-ram
complexity:
  vars: {K: the number of updates, N: the number of environment copies, n: the number of steps per segment, W: the cost of one evaluation of the actor and the critic with their gradients, d: the number of parameters}
  time: {worst: "O(K N n W)"}
  space: {extra: "O(N n + d)"}
properties: {deterministic: false, online: false, exact: false, recursive: false}
history:
  year: 2017
  people: [Yuhuai Wu, Elman Mansimov, Alec Radford, John Schulman]
  note: "OpenAI released A2C in its Baselines library in 2017 as a synchronous, deterministic version of A3C that did as well; there is no single paper that introduced it."
prereqs: [actor-critic, n-step-td, advantage-function]
see_also: [a3c, reinforce, generalized-advantage-estimation, ppo, trpo, td-error, policy-gradient-theorem, stochastic-gradient-descent]
sources:
  - url: https://openai.com/index/openai-baselines-acktr-a2c/
    title: "OpenAI, OpenAI Baselines: ACKTR and A2C, blog post, August 2017"
    locator: the description of A2C as a synchronous, deterministic variant of A3C
  - paper: "Volodymyr Mnih, Adria Puigdomenech Badia, Mehdi Mirza, Alex Graves, Timothy P. Lillicrap, Tim Harley, David Silver and Koray Kavukcuoglu, Asynchronous methods for deep reinforcement learning, Proceedings of the 33rd International Conference on Machine Learning, PMLR 48, 2016, pages 1928 to 1937, arXiv:1602.01783"
    locator: the asynchronous advantage actor-critic (n-step returns, the shared critic, the entropy bonus), which A2C makes synchronous
  - paper: "Yuhuai Wu, Elman Mansimov, Shun Liao, Roger Grosse and Jimmy Ba, Scalable trust-region method for deep reinforcement learning using Kronecker-factored approximation, Advances in Neural Information Processing Systems 30, 2017, arXiv:1708.05144"
    locator: the experiments, which use synchronous A2C as the first-order baseline of ACKTR
  - paper: "Alfredo V. Clemente, Humberto N. Castejon and Arjun Chandra, Efficient parallel methods for deep reinforcement learning, arXiv:1705.04862, 2017"
    locator: the parallel advantage actor-critic (PAAC), a synchronous batched version of the same algorithm
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: Section 7.1 (n-step returns) and Section 13.5 (actor-critic methods)
---

Advantage actor-critic (A2C) is the synchronous, batched form of the n-step [actor-critic](/actor-critic/) that deep reinforcement learning uses as a standard baseline. It keeps $N$ copies of the environment. In each round, every copy takes $n$ steps with the same current policy $\pi_\theta$. For each step the algorithm computes the [n-step return](/n-step-td/) $\hat G_t$, bootstrapped from the critic $V_w$ at the end of the segment, and the advantage estimate $\hat A_t = \hat G_t - V_w(S_t)$. It then takes one gradient step on the average over the $N n$ samples: the actor along $\hat A_t \nabla \log \pi_\theta(A_t \mid S_t)$ plus an entropy bonus, the critic toward $\hat G_t$. A2C came from the [A3C](/a3c/) paper of Mnih et al. (2016) with the asynchronous workers replaced by one synchronous batch. OpenAI released it in its Baselines library in 2017 and found it as good as A3C. No single paper introduced A2C; the name comes from that release.

## In plain words

Picture several copies of the same game, played at the same time by the same player. Each copy plays a few moves. Then the player stops all copies and looks at the short pieces of play. For each move, a judge estimates how good the position was, and compares this with what really happened in the next few moves plus the judge's estimate at the end of the piece. Moves that did better than the estimate become more likely, worse moves become less likely, and the judge corrects its own estimates. Then all copies continue. Because every learning step looks at many copies, the steps are less noisy, and a graphics card can process them in one go.

## The problem

The setting is [reinforcement learning control](/rl-control/) with a simulator that can run $N$ independent copies of an MDP. The agent learns a stochastic policy $\pi_\theta$ and a [state-value function](/state-value-function/) $V_w$, often as two heads of one network. The aim, as for all actor-critic methods, is a policy with a high expected discounted return. A2C also aims at a good use of hardware: batched forward and backward passes, and no locks or stale parameters.

## The algorithm

Notation: $N$ copies, $n$ steps per round, $\gamma$ the discount, $\eta$ the step size, $\beta$ the entropy weight, $c$ the weight of the critic loss, $H(\pi(\cdot \mid s)) = -\sum_a \pi(a \mid s) \log \pi(a \mid s)$ the entropy, and $D^i_{t+1} = 1$ if the episode of copy $i$ ends at step $t$. A copy whose episode ends restarts at once from the start distribution.

```pseudo id=main
A2C(N, n, γ, η, β, c)
L1  S^i_0 ← a start state for each copy i = 1..N
L2  for k ← 1 to K do
L3      for t ← 0 to n − 1 do                          ▷ all copies use the same θ
L4          for each i: A^i_t ~ π_θ(· | S^i_t); step copy i, observe R^i_{t+1}, D^i_{t+1}, S^i_{t+1}
L5      for each i: G ← V_w(S^i_n)
L6          for t ← n − 1 down to 0: G ← R^i_{t+1} + γ (1 − D^i_{t+1}) G; Ĝ^i_t ← G
L7      Â^i_t ← Ĝ^i_t − V_w(S^i_t) for all i, t
L8      g_θ ← (1 / Nn) Σ_{i,t} [Â^i_t ∇_θ log π_θ(A^i_t | S^i_t) + β ∇_θ H(π_θ(· | S^i_t))]
L9      g_w ← (1 / Nn) Σ_{i,t} (Ĝ^i_t − V_w(S^i_t)) ∇_w V_w(S^i_t)
L10     θ ← θ + η g_θ; w ← w + η c g_w
```

Lines L3 and L4 collect a batch of $N n$ transitions with the current parameters. Lines L5 and L6 compute, for each copy, the returns of all steps in one backward pass. The step $t = n - 1$ gets a one-step return, the step $t = 0$ an $n$-step return; the factor $1 - D^i_{t+1}$ stops the sum at the end of an episode, so that a return never crosses into the next episode. Line L7 forms the advantage estimates; they are constants in the gradients of lines L8 and L9. Line L8 is the gradient of the surrogate $\frac{1}{Nn}\sum [\hat A \log \pi_\theta + \beta H]$, and line L9 is the semi-gradient of $-\frac{1}{2Nn}\sum(\hat G - V_w)^2$. Line L10 is one step of gradient ascent; deep RL code uses RMSProp or Adam and clips the norm of the gradient. The Baselines code uses $n = 5$, $\beta = 0.01$ and $c = 0.5$ by default.

## Example

**Returns of one segment.** Let $\gamma = \tfrac12$, $n = 3$, rewards $R_1, R_2, R_3 = 1, 2, 3$, an episode end after the second reward, and $V_w(S_3) = 10$. The backward pass gives $\hat G_2 = 3 + \tfrac12 \cdot 10 = 8$, then $\hat G_1 = 2$ (the end stops the sum) and $\hat G_0 = 1 + \tfrac12 \cdot 2 = 2$. The bootstrap value 10 belongs to the new episode, so only $\hat G_2$ uses it.

**Exact critic.** Take the two-state MDP of the [policy gradient theorem](/policy-gradient-theorem/) page, $\gamma = \tfrac12$ and the uniform policy, whose values are $V^\pi = (\tfrac{28}{27}, \tfrac{44}{27})$ and $Q^\pi(0, \cdot) = (\tfrac{79}{54}, \tfrac{11}{18})$. If $V_w = V^\pi$, the mean of $\hat G_t$ given $(S_t, A_t)$ is exactly $Q^\pi(S_t, A_t)$ for every segment length, so $\hat A_t$ is an unbiased advantage estimate. With the critic $V_w = 0$, the mean $n$-step return from state 0 is biased low, by $\gamma^n$ times the mean value of the state reached after $n$ steps:

| $n$ | 1 | 2 | 3 | 4 | exact $Q^\pi$ |
|---|---|---|---|---|---|
| mean $\hat G$ for action 0 | 1 | 1.3125 | 1.4297 | 1.4541 | 1.4630 |
| mean $\hat G$ for action 1 | 0 | 0.5625 | 0.5859 | 0.6064 | 0.6111 |

Longer segments reduce the bias of a poor critic, at the cost of more variance.

**Learning.** With $N = 4$ copies, $n = 5$, $\eta = 0.5$, $\beta = 0.01$, $c = 0.5$ and a tabular actor and critic starting at 0, the implementation below reaches $\pi(0 \mid 0) > 0.98$ and $\pi(1 \mid 1) > 0.97$ after 100 updates (seed 0). That is the optimal policy, and the critic value of state 1 is then close to $V^*(1) = 3$.

## Correctness

A2C has no convergence guarantee with nonlinear networks. Three facts hold, and the correctness proof below proves them.

1. **The n-step target.** If $V_w = V^\pi$, then $\mathbb{E}[\hat G_t \mid S_t, A_t] = Q^\pi(S_t, A_t)$ for every $n$ and every position $t$ in the segment, so $\mathbb{E}[\hat A_t \mid S_t, A_t] = A^\pi(S_t, A_t)$. In general, the bias is $\gamma^m$ times the mean critic error at the state where the bootstrap happens, with $m$ the number of steps to the end of the segment; it falls geometrically in $m$.
2. **The direction.** With an exact critic and $\beta = 0$, the mean of $g_\theta$ is $\sum_s \rho(s) \sum_a \nabla_\theta \pi_\theta(a \mid s) A^\pi(s, a)$, where $\rho$ is the distribution of the states in the batch. This is the [policy gradient theorem](/policy-gradient-theorem/) with $\rho$ in place of the discounted visitation $d$. A2C, like most deep RL code, drops the factor $\gamma^t$, so for $\gamma < 1$ it is not exactly the gradient of the discounted return from the start; it is a gradient-like direction that favours states the copies actually visit.
3. **One synchronous step.** Lines L8 to L10 are one exact gradient step on the batch surrogate; all samples use the same $\theta$. This is what separates A2C from [A3C](/a3c/), whose workers compute gradients with parameters that may be stale.

## Complexity

One round takes $N n$ environment steps and $N n$ forward and backward passes, $O(N n W)$ work, where $W$ is the cost of one pass of the actor and the critic; $K$ rounds cost $O(K N n W)$ in the worst case. The batch takes $O(N n)$ memory and the parameters $O(d)$. All forward passes of one time step can be one batched call, which is the practical reason for A2C: on a GPU it runs faster than [A3C](/a3c/) with many CPU threads. The environments step in lockstep, so the slowest copy sets the pace.

## Properties

- **On-policy.** The batch comes from the current policy and is used once.
- **Synchronous and deterministic.** For a fixed seed the run is reproducible, unlike A3C.
- **Biased, lower variance than REINFORCE.** The bias comes from the critic and falls with $n$; [generalized advantage estimation](/generalized-advantage-estimation/) gives a smoother trade-off.
- **Randomized.** Action selection and the environments use random numbers.

## Variants and improvements

- **GAE.** Replace $\hat A_t$ by the $\lambda$-weighted sum of TD errors ([generalized advantage estimation](/generalized-advantage-estimation/)).
- **ACKTR.** Precondition the update by a Kronecker-factored approximation of the Fisher matrix and limit the step size by a trust region (Wu et al., 2017), a scalable [natural policy gradient](/natural-policy-gradient/).
- **PPO.** Reuse each batch for several epochs of minibatch updates on a clipped objective ([PPO](/ppo/)); with one epoch and one minibatch the clipping is inactive, and its step is an A2C step with GAE advantages.
- **Off-policy corrections.** IMPALA lets actors and the learner run apart and corrects the lag with [V-trace](/v-trace/).
- **Recurrent policies.** For partially observed tasks, carry the hidden state of a recurrent network across segments.

## When to use it

Use A2C as a simple, reproducible on-policy baseline when a fast simulator can run many copies at once, especially with a GPU. When sample efficiency matters more, [PPO](/ppo/), which reuses each batch, usually does better at the same cost per step; with expensive samples and continuous actions, off-policy methods such as [soft actor-critic](/soft-actor-critic/) need fewer samples. For many CPU workers without a GPU, the asynchronous [A3C](/a3c/) avoids waiting for the slowest copy.

## Pitfalls

- **Returns that cross episodes.** Forgetting the factor $1 - D$ in line L6 adds rewards of the next episode to the return of the current one.
- **Time limits.** A time-limit cut is not a true end; bootstrap there with $V_w$ of the last real state, else the critic learns that rewards stop.
- **Gradients through the targets.** $\hat G$ and $\hat A$ must be constants in lines L8 and L9.
- **Entropy weight.** Too small and the policy becomes deterministic early and stops exploring; too large and it stays random.
- **Loss scales.** With a shared network, the weight $c$ of the critic loss must be tuned so that the critic does not dominate the shared layers.
- **Correlated copies.** If all copies start in the same state with the same seed, the batch is not diverse; seed each copy differently.

## Implementations

## History

Mnih et al. (2016) introduced asynchronous advantage actor-critic ([A3C](/a3c/)), whose workers each computed n-step advantage actor-critic gradients and applied them to shared parameters without locks. In 2017, several groups noticed that a synchronous version, which waits for all workers and averages their gradients, works as well and makes better use of GPUs: Clemente, Castejon and Chandra called it PAAC, and OpenAI released it as A2C in its Baselines library, together with ACKTR (Wu et al., 2017), which used A2C as its first-order baseline. A2C then became the base from which [PPO](/ppo/) implementations are built.

## References
