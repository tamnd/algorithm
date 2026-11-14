---
tag: 1YT62Y
kind: algorithm
slug: angle-based-flattening
name: Angle-based flattening
aliases:
- ABF
- ABF++
area: cad/mesh-processing
level: advanced
summary: Sheffer and de Sturler's parameterization that solves for the planar angles of all triangles closest to the 3D angles under validity constraints, then lays out the mesh.
solves: [mesh-parameterization]
model: real-ram
complexity:
  vars: {n: the number of vertices, k: the number of iterations}
  time: {per_iteration: O(n^3), per_iteration_nested_dissection: O(n^(3/2)), layout: O(n)}
  space: {extra: O(n^2), nested_dissection: O(n log n)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 2001
  people: [Alla Sheffer, Eric de Sturler, Bruno Lévy, Maxim Mogilnitsky, Alexander Bogomyakov]
  note: Sheffer and de Sturler gave ABF in 2001. The 2005 version of Sheffer, Lévy, Mogilnitsky and Bogomyakov made it fast enough for large meshes.
prereqs: [mesh-parameterization, lagrange-multiplier, newton-method-for-systems]
see_also: [least-squares-conformal-maps, tutte-embedding, kkt-conditions, quadratic-programming, mesh-segmentation, texture-mapping, orientation-test, catastrophic-cancellation]
sources:
  - paper: doi:10.1007/PL00013391
    title: Alla Sheffer and Eric de Sturler, Parameterization of faceted surfaces for meshing using angle-based flattening, Engineering with Computers 17(3), 2001, 326 to 337
    locator: the angle objective, the triangle, vertex and wheel constraints, and the proof that angles that meet them define a valid flat mesh
  - paper: doi:10.1145/1061347.1061354
    title: Alla Sheffer, Bruno Lévy, Maxim Mogilnitsky and Alexander Bogomyakov, ABF++, fast and robust angle based flattening, ACM Transactions on Graphics 24(2), 2005, 311 to 330
    locator: the reduction of the Newton system to a smaller one, the reconstruction of positions from angles by least squares, and the hierarchical solution
  - book: isbn:9781568814261
    title: Mario Botsch, Leif Kobbelt, Mark Pauly, Pierre Alliez and Bruno Lévy, Polygon Mesh Processing, AK Peters, 2010
    locator: Chapter 5, Parametrization (angle-based flattening among the conformal methods)
  - paper: doi:10.1561/0600000011
    title: Alla Sheffer, Emil Praun and Kenneth Rose, Mesh parameterization methods and their applications, Foundations and Trends in Computer Graphics and Vision 2(2), 2006, 105 to 171
    locator: the section on angle-based methods
---

Angle-based flattening, ABF, flattens a triangle mesh with the topology of a disk by solving for angles instead of positions. The unknowns are the planar angles of all triangle corners. The method finds the angles that are closest to the angles of the 3D mesh, in a relative least squares sense, among all angle sets that are the angles of some flat mesh. Three kinds of constraints say when that is so: the angles of a triangle add up to $\pi$, the angles around an inner vertex add up to $2\pi$, and a *wheel* condition makes the edge lengths from the law of sines agree around each inner vertex. With these angles the flat mesh is built one triangle at a time. Every triangle of the result is counterclockwise and the map is one to one near every inner vertex, which [least squares conformal maps](/least-squares-conformal-maps/) do not guarantee. The boundary is free. The price is a nonlinear problem, solved by a Newton type iteration with [Lagrange multipliers](/lagrange-multiplier/). It solves the [mesh parameterization](/mesh-parameterization/) problem with low angle distortion.

## In plain words

A flat map of a curved surface must change some angles. ABF decides first what every angle of every small triangle should be in the flat map, and only then draws the triangles.

It wants each flat angle close to the angle on the surface. But it cannot pick them freely. The three angles of a triangle must make a half turn. The angles around a point inside must make a full turn. And the triangles around a point must fit together, so that the sides that meet have the same length.

Among all choices that obey these rules, ABF takes the one with the smallest total change. Then it puts down one triangle, and lays each next triangle along a side that is already drawn.

## The problem

The input is a triangle mesh $M$ with the topology of a disk, with faces oriented so that the outward normal follows the right-hand rule. The output is a point $x_v \in \mathbb{R}^2$ for each vertex such that each triangle is mapped linearly, every triangle is counterclockwise, and the angles of the flat triangles are close to the angles of the 3D triangles.

## The algorithm

Let $\beta_c$ be the 3D angle of the corner $c$. At an inner vertex, scale the $\beta_c$ of its corners so that they add up to $2\pi$; these are the target angles. The unknowns are the planar angles $\alpha_c$, and the objective is

$$F(\alpha) = \sum_c \frac{(\alpha_c - \beta_c)^2}{\beta_c^2}.$$

For a corner at $v$ in a triangle $T$, let $\mathrm{nx}$ and $\mathrm{pv}$ be the corners of $T$ after and before $v$. The constraints are

- triangle: $\alpha_{T,1} + \alpha_{T,2} + \alpha_{T,3} = \pi$ for each triangle,
- vertex: $\sum_{T \ni v} \alpha_{T,v} = 2\pi$ for each inner vertex,
- wheel: $\sum_{T \ni v} \log \sin \alpha_{T,\mathrm{nx}} - \sum_{T \ni v} \log \sin \alpha_{T,\mathrm{pv}} = 0$ for each inner vertex.

With $C(\alpha) = 0$ for all constraints and its Jacobian $J$, the [KKT conditions](/kkt-conditions/) are $\nabla F + J^\top \lambda = 0$ and $C = 0$. Each iteration solves the linearized system, a [quadratic programming](/quadratic-programming/) step with equality constraints. The code of this page takes $H = \mathrm{diag}(2 / \beta_c^2)$, the Hessian of $F$, and drops the second derivatives of the wheel constraint. Then $H$ is diagonal, and eliminating $\delta$ leaves a system in $\lambda$ alone, $J H^{-1} J^\top \lambda = C - J H^{-1} \nabla F$.

```pseudo id=main
ABF(M)
L1  β ← the 3D corner angles, scaled to 2π at each inner vertex
L2  α ← β
L3  repeat
L4      evaluate the constraints C(α), the gradient ∇F and the Jacobian J
L5      solve (J H⁻¹ Jᵀ) λ = C − J H⁻¹ ∇F
L6      δ ← −H⁻¹ (∇F + Jᵀ λ);  α ← α + δ
L7  until |C(α)| ≤ ε and |δ| ≤ ε
LAYOUT(M, α)
L8  place the first triangle: its first edge with its 3D length on the x axis, the third corner by α
L9  in breadth-first order, place each next triangle across an edge already placed, by the law of sines
L10 return x
```

In L9, the third corner $c$ of the triangle $(a, b, c)$ is at $x_a + \frac{\sin \alpha_b}{\sin \alpha_c} R(\alpha_a)(x_b - x_a)$, where $R(\theta)$ is the rotation by $\theta$.

**Degenerate cases.** A 3D triangle with an angle of 0 or $\pi$ gives a target of 0 or a wheel term $\log 0$, so it is rejected. The iteration does not keep $\alpha_c$ in $(0, \pi)$ by itself; Sheffer and de Sturler add the bounds $\alpha_c > 0$, and the code of this page checks them at the end and raises an error. A mesh with no inner vertex has only triangle constraints, and the result is the target angles corrected to sum $\pi$ per triangle; the layout is then free of gaps by construction. A mesh with a hole or a handle must be cut into a disk first.

## Example

Take the pyramid with base corners $(-1, -1, 0)$, $(1, -1, 0)$, $(1, 1, 0)$, $(-1, 1, 0)$ (vertices 0 to 3), apex $(0, 0, 1)$ (vertex 4), and the four side triangles $(0, 1, 4)$, $(1, 2, 4)$, $(2, 3, 4)$, $(3, 0, 4)$. The apex is the only inner vertex.

| step | value |
|---|---|
| L1, 3D angles | $\arctan \sqrt2 \approx 54.74°$ at each base corner, $\arccos(1/3) \approx 70.53°$ at the apex |
| L1, scaling | the apex angles add up to $282.1°$, so they are scaled to $90°$ each |
| L4, first pass | each triangle sum is $199.47°$, so $C = 0.3398$ for each triangle constraint; the vertex and wheel constraints are 0 |
| L5 to L6 | the base angles go to $45°$, the apex angles stay at $90°$ |
| L7 | the second pass finds $C = 0$ and $\delta = 0$ and stops |
| objective | $F = 8 \big((\pi/4 - \arctan\sqrt2) / \arctan\sqrt2\big)^2 \approx 0.2531$ |
| L8 to L10 | $x_0 = (0, 0)$, $x_1 = (2, 0)$, $x_4 = (1, 1)$, $x_2 = (2, 2)$, $x_3 = (0, 2)$ |

The result is a square of side 2 split by its diagonals into four right isosceles triangles. The angle at the apex had to grow, and ABF spread the change equally over the base angles.

**When the arithmetic is floating point.** The angles come from an iteration with square roots, sines and logarithms, so the constraints hold only to rounding, about $10^{-15}$ in the tests. The triangles then do not close exactly, and the position of a vertex depends slightly on the triangle that places it. The code measures this gap, below $10^{-14}$ on bumps with up to 72 triangles. The terms $\log \sin \alpha$ and their derivatives $\cot \alpha$ grow without bound when an angle comes near 0 or $\pi$, and $\sin \alpha$ for $\alpha$ near $\pi$ loses relative accuracy by [catastrophic cancellation](/catastrophic-cancellation/), because the float $\alpha$ is subtracted from a rounded $\pi$. Whether a triangle of the layout is flipped is the sign of ORIENT2D, the [orientation test](/orientation-test/), on the computed points; the tests evaluate it exactly on the floats converted to rationals, and [exact predicates](/shewchuk-expansion-sum/) do the same faster. This is the [robustness problem](/geometric-robustness-problem/) of geometry.

## Correctness

If the angles meet the three constraints exactly and lie in $(0, \pi)$, each triangle is fixed up to a similarity by its angles. The law of sines gives the ratio of two edges at an inner vertex in each triangle, and the wheel constraint says that the product of these ratios around the vertex is 1, so the edge lengths agree. The vertex constraint says that the turns around the vertex add up to a full turn, so the triangles close. The disk minus its inner vertices has loops around the inner vertices as generators of its fundamental group, so the layout is the same along any path. Each triangle is placed with a positive turn, so it is counterclockwise, and the triangles around an inner vertex cover a full turn once. A planar mesh meets the constraints with its own angles and objective 0, so it is mapped to a similar copy. The convergence of the iteration is not proved, only measured. The full proof is below.

## Complexity

There are $3F \approx 6n$ unknowns and $F + 2 n_i$ constraints, where $n_i$ is the number of inner vertices. One iteration builds $J$ in $O(n)$ time. The system in $\lambda$ has size $F + 2 n_i \approx 4n$; dense elimination, as in the code of this page, takes $O(n^3)$ time and $O(n^2)$ space. Its sparsity follows the mesh, so a sparse factorization with [nested dissection](/nested-dissection/) takes $O(n^{3/2})$ time. The 2005 version eliminates the triangle constraints as well and solves a system of size $2 n_i$ only. The number of iterations $k$ is small in practice: 7 to 9 on the bumps of the tests, 2 on the pyramid. The layout is one pass over the triangles, $O(n)$.

## Properties

- **Locally injective.** With exact angles in $(0, \pi)$, no triangle is flipped and every inner vertex has a one to one star. Boundary vertices are not constrained, so the boundary can overlap itself.
- **Free boundary.** No vertex is pinned; the scale comes from the first edge.
- **Reproduction.** A planar mesh is mapped to a similar copy, with $F = 0$.
- **Angle based.** The objective measures relative angle error. Areas are not controlled, as for any conformal method.
- **Nonlinear.** An iteration, not one solve. Each step is a sparse linear system.

## Variants and improvements

- **The fast version of Sheffer, Lévy, Mogilnitsky and Bogomyakov (2005).** Their paper calls it ABF++. Its changes make ABF practical for much larger meshes than the first solver could handle. The Newton system is reduced by eliminating the angle unknowns and the triangle constraints, which leaves a much smaller sparse system. The positions are reconstructed from the angles by a least squares solve in the style of LSCM instead of the greedy layout, which spreads the small errors of the angles evenly. A hierarchical solver handles very large meshes.
- **Linear ABF (Zayer, Lévy and Seidel 2007).** Linearizes the wheel constraint about the target angles and solves one linear system, with results close to ABF.
- **Bounds on the angles.** The original method adds $\alpha_c \ge \varepsilon$; in practice the bound is rarely active and is often dropped.
- **Boundary constraints.** Adding the constraint that a boundary vertex has angle sum $\pi$ maps the mesh onto a region with a straight boundary there, which is used for charts with prescribed boundary shape.

## When to use it

Use it for texture atlases and remeshing when angles matter and the charts are strongly curved, where [LSCM](/least-squares-conformal-maps/) gives large angle errors or folds. On the saddle-shaped wheel with six triangles of the LSCM page, where LSCM folds two triangles, ABF gives six equilateral triangles. Use the 2005 fast version for large meshes. If a map with no overlap at all is required, check the boundary or use a [Tutte embedding](/tutte-embedding/) as a start for a method with barriers. For a quick map of a nearly flat chart, LSCM is cheaper.

## Pitfalls

- **Dropping the wheel constraint.** Without it, the triangle and vertex constraints are linear and easy, but the triangles around a vertex do not close. On the bumps of the tests the layout then has gaps from $0.05$ to $0.49$, for edges of length about 1.
- **The greedy layout.** Laying out one triangle at a time adds up the rounding errors along long paths. The 2005 fast version uses a least squares reconstruction for this reason.
- **Angles near 0 or $\pi$.** The wheel terms and their derivatives blow up. Remesh slivers first.
- **Global overlap.** Local injectivity does not exclude two far parts of the boundary landing on each other. Test it, for example with the [Bentley-Ottmann algorithm](/bentley-ottmann-algorithm/) on the boundary edges.
- **Not converging.** The iteration is not guaranteed to converge from the target angles. Check the constraint residual and the angle bounds before the layout.

## Implementations

## History

Alla Sheffer and Eric de Sturler introduced angle-based flattening in 2001 for meshing faceted surfaces in engineering, with the observation that a set of angles defines a valid flat mesh exactly when it satisfies the triangle, vertex and wheel conditions. The first solver was slow. In 2005 Sheffer, Bruno Lévy, Maxim Mogilnitsky and Alexander Bogomyakov published a fast version, which reduced the linear algebra, reconstructed the positions robustly and made the method one of the standard unwrapping methods. Zayer, Lévy and Seidel gave a linearized version in 2007.

## References
