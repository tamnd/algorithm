---
tag: WHQNWA
kind: problem
slug: minimum-steiner-triangulation
name: Minimum Steiner triangulation
aliases:
- Steiner minimum triangulation
- minimum triangle partition
- minimum partition into triangles
area: geometry/triangulations
level: advanced
summary: Triangulate a polygon or point set with the fewest triangles using added Steiner points; NP-hard.
model: real-ram
prereqs: [steiner-points, polygon-triangulation, polygon-with-holes, euler-formula]
see_also: [polygon-with-holes-triangulation, convex-decomposition, hertel-mehlhorn, min-weight-triangulation, mesh-generation, schonhardt-polyhedron, tetrahedralization, triangulation-counting-theorem]
sources:
  - paper: "Takao Asano, Tetsuo Asano and Ron Y. Pinter, Polygon triangulation, efficiency and minimality, Journal of Algorithms 7(2), 221 to 231 (1986)"
    locator: NP-hardness of partitioning a polygon with holes into the fewest triangles (to be checked)
  - paper: "J. Mark Keil, Polygon decomposition, in Handbook of Computational Geometry, Elsevier, 491 to 518 (2000)"
    locator: the sections on partitions into triangles and convex pieces with and without Steiner points (pages to be checked)
  - paper: "Bernard Chazelle, Convex partitions of polyhedra, a lower bound and worst-case optimal algorithm, SIAM Journal on Computing 13(3), 488 to 507 (1984)"
    locator: polyhedra that need Ω(n^2) convex pieces, hence Ω(n^2) Steiner points to tetrahedralize
  - paper: "Bernard Chazelle and David Dobkin, Optimal convex decompositions, in Computational Geometry, North-Holland, 63 to 133 (1985)"
    locator: minimum convex partitions of simple polygons with Steiner points in polynomial time
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 2, Section on convex partitioning (Steiner points, Hertel and Mehlhorn, Chazelle and Dobkin)
---

A minimum Steiner triangulation of a polygonal region is a partition of the region into as few triangles as possible, where the triangle corners may be new points, called [Steiner points](/steiner-points/), and not only the input vertices. The answer depends on whether the triangles must meet edge to edge. In an edge-to-edge triangulation, Euler's formula shows that every Steiner point adds triangles, so the minimum is reached without them and the problem is trivial. If the triangles may meet a corner in the middle of another triangle's side, Steiner points can save triangles, and the problem becomes hard: for polygons with holes, finding the fewest triangles is NP-hard (Asano, Asano and Pinter). In three dimensions, Steiner points are sometimes needed at all, and their number can be forced to grow quadratically.

## In plain words

You must cut a flat shape into triangles and want as few pieces as possible. You may put new corners anywhere. If neighboring triangles must always share whole sides, extra corners never help: each one forces extra triangles, so the usual cut into triangles between the original corners is already best.

If a corner of one triangle may touch the middle of another triangle's side, extra corners can help on some shapes. Finding the best cut is then very hard once the shape has holes.

## Definition

**Input.** A polygonal region $P$: a simple polygon or a polygon with holes, with $n$ vertices in total, $h$ holes, and $r$ vertices whose interior angle is at least $\pi$ (reflex or flat).

**Output.** A finite set of triangles with pairwise disjoint interiors and union $P$, with as few triangles as possible. The corners may be any points of $P$.

**Two versions.**

- **Edge-to-edge (a triangulation).** Two triangles meet in a common edge, a common corner, or not at all. The triangle corners include all input vertices, and the extra ones are Steiner points.
- **Partition.** Any two triangles have disjoint interiors; a corner may lie inside a side of another triangle. Input vertices of angle exactly $\pi$ need not be corners.

**The edge-to-edge count.** Let a triangulation of $P$ have $b$ Steiner points on the boundary and $s$ in the interior. Counting angles gives the number of triangles:

$$t = n + 2h - 2 + b + 2s.$$

*Proof.* The triangle angles add up to $t\pi$. At each input vertex they add up to its interior angle, and the interior angles of $P$ add up to $(n - 2 + 2h)\pi$. Each boundary Steiner point contributes $\pi$ and each interior Steiner point $2\pi$. $\square$

So edge-to-edge Steiner points never reduce the count, and every triangulation without Steiner points, with $n + 2h - 2$ triangles, is optimal. The same holds for point sets: a triangulation of $n$ points with $h$ on the hull has $2n - h - 2$ triangles, and every Steiner point raises the count.

**A lower bound for partitions.** In a partition, a reflex or flat vertex can lie inside a triangle side, which covers $\pi$ of its angle without a corner, but at most one side can do this without overlap; a vertex with angle less than $\pi$ must be a corner. The same angle count then gives $t \ge n + 2h - 2 - r$. In particular, a convex polygon with no flat vertices needs exactly $n - 2$ triangles in both versions.

## Variants

- **Minimum convex partition.** Use convex pieces instead of triangles. With Steiner points, Chazelle and Dobkin solve it for simple polygons in polynomial time; without them, Keil gives a polynomial algorithm, and the [Hertel and Mehlhorn](/hertel-mehlhorn/) heuristic is within a factor 4. See [convex decomposition](/convex-decomposition/). With holes, both versions are NP-hard.
- **Fewest Steiner points for a quality bound.** Ask for the fewest Steiner points such that all angles are at least a bound, or none is obtuse. Delaunay refinement is within a constant factor of the optimum for a fixed angle bound; see [mesh generation](/mesh-generation/).
- **Fewest Steiner points in space.** A polyhedron may have no tetrahedralization with its own vertices; the [Schönhardt polyhedron](/schonhardt-polyhedron/) needs one Steiner point. Deciding whether zero Steiner points suffice is NP-complete (Ruppert and Seidel), and Chazelle's polyhedra need $\Omega(n^2)$ of them. See [tetrahedralization](/tetrahedralization/).
- **Steiner weight.** Minimize total edge length with Steiner points allowed; see [minimum weight triangulation](/min-weight-triangulation/) for the version without them.

## Examples

- **A square with a center point.** The two triangles of a diagonal are optimal. Adding the center as an interior Steiner point gives 4 triangles, matching $t = 4 + 0 - 2 + 0 + 2 = 4$.
- **A triangle with points on its sides.** A triangle whose sides carry $k$ extra input vertices of angle $\pi$ has $n = k + 3$ vertices. Every edge-to-edge triangulation has $k + 1$ triangles, but as a partition the triangle itself is one piece.
- **A polygon with holes.** A square with one square hole, $n = 8$ and $h = 1$, has edge-to-edge triangulations with $8 + 2 - 2 = 8$ triangles, and no Steiner point can lower that.

## Known algorithms

| version | region | result |
|---|---|---|
| edge-to-edge | any polygonal region | any triangulation without Steiner points is optimal; $O(n \log n)$, or $O(n)$ for simple polygons |
| partition | convex polygon | $n - 2$ minus the number of flat vertices, by a fan |
| partition | polygon with holes | NP-hard (Asano, Asano and Pinter) |
| partition | simple polygon | see Keil's survey; status to be checked |
| tetrahedralization | polyhedron | deciding zero Steiner points is NP-complete; $O(n^2)$ Steiner points always suffice |

## Bounds

- **Edge-to-edge.** Exactly $n + 2h - 2$ triangles, with no Steiner points.
- **Partitions.** At least $n + 2h - 2 - r$ triangles, by the angle count.
- **Three dimensions.** Some polyhedra with $n$ vertices need $\Omega(n^2)$ Steiner points, and $O(n^2)$ always suffice (Chazelle; Chazelle and Palios).

## Reductions

- **From convex partition.** Every partition into triangles is a convex partition, so the minimum convex partition is a lower bound for the minimum triangle partition, and a convex partition into $k$ pieces with $m$ corners in total gives a triangle partition with $m - 2k$ triangles by fanning each piece.
- **To polygon triangulation.** The edge-to-edge version reduces to [triangulating a polygon with holes](/polygon-with-holes-triangulation/), since any triangulation is optimal.

## Applications

- **Rendering.** The number of triangles sent to a graphics card is a cost, so fewer triangles are better; the edge-to-edge count shows that only flat vertices and T-junctions can be exploited.
- **Finite elements in space.** Steiner points in tetrahedral meshes are unavoidable for some inputs, which is why mesh generators add them.
- **Theory.** The angle counts are the basis of the [triangulation counting theorem](/triangulation-counting-theorem/).

## References
