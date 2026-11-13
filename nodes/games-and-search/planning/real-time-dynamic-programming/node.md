---
tag: X8DWC2
kind: algorithm
slug: real-time-dynamic-programming
name: Real-time dynamic programming
aliases:
- RTDP
area: games-and-search/planning
level: advanced
summary: Solve a stochastic shortest path problem from one start state by simulated trials. Each trial acts greedily and backs up only the states it visits, from an admissible start.
solves: [stochastic-shortest-path]
model: real-ram
complexity:
  vars: {L: the number of steps in one trial (the time bound is for one trial), A: the number of actions in a state, B: the number of outcomes of an action, S: the number of states}
  time: {worst: O(L A B)}
  space: {extra: O(S)}
properties: {deterministic: false, online: true, exact: false, recursive: false}
history:
  year: 1995
  people: [Andrew G. Barto, Steven J. Bradtke, Satinder P. Singh]
  note: Barto, Bradtke and Singh defined trial-based RTDP as a stochastic form of Korf's learning real-time A* and proved that it converges on the relevant states from an admissible start.
prereqs: [stochastic-shortest-path, bellman-equation, admissible-heuristic]
see_also: [learning-real-time-a-star, value-iteration, prioritized-sweeping, rollout-algorithm, monte-carlo-tree-search, mdp-planning, pomdp-planning, consistent-heuristic]
sources:
  - paper: doi:10.1016/0004-3702(94)00011-O
    title: Andrew G. Barto, Steven J. Bradtke and Satinder P. Singh, Learning to act using real-time dynamic programming, Artificial Intelligence 72(1-2), 1995
    locator: pp. 81 to 138 (trial-based RTDP, its relation to learning real-time A* and asynchronous dynamic programming, and convergence on the relevant states)
  - paper: "Blai Bonet and Hector Geffner, Labeled RTDP: improving the convergence of real-time dynamic programming, Proceedings of ICAPS 2003"
    locator: pp. 12 to 21 (the solved labels, the residual test and the comparison with RTDP, LAO* and value iteration)
  - paper: doi:10.1016/S0004-3702(01)00106-0
    title: "Eric A. Hansen and Shlomo Zilberstein, LAO*: a heuristic search algorithm that finds solutions with loops, Artificial Intelligence 129(1-2), 2001"
    locator: pp. 35 to 62 (heuristic search from a start state in a cyclic MDP)
  - book: isbn:9781608458868
    title: Mausam and Andrey Kolobov, Planning with Markov Decision Processes, An AI Perspective, Morgan and Claypool, 2012
    locator: Chapter 4 (heuristic search from an initial state, RTDP and LRTDP)
  - book: isbn:9781608459698
    title: Hector Geffner and Blai Bonet, A Concise Introduction to Models and Methods for Automated Planning, Morgan and Claypool, 2013
    locator: Section 6.3 (heuristic search for MDPs, RTDP and LRTDP)
---

Real-time dynamic programming (RTDP) solves a [stochastic shortest path problem](/stochastic-shortest-path/) for one start state $s_0$. It runs trials. Each trial starts at $s_0$, picks the greedy action under the current values, backs up the value of the current state with the [Bellman equation](/bellman-equation/), and samples the next state, until it reaches a goal. The values start from an [admissible heuristic](/admissible-heuristic/), a lower bound on the optimal cost. With positive costs, Barto, Bradtke and Singh (1995) proved that the values converge to the optimal costs on the states that an optimal policy reaches from $s_0$, and that other states can keep their start values for ever. So RTDP can solve problems whose full state space is too large for [value iteration](/value-iteration/). It is the stochastic form of [learning real-time A*](/learning-real-time-a-star/).

## In plain words

You must plan a trip where each move can go wrong, and you start from one fixed place. You do not plan for every place in the world. You walk through the trip in your head again and again. At each step you take the move that looks cheapest now, you write down a new guess of the cost from this place, and you let chance decide where the move takes you.

The first guesses are too low, never too high. So a bad move looks good at first, you try it, and its guess goes up. A good move stays good. After many walks, the guesses on the places that the best plan uses are correct. Places that no good plan goes to are seldom or never seen, and you do no work on them.

## The problem

The input is a stochastic shortest path problem: a finite set $S$ of states, a set $G \subseteq S$ of goal states, a start state $s_0$, for each state $s \notin G$ a set $A(s)$ of actions, a cost $c(s, a) > 0$ and a distribution $P(\cdot \mid s, a)$ over the next states. The goal states are absorbing and cost nothing. From every state that a policy can reach from $s_0$, some policy reaches $G$ with probability 1. The output is a policy that is optimal from $s_0$, together with the optimal cost $V^*(s)$ on the states that this policy reaches.

The algorithm also takes a function $h$ with $h \le V^*$ and $h = 0$ on $G$. For the proof on this page, $h$ is also monotone: $h(s) \le \min_a Q_h(s, a)$, with

$$Q_V(s, a) = c(s, a) + \sum_{s'} P(s' \mid s, a) \, V(s'), \qquad V = 0 \text{ on } G.$$

## The algorithm

$V$ is a table. A state that is not in the table has the value $h(s)$, and line L1 enters it when it is first seen. The call runs $K$ trials.

```pseudo id=main
RTDP(M, s0, h, K)
L1  V(s) ← h(s) for each state s, entered when s is first seen
L2  repeat K times                                  ▷ one trial
L3      s ← s0
L4      while s ∉ G do
L5          a ← an action in A(s) of least Q_V(s, a)   ▷ ties: first action
L6          V(s) ← Q_V(s, a)                         ▷ the Bellman backup at s
L7          s ← a sample from P(· | s, a)
L8  return V and the greedy policy of V
```

Line L5 is the greedy choice. It looks at each action of $s$ and each outcome of each action. Line L6 sets $V(s)$ to the right side of the Bellman equation at $s$. Line L7 is a simulation: it draws the next state from the model. A trial backs up only the states it visits, and it looks up the values of their successors.

The values of the greedy choice decide where the trials go. A state looks cheap while its value is low. The trials go there, the backups raise its value, and the trials go to the other places when the value is high enough. This is how RTDP explores. It needs no random choice of actions.

## Example

A boat is in a channel at the mile marks $1, \ldots, 10$. The dock is the goal $0$. At each mark $s$ there are two actions.

- **row** costs 2 and moves to $s - 1$.
- **sail** costs 1. At $s = 1$ it reaches the dock or is pushed to 2, each with probability $1/2$. At $s \ge 2$ it moves to $s - 1$ with probability $2/3$ and to $\min(s + 1, 10)$ with probability $1/3$.

The optimal costs are $V^*(s) = 2s$ for $s \le 9$, with row, and $V^*(10) = 39/2$, with sail. The start is $s_0 = 3$. The heuristic $h(s) = s$ is the cost when each action has its best outcome. It is admissible and monotone.

The first trial, with the seed 1 of the implementation, is below. Each line shows the two Q-values at the current state, the greedy action and the new value.

| step | $s$ | Q(row) | Q(sail) | action | new $V(s)$ | next state |
|---|---|---|---|---|---|---|
| 1 | 3 | 4 | 3.667 | sail | 3.667 | 2 |
| 2 | 2 | 3 | 2.889 | sail | 2.889 | 3 |
| 3 | 3 | 4.889 | 4.259 | sail | 4.259 | 4 |
| 4 | 4 | 6.259 | 5.506 | sail | 5.506 | 3 |
| 5 | 3 | 4.889 | 4.761 | sail | 4.761 | 2 |
| 6 | 2 | 3 | 3.254 | row | 3 | 1 |
| 7 | 1 | 2 | 2.5 | row | 2 | 0 |

At first the low heuristic makes sail look cheaper than row. Each backup at 2 and 3 raises the value of sail there, until row wins at 2. The trials have the lengths 7, 7, 3 and 7. After the fourth trial, $V(1), V(2), V(3) = 2, 4, 6$, which are the optimal costs, and the greedy policy rows from 3 to the dock. Each later trial has 3 steps and changes no value. The four trials made 24 backups. The states $6, \ldots, 10$ were never backed up, and $V(4) \approx 7.18$ and $V(5) = 7.28$ are still below $V^*(4) = 8$ and $V^*(5) = 10$. This is correct: no optimal trajectory from 3 goes there. Value iteration from 0 needs 42 sweeps, which is 420 backups, to make all ten values correct to $10^{-9}$.

## Correctness

Two facts carry the proof. First, the values stay admissible and monotone, $V \le V^*$ and $V \le TV$, where $T$ is the Bellman operator. So a backup only raises a value, and each value has a limit $V_\infty \le V^*$. Second, a set of states that a policy cannot leave without the goal has no finite cost when each cost is positive. From this, each trial ends with probability 1. Let $C$ be the set of states that infinitely many trials visit; it contains $s_0$. In the limit, the actions that the trials keep taking at $C$ are greedy and keep the process in $C \cup G$, and $V_\infty$ satisfies their Bellman equations. So these actions form a proper policy $\mu$ with cost $V_\mu = V_\infty \le V^*$. Since $V^* \le V_\mu$, all three are equal on $C$, and $\mu$ is optimal from $s_0$. The full proof is below.

The theorem says nothing about the states outside $C$. Their values are lower bounds and need not be close to $V^*$, as the states 4 and 5 of the example show.

## Complexity

One backup at $s$ costs $O(A B)$ arithmetic operations, where $A$ is the number of actions at $s$ and $B$ is the largest number of outcomes of an action. A trial of $L$ steps costs $O(L A B)$. The table holds only the states that the trials visit or see as outcomes, which is at most $S$ states and often far fewer.

There is no bound on the number of trials that plain RTDP needs. The convergence is only in the limit, and plain RTDP has no test that tells when the values are correct. Labeled RTDP adds such a test. The number of trials also depends on the heuristic: a value that is far below $V^*$ must be raised by many backups before the trials leave it.

## Properties

- **Focused.** The trials go only where the greedy policy and the model take them. States that no good policy reaches from $s_0$ need not be backed up.
- **Anytime and online.** The table is a valid lower bound at each moment, and the greedy policy can be used at each moment. An agent can act on the real system while it runs trials, and this is the sense of "real time" in the name.
- **Asynchronous.** RTDP is asynchronous [value iteration](/value-iteration/) that picks the states to back up by simulation. The backups at one state use the newest values of the others.
- **Randomized.** The trials sample the outcomes. Two runs with different seeds back up different states, but both converge on the relevant states.
- **Lower bound.** With an admissible start, $V(s_0)$ never exceeds $V^*(s_0)$ and does not go down.

## Variants and improvements

- **Labeled RTDP (LRTDP).** Bonet and Geffner (2003) mark a state as solved when every state of the greedy graph below it has a residual under $\varepsilon$. A trial stops at a solved state, and the run stops when $s_0$ is solved. This gives a stopping rule and a faster convergence.
- **Learning real-time A*.** When each action has one outcome, a trial of RTDP is a trial of [LRTA*](/learning-real-time-a-star/). [Real-time A*](/real-time-a-star/) is a related method for one trial in a deterministic space.
- **LAO\*.** Hansen and Zilberstein (2001) expand a best partial policy graph from $s_0$ and run value iteration on it. It is a systematic search over the same relevant states, without sampling.
- **Upper bounds.** Some variants keep an upper bound as well as the lower bound, and send the trials to states where the gap is large. The gap at $s_0$ is then a stopping rule.
- **Dead ends.** If some state has no proper policy, a trial can stay among such states for ever. With a finite penalty for giving up, as in the class fSSPUDE of the [stochastic shortest path](/stochastic-shortest-path/) page, RTDP applies again.
- **Discounted problems.** RTDP applies to a discounted MDP from a start state, as one form of [MDP planning](/mdp-planning/). The discount makes each trial end with probability 1 in the reduction to an SSP.
- **POMDPs.** RTDP can run over beliefs, which are the states of [POMDP planning](/pomdp-planning/), when the beliefs are discretized or a table is kept only for the beliefs that the trials see.

## When to use it

Use RTDP when the model is known, there is one start state, the state space is too large to sweep, and a good admissible heuristic exists. Then most states are not relevant, and RTDP does not touch them. Use [value iteration](/value-iteration/) or policy iteration when you need a policy for every state, or when the state space is small. Use LRTDP or a version with an upper bound when you need to know when to stop. When the model is not known and only a simulator is available, use sampling methods such as [Monte Carlo tree search](/monte-carlo-tree-search/) or a [rollout algorithm](/rollout-algorithm/).

## Pitfalls

- **An inadmissible start.** If $h(s) > V^*(s)$ at some state, the trials can avoid a good action for ever, and the result need not be optimal.
- **Zero-cost cycles.** The proof uses $c \ge c_{\min} > 0$. With a cycle of zero cost, a trial can run for ever with no change of value. Cap the length of a trial, as the implementation does.
- **Dead ends.** A state with no way to the goal has $V^* = \infty$. Its value rises without bound, and a trial that falls into it does not end. Detect such states or add a penalty for giving up.
- **Reading the wrong values.** Only the values on the states that the optimal policy reaches from $s_0$ converge. The values on other states are lower bounds, not costs.
- **No stopping rule.** A run of $K$ trials does not certify anything. Check the residual $|V(s) - Q_V(s, \pi(s))|$ on the greedy graph from $s_0$, or use LRTDP.
- **A start value of 0 for new states.** If new states get the value 0 in place of $h(s)$, the values stay admissible but the information in $h$ is lost.

## Implementations

## History

Korf (1990) introduced learning real-time A* for deterministic search. Barto, Bradtke and Singh (1995) gave RTDP as its form for stochastic problems, placed it in the theory of asynchronous dynamic programming, and proved convergence on the relevant states from an admissible start. Hansen and Zilberstein (2001) gave LAO\*, a heuristic search for cyclic MDPs. Bonet and Geffner (2003) added solved labels in LRTDP, which gave RTDP a stopping rule and made it faster.

## References
