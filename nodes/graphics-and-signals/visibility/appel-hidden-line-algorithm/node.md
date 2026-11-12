---
tag: EFMSAP
kind: algorithm
slug: appel-hidden-line-algorithm
name: Appel's hidden-line algorithm
aliases:
- quantitative invisibility
- Appel's algorithm
area: graphics-and-signals/visibility
level: advanced
summary: Remove hidden lines by walking along the edges and counting the faces in front of each point. The count changes only where an edge passes behind a contour edge.
solves: [hidden-line-removal]
model: real-ram
complexity:
  vars: {n: "the total number of vertices, edges and faces", c: the number of contour edges, s: the number of solids}
  time: {worst: O(n (c log c + s))}
  space: {extra: O(n)}
properties: {deterministic: true, in_place: false, online: false}
history:
  year: 1967
  people: [Arthur Appel]
  note: Appel introduced quantitative invisibility at the 1967 ACM National Conference, as a way to make machine drawings of solids with the hidden lines removed.
prereqs: [hidden-line-removal, silhouette-edge, back-face-culling]
see_also: [roberts-hidden-line-algorithm, silhouette-edge, hidden-line-removal, back-face-culling, visibility-coherence, hidden-surface-removal, object-space-vs-image-space, z-buffer]
sources:
  - paper: doi:10.1145/800196.806007
    title: Arthur Appel, The notion of quantitative invisibility and the machine rendering of solids, Proceedings of the 1967 22nd National Conference of the ACM, pages 387 to 393
    locator: the definition of quantitative invisibility and the rule for its change at contour lines
  - paper: doi:10.1145/356625.356626
    title: Ivan E. Sutherland, Robert F. Sproull and Robert A. Schumacker, A characterization of ten hidden-surface algorithms, ACM Computing Surveys 6(1), 1974, pages 1 to 55
    locator: the description of Appel's algorithm among the object space algorithms
  - paper: doi:10.1145/258734.258894
    title: Lee Markosian, Michael A. Kowalski, Daniel Goldstein, Samuel J. Trychin, John F. Hughes and Lubomir D. Bourdev, Real-time nonphotorealistic rendering, SIGGRAPH 1997, pages 415 to 420
    locator: the visibility of the silhouette edges by Appel's quantitative invisibility
---

Appel's hidden line algorithm draws the visible parts of the edges of polyhedral solids. It gives each point a number, its *quantitative invisibility* (QI): the number of faces between the point and the viewer. A point is visible when its QI is 0. Arthur Appel showed in 1967 that along an edge the QI changes only where the edge passes behind a *contour edge*, that is, a [silhouette edge](/silhouette-edge/), and then by exactly 1. So the algorithm finds the QI of one vertex per solid by brute force, and then walks along the edges and updates the count at the contour crossings. Unlike [Roberts' algorithm](/roberts-hidden-line-algorithm/), it does not need convex bodies, and it does not test every edge against every body. This page is the line drawing method for exact object space edges. Methods that decide the color of each pixel are on the [hidden surface removal](/hidden-surface-removal/) and [z-buffer](/z-buffer/) pages.

## In plain words

Think of each point on an edge, and count how many surfaces stand between it and your eye. If the count is zero, you can see the point. If you move along an edge, the count stays the same most of the time. It goes up by one when the edge slides behind the outline of a surface in front of it, and it goes down by one when the edge comes out again. So you do not need to count again at every point. You count once at a corner, then you follow the edges from corner to corner, and you add or subtract one each time you pass behind an outline. You draw the parts where the count is zero.

## The problem

The input is a set of closed polyhedral solids that do not cut into each other. Each face is a planar polygon, convex or not, with its vertices in counterclockwise order as seen from outside the solid. The view is parallel along the $z$ axis: the point $(x, y, z)$ projects to $(x, y)$, and a larger $z$ is nearer to the viewer. A face is a *front face* if its outward normal has a positive $z$ component, and a *back face* if the $z$ component is negative.

The *quantitative invisibility* of a point $p$ is the number of front faces $F$ whose projection contains the projection of $p$ in its interior and whose plane is above $p$ there. An edge is a *contour edge* if exactly one of its two faces is a front face. The output is, for each edge, its division into pieces with their QI values. The visible parts are the pieces with QI 0. The input is in general position: no vertex projects onto another edge or vertex, no face is seen edge on, and no three edges cross at one point in the projection. A perspective view reduces to this case by a projective map of the scene.

## The algorithm

Two facts drive the method. Let $p(t)$ move along an edge, and let it pass behind an edge $e'$ in the projection, with $e'$ in front of $p(t)$. If $e'$ has two front faces, they lie on the two sides of $e'$ in the projection, so one face stops covering $p(t)$ and the other starts: the QI does not change. If $e'$ has two back faces, neither counts. If $e'$ is a contour edge, its one front face starts or stops covering $p(t)$: the QI changes by $+1$ or $-1$. The sign comes from the side: the front face lies to the left of its counterclockwise boundary, so a crossing from the right of $e'$ to its left adds 1.

At a vertex $v$, the faces at $v$ do not cover $v$, but some of them can cover the points of an edge $v w$ just after $v$. Let $\mathrm{cover}(v, w)$ be the number of front faces at $v$ that do not contain the edge $v w$, that contain the direction of $v w$ inside their corner at $v$ in the projection, and below whose plane the edge goes. Then the QI just after $v$ on the edge is $\mathrm{QI}(v) + \mathrm{cover}(v, w)$.

```pseudo id=main
APPEL(solids)                     ▷ closed solids, faces counterclockwise from outside
L1  C ← the contour edges, each directed as in its front face
L2  for each solid S do
L3      v0 ← a vertex of S; QI(v0) ← number of front faces that cover v0 (test all faces)
L4      Q ← a queue that holds v0
L5      while Q is not empty do u ← remove the first vertex of Q
L6          for each edge u w that is not done do
L7              q ← QI(u) + cover(u, w)
L8              X ← the points t where u w passes behind an edge of C, with sign ±1, sorted by t
L9              for each (t, δ) in X do output a piece of u w with QI q that ends at t; q ← q + δ
L10             output the last piece with QI q; if QI(w) is unknown then QI(w) ← q − cover(w, u); add w to Q
L11 output the pieces with QI 0
```

Line L3 is the only test against the whole scene, once per solid. Line L8 tests the edge only against the contour edges, not against all faces. The vertex correction of lines L7 and L10 handles the faces that meet at a vertex, including the faces of nonconvex corners.

## Example

The scene has two boxes: a slab $[0, 4] \times [0, 4] \times [0, 1]$ and a block $[3, 6] \times [3, 5] \times [2, 3]$ above one corner of it. To avoid faces that are seen edge on, both are sheared by the map $(x, y, z) \mapsto (x + z/3, y + z/5, z)$, which keeps them closed and disjoint. After the shear, each box has three front faces (top, left side $-x$ and front side $-y$) and three back faces. The slab has the vertices $(0, 0, 0)$, $(4, 4, 0)$, $(1/3, 21/5, 1)$, $(13/3, 21/5, 1)$ and so on, and the block projects to the parallelogram with $x$ from $11/3$ to $7$ and $y$ from $17/5$ to $28/5$.

Step L1. Each box has 6 contour edges, the outline of its projection. For the block, two of them are the bottom edges $x = 11/3$ and $y = 17/5$ at height $z = 2$.

Step L3. The slab starts at $(0, 0, 0)$ and the block at $(11/3, 17/5, 2)$. No front face covers either point, so both have QI 0.

Steps L7 to L10 for the top back edge of the slab, from $u = (1/3, 21/5, 1)$ to $w = (13/3, 21/5, 1)$. $\mathrm{QI}(u) = 0$ and $\mathrm{cover}(u, w) = 0$. The edge passes behind the block's contour edge $x = 11/3$ at $t = 5/6$, and it moves into the block's projection, so $\delta = +1$. The pieces are QI 0 on $[0, 5/6]$ and QI 1 on $[5/6, 1]$, and $\mathrm{QI}(w) = 1$. The top right edge of the slab, from $(13/3, 1/5, 1)$ to $w$, passes behind the block's contour edge $y = 17/5$ at $t = 4/5$ and gets the same result.

From $w$, the vertical edge down to $(4, 4, 0)$ goes under the slab's top face, which meets $w$ and contains the direction of the edge in its corner. So $\mathrm{cover} = 1$ and the whole edge has QI 2: it is behind the slab's top and the block's top.

| edge | pieces (parameter range, QI) |
|---|---|
| slab, top back edge | $[0, 5/6]$ QI 0, $[5/6, 1]$ QI 1 |
| slab, top right edge | $[0, 4/5]$ QI 0, $[4/5, 1]$ QI 1 |
| slab, bottom back edge to $(4, 4, 0)$ | $[0, 11/12]$ QI 1, $[11/12, 1]$ QI 2 |
| slab, bottom right edge to $(4, 4, 0)$ | $[0, 17/20]$ QI 1, $[17/20, 1]$ QI 2 |
| slab, vertical edge at $(4, 4)$ | $[0, 1]$ QI 2 |
| block, three edges at $(6, 5, 2)$ | $[0, 1]$ QI 1 |
| all other 16 edges | $[0, 1]$ QI 0 |

The drawing shows the 16 visible edges and the visible pieces of the two top edges of the slab.

## Correctness

Fix an edge $u w$ and a front face $F$ that does not contain it. Whether $F$ covers $p(t)$ can change only where the projection of $p(t)$ crosses the boundary of the projection of $F$, because the edge does not pierce $F$: the solids are closed and do not cut into each other. In general position such a crossing is a single point inside an edge $e'$ of $F$, and $F$ counts there only if $e'$ is in front of $p(t)$. Summed over the faces at $e'$, the change is 0 for an edge with two front faces or two back faces and $\pm 1$ for a contour edge. So the QI is constant between the crossings of line L8 and jumps by their signs.

At the ends, a face that does not meet $v$ covers the points near $v$ exactly when it covers $v$, by continuity and general position. A face at $v$ does not cover $v$ itself, and it covers the points just after $v$ exactly when the test of $\mathrm{cover}$ holds. This gives line L7 and, read at $w$, line L10. The edge graph of each closed solid is connected, so the walk from $v_0$ reaches every vertex and every edge. The full proof is below.

## Complexity

Let $n$ be the total number of vertices, edges and faces, $c$ the number of contour edges, and $s$ the number of solids. Line L1 is $O(n)$. Line L3 tests all faces once per solid, which is $O(s n)$ in total. Each edge is walked once; line L8 tests it against the $c$ contour edges and sorts the crossings, and the cover counts at its two ends cost the sizes of the faces there. An edge has at most $c$ crossings, so its sort costs $O(c \log c)$, and the cover counts cost $O(n)$ over all edges when the vertex degrees are bounded. The total time is $O(n (c \log c + s))$. The extra space is $O(n)$ for the QI values, the queue and the list of contour edges. In the worst case $c$ is of order $n$ and the bound is quadratic, like Roberts' method. The gain is that only the contour edges, not all faces, are tested against each edge.

## Properties

- **Object space, exact.** The output is a list of exact segments with their QI values. With rational input and exact arithmetic, it is exact.
- **General polyhedra.** Faces and solids need not be convex. Only closedness, orientation and general position are used.
- **More than visibility.** The pieces with QI 1 are the lines just behind one surface, which some technical drawings show as dashed lines.
- **Coherence.** The work for an edge depends on the contour edges and on its crossings, not on the number of faces. This is an example of [visibility coherence](/visibility-coherence/) along edges.

## Variants and improvements

- **Perspective views.** Apply the perspective map to the scene, then run the parallel version. Contour edges and QI do not change under this map.
- **Surfaces with borders.** For open surfaces, a border edge of a front face also changes the QI by $\pm 1$, so it goes into $C$ with the contour edges.
- **Contour edges only.** Line drawing styles that show only silhouettes walk the QI along the contour edges and skip the other edges. Markosian and others used this with fast methods to find the silhouette, to draw animated polyhedral models in real time.
- **Hidden lines with a buffer.** Many renderers instead draw the edges with a [z-buffer](/z-buffer/) test. This is simpler and runs on the graphics hardware, but its output is pixels, not exact segments.

## When to use it

Use it for exact vector line drawings of polyhedral models, such as engineering parts or architectural models, when the solids are not convex or the scene is large. It is also the method of choice when the drawing must show the hidden lines with a different style, since the QI tells how deep each piece is. For a few convex blocks, [Roberts' algorithm](/roberts-hidden-line-algorithm/) is shorter to write. For images on screen, a z-buffer is simpler.

## Pitfalls

- **Wrong orientation.** The sign of a crossing comes from the side of the front face. If some faces are clockwise from outside, the front and back tests and the signs are wrong. Orient all faces before the run.
- **Degenerate crossings.** An edge that passes behind a vertex, or a vertex that projects onto another edge, breaks the rule of $\pm 1$ per crossing. Perturb the view, or treat such cases with symbolic perturbation.
- **The vertex correction.** Without the term $\mathrm{cover}$, an edge that leaves a vertex under one of the faces at that vertex gets a QI that is too small, and its hidden part is drawn.
- **Error that spreads.** One wrong value spreads along the whole walk. A check is to compare the computed QI of a vertex with the QI reached from another edge, and a negative QI shows an error.
- **Intersecting solids.** If two solids cut into each other, the QI also changes where an edge pierces a face, and the lines where the surfaces cross are missing. Compute those intersections first, or keep the solids apart.

## Implementations

## History

Arthur Appel worked at IBM. His 1967 paper defined quantitative invisibility and the contour lines across which it changes, and he used it for machine drawings of solids. Sutherland, Sproull and Schumacker's 1974 survey of hidden surface algorithms described it as an object space method that uses the coherence of the edges. The same idea of counting the surfaces in front of a point came back in the 1990s in nonphotorealistic rendering, where Markosian and others used it to decide which parts of the silhouette to draw.

## References
