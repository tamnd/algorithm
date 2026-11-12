---
tag: 6A8RCZ
kind: concept
slug: td-error
name: Temporal-difference error
aliases:
- TD error
- one-step TD error
area: machine-learning/reinforcement-learning
level: intro
summary: "The TD error is R_(t+1) + gamma V(S_(t+1)) - V(S_t). Its mean is the Bellman residual, and with V fixed the discounted TD errors of an episode sum to G_t - V(S_t)."
prereqs: [state-value-function, discounted-return, bellman-expectation-equation]
see_also: [temporal-difference-learning, n-step-td, td-lambda, eligibility-traces, sarsa, q-learning, actor-critic, generalized-advantage-estimation]
sources:
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: Section 6.1 (the TD error and the Monte Carlo error as a sum of TD errors), Section 7.1 (n-step returns) and Section 12.1 to 12.2 (the lambda-return and TD(lambda))
  - paper: doi:10.1007/BF00115009
    title: "Richard S. Sutton, Learning to predict by the methods of temporal differences, Machine Learning 3(1), 1988, pages 9 to 44"
    locator: the section on the equivalence of the Widrow-Hoff (Monte Carlo) update and the sum of temporal differences
  - paper: "Wolfram Schultz, Peter Dayan and P. Read Montague, A neural substrate of prediction and reward, Science 275(5306), 1997, pages 1593 to 1599"
    locator: the comparison of dopamine neuron responses with the TD error
---

The temporal-difference (TD) error at time $t$ is $\delta_t = R_{t+1} + \gamma V(S_{t+1}) - V(S_t)$: the one-step target minus the current estimate of the [state value](/state-value-function/). It is the quantity that [TD learning](/temporal-difference-learning/) multiplies by the step size. Its conditional mean is the Bellman residual $(T^\pi V - V)(S_t)$, which is zero for the true values, and when $V$ is held fixed the discounted TD errors of an episode add up exactly to the Monte Carlo error $G_t - V(S_t)$. These two facts tie TD methods to dynamic programming on one side and to [Monte Carlo evaluation](/monte-carlo-policy-evaluation/) on the other.

## In plain words

At each step you have a guess of what the rest of the episode is worth. One step later you know the reward you just got, and you have a new guess for the rest. The reward plus the new guess, minus the old guess, is the TD error. It says how much your opinion changed in one step: positive means the step went better than you expected, negative means worse.

If your guesses are right, these surprises average to zero. If you add up all the surprises from now to the end of the episode, with the right discount, you get exactly how far your first guess was from what really happened.

## The idea

**Definition.** Fix a table $V$ of state values, with $V(\text{terminal}) = 0$, and a discount $0 \le \gamma \le 1$. Along a trajectory $S_0, R_1, S_1, R_2, \ldots$ the TD error is

$$\delta_t = R_{t+1} + \gamma V(S_{t+1}) - V(S_t).$$

When $V$ changes over time, $\delta_t$ uses the table $V_t$ of time $t$ in both terms. For action values the same idea gives three errors, one for each control method:

- [SARSA](/sarsa/): $R_{t+1} + \gamma Q(S_{t+1}, A_{t+1}) - Q(S_t, A_t)$,
- [Expected SARSA](/expected-sarsa/): $R_{t+1} + \gamma \sum_a \pi(a \mid S_{t+1}) Q(S_{t+1}, a) - Q(S_t, A_t)$,
- [Q-learning](/q-learning/): $R_{t+1} + \gamma \max_a Q(S_{t+1}, a) - Q(S_t, A_t)$.

**Property 1 (the mean is the Bellman residual).** For a fixed $V$ and a fixed policy $\pi$, the Markov property gives

$$\mathbb{E}_\pi[\delta_t \mid S_t = s] = r^\pi(s) + \gamma \sum_{s'} P^\pi(s' \mid s) V(s') - V(s) = (T^\pi V)(s) - V(s).$$

This expected TD error is often called the *Bellman error* or Bellman residual of $V$. It is zero in every state exactly when $V = V^\pi$, by the [Bellman expectation equation](/bellman-expectation-equation/) and the [contraction](/bellman-contraction/) of $T^\pi$ for $\gamma < 1$. The TD error of one sample is not zero even at $V = V^\pi$; only its mean is.

**Property 2 (the telescoping sum).** Let an episode end at time $T$, and hold $V$ fixed. Then for each $t < T$,

$$G_t - V(S_t) = \sum_{k=t}^{T-1} \gamma^{k-t} \delta_k .$$

*Proof.* The right side is $\sum_{k=t}^{T-1} \gamma^{k-t} R_{k+1} + \sum_{k=t}^{T-1} \big(\gamma^{k-t+1} V(S_{k+1}) - \gamma^{k-t} V(S_k)\big)$. The first sum is $G_t$. The second sum telescopes to $\gamma^{T-t} V(S_T) - V(S_t) = -V(S_t)$, because $V(S_T) = 0$ for the terminal state. $\square$

The same argument, stopped after $n$ terms, gives the error of the [n-step return](/n-step-td/): $G_{t:t+n} - V(S_t) = \sum_{k=t}^{t+n-1} \gamma^{k-t} \delta_k$, where $G_{t:t+n} = R_{t+1} + \cdots + \gamma^{n-1} R_{t+n} + \gamma^n V(S_{t+n})$. Mixing these with weights $(1-\lambda)\lambda^{n-1}$ gives the error of the λ-return, $G^\lambda_t - V(S_t) = \sum_{k=t}^{T-1} (\gamma\lambda)^{k-t} \delta_k$, which is the reason why [TD(λ)](/td-lambda/) with [eligibility traces](/eligibility-traces/) reproduces the λ-return update. If $V$ changes during the episode, as in online TD(0), the identities hold only up to the changes of $V$.

**Property 3 (TD errors of the true values are martingale differences).** Let $V = V^\pi$ and let $\mathcal{F}_t$ be the history up to $S_t$. Then $\mathbb{E}[\delta_t \mid \mathcal{F}_t] = 0$ by Property 1. For $j < k$, $\delta_j$ is known at time $k$, so $\mathbb{E}[\delta_j \delta_k] = \mathbb{E}[\delta_j\, \mathbb{E}[\delta_k \mid \mathcal{F}_k]] = 0$. With Property 2 this splits the variance of the return into one term per step:

$$\mathrm{Var}\big[G_t \mid S_t = s\big] = \sum_{k \ge t} \gamma^{2(k-t)}\, \mathbb{E}\big[\delta_k^2 \, \mathbf{1}\{k < T\} \mid S_t = s\big],$$

for bounded rewards and episodes whose length has a finite second moment. Each step adds its own noise, which is why the variance of a Monte Carlo return grows with the length of the episode, while a one-step TD target carries the noise of one step only.

## Examples

**A short episode.** Let $\gamma = 1/2$, $V(a) = 1$, $V(b) = 2$, and the episode $a, R_1 = 1, b, R_2 = 0, a, R_3 = 2$, then terminal. The TD errors are

$$\delta_0 = 1 + \tfrac12 \cdot 2 - 1 = 1, \qquad \delta_1 = 0 + \tfrac12 \cdot 1 - 2 = -\tfrac32, \qquad \delta_2 = 2 + 0 - 1 = 1.$$

The return from time 0 is $G_0 = 1 + 0 + \tfrac14 \cdot 2 = \tfrac32$, so $G_0 - V(a) = \tfrac12$, and $\delta_0 + \tfrac12 \delta_1 + \tfrac14 \delta_2 = 1 - \tfrac34 + \tfrac14 = \tfrac12$. From time 1, $G_1 - V(b) = 1 - 2 = -1 = \delta_1 + \tfrac12 \delta_2$. The identities of Property 2 also hold exactly, in rational arithmetic, on 2000 random episodes of up to 7 steps over 3 states, for all $t$ and all $n$.

**The random walk.** In the five-state random walk of Sutton and Barto (Example 6.2) with $V = 1/2$ everywhere, all TD errors of an episode are 0 except the last one, which is $+1/2$ or $-1/2$. The true values $V^\pi(s) = s/6$ give TD errors $\pm 1/6$ inside the walk, with mean 0 in each state, as Property 1 says.

**Non-example.** The difference $G_t - V(S_t)$ itself is not a TD error: it is the Monte Carlo error, a sum of TD errors. The advantage $Q(s, a) - V(s)$ is also not a TD error, but for the true $V^\pi$ the TD error is an unbiased sample of the [advantage](/advantage-function/) of the action taken: $\mathbb{E}[\delta_t \mid S_t = s, A_t = a] = Q^\pi(s, a) - V^\pi(s)$.

## Where it is used

- [TD(0)](/temporal-difference-learning/) moves $V(S_t)$ by $\alpha \delta_t$; [n-step TD](/n-step-td/) and [TD(λ)](/td-lambda/) use sums of TD errors, and [eligibility traces](/eligibility-traces/) spread each $\delta_t$ over the recent states.
- [SARSA](/sarsa/), [Expected SARSA](/expected-sarsa/), [Q-learning](/q-learning/) and [double Q-learning](/double-q-learning/) use the action-value errors above; [DQN](/dqn/) minimizes the mean squared TD error of a network with a target network.
- [Actor-critic](/actor-critic/) methods use $\delta_t$ as the score of the action, since it samples the advantage, and [generalized advantage estimation](/generalized-advantage-estimation/) sums $(\gamma\lambda)^k \delta_{t+k}$ as in the λ-return identity.
- [Prioritized sweeping](/prioritized-sweeping/) and [prioritized experience replay](/prioritized-experience-replay/) order the updates by the size of the TD error.
- In neuroscience, Schultz, Dayan and Montague (1997) compared the firing of dopamine neurons with the TD error, as a reward prediction error.

## References
