---
tag: YMYTYF
kind: algorithm
slug: octree-mesh-generation
name: Octree mesh generation
aliases:
- Yerry-Shephard octree method
area: cad/mesh-generation-for-analysis
level: core
summary: Yerry and Shephard's tetrahedral meshing that refines an octree to the geometry, cuts boundary cells to the surface and fills inner cells with template elements.
solves: [mesh-generation]
model: real-ram
complexity:
  vars: {L: the number of leaves of the balanced octree, D: the depth of the finest leaves, k: the number of output tetrahedra}
  time: {expected: O(D L + k)}
  space: {extra: O(L + k)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1984
  people: [Mark Yerry, Mark Shephard]
  note: Yerry and Shephard gave a modified quadtree mesher in 1983 and the modified octree method for solids in 1984. Mitchell and Vavasis gave the first octree mesher with proved bounds in 1992.
prereqs: [octree, quadtree-mesh-generation, tetrahedralization]
see_also: [isosurface-stuffing, marching-tetrahedra, marching-cubes, tetrahedral-delaunay-refinement, sliver-tetrahedron, radius-edge-ratio, mesh-quality-measures, mesh-sizing-function]
sources:
  - paper: doi:10.1002/nme.1620201103
    title: Mark A. Yerry and Mark S. Shephard, Automatic three-dimensional mesh generation by the modified-octree technique, International Journal for Numerical Methods in Engineering 20(11), 1984, 1965 to 1990
    locator: the modified octree method for solid models (general locator)
  - paper: doi:10.1109/MCG.1983.262997
    title: Mark A. Yerry and Mark S. Shephard, A modified quadtree approach to finite element mesh generation, IEEE Computer Graphics and Applications 3(1), 1983, 39 to 46
    locator: the two-dimensional method (general locator)
  - paper: doi:10.1002/nme.1620320406
    title: Mark S. Shephard and Marcel K. Georges, Automatic three-dimensional mesh generation by the finite octree technique, International Journal for Numerical Methods in Engineering 32(4), 1991, 709 to 749
    locator: the finite octree variant (general locator)
  - paper: doi:10.1145/142675.142720
    title: Scott A. Mitchell and Stephen A. Vavasis, Quality mesh generation in three dimensions, Proceedings of the 8th ACM Symposium on Computational Geometry, 1992, 212 to 221
    locator: the first octree mesher with bounded aspect ratio and size optimality in three dimensions (general locator)
  - paper: doi:10.1137/S0097539796314124
    title: Scott A. Mitchell and Stephen A. Vavasis, Quality mesh generation in higher dimensions, SIAM Journal on Computing 29(4), 2000, 1334 to 1370
    locator: abstract and main theorems (bounded aspect ratio when the domain has no sharp angles, size within a factor of any competing mesh)
  - paper: doi:10.1145/276884.276894
    title: Jonathan Richard Shewchuk, Tetrahedral mesh generation by Delaunay refinement, Proceedings of the 14th ACM Symposium on Computational Geometry, 1998, 86 to 95
    locator: Section 1, the remark that the bounds of the octree methods are too weak to reassure in practice and are not stated explicitly
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, 3rd edition, Springer, 2008
    locator: Chapter 14, Quadtrees (balancing a quadtree and the size of the balanced tree)
---

Octree mesh generation builds a tetrahedral mesh of a solid from an [octree](/octree/). It splits the cubes that meet the boundary of the solid until they are small, balances the tree so that cubes that touch differ in size by at most a factor of 2, fills every cube with tetrahedra from a fixed template, and cuts the cubes at the boundary down to the surface. It is the three-dimensional form of [quadtree mesh generation](/quadtree-mesh-generation/). The original method of Yerry and Shephard is an engineering method with no proved guarantee on element shape. Mitchell and Vavasis later proved that an octree method can get bounded aspect ratio and a size within a constant factor of the best, with constants that are not given as numbers.

## In plain words

Put the solid in a big cube. Cut a cube into eight whenever the surface of the solid passes through it, until the cubes at the surface are small. Then cut more cubes until no cube touches a cube four or more times smaller. Now fill each cube with tetrahedra: put a point at its center, a point at the center of each square on its sides, and join them to the corners. Cubes that share a square cut it the same way, so the pieces fit. Last, throw away what lies outside the solid and trim the cubes that the surface cuts through. The inner tetrahedra have good shapes. The trimmed ones can be very thin.

## The problem

The input is a solid $\Omega$ and a size: the depth $D$ of the finest cubes. On this page the solid is a ball $|x - c|^2 < r^2$ inside the root cube $[0, S]^3$ with $S = 2^{D+1}$, given by the function $f(x) = r^2 - |x - c|^2$, which is positive inside. The output is a set of tetrahedra that meet face to face (a [tetrahedralization](/tetrahedralization/)) and fill a polyhedron close to $\Omega$. The quality measures are the [radius-edge ratio](/radius-edge-ratio/) $R/\ell_{\min}$ and the dihedral angles, two of the [mesh quality measures](/mesh-quality-measures/).

This page makes three kinds of claim, and they must be kept apart.

- *Proved bound with its constant, for the inner tetrahedra.* Every tetrahedron of the template step has radius-edge ratio at most $\sqrt{5/2} \approx 1.5811$ and all six dihedral angles between $\arctan(1/\sqrt2) \approx 35.26°$ and $90° + \arctan(1/\sqrt2) \approx 125.26°$. The proof in `proofs/correctness.md` lists all 112 template shapes. The bounds are attained, so here proof and measurement agree.
- *Method with no guarantee, for the cut tetrahedra.* The cut at the surface, as in Yerry and Shephard, gives no bound. In the example below the smallest dihedral angle after the cut is $1.89°$ and the largest radius-edge ratio is $25.7$, and both get worse as the surface passes closer to a vertex.
- *Proved bounds with unknown constants, cited.* Mitchell and Vavasis proved that their octree method gives a triangulation of bounded aspect ratio if the domain has no sharp angles, with a number of tetrahedra at most a factor times that of any mesh with bounded aspect ratio, the factor depending on that mesh's bound. The constants are not given as numbers. Shewchuk (1998, Section 1) notes that they are too weak to give practical reassurance. So the proved constants are much worse than what the method shows in practice.

A radius-edge bound alone would not do here: a [sliver](/sliver-tetrahedron/) has radius-edge ratio as small as $1/\sqrt2$ and dihedral angles near $0°$ and $180°$. The inner tetrahedra have no slivers because their dihedral angles are bounded directly, by the list of shapes, not because their radius-edge ratio is bounded.

## The algorithm

A box of level $k$ has side $S/2^k$. Two leaves are *balanced* if they share a face or an edge and differ by at most one level. Leaves that share only a corner may differ more. A *boundary square* of a leaf $b$ is one of its faces, or, if the box of the same size across that face is split, one of the four quarters of that face.

```pseudo id=main
OCTREE-MESH(f, c, r², D)
L1  T ← the octree whose only leaf is the root cube [0, S]³, S = 2^(D+1)
L2  while some leaf b of level < D meets the sphere |x − c|² = r²:
L3      split b into its 8 children
L4  while some leaf b shares a face or an edge with a leaf two or more levels finer:
L5      split b
L6  for each leaf b:
L7      add the center p of b
L8      for each boundary square s of b:
L9          add the center m of s; let r₁, …, r_t be the corners of s and the midpoints of its sides that are corners of leaves, in order around s
L10         output the tetrahedra (p, m, r_i, r_(i+1)) for i = 1, …, t (indices mod t)
L11 compute f(v) at every vertex v
L12 for each tetrahedron τ, with j vertices where f > 0:
L13     j = 4: keep τ; j = 0: drop τ
L14     j = 1: keep the tetrahedron spanned by the positive vertex and the three cut points on its edges
L15     j = 2: keep the prism between the positive edge and the four cut points, cut into 3 tetrahedra
L16     j = 3: keep the truncated tetrahedron, a prism, cut into 3 tetrahedra
L17 return the kept tetrahedra
```

The cut point on an edge $uv$ with $f(u) > 0 > f(v)$ is the zero of the linear interpolation, $u + \frac{f(u)}{f(u) - f(v)} (v - u)$. All the cut points of one tetrahedron lie on one plane, the zero set of the linear interpolant of $f$, so every kept piece is convex. Each piece with $j = 2$ or $j = 3$ is a prism: two triangles joined by three edges, with three quadrilateral sides. The quadrilaterals lie on faces of $\tau$ or on the cut plane, and two tetrahedra that share a face see the same quadrilateral. Each one is split by the diagonal through its smallest vertex in a fixed global order (here the lexicographic order of the exact coordinates), so neighbors agree. The smallest of the six vertices is the end of two diagonals, so it sees the opposite triangle as one tetrahedron, and the third diagonal splits the pyramid that remains. A prism with the three diagonals in a cycle has no split into tetrahedra; the global order rules that out.

The root side $S = 2^{D+1}$ makes every corner, box center and center of a quarter face an integer point, so L1 to L10 are integer arithmetic. The values $f(v)$ and the cut points are rational. If $f(v) = 0$ at a vertex, the program stops with an error, since the paper's snapping of vertices to the surface is not part of this page.

## Example

Take the ball with center $(8, 8, 8)$ and $r^2 = 91/3$, so $r \approx 5.508$, and $D = 3$, so the root is $[0, 16]^3$. The counts come from the implementation, and the test file checks them.

| Step | Lines | Result |
|---|---|---|
| refine to the sphere | L2, L3 | all 8 boxes of level 1 and 32 of the 64 boxes of level 2 meet the sphere and are split; 256 leaves of side 2 and 32 of side 4 remain |
| balance | L4, L5 | no split: the levels already differ by at most one |
| templates | L6 to L10 | 264 leaves have 6 boundary squares, 24 leaves of side 4 have two faces next to split boxes and so 12; 1777 vertices and 7680 tetrahedra |
| cut | L11 to L16 | by the number $j$ of positive vertices: 4848 tetrahedra with $j = 0$ dropped, 1344 with $j = 4$ kept, 576 with $j = 1$ give 576, 384 with $j = 2$ give 1152, 528 with $j = 3$ give 1584 |
| output | L17 | 1395 vertices and 4656 tetrahedra |

The template tetrahedra all have dihedral angles in $[35.26°, 125.26°]$ and radius-edge ratio at most $1.5811$. After the cut, the smallest dihedral angle is $1.89°$, the largest is $155.54°$, the largest radius-edge ratio is $25.72$, and 312 of the 4656 tetrahedra have a dihedral angle below $5°$. Moving the center to $(7.5, 8, 8.5)$ gives a smallest dihedral angle of $0.32°$ and a radius-edge ratio of $747.5$. The mesh has volume $673.52$, against $699.79$ for the ball. It is smaller because $f$ is concave: on each tetrahedron $f$ is at least its linear interpolant, so the kept part lies inside the ball.

## Correctness

The proof is in `proofs/correctness.md`. It has four parts.

1. *The loops stop and the tree is balanced.* The refinement loop splits only boxes of level below $D$. The balance loop never splits a leaf of level $D$, since nothing is finer, so it also splits finitely many boxes. When it stops, leaves that share a face or an edge differ by at most one level.
2. *Each boundary square has only its corners and some side midpoints on its boundary, and no tree corner inside.* A tree corner inside a square or inside a side, other than the midpoint, would be the corner of a leaf at least two levels finer than the leaf that owns the square, touching it along a face or an edge. Balance forbids that. So both leaves that share a square list the same ring $r_1, \dots, r_t$ and the same center $m$, and they make the same triangles on it.
3. *The template mesh tiles the cube.* Every triangle on a boundary square is used once from each side with opposite orientation, or lies on the root boundary. The tetrahedra have positive volume and their volumes add up to $S^3$. A covering count argument, as in the quadtree proof, shows that they tile the root cube face to face.
4. *The shape bound.* Up to the symmetries of the cube, a template tetrahedron is $(p, m, r_i, r_{i+1})$ for the bottom face of $[0, 8]^3$ or one of its quarters, with any set of side midpoints on a whole face and none on a quarter (by balance). This gives 112 tetrahedra. Exact arithmetic gives the largest squared radius-edge ratio, $5/2$, and the dihedral angles, which take only the values $35.26°$, $45°$, $54.74°$, $60°$, $90°$ and $125.26°$.

The cut keeps the mesh conforming: two tetrahedra that share a triangle cut it at the same points and split its quadrilateral part by the same diagonal. The test file checks this by cutting with $f$ and with $-f$: the two parts fill the cube exactly, and their cut triangles are the same triangles with opposite orientation.

## Complexity

With hashing for the neighbor lookups and a work queue for the balance step, each level is refined once, each split checks a fixed number of neighbors, and each leaf gives at most $6 \cdot 16 = 96$ tetrahedra (a whole face gives at most 8 triangles, a split face 4 quarters of 4). The time is then $O(D L + k)$ expected, and the space is $O(L + k)$. The balance step adds at most a constant factor of leaves: de Berg et al. (Theorem 14.4) prove this for quadtrees, and the same argument works for octrees with a larger constant.

For a smooth surface of area $A$ and finest side $h = S/2^D$, the leaves at the surface number about $A/h^2$, so $L$ and $k$ grow as $4^D$, while a uniform grid of the same resolution has $8^D$ cubes. This is the reason to use an octree.

The implementation on this page is simpler: every round of both loops scans all leaves, which is $O(L^2)$ in the worst case. It is enough for the test inputs, where $D = 3$.

## Properties

- **Exact.** All decisions are signs of integers or fractions.
- **Deterministic.** Ties do not arise: the quadrilateral diagonals use a fixed global order.
- **Conforming.** The template mesh is face to face across leaves of different sizes, without hanging nodes, because the boundary squares carry their side midpoints.
- **Graded.** Balance makes box sizes change by a factor of at most 2 between neighbors, so the mesh coarsens away from the surface.
- **Proved shape bound inside, no bound at the surface.** Inner tetrahedra: radius-edge ratio at most $\sqrt{5/2}$, dihedral angles in $[35.26°, 125.26°]$. Cut tetrahedra: no bound.
- **Axis dependent.** A rotated solid gives a different mesh.

## Variants and improvements

- **Modified octree of Yerry and Shephard.** The 1984 method works from a solid model. It classifies octants as inside, outside or on the boundary, meshes inner octants with templates and meshes boundary octants by special cases cut to the surface. No shape bound is proved.
- **Finite octree.** Shephard and Georges (1991) store the boundary geometry in the octree cells and mesh the boundary cells with more general procedures. It is also an engineering method.
- **Provably good octrees.** Mitchell and Vavasis (1992, 2000) extend the quadtree method of Bern, Eppstein and Gilbert to three and more dimensions. They warp octree vertices onto the input faces and edges by systematic rules and duplicate boxes for each connected piece of the domain inside them. They prove bounded aspect ratio for domains without sharp angles and size within a factor of optimal, without numeric constants.
- **Isosurface stuffing.** [Isosurface stuffing](/isosurface-stuffing/) replaces the cube templates by the body-centered cubic lattice and snaps or warps vertices near the surface, which gives proved dihedral angle bounds of about $10.78°$ and $164.74°$ for the whole mesh, including the cut cells.
- **Marching cubes and marching tetrahedra.** [Marching cubes](/marching-cubes/) and [marching tetrahedra](/marching-tetrahedra/) extract only the surface from a grid. The cut step of this page is marching tetrahedra applied to the volume.
- **Delaunay refinement.** [Tetrahedral Delaunay refinement](/tetrahedral-delaunay-refinement/) gives a proved radius-edge bound for polyhedral input with fewer elements, but does not bound dihedral angles.

## When to use it

Use it when the domain is given by a function or a voxel image, when the mesh should be graded by a size field that a tree can represent, or when a quick and robust mesher matters more than element shape near the boundary. It needs only an inside test or a function like $f$, not a closed surface mesh. Use [isosurface stuffing](/isosurface-stuffing/) when you need a dihedral angle bound for every element, and [Delaunay refinement](/tetrahedral-delaunay-refinement/) or the [advancing front method](/advancing-front-mesh-generation/) when the boundary is a surface mesh that must be kept.

## Pitfalls

- **Bad elements at the surface.** Cut tetrahedra can be arbitrarily thin when the surface passes close to a vertex. Snap such vertices to the surface, warp them as isosurface stuffing does, or smooth and untangle after the cut.
- **A radius-edge bound is not enough.** It does not exclude slivers. Check the dihedral angles or another measure such as the [scaled Jacobian](/scaled-jacobian/).
- **Face balance only.** Balancing across faces alone lets an edge carry two hanging vertices, and the templates then no longer match. Balance across edges as well.
- **Hanging nodes.** If a coarse leaf ignores the corners of its finer neighbors, the mesh has cracks. Put the side midpoints into the boundary rings, as L9 does.
- **Inconsistent diagonals.** Two prisms that share a quadrilateral must split it the same way. A local rule, such as the shortest diagonal with ties broken by position, can disagree in floating point; a global vertex order cannot.
- **Small features.** A feature smaller than the finest cube is lost or meshed with the wrong topology. The depth must follow the smallest feature, or the tree must be refined by a [sizing function](/mesh-sizing-function/).

## Implementations

## History

Yerry and Shephard published a modified quadtree mesher for finite element analysis in 1983 and the modified octree method for three-dimensional solids in 1984. Shephard and Georges developed it into the finite octree technique in 1991. These were practical methods that worked directly from solid models, and they made fully automatic tetrahedral meshing usable in engineering codes. In 1990 Bern, Eppstein and Gilbert proved bounds for quadtree meshing in the plane, and in 1992 Mitchell and Vavasis carried the proofs to three dimensions, with a journal version for any dimension in 2000. Their QMG code implemented the method. In 2007 Labelle and Shewchuk gave isosurface stuffing, an octree method with explicit dihedral angle bounds.

## References
