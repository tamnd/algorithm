---
tag: D7J46M
kind: algorithm
slug: learning-real-time-a-star
name: "Learning real-time A*"
aliases:
- "LRTA*"
area: games-and-search/heuristic-search
level: research
summary: "Korf's real-time agent that stores the least cost plus value of the next move as the value of the state it leaves. The values stay lower bounds, and repeated trials converge to a shortest path."
solves: [single-pair-shortest-path]
model: word-ram
complexity:
  vars: {d: the largest number of successors of a state, v: the number of states that the agent visits}
  time: {per-move: O(d)}
  space: {extra: O(v)}
properties: {deterministic: true, recursive: false}
prereqs: [real-time-a-star, admissible-heuristic]
see_also: [real-time-dynamic-programming, value-iteration, consistent-heuristic, d-star-lite, online-algorithm, sliding-tile-puzzle, markov-decision-process]
sources:
  - paper: doi:10.1016/0004-3702(90)90054-4
    title: Richard E. Korf, Real-time heuristic search, Artificial Intelligence 42(2-3) (1990)
    locator: pp. 189 to 211; the section on Learning-RTA*, with the update rule, the lower bound property and the convergence over repeated trials
  - paper: doi:10.1016/0004-3702(94)00011-O
    title: Andrew G. Barto, Steven J. Bradtke and Satinder P. Singh, Learning to act using real-time dynamic programming, Artificial Intelligence 72(1-2) (1995)
    locator: pp. 81 to 138; the sections that relate real-time dynamic programming to LRTA* on deterministic problems
---

Learning real-time A* (LRTA*) is a search method for an agent that must make each move after a bounded amount of thought, and that solves the same problem again and again. In each state it looks at the neighbours, moves to the one with the least cost plus value, and stores that least value as the new value of the state it leaves. Richard Korf introduced it in 1990, together with [RTA*](/real-time-a-star/), which stores the second least value instead. With an admissible heuristic the values of LRTA* stay lower bounds on the true distances, so they can be kept from one trial to the next. Over repeated trials from the same start, the values grow, and in the end the agent walks a shortest path.

## In plain words

You walk to the same station every night through a dark town, and you can only see the next corners. At each corner you write down your best guess of the distance from it: the step to the best next corner plus the guess written there. Then you take that step.

The first nights you take wrong turns, because the guesses are too low. Each wrong turn raises some notes, so the next night the bad corners look worse. The notes are never too high, so you never give up a good way by mistake. After some nights the notes on your way are exact, and you walk the shortest way every night.

## The problem

The input is a graph of states with a start state $s$ and a goal state $g$, positive arc costs $c(x, y)$, and a heuristic $h_0(y)$ that estimates the cost from $y$ to the goal. The agent stands in one state at a time, and each move takes it along one arc. It must choose each move with a fixed amount of computation. A *trial* is one walk from $s$ to $g$, and its cost is the sum of the costs of its moves. The agent makes trials from the same start again and again and keeps its table of values between them. The task is to reach the goal in each trial, and to reach optimal trials after a finite number of trials.

For the learning to work, the heuristic must be [admissible](/admissible-heuristic/): $0 \le h_0(x) \le h^*(x)$, where $h^*(x)$ is the distance from $x$ to $g$. The goal must be reachable from every state.

## The algorithm

The agent keeps a table $H$ of values. A state not in the table has the value $h_0$. The table is kept from one trial to the next.

```pseudo id=main
LRTA*-TRIAL(s)
L1  x ← s
L2  while x ≠ g do
L3      for each successor y of x do f(y) ← c(x, y) + H(y)
L4      y_best ← a successor of x with the least f
L5      H(x) ← f(y_best)
L6      x ← y_best
L7  return the walk and whether a value changed
LRTA*-TRIALS(s)
L8  repeat
L9      run LRTA*-TRIAL(s)
L10     if the trial changed no value then stop
L11 return the costs of the trials
```

Line L5 is the only difference from RTA*, which stores the second least $f$ there. The least value is the cost of the best move from $x$ according to what the agent knows, so with an admissible $h_0$ it is never more than $h^*(x)$. The stop rule of line L10 is exact: a trial that changes no value is optimal, and every later trial would repeat it.

Korf also gives LRTA* a lookahead: the value of a successor in line L3 can come from a depth-limited search from it. This page uses a lookahead of one move.

## Example

The map is the one of the [RTA* page](/real-time-a-star/): a 4-connected grid of 5 columns and 3 rows, with unit costs. The cells $(3, 0)$ and $(3, 1)$ are walls. The agent starts at $(0, 0)$ and the goal is $(4, 0)$. The heuristic is the Manhattan distance, which does not see the wall. Ties are broken in the order east, west, south, north, where south is the next row. The first trial is:

| move | at | values of the successors $f$ | goes to | stores |
| --- | --- | --- | --- | --- |
| 1 | $(0, 0)$ | east 4, south 6 | $(1, 0)$ | 4 |
| 2 | $(1, 0)$ | east 3, west 5, south 5 | $(2, 0)$ | 3 |
| 3 | $(2, 0)$ | west 4, south 4 | $(1, 0)$ | 4 |
| 4 | $(1, 0)$ | east 5, west 5, south 5 | $(2, 0)$ | 5 |
| 5 | $(2, 0)$ | west 6, south 4 | $(2, 1)$ | 4 |
| 6 | $(2, 1)$ | west 5, south 5, north 5 | $(1, 1)$ | 5 |
| 7 | $(1, 1)$ | all four 6 | $(2, 1)$ | 6 |
| 8 | $(2, 1)$ | west 7, south 5, north 5 | $(2, 2)$ | 5 |

From $(2, 2)$ the agent goes east along the bottom row and up to the goal in four more moves, and it stores the exact values 4, 3, 2 and 1 on the way. The first trial has 12 moves. The shortest path has 8.

The dead end at $(2, 0)$ shows the learning. Its value goes from 2 to 4, and the value of $(1, 0)$ goes from 3 to 5, because the agent learns that the way east is blocked. Each stored value is at most the true distance: for example $(2, 0)$ stores 4 and its distance is 6.

The next trials cost 10, 8, 8 and 8 moves. The last trial changes no value, so the loop stops after five trials. At the end, every state on the last walk has its exact distance as its value: $(0, 0)$ has 8, $(1, 0)$ has 7, $(2, 0)$ has 6 and $(2, 1)$ has 5. In this example RTA* reaches the goal in 10 moves in its single trial, so the first trial of LRTA* is longer. The gain of LRTA* is in the later trials.

The sum of $h^*(x) - h_0(x)$ over the 13 open cells is $\Phi_0 = 18$. The trials cost $4 + 2 + 0 + 0 + 0 = 6$ moves more than the optimum in total, which is within the bound $\Phi_0$ of the proof.

**A measured experiment.** On 30 random 20 by 20 grids (each cell is a wall with probability 0.25, `random.Random(7)` of Python, the agent starts in a random cell of the component of the goal, Manhattan heuristic), the 30 first trials cost 1,310 moves and the 30 shortest paths cost 592. The trials until the stop rule were 371 in total, about 12 for each grid, and all trials together cost 13,791 moves. These are measurements on these grids, not bounds.

## Correctness

The [proof](proofs/correctness.md) assumes a finite graph with positive costs, an admissible $h_0$, and a goal that can be reached from every state.

- **Lower bounds.** Each stored value is at most the cost of a move along a shortest path plus the value there, so it is at most the true distance.
- **Cost identity.** A move costs exactly the new value of the state it leaves minus the value of the next state. Summed over a trial, the cost is the value of the start plus the rise of the sum of all values. Each trial is thus finite, and the excess cost over all trials together is at most $\Phi_0 = \sum_x (h^*(x) - h_0(x))$.
- **Convergence.** The values take finitely many forms. After the sum of values stops rising, every trial is optimal, and each trial moves the remaining errors on its walk one step back toward the start. A weighted sum of the errors then goes up in each trial that changes a value, so a trial that changes nothing comes. That trial is optimal, and the values on its walk are exact.
- **Consistent heuristics.** If $h_0$ is [consistent](/consistent-heuristic/), the table stays consistent and no value goes down.

The heuristic need not be admissible for one trial to reach the goal: the proof of [RTA*](/real-time-a-star/) works for the least value as well as for the second least. Without admissibility the values are not lower bounds, and the convergence to optimal trials can fail.

## Complexity

The model is the [word RAM](/word-ram/). A move with a lookahead of one looks at the $d$ successors of the state, in $O(d)$ time. The table holds a value for each state that the agent has left, so the space is $O(v)$ for $v$ visited states.

The number of moves follows from the proof. A trial costs at most $h_0(s) + \Phi_0$. With unit costs and $h_0 = 0$ on a graph of $n$ states, each distance is at most $n - 1$, so $\Phi_0 \le n(n - 1)$ and the first trial makes at most $n(n - 1)$ moves. With integer costs and an integer $h_0$, at most $\Phi_0$ trials are not optimal, and with a consistent $h_0$ there are at most $\Phi_0 + 1$ trials in total, because each trial that changes a value raises the sum of the values.

## Properties

- **Bounded work per move.** The work per move is fixed by the lookahead depth, not by the size of the problem.
- **Complete** in each trial, in finite graphs where the goal can be reached from every state.
- **Admissible values.** With an admissible $h_0$, the values never exceed the true distances.
- **Converges.** Repeated trials from the same start reach an optimal trial, and the values on its walk are exact. States off the optimal walks can keep values that are too low.
- **Not optimal in one trial.** A single trial can be much longer than a shortest path.

## Variants and improvements

- **Real-time A*.** [RTA*](/real-time-a-star/) stores the second least value. It is often better in a single trial, but its values can be too high and cannot be kept for later trials.
- **Real-time dynamic programming.** On deterministic problems LRTA* is a special case of [real-time dynamic programming](/real-time-dynamic-programming/), which does the same update with expected costs on [Markov decision processes](/markov-decision-process/). The update is the Bellman update of [value iteration](/value-iteration/), done only at the state of the agent.
- **Deeper lookahead and local search spaces.** Korf's lookahead uses a depth-limited search before each move. Later methods run a bounded A* search before each move and update the values of the whole searched region with a Dijkstra-like pass, which makes the learning faster.
- **Weighted values.** Some later methods multiply the heuristic by a weight above 1, which gives faster convergence to paths that are only near optimal.

## When to use it

Use LRTA* when an agent must move before it can plan a full path, and the same problem comes back many times, for example game units that walk the same map often, or a robot that does the same delivery each day. If the problem is solved only once, RTA* often gives a shorter walk. If there is time to plan the full path, [A*](/a-star-search/) gives an optimal path at once. For a robot whose map changes while it moves, use [D* Lite](/d-star-lite/). The [sliding-tile puzzles](/sliding-tile-puzzle/) were the test problems of the first papers on real-time search.

## Pitfalls

- **An inadmissible heuristic.** Each trial still reaches the goal, but values can be too high, and the trials may settle on a path that is not optimal.
- **Expecting values to rise.** With an inconsistent admissible heuristic, line L5 can lower a value. The convergence still holds, but a proof or a test that assumes rising values is wrong in that case.
- **A stop rule on cost.** Two trials with the same cost do not show convergence. Stop when a trial changes no value, as in line L10.
- **Dead ends.** In a directed graph with a state from which the goal cannot be reached, the agent can walk into it and never stop.
- **Many trials.** With a weak heuristic, such as $h_0 = 0$, the first trials explore much of the graph. The bound $n(n - 1)$ for the first trial shows how bad it can be.

## Implementations

## History

Korf introduced LRTA* in 1990, in Artificial Intelligence 42, in the same paper as RTA* and minimin lookahead. He showed that the values of LRTA* stay admissible and that repeated trials converge to optimal paths, and he tested it on sliding-tile puzzles. Barto, Bradtke and Singh (1995) showed that LRTA* is real-time dynamic programming on deterministic problems, which linked it to reinforcement learning. Later work by Ishida, Shimbo, Koenig, Bulitko and others gave many variants, mostly for path finding in games.

## References
