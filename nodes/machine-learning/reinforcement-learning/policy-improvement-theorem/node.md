---
tag: ZMPCA4
kind: theorem
slug: policy-improvement-theorem
name: Policy improvement theorem
aliases:
- policy improvement
- policy improvement lemma
area: machine-learning/reinforcement-learning
level: core
summary: "If a policy pi' does at least as well as pi for one step in every state, judged by Q^pi, then V^pi' >= V^pi everywhere, strictly where the one-step gain is positive."
prereqs: [policy, state-value-function, action-value-function, bellman-expectation-equation]
see_also: [policy-iteration, modified-policy-iteration, mdp-planning, advantage-function, monte-carlo-control, sarsa, actor-critic, bellman-optimality-equation]
sources:
  - paper: "Ronald A. Howard, Dynamic Programming and Markov Processes, Technology Press of MIT and John Wiley, 1960"
    locator: the policy improvement routine and the proof that it improves the values
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: Section 4.2 (policy improvement, the telescoping proof and the extension to stochastic policies)
  - book: isbn:9780471619772
    title: Martin L. Puterman, Markov Decision Processes, Discrete Stochastic Dynamic Programming, Wiley, 1994
    locator: Section 6.4 (policy iteration; the monotonicity of the values of successive policies)
---

The policy improvement theorem compares two policies of a discounted [Markov decision process](/markov-decision-process/). If, in every state, taking the action of a new policy $\pi'$ once and then following $\pi$ is at least as good as following $\pi$ from the start, then following $\pi'$ always is at least as good as $\pi$ in every state. The comparison uses only the [action value function](/action-value-function/) $Q^\pi$ of the old policy, which is cheap to compute. The theorem is the reason why the greedy step of [policy iteration](/policy-iteration/) never makes a policy worse, and why a policy that cannot be improved this way is optimal.

## Statement

Let $(S, A, P, R, \gamma)$ be an MDP with finitely many states and actions and $0 \le \gamma < 1$. For a deterministic stationary policy $\pi$ let $V^\pi$ be its [state value function](/state-value-function/) and

$$Q^\pi(s, a) = R(s, a) + \gamma \sum_{s'} P(s' \mid s, a)\, V^\pi(s').$$

**Theorem.** Let $\pi$ and $\pi'$ be deterministic stationary policies, and let $g(s) = Q^\pi(s, \pi'(s)) - V^\pi(s)$. If $g(s) \ge 0$ for every state $s$, then

$$V^{\pi'}(s) \ge V^\pi(s) + g(s) \ge V^\pi(s) \quad \text{for every state } s.$$

In particular, if $g(s) > 0$ for some state $s$, then $V^{\pi'}(s) > V^\pi(s)$.

**Exact form.** For any two policies, with no condition on $g$, the difference $d = V^{\pi'} - V^\pi$ is

$$d = (I - \gamma P_{\pi'})^{-1} g = \sum_{k \ge 0} \gamma^k P_{\pi'}^k\, g,$$

where $P_{\pi'}(s, s') = P(s' \mid s, \pi'(s))$. So the effect of a policy change is the one-step gain $g$, summed along the trajectories of the new policy with discount.

**Corollary (greedy improvement).** If $\pi'$ is greedy for $V^\pi$, that is $\pi'(s)$ maximizes $Q^\pi(s, \cdot)$ in each state, then $V^{\pi'} \ge V^\pi$. If moreover $\pi'(s) = \pi(s)$ whenever $\pi(s)$ is a maximizer, then $V^{\pi'}(s) > V^\pi(s)$ in each state where $\pi'$ differs from $\pi$, and $\pi' = \pi$ if and only if $\pi$ is optimal.

The theorem also holds when $\pi'$ is stochastic, with $g(s) = \sum_a \pi'(a \mid s)Q^\pi(s, a) - V^\pi(s)$ (Sutton and Barto, Section 4.2).

## In plain words

You have a way of acting, and you know how good each action is if you take it once and then go back to your old way. Now make a new way of acting: in each place, pick an action that is at least as good as your old one by this measure.

The theorem says that the new way is at least as good as the old one everywhere, even though it changes your actions in all later steps too, not only in the first one. If the new choice was strictly better in some place, then the new way is strictly better in that place.

So you can improve a plan by looking just one step ahead in each place. When no place can be improved like this, the plan is already the best one.

## Proof

Write $\mathbb{E}_{\pi'}$ for the expectation over trajectories that start in state $s$ and follow $\pi'$, and $T^{\pi'}$ for the backup $(T^{\pi'}U)(s) = R(s, \pi'(s)) + \gamma \sum_{s'} P(s' \mid s, \pi'(s))\, U(s')$. The premise $g \ge 0$ reads $V^\pi \le T^{\pi'}V^\pi$, because $(T^{\pi'}V^\pi)(s) = Q^\pi(s, \pi'(s))$.

**The telescoping argument.** Use the premise once in each step, and expand $Q^\pi$ by its definition:

$$
\begin{aligned}
V^\pi(s) &\le Q^\pi(s, \pi'(s)) = \mathbb{E}_{\pi'}\big[r_1 + \gamma V^\pi(s_1)\big] \\
&\le \mathbb{E}_{\pi'}\big[r_1 + \gamma Q^\pi(s_1, \pi'(s_1))\big] = \mathbb{E}_{\pi'}\big[r_1 + \gamma r_2 + \gamma^2 V^\pi(s_2)\big] \\
&\;\;\vdots \\
&\le \mathbb{E}_{\pi'}\Big[\sum_{t=1}^{k} \gamma^{t-1} r_t + \gamma^k V^\pi(s_k)\Big].
\end{aligned}
$$

In the second line we used $V^\pi(s_1) \le Q^\pi(s_1, \pi'(s_1))$ inside the expectation, and the fact that under $\pi'$ the next reward and state from $s_1$ have the distribution that $Q^\pi(s_1, \pi'(s_1))$ averages over. In operator form the chain is $V^\pi \le T^{\pi'}V^\pi \le (T^{\pi'})^2 V^\pi \le \cdots \le (T^{\pi'})^k V^\pi$, where each step applies the monotone map $T^{\pi'}$ to the previous inequality.

Now let $k \to \infty$. The rewards are bounded by $R_{\max} = \max_{s, a}|R(s, a)|$, so the sum converges to $V^{\pi'}(s)$, and the remainder satisfies $|\gamma^k \mathbb{E}_{\pi'}[V^\pi(s_k)]| \le \gamma^k \max_{s'} |V^\pi(s')| \to 0$. This gives $V^\pi(s) \le V^{\pi'}(s)$ for every $s$.

**The exact form and strictness.** By the [Bellman expectation equation](/bellman-expectation-equation/), $V^{\pi'} = r_{\pi'} + \gamma P_{\pi'}V^{\pi'}$, and by definition $T^{\pi'}V^\pi = r_{\pi'} + \gamma P_{\pi'}V^\pi = V^\pi + g$. Subtract:

$$V^{\pi'} - V^\pi - g = \gamma P_{\pi'}\big(V^{\pi'} - V^\pi\big), \qquad \text{so} \qquad (I - \gamma P_{\pi'})\,d = g.$$

The matrix $\gamma P_{\pi'}$ has nonnegative entries and row sums $\gamma < 1$, so the series $\sum_k \gamma^k P_{\pi'}^k$ converges to $(I - \gamma P_{\pi'})^{-1}$, and $d = \sum_{k \ge 0}\gamma^k P_{\pi'}^k g$. If $g \ge 0$, every term is nonnegative, and the term $k = 0$ is $g$, so $d \ge g \ge 0$. At a state with $g(s) > 0$ this gives $d(s) \ge g(s) > 0$.

**The corollary.** If $\pi'$ is greedy for $V^\pi$, then $Q^\pi(s, \pi'(s)) = \max_a Q^\pi(s, a) \ge Q^\pi(s, \pi(s)) = V^\pi(s)$, so $g \ge 0$ and the theorem applies. With the tie rule, a changed state has $\pi(s)$ not a maximizer, so $g(s) > 0$ and $V^{\pi'}(s) > V^\pi(s)$. If $\pi' = \pi$, then $\max_a Q^\pi(s, a) = V^\pi(s)$ in every state, which is the [Bellman optimality equation](/bellman-optimality-equation/), so $V^\pi = V^*$ by the uniqueness of its solution ([Bellman contraction](/bellman-contraction/)). Conversely, if $\pi$ is optimal and some state changed, then $V^{\pi'}(s) > V^\pi(s) = V^*(s)$, which is impossible. $\blacksquare$

## Consequences

- **Policy iteration is correct.** Each greedy step gives a policy that is strictly better in some state and no worse in any, so no policy repeats, and [policy iteration](/policy-iteration/) stops with an optimal policy after finitely many steps. The step is:

```pseudo id=main
IMPROVE(S, A, P, R, γ, π)
L1  V ← V^π                                   ▷ policy evaluation
L2  for each state s do
L3      Q(s, a) ← R(s, a) + γ Σ_{s′} P(s′ | s, a) V(s′) for each action a
L4      π′(s) ← π(s) if π(s) maximizes Q(s, ·), else an action that maximizes Q(s, ·)
L5  return π′
```

- **A test for optimality.** A policy is optimal if and only if no state has an action with a positive [advantage](/advantage-function/) $Q^\pi(s, a) - V^\pi(s)$.
- **Improvement in any subset of states.** Changing the action only in the states where the advantage is positive, and keeping the old action elsewhere, also improves the policy. This allows asynchronous and single-state improvement, as in simple policy iteration and in the simplex method on the [LP for MDPs](/linear-programming-for-mdps/).
- **Generalized policy iteration.** Methods such as [Monte Carlo control](/monte-carlo-control/), [SARSA](/sarsa/) and [actor-critic](/actor-critic/) alternate an estimate of $Q^\pi$ with a step toward the greedy policy. The theorem explains why this pattern makes progress when the estimates are accurate.
- **The size of the gain.** The exact form shows that the improvement is at least the one-step gain, and is larger when the new policy visits states with positive gain again and again. With $d_{\pi'}$, the discounted state visit distribution of $\pi'$ from a start distribution $\mu$, it gives $\mu^\top(V^{\pi'} - V^\pi) = \frac{1}{1-\gamma}\,\mathbb{E}_{s \sim d_{\pi'}}[g(s)]$, the performance difference identity that conservative policy iteration and [TRPO](/trpo/) build on.

## Tightness

- **The premise is needed in every state.** If the gain is positive in one state but negative in another, the new policy can be worse in some states. The exact form shows that a negative gain spreads backward to every state that reaches it.
- **The bound $d \ge g$ is tight.** If the changed states are never visited again under $\pi'$, then $d(s) = g(s)$ at those states.
- **The discount matters.** The theorem can fail with $\gamma = 1$. Take a state with two actions: exit, which pays 1 and ends the episode, and stay, which pays 0 and returns to the same state. For $\pi$ = exit, $V^\pi = 1$ and $Q^\pi(\text{stay}) = 0 + V^\pi = 1 \ge V^\pi$, so the premise holds for $\pi'$ = stay. But $\pi'$ never ends and collects 0. The telescoping proof breaks because the remainder $\gamma^k V^\pi(s_k) = 1$ does not go to 0. For stochastic shortest path problems the theorem holds when $\pi'$ is proper, that is, when it ends with probability 1.
- **Exact values are needed.** If $Q^\pi$ is only estimated, a greedy step can make the policy worse. Approximate policy iteration only guarantees bounds that grow with the estimation error and with $1/(1-\gamma)$.

The tests check the theorem with exact rational arithmetic on 600 random MDPs with up to 4 states and 3 actions: every premise-satisfying $\pi'$ has $d \ge g \ge 0$ and $(I - \gamma P_{\pi'})d = g$ exactly, the reverse premise $g \le 0$ gives $d \le 0$, and the greedy step leaves a policy unchanged exactly when a brute force search over all deterministic policies says it is optimal.

## History

Bellman's 1957 book Dynamic Programming already used approximation in policy space. Howard (1960) gave the policy improvement routine as one half of policy iteration and proved that it improves the values. Puterman's 1994 book proves the monotonicity of policy iteration in this form. Sutton and Barto present the telescoping proof and name the result the policy improvement theorem in Section 4.2, and it is the basis of their generalized policy iteration. Kakade and Langford (2002) stated the exact form as the performance difference lemma and used it for conservative policy iteration.

## References
