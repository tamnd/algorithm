---
tag: K21R8T
kind: algorithm
slug: ppo
name: Proximal policy optimization
aliases:
- PPO
- clipped surrogate objective
- PPO-Clip
area: machine-learning/reinforcement-learning
level: core
summary: "On-policy actor-critic that runs several epochs of minibatch ascent on a clipped importance-ratio objective, so the policy has no incentive to move far from the one that collected the data."
solves: [rl-control]
model: real-ram
complexity:
  vars: {K: the number of iterations, N: the number of actors, T: the segment length, E: the number of epochs, A: the number of actions, k: the number of policy parameters}
  time: {worst: "O(K N T E A k)"}
  space: {extra: "O(N T + k)"}
properties: {deterministic: false, online: false, exact: false, recursive: false}
history:
  year: 2017
  people: [John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, Oleg Klimov]
  note: "Schulman et al. replaced the KL constraint of TRPO by a clipped probability ratio, so that a batch can be reused for several epochs of first-order minibatch updates."
prereqs: [trpo, generalized-advantage-estimation, actor-critic]
see_also: [natural-policy-gradient, a2c, policy-gradient-theorem, advantage-function, importance-sampling-off-policy, stochastic-gradient-descent, adam, soft-actor-critic]
sources:
  - paper: "John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford and Oleg Klimov, Proximal policy optimization algorithms, arXiv:1707.06347, 2017"
    locator: Section 3 Equations (6) and (7) (the surrogate L^CPI and the clipped objective L^CLIP) and Figures 1 and 2, Section 4 Equation (8) (the adaptive KL penalty), Section 5 Equations (9) to (12) and Algorithm 1 (the combined objective, truncated GAE and the actor loop), Section 6.1 (comparison of surrogate objectives), Appendix A (hyperparameters)
  - paper: "John Schulman, Sergey Levine, Philipp Moritz, Michael I. Jordan and Pieter Abbeel, Trust region policy optimization, Proceedings of the 32nd International Conference on Machine Learning, PMLR 37, 2015, pages 1889 to 1897, arXiv:1502.05477"
    locator: Equation (3) and Section 5 (the importance-weighted surrogate that PPO clips)
  - paper: "John Schulman, Philipp Moritz, Sergey Levine, Michael I. Jordan and Pieter Abbeel, High-dimensional continuous control using generalized advantage estimation, International Conference on Learning Representations, 2016, arXiv:1506.02438"
    locator: Sections 3 and 4 (the advantage estimator used by PPO)
  - paper: "Logan Engstrom, Andrew Ilyas, Shibani Santurkar, Dimitris Tsipras, Firdaus Janoos, Larry Rudolph and Aleksander Madry, Implementation matters in deep policy gradients, a case study on PPO and TRPO, International Conference on Learning Representations, 2020, arXiv:2005.12729"
    locator: the study of code-level details and of how well clipping bounds the policy change
---

Proximal policy optimization (PPO) of Schulman, Wolski, Dhariwal, Radford and Klimov (2017) is an on-policy [actor-critic](/actor-critic/) method that keeps the stability of [TRPO](/trpo/) with only first-order updates. After collecting a batch with the policy $\pi_{\theta_{\text{old}}}$, it maximizes the *clipped surrogate objective*

$$L^{\text{CLIP}}(\theta) = \hat{\mathbb{E}}_t\left[\min\left(r_t(\theta) \hat A_t,\ \mathrm{clip}(r_t(\theta), 1 - \epsilon, 1 + \epsilon)\, \hat A_t\right)\right], \qquad r_t(\theta) = \frac{\pi_\theta(A_t \mid S_t)}{\pi_{\theta_{\text{old}}}(A_t \mid S_t)},$$

by several epochs of minibatch stochastic gradient ascent, usually with [Adam](/adam/). Here $\hat A_t$ is an advantage estimate, usually from [generalized advantage estimation](/generalized-advantage-estimation/). The minimum makes the objective a pessimistic bound on the importance-weighted surrogate of TRPO: once the probability of an action has moved by more than the factor $1 \pm \epsilon$ in the direction that its advantage favours, that sample stops contributing gradient. The same batch can then be reused several times without the policy running away. PPO is simple, works with shared policy and value networks, and is one of the most widely used deep reinforcement learning algorithms, including for fine-tuning language models from human feedback.

## In plain words

The agent plays for a while with its current behaviour and records what happened. Then it studies that record several times over to improve. The danger is that the record describes the old behaviour, so changing too much makes the lessons wrong. PPO adds a simple rule: for each recorded decision, if the agent has already made a good choice more likely by a fixed fraction, or a bad choice less likely by that fraction, it stops pushing on that decision. Changes in the wrong direction are never ignored, so mistakes are still corrected. The result is a series of safe, moderate improvements that need only ordinary gradient steps.

## The problem

The setting is [reinforcement learning control](/rl-control/) with a differentiable stochastic policy and a learned value function. The surrogate $L^{\text{CPI}}(\theta) = \hat{\mathbb{E}}_t[r_t(\theta) \hat A_t]$ of [TRPO](/trpo/) has the policy gradient as its gradient at $\theta_{\text{old}}$ ([policy gradient theorem](/policy-gradient-theorem/)), but it is only accurate near $\theta_{\text{old}}$. Maximizing it without a constraint gives excessively large policy updates; TRPO adds a KL constraint, which needs second-order machinery. The task is to keep the benefit of the constraint with plain gradient steps, and to use each batch for many updates.

## The algorithm

$N$ actors each run the policy for $T$ steps; a segment can cross episode boundaries. Advantages use truncated GAE over each segment, bootstrapped from the value of the state after the last step. The value function $V$ is fitted to the targets $\hat R_t = \hat A_t + V(S_t)$.

```pseudo id=main
PPO(π_θ, V, γ, λ, ε, E, M)
L1  for k ← 1 to K do
L2      each of N actors runs π_θ for T steps
L3      Â_t ← GAE(γ, λ) with V for each segment, and R̂_t ← Â_t + V(S_t)
L4      θ_old ← θ
L5      for E epochs, for each minibatch of M of the N T samples do
L6          g ← ∇_θ mean over the minibatch of min(r_t(θ) Â_t, clip(r_t(θ), 1 − ε, 1 + ε) Â_t)
L7          θ ← θ + η g
L8          V ← V − η_V ∇ mean over the minibatch of (V(S_t) − R̂_t)²
```

For one sample, the derivative of the clipped term with respect to the ratio $r$ is

$$\frac{\partial}{\partial r} \min(r \hat A, \mathrm{clip}(r, 1-\epsilon, 1+\epsilon) \hat A) = \begin{cases} \hat A & \text{if } \hat A > 0 \text{ and } r < 1 + \epsilon, \text{ or } \hat A < 0 \text{ and } r > 1 - \epsilon, \\ 0 & \text{otherwise,} \end{cases}$$

and $\nabla_\theta r = r \nabla_\theta \log \pi_\theta(A_t \mid S_t)$. With a shared network, lines L6 to L8 become one step on $L^{\text{CLIP}} - c_1 L^{\text{VF}} + c_2 H$, where $H$ is an entropy bonus (Equation 9 of the paper). The paper's continuous control settings were $\epsilon = 0.2$, $T = 2048$, 10 epochs, minibatches of 64, $\gamma = 0.99$ and $\lambda = 0.95$ with Adam.

## Example

The clip range for $\epsilon = \tfrac15$ is $[\tfrac45, \tfrac65]$. Exact values of one clipped term and of its slope in $r$:

| $r$ | $\hat A$ | $\min(r\hat A, \mathrm{clip}(r)\hat A)$ | slope | meaning |
|---|---|---|---|---|
| $1$ | $2$ | $2$ | $2$ | at the old policy, the plain surrogate |
| $\tfrac32$ | $2$ | $\tfrac{12}{5}$ | $0$ | good action already more likely: no push |
| $\tfrac12$ | $2$ | $1$ | $2$ | good action became less likely: full push back |
| $\tfrac12$ | $-2$ | $-\tfrac85$ | $0$ | bad action already less likely: no push |
| $\tfrac32$ | $-2$ | $-3$ | $-2$ | bad action became more likely: full push back |

Now take one state with two actions, the uniform old policy and one sample with $\hat A = 1$, and repeat gradient steps of size $0.2$ on the same sample. The ratio of the sampled action evolves as follows:

| step | 1 | 2 | 3 | 4 | 5 | 10 | 50 |
|---|---|---|---|---|---|---|---|
| $r$ with $L^{\text{CLIP}}$ | 1.0997 | 1.1964 | 1.2869 | 1.2869 | 1.2869 | 1.2869 | 1.2869 |
| $r$ with $L^{\text{CPI}}$ | 1.0997 | 1.1964 | 1.2869 | 1.3687 | 1.4409 | 1.6751 | 1.9426 |

With clipping, the step that crosses $1.2$ is the last one; the overshoot to $1.2869$ comes from the step size. Without clipping, the reused sample drives the action probability toward 1.

## Correctness

PPO is a heuristic; there is no convergence theorem for the algorithm as used. The correctness proof shows the properties of the objective that motivate it.

1. **First-order match.** $L^{\text{CLIP}}(\theta_{\text{old}}) = L^{\text{CPI}}(\theta_{\text{old}}) = \hat{\mathbb{E}}_t[\hat A_t]$, and their gradients at $\theta_{\text{old}}$ are equal to the policy gradient estimate $\hat{\mathbb{E}}_t[\hat A_t \nabla \log \pi_\theta(A_t \mid S_t)]$, because $r = 1$ lies inside the clip range. So the first minibatch step of each iteration is an ordinary [actor-critic](/actor-critic/) step.
2. **Pessimistic bound.** Each clipped term is at most $r_t \hat A_t$, with equality when $r_t \in [1 - \epsilon, 1 + \epsilon]$ or when moving $r_t$ toward 1 would help the term. So $L^{\text{CLIP}} \le L^{\text{CPI}}$ everywhere.
3. **No incentive past the clip range.** A sample whose ratio has passed $1 + \epsilon$ with $\hat A > 0$, or $1 - \epsilon$ with $\hat A < 0$, has zero gradient. In the other direction the gradient is never clipped.

The clip does not bound the KL divergence: other samples that share parameters, and the step size, can still move a clipped ratio further (Engstrom et al., 2020). Many implementations monitor the mean KL divergence and stop the epochs early when it exceeds a limit.

## Complexity

One iteration takes $N T$ environment steps. Each epoch evaluates the policy, its ratio and its gradient once per sample: $O(A k)$ for a linear softmax with $A$ actions and $k$ parameters, or one forward and backward pass for a network. So $K$ iterations cost $O(K N T E A k)$ arithmetic beyond the environment, and memory is $O(N T + k)$ for the batch and the parameters. Compared with [TRPO](/trpo/), there are no conjugate gradient iterations or line search, and $E$ epochs reuse the batch.

## Properties

- **On-policy**, with limited reuse: each batch is used for $E$ epochs and then discarded.
- **First-order.** Only gradients of the objective; works with any optimizer and with shared networks.
- **Pessimistic surrogate.** The objective never rewards moving a ratio past the clip range in the helpful direction.
- **Randomized.** Sampling of episodes and of minibatches.

## Variants and improvements

- **Adaptive KL penalty.** Maximize $\hat{\mathbb{E}}_t[r_t \hat A_t] - \beta\, \hat{\mathbb{E}}_t[D_{\mathrm{KL}}(\pi_{\text{old}}(\cdot \mid S_t) \,\|\, \pi_\theta(\cdot \mid S_t))]$; after each iteration halve $\beta$ if the measured KL is below $d_{\text{targ}}/1.5$ and double it if it is above $1.5 d_{\text{targ}}$ (Section 4). It performed worse than clipping in the paper's comparison.
- **Value clipping and advantage normalization.** Common code-level additions; Engstrom et al. (2020) found that such details matter as much as the clipping.
- **PPO with a learned reward model.** Used to fine-tune language models from human preferences, with a KL penalty to a reference model.
- **Off-policy and trust region relatives.** [TRPO](/trpo/) solves the constrained problem directly; [natural policy gradient](/natural-policy-gradient/) is its unconstrained ancestor.

## When to use it

Use PPO as a default on-policy method when simulation is cheap, for discrete or continuous actions, with parallel actors. It is the usual baseline for games, robotics in simulation and language model fine-tuning. Prefer off-policy methods such as [soft actor-critic](/soft-actor-critic/) when environment samples are expensive, and [TRPO](/trpo/) when a hard limit on the KL divergence per update is required.

## Pitfalls

- **Clipping is not a trust region.** Large learning rates or many epochs can still move the policy far; watch the mean KL and the fraction of clipped samples.
- **Ratio from the wrong policy.** $\pi_{\theta_{\text{old}}}$ must be the policy that collected the data, frozen for the whole iteration.
- **Advantage scale.** Clipping acts on ratios, so a few large advantages still dominate the gradient; normalize advantages per minibatch or per batch.
- **Truncated segments.** Bootstrap from $V$ of the next state at the end of a segment, but not across the end of an episode.
- **Shared network.** With a joint loss, the value loss coefficient $c_1$ and the entropy coefficient $c_2$ need tuning; a bad $c_1$ lets the value loss swamp the policy gradient.

## Implementations

## History

PPO was proposed by Schulman, Wolski, Dhariwal, Radford and Klimov at OpenAI in 2017, two years after [TRPO](/trpo/). The paper compared the clipped objective with an adaptive KL penalty and with no constraint, and showed that the clipped version matched or beat TRPO and A2C on continuous control and Atari with a simpler implementation. It became the main algorithm of OpenAI Five for Dota 2 and of reinforcement learning from human feedback for language models, and later work studied which of its implementation details matter.

## References
