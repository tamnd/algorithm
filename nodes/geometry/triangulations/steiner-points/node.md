---
tag: YE79SK
kind: concept
slug: steiner-points
name: Steiner points
aliases:
- Steiner vertices
- Steiner point
- added vertices
area: geometry/triangulations
level: advanced
summary: Extra vertices added beyond the input points to improve a triangulation.
prereqs: [triangulation, triangulation-of-point-set, constrained-triangulation]
see_also: [mesh-generation, delaunay-refinement, conforming-delaunay-triangulation, minimum-steiner-triangulation, schonhardt-polyhedron, tetrahedralization, ruppert-algorithm, chew-second-algorithm]
sources:
  - paper: doi:10.1016/S0925-7721(01)00047-5
    title: Jonathan Richard Shewchuk, Delaunay refinement algorithms for triangular mesh generation, Computational Geometry 22(1-3), 21 to 74 (2002)
    locator: Section 1 (why Steiner points are needed for quality meshes) and Section 3 (size optimality)
  - paper: "Marshall Bern and David Eppstein, Mesh generation and optimal triangulation, in Computing in Euclidean Geometry, second edition, World Scientific, 47 to 123 (1995)"
    locator: the sections on Steiner triangulations, conforming triangulations and nonobtuse meshes (pages to be checked)
  - paper: "Erich Schönhardt, Über die Zerlegung von Dreieckspolyedern in Tetraeder, Mathematische Annalen 98, 309 to 312 (1928)"
    locator: a polyhedron with no tetrahedralization without new vertices
  - paper: "Herbert Edelsbrunner and Tiow Seng Tan, An upper bound for conforming Delaunay triangulations, Discrete and Computational Geometry 10(2), 197 to 213 (1993)"
    locator: O(m^2 n) Steiner points suffice for a conforming Delaunay triangulation
  - book: isbn:9781584887300
    title: Siu-Wing Cheng, Tamal K. Dey and Jonathan Richard Shewchuk, Delaunay Mesh Generation, CRC Press, 2012
    locator: Chapter 1 (Steiner points and their role) and Chapter 6 (size optimality; ISBN to be checked)
---

A Steiner point is a vertex of a triangulation that is not one of the input points. Adding Steiner points changes what a triangulation can achieve: a simple polygon or point set always has a triangulation on its own vertices, but the triangles may be forced to be thin, and an input segment may be impossible to keep in a Delaunay triangulation. With extra points one can bound every angle, make every triangle nonobtuse, make the mesh Delaunay while keeping the input segments, or, in three dimensions, tetrahedralize polyhedra that have no tetrahedralization at all. The cost is a larger output, and much of the theory is about how few Steiner points suffice. The name comes from the Steiner tree problem, where extra junction points shorten a network.

## In plain words

Sometimes the corners you are given are not enough to cut a shape into good triangles. A long thin rectangle cut corner to corner gives two long thin triangles, whatever you do. If you are allowed to add new corners of your own, you can place them along the long sides and in the middle, and then cut the rectangle into many triangles that are all close to equal-sided.

These added corners are called Steiner points. They are free to choose, but each one makes the result bigger, so good methods add only as many as needed.

## The idea

**Definition.** Let the input be a point set $S$, or a planar straight-line graph with vertex set $S$ and a set of segments. A triangulation of the input with Steiner points is a triangulation whose vertex set contains $S$, whose union is the same region, and in which every input segment is a union of edges. The vertices not in $S$ are the Steiner points. They may lie in the interior of the region, on input segments, or on the boundary.

**Counting.** In the plane, Steiner points never reduce the number of triangles of an edge-to-edge triangulation: a triangulation of a polygonal region with $n$ vertices and $h$ holes has $n + 2h - 2 + b + 2s$ triangles when $b$ Steiner points lie on the boundary and $s$ inside; see [minimum Steiner triangulation](/minimum-steiner-triangulation/). For a point set with $n$ points, $h$ of them on the hull, the count is $2n - h - 2$, and every interior Steiner point adds 2.

**What Steiner points buy.**

- **Angle bounds.** A domain with a small feature next to a long edge has thin triangles in every triangulation on its own vertices. With Steiner points, every planar domain whose input angles are not small can be meshed with all angles at least about $20.7°$ by [Ruppert's algorithm](/ruppert-algorithm/), and nonobtuse meshes always exist (Baker, Grosse and Rafferty; Bern, Mitchell and Ruppert).
- **Conforming Delaunay.** A segment of the input may not be an edge of the Delaunay triangulation of the vertices. Splitting it with Steiner points until every piece is a Delaunay edge gives a [conforming Delaunay triangulation](/conforming-delaunay-triangulation/); $O(m^2 n)$ points suffice for $n$ vertices and $m$ segments (Edelsbrunner and Tan).
- **Existence in space.** Some polyhedra cannot be cut into tetrahedra using only their vertices; the [Schönhardt polyhedron](/schonhardt-polyhedron/) is the smallest. One Steiner point inside fixes it, and some polyhedra need $\Omega(n^2)$ (Chazelle). See [tetrahedralization](/tetrahedralization/).
- **Smaller weight.** A minimum weight Steiner triangulation can be much lighter than the [minimum weight triangulation](/min-weight-triangulation/) of the points alone.

**How many.** Delaunay refinement places Steiner points at circumcenters and segment midpoints, and the number it adds is within a constant factor of the minimum needed for its angle bound: it is **size-optimal**. The bound is in terms of the local feature size $\mathrm{lfs}(p)$, the radius of the smallest disk centered at $p$ that meets two disjoint features of the input. The output has $\Theta\left(\int 1/\mathrm{lfs}(p)^2 \, dp\right)$ vertices, which no mesh with the same angle bound can beat by more than a constant.

## Examples

- **A thin rectangle.** The rectangle $(0,0)$, $(8,0)$, $(8,1)$, $(0,1)$ has two triangulations on its corners, each with a smallest angle of about $7.13°$. Adding Steiner points at $(1,0), \ldots, (7,0)$ and $(1,1), \ldots, (7,1)$ cuts it into eight unit squares, each split by a diagonal into two triangles with angles $45°$, $45°$ and $90°$; the count is $4 + 0 - 2 + 14 = 16$ triangles.
- **A segment missing from the Delaunay triangulation.** For the points $(0,0)$, $(4,0)$, $(2,1)$, $(2,-1)$ and the segment from $(0,0)$ to $(4,0)$, the points $(2,1)$ and $(2,-1)$ lie inside the circle with that segment as diameter, so the Delaunay triangulation uses the edge from $(2,-1)$ to $(2,1)$ instead. The Steiner point $(2,0)$ on the segment splits it into two halves, which are Delaunay edges of the new point set.
- **A polygon that needs none.** Any simple polygon can be triangulated without Steiner points, by [ear clipping](/ear-clipping/); Steiner points are an option in two dimensions, never a necessity.
- **A polyhedron that needs one.** The Schönhardt polyhedron, a twisted triangular prism, has no tetrahedralization on its 6 vertices; adding its center gives one with 8 tetrahedra.

## Where it is used

- **[Mesh generation](/mesh-generation/).** Finite element and finite volume methods need meshes with bounded angles; all quality meshers add Steiner points, by [Delaunay refinement](/delaunay-refinement/), quadtrees or advancing fronts.
- **Conforming triangulations.** Keeping input edges while staying Delaunay, for interpolation and Voronoi-based methods, is done with Steiner points on the segments.
- **Three-dimensional meshing.** Tetrahedral meshers add Steiner points to recover boundary faces, since some boundaries cannot be recovered otherwise.
- **Optimization problems.** Minimum weight, minimum count and minimum link problems all have Steiner versions, usually with different complexity from the versions without them.

## References
