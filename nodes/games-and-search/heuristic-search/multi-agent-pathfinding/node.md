---
tag: GXKX6H
kind: problem
slug: multi-agent-pathfinding
name: Multi-agent pathfinding
aliases:
- MAPF
area: games-and-search/heuristic-search
level: advanced
summary: "Find paths for several agents from their starts to their goals on a shared graph, so that no two agents meet in a vertex or swap along an edge, with the least sum of costs or makespan."
prereqs: [a-star-search, state-space-search]
see_also: [conflict-based-search, hierarchical-pathfinding-a-star, jump-point-search, sliding-tile-puzzle, motion-planning, np-hard, sat]
sources:
  - paper: doi:10.1609/socs.v10i1.18510
    title: "Roni Stern, Nathan R. Sturtevant, Ariel Felner, Sven Koenig, Hang Ma, Thayne T. Walker, Jiaoyang Li, Dor Atzmon, Liron Cohen, T. K. Satish Kumar, Eli Boyarski and Roman Barták, Multi-agent pathfinding: definitions, variants, and benchmarks, SoCS 2019"
    locator: pp. 151 to 158; the classical problem, the types of conflicts, the cost functions, staying at or leaving the target, and the grid benchmarks
  - paper: doi:10.1109/sfcs.1984.715921
    title: "Daniel Kornhauser, Gary Miller and Paul Spirakis, Coordinating pebble motion on graphs, the diameter of permutation groups, and applications, FOCS 1984"
    locator: pp. 241 to 250; the feasibility of pebble motion on graphs in polynomial time, and the bound of cubic length on the plans
  - paper: doi:10.1609/aaai.v27i1.8541
    title: "Jingjin Yu and Steven M. LaValle, Structure and intractability of optimal multi-robot path planning on graphs, AAAI 2013"
    locator: pp. 1443 to 1449; the NP-hardness of optimal plans on graphs, by a reduction from satisfiability
  - paper: doi:10.1609/aaai.v24i1.7767
    title: "Pavel Surynek, An optimization variant of multi-robot path planning is intractable, AAAI 2010"
    locator: pp. 1261 to 1263; the NP-completeness of plans with a bound on their length
  - paper: doi:10.1609/aaai.v24i1.7564
    title: "Trevor Standley, Finding optimal solutions to cooperative pathfinding problems, AAAI 2010"
    locator: pp. 173 to 178; A* on the joint states with operator decomposition, and independence detection
  - paper: doi:10.1609/aiide.v1i1.18726
    title: "David Silver, Cooperative pathfinding, AIIDE 2005"
    locator: pp. 117 to 122; cooperative A* with a reservation table in space and time, and its hierarchical and windowed versions
  - paper: doi:10.1016/j.artint.2014.11.006
    title: "Guni Sharon, Roni Stern, Ariel Felner and Nathan R. Sturtevant, Conflict-based search for optimal multi-agent pathfinding, Artificial Intelligence 219 (2015)"
    locator: pp. 40 to 66; the problem in its introduction and the comparison of the optimal solvers
---

Multi-agent pathfinding (MAPF) asks for paths for several agents on one graph, each from its start to its goal, so that the agents never collide. Time goes in discrete steps, and in each step each agent moves along an edge or waits. Two agents may not be in one vertex at one time, and they may not swap along one edge. The usual goals are the least *sum of costs* over the agents, or the least *makespan*, the time when the last agent arrives. Robots in warehouses, units in games and aircraft on airport taxiways are typical cases. To decide whether a plan exists takes polynomial time, but an optimal plan is [NP-hard](/np-hard/) to find.

## In plain words

Many robots share the floor of a warehouse. Each must drive to its own shelf. A robot can drive to a free square next to it or wait. Two robots may never be on one square at once, and two robots may not drive through each other.

For one robot, a shortest path is easy to find. With many robots, the best path for one can block another. Then one robot must wait, give way, or take a longer road. The question is how to choose all the paths together so that the total time, or the time until the last robot arrives, is as small as possible.

## Definition

**Input.** An undirected graph $G = (V, E)$, often a grid of free cells with 4 neighbours, and $k$ agents, each with a start $s_i \in V$ and a goal $g_i \in V$. The starts are distinct, and the goals are distinct.

**Moves.** Time steps are $t = 0, 1, 2, \dots$. A *path* of agent $i$ gives its vertex $\pi_i(t)$ at each time, with $\pi_i(0) = s_i$. Between two times, $\pi_i(t + 1)$ is $\pi_i(t)$ (a wait) or a neighbour of it (a move). Each step costs 1, and an agent stays at its goal after it arrives.

**Conflicts.** Two paths have a *vertex conflict* if $\pi_i(t) = \pi_j(t)$ for some $t$, and an *edge conflict* (a swap) if $\pi_i(t) = \pi_j(t + 1)$ and $\pi_j(t) = \pi_i(t + 1)$, with $\pi_i(t) \ne \pi_i(t + 1)$. In the usual definition, an agent may enter a vertex that another agent leaves in the same step, and a cycle of 3 or more agents may move around together.

**Output.** One path for each agent, with no conflicts between any two of them, or the answer that none exists.

**Cost.** The *cost* $T_i$ of a path is the least time after which the agent stays at its goal. Two objectives are common:

- the **sum of costs** $\sum_i T_i$, also called the flowtime;
- the **makespan** $\max_i T_i$.

These objectives can disagree, as the examples show.

## Variants

- **Conflict rules.** Some definitions also forbid *following* (entering a vertex that was left in the same step) or *cycles* of moves. The pebble motion problem allows only one move per step. Each rule changes which instances can be solved.
- **Stay at target or disappear at target.** In some applications, an agent leaves the graph at its goal and no longer blocks it.
- **Anonymous MAPF.** Any agent may go to any goal. With this freedom the problem becomes a flow problem and can be solved in polynomial time.
- **Weighted and continuous time.** Edges have different lengths, agents have sizes, or time is continuous.
- **Robust plans.** A $k$-robust plan keeps $k$ steps between two agents on one vertex, so a small delay does not cause a collision.
- **Lifelong MAPF.** Agents get new goals when they arrive, as in a warehouse that runs all day.
- **Bounded suboptimal.** The plan must cost at most $w$ times the optimum, for a given $w \ge 1$.

## Examples

**The objectives disagree.** Take the map below, with agent A at $(2, 0)$, which is also its goal, and agent B at $(4, 0)$ with goal $(0, 0)$. Cells are $(x, y)$ with $y$ counted down.

```
row 0  . . . . .
row 1  # . . . #
```

B can go straight along row 0 in 4 steps, but then A must step aside to $(2, 1)$ and come back, which costs A at least 3 steps: the sum of costs is 7 and the makespan is 4. Or A stays, and B goes around through row 1 in 6 steps: the sum of costs is 6 and the makespan is 6. A search over the joint states confirms that 6 is the least sum of costs and 4 the least makespan, and that no plan has both. With makespan at most 4 or 5 the least sum of costs is 7.

**A swap needs room.** On a corridor of 4 cells, two agents that start at the two ends and want to change places have no solution, although each one alone can reach its goal. Add a pocket below the second cell, and a solution exists: one agent waits in the pocket while the other passes. The least sum of costs is then 8, and the page on [conflict-based search](/conflict-based-search/) follows the search for it.

**A cycle of moves.** Four agents fill a 2 by 2 grid, and each wants the next cell in the clockwise order. No cell is free, but all four can move together in one step, so the makespan is 1 and the sum of costs is 4. If the conflict rules forbid cycles or following, this instance has no solution.

**A known puzzle.** The [sliding tile puzzle](/sliding-tile-puzzle/) is MAPF on a grid that is full except for one cell, with only one move in each step: the tiles are the agents.

## Known algorithms

| algorithm | objective | guarantee |
| --- | --- | --- |
| [A*](/a-star-search/) on the joint states | sum of costs or makespan | optimal; up to about $n^k$ states |
| A* with operator decomposition and independence detection (Standley 2010) | sum of costs | optimal; moves one agent at a time and splits the agents into independent groups |
| [Conflict-based search](/conflict-based-search/) (Sharon and others 2012, 2015) | sum of costs | optimal; searches a tree of constraints on single-agent paths |
| Increasing cost tree search (Sharon and others) | sum of costs | optimal; searches over the vectors of single-agent costs |
| M* (Wagner and Choset) | sum of costs | optimal; joint search only where agents meet |
| Reductions to [SAT](/sat/) and to integer programs (Surynek and others) | makespan or sum of costs | optimal; on the graph unrolled in time |
| ECBS (Barer and others 2014) | sum of costs | at most $w$ times the optimum |
| Cooperative A* with a reservation table (Silver 2005) | none | fast, plans the agents one after another; not complete and not optimal |
| Rule-based methods for pebble motion | none | complete, polynomial time; plans can be long |

## Bounds

**Feasibility is polynomial.** For pebble motion on a graph, where one agent moves in each step, Kornhauser, Miller and Spirakis (1984) showed that one can decide in polynomial time whether the agents can reach their goals, and that plans of $O(n^3)$ moves suffice when a plan exists, for a graph with $n$ vertices. Some instances need $\Omega(n^3)$ moves. The rules with parallel moves and cycles also have polynomial tests of feasibility.

**Optimality is NP-hard.** Surynek (2010) showed that it is NP-complete to decide whether a plan of a given length exists. Yu and LaValle (2013) showed that optimal plans on graphs are NP-hard to find for the makespan and for objectives that sum over the agents, by a reduction from satisfiability. Earlier, Ratner and Warmuth showed that shortest solutions of the generalized sliding tile puzzle are NP-hard to find.

**The joint state space.** With $n$ free vertices and $k$ agents there are $n (n - 1) \cdots (n - k + 1)$ joint positions, and in each step up to $5^k$ joint moves on a grid. This is why optimal solvers avoid the joint space where they can.

## Reductions

- **To single-agent search.** The joint states, with all joint moves as edges, form one graph, and a shortest path in it is an optimal plan. Any [state-space search](/state-space-search/) applies, at the price of the size above.
- **To satisfiability and integer programs.** Unroll the graph in time up to a bound $T$, with one variable for each agent, vertex and time. Conflicts become clauses or linear constraints. Increase $T$ until a plan exists.
- **To flow.** Anonymous MAPF reduces to a maximum flow in the graph unrolled in time.
- **From puzzles.** The sliding tile puzzle and pebble motion are special cases, so their hardness carries over.

## Applications

- Automated warehouses and sorting centres with hundreds of mobile robots.
- Units and characters in video games.
- Aircraft taxiing at airports, trains on tracks, and autonomous vehicles at junctions.
- Drones in shared airspace, and robots in factories and hospitals.

## References
