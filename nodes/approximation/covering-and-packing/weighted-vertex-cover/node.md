---
tag: 22FWZ3
kind: problem
slug: weighted-vertex-cover
name: Weighted vertex cover problem
aliases:
- minimum-weight vertex cover
- WVC
area: approximation/covering-and-packing
level: core
summary: Find a vertex cover of least total weight; 2-approximable by LP rounding, the primal-dual method or local ratio, and solvable exactly on bipartite graphs by a minimum cut.
prereqs: [vertex-cover, lp-relaxation, dual-linear-program]
see_also: [primal-dual-weighted-vertex-cover, lp-rounding-vertex-cover, bar-yehuda-even-vertex-cover, local-ratio-technique, half-integrality, nemhauser-trotter-theorem, vertex-cover-inapproximability, set-cover]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 35, Section 35.4 (weighted vertex cover by LP rounding)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Chapter 11, Sections 11.4 (the pricing method) and 11.6 (LP rounding for weighted vertex cover)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Chapter 1 (set cover, with weighted vertex cover as the case f = 2)
  - paper: doi:10.1016/0196-6774(81)90020-1
    title: Reuven Bar-Yehuda and Shimon Even, A linear-time approximation algorithm for the weighted vertex cover problem, Journal of Algorithms 2(2), 1981
    locator: pages 198 to 203
  - paper: doi:10.1137/0211045
    title: Dorit S. Hochbaum, Approximation algorithms for the set covering and vertex cover problems, SIAM Journal on Computing 11(3), 1982
    locator: pages 555 to 556
  - title: George L. Nemhauser and Leslie E. Trotter, Vertex packings, structural properties and algorithms, Mathematical Programming 8, 1975
    locator: pages 232 to 248
---

The weighted vertex cover problem gives each vertex of a graph a weight and asks for a [vertex cover](/vertex-cover/) of least total weight. The weights break the simple matching argument of the unweighted case, but three methods still give ratio 2: rounding the LP at $1/2$, the [primal-dual algorithm](/primal-dual-weighted-vertex-cover/), and the [local ratio](/local-ratio-technique/) algorithm of Bar-Yehuda and Even. It is the case $f = 2$ of weighted [set cover](/set-cover/), and the main example for LP-based approximation. The LP is [half-integral](/half-integrality/), and on bipartite graphs the problem is solved exactly by a minimum cut. The hardness is the same as for the unweighted problem.

## In plain words

Each point of a network has a price, and you must buy points so that each link touches a bought point. You want to spend as little as possible. A cheap point with many links is a good buy, and an expensive point may be worth avoiding even if it touches many links.

Taking both ends of a link, as in the unweighted problem, can be a bad idea, because one end may be very expensive. The methods that work all use the same lower limit: let the links pay toward their ends without paying any point more than its price. The total paid is at most the best cost, and buying the fully paid points costs at most twice the total.

## Definition

**Input.** An undirected graph $G = (V, E)$ with $n$ vertices and $m$ edges, and a weight $w(v) \ge 0$ for each vertex.

**Output.** A vertex cover $C \subseteq V$: each edge has an endpoint in $C$.

**Goal.** Minimize $w(C) = \sum_{v \in C} w(v)$. OPT is the least weight of a cover, and the ratio convention is ALG $\le \rho \cdot$ OPT.

**LP and dual.**

$$\text{LP: } \min \sum_v w(v) x_v \ \text{ s.t. } x_u + x_v \ge 1 \ \forall \{u, v\} \in E,\ x \ge 0. \qquad \text{Dual: } \max \sum_e y_e \ \text{ s.t. } \sum_{e \ni v} y_e \le w(v) \ \forall v,\ y \ge 0.$$

LP* is the LP optimum, and LP* $\le$ OPT. A feasible dual is a fractional packing of edges into the vertex weights; by [weak duality](/weak-duality/) its value is at most LP*.

**Half-integrality.** The LP has an optimal solution with all $x_v \in \{0, 1/2, 1\}$. It can be found by one minimum cut in a bipartite double cover of $G$, and some optimal cover contains all vertices with $x_v = 1$ and no vertex with $x_v = 0$ (Nemhauser and Trotter 1975); see the [Nemhauser-Trotter theorem](/nemhauser-trotter-theorem/).

## Variants

- **Unit weights.** All weights 1 gives the [vertex cover](/vertex-cover/) problem, where the [maximal matching](/vertex-cover-2-approximation/) algorithm also gives 2.
- **Bipartite graphs.** Add a source joined to each left vertex with capacity $w(v)$, a sink joined from each right vertex with capacity $w(v)$, and give the edges infinite capacity. A minimum $s$-$t$ cut is a minimum-weight cover, by the [max-flow min-cut theorem](/max-flow-min-cut-theorem/). This is the weighted form of [König's theorem](/konig-theorem/).
- **Weighted set cover with frequency $f$.** The same methods give ratio $f$; see [primal-dual set cover](/set-cover-primal-dual/) and [frequency rounding](/frequency-rounding-set-cover/).
- **Capacitated vertex cover.** Each copy of a chosen vertex covers at most a given number of its edges. With soft capacities, where a vertex may be taken many times, a primal-dual algorithm gives ratio 2 (Guha, Hassin, Khuller and Or 2003).
- **Prize-collecting vertex cover.** An edge may stay uncovered for a penalty. The local ratio and primal-dual methods extend to it.

## Examples

**A seven-vertex graph.** The graph has the edges 1-2, 1-3, 2-3, 2-4, 3-5, 4-5, 4-6, 5-7 and 6-7 and the weights

| vertex | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| weight | 4 | 3 | 5 | 2 | 6 | 3 | 2 |

The optimum is $\{2, 3, 4, 7\}$ with weight 12, and LP* $= 12$. The dual with $y = 3$ on 1-2, $1$ on 1-3, $4$ on 3-5, $2$ on 4-5 and $2$ on 6-7, and 0 elsewhere, has value 12, so it proves the optimality. The unweighted optimum $\{1, 2, 5, 6\}$ has weight 16 here. The [primal-dual algorithm](/primal-dual-weighted-vertex-cover/) with this edge order returns $\{1, 2, 3, 4, 5, 7\}$ of weight 22, within $2 \cdot 12 = 24$.

**A heavy centre.** A star with centre weight 10 and five leaves of weight 1 has OPT $= 5$, the leaves. The unweighted answer, the centre, costs 10. If the centre has weight 4, the centre is optimal with OPT $= 4$.

**A triangle.** With unit weights, the triangle has OPT $= 2$ and LP* $= 3/2$, at $x_v = 1/2$ for each vertex. Rounding at $1/2$ takes all three vertices, cost $3 = 2 \cdot \text{LP}^*$.

## Known algorithms

| algorithm | ratio | lower bound used |
|---|---|---|
| [LP rounding](/lp-rounding-vertex-cover/): take $v$ with $x_v \ge 1/2$ | 2 | LP* |
| [Primal-dual](/primal-dual-weighted-vertex-cover/), linear time | 2 | a feasible dual $y$ |
| [Local ratio](/bar-yehuda-even-vertex-cover/) of Bar-Yehuda and Even | 2 | the local ratio theorem, which is the same dual |
| Clarkson's greedy (1983), by weight per degree with weight updates | 2 | a feasible dual |
| Greedy by $w(v)/\deg(v)$, as in [greedy set cover](/greedy-set-cover/) | $H_\Delta$ | LP*, by dual fitting |
| Local ratio with small odd cycles removed (Bar-Yehuda and Even 1985) | $2 - \frac{\log \log n}{2 \log n}$ | the local ratio theorem |
| Bipartite: minimum cut | 1 | a maximum flow |

All ratios hold in the worst case. The LP has one constraint for each edge and is solved in polynomial time by an interior point method, or by the minimum cut of the half-integral construction.

## Bounds

- **Upper bound (proved on the linked pages).** Ratio 2 on the [primal-dual](/primal-dual-weighted-vertex-cover/) and [LP rounding](/lp-rounding-vertex-cover/) pages.
- **Hardness (cited).** All hardness results of the unweighted problem hold, because unit weights are a special case: 1.3606 (Dinur and Safra 2005) and $\sqrt{2} - \varepsilon$ (Khot, Minzer and Safra 2018) are NP-hard, and $2 - \varepsilon$ is hard under the [Unique Games Conjecture](/unique-games-conjecture/) (Khot and Regev 2008). See [vertex cover inapproximability](/vertex-cover-inapproximability/).
- **Integrality gap.** On the complete graph $K_n$ with unit weights, OPT $= n - 1$ and LP* $= n/2$, so the gap tends to 2. So the ratio 2 of the LP-based methods is tight for their analysis.
- **Tightness of the algorithms.** On $K_{k,k}$ with unit weights, LP rounding at the solution $x_v = 1/2$ and the primal-dual algorithm with a perfect matching of edges both take all $2k$ vertices, while OPT $= k$.

## Reductions

- **To weighted set cover.** The edges are the elements, and each vertex is a set of cost $w(v)$ holding its edges. Each element has [frequency](/element-frequency/) 2.
- **From vertex cover.** Unit weights. This proves NP-hardness.
- **To bipartite cut (for the LP).** Make two copies $v'$ and $v''$ of each vertex, and join $u'$ to $v''$ and $v'$ to $u''$ for each edge. A minimum-weight cover $C$ of this bipartite graph gives the half-integral LP optimum $x_v = (|C \cap \{v', v''\}|)/2$.
- **Complement.** $C$ is a minimum-weight cover if and only if $V \setminus C$ is a maximum-weight [independent set](/independent-set/). The reduction keeps optima but not ratios.

## Applications

- **Network monitoring with costs.** Monitors at routers have different prices, and each link needs a monitored endpoint.
- **Conflict removal.** Remove a cheapest set of items, such as reads, tasks or rules, so that no two conflicting items remain.
- **Kernels and exact solvers.** The half-integral LP fixes the vertices with $x_v \in \{0, 1\}$ and leaves a smaller kernel for an exact search, as used in [kernelization](/kernelization/).

## References
