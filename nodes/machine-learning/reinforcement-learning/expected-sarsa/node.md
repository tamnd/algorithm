---
tag: HAESKC
kind: algorithm
slug: expected-sarsa
name: Expected SARSA
aliases:
- Expected Sarsa
- expected SARSA update
area: machine-learning/reinforcement-learning
level: core
summary: "TD control that moves Q(S,A) toward R + gamma sum_a pi(a|S') Q(S',a), the mean over the next action. Lower variance than SARSA; with a greedy pi it is Q-learning."
solves: [rl-control]
model: real-ram
complexity:
  vars: {T: the total number of steps, A: the largest number of actions in a state, S: the number of states}
  time: {worst: "O(A T)"}
  space: {extra: "O(S A)"}
properties: {deterministic: false, online: true, exact: false, recursive: false}
history:
  year: 2009
  people: [Harm van Seijen, Hado van Hasselt, Shimon Whiteson, Marco Wiering]
  note: They analyzed Expected Sarsa, proved its convergence and showed its lower variance and its robustness to large step sizes.
prereqs: [sarsa, q-learning]
see_also: [double-q-learning, n-step-td, retrace, exploration-exploitation-tradeoff, variance, temporal-difference-learning, tabular-q-learning-convergence, td-error]
sources:
  - paper: "Harm van Seijen, Hado van Hasselt, Shimon Whiteson and Marco Wiering, A theoretical and empirical analysis of Expected Sarsa, IEEE Symposium on Adaptive Dynamic Programming and Reinforcement Learning (ADPRL 2009), pages 177 to 184"
    locator: the algorithm, the convergence proof, the variance analysis, and the cliff walking experiments
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: Section 6.6 (Expected Sarsa, and its relation to Q-learning) and Section 7.5 (n-step tree backup, which generalizes it)
---

Expected SARSA is a [temporal-difference](/temporal-difference-learning/) control algorithm that moves $Q(S, A)$ toward $R + \gamma\sum_{a} \pi(a \mid S')\, Q(S', a)$, the mean of the next action value under the target policy $\pi$, instead of the value of one sampled next action as in [SARSA](/sarsa/). The mean removes the randomness of the next action from the target, so the variance is lower, and in deterministic tasks the step size can go up to 1 without harm (van Seijen, van Hasselt, Whiteson and Wiering 2009). The target policy may differ from the behavior policy; when it is greedy, the mean is $\max_a Q(S', a)$ and Expected SARSA is [Q-learning](/q-learning/) (Sutton and Barto, Section 6.6).

## In plain words

SARSA updates a move's score using the score of the next move it picked. That next pick is random, since the agent explores now and then, so the update jumps around: a rare random pick of a bad move makes it drop a lot.

Expected SARSA does not use the one move it picked. It looks at all the moves in the next place and takes their average score, weighted by how likely the agent is to pick each one. This average is what SARSA's update would be on average, so it aims at the same values but without the jumps. If the agent always picked its best move, the average would just be the best score, which is exactly Q-learning.

## The problem

The setting is the one of [SARSA](/sarsa/) and [Q-learning](/q-learning/): an MDP that the algorithm can only sample, a discount $0 \le \gamma \le 1$, and the goal of a good policy and its action values, the problem of [RL control](/rl-control/). The target policy $\pi$ must give the probabilities $\pi(a \mid s)$ in closed form, for example ε-greedy in $Q$.

## The algorithm

```pseudo id=main
EXPECTED-SARSA(episodes, α, γ, b, π)
L1  Q(s, a) ← 0 for all pairs                       ▷ Q(terminal, ·) = 0
L2  for each episode do
L3      S ← the start state
L4      repeat until S is terminal
L5          A ← an action drawn from the behavior policy b in S    ▷ e.g. ε-greedy for Q
L6          take A, observe R and S′
L7          if S′ is terminal then y ← R else y ← R + γ Σ_a π(a | S′) Q(S′, a)
L8          Q(S, A) ← Q(S, A) + α (y − Q(S, A))
L9          S ← S′
L10 return Q
```

Line L7 is the only change from Q-learning: the max becomes a mean under $\pi$. For an ε-greedy target policy in a state with $k$ actions, the mean is $\frac{\varepsilon}{k}\sum_a Q(S', a) + (1 - \varepsilon) Q(S', a^*)$, with $a^*$ the greedy action. When $b = \pi$ (both ε-greedy for $Q$ with the same $\varepsilon$), the method is on-policy and learns the same values as SARSA. With any other $\pi$ it is off-policy, and it needs no importance sampling, because the next action is not sampled at all.

## Example

**One update.** Suppose $Q(S, A) = -2$, the step gives $R = -1$, $\gamma = 1$, $\alpha = 1/2$, and in $S'$ the four actions have values up $-3$, right $-1$, down $-10$, left $-2$. With $\varepsilon = 1/10$, the ε-greedy policy picks right with probability $37/40$ and each other action with probability $1/40$.

| method | value of $S'$ used in the target | new $Q(S, A)$ |
| --- | --- | --- |
| Expected SARSA | $\tfrac{1}{40}(-3 - 10 - 2) + \tfrac{37}{40}(-1) = -13/10$ | $-2 + \tfrac12(-1 - \tfrac{13}{10} + 2) = -43/20$ |
| Q-learning | $\max = -1$ | $-2$ |
| SARSA | $-1$ with probability $37/40$, else $-3$, $-10$ or $-2$ | $-2$, $-3$, $-13/2$ or $-5/2$ |

The SARSA value has mean $-13/10$, the same as Expected SARSA, and variance $103/50 \approx 2.06$; the expected value has variance 0 here, since the transition is deterministic.

**Cliff walking.** On the cliff walking task of [SARSA](/sarsa/) with $\varepsilon = 0.1$ and 500 episodes, Expected SARSA learned a 15-step path one row above the edge of the cliff, for $\alpha = 1/2$ and for $\alpha = 1$, in seeds 0 to 5. Its mean return over the last 100 episodes was between about $-19$ and $-24$ in both cases. SARSA with $\alpha = 1$ dropped to between $-77$ and $-161$, because each update copies one random next value in full. This matches the experiments of van Seijen et al. (2009) and of Sutton and Barto (Section 6.6), in which Expected SARSA does well over a wide range of step sizes on this task.

## Correctness

**Same mean as SARSA, less variance.** Given $S$, $A$ and the table, let $Y = R + \gamma Q(S', A')$ be the SARSA target with $A' \sim \pi(\cdot \mid S')$, and $\bar Y = R + \gamma\sum_a \pi(a \mid S') Q(S', a)$ the Expected SARSA target. Then $\bar Y = \mathbb{E}[Y \mid R, S']$, so the two targets have the same mean, and by the law of total variance,

$$\operatorname{Var}(Y) = \operatorname{Var}(\bar Y) + \gamma^2\, \mathbb{E}\Big[\operatorname{Var}_{A' \sim \pi(\cdot \mid S')}\big(Q(S', A')\big)\Big] \ge \operatorname{Var}(\bar Y).$$

The gap is the mean spread of $Q(S', \cdot)$ under $\pi$. It is zero only when $\pi(\cdot \mid S')$ puts all its weight on actions with the same value, for example on one greedy action.

**Convergence.** The expected target is $(T^\pi Q)(S, A)$, the [Bellman expectation operator](/bellman-expectation-equation/) for action values, a $\gamma$-contraction with fixed point $q_\pi$. So for a fixed target policy, Expected SARSA is a stochastic approximation of $q_\pi$, and the argument of [tabular Q-learning convergence](/tabular-q-learning-convergence/) applies. van Seijen et al. (2009) proved that with Robbins-Monro steps, every pair visited infinitely often and a target policy that becomes greedy in the limit, $Q$ converges to $q_*$ with probability 1, as SARSA does. With a greedy target policy, line L7 is the Q-learning target, so the Q-learning theorem applies directly.

## Complexity

Each step costs one call to the environment, $O(A)$ for the behavior choice, and $O(A)$ for the mean of line L7, so $T$ steps take $O(AT)$ time, the same order as SARSA and Q-learning. The table takes $O(SA)$ memory. The extra cost over SARSA is the sum over the actions of $S'$, which matters only for large action sets.

## Properties

- **Lower variance than SARSA.** The next action no longer adds noise to the target. In deterministic tasks the target is deterministic given $S$ and $A$.
- **On-policy or off-policy.** With $\pi = b$ it learns $q_b$ like SARSA; with another $\pi$ it learns $q_\pi$ from data of $b$, without importance ratios.
- **Contains Q-learning.** With a greedy $\pi$, it is Q-learning exactly: the same updates and, with the same random numbers, the same table.
- **Large step sizes.** Because the target varies less, step sizes near 1 often work. On cliff walking, $\alpha = 1$ gives about the same returns as $\alpha = 1/2$.

## Variants and improvements

- **n-step Expected SARSA.** Use $n$ sampled rewards and then the mean under $\pi$ at step $n$ (Sutton and Barto, Section 7.2), like [n-step TD](/n-step-td/).
- **Tree backup.** Take the mean at every step of an $n$-step return, weighting the sampled branch by its probability: the n-step tree backup algorithm (Sutton and Barto, Section 7.5), off-policy without importance sampling, and the basis of [Retrace](/retrace/).
- **Double Expected SARSA.** Use two tables, one for the policy and one for the values, as in [Double Q-learning](/double-q-learning/), to reduce the bias of a greedy-leaning target.
- **Function approximation.** Semi-gradient Expected SARSA replaces the table by $\hat q(s, a, w)$; the mean is over the discrete actions.
- **Soft targets.** With a softmax target policy, the mean is the expected value under the softmax, and the same line L7 applies.

## When to use it

Use Expected SARSA instead of SARSA whenever the action set is small enough to sum over: it learns the same values with less noise and tolerates larger step sizes. Use its off-policy form when you want the values of an exploring target policy from data of another policy. When you want $q_*$ and the behavior policy does not matter, set the target to greedy, which gives [Q-learning](/q-learning/), or use [Double Q-learning](/double-q-learning/) if the max is biased.

## Pitfalls

- **Wrong probabilities for the target.** The mean must use $\pi(\cdot \mid S')$ for the current table, with the same tie rule as the action choice. Using $1 - \varepsilon$ for the greedy action and forgetting its share $\varepsilon / k$ of the random choice gives a target that is not a mean under any policy.
- **Large action sets.** The sum over all actions costs $O(A)$ per step. For continuous actions it must be replaced by an integral or a sample, which brings back the variance.
- **Expecting zero variance.** Only the variance from the next action goes away. The variance from the reward and the next state stays.
- **Bootstrapping from a terminal state.** At a terminal $S'$, the target is $R$ alone.

## Implementations

## History

van Seijen, van Hasselt, Whiteson and Wiering (2009) gave the method its name, proved its convergence under GLIE exploration, analyzed its variance and showed in experiments, including cliff walking, that it is better than SARSA over a wide range of step sizes. Sutton and Barto (2018, Section 6.6) present it as the method between SARSA and Q-learning, and use it to define the tree backup algorithm.

## References
