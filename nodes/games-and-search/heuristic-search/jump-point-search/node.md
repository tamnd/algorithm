---
tag: RQYJH2
kind: algorithm
slug: jump-point-search
name: Jump point search
aliases:
- JPS
area: games-and-search/heuristic-search
level: advanced
summary: "A* on 8-connected uniform-cost grids that tries only a few directions from each node and scans in straight lines to the next jump point. It returns an optimal path and expands far fewer nodes."
solves: [single-pair-shortest-path]
model: word-ram
complexity:
  vars: {n: the number of cells of the grid}
  time: {worst: O(n^2)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: true}
prereqs: [a-star-search, consistent-heuristic]
see_also: [theta-star, hierarchical-pathfinding-a-star, dijkstra, uniform-cost-search, motion-planning, multi-agent-pathfinding]
sources:
  - paper: doi:10.1609/aaai.v25i1.7994
    title: Daniel Harabor and Alban Grastien, Online graph pruning for pathfinding on grid maps, AAAI 2011
    locator: pp. 1114 to 1119; the neighbour pruning rules, forced neighbours, the jump procedure and the optimality theorem
  - paper: doi:10.1609/socs.v3i1.18254
    title: Daniel Harabor and Alban Grastien, The JPS pathfinding system, SoCS 2012
    locator: the rules for grids where diagonal moves may not cut corners
  - paper: doi:10.1609/icaps.v24i1.13633
    title: Daniel Harabor and Alban Grastien, Improving jump point search, ICAPS 2014
    locator: pp. 128 to 135; JPS+ with precomputed jump points, and scanning many cells at once with bit operations
---

Jump point search (JPS) is a version of [A*](/a-star-search/) for grid maps where every straight move costs 1 and every diagonal move costs $\sqrt 2$. On such grids many shortest paths have the same cost and differ only in the order of their moves, and plain A* expands the cells of all of them. JPS keeps one order: from each node it tries only a few directions, and it scans in a straight line until it finds a cell where a turn can be needed. Only these cells, the *jump points*, go into the open list. Daniel Harabor and Alban Grastien introduced it in 2011. It needs no preprocessing and no extra memory, and it returns an optimal path.

## In plain words

On an open grid there are many shortest paths from one cell to another: you can go diagonally first and then straight, or straight first and then diagonally, or mix the moves. They all cost the same. A* looks at all of them, which wastes time.

JPS picks one order and keeps to it. When it goes straight, it keeps going straight. When it goes diagonally, it may also turn into the two straight directions that are part of the diagonal. It stops only where a wall makes a turn necessary, because the cell beside it cannot be reached in a better way. These stop cells are the only ones that A* must store.

## The problem

The input is a grid of free and blocked cells, a start cell $s$ and a goal cell $t$. From a free cell you can move to any of the 8 neighbours. A straight move costs 1 and a diagonal move costs $\sqrt 2$. The task is a shortest path from $s$ to $t$, as in [single-pair shortest path](/single-pair-shortest-path/).

The *corner rule* says when a diagonal move is allowed. This page uses the rule without corner cutting: a diagonal move from $x$ by $(d_x, d_y)$ is allowed only if the target and both cells $x + (d_x, 0)$ and $x + (0, d_y)$ are free. The pruning rules depend on the corner rule, so a JPS for one rule is wrong for the other. JPS does not apply to grids with different costs per cell.

## The algorithm

A node is a cell with the direction of the move that reached it. A move $m$ is *straight* if one of its coordinates is 0. For a straight arrival at $x$ in direction $m$, and a direction $q$ perpendicular to $m$, the cell $x + q$ is a *forced neighbour* if $x - m + q$ is blocked and $x + q$ is free. The path from the cell before $x$ to $x + q$ then cannot go around $x$, so the moves $q$ and $m + q$ (if allowed) are forced.

```pseudo id=main
JUMP-POINT-SEARCH(s, t)
L1  open ← {(s, none)}, g(s, none) ← 0
L2  while open is not empty do
L3      take the node (x, d) with the least g + h from open
L4      if x = t then return the jump points on the parent chain of (x, d)
L5      for each move m in PRUNED(x, d) do
L6          y ← JUMP(x, m)
L7          if y ≠ none and g(x, d) + cost(x, y) < g(y, m) then
L8              g(y, m) ← g(x, d) + cost(x, y), parent(y, m) ← (x, d), add (y, m) to open
L9  return no path
PRUNED(x, d)
L10 if d = none then return all allowed moves from x
L11 if d is diagonal then return the allowed moves among d and its two straight parts
L12 return d if it is allowed, and the forced moves of (x, d)
JUMP(x, m)
L13 loop
L14     if the move m from x is not allowed then return none
L15     x ← x + m
L16     if x = t then return x
L17     if m is straight and (x, m) has a forced neighbour then return x
L18     if m is diagonal and JUMP(x, m1) ≠ none or JUMP(x, m2) ≠ none then return x
```

In line L18, $m_1$ and $m_2$ are the two straight parts of the diagonal $m$. The cost of a jump in line L7 is the number of steps times 1 or $\sqrt 2$. The heuristic $h$ is the octile distance $\sqrt 2 \min(|\Delta x|, |\Delta y|) + \bigl||\Delta x| - |\Delta y|\bigr|$ to the goal, which is the cost on an open grid.

The nodes are pairs of a cell and a direction, so a cell can have up to 9 nodes. Many implementations keep one node per cell instead. The proof of this page covers the version with pairs.

## Example

The grid has 8 columns and 6 rows. A cell is $(x, y)$, with $y$ counted down from the top row. The cells $(3, 2)$, $(3, 3)$ and $(3, 4)$ are walls. The start is $S = (1, 3)$ and the goal is $G = (6, 3)$.

```
y=0  . . . . . . . .
y=1  . . . . . . . .
y=2  . . . # . . . .
y=3  . S . # . . G .
y=4  . . . # . . . .
y=5  . . . . . . . .
```

| step | node expanded | $g$ | jump points found |
| --- | --- | --- | --- |
| 1 | $(1, 3)$, start | $0$ | $(2, 4)$ going down-right, $(2, 2)$ going up-right |
| 2 | $(2, 4)$, down-right | $\sqrt 2$ | $(2, 5)$ going down |
| 3 | $(2, 2)$, up-right | $\sqrt 2$ | $(2, 1)$ going up |
| 4 | $(2, 5)$, down | $1 + \sqrt 2$ | $(4, 5)$ going right |
| 5 | $(2, 1)$, up | $1 + \sqrt 2$ | $(4, 1)$ going right |
| 6 | $(4, 5)$, right | $3 + \sqrt 2$ | $(4, 1)$ going up, $G$ going up-right |
| 7 | $(4, 1)$, right | $3 + \sqrt 2$ | $(4, 5)$ going down, $G$ going down-right |
| 8 | $G$, up-right | $3 + 3\sqrt 2$ | the goal |

In step 1 the scans to the right, left, up and down find nothing: the scan to the right hits the wall, and the others reach the border with no forced neighbour. The diagonal scan down-right stops at once at $(2, 4)$, because the straight scan down from $(2, 4)$ finds $(2, 5)$. At $(2, 5)$, moving down, the cell $(3, 4)$ beside the cell before is a wall and $(3, 5)$ is free, so $(3, 5)$ is a forced neighbour. In step 4, $(2, 5)$ may turn right only because of this forced neighbour.

The path is $(1, 3), (2, 4), (2, 5), (4, 5), (6, 3)$, with cost $3 + 3\sqrt 2 \approx 7.24$. JPS expands 8 nodes. Plain A* with the same heuristic and the same corner rule expands 16 cells and finds the same cost.

**A measured experiment.** On 20 random 64 by 64 grids with reachable random start and goal cells (`random.Random(8)` of Python), JPS expanded 878 nodes in total against 3,455 cells for A* when each cell is a wall with probability 0.05, and 1,246 nodes against 2,430 cells with probability 0.2. The costs were the same. JPS does more work per expansion, because it scans, so these counts are not running times. Harabor and Grastien report large speedups over A* on benchmark maps from games. These are measurements, not bounds.

## Correctness

The [proof](proofs/correctness.md) shows that JPS returns an optimal path, for the rule without corner cutting.

- **Allowed paths.** Call a pair of consecutive moves allowed if the second move is in PRUNED of the first. On a shortest path, a pair that is not allowed is a straight move followed by a diagonal move that could be swapped. Swapping such pairs moves diagonals earlier and keeps the cost, so some shortest path has only allowed pairs.
- **Jumps find the turns.** Along an allowed shortest path, each scan stops at the latest at the next cell where the path turns: a straight run turns only at a forced neighbour, and a diagonal run turns into a straight part whose scan finds something.
- **A* on jump points.** The jump arcs cost exactly the octile distance between their ends, so the octile heuristic is consistent on them, and A* returns the cheapest path over jump points. Each jump path is a grid path of the same cost, and the path above is one of them, so the costs are equal.

## Complexity

The model is the [word RAM](/word-ram/). Let $n$ be the number of cells. There are at most $9n$ nodes, and each is expanded at most once. An expansion makes at most 8 scans. A straight scan visits $O(n)$ cells in the worst case, and a diagonal scan starts a straight scan at each of its cells, so it also visits $O(n)$ cells on a square grid. This gives a worst case of $O(n^2)$ time, plus $O(n \log n)$ for the heap. This bound is loose, and the page does not claim a tight one. In practice the scans are short and cheap, and JPS is faster than A* on most maps. The extra space is $O(n)$ for the $g$ values and the parents.

## Properties

- **Optimal** on 8-connected grids with costs 1 and $\sqrt 2$, for the corner rule that its pruning rules were made for.
- **No preprocessing** and no extra memory beyond A*.
- **Grid specific.** It needs uniform costs. With costs per cell, the symmetric paths do not have equal costs, and the pruning loses optimal paths.
- **The same answer as A*.** It returns the same cost as A* on the grid. The path can differ among the paths of equal cost.

## Variants and improvements

- **Corner cutting.** The 2011 paper uses a movement rule with corner cutting, and then diagonal moves have forced neighbours too. The 2012 paper gives the rules without corner cutting that this page uses.
- **JPS+.** The 2014 paper precomputes, for each cell and each direction, the distance to the next jump point or wall, so that a scan becomes one table lookup. It also gives a way to scan many cells at once with bit operations on rows of the grid.
- **Bounded jumps.** A scan can stop after a fixed number of steps and return the cell it reached as a node. This keeps optimality and bounds the work per expansion.
- **Canonical orderings.** Later work explains JPS as A* that follows one canonical order of moves, and uses the same idea on other kinds of grids.

## When to use it

Use JPS for shortest paths on 8-connected grid maps with uniform costs, such as maps of video games, when the map changes too often for preprocessing. If the map is static and memory is free, JPS+ or a hierarchy such as [HPA*](/hierarchical-pathfinding-a-star/) is faster. If cells have different costs, use A* or [Dijkstra](/dijkstra/). If the path may leave the grid lines and go at any angle, use [Theta*](/theta-star/). For many agents on one grid, see [multi-agent pathfinding](/multi-agent-pathfinding/).

## Pitfalls

- **The wrong corner rule.** Rules made for corner cutting give wrong paths on a grid without it, and the other way round. Test against A* with the same rule.
- **Weighted grids.** JPS is not optimal when cells have different costs.
- **One node per cell.** If two arrivals at the same cell have the same cost, an implementation that keeps one of them also keeps only one set of pruned directions. The proof here uses one node per cell and direction.
- **The goal inside a scan.** A scan must stop at the goal (line L16), also when the goal is not a jump point by the other rules.
- **Expansions are not time.** JPS expands fewer nodes than A* but scans many cells. Compare running times, not only expansions.

## Implementations

## History

Harabor and Grastien introduced jump point search at AAAI 2011, as an online way to prune symmetric paths on grid maps, after earlier work by Harabor on symmetry reduction with empty rectangles. The 2012 SoCS paper describes the system for the grid rules without corner cutting, and the 2014 ICAPS paper gives JPS+ and faster scans. Variants of JPS took part in the Grid-Based Path Planning Competition. Sturtevant and Rabin later described JPS in terms of canonical orderings of moves.

## References
