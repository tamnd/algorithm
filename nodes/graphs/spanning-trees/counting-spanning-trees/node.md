---
tag: YR08FJ
kind: problem
slug: counting-spanning-trees
name: Counting spanning trees problem
aliases:
- spanning tree counting
area: graphs/spanning-trees
level: advanced
summary: Count the spanning trees of a given graph, solvable via a determinant.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(n^3)}
prereqs: [spanning-tree, matrix-tree-theorem, determinant, laplacian-matrix]
see_also: [cayley-formula, spanning-tree-enumeration, uniform-spanning-tree-sampling, mst-uniqueness, gabow-myers-enumeration, hamiltonian-path-problem, prufer-sequence, multigraph]
sources:
  - book: isbn:9780521560696
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 2, Cambridge University Press (1999)
    locator: Section 5.6, Oriented trees and the Matrix-Tree Theorem
  - book: isbn:9780387952208
    title: Chris Godsil and Gordon Royle, Algebraic Graph Theory, Springer Graduate Texts in Mathematics 207 (2001)
    locator: Chapter 13, The Laplacian of a Graph
  - paper: doi:10.1002/andp.18471481202
    title: "Gustav Kirchhoff, Ueber die Auflösung der Gleichungen, auf welche man bei der Untersuchung der linearen Vertheilung galvanischer Ströme geführt wird, Annalen der Physik und Chemie 72 (1847), 497-508"
    locator: the whole paper
  - paper: doi:10.1017/S0305004100068936
    title: "François Jaeger, Dirk L. Vertigan and Dominic J. A. Welsh, On the computational complexity of the Jones and Tutte polynomials, Mathematical Proceedings of the Cambridge Philosophical Society 108 (1990), 35-53"
    locator: "the main theorem on the points of the Tutte plane at which evaluation is easy or #P-hard"
---

The counting spanning trees problem asks for the number $\tau(G)$ of [spanning trees](/spanning-tree/) of an undirected graph $G$. The number can be as large as $n^{n-2}$, so listing the trees is not an option for large graphs, but [Kirchhoff's matrix-tree theorem](/matrix-tree-theorem/) gives $\tau(G)$ as one [determinant](/determinant/) of a reduced [Laplacian matrix](/laplacian-matrix/). The problem is therefore solved in $O(n^3)$ arithmetic operations by Gaussian elimination, or in the time of matrix multiplication. Close relatives are harder: counting all spanning forests, or the spanning trees with at most two edges at each vertex (Hamiltonian paths), is #P-hard.

## In plain words

You have a network and you want to know in how many different ways you can choose links that connect all points with no loop. Even small networks have many such choices, and large ones have far more than any computer could list.

There is a shortcut. Write the network as a square table of numbers: how many links each point has, and minus the number of links between each two points. Remove one row and the matching column. One standard calculation on the table, its determinant, gives the exact number of choices.

The same idea counts weighted choices and one-way networks. Small changes to the question, such as asking for trees in which each point has at most two links, make it very hard.

## Definition

**Input.** An undirected multigraph $G = (V, E)$ with $n$ vertices and $m$ edges. Parallel edges are allowed and count as different edges; self-loops are allowed and are in no spanning tree.

**Output.** The number $\tau(G)$ of edge sets $T \subseteq E$ such that $(V, T)$ is a tree.

**Disconnected graphs.** If $G$ is not connected, $\tau(G) = 0$. The number of spanning *forests* with the same components as $G$, a [spanning forest](/spanning-forest/) count, is then the product of $\tau$ over the components.

**Edge weights and ties.** The plain problem ignores weights. With weights, two counts are common: the weighted sum $\sum_T \prod_{e \in T} x_e$, and the number of *minimum* spanning trees, which is 1 when all weights are distinct and can be large when weights tie.

**Size of the answer.** $\tau(G) \le n^{n-2}$ for a simple graph, so the answer has $O(n \log n)$ bits.

## Variants

- **Weighted count.** $\sum_T \prod_{e \in T} x_e$ for edge weights $x_e$. The matrix-tree theorem with the weighted Laplacian gives it as one determinant.
- **Directed graphs.** The number of spanning arborescences rooted at $r$ is a cofactor of the in-degree Laplacian, by Tutte's form of the theorem.
- **Counting minimum spanning trees.** Sort the distinct weights $w_1 < w_2 < \dots$. For each $w_k$, let $H_k$ be the multigraph whose vertices are the components of the edges of weight less than $w_k$, and whose edges are the edges of weight $w_k$, with self-loops removed. The number of minimum spanning trees is $\prod_k \prod_{K} \tau(K)$, over the components $K$ of each $H_k$. This works because each minimum spanning tree meets the edges of weight $w_k$ in a spanning forest of $H_k$, and every such choice can be combined with every other.
- **Counting spanning forests.** The number of all forests, or of all connected spanning subgraphs, is an evaluation of the Tutte polynomial, $T(2, 1)$ and $T(1, 2)$. Both are #P-hard in general (Jaeger, Vertigan and Welsh, 1990), while $\tau(G) = T(1, 1)$ is easy.
- **Spanning trees with a degree bound.** Counting spanning trees of maximum degree 2, which are Hamiltonian paths, is #P-hard.

## Examples

| graph | $\tau$ | how |
|---|---|---|
| $K_n$ | $n^{n-2}$ | [Cayley's formula](/cayley-formula/); $\tau(K_5) = 125$ |
| cycle $C_n$ | $n$ | remove any one of the $n$ edges |
| tree | 1 | the tree itself |
| $K_{a,b}$ | $a^{b-1} b^{a-1}$ | eigenvalues of the Laplacian; $\tau(K_{2,3}) = 12$ |
| $3 \times 3$ grid | 192 | determinant of an $8 \times 8$ cofactor |
| two vertices, $k$ parallel edges | $k$ | each edge is a tree |

**A graph with six vertices.** Take the vertices $a$ to $f$ and the edges $ab$, $ac$, $bc$, $bd$, $cd$, $ce$, $de$, $df$, $ef$. Each cofactor of its Laplacian is 55, so it has 55 spanning trees among the $\binom{9}{5} = 126$ sets of five edges. With the weights $ab = 4$, $ac = 3$, $bc = 1$, $bd = 2$, $cd = 4$, $ce = 5$, $de = 7$, $df = 6$, $ef = 2$, it has one minimum spanning tree, since the weights that tie ($ab$ and $cd$ at 4, $bd$ and $ef$ at 2) do not create a choice: in the formula above, every graph $H_k$ is a forest.

**Ties.** In a triangle with three edges of weight 1, there is one weight class, $H_1$ is the triangle, and the formula gives $\tau(H_1) = 3$ minimum spanning trees.

## Known algorithms

- **Determinant.** Build the Laplacian $L$, delete one row and the matching column, and compute the determinant. Gaussian elimination takes $O(n^3)$ arithmetic operations. With integers, use fraction-free (Bareiss) elimination, whose intermediate values are minors of the matrix and so have $O(n \log n)$ bits, or compute the determinant modulo several primes and combine them by the Chinese remainder theorem. Fast matrix multiplication gives $O(n^{\omega})$ arithmetic operations.
- **Eigenvalues.** $\tau(G) = \frac{1}{n} \mu_2 \cdots \mu_n$, where the $\mu_k$ are the nonzero Laplacian eigenvalues. This is useful for families with known spectra, but in floating point it gives only an approximation.
- **Deletion and contraction.** $\tau(G) = \tau(G - e) + \tau(G / e)$. The recursion takes exponential time in general. On series-parallel graphs, a weighted form of it, which replaces two parallel edges or two edges in series by one weighted edge, takes linear time.
- **Enumeration.** Algorithms for [spanning tree enumeration](/spanning-tree-enumeration/), such as [Gabow and Myers'](/gabow-myers-enumeration/), list all trees in time proportional to their number, so they count in $\Omega(\tau(G))$ time. Use them only when the trees themselves are needed.

## Bounds

- **Upper bound.** $O(n^3)$ arithmetic operations, or $O(n^{\omega})$ with fast matrix multiplication; with exact integers, a polynomial number of bit operations.
- **The answer can be large.** For $K_n$ the answer has about $(n - 2) \log_2 n$ bits, so any algorithm that writes it needs $\Omega(n \log n)$ bit operations.
- **A bound on the count.** For a connected graph with $n$ vertices and $m$ edges, the arithmetic and geometric mean inequality on the nonzero eigenvalues, whose sum is $\operatorname{tr} L = 2m$, gives
$$\tau(G) \le \frac{1}{n} \left( \frac{2m}{n - 1} \right)^{n - 1},$$
with equality for $K_n$. For the six-vertex example above, the bound is $\frac{1}{6} (18/5)^5 \approx 100.8$, against the true value 55.

## Reductions

- **To a determinant.** The matrix-tree theorem reduces counting to one determinant of an $(n - 1) \times (n - 1)$ integer matrix, in $O(n + m)$ time to build the matrix.
- **Counting minimum spanning trees to counting spanning trees,** one count for each component of each weight class, as in the variant above.
- **Uniform sampling.** Counting gives exact sampling of a uniform spanning tree: decide the edges one at a time, keeping $e$ with probability $\tau(G / e) / \tau(G)$, and then contract $e$ or delete it. Random-walk methods, such as [Aldous-Broder](/aldous-broder/) and [Wilson's algorithm](/wilson-algorithm/), avoid the determinants; see [uniform spanning tree sampling](/uniform-spanning-tree-sampling/).

## Applications

- **Electrical networks.** Kirchhoff's analysis expresses the currents and the effective resistances of a resistor network by sums over spanning trees. The effective resistance between the ends of an edge $e$ equals $\tau(G / e) / \tau(G)$ for unit resistors.
- **Network reliability.** The number of spanning trees is a common measure of how well a network survives link failures: a graph with more spanning trees has more ways to stay connected.
- **Chemistry and physics.** The count is used as a measure of the complexity of a molecule, and the asymptotic count on lattices is studied in statistical physics as the entropy of spanning trees.
- **Uniqueness tests.** The count of minimum spanning trees answers whether the MST is unique; see [MST uniqueness](/mst-uniqueness/).

## References
