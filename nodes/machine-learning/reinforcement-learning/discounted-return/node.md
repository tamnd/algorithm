---
tag: HDFR24
kind: definition
slug: discounted-return
name: Discounted return
aliases:
- cumulative discounted reward
area: machine-learning/reinforcement-learning
level: intro
summary: "The random sum G_t of the rewards after time t, each weighted by a power of the discount factor. It obeys G_t = R_(t+1) + gamma G_(t+1)."
prereqs: [discount-factor, reward-function]
see_also: [state-value-function, monte-carlo-policy-evaluation, n-step-td, td-lambda, td-error, reinforce]
sources:
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: "Section 3.3 (returns and episodes, the recursion of the return), Section 3.4 (one notation for episodic and continuing tasks), Section 7.1 (n-step returns), Section 13.3 (REINFORCE with the factor gamma^t)"
  - book: isbn:9780471619772
    title: Martin L. Puterman, Markov Decision Processes, Discrete Stochastic Dynamic Programming, Wiley, 1994
    locator: "Section 5.3 (the expected total discounted reward)"
  - paper: "F. Pardo, A. Tavakoli, V. Levdik and P. Kormushev, Time limits in reinforcement learning, Proceedings of ICML 2018, PMLR 80"
    title: Pardo et al. 2018
    locator: a time limit is not a terminal state, and the return must be bootstrapped there
---

The discounted return $G_t$ is the sum of the rewards that an agent gets after time $t$, where the reward $k$ steps later has the weight $\gamma^k$ for a [discount factor](/discount-factor/) $\gamma$. It is a random variable: it depends on the random states, actions and rewards that follow. Its expectation under a policy is the [state value](/state-value-function/), and one sample of it is the target of [Monte Carlo policy evaluation](/monte-carlo-policy-evaluation/).

## Definition

Let $R_1, R_2, \ldots$ be the rewards of a trajectory of a [Markov decision process](/markov-decision-process/), where $R_{t+1}$ is the reward of the step from time $t$, and let $0 \le \gamma < 1$. The discounted return from time $t$ is

$$G_t = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1} = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \cdots.$$

In an episodic task that ends at a random time $T$, the sum stops: $G_t = \sum_{k=0}^{T-t-1} \gamma^k R_{t+k+1}$ and $G_T = 0$. Here $\gamma = 1$ is also allowed. One formula covers both cases if the terminal state is absorbing and gives reward 0 forever (Sutton and Barto, Section 3.4).

**The recursion.** Splitting off the first term gives

$$G_t = R_{t+1} + \gamma \sum_{k=0}^{\infty} \gamma^{k} R_{t+k+2} = R_{t+1} + \gamma G_{t+1}.$$

The split is valid because the series converges absolutely. This identity is the source of the [Bellman expectation equation](/bellman-expectation-equation/): take the conditional expectation of both sides given $S_t = s$. It also gives an $O(T)$ algorithm for all returns of an episode of $T$ steps: start with $G_T = 0$ and go backward.

**The bound.** If $|R_t| \le R_{\max}$ for all $t$, then

$$|G_t| \le \sum_{k=0}^{\infty} \gamma^k R_{\max} = \frac{R_{\max}}{1-\gamma},$$

with equality when every reward equals $R_{\max}$. If only the first $H$ rewards are added, the error is at most $\gamma^H R_{\max}/(1-\gamma)$, because the rest of the sum is $\gamma^H G_{t+H}$.

**Partial returns.** The $n$-step return $G_{t:t+n} = R_{t+1} + \gamma R_{t+2} + \cdots + \gamma^{n-1} R_{t+n} + \gamma^n V(S_{t+n})$ replaces the tail $\gamma^n G_{t+n}$ by an estimate $V(S_{t+n})$. It is the target of [n-step TD](/n-step-td/). The case $n = 1$ gives the TD target $R_{t+1} + \gamma V(S_{t+1})$ of the [TD error](/td-error/), and a geometric mixture of all $n$ gives the $\lambda$-return of [TD($\lambda$)](/td-lambda/). If $V(S_{t+n})$ is replaced by the true $G_{t+n}$, the $n$-step return equals $G_t$ for every $n$.

## Examples and non-examples

- **A short episode.** An episode has the rewards $R_1, R_2, R_3, R_4 = 1, 0, 2, 3$ and then ends; $\gamma = 1/2$. The backward pass gives:

| $t$ | $R_{t+1}$ | $G_t = R_{t+1} + \frac12 G_{t+1}$ |
|---|---|---|
| 4 | (end) | 0 |
| 3 | 3 | 3 |
| 2 | 2 | 2 + 3/2 = 7/2 |
| 1 | 0 | 0 + 7/4 = 7/4 |
| 0 | 1 | 1 + 7/8 = 15/8 |

The direct sum agrees: $G_0 = 1 + \frac12 \cdot 0 + \frac14 \cdot 2 + \frac18 \cdot 3 = 15/8$.

- **Constant reward.** With $R_t = 1$ forever, $G_t = 1/(1-\gamma)$ for each $t$, which is 10 for $\gamma = 0.9$. The first 200 rewards of this stream, summed with $\gamma = 1/2$, are within $2^{-199}$ of the limit 2.
- **A random return.** In the two-state example of the [MDP page](/markov-decision-process/) with $\gamma = 9/10$ and the policy (switch, stay), the return from $s_1$ depends on the coin flips of the transitions. Its expectation is the value $360/31 \approx 11.61$; single returns spread around this number.
- **Non-example: the value.** $V^\pi(s) = \mathbb{E}^\pi[G_t \mid S_t = s]$ is a number for each state, not a random variable. The return and the value are different objects, and the Monte Carlo method uses the first to estimate the second.
- **Non-example: discount from time 0.** The sum $\sum_{k} \gamma^{t+k} R_{t+k+1}$ discounts from the start of the episode. It equals $\gamma^t G_t$, not $G_t$. The two forms differ in policy gradient code: the [REINFORCE](/reinforce/) update for the discounted value of the start state has the factor $\gamma^t$ in front of $G_t$ (Sutton and Barto, Section 13.3), and code that drops the factor follows a different direction.
- **Non-example: a cut at a time limit.** If an episode stops only because of a time limit, the state at the cut is not terminal, and the true return goes on. Setting $G_T = 0$ there is a bias; the fix is to use $V(S_T)$ as the tail (Pardo et al. 2018).

## Related definitions

- [Discount factor](/discount-factor/): the weight $\gamma$.
- [Reward function](/reward-function/): the source of the terms $R_{t+1}$.
- [State value function](/state-value-function/) and [action value function](/action-value-function/): the expectations of $G_t$ given the state, or the state and the action.
- [Monte Carlo policy evaluation](/monte-carlo-policy-evaluation/): averages sampled returns.
- [n-step TD](/n-step-td/), [TD($\lambda$)](/td-lambda/) and [TD error](/td-error/): use partial returns with an estimated tail.

## References
