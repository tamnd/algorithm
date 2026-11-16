---
tag: C6X95N
kind: algorithm
slug: hybrid-a-star
name: "Hybrid A*"
aliases:
- hybrid-state A*
area: robotics/mobile-and-legged-robots
level: advanced
summary: A* over grid cells that stores a continuous pose in each cell and expands by car motions, with Reeds-Shepp shots to the goal.
solves: [kinodynamic-planning]
model: word-ram
complexity:
  vars: {B: "the number of bins, nx ny ntheta", s: "the number of collision samples on one primitive"}
  time: {worst: "O(B (log B + s))"}
  space: {extra: O(B)}
properties: {deterministic: true, randomized: false, online: false, exact: false}
history:
  year: 2008
  people: [Dmitri Dolgov, Sebastian Thrun, Michael Montemerlo, James Diebel]
  note: Hybrid A* was the path planner of Junior, the Stanford car in the DARPA Urban Challenge of 2007, for parking lots and U-turns; Dolgov et al. described it in 2008 and in a journal paper in 2010.
prereqs: [a-star-search, kinematic-bicycle-model, reeds-shepp-path]
see_also: [a-star-search, kinodynamic-planning, reeds-shepp-path, dubins-path, state-lattice-planning, admissible-heuristic, occupancy-grid-map, conjugate-gradient-method]
sources:
  - paper: doi:10.1177/0278364909359210
    title: Dmitri Dolgov, Sebastian Thrun, Michael Montemerlo and James Diebel, Path planning for autonomous vehicles in unknown semi-structured environments, The International Journal of Robotics Research 29(5), 2010
    locator: pages 485 to 501 (the hybrid-state search, the two heuristics, the analytic Reeds-Shepp expansion, the penalties for reverse and for switching, and the smoothing with conjugate gradient)
  - paper: "Dmitri Dolgov, Sebastian Thrun, Michael Montemerlo and James Diebel, AAAI Workshop on Search Techniques in Artificial Intelligence and Robotics, 2008"
    title: Practical search techniques in path planning for autonomous driving
    locator: pages 32 to 37 (the first description of the method)
  - book: isbn:9780521862059
    title: Steven M. LaValle, Planning Algorithms, Cambridge University Press, 2006
    locator: Section 14.2 (reachability graphs, motion primitives and resolution completeness under differential constraints)
---

Hybrid A\* is a path planner for a car among obstacles. It runs [A\*](/a-star-search/) over a grid of bins in $(x, y, \theta)$, but each bin stores one continuous pose, not the center of the bin. A node expands by driving short arcs of the car, left, straight or right at full steering, forward and backward, from its exact pose. So every path it returns can be driven, while the grid keeps the search finite. Reverse motion and changes of direction cost extra. The heuristic is the larger of two lower bounds: the length of a car path without obstacles, and the length of a grid path with obstacles but without the car's turning limit. Every few expansions the search tries an exact [Reeds-Shepp path](/reeds-shepp-path/) to the goal and stops when it is free. The method is a heuristic: it is neither complete nor optimal for the continuous problem, but it finds good paths in parking lots in a fraction of a second.

## In plain words

Lay a grid over the map. A plain grid search would jump from the center of one square to the center of the next, and a car cannot drive that path. Hybrid A\* instead keeps the real position of the car in each square. From there it tries six short drives: hard left, straight and hard right, forward or backward. Where a drive ends, it records the exact spot, in whatever square that is.

If two drives end in the same square, it keeps only the cheaper one. This keeps the search small, but it can throw away the one way that would have worked. Every now and then it also tries to reach the goal in one go with the shortest car path, and stops if that path is clear.

## The problem

**The model.** The car is the [kinematic bicycle model](/kinematic-bicycle-model/) at the rear axle, with minimum turning radius $\rho$, which may drive forward and backward. The map is an [occupancy grid](/occupancy-grid-map/) with cells of side $r$. The search uses bins of $r \times r$ meters and $\Delta\theta = 2\pi/n_\theta$ radians, so a bounded map has finitely many bins. Bins are integers and costs are floating point numbers; the model is the [word RAM](/word-ram/) at that resolution.

**Input.** The grid, a start pose and a goal pose, the radius $\rho$, the length $\ell$ of a primitive, the reverse factor $c_r \ge 1$, the switch penalty $c_s \ge 0$, and a goal tolerance.

**Output.** A list of arcs of curvature in $\{-1/\rho, 0, 1/\rho\}$ with signed lengths, followed by an exact shot to the goal, or a pose in the goal region. Or failure.

**How it differs from close pages.** Plain [A\*](/a-star-search/) on a grid of cells returns paths with corners that a car cannot follow. [State lattice planning](/state-lattice-planning/) also searches with motion primitives, but its primitives join lattice points exactly, so states never drift off the grid and the search is resolution complete on the lattice; hybrid A\* gives that up for primitives from any pose. [Kinodynamic planning](/kinodynamic-planning/) is the general problem, and sampling planners such as RRT\* solve it with asymptotic optimality, at a higher cost. The [Dubins path](/dubins-path/) and the Reeds-Shepp path solve the problem without obstacles, in constant time.

## The algorithm

```pseudo id=main
HYBRID-A*(map, start, goal, ρ, ℓ)
L1  store start in bin key(start) with g = 0; push it with f = h(start)
L2  h(q) = max(0, |q - goal| - εp), or its max with the grid distance from q to the goal
L3  key(q) = (floor(x / r), floor(y / r), floor(θ / Δθ))
L4  while the open list is not empty: pop the bin b with the least f
L5      if b is closed then continue; close b; q ← the pose stored in b
L6      if q is in the goal region then return the chain of primitives to q
L7      every N expansions: if the shot from q to the goal is free then return the chain + the shot
L8      for each κ in {-1/ρ, 0, 1/ρ} and each direction d in {+1, -1} do
L9          q' ← drive the arc (κ, d ℓ) from q; skip it if it hits an obstacle
L10         b' ← key(q'); skip it if b' is closed
L11         g' ← g(q) + ℓ (times cr if d < 0) (plus cs if d differs from the last direction)
L12         if b' is empty or g' < g(b') then store q' in b' with g', parent b; push b' with f = g' + h(q')
L13 return failure
```

Line L9 integrates the arc exactly, so the stored pose is where the car really is; only the bin is discrete. The shot of line L7 is a Reeds-Shepp path in Dolgov et al.; the implementation uses a [Dubins path](/dubins-path/), which is forward only but simpler, and is still a drivable path. Dolgov et al. try the shot every $N$ expansions and more often near the goal. In the second heuristic of line L2, they precompute the car path length without obstacles as a lookup table, and they compute the grid distance with obstacles by dynamic programming over the 2D grid; the implementation uses the Euclidean distance in place of the first and an 8-connected Dijkstra for the second. After the search, Dolgov et al. smooth the path with the [conjugate gradient method](/conjugate-gradient-method/), trading length, curvature and clearance; the implementation does not smooth.

## Example

A corridor 20 m long and 3 m wide, with cells of 1 m and 72 heading bins of 5 degrees. The car has $\rho = 2$ m and primitives of $\ell = 1.5$ m, with $c_r = 2$ and $c_s = 1$. It starts at $(3, 1.5)$ facing $+x$ and must end at $(12, 1.5)$ facing $-x$. A U-turn needs a corridor at least $2\rho = 4$ m wide, so a forward-only search fails: it closes all reachable bins and returns failure in 2 ms.

Measured, with reverse motion and a shot every 5 expansions: the search expands 360 bins in about 10 ms and returns 13 pieces with a length of 18.71 m, of which 3.0 m are in reverse, and 2 changes of direction, a three-point turn. Its cost is $18.71 + 3.0 + 2 = 23.71$. With a shot at every expansion it expands 307 bins and returns a cheaper path, cost 22.39, with 1.5 m in reverse. Without any shot and with a goal tolerance of 0.5 m and 0.1 rad, it expands 2014 bins and returns a path of cost 53.5 with 10 changes of direction. The goal region is small, and pruned bins make it hard to land in it with primitives alone. The grid heuristic does not change the result in this corridor, because the Euclidean distance is already close to the grid distance.

These numbers show two things. The shot is what makes the method practical, and the result depends on when the shot is tried, so the method is not optimal.

## Correctness

The [proof](proofs/correctness/) shows four things. Soundness: every returned path is a chain of car arcs with curvature at most $1/\rho$ that passed the collision test, and it ends in the goal region or exactly at the goal. Termination: each bin is expanded at most once, so the search stops after at most $B = n_x n_y n_\theta$ expansions. The Euclidean heuristic is consistent. Relative optimality: without shots, with the Euclidean heuristic, with $c_s = 0$, and with bins fine enough that no two reachable poses share a bin, the search is A\* on the graph of primitive sequences and returns the cheapest sequence. With coarse bins, neither this optimality nor completeness holds, and the collision test is only as good as its sampling.

## Complexity

- **Time.** At most $B$ expansions, each with six primitives, each checked at $s$ samples, and heap operations of $O(\log B)$: $O(B(\log B + s))$, plus the cost of the shots. The grid heuristic adds a Dijkstra of $O(n_x n_y \log(n_x n_y))$ once per goal. Dolgov et al. use a grid of 160 m by 160 m with 0.5 m cells and 5 degree heading bins, and report replanning times of about 50 to 300 ms on the vehicle (measurement in the paper).
- **Space.** $O(B)$ for the bins and the open list.
- **Measured.** In the tests, random 20 m by 20 m maps with 15% of the cells blocked need from 5 to about 16,000 expansions; CPython does about 20,000 expansions per second on a laptop.

## Properties

- **Not complete.** A pose dropped by line L12 can be the only one that leads to the goal, so the search can fail when a path exists. Finer bins reduce this; they never remove it.
- **Not optimal.** Relative to its primitives, it is optimal only when the bins separate the reachable poses. Against the continuous problem, the primitives with fixed curvature and length miss shorter paths, and the shot found first need not be the best.
- **Drivable paths.** Unlike grid A\*, every path is a path of the car, with the curvature bound and with exact poses.
- **Asymmetric costs.** Reverse motion and gear changes cost more, which gives the natural parking behavior.
- **Heading continuity.** The path is $C^1$ but its curvature jumps between $0$ and $\pm 1/\rho$; the smoothing step of the paper reduces this.

## Variants and improvements

- **More primitives.** More steering values, or several lengths, give smoother paths at a higher branching factor.
- **Heuristic tables.** The nonholonomic heuristic without obstacles depends only on the relative pose, so a table computed once serves all queries.
- **Footprint checks.** Real implementations test the car's rectangle against the obstacle map, often with a precomputed [distance transform](/distance-transform/) or a set of discs.
- **Smoothing.** Dolgov et al. smooth the result with a cost on length, curvature and a Voronoi field for clearance, then interpolate.
- **State lattice.** [State lattice planning](/state-lattice-planning/) keeps the poses on a lattice and gets resolution completeness with respect to it.

## When to use it

Use it for cars and car-like robots in unstructured spaces where reverse motion matters: parking lots, loading docks, U-turns in narrow streets, and open fields. It needs a map that fits in memory as a grid and a goal pose. For structured roads, a lattice or a sampling planner along the lane is more common. If you need guarantees of completeness or optimality, use a [state lattice](/state-lattice-planning/) with resolution completeness on the lattice, or an asymptotically optimal sampling planner such as [RRT\*](/rrt-star/).

## Pitfalls

- **Primitive length vs bin size.** If a primitive is shorter than a bin, its end often falls in the bin of its start, which is closed, and the search stalls. Make $\ell$ at least the diagonal of a bin, or allow successors in the same bin with a better cost.
- **The heading of the bin.** The heading must be reduced modulo $2\pi$ before binning, or $-\pi$ and $\pi$ fall in different bins.
- **Inadmissible grid heuristic.** The 8-connected grid distance can overestimate the true shortest distance, so the search can return a worse path than it could. Dolgov et al. accept this.
- **Collision checks between samples.** A sampled check can miss a thin obstacle between two samples; dilate the obstacles by the sample spacing.
- **Shot frequency.** Shots are cheap to compute but cost a collision check each. Too rare, and the search wastes expansions near the goal; too frequent, and the checks dominate.
- **Goal tolerance.** Without shots, a tight goal tolerance makes the goal very hard to hit with fixed primitives.

## Implementations

## History

The Stanford Racing Team built Junior for the DARPA Urban Challenge of 2007, a race of autonomous cars in a town with traffic, parking and blocked roads. Junior used hybrid A\* to plan in parking lots and for U-turns, and was second in the race. Dolgov, Thrun, Montemerlo and Diebel described the planner at an AAAI workshop in 2008, and in a longer paper in the International Journal of Robotics Research in 2010, with the two heuristics, the analytic Reeds-Shepp expansion and the smoothing. Hybrid A\* became the standard parking planner of many open-source autonomous driving stacks.

## References
