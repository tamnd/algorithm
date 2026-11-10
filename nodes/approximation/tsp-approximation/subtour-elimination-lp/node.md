---
tag: 9FWRE5
kind: concept
slug: subtour-elimination-lp
name: Subtour elimination linear program
aliases:
- Dantzig-Fulkerson-Johnson LP
- subtour LP
- Held-Karp LP
area: approximation/tsp-approximation
level: advanced
summary: The LP relaxation of the symmetric TSP with degree constraints and one cut constraint for each vertex subset; its separation is a minimum cut, and its integrality gap is between 4/3 and 3/2.
prereqs: [linear-programming-problem, lp-relaxation, traveling-salesman-problem, global-min-cut-problem, integrality-gap]
see_also: [held-karp-bound, separation-oracle, ellipsoid-method, cutting-plane-method, branch-and-cut, stoer-wagner, christofides-algorithm, karlin-klein-oveis-gharan-algorithm]
sources:
  - paper: doi:10.1287/opre.2.4.393
    title: George B. Dantzig, D. Ray Fulkerson and Selmer M. Johnson, Solution of a large-scale traveling-salesman problem, Operations Research 2(4), 1954
    locator: pages 393 to 410
  - title: Laurence A. Wolsey, Heuristic analysis, linear programming and branch and bound, Mathematical Programming Study 13, 1980
    locator: pages 121 to 134 (Christofides' tour costs at most 3/2 of the LP value)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: the subtour LP for the TSP and its integrality gap (index entry subtour LP)
  - book: isbn:9783662560389
    title: Bernhard Korte and Jens Vygen, Combinatorial Optimization, sixth edition
    locator: Chapter 21, The Traveling Salesman Problem (the subtour polytope and its separation)
  - title: Anna R. Karlin, Nathan Klein and Shayan Oveis Gharan, A (slightly) improved bound on the integrality gap of the subtour LP for TSP, Proceedings of FOCS 2022
    locator: pages 832 to 843
---

The subtour elimination LP is the standard [linear programming relaxation](/lp-relaxation/) of the symmetric [traveling salesman problem](/traveling-salesman-problem/). It asks for a fractional edge vector with degree 2 at each vertex and at least 2 units across each cut. Dantzig, Fulkerson and Johnson (1954) used it to solve a 49-city instance, and its value LP* equals the [Held-Karp bound](/held-karp-bound/). It has one constraint for each vertex subset, but a violated constraint can be found by a [global minimum cut](/global-min-cut-problem/), so the LP can be solved in polynomial time. For metric costs its [integrality gap](/integrality-gap/) is at least 4/3 and at most 3/2.

## In plain words

Describe a round trip by a number for each road: 1 if the trip uses the road and 0 if not. Then each city has exactly two roads with the number 1. But two separate small loops also have this property, and they are not one round trip.

To forbid such small loops, ask for one more thing: for each way to split the cities into two groups, at least two roads with the number 1 go between the groups. A single round trip passes each split at least twice.

Now allow fractions, such as one half for a road. The cheapest fractional answer can be found fast, and it is never more than the best trip. This gives a lower bound, and it is the starting point of the best exact solvers and of several approximation algorithms.

## The idea

Let $G = (V, E)$ be the complete graph on $n \ge 3$ vertices with costs $c_e \ge 0$. For $S \subseteq V$, $\delta(S)$ is the set of edges with one end in $S$, and $E(S)$ is the set of edges with both ends in $S$. The LP is

$$\text{LP}^* = \min \sum_{e \in E} c_e x_e \quad \text{subject to} \quad x(\delta(v)) = 2 \ \ (v \in V), \quad x(\delta(S)) \ge 2 \ \ (\emptyset \ne S \subsetneq V), \quad 0 \le x_e \le 1.$$

The 0/1 solutions are exactly the tours. With the degree constraints, $x(\delta(S)) = 2|S| - 2x(E(S))$, so each cut constraint is the same as the *subtour elimination constraint* $x(E(S)) \le |S| - 1$: at most $|S| - 1$ edges inside $S$, so no cycle on $S$ alone. So LP* $\le$ OPT. Without the cut constraints the LP is the fractional 2-matching relaxation, whose 0/1 solutions are sets of disjoint cycles.

**Separation.** There are $2^n - 2$ cut constraints. Given $x$ that satisfies the degree constraints and the bounds, give each edge $e$ the capacity $x_e$. Some cut constraint is violated exactly when the global minimum cut of this weighted graph is less than 2. The [Stoer-Wagner algorithm](/stoer-wagner/) finds that cut in $O(nm + n^2 \log n)$ time on the $m$ edges with $x_e > 0$; a [Gomory-Hu tree](/gomory-hu-tree/) gives all of the minimum cuts. So the LP has a polynomial [separation oracle](/separation-oracle/), and by the [ellipsoid method](/ellipsoid-method/) of Grötschel, Lovász and Schrijver it can be solved in polynomial time.

**A compact form.** By the [max-flow min-cut theorem](/max-flow-min-cut-theorem/), $x(\delta(S)) \ge 2$ for all $S$ holds exactly when, for a fixed vertex $r$ and each $v \ne r$, a flow of value 2 from $r$ to $v$ fits in the capacities $x$. Writing these $n - 1$ flows as variables gives an LP of polynomial size with the same value, which any polynomial LP method solves.

**In practice.** The [cutting plane method](/cutting-plane-method/) starts with the degree constraints, solves the LP with the [simplex method](/simplex-method/), finds a violated cut, adds it, and solves again. First the connected components of the support give cuts of value 0; then minimum cuts give the rest. This loop is the core of [branch and cut](/branch-and-cut/) codes such as Concorde.

**The integrality gap.** For metric costs, let the gap be the largest ratio OPT/LP* over all instances.

- *At most 3/2.* Wolsey (1980) showed that [Christofides' tour](/christofides-algorithm/) costs at most $\tfrac32 \cdot \text{LP}^*$: the vector $(1 - 1/n)x^*$ lies in the [spanning tree polytope](/spanning-tree-polytope/), and $x^*/2$ is a fractional cover of the cuts with an odd number of odd-degree vertices of the tree. Karlin, Klein and Oveis Gharan (2022) improved the bound to $3/2 - 10^{-36}$. These two bounds are cited here.
- *At least 4/3.* The family below has OPT/LP* $= (4k + 2)/(3k + 3)$, which tends to $4/3$. The *4/3 conjecture* says that the gap is exactly 4/3; it is open.

**The 4/3 family.** For $k \ge 1$, take three paths $P_1, P_2, P_3$ of $k$ unit edges each. Their left ends form a triangle of unit edges, and so do their right ends. The costs are the shortest path distances in this graph $H$, which has $n = 3k + 3$ vertices.

*LP* $= 3k + 3$. Put $x_e = 1$ on the path edges and $x_e = 1/2$ on the six triangle edges. Each end of a path has degree $1 + \tfrac12 + \tfrac12 = 2$, and each inner vertex has degree 2. For a cut $\delta(S)$: if $S$ splits two or more paths, two path edges of value 1 cross it. If $S$ splits no path, some path lies in $S$ and some outside, so each triangle is split and gives $2 \cdot \tfrac12$, which is 2 in total. If $S$ splits exactly one path, then it crosses that path at least once, and the ends of the split path lie on different sides (else two path edges cross); then a short check of the two other paths, each wholly in $S$ or wholly outside, shows that the triangles give at least 1 more. So $x$ is feasible, with cost $3k + 6 \cdot \tfrac12 = 3k + 3$. Each cost between two different vertices is at least 1, and $\sum_e x_e = n$, so LP* $\ge n = 3k + 3$.

*OPT* $= 4k + 2$ (a proof sketch). A tour in the metric is a closed walk in $H$ through all vertices, so OPT is the least size of a connected multigraph on the edges of $H$ that spans all vertices and has even degrees. An inner vertex of a path has only its two path edges, so along each path all used edges have the same parity, and a path can miss at most one edge (two missed edges would cut off the vertices between them). If a path misses an edge, each of its other $k - 1$ edges is used at least twice, because the part beyond it is reached only through it and parity needs an even number. A cut through one edge of each path (through the missed edge if there is one) separates the two triangles, so it is crossed an even number of times, at least 2. If no path misses an edge: either all three paths are even, costing $6k$, or exactly two are odd, costing $4k$, and then at each triangle the two odd ends need a triangle edge, for $4k + 2$ in all. If one path misses an edge, the other two are both odd or both even; both odd costs $2k + 2(k - 1)$ plus at least two triangle edges at each side, to join the end of the dip with even degree, so $4k + 2$ again; the other cases cost more. All three paths cannot miss an edge, because then the two sides are not joined. A tour of cost $4k + 2$ walks $P_1$ from left to right, steps to the right end of $P_3$, walks into $P_3$ and back, steps to $P_2$, walks $P_2$ from right to left, steps to the left end of $P_3$, walks into $P_3$ up to the missed edge and back, and steps to $P_1$.

## Examples

**Two clusters.** Six vertices form two triangles $\{A, B, C\}$ and $\{D, E, F\}$. Costs inside a triangle are 1, and costs between them are 3; these costs are a metric.

| round | constraints | LP value | solution | violated cut |
|---|---|---|---|---|
| 1 | degrees and bounds | 6 | $x = 1$ on the two triangles | $S = \{A, B, C\}$, $x(\delta(S)) = 0$ |
| 2 | and the cut of $S$ | 10 | the tour $A\,B\,C\,E\,F\,D$ | none |

The second LP solution is integral, so it is an optimal tour, and LP* $=$ OPT $= 10$.

**A fractional optimum.** On the six-vertex instance of the [Held-Karp bound](/held-karp-bound/) page, the degree constraints and the bounds already give LP* $= 21/2$ with $x = 1$ on $AE$, $BF$, $CD$ and $x = 1/2$ on six other edges. No cut is violated, and OPT $= 11$. A fractional solution can satisfy all cut constraints and still not be a tour.

**The 4/3 family for $k = 1, 2, 3$.**

| $k$ | $n$ | LP* | OPT | OPT/LP* |
|---|---|---|---|---|
| 1 | 6 | 6 | 6 | 1 |
| 2 | 9 | 9 | 10 | 1.111 |
| 3 | 12 | 12 | 14 | 1.167 |
| $k$ | $3k + 3$ | $3k + 3$ | $4k + 2$ | tends to $4/3$ |

For $k = 2$ the LP optimum has $x = 1$ on the six path edges and $x = 1/2$ on the six triangle edges, as in the construction.

## Where it is used

- **Lower bounds and exact solvers.** The LP value is the [Held-Karp bound](/held-karp-bound/), and the LP is the first relaxation in [branch and cut](/branch-and-cut/) for the TSP.
- **Approximation algorithms.** [Christofides' algorithm](/christofides-algorithm/) is within 3/2 of LP*. The [Karlin-Klein-Oveis Gharan algorithm](/karlin-klein-oveis-gharan-algorithm/) samples a spanning tree from a distribution with the marginals of the LP solution. For the [asymmetric TSP](/asymmetric-tsp/), the directed version of the LP is the base of the [Asadpour et al. algorithm](/asadpour-atsp-algorithm/) and of the constant ratio of Svensson, Tarnawski and Végh.
- **Polyhedral combinatorics.** The LP is a standard example of a polytope with exponentially many facets and a polynomial [separation oracle](/separation-oracle/).

## References
