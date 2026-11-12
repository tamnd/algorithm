---
tag: 4NCX83
kind: algorithm
slug: doo-sabin-subdivision
name: Doo-Sabin subdivision
aliases:
- Doo-Sabin scheme
- Doo-Sabin surface
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: A dual subdivision scheme with one new point per face corner, and one new face per old face, edge and vertex. It is biquadratic B-spline refinement on regular quads, with a C1 limit.
solves: [surface-from-control-mesh]
model: real-ram
complexity:
  vars: {E: the number of edges, k: the largest number of sides of a face}
  time: {worst: O(E k)}
  space: {extra: Θ(E)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1978
  people: [Daniel Doo, Malcolm Sabin]
  note: Doo and Sabin published the scheme and the first analysis near extraordinary points in Computer-Aided Design in 1978, in the same issue as Catmull and Clark.
prereqs: [polygon-mesh, b-spline, subdivision-surface]
see_also: [subdivision-surface, catmull-clark-subdivision, chaikin-corner-cutting, surface-from-control-mesh, tensor-product-surface, knot-refinement, euler-formula, eigenvalue]
sources:
  - paper: doi:10.1016/0010-4485(78)90111-2
    title: D. Doo and M. Sabin, Behaviour of recursive division surfaces near extraordinary points, Computer-Aided Design 10(6), 356-360 (1978)
    locator: the new point of each face corner as a weighted average of the corners of the face, the faces made for each old face, edge and vertex, and the eigenvalue analysis near an extraordinary point
  - paper: doi:10.1016/0010-4485(78)90110-0
    title: E. Catmull and J. Clark, Recursively generated B-spline surfaces on arbitrary topological meshes, Computer-Aided Design 10(6), 350-355 (1978)
    locator: the companion paper, which also describes the biquadratic case
  - paper: "Jörg Peters and Ulrich Reif, Analysis of algorithms generalizing B-spline subdivision, SIAM Journal on Numerical Analysis 35(2), 728-748 (1998)"
    locator: the proof that the Doo-Sabin and Catmull-Clark limit surfaces are C1 at extraordinary points (check)
  - book: isbn:9781558604469
    title: Joe Warren and Henrik Weimer, Subdivision Methods for Geometric Design, A Constructive Approach, Morgan Kaufmann, 2002
    locator: Chapter 2 for the subdivision of uniform B-splines, and the chapters on polyhedral meshes for the dual quad schemes
---

Doo-Sabin subdivision refines a [polygon mesh](/polygon-mesh/) by cutting off its corners and edges. Each face shrinks to a smaller copy of itself, made of one new point near each of its corners, and new faces fill the gaps: a quad for each old edge and a polygon for each old vertex. On a regular grid of quads this is the refinement of a biquadratic uniform [B-spline](/b-spline/) surface, so the limit is $C^1$, and the faces that are not quads stay as isolated extraordinary faces with a $C^1$ limit too. It is the dual of [Catmull-Clark subdivision](/catmull-clark-subdivision/): it makes new faces where that scheme makes new vertices.

## In plain words

Take each face of the cage, and inside it put a new point near each corner, a little toward the middle of the face. Join these points to get a smaller copy of the face. Now there are gaps. Across each old edge, two shrunken faces have two points each, and they make a new four-sided face. Around each old corner, the faces that met there each have one point, and they make a new face with as many sides as the corner had edges.

Do this again and again. Every sharp edge and corner gets cut, and the cage settles on a smooth surface. It is the same idea as cutting the corners of a polygon to round it, done on a surface.

## The problem

The input is a mesh with $V$ vertices, $E$ edges and $F$ faces of any number of sides. It is a closed oriented 2-manifold: each edge is in exactly two faces, with opposite directions, and the faces around each vertex form one cycle. The output after one step is again a closed 2-manifold with $2E$ vertices, $4E$ edges and $F + E + V$ faces, and every new vertex has valence 4. The limit of repeated steps is the [subdivision surface](/subdivision-surface/) of the mesh.

The model is the [real RAM](/real-ram/), and the unit of work is one addition or scaling of a point. For faces with 3, 4 or 6 sides the weights are rational, and the implementation is exact. For other sizes it uses floating point cosines.

## The algorithm

For a face $f = (v_0, \dots, v_{k-1})$, the new point of the corner $v_i$ is $p(f, v_i) = \sum_j \alpha_{|i - j|} v_j$, with

$$\alpha_0 = \frac{1}{4} + \frac{5}{4k}, \qquad \alpha_m = \frac{3 + 2 \cos(2 \pi m / k)}{4k} \quad (0 < m < k).$$

```pseudo id=main
DOO-SABIN(M = (V, E, F))
L1  for each face f = (v_0, ..., v_(k−1)) and each i: p(f, v_i) ← Σ_j α_|i−j| v_j
L2  for each face f: add the F-face (p(f, v_0), ..., p(f, v_(k−1)))
L3  for each edge ab with a → b in face f and b → a in face g: add the E-face (p(f, b), p(f, a), p(g, a), p(g, b))
L4  for each vertex v: walk the faces around v, each time from the face g with u → v to the face f with v → u, and add the V-face of the points p(·, v) in that order
L5  return the new points and the faces
```

The orders in lines L3 and L4 make each new directed edge appear once with its reverse in a neighboring face, so the new mesh keeps the orientation. For quads, line L1 is the simple rule "average the corner, the centroid of the face and the two edge midpoints at the corner", with the weights $\frac{9}{16}$, $\frac{3}{16}$, $\frac{1}{16}$ and $\frac{3}{16}$. For triangles the weights are $\frac{2}{3}$, $\frac{1}{6}$ and $\frac{1}{6}$, and for hexagons $\frac{11}{24}$, $\frac{1}{6}$, $\frac{1}{12}$, $\frac{1}{24}$, $\frac{1}{12}$ and $\frac{1}{6}$.

## Example

Take the cube $[-1, 1]^3$ with $V = 8$, $E = 12$ and $F = 6$, so $\chi = 2$. All faces are quads.

- **Line L1.** The face $x = -1$ has the corners $(-1, -1, -1)$, $(-1, -1, 1)$, $(-1, 1, 1)$ and $(-1, 1, -1)$. The new point at $(-1, -1, -1)$ is $\frac{9}{16}(-1, -1, -1) + \frac{3}{16}\big((-1, -1, 1) + (-1, 1, -1)\big) + \frac{1}{16}(-1, 1, 1) = (-1, -\frac{1}{2}, -\frac{1}{2})$. By symmetry, the 24 new points are all points with one coordinate $\pm 1$ and the other two $\pm \frac{1}{2}$.
- **Line L2.** Each face becomes the square of side 1 in its middle, for example the square with $y, z \in \{-\frac12, \frac12\}$ on $x = -1$.
- **Line L3.** The edge from $(-1, -1, -1)$ to $(-1, -1, 1)$ is in the faces $x = -1$ and $y = -1$, and its E-face is the rectangle on $(-1, -\frac12, \pm\frac12)$ and $(-\frac12, -1, \pm\frac12)$.
- **Line L4.** The vertex $(-1, -1, -1)$ has valence 3, and its V-face is the triangle on $(-1, -\frac12, -\frac12)$, $(-\frac12, -1, -\frac12)$ and $(-\frac12, -\frac12, -1)$.

The new mesh has $V' = 2 \cdot 12 = 24$ vertices, $E' = 48$ edges and $F' = 6 + 12 + 8 = 26$ faces: 18 quads and 8 triangles, so it is a rhombicuboctahedron in its combinatorics, and $\chi = 24 - 48 + 26 = 2$. The 8 triangles are extraordinary faces. A second step gives 96 vertices, 192 edges and 98 faces, and the 8 triangles shrink but stay triangles.

## Correctness

The proof file shows four facts. First, the F-faces, E-faces and V-faces form a closed oriented 2-manifold, and each new vertex is in exactly four faces. Second, $V' = 2E$, $E' = 4E$ and $F' = F + E + V$, so the [Euler characteristic](/euler-formula/) is kept. Third, the weights of each face sum to 1, and for quads they are the simple average rule. Fourth, on a regular quad grid each new point is the tensor product of the [Chaikin](/chaikin-corner-cutting/) weights $(\frac34, \frac14)$, and the new faces are the cells of the fine grid, so a step is [knot refinement](/knot-refinement/) of a biquadratic uniform B-spline surface. The limit on the regular part is that surface, which is $C^1$.

The limit is also $C^1$ at the center of an extraordinary face. Doo and Sabin studied the [eigenvalues](/eigenvalue/) of the subdivision matrix there in 1978, and Peters and Reif gave a full proof in 1998 (check). The proof file does not repeat it.

## Complexity

- **One step, $O(E k)$ time.** Line L1 costs $(\deg f)^2$ for each face, and $\sum_f (\deg f)^2 \le k \sum_f \deg f = 2Ek$, where $k$ is the largest face size. Lines L2 to L4 cost $O(E)$, with a hash map from directed edges to faces for the walk. For bounded face sizes this is $\Theta(V + E + F)$.
- **Space, $\Theta(E)$.** The output has $2E$ points and $F + E + V$ faces with $8E$ corners in total.
- **$k$ steps.** After the first step every vertex has valence 4, so $E$ doubles with each later step, and the number of faces grows by a factor of about 4.

## Properties

- **Dual.** New faces correspond to old faces, edges and vertices. The old vertices do not survive, and no new point lies on an old vertex.
- **Approximating.** The limit does not pass through the control points.
- **Extraordinary faces.** After the first step every vertex has valence 4, and the extraordinary elements are the faces with $k \ne 4$ sides. The F-face of each of them keeps $k$ sides at every level, and it shrinks to a point of the limit surface.
- **Smoothness.** $C^1$ everywhere, as a biquadratic surface is. It is not $C^2$, even on the regular part.
- **Positive weights.** All weights are positive for $k \ge 3$, because $3 + 2 \cos x \ge 1$. So each new point is in the convex hull of its face, and the limit is in the convex hull of the mesh.
- **Local and affine.** Each new point depends on one face only, and the weights sum to 1.

## Variants and improvements

- **The simple rule for all faces.** Using the average of the corner, the centroid and the two edge midpoints for every face size is simpler. It equals the rule above for quads. For triangles it gives $\frac{7}{12}$ to the corner in place of $\frac{2}{3}$, and the behavior at extraordinary faces changes.
- **Boundaries.** For an open mesh, a boundary edge has no second face, and a common fix applies Chaikin's rule along the boundary polygon.
- **The curve case.** On a closed polygon, the dual scheme with the weights $(\frac34, \frac14)$ is [Chaikin's corner cutting](/chaikin-corner-cutting/), and the [Lane-Riesenfeld algorithm](/lane-riesenfeld-algorithm/) gives the higher degrees.
- **Other dual schemes.** Dual schemes of higher degree, and dual schemes for triangle meshes, use the same pattern of one new point per face corner with other weights.
- **The primal scheme.** [Catmull-Clark](/catmull-clark-subdivision/) is the bicubic primal scheme, with $C^2$ on the regular part.

## When to use it

Use it when you need a smooth surface from a mesh with faces of any size, and $C^1$ is enough. It has one simple rule, and each new point depends on one face only, so it is easy to code and to run in parallel. For a $C^2$ surface on the regular part, use Catmull-Clark. When the faces are triangles and must stay triangles, use [Loop](/loop-subdivision/) or [$\sqrt{3}$](/sqrt3-subdivision/).

## Pitfalls

- **Orientation of the new faces.** The E-face must list $p(f, b), p(f, a), p(g, a), p(g, b)$ in this order, and the V-face must walk from the face with the edge $u \to v$ to the face with the edge $v \to u$. With the wrong order, faces have inconsistent normals. The implementation checks that each directed edge is in one face only.
- **Wrong weight for the corner.** The weight of the corner has the extra term $\frac14$. Without it the weights sum to $\frac34$ and the mesh shrinks to the origin.
- **The walk at a vertex.** The walk around $v$ needs the face of the reverse edge at each step. On a mesh with boundary the walk stops at the boundary, and the V-face is not closed.
- **Shrinkage.** The limit is inside the convex hull of the mesh, and it can be much smaller than the cage. In the cube example the first step already moves every point off the corners and edges of the cube.
- **Floating point weights.** For face sizes other than 3, 4 and 6, the cosines are irrational, so the weights sum to 1 only up to rounding.

## Implementations

The Python file in this folder has `doo_sabin(vertices, faces)`, which follows the pseudocode, `doo_sabin_weights(k)`, `cos_turn(m, k)`, which returns $\cos(2\pi m / k)$ as a fraction when it is rational, `half_edges(faces)` and `euler_characteristic(faces)`. The tests check the cube example, the counts $V', E', F'$ and the Euler characteristic for one and two steps on six meshes, the weights for triangles, quads and hexagons against the values by hand, the quad rule against the simple average, random positions against the hand weights, and on random regular tori the full result against the tensor product of Chaikin's rule, with the new faces against the cells of the fine grid.

## History

Daniel Doo and Malcolm Sabin published the scheme in 1978 in Computer-Aided Design, in the same issue as the scheme of Catmull and Clark. Their paper also studied the behavior near extraordinary points with the eigenvalues of the subdivision matrix, which became the standard method for the analysis of subdivision surfaces. The full proofs of $C^1$ continuity at extraordinary points came in the 1990s, with the work of Reif and of Peters and Reif.

## References
