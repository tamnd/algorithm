---
tag: ET5H6G
kind: technique
slug: parametric-surface-meshing
name: Surface meshing in parametric space
aliases:
- mesh generation on CAD surfaces
area: cad/mesh-generation-for-analysis
level: core
summary: Meshes each trimmed CAD face in its parameter domain under the metric of the first fundamental form, so the elements are well shaped on the surface.
prereqs: [parametric-surface, fundamental-forms, boundary-representation]
see_also: [trimmed-surface, nurbs, surface-curvature, anisotropic-mesh-adaptation, advancing-front-mesh-generation, delaunay-refinement, delaunay-surface-meshing, mesh-sizing-function]
sources:
  - book: isbn:978-1-84821-029-5
    title: Pascal Jean Frey and Paul-Louis George, Mesh Generation, Application to Finite Elements, 2nd edition, ISTE and Wiley, 2008
    locator: the chapters on curve and surface meshing, parametric surface meshing with a metric, and geometric size from curvature (general locator)
  - book: isbn:978-0-13-212589-5
    title: Manfredo P. do Carmo, Differential Geometry of Curves and Surfaces, Prentice Hall, 1976
    locator: section 2-5 (the first fundamental form) and chapter 3 (principal curvatures)
---

Surface meshing in parametric space makes a triangle or quad mesh of a CAD surface by working in the plane of its parameters. A CAD face is a map $S(u, v)$ from a region of the plane to space, usually a [NURBS](/nurbs/) patch, cut down by trimming curves. Meshing the flat parameter region is a 2D problem, which 2D meshers solve well. But the map stretches and shears: a nice triangle in the $(u, v)$ plane can be a long thin triangle on the surface. The fix is to mesh the parameter region under a metric, the first fundamental form of the surface divided by the square of the wanted size, so that the edges have the right length on the surface, not in the plane. The edges of the B-rep are meshed first and shared by the faces on both sides, so the face meshes fit together.

## In plain words

A map of the Earth is flat, but the Earth is round. Near the poles, a small square on a flat map covers a thin sliver of ground. If you draw nice triangles on the map and then wrap it around the globe, the triangles near the poles come out squashed.

Surface meshing has the same problem. Each curved face of a CAD model comes with a flat map. A mesher draws triangles on the flat map, then wraps them onto the face. To get nice triangles on the face, it measures every edge on the face, not on the map. The rule that turns a step on the map into a length on the face is the first fundamental form.

## When it applies

- The geometry is a [boundary representation](/boundary-representation/): faces with a [parametric surface](/parametric-surface/) $S(u, v)$ each, bounded by edges that are curves in space and, on each face, curves in the parameter plane.
- The map $S$ is smooth and regular on the face: the partial derivatives $S_u$ and $S_v$ are independent, so the first fundamental form is positive definite. Where this fails, at a pole or a collapsed edge, the method needs care.
- The 2D mesher can work with a variable metric in the parameter plane: it measures edge lengths and element shapes with a matrix field.

**The metric.** Let $J = [S_u \; S_v]$ be the $3 \times 2$ Jacobian of the map. A small step $\delta = (du, dv)$ in the parameter plane becomes the step $J\delta$ on the surface, whose squared length is $\delta^T G \delta$ with

$$G = J^T J = \begin{pmatrix} S_u \cdot S_u & S_u \cdot S_v \\ S_u \cdot S_v & S_v \cdot S_v \end{pmatrix},$$

the first fundamental form, see [fundamental forms](/fundamental-forms/). For an isotropic target size $h$ on the surface, the parameter metric is $M = G / h^2$, and an edge of the parameter mesh is unit when its surface length is about $h$. For a 3D metric $M_3$, as in [anisotropic mesh adaptation](/anisotropic-mesh-adaptation/), the parameter metric is the pull back $J^T M_3 J$. Both are exact for an infinitely small edge and accurate for an edge that is short compared with the radius of curvature.

**The size from curvature.** A straight edge of length $c$ between two points of a circle of radius $\rho$ is a chord, and the gap between the chord and the arc is $\rho - \sqrt{\rho^2 - c^2/4}$. Keeping this gap below a tolerance $\delta$ gives $c \le 2\sqrt{\delta(2\rho - \delta)}$. On a surface, $\rho$ is the radius of normal curvature in the direction of the edge, so in the two principal directions of [surface curvature](/surface-curvature/) the sizes can differ, and the size metric is anisotropic.

## The template

```pseudo id=main
MESH-FACE(face S on region Ω with trimming loops, size field h, tolerance δ)
L1  for each edge of the B-rep that bounds the face do
L2      if the edge is not yet meshed then place points along it in 3D, spaced by h and by the chord rule for δ
L3      map its points to the (u, v) plane of this face through the edge's curve on the face
L4  for each point (u, v) where the mesher asks for a metric do
L5      G ← J^T J with J = [S_u S_v] at (u, v)
L6      M ← G / h² intersected with the curvature metric from δ
L7  mesh Ω inside the trimming loops with a 2D mesher that uses M for lengths and shapes
L8  map each interior vertex to S(u, v), keep the connectivity
L9  check the elements on the surface; smooth or swap on the surface where needed
```

L2 to L3 make neighbouring faces conform: both faces take the same points on their shared edge. L7 is a metric version of a planar mesher, such as [advancing front mesh generation](/advancing-front-mesh-generation/) or [Delaunay refinement](/delaunay-refinement/). L9 is needed because the parameter metric is only correct to first order on a curved surface.

## Classic examples

**A cylinder.** For $S(u, v) = (R\cos u, R\sin u, v)$, $S_u = (-R\sin u, R\cos u, 0)$ and $S_v = (0, 0, 1)$, so $G = \mathrm{diag}(R^2, 1)$. Take $R = 2$ and $h = 0.5$. A triangle that is equilateral with side $0.5$ in the $(u, v)$ plane maps to a triangle with sides $0.990$, $0.660$ and $0.660$ on the cylinder, with mean ratio $0.810$: the $u$ direction is stretched by $R = 2$. A triangle that is equilateral in the metric $G/h^2$, with a $u$ step of $h/R = 0.25$, maps to sides $0.499$, $0.500$ and $0.500$ and mean ratio $0.99999$. With a chord tolerance $\delta = 0.01$, the circumferential size must also be at most $2\sqrt{0.01 \cdot 3.99} \approx 0.3995$, while the axial direction has no curvature and keeps $0.5$. The parameter metric is then $\mathrm{diag}(R^2/0.3995^2, 1/0.5^2) \approx \mathrm{diag}(25.06, 4)$.

**A sphere and its poles.** For the unit sphere with longitude $u$ and latitude $v$, $G = \mathrm{diag}(\cos^2 v, 1)$. At the equator, the equilateral parameter triangle with side $0.1$ keeps mean ratio $0.99999$. At latitude $1.2$ radians, the same parameter triangle has mean ratio $0.643$, because the $u$ direction shrinks by $\cos v \approx 0.36$. At the pole, $\cos v = 0$, $G$ is singular, and the whole line $v = \pi/2$ of the parameter plane maps to one point. The metric mesher must then make the $u$ edges near the pole very long, which a 2D mesher handles badly. Common fixes are to split the face so that the pole is a vertex of a small cap, or to mesh the cap with another parametrisation.

**Seams of periodic faces.** A full cylinder has $u \in [0, 2\pi]$, and the lines $u = 0$ and $u = 2\pi$ are the same curve, the seam. The parameter region is a rectangle in which the seam appears twice, as the left and right sides, and both copies take the same points, so the mesh closes up on the surface.

**Trimmed faces.** A face with a hole, such as a plate with a drilled hole, is the region of the parameter plane inside the outer trimming loop and outside the inner one. See [trimmed surfaces](/trimmed-surface/). The mesher meshes this planar region with holes; the trimming curves are given in the parameter plane, so no 3D intersection is needed at meshing time.

## Variations

- **Direct 3D meshing.** An advancing front can work on the surface itself, placing new points by projection onto $S$. It avoids the parameter distortion, at the cost of a point projection per new point.
- **Combined method.** Borouchaki, Laug and George mesh the parameter plane with an anisotropic generalised Delaunay method combined with an advancing front for point placement, under the metric induced by the surface and its curvature.
- **Quad meshes.** Paving or Q-Morph in the parameter plane, under the metric, give quad meshes of CAD faces; see [paving](/paving/) and [Q-Morph](/q-morph/).
- **Discrete surfaces.** When the surface is a triangulation, not a parametric patch, [Delaunay surface meshing](/delaunay-surface-meshing/) and remeshing on the triangulation take the place of the parameter plane.

## Pitfalls

- **Ignoring the metric.** Meshing the $(u, v)$ plane as if it were flat gives stretched triangles on the surface wherever $|S_u| \ne |S_v|$ or $S_u \cdot S_v \ne 0$.
- **Degenerate points.** Poles and collapsed edges have a singular $G$. Detect them and split the face, or mesh a small region around them in another way.
- **Mismatched edges.** If two faces mesh their shared edge separately, the meshes do not conform. Mesh each B-rep edge once, in 3D, and give the same points to both faces.
- **Bad parametrisations.** A NURBS patch with uneven knot spacing or nearly dependent derivatives has a metric that changes fast. The 2D mesher then needs many tries, and the first order metric is inaccurate. Check the elements in 3D.
- **Tolerance gaps.** CAD faces often meet only within a tolerance, so the 3D points of an edge do not lie exactly on the face. Map them to the face by its trimming curve, not by projection only.
- **Chord rule only.** A size from the chord rule alone can be huge on a flat region. Combine it with the physics size field and clip it.

## Exercises

- For a surface of revolution $S(u, v) = (r(v)\cos u, r(v)\sin u, z(v))$, compute $G$, and show that $G$ is singular exactly where $r(v) = 0$.
- Derive the chord rule $c \le 2\sqrt{\delta(2\rho - \delta)}$ from the right triangle formed by the centre of the circle, the midpoint of the chord and one end of the chord.

## References
