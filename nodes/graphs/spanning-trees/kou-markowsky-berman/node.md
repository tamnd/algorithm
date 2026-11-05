---
tag: 97ZJ4F
kind: algorithm
slug: kou-markowsky-berman
name: Kou-Markowsky-Berman algorithm
aliases:
- KMB algorithm
- MST-based Steiner heuristic
area: graphs/spanning-trees
level: advanced
summary: A 2-approximation for the Steiner tree problem via an MST of the terminal distance graph.
solves: [steiner-tree-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, s: the number of terminals}
  time: {worst: "O(s (m + n log n))"}
  space: {extra: O(s n + m)}
properties: {deterministic: true, recursive: false}
prereqs: [steiner-tree-problem, minimum-spanning-tree, dijkstra, approximation-ratio]
see_also: [steiner-tree-problem, metric-tsp, kruskal, prim, all-pairs-shortest-paths, minimum-spanning-tree, dijkstra, approximation-ratio]
sources:
  - paper: doi:10.1007/BF00288961
    title: "Lawrence T. Kou, George Markowsky and Leonard Berman, A fast algorithm for Steiner trees, Acta Informatica 15(2) (1981), 141-145"
    locator: the whole paper (the five steps, the bound 2(1 - 1/l) and the O(|S| |V|^2) running time)
  - paper: doi:10.1016/0020-0190(88)90066-X
    title: "Kurt Mehlhorn, A faster approximation algorithm for the Steiner problem in graphs, Information Processing Letters 27(3) (1988), 125-128"
    locator: the whole paper (the same guarantee in O(m + n log n) time, by Voronoi regions of the terminals)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms, Springer (2001)
    locator: Chapter 3, Steiner Tree and TSP (Section 3.1, the metric Steiner tree problem and the MST-based factor 2 algorithm, with a tight example)
---

The Kou-Markowsky-Berman algorithm, or KMB, is an [approximation algorithm](/approximation-ratio/) for the [Steiner tree problem](/steiner-tree-problem/): connect a given set of terminals in a weighted graph by a tree of least weight, where the tree may pass through other vertices. The problem is NP-hard. KMB builds the complete graph on the terminals with [shortest path](/dijkstra/) distances as weights, takes a [minimum spanning tree](/minimum-spanning-tree/) of it, replaces each of its edges by a shortest path, takes a minimum spanning tree of the result, and trims leaves that are not terminals. The tree it returns weighs at most $2(1 - 1/l)$ times the optimum, where $l$ is the number of leaves of an optimal tree. The original version takes $O(s n^2)$ time for $s$ terminals; Mehlhorn's version gives the same guarantee in $O(m + n \log n)$.

## In plain words

You must link a few chosen towns by roads, and you may route through other towns on the way if that helps. Finding the cheapest such network is hard.

A simple plan gets within a factor of two. For every pair of chosen towns, find the shortest route between them. Now pretend that each such route is a direct road, and build the cheapest network on the chosen towns alone, which is easy. Then lay out the real routes it uses. Where the routes overlap or form a loop, keep a cheapest tree of them, and cut off any dead ends that lead to a town nobody asked for.

## The problem

The input is an undirected graph with $n$ vertices, $m$ edges and a weight $w(e) \ge 0$ on each edge, and a set $S$ of $s$ terminals. Weights may tie. Parallel edges and self-loops are allowed. The graph need not be connected, but a solution exists only if all terminals lie in one component; otherwise the algorithm returns NONE. The output is a tree in the graph that contains every terminal, of small total weight. Negative weights are not allowed: with them, shortest paths may not exist, and the bound fails.

## The algorithm

```pseudo id=main
KOU-MARKOWSKY-BERMAN(G, w, S)
L1  for each terminal a ∈ S do run Dijkstra's algorithm from a       ▷ distances d(a, ·) and shortest paths
L2  G1 ← the complete graph on S with weight d(a, b) on each edge ab; if some d(a, b) = ∞ then return NONE
L3  T1 ← a minimum spanning tree of G1
L4  GS ← the subgraph of G formed by a shortest path from a to b for each edge ab of T1
L5  T2 ← a minimum spanning tree of GS
L6  return T2 after deleting, again and again, each leaf that is not a terminal
```

Lines L1 and L2 compute the *distance graph*, the metric closure of $G$ restricted to the terminals. Line L3 is where the approximation comes from. Lines L4 and L5 turn the tree on terminals back into a subgraph of $G$: two shortest paths can share edges, or together close a cycle, so $G_S$ need not be a tree, and its minimum spanning tree can only be lighter. Line L6 removes branches that serve no terminal. Lines L5 and L6 never make the tree heavier, and they often make it lighter, but the guarantee already holds for $G_S$.

## Example

The graph has the vertices $a$ to $f$ and the edges $ab = 4$, $ac = 3$, $bc = 1$, $bd = 2$, $cd = 4$, $ce = 5$, $de = 7$, $df = 6$, $ef = 2$. The terminals are $a$, $b$ and $e$.

**Lines L1 and L2.** The distances are $d(a, b) = 4$, by the edge $ab$ or by the path $a, c, b$, which ties; $d(a, e) = 8$, by $a, c, e$; and $d(b, e) = 6$, by $b, c, e$.

**Line L3.** The minimum spanning tree of the triangle with weights 4, 8 and 6 is $T_1 = \{ab, be\}$, of weight 10.

**Lines L4 to L6.** The result depends on which shortest path from $a$ to $b$ line L4 takes.

| path for $ab$ | $G_S$ | $T_2$ | after line L6 | weight |
|---|---|---|---|---|
| the edge $ab$ (the implementation's choice) | $\{ab, bc, ce\}$ | $\{ab, bc, ce\}$ | unchanged | 10 |
| $a, c, b$ | $\{ac, bc, ce\}$ | $\{ac, bc, ce\}$ | unchanged | 9 |

The optimum is $\{ac, bc, ce\}$, of weight 9. With the first choice the algorithm returns 10, within the bound $2(1 - 1/3) \cdot 9 = 12$. With the second, the two paths share the edge $bc$, so $G_S$ weighs 9, less than $w(T_1) = 10$; shared edges are the reason the result can beat $T_1$.

**A tight example.** Take a hub $h$, terminals $t_1, \ldots, t_k$, spokes $h t_i$ of weight 1, and edges $t_i t_{i+1}$ of weight $2 - \varepsilon$. Each pair of neighbouring terminals has distance $2 - \varepsilon$, every other pair has distance 2, so $T_1$ is the path $t_1 t_2 \cdots t_k$, and $G_S$ is the same path, of weight $(k - 1)(2 - \varepsilon)$. The optimum is the star through $h$, of weight $k$, with $l = k$ leaves. As $\varepsilon \to 0$, the ratio tends to $2(1 - 1/k)$, so the bound cannot be improved.

## Correctness

**Theorem.** If the terminals lie in one component, KMB returns a tree that contains every terminal, whose leaves are all terminals, and whose weight is at most $2(1 - 1/l)\,\mathrm{OPT} \le 2(1 - 1/s)\,\mathrm{OPT}$, where $l$ is the number of leaves of an optimal tree. Otherwise it returns NONE.

*The output is a Steiner tree.* The paths of line L4 follow the edges of the spanning tree $T_1$, so their union $G_S$ is connected and holds all terminals, and $T_2$ is a tree that holds them. Deleting a non-terminal leaf keeps a tree and keeps every terminal.

*The weight.* Since weights are non-negative, $w(\text{result}) \le w(T_2) \le w(G_S) \le w(T_1)$, the last because each edge of $G_S$ lies on one of the paths, whose lengths add up to $w(T_1)$. To bound $w(T_1)$, walk around an optimal tree $T^*$, using each edge twice, for a closed walk of length $2\,\mathrm{OPT}$. The $l$ leaves cut the walk into $l$ pieces; drop the longest, of length at least $2\,\mathrm{OPT}/l$. The rest still passes every terminal, because each edge appears in two different pieces, so it is a walk of length at most $2(1 - 1/l)\,\mathrm{OPT}$ through all terminals. The order in which it meets them gives a path in $G_1$ that is no longer, and $T_1$ is at most as heavy as that path.

The choice of shortest paths and the tie rule of the two spanning trees do not matter. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The model is the word RAM, with weights that are added and compared in $O(1)$ time.

- **Lines L1 and L2.** $s$ runs of [Dijkstra's algorithm](/dijkstra/) with a [binary heap](/binary-heap/) take $O(s (m + n) \log n)$ time; with a Fibonacci heap, $O(s (m + n \log n))$. The original paper uses the $O(n^2)$ array version, for $O(s n^2)$.
- **Line L3.** $G_1$ has $s(s-1)/2$ edges, and Prim's algorithm on it takes $O(s^2)$ time, which is within the bound since $s \le n$.
- **Lines L4 to L6.** $G_S$ has at most $(s - 1)(n - 1)$ edges, but all of them are edges of $G$, so at most $m$ distinct ones; a minimum spanning tree of it and the trimming take $O(m \log m)$ time, within the bound for $s \ge 2$, since $\log m = O(\log n)$.
- **Space.** The $s$ distance and predecessor arrays take $O(s n)$, and the graph $O(m)$.

| claim | bound | case |
|---|---|---|
| time with Fibonacci heaps | $O(s (m + n \log n))$ | worst |
| time, original version | $O(s n^2)$ | worst |
| time, Mehlhorn's version | $O(m + n \log n)$ | worst |
| approximation ratio | $2(1 - 1/l) \le 2(1 - 1/s)$ | every input |

## Properties

- **Approximation ratio** $2(1 - 1/l)$, and the bound is tight.
- **Exact in two cases.** With $s = 2$ it returns a shortest path, which is optimal. With $S = V$, $G_1$ is the closure of $G$, and the result is a minimum spanning tree of $G$, which is optimal too.
- **Deterministic** with fixed tie rules. Different tie rules can give trees of different weights, as the example shows, but all meet the bound.
- **Leaves are terminals**, by line L6.

## Variants and improvements

- **Mehlhorn (1988).** Run one Dijkstra from all terminals at once, which splits $V$ into regions of the nearest terminal. Each edge between two regions gives a candidate edge between their terminals. The minimum spanning tree of this smaller graph is a minimum spanning tree of a graph that serves as $G_1$, for $O(m + n \log n)$ time in all and the same guarantee.
- **Wu, Widmayer and Wong (1986).** A similar idea in $O(m \log n)$ time.
- **The shortest path heuristic.** Grow the tree from one terminal by adding a shortest path to the nearest terminal not yet connected, as in Prim's algorithm on the closure. It has the same factor 2.
- **Better ratios.** Zelikovsky's algorithm, with ratio $11/6$, and its successors improve on the factor 2 by adding small full components; the best known ratio, $\ln 4 + \varepsilon \approx 1.39$, comes from an LP-based method of Byrka, Grandoni, Rothvoß and Sanità.
- **Metric TSP.** The same double-the-tree argument gives the factor 2 for the [metric traveling salesman problem](/metric-tsp/).

## When to use it

Use it for a fast Steiner tree with a guarantee: wire routing in chip design, multicast trees in networks, and connecting genes or proteins in a network in computational biology. It is a good start for local search. When the number of terminals is small, exact methods such as the Dreyfus-Wagner dynamic program, which is exponential only in $s$, can be practical instead.

## Pitfalls

- **Skipping lines L5 and L6.** Returning the union $G_S$ can return a graph with a cycle, or with dead branches. The bound still holds for its weight, but the output is not a tree.
- **The MST of $G$ restricted to the terminals.** The subgraph of $G$ induced by the terminals may be disconnected or much heavier than needed; the distances of line L1 are what let the tree pass through other vertices.
- **Negative weights.** Shortest paths and the bound need $w \ge 0$; the implementation rejects negative weights.
- **Terminals in different components.** Then some distance is infinite and no Steiner tree exists; return NONE rather than a forest.
- **Expecting optimality.** The result can be off by almost a factor of 2, as the tight example shows.

## Implementations

## History

Lawrence Kou, George Markowsky and Leonard Berman, at the IBM Watson Research Center, published the algorithm and its bound $2(1 - 1/l)$ in Acta Informatica in 1981, with an $O(s n^2)$ running time. Similar MST-based heuristics, with the same factor, were studied in the same years, among them the shortest path heuristic of Takahashi and Matsuyama (1980). Wu, Widmayer and Wong (1986) and Mehlhorn (1988) made it faster. Since then, a long line of work has lowered the ratio below 2.

## References
