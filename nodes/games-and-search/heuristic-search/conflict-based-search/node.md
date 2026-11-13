---
tag: DBEXMS
kind: algorithm
slug: conflict-based-search
name: Conflict-based search
aliases:
- CBS
area: games-and-search/heuristic-search
level: research
summary: "Optimal multi-agent pathfinding by a two-level search: plan each agent alone, and when two paths collide, branch on which agent must avoid the collision. Minimizes the sum of costs."
solves: [multi-agent-pathfinding]
model: word-ram
complexity:
  vars: {n: the number of free cells, k: the number of agents, c: the optimal sum of costs}
  time: {worst: 2^O(k n c)}
  space: {extra: 2^O(k n c)}
properties: {deterministic: true, recursive: false}
prereqs: [multi-agent-pathfinding, a-star-search]
see_also: [best-first-search, best-first-branch-and-bound, state-space-search, hierarchical-pathfinding-a-star, jump-point-search, np-hard, constant-bandwidth-server]
sources:
  - paper: doi:10.1016/j.artint.2014.11.006
    title: "Guni Sharon, Roni Stern, Ariel Felner and Nathan R. Sturtevant, Conflict-based search for optimal multi-agent pathfinding, Artificial Intelligence 219 (2015)"
    locator: pp. 40 to 66; the constraint tree, the low level, the proofs of optimality and completeness, meta-agent CBS, and the experiments
  - paper: doi:10.1609/aaai.v26i1.8140
    title: "Guni Sharon, Roni Stern, Ariel Felner and Nathan R. Sturtevant, Conflict-based search for optimal multi-agent path finding, AAAI 2012"
    locator: pp. 563 to 569; the first description of CBS
  - paper: doi:10.1609/socs.v5i1.18315
    title: "Max Barer, Guni Sharon, Roni Stern and Ariel Felner, Suboptimal variants of the conflict-based search algorithm for the multi-agent pathfinding problem, SoCS 2014"
    locator: pp. 19 to 27; greedy CBS and ECBS, with focal lists at both levels and a bound on the cost
  - paper: doi:10.1609/icaps.v28i1.13883
    title: "Ariel Felner, Jiaoyang Li, Eli Boyarski, Hang Ma, Liron Cohen, T. K. Satish Kumar and Sven Koenig, Adding heuristics to conflict-based search for multi-agent path finding, ICAPS 2018"
    locator: pp. 83 to 87; admissible heuristics for the high level from cardinal conflicts
  - paper: doi:10.1609/socs.v10i1.18510
    title: "Roni Stern and others, Multi-agent pathfinding: definitions, variants, and benchmarks, SoCS 2019"
    locator: pp. 151 to 158; the conflict types and the cost functions that the page uses
---

Conflict-based search (CBS) solves [multi-agent pathfinding](/multi-agent-pathfinding/) optimally: it finds paths for several agents on a shared graph, with no two agents in one place at one time, and with the least sum of the path costs. It plans each agent alone with [A*](/a-star-search/), ignoring the others. When two of the paths collide, it branches: in one branch the first agent may not be there at that time, in the other branch the second agent may not. So it searches a tree of constraints instead of the huge space of all agents together. Guni Sharon, Roni Stern, Ariel Felner and Nathan Sturtevant introduced it in 2012. The name CBS is also used for the [constant-bandwidth server](/constant-bandwidth-server/) of real-time scheduling, which is not related.

## In plain words

Several robots in a warehouse must each go to a place, and they must not bump into each other. Planning all robots at once is hard, because the number of combined positions grows very fast with the number of robots.

CBS starts with the selfish plan: each robot takes its own shortest path. Then it looks for the first moment when two robots would meet. It cannot know which of the two should give way, so it tries both: in one version, robot one must avoid that place at that moment, and in the other version, robot two must. Only the robot that got a new rule plans again. CBS always continues with the version whose plans are cheapest in total. The first version without any collision is the best plan.

## The problem

The input is a graph of free grid cells with their 4 neighbours, and $k$ agents, each with a start $s_i$ and a goal $g_i$, all starts distinct and all goals distinct. Time goes in steps. In each step each agent moves to a neighbouring cell or waits, at cost 1. Two agents may not be in one cell at one time (a *vertex conflict*), and two agents may not swap their cells in one step (an *edge conflict*). An agent stays at its goal after it arrives, and its cost is the time of its last arrival there. The task is a set of paths without conflicts and with the least *sum of costs*. The page [multi-agent pathfinding](/multi-agent-pathfinding/) gives the other variants.

## The algorithm

A *constraint* $(a, v, t)$ says that agent $a$ may not be at $v$ at time $t$, and $(a, u \to v, t)$ says that it may not move from $u$ to $v$ arriving at time $t$. Each node of the *constraint tree* holds a set of constraints for each agent, one path for each agent that obeys them, and the sum of the costs of these paths.

```pseudo id=main
CBS(starts, goals)
L1  root.constraints ← ∅; for each agent i, root.path(i) ← LOW-LEVEL(i, ∅); if one is none then return no solution
L2  root.cost ← the sum of the costs of the paths; open ← {root}
L3  while open is not empty do
L4      take the node N with the least cost out of open
L5      find the earliest conflict between two paths of N
L6      if there is none then return the paths of N
L7      if it is a vertex conflict of agents i and j at v at time t then the new constraints are (i, v, t) and (j, v, t)
L8      if it is an edge conflict, i from u to v and j from v to u at time t, then they are (i, u → v, t) and (j, v → u, t)
L9      for each new constraint c, of agent a do
L10         child ← a copy of N with c added for a; child.path(a) ← LOW-LEVEL(a, constraints of a in child)
L11         if child.path(a) is not none then child.cost ← the sum of the costs of its paths; put child in open
L12 return no solution
LOW-LEVEL(a, C)
L13 start a space-time A* at (s_a, 0), with the grid distance to g_a as the heuristic
L14 while some state (v, t) is open do take the one with the least t + h(v)
L15     if v = g_a and no constraint of C holds a at g_a at time t or later then return the path to (v, t)
L16     for each w that is v or a neighbour of v, if C allows w at t + 1 and the move v → w, open (w, t + 1)
L17 return none
```

Line L15 makes sure that the agent can stay at its goal: a path that reaches the goal too early, before another agent has passed, is not a solution. Line L16 lets the agent wait in place. After the last time of any constraint of $C$, a state $(v, t)$ is no better than the same cell at an earlier time, so the low level stops even though time has no limit. Each child changes the path of one agent only. CBS is a [best-first search](/best-first-search/) on the constraint tree, ordered by the sum of costs.

## Example

Two agents use a corridor of 4 cells with one side pocket. Cells are $(x, y)$, with $y$ counted down. Agent A goes from $(0, 0)$ to $(3, 0)$ and agent B from $(3, 0)$ to $(0, 0)$, so they must pass each other, and one of them must step into the pocket $(1, 1)$.

```
row 0  . . . .
row 1  # . # #
```

Alone, each agent goes straight in 3 steps, so the root costs 6. The table shows the nodes in the order in which line L4 takes them. Ties are broken in the order the nodes were made.

| step | node | constraints | cost | earliest conflict | children and their costs |
| --- | --- | --- | --- | --- | --- |
| 1 | root | none | 6 | A $(1,0) \to (2,0)$ and B $(2,0) \to (1,0)$ at $t = 2$ | 1: A waits once, 7; 2: B waits once, 7 |
| 2 | 1 | A not $(1,0) \to (2,0)$ at 2 | 7 | both at $(1, 0)$ at $t = 2$ | 3: A steps back, 8; 4: B waits, 8 |
| 3 | 2 | B not $(2,0) \to (1,0)$ at 2 | 7 | both at $(2, 0)$ at $t = 2$ | 5: A waits, 8; 6: B steps back, 8 |
| 4 | 3 | 1, and A not at $(1, 0)$ at 2 | 8 | A $(0,0) \to (1,0)$ and B $(1,0) \to (0,0)$ at $t = 3$ | 7: A uses the pocket, 8; 8: B waits, 9 |
| 5 | 4 | 1, and B not at $(1, 0)$ at 2 | 8 | a swap at $t = 3$ | both 9 |
| 6 | 5 | 2, and A not at $(2, 0)$ at 2 | 8 | a swap at $t = 3$ | both 9 |
| 7 | 6 | 2, and B not at $(2, 0)$ at 2 | 8 | a swap at $t = 3$ | 9 and 10 |
| 8 | 7 | 3, and A not $(0,0) \to (1,0)$ at 3 | 8 | none | the solution |

In node 7, agent A goes $(0,0), (1,0), (1,1), (1,0), (2,0), (3,0)$ with cost 5: it waits in the pocket while B passes. Agent B goes straight, $(3,0), (2,0), (1,0), (0,0)$, with cost 3. The sum of costs is 8, and a search over the joint states of both agents confirms that 8 is optimal. CBS expanded 8 tree nodes. Five of them had cost 8, because many partial plans are equally good before the last constraint decides.

**A measured experiment.** On 30 random instances with 6 agents on an 8 by 8 grid (each cell blocked with probability 0.1, random distinct starts and goals that are connected, `random.Random(23)` of Python, at most 2000 tree nodes each), CBS solved all 30. The optimal sums of costs had a total of 1019, against 992 for the agents alone, so the conflicts cost 2.7 percent. CBS expanded 1037 tree nodes in total, but 826 of them were for one instance: most instances need a few nodes, and a few need very many. These are measurements on these grids, not bounds.

## Correctness

The [proof](proofs/correctness.md) shows the following.

- **The low level is optimal.** It is A* with a consistent heuristic on the space-time graph, and it returns a cheapest path that obeys the constraints of its node.
- **Each split keeps every solution.** A solution has no conflicts, so it cannot break both new constraints. One child is always compatible with it.
- **Optimal.** A node compatible with an optimal solution stays in the open list, and its cost is at most $C^*$. So every node that CBS takes costs at most $C^*$, and the first node without conflicts is optimal.
- **It stops on solvable instances.** Each child adds a new constraint that the parent's path breaks, and the nodes that cost at most $C^*$ only have constraints with times at most $C^*$. So there are finitely many of them.

If each agent can reach its goal but the instance has no solution, CBS can run forever. Two agents in a corridor with no room to pass are an example.

## Complexity

The model is the [word RAM](/word-ram/). Let $n$ be the number of free cells, $k$ the number of agents and $c$ the optimal sum of costs. A low level search visits $O(n c)$ states, because the constraints have times at most $c$, and takes $O(n c \log(n c))$ time. A node has at most $k (c + 1)$ time steps to check for conflicts between $O(k^2)$ pairs. The proof bounds the tree: the expanded nodes have depth at most $5 k n (c + 1)$, so in the worst case there are $2^{O(k n c)}$ of them, and the open list can hold as many. Optimal multi-agent pathfinding is [NP-hard](/np-hard/), so no polynomial bound is expected.

In practice the number of tree nodes depends on the number of conflicts, not on the size of the joint state space, which has about $n^k$ states. CBS is fast when the agents meet rarely, and slow in narrow corridors where many conflicts are equally good.

## Properties

- **Optimal** for the sum of costs, and complete on solvable instances.
- **Not complete on unsolvable instances** without an extra check: it can search forever.
- **Two levels.** Best-first search on the constraint tree, A* in space and time for one agent at a time.
- **Independent of the conflict choice.** Any conflict can be split, and the proof still holds, but the choice changes the size of the tree a lot.
- **The cost function can change.** With the largest cost instead of the sum, the same scheme minimizes the makespan.

## Variants and improvements

- **Meta-agent CBS** (in the 2015 paper) merges two agents into one when they conflict too often, and plans them together with a joint search.
- **Improved CBS** (Boyarski and others 2015) first splits *cardinal* conflicts, where both children cost more than the parent, and bypasses conflicts when an equally cheap path without the conflict exists.
- **CBSH** (Felner and others 2018) adds admissible heuristics to the high level, computed from the cardinal conflicts of a node.
- **ECBS** (Barer, Sharon, Stern and Felner 2014) uses focal lists at both levels, and returns a solution whose cost is at most a factor $w$ above the optimum, much faster.
- **Disjoint splitting and symmetry reasoning** add stronger constraints in each split, which removes many equal branches in corridors and rooms.
- **Other cost functions and conflicts**, for example for agents of different sizes, or for paths with continuous time.

## When to use it

Use CBS to get optimal plans for a few to a few dozen agents on maps such as warehouses or game levels, when the agents do not meet too often. For many agents in tight spaces, use a bounded variant such as ECBS, or a fast suboptimal planner such as prioritized planning. For a single agent, use [A*](/a-star-search/) or a grid method such as [jump point search](/jump-point-search/). If the instance may have no solution, run a test of solvability first. Such tests take polynomial time, as the page on [multi-agent pathfinding](/multi-agent-pathfinding/) explains.

## Pitfalls

- **Forgetting the goal rule.** An agent that reaches its goal early and stays there can block another agent later. The low level must not stop at the goal before the last constraint at that goal.
- **Missing edge conflicts.** Without the swap rule, two agents can pass through each other in a corridor, and the plan is not valid.
- **Unsolvable instances.** CBS does not stop by itself when the agents can reach their goals one at a time but not together. Set a limit, or test solvability first.
- **Corridors.** Many conflicts with equal costs make the tree explode. In one of the random cases that we tried, three agents on a 2 by 5 map with a corridor needed more than 200000 tree nodes, while the joint state space had fewer than 3000 states.
- **The other CBS.** In real-time scheduling, CBS is the constant-bandwidth server. Spell out the name at first use.

## Implementations

## History

Sharon, Stern, Felner and Sturtevant introduced CBS at AAAI 2012, and meta-agent CBS at SoCS 2012. The journal version in Artificial Intelligence in 2015 gave both, with the proofs and a study of when CBS beats A* on the joint states. Barer, Sharon, Stern and Felner gave the bounded suboptimal ECBS in 2014. Boyarski and others gave improved CBS in 2015, and Felner and others added heuristics to the high level in 2018. CBS and its variants became the standard optimal solvers for the benchmarks that Stern and others described in 2019.

## References
