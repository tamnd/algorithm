---
tag: 2QKV5N
kind: algorithm
slug: green-coordinates
name: Green coordinates
aliases:
- Green cage coordinates
area: graphics-and-signals/keyframing-and-deformation
level: advanced
summary: Cage coordinates from Green's third identity that use both the cage vertices and face normals, giving conformal deformations in 2D.
solves: [shape-deformation]
model: real-ram
complexity:
  vars: {n: "the number of cage vertices and edges", N: "the number of points to deform"}
  time: {per_point: "Θ(n)", all: "Θ(N n)"}
  space: {extra: "Θ(n)"}
properties: {deterministic: true, exact: true, online: true, recursive: false}
prereqs: [cage-based-deformation]
see_also: [cage-based-deformation, harmonic-coordinates, generalized-barycentric-coordinates, floater-mean-value-coordinates, shape-deformation, least-squares-conformal-maps, poisson-equation, as-rigid-as-possible-shape-manipulation]
sources:
  - paper: doi:10.1145/1360612.1360677
    title: "Yaron Lipman, David Levin and Daniel Cohen-Or, Green coordinates, SIGGRAPH 2008, ACM Transactions on Graphics 27(3), 2008"
    locator: the whole paper (the coordinates from Green's third identity, the scaled normals of the deformed cage, and the conformal and quasi-conformal behaviour in 2D and 3D)
---

Green coordinates are cage coordinates with two kinds of weights: one weight $\phi_i$ per cage vertex and one weight $\psi_j$ per cage edge, or per face in 3D.
A point $\eta$ inside the cage moves to $\sum_i \phi_i(\eta)v'_i + \sum_j \psi_j(\eta)s_jn'_j$, where $v'_i$ are the moved vertices, $n'_j$ the moved edge normals, and $s_j$ the factor by which edge $j$ grew.
The weights come from Green's third identity applied to the coordinate functions, and they have closed forms.
Yaron Lipman, David Levin and Daniel Cohen-Or (2008) introduced them.
The normal terms make the difference: in 2D the deformation is a conformal map, so small shapes inside the cage keep their angles, where other cage coordinates shear them.

## In plain words

Other cage methods move a point by a weighted mix of the cage corners.
Green coordinates also listen to the sides of the cage: how each side turns, and how much it stretches.
If a side turns, the points near it turn with it, and if it gets longer, the shape near it grows in both directions, not only along the side.
That is why a small circle drawn inside the shape stays a small circle, only moved, turned and resized, even when the cage bends.
The price is that the shape no longer touches the cage exactly: the moved cage is a guide, not a hard wall.

## The problem

The input is a cage, a simple polygon $v_0, \dots, v_{n-1}$ in counterclockwise order, with edge $j$ from $v_j$ to $v_{j+1}$ and its outward unit normal $n_j$, and a point $\eta$ inside it.
The output is the $2n$ weights $\phi_i(\eta)$ and $\psi_j(\eta)$ such that

$$\eta = \sum_i \phi_i(\eta)v_i + \sum_j \psi_j(\eta)n_j \quad\text{and}\quad \sum_i \phi_i(\eta) = 1,$$

and the deformed point for a moved cage $v'$.
With $G(\xi, \eta) = \frac{1}{2\pi}\ln|\xi - \eta|$ and the hat function $\Gamma_i$ of vertex $i$ on the boundary, the weights are

$$\phi_i(\eta) = \int_{\partial\Omega} \Gamma_i(\xi)\,\frac{\partial G}{\partial n}(\xi, \eta)\,ds(\xi), \qquad \psi_j(\eta) = -\int_{e_j} G(\xi, \eta)\,ds(\xi).$$

## The algorithm

On edge $j$ with $a = v_j$ and $b = v_{j+1}$, let $q(t) = |a + t(b - a) - \eta|^2 = Qt^2 + Rt + S$. The integrals $I_0 = \int_0^1 dt/q$, $I_1 = \int_0^1 t\,dt/q$ and $\Lambda = \int_0^1 \ln q\,dt$ have closed forms with one arctangent and two logarithms.

```pseudo id=main
GREEN(η, v)
L1  φ ← 0, ψ ← 0
L2  for each edge j from a = v_j to b = v_{j+1} do
L3      n_j ← the outward unit normal of edge j
L4      h ← (a - η) · n_j
L5      compute I_0, I_1 and Λ for edge j
L6      φ_j ← φ_j + (h|b - a|/2π)(I_0 - I_1); φ_{j+1} ← φ_{j+1} + (h|b - a|/2π) I_1
L7      ψ_j ← -(|b - a|/4π) Λ
L8  return φ, ψ
DEFORM(η, v, v')
L9  return Σ_i φ_i v'_i + Σ_j ψ_j s_j n'_j, with s_j = |v'_{j+1} - v'_j| / |v_{j+1} - v_j|
```

Line L4 uses that $(\xi - \eta) \cdot n_j = h$ is the same for every $\xi$ on edge $j$, so $\partial G/\partial n = h/(2\pi q)$ there.
Line L6 splits the integral of line L4 between the two ends of the edge with the hat functions $1 - t$ and $t$.
Line L7 uses $\ln|\xi - \eta| = \frac12\ln q$.
With $D = \sqrt{4QS - R^2} = 2|(b - a) \times (a - \eta)|$ and $A = (\arctan\frac{2Q + R}{D} - \arctan\frac{R}{D})/D$: $I_0 = 2A$, $I_1 = \frac{1}{2Q}\ln\frac{Q + R + S}{S} - \frac{R}{Q}A$, and $\Lambda = \ln(Q + R + S) + \frac{R}{2Q}\ln\frac{Q + R + S}{S} - 2 + (4S - \frac{R^2}{Q})A$. If $\eta$ is on the line of the edge, $h = 0$ and only $\Lambda$ is needed, without the term in $A$.

## Example

For the unit square and its center $\eta = (1/2, 1/2)$, symmetry gives $\phi_i = 1/4$ for every vertex, and every edge has $\psi_j = -\frac{1}{4\pi}\int_0^1 \ln((t - \frac12)^2 + \frac14)\,dt \approx 0.0893138$.
The four normals sum to 0, so $\sum\phi_iv_i + \sum\psi_jn_j = (1/2, 1/2)$, as it must.
Now shear the cage by $(x, y) \mapsto (x + y/2, y)$.
The center goes to $(0.75, 0.5)$, which is the sheared center.
But the point $(0.25, 0.3)$ goes to about $(0.44685, 0.36097)$, not to the sheared point $(0.4, 0.3)$: a shear is not conformal, so Green coordinates cannot reproduce it.
A rotation with a scale and a translation of the cage, on the other hand, moves every inside point by exactly the same map; the tests check this on an L-shaped cage.

## Correctness

The [proof](proofs/correctness.md) proves the following.
Green's third identity says that a function $u$ that is harmonic inside $\Omega$ satisfies $u(\eta) = \int_{\partial\Omega}(u\,\partial G/\partial n - G\,\partial u/\partial n)\,ds$.
For $u = 1$ this gives $\sum_i \phi_i = 1$, and for $u(\xi) = \xi$, with $\partial u/\partial n = n$ and $\xi = \sum_i \Gamma_i(\xi)v_i$ on the boundary, it gives $\eta = \sum_i\phi_iv_i + \sum_j\psi_jn_j$.
If the moved cage is $v' = Mv + c$ with $M$ a rotation times a scale $\lambda > 0$, then $s_j = \lambda$ and $n'_j = Mn_j/\lambda$, so line L9 returns $M\eta + c$: similarities are reproduced.
In complex notation, the map of line L9 equals the Cauchy integral $\frac{1}{2\pi i}\oint g(\xi)/(\xi - \eta)\,d\xi$ of the piecewise linear map $g$ of the cage onto the moved cage, by an integration by parts on each edge.
A Cauchy integral is holomorphic inside the cage, so the deformation is conformal wherever its derivative is not 0.
The tests check the closed forms against Gauss-Legendre quadrature, the equality with the Cauchy integral, and the Cauchy-Riemann equations by finite differences.

## Complexity

Each edge costs $O(1)$, with two logarithms and two arctangents, so the $2n$ weights of one point take $\Theta(n)$ time and line L9 takes $\Theta(n)$.
$N$ points cost $\Theta(Nn)$; storing the weights takes $\Theta(Nn)$ memory, and the work per point needs $\Theta(n)$.
There is no precomputation beyond the weights: unlike [harmonic coordinates](/harmonic-coordinates/) there is no grid and no solve.

## Properties

- **Reproduction and partition of unity (proved).** $\eta = \sum\phi_iv_i + \sum\psi_jn_j$ and $\sum\phi_i = 1$, so the rest cage gives the identity.
- **Similarities reproduced (proved).** Rotating, scaling and moving the cage does the same to the shape.
- **Conformal in 2D (proved).** The map is holomorphic inside the cage; it keeps angles wherever its derivative is not 0.
- **General affine maps not reproduced (proved by the example).** A shear or a scale in one direction of the cage is not a conformal map, so the inside follows it only roughly.
- **Not interpolating.** The deformed shape does not pass through the moved cage vertices, and points near the cage do not follow the cage boundary exactly. A Cauchy integral has the boundary values $g$ only when $g$ extends to a holomorphic map, as for a similarity.
- **Signed weights (measurement).** $\phi_i$ can be negative for concave cages: on a grid of step $0.05$ inside the L-shaped cage of the tests, the smallest $\phi_i$ is about $-0.032$. $\psi_j$ has no fixed sign. Because of the normal terms, the weights are not barycentric coordinates in the strict sense.
- **3D quasi-conformal (stated by the paper, not checked here).** In 3D, with triangle faces in place of edges, Lipman, Levin and Cohen-Or describe the map as quasi-conformal; no 3D code or proof is on this page.

## Variants and improvements

- **3D cages.** The same identity with triangle faces gives weights per vertex and per face, with closed forms over triangles.
- **Complex coordinates.** In 2D, writing the map as a Cauchy integral leads to complex-valued cage coordinates, and to other holomorphic choices of the boundary map than the piecewise linear one.
- **Harmonic and mean value coordinates.** [Harmonic coordinates](/harmonic-coordinates/) and [mean value coordinates](/floater-mean-value-coordinates/) use vertex weights only; they reproduce all affine maps and interpolate the cage, but do not keep angles.
- **Rigid shapes by optimization.** [As-rigid-as-possible shape manipulation](/as-rigid-as-possible-shape-manipulation/) keeps local shapes by a solve over a mesh instead of a closed form.

## When to use it

Use Green coordinates when a cage should bend a shape while keeping its details from shearing, as for the face of a cartoon character, text on a curved band or a pattern on a surface.
They cost the same as other closed-form cage coordinates.
Do not use them when the shape must follow the cage exactly, or when the user expects an affine edit of the cage, such as a stretch along one axis, to stretch the shape the same way.

## Pitfalls

- **Orientation.** The formulas assume a counterclockwise cage with outward normals; a clockwise cage flips the signs of $h$ and of the normals.
- **Points on the boundary.** On an edge, $q$ has a zero and $\ln q$ a singularity, and the weights are not defined. Keep the shape strictly inside the cage.
- **Cancellation.** Compute $D$ as $2|(b - a) \times (a - \eta)|$, not as $\sqrt{4QS - R^2}$, which loses many digits near the line of the edge.
- **Forgetting $s_j$.** Without the edge stretch $s_j$, a uniformly scaled cage no longer scales the shape.
- **Large edits.** Conformal maps can grow or shrink a region a lot; a cage that is pinched hard shrinks the shape near the pinch strongly.

## Implementations

## History

Lipman, Levin and Cohen-Or presented Green coordinates at SIGGRAPH 2008, after mean value coordinates (Ju, Schaefer and Warren 2005) and harmonic coordinates (Joshi and others 2007) had made cages a common deformation tool.
They presented the coordinates as shape preserving: other cage coordinates reproduce affine maps, and so they shear details, while Green coordinates keep angles in 2D.
The equality of 2D Green coordinates with a Cauchy integral connects them with complex analysis.

## References
