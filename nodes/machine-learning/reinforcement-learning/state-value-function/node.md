---
tag: ZWKZEG
kind: definition
slug: state-value-function
name: State value function
aliases:
- V-function
- state-value function
area: machine-learning/reinforcement-learning
level: intro
summary: "V^pi(s): the expected discounted return from state s when the agent follows the policy pi. V*(s) is the largest such value over all policies."
prereqs: [policy, discounted-return]
see_also: [action-value-function, advantage-function, bellman-expectation-equation, bellman-optimality-equation, policy-evaluation, monte-carlo-policy-evaluation, temporal-difference-learning, value-function-approximation]
sources:
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: "Section 3.5 (policies and value functions), Section 3.6 (optimal value functions)"
  - book: isbn:9780471619772
    title: Martin L. Puterman, Markov Decision Processes, Discrete Stochastic Dynamic Programming, Wiley, 1994
    locator: "Section 6.1 (the discounted value of a policy and its matrix form), Theorem 6.2.10"
  - book: isbn:9781608454921
    title: Csaba Szepesvári, Algorithms for Reinforcement Learning, Morgan and Claypool, 2010
    locator: "Chapter 2 (value functions of Markov decision processes)"
---

The state value function $V^\pi$ of a [policy](/policy/) $\pi$ in a [Markov decision process](/markov-decision-process/) gives, for each state $s$, the expected [discounted return](/discounted-return/) of an agent that starts in $s$ and then follows $\pi$. The optimal state value function $V^*$ gives the largest such value over all policies. For a stationary policy in a finite MDP, $V^\pi$ is the unique solution of a linear system, the [Bellman expectation equation](/bellman-expectation-equation/).

## Definition

Let $(S, A, P, R, \gamma)$ be a finite MDP with $0 \le \gamma < 1$ and $|R(s, a)| \le R_{\max}$, and let $\pi$ be a stationary policy. The state value function of $\pi$ is the map $V^\pi : S \to \mathbb{R}$,

$$V^\pi(s) = \mathbb{E}^\pi\left[G_t \mid S_t = s\right] = \mathbb{E}^\pi\left[\sum_{k=0}^{\infty} \gamma^k R_{t+k+1} \,\middle|\, S_t = s\right].$$

The right side does not depend on $t$, because the policy and the dynamics are the same at each step. For a policy that is not stationary, $V^\pi(s)$ is defined with $t = 0$ only. The optimal state value function is

$$V^*(s) = \sup_\pi V^\pi(s),$$

where the supremum is over all policies, history dependent and randomized ones included. In a finite MDP one deterministic stationary policy attains $V^*(s)$ in every state at once ([MDP](/markov-decision-process/), Puterman Theorem 6.2.10).

**The matrix form.** Write $P^\pi(s, s') = \sum_a \pi(a \mid s) P(s' \mid s, a)$ and $R^\pi(s) = \sum_a \pi(a \mid s) R(s, a)$. Then

$$V^\pi = \sum_{k=0}^{\infty} \gamma^k (P^\pi)^k R^\pi = (I - \gamma P^\pi)^{-1} R^\pi.$$

*Proof.* From $S_0 = s$, the law of $S_k$ is row $s$ of $(P^\pi)^k$, by the Markov property. Given $S_k = s'$, the expected reward $R_{k+1}$ is $R^\pi(s')$. So $\mathbb{E}^\pi[R_{k+1} \mid S_0 = s] = ((P^\pi)^k R^\pi)(s)$. The sum over $k$ and the expectation can be swapped, because $\sum_k \gamma^k R_{\max} < \infty$. The series $\sum_k (\gamma P^\pi)^k$ converges to $(I - \gamma P^\pi)^{-1}$, because each power of the stochastic matrix $P^\pi$ has max row sum 1, so $\|(\gamma P^\pi)^k\|_\infty = \gamma^k$. $\blacksquare$

**Basic properties.**

- **Bounded:** $|V^\pi(s)| \le R_{\max}/(1-\gamma)$, since $|G_t| \le R_{\max}/(1-\gamma)$.
- **Linear in the reward:** for a fixed $\pi$, $V^\pi$ is a linear function of $R^\pi$ with nonnegative coefficients. So a larger reward in each state gives a larger value in each state.
- **Value of a start distribution:** from an initial distribution $\mu$ the expected return is $\sum_s \mu(s) V^\pi(s)$.
- **Cost:** for $|S|$ states and $|A|$ actions, the exact value costs $O(|S|^2|A|)$ operations to form $P^\pi$ and $R^\pi$ and $O(|S|^3)$ for the solve. [Iterative policy evaluation](/iterative-policy-evaluation/) costs $O(|S|^2 |A|)$ per sweep instead.

## Examples and non-examples

Take the two-state example of the [MDP page](/markov-decision-process/) with $\gamma = 9/10$: in $s_1$, *stay* gives 1 and stays, *switch* gives 0 and moves to $s_2$ with probability 1/2; in $s_2$, *stay* gives 2 and stays with probability 3/4, *switch* gives 3 and moves to $s_1$.

- **The uniform policy.** With probability 1/2 for each action, $P^\pi = \begin{pmatrix} 3/4 & 1/4 \\ 5/8 & 3/8 \end{pmatrix}$ and $R^\pi = (1/2, 5/2)$. The system $(I - \frac{9}{10} P^\pi) V = R^\pi$ has the solution $V^\pi = (715/71, 875/71) \approx (10.07, 12.32)$.
- **Sampled returns.** 3000 returns of 120 steps from $s_1$ under this policy, drawn with Python's `random.Random(2018)`, have the mean 10.02 and a standard error of 0.03. The exact value is $715/71 \approx 10.07$; the 120 step cut changes it by less than $10^{-4}$.
- **The optimal values.** $V^* = (360/31, 440/31) \approx (11.61, 14.19)$, the value of the policy (switch, stay). It is at least $V^\pi$ in both states for every policy $\pi$, as the bound $V^\pi \le V^*$ requires.
- **No discount.** With $\gamma = 0$ the value is the expected next reward, $V^\pi = R^\pi = (1/2, 5/2)$ for the uniform policy.
- **Non-example: a finite horizon value.** The expected sum of the next $H$ rewards depends on $H$, so the optimal finite horizon value is a function of the state and the number of steps left, not of the state alone.
- **Non-example: one return.** $G_t$ is a random variable; $V^\pi(s)$ is its mean. A single episode gives a sample, not the value.
- **Non-example: a value of an observation.** In a [POMDP](/pomdp/) the expected return given only the current observation depends on the past, so it is not a function of the observation. The state value function there is defined on beliefs.
- **Non-example: the action value.** $V^\pi(s)$ averages over the action of $\pi$ in $s$. The [action value](/action-value-function/) $Q^\pi(s, a)$ fixes the first action.

## Related definitions

- [Action value function](/action-value-function/) $Q^\pi(s, a)$, with $V^\pi(s) = \sum_a \pi(a \mid s) Q^\pi(s, a)$.
- [Advantage function](/advantage-function/) $A^\pi = Q^\pi - V^\pi$.
- [Bellman expectation equation](/bellman-expectation-equation/) for $V^\pi$ and [Bellman optimality equation](/bellman-optimality-equation/) for $V^*$.
- [Policy evaluation](/policy-evaluation/), [Monte Carlo policy evaluation](/monte-carlo-policy-evaluation/) and [temporal difference learning](/temporal-difference-learning/): ways to compute or estimate $V^\pi$.
- [Value function approximation](/value-function-approximation/): $V^\pi$ by a parametric function when the state space is large.

## References
