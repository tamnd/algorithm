---
tag: E9X6ZR
kind: algorithm
slug: sqrt3-subdivision
name: Sqrt(3) subdivision
aliases:
- Kobbelt sqrt(3) subdivision
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: Refines a closed triangle mesh by adding the centroid of each face, moving the old vertices and flipping the old edges. The face count grows by a factor of 3, and two steps split each face into 9.
solves: [surface-from-control-mesh]
model: real-ram
complexity:
  vars: {V: the number of vertices, E: the number of edges, F: the number of faces}
  time: {worst: Θ(V + E + F)}
  space: {extra: Θ(V + E + F)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 2000
  people: [Leif Kobbelt]
  note: Leif Kobbelt presented the scheme at SIGGRAPH 2000, with the vertex weight alpha_n, a boundary rule and an adaptive refinement that uses the slower growth of the mesh.
prereqs: [polygon-mesh, b-spline, subdivision-surface]
see_also: [subdivision-surface, surface-from-control-mesh, loop-subdivision, butterfly-subdivision, catmull-clark-subdivision, doo-sabin-subdivision, euler-formula, eigenvalue]
sources:
  - paper: doi:10.1145/344779.344835
    title: Leif Kobbelt, sqrt(3)-subdivision, Proceedings of SIGGRAPH 2000, 103-112 (2000)
    locator: the centroid insertion and the edge flip, the vertex weight alpha_n = (4 - 2 cos(2 pi / n)) / 9, the limit point rule, the boundary rule and the adaptive refinement
  - book: isbn:9783540764052
    title: Jörg Peters and Ulrich Reif, Subdivision Surfaces, Springer, 2008
    locator: the analysis of the subdivision matrix and the characteristic map, which decides the C1 property at extraordinary vertices (check)
  - book: isbn:9781558604469
    title: Joe Warren and Henrik Weimer, Subdivision Methods for Geometric Design, A Constructive Approach, Morgan Kaufmann, 2002
    locator: the general setting of subdivision on triangle meshes and of the analysis near extraordinary vertices
---

Sqrt(3) subdivision refines a closed triangle [polygon mesh](/polygon-mesh/) by putting a new point at the centroid of each triangle, moving each old vertex toward its neighbors, and flipping every old edge so that it joins the two new points on its sides. Each step multiplies the number of triangles by 3, not by 4 as in [Loop subdivision](/loop-subdivision/), so the edges get shorter by a factor of about $\sqrt{3}$, and the name comes from that. Two steps together split each triangle into 9, as a triadic split does. The limit is $C^2$ where all vertices have valence 6, and $C^1$ at the other vertices (check).

## In plain words

Start with a coarse cage of triangles. Put a new point in the middle of each triangle. Pull each old corner a little toward the corners around it. Then, for each old edge, drop the edge and join the two middle points on its two sides instead. Each old triangle becomes three thinner triangles, and each of them shares a side with a triangle from the next old triangle.

Do it again, and again. The cage gets finer more slowly than with other schemes, so it is easy to stop at the size you need. The surface it settles on is smooth.

## The problem

The input is a triangle mesh $M = (V, E, F)$ with $V$ vertices, $E$ edges and $F$ triangles. The mesh is a closed oriented 2-manifold: each edge is in exactly two triangles, with opposite directions, and the triangles around each vertex form one cycle. Then $3F = 2E$. The output is the mesh after one step, also a closed oriented 2-manifold, with $V + F$ vertices and $3F$ triangles. The limit of repeated steps is the [subdivision surface](/subdivision-surface/) of $M$.

The model is the [real RAM](/real-ram/), and the unit of work is one addition or scaling of a point. With rational coordinates the new points are rational for the valences 3, 4 and 6.

## The algorithm

For a vertex $v$ of valence $n$, the weight of its ring is
$$\alpha_n = \frac{4 - 2 \cos(2\pi / n)}{9}.$$

```pseudo id=main
SQRT3(M = (V, E, F))
L1  for each triangle f = (a, b, c): face point c_f ← (a + b + c) / 3
L2  for each vertex v with the neighbors u_1, ..., u_n: vertex point v' ← (1 − α_n) v + (α_n / n)(u_1 + ... + u_n)
L3  for each edge ab with a → b in the triangle f and b → a in the triangle g: add (c_f, a', c_g) and (c_g, b', c_f)
L4  return the new points and the new triangles
```

Lines L1 and L2 use only the old points, so they can run in any order, and in parallel. Line L3 is the edge flip: the old edge $ab$ is replaced by the edge $c_f c_g$, and the two new triangles keep the orientation of $f$ and $g$. The weights give $\alpha_3 = \frac59$, $\alpha_4 = \frac49$ and $\alpha_6 = \frac13$, so a regular vertex keeps $\frac23$ of itself and takes $\frac{1}{18}$ of each of its six neighbors.

## Example

Take the regular tetrahedron with the vertices $p_0 = (1, 1, 1)$, $p_1 = (1, -1, -1)$, $p_2 = (-1, 1, -1)$ and $p_3 = (-1, -1, 1)$, and the triangles $f_0 = (0,1,2)$, $f_1 = (0,3,1)$, $f_2 = (0,2,3)$ and $f_3 = (1,3,2)$. It has $V = 4$, $E = 6$ and $F = 4$, it is a closed 2-manifold with $\chi = 4 - 6 + 4 = 2$, and every vertex has valence $n = 3$.

| Step | Item | Rule | Value |
|---|---|---|---|
| L1 | centroid of $f_0$ | $(p_0 + p_1 + p_2)/3$ | $(\frac13, \frac13, -\frac13)$ |
| L1 | centroid of $f_1$ | $(p_0 + p_3 + p_1)/3$ | $(\frac13, -\frac13, \frac13)$ |
| L2 | vertex $p_0$ | $\alpha_3 = \frac59$, so $\frac49 p_0 + \frac{5}{27}(p_1 + p_2 + p_3)$ | $\frac49(1,1,1) - \frac{5}{27}(1,1,1) = \frac{7}{27}(1, 1, 1)$ |
| L3 | edge $p_0 p_1$ | $0 \to 1$ is in $f_0$ and $1 \to 0$ is in $f_1$ | triangles $(c_{f_0}, p_0', c_{f_1})$ and $(c_{f_1}, p_1', c_{f_0})$ |

The new mesh has $V' = 4 + 4 = 8$ vertices, $E' = 6 + 3 \cdot 4 = 18$ edges and $F' = 12$ triangles, so $\chi = 8 - 18 + 12 = 2$. The 4 old vertices keep valence 3, and the 4 centroids have valence 6. A second step gives $V = 20$, $E = 54$ and $F = 36 = 9 \cdot 4$. The corner moves from distance $\sqrt3 \approx 1.73$ to $\frac{7\sqrt3}{27} \approx 0.45$ from the center, and its limit point is $(\frac16, \frac16, \frac16)$, at distance $\approx 0.29$.

## Correctness

The proof file shows five facts. First, the triangles of line L3 form a closed oriented 2-manifold, in which each old vertex keeps its valence and each centroid has valence 6. Second, $V' = V + F$, $E' = E + 3F$ and $F' = 3F$, so $V' - E' + F' = V - E + F$, and the [Euler characteristic](/euler-formula/) is kept. Third, the weights sum to 1, and the cosine formula gives $\frac59$, $\frac49$ and $\frac13$ for the valences 3, 4 and 6. Fourth, the value $\frac{v + 3\alpha_n \bar u}{1 + 3\alpha_n}$, with the mean $\bar u$ of the neighbors, does not change in a step, so it is the limit point of $v$. Fifth, on the regular planar mesh of $\mathbb{Z}^2$ the points do not move, and two steps give exactly the regular mesh of $\frac13 \mathbb{Z}^2$, with two new points on each old edge at a third and two thirds of its length.

The limit is $C^2$ on the regular part, and Kobbelt chose $\alpha_n$ so that the limit is $C^1$ at an extraordinary vertex (check). The proof of both uses the eigenvalues of the subdivision matrix, and the proof file does not repeat it.

## Complexity

- **One step, $\Theta(V + E + F)$ time.** Each centroid costs 3 additions, each vertex point $n_v + 1$, and each edge flip $O(1)$. The sum $\sum_v n_v$ is $2E$. The lookup of the triangle at a directed edge uses a hash map, which is expected $O(1)$ per edge.
- **Space, $\Theta(V + E + F)$.** The output has $V + F$ points and $3F$ triangles.
- **$k$ steps.** Each step multiplies the number of triangles by 3, so $k$ steps make $3^k F$ triangles. To reach a given size, sqrt(3) subdivision takes about $\log_3$ steps where Loop takes $\log_4$, and it has more sizes to stop at.

## Properties

- **Approximating.** The old vertices move, so the limit does not pass through the control points.
- **Slow growth.** The number of triangles grows by a factor of 3 per step, and two steps give the same 9 times as many triangles as a triadic split, with the edges in the same directions as the first mesh. On a regular mesh of equilateral triangles, one step turns the edge directions by 30 degrees.
- **Small stencils.** A centroid uses 3 points, and a vertex point uses its 1-ring. An edge point of Loop subdivision uses 4 points, so the stencils here are smaller.
- **Extraordinary vertices are kept.** All centroids have valence 6, and the old vertices keep their valence.
- **Smoothness.** $C^2$ on the regular part and $C^1$ at extraordinary vertices (check).
- **Local and affine.** The weights sum to 1, so a step commutes with affine maps.
- **Convex hull.** All weights are positive, so each new point is in the convex hull of its stencil.
- **Limit points.** The limit point of a vertex is $\frac{v + 3\alpha_n \bar u}{1 + 3\alpha_n}$. For $n = 6$ it is $\frac12 v + \frac12 \bar u$.

## Variants and improvements

- **Adaptive refinement.** Kobbelt refines only the triangles that need it, and the slow growth gives a mesh without cracks between the refined and the coarse parts (check).
- **Boundaries.** Kobbelt gives a boundary rule that splits each boundary edge into three every second step, with univariate weights along the boundary (check).
- **Interpolating variant.** Labsik and Greiner gave an interpolating sqrt(3) scheme that keeps the old vertices, as the [butterfly scheme](/butterfly-subdivision/) does for the four-way split (check).
- **Other schemes.** [Loop subdivision](/loop-subdivision/) uses the four-way split and also gives $C^2$ on the regular part. [Catmull-Clark](/catmull-clark-subdivision/) and [Doo-Sabin](/doo-sabin-subdivision/) are the schemes for quads.

## When to use it

Use it when the mesh must grow slowly, for example to refine until a given size or error, or to refine only parts of a mesh. The stencils are small, so a step is cheap and easy to code on a half-edge or [doubly connected edge list](/doubly-connected-edge-list/). When the mesh must keep its edge directions at every step, or when the code already uses the four-way split, Loop subdivision is simpler to combine with other tools.

## Pitfalls

- **Wrong orientation of the flip.** The new triangles are $(c_f, a, c_g)$ and $(c_g, b, c_f)$, where $f$ has $a \to b$. Swapping $f$ and $g$ gives triangles with the wrong orientation. The implementation checks the result with the half-edge map.
- **Old points in place of new ones.** Lines L1 and L2 use the old points only. The centroids must use the old vertices, not the moved ones.
- **Edge flip on a boundary.** A boundary edge has only one triangle, so it cannot be flipped. Without the boundary rule the step is not defined, and the implementation rejects such meshes.
- **Odd and even steps.** After an odd number of steps the edges run in other directions than in the first mesh, which can look uneven on a coarse mesh. Compare meshes after an even number of steps.
- **Floating point weights.** For valences other than 3, 4 and 6, $\alpha_n$ is irrational, so the result is not exact.

## Implementations

The Python file in this folder has `sqrt3_subdivision(vertices, faces)`, which follows the pseudocode, `sqrt3_alpha(n)`, `half_edges(faces)`, which builds the map from directed edges to triangles and checks that the mesh is a closed oriented 2-manifold, and `euler_characteristic(faces)`. The new points are the moved old vertices and then the centroids in the order of the faces. The tests check the tetrahedron example, the counts $V', E', F'$ and the Euler characteristic for one and two steps on a tetrahedron, an octahedron, two bipyramids and two tori, the valences, the stencil weights against the hand computation, the limit point formula, and on a planar regular torus that two steps give the points of $\frac13 \mathbb{Z}^2$ with the six short edges at each inner point.

## History

Leif Kobbelt presented the scheme at SIGGRAPH 2000. He chose the centroid insertion with the edge flip for its slow growth and small stencils, and the weight $\alpha_n$ from the eigenvalues of the subdivision matrix. The paper also gave a boundary rule and an adaptive refinement. Later work gave an interpolating variant and analyzed the smoothness at extraordinary vertices.

## References
