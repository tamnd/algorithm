---
tag: 9VT1PP
kind: algorithm
slug: prioritized-multi-robot-planning
name: Prioritized multi-robot planning
aliases:
- Erdmann-Lozano-Perez prioritized planning
area: robotics/multi-robot-systems
level: core
summary: Plan robots one at a time in a fixed priority order, each one treating the paths of the robots before it as moving obstacles in space-time.
solves: [multi-agent-pathfinding]
model: word-ram
complexity:
  vars: {r: the number of robots, g: the number of free grid cells, H: the time horizon in steps}
  time: {total: O(r g H log(g H))}
  messages: {total: O(r)}
  space: {extra: O(g H + r H)}
properties: {deterministic: true, randomized: false, online: false, complete: false}
history:
  year: 1987
  people: [Michael Erdmann, Tomas Lozano-Perez]
  note: Erdmann and Lozano-Perez gave each moving object a priority and planned it in configuration space-time among the objects of higher priority.
prereqs: [multi-agent-pathfinding, a-star-search, coupled-and-decoupled-planning]
see_also: [conflict-based-search, pebble-motion-on-graphs, configuration-space, motion-planning, multi-robot-system, sliding-tile-puzzle]
sources:
  - paper: doi:10.1007/BF01840371
    title: Michael Erdmann and Tomas Lozano-Perez, On multiple moving objects, Algorithmica 2, 1987
    locator: pages 477 to 521 (priorities, configuration space-time and planning among moving obstacles)
  - book: isbn:9780521862059
    title: Steven M. LaValle, Planning Algorithms, Cambridge University Press, 2006
    locator: Chapter 7, the section on multiple robots (decoupled planning and prioritized planning)
  - book: isbn:9783319325507
    title: Bruno Siciliano and Oussama Khatib (editors), Springer Handbook of Robotics, 2nd edition, Springer, 2016
    locator: the chapter on multiple mobile robot systems (path coordination and priorities)
---

Prioritized planning finds collision-free paths for several robots by planning them one at a time in a fixed order. Each robot searches in space-time and treats the planned paths of all robots before it as moving obstacles, so it never has to search the joint space of the team. It is the simplest *decoupled* method on the [coupled and decoupled planning](/coupled-and-decoupled-planning/) page: it is fast and usually good, but unlike [conflict-based search](/conflict-based-search/) or a search of the joint space for [multi-agent pathfinding](/multi-agent-pathfinding/), it is incomplete and can fail on instances that have a solution.

## In plain words

The robots take turns, by rank. The first robot plans the shortest route to its goal as if it were alone. The second robot plans its route while it keeps out of the way of the first, and it may wait or step aside to let the first robot pass. The third one keeps out of the way of both, and so on. Each robot writes down where it will be at each moment, and the later robots read this list.

This is quick, because each robot plans only for itself. The weak point is that a robot with a high rank never makes room for the robots after it. If the first robot parks in the only doorway, the others can never get through, even if a better plan for the whole team exists.

## The problem

**The model.** The workspace is a 4-connected grid with $g$ free cells. Time is discrete and synchronous: in each step every robot moves to a neighbor cell or waits. There are $r$ robots, each with a start cell and a goal cell. Two robots must never be in the same cell at the same time (a *vertex conflict*) and must never swap cells in one step (a *swap conflict*). A robot that reaches its goal stays there. The plans are computed by one planner, or by the robots in turn: robot $k$ receives the plans of robots $1$ to $k - 1$ and broadcasts its own, so the team sends $r$ plan messages in $r$ sequential rounds over any graph that can broadcast.

**Input.** The grid, the starts and goals, a priority order of the robots, and a time horizon $H$.

**Output.** One path per robot with no vertex or swap conflicts, or the answer "no plan found".

**How it differs from close pages.** [Multi-agent pathfinding](/multi-agent-pathfinding/) is the problem on a general graph, and [conflict-based search](/conflict-based-search/) solves it optimally and completely by splitting on conflicts. A coupled search over the joint space is complete but grows exponentially with $r$; the [coupled and decoupled planning](/coupled-and-decoupled-planning/) page compares the two families. [Pebble motion on graphs](/pebble-motion-on-graphs/) asks only whether the robots can reach their goals, one move at a time, and is decidable in polynomial time. Prioritized planning is the greedy end of this range.

## The algorithm

```pseudo id=main
PRIORITIZED-PLANNING(grid, starts, goals, order, H)
L1  R ← an empty reservation table of (cell, time) and (move, time)
L2  for each robot k in order do
L3      π_k ← space-time A* from (s_k, 0) to g_k that avoids every entry of R, up to time H
L4      if π_k = none then return none
L5      add every (cell, time) and every move of π_k to R, and hold g_k from the arrival time on
L6  return π_1, ..., π_r
```

Line L3 runs [A*](/a-star-search/) on states $(c, t)$, a cell and a time, with the Manhattan distance to the goal as the heuristic. A state is blocked if an earlier robot is in cell $c$ at time $t$, also when it has parked there; a move from $c$ to $c'$ is forbidden if an earlier robot moves from $c'$ to $c$ in the same step. The search may end at the goal only at a time after which no earlier robot passes the goal, since the robot will park there. The waiting move keeps the robot in place, so a robot can let others pass. Line L5 writes the plan into the table, and parks the robot at its goal for ever.

In the code the default horizon is $H = g (r + 1)$, a design choice, not a bound from the paper.

## Example

The pocket grid has 2 rows and 4 columns, with a single free cell in row 0 above column 1:

```
row 0:  #  .  #  #
row 1:  .  .  .  .
```

Robot 0 starts at $(1, 0)$ and must reach $(1, 3)$. Robot 1 starts at $(1, 3)$ and must reach $(1, 0)$. They must pass each other in the corridor.

**Order 0, then 1.** Robot 0 takes its shortest path along row 1 and reaches $(1, 3)$ at time 3. Robot 1 now needs to step into the pocket $(0, 1)$, but it cannot get there before robot 0 passes, and it cannot swap with robot 0. The search returns no plan.

**Order 1, then 0.** Robot 1 takes $(1, 3), (1, 2), (1, 1), (1, 0)$. Robot 0 plans around it: $(1, 0), (1, 1), (0, 1), (1, 1), (1, 2), (1, 3)$. It steps into the pocket at time 2, while robot 1 passes below, and arrives at time 5. A search of the joint space also finds makespan 5, so this order is optimal here.

**No order works.** On the grid with rows `....` and `..##`, robot 0 starts at $(0, 2)$ with goal $(0, 1)$, and robot 1 starts at $(0, 0)$ with goal $(0, 3)$. Prioritized planning fails for both orders, but a joint plan with makespan 4 exists: robot 0 moves to $(0, 1)$, steps down to $(1, 1)$ to let robot 1 pass, and steps back. In each order, the first robot takes its shortest path and blocks the other.

## Correctness

The [proof](proofs/correctness/) shows three theorems. *Soundness*: if line L6 returns plans, no two of them have a vertex or swap conflict, also after the robots park. *Greedy optimality per robot*: robot $k$ gets the earliest arrival time among all plans that avoid robots $1$ to $k - 1$, because A* with a consistent heuristic finds the earliest final goal state. *Incompleteness*: the 2-robot instance above has a plan with makespan 4, and prioritized planning fails for both orders and every horizon.

## Complexity

- **Time (theorem).** One space-time search visits at most $g (H + 1)$ states with 5 moves each, so it costs $O(g H \log(g H))$ with a binary heap. The whole method costs $O(r g H \log(g H))$ in the [word RAM](/word-ram/) model.
- **Memory.** The reservation table holds one entry per step of every plan, $O(r H)$, and one search holds $O(g H)$ states.
- **Messages.** If the robots plan in turn, each one broadcasts one plan of $O(H)$ cells, $r$ messages in $r$ sequential rounds.
- **Compared with coupled search.** A search of the joint space has up to $g^r$ states per time step, which is the price of completeness.

## Properties

- **Sound (theorem).** Returned plans never collide.
- **Incomplete (theorem).** It can fail when a plan exists, for every order.
- **Not optimal for the team.** Each robot is optimal given the robots before it, but the makespan or the sum of path lengths can be far from the best.
- **Order dependent.** The pocket example succeeds in one order and fails in the other.
- **Scales well (measurement).** In the tests, with 2 or 3 robots on random grids of up to 3 by 4 cells, it solved more than 50 of 250 instances and failed on some that the joint search solved; it never returned a conflicting plan.

## Variants and improvements

- **Cooperative A*.** Silver (2005) reserved space-time cells in a shared table for game characters, which is this method with a window of limited length.
- **Choosing the order.** Heuristics give priority to the robot with the longest path, or to robots whose start or goal blocks others. Searching over orders, or restarting with a random order after a failure, solves more instances (heuristic).
- **Priority-based search.** Later work searches over pairwise priorities instead of a fixed order, which is still incomplete but solves more instances.
- **Path coordination.** Another decoupled method fixes the paths and plans only the timing along them, in a coordination space of dimension $r$.
- **Continuous spaces.** The same idea works with sampling planners such as [probabilistic roadmaps](/probabilistic-roadmap/), where each robot plans in configuration space-time.

## When to use it

Use prioritized planning when there are many robots, the space is not crowded, and a quick plan matters more than a guarantee: warehouses with wide aisles, or game characters. Use [conflict-based search](/conflict-based-search/) or a coupled planner when the space has narrow passages, when optimal plans are needed, or when a failure is not acceptable.

## Pitfalls

- **Parking robots.** A robot that has arrived blocks its goal for ever. If its goal lies on the path of a later robot, the later robot fails, as in the siding example. Give such robots a lower priority, or let them move away.
- **Horizon too short.** A robot may need to wait a long time for others. If $H$ is short, the search fails although a plan exists.
- **Swap conflicts.** Checking only cells, and not moves, lets two robots pass through each other on an edge.
- **Goal test.** The search must not stop at the goal at a time when an earlier robot will pass the goal later.
- **Treating failure as proof.** "No plan found" does not mean that no plan exists.

## Implementations

## History

Erdmann and Lozano-Pérez (1987) studied several objects moving in the same space. They gave the objects priorities and planned each object in configuration space-time among the objects with higher priority, which is the prioritized method. LaValle's book (2006) presents it as a decoupled method next to path coordination. Silver (2005) used reservation tables for cooperative pathfinding in games, and the method is now a standard baseline for multi-agent pathfinding.

## References
