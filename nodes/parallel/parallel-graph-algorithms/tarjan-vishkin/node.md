---
tag: 91X4KQ
kind: algorithm
slug: tarjan-vishkin
name: Tarjan-Vishkin biconnectivity
aliases:
- Tarjan-Vishkin algorithm
- parallel biconnected components
area: parallel/parallel-graph-algorithms
level: advanced
summary: Parallel biconnected components computed from a spanning tree via Euler tour and auxiliary connectivity.
solves: [biconnected-components]
model: crcw-pram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O((n + m) log n)}
  depth: {worst: O(log n)}
  space: {extra: O(n + m)}
properties: {deterministic: true, recursive: false}
prereqs: [biconnected-components, shiloach-vishkin, euler-tour-technique, parallel-list-ranking, all-prefix-sums]
see_also: [hopcroft-tarjan-biconnectivity, articulation-point, bridge-finding, block-cut-tree, ear-decomposition, range-minimum-query, sparse-table, tree-contraction]
sources:
  - paper: doi:10.1137/0214061
    title: Robert E. Tarjan and Uzi Vishkin, An efficient parallel biconnectivity algorithm, SIAM Journal on Computing 14(4), 1985
    locator: pp. 862 to 874 (the auxiliary graph built from an arbitrary spanning tree, preorder numbers, nd, low and high, and the O(log n) time CRCW PRAM bound with O(n + m) processors)
  - book: isbn:9780201548563
    title: Joseph JaJa, An Introduction to Parallel Algorithms, Addison-Wesley, 1992
    locator: Chapter 5, the section on biconnected components; section number to be checked
---

Tarjan-Vishkin biconnectivity finds the [biconnected components](/biconnected-components/) of an undirected graph on the [CRCW PRAM](/crcw-pram/) in $O(\log n)$ time with $O(n + m)$ processors. The sequential [Hopcroft-Tarjan](/hopcroft-tarjan-biconnectivity/) algorithm needs a depth-first search tree, which has no known fast parallel algorithm. Tarjan and Vishkin (1985) work with any spanning tree instead: they compute preorder numbers and subtree sizes with the [Euler tour technique](/euler-tour-technique/), build an auxiliary graph whose vertices are the tree edges, and reduce the problem to [connected components](/connected-components/) of that graph.

Notation on this page: $G = (V, E)$ is a simple undirected graph with $n$ vertices and $m$ edges, $T$ is a spanning forest, $W$ is the work, $S$ the span and $T_p$ the time on $p$ processors. The model is the synchronous CRCW PRAM with the arbitrary write rule. Two edges are in the same biconnected component (block) when they are equal or lie on a common simple cycle; this is an equivalence relation on $E$. The bounds are worst case and deterministic.

## In plain words

Two edges belong to the same block when some loop in the graph runs through both. The sequential method finds these loops with a depth-first search, but a depth-first search is slow to run in parallel.

This algorithm takes any spanning tree, which is fast to find in parallel. It numbers the vertices in the order a walk around the tree meets them, so that each subtree gets a block of consecutive numbers. Each edge outside the tree closes a loop with the tree.

The algorithm then builds a new graph whose points are the tree edges. It joins two tree edges when a simple rule, read off the numbers, shows that some loop runs through both. The groups of connected points in the new graph are exactly the blocks. Each edge outside the tree joins the group of one tree edge on its loop.

## The problem

The input is a simple undirected graph $G$ as a list of edges. The output is a label for each edge, with two labels equal if and only if the two edges are in the same block. Articulation points and bridges follow from the labels: a vertex is an [articulation point](/articulation-point/) when its edges carry two or more labels, and an edge is a [bridge](/bridge-finding/) when its label occurs once.

## The algorithm

The algorithm roots the spanning forest at a new vertex $z$ joined to one vertex of each tree, so that it is one tree. In the tree, $p(v)$ is the parent of $v$, $pre(v)$ the preorder number with $pre(z) = 0$, and $nd(v)$ the number of descendants of $v$, $v$ included. The descendants of $v$ are exactly the vertices $u$ with $pre(v) \le pre(u) < pre(v) + nd(v)$. Each tree edge $\{p(w), w\}$ is named by its lower end $w$. For a vertex $v$,

$$low(v) = \min \{\, pre(y) : y = x \text{ or } \{x, y\} \text{ a nontree edge, for a descendant } x \text{ of } v \,\},$$

and $high(v)$ is the same with max.

```pseudo id=main
TARJAN-VISHKIN(V, E)
L1  T ← a spanning forest of G, by Shiloach-Vishkin with recorded hooks
L2  add a vertex z and an edge from z to one vertex of each tree of T
L3  build the Euler tour of the tree from z, and rank it by list ranking
L4  for all v in parallel do p(v), pre(v), nd(v) ← from the ranks and a prefix sum
L5  for all v in parallel do local(v) ← min and max of pre(v) and pre(y) over nontree edges {v, y}
L6  for all v in parallel do low(v), high(v) ← min and max of local over the preorder range of v
L7  for all nontree edges {v, w} with pre(v) < pre(w) in parallel do                 ▷ rule 1
        if pre(v) + nd(v) ≤ pre(w) then join v and w in G'
L8  for all tree edges {v, w} with v = p(w) and v ≠ z in parallel do                   ▷ rule 2
        if low(w) < pre(v) or high(w) ≥ pre(v) + nd(v) then join v and w in G'
L9  label ← the connected components of G', by Shiloach-Vishkin
L10 give each tree edge {p(w), w} and each nontree edge {v, w} with pre(v) < pre(w) the label of w   ▷ rule 3
L11 return the labels of the edges of G
```

The vertices of $G'$ stand for tree edges: vertex $w$ of $G'$ is the edge $\{p(w), w\}$. Rule 1 joins the two tree edges at the ends of a nontree edge whose ends are not ancestor and descendant. Rule 2 joins a tree edge to the tree edge above it when some nontree edge leaves the subtree of the lower edge and also leaves the subtree of the upper one. Rule 3 puts each nontree edge with the tree edge above its end with the larger preorder number. The edges at $z$ are bridges and form their own blocks; line L11 drops them.

## Example

The graph has the vertices 0 to 6 and the edges $\{0,1\}$, $\{0,2\}$, $\{1,3\}$, $\{2,3\}$, $\{3,4\}$, $\{4,5\}$, $\{4,6\}$, $\{5,6\}$: a square $0, 1, 3, 2$, a bridge $\{3,4\}$, and a triangle $4, 5, 6$. Say line L1 returns the tree with all edges except $\{2,3\}$ and $\{5,6\}$. The root $z$ is joined to 0, and the tour visits the neighbours of each vertex in increasing order, with $z$ last.

| $v$ | $p(v)$ | $pre(v)$ | $nd(v)$ | local | $low(v)$ | $high(v)$ |
|---|---|---|---|---|---|---|
| 0 | $z$ | 1 | 7 | 1, 1 | 1 | 7 |
| 1 | 0 | 2 | 5 | 2, 2 | 2 | 7 |
| 3 | 1 | 3 | 4 | 3, 7 | 3 | 7 |
| 4 | 3 | 4 | 3 | 4, 4 | 4 | 6 |
| 5 | 4 | 5 | 1 | 5, 6 | 5 | 6 |
| 6 | 4 | 6 | 1 | 5, 6 | 5 | 6 |
| 2 | 0 | 7 | 1 | 3, 7 | 3 | 7 |

Rule 1: the nontree edge $\{3, 2\}$ has $pre(3) + nd(3) = 7 \le pre(2) = 7$, so 3 and 2 are joined; $\{5, 6\}$ has $5 + 1 \le 6$, so 5 and 6 are joined. Rule 2: for $v = 1$, $w = 3$, $high(3) = 7 \ge pre(1) + nd(1) = 7$, so 1 and 3 are joined. No other tree edge passes: for $v = 3$, $w = 4$, $low(4) = 4 \ge 3$ and $high(4) = 6 < 7$, which marks $\{3, 4\}$ as a bridge. The components of $G'$ are $\{1, 2, 3\}$, $\{4\}$ and $\{5, 6\}$, plus $\{0\}$ for the edge at $z$. Rule 3 puts $\{2, 3\}$ with 2 and $\{5, 6\}$ with 6. The blocks are $\{01, 02, 13, 23\}$, $\{34\}$ and $\{45, 46, 56\}$.

## Correctness

The proof file proves the following in full. Every join made by rules 1, 2 and 3 joins two edges of one fundamental cycle, the cycle that a nontree edge closes with the tree path between its ends, so joined edges are in one block. Conversely, all tree edges of one fundamental cycle are joined in $G'$ by rule 1 at the top and rule 2 along both sides, and rule 3 adds the nontree edge. Two edges in one block lie on a simple cycle $C$, and the fundamental cycles of the nontree edges of $C$ form a chain in which neighbours share an edge: if they split into two groups with no shared edge, the edges of $C$ would split into two nonempty sets in which every vertex has even degree, which a simple cycle does not allow. So the labels are exactly the blocks.

## Complexity

The model is the CRCW PRAM, arbitrary write.

- **Line L1 and line L9.** Two calls to [Shiloach-Vishkin](/shiloach-vishkin/) on graphs with at most $n$ vertices and $m$ edges: $O((n + m) \log n)$ work and $O(\log n)$ time, the time bound as cited on that page.
- **Lines L2 to L4.** The Euler tour of the tree on $n + 1$ vertices has $2n$ arcs. With work-efficient [list ranking](/parallel-list-ranking/) and [prefix sums](/all-prefix-sums/), this is $O(n)$ work and $O(\log n)$ span, once the arcs are grouped by their tail. The grouping comes from adjacency arrays of $G$, or from a sort; the implementation charges a sort, $O(n \log n)$ work and $O(\log n)$ span.
- **Lines L5 and L6.** The local values need a minimum and a maximum over the edges at each vertex: $O(n + m)$ work and $O(\log n)$ span. The values $low(v)$ and $high(v)$ are minima and maxima over the preorder range of the subtree, which a [sparse table](/sparse-table/) gives with $O(n \log n)$ work and $O(\log n)$ span, or a [range-minimum](/range-minimum-query/) structure with $O(n)$ work.
- **Lines L7, L8, L10.** $O(n + m)$ work and $O(1)$ time.

In total

$$W = O((n + m) \log n), \qquad S = O(\log n),$$

and the connectivity calls dominate the work. The other steps can be done in $O(n + m)$ work, so the work of the whole algorithm is that of connectivity plus $O(n + m)$. By [Brent's theorem](/brent-theorem/), $T_p = O((n + m) \log n / p + \log n)$. The implementation uses the full-shortcut form of Shiloach-Vishkin, which has $O(\log^2 n)$ span; on all test graphs its span counter stays below $12 \log_2^2 (n + 2) + 40$ steps.

## Properties

- **Any spanning tree works.** The rules use only preorder numbers and subtree sizes, which are defined for every rooted tree. This is what removes the depth-first search.
- **Reduction to connectivity.** All the graph-dependent work is in two connectivity calls; the rest is list ranking, prefix sums and range minima, which are work-efficient.
- **Labels, not a tree of blocks.** The output is a partition of the edges. The [block-cut tree](/block-cut-tree/) follows with $O(n + m)$ more work.

## Variants and improvements

- **Ear decomposition.** A graph has an [ear decomposition](/ear-decomposition/) if and only if it is 2-edge-connected, and an open one if and only if it is 2-vertex-connected. Parallel ear decomposition algorithms use the same spanning tree, preorder and connectivity steps, and they also give st-numberings.
- **Bridges only.** Bridges need no auxiliary graph: the tree edge $\{p(w), w\}$ is a bridge if and only if $low(w) \ge pre(w)$ and $high(w) < pre(w) + nd(w)$, that is, no nontree edge leaves the subtree of $w$.
- **Low and high by tree contraction.** Instead of a range structure on the preorder, $low$ and $high$ are subtree minima and maxima, which [tree contraction](/tree-contraction/) also computes in $O(n)$ work and $O(\log n)$ span.

## When to use it

Use it for biconnected components, articulation points and bridges on a parallel machine, when a depth-first search tree would be the bottleneck. On a single core, [Hopcroft-Tarjan](/hopcroft-tarjan-biconnectivity/) is simpler and does $O(n + m)$ work with a small constant. The parallel method pays for an Euler tour, list ranking and two connectivity passes.

## Pitfalls

- **Rule 1 on ancestor pairs.** A nontree edge from a vertex to its own ancestor must not join the two tree edges at its ends directly in rule 1. Its cycle is handled by rule 2 along the tree path; the test $pre(v) + nd(v) \le pre(w)$ rules such edges out.
- **Rule 2 at the root.** The root has no parent edge, so rule 2 must skip $v = z$. With a forest, a real vertex joined to $z$ is the root of its own tree; its edge to $z$ is a bridge and must not reach the output.
- **The range of $low$.** $low(w)$ is a minimum over the whole subtree of $w$, not over the nontree edges at $w$ only. Using only the edges at $w$ misses cycles that start deeper in the subtree.
- **Labels for nontree edges.** Rule 3 must use the end with the larger preorder number. The edge above the other end need not lie on the fundamental cycle, for example when that end is an ancestor of the first.
- **Multigraphs.** Two parallel edges form a block of their own. The rules work if the second copy is a nontree edge, but the pseudocode and the proof assume a simple graph.

## Implementations

## History

Tarjan and Vishkin presented the algorithm at FOCS 1984 and in the SIAM Journal on Computing in 1985. It answered the question of finding biconnected components in parallel without a depth-first search tree, whose parallel complexity was open. The idea of computing tree functions by an Euler tour and list ranking, introduced in the same work, became the Euler tour technique used across parallel tree algorithms.

## References
