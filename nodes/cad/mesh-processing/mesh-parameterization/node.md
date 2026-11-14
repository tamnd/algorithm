---
tag: 2R1FZD
kind: problem
slug: mesh-parameterization
name: Mesh parameterization
aliases:
- surface parameterization
- UV unwrapping
area: cad/mesh-processing
level: core
summary: Map a mesh with disk topology one to one onto a region of the plane with low distortion of angles or areas, for texture, remeshing and fitting.
prereqs: [manifold-mesh, discrete-gaussian-curvature]
see_also: [tutte-embedding, floater-mean-value-coordinates, least-squares-conformal-maps, angle-based-flattening, mixed-integer-quadrangulation, mesh-segmentation, texture-mapping, discrete-gauss-bonnet-theorem]
sources:
  - paper: doi:10.1007/3-540-26808-1_9
    title: Michael S. Floater and Kai Hormann, Surface parameterization, a tutorial and survey, in Advances in Multiresolution for Geometric Modelling, Springer, 2005, 157 to 186
    locator: the definitions of isometric, conformal and equiareal maps by the singular values of the Jacobian, the theorem of Tutte and Floater on convex combination maps, and the survey of methods
  - paper: doi:10.1561/0600000011
    title: Alla Sheffer, Emil Praun and Kenneth Rose, Mesh parameterization methods and their applications, Foundations and Trends in Computer Graphics and Vision 2(2), 2006, 105 to 171
    locator: the distortion measures, fixed and free boundaries, cutting and charts, and the applications
  - book: isbn:9781568814261
    title: Mario Botsch, Leif Kobbelt, Mark Pauly, Pierre Alliez and Bruno Lévy, Polygon Mesh Processing, AK Peters, 2010
    locator: Chapter 5, Parametrization (the problem statement, the distortion of a piecewise linear map, and the families of methods)
---

Mesh parameterization is the problem of mapping a triangle mesh in space onto a region of the plane, one to one, so that the flat image looks as much as possible like the surface: angles, lengths or areas change little. The map gives each vertex a point $(u, v)$ in the plane and is linear on each triangle. A flat map that keeps all lengths exists only for a surface that can be unrolled without stretching, such as a cylinder or a cone, so in general the problem is to choose which distortion to accept. The input must have the topology of a disk; a closed surface or a surface with handles is first cut along seams or split into charts by [mesh segmentation](/mesh-segmentation/). The problem is the basis of [texture mapping](/texture-mapping/), of remeshing and of fitting spline surfaces to meshes.

## In plain words

Think of peeling an orange and pressing the peel flat on a table. The peel tears or stretches, because a piece of a sphere cannot lie flat without changing. A paper cylinder, on the other hand, unrolls perfectly once you cut it along one line.

A mesh is a surface made of small triangles. Parameterizing it means laying all its triangles flat in the plane, edge to edge, with no overlap. Each triangle may change its shape a little. The goal is to keep the change small, for example to keep the angles of each triangle, or its area.

The flat picture is then used to put an image on the surface, or to lay a regular grid over it.

## Definition

**Input.** A triangle mesh $M$ with vertices $p_0, \ldots, p_{n-1}$ in $\mathbb{R}^3$, which is a connected oriented [manifold mesh](/manifold-mesh/) with one boundary loop and the topology of a disk, so its Euler characteristic $V - E + F$ is 1. The faces are oriented so that the outward normal follows the right-hand rule.

**Output.** A point $u_i \in \mathbb{R}^2$ for each vertex. The map $f$ is the piecewise linear map that sends each triangle $(p_i, p_j, p_k)$ to the triangle $(u_i, u_j, u_k)$.

**Conditions.**

- **Local injectivity.** Each image triangle keeps its orientation: $\mathrm{ORIENT2D}(u_i, u_j, u_k) > 0$ for each face $(i, j, k)$, by the [orientation test](/orientation-test/). A triangle with a negative sign is flipped.
- **Global injectivity.** No two image triangles overlap. For a locally injective map this holds if and only if the image of the boundary loop does not cross itself.
- **Boundary.** Either the image of the boundary is given (a *fixed boundary*, often a convex polygon), or it is part of the output (a *free boundary*).

**Checking the conditions.** Local injectivity is a sign test per triangle. With floating point coordinates the sign of ORIENT2D can be wrong for nearly degenerate image triangles, through [catastrophic cancellation](/catastrophic-cancellation/), and [exact predicates](/shewchuk-expansion-sum/) make the check reliable. Very thin image triangles are close to flips, so the check is part of the [robustness problem](/geometric-robustness-problem/) of geometry, not a formality.

**Distortion.** On a triangle $T$, $f$ has a constant $2 \times 2$ Jacobian $J_T$ in an orthonormal frame of the plane of $T$, with singular values $\sigma_1 \ge \sigma_2 > 0$. The map is

- *isometric* on $T$ if $\sigma_1 = \sigma_2 = 1$ (lengths are kept),
- *conformal* if $\sigma_1 = \sigma_2$ (angles are kept),
- *equiareal* or *authalic* if $\sigma_1 \sigma_2 = 1$ (areas are kept).

A map is isometric if and only if it is conformal and equiareal. A distortion energy is a sum over the triangles, weighted by area, of a function of $\sigma_1$ and $\sigma_2$ that is smallest at the ideal; for example $(\sigma_1 - \sigma_2)^2$ for angles, or $\sigma_1^2 + \sigma_1^{-2} + \sigma_2^2 + \sigma_2^{-2}$ for lengths. The problem is to minimize a chosen energy subject to the conditions.

**What is possible.** A piecewise linear isometry onto the plane exists for a disk mesh if and only if the angles of the triangles around each inner vertex sum to exactly $2\pi$, that is, the [discrete Gaussian curvature](/discrete-gaussian-curvature/) is 0 at every inner vertex, and the resulting unfolding does not overlap. By the [discrete Gauss-Bonnet theorem](/discrete-gauss-bonnet-theorem/), a mesh with curvature cannot be flattened without distortion, and the total curvature tells how much must be absorbed.

## Variants

- **Fixed or free boundary.** A fixed convex boundary makes injectivity easier to guarantee; a free boundary lowers the distortion.
- **Conformal, authalic or isometric.** The choice of energy; isometric energies balance angles against areas.
- **Bijective.** The map must be globally injective, not only free of flipped triangles.
- **Seamless and global.** A closed surface or one with handles is cut into a disk, and the maps on the two sides of each cut must agree up to a rotation by a multiple of $90°$ and an integer translation, so that a grid in the plane closes over the seams. This is the variant behind quad meshing.
- **Cone singularities.** Curvature is gathered into a few vertices, the cones, and the rest of the map is flat.
- **Volume parameterization.** A tetrahedral mesh is mapped into space with low distortion, for hexahedral meshing.

## Examples

**A flat mesh.** If all vertices lie in a plane, the identity is an isometry. A good method should return a copy of the input up to a rotation, a translation and, for conformal methods, a scale.

**A square pyramid.** Take the base square $(0,0,0)$, $(2,0,0)$, $(2,2,0)$, $(0,2,0)$ as the boundary loop and the apex $(1,1,1)$ as the one inner vertex, with four triangles. Each triangle has base 2 and height $\sqrt2$, so its angle at the apex is $2\arctan(1/\sqrt2) \approx 70.53°$, and the four sum to $282.1°$, short of $360°$ by $77.9°$. So no isometry exists. Mapping the base to the same square in the plane and the apex to $(1, 1)$ gives four flat triangles of base 2 and height 1. On each, the map keeps the base direction and shrinks the height direction from $\sqrt2$ to 1, so $\sigma_1 = 1$, $\sigma_2 = 1/\sqrt2 \approx 0.707$: the angles change, the ratio $\sigma_1 / \sigma_2$ is $\sqrt2$, and each area shrinks from $\sqrt2$ to 1.

**An open cylinder.** A tube has two boundary loops and is not a disk. Its curvature is 0, so after one cut from one loop to the other it unrolls onto a rectangle without distortion.

**A sphere.** A closed mesh has no boundary and Euler characteristic 2. It must be cut, and since its total curvature is $4\pi$, every flattening of the cut sphere has distortion; the cuts decide where it goes.

## Known algorithms

| method | boundary | what it guarantees | cost |
|---|---|---|---|
| [Tutte embedding](/tutte-embedding/), with uniform or other positive weights | fixed, convex | a bijection onto the convex polygon (Tutte 1963, Floater 2003); high distortion near the boundary | one sparse linear solve |
| [Floater mean value coordinates](/floater-mean-value-coordinates/) as the weights of a Tutte map | fixed, convex | a bijection, and a flat mesh is reproduced exactly | one sparse linear solve |
| [least squares conformal maps](/least-squares-conformal-maps/) | free, two pinned vertices | the minimum of a conformal energy; flipped triangles and overlaps are possible | one sparse linear solve |
| [angle-based flattening](/angle-based-flattening/) | free | valid angles for every triangle, so no flipped triangles; overlaps of the boundary are possible | nonlinear, Newton iterations |
| [mixed-integer quadrangulation](/mixed-integer-quadrangulation/) | seamless, with cones | a map aligned to a cross field whose seams and cones are integer; flips are possible | a sequence of sparse solves with greedy rounding |

Other known methods minimize isometric energies by local and global steps or by Newton iterations with a barrier against flips, and some solve for conformal maps through the boundary curvature. These are outside the pages of this site.

## Bounds

- **Proved.** With a fixed convex boundary and positive weights in each row, the Tutte map is a bijection; this is the only general guarantee of injectivity with a linear solve. A linear method needs $\Omega(n)$ time to write its output, and the sparse systems of the linear methods have the graph of the mesh, which is planar for a disk, so [nested dissection](/nested-dissection/) solves them in $O(n^{3/2})$ time.
- **Impossibility.** An isometry exists only for zero discrete curvature at every inner vertex, as the pyramid shows. For a free boundary, the energies that measure lengths are not convex, and the set of locally injective maps is not convex either, so the methods that search over it have no general guarantee of the global optimum.
- **Measured.** The distortion of a method on a given mesh is measured, not proved, and comparisons between methods are made on collections of meshes.

## Reductions

- **From a closed surface.** A closed mesh or one with handles is reduced to disks by cutting it along a cut graph or by [mesh segmentation](/mesh-segmentation/) into charts.
- **To a linear system.** Fixed-boundary convex combination maps reduce to a sparse linear system with the matrix of a weighted graph Laplacian, a discrete form of the [Poisson equation](/poisson-equation/) with Dirichlet boundary values.
- **To a least squares problem.** Conformal maps with a free boundary reduce to a [least squares problem](/least-squares-problem/) once two vertices are pinned.
- **Into quad meshing.** A seamless map with integer seams turns the grid of the plane into a quad mesh of the surface.

## Applications

- **Texture mapping.** The flat image is the texture atlas: a picture drawn in the plane is carried onto the surface.
- **Remeshing.** A regular grid or a good triangulation in the plane is mapped back to give a new mesh of the surface, as in quad meshing.
- **Surface fitting.** Spline and NURBS patches are fitted to scanned meshes over a parameter domain.
- **Detail transfer and morphing.** Two surfaces mapped to the same domain get a correspondence between them.

## References
