---
tag: JNKP33
kind: problem
slug: minimum-spanning-tree
name: Minimum spanning tree problem
aliases:
- MST problem
- minimum-weight spanning tree
area: graphs/spanning-trees
level: intro
summary: Find a spanning tree of least total edge weight.
model: comparison-model
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Ω(m)}
prereqs: [spanning-tree, weighted-graph, connected-graph]
see_also: [kruskal, prim, boruvka, cut-property, cycle-property, spanning-forest, maximum-spanning-tree, mst-lower-bound]
sources:
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 7, Minimum Spanning Trees (the problem, the generic method, Borůvka, Jarník and Kruskal, and the history notes)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 21, Minimum Spanning Trees (Sections 21.1 and 21.2) and the chapter notes
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 4.5, The minimum spanning tree problem, and Section 4.7, Clustering
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.3, Minimum Spanning Trees
  - paper: doi:10.1109/MAHC.1985.10011
    title: Ronald L. Graham and Pavol Hell, On the history of the minimum spanning tree problem, Annals of the History of Computing 7(1) (1985), 43-57
    locator: the whole survey
  - paper: doi:10.1145/355541.355562
    title: Bernard Chazelle, A minimum spanning tree algorithm with inverse-Ackermann type complexity, Journal of the ACM 47(6) (2000), 1028-1047
    locator: the main theorem, O(m α(m, n)) time
  - paper: doi:10.1145/201019.201022
    title: David R. Karger, Philip N. Klein and Robert E. Tarjan, A randomized linear-time algorithm to find minimum spanning trees, Journal of the ACM 42(2) (1995), 321-328
    locator: the main theorem, expected O(m) time
  - paper: doi:10.1145/505241.505243
    title: Seth Pettie and Vijaya Ramachandran, An optimal minimum spanning tree algorithm, Journal of the ACM 49(1) (2002), 16-34
    locator: the main theorem, time within a constant factor of the decision-tree complexity
---

The minimum spanning tree problem asks, for a connected undirected [weighted graph](/weighted-graph/), for a [spanning tree](/spanning-tree/) whose total edge weight is as small as possible. The classical greedy algorithms of [Borůvka](/boruvka/), [Jarník and Prim](/prim/) and [Kruskal](/kruskal/) solve it in $O(m \log n)$ time, the best deterministic bound is $O(m\,\alpha(m, n))$, and a randomized algorithm runs in expected $O(m)$ time. Each algorithm must read every edge, so $\Omega(m)$ is a lower bound, and the exact deterministic complexity is still open. The problem is a model case for greedy algorithms and a step in network design, clustering and approximation algorithms.

## In plain words

You must connect some houses to a power network. For each pair of houses that you can join with a cable, you know the price of that cable. You want every house connected, maybe through other houses, at the least total price.

A cheapest solution never has a loop, because you could remove one cable of the loop and still have every house connected, at a lower price. So the answer is a tree that reaches every house.

Two simple rules find it. First, the cheapest cable that leaves any group of houses can always be part of a cheapest network. Second, the most expensive cable on any loop is never needed. Each fast method uses one of the two rules again and again.

## Definition

**Input.** A finite undirected graph $G = (V, E)$ with $n = |V| \ge 1$ vertices and $m = |E|$ edges, and a weight $w(e) \in \mathbb{R}$ for each edge $e$. The graph must be [connected](/connected-graph/). Weights may be negative, zero, and may tie. Parallel edges and [self-loops](/self-loop/) are allowed; a self-loop is never used.

**Output.** A set $T \subseteq E$ such that $(V, T)$ is a spanning tree of $G$ and

$$w(T) = \sum_{e \in T} w(e) \le w(T') \quad \text{for each spanning tree } T' \text{ of } G.$$

Such a $T$ is a **minimum spanning tree** (MST). An MST exists because $G$ is connected, so it has at least one spanning tree, and it has only finitely many.

**Graphs that are not connected.** A graph with $c \ge 2$ components has no spanning tree. The natural output is then a *minimum spanning forest*: a [spanning forest](/spanning-forest/) of least total weight, which is the union of an MST of each component. Most algorithms, Kruskal's for example, return it with no change.

**Ties and uniqueness.** When all weights are distinct, the MST is unique ([MST uniqueness](/mst-uniqueness/)). With ties there can be many: if all weights are equal, every spanning tree is an MST. The weights matter only through their order, because the optimality conditions below compare weights and never add them. So a strictly increasing map of the weights gives the same set of MSTs.

**Optimality conditions.** A spanning tree $T$ is an MST if and only if, for each edge $e = uv \notin T$, every edge on the path from $u$ to $v$ in $T$ has weight at most $w(e)$ ([MST optimality conditions](/mst-optimality-conditions/)). The two rules behind the algorithms are the [cut property](/cut-property/) (a lightest edge across a cut is in some MST) and the [cycle property](/cycle-property/) (an edge that is strictly heaviest on some cycle is in no MST).

**All MSTs have the same weights.** For each two MSTs $T_1$ and $T_2$, the multisets $\{w(e) : e \in T_1\}$ and $\{w(e) : e \in T_2\}$ are equal. *Proof.* Fix a threshold $t$ and let $E_{\le t}$ be the edges of weight at most $t$. Let $T$ be an MST. Suppose that some edge $e = uv \in E_{\le t}$ joins two different trees of the forest $T \cap E_{\le t}$. The path from $u$ to $v$ in $T$ then has an edge $f$ of weight more than $t$, else $u$ and $v$ would be in one tree of $T \cap E_{\le t}$. The set $T - f + e$ is a spanning tree, because $f$ is on the cycle that $e$ closes, and its weight is $w(T) - w(f) + w(e) < w(T)$. This is a contradiction. So $T \cap E_{\le t}$ is a spanning forest of $(V, E_{\le t})$, and it has $n - c_t$ edges, where $c_t$ is the number of components of $(V, E_{\le t})$. This number does not depend on $T$, for each $t$, so the number of edges of each weight is the same in every MST. $\square$

## Variants

- **Minimum spanning forest.** The graph need not be connected, as above.
- **[Maximum spanning tree](/maximum-spanning-tree/).** Maximize $w(T)$. Negate the weights and solve the MST problem.
- **[Minimum bottleneck spanning tree](/minimum-bottleneck-spanning-tree/).** Minimize the largest edge weight of the tree. Every MST is one, and the problem alone is solvable in $O(m)$ time.
- **Directed graphs.** The analogue is the [minimum arborescence](/minimum-arborescence/), solved by [Edmonds' algorithm](/edmonds-arborescence/). The greedy methods of the undirected case fail there.
- **Geometric input.** The [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/) of $n$ points in the plane uses the distance as the weight of each of the $\binom{n}{2}$ pairs, and is found in $O(n \log n)$ time from the [Delaunay triangulation](/delaunay-triangulation/).
- **Other objectives.** The [minimum diameter spanning tree](/minimum-diameter-spanning-tree/) minimizes the longest path in the tree and is solvable in polynomial time. The [degree-constrained spanning tree](/degree-constrained-spanning-tree/), the [minimum routing cost spanning tree](/minimum-routing-cost-spanning-tree/) and the [Steiner tree problem](/steiner-tree-problem/), which may use extra vertices, are NP-hard.
- **Related questions about one MST.** [MST verification](/mst-verification/) checks a given tree, [MST sensitivity analysis](/mst-sensitivity-analysis/) finds how far each weight can move, and the [second-best MST](/second-best-mst/) is the next tree in weight order.
- **[Dynamic MST](/dynamic-minimum-spanning-tree/).** Keep an MST while edges are inserted and deleted.

## Examples

**A graph with six vertices.** Take the vertices $a$ to $f$ and these nine edges.

| edge | $ab$ | $ac$ | $bc$ | $bd$ | $cd$ | $ce$ | $de$ | $df$ | $ef$ |
|---|---|---|---|---|---|---|---|---|---|
| weight | 4 | 3 | 1 | 2 | 4 | 5 | 7 | 6 | 2 |

The graph has 55 spanning trees, with weights from 13 to 25. The MST is $\{bc, bd, ef, ac, ce\}$ of weight 13, and it is the only tree of weight 13, even though two pairs of weights tie. Two trees have weight 14, the next value. The edge $ce$ is the only edge that joins $\{a, b, c, d\}$ to $\{e, f\}$ with weight less than 6, so the [cut property](/cut-property/) forces it into each MST. [Kruskal's algorithm](/kruskal/) shows each step on this graph.

**Ties.** In the cycle $C_4$ with four edges of weight 1, each of the four spanning trees has weight 3, and all four are MSTs. In the triangle with weights $1, 2, 2$, the two trees that hold the edge of weight 1 are MSTs, and both have the weight multiset $\{1, 2\}$.

**Negative weights.** In the triangle with weights $-5, -1, 3$, the MST is the two edges $-5$ and $-1$, with weight $-6$. A spanning tree always has exactly $n - 1$ edges, so negative weights do not make the problem harder: adding a constant to each weight adds $(n - 1)$ times that constant to each tree.

**A disconnected input.** Two disjoint triangles with weights $1, 2, 3$ each have no spanning tree. The minimum spanning forest takes the edges $1$ and $2$ of each triangle, with total weight 6 and $6 - 2 = 4$ edges.

## Known algorithms

The [generic MST method](/generic-mst-method/) adds a [safe edge](/safe-edge/) at each step. Each algorithm below is a way to find safe edges fast. In the table, $\alpha$ is the [inverse Ackermann function](/inverse-ackermann-function/), and $\beta(m, n) = \min\{i : \log^{(i)} n \le m/n\}$.

| algorithm | year | time | model and case |
|---|---|---|---|
| [Borůvka](/boruvka/) | 1926 | $O(m \log n)$ | deterministic, worst case |
| [Jarník, Prim](/prim/) with a [binary heap](/binary-heap/) | 1930, 1957 | $O(m \log n)$ | deterministic, worst case |
| [Prim](/prim/) with a [Fibonacci heap](/fibonacci-heap/) | 1987 | $O(m + n \log n)$ | deterministic, worst case |
| [Kruskal](/kruskal/) | 1956 | $O(m \log m)$ | deterministic, worst case, the sort dominates |
| [Reverse-delete](/reverse-delete/) | 1956 | $O(m \log n (\log \log n)^3)$ with dynamic connectivity | deterministic, amortized |
| [Yao](/yao-mst/) | 1975 | $O(m \log \log n)$ | deterministic, worst case |
| [Fredman and Tarjan](/fredman-tarjan-mst/) | 1987 | $O(m \beta(m, n))$ | deterministic, worst case |
| [Chazelle](/chazelle-mst/) | 2000 | $O(m\,\alpha(m, n))$ | deterministic, worst case, comparison model |
| [Karger, Klein and Tarjan](/karger-klein-tarjan-mst/) | 1995 | $O(m)$ | randomized, expected |
| [Pettie and Ramachandran](/pettie-ramachandran-mst/) | 2002 | optimal, the exact bound is unknown | deterministic, comparison model |

The [greedy MST algorithm](/greedy-mst-algorithm/) page covers the common frame of the first four.

## Bounds

**Lower bound.** In the comparison model, and in any model where an edge weight is read before it is used, each algorithm reads every edge of some inputs, so it takes $\Omega(m)$ time ([MST lower bound](/mst-lower-bound/)). No better general lower bound is known.

**Deterministic upper bound.** Chazelle's algorithm runs in $O(m\,\alpha(m, n))$ time in the comparison model. The algorithm of Pettie and Ramachandran is optimal: its running time is within a constant factor of the least depth of a decision tree for the MST problem on graphs of the same size. That depth lies between $\Omega(m)$ and $O(m\,\alpha(m, n))$, and its exact value is not known. So the deterministic complexity of the problem is an open question.

**Randomized upper bound.** The Karger-Klein-Tarjan algorithm runs in $O(m)$ expected time, with only comparisons of weights, and in $O(m)$ time with high probability.

**Integer weights.** On the [word RAM](/word-ram/), with integer weights that fit in a word, Fredman and Willard (Journal of Computer and System Sciences 48, 1994) find an MST in $O(m)$ time in the worst case.

**Dense graphs.** When $m = \Omega(n \log n)$, Prim's algorithm with a Fibonacci heap already runs in $O(m)$ time, which is optimal.

## Reductions

- **Maximum spanning tree to MST.** Replace each weight $w(e)$ by $-w(e)$. This costs $O(m)$, and the MSTs of the new weights are the maximum spanning trees of the old ones.
- **Minimum spanning forest to MST.** Run an MST algorithm on each component, found by a [graph traversal](/graph-traversal/) in $O(n + m)$ time. Or add a new vertex joined to one vertex of each component by an edge heavier than all others, and remove those edges from the MST.
- **MST verification to MST.** Compute an MST $T^*$ and test $w(T) = w(T^*)$. The direct algorithms for verification run in $O(m)$ time in the worst case, which is faster than any known deterministic MST algorithm.
- **Sorting to the Euclidean MST.** Given distinct numbers $x_1, \ldots, x_n$, the MST of the points $x_i$ on the real line is the path that joins each number to the next larger one. From the MST, find the two vertices of degree 1, start at the smaller one and walk the path, in $O(n)$ time, to output the sorted order. So in the [algebraic decision tree](/algebraic-decision-tree/) model, where sorting needs $\Omega(n \log n)$ steps, the Euclidean MST also needs $\Omega(n \log n)$ steps.
- **MST to approximation.** The weight of an MST is a lower bound for a [metric TSP](/metric-tsp/) tour, since removing one edge of a tour gives a spanning tree. The [double-tree algorithm](/double-tree-algorithm/) and [Christofides' algorithm](/christofides-algorithm/) build on this.

## Applications

- **Network design.** Borůvka studied the problem in 1926 for an electrical network in Moravia. Cable, pipe and road networks of least total length are MSTs when no extra junction points are allowed. With extra points, the problem is the [Steiner tree problem](/steiner-tree-problem/), and the MST is a 2-approximation for it.
- **Clustering.** [Single-linkage clustering](/single-linkage-clustering/) into $k$ groups removes the $k - 1$ heaviest edges of an MST. The groups have the largest possible spacing (Kleinberg and Tardos, Section 4.7).
- **Image segmentation.** The method of [Felzenszwalb and Huttenlocher](/felzenszwalb-segmentation/) merges regions in the order of Kruskal's algorithm on the graph of neighbouring pixels.
- **Approximation of hard problems.** Metric TSP, the Steiner tree problem and other network design problems use an MST as a lower bound or as a first solution.
- **Bottleneck paths.** In a maximum spanning tree, the tree path between two vertices is a [widest path](/widest-path/) of the graph: its lightest edge is as heavy as possible. The same holds for minimax paths in an MST.

## References
