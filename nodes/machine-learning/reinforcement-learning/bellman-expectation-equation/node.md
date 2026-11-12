---
tag: MAY0T7
kind: concept
slug: bellman-expectation-equation
name: Bellman expectation equation
aliases:
- Bellman equation for a policy
- "Bellman equation for V^pi"
area: machine-learning/reinforcement-learning
level: intro
summary: "V^pi(s) = sum_a pi(a|s)[R(s,a) + gamma sum_s' P(s'|s,a) V^pi(s')]. A linear system with the unique solution (I - gamma P^pi)^(-1) R^pi."
prereqs: [state-value-function, action-value-function]
see_also: [bellman-optimality-equation, bellman-contraction, policy-evaluation, iterative-policy-evaluation, temporal-difference-learning, least-squares-td, policy-iteration, bellman-equation]
sources:
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: "Section 3.5 (equation 3.14, the Bellman equation for v_pi), Section 4.1 (iterative policy evaluation)"
  - book: isbn:9780471619772
    title: Martin L. Puterman, Markov Decision Processes, Discrete Stochastic Dynamic Programming, Wiley, 1994
    locator: "Section 6.1 (the policy evaluation equation and its matrix form)"
  - book: isbn:9781886529106
    title: Dimitri P. Bertsekas and John N. Tsitsiklis, Neuro-Dynamic Programming, Athena Scientific, 1996
    locator: "Chapter 2, Section 2.2"
---

The Bellman expectation equation says that the value of a state under a fixed [policy](/policy/) equals the expected reward of one step plus the discounted value of the next state. For a finite [MDP](/markov-decision-process/) it is a system of $|S|$ linear equations, and the [state value function](/state-value-function/) $V^\pi$ is its only solution. It is the equation that [policy evaluation](/policy-evaluation/) solves, by a direct solve, by iteration or from samples.

## In plain words

Think of the long term worth of a situation when you always act in the same fixed way. That worth splits into two parts: what you expect to get on the next step, and the worth of where you expect to be after that step, made a little smaller because it comes later. This split holds for every situation at once. So the worths of all situations are tied to each other by one set of simple balance rules, one rule per situation. Those rules have exactly one answer, and that answer is the true worth of each situation. You can find it by solving the rules directly, or by starting from any guess and applying the rules again and again. Each round makes the error smaller by the same fixed factor. Learning methods use the same rules with sampled steps in place of the expected step.

## The idea

Fix a finite MDP $(S, A, P, R, \gamma)$ with $0 \le \gamma < 1$ and a stationary policy $\pi$. Write $P^\pi(s, s') = \sum_a \pi(a \mid s) P(s' \mid s, a)$ and $R^\pi(s) = \sum_a \pi(a \mid s) R(s, a)$.

**The equations.** For every state $s$ and action $a$,

$$V^\pi(s) = \sum_a \pi(a \mid s)\left[R(s, a) + \gamma \sum_{s'} P(s' \mid s, a)\, V^\pi(s')\right],$$

$$Q^\pi(s, a) = R(s, a) + \gamma \sum_{s'} P(s' \mid s, a) \sum_{a'} \pi(a' \mid s')\, Q^\pi(s', a').$$

In matrix form the first one is $V^\pi = R^\pi + \gamma P^\pi V^\pi$, or $V^\pi = T^\pi V^\pi$ with the Bellman operator $T^\pi v = R^\pi + \gamma P^\pi v$.

**Derivation.** The [discounted return](/discounted-return/) satisfies $G_t = R_{t+1} + \gamma G_{t+1}$. Take the expectation given $S_t = s$:

$$V^\pi(s) = \mathbb{E}^\pi[R_{t+1} \mid S_t = s] + \gamma\, \mathbb{E}^\pi\left[\mathbb{E}^\pi[G_{t+1} \mid S_t, A_t, S_{t+1}] \,\middle|\, S_t = s\right]$$

by the tower rule. By the Markov property and the stationarity of $\pi$, the inner expectation depends only on $S_{t+1}$ and equals $V^\pi(S_{t+1})$. The first term is $R^\pi(s)$, and the law of $S_{t+1}$ given $S_t = s$ is row $s$ of $P^\pi$. This gives the equation for $V^\pi$. The $Q$ form follows in the same way with $A_t = a$ fixed.

**Unique solution.** The matrix $I - \gamma P^\pi$ is invertible and

$$V^\pi = (I - \gamma P^\pi)^{-1} R^\pi = \sum_{k=0}^{\infty} \gamma^k (P^\pi)^k R^\pi.$$

*Proof.* $P^\pi$ is a stochastic matrix, so its max norm $\|P^\pi\|_\infty$ (the max row sum) is 1, and $\|(\gamma P^\pi)^k\|_\infty \le \gamma^k$. So the Neumann series $\sum_k (\gamma P^\pi)^k$ converges absolutely. Let $N$ be its sum. Then $(I - \gamma P^\pi) N = \lim_K \left(I - (\gamma P^\pi)^{K+1}\right) = I$, and in the same way $N(I - \gamma P^\pi) = I$. So $I - \gamma P^\pi$ is invertible with inverse $N$, and the linear system has exactly one solution. $\blacksquare$

The series also shows that $(I - \gamma P^\pi)^{-1}$ has nonnegative entries and row sums $1/(1-\gamma)$. So $V^\pi$ is monotone in $R^\pi$, and $|V^\pi| \le \max|R^\pi|/(1-\gamma)$.

**Iteration.** $T^\pi$ is a $\gamma$-contraction in the max norm ([Bellman contraction](/bellman-contraction/)). So $v_{k+1} = T^\pi v_k$ converges to $V^\pi$ from any $v_0$, with $\|v_k - V^\pi\|_\infty \le \gamma^k \|v_0 - V^\pi\|_\infty$. From $v_0 = 0$, the iterate $v_k = \sum_{j<k} \gamma^j (P^\pi)^j R^\pi$ is the expected sum of the first $k$ discounted rewards. This is [iterative policy evaluation](/iterative-policy-evaluation/).

**Cost.** A direct solve costs $O(|S|^3)$ operations after $O(|S|^2|A|)$ to form $P^\pi$ and $R^\pi$. One sweep of iteration costs $O(|S|^2|A|)$, or less for sparse transitions. About $\log(1/\varepsilon) / (1-\gamma)$ sweeps reach a relative error of $\varepsilon$.

**From samples.** The equation says that $R_{t+1} + \gamma V^\pi(S_{t+1}) - V^\pi(S_t)$ has mean 0 given $S_t$. [Temporal difference learning](/temporal-difference-learning/) moves an estimate toward this zero by stochastic approximation. [Least-squares TD](/least-squares-td/) solves a projected version of the equation for a linear value function.

## Examples

Take the two-state example of the [MDP page](/markov-decision-process/) with $\gamma = 9/10$: in $s_1$, *stay* gives 1 and stays, *switch* gives 0 and moves to $s_2$ with probability 1/2; in $s_2$, *stay* gives 2 and stays with probability 3/4, *switch* gives 3 and moves to $s_1$.

- **The uniform policy, direct solve.** $P^\pi = \begin{pmatrix} 3/4 & 1/4 \\ 5/8 & 3/8 \end{pmatrix}$ and $R^\pi = (1/2, 5/2)$. The system is
  $$\tfrac{13}{40} V_1 - \tfrac{9}{40} V_2 = \tfrac12, \qquad -\tfrac{9}{16} V_1 + \tfrac{53}{80} V_2 = \tfrac52,$$
  with the solution $V^\pi = (715/71, 875/71)$. Check in $s_1$: $\frac12 + \frac{9}{10}\left(\frac34 \cdot \frac{715}{71} + \frac14 \cdot \frac{875}{71}\right) = \frac12 + \frac{9}{10} \cdot \frac{3020}{284} = \frac{715}{71}$.
- **The uniform policy, iteration.** From $v_0 = 0$: $v_1 = (1/2, 5/2)$, $v_2 = (7/5, 29/8)$, $v_3 = (3617/1600, 2887/640)$. Each $v_k$ equals the expected sum of the first $k$ discounted rewards, found by a sum over all paths of length $k$. With floats, the error after 10, 50 and 100 sweeps is about 3.74, 0.055 and 0.00028 in both states, below the bound $0.9^k \cdot 875/71$.
- **The $Q$ form.** The table $Q^\pi(s_1, \cdot) = (1429/142, 1431/142)$, $Q^\pi(s_2, \cdot) = (1787/142, 1713/142)$ is a fixed point of the $Q$ form of the equation.
- **No discount, a counterexample.** With $\gamma = 1$ and $P^\pi = I$, every $v$ with $v = R^\pi + v$ requires $R^\pi = 0$. If $R^\pi = 0$, every vector solves the equation. The discount, or a terminal state reached with probability 1 as in a [stochastic shortest path](/stochastic-shortest-path/) problem, is what makes the solution unique.

## Where it is used

- **Policy evaluation.** The evaluation step of [policy iteration](/policy-iteration/) solves this equation, exactly or by a few sweeps ([modified policy iteration](/modified-policy-iteration/)).
- **TD methods.** [Temporal difference learning](/temporal-difference-learning/), [SARSA](/sarsa/) and [TD($\lambda$)](/td-lambda/) use sampled versions of the equation, for $V^\pi$ or $Q^\pi$.
- **Linear function approximation.** [Least-squares TD](/least-squares-td/) and [gradient TD](/gradient-temporal-difference/) work with the projected Bellman equation.
- **Planning outside RL.** The same linear equation gives the expected discounted cost of a Markov chain with rewards. The [Bellman equation](/bellman-equation/) page of the planning area covers the optimality form for planning.

## References
