---
tag: BD4HAH
kind: algorithm
slug: tutte-embedding
name: Tutte embedding
aliases:
- barycentric mapping
- Tutte parameterization
area: cad/mesh-processing
level: core
summary: Fixes the boundary on a convex polygon and puts each inner vertex at a convex combination of its neighbours, by one sparse linear solve, which gives a planar embedding.
solves: [mesh-parameterization]
model: real-ram
complexity:
  vars: {n: the number of inner vertices}
  time: {worst: O(n^3), nested_dissection: O(n^(3/2))}
  space: {extra: O(n^2), nested_dissection: O(n log n)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1963
  people: [W. T. Tutte, Michael S. Floater]
  note: Tutte drew 3-connected planar graphs by barycentric positions in 1963. Floater used the same linear system with positive weights to parameterize triangulated surfaces in 1997.
prereqs: [mesh-parameterization, tutte-spring-theorem, convex-combination, laplacian-matrix]
see_also: [floater-mean-value-coordinates, least-squares-conformal-maps, angle-based-flattening, cotangent-laplacian, fary-theorem, nested-dissection, conjugate-gradient-method, orientation-test]
sources:
  - paper: doi:10.1112/plms/s3-13.1.743
    title: W. T. Tutte, How to draw a graph, Proceedings of the London Mathematical Society s3-13(1), 1963, 743 to 767
    locator: the barycentric construction and the theorem that it draws a 3-connected planar graph without crossings
  - paper: doi:10.1016/S0167-8396(96)00031-3
    title: Michael S. Floater, Parametrization and smooth approximation of surface triangulations, Computer Aided Geometric Design 14(3), 1997, 231 to 250
    locator: the parameterization by convex combinations with the boundary on a convex polygon, and the shape-preserving weights
  - paper: doi:10.1090/S0025-5718-02-01466-7
    title: Michael S. Floater, One-to-one piecewise linear mappings over triangulations, Mathematics of Computation 72(242), 2003, 685 to 696
    locator: the proof that the convex combination map of a triangulated disk is one to one, also for a boundary that is convex but not strictly convex
  - paper: doi:10.1007/3-540-26808-1_9
    title: Michael S. Floater and Kai Hormann, Surface parameterization, a tutorial and survey, in Advances in Multiresolution for Geometric Modelling, Springer, 2005, 157 to 186
    locator: the section on barycentric mappings and the choice of weights
  - book: isbn:9781568814261
    title: Mario Botsch, Leif Kobbelt, Mark Pauly, Pierre Alliez and Bruno Lévy, Polygon Mesh Processing, AK Peters, 2010
    locator: Chapter 5, Parametrization (barycentric mapping with fixed boundary)
---

The Tutte embedding maps a triangle mesh with the topology of a disk into the plane. It pins the boundary vertices, in their order, to the corners of a convex polygon, and it puts each inner vertex at a [convex combination](/convex-combination/) of its neighbours, $x_i = \sum_j \lambda_{ij} x_j$ with $\lambda_{ij} > 0$. These conditions are one sparse linear system. If the polygon is strictly convex, the solution is a one-to-one map of the mesh onto the polygon in which no triangle is flipped. This is the theorem of Tutte (1963) for graphs, see [Tutte's spring theorem](/tutte-spring-theorem/), in the form that Floater (1997, 2003) proved for triangulated disks. This page is the algorithm: the system, how to solve it, and how to check the result. The weights decide the shape of the map. Equal weights ignore the 3D geometry, and [mean value coordinates](/floater-mean-value-coordinates/) keep it better. It is the simplest method for the [mesh parameterization](/mesh-parameterization/) problem, and the only common one with a proof of global injectivity.

## In plain words

Think of the mesh as a net of rubber bands. Nail the edge of the net to the rim of a convex frame, in order, and let go. Each free knot moves until the pulls of its bands cancel. Then it sits at a weighted average of its neighbours.

The net that settles lies flat in the frame. No band crosses another, and no small triangle of the net is turned over. This is true for any net that is one piece without holes, if the frame is convex and every band pulls a little.

A stiffer band pulls its knot closer. If the strengths follow the shape of the surface, the flat net looks more like the surface. To find where the knots settle, a program solves one set of linear equations.

## The problem

The input is a triangle mesh $M$ with the topology of a disk: its Euler characteristic is $V - E + F = 1$, it has one boundary loop $b_1, \ldots, b_k$ with $k \ge 3$, and its faces are oriented so that the outward normal follows the right-hand rule, which makes the boundary loop run counterclockwise when the mesh lies flat. The input also gives a strictly convex polygon with corners $p_1, \ldots, p_k$ in counterclockwise order, and weights $\lambda_{ij} > 0$ for each inner vertex $i$ and neighbour $j$ with $\sum_j \lambda_{ij} = 1$. The output is a point $x_v \in \mathbb{R}^2$ for each vertex. Each triangle is mapped linearly, and the result must be one to one, with ORIENT2D$(x_a, x_b, x_c) > 0$ for every triangle $(a, b, c)$.

## The algorithm

ORIENT2D$(a, b, c) = (b_x - a_x)(c_y - a_y) - (b_y - a_y)(c_x - a_x)$ is the [orientation test](/orientation-test/). It is twice the signed area of the triangle.

```pseudo id=main
TUTTE-EMBED(M, p, λ)
L1  b_1, ..., b_k ← BOUNDARY-LOOP(M)                 ▷ in the orientation of the faces
L2  x_{b_t} ← p_t for t = 1, ..., k
L3  number the inner vertices 1, ..., n
L4  A ← I_n (n × n); r ← 0 (n × 2)
L5  for each inner vertex i and each neighbour j of i do
L6      if j is inner then A[i][j] ← A[i][j] − λ_ij
L7      else r[i] ← r[i] + λ_ij · x_j
L8  solve A X = r                                    ▷ two right-hand sides, x and y
L9  x_i ← X[i] for each inner vertex i
L10 return x

CHECK(M, x)
L11 for each triangle (a, b, c) of M do
L12     if ORIENT2D(x_a, x_b, x_c) ≤ 0 then return false
L13 return true
```

Row $i$ of the system is $x_i - \sum_{j \text{ inner}} \lambda_{ij} x_j = \sum_{j \in B} \lambda_{ij} x_j$. With symmetric weights, $w_{ij} = w_{ji} > 0$ and $\lambda_{ij} = w_{ij} / \sum_l w_{il}$, row $i$ times $\sum_l w_{il}$ is the inner block of a weighted [Laplacian matrix](/laplacian-matrix/). That block is symmetric and positive definite, so [Cholesky decomposition](/cholesky-decomposition/) or the [conjugate gradient method](/conjugate-gradient-method/) solves it. Uniform weights, $\lambda_{ij} = 1/\deg i$, are of this kind. Mean value weights are not symmetric, and need an LU solve or an iterative method for general matrices.

The common weights are these:

| weights | $\lambda_{ij}$ proportional to | positive | reproduces a planar mesh |
|---|---|---|---|
| uniform (Tutte) | $1$ | yes | no |
| shape-preserving (Floater 1997) | built from a local flattening of the 1-ring | yes | yes |
| mean value (Floater 2003) | $(\tan(\alpha_{j-1}/2) + \tan(\alpha_j/2)) / \lVert x_j - x_i \rVert$ | yes | yes |
| harmonic, the [cotangent Laplacian](/cotangent-laplacian/) | $\cot \alpha_{ij} + \cot \beta_{ij}$ | not always | yes |

**Degenerate cases.** A boundary vertex at a straight angle of the polygon (a convex but not strictly convex polygon) is allowed only if no inner edge joins two vertices of the same side, see the proof. A vertex of degree 2 or a non-manifold vertex is not allowed, because then the mesh is not a disk; BOUNDARY-LOOP rejects such input. Negative weights break the theorem.

## Example

Take a mesh with boundary vertices 0, 1, 2, 3 and inner vertices 4 and 5, and the triangles $(0,1,4)$, $(1,5,4)$, $(1,2,5)$, $(2,3,5)$, $(3,4,5)$, $(3,0,4)$. In 3D it could be a square roof with the ridge $45$. Pin the boundary to the square $(0,0)$, $(12,0)$, $(12,12)$, $(0,12)$ and use uniform weights. Vertex 4 has the neighbours 0, 1, 3, 5, and vertex 5 has 1, 2, 3, 4.

| step | value |
|---|---|
| L5 to L7, row of 4 | $x_4 - \tfrac14 x_5 = \tfrac14 (x_0 + x_1 + x_3) = (3, 3)$ |
| L5 to L7, row of 5 | $x_5 - \tfrac14 x_4 = \tfrac14 (x_1 + x_2 + x_3) = (6, 6)$ |
| L8 | $x_4 = (24/5, 24/5)$, $x_5 = (36/5, 36/5)$ |
| L11, ORIENT2D | $288/5$, $144/5$, $288/5$, $288/5$, $144/5$, $288/5$ for the six triangles |

All signs are positive, and the six values add up to $288$, twice the area of the square, so the triangles tile the square.

Now pin a wheel with centre 5 and boundary 0, 1, 2, 3, 4 to the polygon $(0,0)$, $(10,0)$, $(10,10)$, $(9,1)$, $(0,1)$, which is not convex. The centre goes to the average $(29/5, 12/5)$, and the five triangles have ORIENT2D values $24$, $42$, $-151/5$, $-63/5$, $29/5$. Two triangles are flipped. The convexity of the boundary is necessary.

**When the arithmetic is floating point.** The solve is well conditioned for small meshes, but the triangles of a Tutte map can be very small. Take 31 nested triangles $a_t b_t c_t$, $t = 0, \ldots, 30$, each joined to the next by a band of 6 triangles, with the outer one pinned to $(0,0)$, $(1,0)$, $(0,1)$. With uniform weights the area shrinks by a factor of about 50 per layer, and the innermost triangle has ORIENT2D $\approx 1.3 \times 10^{-50}$. The same system solved in IEEE double gives 49 of the 181 triangles a sign that is zero or negative, because the positions near the centre differ by less than the spacing of doubles there. The exact map has no such triangle. A float result with flips does not mean that the theorem fails. To decide the signs, compute in exact rational arithmetic, as in the code of this page, or test ORIENT2D with [exact predicates](/shewchuk-expansion-sum/) on the computed points. Exact predicates on rounded points can still report a flip, because rounding moves the points. This is the [robustness problem](/geometric-robustness-problem/) of geometry, and [catastrophic cancellation](/catastrophic-cancellation/) is its cause.

## Correctness

The system has one solution by the maximum principle: with the boundary fixed at 0, the largest value of a solution is attained at a vertex all of whose neighbours have the same value, and a path to the boundary carries it to 0. If the mesh has no chord, an inner edge between two boundary vertices, its graph is 3-connected, and [Tutte's spring theorem](/tutte-spring-theorem/) gives a drawing with no crossings in which the triangles are the faces. The boundary triangles are counterclockwise, and two triangles at an inner edge lie on opposite sides of it, so all triangles are counterclockwise. A chord cuts the disk into two smaller disks on two strictly convex polygons, and induction finishes the proof. The full proof is below.

## Complexity

The matrix has $n$ rows, one per inner vertex, and about $7n$ nonzero entries, because the average degree of a triangle mesh is about 6. Dense Gaussian elimination takes $O(n^3)$ time and $O(n^2)$ space, which is what the code of this page does for small meshes. The graph is planar, so [nested dissection](/nested-dissection/) with a [planar separator](/planar-separator-theorem/) orders the elimination with $O(n \log n)$ fill and $O(n^{3/2})$ operations. In practice a sparse Cholesky or LU factorization or a preconditioned iterative solver is used.

In exact arithmetic the size of the numbers also counts. By Cramer's rule each coordinate is a ratio of two $n \times n$ determinants, so its numerator and denominator have $O(n \log n)$ more bits than the input, and fraction-free elimination as in the [Bareiss algorithm](/bareiss-algorithm/) keeps the cost polynomial. For the nested triangles above, with 90 inner vertices, the exact coordinates have denominators of at most 25 digits.

## Properties

- **Globally injective.** With a strictly convex boundary and positive weights, the map is one to one, which most other parameterization methods do not guarantee.
- **Fixed boundary.** The boundary shape is chosen in advance. A circle or a square is common, and the distortion near the boundary can be large.
- **Linear.** One linear solve, with no iteration and no initial guess. The solution depends continuously on the weights.
- **Reproduction.** With weights that reproduce linear functions, a planar mesh whose boundary is already convex is mapped to itself.
- **Exact.** With rational weights and corners, the positions and all orientation signs are exact.

## Variants and improvements

- **Shape-preserving weights (Floater 1997).** For each inner vertex, flatten its 1-ring by keeping the edge lengths and scaling the angles to add up to $2\pi$, then take the barycentric coordinates of the centre in this flat ring. The map reproduces planar meshes, and it looks much more like the surface than the uniform map.
- **Mean value weights (Floater 2003).** The [mean value coordinates](/floater-mean-value-coordinates/) are positive and have a closed formula, so they are now the usual choice.
- **Harmonic weights.** The cotangent weights of the [cotangent Laplacian](/cotangent-laplacian/) give the discrete harmonic map of Eck and coauthors and of Pinkall and Polthier. It minimizes the Dirichlet energy, but some weights are negative on obtuse triangles, and then flips can occur.
- **Convex but not strictly convex boundary.** Floater (2003) proves that the map stays one to one if no inner edge joins two vertices on the same side. This allows a square with many boundary vertices on each side.
- **Free boundary.** [Least squares conformal maps](/least-squares-conformal-maps/) and [angle-based flattening](/angle-based-flattening/) let the boundary move, which lowers distortion but loses the guarantee.
- **Tutte maps as a start.** Methods that minimize a nonlinear distortion energy with barriers against flips start from a Tutte map, because it is the one map that is known to be valid.

## When to use it

Use it when a valid map with no flips is more important than low distortion: as a start for a nonlinear optimizer, for remeshing a patch, or for a robust texture layout of a patch that is close to a disk. Use mean value weights unless the mesh is planar, and pick a boundary polygon that follows the shape of the boundary, such as the boundary vertices placed on a circle in proportion to their arc length. Do not use it for long thin patches or patches with a very non-convex boundary, because the distortion is large; [mesh segmentation](/mesh-segmentation/) into more compact charts or a free-boundary method is better there.

## Pitfalls

- **A non-convex boundary.** The theorem needs a convex polygon. Mapping the boundary to its own projection is a common mistake.
- **Negative weights.** Cotangent weights on obtuse triangles can be negative, and then the map can fold.
- **Orientation of the boundary.** The polygon must run in the same direction as the boundary loop in the face orientation. If not, every triangle comes out with a negative sign.
- **Thin triangles.** The map is one to one in exact arithmetic, but the triangles near a long, narrow part of the mesh can be so small that float coordinates collapse them. See the example.
- **Not a disk.** A mesh with a handle or two boundary loops must be cut into a disk first; the seams are the cost.

## Implementations

## History

W. T. Tutte published "How to draw a graph" in 1963. He proved that the barycentric drawing of a 3-connected planar graph with a convex outer face has no crossings, which also gives a new proof of [Fáry's theorem](/fary-theorem/) for these graphs. Michael Floater used the same system with general positive weights to parameterize surface triangulations for surface fitting in 1997, and introduced shape-preserving weights. In 2003 he gave mean value coordinates and a direct proof that the map of a triangulated disk is one to one. Gortler, Gotsman and Thurston gave a short proof with discrete one-forms in 2006. The method is the reference point for every later parameterization method.

## References
