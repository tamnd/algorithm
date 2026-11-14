---
tag: E53E2T
kind: definition
slug: discrete-gaussian-curvature
name: Discrete Gaussian curvature
aliases:
- angle defect
- angular deficit
area: cad/mesh-processing
level: core
summary: At a mesh vertex, 2 pi minus the sum of the angles of its faces at that vertex, divided by an area or taken as a concentrated curvature.
prereqs: [polygon-mesh, manifold-mesh, surface-curvature]
see_also: [discrete-gauss-bonnet-theorem, cotangent-laplacian, euler-poincare-formula, convex-polytope, isotropic-remeshing, discrete-geodesic-problem]
sources:
  - paper: doi:10.1007/978-3-662-05105-4_2
    title: Mark Meyer, Mathieu Desbrun, Peter Schröder and Alan H. Barr, Discrete differential-geometry operators for triangulated 2-manifolds, in Visualization and Mathematics III (H.-C. Hege and K. Polthier, eds.), Springer, 2003, 35 to 57
    locator: the discrete Gaussian curvature operator, the angle defect divided by the mixed Voronoi area
  - paper: "Vincent Borrelli, Frédéric Cazals and Jean-Marie Morvan, On the angular defect of triangulations and the pointwise approximation of curvatures, Computer Aided Geometric Design 20, 2003, 319 to 341"
    locator: the conditions on the triangles around a vertex under which the angle defect over the area converges to the Gaussian curvature, and the counterexamples (general locator)
  - book: isbn:9781568814261
    title: Mario Botsch, Leif Kobbelt, Mark Pauly, Pierre Alliez and Bruno Lévy, Polygon Mesh Processing, AK Peters, 2010
    locator: Chapter 3, Differential Geometry (discrete curvatures, the angle deficit as Gaussian curvature)
  - book: isbn:9780132125895
    title: Manfredo P. do Carmo, Differential Geometry of Curves and Surfaces, Prentice-Hall, 1976
    locator: Section 3-3 (the Gaussian curvature as the limit of the area of the Gauss image over the area) and Section 4-5 (the local Gauss-Bonnet theorem with the geodesic curvature of the border)
---

The discrete Gaussian curvature of a mesh is a number at each vertex: $2\pi$ minus the sum of the angles of the faces at that vertex. This number is the *angle defect*. A vertex where the faces close up flat, like a point of a plane, has defect 0. A corner of a cube has three right angles, so its defect is $2\pi - 3\pi/2 = \pi/2$. The defect is the total [Gaussian curvature](/surface-curvature/) that the mesh concentrates at the vertex, so it is the integral of $K$ over a small region, not a value of $K$. Dividing it by an area of the vertex gives an estimate of $K$ itself. The defects of a closed mesh always sum to $2\pi\chi$, which is the [discrete Gauss-Bonnet theorem](/discrete-gauss-bonnet-theorem/).

## Definition

Let $M$ be a [polygon mesh](/polygon-mesh/) whose faces are planar, simple polygons, for example a triangle mesh. For a vertex $i$ and a face $f$ that contains it, let $\theta_i^f \in (0, \pi)$ be the interior angle of $f$ at $i$. The *angle sum* of $i$ is $\Theta_i = \sum_{f \ni i} \theta_i^f$.

**Angle defect.** For an inner vertex $i$ of a [manifold mesh](/manifold-mesh/), whose faces form a closed fan,

$$K_i = 2\pi - \Theta_i .$$

$K_i$ is the *discrete Gaussian curvature*, or *concentrated curvature*, of $i$. Cut the fan of faces open along one edge and lay it in the plane: it is a flat sector of angle $\Theta_i$, and $K_i$ is the angle of the gap that is missing to close a full disk.

**At a border vertex.** For a border vertex $i$, whose faces form an open fan, the number

$$\kappa_i = \pi - \Theta_i$$

is the turning angle of the border curve at $i$ inside the surface, which is a discrete *geodesic curvature* of the border. It is not a Gaussian curvature: a flat square has $\kappa = \pi/2$ at each corner and no Gaussian curvature at all. The two kinds of term appear together in the Gauss-Bonnet sum, where $\kappa$ plays the role of $\int k_g \, ds$ in the smooth theorem (do Carmo, Section 4-5).

**Area-normalized form.** To estimate the pointwise curvature $K$ at vertex $i$, divide by an area $A_i$ that the vertex stands for:

$$\tilde K_i = \frac{K_i}{A_i} .$$

The usual areas are the barycentric area, one third of the area of the triangles at $i$, and the mixed Voronoi area of Meyer, Desbrun, Schröder and Barr (2003), defined on the [cotangent Laplacian](/cotangent-laplacian/) page. Both sum to the total area of the mesh.

**Why it is a Gaussian curvature.** On a smooth surface, $K$ at a point is the limit of the area of the Gauss image of a small region, the set of its unit normals on the sphere, over the area of the region (do Carmo, Section 3-3). At a convex vertex of a polyhedron, the normals of the faces around $i$ span a spherical polygon whose sides are the arcs between the normals of neighbouring faces. The exterior angle of this polygon at the normal of face $f$ is $\theta_i^f$, so by the area formula for spherical polygons its area is $2\pi - \sum_f \theta_i^f = K_i$. So the angle defect is the area of the Gauss image of the vertex, which is the integral of $K$ over a neighbourhood that collapses onto the vertex.

**Properties.**

- *Sign.* $K_i > 0$ when the angle sum is less than $2\pi$, as at a vertex of a [convex polytope](/convex-polytope/), where $0 < K_i < 2\pi$. $K_i = 0$ when the fan is flat after cutting. $K_i < 0$ when the angles sum to more than $2\pi$, as at a saddle.
- *Intrinsic.* $\Theta_i$ depends only on the edge lengths of the faces at $i$, by the law of cosines. So bending the mesh without stretching, for example folding a flat sheet along an edge, does not change $K_i$. This is the discrete form of Gauss's Theorema Egregium. It also means that the defect cannot tell a bump from a dent: pushing a vertex of a flat grid up or down by the same amount gives the same defect.
- *Total.* For a closed mesh, $\sum_i K_i = 2\pi\chi$ with $\chi = V - E + F$. With a border, $\sum_{\text{inner}} K_i + \sum_{\text{border}} \kappa_i = 2\pi\chi$. The proof is on the [discrete Gauss-Bonnet theorem](/discrete-gauss-bonnet-theorem/) page.
- *Scale.* $K_i$ has no unit: scaling the mesh does not change it, while $A_i$ scales by the square. Refining a mesh spreads the same total over more vertices, so each $K_i$ gets smaller, and only $K_i / A_i$ has a limit.

## Examples and non-examples

**The five Platonic solids.** At each vertex all faces are regular, so the defects are exact multiples of $\pi$. Each total is $4\pi$, since $\chi = 2$.

| solid | faces at a vertex | angle sum | defect $K_i$ | vertices | total |
|---|---|---|---|---|---|
| tetrahedron | 3 triangles | $\pi$ | $\pi$ | 4 | $4\pi$ |
| cube | 3 squares | $3\pi/2$ | $\pi/2$ | 8 | $4\pi$ |
| octahedron | 4 triangles | $4\pi/3$ | $2\pi/3$ | 6 | $4\pi$ |
| dodecahedron | 3 pentagons | $9\pi/5$ | $\pi/5$ | 20 | $4\pi$ |
| icosahedron | 5 triangles | $5\pi/3$ | $\pi/3$ | 12 | $4\pi$ |

**Flat and folded.** An inner vertex of a grid of equilateral triangles has six angles of $\pi/3$, so $K = 0$. Fold the grid along a line of edges through the vertex: the six angles do not change, and $K$ is still 0, although the surface now has a crease.

**A saddle.** Put the vertex at the origin with the four neighbours $(1, 0, 1)$, $(0, 1, -1)$, $(-1, 0, 1)$, $(0, -1, -1)$ in this order, alternately up and down. Each pair of neighbouring vectors has dot product $-1$ and lengths $\sqrt{2}$, so each angle is $2\pi/3$. The angle sum is $8\pi/3$ and $K = -2\pi/3$.

**Border vertices.** A corner of a flat square sheet has $\kappa = \pi - \pi/2 = \pi/2$. A vertex in the middle of a straight side, with two triangles of angle $\pi/2$ each, has $\kappa = 0$. Neither value is a Gaussian curvature.

**Area-normalized values on a sphere.** The octahedron with vertices on the unit sphere has $K_i = 2\pi/3$ and barycentric area $2/\sqrt{3}$, so $\tilde K_i = \pi/\sqrt{3} \approx 1.814$, against $K = 1$ for the sphere. The icosahedron gives $\pi/3$ over $0.7979$, about $1.312$. On the icospheres made by cutting each triangle of the icosahedron into four and projecting to the unit sphere, the measured values at the twelve vertices of valence 5 are:

| level | vertices | $K_i / A_i$, barycentric | $K_i / A_i$, mixed Voronoi |
|---|---|---|---|
| 1 | 42 | 1.180 | 1.070 |
| 2 | 162 | 1.154 | 1.017 |
| 3 | 642 | 1.148 | 1.004 |
| 4 | 2562 | 1.146 | 1.001 |

With the barycentric area the estimate at these vertices does not tend to 1, because the triangles around them are not of equal size, while at the vertices of valence 6 it is within $0.3\%$ of 1 at level 4. This is a case of the general fact proved by Borrelli, Cazals and Morvan (2003): $K_i / A_i$ converges to $K$ only under conditions on the shape of the triangles around the vertex, and not for every refinement.

**Non-example: a skew face.** If a quadrilateral face is not planar, its four angles sum to less than $2\pi$, and the definition, which takes the angles of planar faces, does not apply. Triangulate such faces first. The [Gauss-Bonnet page](/discrete-gauss-bonnet-theorem/) shows that the total then fails.

**Non-example: the defect as a pointwise value.** Take a sphere mesh and cut each triangle into four. The defect at an old vertex falls by about a factor of 4, since the same total curvature is now spread over four times as many vertices, while the curvature of the sphere stays the same. Thresholds on $K_i$ without the area, for feature detection or for [remeshing](/isotropic-remeshing/), change with the density of the mesh.

## Related definitions

- [Surface curvature](/surface-curvature/): the smooth Gaussian curvature $K$ and mean curvature $H$. The angle defect is the discrete form of $\int K \, dA$.
- [Cotangent Laplacian](/cotangent-laplacian/): its value on the positions gives the discrete mean curvature normal, the companion of the angle defect. Together they estimate both principal curvatures.
- [Discrete Gauss-Bonnet theorem](/discrete-gauss-bonnet-theorem/): the sum of all defects is $2\pi\chi$, exactly, for every mesh.
- [Euler-Poincaré formula](/euler-poincare-formula/): the value of $\chi = V - E + F$ for solids with holes, handles and several shells.
- [Discrete geodesic problem](/discrete-geodesic-problem/): shortest paths on a mesh pass straight through no vertex of positive defect, and can bend only at vertices of negative defect or on the border.

## References
