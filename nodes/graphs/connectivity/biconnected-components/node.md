---
tag: J43BN8
kind: problem
slug: biconnected-components
name: Biconnected components
aliases:
- Blocks
- 2-vertex-connected components
area: graphs/connectivity
level: core
summary: Partition the edges into maximal biconnected subgraphs (blocks) that share only articulation points.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(n + m)}
prereqs: [biconnected-graph, articulation-point]
see_also: [hopcroft-tarjan-biconnectivity, block-cut-tree, articulation-point-finding, bridge-finding, two-edge-connected-components, ear-decomposition, gabow-path-based-scc]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer
    locator: Section 3.1, 2-connected graphs and subgraphs (blocks, the block graph, and the fact that it is a tree)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 4.1, Cuts and connectivity (blocks, and the block-cutpoint graph)
  - paper: doi:10.1145/362248.362272
    title: John Hopcroft and Robert Tarjan, Algorithm 447, Efficient algorithms for graph manipulation, Communications of the ACM 16(6), 372 to 378 (1973)
    locator: the biconnected components algorithm
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 20, Problem 20-2, Articulation points, bridges, and biconnected components (Problem 22-2 in the third edition)
---

The biconnected components problem asks to split the edges of an [undirected graph](/undirected-graph/) into its *blocks*: two edges are in the same block when they lie on a common cycle. Each block with at least two edges is a maximal [biconnected](/biconnected-graph/) subgraph, a block with one edge is a [bridge](/bridge/) or a loop, and two blocks share at most one vertex, which is then an [articulation point](/articulation-point/). The [Hopcroft-Tarjan algorithm](/hopcroft-tarjan-biconnectivity/) finds all blocks with one [depth-first search](/depth-first-search/) in $\Theta(n + m)$ time. The blocks and the articulation points form a tree, the [block-cut tree](/block-cut-tree/), which describes how the graph hangs together.

## In plain words

Some parts of a network are tightly knit: inside such a part, the loss of any one point never cuts two other points of the part apart. These parts are the blocks. A road that is the only link between two places is a block on its own.

Two blocks touch in at most one point, and that point is a weak spot of the network: if it fails, the two blocks lose their link. So the blocks and the weak spots fit together like a tree, with the blocks as the rooms and the weak spots as the doors between rooms.

The task is to name, for each road, the block it belongs to. One depth-first walk over the network does it, with a stack of the roads seen so far.

## Definition

**Input.** An undirected graph $G = (V, E)$ with $V = \{0, \ldots, n-1\}$, given by adjacency lists, where $E$ is a multiset of $m$ edges: parallel edges and [self-loops](/self-loop/) are allowed. A *cycle* is a closed trail with $k \ge 1$ distinct edges and no repeated vertex except its first and last; a loop is a cycle of length 1, and two parallel edges form a cycle of length 2.

**Relation.** For edges $e, f \in E$, write

$$e \equiv f \iff e = f \ \text{ or } \ e \text{ and } f \text{ lie on a common cycle of } G.$$

**Output.** The classes $B_1, \ldots, B_b$ of $\equiv$, for example as a label $\beta : E \to \{1, \ldots, b\}$ with $\beta(e) = \beta(f) \iff e \equiv f$. The *vertex set* of a block is the set of ends of its edges. A vertex with no edges other than loops is often counted as an extra block with no edge; the vertex view of the problem then outputs the vertex sets, and the isolated vertices as blocks of one vertex.

**$\equiv$ is an equivalence relation.** It is reflexive and symmetric by definition. For transitivity, let $e \equiv f$ by a cycle $C_1$ and $f \equiv g$ by a cycle $C_2$, with $e, f, g$ distinct and $g \notin C_1$. If $f$ is a loop, then $C_1 = C_2 = \{f\}$ and $e = f$, a contradiction, so $f$ has two distinct ends, which lie on $C_1$ and on $C_2$. Walk along $C_2$ from $g$ in each of the two directions, and stop at the first vertex of $C_1$. This gives a path $Q \subseteq C_2$ that contains $g$, whose ends $x$ and $y$ are on $C_1$, and whose inner vertices are not on $C_1$. If $x = y$, all vertices of $C_2$ other than $x$ would be off $C_1$, but $C_2$ shares the two ends of $f$ with $C_1$; so $x \neq y$. The vertices $x$ and $y$ cut $C_1$ into two $x$-$y$ paths, and one of them, $P$, contains $e$. Then $P$ and $Q$ meet only in $x$ and $y$, so $P \cup Q$ is a cycle that contains $e$ and $g$. $\square$

**Facts about blocks.** Let $B$ and $B'$ be two different blocks.

1. *A block is connected.* If $e \equiv f$ by a cycle $C$, every edge of $C$ is in the class of $e$, so $e$ and $f$ are joined inside the class.
2. *Two blocks share at most one vertex.* Suppose they share $x \neq y$. By fact 1 there are $x$-$y$ paths $P \subseteq B$ and $P' \subseteq B'$, and they have no common edge. Follow $P$ from $x$ to the first vertex $z \neq x$ that lies on $P'$; it exists since $y$ is on $P'$. This part of $P$ and the part of $P'$ between $z$ and $x$ form a cycle with an edge of $B$ and an edge of $B'$, so $B = B'$, a contradiction.
3. *A shared vertex is an articulation point, and each articulation point is shared.* Let $x$ lie in $B$ and in $B'$, by the edges $xu \in B$ and $xw \in B'$, neither a loop. Then $u \neq w$, else the two edges form a cycle of length 2. A $u$-$w$ path that avoids $x$ would close a cycle with $xu$ and $xw$, so every $u$-$w$ path passes through $x$, and $x$ is an articulation point. Conversely, if $x$ is an articulation point, take neighbours $u$ and $w$ of $x$ in two different components of $G - x$. A cycle through the edges $xu$ and $xw$ would give a $u$-$w$ path without $x$, so these edges lie in two different blocks at $x$.
4. *The kinds of blocks.* A block with one edge is a loop or a bridge, by the theorem on the [bridge](/bridge/) page. A block with at least two edges is a bundle of parallel edges between two vertices, or it has at least three vertices; in a simple graph it is then a maximal biconnected subgraph (Diestel, Section 3.1).

## Variants

- **Vertex sets only.** Output the vertex set of each block. An articulation point appears in several sets; every other vertex appears in exactly one.
- **The block-cut tree.** Output the bipartite tree of blocks and articulation points. See [block-cut tree](/block-cut-tree/).
- **Excluding bridges.** CLRS defines a biconnected component as a maximal set of edges in which each two edges lie on a common simple cycle. Under that definition a bridge belongs to no component, and the components partition the edges that are not bridges.
- **2-edge-connected components.** Remove all bridges and take the [connected components](/connected-components/) that remain. This is a coarser partition: two triangles that share one vertex form one 2-edge-connected component but two blocks. See [two-edge-connected components](/two-edge-connected-components/).
- **Triconnected components.** Split each block further at pairs of vertices whose removal disconnects it. Hopcroft and Tarjan gave a linear-time method in 1973; it is much harder.
- **Dynamic.** Keep the blocks while edges are added or deleted. See [dynamic biconnectivity](/dynamic-biconnectivity/).

## Examples

The graph has $n = 7$ vertices and 10 edges: a triangle $0, 1, 2$ with a second copy of $\{0, 1\}$, the edge $\{2, 3\}$, a triangle $3, 4, 5$, the edge $\{5, 6\}$, and a loop at 6.

| block | edges | vertex set | kind |
|---|---|---|---|
| $B_1$ | $\{0,1\}$ twice, $\{1,2\}$, $\{2,0\}$ | $\{0, 1, 2\}$ | biconnected, with a parallel edge |
| $B_2$ | $\{2,3\}$ | $\{2, 3\}$ | bridge |
| $B_3$ | $\{3,4\}$, $\{4,5\}$, $\{5,3\}$ | $\{3, 4, 5\}$ | biconnected |
| $B_4$ | $\{5,6\}$ | $\{5, 6\}$ | bridge |
| $B_5$ | the loop at 6 | $\{6\}$ | loop |

The vertices in two or more blocks are 2 ($B_1$, $B_2$), 3 ($B_2$, $B_3$) and 5 ($B_3$, $B_4$): exactly the articulation points. The vertex 6 lies in $B_4$ and in the loop block $B_5$ but is not an articulation point, so fact 3 needs its condition "neither a loop". This is one reason why most texts and programs leave loops out of the problem.

More cases:

| graph | blocks |
|---|---|
| a tree with $n$ vertices | its $n - 1$ edges, one block each |
| a cycle, or a [complete graph](/complete-graph/) $K_n$ with $n \ge 3$ | one block with all edges |
| two triangles sharing the vertex 0 | two blocks, meeting at 0 |
| the path $0 - 1 - 2$ plus the edge $\{0, 2\}$ | one block: the three edges lie on one cycle |
| two vertices with three parallel edges | one block |
| a single vertex | no edge block; one trivial block in the vertex view |

**Non-example.** In the two triangles that share the vertex 0, the set of all six edges is connected and has no bridge, but it is not one block: an edge of the first triangle and an edge of the second lie on no common cycle, since such a cycle would pass through 0 twice.

## Known algorithms

| algorithm | time | remark |
|---|---|---|
| [Hopcroft-Tarjan biconnectivity](/hopcroft-tarjan-biconnectivity/) | $\Theta(n + m)$ | one depth-first search with [low-link](/low-link/) values and a stack of edges |
| [Gabow's path-based method](/gabow-path-based-scc/), biconnected version | $\Theta(n + m)$ | one search with stacks of the current path |
| Remove each vertex, then test which edges stay joined | $O(n(n + m))$ | brute force from fact 3 |

## Bounds

**Upper bound.** $O(n + m)$ time in the [word RAM](/word-ram/) model with adjacency lists, by the Hopcroft-Tarjan algorithm.

**Lower bound.** $\Omega(n + m)$ list entries must be read in the worst case by each deterministic algorithm. The articulation points follow from the blocks in $O(n + m)$ time (the vertices in two or more blocks that are not loops), and the [articulation point finding](/articulation-point-finding/) page proves the bound for that problem.

## Reductions

- **Articulation points from blocks.** Count the non-loop blocks at each vertex. A count of at least 2 marks an articulation point (fact 3). Cost $O(n + m)$.
- **Bridges from blocks.** A block with exactly one edge that is not a loop is a bridge.
- **Block-cut tree from blocks.** One node for each block and each articulation point, and an edge between a block and each articulation point in it. Cost $O(n + m)$.
- **Problems that split over blocks.** The number of [spanning trees](/counting-spanning-trees/) of a connected graph is the product of the numbers for the blocks, a graph is [planar](/planar-graph/) if and only if each block is, and the [chromatic number](/chromatic-number/) is the largest chromatic number of a block. In each case the problem reduces to its blocks in $O(n + m)$ time.

## Applications

- Find the parts of a network that survive the failure of any one node, and the nodes between them.
- Run [planarity testing](/planarity-testing/), [ear decomposition](/ear-decomposition/) or [st-numbering](/st-numbering/), which need a biconnected input, block by block.
- Answer "does every path from $u$ to $v$ pass through $x$?" for many queries with the [block-cut tree](/block-cut-tree/).

## References
