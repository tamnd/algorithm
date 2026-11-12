---
tag: V75JCF
kind: algorithm
slug: v-trace
name: V-trace
aliases:
- IMPALA V-trace
- V-trace target
area: machine-learning/reinforcement-learning
level: research
summary: "Off-policy n-step value targets with ratios clipped at rho-bar in the TD errors and c-bar in the traces. Learns the value of a policy between mu and pi; on-policy it is the n-step return."
solves: [off-policy-evaluation, rl-control]
model: real-ram
complexity:
  vars: {n: the number of steps in the trajectory}
  time: {worst: "O(n)"}
  space: {extra: "O(n)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2018
  people: [Lasse Espeholt, Hubert Soyer, Rémi Munos, Karen Simonyan, Volodymyr Mnih, Tom Ward, Yotam Doron, Vlad Firoiu, Tim Harley, Iain Dunning, Shane Legg, Koray Kavukcuoglu]
  note: "Introduced with the IMPALA distributed actor-learner architecture, to correct for the lag between the policies of the actors and of the learner."
prereqs: [retrace, importance-sampling-off-policy, n-step-td]
see_also: [a3c, actor-critic, policy-gradient-theorem, td-lambda, off-policy-evaluation, experience-replay, ppo, deadly-triad]
sources:
  - paper: arxiv:1802.01561
    title: Lasse Espeholt, Hubert Soyer, Rémi Munos, Karen Simonyan, Volodymyr Mnih, Tom Ward, Yotam Doron, Vlad Firoiu, Tim Harley, Iain Dunning, Shane Legg and Koray Kavukcuoglu, IMPALA, Scalable distributed deep-RL with importance weighted actor-learner architectures, Proceedings of the 35th International Conference on Machine Learning, 2018
    locator: Section 4 (the V-trace target, its on-policy form, the recursive form and the actor-critic update) and Appendix A (Theorem 1 on the fixed point and contraction, Theorem 2 on online convergence)
  - paper: arxiv:1606.02647
    title: Rémi Munos, Tom Stepleton, Anna Harutyunyan and Marc G. Bellemare, Safe and efficient off-policy reinforcement learning, Advances in Neural Information Processing Systems 29, 2016
    locator: Retrace(lambda), the action value method with truncated traces that V-trace adapts to state values
---

V-trace computes off-policy multi-step targets for a state value function $V$ from trajectories of a behavior policy $\mu$, to learn about a target policy $\pi$. Each TD error is weighted by a ratio clipped at $\bar{\rho}$, and each step of the trace by a ratio clipped at $\bar{c}$. Espeholt et al. (2018) introduced it for IMPALA, a distributed [actor-critic](/actor-critic/) system in which many actors generate data with slightly old copies of the policy while one learner updates the newest copy. The two clipping levels play different roles. $\bar{\rho}$ fixes what is learned: the value of the policy $\pi_{\bar{\rho}} \propto \min(\bar{\rho}\mu, \pi)$, which lies between $\mu$ and $\pi$ and equals $\pi$ when $\bar{\rho}$ is large. $\bar{c}$ only sets how fast the operator contracts and how much variance the traces carry. On-policy, with $\bar{\rho}, \bar{c} \ge 1$, the target is exactly the [n-step return](/n-step-td/), so the same code serves on-policy and off-policy data. It adapts [Retrace](/retrace/) from action values to state values.

## In plain words

Many workers play a game with copies of the current rule for acting, while a central learner improves the rule. By the time the learner sees a worker's game, the rule has changed a little, so the game was played by a slightly old rule.

V-trace corrects for this. Where the new rule likes a move more than the old rule did, the move counts more, but only up to a cap, so that rare moves cannot swing the update. The trust in later steps of the game also shrinks where the new rule likes the moves less. The cap means the learner learns about a rule a little closer to the old one than the new one, but the answers stay steady. If the old and new rules are the same, nothing is changed and the update is the usual one.

## The problem

The input is a trajectory $x_s, a_s, r_s, \ldots, x_{s+n}$ from $\mu$, the probabilities $\mu(a_t \mid x_t)$ and $\pi(a_t \mid x_t)$, a value estimate $V$, a discount $\gamma < 1$, clipping levels $\bar{\rho} \ge \bar{c} > 0$, and a step size $\alpha$. The output is a target $v_t$ for every $V(x_t)$, and an advantage estimate for the policy gradient. The goal is a state value function for [off-policy evaluation](/off-policy-evaluation/) inside an actor-critic method for the [control problem](/rl-control/).

## The algorithm

With $\rho_t = \min(\bar{\rho}, \pi(a_t \mid x_t)/\mu(a_t \mid x_t))$, $c_i = \min(\bar{c}, \pi(a_i \mid x_i)/\mu(a_i \mid x_i))$ and $\delta_t = \rho_t(r_t + \gamma V(x_{t+1}) - V(x_t))$, the $n$-step V-trace target is

$$v_s = V(x_s) + \sum_{t=s}^{s+n-1}\gamma^{t-s}\Big(\prod_{i=s}^{t-1}c_i\Big)\delta_t,$$

and it satisfies $v_t = V(x_t) + \delta_t + \gamma c_t(v_{t+1} - V(x_{t+1}))$ with $v_{s+n} = V(x_{s+n})$.

```pseudo id=main
V-TRACE(x_s, a_s, r_s, …, x_{s+n};  V, π, μ, γ, ρ̄, c̄, α)
L1  v_{s+n} ← V(x_{s+n}), or 0 if x_{s+n} is terminal
L2  for t ← s + n − 1 down to s do
L3      ρ_t ← min(ρ̄, π(a_t | x_t) / μ(a_t | x_t));   c_t ← min(c̄, π(a_t | x_t) / μ(a_t | x_t))
L4      δ_t ← ρ_t (r_t + γ V(x_{t+1}) − V(x_t))
L5      v_t ← V(x_t) + δ_t + γ c_t (v_{t+1} − V(x_{t+1}))
L6      A_t ← ρ_t (r_t + γ v_{t+1} − V(x_t))            ▷ advantage for the policy gradient
L7  for t ← s to s + n − 1:  V(x_t) ← V(x_t) + α (v_t − V(x_t))
L8  return v_s, …, v_{s+n−1} and A_s, …, A_{s+n−1}
```

In IMPALA the value network takes a gradient step on $\sum_t(v_t - V_\theta(x_t))^2$, which is line L7 for a network, and the policy network takes a step along $\sum_t A_t\nabla\log\pi_\omega(a_t \mid x_t)$, plus an entropy bonus. The advantage uses $r_t + \gamma v_{t+1}$, an estimate of $Q^{\pi_{\bar{\rho}}}(x_t, a_t)$. With an extra trace parameter, $c_i = \lambda\min(\bar{c}, \pi/\mu)$.

## Example

**What $\bar{\rho}$ learns.** One state, two actions, the episode ends after one step. Action $0$ has reward $1$ and action $1$ has reward $0$. The target policy is $\pi = (0.9, 0.1)$ and the behavior policy is $\mu = (0.2, 0.8)$, so $V^\pi = 0.9$ and $V^\mu = 0.2$. The target is $v = V + \rho(r - V)$, and its mean is zero at $V = \sum_a\min(\bar{\rho}\mu(a), \pi(a))r(a)/\sum_a\min(\bar{\rho}\mu(a), \pi(a))$.

| $\bar{\rho}$ | $\min(\bar{\rho}\mu, \pi)$ | $\pi_{\bar{\rho}}$ | fixed point |
|---|---|---|---|
| 0.1 | $(0.02, 0.08)$ | $(0.2, 0.8) = \mu$ | 0.2 |
| 0.5 | $(0.1, 0.1)$ | $(0.5, 0.5)$ | 0.5 |
| 1 | $(0.2, 0.1)$ | $(2/3, 1/3)$ | 0.667 |
| 2 | $(0.4, 0.1)$ | $(0.8, 0.2)$ | 0.8 |
| 4.5 | $(0.9, 0.1)$ | $(0.9, 0.1) = \pi$ | 0.9 |

The common choice $\bar{\rho} = 1$, which Espeholt et al. (2018) found to work best in their experiments, learns $0.667$ here, not $0.9$: a bias toward $\mu$ in exchange for bounded weights. In IMPALA the actors lag the learner by only a few updates, so $\pi$ and $\mu$ are close and $\pi_1$ is close to $\pi$.

**A two-state problem.** Action $0$ in state $0$ moves to state $1$ with reward $1$, and action $1$ stays with reward $0$. Action $0$ in state $1$ moves to state $0$ with reward $0$ or stays with reward $3$, each with probability $1/2$, and action $1$ stays with reward $2$. With $\gamma = 0.9$, $\pi = (0.9, 0.1)$ in state $0$ and $(0.2, 0.8)$ in state $1$, and $\mu = (0.25, 0.75)$ and $(0.5, 0.5)$, the exact values are $V^\mu = (8.64, 11.36)$, $V^{\pi_1} = (15.57, 16.89)$, $V^{\pi_2} = (16.84, 17.98)$ and $V^\pi = (17.10, 18.10)$. Sampled V-trace with $\bar{\rho} = \bar{c} = 1$, $6000$ trajectories of $10$ steps and $\alpha = 0.01$ ends at $(15.51, 16.83)$, $(15.89, 17.19)$ and $(15.78, 17.08)$ for seeds 0, 1 and 2. Without clipping, it ends at $(16.94, 17.98)$, $(17.86, 18.75)$ and $(17.52, 18.64)$: near $V^\pi$, but with more than twice the spread across seeds.

## Correctness

The [proof](proofs/correctness.md) follows Appendix A of Espeholt et al. (2018). The recursion of line L5 computes the sum of clipped and traced TD errors, so the mean target is the V-trace operator $\mathcal{R}V$. Rewriting $\mathcal{R}V_1 - \mathcal{R}V_2$ as a combination of values of $V_1 - V_2$ shows that the weights are nonnegative, because $c_t \le \rho_t$ and $\mathbb{E}_\mu\rho_t \le 1$, and that they sum to at most $1 - (1 - \gamma)\beta$ with $\beta = \min_x\mathbb{E}_\mu\rho_0$. So $\mathcal{R}$ is a contraction. Each clipped TD error has conditional mean $N(x)(T^{\pi_{\bar{\rho}}}V - V)(x)$, with $N(x) = \sum_b\min(\bar{\rho}\mu(b \mid x), \pi(b \mid x))$, so the fixed point is $V^{\pi_{\bar{\rho}}}$, whatever $\bar{c}$ is. On-policy, with $\bar{\rho}, \bar{c} \ge 1$, all ratios are $1$ and the sum telescopes to the $n$-step return. With step sizes that meet the [Robbins-Monro conditions](/robbins-monro-conditions/) and every state visited infinitely often, the online tabular update converges almost surely to $V^{\pi_{\bar{\rho}}}$ (Espeholt et al. 2018, Theorem 2).

## Complexity

A trajectory of $n$ steps costs $O(n)$ time and $O(n)$ memory, one backward pass. Unlike [Retrace](/retrace/), it needs only the probabilities of the actions taken, not a sum over all actions. With networks, the cost is one forward pass of the value and policy networks per state; IMPALA computes the targets for a batch of trajectories on the learner.

## Properties

- **Off-policy with bounded weights.** Products of ratios appear only in the traces, which are clipped at $\bar{c}$; the TD errors use single ratios clipped at $\bar{\rho}$.
- **Biased toward $\mu$ when $\bar{\rho}$ is small.** The fixed point is $V^{\pi_{\bar{\rho}}}$, not $V^\pi$, unless $\bar{\rho} \ge \max\pi/\mu$.
- **On-policy exact.** With $\pi = \mu$ it is the $n$-step return, unlike Retrace, whose on-policy target uses $\mathbb{E}_\pi Q$.
- **The fixed point does not depend on $\bar{c}$.** $\bar{c}$ trades the speed of contraction against the variance of the traces.

## Variants and improvements

- **V-trace with $\lambda$.** $c_i = \lambda\min(\bar{c}, \pi/\mu)$; on-policy with $n = \infty$ it is [TD($\lambda$)](/td-lambda/).
- **Retrace.** The action value version, with $c_i = \lambda\min(1, \pi/\mu)$ and no clipping in the TD errors, converges to $Q^\pi$ itself; see [Retrace](/retrace/).
- **Policy gradient with clipped ratios.** The IMPALA actor update weights each advantage by $\rho_t$; it follows the [policy gradient](/policy-gradient-theorem/) of $\pi_{\bar{\rho}}$ rather than $\pi$. [PPO](/ppo/) also clips ratios, but to keep each update close to the old policy, not to correct for lag.
- **Synchronous actor-critic.** With no lag, IMPALA becomes a batched [A3C](/a3c/)-style method, and V-trace becomes the $n$-step return.
- **Replay.** Adding [experience replay](/experience-replay/) on the learner makes the data more off-policy; V-trace keeps it stable at the cost of bias.

## When to use it

Use V-trace in actor-critic systems where the data come from slightly stale policies: distributed actors, asynchronous updates or a small replay buffer. It is cheap, needs only the logged probabilities of the actions taken, and falls back to the $n$-step return on-policy. For learning about a policy far from the behavior policy, its bias toward $\mu$ grows; use Retrace for action values or larger $\bar{\rho}$ with more variance.

## Pitfalls

- **Not storing $\mu(a_t \mid x_t)$.** The actors must send the probability of each action under the policy they used; recomputing it later with the learner's network gives $\pi$, not $\mu$.
- **$\bar{c} > \bar{\rho}$.** The proof needs $c_t \le \rho_t$; with larger traces the contraction can fail.
- **Reading the fixed point as $V^\pi$.** With $\bar{\rho} = 1$ and a large policy lag, the learned value belongs to a mixture of $\mu$ and $\pi$.
- **Bootstrapping across episode ends.** At a terminal state, $V(x_{t+1})$ must be $0$ and the trace must stop.

## Implementations

## History

Espeholt et al. (2018) introduced V-trace together with IMPALA, a system of actors and learners that scales to thousands of machines, tested on DeepMind Lab and Atari tasks. They derived it from the Retrace analysis of Munos et al. (2016), moved it from action values to state values, and split the single truncation of Retrace into two levels with the roles described above. Their experiments compared it with no correction, $\epsilon$-correction and one-step importance sampling. With a small policy lag, V-trace and one-step importance sampling did about equally well; with the larger lag of experience replay, V-trace did best on 4 of 5 tasks.

## References
