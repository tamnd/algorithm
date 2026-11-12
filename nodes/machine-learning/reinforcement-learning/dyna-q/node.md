---
tag: DC1KQ2
kind: algorithm
slug: dyna-q
name: Dyna-Q
aliases:
- Dyna
area: machine-learning/reinforcement-learning
level: core
summary: "After each real step, do a Q-learning update, store the transition in a table model, and do n more Q-learning updates on transitions replayed from the model."
solves: [rl-control]
model: real-ram
complexity:
  vars: {T: the number of real steps, n: the number of planning steps after each real step, A: the number of actions, S: the number of states}
  time: {worst: "O(T (n + 1) A)"}
  space: {extra: "O(S A)"}
properties: {deterministic: false, online: true, exact: false, recursive: false}
history:
  year: 1990
  people: [Richard S. Sutton]
  note: Sutton proposed the Dyna architecture, which mixes learning from real experience with planning on a learned model, at ICML 1990.
prereqs: [q-learning, markov-decision-process]
see_also: [prioritized-sweeping, model-based-reinforcement-learning, experience-replay, value-iteration, muzero, real-time-dynamic-programming, epsilon-greedy, exploration-exploitation-tradeoff]
sources:
  - paper: doi:10.1016/B978-1-55860-141-3.50030-4
    title: "Richard S. Sutton, Integrated architectures for learning, planning, and reacting based on approximating dynamic programming, Proceedings of the Seventh International Conference on Machine Learning (ICML 1990), pages 216 to 224"
    locator: the Dyna architecture, Dyna-Q, and the maze experiments with different numbers of planning steps
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: Section 8.2 (Dyna, the tabular Dyna-Q algorithm and Example 8.1, the Dyna maze) and Section 8.3 (Dyna-Q+)
---

Dyna-Q is a reinforcement learning agent that both learns and plans. After each real step $(S, A, R, S')$ it does the [Q-learning](/q-learning/) update, and it writes the transition into a table, the model: $\mathrm{Model}(S, A) \leftarrow (R, S')$. Then it does $n$ planning steps. Each planning step picks a state and action that it saw before, asks the model what happened, and does the same Q-learning update on that simulated transition. The real step and the planning steps use the same update and the same table $Q$. So the model is a way to reuse past experience many times. With $n = 0$ the method is plain Q-learning. With large $n$ it spreads the value of a new discovery through the whole table after a few real steps. In a deterministic environment the model is exact for every pair it has seen, and with $\alpha = 1$ the planning steps are exact backups of [value iteration](/value-iteration/) on $Q$ (with $\alpha < 1$ they move part of the way to the backup).

## In plain words

Think of a person who finds a way through a new building. Each time they walk, they learn a little about which turns are good. Dyna-Q also writes down every turn it took and where that turn led. Between walks, it reads its notes and imagines taking those turns again, and each time it updates its opinion of the turns as if it walked them for real.

The notes are cheap to replay, so the agent can think many times for each real step. When it finds the exit once, the imagined replays carry that news back along the whole route, and the next real walk is already much better. The cost is computation, not more real walks.

## The problem

The agent acts in a finite MDP that it does not know, with states $S$, actions $A$, rewards and a discount $0 \le \gamma < 1$. It sees the current state, picks an action, and gets a reward, the next state, and a flag that says whether the episode ended. The goal is the [control problem](/rl-control/): find a policy with the largest expected discounted return, using as few real steps as possible. Dyna-Q assumes that the environment is deterministic, or close to it, because its model stores only the last outcome of each state and action.

## The algorithm

```pseudo id=main
DYNA-Q(environment, α, γ, ε, n, q0, number of steps)
L1  Q(s, a) ← q0 for every state s and action a; Model ← empty
L2  repeat for the given number of real steps
L3      S ← the start state if the last step ended an episode, else the last next state; do lines L4 to L11 from S
L4      A ← an ε-greedy action for Q(S, ·)
L5      take action A; observe the reward R, the next state S′ and whether S′ is terminal
L6      Q(S, A) ← Q(S, A) + α [R + γ max_a Q(S′, a) − Q(S, A)]          ▷ use R alone as the target if S′ is terminal
L7      Model(S, A) ← (R, S′, terminal)
L8      repeat n times
L9          S̄ ← a random state seen before; Ā ← a random action taken before in S̄
L10         (R̄, S̄′, terminal) ← Model(S̄, Ā)
L11         Q(S̄, Ā) ← Q(S̄, Ā) + α [R̄ + γ max_a Q(S̄′, a) − Q(S̄, Ā)]       ▷ R̄ alone if terminal
```

Lines L4 to L6 are one step of Q-learning, which Sutton calls direct reinforcement learning. Line L7 is model learning. Lines L8 to L11 are planning, which Sutton calls indirect reinforcement learning. Planning picks only pairs that the model knows, so it never asks the model about an action that was not tried. The initial value $q_0$ is any number. A value above every return that the agent can get, as in the example below, makes the greedy policy try each action at least once.

## Example

The Dyna maze of Sutton and Barto (Example 8.1) has 6 by 9 cells, seven wall cells, a start on the left and a goal in the top right corner. The four actions move up, down, left and right, and a move into a wall or the border leaves the agent in place. The step into the goal gives reward 1 and ends the episode. All other rewards are 0. The shortest path has 14 steps, which a breadth-first search in the tests confirms.

The implementation runs with $\alpha = 1$, $\gamma = 0.95$, $\varepsilon = 0.1$ and $q_0 = 1$. After each episode, a test follows the greedy policy from the start and records the first real step at which this path has 14 steps. Over the seeds 0 to 9:

| planning steps $n$ | fastest | median | slowest |
| --- | --- | --- | --- |
| 0 (Q-learning) | 2059 | 2274 | 2437 |
| 5 | 752 | 871.5 | 934 |
| 50 | 291 | 372.5 | 408 |

The mean lengths of the first three episodes show the same effect:

| $n$ | episode 1 | episode 2 | episode 3 |
| --- | --- | --- | --- |
| 0 | 265.2 | 250.0 | 175.4 |
| 5 | 268.1 | 163.3 | 99.8 |
| 50 | 241.3 | 65.9 | 35.0 |

The first episode is about the same for all $n$, because nothing is known yet and the agent explores. In the first episode, Q-learning with $n = 0$ changes only the value of the last action before the goal. With $n = 50$, the planning steps during the first episode and right after it already carry the reward far back along the path, so the second episode is short. Sutton and Barto report the same pattern with $q_0 = 0$ and $\alpha = 0.1$.

## Correctness

Dyna-Q does not stop by itself. It runs for the given number of steps, so it terminates. The claim is about the limit.

Assume a deterministic environment and $\gamma < 1$. Every entry of the model is then a true transition, so each update in lines L6 and L11 has the form $Q(s, a) \leftarrow (1 - \alpha)Q(s, a) + \alpha (\mathcal{T}Q)(s, a)$, where $\mathcal{T}$ is the Bellman optimality operator for action values, a $\gamma$-contraction in the max norm ([Bellman contraction](/bellman-contraction/)). If $0 < \alpha \le 1$, one such update moves $Q(s, a)$ closer to $Q^*(s, a)$ by a factor of at most $1 - \alpha(1 - \gamma)$ relative to the largest error, and it never increases the largest error. When every pair has been tried in the real environment, and $n \ge 1$, the random choice in line L9 updates every pair again and again with probability 1. So $Q \to Q^*$, and the greedy policy becomes optimal after finitely many steps. The full proof is in the proofs section.

In a stochastic environment the model keeps only the last outcome, so the planning steps use a wrong model and $Q$ need not converge to $Q^*$. Use a count model, as in [model-based reinforcement learning](/model-based-reinforcement-learning/) and the online form of [prioritized sweeping](/prioritized-sweeping/), in that case.

## Complexity

One real step costs $O(A)$ for the action choice and the update, and $O(1)$ expected time for the model write with a hash table. Each planning step costs $O(A)$ for the maximum in line L11, plus $O(1)$ for the random choice if the agent keeps a list of the seen states and, for each, a list of its tried actions. So $T$ real steps cost $O(T(n + 1)A)$. The table $Q$ and the model take $O(SA)$ space.

The point of $n$ is the trade-off between computation and data. In the example, 50 planning steps per real step cut the real steps to the optimal path by a factor of about 6, for about 50 times as many updates.

## Properties

- **Online.** The agent learns and plans at every step, with a fixed amount of work per step.
- **Model-based and model-free at once.** The same update and the same table serve real and simulated experience.
- **Randomized.** Both the ε-greedy choice and the planning choice in line L9 use random numbers. The implementation uses a seeded generator, so a run is reproducible.
- **Reduces to Q-learning.** With $n = 0$ it is exactly tabular Q-learning, and the tests check that a step with $n = 0$ changes only one entry.
- **Exact in the deterministic case.** The random tests check that with random actions, random restarts and $n = 40$, $Q$ matches $Q^*$ to $10^{-6}$ on 500 random deterministic MDPs.

## Variants and improvements

- **Dyna-Q+.** Sutton and Barto (Section 8.3) add an exploration bonus $\kappa\sqrt{\tau}$ to the planning reward, where $\tau$ is the number of steps since the pair was last tried in the real environment. This helps when the environment changes, for example when a shortcut opens.
- **Prioritized sweeping.** [Prioritized sweeping](/prioritized-sweeping/) replaces the uniform choice in line L9 by the pairs whose values would change most, starting from the predecessors of the last real transition. It needs far fewer planning steps on mazes.
- **Stochastic models.** Store counts or sample outcomes from all past transitions instead of the last one. With expected updates over the model, the planning step is a value iteration backup on the learned model.
- **Experience replay.** [Experience replay](/experience-replay/) in deep Q-learning stores the transitions themselves and replays them, which is a nonparametric model in the same spirit.
- **Learned models with function approximation.** Later methods learn a model as a neural network and plan with it. [MuZero](/muzero/) plans with a learned model by tree search instead of by replayed updates.

## When to use it

Use Dyna-Q when real steps are expensive and computation is cheap, the state and action spaces are small enough for tables, and the environment is deterministic or nearly so. It is a good first model-based method, and it shows the value of planning clearly. For stochastic environments use a count model. For large state spaces use function approximation, where a wrong model can do more harm, as described in [model-based reinforcement learning](/model-based-reinforcement-learning/).

## Pitfalls

- **Exploration.** With $q_0 = 0$ and ε-greedy, some actions on the shortest path may stay untried for a long time, and planning cannot help with pairs that the model does not know. The greedy path can then stay at a longer route. An optimistic $q_0$ or a larger $\varepsilon$ helps.
- **Changing environments.** The model keeps old transitions. If a wall moves, the agent keeps planning with the old map until it tries the changed pair again. Dyna-Q+ was made for this case.
- **Stochastic transitions.** A model that keeps the last outcome gives a biased planning target. Planning many times on it makes the bias stronger, not weaker.
- **Terminal states.** The model must store whether the next state is terminal. Otherwise the planning target adds $\gamma \max_a Q(S', a)$ for a state that has no future.
- **Wrong planning pairs.** Line L9 must pick only pairs that were tried. A pair with no model entry has no defined outcome.

## Implementations

## History

Sutton (1990) introduced the Dyna architecture at ICML, as a way to combine learning, planning and reacting in one agent, and he tested Dyna-Q and Dyna-PI on mazes. He described the architecture again in a short paper in the SIGART Bulletin (1991). The idea that planning is learning from simulated experience led to [prioritized sweeping](/prioritized-sweeping/) and Queue-Dyna (Moore and Atkeson, and Peng and Williams, both 1993), which replace the random choice of planning pairs by an ordered one. Sutton and Barto made Dyna-Q the central example of planning and learning in Chapter 8 of their book.

## References
