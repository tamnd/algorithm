---
tag: 25P3CM
kind: algorithm
slug: generalized-advantage-estimation
name: Generalized advantage estimation
aliases:
- GAE
- "GAE(gamma, lambda)"
area: machine-learning/reinforcement-learning
level: advanced
summary: "Advantage estimate A_t = sum_l (gamma lambda)^l delta_(t+l) from TD errors of a critic; lambda = 0 gives the TD error, lambda = 1 the return minus V."
solves: [policy-evaluation]
model: real-ram
complexity:
  vars: {T: the number of steps in the segment}
  time: {worst: "O(T)"}
  space: {extra: "O(T)"}
properties: {deterministic: true, online: false, exact: false, recursive: false}
history:
  year: 2015
  people: [John Schulman, Philipp Moritz, Sergey Levine, Michael I. Jordan, Pieter Abbeel]
  note: "Schulman et al. defined GAE(gamma, lambda) in a 2015 preprint, published at ICLR 2016, and used it with TRPO to learn 3D locomotion from raw joint angles."
prereqs: [advantage-function, td-error, td-lambda]
see_also: [ppo, trpo, a2c, actor-critic, reinforce, eligibility-traces, n-step-td, potential-based-reward-shaping]
sources:
  - paper: "John Schulman, Philipp Moritz, Sergey Levine, Michael I. Jordan and Pieter Abbeel, High-dimensional continuous control using generalized advantage estimation, International Conference on Learning Representations, 2016, arXiv:1506.02438"
    locator: Section 2 (gamma-just estimators), Section 3 (the definition of GAE and its special cases lambda = 0 and lambda = 1), Section 4 (the reward shaping view), Section 5 (value function fitting) and Section 6 (experiments)
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: Section 12.1 (the lambda-return) and Section 13.5 (actor-critic methods)
  - paper: "John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford and Oleg Klimov, Proximal policy optimization algorithms, arXiv:1707.06347, 2017"
    locator: Section 5 (the truncated GAE over segments of fixed length) and the hyperparameter tables
---

Generalized advantage estimation (GAE) turns the [TD errors](/td-error/) of a critic $V$ into estimates of the [advantage](/advantage-function/) $A^\pi(S_t, A_t)$ for policy gradient methods. With $\delta_t = R_{t+1} + \gamma V(S_{t+1}) - V(S_t)$, the estimate is

$$\hat A_t^{\mathrm{GAE}(\gamma, \lambda)} = \sum_{l \ge 0} (\gamma\lambda)^l \delta_{t+l},$$

a geometric average of TD errors that stops at the end of the episode or of the data. One parameter $\lambda \in [0, 1]$ trades bias against variance: $\lambda = 0$ gives the one-step TD error, which has low variance but is biased when $V$ is wrong, and $\lambda = 1$ gives the Monte Carlo return minus $V(S_t)$, which is unbiased for the policy gradient but noisy. With an exact critic $V = V^\pi$, every $\lambda$ gives an unbiased advantage. GAE is computed in one backward pass over a segment, and $\hat A_t + V(S_t)$ is the [TD(λ)](/td-lambda/) return, the usual target for the critic. Schulman et al. (2016) introduced it, and it is the default advantage estimator of [PPO](/ppo/) and [TRPO](/trpo/) implementations.

## In plain words

A policy gradient method needs to know, for each action it took, whether that action was better or worse than usual. A critic predicts how good each situation is. One way to judge an action is to look one step ahead: the reward plus the critic's opinion of the next situation, compared with its opinion of the current one. This is steady but trusts the critic fully. Another way is to look at all the rewards until the end: this is fair but very noisy. GAE blends all the look-ahead lengths, giving less and less weight to later steps. A single knob sets how far ahead it looks in effect. A good critic allows a short look; a poor critic needs a long one.

## The problem

Given a segment $S_0, A_0, R_1, S_1, \ldots, S_T$ from a policy $\pi$, a critic $V$, a discount $\gamma$ and the flags that mark the ends of episodes, compute for each $t < T$ an estimate $\hat A_t$ of $A^\pi(S_t, A_t) = Q^\pi(S_t, A_t) - V^\pi(S_t)$ to use in the [policy gradient](/policy-gradient-theorem/) $\mathbb{E}[\hat A_t \nabla \log \pi(A_t \mid S_t)]$. The estimate should keep the gradient (nearly) unbiased and have low variance. The same pass should give targets for fitting $V$.

## The algorithm

The pseudocode treats a segment inside one episode, with $V(S_T) = 0$ if the episode ends at step $T$. If an episode ends at step $t + 1$ inside the segment, the implementation sets $V(S_{t+1}) = 0$ in line L3 and drops $\gamma\lambda \hat A$ in line L4, so that no sum crosses into the next episode.

```pseudo id=main
GAE(R_1..R_T, V(S_0)..V(S_T), γ, λ)
L1  Â ← 0
L2  for t ← T − 1 down to 0 do
L3      δ_t ← R_{t+1} + γ V(S_{t+1}) − V(S_t)
L4      Â ← δ_t + γλ Â
L5      Â_t ← Â; Ĝ_t ← Â_t + V(S_t)                 ▷ Ĝ_t is the λ-return, the target for V
L6  return Â_0..Â_{T−1}, Ĝ_0..Ĝ_{T−1}
```

Line L4 is the recursion $\hat A_t = \delta_t + \gamma\lambda \hat A_{t+1}$, which unrolls to $\hat A_t = \sum_{l=0}^{T-1-t} (\gamma\lambda)^l \delta_{t+l}$. Within one episode, the sum of TD errors telescopes into $n$-step advantages: $\sum_{l=0}^{n-1} \gamma^l \delta_{t+l} = G_t^{(n)} - V(S_t)$, where $G_t^{(n)}$ is the [n-step return](/n-step-td/). So GAE is the $\lambda$-weighted average $(1 - \lambda)\sum_{n \ge 1} \lambda^{n-1} (G_t^{(n)} - V(S_t))$, with the remaining weight on the longest return the segment allows. In an actor-critic loop, a batch of segments is collected with the current policy, GAE gives $\hat A_t$ for the actor and $\hat G_t$ for the critic, and both are updated, for example with [PPO](/ppo/) or [TRPO](/trpo/).

## Example

Let $\gamma = \lambda = \tfrac12$, rewards $R_1, R_2, R_3 = 1, 0, 2$, critic values $V(S_0), V(S_1), V(S_2), V(S_3) = 1, 2, 1, 4$, and no episode end. The TD errors are $\delta_0 = 1 + 1 - 1 = 1$, $\delta_1 = 0 + \tfrac12 - 2 = -\tfrac32$ and $\delta_2 = 2 + 2 - 1 = 3$. The backward pass with $\gamma\lambda = \tfrac14$ gives

| $t$ | $\delta_t$ | $\hat A_t = \delta_t + \tfrac14 \hat A_{t+1}$ | $\hat G_t = \hat A_t + V(S_t)$ |
|---|---|---|---|
| 2 | 3 | 3 | 4 |
| 1 | $-\tfrac32$ | $-\tfrac32 + \tfrac34 = -\tfrac34$ | $\tfrac54$ |
| 0 | 1 | $1 - \tfrac{3}{16} = \tfrac{13}{16}$ | $\tfrac{29}{16}$ |

With $\lambda = 0$ the advantages would be the TD errors $1, -\tfrac32, 3$. With $\lambda = 1$ they would be $G_t^{(T-t)} - V(S_t)$, for example $\hat A_0 = 1 + 0 + \tfrac14 \cdot 2 + \tfrac18 \cdot 4 - 1 = 1$.

**Exactness in expectation.** On random acyclic MDPs, where every episode can be listed, the mean of $\hat A_0$ given $(S_0, A_0) = (s, a)$, with the critic $V = V^\pi$, equals $A^\pi(s, a)$ exactly for $\lambda = 0, \tfrac13, \tfrac{9}{10}, 1$. With a wrong critic $V_w$, the mean for $\lambda = 1$ is $Q^\pi(s, a) - V_w(s)$, whose error does not depend on $a$, while for $\lambda = \tfrac12$ the error is different for the two actions.

## Correctness

The correctness proof below proves four facts. Let the segment lie in one episode that ends at step $T$ or later.

1. **Recursion.** Lines L1 to L5 compute $\hat A_t = \sum_{l=0}^{T-1-t} (\gamma\lambda)^l \delta_{t+l}$, and $\hat G_t = \hat A_t + V(S_t)$ is the truncated $\lambda$-return $(1 - \lambda)\sum_{n=1}^{m-1}\lambda^{n-1} G_t^{(n)} + \lambda^{m-1} G_t^{(m)}$, with $m = T - t$.
2. **Special cases.** $\lambda = 0$ gives $\hat A_t = \delta_t$. $\lambda = 1$ gives $\hat A_t = G_t^{(m)} - V(S_t)$, the return to the end of the segment (bootstrapped from $V(S_T)$) minus the value, which is the Monte Carlo advantage when the episode ends at $T$.
3. **Exact critic.** If $V = V^\pi$, then $\mathbb{E}[\delta_{t+l} \mid S_t, A_t] = 0$ for $l \ge 1$ and $\mathbb{E}[\delta_t \mid S_t, A_t] = A^\pi(S_t, A_t)$, so $\mathbb{E}[\hat A_t \mid S_t, A_t] = A^\pi(S_t, A_t)$ for every $\lambda$.
4. **Approximate critic.** If the episode ends at $T$ and $\lambda = 1$, then $\mathbb{E}[\hat A_t \mid S_t, A_t] = Q^\pi(S_t, A_t) - V(S_t)$. The error $V^\pi(S_t) - V(S_t)$ depends only on the state, so it acts as a baseline and leaves the policy gradient unbiased. For $\lambda < 1$ the errors of $V$ at later states enter, with weights that depend on the action, and the gradient is biased in general.

Schulman et al. call an estimator *$\gamma$-just* if it gives the same expected policy gradient as the true discounted advantage; facts 3 and 4 say that GAE is $\gamma$-just for all $\lambda$ when $V = V^\pi$, and for $\lambda = 1$ with any $V$. The discount $\gamma$ itself is a second source of bias when the real objective is undiscounted; the paper treats both $\gamma$ and $\lambda$ as variance reduction parameters.

## Complexity

One backward pass does a constant number of operations per step: $O(T)$ time for a segment of $T$ steps, and $O(T)$ space for the output (the recursion itself needs only $O(1)$). For a batch of $N$ segments of length $T$ it is $O(N T)$, much less than the cost of the network passes that produce $V$.

## Properties

- **Bias and variance in one knob.** Variance grows and bias from the critic shrinks as $\lambda$ goes from 0 to 1.
- **Unbiased with an exact critic,** for every $\lambda$.
- **Backward and offline.** It needs the whole segment; the forward-view sum has an online equivalent with [eligibility traces](/eligibility-traces/).
- **Deterministic.** Given the data and the critic, the output is fixed.

## Variants and improvements

- **Truncated segments.** PPO and A2C implementations compute GAE over fixed-length segments and bootstrap from $V(S_T)$ at the cut; the weight that the infinite sum gives to later steps goes to the last term.
- **Advantage normalization.** Implementations often subtract the batch mean and divide by the batch standard deviation of $\hat A$ before the policy update. This changes the scale of the step and is a heuristic.
- **Off-policy versions.** [Retrace](/retrace/) and [V-trace](/v-trace/) multiply the terms of the sum by truncated importance weights, so that the same idea works with data from older policies.
- **Reward shaping view.** GAE is the $\gamma\lambda$-discounted sum of the shaped rewards $\delta_t$, where $V$ is the potential of [potential-based reward shaping](/potential-based-reward-shaping/).

## When to use it

Use GAE whenever an on-policy policy gradient method has a learned critic: it is the standard choice in [PPO](/ppo/), [TRPO](/trpo/) and [A2C](/a2c/) implementations, with $\lambda$ around 0.95 and $\gamma$ around 0.99 as common starting points. Without a critic, use the return as in [REINFORCE](/reinforce/). For off-policy data, use estimators with importance weights.

## Pitfalls

- **Crossing episode boundaries.** Forgetting to reset the sum at an episode end mixes the advantages of two episodes.
- **Time limits treated as ends.** A cut by a time limit is not a real end: bootstrap with $V$ of the last state there.
- **Stale values.** The values must come from the critic before its update on the same batch; recomputing them after the update gives targets that chase themselves.
- **Gradients through the estimate.** $\hat A_t$ and $\hat G_t$ are constants for the actor and critic losses.
- **$\lambda = 1$ with long segments.** The variance can be as large as that of REINFORCE; a slightly smaller $\lambda$ often helps a lot.

## Implementations

## History

The $\lambda$-return goes back to Sutton's TD($\lambda$) (1988) and Watkins (1989). Kimura and Kobayashi (1998) used a $\lambda$-weighted advantage with an imperfect critic in an actor-critic, and Sutton and Barto describe actor-critics with eligibility traces. Schulman, Moritz, Levine, Jordan and Abbeel (2015 preprint, ICLR 2016) defined GAE($\gamma$, $\lambda$), analysed it with the notion of $\gamma$-just estimators and the reward shaping view, and combined it with [TRPO](/trpo/) for both the policy and the value function to learn running gaits for simulated 3D robots. Since [PPO](/ppo/) (2017), GAE has been the default advantage estimator in on-policy deep RL.

## References
