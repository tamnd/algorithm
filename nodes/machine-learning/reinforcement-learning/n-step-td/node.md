---
tag: FP2Z3F
kind: algorithm
slug: n-step-td
name: n-step temporal-difference learning
aliases:
- n-step TD
- n-step return
- n-step TD prediction
area: machine-learning/reinforcement-learning
level: core
summary: "Move V(S_t) toward the n-step return: n discounted rewards plus gamma^n V(S_(t+n)). n = 1 is TD(0), and n at least the episode length is Monte Carlo."
solves: [policy-evaluation]
model: real-ram
complexity:
  vars: {T: the total number of steps, n: the number of steps before bootstrapping, S: the number of states}
  time: {worst: "O(n T)"}
  space: {extra: "O(S + n)"}
properties: {deterministic: true, online: true, exact: false, recursive: false}
prereqs: [temporal-difference-learning, monte-carlo-policy-evaluation, td-error]
see_also: [td-lambda, eligibility-traces, sarsa, expected-sarsa, retrace, bellman-contraction]
sources:
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: Section 7.1 (n-step TD prediction, the n-step return, the error reduction property in equation 7.3, and the 19-state random walk) and Section 7.2 (n-step Sarsa)
  - paper: doi:10.1007/BF00115009
    title: "Richard S. Sutton, Learning to predict by the methods of temporal differences, Machine Learning 3(1), 1988, pages 9 to 44"
    locator: the family of predictions between one-step TD and the Widrow-Hoff (Monte Carlo) rule
  - paper: "Christopher J. C. H. Watkins, Learning from delayed rewards, PhD thesis, King's College, University of Cambridge, 1989"
    locator: the chapter on temporal difference methods (corrected n-step truncated returns)
---

n-step TD is the [policy evaluation](/policy-evaluation/) method that updates $V(S_t)$ toward the $n$-step return: the next $n$ rewards, discounted, plus $\gamma^n V(S_{t+n})$. It fills the range between [TD(0)](/temporal-difference-learning/), the case $n = 1$, and constant-$\alpha$ [Monte Carlo](/monte-carlo-policy-evaluation/), the case where $n$ reaches the end of the episode. Its expected target is $n$ applications of the Bellman operator, so its error shrinks by $\gamma^n$ (the error reduction property, Sutton and Barto, equation 7.3). Intermediate values of $n$ often learn fastest in practice.

## In plain words

TD(0) looks one step ahead and then trusts its own guess. Monte Carlo looks all the way to the end and trusts nothing. n-step TD picks a middle point: it waits a fixed number of steps, adds up the rewards it saw, and only then uses its guess for the place it reached.

Waiting longer means less trust in guesses that may be wrong, but also more random rewards in the sum, so more noise. Waiting less means less noise but more dependence on guesses. A middle value often learns fastest. Each update can only happen a fixed number of steps late, because the method needs those future rewards first.

## The problem

The setting is the one of [TD(0)](/temporal-difference-learning/): an unknown MDP, a fixed policy $\pi$, the discounted criterion with $0 \le \gamma \le 1$ (with $\gamma = 1$ only if episodes end with probability 1), and the goal $V^\pi$. Episodes are the pairs $(S_t, R_{t+1})$ for $t < T$, with $S_T$ terminal and $V(S_T) = 0$. For $n \ge 1$, the **n-step return** is

$$G_{t:t+n} = R_{t+1} + \gamma R_{t+2} + \cdots + \gamma^{n-1} R_{t+n} + \gamma^n V(S_{t+n}) \quad (t + n < T),$$

and $G_{t:t+n} = G_t$, the full return, when $t + n \ge T$. The table $V$ in the formula is the one at the time of the update, time $t + n$.

## The algorithm

```pseudo id=main
N-STEP-TD(episodes, n, α, γ, V)
L1  for each episode (S_0, R_1), ..., (S_{T−1}, R_T) do
L2      for τ ← 0 to T − 1 do                         ▷ online: done at time τ + n
L3          G ← Σ_{i = τ+1}^{min(τ+n, T)} γ^{i−τ−1} R_i
L4          if τ + n < T then G ← G + γ^n V(S_{τ+n})
L5          V(S_τ) ← V(S_τ) + α (G − V(S_τ))
L6  return V
```

Line L3 adds the discounted rewards of the window, and line L4 adds the bootstrap term unless the window reaches the end. Line L5 is the update. In the online form of Sutton and Barto (Section 7.1), the update of $S_\tau$ runs at time $t = \tau + n - 1$, right after $R_{\tau+n}$ and $S_{\tau+n}$ are seen, and the last $n - 1$ updates run after the episode ends. That online program does the same updates in the same order $\tau = 0, 1, \ldots$, and each update sees exactly the earlier ones, so it gives the same values as this loop. The online form keeps only the last $n + 1$ states and rewards.

## Example

Take the random walk A to E of the [TD(0)](/temporal-difference-learning/) page: start in C, reward 1 only when leaving at the right end, $\gamma = 1$, $V = 1/2$ everywhere, $\alpha = 1/10$, and $n = 2$. Episode 1 is C, B, C, D, E, right. Episode 2 is C, D, E, D, C, B, A, left.

| episode | $\tau$ | $S_\tau$ | $G_{\tau:\tau+2}$ | new $V(S_\tau)$ |
| --- | --- | --- | --- | --- |
| 1 | 0 to 2 | C, B, C | $0 + 0 + 1/2$ | unchanged |
| 1 | 3 | D | $0 + 1 = 1$ (end) | $11/20$ |
| 1 | 4 | E | $1$ (end) | $11/20$ |
| 2 | 0 | C | $V(\mathrm{E}) = 11/20$ | $101/200$ |
| 2 | 1 | D | $V(\mathrm{D}) = 11/20$ | $11/20$ |
| 2 | 2 | E | $V(\mathrm{C}) = 101/200$ | $1091/2000$ |
| 2 | 3 | D | $V(\mathrm{B}) = 1/2$ | $109/200$ |
| 2 | 4 | C | $V(\mathrm{A}) = 1/2$ | $1009/2000$ |
| 2 | 5 | B | $0$ (end) | $9/20$ |
| 2 | 6 | A | $0$ (end) | $9/20$ |

After episode 1, two states have learned from the reward, D and E, where TD(0) changed only E. After episode 2 the values are A $= 0.45$, B $= 0.45$, C $= 0.5045$, D $= 0.545$, E $= 0.5455$. With $n = 3$ and the steps $\alpha_k = 0.5\, k^{-0.6}$ for episode $k$, 4000 episodes give values within $0.04$ of $s/6$ (seed 8 in the tests).

## Correctness

**Error reduction property.** Let $V$ be the table used for the bootstrap. Then for every $n \ge 1$,

$$\max_s \Big| \mathbb{E}_\pi[G_{t:t+n} \mid S_t = s] - V^\pi(s) \Big| \le \gamma^n \max_s |V(s) - V^\pi(s)| .$$

*Proof.* Let $P_\pi$ be the transition matrix of $\pi$ among the nonterminal states (it is substochastic, since the terminal state is left out) and $r_\pi$ the expected reward vector. By the Markov property, $\mathbb{E}_\pi[G_{t:t+n} \mid S_t = \cdot] = \sum_{k=0}^{n-1} \gamma^k P_\pi^k r_\pi + \gamma^n P_\pi^n V$, where the terminal state contributes 0 to both terms. The value $V^\pi$ satisfies $V^\pi = r_\pi + \gamma P_\pi V^\pi$, and unrolling it $n$ times gives $V^\pi = \sum_{k=0}^{n-1} \gamma^k P_\pi^k r_\pi + \gamma^n P_\pi^n V^\pi$. Subtracting, the difference is $\gamma^n P_\pi^n (V - V^\pi)$. Each row of $P_\pi^n$ has nonnegative entries that sum to at most 1, so each entry of the difference is at most $\gamma^n \max_s |V(s) - V^\pi(s)|$ in absolute value. $\square$

In operator form, the expected target is $(T^\pi)^n V$, a $\gamma^n$-contraction toward $V^\pi$. So $V^\pi$ is the only fixed point of the expected update, and a larger $n$ gives a stronger pull toward it per update. Sutton and Barto (Section 7.1) note that this property lets one show that all $n$-step TD methods converge to $V^\pi$ under suitable conditions on the steps. The proofs section proves the error reduction property, the equivalence with the online loop, and the two end cases $n = 1$ and $n \ge T$.

## Complexity

Lines L3 and L4 cost $O(\min(n, T))$ arithmetic operations, so an episode of $T$ steps costs $O(nT)$ time. The online form stores the last $n + 1$ states and rewards and the table: $O(|S| + n)$ memory. Each update is late by $n - 1$ steps. No sample complexity bound in $n$ alone is known to us; the best $n$ depends on the task. On the 19-state random walk, Sutton and Barto (Section 7.1) observed the lowest error for an intermediate $n$, neither 1 nor the full episode; this is an observation for that task, not a theorem.

## Properties

- **Bias and variance.** For a wrong $V$, the bias of the target shrinks by $\gamma^n$ (the error reduction property), while the variance grows with $n$, since the target sums $n$ random rewards.
- **Delayed.** The update of $S_t$ waits $n$ steps, so a state is not improved until $n$ steps after the visit.
- **End cases.** $n = 1$ gives the same updates as [TD(0)](/temporal-difference-learning/), and $n \ge T$ gives the same updates as incremental constant-$\alpha$ every-visit [Monte Carlo](/monte-carlo-policy-evaluation/).
- **Sum of TD errors.** If $V$ does not change during the window, $G_{t:t+n} - V(S_t) = \sum_{k=t}^{t+n-1} \gamma^{k-t} \delta_k$ ([TD error](/td-error/), Property 2).

## Variants and improvements

- **n-step SARSA and n-step Expected SARSA.** Use $Q(S_{t+n}, A_{t+n})$ or the expectation under $\pi$ as the bootstrap (Sutton and Barto, Section 7.2). See [SARSA](/sarsa/) and [Expected SARSA](/expected-sarsa/).
- **Off-policy n-step.** Weight the update by the product of $n$ importance ratios ([importance sampling](/importance-sampling-off-policy/)), or use the tree backup and [Retrace](/retrace/), which keep the variance bounded.
- **Averages of n-step returns.** Any convex mix of $n$-step returns also has the error reduction property. The geometric mix with weights $(1-\lambda)\lambda^{n-1}$ is the λ-return of [TD(λ)](/td-lambda/), which [eligibility traces](/eligibility-traces/) compute without delay.
- **Function approximation.** Replace line L5 by $w \leftarrow w + \alpha(G - \hat v(S_\tau, w)) \nabla \hat v(S_\tau, w)$.

## When to use it

Use n-step TD when TD(0) learns too slowly because the reward is many steps away, and Monte Carlo is too noisy. Pick $n$ by a small search. Use [TD(λ)](/td-lambda/) when you want the same trade-off without an $n$-step delay or an $n$-step buffer. With replayed or off-policy data, the $n$-step target is biased toward the behavior policy unless it is corrected, so keep $n$ small there or use [Retrace](/retrace/).

## Pitfalls

- **Bootstrapping past the end.** If $\tau + n \ge T$, line L4 must not add $\gamma^n V(S_{\tau+n})$. The window then holds only $T - \tau$ rewards.
- **Forgetting the last updates.** In the online loop, the states of the last $n - 1$ steps are updated after the episode ends. A loop that stops at $t = T - 1$ skips them.
- **The wrong discount power.** The reward $R_i$ in the window gets $\gamma^{i - \tau - 1}$, and the bootstrap gets $\gamma^n$, not $\gamma^{n-1}$.
- **A stale bootstrap.** Line L4 must read $V(S_{\tau+n})$ at update time, after the earlier updates of the episode. Precomputing all targets at the start of the episode gives the offline variant, which is a different algorithm.

## Implementations

## History

Sutton (1988) placed one-step TD and the Widrow-Hoff (Monte Carlo) rule at the two ends of one family. Watkins (1989) discussed corrected $n$-step truncated returns in his thesis. Sutton and Barto give n-step TD its own chapter in the second edition and state the error reduction property as equation 7.3.

## References
