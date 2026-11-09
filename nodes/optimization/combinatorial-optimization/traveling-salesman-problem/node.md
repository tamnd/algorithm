---
tag: ARJ659
kind: problem
slug: traveling-salesman-problem
name: Traveling salesman problem
aliases:
- TSP
- travelling salesman problem
- symmetric TSP
area: optimization/combinatorial-optimization
level: core
summary: Find a shortest closed tour visiting every city exactly once.
prereqs: [combinatorial-optimization-problem, hamiltonian-cycle, np-hard]
see_also: [metric-tsp, euclidean-tsp, asymmetric-tsp, held-karp-algorithm, christofides-algorithm, nearest-neighbor-heuristic, two-opt, vehicle-routing-problem]
sources:
  - book: isbn:9780691129938
    title: David L. Applegate, Robert E. Bixby, Vasek Chvátal and William J. Cook, The Traveling Salesman Problem, A Computational Study, Princeton University Press, 2006
    locator: Chapter 1 (the problem and its history), Chapter 2 (applications), Chapter 5 (the linear programming bound and the subtour constraints)
  - book: isbn:9783662560389
    title: Bernhard Korte and Jens Vygen, Combinatorial Optimization, Theory and Algorithms, sixth edition, Springer, 2018
    locator: Chapter 21, The Traveling Salesman Problem (approximation, Euclidean TSP, local search, the polytope, lower bounds, branch and bound)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Appendix A2, problem ND22 (Traveling Salesman)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms, Cambridge University Press, 2011
    locator: Section 2.4, The traveling salesman problem (inapproximability of the general case, the double tree and Christofides' algorithm)
  - paper: doi:10.1145/321958.321975
    title: Sartaj Sahni and Teofilo Gonzalez, P-complete approximation problems, Journal of the ACM 23(3), 555 to 565, 1976
    locator: the theorem that the general TSP has no polynomial-time approximation with a constant ratio unless P = NP
  - paper: "Nicos Christofides, Worst-case analysis of a new heuristic for the travelling salesman problem, Report 388, Graduate School of Industrial Administration, Carnegie Mellon University, 1976"
    locator: the 3/2 bound for metric costs
  - paper: doi:10.1145/3406325.3451009
    title: Anna R. Karlin, Nathan Klein and Shayan Oveis Gharan, A (slightly) improved approximation algorithm for metric TSP, STOC 2021, 32 to 45
    locator: main theorem, the ratio 3/2 minus epsilon with epsilon above 10^-36
  - paper: doi:10.1016/j.jcss.2015.06.003
    title: Marek Karpinski, Michael Lampis and Richard Schmied, New inapproximability bounds for TSP, Journal of Computer and System Sciences 81(8), 1665 to 1677, 2015
    locator: the bounds 123/122 for metric TSP and 75/74 for asymmetric TSP
  - paper: doi:10.1137/0110015
    title: Michael Held and Richard M. Karp, A dynamic programming approach to sequencing problems, Journal of the Society for Industrial and Applied Mathematics 10(1), 196 to 210, 1962
    locator: the dynamic program over subsets for the TSP
  - paper: doi:10.1287/opre.2.4.393
    title: George B. Dantzig, D. Ray Fulkerson and Selmer M. Johnson, Solution of a large-scale traveling-salesman problem, Operations Research 2(4), 393 to 410, 1954
    locator: the integer program with subtour elimination constraints and the 49-city instance
  - paper: doi:10.1145/290179.290180
    title: Sanjeev Arora, Polynomial time approximation schemes for Euclidean traveling salesman and other geometric problems, Journal of the ACM 45(5), 753 to 782, 1998
    locator: the PTAS for Euclidean TSP in fixed dimension
  - paper: doi:10.1016/0304-3975(77)90012-3
    title: Christos H. Papadimitriou, The Euclidean travelling salesman problem is NP-complete, Theoretical Computer Science 4(3), 237 to 244, 1977
    locator: main theorem
  - paper: "Ola Svensson, Jakub Tarnawski and László A. Végh, A constant-factor approximation algorithm for the asymmetric traveling salesman problem, STOC 2018; journal version in Journal of the ACM 67(6), 2020"
    locator: main theorem
  - paper: "Vera Traub and Jens Vygen, An improved approximation algorithm for ATSP, STOC 2020; journal version in SIAM Journal on Computing 51(1), 2022"
    locator: the ratio 22 + epsilon
  - paper: "Laurence A. Wolsey, Heuristic analysis, linear programming and branch and bound, Mathematical Programming Study 13, 121 to 134, 1980"
    locator: the bound of Christofides' tour against the subtour elimination LP
  - paper: "Richard M. Karp, Reducibility among combinatorial problems, in R. E. Miller and J. W. Thatcher (editors), Complexity of Computer Computations, Plenum Press, 1972, pages 85 to 103"
    locator: the problems DIRECTED HAMILTON CIRCUIT and UNDIRECTED HAMILTON CIRCUIT in the list of 21 NP-complete problems
---

The traveling salesman problem (TSP) asks for a shortest closed tour through $n$ cities that visits each city exactly once, given the distance between every two cities. It is the best-known [NP-hard](/np-hard/) problem in combinatorial optimization. In general it cannot be approximated within any polynomial-time computable factor unless P = NP. With [metric](/metric-tsp/) distances, [Christofides' algorithm](/christofides-algorithm/) is within $3/2$ of the optimum and the [Karlin, Klein and Oveis Gharan algorithm](/karlin-klein-oveis-gharan-algorithm/) is within $3/2 - \varepsilon$ for some $\varepsilon > 10^{-36}$. With [Euclidean](/euclidean-tsp/) distances there is a [PTAS](/arora-euclidean-tsp-ptas/). Exact solvers based on [branch and cut](/branch-and-cut/) solve instances with tens of thousands of cities.

## In plain words

A salesman must visit a list of towns and come back home. The distance between every two towns is known. In which order should he visit the towns so that the whole trip is as short as possible?

With 5 towns there are only 12 different round trips, and you can check them all. The number of trips grows faster than any power of the number of towns, so with 30 towns checking them all is out of the question. No method is known that is fast on every list of towns. In practice, simple rules give trips a few percent too long, and clever search with lower bounds proves the best trip for very large lists.

## Definition

**Input.** A finite set $V$ of $n \ge 3$ cities and a cost $c(u, v) = c(v, u) \ge 0$ for every pair of distinct cities, that is, a complete graph $K_n$ with edge costs.

**Output.** A *tour*, a [Hamiltonian cycle](/hamiltonian-cycle/) $T$ of $K_n$, that minimizes $c(T) = \sum_{e \in T} c(e)$. Equivalently, a cyclic order $v_1, \ldots, v_n$ of the cities that minimizes $\sum_{i=1}^{n} c(v_i, v_{i+1})$ with $v_{n+1} = v_1$.

A tour is fixed by a cyclic order up to the start and the direction, so $K_n$ has $(n-1)!/2$ tours. The [decision version](/traveling-salesman-decision/) asks if a tour of cost at most $B$ exists. As an integer program over edge variables $x_e \in \{0, 1\}$ (Dantzig, Fulkerson and Johnson, 1954):

$$ \min \sum_{e} c_e x_e \quad \text{s.t.} \quad x(\delta(v)) = 2 \ \ (v \in V), \qquad x(\delta(S)) \ge 2 \ \ (\emptyset \ne S \subsetneq V), \qquad x \in \{0,1\}^{E}. $$

The degree constraints make each city have two tour edges, and the *subtour elimination constraints* forbid a union of shorter cycles. The [LP relaxation](/lp-relaxation/) of this program is the [subtour elimination LP](/subtour-elimination-lp/), and its optimum is the [Held-Karp bound](/held-karp-bound/).

## Variants

- **[Metric TSP](/metric-tsp/).** The costs satisfy the triangle inequality $c(u, w) \le c(u, v) + c(v, w)$. This is the case for every distance in a road network or a metric space, and it is the case most approximation results are about.
- **[Euclidean TSP](/euclidean-tsp/).** The cities are points in $\mathbb{R}^d$ and the costs are Euclidean distances. It is still NP-hard (Papadimitriou, 1977) but has a PTAS for each fixed $d$.
- **[Asymmetric TSP](/asymmetric-tsp/).** $c(u, v)$ may differ from $c(v, u)$, for example with one-way streets or sequence-dependent setup times. The tour is a directed Hamiltonian cycle.
- **(1,2)-TSP.** Every cost is 1 or 2. This is metric, and it is already NP-hard and [APX](/apx/)-hard.
- **[Bottleneck TSP](/bottleneck-tsp/).** Minimize the longest edge of the tour instead of the sum.
- **Path version.** Find a shortest Hamiltonian path, with or without fixed end points. A path with free end points reduces to a tour by a dummy city at cost 0 to all others.
- **[Bitonic tours](/bitonic-tsp/).** For points in the plane, restrict to tours that go from left to right and back. A dynamic program solves this in $O(n^2)$.
- **Online and many-vehicle versions.** The [online TSP](/online-traveling-salesman-problem/) reveals the cities over time. The [vehicle routing problem](/vehicle-routing-problem/) uses several tours from a depot with capacities.

## Examples

Take 5 cities on a grid with the Manhattan distance $|x_1 - x_2| + |y_1 - y_2|$, which is a metric: A $(0, 0)$, B $(4, 0)$, C $(4, 3)$, D $(1, 3)$, E $(2, 1)$. The cost matrix is

| | A | B | C | D | E |
| --- | --- | --- | --- | --- | --- |
| A | 0 | 4 | 7 | 4 | 3 |
| B | 4 | 0 | 3 | 6 | 3 |
| C | 7 | 3 | 0 | 3 | 4 |
| D | 4 | 6 | 3 | 0 | 3 |
| E | 3 | 3 | 4 | 3 | 0 |

There are $4!/2 = 12$ tours. Their costs are 16 (two tours), 18 (two), 20 (four), 22 (two) and 24 (two). The optimal tours are A B C D E A, with cost $4 + 3 + 3 + 3 + 3 = 16$, and A D C B E A, with cost $4 + 3 + 3 + 3 + 3 = 16$. The worst tours, such as A B D E C A with cost $4 + 6 + 3 + 4 + 7 = 24$, are 50 percent longer.

A non-example of the metric case: on a graph where the direct road from A to C is blocked, set $c(A, C)$ to a huge number. The costs are no longer metric. If a symmetric instance uses only costs 1 and 2, it is metric again, because $2 \le 1 + 1$.

## Known algorithms

- **Brute force.** Check all $(n-1)!/2$ tours. Feasible up to about $n = 12$.
- **[Held-Karp dynamic programming](/held-karp-algorithm/).** For each set $S$ of cities that contains the start and each end city in $S$, store the shortest path that covers $S$. Time $O(n^2 2^n)$, space $O(n 2^n)$ (Held and Karp 1962, and Bellman in the same year). No algorithm with time $O((2 - \varepsilon)^n)$ is known for general costs.
- **[Branch and cut](/branch-and-cut/).** Solve the [subtour elimination LP](/subtour-elimination-lp/), add violated subtour and comb inequalities as cutting planes, and branch when no cut is found. This is the method of Dantzig, Fulkerson and Johnson (1954) and of the Concorde code. Applegate, Bixby, Chvátal and Cook report the optimal tour for an instance with 85,900 cities (pla85900) in their book of 2006.
- **Approximation, metric case.** The [double-tree algorithm](/double-tree-algorithm/) has ratio 2. [Christofides' algorithm](/christofides-algorithm/) (1976, found at the same time by Serdyukov) has ratio $3/2$. The [Karlin, Klein and Oveis Gharan algorithm](/karlin-klein-oveis-gharan-algorithm/) (2021) has ratio $3/2 - \varepsilon$ for some $\varepsilon > 10^{-36}$. It was the first improvement on $3/2$ in more than 40 years.
- **Approximation, other cases.** [Arora's PTAS](/arora-euclidean-tsp-ptas/) and [Mitchell's PTAS](/mitchell-euclidean-tsp-ptas/) for Euclidean TSP. For asymmetric TSP, the [Asadpour et al. algorithm](/asadpour-atsp-algorithm/) has ratio $O(\log n / \log \log n)$, Svensson, Tarnawski and Végh (2018) gave the first constant ratio, and Traub and Vygen (2020) improved it to $22 + \varepsilon$.
- **Construction heuristics.** [Nearest neighbor](/nearest-neighbor-heuristic/) (ratio $\Theta(\log n)$ in the metric case), [greedy edge](/greedy-edge-heuristic/), [nearest insertion](/nearest-insertion/) and [cheapest insertion](/cheapest-insertion/) (ratio 2), [farthest insertion](/farthest-insertion/), and [space-filling curves](/space-filling-curve-tsp/).
- **Local search.** [2-opt](/two-opt/), [3-opt](/three-opt/), [Or-opt](/or-opt/) and [Lin-Kernighan](/lin-kernighan/), with the [Lin-Kernighan-Helsgaun](/lin-kernighan-helsgaun/) code as the strongest. Metaheuristics such as [simulated annealing](/simulated-annealing/), [tabu search](/tabu-search/) and [large neighborhood search](/large-neighborhood-search/) build on these moves.

## Bounds

| case | hardness | best known ratio in polynomial time |
| --- | --- | --- |
| general costs | no ratio $\alpha(n)$ for any polynomial-time computable $\alpha$, unless P = NP | none |
| metric | no ratio below $123/122$ unless P = NP | $3/2 - \varepsilon$, $\varepsilon > 10^{-36}$ |
| asymmetric, triangle inequality | no ratio below $75/74$ unless P = NP | $22 + \varepsilon$ |
| Euclidean, fixed dimension | strongly NP-hard | $1 + \varepsilon$ for every fixed $\varepsilon > 0$ (PTAS) |

- **NP-hardness.** The decision version is [NP-complete](/np-complete/) (Garey and Johnson, problem ND22), by the reduction below from Hamiltonian cycle, which Karp (1972) showed NP-complete. It is NP-complete in the strong sense, already with costs 1 and 2, so there is no pseudo-polynomial algorithm unless P = NP.
- **General costs** ([general TSP inapproximability](/general-tsp-inapproximability/)). Sahni and Gonzalez (1976): if a polynomial-time algorithm had ratio $\alpha$, it would decide [Hamiltonian cycle](/hamiltonian-cycle-problem/), by the reduction below.
- **Metric costs** ([metric TSP inapproximability](/metric-tsp-inapproximability/)). Karpinski, Lampis and Schmied (2015) showed that no polynomial-time algorithm has ratio below $123/122$ unless P = NP. The gap between $123/122 \approx 1.008$ and $1.5$ is open.
- **LP bound.** For metric costs the integrality gap of the [subtour elimination LP](/subtour-elimination-lp/) is at least $4/3$ and at most $3/2$. The upper bound holds because Christofides' tour is within $3/2$ of the LP optimum, not only of the integer optimum (Wolsey 1980).
- **Exact time.** $O(n^2 2^n)$ by Held-Karp for general costs.

## Reductions

- **From [Hamiltonian cycle](/hamiltonian-cycle-problem/).** Given a graph $G$ on $n$ vertices, set $c(u, v) = 1$ for edges of $G$ and $c(u, v) = 2$ otherwise. Then $G$ has a Hamiltonian cycle if and only if some tour costs $n$. Since the costs are 1 and 2, this shows strong NP-hardness of the metric case.
- **Gap version.** Set $c(u, v) = \alpha n + 1$ for non-edges instead. A Hamiltonian cycle gives a tour of cost $n$, and every other tour costs more than $\alpha n$. An $\alpha$-approximation would tell the two cases apart.
- **To an integer program.** The formulation above, with exponentially many subtour constraints that a [min cut](/min-cut-problem/) computation separates in polynomial time.
- **To and from the asymmetric case.** The symmetric TSP is the special case $c(u, v) = c(v, u)$. In the other direction, a standard construction with two copies of each city turns an asymmetric instance on $n$ cities into a symmetric instance on $2n$ cities.
- **Used by.** The [vehicle routing problem](/vehicle-routing-problem/) contains TSP as the case with one vehicle and no capacity limit.

## Applications

Applegate, Bixby, Chvátal and Cook (Chapter 2) list many applications. The common ones are:

- **Drilling and plotting.** The order in which a machine drills the holes of a circuit board or moves a pen.
- **Delivery and pickup.** Mail, school buses and service visits, usually as a [vehicle routing problem](/vehicle-routing-problem/) with TSP as the inner step.
- **Scheduling with setup times.** Jobs on one machine, where the setup time depends on the job before. This is an asymmetric TSP.
- **Genome and data sequencing.** Ordering markers or fragments so that adjacent items are similar.
- **Testing ideas.** TSP is the standard test bed for [local search](/local-search/), [branch and cut](/branch-and-cut/) and [metaheuristics](/metaheuristic/), with public benchmark sets.

## References
