---
tag: 122K35
kind: theorem
slug: tutte-spring-theorem
name: Tutte's spring theorem
aliases:
- Tutte embedding theorem
area: graphs/planar-graphs
level: advanced
summary: Placing outer-face vertices on a convex polygon and each inner vertex at the barycenter of its neighbours yields a planar straight-line drawing for 3-connected planar graphs.
prereqs: [planar-graph, planar-face, k-vertex-connected-graph, laplacian-matrix]
see_also: [planar-straight-line-drawing, schnyder-drawing, wagner-theorem, graph-drawing, maximal-planar-graph, gaussian-elimination, planar-embedding, rotation-system]
sources:
  - paper: doi:10.1112/plms/s3-13.1.743
    title: W. T. Tutte, How to draw a graph, Proceedings of the London Mathematical Society s3-13(1), 743 to 767 (1963)
    locator: the barycentric construction and the theorem that it gives a convex planar drawing of a 3-connected planar graph
  - paper: "Steven J. Gortler, Craig Gotsman and Dylan Thurston, Discrete one-forms on meshes and applications to 3D mesh parameterization, Computer Aided Geometric Design 23(2), 83 to 112 (2006)"
    locator: the short proof of Tutte's theorem by counting the turns of discrete one-forms
  - book: isbn:9780133016154
    title: Giuseppe Di Battista, Peter Eades, Roberto Tamassia and Ioannis G. Tollis, Graph Drawing, Algorithms for the Visualization of Graphs, Prentice Hall, 1999
    locator: the barycenter method of Tutte in the chapter on force-directed methods
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 4.3, Drawings (3-connected planar graphs have a unique embedding and their faces are bounded by cycles)
---

Tutte's spring theorem says that a [3-connected](/k-vertex-connected-graph/) [planar graph](/planar-graph/) can be drawn with straight edges and convex faces by a simple rule: fix the vertices of one face cycle at the corners of a strictly convex polygon, in their cyclic order, and put every other vertex at the average of the positions of its neighbours. The positions solve a linear system with the [Laplacian matrix](/laplacian-matrix/), which has exactly one solution. Tutte proved in 1963 that this solution is a planar straight-line drawing in which every face is a convex polygon. Without 3-connectivity the rule can put vertices on top of each other.

## Statement

**Theorem (Tutte, 1963).** Let $G$ be a 3-connected planar graph and let $C = (c_1, \ldots, c_k)$ be the boundary cycle of a face of a planar embedding of $G$. Place $c_1, \ldots, c_k$ at the corners of a strictly convex polygon $Q$, in this cyclic order. Then there is exactly one placement $x : V \to \mathbb{R}^2$ of the other vertices with

$$x_v = \frac{1}{\deg v} \sum_{w \in N(v)} x_w \qquad \text{for every } v \notin C,$$

and drawing each edge as a straight segment between its ends gives a planar drawing: distinct vertices go to distinct points, and two edges meet only at a common end. The faces of this drawing are the faces of the embedding, every inner face is a convex polygon, and the outer face is the outside of $Q$.

**How the embedding is given.** A 3-connected planar graph has only one planar embedding up to a mirror image and the choice of outer face (Diestel, Section 4.3), so the only input beyond the graph is the face cycle $C$, read off a [rotation system](/rotation-system/) with [face tracing](/planar-face-finding/). The output is a coordinate for each vertex.

The same holds with any positive weights $\lambda_{vw}$ on the edges at each inner vertex in place of the equal weights $1/\deg v$; the proof below does not use the equality.

**Small cases.**

| graph | outer cycle and polygon | inner positions | result |
|---|---|---|---|
| $K_4$ | $0, 1, 2$ at $(0, 0), (6, 0), (0, 6)$ | $3$ at $(2, 2)$, the centroid | three convex triangles inside |
| the cube $Q_3$ | the outer square at $(\pm 3, \pm 3)$ | the inner square at $(\pm 1, \pm 1)$ | four convex quadrilaterals and the inner square |
| the octahedron | $0, 1, 2$ at $(0, 0), (12, 0), (0, 12)$ | $(12/5, 24/5)$, $(24/5, 12/5)$, $(24/5, 24/5)$ | seven convex triangles inside |
| a triangle $0, 1, 2$ plus a vertex 3 joined to 0 and 1 | $0, 1, 2$ | 3 at the midpoint of the edge $01$ | not a drawing: 3 lies on the edge $01$; the graph is only 2-connected |
| $K_5$ | $0, 1, 2$ | $3$ and $4$ both at the centroid | not a drawing: $K_5$ is not planar |
| $K_{3,3}$ | the 4-cycle $a_1 b_1 a_2 b_2$ as a square | $a_3$ and $b_3$ both at the center | not a drawing: $K_{3,3}$ is not planar |

A single vertex and a tree are not 3-connected, so the theorem says nothing about them; a tree with fixed leaves even puts all inner vertices on segments between leaves.

## In plain words

Pin one ring of the network to the corners of a convex shape, like a picture frame. Replace every link by a rubber band of the same strength and let the free nodes settle. Each free node stops where the pulls of its bands cancel, which is the average of its neighbours' positions.

If the network is planar and stays connected after you remove any two nodes, the settled picture has no crossings at all, and every region is convex. The pull of the bands cannot fold the picture over, because that would need a part that is attached to the rest by only one or two nodes.

## Proof

Let $V_C$ be the vertices of $C$ and $I = V \setminus V_C$ the inner vertices. For a linear function $h : \mathbb{R}^2 \to \mathbb{R}$, write $h(v)$ for $h(x_v)$. The equation of the theorem says that for each inner vertex, $h(v)$ is the average of $h$ over its neighbours.

**Step 1: exactly one solution.** The equations form a square linear system for the inner positions, one system per coordinate, with the matrix $L_{II}$, the rows and columns of the inner vertices in the Laplacian. Suppose $L_{II}\, y = 0$, that is, $y$ on $I$ is the average of its neighbours when $y = 0$ on $V_C$. Let $y(v)$ be largest at $v$. Then all neighbours of $v$ have the same value, and so on along every path; since $G$ is connected, the value $y(v)$ reaches $V_C$, where it is 0. So $\max y = 0$, and likewise $\min y = 0$. So $L_{II}$ is nonsingular and the solution is unique. It can be computed by [Gaussian elimination](/gaussian-elimination/).

**Step 2: every half-plane is connected.** Let $\ell$ be a line, $h$ a linear function with $\ell = \{h = t\}$, and $V^+ = \{v : h(v) > t\}$. *Claim: if $V^+ \ne \emptyset$, then $G[V^+]$ is connected and contains a vertex of $C$.* Let $Q$ be a component of $G[V^+]$ and let $M$ be the vertices of $Q$ where $h$ is largest. If some vertex of $M$ is in $V_C$, fine. Otherwise, every $w \in M$ is inner, its value is the average of its neighbours, and every neighbour has a value at most $h(w)$: neighbours in $V^+$ are in $Q$, others have value at most $t$. So all neighbours have the value $h(w)$ and are in $M$. Then $M$ is closed under taking neighbours, so $M = V$, and $M$ contains vertices of $C$ after all. So each component of $G[V^+]$ contains a vertex of $C$. Because $Q$ is strictly convex, the corners of $Q$ in the open half-plane $h > t$ form one contiguous arc of $C$, which is connected. So $G[V^+]$ is connected.

**Step 3: inner vertices lie strictly inside $Q$.** Let $\ell$ be the line of a side $c_i c_{i+1}$ of $Q$, with $h \le t$ on $Q$. By the argument of Step 2 (the maximum principle), no inner vertex has $h > t$. Suppose a set $Z$ of inner vertices has $h = t$, and let $Z_0$ be a component of $G[Z]$. Each $w \in Z_0$ is an average of values at most $t$ that equals $t$, so all its neighbours have the value $t$; those neighbours are in $Z_0$ or are $c_i$ or $c_{i+1}$. So $\{c_i, c_{i+1}\}$ separates $Z_0$ from the other corners of $Q$, against 3-connectivity. Hence every inner vertex is strictly inside $Q$.

**Step 4: no inner vertex is degenerate.** Call an inner vertex $v$ *degenerate* if all its neighbours lie on one line $\ell$; then $x_v \in \ell$ too. Suppose such a $v$ exists, with $\ell = \{h = t\}$. Since $x_v$ is strictly inside $Q$, both open sides $V^+$ and $V^-$ of $\ell$ contain corners of $Q$, and by Step 2 both induce connected subgraphs. Let $Z$ be the component containing $v$ of the subgraph induced by the inner vertices that are degenerate on $\ell$, and let $N$ be the set of vertices outside $Z$ with a neighbour in $Z$. All of $N$ lies on $\ell$, and $N$ separates $Z$ from the corners of $Q$ off $\ell$, so $|N| \ge 3$ by 3-connectivity. Each $w \in N$ has a neighbour in $V^+$ and one in $V^-$: if $w$ is inner, it is not degenerate on $\ell$ and is the average of its neighbours, so it has neighbours strictly on both sides; if $w$ is a corner of $Q$, then $\ell$ passes through $w$ and through the interior of $Q$, so the two neighbours of $w$ on $C$ lie strictly on opposite sides. Take $w_1, w_2, w_3 \in N$ and contract $V^+$, $V^-$ and $Z$ to single vertices. Each $w_i$ is adjacent to all three, which gives a $K_{3,3}$ minor in the planar graph $G$, a contradiction by [Wagner's theorem](/wagner-theorem/).

**Step 5: neighbours surround each inner vertex.** For an inner vertex $v$ and any line $\ell$ through $x_v$, with $\ell = \{h = h(v)\}$, the values $h(w) - h(v)$ over the neighbours sum to 0. By Step 4 they are not all 0, so some neighbour lies strictly on each side of $\ell$. The same argument with Step 2 shows that no edge has length 0: if $x_u = x_v$ for an edge $uv$, apply Step 4 to the set of vertices at that point.

**Step 6: the drawing is an embedding (outline).** This last step is an angle count; we give it in outline and refer to Tutte (1963) and to the shorter proof of Gortler, Gotsman and Thurston (2006) for the details. Every face of the embedding is bounded by a cycle, since $G$ is 2-connected. First, one shows that for every inner edge $uv$ the two faces at $uv$ lie on opposite sides of the line through $x_u$ and $x_v$, near the edge; if they lay on the same side, Step 2 applied to that line and the argument of Step 4 would again give a $K_{3,3}$ minor. With this and Step 5, every inner face is drawn as a polygon traversed in the orientation of the embedding, and every inner vertex sees its faces in rotation order, turning the same way. Then the face angles around an inner vertex add up to $2\pi$ times a positive integer, and around a corner of $Q$ to at least the inner angle of $Q$ there. The sum of all face angles of the inner faces is $\sum_f (k_f - 2)\pi$, where $k_f$ is the length of $f$, and by [Euler's formula](/euler-formula/) this equals $2\pi |I| + (k - 2)\pi$, the value obtained if every inner vertex is surrounded exactly once and every corner of $Q$ exactly by its inner angle. So equality holds everywhere: each face is convex, the faces around each vertex fit together without overlap, the faces cover $Q$ exactly once, and the drawing is planar. $\blacksquare$

## Consequences

- **Convex drawings.** Every 3-connected planar graph has a straight-line drawing with convex faces, and it can be computed by solving one sparse linear system. Every planar graph is a subgraph of a [maximal planar graph](/maximal-planar-graph/), which is 3-connected for $n \ge 4$, so every planar graph has a straight-line drawing; this reproves Fáry's theorem (see [planar straight-line drawing](/planar-straight-line-drawing/)).
- **Steinitz-type results.** Tutte drawings are the starting point of lifting constructions that realize 3-connected planar graphs as convex polyhedra.
- **Mesh parameterization.** In geometry processing, a triangulated disc is flattened by fixing its boundary on a convex polygon and solving the same system, with weights chosen to reduce distortion. The theorem with positive weights guarantees that the flattened mesh does not fold over.
- **Uniqueness of embeddings.** The drawing realizes the unique embedding of a 3-connected planar graph; its faces are the cycles that are induced and non-separating.

## Tightness

- **3-connectivity is needed.** The 2-connected example in the table puts a vertex on an edge, and in general a 2-cut $\{a, b\}$ lets the part behind it collapse onto the segment $ab$.
- **Convexity of $Q$ is needed.** If the outer polygon is not convex, inner vertices near a reflex corner can be pulled outside $Q$, and edges can cross the boundary.
- **Planarity is needed.** For $K_5$ and $K_{3,3}$ the system still has one solution, but two vertices coincide, as the table shows.
- **Bad resolution.** The coordinates can need exponentially many bits relative to $n$: in nested structures, each level shrinks by a constant factor, so the smallest distances can be exponentially small. Grid drawings such as the [Schnyder drawing](/schnyder-drawing/) avoid this, with all coordinates in $\{0, \ldots, n - 2\}$.

## History

Tutte published the theorem in 1963 in "How to draw a graph", with the barycentric construction and a proof through the connectivity of half-planes. It became the base of force-directed graph drawing, where springs between all vertices replace the fixed rule (Di Battista, Eades, Tamassia and Tollis), and of mesh parameterization in computer graphics, where Gortler, Gotsman and Thurston gave a short proof by discrete one-forms in 2006.

## References
