---
tag: NRKTQX
kind: algorithm
slug: prioritized-sweeping
name: Prioritized sweeping
aliases:
- Moore-Atkeson prioritized sweeping
area: machine-learning/reinforcement-learning
level: advanced
summary: "Do value backups in the order of their Bellman error, kept in a priority queue. When a value changes, put its predecessor states back in the queue."
solves: [mdp-planning]
model: real-ram
complexity:
  vars: {S: the number of states, A: the number of actions in each state, d: the largest number of predecessors of a state, b: the number of backups}
  time: {worst: "O(b d (S A + log(b d)))"}
  space: {extra: "O(S d + b d)"}
properties: {deterministic: true, online: true, exact: false, recursive: false}
history:
  year: 1993
  people: [Andrew W. Moore, Christopher G. Atkeson, Jing Peng, Ronald J. Williams]
  note: Moore and Atkeson (prioritized sweeping) and Peng and Williams (Queue-Dyna) published the same idea independently in 1993.
prereqs: [value-iteration, priority-queue]
see_also: [dyna-q, model-based-reinforcement-learning, real-time-dynamic-programming, modified-policy-iteration, prioritized-experience-replay, dijkstra, binary-heap, q-learning]
sources:
  - paper: doi:10.1007/BF00993104
    title: "Andrew W. Moore and Christopher G. Atkeson, Prioritized sweeping: reinforcement learning with less data and less time, Machine Learning 13(1), 1993, pages 103 to 130"
    locator: the prioritized sweeping algorithm, its priority queue of predecessors, and the experiments on stochastic mazes
  - paper: doi:10.1177/105971239300100403
    title: "Jing Peng and Ronald J. Williams, Efficient learning and planning within the Dyna framework, Adaptive Behavior 1(4), 1993, pages 437 to 454"
    locator: Queue-Dyna, the ordering of planning backups by the size of the expected change
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: Section 8.4 (prioritized sweeping for a deterministic environment, and Example 8.4 on mazes)
  - paper: "David Wingate and Kevin D. Seppi, Prioritization methods for accelerating MDP solvers, Journal of Machine Learning Research 6, 2005"
    locator: the comparison of priority metrics and the partitioned variants
---

Prioritized sweeping is a way to order the backups of [value iteration](/value-iteration/). Instead of sweeping over all states in a fixed order, it keeps the states in a [priority queue](/priority-queue/) keyed by their Bellman error $|(TV)(s) - V(s)|$, the amount by which a backup would change their value. It always backs up the state with the largest error. When $V(s)$ changes, only the states that can reach $s$ in one step, the predecessors of $s$, can get a new error, so only they are updated in the queue. The method stops when no error exceeds a threshold $\theta$. On problems where the value spreads out from a few sources, such as a goal in a maze, it does far fewer backups than sweeping, about one per state on a chain. In the online form, the agent learns a model from experience and does a few prioritized backups after each real step.

## In plain words

When you learn that one place is good, the places that lead to it become better too, and then the places that lead to those, and so on backward. Updating every place on every round wastes work, because most places did not change.

Prioritized sweeping keeps a to-do list of places whose value is out of date, sorted by how much their value would change. It always fixes the most out-of-date place first. When it changes a place, it checks only the places that lead to it and puts them on the list if they are now out of date. When the list is empty, or all remaining changes are tiny, it stops.

## The problem

The input is a finite MDP $(S, A, P, R, \gamma)$ with $0 \le \gamma < 1$, given as a model, and a threshold $\theta > 0$. In the online form, the model is learned from transitions. The output is a vector $V$ with $\lVert TV - V \rVert_\infty \le \theta$, where $(TV)(s) = \max_a [R(s, a) + \gamma \sum_{s'} P(s' \mid s, a)V(s')]$, and so $\lVert V - V^* \rVert_\infty \le \theta/(1-\gamma)$. The predecessors of a state $s'$ are $\mathrm{pred}(s') = \{s : P(s' \mid s, a) > 0 \text{ for some } a\}$.

## The algorithm

```pseudo id=main
PRIORITIZED-SWEEPING(S, A, P, R, γ, θ)
L1  V ← 0; for each state s′, pred(s′) ← the states s with P(s′ | s, a) > 0 for some a
L2  for each state s: e ← |max_a Q(s, a) − V(s)|; if e > θ then insert s into PQ with priority e
L3  while PQ is not empty do
L4      s ← EXTRACT-MAX(PQ)
L5      V(s) ← max_a [R(s, a) + γ Σ_{s′} P(s′ | s, a) V(s′)]
L6      for each p in pred(s) do
L7          e ← |max_a Q(p, a) − V(p)|                 ▷ Q(p, a) = R(p, a) + γ Σ_{s′} P(s′ | p, a) V(s′)
L8          if e > θ then set the priority of p to e (insert p if absent) else remove p from PQ
L9  return V
```

The queue holds every state whose Bellman error exceeds $\theta$, with that error as its priority. Line L8 can raise or lower a priority. With a [binary heap](/binary-heap/), the implementation does this by lazy deletion: it pushes a new entry and skips old entries when they come out. An indexed heap with a decrease-key operation also works. If $s$ has a self-loop, $s$ is its own predecessor and line L7 recomputes its error.

**Online form (Moore and Atkeson).** The agent keeps counts of its transitions. After each real step $(s, a, r, s')$ it updates the empirical model $\hat P(\cdot \mid s, a)$ and the mean reward $\hat R(s, a)$, adds $s$ to $\mathrm{pred}(s')$, puts $s$ into the queue with its new Bellman error, and runs lines L3 to L8 on the learned model for at most $n$ backups. Sutton and Barto give a version for a deterministic model that works with action values, as an extension of [Dyna-Q](/dyna-q/).

## Example

Take a chain of $n$ states $0, 1, \ldots, n-1$. Action right moves from $s$ to $s + 1$, action left moves to $s - 1$ (state 0 stays), and the last state is absorbing. The only reward is 1, for the step from $n - 2$ into $n - 1$. With $\gamma = 0.9$, $V^*(s) = 0.9^{\,n-2-s}$ for $s \le n - 2$.

Start from $V = 0$ with $n = 5$. Only state 3 has a positive Bellman error (1, from the reward of moving right), so line L2 puts only state 3 in the queue.

| step | state backed up | new value | predecessors checked | queue after |
| --- | --- | --- | --- | --- |
| 1 | 3 | 1 | 2 (error 0.9) | {2: 0.9} |
| 2 | 2 | 0.9 | 1 (error 0.81), 3 (error 0) | {1: 0.81} |
| 3 | 1 | 0.81 | 0 (error 0.729), 2 (error 0) | {0: 0.729} |
| 4 | 0 | 0.729 | 0 and 1 (error 0) | empty |

Four backups give the exact values. Synchronous value iteration needs one sweep for each step of the chain, plus one to see that nothing changes, so it does about $n^2$ backups. The tests count the backups with $\theta = 10^{-6}$:

| $n$ | 5 | 10 | 30 | 60 |
| --- | --- | --- | --- | --- |
| prioritized sweeping | 4 | 9 | 29 | 59 |
| synchronous value iteration | 25 | 100 | 900 | 3600 |

## Correctness

The method keeps an invariant: a state is in the queue exactly when its Bellman error exceeds $\theta$, and its priority is that error. A backup at $s$ changes only $V(s)$, so only the errors of $s$ and of the predecessors of $s$ can change. Line L4 removes $s$, after which its error is 0 unless $s$ is its own predecessor, and lines L6 to L8 recompute the rest. When the queue is empty, every error is at most $\theta$, so $\lVert TV - V\rVert_\infty \le \theta$, and the [contraction](/bellman-contraction/) of $T$ gives $\lVert V - V^* \rVert_\infty \le \theta/(1-\gamma)$.

The loop ends because each backup is applied to a state whose error exceeds $\theta$, and an infinite run of such backups would make the values of the states that are backed up infinitely often converge, so their errors would fall below $\theta$. The full proof is in the proofs section.

## Complexity

**One backup.** Line L5 costs $O(|S||A|)$ with dense transitions, or the number of nonzero transition probabilities of $s$. Lines L6 to L8 repeat this for up to $d$ predecessors and do up to $d$ heap operations. So one backup costs $O(d(|S||A| + \log h))$, where $h \le |S| + bd$ is the size of the heap with lazy deletion.

**Number of backups.** No useful worst-case bound is better than that of value iteration, because the method may back up the same states many times when the values depend on each other in cycles. The gain is on problems where the values flow in one direction, as on the chain above, where it does $n - 1$ backups against about $n^2$.

**Memory.** The predecessor lists take $O(|S|d)$ space and the heap $O(|S| + bd)$.

## Properties

- **Focused.** Work goes to the states whose values are changing, near the place where new information arrived. States far from any change are not touched.
- **Approximate.** The output satisfies $\lVert V - V^* \rVert_\infty \le \theta/(1-\gamma)$.
- **Online.** The online form spends a bounded amount of computation after each real step, which suits agents that act in real time.
- **Sensitive to the model.** In the online form the backups use the learned model, so early values can be wrong, and the method corrects them as the counts grow.

## Variants and improvements

- **Action values and deterministic models.** Sutton and Barto (Section 8.4) give the form for [Dyna-Q](/dyna-q/): the priority is the size of the one-step Q-learning update, and the predecessors are the pairs $(\bar s, \bar a)$ that the model predicts lead to $s$.
- **Other priorities.** Priorities can use the error times the transition probability into the changed state, as in Moore and Atkeson, or other estimates of the effect of a backup. Wingate and Seppi (2005) compare several such metrics.
- **Shortest path order.** For deterministic shortest path problems with nonnegative costs, backing up the state with the smallest tentative distance is [Dijkstra's algorithm](/dijkstra/), and every state needs one backup.
- **Sampled transitions.** [Prioritized experience replay](/prioritized-experience-replay/) brings the same idea to deep reinforcement learning: it replays stored transitions in the order of their TD error.
- **Trajectory-based ordering.** [Real-time dynamic programming](/real-time-dynamic-programming/) orders the backups along simulated trajectories from a start state instead.

## When to use it

Use prioritized sweeping when the model is known or learned, the state space is large, and the changes in value come from a few places, such as goals or newly discovered rewards. It is less useful when every state changes a little in each sweep, for example with dense random transitions, because the queue overhead then buys little. When the predecessors are hard to compute, as with a model given only as a simulator, it cannot be used directly.

## Pitfalls

- **Missing predecessors.** If $\mathrm{pred}(s)$ misses a state that can reach $s$, that state keeps an out-of-date value, and the invariant fails. In the online form, add $s$ to $\mathrm{pred}(s')$ for each observed transition.
- **Self-loops.** A state with a self-loop must be in its own predecessor list. Otherwise its error after a backup is not 0 and it is never put back in the queue.
- **Stale heap entries.** With lazy deletion, an old entry of a state can come out of the heap after the state was updated. Compare the entry with the current priority and skip it if they differ.
- **The threshold is not the error.** The output error can be up to $\theta/(1-\gamma)$, which is 100 times $\theta$ for $\gamma = 0.99$.

## Implementations

## History

Moore and Atkeson (1993) introduced prioritized sweeping as a way to get the data efficiency of model-based learning with a bounded computation per step. Peng and Williams (1993) independently proposed Queue-Dyna, which adds the same ordering to the Dyna architecture of Sutton (1990). Sutton and Barto present the method in Section 8.4 of their book, and Wingate and Seppi (2005) studied prioritization for large MDP solvers. Schaul and others (2016) carried the idea of ordering by error to deep reinforcement learning in [prioritized experience replay](/prioritized-experience-replay/).

## References
