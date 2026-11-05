---
tag: YBGV0C
kind: theorem
slug: fary-theorem
name: Fáry's theorem
aliases:
- Fary's theorem
area: graphs/planar-graphs
level: intro
summary: Every simple planar graph has a planar drawing with straight-line edges.
prereqs: [planar-graph, planar-embedding, maximal-planar-graph]
see_also: [de-fraysseix-pach-pollack, planar-straight-line-drawing, schnyder-drawing, tutte-spring-theorem, canonical-ordering, graph-drawing, euler-formula, jordan-curve-theorem]
sources:
  - paper: "István Fáry, On straight line representation of planar graphs, Acta Scientiarum Mathematicarum (Szeged) 11, 229 to 233 (1948)"
    locator: the main theorem
  - paper: "Klaus Wagner, Bemerkungen zum Vierfarbenproblem, Jahresbericht der Deutschen Mathematiker-Vereinigung 46, 26 to 32 (1936)"
    locator: the straight-line drawing of maximal planar graphs
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 6.1, Embeddings and Euler's formula (Fáry's theorem and its proof)
  - paper: "S. K. Stein, Convex maps, Proceedings of the American Mathematical Society 2(3), 464 to 466 (1951)"
    locator: the straight-line theorem, found independently
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 4.2, Plane graphs (maximal plane graphs are triangulations)
  - paper: "Walter Schnyder, Embedding planar graphs on the grid, Proceedings of the First Annual ACM-SIAM Symposium on Discrete Algorithms (SODA 1990), 138 to 148"
    locator: the (n - 2) by (n - 2) grid drawing
  - paper: doi:10.1007/BF02122694
    title: Hubert de Fraysseix, János Pach and Richard Pollack, How to draw a planar graph on a grid, Combinatorica 10(1), 41 to 51 (1990)
    locator: the main theorem (straight-line drawing on a grid of size 2n - 4 by n - 2)
---

Fáry's theorem says that every simple [planar graph](/planar-graph/) can be drawn in the plane with each edge a straight line segment and no two edges crossing. More strongly, every plane embedding of a simple graph, given as a [rotation system](/rotation-system/) together with an outer face, can be realized by a straight-line drawing with the same cyclic orders and the same outer face. So for simple graphs, curved edges never help planarity, and an algorithm may always output points instead of curves. Wagner (1936), Fáry (1948) and Stein (1951) proved it independently.

## Statement

A **straight-line drawing** of a graph $G = (V, E)$ is a one-to-one map $p : V \to \mathbb{R}^2$ such that each edge $uv$ is drawn as the closed segment $[p(u), p(v)]$. It is **plane** when two segments meet only at a common end, and no segment contains the point of a vertex other than its two ends.

A **combinatorial embedding** of a connected graph is a rotation system (a cyclic order of the neighbours at each vertex) whose faces satisfy [Euler's formula](/euler-formula/) with $n - m + f = 2$, together with a choice of one face as the outer face.

**Theorem (Wagner 1936, Fáry 1948).** Let $G$ be a simple planar graph. Then $G$ has a plane straight-line drawing. Moreover, for every plane embedding of $G$ there is a plane straight-line drawing with the same rotation system and the same outer face.

The word *simple* is needed: two parallel edges between the same two vertices would be the same segment, and a loop cannot be a segment at all.

## In plain words

If you can draw a network on paper with curved lines and no crossings, then you can also draw it with a ruler. You may have to move the dots, but you never need to bend a line.

The proof first adds lines until every region is a triangle, because a full triangulation is the hardest case and removing lines later keeps a drawing valid. Then it shrinks the problem. Either a triangle of lines has dots both inside and outside it, and the two parts are drawn one after the other. Or two neighbouring dots can be merged into one. The smaller picture is drawn with a ruler, and the merged dot is split again into two dots very close together.

## Proof

**Step 1: reduction to maximal plane graphs.** A simple plane graph with $n \ge 3$ vertices to which no edge can be added in its faces without losing simplicity has every face bounded by a triangle (Diestel, Section 4.2; see [maximal planar graph](/maximal-planar-graph/)). So add edges inside faces, one at a time, until no edge can be added. This keeps the given faces subdivided, so the rotation system of $G$ is the restriction of the new one. A straight-line drawing of the new graph with its embedding gives one of $G$ by deleting the added segments. Graphs with $n \le 2$ are trivial. So it suffices to prove the following claim.

**Claim.** Let $G$ be a maximal plane graph with $n \ge 3$ vertices and outer triangle $abc$, and let $P_a, P_b, P_c$ be three points that are not on a line. Then $G$ has a plane straight-line drawing with the same faces, in which $a, b, c$ are at $P_a, P_b, P_c$ and all other vertices are inside the triangle $P_a P_b P_c$.

We prove the claim by induction on $n$. For $n = 3$ the graph is the triangle and the drawing is given. Let $n \ge 4$.

**Case A: $G$ has a separating triangle** $T = uvw$, a 3-cycle with vertices both inside and outside it. Let $G_{\mathrm{out}}$ be $G$ without the vertices inside $T$, and $G_{\mathrm{in}}$ the subgraph made of $T$ and the vertices and edges inside $T$. Both are maximal plane graphs with fewer than $n$ vertices, and $T$ is a face of $G_{\mathrm{out}}$ and the outer face of $G_{\mathrm{in}}$. By induction, draw $G_{\mathrm{out}}$ with $a, b, c$ at the given points. The face $T$ is drawn as a nondegenerate triangle, since its three segments are part of a plane drawing. By induction again, draw $G_{\mathrm{in}}$ with $u, v, w$ at their points in that drawing, with all inner vertices inside that triangle. The two drawings meet only in $T$, so their union is a plane straight-line drawing of $G$ with the same faces.

**Case B: $G$ has no separating triangle.** Since $n \ge 4$, there is a vertex $x \notin \{a, b, c\}$. Let $y$ be any neighbour of $x$. The edge $xy$ lies on two faces $xyp$ and $xyq$. A third common neighbour $z$ of $x$ and $y$ would make $xyz$ a separating triangle, so $p$ and $q$ are the only common neighbours. Contract $xy$ into the vertex $y$. The faces $xyp$ and $xyq$ disappear, the edges $xp, xq$ merge with $yp, yq$, and the result $G'$ is a simple maximal plane graph with $n - 1$ vertices and the same outer triangle, because $x$ was not on it. By induction, $G'$ has a straight-line drawing with $a, b, c$ at the given points.

In the rotation of $x$ in $G$, the neighbours are $y, p, x_1, \ldots, x_k, q$ for some $k \ge 0$, so in $G'$ the neighbours of $y$ around $y$ are $p, x_1, \ldots, x_k, q$ and then the other neighbours of $y$. Let $A$ be the polygon $y, p, x_1, \ldots, x_k, q$. It is the union of the triangles $y p x_1, y x_1 x_2, \ldots, y x_k q$ (or of the one triangle $ypq$ when $k = 0$), which are faces of the drawing of $G'$. So $A$ is a simple polygon, and $y$ sees every vertex of $A$ along a segment inside $A$.

Now find a point $X$ in the interior of the kernel of $A$, the set of points that lie strictly on the inner side of the line of every edge of $A$. The edges of $A$ that do not contain $y$ are edges of triangle faces with apex $y$, so $y$ is strictly on their inner side, and so is every point of a small disk $D$ around $y$. The two edges $yp$ and $yq$ pass through $y$. The set of points strictly on the inner side of both lines is an open cone with apex $y$; it is not empty, because the two inner half-planes are not opposite (the interior of $A$ near $y$ meets both). Take $X$ in this cone and in $D$. Then $X$ is strictly on the inner side of every edge line of $A$. From such a point, each ray meets the boundary of $A$ exactly once, so the segments from $X$ to the vertices of $A$ lie inside $A$, meet its boundary only at their ends, and meet each other only at $X$.

Draw $G$ as the drawing of $G'$ with $x$ placed at $X$: the segments from $X$ go to $y, p, x_1, \ldots, x_k, q$, and the segments $y x_i$ of $G'$ are removed. Inside $A$, the new segments are the fan from $X$, which is plane by the previous paragraph. Outside $A$ nothing changes. The faces around $X$ are $X y p$, $X p x_1, \ldots, X x_k q$ and $X q y$, the faces of $G$ at $x$, in the same cyclic order. So this is a plane straight-line drawing of $G$ with the same faces. This proves the claim and the theorem. $\blacksquare$

The proof is constructive, but the points can need exponentially many digits. The [de Fraysseix-Pach-Pollack algorithm](/de-fraysseix-pach-pollack/) gives a different, constructive proof with integer coordinates.

## Consequences

- **Grid drawings.** Every simple planar graph with $n \ge 3$ vertices has a straight-line drawing with integer coordinates on a grid of size $(2n - 4) \times (n - 2)$, by the [shift method](/de-fraysseix-pach-pollack/), or $(n - 2) \times (n - 2)$ by [Schnyder's method](/schnyder-drawing/). These are the standard ways to compute a [planar straight-line drawing](/planar-straight-line-drawing/).
- **Output format of drawing algorithms.** [Graph drawing](/graph-drawing/) software may output only vertex positions for a planar input and draw edges as segments.
- **Convex drawings.** For 3-connected planar graphs Tutte proved a stronger statement: the drawing can have all faces convex, and it is found by solving a linear system ([Tutte's spring theorem](/tutte-spring-theorem/)).
- **Crossing number.** The [crossing number](/crossing-number/) of a graph is at most its rectilinear crossing number, and they agree at 0 by this theorem; they differ for some graphs with crossings, for example $K_8$ (crossing number 18, rectilinear crossing number 19).

## Tightness

- **Simplicity is needed.** The multigraph with two vertices and two parallel edges is planar, but it has no straight-line drawing, since both edges would be the same segment.
- **The embedding is kept, but not the metric.** The theorem says nothing about angles, lengths or area. Grid drawings reach area $O(n^2)$, and this is optimal up to a constant factor: the nested triangles graph (a chain of $n/3$ triangles, each inside the next and joined to it) needs a grid with both sides of order $n$, as de Fraysseix, Pach and Pollack observe.

Small cases, each drawn with integer points:

| graph | points | edges |
|---|---|---|
| a single vertex | $(0, 0)$ | none |
| a path $a b c$ (a tree) | $(0,0), (1,0), (2,1)$ | 2 segments |
| $K_4$ | $(0,0), (4,0), (2,3), (2,1)$ | 6 segments, 4 triangular faces |
| octahedron $K_{2,2,2}$ | $(0,0), (6,0), (3,6)$ outside; $(2,2), (3,1), (4,2)$ inside | 12 segments, 8 triangular faces |
| $K_5$, $K_{3,3}$ | none | not planar, so no plane drawing of any kind |

In the octahedron row, the inner vertex at $(4, 2)$ is opposite the outer vertex $(0,0)$, the one at $(2,2)$ is opposite $(6,0)$, and the one at $(3,1)$ is opposite $(3,6)$; each vertex is joined to the four vertices other than itself and its opposite.

## History

Wagner proved in 1936 that every maximal planar graph has a straight-line drawing, as a remark in a paper on the four color problem. Fáry published the theorem in 1948, and Stein found it independently in 1951. The induction with the contraction of an edge is the usual textbook proof (West, Section 6.1). In 1990 de Fraysseix, Pach and Pollack showed that a grid of size $(2n-4) \times (n-2)$ suffices and that it can be computed fast; Schnyder found an $(n-2) \times (n-2)$ grid the same year.

## References
