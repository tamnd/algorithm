---
tag: YMQYKM
kind: algorithm
slug: real-time-a-star
name: "Real-time A*"
aliases:
- "RTA*"
area: games-and-search/heuristic-search
level: research
summary: "Korf's agent that must act before it has a plan: it moves to the neighbour with the least cost plus value and stores the second-best value for the state it leaves, so it never loops forever."
solves: [single-pair-shortest-path]
model: word-ram
complexity:
  vars: {d: the largest number of successors of a state, v: the number of states that the agent visits}
  time: {per-move: O(d log d)}
  space: {extra: O(v)}
properties: {deterministic: true, recursive: false}
prereqs: [a-star-search, admissible-heuristic]
see_also: [learning-real-time-a-star, online-algorithm, real-time-dynamic-programming, d-star-lite, sliding-tile-puzzle, bug-algorithms]
sources:
  - paper: doi:10.1016/0004-3702(90)90054-4
    title: Richard E. Korf, Real-time heuristic search, Artificial Intelligence 42(2-3) (1990)
    locator: pp. 189 to 211; minimin lookahead with alpha pruning, Real-Time-A* and its update rule, Theorem 1 (completeness), Theorem 2 (locally optimal moves on trees), and Learning-RTA*
---

Real-time A* (RTA*) is a search method for an agent that must make each move after a bounded amount of thought, before it knows a full path to the goal. It looks only at the states next to it, moves to the one that looks cheapest, and writes down, for the state it leaves, the cost of the best other way out of it. This note keeps the agent from going around the same loop for ever. Richard Korf introduced it in 1990, together with its learning form [LRTA*](/learning-real-time-a-star/). The moves of RTA* are not optimal, but it reaches the goal in every finite graph where the goal can be reached from every state.

## In plain words

You are lost in a town at night and you want to reach the station. At each corner you can only see the next corners and guess their distance to the station. You walk to the corner that looks best.

Before you leave, you write on the corner how good your second choice was. If you ever come back to this corner, the way you took the first time did not work, so the honest cost of this corner is its second choice. Each time you go around a loop, the notes on the loop get higher, and soon some corner off the loop looks better. So you cannot walk in the same circle for ever.

## The problem

The input is a graph of states with a start state and a goal state $g$, positive arc costs $c(x, y)$, and a heuristic $h_0(y)$ that estimates the cost from $y$ to the goal. The agent stands in one state at a time, and each move takes it along one arc. It must choose each move with a fixed amount of computation. The task is to reach the goal, and the cost of the solution is the sum of the costs of the moves, including the moves that turn out to be useless.

This differs from offline search such as [A*](/a-star-search/), which plans the full path before the first move, and whose cost is the planning time. Here the planning per move is bounded and the agent pays for the moves. The setting is an [online problem](/online-algorithm/): the agent learns the graph only as it walks.

## The algorithm

The agent keeps a table $H$ of values for the states that it has left. A state not in the table has the value $h_0$.

```pseudo id=main
RTA*(s, g, h0)
L1  H ← an empty table
L2  x ← s, walk ← [s]
L3  while x ≠ g do
L4      for each successor y of x do f(y) ← c(x, y) + (H(y) if y ∈ H else h0(y))
L5      y_best ← a successor of x with the least f
L6      if x has at least two successors then H(x) ← the second least value of f
L7      else H(x) ← f(y_best)
L8      x ← y_best, append x to walk
L9  return walk
```

Line L6 is the key rule. If the agent comes back to $x$ later, the move to $y_{best}$ did not lead to the goal, so the best that it can expect from $x$ is the next move. A tie counts twice: if two successors have the least $f$, the second least value is that same value. When $x$ has only one successor, there is no second value. This page then stores the least value (line L7), which keeps all values finite.

Korf's RTA* can look further ahead: before each move it runs a depth-limited search, called *minimin lookahead*, from each successor, and uses the least value at the frontier of that search as $h_0$. Alpha pruning cuts the lookahead search. Line L4 is the case of a lookahead of one move.

## Example

The map is a 4-connected grid of 5 columns and 3 rows, with unit costs. The cells $(3, 0)$ and $(3, 1)$ are walls. The agent starts at $(0, 0)$ and the goal is $(4, 0)$, on the other side of the wall. The heuristic is the Manhattan distance, which does not see the wall. Ties are broken in the order east, west, south, north, where south is the next row.

| move | at | values of the successors $f$ | goes to | stores |
| --- | --- | --- | --- | --- |
| 1 | $(0, 0)$ | east 4, south 6 | $(1, 0)$ | 6 |
| 2 | $(1, 0)$ | east 3, west 7, south 5 | $(2, 0)$ | 5 |
| 3 | $(2, 0)$ | west 6, south 4 | $(2, 1)$ | 6 |
| 4 | $(2, 1)$ | west 5, south 5, north 7 | $(1, 1)$ | 5 |
| 5 | $(1, 1)$ | all four 6 | $(2, 1)$ | 6 |
| 6 | $(2, 1)$ | west 7, south 5, north 7 | $(2, 2)$ | 7 |

From $(2, 2)$ the way east along the bottom row is free, and four more moves reach the goal. The walk has 10 moves, while the shortest path has 8.

In move 2 the value 7 of the west neighbour comes from the table: $(0, 0)$ stored 6 in move 1, and $1 + 6 = 7$. In move 5 the agent goes back to $(2, 1)$ because all values are equal. In move 6 the stored value of $(1, 1)$ makes the west move cost 7, so the agent takes the south move. The values stored for $(2, 1)$ are first 5, then 7. Its distance to the goal is 5, so the second value is too high: the values of RTA* are not lower bounds.

**A measured experiment.** On 50 random 20 by 20 grids (each cell is a wall with probability 0.25, `random.Random(7)` of Python, the agent starts in a random cell of the component of the goal, Manhattan heuristic), the 50 walks of RTA* cost 1,750 moves in total, and the 50 shortest paths cost 1,026. So the walks were about 1.7 times as long as the shortest paths. This is a measurement on these grids, not a bound.

## Correctness

The [proof](proofs/correctness.md) shows that RTA* reaches the goal in every finite graph with positive costs and a finite heuristic, when the goal can be reached from every state. This is Theorem 1 of Korf (1990).

- **The update rule.** The value stored for the state that the agent leaves is at least the cost of the move plus the value of the next state.
- **No endless loop.** If the agent stayed in a set of states for ever, each pass over the set would raise the least value in it by at least the least arc cost. The values outside the set do not change. So in the end a state of the set with an arc out of it would prefer that arc, which is a contradiction.

The heuristic need not be admissible for this. The condition that the goal can be reached from every state matters: in a graph with a dead end, the agent can walk into it and never come out.

Korf also proved that on a tree, RTA* with lookahead makes moves that are optimal given the information that it has (his Theorem 2). On graphs with cycles this does not hold. The [proof](proofs/correctness.md) of this page does not cover that theorem.

## Complexity

The model is the [word RAM](/word-ram/). A move with a lookahead of one looks at the $d$ successors of the state and finds the least and second least values. This page sorts them, in $O(d \log d)$ time, and two passes give the same in $O(d)$. With lookahead to depth $k$, a move costs $O(d^k)$ in the worst case, less with alpha pruning. The table holds a value for each state that the agent has left, so the space is $O(v)$ for $v$ visited states.

No bound on the number of moves is given here. The number of moves depends on the graph and the heuristic. The proof only shows that it is finite. In the experiment above, the walks were about 1.7 times the shortest paths.

## Properties

- **Bounded work per move.** The work per move is fixed by the lookahead depth, not by the size of the problem.
- **Complete** in finite graphs where the goal can be reached from every state.
- **Not optimal.** The walk can be longer than a shortest path, and it can visit a state more than once.
- **Values are not lower bounds.** The stored second-best values can be larger than the true distances, so they are not reused across trials.
- **No heuristic condition.** Completeness needs only a finite heuristic. A better heuristic gives shorter walks.

## Variants and improvements

- **Learning RTA*.** [LRTA*](/learning-real-time-a-star/) stores the least value instead of the second least. Its values stay lower bounds when the heuristic is admissible, and over repeated trials from the same start they converge to the true distances along a shortest path.
- **Deeper lookahead.** A larger lookahead gives better moves for more work per move. Korf found that the best depth depends on how expensive moves are compared with computation.
- **Real-time dynamic programming.** On deterministic problems LRTA* is a special case of [real-time dynamic programming](/real-time-dynamic-programming/), which extends the idea to stochastic problems.
- **Later real-time methods.** Many later methods, such as LSS-LRTA* by Koenig and Sun, run an A* search of bounded size before each move and update the values of the whole searched region.

## When to use it

Use RTA* when an agent must move before it can plan a full path, for example a game unit that must act each frame, or a robot whose planner must answer within a fixed time. It suits a single trial in a new graph. If the agent solves the same problem many times, use LRTA*, which learns. If there is time to plan the full path, A* gives an optimal path. For a robot that replans a full shortest path after each change of its map, use [D* Lite](/d-star-lite/). The [sliding-tile puzzles](/sliding-tile-puzzle/) were the test problems of the first papers on real-time search.

## Pitfalls

- **Storing the least value.** That is LRTA*, not RTA*. With a single trial it works too, but it is a different rule with different properties.
- **Reusing the table as a heuristic.** The second-best values of RTA* can be too high, so a later A* search with them may return paths that are not optimal.
- **Dead ends.** In a directed graph with a state from which the goal cannot be reached, RTA* can walk into it and never stop.
- **Ties.** With many equal values, as on open grids, the agent can step back and forth. A fixed tie rule makes runs repeatable but does not remove the extra moves.

## Implementations

## History

Korf introduced real-time heuristic search in 1990, in Artificial Intelligence 42, building on his work in 1987 and 1988 on single-agent search under a time limit. He gave minimin lookahead with alpha pruning, RTA* and LRTA*, and he tested them on sliding-tile puzzles. Barto, Bradtke and Singh (1995) showed that LRTA* is a case of real-time dynamic programming. Later work by Ishida, Koenig, Bulitko and others gave many real-time search methods, mostly for path finding in games.

## References
