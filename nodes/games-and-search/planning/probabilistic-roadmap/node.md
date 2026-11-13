---
tag: S30SPN
kind: algorithm
slug: probabilistic-roadmap
name: Probabilistic roadmap
aliases:
- PRM
area: games-and-search/planning
level: core
summary: Samples collision-free configurations, connects them into a roadmap, and searches it.
solves: [motion-planning]
model: real-ram
complexity:
  vars: {n: the number of free samples, k: the average number of samples within the connection radius of a sample}
  time: {worst: O(n^2), expected: O(n^2 + n k)}
  space: {extra: O(n k)}
properties: {deterministic: false, randomized: true, online: false}
history:
  year: 1996
  people: [Lydia E. Kavraki, Petr Švestka, Jean-Claude Latombe, Mark H. Overmars]
  note: The PRM paper of 1996 joined the work of the Stanford group and the Utrecht group of the years before.
prereqs: [motion-planning, configuration-space, dijkstra]
see_also: [rapidly-exploring-random-tree, rrt-star, rrt-star-asymptotic-optimality, random-geometric-graph, kd-tree-nearest-neighbor-search, collision-detection, disjoint-set, cell-decomposition]
sources:
  - paper: doi:10.1109/70.508439
    title: Lydia E. Kavraki, Petr Švestka, Jean-Claude Latombe and Mark H. Overmars, Probabilistic roadmaps for path planning in high-dimensional configuration spaces, IEEE Transactions on Robotics and Automation 12(4), 1996
    locator: pages 566 to 580 (the learning phase with construction and expansion steps, the local planner, the connection to neighbors in other components, and the query phase)
  - paper: doi:10.1109/70.660866
    title: Lydia E. Kavraki, Mihail N. Kolountzakis and Jean-Claude Latombe, Analysis of probabilistic roadmaps for path planning, IEEE Transactions on Robotics and Automation 14(1), 1998
    locator: pages 166 to 171 (the failure probability for a path of length L and clearance, exponentially small in the number of samples)
  - paper: doi:10.1142/S0218195999000285
    title: David Hsu, Jean-Claude Latombe and Rajeev Motwani, Path planning in expansive configuration spaces, International Journal of Computational Geometry and Applications 9(4-5), 1999
    locator: pages 495 to 512 (expansive free spaces and the exponential decay of the failure probability)
  - paper: doi:10.1177/0278364911406761
    title: Sertac Karaman and Emilio Frazzoli, Sampling-based algorithms for optimal motion planning, International Journal of Robotics Research 30(7), 2011
    locator: pages 846 to 894 (PRM, sPRM and PRM*; Theorems 29 to 31 on the optimality of PRM and sPRM, Theorems 34 and 35 on PRM* with radius or k nearest neighbors; numbering of arXiv:1105.1186)
  - book: isbn:9780521862059
    title: Steven M. LaValle, Planning Algorithms, Cambridge University Press, 2006
    locator: Section 5.6 (sampling-based roadmaps), Section 5.6.1 (the basic PRM and its variants), Section 5.3.4 (checking a segment for collision)
  - book: isbn:9780262033275
    title: Howie Choset, Kevin M. Lynch, Seth Hutchinson, George Kantor, Wolfram Burgard, Lydia E. Kavraki and Sebastian Thrun, Principles of Robot Motion, MIT Press, 2005
    locator: Chapter 7 (sampling-based algorithms, the PRM, its sampling strategies and its analysis)
---

The probabilistic roadmap (PRM) solves [motion planning](/motion-planning/) by random sampling. In a learning phase it samples free configurations, joins the pairs that are close and that a straight segment links without collision, and so builds a graph, the roadmap, of the free space. In a query phase it links the start and the goal to the roadmap and finds a path with [Dijkstra's algorithm](/dijkstra/). It is probabilistically complete: for a problem with a path of positive clearance, the chance that it fails falls exponentially with the number of samples, but it cannot prove that no path exists.

## In plain words

You must find a way through a dark building, and all you can do is drop a lamp at a random spot and check whether that spot is inside a wall. Drop many lamps. Keep the ones that are in open space. For each new lamp, look at the lamps close to it, and if you can walk in a straight line from one to the other without a wall in between, draw a line on your map.

After many lamps, the lines form a network of safe routes. To travel from A to B, walk from A to a lamp you can see, follow the network to a lamp that sees B, and walk to B. The same network serves many trips. If a passage is very narrow, few lamps land in it, and you need many lamps before the network goes through it.

## The problem

**The model.** The robot has $d$ degrees of freedom, and its [configuration space](/configuration-space/) $\mathcal{C}$ is a box in $\mathbb{R}^d$, or a space that a box covers, such as a torus of angles. The free space $\mathcal{C}_{free}$ is known only through a collision checker, which answers two questions: is the configuration $q$ free, and is the straight segment from $q$ to $q'$ free. The obstacles have complexity $n_o$, and each call of the checker costs time that depends on $n_o$ and on the robot, not on the planner. The checker is the dominant cost in practice, so the cost of a run is measured in calls.

**Input.** The checker, a connection radius $r$, a number $n$ of samples, and then any number of queries $(q_I, q_G)$.

**Output.** For each query, a path in $\mathcal{C}_{free}$ made of straight segments, or failure.

**How it differs from close pages.** The [RRT](/rapidly-exploring-random-tree/) grows one tree from the start for one query, and is better when the query is known in advance or when the robot has differential constraints. The PRM is a *multi-query* method: one roadmap answers many queries in the same scene. The [cell decomposition](/cell-decomposition/) builds an exact or a box graph of $\mathcal{C}_{free}$ and is complete, but only in low dimension. The roadmap of the PRM is a [random geometric graph](/random-geometric-graph/) on the free samples with the edges that the checker accepts.

## The algorithm

```pseudo id=main
PRM-LEARN(n, r)
L1  V ← ∅, E ← ∅
L2  while |V| < n do
L3      q ← a uniform random configuration in C
L4      if q is not free then continue                 ▷ one call of the checker
L5      add q to V
L6      for each q′ in V with ‖q − q′‖ ≤ r, nearest first do
L7          if q and q′ are in the same component then skip   ▷ the forest rule of the 1996 paper
L8          if the segment q q′ is free then add the edge {q, q′} to E, weighted by ‖q − q′‖

PRM-QUERY(q_I, q_G)
L9  A ← the nodes within r of q_I with a free segment to q_I; B ← the same for q_G
L10 if no a ∈ A and b ∈ B lie in the same component then return failure   ▷ else take the nearest such a
L11 return q_I, the shortest path from a to b in (V, E) found by Dijkstra, q_G
```

The components are kept in a [disjoint-set](/disjoint-set/) structure. Line L7 is the forest rule: an edge between two nodes of the same component cannot join new components, so the 1996 paper skips it, and the roadmap is a forest. The *simplified PRM* (sPRM) drops line L7 and tries every pair within $r$. It has the same components, but many more edges and shorter paths. The implementation also tries the direct segment from $q_I$ to $q_G$ first when they are within $r$. The 1996 paper adds an *expansion step* after line L8: it resamples near the nodes that have few edges, to fill hard regions.

## Example

**A hand trace.** A wall $[4, 5] \times [0, 6]$ stands in the square $[0, 10]^2$, with a free passage above it. The radius is $r = 3$. The seven free samples come in the order of the table.

| node | point | links | checks of segments | components after |
|---|---|---|---|---|
| 0 | $(2, 2)$ | none | 0 | 1 |
| 1 | $(3, 4.5)$ | to 0, length 2.693 | 1 | 1 |
| 2 | $(6.5, 2)$ | none, no node within 3 | 0 | 2 |
| 3 | $(3, 7)$ | to 1, length 2.5 | 1 | 2 |
| 4 | $(5.5, 7.5)$ | to 3, length 2.55 | 1 | 2 |
| 5 | $(6.5, 5)$ | to 4, length 2.693, and to 2, length 3.0 | 2 | 1 |
| 6 | $(1, 5)$ | to 1, length 2.062; node 3 at 2.83 is skipped by line L7 | 1 | 1 |

Node 2 is alone until node 5 arrives, because the nodes to the left of the wall are more than 3 away. Node 5 joins the two components. For node 6, node 1 is nearer and is tried first, and after that link node 3 is already in the same component, so the forest rule saves one check. The query from $(1, 1)$ to $(8, 1)$ attaches to nodes 0 and 2 and returns

$$(1, 1), (2, 2), (3, 4.5), (3, 7), (5.5, 7.5), (6.5, 5), (6.5, 2), (8, 1)$$

of length 16.652.

**Forest against sPRM.** A wall $[4.5, 5.5] \times [0, 10]$ has one gap of width 1 at $y \in [3.134, 4.134]$, and two more obstacles stand on its two sides. With $n = 500$ samples, $r = 1.5$, seed 0 and the query from $(1, 1)$ to $(9, 9)$, the two versions give these measured numbers.

| version | edges | checker calls in the learning phase | components | path length |
|---|---|---|---|---|
| PRM, forest rule | 499 | 1075 | 1 | 18.176 |
| sPRM, every pair | 7374 | 8144 | 1 | 12.121 |

The forest has the same single component with 7.6 times fewer checks, but its path is 50 percent longer, because a tree has only one route between two nodes.

**Success rate.** Over 20 seeds on such wall maps with a gap of width 1, $n = 300$ and $r = 1.5$ succeed in 19, 17 and 18 runs out of 20 on three maps, and $n = 500$ succeeds in 20 out of 20, with a median of about 1145 checker calls per run, of which about 70 are in the query. On the same maps with the gap closed, all runs report failure, which is correct here, but a PRM failure is never a proof.

## Correctness

The [proof](proofs/correctness/) shows two things. Every path that PRM-QUERY returns is free, because each of its segments passed the checker. And the planner is probabilistically complete: if a path of length $L$ has clearance $\rho$, so that the ball of radius $\rho$ around each of its points is free, and $r \ge 3\rho/2$, then the query fails with probability at most

$$\left\lceil \frac{2L}{\rho} \right\rceil e^{-\sigma \rho^d n}, \qquad \sigma = \frac{\zeta_d}{2^d \mu(\mathcal{C}_{free})},$$

where $\zeta_d$ is the volume of the unit ball in $\mathbb{R}^d$ and $\mu$ is volume. This is the bound of Kavraki, Kolountzakis and Latombe (1998). The proof places $\lceil 2L/\rho \rceil$ balls of radius $\rho/2$ along the path and uses the [union bound](/union-bound/) on the events that a ball gets no sample.

## Complexity

- **Proved.** With a brute-force neighbor search, the learning phase computes $O(n^2)$ distances and makes $O(n k)$ calls of the segment checker, where $k$ is the average number of samples within $r$. With $r$ fixed and $n$ growing, $k$ grows linearly in $n$, so the work is $\Theta(n^2)$ checks for sPRM. With $r = \gamma (\log n / n)^{1/d}$, as in PRM*, $k = O(\log n)$ in expectation. A [k-d tree](/kd-tree-nearest-neighbor-search/) makes the neighbor search fast in low dimension. The roadmap needs $O(n k)$ space, and a query costs one Dijkstra run, $O(n k + n \log n)$.
- **Proved, in probability.** The failure bound above falls exponentially in $n$, at a rate that depends on the clearance $\rho$, on $L$ and on the volume of $\mathcal{C}_{free}$. Hsu, Latombe and Motwani (1999) give a bound of the same form in terms of how *expansive* the free space is, which captures narrow passages better than the clearance of one path.
- **No worst-case bound.** A passage can be as thin as you like, so no number of samples works for every input.
- **Measured.** The counts of checks in the tables are measured on the maps above. In practice the time of a PRM is the number of checker calls times the cost of one call.

## Properties

- **Probabilistically complete**, but not complete. It never reports that no path exists with certainty.
- **Multi-query.** The learning phase is done once, and each query costs only the attachment and a graph search.
- **Not asymptotically optimal with a fixed radius and the forest rule.** Karaman and Frazzoli prove that PRM with the forest rule is not asymptotically optimal (Theorem 29), that sPRM with a fixed radius is (Theorem 30), and that sPRM with a fixed number $k$ of nearest neighbors is not (Theorem 31). PRM* uses the shrinking radius $r_n = \gamma (\log n / n)^{1/d}$ with $\gamma > 2 (1 + 1/d)^{1/d} (\mu(\mathcal{C}_{free}) / \zeta_d)^{1/d}$, and is asymptotically optimal (Theorem 34).
- **Randomized**, with results that depend on the seed. Tests use fixed seeds.

## Variants and improvements

- **sPRM and PRM\*.** Drop the forest rule, and use the radius of PRM* to keep $O(\log n)$ neighbors and converge to an optimal path. The analysis of the optimal case is on the page on [asymptotic optimality](/rrt-star-asymptotic-optimality/).
- **Lazy PRM.** Build the roadmap without checking the edges, search it, and check only the edges of the path found. Remove the bad edges and search again (Bohlin and Kavraki, 2000).
- **Sampling near obstacles.** Gaussian sampling keeps a sample when it is free and a nearby sample is not. The bridge test keeps the midpoint of two blocked samples when it is free. Obstacle-based PRM pushes samples to the boundary. All three put more samples in narrow passages.
- **Visibility PRM.** Keep a sample only if it sees no guard node or joins two components, which gives a small roadmap.
- **Quasi-random samples.** Halton or lattice points instead of random ones give a deterministic, resolution-complete roadmap.

## When to use it

Use a PRM when many queries come in the same static scene, for example an arm in a fixed work cell, and when the robot has many degrees of freedom, so that exact methods are too slow. Use a tree planner such as the [RRT](/rapidly-exploring-random-tree/) or [RRT-Connect](/rrt-connect/) for a single query, for a scene that changes, or for a robot with differential constraints. Use [RRT*](/rrt-star/) or PRM* when the path must also be short.

## Pitfalls

- **Narrow passages.** Few uniform samples land in a passage of small volume. The failure bound grows with $1/\rho^d$, so in high dimension a thin passage needs a very large $n$.
- **Segment checks at a fixed resolution.** A checker that tests points along the segment at a step $h$ can miss a thin obstacle. Use an exact test, as the implementation does for polygons, or a step tied to the clearance (LaValle, Section 5.3.4).
- **Metric on angles.** The distance in line L6 must measure angles the short way around, or the roadmap misses the links across the wrap.
- **A failure is not a proof.** With a closed gap the PRM fails, but it would also fail with a gap that it did not sample.
- **Long paths.** The forest rule gives a tree and long detours. Smooth the path, or use sPRM or PRM* if the length matters.

## Implementations

## History

Kavraki and Latombe at Stanford, and Overmars and Švestka at Utrecht, developed randomized roadmap planners in the early 1990s, and the joint paper of 1996 named the probabilistic roadmap. Kavraki, Kolountzakis and Latombe proved the failure bound for paths with clearance in 1998, and Hsu, Latombe and Motwani gave the analysis for expansive spaces in 1999. Karaman and Frazzoli introduced PRM* with its shrinking radius in 2011.

## References
