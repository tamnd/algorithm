---
tag: EQC8ZX
kind: concept
slug: schnyder-woods
name: Schnyder woods
aliases:
- Schnyder's orientation
area: graphs/planar-graphs
level: advanced
summary: Three-coloring of the edges of a triangulation, giving a dimension characterization of planar graphs.
prereqs: [maximal-planar-graph, rotation-system, tree]
see_also: [schnyder-drawing, canonical-ordering, de-fraysseix-pach-pollack, planar-straight-line-drawing, planar-face, euler-formula, planar-embedding, topological-sort]
sources:
  - paper: doi:10.1007/BF00353652
    title: Walter Schnyder, Planar graphs and poset dimension, Order 5(4), 323 to 343 (1989)
    locator: the definition of normal labelings and realizers, the three trees and their paths, and the theorem that a graph is planar if and only if its incidence order has dimension at most 3
  - paper: "Walter Schnyder, Embedding planar graphs on the grid, Proceedings of the First Annual ACM-SIAM Symposium on Discrete Algorithms (SODA 1990), 138 to 148"
    locator: the regions of a vertex, the barycentric coordinates by region counts and the linear-time construction
  - paper: "Hubert de Fraysseix and Patrice Ossona de Mendez, On topological aspects of orientations, Discrete Mathematics 229, 57 to 72 (2001)"
    locator: the bijection between Schnyder woods of a triangulation and its orientations with out-degree 3 at every inner vertex
  - paper: "Stefan Felsner, Lattice structures from planar graphs, Electronic Journal of Combinatorics 11(1), R15 (2004)"
    locator: the distributive lattice on the Schnyder woods of a plane triangulation
---

A Schnyder wood of a plane triangulation colours each inner edge with one of three colours and orients it, so that every inner vertex has exactly one outgoing edge of each colour, arranged around the vertex by a fixed local rule. The edges of each colour then form a spanning [tree](/tree/) of the inner vertices, rooted at one of the three outer vertices. Walter Schnyder introduced these structures in 1989, as *realizers*, to prove that a graph is planar exactly when its incidence order has dimension at most 3. They also give the [Schnyder drawing](/schnyder-drawing/) of a planar graph on an $(n - 2) \times (n - 2)$ grid.

## In plain words

Take a [maximal planar graph](/maximal-planar-graph/), a network in which every region is a triangle, and name the three corners of the outside triangle 1, 2 and 3. Every other node gets three arrows, one pointing toward each corner, and each arrow is an edge of the network. Following arrows of colour 1 from any node always leads to corner 1, without loops.

The rule that makes this work is about the order around a node: the three arrows leave in the order 1, 2, 3 counterclockwise, and arrows of a colour arrive only in the gap opposite their own outgoing arrow. Because of this rule, the three paths from a node to the corners never meet again, and they cut the big triangle into three slices.

## The idea

**How the embedding is given.** A plane triangulation with $n \ge 3$ vertices is given by a [rotation system](/rotation-system/) $\rho$ in which every [face](/planar-face/) is a triangle, together with one face $a_1, a_2, a_3$ chosen as the outer face and listed counterclockwise. All other vertices are *inner*, and the *inner edges* are all edges except the three outer ones.

**Definition.** A Schnyder wood assigns each inner edge one direction and one colour in $\{1, 2, 3\}$ such that:

1. every inner vertex has exactly one outgoing edge of each colour;
2. counterclockwise around each inner vertex come: the outgoing edge of colour 1, the incoming edges of colour 3, the outgoing edge of colour 2, the incoming edges of colour 1, the outgoing edge of colour 3, the incoming edges of colour 2 (each group of incoming edges may be empty);
3. every inner edge at $a_i$ is incoming at $a_i$ and has colour $i$.

**Edge count.** A triangulation has $3n - 6$ edges, so $3n - 9 = 3(n - 3)$ inner edges, exactly one outgoing edge per colour for each of the $n - 3$ inner vertices. So condition 1 already says that every inner edge leaves exactly one inner vertex.

**Three trees.** Let $T_i$ be the edges of colour $i$. Following the outgoing edge of colour $i$ from an inner vertex never repeats a vertex and ends at $a_i$, so $T_i$ is a spanning tree of the inner vertices plus $a_i$, rooted at $a_i$. Write $P_i(v)$ for the path from $v$ to $a_i$ in $T_i$.

**Three paths, three regions.** The key property is that $P_1(v)$, $P_2(v)$ and $P_3(v)$ meet only in $v$. Together with the outer edges they cut the outer triangle into three regions: $R_i(v)$ is bounded by $P_{i+1}(v)$, $P_{i-1}(v)$ and the outer edge $a_{i+1} a_{i-1}$ (indices mod 3), and lies opposite the corner $a_i$. A second property makes the regions nest: if $u$ lies in $R_i(v)$, then $R_i(u) \subseteq R_i(v)$, because a path of colour $i \pm 1$ that starts inside $R_i(v)$ cannot cross its boundary. The rule of condition 2 guarantees this: at a vertex of the boundary path of colour $i - 1$, all incoming edges of colour $i + 1$ arrive from outside the region.

**Existence.** Every plane triangulation has a Schnyder wood. One construction uses a [canonical ordering](/canonical-ordering/) $v_1 = a_1$, $v_2 = a_2$, $\ldots$, $v_n = a_3$, in which each $v_k$ is added above the current boundary path and is adjacent to a contiguous part $c_l, \ldots, c_r$ of it. Orient $v_k c_l$ out of $v_k$ with colour 1, $v_k c_r$ out of $v_k$ with colour 2, and every edge $c_j v_k$ with $l < j < r$ into $v_k$ with colour 3. This takes linear time; the [Schnyder drawing](/schnyder-drawing/) page builds the canonical ordering by peeling vertices off the outer path.

**Orientations determine the wood.** An orientation of the inner edges with out-degree exactly 3 at each inner vertex and out-degree 0 at the outer vertices, a *3-orientation*, has exactly one colouring that makes it a Schnyder wood (de Fraysseix and Ossona de Mendez). So Schnyder woods and 3-orientations are in bijection.

**Many woods, one lattice.** A triangulation usually has many Schnyder woods. Reversing a directed cycle of a 3-orientation keeps every out-degree, so it maps one wood to another. Felsner showed that, ordered by such reversals of counterclockwise cycles, the Schnyder woods of a triangulation form a distributive lattice.

**Dimension.** The three trees define three linear orders of the vertices: for colour $i$, a linear extension of the order in which $u$ comes before $v$ when $u$ lies in $R_i(v)$. Schnyder used them to show that the vertex-edge incidence order of a planar graph has dimension at most 3; with the converse, a graph is planar if and only if this dimension is at most 3.

## Examples

**$K_4$.** With outer face $a_1, a_2, a_3$ and inner vertex $v$, the only Schnyder wood orients $v \to a_i$ with colour $i$. Counterclockwise around $v$, the three outgoing edges are in the order 1, 2, 3, as condition 2 requires. In the Schnyder drawing, $v$ gets coordinates $(1, 1, 1)$.

**The octahedron.** Take outer face $0, 1, 2$ and inner vertices $3, 4, 5$, where $3$ is not adjacent to $1$, $4$ not to $2$, and $5$ not to $0$. Counterclockwise rotations: $\rho(3) = (0, 4, 5, 2)$, $\rho(4) = (0, 1, 5, 3)$, $\rho(5) = (4, 1, 2, 3)$. One Schnyder wood is

| colour | edges | tree |
|---|---|---|
| 1 | $3 \to 0$, $4 \to 0$, $5 \to 3$ | rooted at 0 |
| 2 | $3 \to 4$, $4 \to 1$, $5 \to 1$ | rooted at 1 |
| 3 | $3 \to 2$, $5 \to 2$, $4 \to 5$ | rooted at 2 |

At vertex 3, counterclockwise from $0$: out 1 to 0, out 2 to 4, in 1 from 5, out 3 to 2, which fits the rule. The inner triangle is the directed cycle $5 \to 3 \to 4 \to 5$. Reversing it gives a second 3-orientation, and a brute-force count over all $2^9$ orientations of the 9 inner edges confirms that these are the only two: the octahedron has exactly 2 Schnyder woods.

**Paths and regions.** In the wood above, $P_1(5) = 5, 3, 0$, $P_2(5) = 5, 1$ and $P_3(5) = 5, 2$ meet only at 5. The region $R_3(5)$, bounded by $P_1(5)$, $P_2(5)$ and the edge $0\text{-}1$, contains the vertices $5, 3, 0, 1$ and, inside, vertex 4. Its subregion $R_3(4)$, bounded by $P_1(4) = 4, 0$ and $P_2(4) = 4, 1$, is the triangle $4, 0, 1$, which nests inside $R_3(5)$.

**Not triangulations.** A single vertex, a tree, or any graph with a face of length at least 4 has no Schnyder wood in this sense; one first adds edges until every face is a triangle, as the Schnyder drawing algorithm does, or uses the extension of Schnyder woods to 3-connected plane graphs, in which some edges get two colours. $K_5$ and $K_{3,3}$ are not planar, so they have no plane embedding and no Schnyder wood; by Schnyder's theorem their incidence orders have dimension at least 4.

## Where it is used

- **Grid drawings.** Counting vertices in the three regions of each vertex gives barycentric coordinates and the planar straight-line drawing on the $(n - 2) \times (n - 2)$ grid of the [Schnyder drawing](/schnyder-drawing/) algorithm. It is one of the two classic answers to the [planar straight-line drawing](/planar-straight-line-drawing/) problem, the other being the [de Fraysseix-Pach-Pollack](/de-fraysseix-pach-pollack/) shift method.
- **Order dimension.** Schnyder's theorem characterizes planarity by the dimension of the incidence order and started a line of work on the dimension of orders built from planar maps.
- **Encoding and counting.** The trees of a Schnyder wood give compact encodings of planar triangulations and bijections used to count them.
- **Other drawing styles.** Schnyder woods lead to representations by touching triangles and to visibility and orthogonal drawings.

## References
