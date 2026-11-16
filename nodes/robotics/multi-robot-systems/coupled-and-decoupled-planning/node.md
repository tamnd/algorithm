---
tag: YCNQBT
kind: concept
slug: coupled-and-decoupled-planning
name: Coupled and decoupled multi-robot planning
aliases:
- centralized versus decoupled planning
area: robotics/multi-robot-systems
level: core
summary: Coupled planners search the joint space of all robots and are complete; decoupled ones plan robots separately and are fast but incomplete.
prereqs: [configuration-space, motion-planning, multi-robot-system]
see_also: [prioritized-multi-robot-planning, multi-agent-pathfinding, conflict-based-search, pebble-motion-on-graphs, piano-movers-problem, pspace, a-star-search, probabilistic-roadmap]
sources:
  - book: isbn:9780521862059
    title: Steven M. LaValle, Planning Algorithms, Cambridge University Press, 2006
    locator: Chapter 7, the section on multiple robots (the joint configuration space, decoupled planning, prioritized planning and path coordination)
  - paper: doi:10.1177/027836498400300405
    title: John E. Hopcroft, Jacob T. Schwartz and Micha Sharir, On the complexity of motion planning for multiple independent objects; PSPACE-hardness of the warehouseman's problem, International Journal of Robotics Research 3(4), 1984
    locator: pages 76 to 88 (rectangles in a rectangular box, PSPACE-hard)
  - paper: doi:10.1007/BF01840371
    title: Michael Erdmann and Tomas Lozano-Perez, On multiple moving objects, Algorithmica 2, 1987
    locator: pages 477 to 521 (prioritized planning in configuration space-time)
---

Multi-robot motion planners fall into two families. A *coupled* (or centralized) planner treats the whole team as one robot whose configuration space is the product of the robots' spaces, so it is complete but its cost grows exponentially with the number of robots. A *decoupled* planner plans each robot, or each robot's timing, on its own and then resolves conflicts, so it is fast but can miss solutions; [prioritized planning](/prioritized-multi-robot-planning/) is its standard example, while [conflict-based search](/conflict-based-search/) for [multi-agent pathfinding](/multi-agent-pathfinding/) sits between the two, decoupled until robots conflict.

## In plain words

To plan for a team, you can think of the whole team as one big machine and plan its moves all at once. Then you never miss a way out, but the number of situations to check grows very fast: two robots on a map of 100 places give about ten thousand joint situations, and ten robots give more than a billion billion.

Or you can plan for each robot alone and fix the clashes afterward, for example by letting robots go one after another or wait for each other. This is quick, but a robot that planned first may block the only passage, and the planner then says "no plan" when there is one.

## The idea

**The joint space.** Robot $i$ has a [configuration space](/configuration-space/) $C_i$ of dimension $d_i$. The team has the joint space $C = C_1 \times \dots \times C_r$ of dimension $d_1 + \dots + d_r$. A joint configuration is free if each robot is free of the obstacles and no two robots overlap. A plan for the team is a path in the free part of $C$. A coupled planner runs any complete or resolution-complete planner, such as a grid search with [A*](/a-star-search/) or a [probabilistic roadmap](/probabilistic-roadmap/), in this space. On a grid with $g$ free cells, the joint space has up to $g^r$ states, and with time added, $g^r$ states per step.

**Hardness.** The cost of coupling is not just a weakness of the methods. Hopcroft, Schwartz and Sharir (1984) showed that moving many rectangles in a rectangular box to given places, the warehouseman's problem, is [PSPACE](/pspace/)-hard when the number of rectangles is part of the input (theorem). So no planner that is complete for any number of robots runs in polynomial time, unless P = PSPACE.

**Decoupled planning.** Two main forms exist:

- **Prioritized planning.** Robots are planned one at a time in an order, each among the planned paths of the earlier ones as moving obstacles in configuration space-time. Erdmann and Lozano-Pérez (1987) proposed it.
- **Path coordination.** Each robot first gets a path that ignores the others. Then only the timing is planned: the coordination space is $[0, 1]^r$, one parameter per robot along its path, and some points of it are blocked because two robots would overlap there.

Both are incomplete (theorem, by example): fixing paths or fixing an order can rule out the only solutions.

**In between.** Methods that couple robots only when needed keep the speed of decoupled planning on easy instances and the completeness of coupled planning:

- [Conflict-based search](/conflict-based-search/) plans each robot alone and splits the search into two branches at each conflict, adding a constraint to one robot in each branch. It is complete and optimal for multi-agent pathfinding.
- Subdimensional expansion, as in M* by Wagner and Choset, searches in each robot's own space and grows the joint space only around robots that collide.
- Grouping methods merge robots that conflict into one group and plan each group in its joint space.

**Two distinctions that are often mixed up.** "Centralized" can mean the computation runs on one computer, or the planner searches the joint space. A decoupled planner can run on one computer, and a coupled search can be distributed. This page uses "coupled" for the search space only.

## Examples

**A corridor with a siding.** On the grid with rows `....` and `..##`, robot 0 starts at $(0, 2)$ with goal $(0, 1)$, and robot 1 starts at $(0, 0)$ with goal $(0, 3)$. The grid has $g = 6$ free cells, so a coupled breadth-first search has at most $6 \times 5 = 30$ joint states per time step. It finds a plan with makespan 4: robot 0 steps into $(0, 1)$, ducks into $(1, 1)$ while robot 1 passes, and steps back. [Prioritized planning](/prioritized-multi-robot-planning/) fails for both orders, because the first robot always takes its shortest path and parks where the second one must pass. The proof on that page shows this.

**A pocket.** On the grid with rows `#.##` and `....`, two robots swap ends of the corridor using the pocket above column 1. Prioritized planning works in one order and fails in the other, and when it works it matches the coupled makespan of 5 steps.

**Growth.** On a $10 \times 10$ grid with no obstacles, $g = 100$. The joint space has $100 \cdot 99 = 9900$ states for 2 robots and $100 \cdot 99 \cdots 91 \approx 6.3 \times 10^{19}$ for 10 robots, so a plain coupled search is hopeless at 10 robots, while prioritized planning runs 10 searches of $100$ cells times the horizon.

**Puzzles.** The [sliding tile puzzle](/sliding-tile-puzzle/) is a team of tiles on a grid with one empty cell, the densest case of coupling. Ratner and Warmuth (1990) showed that finding a shortest solution of the $n \times n$ version is NP-hard (theorem), while deciding whether a solution exists is easy by a parity test.

## Where it is used

Warehouse and factory fleets use decoupled methods, often prioritized ones with reservation tables, because they have many robots and wide aisles. Multi-arm work cells, where two arms share a small space, use coupled planning, because the joint space has only twice the dimension and the arms interact closely. Multi-agent pathfinding research uses methods in between, such as conflict-based search, to get optimal plans for tens or hundreds of agents. The question "is a plan possible at all" on a graph is answered by [pebble motion on graphs](/pebble-motion-on-graphs/), which is decidable in polynomial time when the robots move one at a time.

## References
