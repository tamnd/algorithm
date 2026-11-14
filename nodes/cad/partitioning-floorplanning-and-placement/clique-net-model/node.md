---
tag: 2SRSJX
kind: definition
slug: clique-net-model
name: Clique net model
aliases:
- clique model of a net
area: cad/partitioning-floorplanning-and-placement
level: core
summary: Replaces a net of p pins with a weighted clique on its pins, often with weight 1/(p - 1), so graph methods apply to a netlist.
prereqs: [hypergraph, complete-graph, half-perimeter-wirelength]
see_also: [hypergraph-partitioning, half-perimeter-wirelength, quadratic-placement, multilevel-hypergraph-partitioning, kernighan-lin, spectral-partitioning, graph-partitioning-problem, laplacian-matrix]
sources:
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 2, Netlist and System Partitioning (netlists as hypergraphs and their graph models), and Chapter 4, Global and Detailed Placement (net models in quadratic placement)
  - paper: doi:10.1016/0020-0190(93)90115-P
    title: Edmund Ihler, Dorothea Wagner and Frank Wagner, Modeling hypergraphs by graphs with the same mincut properties, Information Processing Letters 45(4), 171 to 175, 1993
    locator: the question whether a graph can represent the cuts of a hyperedge exactly (general locator; the exact statement of the main theorem is not given on this page)
  - paper: doi:10.1109/92.748202
    title: George Karypis, Rajat Aggarwal, Vipin Kumar and Shashi Shekhar, Multilevel hypergraph partitioning, applications in VLSI domain, IEEE Transactions on VLSI Systems 7(1), 69 to 79, 1999
    locator: the edge coarsening scheme, which scores a pair of vertices by the sum of 1/(|e| - 1) over the nets that contain both
  - paper: "Charles J. Alpert and Andrew B. Kahng, Recent directions in netlist partitioning, a survey, Integration, the VLSI Journal 19(1 to 2), 1 to 81, 1995"
    locator: the section on net models and the conversion of hyperedges to graph edges
---

The clique net model replaces each net of a circuit, a [hypergraph](/hypergraph/) edge with $p$ pins, by a [complete graph](/complete-graph/) on those pins whose $\binom{p}{2}$ edges share a weight that depends on $p$. Then graph tools apply: the [Laplacian](/laplacian-matrix/) for [spectral partitioning](/spectral-partitioning/), [Kernighan-Lin](/kernighan-lin/) swaps, and the quadratic objective of [quadratic placement](/quadratic-placement/). The two usual weights are $1/(p-1)$ and $2/p$, and a page or a tool must say which one it uses. The model is exact for quadratic wirelength in a sense made precise below, but for the cut of a net and for [HPWL](/half-perimeter-wirelength/) it is exact only for $p \le 3$.

## Definition

Let a net $e$ have weight $w_e$ and pins $v_1, \ldots, v_p$, $p \ge 2$. The *clique model with edge weight* $\omega(p)$ replaces $e$ by the edges $\{v_i, v_j\}$, $i < j$, each of weight $w_e \, \omega(p)$. Edges from different nets between the same two vertices add up. The common choices are:

- $\omega(p) = 1/(p - 1)$. The edges at each pin have total weight $w_e$, and a split that separates one pin from the rest costs exactly $w_e$.
- $\omega(p) = 2/p$. The clique has total weight $(p - 1) w_e$, the number of edges of a spanning tree of the pins.
- $\omega(p) = 1$, the unweighted clique, which gives large nets far too much weight.

The *star model* is the alternative. It adds one new free vertex $s_e$ for the net and the $p$ edges $\{s_e, v_i\}$, each of weight $w_e \, \sigma(p)$. It has $p$ edges instead of $\binom{p}{2}$, so it keeps the graph sparse for large nets.

A net of a netlist is cut by a partition when its pins lie in more than one part, and the cut counts it once (see [hypergraph partitioning](/hypergraph-partitioning/)). The model replaces this count, and the bounding box length of the net, by sums over clique edges. The following facts say how close the sums are.

**Fact 1 (cut).** If a partition puts $k$ pins of $e$ on one side and $p - k$ on the other, the clique edges that cross have weight $w_e \, \omega(p) \, k (p - k)$. For $1 \le k \le p - 1$, $k(p - k)$ lies between $p - 1$ and $\lfloor p^2 / 4 \rfloor$. With $\omega = 1/(p-1)$ the cost of a cut net lies in $[w_e, \, w_e \lfloor p^2/4 \rfloor / (p - 1)]$, so a 2:2 split of a 4-pin net costs $4/3$ of a 1:3 split.

**Fact 2 (no clique weighting is exact for $p \ge 4$).** Let $p \ge 4$ and give the edges of the clique any real weights $c_{ij}$. Then some two splits of the pins have different crossing weights, while the cut-net count gives both the value 1. *Proof.* Suppose every split costs 1. The split $\{v_i\}$ against the rest gives $d_i = \sum_j c_{ij} = 1$ for every $i$, so the total weight is $C = \frac12 \sum_i d_i = p/2$. The split $\{v_i, v_j\}$ against the rest, which is a proper split because $p \ge 4$, costs $d_i + d_j - 2 c_{ij} = 2 - 2 c_{ij} = 1$, so $c_{ij} = 1/2$ for every pair and $C = \binom{p}{2} / 2$. Then $p/2 = p(p-1)/4$, so $p = 3$, a contradiction. For $p = 3$ the weight $1/2 = 1/(p-1)$ is exact, and for $p = 2$ the single edge is exact. $\square$

**Fact 3 (linear length).** Let the pins have coordinates $x_{(1)} \le \cdots \le x_{(p)}$ along one axis, with gaps $g_t = x_{(t+1)} - x_{(t)}$ and range $R = \sum_t g_t$. The pair $(i, j)$ with $i < j$ spans the gaps $t = i, \ldots, j - 1$, and gap $t$ is spanned by $t (p - t)$ pairs, so

$$ \sum_{i < j} |x_{(i)} - x_{(j)}| = \sum_{t=1}^{p-1} t (p - t) \, g_t, \qquad (p - 1) R \le \sum_{i<j} |x_i - x_j| \le \Big\lfloor \frac{p^2}{4} \Big\rfloor R. $$

So with $\omega = 1/(p-1)$ the clique length in each axis is at least the range, and the clique length is at least the [HPWL](/half-perimeter-wirelength/) of the net. It equals the HPWL for every position when $p \le 3$, since then $t(p - t) = p - 1$ for all $t$. For $p \ge 4$ equality needs $g_t = 0$ for $2 \le t \le p - 2$, so in each axis all pins except the smallest and the largest must share one coordinate.

**Fact 4 (quadratic length, clique equals star).** For any reals $x_1, \ldots, x_p$ with mean $\bar x$,

$$ \sum_{i < j} (x_i - x_j)^2 = p \sum_{i} (x_i - \bar x)^2 = p \min_{s} \sum_i (x_i - s)^2. $$

*Proof.* Expand: $\sum_{i<j} (x_i - x_j)^2 = \frac12 \sum_{i,j} (x_i^2 - 2 x_i x_j + x_j^2) = p \sum_i x_i^2 - (\sum_i x_i)^2 = p \sum_i (x_i - \bar x)^2$. The function $s \mapsto \sum_i (x_i - s)^2$ is least at $s = \bar x$. $\square$

So in a quadratic placer, where the star vertex is free and moves to its optimal position, a clique with edge weight $\omega$ and a star with edge weight $p \, \omega$ give the same objective and the same optimal cell positions. The clique with $\omega = 1/(p - 1)$ equals the star with $\sigma = p/(p - 1)$. Big nets can use the star and small nets the clique, with no change to the optimum.

## Examples and non-examples

- **A 4-pin net under a partition.** Net $\{a, b, c, d\}$ with $w_e = 1$. The cut-net metric gives 1 to every split. The clique gives:

  | split | crossing clique edges | $\omega = 1/3$ | $\omega = 2/4$ |
  | --- | --- | --- | --- |
  | $\{a\} \mid \{b, c, d\}$ | 3 | 1 | 1.5 |
  | $\{a, b\} \mid \{c, d\}$ | 4 | 4/3 | 2 |
  | not cut | 0 | 0 | 0 |

  A graph partitioner that sees the clique prefers to cut off one pin of this net rather than split it evenly, while the circuit cost is the same.
- **Three pins, exact.** For $p = 3$ and $\omega = 1/2$, each split crosses two clique edges and costs 1, the cut-net value. In one axis, pins at $0, 1, 5$ have clique length $\frac12 (1 + 5 + 4) = 5$, the range.
- **Four pins in one axis.** Pins at $0, 1, 2, 3$: the clique sum is $1 \cdot 3 + 2 \cdot 2 + 3 \cdot 1 = 10$, so with $\omega = 1/3$ the length is $10/3$ against a range of 3. Pins at $0, 0, 0, 3$: the sum is 9, the length is 3, equal to the range. Pins at $0, 1, 1, 3$: the sum is 9 and the length is again 3. Pins at $0, 0, 3, 3$: the sum is 12 and the length is 4.
- **Quadratic.** Pins at $0, 1, 5$, mean 2. The squared deviations sum to $4 + 1 + 9 = 14$, and the clique sum of squared differences is $1 + 25 + 16 = 42 = 3 \cdot 14$, as Fact 4 says.
- **Non-example: the clique as a hypergraph.** Two different netlists can give the same weighted graph: one 3-pin net $\{a, b, c\}$ with $\omega = 1/2$, and three 2-pin nets $ab, bc, ca$ of weight $1/2$ each. So the model loses information, and a partition that is optimal for the graph need not be optimal for the netlist.

## Related definitions

- **Cut-net metric and connectivity metric.** The exact costs of a partition of a netlist, defined on [hypergraph partitioning](/hypergraph-partitioning/). Fiduccia-Mattheyses and hMETIS work with them directly and need no clique.
- **Edge coarsening.** The [multilevel hypergraph partitioner](/multilevel-hypergraph-partitioning/) scores a pair of vertices by $\sum w_e/(|e| - 1)$ over the nets they share, which is the clique model with $\omega = 1/(p - 1)$.
- **Star model and hybrid models.** The star with a free center vertex, as in Fact 4. Some placers use the clique for small nets and the star for large ones.
- **Graphs with extra vertices.** One may ask for a graph with extra vertices whose minimum cuts match those of a net. Ihler, Wagner and Wagner (1993) study this question.
- **Wirelength models.** [HPWL](/half-perimeter-wirelength/) is the target that the linear clique length bounds from above, and [quadratic placement](/quadratic-placement/) uses the quadratic clique or star.

## References
