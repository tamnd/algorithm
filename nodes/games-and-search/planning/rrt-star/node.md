---
tag: 4RBAE6
kind: algorithm
slug: rrt-star
name: RRT*
aliases:
- RRT-star
area: games-and-search/planning
level: advanced
summary: RRT variant that rewires the tree to converge toward optimal paths.
solves: [motion-planning]
model: real-ram
complexity:
  vars: {n: the number of iterations}
  time: {worst: O(n^3), expected: O(n log n)}
  space: {extra: O(n)}
properties: {deterministic: false, randomized: true, online: false}
history:
  year: 2011
  people: [Sertac Karaman, Emilio Frazzoli]
  note: Karaman and Frazzoli gave RRT* and PRM* in the International Journal of Robotics Research in 2011, with the first proofs that sampling planners can converge to optimal paths.
prereqs: [rapidly-exploring-random-tree]
see_also: [rapidly-exploring-random-tree, rrt-star-asymptotic-optimality, rrt-connect, probabilistic-roadmap, random-geometric-graph, kd-tree-nearest-neighbor-search, kinodynamic-planning, motion-planning]
sources:
  - paper: doi:10.1177/0278364911406761
    title: Sertac Karaman and Emilio Frazzoli, Sampling-based algorithms for optimal motion planning, International Journal of Robotics Research 30(7), 2011
    locator: pages 846 to 894 (RRT* as Algorithm 6 with the radius min(γ (log n / n)^(1/d), η), Theorem 38 on its asymptotic optimality, Theorem 33 on RRT, and Section 4.3 on the number of calls per iteration; numbering of arXiv:1105.1186)
  - paper: doi:10.1109/ICRA40945.2020.9196553
    title: Kiril Solovey, Lucas Janson, Edward Schmerling, Emilio Frazzoli and Marco Pavone, Revisiting the asymptotic optimality of RRT*, Proceedings of the IEEE International Conference on Robotics and Automation, 2020
    locator: pages 2189 to 2195 (a gap in the original proof, and a new proof with the radius exponent 1/(d+1); arXiv:1909.09688)
  - paper: doi:10.1109/IROS.2014.6942976
    title: Jonathan D. Gammell, Siddhartha S. Srinivasa and Timothy D. Barfoot, Informed RRT*, optimal sampling-based path planning focused via direct sampling of an admissible ellipsoidal heuristic, Proceedings of the IEEE/RSJ International Conference on Intelligent Robots and Systems, 2014
    locator: pages 2997 to 3004 (sampling inside the ellipse of points that can improve the current path)
  - book: isbn:9780521862059
    title: Steven M. LaValle, Planning Algorithms, Cambridge University Press, 2006
    locator: Section 5.5.3 (rapidly exploring dense trees, the base of RRT*)
---

RRT\* solves [motion planning](/motion-planning/) with a cost, usually the length of the path, and returns paths whose cost converges to the optimum as the number of samples grows. It grows a tree like the [RRT](/rapidly-exploring-random-tree/), with two changes. Each new vertex takes as parent the near vertex that gives it the least cost, not just the nearest one. And each near vertex whose cost drops when it goes through the new vertex is *rewired* to it. With a near radius that shrinks like $(\log n / n)^{1/d}$, the extra work per iteration is $O(\log n)$ calls of the checker in expectation.

## In plain words

You build a rope net from the entrance of a dark field, as in the RRT. Each knot also has a label: the length of rope from the entrance to it. When you tie a new knot, you do not just tie it to the closest knot. You look at all knots within a small circle, and you tie it to the one that gives the shortest total rope, if the straight piece is clear.

Then you look at the knots in the same circle again. If any of them would have a shorter rope by going through the new knot, you cut its old rope and tie it to the new knot. Over time the net straightens out, and the rope to the exit gets close to the shortest possible route.

## The problem

**The model.** The robot has $d$ degrees of freedom, and its [configuration space](/configuration-space/) $\mathcal{C}$ is a box in $\mathbb{R}^d$. The free space $\mathcal{C}_{free}$ is known only through a collision checker that tests a straight segment. The obstacles have complexity $n_o$, and the cost of one call depends on $n_o$, not on the planner. The checker is the dominant cost in practice, so the cost of a run is measured in calls.

**Input.** The checker, a start $x_{init}$, a goal region $\mathcal{X}_{goal}$, a step size $\eta > 0$, a constant $\gamma$ and a number $n$ of iterations. The cost of a path is its length. Karaman and Frazzoli allow any cost that does not decrease when a path is extended and is at most a constant times the length, and they state the algorithm for an additive cost.

**Output.** A tree of free segments rooted at $x_{init}$. The answer is the tree path to the vertex in $\mathcal{X}_{goal}$ of least cost, or failure if no vertex lies in $\mathcal{X}_{goal}$.

**How it differs from close pages.** The [RRT](/rapidly-exploring-random-tree/) adds the same vertices on the same samples, but each vertex keeps the nearest vertex as its parent, and its path does not converge to the optimum. RRT\* is the tree version of the roadmap PRM\*, which joins each sample to all neighbors within the same kind of radius, see [probabilistic roadmap](/probabilistic-roadmap/). The proof of convergence and its exact hypotheses are on the page on [asymptotic optimality](/rrt-star-asymptotic-optimality/).

## The algorithm

```pseudo id=main
RRT*(x_init, η, γ, n)
L1  V ← {x_init}, cost(x_init) ← 0
L2  for i = 1 to n do
L3      x_rand ← a uniform random point of C
L4      x_nearest ← the vertex of V nearest to x_rand
L5      x_new ← STEER(x_nearest, x_rand, η)
L6      if the segment x_nearest x_new is not free then continue
L7      r ← min(γ (log |V| / |V|)^(1/d), η); X_near ← the vertices within r of x_new
L8      x_min ← x_nearest; c_min ← cost(x_nearest) + ‖x_nearest − x_new‖
L9      for each x ∈ X_near with cost(x) + ‖x − x_new‖ < c_min and a free segment to x_new do x_min ← x, c_min ← that cost
L10     add x_new to V with parent x_min and cost(x_new) ← c_min
L11     for each x ∈ X_near other than x_min do
L12         if c_min + ‖x_new − x‖ < cost(x) and the segment x_new x is free then
L13             make x_new the parent of x, and lower the cost of x and of all its descendants by the same amount
L14 return the tree; the answer is the vertex v ∈ X_goal with the least cost, and its tree path
```

Lines L3 to L6 are the RRT step. Karaman and Frazzoli draw $x_{rand}$ from $\mathcal{C}_{free}$. The implementation draws it from the box $\mathcal{C}$, as the RRT does, so a free ball gets a sample with probability proportional to its volume over $\mu(\mathcal{C})$ and not over $\mu(\mathcal{C}_{free})$. Line L9 is the *choice of parent*: it tests the segment only for the neighbors that would improve the cost, in increasing order of that cost if you sort them. Lines L11 to L13 are the *rewiring*. The implementation keeps the costs in an array and pushes each drop down the subtree in line L13, uses a uniform grid with cells of side $\eta$ for the near queries, and remembers the result of a segment test from line L9 so that line L12 does not repeat it.

## Example

**One step by hand.** The tree has the vertices $A = (0, 0)$ with cost 0, $B = (2, 0)$ with parent $A$ and cost 2, $C = (2, 2)$ with parent $B$ and cost 4, and $D = (4, 1)$ with parent $C$ and cost $4 + \sqrt{5} = 6.2361$. A small box $[1.3, 1.7] \times [0.4, 0.9]$ is an obstacle. The sample is $x_{rand} = (3, 1)$, with $\eta = 4$ and $\gamma = 10.749$, so the radius is $\min(10.749 \sqrt{\ln 4 / 4}, 4) = \min(6.33, 4) = 4$, and all four vertices are near. The nearest vertex is $D$ at distance 1, and $x_{new} = (3, 1)$.

| vertex | cost | $\lVert x - x_{new} \rVert$ | cost through it | segment to $x_{new}$ |
|---|---|---|---|---|
| $D$, nearest | 6.2361 | 1 | 7.2361 | free, from line L6 |
| $A$ | 0 | 3.1623 | 3.1623 | blocked by the box |
| $B$ | 2 | 1.4142 | 3.4142 | free |
| $C$ | 4 | 1.4142 | 5.4142 | not tested, no gain over $B$ |

So $x_{new}$ gets the parent $B$ and the cost 3.4142, not the parent $D$ that the RRT would give. In the rewiring, $D$ would cost $3.4142 + 1 = 4.4142 < 6.2361$ through $x_{new}$, so $D$ is rewired to $x_{new}$. $C$ would cost $3.4142 + 1.4142 = 4.8284$, which is more than its cost 4, so it keeps its parent. The step makes 3 calls of the checker, since the test for $D$ is reused.

**Convergence.** A block $[4, 6] \times [3, 7]$ stands in the square $[0, 10]^2$. The start is $(1, 5)$, the goal is the point $(9, 5)$, which a path reaches by a last free segment from a vertex within distance 1 of it, and $\eta = 1$. The optimum is $c^* = 2\sqrt{13} + 2 = 9.2111$. The threshold of Theorem 38 with $\mu(\mathcal{C}) = 100$ in place of $\mu(\mathcal{C}_{free})$ is $\gamma^* = 9.772$, and the runs use $\gamma = 1.1 \gamma^* = 10.749$. The table gives the best cost after each number of iterations for three seeds.

| iterations | seed 0 | seed 1 | seed 2 |
|---|---|---|---|
| 250 | 10.6642 | 11.7411 | 11.2389 |
| 500 | 9.7459 | 9.9446 | 10.5064 |
| 1000 | 9.6491 | 9.7356 | 9.5014 |
| 2000 | 9.3573 | 9.4338 | 9.3277 |
| 4000 | 9.3351 | 9.3393 | 9.3064 |
| 8000 | 9.2804 | 9.3067 | 9.2873 |
| 16000 | 9.2654 | 9.2639 | 9.2715 |

At 16000 iterations the best cost is within 0.7 percent of $c^*$. For seed 0, 4000 iterations give 3641 vertices and 14592 calls of the checker, about 3.6 calls per iteration, and 16000 iterations give about 14700 vertices and 58000 calls. The number of calls per iteration stays near 3.6, below the $O(\log n)$ bound, because line L9 tests only the neighbors that would lower the cost and line L12 reuses those tests.

**Against RRT.** The same code with radius 0 is the RRT without goal bias. Its best cost stays far from $c^*$.

| iterations | RRT, seed 0 | RRT, seed 1 | RRT, seed 2 | RRT\*, seed 0 | RRT\*, seed 1 | RRT\*, seed 2 |
|---|---|---|---|---|---|---|
| 1000 | 10.8999 | 13.9219 | 11.6231 | 9.6491 | 9.7356 | 9.5014 |
| 4000 | 10.8999 | 13.334 | 11.6231 | 9.3351 | 9.3393 | 9.3064 |
| 16000 | 10.8999 | 13.334 | 11.6231 | 9.2654 | 9.2639 | 9.2715 |

## Correctness

The [proof](proofs/correctness/) shows four things. The vertices and edges always form a tree of free segments, and line L13 cannot make a cycle, because a vertex on the path to $x_{new}$ never passes the test of line L12. The stored cost of each vertex is the length of its tree path. Costs never increase, so the best cost to the goal region never increases. And RRT\* adds the same vertices as the RRT on the same samples, so it is probabilistically complete with the same bound. Convergence to the optimal cost is the content of the [optimality theorem](/rrt-star-asymptotic-optimality/), which needs $\gamma$ above a threshold that depends on $d$ and on $\mu(\mathcal{C}_{free})$.

## Complexity

- **Proved, in expectation.** With the radius of line L7 and $\gamma$ fixed, the expected size of $X_{near}$ is $O(\log n)$, so each iteration makes $O(\log n)$ calls of the checker, and $n$ iterations make $O(n \log n)$ calls (Karaman and Frazzoli, Section 4.3). With a nearest-neighbor structure that answers the near and nearest queries in $O(\log n)$ time, the total time is $O(n \log n)$ in expectation, within a constant factor of the RRT.
- **Proved, worst case.** In this implementation one rewiring step can touch every vertex, and $X_{near}$ can hold every vertex while the radius is $\eta$, so a single iteration can cost $O(n^2)$, and $n$ iterations $O(n^3)$. This does not happen in practice.
- **Space.** The tree needs $O(n)$ space.
- **Measured.** On the block map, the number of checker calls per iteration is about 3.6 at 4000 iterations, and the best cost falls as in the table. The rate of convergence is not part of the theorem.

## Properties

- **Asymptotically optimal**, under the hypotheses of the [optimality theorem](/rrt-star-asymptotic-optimality/). Karaman and Frazzoli state this for $\gamma > (2(1 + 1/d))^{1/d} (\mu(\mathcal{C}_{free}) / \zeta_d)^{1/d}$ (Theorem 38). Solovey, Janson, Schmerling, Frazzoli and Pavone (2020) found a gap in that proof and proved convergence in probability for the radius $\gamma (\log n / n)^{1/(d+1)}$.
- **Probabilistically complete**, with the same vertices as the RRT.
- **Anytime.** The best cost never increases, so the run can stop at any time with the best path so far.
- **Single query.** The tree is rooted at the start.
- **Randomized**, with results that depend on the seed. Tests use fixed seeds.

## Variants and improvements

- **k nearest neighbors.** Use the $k = \lceil k_{RRT^*} \log |V| \rceil$ nearest vertices instead of a radius, with $k_{RRT^*} > 2^{d+1} e (1 + 1/d)$ (Karaman and Frazzoli, Theorem 39).
- **Informed RRT\*.** After a first solution of cost $c$, sample only in the ellipse of points whose distances to the start and the goal sum to less than $c$, since no other point can be on a better path (Gammell, Srinivasa and Barfoot, 2014). This speeds up convergence a lot in large spaces.
- **RRG.** Keep all the free edges to $X_{near}$ instead of a tree, which gives a graph with the same optimality guarantee.
- **Bidirectional RRT\*.** Grow two trees as in [RRT-Connect](/rrt-connect/) and rewire both.
- **Kinodynamic RRT\*.** Replace the straight segments by optimal trajectories of the dynamics between two states, which needs an exact steering function, see [kinodynamic planning](/kinodynamic-planning/).

## When to use it

Use RRT\* when the path must be short and you can spend more time after the first solution, for example for an arm in a cluttered cell or a mobile robot in a fixed map. Use the [RRT](/rapidly-exploring-random-tree/) or [RRT-Connect](/rrt-connect/) when any path will do, since they find one with fewer checks. Use PRM\* from the [probabilistic roadmap](/probabilistic-roadmap/) page when many queries come in one scene, and a grid search such as [A\*](/a-star-search/) in two or three dimensions.

## Pitfalls

- **The constant $\gamma$.** The threshold depends on $\mu(\mathcal{C}_{free})$, which is often unknown. Using $\mu(\mathcal{C})$ gives a larger value, which is safe for the theorem, as in the example. A $\gamma$ below the threshold can stop the convergence.
- **The radius formula.** The radius uses the number of vertices, not the number of iterations, and it is capped by $\eta$. The logarithm is the natural one, as in the threshold.
- **Stale costs.** After a rewiring, all descendants of the rewired vertex must get the lower cost, or later choices of parent use wrong costs.
- **Slow convergence.** The theorem says nothing about the rate. In high dimension the cost can stay well above $c^*$ for a long time.
- **Exact steering.** The rewiring needs a path between two given configurations. For straight segments this is free, but for robots with dynamics it is a hard boundary value problem.

## Implementations

## History

Karaman and Frazzoli introduced RRT\*, RRG and PRM\* in 2011 and proved that RRT and PRM with the forest rule are not asymptotically optimal while the new methods are. Gammell, Srinivasa and Barfoot added informed sampling in 2014. In 2020, Solovey, Janson, Schmerling, Frazzoli and Pavone showed a gap in the proof of the 2011 theorem for RRT\* and gave a new proof with a larger radius, of order $(\log n / n)^{1/(d+1)}$.

## References
