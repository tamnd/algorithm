---
tag: HE01QC
kind: algorithm
slug: boundary-first-flattening
name: Boundary first flattening
aliases:
- BFF
area: cad/mesh-processing
level: research
summary: Sawhney and Crane's conformal flattening that first fixes boundary scale factors or angles, then extends them inside by harmonic functions, with a few linear solves.
solves: [mesh-parameterization]
model: real-ram
complexity:
  vars: {n: the number of vertices, m: the number of boundary vertices}
  time: {worst: O(n^3), nested_dissection: O(n^(3/2)), new_target: O(n^2 + m)}
  space: {extra: O(n^2), nested_dissection: O(n log n)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 2017
  people: [Rohan Sawhney, Keenan Crane]
  note: Sawhney and Crane gave BFF in ACM Transactions on Graphics in 2017, with a discrete form of the Cherrier formula that ties the boundary scale factors to the boundary curvature.
prereqs: [mesh-parameterization, cotangent-laplacian, discrete-gauss-bonnet-theorem, poisson-equation]
see_also: [least-squares-conformal-maps, arap-parameterization, discrete-conformal-equivalence, angle-based-flattening, tutte-embedding, discrete-gaussian-curvature, cholesky-decomposition, texture-mapping]
sources:
  - paper: doi:10.1145/3132705
    title: Rohan Sawhney and Keenan Crane, Boundary first flattening, ACM Transactions on Graphics 37(1), Article 5, 2017
    locator: the Cherrier formula and its discrete form, the Dirichlet-to-Neumann and Neumann-to-Dirichlet maps, the closing of the boundary curve, and the extension to the interior
  - book: isbn:9781568814261
    title: Mario Botsch, Leif Kobbelt, Mark Pauly, Pierre Alliez and Bruno Lévy, Polygon Mesh Processing, AK Peters, 2010
    locator: Chapter 5, Parametrization (conformal maps and the discrete Laplacian)
---

Boundary first flattening, BFF, computes a conformal flattening of a triangle mesh with the topology of a disk, and lets the user choose the shape of the boundary. A conformal map keeps angles and changes only the local scale, by a factor $e^{u}$. On a smooth surface, the *Cherrier formula* says how $u$ changes the curvature of the boundary, so the user can give either the scale factors on the boundary or the turning angles of the boundary, and the other one follows from a linear solve. BFF builds the boundary curve first and then fills in the interior with a harmonic map. All the steps are linear, and they use one Laplace matrix, so a new boundary target costs only solves with a factored matrix. It solves the [mesh parameterization](/mesh-parameterization/) problem.

## In plain words

To flatten a curved patch without bending its small angles, each small piece may only grow or shrink. How much each piece grows is one number per point, and these numbers are tied to the curvature of the surface.

BFF uses this tie at the edge of the patch. You say either how much the edge should stretch, or how sharply the flat outline should turn at each edge point, for example to get a rectangle. The method computes the other one, draws the flat outline from the turns and the lengths, and closes it with the smallest change.

The inside is then filled the smoothest way that fits the outline, the way a soap film fills a wire loop.

## The problem

The input is a triangle mesh $M$ with $n$ vertices, with the topology of a disk, whose triangles all have positive area and whose faces are oriented so that the outward normal follows the right-hand rule. The boundary is one loop $b_1, \dots, b_m$, in the order of the face orientation. The input also has one of two targets:

- **Scale factors.** A number $u_b$ for each boundary vertex. The image of a boundary edge $ij$ should have the length $e^{(u_i + u_j)/2}\, \ell_{ij}$. With $u_b = 0$ the boundary keeps its lengths.
- **Turning angles.** An angle $\tilde k_b$ for each boundary vertex, with $\sum_b \tilde k_b = 2\pi$. The image of the boundary should turn left by $\tilde k_b$ at $b$. A polygon with $p$ corners has $\tilde k = 2\pi / p$ at its corners, or any other angles that add up to $2\pi$, and 0 at the other boundary vertices.

The output is a point in the plane for each vertex. The map should be close to conformal and meet the target on the boundary.

## The algorithm

**The smooth relation.** If a metric $g$ is changed to $e^{2u} g$, the Gaussian curvature $K$ and the geodesic curvature $\kappa$ of the boundary change as

$$\tilde K = e^{-2u}(K - \Delta u), \qquad \tilde \kappa = e^{-u}(\kappa + \partial_n u),$$

where $\Delta$ is the Laplace-Beltrami operator and $\partial_n$ is the derivative along the outward normal. The second equation is the Cherrier formula. A flat image needs $\tilde K = 0$, that is $\Delta u = K$ inside. Given $u$ on the boundary, this Poisson problem fixes $u$, and then $\partial_n u$ gives the new boundary curvature. Given the new boundary curvature, the same problem with Neumann data fixes $u$ up to a constant.

**The discrete relation.** Let $\Omega_i = 2\pi - \sum \theta$ be the angle defect at an inner vertex $i$, the [discrete Gaussian curvature](/discrete-gaussian-curvature/), and $k_b = \pi - \sum \theta$ the turning angle at a boundary vertex $b$, where $\sum \theta$ is the sum of the corner angles at the vertex. Let $A$ be the [cotangent Laplacian](/cotangent-laplacian/) with $A_{ij} = -\frac12 (\cot \alpha_{ij} + \cot \beta_{ij})$ for an edge $ij$ and rows that add up to 0. BFF uses

$$\tilde \Omega_I = \Omega_I + (A u)_I, \qquad \tilde k_B = k_B + (A u)_B,$$

and asks for $\tilde \Omega_I = 0$. The subscripts $I$ and $B$ are the inner and boundary vertices.

```pseudo id=main
BFF(M, target)
L1  compute the corner angles, Ω_I, k_B and the cotangent Laplacian A
L2  if the target is the scale factors u_B then
L3      solve A_II u_I = −Ω_I − A_IB u_B                        ▷ Dirichlet problem
L4      k̃_B ← k_B + (A u)_B
L5  else                                                        ▷ the target is k̃_B, with Σ k̃_B = 2π
L6      solve A u = (−Ω_I, k̃_B − k_B), with u = 0 at one vertex  ▷ Neumann problem
L7  l̃_t ← e^{(u_i + u_j)/2} ℓ_ij for each boundary edge t = (b_t, b_{t+1})
L8  φ_t ← k̃_1 + ⋯ + k̃_t;  T_t ← (cos φ_t, sin φ_t)
L9  l*_t ← l̃_t − l̃_t (λ · T_t), with λ such that Σ_t l*_t T_t = 0
L10 γ(b_1) ← 0;  γ(b_{t+1}) ← γ(b_t) + l*_t T_t
L11 solve A_II x_I = −A_IB γ for each of the two coordinates   ▷ harmonic extension
L12 return (γ on the boundary, x inside)
```

Lines L2 to L6 turn one kind of boundary data into the other. Line L3 is a Poisson problem with the curvature as its source, and line L4 reads off the new turning angles. Line L6 is the inverse: the system is singular because $A$ kills the constants, and it is solvable because the right side adds up to 0 (see the correctness section), so one vertex is fixed.

Lines L7 to L10 draw the boundary. The edge $t$ leaves $b_t$ in the direction $T_t$, after the curve has turned by $\tilde k_t$ at $b_t$. The asked lengths $\tilde l$ and the angles $\tilde k$ do not in general give a closed polygon, because the discrete relation is only an approximation of the smooth one. Line L9 changes the lengths by the least amount, in the weighted norm $\sum_t (l^*_t - \tilde l_t)^2 / \tilde l_t$, that closes the polygon. The minimizer has the form of line L9 by a Lagrange multiplier $\lambda \in \mathbb{R}^2$, and $\lambda$ solves the $2 \times 2$ system $\big(\sum_t \tilde l_t T_t T_t^\top\big) \lambda = \sum_t \tilde l_t T_t$. The angles are not changed.

Line L11 extends the boundary curve inside. The two coordinates of a conformal map are harmonic functions, so in the smooth setting the harmonic extension of the boundary values is the conformal map itself. Sawhney and Crane also give a variant that extends one coordinate and takes the other as its harmonic conjugate, which is closer to conformal on coarse meshes.

**Degenerate cases.** Turning angles that do not add up to $2\pi$ have no solution, and the code raises an error. If all the directions $T_t$ are parallel, the $2 \times 2$ system of line L9 is singular. If the asked polygon is far from closed, line L9 can give a length that is 0 or negative, and the output boundary then crosses itself.

## Example

Take the pyramid of the LSCM and ARAP pages: base corners $x_0 = (-1, -1, 0)$, $x_1 = (1, -1, 0)$, $x_2 = (1, 1, 0)$, $x_3 = (-1, 1, 0)$, apex $x_4 = (0, 0, 1)$, side triangles $(0, 1, 4)$, $(1, 2, 4)$, $(2, 3, 4)$, $(3, 0, 4)$. The boundary loop is $0, 1, 2, 3$.

**Target $u_B = 0$, keep the boundary lengths.**

| step | value |
|---|---|
| L1 | apex angles $70.53°$ each, so $\Omega_4 = 77.88° = 1.3593$; base corners have two angles of $54.74°$, so $k_b = 70.53°$; $A_{44} = 2.8284$, $A_{b4} = -0.7071$ |
| L3 | $u_4 = -\Omega_4 / A_{44} = -0.4806$ |
| L4 | $(A u)_b = 0.7071 \cdot 0.4806 = 0.3398 = 19.47°$, so $\tilde k_b = 70.53° + 19.47° = 90°$ at each corner |
| L7 | $\tilde l_t = 2$ for all four edges |
| L9 | the square closes, so $l^* = \tilde l$, no change |
| L10 | $\gamma = (0, 0), (0, 2), (-2, 2), (-2, 0)$ |
| L11 | apex at $(-1, 1)$, the centre |

The image is a square of side 2 with the apex at its centre, so the four side edges have length $\sqrt2 = 1.414$ instead of $\sqrt3 = 1.732$. The apex has the scale factor $e^{-0.48} = 0.62$, so the region near it shrinks, as a conformal map must do near a point of positive curvature. ARAP gives a square of side $2.276$ on the same pyramid instead, because it trades angles for lengths.

**Target turning angles $(120°, 120°, 120°, 0°)$, a triangle.** Line L6 gives $u = (0, 0.2468, 0, -1.7278, -0.8508)$ for the vertices $0$ to $4$. Line L7 asks for the lengths $2.2627, 2.2627, 0.8430, 0.8430$, which do not close. Line L9 changes them to $2.0312, 2.0312, 1.0156, 1.0156$. The output is an equilateral triangle of side $2.0312$ with vertex 3 at the midpoint of the side from vertex 2 to vertex 0, and its turning angles are $120°, 120°, 120°, 0°$ to $10^{-14}$. The large change of the lengths comes from the coarse mesh: four triangles are a poor model of a conformal map.

**Measured on finer meshes.** On 5 random disks of 37 vertices and 18 boundary vertices (a hexagonal grid with jitter, lifted to a random quadratic surface, seeds 0 to 4):

| target | largest relative change of a length at L9 | turning angles met to | flipped triangles |
|---|---|---|---|
| $u_B = 0$ | $4.5 \times 10^{-7}$ to $8.6 \times 10^{-4}$ | (not asked) | 0 |
| rectangle, $\tilde k = 90°$ at 4 vertices | $0.012$ to $0.040$ | $1.2 \times 10^{-15}$ | 0 |

The flips were checked with ORIENT2D, the [orientation test](/orientation-test/), evaluated exactly on the float coordinates converted to rationals. A float evaluation of that sign is not reliable for tiny triangles, because of [catastrophic cancellation](/catastrophic-cancellation/); [exact predicates](/shewchuk-expansion-sum/) avoid it. This is the [robustness problem](/geometric-robustness-problem/) of geometry. The numbers are measurements on these meshes, not bounds.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows the following.

1. For every choice of $u_B$, the angles of line L4 add up to $2\pi$. This uses the [discrete Gauss-Bonnet theorem](/discrete-gauss-bonnet-theorem/), $\sum_I \Omega_i + \sum_B k_b = 2\pi\chi = 2\pi$ for a disk, and the fact that the columns of $A$ add up to 0.
2. $A_{II}$ is positive definite, so lines L3 and L11 have unique solutions. The system of line L6 has a solution exactly when $\sum_B \tilde k_b = 2\pi$, and the solution is unique up to a constant. Lines L3 to L4 and line L6 are inverse maps: from the $\tilde k_B$ of line L4, line L6 gives back $u$ up to a constant.
3. **Key invariant.** The polygon of line L10 is closed, its turning angle at each $b_t$ is $\tilde k_t$ (when all $l^*_t > 0$), and $l^*$ is the unique closest closed choice of lengths to $\tilde l$ in the weighted norm. If the asked polygon closes, $l^* = \tilde l$.
4. If $M$ is planar and $u_B = 0$, the output is congruent to the input.

So the turning angles that were asked for are met exactly, up to rounding, and the lengths that were asked for are met up to the smallest change that closes the boundary. The proof does not show that the interior map has no flipped triangle, or that the output is exactly conformal in any discrete sense.

## Complexity

For $n$ vertices and $m$ boundary vertices, line L1 takes $O(n)$ time. Lines L3, L6 and L11 are solves with $A_{II}$ or with $A$ without one row and column, which do not depend on the target. With dense elimination, as in the code of this page, each takes $O(n^3)$ time and $O(n^2)$ space. With sparse Cholesky factorization and [nested dissection](/nested-dissection/) on the planar mesh graph, the factorization takes $O(n^{3/2})$ time and $O(n \log n)$ space, and each solve $O(n \log n)$ time. Lines L7 to L10 take $O(m)$ time. The matrices are factored once, so a new target costs only back substitutions, $O(n^2)$ dense or $O(n \log n)$ sparse, and $O(m)$ for the boundary.

## Properties

- **Proved.** Exact boundary angles: the output boundary turns by the asked angles, up to rounding.
- **Proved.** The asked lengths are changed only by the smallest weighted change that closes the polygon, and not at all when the asked polygon closes.
- **Proved.** A planar mesh with $u_B = 0$ comes back congruent to itself.
- **Linear.** Every step is a linear solve with a fixed matrix, or a 2 by 2 solve. There is no iteration and no start map.
- **Not guaranteed.** The interior can have flipped triangles, because the cotangent weights can be negative, and the boundary can cross itself when the asked target is far from what the surface allows.
- **Approximately conformal.** The discrete relation is a discretization of the smooth one, and the page proves no bound on the angle distortion of the result.

## Variants and improvements

- **Cone singularities.** The paper puts curvature at a few inner vertices, the cones, and cuts the mesh through them. Then the area distortion of a conformal map can be made much smaller. Choosing the cones is a separate problem.
- **Target shapes.** The paper uses the same two boundary maps to flatten onto a disk and onto a given boundary curve.
- **Harmonic conjugate.** Line L11 can extend only one coordinate and compute the other as its conjugate, which is closer to conformal.
- **Nonlinear discrete conformal maps.** [Discrete conformal equivalence](/discrete-conformal-equivalence/) changes the lengths exactly by $e^{(u_i + u_j)/2}$ and solves a convex nonlinear problem for exact target angles inside and on the boundary. It is slower but its result is exactly a discrete conformal map in its sense.
- **Other conformal maps.** [LSCM](/least-squares-conformal-maps/) also needs one linear solve, but it does not let the user choose the boundary. [ARAP](/arap-parameterization/) trades angles for lengths.

## When to use it

Use it when a conformal map must have a given outline, for example a rectangle for a texture atlas or a polygon that fits a cutting sheet, or when a user changes the boundary target many times and each change must be fast. With $u_B = 0$ it is a good default free-boundary conformal map. It needs a disk; cut a closed or higher-genus surface first along a [cut graph](/cut-graph/). Check the result with an exact orientation test. If injectivity is required, use a method that guarantees it.

## Pitfalls

- **Angles that do not add up to $2\pi$.** A user who asks for a rectangle by setting four angles to $\pi/2$ and forgets to set all other boundary angles to 0 gives line L6 a right side that does not add up to 0. A solver that ignores the singular row then returns a $u$ that meets none of the angles.
- **Wrong sign of the Laplacian.** Some texts use the negative semidefinite Laplacian. Putting that matrix into lines L3 and L6 without changing the signs of the right sides gives $-u$ instead of $u$. With a turning-angle target, line L7 then asks for $e^{-u}$ times the lengths, the regions that should shrink grow, and line L9 must make large changes to close the curve.
- **Exterior angle against interior angle.** $k_b$ is $\pi$ minus the angle sum, the turning of the boundary. Using the angle sum itself at line L4 gives angles whose sum is not $2\pi$, so the directions of line L8 do not wind around once, and no change of the lengths at line L9 gives a simple closed curve.
- **Expecting exact lengths.** The asked lengths are met only if the asked polygon closes. Line L9 changes them, by up to $4\%$ in the rectangle test above and $20\%$ on the coarse pyramid. A target that needs exact lengths must allow the angles to change instead.
- **Clamping cotangents.** Setting negative cotangent weights to 0 at line L1 keeps the rows of $A$ adding up to 0, so the angles still add up to $2\pi$, but line L11 then no longer reproduces linear functions, and a planar mesh does not come back congruent to itself.

## Implementations

## History

Rohan Sawhney and Keenan Crane published boundary first flattening in ACM Transactions on Graphics in 2017. Earlier conformal flattenings either fixed the boundary completely, as in harmonic maps, or left it free, as in LSCM, and the nonlinear methods of discrete conformal geometry could prescribe the boundary angles but needed an iterative solver. BFF uses the Cherrier formula, known from conformal geometry, to turn boundary data of one kind into the other by one linear solve, and so gives boundary control at the cost of a few back substitutions with one factored matrix.

## References
