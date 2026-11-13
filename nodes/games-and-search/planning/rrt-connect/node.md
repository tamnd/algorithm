---
tag: 2V2P6G
kind: algorithm
slug: rrt-connect
name: RRT-Connect
aliases:
- bidirectional RRT
area: games-and-search/planning
level: advanced
summary: Grows two RRTs from start and goal and extends each greedily toward the other.
solves: [motion-planning]
model: real-ram
complexity:
  vars: {N: the number of iterations, K: the number of vertices of the two trees at the end}
  time: {worst: O(N K + K^2)}
  space: {extra: O(K)}
properties: {deterministic: false, randomized: true, online: false}
history:
  year: 2000
  people: [James J. Kuffner, Steven M. LaValle]
  note: Kuffner and LaValle gave RRT-Connect at ICRA 2000, for path planning of robots that can move both ways between two configurations.
prereqs: [rapidly-exploring-random-tree]
see_also: [rapidly-exploring-random-tree, rrt-star, probabilistic-roadmap, motion-planning, bidirectional-search, kd-tree-nearest-neighbor-search, collision-detection, kinodynamic-planning]
sources:
  - paper: doi:10.1109/ROBOT.2000.844730
    title: James J. Kuffner and Steven M. LaValle, RRT-Connect, an efficient approach to single-query path planning, Proceedings of the IEEE International Conference on Robotics and Automation, 2000
    locator: volume 2, pages 995 to 1001 (the EXTEND and CONNECT functions, the two trees that swap roles, and experiments with arms and rigid bodies)
  - paper: doi:10.1177/02783640122067453
    title: Steven M. LaValle and James J. Kuffner, Randomized kinodynamic planning, International Journal of Robotics Research 20(5), 2001
    locator: pages 378 to 400 (the RRT and its bidirectional version for systems with differential constraints)
  - paper: doi:10.1109/LRA.2018.2888947
    title: Michal Kleinbort, Kiril Solovey, Zakary Littlefield, Kostas E. Bekris and Dan Halperin, Probabilistic completeness of RRT for geometric and kinodynamic planning with forward propagation, IEEE Robotics and Automation Letters 4(2), 2019
    locator: the proof of probabilistic completeness for the geometric RRT that the argument on this page follows
  - book: isbn:9780521862059
    title: Steven M. LaValle, Planning Algorithms, Cambridge University Press, 2006
    locator: Section 5.5.3 (rapidly exploring dense trees, and the bidirectional planner with two trees that grow toward each other)
---

RRT-Connect solves a single [motion planning](/motion-planning/) query with two [rapidly-exploring random trees](/rapidly-exploring-random-tree/), one rooted at the start and one at the goal. Each iteration extends one tree one step toward a random point, and then the other tree runs CONNECT: it steps greedily toward the new vertex until it reaches it or hits an obstacle. The trees then swap roles. The greedy connection makes it much faster than a single RRT when the robot can move both ways between two configurations, and it stays probabilistically complete.

## In plain words

Two teams search a dark field, one from the entrance and one from the exit. In each round one team grows its rope net by one step toward a random spot, as in the RRT. Then the other team looks at the new knot and walks straight at it, step after step, until it ties onto that knot or runs into a wall.

When the walk ties on, the two nets touch, and you follow one rope back to the entrance and the other to the exit. Then the teams swap jobs, so each net both explores and chases. In open space the chase ends the search at once. Near walls the chase stops early, but the next random step often opens a new line.

## The problem

**The model.** The robot has $d$ degrees of freedom, and its [configuration space](/configuration-space/) $\mathcal{C}$ is a box in $\mathbb{R}^d$. The free space $\mathcal{C}_{free}$ is known only through a collision checker that tests a point or a straight segment. The obstacles have complexity $n_o$, and the cost of one call depends on $n_o$, not on the planner. The checker is the dominant cost in practice, so the cost of a run is measured in calls.

**Input.** The checker, a start $x_{init}$, a goal $x_{goal}$, a step size $\eta > 0$ and a limit $N$ on the number of iterations.

**Output.** A path in $\mathcal{C}_{free}$ made of straight segments from $x_{init}$ to $x_{goal}$, or failure.

**How it differs from close pages.** The [RRT](/rapidly-exploring-random-tree/) grows one tree and must hit a small goal region by chance or by a goal bias. RRT-Connect grows a second tree from the goal, so the goal is a whole tree and not a point. This needs a *reversible* system: a path found from the goal tree backward must be one the robot can follow forward, which is true for the straight segments of a geometric problem but not in general for [kinodynamic planning](/kinodynamic-planning/). It is a random version of [bidirectional search](/bidirectional-search/).

## The algorithm

```pseudo id=main
EXTEND(T, x, η)
L1  x_near ← the vertex of T nearest to x
L2  x_new ← STEER(x_near, x, η)                   ▷ at distance min(η, ‖x − x_near‖) toward x
L3  if the segment x_near x_new is not free then return TRAPPED
L4  add the vertex x_new to T with parent x_near
L5  if x_new = x then return REACHED else return ADVANCED

CONNECT(T, x, η)
L6  repeat S ← EXTEND(T, x, η) until S ≠ ADVANCED
L7  return S

RRT-CONNECT(x_init, x_goal, η, N)
L8  T_a ← the tree with the vertex x_init; T_b ← the tree with the vertex x_goal
L9  for i = 1 to N do
L10     x_rand ← a uniform random point of C
L11     if EXTEND(T_a, x_rand, η) ≠ TRAPPED then      ▷ it added a vertex x_new
L12         if CONNECT(T_b, x_new, η) = REACHED then
L13             return the path of the start tree to x_new, then the path of the goal tree from x_new
L14     swap T_a and T_b
L15 return failure
```

When CONNECT returns REACHED, its last vertex is the point $x_{new}$ itself, so the two tree paths share that point. Line L13 joins them in the right order: start tree first, whichever tree is $T_a$ at that moment. The implementation also checks first that the start and the goal are free.

## Example

**Free space.** With no obstacles, start $(1, 5)$, goal $(9, 5)$ and $\eta = 1$, seed 0 ends in the first iteration. EXTEND adds one vertex $(1.945, 5.327)$ to the start tree, and CONNECT from the goal walks 8 steps straight to it. The run makes 11 calls of the checker: two for the start and the goal, one for EXTEND, and eight for CONNECT.

**A hand trace.** A block $[4, 6] \times [3, 7]$ stands between the start $(1, 5)$ and the goal $(9, 5)$, with $\eta = 1$ and seed 2. The table shows the first six iterations and the last one. The column *connect* gives the result of CONNECT and the number of vertices it added.

| iteration | $T_a$ | $x_{rand}$ | EXTEND | $x_{new}$ | connect |
|---|---|---|---|---|---|
| 1 | start | $(9.56, 9.478)$ | advanced | $(1.886, 5.464)$ | trapped, 3 vertices up to $(6.006, 5.195)$ |
| 2 | goal | $(0.566, 0.849)$ | trapped | none | none |
| 3 | start | $(8.355, 7.36)$ | advanced | $(2.846, 5.745)$ | trapped, 0 vertices |
| 4 | goal | $(6.697, 3.081)$ | advanced | $(6.856, 4.141)$ | trapped, 1 vertex at $(3.774, 5.374)$ |
| 5 | start | $(6.059, 6.068)$ | trapped | none | none |
| 6 | goal | $(5.812, 1.584)$ | advanced | $(6.478, 3.215)$ | trapped, 0 vertices |
| 20 | goal | $(7.344, 9.066)$ | advanced | $(7.15, 7.124)$ | reached, 3 vertices |

In iteration 1, CONNECT from the goal walks toward the new start vertex until the next step would enter the block. In iteration 20 the start tree has climbed over the block to $(4.645, 7.637)$, the goal tree adds a vertex at $(7.15, 7.124)$, and CONNECT from the start tree reaches it in 3 steps. The run makes 39 checker calls, the trees have 12 and 10 vertices, and the path has 13 points and length 11.557. The shortest path has length $2\sqrt{13} + 2 = 9.211$. Seeds 0 to 5 need 20, 57, 20, 26, 30 and 45 iterations.

**RRT-Connect against RRT.** On wall maps with one gap of width 1, the medians over 20 seeds, with $\eta = 0.5$ from $(1, 1)$ to $(9, 9)$, are as follows. No run failed.

| gap at | method | iterations | checker calls | vertices | path length |
|---|---|---|---|---|---|
| $y \in [3, 4]$ | RRT | 123 | 126 | 100 | 14.763 |
| $y \in [3, 4]$ | RRT-Connect | 31 | 72.5 | 45.5 | 13.136 |
| $y \in [6, 7]$ | RRT | 115.5 | 118.5 | 87.5 | 14.403 |
| $y \in [6, 7]$ | RRT-Connect | 28.5 | 76.5 | 47 | 13.295 |

RRT-Connect needs about a quarter of the iterations, 55 to 65 percent of the checks and half of the vertices. Its iterations cost more checks each, because CONNECT makes several steps.

## Correctness

The [proof](proofs/correctness/) shows two things. Every returned path is free and joins $x_{init}$ to $x_{goal}$, because both trees have only free edges and they share the vertex $x_{new}$. And RRT-Connect is probabilistically complete: if a path of length $L$ has clearance $\delta > 0$, let $\nu = \min(\delta/4, \eta/3)$, $m = \lceil L/\nu \rceil$ and $p = \zeta_d \nu^d / \mu(\mathcal{C})$, where $\zeta_d$ is the volume of the unit ball. Then for $N \ge 4(m + 1)/p$ it fails with probability at most $e^{-pN/16}$. The proof looks only at the iterations in which the start tree extends, which are RRT steps without goal bias, and shows that the goal tree connects as soon as the start tree draws a point near the goal.

## Complexity

- **Proved.** Each iteration makes at most one failed EXTEND and at most one failed step of CONNECT, and every other check adds a vertex. So a run makes at most $2N + K$ calls of the segment checker. Each call of EXTEND searches for the nearest vertex, which costs $O(K)$ by brute force, so the time is $O(N K + K^2)$. A [k-d tree](/kd-tree-nearest-neighbor-search/) brings each search down to about $O(\log K)$ in low dimension. One CONNECT adds at most $\lceil D/\eta \rceil$ vertices, where $D$ is the diameter of $\mathcal{C}$. The trees need $O(K)$ space.
- **Proved, in probability.** The failure probability falls exponentially in $N$ for a problem with a path of positive clearance.
- **No worst-case bound.** A passage can be as thin as you like.
- **Measured.** The table above shows the speed-up over RRT on the wall maps. The gain is largest in open spaces with few obstacles, and smallest in maze-like maps, where CONNECT stops after a step or two.

## Properties

- **Probabilistically complete**, but not complete.
- **Not asymptotically optimal.** Like the RRT, a vertex never changes its parent, and the greedy steps follow straight lines toward the other tree, not toward a short path. Smooth the path afterward.
- **Single query, reversible systems.** The goal tree grows backward, so the robot must be able to follow its edges forward.
- **Parameter-light.** It has only the step size $\eta$, and no goal bias or goal radius, since the goal is a tree.
- **Randomized**, with results that depend on the seed. Tests use fixed seeds.

## Variants and improvements

- **EXTEND-EXTEND.** Replace CONNECT in line L12 by one EXTEND. This is more careful near obstacles and closer to the kinodynamic setting, but slower in open space.
- **CONNECT for both trees.** Use CONNECT in line L11 too, so the tree moves greedily toward the random point. This spreads the trees faster in open space, but it adds long chains of vertices.
- **Balanced trees.** Swap the trees in line L14 only when the other tree is smaller, so that both trees keep a similar size.
- **Bidirectional RRT\*.** Add the choice of parent and the rewiring of [RRT\*](/rrt-star/) to both trees to get a path that converges to an optimal one.

## When to use it

Use RRT-Connect for a single query of a geometric problem: an arm, a rigid body, or any robot that can move along a straight segment in both directions. Use the plain [RRT](/rapidly-exploring-random-tree/) for systems with differential constraints, where the goal tree cannot be followed forward. Use [RRT\*](/rrt-star/) when the length of the path matters, and a [probabilistic roadmap](/probabilistic-roadmap/) for many queries in one scene.

## Pitfalls

- **Matching the end points.** CONNECT reaches the point $x_{new}$ exactly only if STEER returns its target when it is within $\eta$. With floating-point steps, test the distance, not equality of computed points.
- **Order of the path.** After the swap in line L14, $T_a$ may be the goal tree. Line L13 must put the start tree first and reverse the goal tree path.
- **Irreversible systems.** A car with a minimum turning radius can follow a goal tree edge only if it is built by the reverse dynamics. Using the forward dynamics for both trees gives paths that the robot cannot follow.
- **Narrow passages.** The greedy chase does not help a tree find a thin passage. Both trees can grow large on the two sides of a wall before a sample hits the gap.
- **A failure is not a proof.**

## Implementations

## History

Kuffner and LaValle published RRT-Connect at ICRA 2000, after the RRT of LaValle (1998), with experiments on arms and rigid bodies. LaValle and Kuffner described bidirectional trees for systems with differential constraints in 2001. Karaman and Frazzoli introduced RRT\* in 2011, and bidirectional versions of it followed. Kleinbort, Solovey, Littlefield, Bekris and Halperin gave a full proof of probabilistic completeness for the geometric RRT in 2019, and the same argument covers the start tree of RRT-Connect.

## References
