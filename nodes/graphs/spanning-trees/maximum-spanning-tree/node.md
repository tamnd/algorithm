---
tag: J7EVGB
kind: problem
slug: maximum-spanning-tree
name: Maximum spanning tree
area: graphs/spanning-trees
level: intro
summary: Finds a spanning tree of maximum total edge weight, solved by running a minimum spanning tree algorithm on negated weights.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Ω(m)}
prereqs: [minimum-spanning-tree, spanning-tree, weighted-graph]
see_also: [kruskal, prim, widest-path, minimum-bottleneck-spanning-tree, maximum-weight-matroid-basis, single-linkage-clustering, chow-liu-algorithm, cut-property]
sources:
  - book: isbn:9783030542559
    title: Steven S. Skiena, The Algorithm Design Manual, third edition
    locator: Section 8.1, Minimum Spanning Trees (the variations, including maximum spanning trees and minimum product spanning trees)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 7, Minimum Spanning Trees
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 21, Minimum Spanning Trees (Sections 21.1 and 21.2, which the reduction reuses)
  - paper: doi:10.1287/opre.9.6.898
    title: "T. C. Hu, The maximum capacity route problem, Operations Research 9(6) (1961), 898-900"
    locator: the whole paper (maximum capacity routes lie on a maximum spanning tree)
  - paper: doi:10.1109/TIT.1968.1054142
    title: "C. K. Chow and C. N. Liu, Approximating discrete probability distributions with dependence trees, IEEE Transactions on Information Theory 14(3) (1968), 462-467"
    locator: the whole paper (the best tree is a maximum weight spanning tree under mutual information)
---

The maximum spanning tree problem asks, for a connected undirected [weighted graph](/weighted-graph/), for a [spanning tree](/spanning-tree/) of the largest total edge weight. It is the [minimum spanning tree](/minimum-spanning-tree/) problem with the order of the weights reversed: negate each weight, or reverse each comparison, and run [Kruskal's](/kruskal/) or [Prim's](/prim/) algorithm. So it has the same bounds, $O(m \log n)$ time with the textbook algorithms and an $\Omega(m)$ lower bound. Its main uses are the widest paths of a network and the dependence trees of Chow and Liu.

## In plain words

You have a network of links, and each link has a value, such as its capacity or how strongly two items are related. You want to keep a set of links that connects every point, with no loop, and with the largest total value.

This is the same task as finding the cheapest connecting network, with the scale turned upside down. Sort the links from the most valuable to the least valuable, and take each link that does not close a loop. The rules that make the cheapest network correct work the same way when "cheapest" becomes "most valuable".

## Definition

**Input.** A connected undirected graph $G = (V, E)$ with $n = |V|$ and $m = |E|$, and a weight $w : E \to \mathbb{R}$. Weights may be negative and may tie.

**Output.** A spanning tree $T \subseteq E$ such that

$$w(T) = \sum_{e \in T} w(e) \ge w(T') \quad \text{for each spanning tree } T' \text{ of } G.$$

**Disconnected graphs.** If $G$ is not connected, it has no spanning tree. The usual output is then a *maximum spanning forest*: a forest with the same components as $G$ and the largest weight among such forests. It is the union of a maximum spanning tree of each component.

**Ties.** When weights tie, more than one tree can be maximum, and each of them is a correct output. With distinct weights the maximum spanning tree is unique, by the same proof as for the minimum.

**The reduction.** Let $w'(e) = -w(e)$. Each spanning tree has exactly $n - 1$ edges, so $w'(T) = -w(T)$, and $T$ is a minimum spanning tree for $w'$ if and only if it is a maximum spanning tree for $w$. If an algorithm needs non-negative weights, use $w'(e) = W - w(e)$ with $W = \max_e w(e)$: then $w'(T) = (n - 1)W - w(T)$, and the same equivalence holds, because each spanning tree has the same number of edges. The map takes $O(m)$ time. An algorithm that only compares weights, as Kruskal's and Prim's algorithms do, needs no map at all: reverse each comparison.

## Variants

- **Maximum weight forest.** Find a forest, not necessarily spanning, of the largest weight. This differs when some weights are negative: the answer is a maximum spanning forest of the subgraph of the edges with positive weight. On the [graphic matroid](/graphic-matroid/), this is the [maximum weight independent set](/maximum-weight-matroid-basis/) problem, and the greedy algorithm that stops at the first non-positive edge solves it.
- **[Minimum bottleneck spanning tree](/minimum-bottleneck-spanning-tree/), reversed.** A spanning tree that maximizes its smallest edge weight. Each maximum spanning tree is one, by the reversed cut property.
- **Maximum spanning arborescence.** In a directed graph, the reversed [minimum arborescence](/minimum-arborescence/) problem, solved by [Edmonds' algorithm](/edmonds-arborescence/) on negated weights.
- **Maximum product spanning tree.** Maximize the product of positive weights. Take logarithms, which keep the order, and solve the sum version (Skiena, Section 8.1).

## Examples

Take the vertices $a$ to $f$ and the edges $ab = 4$, $ac = 3$, $bc = 1$, $bd = 2$, $cd = 4$, $ce = 5$, $de = 7$, $df = 6$, $ef = 2$. Kruskal's algorithm in non-increasing order of weight does:

| step | edge | weight | action | weight so far |
|---|---|---|---|---|
| 1 | $de$ | 7 | add | 7 |
| 2 | $df$ | 6 | add | 13 |
| 3 | $ce$ | 5 | add | 18 |
| 4 | $ab$ | 4 | add | 22 |
| 5 | $cd$ | 4 | skip: $c$ and $d$ already joined | 22 |
| 6 | $ac$ | 3 | add | 25 |

The tree $\{de, df, ce, ab, ac\}$ has weight 25. The graph has 55 spanning trees. This tree is the only one of weight 25, and the next ones have weight 24, for example $\{ab, ac, cd, de, df\}$. The minimum spanning tree of the same graph is $\{bc, bd, ef, ac, ce\}$ with weight 13; the two trees share the edges $ac$ and $ce$.

**Widest paths.** In this graph, read the weights as capacities. The path from $a$ to $f$ in the maximum spanning tree is $a, c, e, d, f$, with the smallest capacity $\min(3, 5, 7, 6) = 3$. No path from $a$ to $f$ does better. Each path starts with $ab$ or with $ac$. A path that starts with $ab$ leaves $b$ by $bc = 1$ or by $bd = 2$, so its smallest capacity is at most 2. A path that starts with $ac$ has a smallest capacity of at most 3.

**Negative weights.** For the triangle with $w(ab) = -1$, $w(bc) = -2$ and $w(ca) = -5$, the maximum spanning tree is $\{ab, bc\}$ with weight $-3$. The maximum weight forest is the empty set, with weight 0.

## Known algorithms

Each algorithm for the [minimum spanning tree](/minimum-spanning-tree/) solves this problem with reversed comparisons, at the same cost.

- [Kruskal's algorithm](/kruskal/): sort in non-increasing order, $O(m \log m)$ time.
- [Prim's algorithm](/prim/): grow one tree, always taking the heaviest edge that leaves it; $O(m \log n)$ with a [binary heap](/binary-heap/), $O(m + n \log n)$ with a [Fibonacci heap](/fibonacci-heap/), $O(n^2)$ with an array.
- [Borůvka's algorithm](/boruvka/): each component takes its heaviest outgoing edge; $O(m \log n)$ time.
- The [Karger-Klein-Tarjan algorithm](/karger-klein-tarjan-mst/), expected $O(m)$ time, and [Chazelle's algorithm](/chazelle-mst/), $O(m \, \alpha(m, n))$ time.

## Bounds

The reduction in both directions takes $O(m)$ time and preserves the set of optimal trees, so the maximum and the minimum spanning tree problems have the same complexity in each model in which negation, or the reversal of comparisons, is free.

- **Upper bounds.** $O(m \, \alpha(m, n))$ deterministic time in the comparison-based model of Chazelle, and $O(m)$ expected time with the randomized algorithm of Karger, Klein and Tarjan.
- **Lower bound.** $\Omega(m)$ for each deterministic algorithm. Take a graph in which each edge lies on a cycle, and assume an algorithm never reads the weight of some edge $e$. If its output omits $e$, make $e$ the unique heaviest edge of the graph, which every maximum spanning tree contains. If its output contains $e$, make $e$ the unique lightest edge of a cycle, which no maximum spanning tree contains, by the [cycle property](/cycle-property/) with the order reversed. In both cases the output is wrong.

## Reductions

- **To and from the minimum spanning tree.** Negate the weights, as in the definition. Cost $O(m)$.
- **[Widest path](/widest-path/) for all pairs.** For each pair $u, v$, the path in a maximum spanning tree maximizes the smallest edge weight among all paths from $u$ to $v$ (Hu, 1961). So one maximum spanning tree answers all widest path queries, each by a bottleneck query on a tree path.
- **[Single-linkage clustering](/single-linkage-clustering/).** With similarities as weights, removing the $k - 1$ lightest edges of a maximum spanning tree gives the $k$ single-linkage clusters. With distances, use the minimum spanning tree, as in [maximum spacing clustering](/maximum-spacing-k-clustering/).

## Applications

- **Dependence trees.** The [Chow-Liu algorithm](/chow-liu-algorithm/) approximates a joint distribution of many variables by a tree. The best tree is a maximum spanning tree of the complete graph whose edge weights are the mutual informations of pairs of variables (Chow and Liu, 1968).
- **Capacity of routes.** In a network with link capacities, a maximum spanning tree holds a route of the largest bottleneck capacity between each pair of nodes.

## References
