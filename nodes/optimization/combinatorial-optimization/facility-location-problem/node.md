---
tag: QCSCTM
kind: problem
slug: facility-location-problem
name: Facility location problem
aliases:
- UFL
- Uncapacitated facility location
- metric facility location
- uncapacitated facility location
- simple plant location problem
area: optimization/combinatorial-optimization
level: core
summary: Open facilities and assign clients to them minimizing opening plus service cost.
prereqs: [combinatorial-optimization-problem, set-cover, lp-relaxation]
see_also: [jain-vazirani-facility-location, shmoys-tardos-aardal-facility-location, capacitated-facility-location, k-median-problem, k-center-problem, online-facility-location-problem, competitive-facility-location, lagrangian-relaxation]
sources:
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms, Cambridge University Press, 2011
    locator: the sections on the uncapacitated facility location problem in Chapter 4 (deterministic rounding), Chapter 5 (randomized rounding), Chapter 7 (primal-dual) and Chapter 9 (local search and greedy)
  - book: isbn:9783662560389
    title: Bernhard Korte and Jens Vygen, Combinatorial Optimization, Theory and Algorithms, sixth edition, Springer, 2018
    locator: Chapter 22, Facility Location
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms, Springer, 2001
    locator: Chapter 24, Facility location (the primal-dual 3-approximation)
  - paper: doi:10.1006/jagm.1998.0993
    title: Sudipto Guha and Samir Khuller, Greedy strikes back, improved facility location algorithms, Journal of Algorithms 31(1), 228 to 248, 1999
    locator: the hardness result with the constant 1.463
  - paper: doi:10.1016/j.ic.2012.01.007
    title: Shi Li, A 1.488 approximation algorithm for the uncapacitated facility location problem, Information and Computation 222, 45 to 58, 2013
    locator: main theorem
  - paper: doi:10.1145/375827.375845
    title: Kamal Jain and Vijay V. Vazirani, Approximation algorithms for metric facility location and k-median problems using the primal-dual schema and Lagrangian relaxation, Journal of the ACM 48(2), 274 to 296, 2001
    locator: the primal-dual 3-approximation and its use for k-median
  - paper: doi:10.1145/258533.258600
    title: David B. Shmoys, Éva Tardos and Karen Aardal, Approximation algorithms for facility location problems, STOC 1997, 265 to 274
    locator: the first constant-factor approximation, by LP rounding
  - paper: doi:10.1007/BF01581035
    title: Dorit S. Hochbaum, Heuristics for the fixed cost median problem, Mathematical Programming 22, 148 to 162, 1982
    locator: the greedy O(log n) approximation for the general case
  - paper: "Vijay Arya, Naveen Garg, Rohit Khandekar, Adam Meyerson, Kamesh Munagala and Vinayaka Pandit, Local search heuristics for k-median and facility location problems, SIAM Journal on Computing 33(3), 544 to 562, 2004"
    locator: the analysis of local search for uncapacitated facility location
  - paper: "Jarosław Byrka, An optimal bifactor approximation algorithm for the metric uncapacitated facility location problem, APPROX 2007, Lecture Notes in Computer Science 4627, 29 to 43"
    locator: the 1.5-approximation
---

The uncapacitated facility location problem (UFL) asks which facilities to open, and which open facility should serve each client, to minimize the sum of opening costs and service costs. It is [NP-hard](/np-hard/). In general it is as hard to approximate as [set cover](/set-cover/), with a ratio of $\Theta(\log n)$ the best possible in polynomial time unless P = NP. With *metric* service costs it has constant-factor algorithms: the best known ratio is 1.488 (Li, 2013), and no ratio below 1.463 is possible unless NP has slightly superpolynomial algorithms (Guha and Khuller, 1999). The problem is a standard example for [LP rounding](/lp-relaxation/), the primal-dual method and [local search](/local-search/).

## In plain words

A company wants to open warehouses to serve its shops. Each possible warehouse site has a fixed cost to open. Each shop is served by one open warehouse, and the cost of service grows with the distance. Opening many warehouses makes service cheap but costs a lot to build. Opening few saves on building but makes service expensive. Which sites should the company open?

Once the open sites are chosen, the rest is easy: each shop uses its cheapest open warehouse. So the whole problem is to choose a set of sites, and the number of sets doubles with each site. When costs behave like real distances, simple methods are known that never pay more than about one and a half times the best.

## Definition

**Input.** A finite set $F$ of facilities with opening costs $f_i \ge 0$, a finite set $D$ of clients, and service costs $c_{ij} \ge 0$ for $i \in F$, $j \in D$.

**Output.** A non-empty set $S \subseteq F$ of open facilities that minimizes

$$ \mathrm{cost}(S) = \sum_{i \in S} f_i + \sum_{j \in D} \min_{i \in S} c_{ij}. $$

Each client is served by a closest open facility. The instance is *metric* if the costs come from a metric on $F \cup D$, that is, $c_{ij} \le c_{ij'} + c_{i'j'} + c_{i'j}$ for all $i, i' \in F$ and $j, j' \in D$. As an integer program, with $y_i$ for "open $i$" and $x_{ij}$ for "$i$ serves $j$":

$$ \min \sum_{i} f_i y_i + \sum_{i, j} c_{ij} x_{ij} \quad \text{s.t.} \quad \sum_{i} x_{ij} = 1 \ (j \in D), \quad x_{ij} \le y_i, \quad x, y \in \{0, 1\}. $$

The [LP relaxation](/lp-relaxation/) replaces $\{0, 1\}$ by $[0, 1]$. The constraints $x_{ij} \le y_i$, one per pair, make this relaxation much stronger than the aggregated form $\sum_j x_{ij} \le |D|\, y_i$.

## Variants

- **[Capacitated facility location](/capacitated-facility-location/).** Facility $i$ can serve at most $u_i$ clients or a demand of at most $u_i$. With hard capacities the natural LP has an unbounded integrality gap, and the best algorithms use local search.
- **[k-median](/k-median-problem/).** No opening costs, but at most $k$ facilities may open. A [Lagrangian relaxation](/lagrangian-relaxation/) of the bound $k$ gives a UFL instance, which is how Jain and Vazirani turned their UFL algorithm into a k-median algorithm.
- **[k-center](/k-center-problem/).** At most $k$ facilities, and the objective is the largest service cost instead of the sum.
- **[Online facility location](/online-facility-location-problem/).** Clients arrive one by one and must be served at once.
- **[Competitive facility location](/competitive-facility-location/).** Two players claim sites in turns. This is a game, not a cost minimization.
- **Continuous location.** Facilities may be placed anywhere in the plane, as in the Weber problem and the [weighted median](/weighted-median-post-office-location/) on a line.

## Examples

Put facilities A, B, C at positions 0, 5, 9 on a line with opening costs 4, 3, 5, and clients 1 to 5 at positions 1, 3, 6, 8, 10. The service cost is the distance, so the instance is metric.

| open set | opening | service per client | total |
| --- | --- | --- | --- |
| {A} | 4 | 1, 3, 6, 8, 10 | 32 |
| {B} | 3 | 4, 2, 1, 3, 5 | 18 |
| {C} | 5 | 8, 6, 3, 1, 1 | 24 |
| {A, B} | 7 | 1, 2, 1, 3, 5 | 19 |
| {A, C} | 9 | 1, 3, 3, 1, 1 | 18 |
| {B, C} | 8 | 4, 2, 1, 1, 1 | 17 |
| {A, B, C} | 12 | 1, 2, 1, 1, 1 | 18 |

The optimum opens B and C at cost 17. Adding A to it saves 3 in service but costs 4 to open. Opening B alone is the best single choice, and adding C then saves $5 - 1 + 3 - 1 = 6$ in service against an opening cost of 5.

## Known algorithms

- **Exact.** [Branch and bound](/knapsack-branch-and-bound/) style search with the strong LP bound, or [branch and cut](/branch-and-cut/). Dual ascent on the LP (Erlenkotter's method) is a classical fast bound. The LP bound is often tight in practice.
- **General costs.** A greedy algorithm over "stars" (a facility with a set of clients), as for [set cover](/set-cover/), has ratio $O(\log |D|)$ (Hochbaum, 1982).
- **Metric, LP rounding.** Shmoys, Tardos and Aardal (1997) gave the first constant ratio, 3.16, by filtering and rounding the LP ([Shmoys-Tardos-Aardal](/shmoys-tardos-aardal-facility-location/)). Simpler roundings in Williamson and Shmoys give 4 and then 3.
- **Metric, primal-dual.** The [Jain-Vazirani algorithm](/jain-vazirani-facility-location/) (1999, journal version 2001) has ratio 3 and runs in $O(m \log m)$ time on $m$ facility-client pairs.
- **Metric, local search.** Open, close or swap one facility at a time while the cost goes down. Arya et al. (2004) showed ratio $3 + \varepsilon$ with polynomially many steps.
- **Metric, best known.** A line of greedy and rounding algorithms led to ratio 1.5 (Byrka, 2007) and 1.488 (Li, 2013), which combines randomized LP rounding with a greedy algorithm.

## Bounds

- **NP-hardness.** UFL is NP-hard, and so is the metric case. The reduction from [set cover](/set-cover/) below is metric-preserving if the large costs are replaced by 3.
- **General costs.** The reduction from set cover preserves the ratio, so no polynomial-time algorithm has ratio $(1 - \varepsilon) \ln |D|$ unless P = NP, and Hochbaum's greedy is within a constant factor of this.
- **Metric costs.** No polynomial-time algorithm has ratio below $\gamma \approx 1.463$, the root of $\gamma = 1 + 2e^{-\gamma}$, unless $\mathrm{NP} \subseteq \mathrm{DTIME}(n^{O(\log \log n)})$ (Guha and Khuller, 1999). The best known ratio is 1.488 (Li, 2013). The gap between 1.463 and 1.488 is open.
- **LP gap.** For metric instances the integrality gap of the LP above is at least 1.463 and at most 1.488, because Li's algorithm rounds this LP.
- **Supermodularity.** The service cost $\sum_j \min_{i \in S} c_{ij}$ is a non-increasing, supermodular function of $S$. The opening cost is modular, so $-\mathrm{cost}(S)$ is a [submodular function](/submodular-function/) on the non-empty sets $S$, which links UFL to submodular maximization.

## Reductions

- **From [set cover](/set-cover/).** For a set system with sets $S_1, \ldots, S_m$ over elements $U$, make a facility $i$ for each set with $f_i = 1$, a client for each element, and $c_{ij} = 0$ if $j \in S_i$ and a large cost otherwise. A cover of size $k$ gives a solution of cost $k$, and a solution of cost below the large cost is a cover. With the large cost replaced by 3 and the zero costs by 1, the costs are metric, and the reduction shows NP-hardness of the metric case.
- **To [set cover](/set-cover/).** A "star" is a facility $i$ with a set $C$ of clients, at cost $f_i + \sum_{j \in C} c_{ij}$. UFL is a weighted set cover over all stars, which has exponentially many sets but a greedy step that can be computed fast. This is the basis of Hochbaum's algorithm.
- **To k-median, by Lagrangian relaxation.** Moving the constraint "at most $k$ open" into the objective with a price $\lambda$ per open facility gives a UFL instance with $f_i = \lambda$. Searching over $\lambda$ connects the two problems.

## Applications

- **Supply chains.** Warehouses, plants and distribution centers, with fixed costs and transport costs.
- **Networks.** Placing caches, mirrors or servers in a network to serve users at low latency.
- **Clustering.** UFL is a clustering model in which the number of clusters is not fixed but paid for. The [k-median](/k-median-problem/) model fixes it.
- **Public services.** Schools, hospitals and fire stations, often with the [k-center](/k-center-problem/) objective instead.

## References
