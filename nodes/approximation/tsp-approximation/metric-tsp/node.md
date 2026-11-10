---
tag: YCHD4S
kind: problem
slug: metric-tsp
name: Metric TSP
aliases:
- metric traveling salesman problem
- TSP with the triangle inequality
- Delta-TSP
area: approximation/tsp-approximation
level: core
summary: The symmetric TSP with costs that satisfy the triangle inequality. It is NP-hard and APX-hard, but unlike general TSP it has constant-factor approximations, from 2 to 3/2 and slightly below.
prereqs: [traveling-salesman-problem, hamiltonian-cycle-problem, approximation-ratio, minimum-spanning-tree]
see_also: [general-tsp-inapproximability, metric-tsp-inapproximability, double-tree-algorithm, christofides-algorithm, karlin-klein-oveis-gharan-algorithm, held-karp-bound, euclidean-tsp, asymmetric-tsp]
sources:
  - paper: doi:10.1145/321958.321975
    title: Sartaj Sahni and Teofilo Gonzalez, P-complete approximation problems, Journal of the ACM 23(3), 1976
    locator: pages 555 to 565 (no constant ratio for the TSP without the triangle inequality unless P = NP)
  - title: Nicos Christofides, Worst-case analysis of a new heuristic for the travelling salesman problem, Report 388, Graduate School of Industrial Administration, Carnegie Mellon University, 1976
    locator: the whole report (the 3/2 algorithm)
  - title: Anatoliy I. Serdyukov, On some extremal routes in graphs, Upravlyaemye Sistemy 17, 1978
    locator: pages 76 to 79, in Russian (the same 3/2 algorithm, found independently)
  - paper: doi:10.1137/0206041
    title: Daniel J. Rosenkrantz, Richard E. Stearns and Philip M. Lewis II, An analysis of several heuristics for the traveling salesman problem, SIAM Journal on Computing 6(3), 1977
    locator: pages 563 to 581 (insertion heuristics within 2, nearest neighbor within a log n factor)
  - paper: doi:10.1145/3406325.3451009
    title: Anna R. Karlin, Nathan Klein and Shayan Oveis Gharan, A (slightly) improved approximation algorithm for metric TSP, STOC 2021
    locator: pages 32 to 45 (ratio 3/2 minus 10^(-36))
  - paper: doi:10.1016/j.jcss.2015.06.003
    title: Marek Karpinski, Michael Lampis and Richard Schmied, New inapproximability bounds for TSP, Journal of Computer and System Sciences 81(8), 2015
    locator: pages 1665 to 1677 (no ratio below 123/122 unless P = NP)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Chapter 2, Section 2.4 (the TSP, its hardness without the triangle inequality, the double-tree and Christofides algorithms)
---

The metric TSP is the [traveling salesman problem](/traveling-salesman-problem/) on a complete graph whose symmetric edge costs satisfy the triangle inequality $c_{uw} \le c_{uv} + c_{vw}$. Without this condition, no polynomial algorithm has a constant [approximation ratio](/approximation-ratio/) unless P = NP. With it, a tour within a factor 2 of OPT comes from a [minimum spanning tree](/minimum-spanning-tree/), [Christofides' algorithm](/christofides-algorithm/) gives 3/2, and Karlin, Klein and Oveis Gharan gave $3/2 - 10^{-36}$. The problem is still NP-hard, and no ratio below $123/122$ is possible unless P = NP.

## In plain words

A salesman must visit each city once and come back home, and wants the cheapest round trip. In the metric version, the direct road between two cities is never more costly than a detour through a third city. Distances on a map behave like this, and so do travel times when you can always take the fastest route.

This one rule changes a lot. It lets an algorithm plan a rough route that may pass through a city more than once, and then skip each repeated city. Skipping can only make the trip cheaper. So simple methods find a trip at most twice as costly as the best one, and a cleverer method gets within one and a half. Finding the best trip exactly is still hard.

## Definition

**Input.** A set $V$ of $n \ge 3$ vertices and a cost $c_{uv} = c_{vu} \ge 0$ for each pair $u \ne v$, such that for all distinct $u, v, w$:

$$c_{uw} \le c_{uv} + c_{vw} \qquad \text{(the triangle inequality)}.$$

**Output.** A *tour*: a cyclic order $v_1, v_2, \ldots, v_n$ of all vertices, that is, a Hamiltonian cycle of the complete graph. Its cost is $\sum_{i=1}^{n} c_{v_i v_{i+1}}$ with $v_{n+1} = v_1$.

**Goal.** Minimize the cost. OPT is the least cost of a tour, and ALG is the cost of the tour that an algorithm returns. This page uses the convention for minimization: an algorithm is a $\rho$-approximation if ALG $\le \rho \cdot \text{OPT}$ on each instance, with $\rho \ge 1$. Ratios are worst case unless the page says "in expectation".

**The shortcut lemma.** The triangle inequality is what all the algorithms below use. *If a closed walk visits every vertex, then the tour that keeps only the first visit to each vertex costs at most as much as the walk.* Proof: each step of the tour from $u$ to $w$ replaces a piece $u, x_1, \ldots, x_k, w$ of the walk, and by the triangle inequality applied $k$ times, $c_{uw} \le c_{u x_1} + c_{x_1 x_2} + \cdots + c_{x_k w}$. The pieces of the walk do not overlap, so the sum over the tour is at most the cost of the walk. $\blacksquare$

**The metric closure.** Let $H$ be any connected graph with edge lengths $\ell \ge 0$, and let $d$ be its shortest path distance. Then $d$ satisfies the triangle inequality, and OPT for $d$ equals the least length of a closed walk in $H$ that visits every vertex. Proof: a tour for $d$ becomes such a walk when each step is replaced by a shortest path, with the same length; and such a walk shortcut as above gives a tour for $d$ of at most its length. $\blacksquare$ So "visit each city at least once in a road network" is the metric TSP on the [shortest path distances](/floyd-warshall/).

## Variants

- **General (non-metric) TSP.** Any costs. No polynomial $\rho$-approximation for any polynomial-time computable $\rho(n)$ unless P = NP; see [general TSP inapproximability](/general-tsp-inapproximability/) and the proof under Bounds.
- **(1,2)-TSP.** All costs are 1 or 2, which is always metric. It is the special case used for hardness. Papadimitriou and Yannakakis (1993) gave a $7/6$-approximation, and Berman and Karpinski (2006) gave $8/7$.
- **Graphic TSP.** The metric closure of an unweighted connected graph. Sebő and Vygen (2014) gave a $7/5$-approximation.
- **Euclidean TSP.** The vertices are points in $\mathbb{R}^d$ with the Euclidean distance. For fixed $d$ it has a [PTAS](/ptas/); see [Euclidean TSP](/euclidean-tsp/).
- **Path TSP.** Find a Hamiltonian path with two given ends $s$ and $t$. Hoogeveen (1991) adapted Christofides' algorithm to get $5/3$, and Zenklusen (2019) reached $3/2$.
- **Asymmetric TSP.** $c_{uv} \ne c_{vu}$ is allowed, with the directed triangle inequality. The best ratios are much weaker; see [asymmetric TSP](/asymmetric-tsp/).
- **Bottleneck TSP.** Minimize the largest edge of the tour, not the sum; see [bottleneck TSP](/bottleneck-tsp/).
- **Many salesmen and capacities.** The [vehicle routing problem](/vehicle-routing-problem/) splits the vertices among several tours from a depot.

## Examples

**Seven cities.** The cities $A(5,1)$, $B(6,5)$, $C(0,0)$, $D(8,0)$, $E(5,4)$, $F(0,4)$ and $G(3,0)$ with the Manhattan distance $|x_1 - x_2| + |y_1 - y_2|$, which is a metric. The values below were computed by a script, with OPT by trying all tours.

| method | tour | cost | cost / OPT |
|---|---|---|---|
| minimum spanning tree (a lower bound) | $AE$, $EB$, $AG$, $GC$, $AD$, $CF$ | 19 | 0.679 |
| subtour LP, the [Held-Karp bound](/held-karp-bound/) | integral here | 28 | 1 |
| [double tree](/double-tree-algorithm/) | $A\,E\,B\,G\,C\,F\,D$ | 36 | 1.286 |
| [nearest neighbor](/nearest-neighbor-tsp/) from $A$ | $A\,E\,B\,D\,G\,C\,F$ | 32 | 1.143 |
| [Christofides](/christofides-algorithm/) | $A\,E\,B\,F\,C\,G\,D$ | 28 | 1 |
| optimal | $A\,B\,E\,F\,C\,G\,D$ | 28 | 1 |

Nearest neighbor from the other six start cities gives 34, 34, 28, 36, 34 and 34 (from $B$ to $G$ in order).

**Why the triangle inequality matters.** Take four vertices $A, B, C, D$ with $c_{AB} = c_{AC} = c_{AD} = 1$ and $c_{BC} = c_{BD} = c_{CD} = 10$. The triangle inequality fails, because $c_{BC} = 10 > c_{BA} + c_{AC} = 2$. The walk $A\,B\,A\,C\,A\,D\,A$ costs 6, but every tour uses two of the edges of cost 10, so OPT $= 22$, and shortcutting the walk to $A\,B\,C\,D$ raises the cost from 6 to 22. On the metric closure the edges among $B$, $C$, $D$ cost 2, and the same tour costs $1 + 2 + 2 + 1 = 6$.

**A (1,2) instance from the Petersen graph.** Give cost 1 to the 15 edges of the Petersen graph on 10 vertices and cost 2 to the other 30 pairs. The Petersen graph has no Hamiltonian cycle but has a Hamiltonian path, so OPT $= 9 \cdot 1 + 2 = 11 = n + 1$. For the 10-cycle in the same way, OPT $= 10 = n$. This is the reduction that shows the metric TSP is NP-hard.

## Known algorithms

The ratios below are for the metric TSP with $n$ vertices. "Proved" points to the page with the full proof.

| algorithm | ratio | time | status |
|---|---|---|---|
| [double tree](/double-tree-algorithm/), [MST preorder walk](/mst-preorder-walk-tsp/) | $2 - 2/n$, tight | $O(n^2)$ | proved on those pages |
| [nearest insertion](/nearest-insertion/), [cheapest insertion](/cheapest-insertion/) | 2 | $O(n^2)$ to $O(n^2 \log n)$ | Rosenkrantz, Stearns and Lewis 1977 |
| [nearest neighbor](/nearest-neighbor-tsp/) | $\tfrac12(\lceil \log_2 n \rceil + 1)$, and $\Omega(\log n)$ on some instances | $O(n^2)$ | Rosenkrantz, Stearns and Lewis 1977 |
| [Christofides](/christofides-algorithm/) (Serdyukov 1978) | $3/2$, tight | $O(n^3)$ | proved on that page |
| [Karlin, Klein and Oveis Gharan](/karlin-klein-oveis-gharan-algorithm/) | $3/2 - 10^{-36}$ in expectation | polynomial | cited, outline on that page |
| [Held-Karp dynamic program](/held-karp-algorithm/) | exact | $O(n^2 2^n)$ | exact algorithm |
| [2-opt](/two-opt/), [Lin-Kernighan](/lin-kernighan/), [LKH](/lin-kernighan-helsgaun/) | no good worst-case ratio | per pass | local search, very good in practice |

The [MST TSP heuristic](/mst-tsp-heuristic/) page compares the tree-based methods on random instances. For exact solutions of large instances, [branch and cut](/branch-and-cut/) on the [subtour elimination LP](/subtour-elimination-lp/) is the standard method.

## Bounds

**Lower bounds on OPT.** For non-negative costs, the [minimum spanning tree](/mst-lower-bound-for-tsp/) costs at most $(1 - 1/n) \cdot \text{OPT}$, and the [Held-Karp bound](/held-karp-bound/), which is the value LP* of the subtour LP, is at most OPT. With the triangle inequality also $\text{OPT} \le 2 \cdot \text{MST}$ and $\text{OPT} \le \tfrac32 \text{LP}^*$ (Wolsey 1980), so both bounds are within a constant factor of OPT.

**NP-hardness (proved here).** Hamiltonian cycle reduces to the metric TSP. Given a graph $G$ on $n$ vertices, set $c_{uv} = 1$ if $uv$ is an edge and $c_{uv} = 2$ if not. Costs 1 and 2 satisfy the triangle inequality, since $2 \le 1 + 1$. A tour costs $n$ exactly when all its edges are edges of $G$, so OPT $= n$ if and only if $G$ has a [Hamiltonian cycle](/hamiltonian-cycle-problem/). $\blacksquare$ The decision version is NP-complete; see [TSP decision](/traveling-salesman-decision/).

**No constant ratio without the triangle inequality (proved here; Sahni and Gonzalez 1976).** Let $\rho \ge 1$. Given $G$ on $n$ vertices, set $c_{uv} = 1$ on edges and $c_{uv} = \rho n + 1$ on non-edges. If $G$ is Hamiltonian, OPT $= n$, and a $\rho$-approximation returns a tour of cost at most $\rho n$. If $G$ is not Hamiltonian, each tour uses a non-edge and costs at least $(n - 1) + \rho n + 1 > \rho n$. So a polynomial $\rho$-approximation decides Hamiltonian cycle, and P = NP. The same holds for $\rho = 2^n$, since the costs still have polynomially many digits. These costs break the triangle inequality as soon as $\rho n + 1 > 2$. See [general TSP inapproximability](/general-tsp-inapproximability/). $\blacksquare$

**Exact hardness does not depend on the metric.** Adding a constant $M \ge \max c$ to every cost makes any instance metric, because then $c_{uw} + M \le 2M \le (c_{uv} + M) + (c_{vw} + M)$. Each tour gains exactly $nM$, so the optimal tours do not change. This reduction keeps optimality but not ratios, which is why the two problems differ only in approximation.

**Hardness of approximation (cited).** No polynomial algorithm reaches a ratio below $123/122$ unless P = NP (Karpinski, Lampis and Schmied 2015), improving $220/219$ (Papadimitriou and Vempala 2006). So the metric TSP has no [PTAS](/ptas/) unless P = NP, and it is [APX-complete](/apx-completeness/) (Papadimitriou and Yannakakis 1993, for (1,2)-TSP). See [metric TSP inapproximability](/metric-tsp-inapproximability/).

**The gap between the bounds.** The best ratio is just below $3/2$ and the hardness is $123/122 \approx 1.008$. The [integrality gap](/integrality-gap/) of the subtour LP is at least $4/3$ and at most $3/2 - 10^{-36}$; the conjecture that it is $4/3$ is open.

## Reductions

- **From Hamiltonian cycle.** The 1 and 2 cost reduction above shows NP-hardness; with costs 1 and $\rho n + 1$ it shows that general TSP has no ratio.
- **From closed walks.** The metric closure turns "visit each vertex at least once" on any connected graph into the metric TSP, with the same optimum.
- **To spanning trees and matchings.** The approximation algorithms reduce the problem to a [minimum spanning tree](/minimum-spanning-tree/), a [minimum weight perfect matching](/minimum-weight-perfect-matching/) and an [Eulerian circuit](/eulerian-circuit/), and then shortcut.
- **Special cases.** [Euclidean TSP](/euclidean-tsp/) and graphic TSP are metric TSP with more structure, and they have better algorithms. The [bitonic tour](/bitonic-tsp/) is a restricted form that a dynamic program solves exactly.

## Applications

- **Routing.** Delivery and pickup routes, service visits and school buses, often as parts of [vehicle routing](/vehicle-routing-problem/) models.
- **Manufacturing.** The order in which a machine drills holes in a circuit board or moves a tool head, where the costs are travel times of the head.
- **Data analysis.** Ordering items so that neighbors are similar, for example in clustering and genome mapping, with a dissimilarity that is a metric.
- **A test bed for algorithms.** The metric TSP is the standard example for approximation by spanning trees, for LP relaxations with exponentially many constraints, and for local search.

## References
