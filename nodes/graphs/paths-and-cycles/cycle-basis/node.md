---
tag: 8Q0TKW
kind: concept
slug: cycle-basis
name: Cycle basis
aliases:
- cycle space basis
- fundamental cycles
area: graphs/paths-and-cycles
level: advanced
summary: A set of cycles that forms a basis of the cycle space over GF(2); it has m - n + c cycles, and the fundamental cycles of a spanning forest form one.
prereqs: [fundamental-cycle, spanning-tree, eulerian-graph]
see_also: [graphic-matroid, gaussian-elimination, bitset-gaussian-elimination, minimum-spanning-tree, girth, electrical-flow, dfs-cycle-detection, spanning-forest]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer
    locator: Section 1.9, Some linear algebra (the edge space, the cycle space and the cut space, their dimensions, and fundamental cycles)
  - book: isbn:9781846289699
    title: J. A. Bondy and U. S. R. Murty, Graph Theory, Graduate Texts in Mathematics 244, Springer (2008)
    locator: Section 2.6, Cycle space and bond space
  - paper: doi:10.1137/0216026
    title: J. D. Horton, A polynomial-time algorithm to find the shortest cycle basis of a graph, SIAM Journal on Computing 16(2), 358 to 366 (1987)
    locator: the whole paper (a minimum cycle basis can be chosen from a polynomial set of candidate cycles)
  - paper: doi:10.1016/j.cosrev.2009.08.001
    title: Telikepalli Kavitha, Christian Liebchen, Kurt Mehlhorn, Dimitrios Michail, Romeo Rizzi, Torsten Ueckerdt and Katharina A. Zweig, Cycle bases in graphs, characterization, algorithms, complexity, and applications, Computer Science Review 3(4), 199 to 243 (2009)
    locator: the whole survey (classes of cycle bases, minimum cycle basis algorithms, directed cycle bases)
---

A cycle basis of a [graph](/graph/) is a set of cycles such that every *even subgraph*, a set of edges in which every vertex has even degree, is the sum of a unique subset of them, where the sum of edge sets is the symmetric difference. The even subgraphs form a vector space over the field with two elements, the *cycle space*, and a cycle basis is a basis of it. Every cycle basis of a graph with $n$ vertices, $m$ edges and $c$ components has exactly $m - n + c$ cycles. The [fundamental cycles](/fundamental-cycle/) of any [spanning forest](/spanning-forest/) form one, and it can be found in linear time; a basis of least total length, a minimum cycle basis, needs more work but is still found in polynomial time.

## In plain words

A graph can have a huge number of cycles, but they are built from a small set. Take a set of edges and add another set by keeping the edges that are in exactly one of the two. With this kind of adding, every cycle, and every way of combining cycles, can be made from a fixed small list of cycles. Such a list is a cycle basis.

The size of the list is always the same: the number of edges, minus the number of points, plus the number of separate pieces of the graph. One easy way to get a list: pick a tree that connects everything, and for each edge outside the tree take the cycle that this edge closes with the tree.

## The idea

**The edge space.** Identify a set of edges $F \subseteq E$ with its indicator vector in $\mathrm{GF}(2)^E$. Addition is symmetric difference: $F_1 + F_2 = F_1 \triangle F_2$. The *cycle space* $\mathcal{C}(G)$ is the set of $F$ in which every vertex has even degree. It is a subspace, because the degree of $v$ in $F_1 \triangle F_2$ has the parity of $d_{F_1}(v) + d_{F_2}(v)$. Every cycle is in $\mathcal{C}(G)$, and every nonempty element of $\mathcal{C}(G)$ is an edge-disjoint union of cycles: the even subgraphs of the [Eulerian graph](/eulerian-graph/) page.

**Directed and multigraphs.** The definition ignores directions: in a directed graph, the cycle space is that of the underlying undirected multigraph, and its cycles need not be directed cycles. A self-loop is a cycle of length 1 and two parallel edges form a cycle of length 2, so each loop and each extra parallel edge adds 1 to the dimension. (For directed graphs there is also a cycle space over $\mathbb{Q}$, with signed cycle vectors; it has the same dimension, and its bases are called directed cycle bases.)

**Dimension.** Let $F$ be a spanning forest of $G$, with $n - c$ edges. For each edge $e \notin F$, the forest plus $e$ contains exactly one cycle $C_e$, the fundamental cycle of $e$.

*Claim.* The $m - n + c$ fundamental cycles form a basis of $\mathcal{C}(G)$.

*Proof.* Independence: $C_e$ contains $e$ and no other edge outside $F$, so in a sum of some $C_e$ each chosen $e$ appears exactly once, and a nonempty sum is not $\emptyset$. Spanning: for $Z \in \mathcal{C}(G)$, let $Z' = Z + \sum_{e \in Z \setminus F} C_e$. Then $Z'$ is in $\mathcal{C}(G)$ and has no edge outside $F$, so it is an even subgraph of a forest. A nonempty forest has a vertex of degree 1, so $Z' = \emptyset$ and $Z = \sum_{e \in Z \setminus F} C_e$. $\square$

So $\dim \mathcal{C}(G) = m - n + c$, the *cyclomatic number* or circuit rank, and $|\mathcal{C}(G)| = 2^{m - n + c}$. A graph is a forest if and only if the dimension is 0.

**The cut space.** The orthogonal complement of $\mathcal{C}(G)$ in $\mathrm{GF}(2)^E$ is the cut space, spanned by the edge cuts $\delta(S)$, of dimension $n - c$. An edge set is in the cycle space if and only if it meets every cut in an even number of edges.

**Kinds of cycle bases.** Fundamental bases come from spanning trees. Every fundamental basis is a cycle basis, but not every cycle basis is fundamental. Some applications need *weakly fundamental* or *integral* bases, which sit between the two; the survey of Kavitha and others describes the hierarchy.

**Minimum cycle basis.** With nonnegative edge weights, the weight of a basis is the total weight of its cycles. The cycles of $\mathcal{C}(G)$ form the circuits of a matroid on the vectors, so a greedy algorithm that adds the shortest cycle independent of those already chosen gives a minimum basis. Horton (1987) proved that a minimum basis can be chosen among $O(mn)$ candidate cycles, each formed by a vertex $x$, an edge $uv$, and shortest paths from $x$ to $u$ and to $v$, which made the greedy method polynomial. Independence is tested by [Gaussian elimination](/gaussian-elimination/) over $\mathrm{GF}(2)$, often with [bitsets](/bitset-gaussian-elimination/). Later algorithms, surveyed by Kavitha and others, reduce the time further. By contrast, finding a minimum *fundamental* cycle basis is NP-hard.

## Examples

**$K_4$.** $n = 4$, $m = 6$, $c = 1$, so the dimension is 3 and the cycle space has $2^3 = 8$ elements: $\emptyset$, the 4 triangles and the 3 four-cycles. With unit weights:

| spanning tree | fundamental cycles | weight |
|---|---|---|
| the star at 0: $01, 02, 03$ | triangles $012$, $013$, $023$ | 9 |
| the path $0, 1, 2, 3$ | triangles $012$, $123$, and the 4-cycle $0123$ | 10 |

The first is a minimum cycle basis. Any 3 of the 4 triangles form a basis, since the only relation among the triangles is that all four sum to $\emptyset$ (each edge is in exactly two triangles).

**A tree and isolated vertices.** A tree has $m = n - 1$, so the dimension is 0 and the empty set is the only basis. Isolated vertices add 1 to both $n$ and $c$ and do not change the dimension.

**Loops and parallel edges.** One vertex with two self-loops has the basis of the two loops, dimension $2 - 1 + 1 = 2$. Two vertices joined by three parallel edges $a, b, c$ have dimension $3 - 2 + 1 = 2$; with $a$ as the tree, the fundamental cycles are $\{a, b\}$ and $\{a, c\}$, and their sum $\{b, c\}$ is the third 2-cycle.

**Petersen graph.** $m - n + c = 15 - 10 + 1 = 6$. Its [girth](/girth/) is 5, so every basis has weight at least $6 \cdot 5 = 30$; there are 12 five-cycles, and 6 of them can be chosen independent, so the minimum cycle basis has weight 30.

**A directed graph.** The arcs $0 \to 1$, $1 \to 2$ and $0 \to 2$ have no directed cycle, but the cycle space of the underlying graph has dimension 1, spanned by the triangle.

## Where it is used

- **Electrical networks.** Kirchhoff's voltage law is one equation for each cycle of a basis; the $m - n + c$ fundamental cycles give a complete independent set of equations for the [current](/electrical-flow/) in a network. This is where cycle bases began, with Kirchhoff in 1847.
- **Chemistry.** Ring perception in molecules uses a minimum cycle basis, the "smallest set of smallest rings".
- **Periodic scheduling and timetabling.** Integral cycle bases give compact formulations of periodic event scheduling problems.
- **Structural analysis and surface reconstruction.** The cycles of a short basis serve as the elementary loops of frames and meshes.
- **Algorithms.** The rank of the cycle space tells whether a graph is a forest; parity questions on cycles, such as whether every cycle is even, are linear algebra over $\mathrm{GF}(2)$ on a basis. [DFS cycle detection](/dfs-cycle-detection/) with all back edges recorded produces a fundamental basis of the DFS tree.

## References
