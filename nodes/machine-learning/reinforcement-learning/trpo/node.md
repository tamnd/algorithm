---
tag: TNPH8G
kind: algorithm
slug: trpo
name: Trust region policy optimization
aliases:
- TRPO
- trust region policy optimisation
area: machine-learning/reinforcement-learning
level: advanced
summary: "Policy update that maximizes an importance-weighted surrogate subject to a bound on the mean KL divergence, solved by a natural gradient step with conjugate gradients and a line search."
solves: [rl-control]
model: real-ram
complexity:
  vars: {K: the number of iterations, N: the number of episodes per iteration, T: the maximum episode length, A: the number of actions, k: the number of policy parameters, c: the number of conjugate gradient iterations, l: the number of line search steps}
  time: {worst: "O(K N T A k (c + l))"}
  space: {extra: "O(N T + k)"}
properties: {deterministic: false, online: false, exact: false, recursive: false}
history:
  year: 2015
  people: [John Schulman, Sergey Levine, Philipp Moritz, Michael I. Jordan, Pieter Abbeel]
  note: "Schulman et al. proved a lower bound on the return of a new policy in terms of a surrogate objective and the maximum KL divergence, and turned it into a constrained natural gradient step that trained neural network policies for locomotion and Atari games."
prereqs: [natural-policy-gradient, conjugate-gradient-method, advantage-function]
see_also: [ppo, generalized-advantage-estimation, backtracking-line-search, policy-improvement-theorem, total-variation-distance, fisher-information-matrix, policy-iteration, mirror-descent]
sources:
  - paper: "John Schulman, Sergey Levine, Philipp Moritz, Michael I. Jordan and Pieter Abbeel, Trust region policy optimization, Proceedings of the 32nd International Conference on Machine Learning, PMLR 37, 2015, pages 1889 to 1897, arXiv:1502.05477"
    locator: Equation (1) (the identity of Kakade and Langford), Equations (3) and (4) (the local approximation L and its first-order match), Section 3 Theorem 1 and Equations (8) and (9) (the lower bound), Algorithm 1, Equations (11) and (12) (the maximum and mean KL constraints), Section 5 (single path and vine sampling), Section 6 and Appendix C (conjugate gradients and the line search), Appendix A (proofs)
  - paper: "Sham Kakade and John Langford, Approximately optimal approximate reinforcement learning, Proceedings of the 19th International Conference on Machine Learning, 2002, pages 267 to 274"
    locator: the identity for the difference of two returns and conservative policy iteration with its improvement bound
  - paper: "Sham Kakade, A natural policy gradient, Advances in Neural Information Processing Systems 14, 2001, pages 1531 to 1538"
    locator: Equations (2) to (4), the Fisher matrix averaged over states and the natural gradient
  - paper: "John Schulman, Philipp Moritz, Sergey Levine, Michael I. Jordan and Pieter Abbeel, High-dimensional continuous control using generalized advantage estimation, International Conference on Learning Representations, 2016, arXiv:1506.02438"
    locator: Section 6 (TRPO with generalized advantage estimation and a value function fitted in a trust region)
  - book: isbn:9780387303031
    title: "Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006"
    locator: Chapter 4 (trust region methods) and Chapter 5 (the conjugate gradient method)
---

Trust region policy optimization (TRPO) of Schulman, Levine, Moritz, Jordan and Abbeel (2015) improves a stochastic policy by maximizing a local model of its return, the *surrogate objective*, while keeping the new policy close to the old one in KL divergence. The surrogate is the importance-weighted [advantage](/advantage-function/) of the old policy:

$$L_{\theta_{\text{old}}}(\theta) = \mathbb{E}_{s \sim \rho_{\text{old}},\, a \sim \pi_{\text{old}}}\left[\frac{\pi_\theta(a \mid s)}{\pi_{\theta_{\text{old}}}(a \mid s)} A^{\pi_{\text{old}}}(s, a)\right], \qquad \text{subject to } \bar D_{\mathrm{KL}}(\theta_{\text{old}}, \theta) \le \delta.$$

Its gradient at $\theta_{\text{old}}$ is the policy gradient, and the paper proves that the true return is at least the surrogate minus a penalty proportional to the largest KL divergence, so small steps that improve the surrogate improve the policy. TRPO solves the constrained problem approximately: a [natural policy gradient](/natural-policy-gradient/) direction computed with [conjugate gradients](/conjugate-gradient-method/), scaled to the edge of the trust region, then shortened by a [backtracking line search](/backtracking-line-search/) until the constraint and an improvement hold. It was the first method to train large neural network policies reliably with policy gradients, and [PPO](/ppo/) replaced it with a simpler first-order objective.

## In plain words

Policy gradient methods learn by trial: play with the current behaviour, then change it toward what worked. If the change is too large, the data no longer describes the new behaviour, and the agent can get much worse in one step and never recover. TRPO first builds a forecast of how good a changed behaviour would be, using only the old data. The forecast is reliable only near the old behaviour. So TRPO looks for the best change inside a small region, measured by how differently the new behaviour chooses actions. It takes the largest change that stays inside the region, checks it, and halves it until the check passes.

## The problem

The setting is [reinforcement learning control](/rl-control/) with a differentiable stochastic policy $\pi_\theta$ in a [Markov decision process](/markov-decision-process/) with discount $\gamma < 1$. Write $\eta(\pi)$ for the expected discounted return from the start distribution and $\rho_\pi(s) = \sum_t \gamma^t \Pr(S_t = s)$ for the discounted visitation, not normalized. The identity of Kakade and Langford (Equation 1 of the paper) is

$$\eta(\tilde\pi) = \eta(\pi) + \sum_s \rho_{\tilde\pi}(s) \sum_a \tilde\pi(a \mid s) A^\pi(s, a).$$

It is exact but uses the visitation of the new policy, which is unknown. The *local approximation* replaces it by the visitation of the old policy:

$$L_\pi(\tilde\pi) = \eta(\pi) + \sum_s \rho_\pi(s) \sum_a \tilde\pi(a \mid s) A^\pi(s, a).$$

$L_\pi$ and $\eta$ have the same value and the same gradient at $\pi$. The task is to find a step that makes $\eta$ larger, using only samples from $\pi$.

## The algorithm

The single-path version samples whole episodes with the current policy. Each step $t$ of an episode gives a sample $(w_t, S_t, A_t, \hat A_t)$ with weight $w_t = \gamma^t / N$, so that sums over samples estimate sums over $\rho_\pi$. The mean KL divergence $\bar D_{\mathrm{KL}}$ and the Fisher matrix $\hat F$ (its Hessian at $\theta_{\text{old}}$) are averages over the sampled states with these weights; the KL divergence between two action distributions is computed exactly. $\hat F$ is never formed: conjugate gradients needs only products $\hat F v$.

```pseudo id=main
TRPO(π_θ, γ, δ, N, c, l)
L1  for k ← 1 to K do
L2      run π_θ for N episodes
L3      Â_t ← G_t − b(S_t) for every step t of every episode
L4      g ← Σ_t w_t Â_t ∇_θ log π_θ(A_t | S_t)
L5      x ← c steps of conjugate gradients on F̂ x = g
L6      β ← √(2δ / xᵀF̂x)
L7      for j ← 0 to l − 1 do θ′ ← θ + β 2^(−j) x
L8          if D̄_KL(θ, θ′) ≤ δ and L(θ′) > L(θ) then
L9              θ ← θ′ and stop the line search
```

Line L4 is the gradient of the sampled surrogate $\sum_t w_t \frac{\pi_\theta(A_t \mid S_t)}{\pi_{\text{old}}(A_t \mid S_t)} \hat A_t$ at $\theta_{\text{old}}$. Line L5 approximates the natural gradient $\hat F^{-1} g$; a small damping term $\epsilon v$ is added to $\hat F v$, because $\hat F$ is often singular. Line L6 scales the step so that the quadratic model of the KL divergence, $\tfrac12 \beta^2 x^\top \hat F x$, equals $\delta$. Lines L7 to L9 check the real KL divergence and the real surrogate, because the quadratic model can be wrong. If no step passes, the policy does not change. Here $b$ is a baseline, the mean return per state of the previous batch; the paper's experiments and most implementations use [generalized advantage estimation](/generalized-advantage-estimation/) with a value network instead. The vine version (Section 5 of the paper) branches several rollouts from each sampled state to estimate $Q$ with less variance, but needs a simulator that can reset to a state.

## Example

Take the two-state MDP of the [policy gradient theorem](/policy-gradient-theorem/) page: $\gamma = \tfrac12$, start state 0, $\eta(\pi_{\text{old}}) = \tfrac{28}{27} \approx 1.037$ for the uniform policy. Its advantages are $A(0, \cdot) = (\tfrac{23}{54}, -\tfrac{23}{54})$ and $A(1, \cdot) = (-\tfrac{37}{27}, \tfrac{37}{27})$, so $\epsilon = \max |A| = \tfrac{37}{27}$, and the constant of Theorem 1 is $C = 4\epsilon\gamma / (1-\gamma)^2 = \tfrac{296}{27} \approx 10.96$. Move each state toward its better action by $\alpha$ in total variation:

| new policy $\pi(0 \mid 0), \pi(1 \mid 1)$ | $\alpha$ | $L(\tilde\pi)$ | $\eta(\tilde\pi)$ | $L - C\alpha^2$ |
|---|---|---|---|---|
| $\tfrac58, \tfrac58$ | $\tfrac18$ | $\tfrac{922}{729} \approx 1.2647$ | $\tfrac{1060}{843} \approx 1.2574$ | $1.0934$ |
| $\tfrac34, \tfrac34$ | $\tfrac14$ | $\tfrac{1088}{729} \approx 1.4925$ | $\tfrac{60}{41} \approx 1.4634$ | $0.8073$ |
| $1, 1$ | $\tfrac12$ | $\tfrac{1420}{729} \approx 1.9479$ | $\tfrac{11}{6} \approx 1.8333$ | $-0.7929$ |

The surrogate forecasts the true return well near the old policy and overestimates it more as the step grows. The lower bound holds in every row, but it is far too loose to choose the step: only the smallest step has a bound above $\eta(\pi_{\text{old}})$. This is why TRPO replaces the penalty by a constraint with a tuned $\delta$.

## Correctness

The correctness proof shows three facts, following Section 3 and Appendix A of the paper.

1. **First-order match.** $L_\pi(\pi) = \eta(\pi)$ and $\nabla_\theta L_{\pi_{\text{old}}}(\pi_\theta) = \nabla_\theta \eta(\pi_\theta)$ at $\theta = \theta_{\text{old}}$. So line L4 estimates the policy gradient, and the expected sampled surrogate gradient equals it exactly.
2. **Lower bound (Theorem 1).** With $\alpha = \max_s D_{\mathrm{TV}}(\pi(\cdot \mid s), \tilde\pi(\cdot \mid s))$ and $\epsilon = \max_{s,a} |A^\pi(s, a)|$, $\eta(\tilde\pi) \ge L_\pi(\tilde\pi) - \frac{4 \epsilon \gamma}{(1-\gamma)^2} \alpha^2$. Since $D_{\mathrm{TV}}^2 \le D_{\mathrm{KL}}$, the same holds with $\alpha^2$ replaced by the maximum KL divergence.
3. **Monotone improvement (Algorithm 1).** If each iteration maximizes $M_i(\pi) = L_{\pi_i}(\pi) - C D^{\max}_{\mathrm{KL}}(\pi_i, \pi)$, then $\eta(\pi_{i+1}) - \eta(\pi_i) \ge M_i(\pi_{i+1}) - M_i(\pi_i) \ge 0$, a minorize-maximize scheme.

The practical algorithm departs from the theory in three ways: a constraint instead of the penalty, the mean KL instead of the maximum, and sampled estimates. So the guarantee of fact 3 does not hold for it; the line search only enforces the constraint and an improvement of the sampled surrogate.

## Complexity

Per iteration, sampling costs $O(N T)$ environment steps and policy evaluations. With a linear softmax policy over $A$ actions and $k$ parameters, the gradient costs $O(N T A k)$, each Fisher-vector product $O(N T A k)$, and each line search step $O(N T A k)$ to recompute the policy at the sampled states, so one iteration costs $O(N T A k (c + l))$ with $c$ conjugate gradient iterations (typically 10) and $l$ line search steps. Memory is $O(N T + k)$: the batch and a few vectors; the $k \times k$ matrix is never stored. For a neural network, each Fisher-vector product costs about two passes of automatic differentiation over the batch.

## Properties

- **On-policy.** Each batch is used for one update and then discarded.
- **Second-order direction, first-order cost.** Conjugate gradients with Fisher-vector products give the natural direction in $O(c)$ gradient-sized passes.
- **Step size by divergence.** $\delta$ bounds the change of the action distributions, not of the parameters, so the same $\delta$ works for different networks; typical values are $0.01$ to $0.05$.
- **Randomized.** Episodes are sampled.

## Variants and improvements

- **Vine sampling.** Several rollouts from each sampled state, with common random numbers, for low-variance $Q$ estimates (Section 5).
- **TRPO with GAE.** Advantages from [generalized advantage estimation](/generalized-advantage-estimation/) and a value network fitted with its own trust region (Schulman et al., 2016).
- **PPO.** A clipped surrogate optimized with several epochs of minibatch gradient ascent, without second-order steps ([PPO](/ppo/)).
- **ACKTR.** A Kronecker-factored approximation of $F$ ([K-FAC](/kronecker-factored-approximate-curvature/)) instead of conjugate gradients.
- **Constrained and mirror descent views.** Constrained policy optimization adds cost constraints; mirror descent policy optimization treats the KL step as [mirror descent](/mirror-descent/).

## When to use it

Use TRPO for on-policy learning when stability matters more than simplicity, for example with continuous control and small batches, or when a hard limit on the policy change per update is needed. For most problems [PPO](/ppo/) is easier to implement, works with shared policy and value networks and minibatches, and gives similar results. When samples are expensive, off-policy methods such as [soft actor-critic](/soft-actor-critic/) are usually more efficient.

## Pitfalls

- **Line search failures.** If the step fails all checks, the policy stays the same; frequent failures mean $\delta$ is too large or the advantages are too noisy.
- **Fisher matrix from the wrong distribution.** The Fisher-vector products must use the old policy at the sampled states, not the actions alone, and the same weights as the KL divergence.
- **Singular Fisher matrix.** Add damping to $\hat F v$.
- **Advantage scale.** The step length depends on $\delta$, not on the scale of the advantages, but the line search compares surrogate values, so outlier advantages can still mislead it; many implementations normalize advantages per batch.
- **No monotone guarantee in practice.** The theorem needs the maximum KL and the penalty constant; with the mean KL and sampled estimates, the return can still drop.

## Implementations

## History

Kakade (2001) introduced the [natural policy gradient](/natural-policy-gradient/), and Kakade and Langford (2002) proved the identity for the difference of returns and a bound for conservative policy iteration, which mixes the old policy with a greedy one. Schulman, Levine, Moritz, Jordan and Abbeel (ICML 2015) extended the bound to general stochastic policies with the total variation and KL divergences, and turned it into a practical algorithm with conjugate gradients, a KL constraint and a line search, which learned swimming, hopping and walking gaits and played Atari games from images. The GAE paper (Schulman et al., 2016) combined TRPO with learned value functions for 3D locomotion, and PPO (Schulman et al., 2017) replaced the constrained step by a clipped objective.

## References
