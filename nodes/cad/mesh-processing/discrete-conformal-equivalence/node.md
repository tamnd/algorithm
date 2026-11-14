---
tag: VG00WC
kind: algorithm
slug: discrete-conformal-equivalence
name: Discrete conformal maps by conformal equivalence
aliases:
- discrete Yamabe flow
- Springborn-Schroder-Pinkall conformal maps
area: cad/mesh-processing
level: research
summary: Springborn, Schroder and Pinkall's maps that scale edge lengths by vertex factors found by minimising a convex energy, to reach target angle sums.
solves: [mesh-parameterization]
model: real-ram
complexity:
  vars: {n: the number of vertices, k: the number of Newton steps}
  time: {worst: O(k n^3), nested_dissection: O(k n^(3/2))}
  space: {extra: O(n^2), nested_dissection: O(n log n)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 2008
  people: [Boris Springborn, Peter Schröder, Ulrich Pinkall]
  note: Springborn, Schröder and Pinkall gave the convex energy for discrete conformal equivalence in ACM Transactions on Graphics in 2008, and solved it by Newton's method.
prereqs: [mesh-parameterization, cotangent-laplacian, discrete-gaussian-curvature, convex-function, newton-method-for-systems]
see_also: [boundary-first-flattening, least-squares-conformal-maps, arap-parameterization, discrete-gauss-bonnet-theorem, backtracking-line-search, edge-flip, delaunay-triangulation, cut-graph]
sources:
  - paper: doi:10.1145/1360612.1360676
    title: Boris Springborn, Peter Schröder and Ulrich Pinkall, Conformal equivalence of triangle meshes, ACM Transactions on Graphics 27(3), Article 77, 2008
    locator: the definition of discrete conformal equivalence, the energy with the Lobachevsky function, its gradient and Hessian, and the Newton solver
  - paper: doi:10.2140/gt.2015.19.2155
    title: Alexander I. Bobenko, Ulrich Pinkall and Boris A. Springborn, Discrete conformal maps and ideal hyperbolic polyhedra, Geometry and Topology 19(4), 2155-2215, 2015
    locator: the variational principle, and the extension of the energy to a convex function on all of the space of scale factors
  - paper: doi:10.4310/jdg/1527040872
    title: Xianfeng David Gu, Feng Luo, Jian Sun and Tianqi Wu, A discrete uniformization theorem for polyhedral surfaces, Journal of Differential Geometry 109(2), 223-256, 2018
    locator: the changed definition with Delaunay edge flips, and existence and uniqueness of a metric with given curvature
---

Two edge-length metrics on the same triangle mesh are *discretely conformally equivalent* if each vertex $i$ has a number $u_i$, its logarithmic scale factor, such that every edge length is multiplied by $e^{(u_i + u_j)/2}$. Springborn, Schröder and Pinkall showed that the scale factors that give prescribed angle sums at the vertices are the minimizer of a convex energy, whose gradient is the angle error and whose Hessian is the [cotangent Laplacian](/cotangent-laplacian/) of the new metric. Newton's method then finds them in a few steps. With target angle sums $2\pi$ at the inner vertices the new metric is flat, and laying out its triangles gives a [mesh parameterization](/mesh-parameterization/) that is conformal in this discrete sense.

## In plain words

A conformal flattening may only grow or shrink each small region, never shear it. On a triangle mesh this becomes a rule: give each corner point a growth number, and scale each edge by the average growth of its two ends.

The task is to pick the growth numbers so that the corners around each inner point add up to a full turn, because then the triangles fit flat in the plane.

There is a hill-shaped quantity whose lowest point is exactly such a choice, and a hill of this shape has only one lowest point. So a standard downhill method with good steps finds it in a few rounds, and it cannot be caught in a wrong hollow. If the lowest point needs a triangle that is squashed flat, there is no answer for this mesh.

## The problem

The input is a connected triangle mesh $M$ with $n$ vertices, edge lengths $\ell_{ij}$ that satisfy the strict triangle inequality in every triangle, a set $F$ of free vertices with a target angle sum $\Theta_i > 0$ for each $i \in F$, and the value $u_i = 0$ at the other vertices, which must be at least one vertex. The faces are oriented so that the outward normal follows the right-hand rule.

The output is $u \in \mathbb{R}^n$ such that the new lengths $\tilde\ell_{ij} = e^{(u_i + u_j)/2} \ell_{ij}$ satisfy the triangle inequalities and the sum of the corner angles at each $i \in F$ is $\Theta_i$. The usual targets are:

- **Flattening a disk.** $\Theta_i = 2\pi$ at the inner vertices and $u_b = 0$ on the boundary, so that the boundary keeps its lengths. Or $\Theta_b = \pi - \tilde k_b$ at the boundary vertices too, for turning angles $\tilde k_b$ of the outline that add up to $2\pi$, with one vertex fixed.
- **Closed surfaces.** Targets at all vertices but one, which add up, with the angle sum of the fixed vertex, to $2\pi(V - \chi)$, where $\chi = V - E + F = 2 - 2g$ is the Euler characteristic. This is the [discrete Gauss-Bonnet theorem](/discrete-gauss-bonnet-theorem/).

**Length cross ratios.** An inner edge $ij$ with the triangles $ijk$ and $jil$ has the length cross ratio $\ell_{il}\ell_{jk} / (\ell_{lj}\ell_{ki})$. A change of the lengths by vertex factors keeps it, because each of $i, j, k, l$ is an end of one edge in the numerator and one in the denominator, so the factors cancel. Springborn, Schröder and Pinkall show the converse: two metrics with the same length cross ratios on all inner edges are conformally equivalent. The length cross ratio is the absolute value of the complex cross ratio of the four points, which Möbius transformations keep.

The corner angles come from the lengths by the law of cosines, so the problem is about lengths only. The vertex positions are not needed, and a flat result is laid out afterwards.

## The algorithm

For a triangle with new lengths $\tilde\ell$, let $x = \log\tilde\ell$ for each side and $\alpha$ the corner angle opposite it. Let $\Lambda(\alpha) = -\int_0^\alpha \log\lvert 2\sin t \rvert \, dt$ be Milnor's Lobachevsky function. The energy is

$$E(u) = \sum_{t} \Big( 2 f_t(u) - \pi (u_i + u_j + u_k) \Big) + \sum_{i \in F} \Theta_i u_i, \qquad f_t = \sum_{\text{corners of } t} \big( \alpha\, x_{\text{opposite}} + \Lambda(\alpha) \big),$$

where $i, j, k$ are the corners of the triangle $t$. Its gradient is $\partial E / \partial u_i = \Theta_i - \sum \alpha$, the target minus the angle sum at $i$, and its Hessian is the cotangent Laplacian $H_{ij} = -\frac12(\cot\alpha_{ij} + \cot\beta_{ij})$, $H_{ii} = -\sum_{j \ne i} H_{ij}$, of the new lengths. A triangle whose new lengths break the triangle inequality is given the angles $\pi$, 0, 0, with $\pi$ opposite the longest side. This extends $E$ to a convex function on all of $\mathbb{R}^n$ with a continuous gradient.

```pseudo id=main
DiscreteConformal(M, ℓ, Θ, F, ε)
L1  u ← 0
L2  repeat at most K times
L3      ℓ̃_ij ← e^{(u_i + u_j)/2} ℓ_ij;  angles of each triangle from ℓ̃, or (π, 0, 0) if it is degenerate
L4      g_i ← Θ_i − (sum of the angles at i), for i ∈ F       ▷ the gradient of E
L5      if max_i |g_i| < ε then
L6          if some triangle is degenerate then fail          ▷ no solution with this triangulation
L7          return u
L8      H ← the cotangent Laplacian of ℓ̃, rows and columns in F   ▷ the Hessian of E
L9      solve H d = −g;  if H is singular then d ← −g
L10     t ← 1;  while E(u + t d) > E(u) + c t (g · d) do t ← t/2   ▷ backtracking, c = 10^{-4}
L11     u_F ← u_F + t d
L12 fail                                                      ▷ no convergence in K steps
```

Line L3 is the only place where the lengths enter. Line L8 skips degenerate triangles: their angles are constant, so they add nothing to the Hessian. Line L9 is a Newton step for minimizing $E$, the [Newton method](/newton-method-for-systems/) applied to the gradient equation $g = 0$. Line L10 is a [backtracking line search](/backtracking-line-search/): it halves the step until $E$ drops by a fixed fraction of the drop that the slope predicts, so the energy decreases at every step. Near the minimum the full step is taken, and Newton's method then converges quadratically. The code of this page takes the full step without the test when the predicted drop is below the rounding level of $E$, because the energy values can no longer tell the steps apart there.

**Layout.** For a disk with flat targets, place one triangle in the plane with its new lengths, then place each neighbour across a shared edge, in the order of a traversal of the triangles. The angle sums $2\pi$ at the inner vertices make the triangles around each inner vertex close up, so on a disk the result does not depend on the order. A closed surface or a surface of higher genus is first cut to a disk along a [cut graph](/cut-graph/), and the targets at the cut vertices are set so that the copies match.

## Example

Take the pyramid of the BFF page: base corners $(\pm1, \pm1, 0)$ numbered $0$ to $3$ counterclockwise from $(-1, -1, 0)$, apex $4$ at $(0, 0, 1)$, side triangles $(0, 1, 4)$, $(1, 2, 4)$, $(2, 3, 4)$, $(3, 0, 4)$. The base edges have length 2, the side edges $\sqrt3$. The only free vertex is the apex, with $\Theta_4 = 2\pi$, and $u = 0$ on the boundary. The apex angles are $70.53°$ each, so the angle sum is $282.1°$ and the apex has the defect $77.88° = 1.3593$.

| step | $u_4$ | $g_4 = 2\pi - \text{angle sum}$ | $H_{44}$ | $E(u)$ |
|---|---|---|---|---|
| 0 | $0$ | $1.3593$ | $2.8284$ | $23.232303$ |
| 1 | $-0.4806020$ | $-0.3124$ | $4.3253$ | $22.952439$ |
| 2 | $-0.4083658$ | $-1.16 \times 10^{-2}$ | $4.0116$ | $22.940871$ |
| 3 | $-0.4054693$ | $-1.68 \times 10^{-5}$ | $4.0000$ | $22.940854$ |
| 4 | $-0.4054651$ | $-3.5 \times 10^{-11}$ | $4.0000$ | $22.940854$ |
| 5 | $-0.4054651$ | $9 \times 10^{-16}$ | $4.0000$ | $22.940854$ |

Each line search takes the full step, and the code returns after step 5. The limit is $u_4 = \log(2/3) = -0.4054651$: the side edges become $e^{u_4/2}\sqrt3 = \sqrt2$, the apex angles become $90°$, and the layout is a square of side 2 with the apex at its centre. The angle error is roughly squared at each step from step 1 on. The first step is the linear solve of [boundary first flattening](/boundary-first-flattening/), whose $u_4 = -0.4806$ is the linearization of this problem; Newton's method continues to the exact discrete answer.

**A target with no solution.** If $\Theta_4 \ge 4\pi$, the side triangles must have apex angles of $\pi$, which only degenerate triangles have, when $e^{u_4/2}\sqrt3 \le 1$. For $\Theta_4 = 4\pi$ the code stops at line L6, and for $\Theta_4 = 4.5\pi$ the energy decreases without bound and it stops at line L12. For $\Theta_4 = 3.9\pi$ the first Newton step lands in the degenerate region, line L9 takes gradient steps out of it, and the code returns $u_4 = -1.0971$ with all triangles valid.

**Measured on finer meshes.** On 5 random disks of 37 vertices, 54 triangles and 18 boundary vertices (a hexagonal grid with jitter, lifted to a random quadratic surface, seeds 0 to 4), with $\varepsilon = 10^{-12}$:

| target | Newton steps | largest angle error | flipped triangles in the layout | range of $u$ |
|---|---|---|---|---|
| $2\pi$ inside, $u = 0$ on the boundary | 3 to 4 | $9.5 \times 10^{-14}$ | 0 | $-0.22$ to $0.47$ |
| rectangle: $\pi/2$ at 4 boundary vertices, $\pi$ at the others | 5 to 11 | $5.3 \times 10^{-14}$ | 0 | $-2.14$ to $2.16$ |

The flips were checked with ORIENT2D, the [orientation test](/orientation-test/), evaluated exactly on the float coordinates converted to rationals. A float evaluation of that sign is not reliable for tiny triangles, because of [catastrophic cancellation](/catastrophic-cancellation/); [exact predicates](/shewchuk-expansion-sum/) avoid it. This is the [robustness problem](/geometric-robustness-problem/) of geometry. The large range of $u$ for the rectangle shows the area distortion near its corners. These numbers are measurements on these meshes, not bounds.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows the following.

1. For a triangle, $\partial f_t / \partial x = \alpha$, the angle opposite that side. This follows from the law of sines and the angle sum $\pi$. Then $\partial E / \partial u_i = \Theta_i - \sum \alpha$ at $i$.
2. The Hessian of $E$ is the cotangent Laplacian of the new lengths, which is positive semidefinite with the constants as its kernel. With at least one vertex fixed, it is positive definite on the free vertices.
3. With the angles $(\pi, 0, 0)$ for degenerate triangles, $E$ is a [convex function](/convex-function/) on all of $\mathbb{R}^n$ with a continuous gradient.
4. **Key invariant.** $u$ gives the target angle sums with valid triangles if and only if $u$ minimizes $E$ and all its triangles are valid, and such a $u$ is unique.
5. Every $u$ that the code returns has all triangles valid and angle errors below $\varepsilon$, and the code stops after at most $K$ steps.

So when the code returns, the result is correct up to $\varepsilon$, and it is the only answer. What can fail is existence. The proof does not show that Newton's method reaches the minimum from every start, and with a fixed triangulation the minimum may have degenerate triangles, or $E$ may have no minimum at all, as in the pyramid with $\Theta_4 \ge 4\pi$. Gu, Luo, Sun and Wu changed the definition so that the triangulation changes by [Delaunay](/delaunay-triangulation/) [edge flips](/edge-flip/) as $u$ changes, and proved that then a metric with the given curvature exists and is unique up to scale, for every target that satisfies the Gauss-Bonnet condition. That result is cited here, not proved.

## Complexity

For $n$ vertices, lines L3, L4 and L8 take $O(n)$ time, and each evaluation of $E$ in line L10 also takes $O(n)$. Line L9 is a solve with a sparse symmetric positive definite matrix. Dense elimination, as in the code of this page, takes $O(n^3)$ time and $O(n^2)$ space per step. Sparse [Cholesky factorization](/cholesky-decomposition/) with [nested dissection](/nested-dissection/) on the planar mesh graph takes $O(n^{3/2})$ time and $O(n \log n)$ space per step. The matrix changes with $u$, so each step factors it again. For $k$ Newton steps the total is $O(k n^3)$ dense or $O(k n^{3/2})$ sparse, plus the line searches. The number of steps is not bounded by the proof; on the meshes above it was 3 to 11.

## Properties

- **Proved.** The energy is convex, with the angle error as its gradient and the cotangent Laplacian as its Hessian.
- **Proved.** A solution with valid triangles is unique and is the minimizer of $E$, and a returned $u$ has angle errors below $\varepsilon$.
- **Proved.** The energy does not increase in a step that passes the test of line L10.
- **Exact discrete conformality.** The result is exactly conformally equivalent to the input in the discrete sense, not an approximation of it, and the angle sums are met up to $\varepsilon$.
- **Measured.** 3 to 11 Newton steps and no flipped triangles on the 10 runs above.
- **Not guaranteed.** With a fixed triangulation, a solution may not exist. Without edge flips the code then fails at line L6 or line L12.

## Variants and improvements

- **Delaunay flips.** Gu, Luo, Sun and Wu let the triangulation follow $u$, flipping an edge when it stops being Delaunay in the current metric. With this change, existence holds for every target that satisfies Gauss-Bonnet. The flipped edges are intrinsic: they are straight in the current metric, not in the input surface.
- **Curvature flow.** Luo proposed in 2004 to move $u$ by a flow that, written with these targets, is $\dot u_i = \sum\alpha - \Theta_i$, a gradient descent on the same energy. Newton's method on $E$ reaches the same point in far fewer steps.
- **Hyperbolic and spherical targets.** The same notion with hyperbolic or spherical triangles gives uniformization of surfaces of genus at least 2, or of the sphere. Bobenko, Pinkall and Springborn related the energy to volumes of ideal hyperbolic polyhedra.
- **Cone singularities.** Targets other than $2\pi$ at a few inner vertices, the cones, take up the curvature and reduce the area distortion. The layout then needs cuts through the cones.
- **Linear methods.** [Boundary first flattening](/boundary-first-flattening/) solves a linearized form of the same problem in one step. [LSCM](/least-squares-conformal-maps/) gives another linear conformal map with a free boundary.

## When to use it

Use it when the angle sums at the vertices must be met exactly, for example a flat metric with chosen cone angles for seamless texture maps, or a polygon outline with exact corner angles. It is a good choice for meshes of good quality, where the minimum has valid triangles and Newton's method needs few steps. For meshes with very bad triangles or extreme targets, use the version with Delaunay flips. If a fast approximate map is enough, BFF or LSCM needs one linear solve instead of several.

## Pitfalls

- **A line search near the minimum.** Near the minimum, the drop of $E$ in a Newton step is about the square of the angle error, and it soon falls below the rounding error of $E$ itself. The test of line L10 then compares rounding noise and can reject every step, so the method stalls at an angle error far above $\varepsilon$. A first version of the code of this page did this on the disks above with $\varepsilon = 10^{-12}$, although pure Newton steps reached $2 \times 10^{-15}$. Take the full Newton step when the predicted drop is below the rounding level of $E$.
- **No fixed vertex.** On a closed mesh, $E$ is unchanged when the same constant is added to all $u_i$, if the targets satisfy Gauss-Bonnet, and the Hessian is singular. Fix one vertex. If the targets do not satisfy Gauss-Bonnet, $E$ decreases without bound along the constants and there is no solution.
- **Wrong Lobachevsky function.** Integrating $\log\lvert 2\sin t\rvert$ with a plain quadrature rule loses accuracy at the singularity at 0. Use a series, for example $\Lambda(x) = x - x\log(2x) + \sum_{n \ge 1} \frac{\zeta(2n)}{n(2n+1)} \frac{x^{2n+1}}{\pi^{2n}}$ on $(0, \pi/2]$, and the symmetries $\Lambda(-x) = -\Lambda(x)$ and $\Lambda(x + \pi) = \Lambda(x)$.
- **Cotangents of degenerate triangles.** A degenerate triangle has a zero angle, whose cotangent is infinite. Skip it in the Hessian, and give it the angles $(\pi, 0, 0)$ in the gradient, or the function is not convex and Newton's method can jump to nonsense.
- **Laying out a surface that is not a disk.** The layout across shared edges needs a disk. On a cylinder or a surface with handles, the triangles met along two different paths need not agree, even with angle sums $2\pi$, because going around a loop can rotate and scale the layout.

## Implementations

## History

The notion that two metrics on a triangulation are conformally equivalent when the edge lengths change by vertex factors is older than the algorithm. Feng Luo studied it in 2004 together with a curvature flow on the scale factors. Boris Springborn, Peter Schröder and Ulrich Pinkall gave the convex energy with the Lobachevsky function in ACM Transactions on Graphics in 2008, solved it by Newton's method, and used it for conformal maps with cone singularities. Bobenko, Pinkall and Springborn related it in 2015 to ideal hyperbolic polyhedra and extended the energy to all scale factors. Gu, Luo, Sun and Wu proved a discrete uniformization theorem in 2018, with Delaunay flips as part of the definition, which settled the existence question.

## References
