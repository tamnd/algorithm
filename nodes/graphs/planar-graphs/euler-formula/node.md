---
tag: 8FJ58P
kind: theorem
slug: euler-formula
name: Euler's formula for planar graphs
aliases:
- Euler's polyhedron formula
- V - E + F = 2
area: graphs/planar-graphs
level: intro
summary: For a connected plane graph, V - E + F = 2.
prereqs: [planar-graph, connected-graph, tree]
see_also: [planar-edge-bound, planar-face, planar-dual-graph, rotation-system, jordan-curve-theorem, graph-genus, five-color-theorem, kuratowski-theorem]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 4.2, Plane graphs (Euler's formula and the corollary on the number of edges)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 6.1, Embeddings and Euler's formula
  - book: isbn:9781846289699
    title: J. A. Bondy and U. S. R. Murty, Graph Theory, Graduate Texts in Mathematics 244, Springer, 2008
    locator: Chapter 10, Planar graphs (the section on Euler's formula)
  - book: isbn:9783662572641
    title: Martin Aigner and Günter M. Ziegler, Proofs from THE BOOK, sixth edition, Springer, 2018
    locator: the chapter Three applications of Euler's formula
  - paper: "Leonhard Euler, Elementa doctrinae solidorum, Novi Commentarii Academiae Scientiarum Petropolitanae 4 (1752/53), published 1758"
    locator: the relation between the numbers of vertices, edges and faces of a polyhedron
---

Euler's formula says that a connected [plane graph](/planar-graph/) with $n$ vertices, $m$ edges and $f$ [faces](/planar-face/) satisfies $n - m + f = 2$. The number of faces therefore does not depend on the drawing: every planar drawing of the same connected graph has $m - n + 2$ faces. The formula is the source of almost every counting fact about planar graphs, such as the [edge bound](/planar-edge-bound/) $m \le 3n - 6$, the existence of a vertex of degree at most 5, and the non-planarity of $K_5$ and $K_{3,3}$.

## Statement

A **plane graph** is a finite graph $G = (V, E)$ together with a drawing in $\mathbb{R}^2$: each vertex is a distinct point, each edge is a simple arc (a homeomorphic image of $[0,1]$) between its two ends, and two arcs meet only at common ends. The **faces** of $G$ are the connected components (regions) of $\mathbb{R}^2$ minus the points and arcs of the drawing. Exactly one face is unbounded; it is the outer face.

The same data can be given without coordinates, by a [rotation system](/rotation-system/): for each vertex, the cyclic order of its neighbours around it. A face is then an orbit of the map that sends the dart $(u, v)$ to $(v, w)$, where $w$ is the neighbour that comes just before $u$ in the cyclic order at $v$. A rotation system that comes from a plane drawing has the same faces as the drawing. This page states the formula for drawings; the combinatorial form is in the consequences.

**Theorem (Euler).** Let $G$ be a connected plane graph with $n \ge 1$ vertices, $m$ edges and $f$ faces. Then

$$n - m + f = 2.$$

**Corollary (any number of components).** If the plane graph $G$ has $c \ge 1$ connected components, then $n - m + f = 1 + c$.

Multiple edges and loops are allowed in the theorem, provided each is drawn as a simple arc (a loop as a simple closed curve through its vertex).

## In plain words

Draw a connected network on paper with no crossing lines. Count the dots, the lines, and the regions that the lines cut the paper into, with the outside counted as one region. Dots minus lines plus regions is always two.

The reason is that you can build any such drawing one line at a time. Start with one dot: one dot, no lines, one region. A new line to a new dot adds one dot and one line, so the count does not change. A new line between two dots that are already joined closes a loop. It cuts one region into two, so it adds one line and one region, and again the count does not change.

## Proof

We prove the corollary, which contains the theorem as the case $c = 1$. The proof is by induction on $m$, with $n$ and $c$ fixed. A graph with $n$ vertices and $c$ components has at least $n - c$ edges, with equality exactly when it is a forest.

**Base case: $G$ is a forest.** Then $m = n - c$. The drawing of a forest contains no closed curve, and the complement of a finite union of points and arcs that contains no closed curve is connected (Diestel, Section 4.1; this is the easy half of the [Jordan curve theorem](/jordan-curve-theorem/), the fact that an arc does not separate the plane). So $f = 1$ and $n - m + f = n - (n - c) + 1 = 1 + c$.

**Step: $G$ is not a forest.** Then $G$ has a cycle $C$. Let $e$ be an edge of $C$. The cycle $C$ is drawn as a simple closed curve. By the Jordan curve theorem its complement has exactly two regions, an inside and an outside, and every point of $C$ is on the boundary of both. Points near the middle of $e$ on one side of $e$ are in the inside of $C$, and points on the other side are in the outside. No face of $G$ meets both regions, because $C$ is part of the drawing. So the two faces of $G$ that touch the two sides of $e$ are different.

Delete $e$. The graph $G - e$ has the same $c$ components, because the other edges of $C$ still join the ends of $e$. Its drawing is the drawing of $G$ without the open arc $e$. The two faces on the two sides of $e$ become one face, since they are now joined through the points of $e$. Every other face of $G$ does not touch the interior of $e$ and stays a face of $G - e$. So $G - e$ has $f - 1$ faces and $m - 1$ edges. By the induction hypothesis, $n - (m-1) + (f-1) = 1 + c$, which is $n - m + f = 1 + c$. $\blacksquare$

## Consequences

**Edge bounds.** Let $G$ be a simple connected plane graph with $n \ge 3$ vertices. Each face is bounded by a closed walk that uses at least 3 edge sides, and each edge has two sides, so $3f \le 2m$. With $f = 2 - n + m$ this gives $m \le 3n - 6$. If $G$ has no triangle, each face uses at least 4 edge sides, so $4f \le 2m$ and $m \le 2n - 4$. These are the bounds of the [planar edge bound](/planar-edge-bound/) page.

**Small degree.** By the [handshake lemma](/handshake-lemma/), the average degree is $2m/n \le 6 - 12/n < 6$, so every simple planar graph has a vertex of degree at most 5. This fact drives the [five color theorem](/five-color-theorem/), the [five-color algorithm](/five-color-algorithm/), and the linear-time bounds of many planar algorithms.

**Two non-planar graphs.** $K_5$ has $n = 5$ and $m = 10 > 3 \cdot 5 - 6 = 9$, so it is not planar. $K_{3,3}$ has no triangle, $n = 6$ and $m = 9 > 2 \cdot 6 - 4 = 8$, so it is not planar. With [Kuratowski's theorem](/kuratowski-theorem/) these two graphs describe all non-planar graphs.

**Combinatorial form.** For a connected graph with a rotation system, let $f$ be the number of face orbits. Then $n - m + f = 2 - 2g$ for an integer $g \ge 0$, the genus of the embedding. The rotation system describes a plane embedding exactly when $g = 0$. Planarity tests such as the [Boyer-Myrvold test](/boyer-myrvold-planarity-test/) can check their output this way, and [graph genus](/graph-genus/) is the least $g$ over all rotation systems.

**Duality.** The [planar dual](/planar-dual-graph/) $G^*$ has $f$ vertices, $m$ edges and $n$ faces, so Euler's formula is symmetric in vertices and faces.

## Tightness

The formula is an equality, so the question is when its hypotheses can be weakened.

| plane graph | $n$ | $m$ | $f$ | $n - m + f$ |
|---|---|---|---|---|
| a single vertex | 1 | 0 | 1 | 2 |
| a tree with 4 vertices (a star) | 4 | 3 | 1 | 2 |
| $K_4$ (a triangle with one vertex inside) | 4 | 6 | 4 | 2 |
| the cube graph $Q_3$ | 8 | 12 | 6 | 2 |
| two disjoint triangles | 6 | 6 | 3 | 3 |

- **Connectivity is needed.** Two disjoint triangles give $n - m + f = 3 = 1 + c$ with $c = 2$.
- **The plane (or sphere) is needed.** On the torus the same count gives $n - m + f = 0$ for a cellular embedding. For example $K_7$ embeds on the torus with all 14 faces triangles: $7 - 21 + 14 = 0$. See [graph genus](/graph-genus/).
- **The bound $m \le 3n - 6$ is tight.** Every [maximal planar graph](/maximal-planar-graph/) with $n \ge 3$ vertices has all faces triangles and exactly $3n - 6$ edges; $K_4$ has $6 = 3 \cdot 4 - 6$.
- **$K_5$ is non-planar, but just barely.** Deleting any one edge of $K_5$ leaves 9 edges, which meets $3n - 6$, and $K_5 - e$ is planar.

## History

Euler stated the relation between the numbers of vertices, edges and faces of a convex polyhedron in a paper written in 1752 and published in 1758. His argument cut corners off the polyhedron one at a time and was not complete by modern standards. The graph form proved above, by deleting cycle edges down to a spanning tree, is the standard textbook proof, as in Diestel (Section 4.2) and West (Section 6.1). Aigner and Ziegler give three proofs of the formula, including one by spanning trees of the graph and of its dual.

## References
