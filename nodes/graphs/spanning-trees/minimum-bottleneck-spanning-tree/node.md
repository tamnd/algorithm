---
tag: 22QWHV
kind: problem
slug: minimum-bottleneck-spanning-tree
name: Minimum bottleneck spanning tree problem
aliases:
- minimax spanning tree
area: graphs/spanning-trees
level: core
summary: Find a spanning tree minimizing the maximum edge weight; every MST solves it.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(m)}
prereqs: [minimum-spanning-tree, spanning-tree, cut-property, connected-graph]
see_also: [maximum-spanning-tree, widest-path, kruskal, single-linkage-clustering, median-of-medians, minimum-arborescence, cycle-property, mst-uniqueness]
sources:
  - paper: doi:10.1016/0020-0190(78)90030-3
    title: "Paolo M. Camerini, The min-max spanning tree problem and some extensions, Information Processing Letters 7(1) (1978), 10-14"
    locator: the whole paper (the linear-time algorithm by medians and contraction)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 21, Minimum Spanning Trees (the chapter problem on bottleneck spanning trees)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 4.5, The Minimum Spanning Tree Problem (the cut property used in the proof)
  - book: isbn:9780898711875
    title: Robert E. Tarjan, Data Structures and Network Algorithms, SIAM (1983)
    locator: Chapter 6, Minimum Spanning Trees
---

The minimum bottleneck spanning tree problem asks, for a connected undirected [weighted graph](/weighted-graph/), for a [spanning tree](/spanning-tree/) whose heaviest edge is as light as possible. The weight of that heaviest edge is the *bottleneck* of the tree. Every [minimum spanning tree](/minimum-spanning-tree/) is a minimum bottleneck spanning tree (MBST), so [Kruskal's](/kruskal/) or [Prim's](/prim/) algorithm solves the problem, but not every MBST is a minimum spanning tree. The problem is easier than the MST problem: Camerini's algorithm solves it in $O(m)$ time by medians and contraction, and $\Omega(m)$ time is needed.

## In plain words

You must connect a set of towns with roads, and you care only about the worst road you build, for example the longest bridge or the most expensive single link. You want that worst road to be as good as possible. The total of all roads does not matter.

The cheapest connecting network always works for this goal: its worst road is as good as the worst road of any other connecting network. But there can be other answers, which are more expensive in total and have the same worst road.

The best possible worst road is found by a simple test: take only the roads up to some limit and ask whether they connect all the towns. The smallest limit that works is the answer.

## Definition

**Input.** A connected undirected graph $G = (V, E)$ with $n = |V|$ and $m = |E|$, and a weight $w : E \to \mathbb{R}$. Weights may tie and may be negative. Parallel edges are allowed; self-loops are in no spanning tree and can be dropped.

**Output.** A spanning tree $T$ that minimizes the bottleneck

$$b(T) = \max_{e \in T} w(e).$$

The optimal value is

$$b^* = \min \{ \beta : \text{the graph } (V, \{e \in E : w(e) \le \beta\}) \text{ is connected} \},$$

and a spanning tree $T$ is an MBST if and only if $T$ is a spanning tree of this *threshold graph* at $\beta = b^*$.

**Disconnected graphs.** If $G$ is not connected, it has no spanning tree. The usual extension asks for a spanning forest whose heaviest edge is as light as possible, which is the same problem solved in each component, with the largest of the component values as the result.

**Ties.** MBSTs are almost never unique, even with distinct weights: each spanning tree of the threshold graph at $b^*$ is one.

**Every MST is an MBST.** Let $T$ be a minimum spanning tree with a heaviest edge $e$, and assume a spanning tree $T'$ has $b(T') < w(e)$. Removing $e$ from $T$ leaves two trees, with vertex sets $S$ and $V \setminus S$. The tree $T'$ connects them, so it has an edge $f$ across the cut, with $w(f) \le b(T') < w(e)$. Then $T - e + f$ is a spanning tree lighter than $T$, a contradiction.

**The converse is false.** In the triangle with $w(ab) = 1$ and $w(bc) = w(ca) = 5$, each spanning tree has bottleneck 5, so all three are MBSTs, but only $\{ab, bc\}$ and $\{ab, ca\}$, of weight 6, are minimum spanning trees; $\{bc, ca\}$ has weight 10.

## Variants

- **Maximum bottleneck spanning tree.** Maximize the smallest edge weight. Reverse the order; every [maximum spanning tree](/maximum-spanning-tree/) is a solution.
- **Lexicographic bottleneck.** Minimize the largest weight, then the second largest, and so on. Every minimum spanning tree solves it: by the matroid structure of spanning trees, an MST minimizes, for each $k$, the $k$-th largest edge weight among all spanning trees. This is the strong form of the claim that every MST is an MBST.
- **Directed version.** In a directed graph with a root, find a spanning arborescence whose heaviest arc is lightest. The threshold test is a reachability search from the root, and the [minimum arborescence](/minimum-arborescence/) problem also solves it. Camerini (1978) treats it with the same median method; Gabow and Tarjan (1988) gave an $O(m \log^* n)$ algorithm.
- **Bottleneck path.** For two vertices $u$ and $v$, find a path whose heaviest edge is lightest, a minimax path. See [widest path](/widest-path/) for the max-min form.

## Examples

Take the vertices $a$ to $f$ and the edges $ab = 4$, $ac = 3$, $bc = 1$, $bd = 2$, $cd = 4$, $ce = 5$, $de = 7$, $df = 6$, $ef = 2$.

- The threshold graph at $\beta = 4$ has the edges $ab, ac, bc, bd, cd, ef$ and the two components $\{a, b, c, d\}$ and $\{e, f\}$, so $b^* > 4$. At $\beta = 5$ the edge $ce$ joins them, so $b^* = 5$.
- The minimum spanning tree $\{bc, bd, ef, ac, ce\}$ has weight 13 and bottleneck $w(ce) = 5$.
- In the threshold graph at 5, the edges $ce$ and $ef$ are bridges, so every MBST contains them, plus a spanning tree of the four vertices $a, b, c, d$ with the edges $ab, ac, bc, bd, cd$. That graph is $K_4$ without the edge $ad$, which has 8 spanning trees. So the graph has 8 MBSTs among its 55 spanning trees, and only one of them is minimum. For example, $\{ab, ac, cd, ce, ef\}$ is an MBST of weight 18.
- Of the 55 spanning trees, 8 have bottleneck 5, 21 have bottleneck 6 and 26 have bottleneck 7.

## Known algorithms

- **Any MST algorithm.** [Kruskal's algorithm](/kruskal/) in $O(m \log m)$ time, [Prim's](/prim/) in $O(m \log n)$, or the faster MST algorithms. Kruskal's algorithm can stop at the edge that makes the forest a tree; that edge has weight $b^*$.
- **Sort and binary search.** Sort the distinct weights, and binary search for the smallest $\beta$ whose threshold graph is connected, with a [breadth-first search](/breadth-first-search/) for each test. $O(m \log m)$ time.
- **Camerini's algorithm, $O(m)$.** On a connected graph with $m$ edges:
  1. If $m$ is at most a constant, solve the problem directly.
  2. Find a median weight by linear-time [selection](/median-of-medians/), and split $E$ into the lighter half $L$ and the heavier half $H$, with ties broken by the edge index so that the halves have sizes $\lceil m/2 \rceil$ and $\lfloor m/2 \rfloor$.
  3. If $(V, L)$ is connected, an MBST of $(V, L)$ is an MBST of $G$: recurse on $(V, L)$.
  4. Otherwise compute a spanning forest $F$ of $(V, L)$, contract each of its components to one vertex, and recurse on the contracted graph with the edges of $H$, dropping self-loops. Return $F$ together with the edges of the recursive answer.

  Each level takes $O(n + m)$ time. In step 3 the graph $(V, L)$ is connected, so $n \le |L| + 1$; in step 4 the contracted graph is connected, so its vertex count is at most $|H| + 1$. So the cost is $T(m) = T(m/2) + O(m) = O(m)$. Correctness of step 4: each spanning tree contains at least $c - 1$ edges of $H$, where $c$ is the number of components of $(V, L)$, so $b^* > \max_{e \in L} w(e)$, and joining the components with edges of $H$ is the only question left.

## Bounds

- **Upper bound.** $O(m)$ deterministic time on the word RAM, and in the comparison model, by Camerini's algorithm.
- **Lower bound.** $\Omega(m)$. On a cycle with $m$ edges, the spanning trees are the $m$ paths that leave out one edge, and a tree is an MBST if and only if the edge left out is a heaviest edge of the cycle. Let an adversary give distinct weights to the edges that the algorithm reads. If the algorithm never reads two edges $e$ and $f$, its output leaves out some edge, and the adversary makes some other unread edge the unique heaviest, so the output is wrong. So a correct algorithm reads at least $m - 1$ weights.
- So the problem takes $\Theta(m)$ time, while for the minimum spanning tree problem no deterministic $O(m)$ algorithm is known.

## Reductions

- **From MBST to MST.** Every MST is an MBST, so each MST algorithm solves the problem.
- **To graph connectivity.** The decision version, "is there a spanning tree with bottleneck at most $\beta$", is one connectivity test of the threshold graph, in $O(n + m)$ time.
- **Minimax paths.** For each pair $u, v$, the path from $u$ to $v$ in a minimum spanning tree is a minimax path. This holds for minimum spanning trees, not for all MBSTs: in the triangle above, the MBST $\{bc, ca\}$ joins $a$ and $b$ by a path of bottleneck 5, while the edge $ab$ alone has bottleneck 1.

## Applications

- **Critical range of a network.** For points in the plane, the smallest radius at which the disk graph of the points is connected is the longest edge of a Euclidean minimum spanning tree. This is the smallest transmission range that connects a wireless network.
- **Clustering thresholds.** In [single-linkage clustering](/single-linkage-clustering/), the distance at which all points form one cluster is the bottleneck $b^*$.
- **Worst-link design.** When the quality of a network is that of its weakest or longest link, as with the length of cables or the capacity of links, the MBST is the right model, and the extra freedom over the MST can be used for a second goal.

## References
