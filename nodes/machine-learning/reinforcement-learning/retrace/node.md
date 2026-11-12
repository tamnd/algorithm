---
tag: Y7PV00
kind: algorithm
slug: retrace
name: Retrace
aliases:
- Retrace(lambda)
- Retrace operator
area: machine-learning/reinforcement-learning
level: research
summary: "Off-policy multi-step learning of Q with traces c = lambda min(1, pi/mu). The operator is a gamma-contraction to Q^pi for any behavior policy, with no trace cut on-policy."
solves: [off-policy-evaluation, rl-control]
model: real-ram
complexity:
  vars: {T: the length of the trajectory, A: the number of actions}
  time: {worst: "O(T A)"}
  space: {extra: "O(T)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2016
  people: [Rémi Munos, Tom Stepleton, Anna Harutyunyan, Marc G. Bellemare]
  note: "Munos, Stepleton, Harutyunyan and Bellemare unified off-policy return-based methods with one trace function and derived Retrace(lambda), the first such control method shown to converge to Q* without the GLIE assumption."
prereqs: [importance-sampling-off-policy, eligibility-traces, action-value-function]
see_also: [v-trace, watkins-q-lambda, td-lambda, off-policy-evaluation, experience-replay, dqn, actor-critic, deadly-triad]
sources:
  - paper: arxiv:1606.02647
    title: Rémi Munos, Tom Stepleton, Anna Harutyunyan and Marc G. Bellemare, Safe and efficient off-policy reinforcement learning, Advances in Neural Information Processing Systems 29, 2016
    locator: the general operator with traces c_s, Retrace(lambda), the contraction theorem for policy evaluation, and the control results including the convergence of Watkins' Q(lambda)
  - paper: doi:10.1007/978-3-319-46379-7_21
    title: Anna Harutyunyan, Marc G. Bellemare, Tom Stepleton and Rémi Munos, Q(lambda) with off-policy corrections, Algorithmic Learning Theory 2016, Lecture Notes in Computer Science 9925, pages 305 to 320
    locator: Q^pi(lambda) and Q*(lambda), and the condition on lambda, gamma and the distance between the policies under which they converge
  - paper: "Doina Precup, Richard S. Sutton and Satinder Singh, Eligibility traces for off-policy policy evaluation, Proceedings of the 17th International Conference on Machine Learning, 2000, pages 759 to 766"
    locator: Tree Backup and per-decision importance sampling traces
  - paper: arxiv:1611.01224
    title: Ziyu Wang, Victor Bapst, Nicolas Heess, Volodymyr Mnih, Rémi Munos, Koray Kavukcuoglu and Nando de Freitas, Sample efficient actor-critic with experience replay, International Conference on Learning Representations, 2017
    locator: ACER, which uses Retrace targets for the critic
---

Retrace($\lambda$) learns the [action value function](/action-value-function/) $Q^\pi$ of a target policy $\pi$ from multi-step trajectories of a different behavior policy $\mu$. Like every [eligibility trace](/eligibility-traces/) method, it corrects $Q(x_t, a_t)$ with a discounted sum of later TD errors, each weighted by the product of trace coefficients $c_s$ of the steps in between. Retrace chooses $c_s = \lambda\min(1, \pi(a_s \mid x_s)/\mu(a_s \mid x_s))$: an [importance sampling](/importance-sampling-off-policy/) ratio truncated at $1$. Munos, Stepleton, Harutyunyan and Bellemare (2016) show that this choice has three properties at once. The traces are at most $1$, so the variance stays bounded. The expected operator is a $\gamma$-contraction to $Q^\pi$ for any $\mu$, so it is safe. On-policy the traces are $\lambda$ and are not cut, so it is efficient. Tree Backup is safe but cuts traces even on-policy; $Q^\pi(\lambda)$ never cuts them and can diverge far off-policy; plain importance sampling is safe but has unbounded variance.

## In plain words

You want to learn how good each move is under a new way of acting, but your records come from an old way of acting. A one-step update looks only at the next reward and your current guess. A multi-step update also uses the later steps of the record, which carries information faster, but those later steps follow the old way of acting, not the new one.

Retrace keeps using later steps as long as the old choices are ones the new way would also make. Each step can only shrink the trust in what comes after it, never raise it, so no single step can blow up the update. If both ways of acting are the same, the trust never shrinks. If the old way made a choice the new way would never make, the trust drops to zero and the update stops there.

## The problem

The input is a trajectory $x_0, a_0, r_0, x_1, \ldots, x_T$ from $\mu$, with $\mu(a_t \mid x_t) > 0$ known, a target policy $\pi$, a current estimate $Q$, a discount $\gamma < 1$, a trace parameter $\lambda \in [0, 1]$ and a step size $\alpha$. The goal is the fixed point $Q^\pi$ of the [Bellman expectation equation](/bellman-expectation-equation/) for $Q$, that is [off-policy evaluation](/off-policy-evaluation/) of $\pi$; with $\pi$ greedy with respect to $Q$, the goal is $Q^*$, the [control problem](/rl-control/).

## The algorithm

Write $\mathbb{E}_\pi Q(x, \cdot) = \sum_b \pi(b \mid x)Q(x, b)$. The Retrace target is

$$Q^{\text{ret}}_t = Q(x_t, a_t) + \sum_{s \ge t}\gamma^{s-t}\Big(\prod_{i=t+1}^{s}c_i\Big)\big(r_s + \gamma\mathbb{E}_\pi Q(x_{s+1}, \cdot) - Q(x_s, a_s)\big), \qquad c_i = \lambda\min\Big(1, \frac{\pi(a_i \mid x_i)}{\mu(a_i \mid x_i)}\Big).$$

It satisfies the backward recursion $Q^{\text{ret}}_t = r_t + \gamma\big[\mathbb{E}_\pi Q(x_{t+1}, \cdot) + c_{t+1}(Q^{\text{ret}}_{t+1} - Q(x_{t+1}, a_{t+1}))\big]$, which the algorithm uses.

```pseudo id=main
RETRACE(x₀, a₀, r₀, …, x_T;  Q, π, μ, γ, λ, α)
L1  g ← Σ_b π(b | x_T) Q(x_T, b), or 0 if x_T is terminal
L2  for t ← T − 1 down to 0 do
L3      y_t ← r_t + γ g                                 ▷ the target Q^ret_t
L4      c ← λ min(1, π(a_t | x_t) / μ(a_t | x_t))
L5      g ← Σ_b π(b | x_t) Q(x_t, b) + c (y_t − Q(x_t, a_t))
L6  for t ← 0 to T − 1 do
L7      Q(x_t, a_t) ← Q(x_t, a_t) + α (y_t − Q(x_t, a_t))
L8  return y₀, …, y_{T−1}
```

All targets use the $Q$ from before the updates. With a neural network, line L7 becomes a gradient step on $\sum_t(y_t - Q_\theta(x_t, a_t))^2$, with the targets held fixed, as in ACER. Changing line L4 gives the other methods: $c = \lambda\pi(a_t \mid x_t)$ is Tree Backup, $c = \lambda$ is $Q^\pi(\lambda)$, and $c = \lambda\pi/\mu$ is per-decision importance sampling.

## Example

The switch MDP has two states. Action $0$ moves to the other state, action $1$ stays, and the rewards are $1$ for leaving state $0$, $2$ for staying in state $1$, and $0$ otherwise. Take $\gamma = 0.9$, $\lambda = 1$, and the same action probabilities in both states. The expected operator $\mathcal{R}$ of each method is affine, and $\mathcal{R}Q - Q^\pi$ is a linear map $M$ of $Q - Q^\pi$. The table gives the spectral radius of $M$, the factor by which the error shrinks per application in the long run; a value above $1$ means the iteration diverges.

| $\pi$ | $\mu$ | $Q^\pi(\lambda)$ | Tree Backup | Retrace |
|---|---|---|---|---|
| $(1, 0)$ | $(0.1, 0.9)$ | 5.786 | 0.890 | 0.890 |
| $(0.7, 0.3)$ | $(0.3, 0.7)$ | 1.125 | 0.839 | 0.783 |
| $(0.9, 0.1)$ | $(0.5, 0.5)$ | 0.720 | 0.818 | 0.783 |
| $(0.5, 0.5)$ | $(0.5, 0.5)$ | 0 | 0.818 | 0 |

In the first row $\pi$ is deterministic, so $\min(1, \pi/\mu) = \pi$ and Retrace equals Tree Backup. $Q^\pi(\lambda)$ diverges there, and still diverges with $\lambda = 0.5$ (radius $1.969$); the safe bound of Harutyunyan et al. (2016) asks for $\lambda < 0.1/(0.9 \cdot 1.8) \approx 0.062$. In the last row the data are on-policy: Retrace and $Q^\pi(\lambda)$ use full traces and reach $Q^\pi$ in one application, while Tree Backup multiplies its traces by $\pi = 0.5$ at every step and contracts no faster than at rate $0.818$. In the third row $Q^\pi(\lambda)$ is fastest, but its sup norm factor is $7.2$, so it is not a contraction.

## Correctness

The [proof](proofs/correctness.md) first shows that the backward recursion computes the sum of traced TD errors, so the mean target from $(x, a)$ is $\mathcal{R}Q(x, a) = Q(x, a) + \big[(I - \gamma P^{c\mu})^{-1}(T^\pi Q - Q)\big](x, a)$ with $P^{c\mu}((x, a), (y, b)) = P(y \mid x, a)\mu(b \mid y)c(y, b)$. It then proves Theorem 1 of Munos et al. (2016): if $0 \le c \le \pi/\mu$, then $\|\mathcal{R}Q - Q^\pi\|_\infty \le \gamma\|Q - Q^\pi\|_\infty$. The key step writes $\mathcal{R}Q - Q^\pi$ as a combination of values of $Q - Q^\pi$ with weights $\gamma^t c_1 \cdots c_{t-1}(\pi(b \mid x_t) - \mu(b \mid x_t)c(x_t, b))$, which are nonnegative under the condition and sum to at most $\gamma$. Retrace, Tree Backup and importance sampling meet the condition; $Q^\pi(\lambda)$ does not.

For control, Munos et al. (2016) prove that the Retrace iteration with increasingly greedy target policies converges to $Q^*$, and that online Retrace converges almost surely under the usual [Robbins-Monro conditions](/robbins-monro-conditions/), without requiring the behavior policy to become greedy. As a corollary they prove the convergence of [Watkins' Q(lambda)](/watkins-q-lambda/), whose traces are the Retrace traces for a greedy $\pi$.

## Complexity

One pass over a trajectory of length $T$ costs $O(TA)$ time, for the expectations $\mathbb{E}_\pi Q(x_t, \cdot)$ over $A$ actions, and $O(T)$ memory for the targets. With a network, the cost is one forward pass per state of the trajectory, the same as an $n$-step return.

## Properties

- **Off-policy and safe.** Converges to $Q^\pi$ for any behavior policy with $\mu > 0$ where it is used.
- **Bounded traces.** $c_s \le \lambda \le 1$, so the targets have no products of large ratios.
- **Efficient near on-policy.** When $\pi = \mu$, $c_s = \lambda$, the same as on-policy [TD($\lambda$)](/td-lambda/) for $Q$.
- **Cuts traces off-policy.** One step with a small $\pi/\mu$ cuts all later corrections, which can make it slow when $\pi$ and $\mu$ are far apart.
- **Tabular theory.** The contraction holds for the expected operator in the tabular case; with function approximation the [deadly triad](/deadly-triad/) still applies.

## Variants and improvements

- **Tree Backup** (Precup, Sutton and Singh 2000): $c_s = \lambda\pi(a_s \mid x_s)$. Needs no knowledge of $\mu$ but cuts traces on-policy.
- **$Q^\pi(\lambda)$ and $Q^*(\lambda)$** (Harutyunyan et al. 2016): $c_s = \lambda$. No cuts, no ratios; safe only when $\lambda$ is small compared with $(1 - \gamma)/(\gamma\epsilon)$.
- **Watkins' Q($\lambda$):** for greedy $\pi$, Retrace traces are $\lambda$ on greedy actions and $0$ otherwise, which is [Watkins' Q(lambda)](/watkins-q-lambda/).
- **ACER** (Wang et al. 2017): an [actor-critic](/actor-critic/) method with [experience replay](/experience-replay/) whose critic learns from Retrace targets.
- **V-trace** (Espeholt et al. 2018): the state value analogue with clipped ratios in both the correction and the traces; see [V-trace](/v-trace/).
- **Reactor** and later replay agents combine Retrace with distributional and prioritized updates.

## When to use it

Use Retrace to learn $Q$ from replayed or logged multi-step data generated by older or different policies, when the behavior probabilities are known. It is a good default for multi-step off-policy targets in replay-based agents. For one-step learning there is no trace and Retrace is plain [expected SARSA](/expected-sarsa/). If $\mu$ is unknown, use Tree Backup.

## Pitfalls

- **Unknown or wrong $\mu$.** The traces need $\mu(a_t \mid x_t)$ at the time the data were collected; store it with each transition.
- **Using the updated $Q$ inside the targets.** Compute all targets of a trajectory before updating $Q$.
- **Expecting long traces off-policy.** With a near-greedy $\pi$ and an exploratory $\mu$, most traces are cut after a few steps, and the method behaves like a short $n$-step return.
- **Truncating at $1$ in the wrong place.** The truncation is on each factor, $\min(1, \pi/\mu)$, not on the product.

## Implementations

## History

Off-policy eligibility traces go back to Precup, Sutton and Singh (2000), who introduced Tree Backup and per-decision importance sampling. Harutyunyan, Bellemare, Stepleton and Munos (2016) studied traces with no correction, $Q^\pi(\lambda)$, and found the condition on $\lambda$ under which they still converge. In the same year Munos, Stepleton, Harutyunyan and Bellemare wrote all these methods with one trace function $c$, proved the contraction theorem for $0 \le c \le \pi/\mu$, and proposed Retrace($\lambda$) as the choice that is safe, efficient and of low variance. ACER (2017) and Reactor used it for deep agents, and IMPALA's [V-trace](/v-trace/) (2018) adapted it to state values.

## References
