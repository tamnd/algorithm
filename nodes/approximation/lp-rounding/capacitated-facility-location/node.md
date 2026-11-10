---
tag: XN8YFE
kind: problem
slug: capacitated-facility-location
name: Capacitated facility location
aliases:
- CFL
- capacitated facility location problem
- hard-capacitated facility location
area: approximation/lp-rounding
level: advanced
summary: Open facilities and assign clients, with at most u_i clients at facility i, to minimize opening plus connection cost; the natural LP has an unbounded gap, and local search gives ratio 5.
model: word-ram
complexity:
  vars: {m: the number of facilities, n: the number of clients}
  time: {worst: O(2^m n^2 m (n + m))}
prereqs: [facility-location-problem, lp-relaxation, integrality-gap, min-cost-flow-problem, local-search]
see_also: [facility-location-problem, shmoys-tardos-aardal-facility-location, jain-vazirani-facility-location, k-median-problem, integrality-gap, local-search, bicriteria-approximation, min-cost-flow-problem]
sources:
  - title: Martin Pál, Éva Tardos and Tom Wexler, Facility location with nonuniform hard capacities, Proceedings of the 42nd IEEE Symposium on Foundations of Computer Science, 2001
    locator: the open, close and multi-swap local search for nonuniform capacities
  - title: Manisha Bansal, Naveen Garg and Neelima Gupta, A 5-approximation for capacitated facility location, European Symposium on Algorithms, 2012
    locator: the analysis of the Pál, Tardos and Wexler moves with ratio 5
  - title: Madhukar R. Korupolu, C. Greg Plaxton and Rajmohan Rajaraman, Analysis of a local search heuristic for facility location problems, Journal of Algorithms 37(1), 2000
    locator: the first constant ratio for uniform capacities
  - title: Hyung-Chan An, Mohit Singh and Ola Svensson, LP-based algorithms for capacitated facility location, SIAM Journal on Computing 46(1), 2017
    locator: an LP with constant integrality gap, and the gap of the natural LP
---

Capacitated facility location (CFL) is [facility location](/facility-location-problem/) with a limit on each facility. There are facilities with opening costs $f_i$ and capacities $u_i$, clients, and metric connection costs $c_{ij}$. The task is to open some facilities and assign each client to an open one, so that facility $i$ serves at most $u_i$ clients, at the least total opening and connection cost. Each facility can be opened at most once, which is why the capacities are called *hard*. The natural LP relaxation, which works so well for the uncapacitated problem, has an [integrality gap](/integrality-gap/) that grows with the capacities. For a long time all constant ratios came from [local search](/local-search/): ratio 5 by Bansal, Garg and Gupta (2012) for general capacities, and 3 for equal capacities. An, Singh and Svensson (2014) gave the first LP with a constant gap.

## In plain words

A company opens warehouses and sends each shop to one of them. A warehouse costs money to open and each shop pays for its distance to its warehouse. Unlike the basic problem, a warehouse can serve only a limited number of shops.

The limit breaks the usual LP method. In the fractional answer, a warehouse can be opened a tiny fraction and still take a whole extra shop worth of load, spread across shops. A whole answer must open it fully. Local search, which opens, closes and swaps warehouses while that lowers the cost, gives the best known guarantees.

## Definition

**Input.** A set $\mathcal{F}$ of $m$ facilities, each with an opening cost $f_i \ge 0$ and an integer capacity $u_i \ge 1$. A set $\mathcal{D}$ of $n$ clients. Costs $c_{ij} \ge 0$ between facilities and clients that come from a metric, so they satisfy the [triangle inequality](/triangle-inequality/).

**Output.** A set $X \subseteq \mathcal{F}$ of open facilities and a map $\sigma : \mathcal{D} \to X$ with $|\sigma^{-1}(i)| \le u_i$ for each $i \in X$, of least cost

$$\sum_{i \in X} f_i + \sum_{j \in \mathcal{D}} c_{\sigma(j) j}.$$

**The assignment for fixed $X$.** When $X$ is fixed, the best $\sigma$ is a min-cost flow: send one unit from each client to the facilities, with capacity $u_i$ at facility $i$. A [min-cost flow](/min-cost-flow-problem/) problem with integer capacities has an integral optimum, so the hard part is only the choice of $X$.

**The natural LP.**

$$\min \sum_i f_i y_i + \sum_{i, j} c_{ij} x_{ij} \ \text{ s.t. } \ \sum_i x_{ij} = 1, \quad x_{ij} \le y_i, \quad \sum_j x_{ij} \le u_i y_i, \quad 0 \le y_i \le 1, \ x \ge 0.$$

The bound $y_i \le 1$ is what makes the capacities hard. Without it, the LP describes *soft* capacities.

## Variants

- **Soft capacities.** Facility $i$ may be opened several times, each time at cost $f_i$ and with $u_i$ more capacity. The natural LP then has a constant gap. Jain and Vazirani reduced this version to the uncapacitated problem, and Mahdian, Ye and Zhang (2003) gave ratio 2.
- **Uniform capacities.** All $u_i = u$. Korupolu, Plaxton and Rajaraman gave the first constant ratio by local search, and Aggarwal et al. (2013) reached 3.
- **Demands.** Client $j$ has a demand $d_j$. If the demand may be split among facilities, the problem stays close to the unit case. If it may not, even deciding whether a feasible assignment exists is like bin packing, so only [bicriteria](/bicriteria-approximation/) results, with a small capacity violation, are possible.
- **Capacitated $k$-median.** At most $k$ facilities may be opened and there are no opening costs. Constant ratios are known only with a violation of the capacities or of $k$.
- **Uncapacitated.** All $u_i \ge n$ gives the [uncapacitated facility location problem](/facility-location-problem/), where LP rounding gives ratio about $1.488$.

## Examples

**The gap of the natural LP.** Take two facilities at the same point, with $f_1 = 0$, $f_2 = f$ and the same capacity $u$, and $u + 1$ clients at that point, so every $c_{ij} = 0$. Facility 1 can serve only $u$ clients, so every solution opens both facilities, and OPT $= f$. The LP can set $y_1 = 1$, $y_2 = 1/u$, and $x_{2j} = 1/(u + 1)$, $x_{1j} = u/(u + 1)$ for each client. Then $x_{2j} \le y_2$, facility 1 gets load $u$, and facility 2 gets load $1 = u y_2$. The LP value is $f/u$, so the gap is $f / (f/u) = u$, which is unbounded.

For $u = 2$ and $f = 6$, the three clients need both facilities at cost 6, while the LP pays $6 \cdot 1/2 = 3$.

**Why the LP fails.** The rows $x_{ij} \le y_i$ and $\sum_j x_{ij} \le u_i y_i$ cannot see that facility 2 must serve a whole client once it serves any part of one. Simple extra rows do not fix this, and An, Singh and Svensson needed a much stronger multi-commodity flow LP.

## Known algorithms

| algorithm | capacities | guarantee |
|---|---|---|
| brute force over open sets, with a min-cost flow for each | hard | exact, time $O(2^m n^2 m (n + m))$ |
| Korupolu, Plaxton and Rajaraman (1998) | uniform, hard | local search, ratio $8 + \varepsilon$ |
| Chudak and Williamson (1999) | uniform, hard | local search, ratio $6 + \varepsilon$ |
| Aggarwal et al. (2013) | uniform, hard | local search, ratio $3 + \varepsilon$ |
| Pál, Tardos and Wexler (2001) | general, hard | local search with open, close and multi-swap moves, ratio $9 + \varepsilon$ |
| Zhang, Chen and Ye (2005) | general, hard | local search, ratio $3 + 2\sqrt{2} + \varepsilon$ |
| Bansal, Garg and Gupta (2012) | general, hard | local search, ratio $5 + \varepsilon$ |
| An, Singh and Svensson (2014) | general, hard | LP rounding with a strong LP, a constant ratio |
| Mahdian, Ye and Zhang (2003) | soft | greedy with dual fitting, ratio 2 |

The $\varepsilon$ comes from accepting only moves that lower the cost by a factor $1 - \varepsilon/\text{poly}(m)$, which makes the search end in polynomial time. The local search moves are: open one facility, close one and open a set of others, or swap one facility for a set. After each move, the assignment is recomputed as a min-cost flow.

## Bounds

- **Natural LP.** The gap is at least $u$ for each capacity $u$, by the example, so it is not bounded by any constant.
- **Strong LP.** The multi-commodity flow LP of An, Singh and Svensson has a constant gap, but the constant is large, and no simple LP rounding that matches local search is known.
- **Hardness.** With large capacities the problem is uncapacitated facility location, which is hard to approximate within about $1.463$ (Guha and Khuller 1999), unless NP has algorithms of time $n^{O(\log \log n)}$.
- **Local search.** Each bound in the table holds for every local optimum of its neighborhood, so the algorithms need no LP at all.

## Reductions

- **From uncapacitated facility location.** Set $u_i = n$ for all $i$; then capacities never bind.
- **Assignment to min-cost flow.** For fixed $X$, the best assignment is a [min-cost flow](/min-cost-flow-problem/), as in the Definition.
- **Soft to uncapacitated.** With soft capacities, replace $c_{ij}$ with $c_{ij} + f_i / u_i$, the cost of the share of a copy that one client uses. An algorithm for the uncapacitated problem with a strong guarantee on the opening cost then gives a constant ratio.
- **Unsplittable demands from bin packing.** Take $k$ facilities of capacity 1, all costs 0, and client demands equal to item sizes in $(0, 1]$. A feasible unsplittable assignment exists exactly when the items fit into $k$ bins. So deciding feasibility is NP-hard, as for [bin packing](/bin-packing/), and only bicriteria results are possible.

## Applications

- **Warehouse and plant location.** Each warehouse has a limited size or throughput, which is the usual case in practice.
- **Server and cache placement.** Each server can handle a bounded number of users.
- **School and hospital districting.** Each site has a fixed number of places, and each person is sent to one site.

## References
