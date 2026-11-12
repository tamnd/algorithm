---
tag: WDFA4D
kind: algorithm
slug: temporal-difference-learning
name: Temporal-difference learning
aliases:
- TD(0)
- TD learning
- TD(0) prediction
area: machine-learning/reinforcement-learning
level: intro
summary: "Learn the value of a fixed policy from single transitions: after each step, move V(s) toward the reward plus the discounted value of the next state."
solves: [policy-evaluation]
model: real-ram
complexity:
  vars: {T: the total number of steps, S: the number of states}
  time: {worst: "O(T)"}
  space: {extra: "O(S)"}
properties: {deterministic: true, online: true, exact: false, recursive: false}
history:
  year: 1988
  people: [Richard S. Sutton]
  note: "Sutton defined the TD(lambda) family, with TD(0) as the case lambda = 0, and proved convergence in the mean for TD(0) with linearly independent features."
prereqs: [td-error, monte-carlo-policy-evaluation, bellman-expectation-equation]
see_also: [n-step-td, td-lambda, eligibility-traces, sarsa, q-learning, stochastic-approximation, least-squares-td, actor-critic]
sources:
  - paper: doi:10.1007/BF00115009
    title: "Richard S. Sutton, Learning to predict by the methods of temporal differences, Machine Learning 3(1), 1988, pages 9 to 44"
    locator: the definition of TD(lambda) and the convergence theorem for TD(0) in the mean
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: "Chapter 6: Section 6.1 (TD prediction), Section 6.2 (advantages, Example 6.2 random walk) and Section 6.3 (optimality of TD(0), Example 6.4)"
  - paper: "Tommi Jaakkola, Michael I. Jordan and Satinder P. Singh, On the convergence of stochastic iterative dynamic programming algorithms, Neural Computation 6(6), 1994, pages 1185 to 1201"
    locator: the convergence with probability 1 of tabular TD(lambda) and Q-learning
  - paper: "Peter Dayan and Terrence J. Sejnowski, TD(lambda) converges with probability 1, Machine Learning 14(3), 1994, pages 295 to 301"
    locator: the main theorem
  - book: isbn:9781886529106
    title: Dimitri P. Bertsekas and John N. Tsitsiklis, Neuro-Dynamic Programming, Athena Scientific, 1996
    locator: Chapter 5 (temporal difference methods for policy evaluation)
---

Temporal-difference learning is the family of methods that learn value estimates from the difference between successive estimates, and TD(0) is its simplest member for the [policy evaluation](/policy-evaluation/) problem. After each transition $S_t \to S_{t+1}$ with reward $R_{t+1}$, TD(0) moves $V(S_t)$ a step $\alpha$ toward the target $R_{t+1} + \gamma V(S_{t+1})$, that is, by $\alpha$ times the [TD error](/td-error/). It needs no model, as [Monte Carlo evaluation](/monte-carlo-policy-evaluation/) needs none, and it bootstraps from the current estimate, as dynamic programming does. Sutton (1988) introduced the family; with steps that meet the [Robbins-Monro conditions](/robbins-monro-conditions/), tabular TD(0) converges to $V^\pi$ with probability 1.

## In plain words

You keep a guess of how much reward each place is worth. You take one step and see the reward and the next place. Now you have a better guess for the place you just left: the reward you saw plus the guess for the next place. You move your old guess a small part of the way toward this better guess. Then you take the next step.

You do not wait until the end of the game, as the averaging method does. Each step teaches you something at once, and good news travels back one step at a time. The price is that your better guess is partly built on other guesses, which may still be wrong.

## The problem

The setting is an unknown MDP $(S, A, P, R, \gamma)$ and a fixed [policy](/policy/) $\pi$. The criterion is the discounted return with $0 \le \gamma < 1$, or $\gamma = 1$ when every episode ends with probability 1. The algorithm sees the stream of transitions $(S_t, R_{t+1}, S_{t+1})$ that $\pi$ generates. The goal is the [state value function](/state-value-function/) $V^\pi$, the unique solution of the [Bellman expectation equation](/bellman-expectation-equation/)

$$V^\pi(s) = \mathbb{E}_\pi\big[R_{t+1} + \gamma V^\pi(S_{t+1}) \mid S_t = s\big] = (T^\pi V^\pi)(s).$$

The value of the terminal state is 0. An episode is written as the pairs $(S_t, R_{t+1})$, $t = 0, \ldots, T-1$, and $S_T$ is terminal.

## The algorithm

```pseudo id=main
TD0(episodes, α, γ, V)
L1  for each episode (S_0, R_1), ..., (S_{T−1}, R_T) do
L2      for t ← 0 to T − 1 do
L3          if t + 1 < T then target ← R_{t+1} + γ V(S_{t+1})
L4          else target ← R_{t+1}                    ▷ V(terminal) = 0
L5          δ ← target − V(S_t)                       ▷ the TD error
L6          V(S_t) ← V(S_t) + α δ
L7  return V
```

Line L3 forms the one-step target from the reward and the current estimate of the next state. Line L4 uses the value 0 of the terminal state; forgetting it is a common bug. Lines L5 and L6 move $V(S_t)$ by the fraction $\alpha$ of the [TD error](/td-error/). The step $\alpha$ may depend on the number of visits to $S_t$, for example $\alpha = 1/n$ or $n^{-0.75}$. The update happens right after the step, so the method also runs on a single endless stream of transitions: drop the episode loop and line L4.

## Example

Take the random walk of Sutton and Barto (Example 6.2): states A, B, C, D, E in a row, start in C, move left or right with probability $1/2$ each. Leaving at the left end gives reward 0, leaving at the right end gives reward 1, and all other rewards are 0. With $\gamma = 1$ the true values are $V^\pi = (1/6, 2/6, 3/6, 4/6, 5/6)$. Start from $V = 1/2$ everywhere, with $\alpha = 1/10$.

Episode 1 is C, B, C, D, E, then right (+1). Episode 2 is C, D, E, D, C, B, A, then left (0).

| episode | step | target | $\delta$ | new value |
| --- | --- | --- | --- | --- |
| 1 | C to B, B to C, C to D, D to E | $0 + 1/2$ | 0 | unchanged |
| 1 | E to right end | 1 | $1/2$ | $V(\mathrm{E}) = 11/20 = 0.55$ |
| 2 | C to D | $0 + 1/2$ | 0 | unchanged |
| 2 | D to E | $0 + 11/20$ | $1/20$ | $V(\mathrm{D}) = 101/200 = 0.505$ |
| 2 | E to D | $0 + 101/200$ | $-9/200$ | $V(\mathrm{E}) = 1091/2000 = 0.5455$ |
| 2 | D to C | $0 + 1/2$ | $-1/200$ | $V(\mathrm{D}) = 1009/2000 = 0.5045$ |
| 2 | C to B, B to A | $0 + 1/2$ | 0 | unchanged |
| 2 | A to left end | 0 | $-1/2$ | $V(\mathrm{A}) = 9/20 = 0.45$ |

In episode 1 only the last state changes: TD(0) moves information back one step per visit. Constant-$\alpha$ MC would move every visited state toward the return 1 in the same episode. With the step $\alpha_n = n^{-0.75}$ for the $n$-th visit of a state and the start $V = 1/2$, 6000 episodes give values within $0.03$ of $V^\pi$ in each state (seed 3 in the tests).

**Batch TD(0) against batch MC** (Sutton and Barto, Example 6.4). The batch has eight episodes: A, 0, B, 0 once; B, 1 six times; B, 0 once. Both methods give $V(\mathrm{B}) = 3/4$. Batch Monte Carlo gives $V(\mathrm{A}) = 0$, the only return seen from A. Batch TD(0), which applies the summed updates of the whole batch again and again with a small $\alpha$, gives $V(\mathrm{A}) = 3/4$: in the data, A always goes to B with reward 0, so the maximum likelihood model says $V(\mathrm{A}) = V(\mathrm{B})$.

## Correctness

The key fact is that the expected TD error is the Bellman residual: with $V$ held fixed,

$$\mathbb{E}_\pi[\delta_t \mid S_t = s] = (T^\pi V)(s) - V(s).$$

So $V^\pi$ is the only table at which the expected update is zero in every state, because $T^\pi$ is a $\gamma$-contraction ([Bellman contraction](/bellman-contraction/)) for $\gamma < 1$. Tabular TD(0) is a [stochastic approximation](/stochastic-approximation/) scheme for this fixed point. The convergence theorem: if every state is updated infinitely often and the steps $\alpha_n(s)$ of each state meet $\sum_n \alpha_n(s) = \infty$ and $\sum_n \alpha_n(s)^2 < \infty$, then $V \to V^\pi$ with probability 1 (Jaakkola, Jordan and Singh 1994; Dayan and Sejnowski 1994). For batch TD(0), the fixed point is the value function of the maximum likelihood Markov model of the batch, the certainty-equivalence estimate. The full proofs are in the proofs section.

With a constant $\alpha$, $V$ does not converge: it keeps a random error whose size grows with $\alpha$. Sutton (1988) proved convergence in the mean for small constant $\alpha$ in the linear case with linearly independent features, which includes the table.

## Complexity

Each step costs $O(1)$ arithmetic operations and two table reads, so $T$ steps cost $O(T)$ time. The memory is the table, $O(|S|)$, and nothing else: unlike Monte Carlo, TD(0) does not store the episode. Batch TD(0) costs $O(T_b)$ per sweep over a batch of $T_b$ steps.

The number of samples to reach a given accuracy depends on $\gamma$, on how often $\pi$ visits each state and on the step sizes; the convergence theorem below gives no rate, and there is no bound in $|S|$ alone. The expected update, with $V$ fixed, is one step of the damped iteration $V \leftarrow V + \alpha D(T^\pi V - V)$, where $D$ is the diagonal matrix of the visit frequencies.

## Properties

- **Online and incremental.** It updates after each step, needs no end of the episode and works on continuing tasks.
- **Model free.** It uses only sampled transitions.
- **Bootstrapping.** The target uses $V(S_{t+1})$. So the target is biased while $V$ is wrong, but its variance is lower than the variance of the full return, because it depends on one random transition instead of the whole rest of the episode.
- **Markov sensitive.** The fixed point is right only if the states are Markov. Monte Carlo does not need this.
- **Batch fixed point.** Batch TD(0) finds the certainty-equivalence estimate, batch MC the minimum squared error fit to the returns.

## Variants and improvements

- **[n-step TD](/n-step-td/).** Wait $n$ steps and bootstrap from $V(S_{t+n})$. The case $n = 1$ is TD(0), and $n \ge T$ is Monte Carlo.
- **[TD(λ)](/td-lambda/).** Average all $n$-step returns with weights $(1-\lambda)\lambda^{n-1}$, and implement it online with [eligibility traces](/eligibility-traces/).
- **Control.** Apply the same update to action values: [SARSA](/sarsa/) is on-policy, [Q-learning](/q-learning/) uses the max target, [Expected SARSA](/expected-sarsa/) the expected target.
- **Function approximation.** Semi-gradient TD(0) updates weights $w \leftarrow w + \alpha \delta_t \nabla \hat v(S_t, w)$. With linear features and on-policy sampling it converges (Tsitsiklis and Van Roy 1997); off-policy it can diverge, see the [deadly triad](/deadly-triad/). [Least-squares TD](/least-squares-td/) solves for the linear fixed point directly, and [gradient TD](/gradient-temporal-difference/) methods are stable off-policy.
- **Critic.** In [actor-critic](/actor-critic/) methods the TD error of a learned $V$ scores the actions of the actor.

## When to use it

Use TD(0) when episodes are long or never end, when updates must happen during an episode, or when memory for whole episodes is not available. It often learns faster than constant-$\alpha$ Monte Carlo on Markov tasks, such as the random walk above, but this is an observed result, not a theorem for all tasks. Use [Monte Carlo evaluation](/monte-carlo-policy-evaluation/) when the state signal may not be Markov or when an unbiased estimate is needed. Use [TD(λ)](/td-lambda/) or [n-step TD](/n-step-td/) to trade between the two.

## Pitfalls

- **Bootstrapping from the terminal state.** Line L4 must use 0, not a stored $V(S_T)$. A table entry for the terminal state that is ever updated breaks the fixed point.
- **Updating before the target is read.** In code that reads $V(S_{t+1})$ after the write of line L6, a self-loop $S_{t+1} = S_t$ uses the new value. Compute the target in line L3 first.
- **Constant step and convergence.** A constant $\alpha$ makes the estimate wander around $V^\pi$. For convergence, use steps such as $1/n$ or $n^{-0.75}$ per state.
- **Off-policy data.** TD(0) with transitions from another policy estimates the value of that other policy. Use [importance sampling](/importance-sampling-off-policy/) or a control method such as [Q-learning](/q-learning/).

## Implementations

## History

Earlier programs, starting with Samuel's checkers player of 1959, already moved an evaluation toward the evaluation of a later position; Sutton and Barto trace this line in their book. Sutton (1988) named and analyzed the TD($\lambda$) family and proved convergence in the mean for TD(0). Dayan and Sejnowski (1994) and Jaakkola, Jordan and Singh (1994) proved convergence with probability 1 in the tabular case under Robbins-Monro steps.

## References
