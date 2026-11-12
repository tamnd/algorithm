---
tag: E1K7NT
kind: definition
slug: discount-factor
name: Discount factor
aliases:
- discount rate
area: machine-learning/reinforcement-learning
level: intro
summary: "The number gamma in [0, 1) that weights a reward k steps ahead by gamma^k. It keeps infinite sums finite and is a probability of going on."
prereqs: [markov-decision-process]
see_also: [discounted-return, state-value-function, bellman-contraction, value-iteration, stochastic-shortest-path, geometric-distribution]
sources:
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: "Section 3.3 (returns and episodes, the discount rate), Section 3.4 (episodic and continuing tasks)"
  - book: isbn:9780471619772
    title: Martin L. Puterman, Markov Decision Processes, Discrete Stochastic Dynamic Programming, Wiley, 1994
    locator: "Section 5.3 (the discounted criterion, and its form as a total reward with a geometric random horizon), Chapter 8 (the limit of discounted values as the discount factor tends to 1)"
  - paper: "M. Kearns and S. Singh, Near-optimal reinforcement learning in polynomial time, Machine Learning 49(2-3):209-232, 2002"
    title: Kearns and Singh 2002
    locator: the epsilon-horizon time of a discounted MDP
---

The discount factor $\gamma$ of a [Markov decision process](/markov-decision-process/) is a number in $[0, 1)$ that weights a reward received $k$ steps in the future by $\gamma^k$. It makes the infinite sum of rewards finite, it says how much the agent cares about the far future, and it equals the probability that the process goes on for one more step in an equivalent model with random termination. Its size sets the effective horizon, about $1/(1-\gamma)$ steps, and the speed of [value iteration](/value-iteration/).

## Definition

Let $R_1, R_2, \ldots$ be the rewards of an MDP, with $|R_t| \le R_{\max}$. For a discount factor $\gamma$ with $0 \le \gamma < 1$, the [discounted return](/discounted-return/) from time $t$ is

$$G_t = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}, \qquad |G_t| \le \sum_{k=0}^{\infty} \gamma^k R_{\max} = \frac{R_{\max}}{1-\gamma}.$$

In an episodic task, where each episode ends in a terminal state, $\gamma = 1$ is also allowed. The value $\gamma = 0$ makes the agent *myopic*: it maximizes only the next reward. Four views of $\gamma$ are in use, and each one is exact.

**1. A weight that keeps sums finite.** With bounded rewards, the series converges absolutely for every $\gamma < 1$, so every policy has a finite value. The same $\gamma$ is the contraction modulus of the Bellman operators in the max norm ([Bellman contraction](/bellman-contraction/)), which gives unique value functions and the geometric convergence of value iteration.

**2. An interest rate.** If money earns interest at a rate $\rho > 0$ per step, a payment one step later is worth $1/(1+\rho)$ of the same payment now. With $\gamma = 1/(1+\rho)$, the discounted return is the present value of the stream of rewards. This is the economic reading of the discounted criterion.

**3. A probability of going on.** Let $\tau \ge 1$ be a random stopping time, independent of the states, actions and rewards, with $\Pr(\tau > t) = \gamma^t$ for $t = 0, 1, 2, \ldots$. So $\tau$ has the [geometric distribution](/geometric-distribution/) with success probability $1 - \gamma$: after each step the process stops with probability $1 - \gamma$. Then

$$\mathbb{E}\left[\sum_{t=0}^{\tau - 1} R_{t+1}\right] = \mathbb{E}\left[\sum_{t=0}^{\infty} \gamma^t R_{t+1}\right].$$

*Proof.* Write the left sum as $\sum_{t \ge 0} \mathbf{1}[\tau > t] R_{t+1}$. Since $\sum_t \mathbb{E}[\mathbf{1}[\tau > t] |R_{t+1}|] \le R_{\max} \sum_t \gamma^t < \infty$, the expectation and the sum can be swapped (dominated convergence). By independence, $\mathbb{E}[\mathbf{1}[\tau > t] R_{t+1}] = \Pr(\tau > t)\, \mathbb{E}[R_{t+1}] = \gamma^t\, \mathbb{E}[R_{t+1}]$. $\blacksquare$

So a discounted MDP is an undiscounted MDP with one extra absorbing state that each step reaches with probability $1 - \gamma$. This is a [stochastic shortest path](/stochastic-shortest-path/) problem whose goal is reached with probability 1. The expected number of steps is $\mathbb{E}[\tau] = 1/(1-\gamma)$.

**4. An effective horizon.** Since $\ln \gamma \le \gamma - 1$, we have $\gamma^H \le e^{-(1-\gamma)H}$. The rewards after step $H$ change the return by at most $\gamma^H R_{\max}/(1-\gamma)$, so

$$H \ge \frac{\ln(1/\varepsilon)}{1-\gamma} \implies \gamma^H \le \varepsilon,$$

and a planner that looks $H$ steps ahead loses at most $\varepsilon R_{\max}/(1-\gamma)$. Kearns and Singh (2002) call such an $H$ the $\varepsilon$-horizon time. The rough rule "$\gamma$ looks about $1/(1-\gamma)$ steps ahead" comes from this bound and from $\mathbb{E}[\tau] = 1/(1-\gamma)$.

**The limit $\gamma \to 1$.** For a stationary policy in a finite MDP, $(1-\gamma) V^\pi_\gamma(s)$ tends to the average reward $g^\pi(s)$ as $\gamma \to 1$ (Puterman, Chapter 8). So the average reward criterion is the limit of the discounted one, scaled by $1 - \gamma$.

## Examples and non-examples

- **Constant reward.** With $R_t = 1$ for all $t$, the return is $1/(1-\gamma)$: 2 for $\gamma = 1/2$, 10 for $\gamma = 0.9$ and 100 for $\gamma = 0.99$.
- **Effective horizons.** The least $H$ with $\gamma^H \le 0.01$ is 44 for $\gamma = 0.9$ and 459 for $\gamma = 0.99$. The bound $\ln(100)/(1-\gamma)$ gives 47 and 461. A reward 100 steps ahead keeps the weight $0.99^{100} \approx 0.366$.
- **The optimal policy depends on $\gamma$.** In the two-state example of the [MDP page](/markov-decision-process/), the deterministic optimal policy (action in $s_1$, action in $s_2$) is (stay, switch) for $\gamma < 2/3$, (stay, stay) for $2/3 < \gamma < 4/5$, and (switch, stay) for $\gamma > 4/5$. At $\gamma = 2/3$ the two first policies tie with values $(3, 5)$, and at $\gamma = 4/5$ the two last tie with values $(5, 15/2)$. A myopic agent takes the reward 3 of switch in $s_2$; a patient one stays in $s_2$ to collect 2 again and again.
- **Random termination.** In the same example with $\gamma = 9/10$ and the policy (switch, stay), let the process stop with probability 1/10 after each step and add up the rewards with no discount. The expected total from $s_1$ is $360/31$, the discounted value of that policy.
- **Myopic agent.** With $\gamma = 0$ the value is $V^\pi(s) = R^\pi(s)$, and a greedy one-step choice is optimal. A [multi-armed bandit](/multi-armed-bandit/) agent usually works in this way.
- **Non-example: $\gamma = 1$ in a continuing task.** With reward 1 in each step and no end, $\sum_t R_{t+1}$ diverges, and all policies that keep the reward positive have the value $+\infty$. Use the average reward criterion instead.
- **Non-example: $\gamma > 1$ or $\gamma < 0$.** A factor above 1 gives more weight to the far future and the sums diverge for a constant reward. A negative factor makes the weights change sign. Neither is a discount factor.

## Related definitions

- [Discounted return](/discounted-return/): the weighted sum that $\gamma$ defines.
- [State value function](/state-value-function/): the expected discounted return of a policy.
- [Bellman contraction](/bellman-contraction/): $\gamma$ is the contraction modulus of the Bellman operators.
- [Value iteration](/value-iteration/): needs about $\log(1/\varepsilon)/(1-\gamma)$ sweeps for accuracy $\varepsilon$.
- [Stochastic shortest path](/stochastic-shortest-path/): the undiscounted model that contains discounting as random termination.
- [Generalized advantage estimation](/generalized-advantage-estimation/): uses $\gamma$ together with a second factor $\lambda$.

## References
