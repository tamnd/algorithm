---
tag: C6S6KW
kind: algorithm
slug: rapidly-exploring-random-tree
name: Rapidly-exploring random tree
aliases:
- RRT
area: games-and-search/planning
level: core
summary: Grows a tree from the start by extending toward random samples, biased to explore.
solves: [motion-planning]
model: real-ram
complexity:
  vars: {N: the number of iterations}
  time: {worst: O(N^2)}
  space: {extra: O(N)}
properties: {deterministic: false, randomized: true, online: false}
history:
  year: 1998
  people: [Steven M. LaValle]
  note: LaValle introduced the RRT in a technical report of Iowa State University in October 1998.
prereqs: [motion-planning, nearest-neighbor-search]
see_also: [rrt-connect, rrt-star, probabilistic-roadmap, kinodynamic-planning, voronoi-diagram, kd-tree-nearest-neighbor-search, collision-detection, rrt-star-asymptotic-optimality]
sources:
  - paper: "Steven M. LaValle, Rapidly-exploring random trees, a new tool for path planning, Technical Report TR 98-11, Computer Science Department, Iowa State University, 1998"
    locator: the whole report (the EXTEND step toward a random sample, the nearest vertex, and the bias toward large Voronoi regions)
  - paper: doi:10.1177/02783640122067453
    title: Steven M. LaValle and James J. Kuffner, Randomized kinodynamic planning, International Journal of Robotics Research 20(5), 2001
    locator: pages 378 to 400 (the RRT for systems with differential constraints, its Voronoi bias and the argument for probabilistic completeness)
  - paper: doi:10.1177/0278364911406761
    title: Sertac Karaman and Emilio Frazzoli, Sampling-based algorithms for optimal motion planning, International Journal of Robotics Research 30(7), 2011
    locator: pages 846 to 894 (RRT as Algorithm 3, Theorem 16 on its probabilistic completeness after LaValle and Kuffner, Lemma 42 on one check per iteration, Theorem 33 and Appendix B on why it is not asymptotically optimal; numbering of arXiv:1105.1186)
  - paper: doi:10.1109/LRA.2018.2888947
    title: Michal Kleinbort, Kiril Solovey, Zakary Littlefield, Kostas E. Bekris and Dan Halperin, Probabilistic completeness of RRT for geometric and kinodynamic planning with forward propagation, IEEE Robotics and Automation Letters 4(2), 2019
    locator: the proof of probabilistic completeness for the geometric RRT, and the gap it closes in the earlier argument for the kinodynamic RRT
  - book: isbn:9780521862059
    title: Steven M. LaValle, Planning Algorithms, Cambridge University Press, 2006
    locator: Section 5.5 (incremental sampling and searching), Section 5.5.3 (rapidly exploring dense trees, the Voronoi bias, and the step size)
  - book: isbn:9780262033275
    title: Howie Choset, Kevin M. Lynch, Seth Hutchinson, George Kantor, Wolfram Burgard, Lydia E. Kavraki and Sebastian Thrun, Principles of Robot Motion, MIT Press, 2005
    locator: Chapter 7 (sampling-based algorithms, including the tree planners)
---

The rapidly-exploring random tree (RRT) solves [motion planning](/motion-planning/) for one query by growing a tree from the start. Each step draws a random configuration, finds the nearest vertex of the tree, and adds a new vertex a short step toward the random point if the step is free. A vertex is extended with a probability equal to the volume of its Voronoi cell, so the tree grows fast into the large unexplored parts of the space. The RRT is probabilistically complete, but the path it returns does not converge to a shortest one.

## In plain words

You stand at the entrance of a dark field with obstacles, and you hold a rope. Someone calls out a random spot in the field. You find the knot on your rope net that is closest to that spot, and you walk one step from it toward the spot. If the step does not hit anything, you tie a new knot there.

Spots far from the net are closer to the knots at its edge than to the knots inside, so most new knots grow at the edge, into open space. After many calls the net spreads over the whole field, and when a knot lands near the exit, you follow the rope back to the entrance. The route works, but it zigzags, because no knot ever changes the knot it hangs from.

## The problem

**The model.** The robot has $d$ degrees of freedom, and its [configuration space](/configuration-space/) $\mathcal{C}$ is a box in $\mathbb{R}^d$. The free space $\mathcal{C}_{free}$ is known only through a collision checker that tests a point or a straight segment. The obstacles have complexity $n_o$, and the cost of one call depends on $n_o$, not on the planner. The checker is the dominant cost in practice, so the cost of a run is measured in calls, with the time of the nearest-vertex search as a second term.

**Input.** The checker, a start $x_{init}$, a goal $x_{goal}$, a step size $\eta > 0$, a goal radius $r_{goal}$, a goal bias $p_{goal} \in [0, 1)$ and a limit $N$ on the number of iterations.

**Output.** A path in $\mathcal{C}_{free}$ made of straight segments from $x_{init}$ to $x_{goal}$, or failure.

**How it differs from close pages.** The [probabilistic roadmap](/probabilistic-roadmap/) builds a graph for many queries. The RRT grows one tree for one query, and it needs no connection between two given configurations, only a step forward, so it also works for robots with differential constraints, see [kinodynamic planning](/kinodynamic-planning/). [RRT-Connect](/rrt-connect/) grows two trees and joins them. [RRT\*](/rrt-star/) adds a choice of the best parent and a rewiring step, which makes the path converge to an optimal one.

## The algorithm

```pseudo id=main
RRT(x_init, x_goal, η, N, p_goal, r_goal)
L1  T ← the tree with the single vertex x_init
L2  for i = 1 to N do
L3      x_rand ← x_goal with probability p_goal, else a uniform random point of C
L4      x_near ← the vertex of T nearest to x_rand
L5      x_new ← STEER(x_near, x_rand, η)        ▷ the point at distance min(η, ‖x_rand − x_near‖) toward x_rand
L6      if the segment x_near x_new is not free then continue   ▷ one call of the checker
L7      add the vertex x_new to T with parent x_near
L8      if ‖x_new − x_goal‖ ≤ r_goal and the segment x_new x_goal is free then
L9          return the path of T from x_init to x_new, then x_goal
L10 return failure
```

The random point in line L3 is not added to the tree. Only the new point of line L5 is, and it is at most $\eta$ from its parent. The goal bias $p_{goal}$, often 0.05, pulls the tree toward the goal from time to time. The implementation also checks first that the start and the goal are free, so a run of $i$ iterations that ends at the goal makes $i + 3$ calls of the checker.

## Example

**A hand trace.** A block $[4, 6] \times [3, 7]$ stands in the square $[0, 10]^2$. The tree starts at $(1, 5)$, with $\eta = 1$ and no goal bias, and seed 4 gives the random points of the table. Numbers are rounded to three places.

| iteration | $x_{rand}$ | $x_{near}$ | $x_{new}$ | result |
|---|---|---|---|---|
| 1 | $(2.36, 1.032)$ | 0 | $(1.324, 4.054)$ | vertex 1 |
| 2 | $(3.961, 1.55)$ | 1 | $(2.049, 3.365)$ | vertex 2 |
| 3 | $(0.665, 4.016)$ | 1 | $(0.665, 4.016)$ | vertex 3, the random point is within $\eta$ |
| 4 | $(9.18, 8.005)$ | 2 | $(2.888, 3.911)$ | vertex 4 |
| 5 | $(7.652, 2.219)$ | 4 | $(3.83, 3.576)$ | vertex 5 |
| 6 | $(5.367, 2.767)$ | 5 | $(4.715, 3.11)$ | rejected, the step enters the block |
| 7 | $(1.727, 1.062)$ | 2 | $(1.911, 2.375)$ | vertex 6 |
| 8 | $(2.144, 9.275)$ | 0 | $(1.259, 5.966)$ | vertex 7 |

In iteration 4 the random point is far in the upper right, but the nearest vertex is vertex 2 in the lower left, so the step goes toward it from there.

**The Voronoi bias.** After the trace, the share of the square that is nearest to each vertex, measured on a grid of $400 \times 400$ points, is as follows.

| vertex | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| share of the square | 0.019 | 0.012 | 0.013 | 0.020 | 0.037 | 0.553 | 0.107 | 0.238 |

Vertex 5, at the right edge of the tree, will be extended in 55 percent of the next iterations, while the vertices inside the cluster near the start are extended in 1 to 2 percent. This is the bias that gives the method its name.

**Full runs.** On the same map with $\eta = 1$, $r_{goal} = 1$ and $p_{goal} = 0.05$, from $(1, 5)$ to $(9, 5)$, seeds 0 to 4 need 77, 53, 35, 72 and 43 iterations and return paths of length 14.332, 12.933, 11.957, 11.408 and 12.627. The shortest path has length $2\sqrt{13} + 2 = 9.211$.

**RRT against RRT-Connect.** On wall maps with one gap of width 1, the medians over 20 seeds, with $\eta = 0.5$ from $(1, 1)$ to $(9, 9)$, are as follows. No run failed.

| gap at | method | iterations | checker calls | vertices | path length |
|---|---|---|---|---|---|
| $y \in [3, 4]$ | RRT | 123 | 126 | 100 | 14.763 |
| $y \in [3, 4]$ | RRT-Connect | 31 | 72.5 | 45.5 | 13.136 |
| $y \in [6, 7]$ | RRT | 115.5 | 118.5 | 87.5 | 14.403 |
| $y \in [6, 7]$ | RRT-Connect | 28.5 | 76.5 | 47 | 13.295 |

**No convergence.** With more samples the RRT path does not approach the optimum. On the block map with goal radius 1, the best path in the tree after 1000, 4000 and 16000 samples has length 10.8999 at all three sizes for seed 0, and 13.9219, 13.334 and 13.334 for seed 1, against the optimum 9.2111. The [RRT\*](/rrt-star/) page shows the same runs with rewiring.

## Correctness

The [proof](proofs/correctness/) shows two things. Every returned path is free and joins $x_{init}$ to $x_{goal}$, because every edge passed the checker in line L6 and the last segment passed it in line L8. And the RRT is probabilistically complete: if a path of length $L$ has clearance $\delta > 0$, let $\nu = \min(\delta/4, \eta/3, r_{goal})$, $m = \lceil L/\nu \rceil$ and

$$p = (1 - p_{goal}) \frac{\zeta_d \nu^d}{\mu(\mathcal{C})},$$

where $\zeta_d$ is the volume of the unit ball. Then for $N \ge 2m/p$ the RRT fails with probability at most $e^{-pN/8}$. The proof puts $m + 1$ balls of radius $\nu$ along the path and shows that a random point in the next ball always adds a vertex in it, whatever vertex is nearest.

## Complexity

- **Proved.** Each iteration makes at most two calls of the checker, so a run makes $O(N)$ calls. With a brute-force nearest-vertex search, iteration $i$ costs $O(i)$ distance computations, and the whole run costs $O(N^2)$ time. A [k-d tree](/kd-tree-nearest-neighbor-search/) or an approximate [nearest-neighbor search](/nearest-neighbor-search/) brings this down to about $O(N \log N)$ in low dimension. The tree needs $O(N)$ space.
- **Proved, in probability.** The failure probability falls exponentially in $N$ for a problem with a path of positive clearance (Karaman and Frazzoli, Theorem 16, after LaValle and Kuffner; Kleinbort et al., 2019). The rate depends on the clearance, the step size and the dimension.
- **No worst-case bound.** A passage can be as thin as you like, so no $N$ works for every input.
- **Measured.** The counts in the tables are measured on the maps above. In practice the time is the number of checker calls times the cost of one call, plus the nearest-vertex search, which dominates when the checker is cheap and the tree is large.

## Properties

- **Probabilistically complete**, but not complete. A failure after $N$ iterations is not a proof that no path exists.
- **Not asymptotically optimal.** Karaman and Frazzoli prove that the cost of the best RRT path converges with probability 1 to a value that is larger than the optimum when the optimal paths have measure zero (Theorem 33). The reason is that a vertex never changes its parent.
- **Single query.** The tree is rooted at the start and serves one goal.
- **No steering between two given states.** The method only needs to move from a vertex toward a point, not to reach it, so it fits systems with differential constraints.
- **Randomized**, with results that depend on the seed. Tests use fixed seeds.

## Variants and improvements

- **Goal bias.** Line L3 with $p_{goal} > 0$ draws the goal from time to time. A large bias makes the tree greedy and slow in maps with traps.
- **Extend or connect.** The step of line L5 can be repeated toward the same random point until it is reached or blocked. [RRT-Connect](/rrt-connect/) uses this greedy step with two trees.
- **RRT\* and RRG.** Choose the parent with the lowest cost among the near vertices and rewire them through the new vertex, see [RRT\*](/rrt-star/) and its [optimality theorem](/rrt-star-asymptotic-optimality/).
- **Kinodynamic RRT.** Replace the straight step by a control applied for a short time from $x_{near}$, which gives a tree of feasible trajectories, see [kinodynamic planning](/kinodynamic-planning/).
- **Rapidly exploring dense trees.** LaValle (2006, Section 5.5) replaces the random samples by any dense sequence, which gives a deterministic, resolution-complete version.

## When to use it

Use the RRT for a single query in a space of moderate or high dimension, and for robots whose motion is constrained, where a roadmap needs a local planner that may not exist. Use [RRT-Connect](/rrt-connect/) when the robot can move both ways between two configurations, since two trees find a path much faster. Use [RRT\*](/rrt-star/) when the path must be short. Use a [probabilistic roadmap](/probabilistic-roadmap/) when many queries come in the same scene, and a grid search such as [A\*](/a-star-search/) when the space has two or three dimensions and a grid is fine enough.

## Pitfalls

- **The step size.** A large $\eta$ makes many steps fail near obstacles, and a small one makes the tree slow to spread. The proof needs $\eta$ fixed and positive.
- **The metric.** The nearest vertex in line L4 depends on the metric. With angles, measure the short way around, and with mixed units, scale the axes, or the Voronoi bias favors the wrong directions.
- **Zigzag paths.** The path is far from short. Smooth it by shortcutting, or use RRT\*.
- **Narrow passages.** The Voronoi bias pushes the tree to large open regions, not into thin passages, which a uniform sample rarely hits.
- **Uniform sampling of $\mathcal{C}$, not of $\mathcal{C}_{free}$.** A random point inside an obstacle is still useful, because it pulls the tree toward that side. Rejecting it changes the bias.

## Implementations

## History

LaValle introduced the RRT in a technical report of Iowa State University in 1998, as a tree planner that handles differential constraints. LaValle and Kuffner gave the kinodynamic version and its analysis in 1999 and in a journal paper in 2001, and Kuffner and LaValle published RRT-Connect in 2000. Karaman and Frazzoli proved in 2011 that the RRT is not asymptotically optimal and gave RRT\*. Kleinbort, Solovey, Littlefield, Bekris and Halperin gave a full proof of probabilistic completeness in 2019, and they showed a gap in the earlier argument for the kinodynamic case.

## References
