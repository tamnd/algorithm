---
tag: K9FDTT
kind: algorithm
slug: double-q-learning
name: Double Q-learning
aliases:
- double learning
- tabular Double Q-learning
area: machine-learning/reinforcement-learning
level: advanced
summary: "Q-learning with two tables: one picks the greedy next action, the other gives its value. This removes the upward maximization bias of the max in the Q-learning target."
solves: [rl-control]
model: real-ram
complexity:
  vars: {T: the total number of steps, A: the largest number of actions in a state, S: the number of states}
  time: {worst: "O(A T)"}
  space: {extra: "O(S A)"}
properties: {deterministic: false, online: true, exact: false, recursive: false}
history:
  year: 2010
  people: [Hado van Hasselt]
  note: van Hasselt showed that the max in the Q-learning target overestimates, proposed the double estimator with two tables, and proved convergence.
prereqs: [q-learning]
see_also: [double-dqn, expected-sarsa, tabular-q-learning-convergence, dqn, epsilon-greedy, td-error, stochastic-approximation, sarsa]
sources:
  - paper: "Hado van Hasselt, Double Q-learning, Advances in Neural Information Processing Systems 23 (NIPS 2010), pages 2613 to 2621"
    locator: the single and double estimators and their bias, the algorithm, the convergence theorem, and the roulette and grid world experiments
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: Section 6.7 (Maximization Bias and Double Learning), Example 6.7 and Figure 6.5
---

Double Q-learning is a form of [Q-learning](/q-learning/) that keeps two action value tables, $Q^A$ and $Q^B$, and at each step updates one of them, chosen by a fair coin. The updated table picks the greedy action in the next state, and the other table gives the value of that action: $Q^A(S, A) \leftarrow Q^A(S, A) + \alpha\big(R + \gamma Q^B(S', \arg\max_a Q^A(S', a)) - Q^A(S, A)\big)$. Hado van Hasselt (2010) introduced it to remove the maximization bias of Q-learning: the max of noisy estimates is, on average, larger than the max of the true values, so Q-learning overestimates. The double target is unbiased when the estimates of all actions have the same mean, and it can only underestimate otherwise. It converges to $q_*$ under the conditions of Q-learning, and with neural networks it became [Double DQN](/double-dqn/).

## In plain words

Suppose ten coins are each tossed a few times, and you guess which coin is luckiest by picking the one with the best record so far. The record of the coin you pick is too high on average, even if all coins are fair: you picked it because it was lucky. Q-learning does this at every step, since its target takes the best of its own noisy estimates.

Double Q-learning keeps two separate records. It uses one record to pick the best move and the other record to score that move. The second record did not take part in the choice, so its score is not inflated by luck. The two records swap roles at random, and both learn.

## The problem

The setting is that of [Q-learning](/q-learning/) and [RL control](/rl-control/): a finite MDP that the algorithm can only sample, a discount $0 \le \gamma \le 1$, and the goal of $q_*$ and a greedy optimal policy. The problem it solves within that setting is the bias of the max. If $X_1, \dots, X_k$ are unbiased estimates of $\mu_1, \dots, \mu_k$, the max is convex, so by Jensen's inequality

$$\mathbb{E}\big[\max_i X_i\big] \ge \max_i \mathbb{E}[X_i] = \max_i \mu_i,$$

often with a large gap when many actions have about the same value. The Q-learning target $R + \gamma \max_a Q(S', a)$ is this single estimator, and the bias spreads backward through the bootstrapped updates.

## The algorithm

```pseudo id=main
DOUBLE-Q-LEARNING(episodes, α, γ, ε)
L1  Q^A(s, a) ← 0 and Q^B(s, a) ← 0 for all pairs     ▷ both are 0 at the terminal state
L2  for each episode do
L3      S ← the start state
L4      repeat until S is terminal
L5          A ← ε-greedy action for Q^A + Q^B in S
L6          take A, observe R and S′
L7          with probability 1/2 let (X, Y) ← (Q^A, Q^B), else (X, Y) ← (Q^B, Q^A)
L8          if S′ is terminal then y ← R else a* ← argmax_a X(S′, a); y ← R + γ Y(S′, a*)
L9          X(S, A) ← X(S, A) + α (y − X(S, A))
L10         S ← S′
L11 return Q^A, Q^B
```

Line L8 is the double estimator: the table $X$ chooses, the table $Y$ evaluates. Line L5 acts on the sum (or the mean) of the two tables, which uses all the data; van Hasselt's algorithm lets the behavior depend on both tables in any way that keeps visiting all pairs. Each step updates one table, so the cost per step is that of Q-learning, but each table sees about half of the data. The implementation breaks ties at random, because the bias example below starts with all values equal.

## Example

**One update.** Let $Q^A(S', \cdot) = (1, 3)$ and $Q^B(S', \cdot) = (2, 0)$ for two actions, with $R = 0$ and $\gamma = 1$.

| update | action chosen in $S'$ | value used in the target |
| --- | --- | --- |
| Q-learning on $Q^A$ | the second ($Q^A = 3$) | $3$ |
| Double, coin picks $X = Q^A$ | the second ($Q^A = 3$) | $Q^B = 0$ |
| Double, coin picks $X = Q^B$ | the first ($Q^B = 2$) | $Q^A = 1$ |

**Exact bias of the two estimators.** Let each estimate be its true mean plus an independent noise of $-1$ or $+1$ with probability $1/2$ each. For two actions with true values $0$ and $0$, the max of the estimates is $-1$ with probability $1/4$ and $+1$ otherwise, so $\mathbb{E}[\max] = 1/2$ while the true max is $0$. With $m$ equal actions, $\mathbb{E}[\max] = 1 - 2^{1-m}$, which tends to $1$, the full size of the noise. The double estimator picks with one set of estimates and reads the value from an independent set, so its mean is the true value of the chosen action, $0$. For true values $0$ and $1/2$, the single estimator has mean $7/8$ and the double estimator $3/8$, against a true max of $1/2$: one overestimates and the other underestimates.

**The maximization bias task.** Sutton and Barto (Example 6.7, Figure 6.5) use a small MDP. From state A, the action right ends the episode with reward 0. The action left gives reward 0 and leads to state B, where each of many actions ends the episode with a reward drawn from a normal law with mean $-0.1$ and variance 1. Every path through B has expected return $-0.1$, so right is optimal. With 10 actions in B, ε-greedy behavior with $\varepsilon = 0.1$, $\alpha = 0.1$, $\gamma = 1$, random ties and 1000 seeded runs, the fraction of runs that went left in A was:

| episode | 1 | 5 | 10 | 20 | 50 | 100 | 200 | 300 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q-learning | 0.497 | 0.685 | 0.893 | 0.921 | 0.824 | 0.467 | 0.169 | 0.117 |
| Double Q-learning | 0.497 | 0.499 | 0.449 | 0.294 | 0.148 | 0.097 | 0.078 | 0.069 |

The best possible rate is $\varepsilon / 2 = 0.05$, the chance of a random left. Q-learning goes left more than 90 percent of the time near episode 20, because $\max_b Q(B, b)$ is positive after a few lucky draws, and it takes hundreds of episodes to recover. Double Q-learning stays near the start rate and then falls toward 0.05. This is the shape of Figure 6.5.

## Correctness

**The double estimator does not overestimate.** Let $a^*$ maximize the estimates $X_a$, and let the estimates $Y_a$ be independent of the $X$s with $\mathbb{E}[Y_a] = \mu_a$. Then $\mathbb{E}[Y_{a^*} \mid X] = \mu_{a^*} \le \max_a \mu_a$, so $\mathbb{E}[Y_{a^*}] \le \max_a \mu_a$, with equality when all $\mu_a$ are equal (van Hasselt 2010). In Double Q-learning the two tables are trained on different samples (each step goes to one table only), which is what makes them close to independent.

**Convergence.** Under the conditions of [tabular Q-learning convergence](/tabular-q-learning-convergence/) (finite MDP, bounded rewards, $\gamma < 1$, every pair visited infinitely often, Robbins-Monro step sizes), both tables converge to $q_*$ with probability 1 (van Hasselt 2010). The proof has two parts. First, the difference $Q^B - Q^A$ goes to 0: on average over the coin, one step multiplies it by $1 - \alpha/2$ and adds at most $\gamma\alpha/2$ times its max norm, which is a contraction. Second, the target of $Q^A$ is the Q-learning target plus $\gamma\big(Q^B(S', a^*) - Q^A(S', a^*)\big)$, a bias that goes to 0, and a stochastic approximation with a vanishing bias has the same limit (Singh, Jaakkola, Littman and Szepesvari 2000). The proofs section gives both steps.

## Complexity

Each step costs one call to the environment, $O(A)$ for the ε-greedy choice on the sum, and $O(A)$ for the argmax of line L8, so $T$ steps take $O(AT)$ time. The two tables take $O(SA)$ memory, twice that of Q-learning. The sample cost is higher in a different sense: each table learns from about half of the steps, so Double Q-learning can learn more slowly when the bias is small.

## Properties

- **No overestimation from the max.** The target can underestimate when the action values differ, but it has no upward bias from noise.
- **Off-policy.** Like Q-learning, it learns $q_*$ from any behavior that visits every pair infinitely often.
- **Same cost per step as Q-learning.** One table is updated per step, and the work is an argmax and one lookup.
- **Symmetric.** The two tables play the same role on average; their mean is a natural final estimate.

## Variants and improvements

- **[Double DQN](/double-dqn/).** van Hasselt, Guez and Silver (2016) use the online network to pick the action and the target network to evaluate it, a cheap form of the same idea for [DQN](/dqn/).
- **Clipped double Q-learning.** TD3 takes the minimum of two critics as the target, which pushes the bias downward on purpose (Fujimoto, van Hoof and Meger 2018).
- **Double SARSA and Double Expected SARSA.** The same two-table scheme applies to the on-policy targets of [SARSA](/sarsa/) and [Expected SARSA](/expected-sarsa/).
- **Weighted and bias-corrected estimators.** Later work mixes the single and double estimators to trade the upward bias of one for the downward bias of the other.

## When to use it

Use Double Q-learning instead of Q-learning when rewards or transitions are noisy and many actions have similar values, the case in which the max is most biased: stochastic games, tasks with many near-equal actions, or any task where Q-learning visibly prefers risky paths early on. In deterministic tasks with few actions the bias is small, and plain Q-learning learns faster because it uses every sample in one table.

## Pitfalls

- **Updating both tables with the same sample.** Then the two tables are not independent and the bias returns.
- **Acting on one table only.** That wastes half of the data in the behavior. Act on the sum or the mean of the two tables.
- **Ties broken by a fixed order.** With all values equal at the start, a fixed tie rule makes the first action special and can hide or fake the bias in small examples. Break ties at random.
- **Expecting no bias at all.** The double estimator underestimates when the action values differ. In some tasks this is also harmful, though it is usually safer than overestimation.
- **Step sizes per table.** Each table is updated on about half of the visits; schedules such as $1/n$ should count the visits that actually update a table, or count all visits of the pair, as in the implementation.

## Implementations

## History

The overestimation of Q-learning had been noted before, for example by Thrun and Schwartz (1993) for Q-learning with function approximation. Hado van Hasselt (2010) traced it to the single estimator $\max_a Q(S', a)$, proposed the double estimator with two tables, proved that it does not overestimate and that Double Q-learning converges to $q_*$, and showed large gains on a roulette task and a noisy grid world. Sutton and Barto (2018, Section 6.7) present the method as double learning, with the maximization bias example of Figure 6.5. van Hasselt, Guez and Silver (2016) carried the idea to deep networks as Double DQN.

## References
