---
tag: B7WM22
kind: algorithm
slug: isosurface-stuffing
name: Isosurface stuffing
aliases:
- Labelle-Shewchuk stuffing
area: cad/mesh-generation-for-analysis
level: research
summary: Labelle and Shewchuk's tetrahedral mesher for smooth domains that warps a body-centred cubic lattice to the surface, with proven dihedral angle bounds.
solves: [mesh-generation]
model: real-ram
complexity:
  vars: {N: the number of lattice points in a box around the domain, k: the number of output tetrahedra}
  time: {expected: O(N)}
  space: {extra: O(N + k)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 2007
  people: [François Labelle, Jonathan Richard Shewchuk]
  note: Labelle and Shewchuk presented isosurface stuffing at SIGGRAPH 2007, with dihedral angle bounds proved by a computer-assisted interval arithmetic search over all stencil configurations.
prereqs: [marching-tetrahedra, octree-mesh-generation, sliver-tetrahedron]
see_also: [octree-mesh-generation, tetrahedral-delaunay-refinement, sliver-exudation, delaunay-surface-meshing, quadtree-mesh-generation, mesh-quality-measures, isosurface-extraction, distmesh]
sources:
  - paper: doi:10.1145/1276377.1276448
    title: François Labelle and Jonathan Richard Shewchuk, Isosurface stuffing, fast tetrahedral meshes with good dihedral angles, ACM Transactions on Graphics 26(3), 2007, article 57 (SIGGRAPH 2007)
    locator: Section 3 (the four steps, the stencils and the Parity Rule), Section 4.1 (Theorem 1 and Table 1, the dihedral angle bounds and the parameters alpha), Section 4.2 (Theorems 2 and 3), Section 5 (graded meshes), Section 2 (the comparison with other methods)
  - paper: doi:10.1145/1137856.1137907
    title: François Labelle, Sliver removal by lattice refinement, Proceedings of the 22nd ACM Symposium on Computational Geometry, 2006, 347 to 356
    locator: the lattice mesher with dihedral angles between 30 and 135 degrees that does not conform to the boundary (general locator; the numbers are quoted from Section 2 of Labelle and Shewchuk)
  - paper: doi:10.1016/S0022-0000(05)80059-5
    title: Marshall Bern, David Eppstein and John Gilbert, Provably good mesh generation, Journal of Computer and System Sciences 48(3), 1994, 384 to 409
    locator: the warping of a background grid onto the boundary (general locator), which Labelle and Shewchuk adopt
  - paper: doi:10.1017/S001309150007783X
    title: D. M. Y. Sommerville, Space-filling tetrahedra in Euclidean space, Proceedings of the Edinburgh Mathematical Society 41, 49 to 57
    locator: the tetrahedra that tile space, among them the BCC tetrahedron (general locator)
---

Isosurface stuffing is a tetrahedral mesher for a domain with a smooth boundary given by a function $f$, positive inside. It lays a body-centred cubic (BCC) lattice over the domain, moves the lattice points that lie too close to the surface onto it, and fills each lattice tetrahedron near the surface from a short table of stencils. Labelle and Shewchuk (2007) proved, with a computer-assisted search, that every dihedral angle of the output lies between $10.7843°$ and $164.7373°$ for a uniform lattice. Few tetrahedral meshers have a proved dihedral angle bound with a useful constant and also fit the boundary. It is also fast, because it does no point location and no geometric search.

## In plain words

Fill space with a lattice: the corners of all unit cubes plus their centers. Join them into identical tetrahedra whose angles are only 60° and 90°. These are very good shapes. Now look at the boundary of the domain. Each lattice edge that crosses it gets a cut point where it crosses. If a cut point lies very close to one end of its edge, cutting there would make a thin tetrahedron, so move that lattice point onto the surface instead. After all such moves, cut each lattice tetrahedron at the surface by a fixed rule. The moves keep every piece fat, and a computer-checked proof gives the exact limits.

## The problem

The input is a function $f : \mathbb{R}^3 \to \mathbb{R}$ that is positive inside the domain and negative outside, a way to find the point where $f = 0$ on a segment, and a lattice spacing $h$. The output is a set of tetrahedra that meet face to face (a [tetrahedralization](/tetrahedralization/)), whose boundary vertices lie on the surface $f = 0$. On this page $f(x) = r^2 - |x - c|^2$, so the domain is a ball, and the zero on a segment is the root of a quadratic.

This page makes three kinds of claim, and they must be kept apart.

- *Proved bound with its constant, cited.* Theorem 1 of Labelle and Shewchuk: with the parameters $\alpha_{\text{long}} = 0.28511$ and $\alpha_{\text{short}} = 0.39882$, every dihedral angle of every output tetrahedron lies in $[10.7843°, 164.7373°]$, and every plane angle in $[9.0454°, 154.9845°]$. The proof is computer assisted: interval arithmetic over a quadtree subdivision of the parameter space of each stencil case. It holds for every cut function, smooth or not, since the search covers every position of the cut points. The bounds are rounded outward and are tight to within $0.0001°$: some cut functions produce these angles. This page does not repeat that proof.
- *Proved here.* The BCC tetrahedron has dihedral angles $60°$ (four times) and $90°$ (twice), volume $h^3/12$, circumradius $\sqrt{5/16}\,h$ and radius-edge ratio $\sqrt{5/12} \approx 0.6455$. The BCC tetrahedra tile space and are Delaunay. The stencils fit face to face: the Parity Rule gives the same diagonal from both sides of a face, and every prism has a split. See `proofs/correctness.md`.
- *Measured, no guarantee.* On balls the angles are far better than the bound. In the example below they lie in $[19.08°, 135.68°]$, and over 25 random balls with $r/h$ between $1.6$ and $6.2$ the worst were $18.48°$ and $149.78°$. Labelle and Shewchuk show meshes of real models with all angles in $[14°, 158°]$. The proved bound is tight over all inputs, but the inputs that reach it are rare. Against Delaunay methods the gap is the other way round: Labelle and Shewchuk note that the provable dihedral angle bounds of Delaunay refinement with sliver removal are below $0.1°$ and probably below a millionth of a degree, while these methods give much better angles in practice.

A [radius-edge ratio](/radius-edge-ratio/) bound would not be enough. A [sliver](/sliver-tetrahedron/) has radius-edge ratio as small as $1/\sqrt2$ while its dihedral angles approach $0°$ and $180°$. Isosurface stuffing bounds the dihedral angles directly, so it has no slivers. Its radius-edge ratio is not what it controls: in the example it reaches $2.21$.

## The algorithm

A lattice point has doubled coordinates $(i, j, k)$, all even or all odd, at position $\frac{h}{2}(i, j, k)$. The even points form the cubic lattice and the odd points the shifted lattice. *Black* edges join neighbors at distance $h$ along an axis; *red* edges join a cube corner to a cube center, length $\frac{\sqrt3}{2} h$. Each BCC tetrahedron has two opposite black edges and four red edges. A lattice point $q$ is *violated* if a cut point on one of its edges lies at less than $\alpha$ times the edge length from $q$, with $\alpha = \alpha_{\text{long}}$ on black edges and $\alpha_{\text{short}}$ on red edges.

```pseudo id=main
ISOSURFACE-STUFFING(f, h)
L1  compute f(q) at every lattice point q in a box around the domain
L2  for each edge pq with f(p) f(q) < 0, find its cut point, the zero of f on pq
L3  for each lattice point q, in a fixed order:
L4      if q is violated by a cut point on one of its edges that still has one:
L5          move q to the nearest such cut point; set f(q) ← 0, which removes the cut points on its edges
L6  for each BCC tetrahedron τ, by the signs of f at its vertices:
L7      no positive vertex: drop τ (also when all four are zero)
L8      no negative vertex: output τ
L9      one positive vertex a: output the tetrahedron of a, the zero vertices and the cut points on the edges from a
L10     two positive, one zero, one negative: output the pyramid over the quadrilateral of the face ab with the negative vertex, split into 2
L11     two positive, two negative: output the prism between edge ab and the four cut points, split into 3
L12     three positive, one negative: output the truncated tetrahedron, a prism, split into 3
L13     output the pieces, with the moved positions of the moved points
L14 return the output tetrahedra
```

Each quadrilateral on a face of $\tau$ has corners $a, b$ (positive) and the cut points $c$ on $bx$ and $d$ on $ax$, where $x$ is the negative vertex of the face. It is split by one of the diagonals $ac$ or $bd$:

- if $ax$ or $bx$ is black, the diagonal that ends at the cut point on that black edge;
- otherwise $ab$ is black and the *Parity Rule* applies: if $a$ and $b$ are on the cubic lattice, take $ac$ when an odd number of the coordinates of $a$ are greater than those of $c$, and $bd$ otherwise; on the shifted lattice the choice is reversed.

The quadrilateral of a two-positive prism that lies on the surface is inside $\tau$, so its diagonal is free; the implementation takes the one for which the prism splits. A prism can be cut into three tetrahedra with given diagonals on its three quadrilaterals exactly when the diagonals do not form a cycle, which is when some vertex is the end of two of them.

L5 moves $q$ to the cut point that violates it and lies nearest to it, as the paper suggests. Ties go to the smaller neighbor. The order of L3 matters only when two neighbors are both violated by their shared cut point; the first one moved removes it.

The implementation stores the lattice in doubled integer coordinates. It finds each cut point as the float root of the quadratic and then keeps it as an exact fraction, so all orientation tests on the output are exact. It orients every piece by the unmoved positions, where it is a part of the BCC tetrahedron, and the tests then check that every output tetrahedron has positive volume after the moves.

## Example

Take the ball with center $(0.03, -0.02, 0.01)$ and $r = 1$, and $h = 1/4$. The counts come from the implementation, and the test file checks them.

| Step | Lines | Result |
|---|---|---|
| values | L1 | 3456 lattice points in the box, 544 inside the ball |
| cut points | L2 | 1288 lattice edges cross the sphere |
| warp | L3 to L5 | 242 lattice points move onto the sphere, 84 of them along black edges; 172 cut points remain |
| stencils | L6 to L12 | 16698 BCC tetrahedra: 1721 with four positive vertices and 1181 with positive and zero vertices only are kept whole, 464 with one positive vertex and some negative give one piece each, 69 pyramids give 2, 9 two-positive prisms and 5 three-positive prisms give 3; the other 13249 are dropped |
| output | L13, L14 | 834 vertices and 3546 tetrahedra |

The dihedral angles lie in $[19.08°, 135.68°]$, inside the proved range $[10.78°, 164.74°]$. The mesh has volume $4.1222$, against $4.1888$ for the ball, and every boundary vertex lies on the sphere up to rounding: $|f| < 3 \cdot 10^{-16}$ there. The radius-edge ratio reaches $2.21$. Without step 3, that is with $\alpha = 0$, the same input gives 6628 tetrahedra with a smallest dihedral angle of $0.17°$ and a largest of $169.62°$: the warping is what removes the slivers.

## Correctness

Correctness has two parts with different status.

*The mesh is a tetrahedralization of a region bounded by the surface.* This is proved in `proofs/correctness.md`. The BCC tetrahedra are Delaunay with strictly empty circumspheres, so they tile space without overlap, and a volume count (12 tetrahedra of volume $h^3/12$ per cubic cell) shows they also leave no gap. Each output piece lies in one BCC tetrahedron. What a stencil puts on a face of $\tau$ depends only on the signs at the three vertices of the face and on the quadrilateral rule, and the rule gives the same diagonal for the face $abx$ and for $bax$. So two neighbors put the same triangles on their common face. The prisms always split: in the three-positive case the cut point on the black edge at the negative vertex is the end of two diagonals, and in the two-positive case the two face diagonals have no common end, so exactly one of the two diagonals of the surface quadrilateral avoids a cycle.

*The angles are bounded.* This is Theorem 1 of the paper, proved by computer. Its key facts are that a moved lattice point has value zero and lies within the $\alpha$ part of one of its edges (its *asterisk*), that a lattice point labelled positive or negative was not moved, and that no edge at a moved point carries a cut point. Each stencil piece then has each vertex fixed or on a segment, and the extremes of a dihedral angle occur with the two vertices off the edge at ends of their segments. This reduces each case to at most two parameters, which a quadtree with interval arithmetic covers.

The paper also proves that every boundary vertex lies on the surface, that a point farther than $\omega h$ from the surface is classified correctly for a constant $\omega$ given in Theorem 2, and that for a smooth surface with distance $d_M$ to the medial axis the mesh boundary is within $\omega h$ of the surface in both directions when $d_M > \omega h$, and is ambient isotopic to it when $h / d_M$ is small enough (Theorem 3).

## Complexity

Each lattice point is evaluated once, each edge gets at most one cut point, and each BCC tetrahedron gives at most three pieces, so the time is $O(N)$ evaluations and root findings, with hashing for the lattice, and the space is $O(N + k)$. With a uniform lattice $N$ grows as $h^{-3}$. The graded version uses an octree, so the count grows as $h^{-2}$ near the surface plus a coarse interior. On a dense domain, Labelle and Shewchuk report about 510 tetrahedra per millisecond for their prototype, against about 157 for Pyramid, their Delaunay mesher, because stuffing does far fewer numerical calculations and needs simpler data structures.

## Properties

- **Proved dihedral angle bound with explicit constant.** $[10.7843°, 164.7373°]$ for the parameters on this page, by a computer-assisted proof, tight to within $0.0001°$.
- **Boundary fit.** Every vertex on the mesh boundary lies on the surface $f = 0$.
- **Deterministic.** The result depends on the warping order only through ties of the kind described above.
- **Not exact.** The cut points are float roots, kept exactly afterwards. With exact roots the method would need algebraic numbers.
- **No sharp features.** Edges and corners of the domain are rounded off.
- **Lattice aligned.** Most tetrahedra are exact BCC tetrahedra, so more than half of the dihedral angles are $60°$ or $90°$.

## Variants and improvements

- **Other parameters.** Table 1 of the paper gives several choices of $(\alpha_{\text{long}}, \alpha_{\text{short}})$. Optimizing the largest angle instead gives $[8.9716°, 158.7403°]$ with $\alpha = (0.26649, 0.36918)$. Safe variants, in which no BCC tetrahedron can invert during warping, give $[9.3171°, 161.6432°]$ or $[9.0551°, 160.5331°]$, and ordered warping gives $[9.7766°, 163.5685°]$.
- **Both sides.** The double-sided rows of Table 1 mesh the inside and the outside with compatible tetrahedra, with weaker bounds: $[6.4917°, 164.1013°]$ and $[7.6872°, 168.0481°]$.
- **Graded interior.** A BCC-like octree coarsens the mesh away from the surface while the tetrahedra at the surface stay of one size. The dihedral bounds of Table 1 still hold. If the surface tetrahedra vary in size too, the authors cannot guarantee better than $1.66°$.
- **Linear cut points.** Placing each cut point by linear interpolation of $f$ instead of on the surface keeps the angle bound but gives up the boundary guarantees.
- **Lattice refinement without a fitted boundary.** Labelle (2006) gives a lattice method with all dihedral angles between $30°$ and $135°$ for meshes that do not conform to the boundary.
- **Other boundary-fitted methods.** [Octree mesh generation](/octree-mesh-generation/) cuts cubes without moving vertices and has no bound at the surface. [Tetrahedral Delaunay refinement](/tetrahedral-delaunay-refinement/) bounds the radius-edge ratio, and [sliver exudation](/sliver-exudation/) removes slivers with a far weaker proved angle.

## When to use it

Use it for domains with smooth boundaries given by a level set, a signed distance function or a voxel image, when every tetrahedron must have good dihedral angles and the mesh is needed fast or often, as in simulations that remesh a moving liquid or soft tissue. It is a poor choice when the domain has sharp edges or corners that must be kept, or when the boundary is a given triangle mesh that must appear in the output; use [Delaunay surface meshing](/delaunay-surface-meshing/) followed by [Delaunay refinement](/tetrahedral-delaunay-refinement/) there.

## Pitfalls

- **Skipping the warp.** Cutting the lattice where the surface crosses it, without moving vertices, gives slivers ($0.17°$ in the example).
- **Inconsistent diagonals.** A diagonal rule that depends on the tetrahedron, not on the face, makes neighbors disagree and leaves a crack. The Parity Rule and the black-edge rule depend only on the face.
- **Quadruple-zero tetrahedra.** A BCC tetrahedron whose four vertices all moved onto the surface may be very flat. Dropping it keeps the bounds of Table 1. A well-shaped one is a sign that the lattice is too coarse for the surface.
- **Expecting the radius-edge ratio to be small.** The method bounds dihedral angles, not the radius-edge ratio, which is a different measure and does not exclude slivers by itself.
- **Too coarse a lattice.** Features smaller than about $h$ are lost or meshed with the wrong topology. Theorem 3 needs $h$ small against the distance $d_M$ to the medial axis.
- **Floating-point cut points.** Rounding can put a cut point exactly at an end of its edge. Clamp it and test orientations exactly, as here.

## Implementations

## History

Body-centred cubic tetrahedra were listed by Sommerville among the tetrahedra that tile space, and Fuchs and Naylor proposed the BCC lattice for meshing. Bern, Eppstein and Gilbert introduced the warping of a background grid onto a boundary in their quadtree mesher of 1990. Labelle and Shewchuk combined the BCC lattice, warping and a table of stencils in isosurface stuffing, presented at SIGGRAPH 2007, and proved its dihedral angle bounds by an interval arithmetic search. Earlier provable tetrahedral meshers either bounded only the radius-edge ratio or had dihedral angle bounds far below one degree.

## References
