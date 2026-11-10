---
tag: 426R8D
kind: concept
slug: graph-contraction
name: Graph contraction
aliases:
- edge contraction
- vertex contraction in parallel
- star contraction
area: parallel/parallel-graph-algorithms
level: core
summary: Merging groups of vertices into supervertices to shrink a graph while preserving the answer.
prereqs: [connected-components, work-span-model, parallel-pack]
see_also: [random-mate-contraction, shiloach-vishkin, parallel-minimum-spanning-tree, boruvka, list-contraction, tree-contraction, maximal-matching, karger-min-cut]
sources:
  - url: https://sites.google.com/site/alphalambdabook/
    title: Umut A. Acar and Guy E. Blelloch, Algorithms, Parallel and Sequential, draft book for Carnegie Mellon course 15-210
    locator: part Graph Contraction (edge contraction, star contraction, and connectivity by star contraction with work O(m log n) and span O(log^2 n)); chapter numbers differ between drafts
  - paper: "John H. Reif, Optimal parallel algorithms for integer sorting and graph connectivity, Technical Report TR-08-85, Aiken Computation Laboratory, Harvard University, 1985"
    title: Optimal parallel algorithms for integer sorting and graph connectivity
    locator: the random-mate connectivity algorithm; report number and sections to be checked
  - book: isbn:9780201548563
    title: Joseph JaJa, An Introduction to Parallel Algorithms, Addison-Wesley, 1992
    locator: Chapter 5 (connected components and minimum spanning trees by hooking and contraction); section numbers to be checked
---

Graph contraction is the step of parallel graph algorithms that splits the vertices into connected groups, merges each group into one supervertex, and keeps the edges between groups. If the groups are chosen so that the number of vertices falls by a constant factor in each round, then $O(\log n)$ rounds shrink any graph to isolated vertices, whatever its diameter. Problems whose answer survives the merge, such as [connected components](/connected-components/) and [minimum spanning trees](/parallel-minimum-spanning-tree/), are then solved by contracting, solving the small graph, and mapping the answer back. The usual groups are single edges (edge contraction), stars (star contraction), and the trees of hooked vertices in [Shiloach-Vishkin](/shiloach-vishkin/) and [Borůvka](/boruvka/).

## In plain words

To count the islands on a map, you can join any two pieces of land that touch into one piece. The count does not change. If every round joins many pairs at once, the map soon has one blob for each island, and you count the blobs.

Graph contraction does this to a graph. In each round it picks groups of vertices that are connected to each other, glues each group into one vertex, and keeps the edges that run between different groups. Edges inside a group disappear. The answer to the question, such as which vertices can reach each other, stays the same, so the algorithm solves the smaller graph and then tells each original vertex the answer of its group.

The groups must be picked in parallel and must not interfere. Random coin flips are the usual way, and stars are the usual shape.

## The idea

Notation: $G = (V, E)$ is an undirected graph with $n$ vertices and $m$ edges, $W$ is the work and $S$ the span. The model is the [work-span model](/work-span-model/) with random choices; the bounds for star contraction are in expectation for the work and with high probability for the span, that is, with probability at least $1 - n^{-c}$ for a constant $c$ that can be chosen.

**A contraction step.** A partition $\pi$ of $V$ into blocks $B_1, \ldots, B_k$, each of which induces a connected subgraph, gives the contracted graph $G / \pi$. It has one vertex for each block, and an edge $\{B_a, B_b\}$ for each edge $\{u, v\} \in E$ with $u \in B_a$, $v \in B_b$, $a \ne b$. Edges inside a block are dropped. Parallel edges between two blocks may be kept or removed. The step is stored as a map $r : V \to V$ that sends each vertex to the representative of its block. Then the edges of $G / \pi$ are the pairs $\{r(u), r(v)\}$ with $r(u) \ne r(v)$, which a [pack](/parallel-pack/) of the relabeled edge list computes in $O(m)$ work and $O(\log n)$ span.

**Contraction for connectivity.** Two vertices are connected in $G$ if and only if their blocks are connected in $G / \pi$: a path in $G$ maps to a walk in $G / \pi$, and a walk in $G / \pi$ lifts to a path in $G$, because each block is connected. So the components of $G$ are found by the recursion

$$\mathrm{CC}(G) = \text{if } E = \emptyset \text{ then each vertex is its own label, else } \mathrm{label}(v) = \mathrm{CC}(G / \pi)\big(r(v)\big).$$

**Kinds of blocks.**

- *Edge contraction*: the blocks are the edges of a [matching](/maximal-matching/) and single vertices. A round removes one vertex for each matched edge.
- *Star contraction*: each block is a star, a center and some neighbours of it (the satellites). With [random-mate](/random-mate-contraction/) coins, a vertex that flips tails and has a neighbour that flips heads joins one such neighbour. Each non-isolated vertex is removed with probability at least $1/4$, so the expected number of non-isolated vertices falls by a factor of $3/4$ in each round.
- *Tree contraction*: the blocks are trees of a forest of hook pointers, flattened by [pointer jumping](/pointer-jumping/). This is the form of [Shiloach-Vishkin](/shiloach-vishkin/) and of [parallel Borůvka](/parallel-minimum-spanning-tree/).

**Cost of connectivity by star contraction.** The vertices fall to zero non-isolated ones in $O(\log n)$ rounds with high probability (the proof is on the [random-mate](/random-mate-contraction/) page). The edges need not fall: in the worst case, few edges disappear per round, so each round costs $O(m)$ work. With $O(\log n)$ span per round,

$$W = O(m \log n), \qquad S = O(\log^2 n),$$

the work in expectation and the span with high probability. The sequential [union-find](/union-find-connectivity/) or a BFS does $O(n + m)$ work, so this is not work-efficient. Work-efficient forms exist, which first sparsify the graph; this page does not cover them.

## Examples

**Star contraction, one round.** The graph has 7 vertices and the edges $\{0,1\}$, $\{1,2\}$, $\{2,3\}$, $\{3,0\}$, $\{3,4\}$, $\{4,5\}$, $\{5,6\}$. The coins are heads for 0, 2 and 5, and tails for 1, 3, 4 and 6. Each tails vertex with a heads neighbour hooks to its smallest heads neighbour.

| vertex | coin | heads neighbours | $r(v)$ |
|---|---|---|---|
| 0 | heads | | 0 |
| 1 | tails | 0, 2 | 0 |
| 2 | heads | | 2 |
| 3 | tails | 0, 2 | 0 |
| 4 | tails | 5 | 5 |
| 5 | heads | | 5 |
| 6 | tails | 5 | 5 |

The blocks are the stars $\{0, 1, 3\}$, $\{2\}$ and $\{4, 5, 6\}$. Relabeling gives the edges $\{0,0\}$, $\{0,2\}$, $\{2,0\}$, $\{0,0\}$, $\{0,5\}$, $\{5,5\}$, $\{5,5\}$. Dropping the 4 self-loops leaves $\{0,2\}$ twice and $\{0,5\}$. The round takes the graph from 7 vertices to 3, and from 7 edges to 3.

**Edge contraction on a star.** On the star with center 0 and leaves 1 to $n - 1$, every matching has one edge, so a round of edge contraction removes one vertex, and $n - 1$ rounds are needed. One round of star contraction removes all the tails leaves when the center flips heads. This is why parallel connectivity uses stars, not matchings.

**Non-example.** Merging the two ends of each edge of a spanning tree in one step is a contraction, but finding the blocks is the whole problem: the blocks are the components themselves. A contraction step is useful only when its blocks are cheap to find, in $O(1)$ or $O(\log n)$ span.

## Where it is used

- **Connected components.** [Shiloach-Vishkin](/shiloach-vishkin/) contracts trees of hook pointers; Reif's random-mate algorithm contracts stars.
- **Minimum spanning trees.** [Borůvka](/boruvka/) contracts along the lightest edge of each vertex; the [parallel form](/parallel-minimum-spanning-tree/) does it in $O(\log n)$ rounds.
- **Lists and trees.** [List contraction](/list-contraction/) and [tree contraction](/tree-contraction/) are graph contraction on paths and on trees, where the answer to map back is a rank or a value.
- **Biconnectivity.** [Tarjan-Vishkin](/tarjan-vishkin/) reduces biconnected components to connected components of an auxiliary graph, which then uses contraction.
- **Randomized cuts.** [Karger's min cut algorithm](/karger-min-cut/) contracts random edges, but to find a cut, not to keep connectivity; it is sequential in its basic form.

## References
