---
tag: 99X6NV
kind: theorem
slug: circle-packing-theorem
name: Circle packing theorem
aliases:
- Koebe-Andreev-Thurston theorem
area: graphs/planar-graphs
level: advanced
summary: Every planar graph is the tangency graph of a circle packing in the plane.
prereqs: [planar-graph, maximal-planar-graph, euler-formula, planar-face, jordan-curve-theorem]
see_also: [fary-theorem, planar-separator-theorem, tutte-spring-theorem, schnyder-drawing, graph-drawing, planar-straight-line-drawing, canonical-ordering, planar-dual-graph]
sources:
  - paper: "Paul Koebe, Kontaktprobleme der konformen Abbildung, Berichte über die Verhandlungen der Sächsischen Akademie der Wissenschaften zu Leipzig, Mathematisch-Physische Klasse 88, 141 to 164 (1936)"
    locator: the existence of a circle packing for every triangulation
  - paper: doi:10.1007/BF01245096
    title: Yves Colin de Verdière, Un principe variationnel pour les empilements de cercles, Inventiones Mathematicae 104(3), 655 to 669 (1991)
    locator: the concave functional whose critical points are the packings
  - book: isbn:9780521823562
    title: Kenneth Stephenson, Introduction to Circle Packing, The Theory of Discrete Analytic Functions, Cambridge University Press, 2005
    locator: Part I (the discrete uniformization theorem, existence and uniqueness of packings) and the history of the theorem
  - paper: doi:10.1145/256292.256294
    title: Gary L. Miller, Shang-Hua Teng, William Thurston and Stephen A. Vavasis, Separators for sphere-packings and nearest neighbor graphs, Journal of the ACM 44(1), 1 to 29 (1997)
    locator: the separator theorem for intersection graphs of sphere packings and its use of the circle packing theorem
  - paper: "Graham R. Brightwell and Edward R. Scheinerman, Representations of planar graphs, SIAM Journal on Discrete Mathematics 6(2), 214 to 229 (1993)"
    locator: the simultaneous packing of a 3-connected planar graph and its dual
---

The circle packing theorem says that the vertices of every [planar graph](/planar-graph/) can be drawn as closed discs in the plane, with disjoint interiors, so that two discs touch exactly when their vertices are adjacent. Koebe proved it in 1936; Andreev and Thurston found it again in the 1970s, which gives the name Koebe-Andreev-Thurston theorem. The centers of the discs give a plane straight-line drawing, so the theorem implies [Fáry's theorem](/fary-theorem/), and the geometry of the discs gives short proofs of the [planar separator theorem](/planar-separator-theorem/).

## Statement

A **circle packing** is a finite family of closed discs $D_v$ in the plane with pairwise disjoint interiors. Its **tangency graph** has a vertex for each disc and an edge between two discs that touch.

**Theorem (Koebe, 1936).** For every finite simple planar graph $G$ there is a circle packing $(D_v)_{v \in V(G)}$ whose tangency graph is $G$: $D_u \cap D_v \ne \emptyset$ exactly when $uv$ is an edge.

**Uniqueness for triangulations.** If $G$ is a [maximal planar graph](/maximal-planar-graph/) with at least 4 vertices, the packing is unique up to Möbius transformations and reflections of the plane (Stephenson, Part I). In the proof below, with the three outer discs fixed as unit discs, the radii are unique.

**How the embedding is given.** The statement needs no embedding. The proof uses a combinatorial embedding of a triangulation as a list of triangular faces with a fixed orientation, which is the same as a [rotation system](/rotation-system/), and produces coordinates: a center and a radius for each vertex.

## In plain words

Take any map of towns and roads that you can draw on paper without crossings. You can then replace each town by a coin, with coins of different sizes, and lay the coins flat on a table so that no two coins overlap, and two coins touch exactly when their towns have a road between them.

The proof chooses the sizes first. Around each inner coin the neighbouring coins must close up exactly, with no gap and no overlap. A smooth function of the sizes has its highest point exactly where this happens everywhere, so a solution exists. Then the coins are laid out one triangle at a time, and the triangles tile a large outer triangle without overlap.

## Proof

The full proof is in [the proof](proofs/main.md). It follows the variational method of Colin de Verdière. These are the steps.

1. **Reduction to triangulations.** Every connected simple plane graph with $n \ge 3$ vertices is an induced subgraph of a triangulation: inside each face with a boundary walk of $k \ge 3$ corners, add a cycle of $k$ new vertices and a center vertex, and join them so that all faces become triangles and no edge between two old vertices is added. A packing of the triangulation, with the new discs deleted, is a packing of $G$, because $G$ is induced. Components are packed separately and placed far apart.
2. **Angles.** Three pairwise tangent discs with radii $r_i, r_j, r_k$ have centers that form a triangle with sides $r_i + r_j$, $r_j + r_k$, $r_i + r_k$. Its angle at $i$ is $\alpha_i$ with $\cos \alpha_i = 1 - 2 r_j r_k / ((r_i + r_j)(r_i + r_k))$. In a triangulation with outer face $a b c$, fix $r_a = r_b = r_c = 1$. A packing needs, at every inner vertex $v$, angle sum $\theta_v = 2\pi$ over the faces at $v$.
3. **A concave function.** In the variables $u_v = \log r_v$, the matrix $\partial \alpha_i / \partial u_j$ of one triangle is symmetric: for $i \ne j$ it equals $\sqrt{r_i r_j r_k / (r_i + r_j + r_k)} / (r_i + r_j) > 0$. So $\sum_i \alpha_i \, du_i$ is the gradient of a function $F$, and $\Phi(u) = \sum_{\text{faces}} F - 2\pi \sum_{v \text{ inner}} u_v$ has gradient $(\theta_v - 2\pi)_v$. Its Hessian is minus a weighted Laplacian with the outer vertices fixed, so $\Phi$ is strictly concave.
4. **A maximum exists.** Along every ray $u = t w$, the slope of $\Phi$ tends to $\pi \sum_f \min_{v \in f} w_v - 2\pi \sum_v w_v$. Two counts with [Euler's formula](/euler-formula/) show that this limit is negative for every $w \ne 0$: a set $S$ of $k$ inner vertices spans at most $2k - 5$ inner faces, and a nonempty set $U$ of inner vertices meets at least $2|U| + 1$ faces. So $\Phi$ tends to $-\infty$ at infinity, attains its maximum, and at the maximum $\theta_v = 2\pi$ for every inner vertex. Strict concavity makes the radii unique.
5. **Layout.** Place the triangles one by one. The angle sum $2\pi$ at each inner vertex makes the placement consistent and locally one-to-one. The outer vertices get angle sums that add up to $\pi$, so the boundary becomes the equilateral triangle with side 2, traversed once, and a winding number argument shows that the triangles tile it without overlap.
6. **Discs.** Each disc meets its triangles in sectors, the sectors of one triangle are pairwise tangent and inside the triangle, and the triangles do not overlap. So the discs have disjoint interiors, and two discs touch only when their vertices share an edge. $\blacksquare$

## Consequences

- **Fáry's theorem.** Join the centers of tangent discs by segments. The segment between the centers of $D_u$ and $D_v$ lies in $D_u \cup D_v$ and leaves $D_u$ only at the point where $D_u$ touches $D_v$. So a crossing of two segments with four different ends would be a point common to three discs, and three discs with disjoint interiors have no common point. So no two segments cross. This is a plane straight-line drawing, as in [Fáry's theorem](/fary-theorem/), but with irrational coordinates in general and no small grid; see [de Fraysseix-Pach-Pollack](/de-fraysseix-pach-pollack/) for a grid drawing.
- **Separators.** Miller, Teng, Thurston and Vavasis map a circle packing to the sphere, move it with a Möbius transformation so that a centerpoint of the centers is at the origin, and cut with a random great circle. The cut meets $O(n^{1/2})$ discs in expectation and splits the rest in a balanced way. This is a geometric proof of the [planar separator theorem](/planar-separator-theorem/) with good constants.
- **Spectral partitioning.** Spielman and Teng (1996) used circle packings to show that the second smallest Laplacian eigenvalue of a planar graph with bounded degree is $O(1/n)$, so spectral bisection finds small cuts on such graphs.
- **Primal and dual together.** For a 3-connected planar graph, the graph and its [dual](/planar-dual-graph/) can be packed at the same time so that the dual circles cross the primal circles at right angles at the points of tangency (Brightwell and Scheinerman, 1993). This gives a convex drawing of the graph and its dual together.
- **Conformal maps.** Thurston conjectured, and Rodin and Sullivan proved (1987), that the packings of fine hexagonal triangulations of a domain converge to the Riemann map of the domain. This is the start of discrete conformal geometry.

## Tightness

| graph | packing | reason |
|---|---|---|
| a single vertex | one disc | no tangency is required |
| a tree | each child disc touches its parent disc, smaller discs at each level | trees are planar; children of a disc fit on its boundary when they are small enough |
| $K_4$ | three unit discs at the corners of an equilateral triangle with side 2, and a central disc of radius $2/\sqrt{3} - 1 \approx 0.1547$ | the circumradius of the triangle is $2/\sqrt{3}$ |
| octahedron | three unit outer discs and three inner discs of radius $5 - 2\sqrt{6} \approx 0.1010$ | angle sum $2\pi$ at an inner vertex, checked numerically |
| $K_5$, $K_{3,3}$ | no packing | the tangency graph of a packing is planar by the Fáry argument above |

In the octahedron, an inner vertex has four faces: one with the other two inner discs (angle $\pi/3$), one with two outer discs, and two with one outer and one inner disc. With $r = 5 - 2\sqrt{6}$ these angles add up to $2\pi$, and each outer vertex gets angle $\pi/3$, as the proof predicts.

- **Equal radii are not enough.** A unit disc touches at most 6 unit discs with disjoint interiors, so the star $K_{1,7}$ is not the tangency graph of equal discs. Different radii are needed.
- **Planarity is necessary.** The tangency graph of every circle packing is planar, so the theorem characterizes planar graphs.
- **Uniqueness needs a triangulation.** For the cycle $C_4$, four discs have 12 real parameters (centers and radii) and the four tangencies give 4 equations, which leaves a family of dimension 8, while the Möbius transformations and reflections form a group of dimension 6. So $C_4$ has packings that no Möbius transformation relates. The uniqueness statement holds for maximal planar graphs only.

## History

Paul Koebe proved the theorem in 1936 as a corollary of his work on conformal maps of domains bounded by circles. E. M. Andreev proved a more general result on hyperbolic polyhedra with prescribed angles in 1970, and William Thurston rediscovered the circle packing theorem in his 1978 lecture notes on three-manifolds, derived it from Andreev's theorem, and proposed an iterative algorithm to compute the radii. Rodin and Sullivan (1987) proved his conjecture on the approximation of conformal maps. Colin de Verdière (1991) gave the variational proof used here. Brightwell and Scheinerman (1993) proved the primal and dual form, and Miller, Teng, Thurston and Vavasis (1997) used the theorem for geometric separators. Stephenson's book (2005) collects the theory and the algorithms.

## References
