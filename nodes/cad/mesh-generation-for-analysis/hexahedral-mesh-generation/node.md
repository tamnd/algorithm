---
tag: AXBDXR
kind: problem
slug: hexahedral-mesh-generation
name: Hexahedral mesh generation
aliases:
- hex meshing
- all-hex meshing
area: cad/mesh-generation-for-analysis
level: core
summary: Fill a solid with hexahedra that meet face to face and match its boundary, preferred for analysis but much harder to automate than tetrahedral meshing.
prereqs: [mesh-generation, finite-element-method]
see_also: [hexahedral-mesh-existence-theorem, spatial-twist-continuum, scaled-jacobian, mesh-quality-measures, mesh-untangling, octree-mesh-generation, tetrahedral-delaunay-refinement, structured-grid-generation]
sources:
  - paper: "Nico Pietroni, Marcel Campen, Alla Sheffer, Gianmarco Cherchi, David Bommes, Xifeng Gao, Riccardo Scateni, Franck Ledoux, Jean-François Remacle and Marco Livesu, Hex-mesh generation and processing, a survey, arXiv 2202.12670, 2022"
    locator: Section 1 on the open problem, Section 2 on the dual, Section 4 on all classes of methods with their table of properties, and Section 4.1 on direct and indirect methods
  - paper: "J. F. Shepherd and C. R. Johnson, Hexahedral mesh generation constraints, Engineering with Computers 24(3), 2008, 195 to 213"
    locator: the constraints that a boundary quad mesh puts on a hex mesh (general locator)
  - paper: "Ted Blacker, Meeting the challenge for automated conformal hexahedral meshing, Proceedings of the 9th International Meshing Roundtable, 2000, 11 to 20"
    locator: the description of the goals and the difficulties of automatic hex meshing (general locator)
  - paper: doi:10.1007/3-540-60922-9_38
    title: Scott A. Mitchell, A characterization of the quadrilateral meshes of a surface which admit a compatible hexahedral mesh of the enclosed volume, STACS 96, Lecture Notes in Computer Science 1046, Springer, 1996
    locator: the condition of an even number of boundary quads for a ball (general locator)
  - paper: doi:10.1016/S0925-7721(98)00032-7
    title: David Eppstein, Linear complexity hexahedral mesh generation, Computational Geometry 12(1-2), 1999, 3 to 16
    locator: the O(n) upper bound on the number of hexes (general locator)
  - paper: "T. S. Li, R. M. McKeag and C. G. Armstrong, Hexahedral meshing using midpoint subdivision and integer programming, Computer Methods in Applied Mechanics and Engineering 124(1-2), 1995, 171 to 193"
    locator: the split of tetrahedra and other simple cells into hexahedra by midpoint subdivision (general locator)
---

Fill a solid with hexahedra that meet face to face and match its boundary, preferred for analysis but much harder to automate than tetrahedral meshing.

A hexahedral mesh, or hex mesh, divides a solid into cells that are each a deformed cube: eight corners, twelve edges and six quadrilateral faces. Two hexes meet in a whole face, a whole edge, a corner, or not at all. Many analysts prefer hexes to tetrahedra for finite element analysis, because a hex mesh often needs fewer elements for the same accuracy and the elements can follow the main directions of the solid. But while every solid can be filled with good tetrahedra by robust automatic methods, no known method fills every solid with good hexes. The survey of Pietroni and others (2022) calls the problem open, and Blacker (2000) called it the holy grail of mesh generation.

## In plain words

You have a solid part and you want to cut it into small bricks. The bricks may bend a little, but each must still look like a brick, and two bricks that touch must share a whole face. The bricks on the outside must lie on the outside of the part, and their edges should follow the sharp edges of the part.

With tetrahedra this is easy, because a tetrahedron can be fitted almost anywhere. With bricks it is hard, because bricks come in layers. A layer of bricks that starts at one place on the surface must go on through the whole solid until it ends at the surface again, or closes on itself. So a choice at one place changes the mesh far away. A simple count also shows that the outside must have an even number of brick faces.

## Definition

**Input.** A solid $\Omega \subset \mathbb{R}^3$, usually a B-rep model, with its feature curves and corners. Often also a target element size, and sometimes a fixed quad mesh $Q$ of the boundary.

**Output.** A finite set of hexes. Each hex is given by eight vertices in the standard order and is the image of the unit cube under the trilinear map of these vertices, or of a higher order map. The mesh must satisfy:

1. **Conformity.** Two hexes meet in a shared face, a shared edge, a shared vertex or not at all.
2. **Cover.** The union of the hexes is $\Omega$, or a close approximation of it, and the faces that lie in one hex only form a quad mesh of the boundary. If $Q$ is given, these faces are exactly the quads of $Q$.
3. **Validity.** The Jacobian determinant of each hex map is positive everywhere in the hex. In practice it is checked at the corners, by the [scaled Jacobian](/scaled-jacobian/), or by a certified bound.
4. **Features.** The sharp edges and corners of $\Omega$ lie on edges and vertices of the mesh.

**Goal.** Among the meshes that satisfy 1 to 4, find one with good quality, usually a large minimum scaled Jacobian (see [mesh quality measures](/mesh-quality-measures/)), with element sizes close to the target, and with few singular edges. An inner edge is singular if it is not in exactly four hexes.

## Variants

- **Constrained or free boundary.** In the constrained problem the quad mesh $Q$ of the boundary is fixed, for example because it is shared with a neighbour part. In the free problem the method also chooses the boundary quads.
- **Topological or geometric.** The topological problem asks only for a cell complex of topological cubes. This is the version that the [existence theorem](/hexahedral-mesh-existence-theorem/) answers. The geometric problem asks for real hexes with positive Jacobians, and it is much harder.
- **Structured, block structured, unstructured.** A structured mesh is one grid, as in [structured grid generation](/structured-grid-generation/). A block structured mesh is a few grids glued face to face. An unstructured mesh allows any number of hexes around an inner edge.
- **Hex dominant.** Most cells are hexes, but some prisms, pyramids or tetrahedra are allowed. This is much easier and is common in practice.
- **Non-conforming.** Hexes of an [octree](/octree-mesh-generation/) can have hanging nodes, or templates can remove them at a cost in quality.
- **Assemblies.** Several parts are meshed so that the meshes match on the contact faces.

## Examples

**A box.** A box with sides $a \times b \times c$ and a size $h$ that divides each side gets the grid of $(a/h)(b/h)(c/h)$ hexes, all perfect cubes. No singular edges are needed.

**A ball.** A ball has no grid mesh. Take a cube $[0, 3]^3$ cut into an inner cube $[1, 2]^3$ and six hexes that join each inner face to an outer face, and project the outer corners to the sphere. This gives 7 hexes and 6 boundary quads. At the 8 outer corners, three boundary quads meet, not four. For a finer mesh one refines all 7 blocks as grids.

**An odd boundary.** Take the six quads of a cube and split one face $ABCD$ into the quads $ABCX$ and $AXCD$, with a new point $X$ inside it. This boundary has 7 quads. By the parity count below, no hex mesh has this boundary.

**A small hard boundary.** Schneiders' pyramid is a square pyramid whose base is split into 4 quads and each triangle into 3, so 16 quads in all. Schneiders and Bünten posed it in 1995. Hex meshes of it with 118, 88, 36 and 44 hexes were found later, in 2002, 2010, 2018 and 2019. So even a 16 quad boundary can be very hard to fill.

**Two meshes for one boundary.** The six quads of a cube bound both the single cube and the 7 hex pillowed cube above. So the boundary does not fix the mesh, not even its number of hexes.

## Known algorithms

Each method below has its own page, which proves what that page claims for its own steps. The column "proved" lists what is proved, and the column "measured" what is only reported in tests or papers.

| method | idea | proved | measured |
|---|---|---|---|
| [hexahedral sweeping](/hexahedral-sweeping/) | map a source quad mesh layer by layer to a target face | valid hexes for affine layer maps and convex source quads | validity for curved sides is checked, not proved; the most used method in practice |
| [plastering](/plastering/) | advance layers of hexes inward from the boundary | nothing about closing the last void | often fails where the fronts meet |
| [whisker weaving](/whisker-weaving/) | build the dual sheets from the boundary loops first, then the hexes | the sheet structure of a finished mesh | no general guarantee to finish |
| [polycube hex meshing](/polycube-hex-meshing/) | map the solid to a union of axis-aligned cubes, mesh with a grid, map back | a valid mesh when the map is injective and passes a positivity test | good quality on organic shapes, poor on parts with many features |
| [frame field hex meshing](/frame-field-hex-meshing/) | smooth a field of cube frames, then an integer-grid map aligned to it | the smoothing step lowers the energy | the map can fail at singular curves, no general guarantee |
| [medial axis decomposition](/medial-axis-decomposition-meshing/) | cut the solid at its medial surface into simple parts, then mesh each | when midpoint subdivision of a simple part works, by parity and size conditions | needs a stable medial surface |
| [octree mesh generation](/octree-mesh-generation/) | refine a grid of cubes to fit the solid, then fit the boundary | a valid inner grid | poor elements near the boundary |
| split each tetrahedron into 4 hexes | an indirect method from a tetrahedral mesh | always a valid mesh | many hexes, very many singular edges, poor quality |

How the problem differs from each method page: this page states the general task and its limits, while each method page solves it only under its own conditions, such as a sweep direction for sweeping or an injective map for polycubes, and many methods give no guarantee at all.

## Bounds

**Parity and a lower bound.** Each hex has 6 faces, each inner face is in 2 hexes and each boundary quad in 1. So $6H = 2I + B$ for $H$ hexes, $I$ inner faces and $B$ boundary quads. Hence $B$ is even and $H \ge B/6$. The full proof is on the [existence theorem](/hexahedral-mesh-existence-theorem/) page.

**Existence for a ball.** For a ball with a quad mesh $Q$ of $n$ quads on its boundary, a topological hex mesh exists if and only if $n$ is even (Thurston 1993, Mitchell 1996). Mitchell's construction can need $O(n^2)$ hexes. Eppstein (1999) showed that $O(n)$ hexes are enough, and later meshes of his buffer cubes bring this to at most $78 n$. These bounds are about topology. They give no bound on the shape of the hexes.

**Free boundary.** If the boundary quads are free, every polyhedral solid has a hex mesh: take any tetrahedral mesh and split each tetrahedron into 4 hexes by its edge midpoints, face centres and centroid. So existence is easy, and the whole difficulty is quality and control of the boundary.

**What is open.** No known method is proved to give, for every solid, a valid hex mesh with all scaled Jacobians above a fixed positive bound and a prescribed boundary. Whether every even quad mesh of a convex polyhedron with planar convex quads has a mesh of convex hexes is open, as far as the survey reports.

## Reductions

- **To the dual.** A hex mesh is the same as an arrangement of surfaces with valid cells, the [spatial twist continuum](/spatial-twist-continuum/). Methods such as whisker weaving solve the problem in the dual.
- **To a parameterization.** Polycube and frame field methods reduce the problem to a volumetric map $f: \Omega \to \mathbb{R}^3$ whose integer grid gives the hexes. The hard part moves to making $f$ injective with the right singular curves.
- **To decomposition.** Medial axis methods, manual blocking and sweeping split the solid into parts that are each easy to mesh, then match the parts. The matching of the numbers of intervals on shared edges is an integer program, as in Li, McKeag and Armstrong (1995).
- **From tetrahedral meshing.** The split of tetrahedra gives a mesh from any tetrahedral mesh, so hex meshing with a free boundary is never harder than [tetrahedral meshing](/tetrahedral-delaunay-refinement/), only harder to do well.

## Applications

- **Structural analysis.** Linear tetrahedra are stiff in bending and lock for nearly incompressible materials, such as rubber or metals in plastic flow. Hexes with the same number of nodes behave better, so they are common in crash, forming and contact analysis.
- **Fluid flow.** Layers of thin hexes along walls resolve boundary layers, as in [boundary layer mesh generation](/boundary-layer-mesh-generation/).
- **High order and spline analysis.** Hexes are tensor products, so they carry tensor product polynomial and spline bases, as in [volumetric spline parameterization](/volumetric-spline-parameterization/) and [high-order mesh generation](/high-order-mesh-generation/).
- **Medicine and geoscience.** Models of bones, organs and rock layers are often meshed with hexes, sometimes from voxel images.

## References
