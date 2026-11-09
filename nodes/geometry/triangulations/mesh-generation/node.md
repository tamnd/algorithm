---
tag: 3384M3
kind: problem
slug: mesh-generation
name: Mesh generation
aliases:
- Delaunay mesh generation
- Quality mesh generation
- Triangular mesh generation
- unstructured mesh generation
area: geometry/triangulations
level: core
summary: Produce a triangulation of a domain whose triangles have bounded angles and sizes.
model: real-ram
complexity:
  vars: {n: the number of input vertices and segments, m: the number of output triangles}
  time: {worst: O(n log n + m)}
prereqs: [triangulation, constrained-triangulation, steiner-points, delaunay-triangulation]
see_also: [ruppert-algorithm, chew-second-algorithm, delaunay-refinement, conforming-delaunay-triangulation, constrained-delaunay-triangulation, max-min-angle-triangulation, minimum-steiner-triangulation, tetrahedralization]
sources:
  - paper: doi:10.1016/S0925-7721(01)00047-5
    title: Jonathan Richard Shewchuk, Delaunay refinement algorithms for triangular mesh generation, Computational Geometry 22(1-3), 21 to 74 (2002)
    locator: Section 1 (quality measures and the history of provably good meshing), Section 3 (Ruppert's algorithm) and Section 4 (Chew's second algorithm)
  - paper: doi:10.1006/jagm.1995.1021
    title: Jim Ruppert, A Delaunay refinement algorithm for quality 2-dimensional mesh generation, Journal of Algorithms 18(3), 548 to 585 (1995)
    locator: the angle bound for inputs without acute angles, and size optimality
  - paper: "Marshall Bern, David Eppstein and John Gilbert, Provably good mesh generation, Journal of Computer and System Sciences 48(3), 384 to 409 (1994)"
    locator: the quadtree method, the first size-optimal mesh generator
  - paper: "Brenda S. Baker, Eric Grosse and Conor S. Rafferty, Nonobtuse triangulation of polygons, Discrete and Computational Geometry 3, 147 to 168 (1988)"
    locator: the first provably good meshing algorithm (angle bounds to be checked)
  - book: isbn:9781584887300
    title: Siu-Wing Cheng, Tamal K. Dey and Jonathan Richard Shewchuk, Delaunay Mesh Generation, CRC Press, 2012
    locator: Chapters 1 (introduction), 6 (2D Delaunay refinement) and later chapters on tetrahedral meshes (ISBN to be checked)
  - paper: "Sariel Har-Peled and Alper Üngör, A time-optimal Delaunay refinement algorithm in two dimensions, Proceedings of the 21st Symposium on Computational Geometry, 228 to 236 (2005)"
    locator: O(n log n + m) time (pages to be checked)
---

Mesh generation is the problem of cutting a geometric domain into triangles (or, in space, tetrahedra) that are well shaped and well sized, so that a numerical method can run on them. The domain is usually given as a planar straight-line graph: a set of vertices and segments that bound the region and mark internal boundaries. The output must respect every segment, may use new vertices, called [Steiner points](/steiner-points/), and must have no angle smaller than a prescribed bound, except where the input itself has a small angle. The standard methods are [Delaunay refinement](/delaunay-refinement/) algorithms, [Ruppert's](/ruppert-algorithm/) and [Chew's](/chew-second-algorithm/), which guarantee angles of about 20.7 and 26.5 degrees under stated hypotheses, and quadtree methods.

## In plain words

Engineers who simulate heat, stress or air flow cut the shape they study into many small triangles and solve simple equations on each one. The answer is only accurate if no triangle is too thin and if the triangles are small where the shape has fine detail. Mesh generation produces such a set of triangles.

The input is the outline of the shape, with any inner lines that must stay visible. The program may add new corners anywhere inside. It must keep every triangle fat, and it should use as few triangles as it can, so small ones only where the shape is tight and large ones elsewhere.

## Definition

**Input.** A planar straight-line graph (PSLG) $X$: a finite set of vertices and a set of segments between them, such that two segments meet only at a common end point and no vertex lies inside a segment. The domain $\Omega$ is the region to mesh, typically the union of the bounded faces of $X$ or the convex hull of $X$.

**Output.** A triangulation $T$ of $\Omega$ whose vertex set contains the vertices of $X$ and possibly Steiner points, such that every segment of $X$ is a union of edges of $T$, and such that every triangle has good quality.

**Quality.** The two usual measures of a triangle are its smallest angle $\theta$ and its **circumradius-to-shortest-edge ratio** $\rho = R / \ell$, where $R$ is the circumradius and $\ell$ the length of the shortest edge. They are linked by $\rho = 1 / (2 \sin \theta)$, so a bound $\rho \le B$ is the same as $\theta \ge \arcsin(1 / (2B))$. The ratio is preferred in proofs and in code, because $\rho^2 \le B^2$ can be tested exactly on rational input. A lower bound $\theta$ on all angles also bounds the largest angle by $180° - 2\theta$.

**Size.** The **local feature size** $\mathrm{lfs}(p)$ of a point $p$ is the radius of the smallest disk centered at $p$ that meets two vertices or segments of $X$ that do not touch each other. A mesh is **nicely graded** if every edge near $p$ has length at least a constant times $\mathrm{lfs}(p)$, and **size-optimal** if it has at most a constant times as many triangles as the smallest mesh that meets the same angle bound.

## Variants

- **Conforming or constrained.** A conforming mesh is a true [Delaunay triangulation](/delaunay-triangulation/) whose edges cover the segments, as in Ruppert's original algorithm and the [conforming Delaunay triangulation](/conforming-delaunay-triangulation/). A constrained mesh is a [constrained Delaunay triangulation](/constrained-delaunay-triangulation/), as in Chew's algorithm, and needs fewer points.
- **Angle bounds only, or size too.** Some users ask only for a minimum angle; others also give a size function $h(p)$ that bounds the edge length near each point.
- **Nonobtuse meshes.** Ask for no angle larger than $90°$, which some finite volume methods need. Bern, Mitchell and Ruppert showed that every polygon has a nonobtuse triangulation with $O(n)$ triangles.
- **Quadrilateral meshes.** Cut the domain into quadrilaterals instead.
- **Tetrahedral meshes.** In three dimensions the domain is a piecewise linear complex, and the output is a [tetrahedralization](/tetrahedralization/). Delaunay refinement bounds the radius-edge ratio but cannot by itself remove slivers, and some polyhedra, such as the [Schönhardt polyhedron](/schonhardt-polyhedron/), need Steiner points even to be tetrahedralized.

## Examples

- **A thin rectangle.** The rectangle with corners $(0,0)$, $(8,0)$, $(8,1)$, $(0,1)$ has two triangulations without Steiner points, both with smallest angle $\arctan(1/8) \approx 7.13°$. Adding the 14 points $(i, 0)$ and $(i, 1)$ for $1 \le i \le 7$ and cutting each unit square by a diagonal gives 16 right isosceles triangles with smallest angle $45°$.
- **A square with a short slit.** Put a segment of length $\varepsilon$ in the middle of the unit square. The local feature size near the slit is about $\varepsilon$, so any mesh with a fixed angle bound has edges of length about $\varepsilon$ near the slit, and a nicely graded mesh grows the edges geometrically away from it. The number of triangles is then $O(\log(1/\varepsilon))$, not $O(1/\varepsilon^2)$.
- **Small input angles.** Two segments that meet at an angle of $5°$ force a triangle with an angle of at most $5°$ at their common end point. No algorithm can do better, so the guarantees exclude small input angles. Ruppert proved his guarantee for input angles of at least $90°$, and Shewchuk's analyses of Ruppert's and Chew's algorithms need at least $60°$; Shewchuk's modifications handle small angles in practice by keeping the bad triangles inside the small input angle.

## Known algorithms

| algorithm | output | guarantee | hypothesis |
|---|---|---|---|
| Baker, Grosse and Rafferty (1988) | grid based, uniform size | no obtuse angles and a fixed lower angle bound | polygons |
| Chew's first algorithm (1989) | constrained Delaunay, uniform size | smallest angle $30°$ | input angles at least $30°$ (to be checked) |
| Bern, Eppstein and Gilbert (1994) | quadtree, graded | size-optimal, angle bound about $18.4°$ | polygons, apart from small input angles |
| [Ruppert](/ruppert-algorithm/) (1995) | conforming Delaunay | $\rho \le B$ for every $B \ge \sqrt{2}$, so about $20.7°$; graded and size-optimal for $B > \sqrt{2}$ | no input angle less than $90°$ (Shewchuk: $60°$ suffices) |
| [Chew's second algorithm](/chew-second-algorithm/) (1993) | constrained Delaunay | $30°$ with off-center splits; Shewchuk: $\rho \le B$ for $B \ge \sqrt{5}/2$, about $26.57°$, graded and size-optimal below that angle | no input angle less than $60°$ |
| Har-Peled and Üngör (2005) | Delaunay | Ruppert-type quality | $O(n \log n + m)$ time |

In practice the Delaunay refinement algorithms reach a smallest angle of about $33°$ or more before they fail to terminate, much better than the proven bounds.

## Bounds

- **Output size.** For a fixed angle bound, the smallest mesh of $\Omega$ has $\Theta\!\left(\int_\Omega \mathrm{lfs}(p)^{-2} \, dp\right)$ triangles. Size-optimal algorithms reach this up to a constant that depends on the angle bound.
- **No bound in $n$.** The output size cannot be bounded by a function of $n$ alone: the slit example shows that it depends on the geometry. Algorithms are therefore measured by $n$ and the output size $m$.
- **Time.** Building the initial constrained Delaunay triangulation takes $O(n \log n)$, and good implementations then spend $O(1)$ amortized time per inserted vertex in practice. Har-Peled and Üngör proved $O(n \log n + m)$ in the worst case.

## Reductions

- **From constrained triangulation.** Every Delaunay refinement method starts from a [constrained triangulation](/constrained-triangulation/) or a Delaunay triangulation of the input vertices.
- **To point placement.** Given a Delaunay triangulation, the question is only where to put the next Steiner point. Placing it at the circumcenter of a bad triangle is as far as possible from the existing vertices, and that is why Delaunay refinement terminates.
- **Lower bounds on Steiner points.** Without a quality bound, the fewest triangles with Steiner points is the [minimum Steiner triangulation](/minimum-steiner-triangulation/) problem, which is NP-hard for polygons with holes.

## Applications

- **Finite element and finite volume methods.** Small angles make the stiffness matrix ill conditioned, and large angles hurt the interpolation error of gradients.
- **Computer graphics.** Surface meshes for rendering and for geometry processing.
- **Geographic information systems.** Terrain models that keep breaklines such as rivers and roads as segments.
- **Software.** Shewchuk's Triangle and the CGAL 2D mesh generator implement Delaunay refinement; TetGen and CGAL do tetrahedral meshes.

## References
