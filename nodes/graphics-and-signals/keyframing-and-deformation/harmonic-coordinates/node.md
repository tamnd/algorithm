---
tag: XS2ZCM
kind: algorithm
slug: harmonic-coordinates
name: Harmonic coordinates
aliases:
- harmonic cage coordinates
area: graphics-and-signals/keyframing-and-deformation
level: advanced
summary: Cage coordinates that solve Laplace's equation inside the cage on a grid; they are nonnegative and decay with distance inside the cage, even for concave cages.
solves: [shape-deformation]
model: real-ram
complexity:
  vars: {G: "the number of grid cells across the cage", n: "the number of cage vertices", N: "the number of points to deform"}
  time: {precompute: "O(G^4 + n G^3)", per_point: "O(n)", all: "O(G^4 + n G^3 + N n)"}
  space: {extra: "O(G^3 + n G^2)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
prereqs: [cage-based-deformation, finite-difference-method]
see_also: [cage-based-deformation, generalized-barycentric-coordinates, green-coordinates, floater-mean-value-coordinates, shape-deformation, poisson-equation, multigrid-method, laplacian-matrix]
sources:
  - paper: doi:10.1145/1276377.1276466
    title: "Pushkar Joshi, Mark Meyer, Tony DeRose, Brian Green and Tom Sanocki, Harmonic coordinates for character articulation, SIGGRAPH 2007, ACM Transactions on Graphics 26(3), article 71, 2007"
    locator: the whole paper (the definition by the Laplace equation with piecewise linear boundary data, the nonnegativity and the comparison with mean value coordinates on concave cages, and the numerical solution on a grid)
  - paper: doi:10.1017/S0962492914000129
    title: "Michael S. Floater, Generalized barycentric coordinates and applications, Acta Numerica 24, 161-214, 2015"
    locator: the whole survey (harmonic coordinates among the generalized barycentric coordinates)
---

Harmonic coordinates are the weights of a [cage-based deformation](/cage-based-deformation/) that come from the Laplace equation.
The coordinate $h_i$ of cage vertex $i$ is the harmonic function inside the cage that equals 1 at vertex $i$, 0 at the other vertices, and is linear along each cage edge.
A point $p$ then moves to $\sum_i h_i(p)c'_i$, where $c'_i$ are the moved cage vertices.
Pushkar Joshi, Mark Meyer, Tony DeRose, Brian Green and Tom Sanocki (2007) introduced them at Pixar for posing characters with cages.
Unlike [mean value coordinates](/floater-mean-value-coordinates/), harmonic coordinates are never negative, so a vertex on the far side of a concave part of the cage cannot pull a point the wrong way.
They have no closed form; this page computes them in 2D with a finite difference solve on a grid.

## In plain words

Think of the cage as a wire frame that holds a flat sheet of soap film.
Lift one corner of the frame to height 1 and keep the other corners at 0, with the wire straight between corners.
The film takes the smoothest shape that the frame allows, and its height at a point is the coordinate of that corner at the point.
The film never dips below the lowest wire, so the height is never negative.
It also cannot see through walls: around a sharp inner corner of the frame, the film has to go around it.
Do this once for each corner, and each point of the shape has one weight per corner, which add up to 1.

## The problem

The input is a cage, a simple polygon with the vertices $c_1, \dots, c_n$ in counterclockwise order, and the grid spacing $\delta$.
On the boundary of the cage, the hat function $\phi_i$ of vertex $i$ is 1 at $c_i$, 0 at every other vertex, and linear on each edge.
The harmonic coordinate $h_i$ is the solution of

$$\Delta h_i = 0 \text{ inside the cage}, \qquad h_i = \phi_i \text{ on the boundary}.$$

The output is a discrete $h_i$ at the nodes of a grid with the spacing $\delta$, and then $h_i(p)$ at any point $p$ inside the cage, for the deformation $p \mapsto \sum_i h_i(p)c'_i$.

## The algorithm

Each interior node has four arms to its neighbours. An arm that leaves the cage is cut at its first crossing with the boundary, so its length $\ell$ is at most $\delta$; this is the Shortley-Weller stencil.

```pseudo id=main
HARMONIC(cage, δ)
L1  U ← the grid nodes strictly inside the cage
L2  for each node p in U, cut each arm of p at its first crossing with the cage, giving the length ℓ ≤ δ
L3      give the arm of length ℓ, opposite an arm of length ℓ', the weight a = 2 / (ℓ(ℓ + ℓ'))
L4      if the arm ends on the cage at q then add a φ_i(q) to b_i[p] for each i, else put -a in the row of p of A
L5  factor A = LU, with the diagonal of A equal to the sum of the weights of the arms of each node
L6  for each vertex i, solve A x_i = b_i
L7  h_i(p) ← x_i[p] for every p in U
DEFORM(p, c')
L8  return Σ_i h_i(p) c'_i, with h_i(p) by bilinear interpolation of the nodes
```

Lines L2 to L4 discretize $\partial^2 h/\partial x^2 + \partial^2 h/\partial y^2$ at each node with the uneven three-point formula in each direction.
Line L5 factors the matrix once; it is banded, with a band of width about $G$ when the nodes are numbered row by row, and it needs no pivoting because it is an M-matrix.
For line L8, a grid node outside the cage takes the boundary data at its nearest boundary point.
The paper of Joshi and others also uses a grid; the details of its solver are not repeated here.

## Example

The cage is the L shape with the vertices $(0, 0)$, $(2, 0)$, $(2, 1)$, $(1, 1)$, $(1, 2)$, $(0, 2)$; the vertex $(1, 1)$ is the inner, reflex corner.
The grid has $G = 16$ cells across the cage, so $\delta = 0.125$, with 161 interior nodes.
At the node $p = (0.875, 1.375)$ in the upper arm of the L, the six harmonic coordinates are about

$$h(p) = (0.0479,\ 0.0072,\ 0.0031,\ 0.5117,\ 0.3426,\ 0.0875).$$

The vertex $(2, 1)$ is hidden from $p$ behind the reflex corner: the segment from $p$ to it leaves the cage.
Its harmonic coordinate is small and positive, $0.0031$.
The [mean value coordinates](/floater-mean-value-coordinates/) at the same point are about $(0.0598, 0.0312, -0.0097, 0.4527, 0.3793, 0.0867)$, with a negative weight for that vertex.
So if the user drags $(2, 1)$ to the right, the mean value deformation moves $p$ to the left, against the drag, while the harmonic deformation moves it a little to the right.
The tests check these values, the nonnegativity at all nodes, the sum 1, the exact reproduction of linear functions at the nodes, and that the coordinate of $(1, 1)$ peaks close to $(1, 1)$.

## Correctness

The claims here are about the discrete coordinates, and the [proof](proofs/correctness.md) proves them.

- The constant 1 solves the discrete problem with the data $\sum_i \phi_i = 1$, and the solution is unique, so $\sum_i h_i = 1$ at every node.
- The Shortley-Weller formula is exact on quadratic polynomials, so a linear function $g$ satisfies the discrete equation with its own boundary values. The data $\sum_i \phi_i c_i$ is the identity on the boundary, because each $\phi_i$ is linear on edges. So $\sum_i h_i(p)c_i = p$ at every node: linear precision.
- The matrix $A$ has a positive diagonal, nonpositive entries off it, row sums at least 0, and a strictly dominant row in every connected set of nodes. So it is a nonsingular M-matrix with $A^{-1} \ge 0$. The right sides $b_i$ are nonnegative, so $h_i \ge 0$: a discrete maximum principle.
- Bilinear interpolation in L8 keeps the sum 1 and the nonnegativity, and keeps linear precision in cells whose four nodes are interior.

For the continuous problem, the strong maximum principle gives $0 < h_i < 1$ strictly inside the cage when the cage has at least three vertices, and $h_i$ is smooth inside.
The coordinates are not local in the strict sense: each $h_i$ is positive everywhere inside.
They do decay with the distance from vertex $i$ measured inside the cage, which the test of the peak measures for one cage; this decay is an observed property, not a bound proved here.

## Complexity

Let $G$ be the number of cells across the cage, so there are $O(G^2)$ unknowns.
Lines L1 to L4 test each node against the cage and cut each arm in $O(n)$ time, so they cost $O(nG^2)$.
The band LU of line L5 has a band of width $O(G)$, so it costs $O(G^4)$ time and $O(G^3)$ memory; each solve of line L6 costs $O(G^3)$, and there are $n$ of them.
The values take $O(nG^2)$ memory.
One evaluation of line L8 reads four nodes with $n$ values each, plus a nearest boundary point in $O(n)$ for outside nodes, so it costs $O(n)$.
A [multigrid](/multigrid-method/) or [conjugate gradient](/conjugate-gradient-method/) solver makes the precomputation close to linear in the number of unknowns; the band LU is used here because it is short and exact up to rounding.

## Properties

- **Partition of unity (proved).** $\sum_i h_i = 1$, so a translation of the cage translates the shape.
- **Linear precision (proved, at the nodes).** $\sum_i h_i(p)c_i = p$ at every node, so the rest cage gives the identity there. Between nodes near the boundary, the bilinear interpolation leaves an error of order $\delta$.
- **Nonnegative (proved).** $h_i \ge 0$ at every node, for every simple cage, convex or not.
- **Interpolation on the boundary (by definition).** On the cage boundary $h_i = \phi_i$, so the cage edges map linearly onto the moved cage edges.
- **Bilinear on rectangles (proved).** On an axis-aligned rectangle the discrete coordinates are exactly the bilinear coordinates, because bilinear functions are harmonic and the stencil is exact on them.
- **Decay inside the cage (measurement).** The coordinate of a vertex is largest near the vertex and small at points that are far from it along paths inside the cage.
- **Discretization error (known, not proved here).** The Shortley-Weller scheme converges with order $\delta^2$ for smooth solutions; at reflex corners the exact $h_i$ is not smooth, and the convergence there is slower.

## Variants and improvements

- **3D cages.** The same definition works for a closed polyhedral cage with triangle faces and linear data on each face; Joshi and others work with 3D character cages.
- **Faster solvers.** [Multigrid](/multigrid-method/), [conjugate gradients](/conjugate-gradient-method/), [Gauss-Seidel](/gauss-seidel-method/) or [successive over-relaxation](/successive-over-relaxation/) replace the band LU for large grids.
- **Finite elements.** A triangulation of the cage interior with the [finite element method](/finite-element-method/) follows the boundary exactly instead of cutting grid arms.
- **Closed forms.** [Mean value coordinates](/floater-mean-value-coordinates/) are closed form but can be negative, and [Green coordinates](/green-coordinates/) add the edge normals to keep shapes conformal in 2D.
- **Bounded biharmonic weights.** [Bounded biharmonic weights](/bounded-biharmonic-weights/) solve a fourth-order problem with bound constraints, for handles that are points and bones as well as cages.

## When to use it

Use harmonic coordinates when the cage is concave, for example a cage around the legs or fingers of a character, and mean value coordinates would let one part pull on another across a gap.
The precomputation is heavy but runs once per cage, and after it each point has fixed weights, so posing is as cheap as for any cage.
If the cage is convex or nearly so, or if the weights must have a closed form, [mean value coordinates](/floater-mean-value-coordinates/) are simpler.

## Pitfalls

- **Grid too coarse.** Thin parts of the cage that are narrower than the grid spacing have no interior nodes and get only boundary data; choose $\delta$ well below the smallest feature.
- **Nodes on the boundary.** A node that lies on the cage within rounding must be treated as a boundary node, or the cut arm has length near 0 and the weight $a$ blows up.
- **Outside points.** The coordinates are defined only inside the cage. Points of the shape that stick out need a cage that encloses them.
- **Linear precision between nodes.** Near the boundary, the interpolated coordinates reproduce linear functions only up to order $\delta$, so the rest cage moves such points a little.
- **Storage.** One value per node per vertex is a lot in 3D; store only the coordinates at the points of the shape after the solve.

## Implementations

## History

Joshi, Meyer, DeRose, Green and Sanocki presented harmonic coordinates at SIGGRAPH 2007, from work on character articulation at Pixar.
They showed that the mean value coordinates of Ju, Schaefer and Warren (2005) can be negative inside concave cages and proposed the solutions of the Laplace equation instead, computed numerically.
Floater (2015) surveys harmonic coordinates together with the other [generalized barycentric coordinates](/generalized-barycentric-coordinates/).

## References
