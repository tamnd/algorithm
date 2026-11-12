---
tag: CHAYP3
kind: algorithm
slug: q-learning
name: Q-learning
aliases:
- Watkins Q-learning
- one-step Q-learning
- tabular Q-learning
area: machine-learning/reinforcement-learning
level: intro
summary: "Off-policy TD control: move Q(S,A) toward R + gamma max_a Q(S',a). Tabular, with gamma < 1 and Robbins-Monro steps, it learns Q* under any policy that tries all pairs infinitely often."
solves: [rl-control]
model: real-ram
complexity:
  vars: {T: the total number of steps, A: the largest number of actions in a state, S: the number of states}
  time: {worst: "O(A T)"}
  space: {extra: "O(S A)"}
properties: {deterministic: false, online: true, exact: false, recursive: false}
history:
  year: 1989
  people: [Christopher J. C. H. Watkins]
  note: Watkins introduced Q-learning in his PhD thesis at Cambridge; the convergence proof with Peter Dayan followed in 1992.
prereqs: [temporal-difference-learning, bellman-optimality-equation, action-value-function, epsilon-greedy]
see_also: [tabular-q-learning-convergence, sarsa, expected-sarsa, double-q-learning, watkins-q-lambda, dqn, dyna-q, deadly-triad]
sources:
  - paper: "Christopher J. C. H. Watkins, Learning from delayed rewards, PhD thesis, King's College, University of Cambridge, 1989"
    locator: the definition of one-step Q-learning
  - paper: doi:10.1007/BF00992698
    title: "Christopher J. C. H. Watkins and Peter Dayan, Q-learning, Machine Learning 8(3-4), 1992, pages 279 to 292"
    locator: the algorithm and the proof of convergence of tabular Q-learning with probability 1
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: Section 6.5 (Q-learning, off-policy TD control, and Example 6.6, cliff walking)
  - paper: "Eyal Even-Dar and Yishay Mansour, Learning rates for Q-learning, Journal of Machine Learning Research 5, 2003, pages 1 to 25"
    locator: convergence rates for polynomial and linear step sizes
---

Q-learning is the off-policy [temporal-difference](/temporal-difference-learning/) control algorithm of Watkins (1989). After each step $(S, A, R, S')$ it moves $Q(S, A)$ toward $R + \gamma\max_{a} Q(S', a)$, a sample of the [Bellman optimality equation](/bellman-optimality-equation/). The target uses the best next action, not the action the agent takes next, so Q-learning learns the optimal values $q_*$ while it follows any policy that keeps trying every action, for example [ε-greedy](/epsilon-greedy/) in $Q$, or a log of old data. In a finite MDP, with every pair tried infinitely often and Robbins-Monro step sizes per pair, it converges to $q_*$ with probability 1 ([convergence of tabular Q-learning](/tabular-q-learning-convergence/)). It is the base of [DQN](/dqn/) and [Double Q-learning](/double-q-learning/).

## In plain words

You keep a score for each move in each place. After each move you see the reward and where you landed. You then update the score of the move you made toward the reward plus the best score you have for the place where you landed, as if from now on you will always play your best.

Because the update always assumes the best future, it does not matter how you really choose your moves while you learn. You can explore at random, or learn from a record of someone else's games. As long as every move in every place gets tried again and again, the scores move toward the true scores of perfect play.

## The problem

The input is an MDP that the algorithm can only sample, with a discount $0 \le \gamma \le 1$ ($\gamma < 1$ for continuing tasks). The goal is $q_*$ and a greedy policy for it, the problem of [RL control](/rl-control/). The *behavior policy*, which chooses the actions, may differ from the *target policy*, the greedy policy for $Q$: this is what off-policy means.

## The algorithm

```pseudo id=main
Q-LEARNING(episodes, α, γ, ε)
L1  Q(s, a) ← 0 for all pairs                       ▷ Q(terminal, ·) = 0
L2  for each episode do
L3      S ← the start state
L4      repeat until S is terminal
L5          A ← ε-greedy action for Q in S          ▷ any behavior that explores
L6          take A, observe R and S′
L7          if S′ is terminal then y ← R else y ← R + γ max_a Q(S′, a)
L8          Q(S, A) ← Q(S, A) + α (y − Q(S, A))
L9          S ← S′
L10 return Q
```

Line L5 may use any rule that keeps choosing every action in every state. Line L7 is the max target, which does not depend on that rule. Line L8 is the usual [TD error](/td-error/) update for one pair. For the convergence theorem the step $\alpha$ must depend on the pair, for example $\alpha = 1/n(S, A)$, where $n$ counts the updates of the pair. For continuing tasks, drop the episodes and run lines L5 to L9 forever.

## Example

**One update at a time.** Two states x and y, actions L and R, $\gamma = 1/2$, $\alpha = 1/2$ and $Q = 0$. The transitions come from a log, in this order:

| step | transition $(S, A, R, S')$ | target $y$ | new $Q(S, A)$ |
| --- | --- | --- | --- |
| 1 | (x, R, 0, y) | $0 + \tfrac12 \max(0, 0) = 0$ | $Q(\mathrm{x}, \mathrm{R}) = 0$ |
| 2 | (y, R, 2, end) | $2$ | $Q(\mathrm{y}, \mathrm{R}) = 1$ |
| 3 | (x, R, 0, y) | $0 + \tfrac12 \cdot 1 = 1/2$ | $Q(\mathrm{x}, \mathrm{R}) = 1/4$ |
| 4 | (y, L, $-1$, x) | $-1 + \tfrac12 \cdot \tfrac14 = -7/8$ | $Q(\mathrm{y}, \mathrm{L}) = -7/16$ |
| 5 | (x, L, 1, end) | $1$ | $Q(\mathrm{x}, \mathrm{L}) = 1/2$ |
| 6 | (y, L, $-1$, x) | $-1 + \tfrac12 \cdot \tfrac12 = -3/4$ | $Q(\mathrm{y}, \mathrm{L}) = -19/32$ |

In step 6 the target uses $\max_a Q(\mathrm{x}, a) = Q(\mathrm{x}, \mathrm{L}) = 1/2$, whatever action was taken in x afterward. If the transitions are deterministic, the optimal values are $q_*(\mathrm{y}, \mathrm{R}) = 2$, $q_*(\mathrm{x}, \mathrm{L}) = q_*(\mathrm{x}, \mathrm{R}) = 1$ and $q_*(\mathrm{y}, \mathrm{L}) = -1/2$, and repeating the log moves $Q$ toward them.

**Cliff walking.** On the cliff walking task of [SARSA](/sarsa/) (Sutton and Barto, Example 6.6), with $\varepsilon = 0.1$, $\alpha = 1/2$ and 500 episodes, Q-learning finds the optimal 13-step path along the edge of the cliff for every seed tried (0 to 9 in our runs). Its ε-greedy behavior still falls off the cliff now and then, so its mean return while learning, about $-40$ to $-60$ over the last 100 episodes, is worse than the $-25$ of SARSA. Q-learning learns the best greedy policy, not the best way to behave while exploring.

**Convergence.** On a continuing MDP with 3 states, 2 actions and $\gamma = 1/2$ (the [convergence](/tabular-q-learning-convergence/) page gives it), with a uniform random behavior policy and $\alpha = 1/n(s, a)$, the largest error $\max_{s,a}|Q - q_*|$ over 5 seeds was 0.08 to 0.18 after $10^3$ steps, 0.012 to 0.055 after $10^4$ steps, and 0.003 to 0.019 after $10^5$ steps.

## Correctness

The expected target of line L7, given $S = s$, $A = a$ and the table, is $(T^* Q)(s, a) = r(s, a) + \gamma\sum_{s'} p(s' \mid s, a) \max_{a'} Q(s', a')$, whatever the behavior policy is. The operator $T^*$ is a $\gamma$-contraction in the max norm with the unique fixed point $q_*$ ([Bellman contraction](/bellman-contraction/)). So line L8 is a [stochastic approximation](/stochastic-approximation/) of the fixed point of a contraction, one pair at a time.

**Theorem (Watkins and Dayan 1992; Jaakkola, Jordan and Singh 1994; Tsitsiklis 1994).** In a finite MDP with $\gamma < 1$ and bounded rewards, if every pair is updated infinitely often and the steps of each pair satisfy $\sum_t \alpha_t(s, a) = \infty$ and $\sum_t \alpha_t(s, a)^2 < \infty$, then $Q \to q_*$ with probability 1.

The proof is on the [convergence of tabular Q-learning](/tabular-q-learning-convergence/) page. The proofs section of this page proves that the expected target is $T^* Q$, that $T^*$ is a contraction, and that the update is a stochastic approximation step with noise of mean 0. The greedy policy for $q_*$ is optimal, so once $Q$ is close enough to $q_*$, its greedy policy is optimal.

## Complexity

Each step does one call to the environment, $O(A)$ work for the ε-greedy choice of line L5 and $O(A)$ for the max of line L7. So $T$ steps take $O(AT)$ time, and the table takes $O(SA)$ memory. The number of steps to reach a given accuracy depends strongly on the steps: with $\alpha = 1/n$, Even-Dar and Mansour (2003) show that the time can grow exponentially in $1/(1-\gamma)$, while polynomial steps $\alpha = 1/n^\omega$ with $1/2 < \omega < 1$ give polynomial bounds.

## Properties

- **Off-policy.** The target does not depend on the behavior policy, so Q-learning can learn from exploration, from old data and from other agents.
- **Online and model-free.** One update per step, using only the sample.
- **Optimistic about its own future.** The max in the target ignores that the agent will explore. In tasks where exploring is costly, such as cliff walking, the learned greedy policy is optimal but the behavior while learning is poor.
- **Maximization bias.** $\max_a Q(S', a)$ is a biased estimate of $\max_a q(S', a)$ when the estimates are noisy: $\mathbb{E}[\max] \ge \max \mathbb{E}$. [Double Q-learning](/double-q-learning/) reduces this bias.
- **Unstable with function approximation.** With off-policy updates, bootstrapping and function approximation together, the values can diverge ([deadly triad](/deadly-triad/)).

## Variants and improvements

- **Double Q-learning.** Two tables, one to choose the max action and the other to value it ([Double Q-learning](/double-q-learning/)).
- **Q(λ).** Eligibility traces cut after exploratory actions ([Watkins's Q(λ)](/watkins-q-lambda/)), or not cut, in Peng's Q(λ).
- **Deep Q-networks.** A neural network for $Q$, with [experience replay](/experience-replay/) and a target network ([DQN](/dqn/)).
- **Dyna-Q.** Learn a model from the same transitions and add planning updates from it ([Dyna-Q](/dyna-q/)).
- **Fitted Q iteration.** Apply the same target to a whole batch of data with a regression ([fitted Q iteration](/fitted-q-iteration/)).
- **Expected SARSA with a greedy target.** This is Q-learning itself ([Expected SARSA](/expected-sarsa/)).

## When to use it

Use Q-learning for small discrete problems when you want an optimal greedy policy and can explore freely, for example in a simulator, or when the data come from another policy. Use [SARSA](/sarsa/) or [Expected SARSA](/expected-sarsa/) when the agent must act well while it learns. When the noise in the rewards makes the max target too optimistic, use [Double Q-learning](/double-q-learning/). For large state spaces, use a function approximator, with the care that [DQN](/dqn/) takes.

## Pitfalls

- **No exploration.** With $\varepsilon = 0$ and ties broken the same way, some actions are never tried, and their values never change. The convergence theorem needs every pair to be updated infinitely often.
- **A step size shared by all pairs.** The theorem needs Robbins-Monro steps per pair. A global $1/t$ step shrinks too fast for pairs that are visited rarely.
- **$\alpha = 1/n$ with a large $\gamma$.** These steps satisfy the theorem but can be very slow when $\gamma$ is close to 1 (Even-Dar and Mansour 2003). A step such as $1/n^{0.8}$ is often faster.
- **Bootstrapping from a terminal state.** At the end of an episode the target is $R$ alone. A time limit is not a terminal state: if an episode is cut by a time limit, keep the bootstrap term.
- **Reading the learning curve as the policy's quality.** The rewards earned while learning come from the ε-greedy behavior, not from the greedy policy that Q-learning learns.

## Implementations

## History

Watkins (1989) introduced Q-learning in his PhD thesis, *Learning from Delayed Rewards*, with a proof sketch of convergence. Watkins and Dayan (1992) gave a full proof for the tabular case. Jaakkola, Jordan and Singh (1994) and Tsitsiklis (1994) proved convergence again within the theory of stochastic approximation, under weaker conditions. Mnih et al. (2015) combined Q-learning with deep networks in [DQN](/dqn/).

## References
