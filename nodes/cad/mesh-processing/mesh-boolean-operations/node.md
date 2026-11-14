---
tag: HESZ8C
kind: problem
slug: mesh-boolean-operations
name: Mesh Boolean operations
aliases:
- mesh Booleans
- mesh CSG
area: cad/mesh-processing
level: core
summary: Compute the union, intersection or difference of the solids bounded by two triangle meshes, as a new closed mesh, robustly when faces nearly coincide.
prereqs: [manifold-mesh, regularized-set-operations, winding-number-algorithm]
see_also: [mesh-arrangements, generalized-winding-number, solid-boolean-operations, constructive-solid-geometry, mesh-self-intersection, triangle-triangle-intersection, polygon-union, exact-geometric-computation]
sources:
  - paper: doi:10.1145/2897824.2925901
    title: Qingnan Zhou, Eitan Grinspun, Denis Zorin and Alec Jacobson, Mesh arrangements for solid geometry, ACM Transactions on Graphics 35(4), 2016, Article 39
    locator: the definition of Booleans by winding numbers for self-intersecting and nested input, and the survey of earlier mesh Boolean methods
  - paper: doi:10.1007/978-3-540-39658-1_59
    title: Miguel Granados, Peter Hachenberger, Susan Hert, Lutz Kettner, Kurt Mehlhorn and Michael Seel, Boolean operations on 3D selective Nef complexes, data structure, algorithms, and implementation, Algorithms ESA 2003, Springer, 2003, 654 to 666
    locator: exact Boolean operations on general polyhedra, including non-manifold results, with exact arithmetic
  - paper: doi:10.1016/j.comgeo.2006.11.009
    title: Peter Hachenberger, Lutz Kettner and Kurt Mehlhorn, Boolean operations on 3D selective Nef complexes, optimized implementation and experiments, Computational Geometry 38(1-2), 2007, 64 to 99
    locator: the experiments on the cost of exact Booleans
---

Mesh Boolean operations take two solids, each given by a closed triangle mesh, and produce a closed triangle mesh of their union, intersection or difference. They are the triangle mesh form of the [Boolean operations on solids](/solid-boolean-operations/) of CAD, and the basic step of [constructive solid geometry](/constructive-solid-geometry/) on meshes. The problem is easy to state and hard to solve reliably. The new vertices are intersection points of edges and triangles, and the hard cases are exactly the common ones in practice: faces that coincide or nearly coincide, edges that touch, vertices that lie on faces, and input meshes that are themselves not clean. Robustness in these cases is the core of the problem.

## In plain words

Take two solid objects, each described by its skin of small triangles. Their union is everything inside either one, their intersection is what is inside both, and the difference is what is inside the first and not the second. The task is to build the skin of the result.

Where the two skins cross, new edges appear. Pieces of each skin are kept or thrown away depending on whether they are inside the other object. The result must again be a closed skin with no gaps, so that it has an inside and an outside.

The difficulty is precision. When two faces lie almost on top of each other, a computer that rounds numbers can decide "inside" in one place and "outside" in the next, and the result gets holes or extra faces.

## Definition

**Input.** Two triangle meshes $A$ and $B$ with rational or floating point vertex coordinates, with faces oriented so that the outward normal follows the right-hand rule. In the clean case each is a closed oriented [manifold mesh](/manifold-mesh/) without self-intersections, which bounds a solid. In the general case, each is any *closed* mesh, meaning that every edge is used as often in one direction as in the other.

**Inside.** For a point $p$ not on $A$, the winding number $w_A(p)$ is the number of times the surface $A$ wraps around $p$, the 3D form of the [winding number of a polygon](/winding-number-algorithm/). For a clean mesh it is 1 inside and 0 outside. The solid of $A$ is the closure of $\{p : w_A(p) > 0\}$. This definition also gives a meaning to self-intersecting and nested input: a region inside two overlapping shells of $A$ has $w_A = 2$ and is inside.

**Output.** For the union, the boundary of the regularized set $\{w_A > 0 \text{ or } w_B > 0\}$; for the intersection, $\{w_A > 0 \text{ and } w_B > 0\}$; for the difference, $\{w_A > 0 \text{ and not } w_B > 0\}$. Regularization, as in [regularized set operations](/regularized-set-operations/), removes parts of zero volume, such as the shared face of two cubes that touch. The output is a closed oriented triangle mesh with no self-intersections whose solid is that set. Its vertices are input vertices or intersection points of input edges and triangles.

**Exactness.** An exact output has rational vertices. An intersection of the edge $pq$ with the plane of triangle $abc$ is $p + t(q - p)$ with $t = \mathrm{ORIENT3D}(a, b, c, p) / (\mathrm{ORIENT3D}(a, b, c, p) - \mathrm{ORIENT3D}(a, b, c, q))$, where ORIENT3D is the [orientation test](/orientation-test/). Its coordinates are ratios of polynomials of degree 4 and 3 in the input coordinates, so they need about four times the bits of the input. In floating point, the signs that decide whether a piece is inside are subject to [catastrophic cancellation](/catastrophic-cancellation/) whenever faces nearly coincide, and [exact predicates](/shewchuk-expansion-sum/) or exact arithmetic are needed to get them right. This is the [geometric robustness problem](/geometric-robustness-problem/) in its most visible form.

## Variants

- **Exact or rounded output.** The output keeps rational coordinates, or is rounded to doubles. Rounding can create new self-intersections.
- **Manifold or not.** The exact result can be non-manifold, for example two cubes that share only an edge. Some uses require a manifold output and resolve such edges by a choice.
- **Many inputs.** A rule on several winding numbers, such as "inside at least two of five solids", or a whole CSG tree at once.
- **Self-union.** One input, with the rule $w > 0$: this removes the self-intersections of a mesh, a step of the [mesh repair problem](/mesh-repair-problem/).
- **Broken input.** Meshes with holes or gaps have no integer winding number; the inside is then decided by the [generalized winding number](/generalized-winding-number/) with a threshold.
- **Approximate.** Volumetric methods convert the solids to voxels or a distance field, combine them, and extract a new surface; the result is closed but moves every face.

## Examples

**Two offset cubes.** Let $A = [0, 1]^3$ and $B = [\tfrac12, \tfrac32]^3$, each with 12 triangles. They overlap in the cube $[\tfrac12, 1]^3$ of volume $1/8$. The union has volume $2 - 1/8 = 15/8$, the intersection $1/8$, and the difference $A - B$ has volume $1 - 1/8 = 7/8$. The difference is the unit cube with one corner notch; it has 9 planar faces: the three faces of $A$ at $x = 0$, $y = 0$, $z = 0$, the three faces at $x = 1$, $y = 1$, $z = 1$, each now an L-shaped polygon, and three squares of side $1/2$ from the faces of $B$ at $x = \tfrac12$, $y = \tfrac12$, $z = \tfrac12$, whose orientation is reversed so that their normals point out of the result.

**Touching cubes.** Let $A = [0, 1]^3$ and $B = [1, 2] \times [0, 1]^2$. The union is the box $[0, 2] \times [0, 1]^2$ of volume 2, and the shared face at $x = 1$ disappears. The regularized intersection is empty, although the sets meet in a square. A method that decides inside and outside with a tolerance, or with rounded signs, may keep parts of the shared face or leave a gap.

**Equal cubes.** If $B = A$, the union, the intersection and $A$ are the same, and every face of $A$ coincides with a face of $B$. This is the extreme case of coplanar faces.

**A self-intersecting input.** If $A$ is a single mesh made of two overlapping cube shells, the overlap has $w_A = 2$. The self-union, rule $w_A > 0$, gives one clean surface around both cubes.

## Known algorithms

| method | input | exact | notes |
|---|---|---|---|
| [mesh arrangements](/mesh-arrangements/) (Zhou, Grinspun, Zorin and Jacobson 2016) | closed meshes, also self-intersecting, nested or overlapping | yes | cuts all triangles exactly and labels cells by winding numbers; any rule on several inputs |
| Nef polyhedra (Granados and coauthors 2003, in CGAL) | general polyhedra, including non-manifold ones | yes | a complete structure with local views at each vertex; large and slow in practice |
| plane-based methods (Bernstein and Fussell 2009; Campen and Kobbelt 2010) | closed meshes | yes, by representing points as intersections of planes with bounded bit lengths | faster than rational arithmetic |
| [BSP trees](/bsp-tree/) (Thibault and Naylor 1987) | polyhedra | with exact predicates | merges the binary space partitions of the two solids |
| floating point methods with tolerances | clean closed meshes | no | fast; fail on coincident or nearly coincident faces |
| volumetric methods, as in [spatial occupancy enumeration](/spatial-occupancy-enumeration/) and [volumetric mesh repair](/volumetric-mesh-repair/) | any, even broken | no | always closed output, but resampled |
| [generalized winding number](/generalized-winding-number/) labelling | broken or open meshes | no | a soft inside test for input without a defined inside |

All the exact methods share the first step, finding the pairs of triangles that meet, which is the [mesh self-intersection](/mesh-self-intersection/) problem with [triangle-triangle intersection](/triangle-triangle-intersection/) tests.

## Bounds

- **Output size.** The output can have $\Theta(n m)$ triangles for inputs of $n$ and $m$ triangles. Let $A$ be a comb of $k$ thin parallel plates joined by a back, and $B$ the same comb turned by $90°$, with its plates perpendicular to those of $A$ and placed so that every plate of $A$ crosses every plate of $B$ while the two backs stay apart. Each input has $O(k)$ triangles, and the intersection has $k^2$ separate boxes. So any method that writes the output needs $\Omega(n m)$ time in the worst case.
- **Bit length.** Exact intersection vertices need about four times the bits of the input coordinates, as shown in the definition. Vertices of later operations on these results grow further, unless the method keeps points as intersections of input planes.
- **Detection.** Deciding whether two closed meshes intersect at all contains the detection of a crossing pair of triangles, which takes $\Omega(N \log N)$ time for $N$ triangles in the algebraic decision tree model, as on the [mesh self-intersection](/mesh-self-intersection/) page.
- **What is proved and what is measured.** The exact methods are proved correct for their stated input, in exact arithmetic. Their running times on real meshes, and the failure rates of floating point methods on collections of meshes, are measured.

## Reductions

- **From polygon Booleans.** Extruding two polygons to prisms of the same height turns a [polygon union](/polygon-union/) or difference into a mesh Boolean, so mesh Booleans are at least as hard as their planar form.
- **To an arrangement.** A Boolean is a selection of cells of the arrangement of the input triangles by a rule on winding numbers, the reduction used by [mesh arrangements](/mesh-arrangements/).
- **Into CSG evaluation.** Evaluating a CSG tree on meshes is a sequence of Booleans, or one arrangement with a rule for the whole tree; this is the mesh form of [boundary evaluation](/boundary-evaluation/).
- **Into repair.** A self-union removes self-intersections, which is part of the [mesh repair problem](/mesh-repair-problem/).

## Applications

- **CAD on meshes.** Combining scanned or exported parts, cutting holes, and adding fixtures, where a B-rep is not available.
- **3D printing.** Merging overlapping parts into one printable solid, hollowing, and adding support or text.
- **Machining simulation.** The stock minus the swept volume of the tool, step by step.
- **Games and film.** Fracture and destruction effects, and modelling by adding and subtracting shapes.
- **Medical and dental design.** Fitting implants and guides to scanned anatomy.

The difference from [solid Boolean operations](/solid-boolean-operations/) is the representation: there the faces are exact curved surfaces of a B-rep, and the intersection curves are computed by surface intersection; here all faces are flat triangles, which makes exact computation possible with rational numbers.

## References
