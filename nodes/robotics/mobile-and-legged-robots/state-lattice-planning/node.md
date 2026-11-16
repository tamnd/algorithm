---
tag: C6YCHP
kind: algorithm
slug: state-lattice-planning
name: State lattice planning
aliases:
- state lattice
area: robotics/mobile-and-legged-robots
level: advanced
summary: Searches a regular lattice of states joined by precomputed feasible motion primitives, so every path respects the vehicle model.
solves: [kinodynamic-planning]
model: word-ram
complexity:
  vars: {N: "the number of lattice states in the map", b: "the number of primitives per state", c: "the number of cells in the swath of a primitive"}
  time: {worst: "O(N (log N + b c))"}
  space: {extra: O(N)}
properties: {deterministic: true, randomized: false, online: false, exact: false}
history:
  year: 2005
  people: [Mihail Pivtoraiko, Alonzo Kelly]
  note: Pivtoraiko and Kelly introduced state lattices with control sets of motion primitives that join lattice states exactly in 2005; Pivtoraiko, Knepper and Kelly gave the full method for field robots in 2009.
prereqs: [a-star-search, configuration-space, kinematic-bicycle-model]
see_also: [hybrid-a-star, a-star-search, kinodynamic-planning, dubins-path, reeds-shepp-path, dijkstra, consistent-heuristic, occupancy-grid-map]
sources:
  - paper: doi:10.1002/rob.20285
    title: Mihail Pivtoraiko, Ross A. Knepper and Alonzo Kelly, Differentially constrained mobile robot motion planning in state lattices, Journal of Field Robotics 26(3), 2009
    locator: pages 308 to 333 (the state lattice, control sets of primitives that join lattice states, precomputed swaths for collision checks, and completeness and optimality with respect to the lattice)
  - paper: "Mihail Pivtoraiko and Alonzo Kelly, IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 2005"
    title: Generating near minimal spanning control sets for constrained motion planning in discrete state spaces
    locator: the whole paper (the first description of state lattices and of control sets that are small but reach the same states)
  - book: isbn:9780521862059
    title: Steven M. LaValle, Planning Algorithms, Cambridge University Press, 2006
    locator: Section 14.2 (reachability graphs, motion primitives and resolution completeness under differential constraints)
---

State lattice planning finds paths for a vehicle with motion constraints, such as a car that cannot turn on the spot. It chooses a regular grid of states, for example positions on a square lattice and 8 or 16 headings. It then builds, once and offline, a small set of motion primitives: short paths that the vehicle can drive and that start and end exactly at lattice states. These primitives, repeated at every state, turn the lattice into a graph, and a graph search such as [A\*](/a-star-search/) finds a path in it. Because each edge is a feasible motion and joins states exactly, every path in the graph can be driven, and the search is complete and optimal with respect to the lattice and the set of primitives. The method plans for planetary rovers, field robots and autonomous cars.

## In plain words

Think of a city of square blocks where a car may only stop at street corners, and only facing one of eight directions. Someone has worked out, once, a short list of moves: go one block straight, or make a gentle curve that ends exactly at another corner, facing another of the eight directions. The car never needs to know more than these moves.

To plan a trip, you search over corners and directions, using only the moves on the list, like a route planner on a map. Every route found is one the car can drive. The catch: a route that needs a stop between corners, or a curve that is not on the list, is never found.

## The problem

**The model.** The vehicle is a forward-driving car with a minimum turning radius, as in the [kinematic bicycle model](/kinematic-bicycle-model/) or the Dubins car. The map is an [occupancy grid](/occupancy-grid-map/). The lattice has spacing $r$ and 8 headings $k\pi/4$; the implementation uses arcs of radius $R = (1 + \sqrt2)\,r$, which is the radius the 45 degree turns below need, so the car's own minimum radius must be at most $R$. The model is the [word RAM](/word-ram/) with states as integer triples at this resolution.

**Input.** The grid, a start state and a goal state on the lattice.

**Output.** A list of lattice states joined by primitives, of least total length among the paths of the lattice graph, or failure.

**How it differs from close pages.** [Hybrid A\*](/hybrid-a-star/) also searches with arcs of the car, but from the exact poses where the arcs end, which are off the grid; it keeps one pose per cell and loses completeness and optimality even with respect to its own primitives. A state lattice keeps the states on the grid, so the graph is fixed and the guarantees of graph search hold for it. Grid A\* on cells ignores the heading and the turning radius. [Kinodynamic planning](/kinodynamic-planning/) is the general problem; sampling planners solve it without a fixed lattice.

## The algorithm

The control set for heading 0 is three primitives: straight to $(1, 0, 0)$, length 1; a left turn to $(2, 1, 1)$, an arc of radius $1 + \sqrt2$ through $\pi/4$ and then a straight piece of $\sqrt2 - 1$, length $2.3103$; and the mirror right turn to $(2, -1, 7)$. For heading 1 ($\pi/4$): straight to $(1, 1, 1)$, length $\sqrt2$; a right turn to $(2, 1, 0)$, the straight piece first and then the arc; and the mirror left turn to $(1, 2, 2)$. Rotations by $\pi/2$ give the other six headings. Lengths are in units of $r$.

```pseudo id=main
LATTICE-PLAN(map, start, goal)
L1  g(start) ← 0; push start with f = h(start)
L2  h(s) = r |(i, j) - (i_goal, j_goal)|
L3  while the open list is not empty: pop the state s with the least f; skip it if closed; close it
L4      if s = goal then return the path of parents to s
L5      for each primitive p of the control set for the heading of s do
L6          if the swath of p, shifted to s, is inside the map and free then
L7              t ← the end state of p from s; if g(s) + r length(p) < g(t) then set g(t), parent(t) ← s, push t
L8  return failure
```

The swath of a primitive is the set of cells it touches when driven from $(0, 0, k)$. It is computed once for each primitive and shifted by $(i, j)$ at search time, so the collision check of line L6 is a few set lookups. This is the main practical gain of the lattice: all the geometry is done offline.

## Example

Lattice spacing $r = 1$ m, so $R = 2.4142$ m. On an empty map, from $(5, 5, 0)$ to $(11, 8, 2)$, that is, 6 m ahead and 3 m to the left, now facing north. A\* expands 24 states and returns three straight primitives, a left turn to $(10, 6, 1)$ and a left turn to $(11, 8, 2)$, length 7.6207 m. Dijkstra on the same graph expands 71 states and finds the same length. The [Dubins path](/dubins-path/) with the same radius, which is the continuous optimum, has length 7.4256 m, so the lattice path is 2.6% longer.

The gap can be large. For a U-turn from $(5, 5, 0)$ to $(10, 5, 4)$, the lattice path has 9 primitives and length 19.4827 m, against 15.1990 m for the Dubins path: 28% longer, because the lattice offers only 45 degree turns of one radius. Measured: 376 expansions for A\* and 1548 for Dijkstra.

Obstacles show the other limit. Add a wall of cells at $x \in [9, 10)$, $6 \le y < 15$ on a 20 m by 20 m map, and plan from $(5, 10, 0)$ to $(14, 10, 0)$, just behind the wall, facing east. A\* finds a path of 16 primitives and 34.76 m that passes under the wall and loops back, in about 30 ms in CPython. For the goal $(13, 10, 0)$ it returns failure: no sequence of primitives ends there, because the turns need more room than the lattice gives next to the wall. A continuous car with the same radius can reach it: driving south at $x = 10.1$ and turning left through a quarter circle ends facing east at $x = 12.5$, $y = 10$, and a short straight piece reaches $x = 13$. This is what completeness with respect to the lattice means.

## Correctness

The [proof](proofs/correctness/) has three lemmas and a theorem. Lemma 1: each primitive ends exactly at a lattice state; for the 45 degree turn this is the identity $R/\sqrt2 + 1 - 1/\sqrt2 = 2$ with $R = 1 + \sqrt2$. Lemma 2: each primitive and each sequence of primitives is a $C^1$ forward path with curvature at most $1/R$, so it can be driven. Lemma 3: the shifted swath is the set of cells the primitive's samples touch. Theorem: the heuristic is consistent, the lattice graph is finite, and A\* returns a least-length path in the graph or reports that none exists. The guarantees hold with respect to the lattice and the control set, not for the continuous problem.

## Complexity

- **Time.** With $N$ lattice states, $b$ primitives per state and swaths of $c$ cells, A\* does at most $N$ expansions, each with $b$ swath checks of $c$ lookups and heap operations of $O(\log N)$: $O(N(\log N + bc))$. Here $N = 8(n_x + 1)(n_y + 1)$, $b = 3$, and $c$ is 6 to 8.
- **Space.** $O(N)$ for the costs and the parents, plus the control set and the swaths, which do not depend on the map.
- **Offline work.** Building the control set is a boundary value problem for each primitive. For this lattice it has a closed form; for richer vehicle models, Pivtoraiko et al. compute the primitives with a trajectory generator offline.

## Properties

- **Feasible by construction.** Every path respects the curvature bound and has a continuous heading, with no smoothing step.
- **Complete and optimal with respect to the lattice.** If the lattice graph has a path, the search finds the shortest one; this is a theorem, relative to the lattice and the control set.
- **Not complete for the continuous problem.** The example above has a reachable goal that the lattice cannot reach.
- **Regular.** The graph is the same at every lattice point up to a shift, so primitives, swaths and heuristic tables are computed once.
- **Choice of control set.** More primitives give shorter paths and fewer failures, at a higher branching factor. Pivtoraiko and Kelly choose a near minimal control set: one that reaches the same states with as few primitives as possible.

## Variants and improvements

- **More headings and curvatures.** 16 headings, and states that also store the curvature, so that the path has continuous curvature.
- **Reverse primitives.** Add primitives driven backward, with a higher cost, for parking.
- **Time and velocity.** Add time and speed to the state for dynamic obstacles; the lattice becomes a spatio-temporal lattice.
- **Road-aligned lattices.** For driving on roads, the lattice follows the lane, with stations along the road and lateral offsets.
- **Heuristic look-up tables.** Precompute the exact lattice cost without obstacles for nearby goals and use it as the heuristic; it dominates the Euclidean distance.
- **Incremental search.** Replan with D\* Lite or anytime search when the map changes.

## When to use it

Use it when the vehicle has motion constraints, the environment is known as a grid, and you want guarantees that a graph search gives: an answer whenever the lattice has one, and the best one. It fits rovers, field robots and cars on structured roads or in parking lots. It fits less when the goal pose is not on the lattice (connect to it with a final local path), or when the robot needs paths that the lattice cannot express. [Hybrid A\*](/hybrid-a-star/) is a common alternative with fewer guarantees but no need for a carefully designed control set.

## Pitfalls

- **Primitives that do not land on the lattice.** Rounding the end of a primitive to the nearest state breaks feasibility. Solve for primitives that end exactly, as Lemma 1 does.
- **Heading set and lattice spacing.** On a square lattice, only some headings, such as multiples of $\pi/4$ or the directions of $(2, 1)$, have short straight primitives. 16 headings with non-uniform angles are common for this reason.
- **Turning radius.** The control set fixes the radius. A lattice built for one radius cannot be used for a car that turns less sharply.
- **Swath sampling.** A sampled swath can miss a corner. Dilate the obstacles or compute the swath with the vehicle footprint.
- **The goal must be a state.** If the goal pose is between states, the search can only reach a nearby state.
- **Branching.** Large control sets slow the search more than they improve the paths. Use a small, spanning set.

## Implementations

## History

Pivtoraiko and Kelly introduced the state lattice and control sets in 2005, for the mobile robots of the Robotics Institute at Carnegie Mellon. Pivtoraiko, Knepper and Kelly gave the full method in 2009, with swaths, heuristics and tests on field robots. Likhachev and Ferguson used lattices with anytime search for Boss, the Carnegie Mellon car that won the DARPA Urban Challenge of 2007, in parking lots. Lattices aligned with the road became a common planner for autonomous cars on highways.

## References
