---
tag: 702PFN
kind: algorithm
slug: barr-global-deformations
name: Barr's global deformations
aliases:
- twist bend taper deformations
area: graphics-and-signals/keyframing-and-deformation
level: intro
summary: Deform a solid by a transform whose matrix varies along an axis, giving tapering, twisting and bending, and transform normals by the inverse transpose Jacobian.
solves: [shape-deformation]
model: real-ram
complexity:
  vars: {N: "the number of points", g: "the number of operations in the chain"}
  time: {all: "Θ(N g)"}
  space: {extra: "O(1)"}
properties: {deterministic: true, exact: true, online: true, recursive: false}
prereqs: [deformation-gradient]
see_also: [free-form-deformation, extended-free-form-deformation, wire-deformation, shape-deformation, cage-based-deformation, frenet-frame, rotation-minimizing-frame, linear-blend-skinning]
sources:
  - paper: doi:10.1145/800031.808573
    title: "Alan H. Barr, Global and local deformations of solid primitives, SIGGRAPH 84, Computer Graphics 18(3), 21-30, 1984"
    locator: the whole paper (tapering, twisting and bending along an axis, the Jacobian matrices of these maps, and the transformation of normal vectors)
---

Barr's global deformations are three simple maps of space: taper, twist and bend.
Each one changes a solid by a transform that varies smoothly along one axis: a scale that depends on the height, a rotation whose angle depends on the height, or a bend of the axis onto a circle.
Because each map has a closed form, its Jacobian matrix $J$ has one too, and normal vectors move with the cofactor matrix of $J$, which is $\det(J)J^{-\mathsf T}$.
Alan Barr (1984) introduced them, and they are still the twist, bend and taper tools of modeling programs.
They need no lattice, no handles and no solve; a chain of them builds a horn or a twisted column from a cylinder.

## In plain words

Take a straight bar of soft clay.
Squeeze the top end thinner than the bottom: that is a taper.
Turn the top end while you hold the bottom: that is a twist.
Curl the bar around a can: that is a bend.
Each of these acts on every point of the bar by a simple rule that depends only on how high the point is.
Barr wrote each rule as a formula, and also the formula for how a small arrow on the surface changes.
That second formula tells the renderer which way the bent surface faces, so the shading comes out right.

## The problem

The input is a point $p = (x, y, z)$ with a normal vector $n$, and a chain of operations, each a smooth map $F: \mathbb{R}^3 \to \mathbb{R}^3$ with its Jacobian $J_F$.
The output is the moved point and its new unit normal.
Barr's three maps, along the $z$ axis for taper and twist and along the $y$ axis for bend:

- **Taper** with a scale $r(z)$: $F(x, y, z) = (r(z)x, r(z)y, z)$, with $J = \begin{pmatrix} r & 0 & r'x \\ 0 & r & r'y \\ 0 & 0 & 1 \end{pmatrix}$ and $\det J = r^2$.
- **Twist** with an angle $\theta(z)$: $F = (x\cos\theta - y\sin\theta,\; x\sin\theta + y\cos\theta,\; z)$, with $\det J = 1$.
- **Bend** with the rate $k$, the center $y_0$ and the region $[y_{\min}, y_{\max}]$: let $\hat y$ be $y$ clamped to the region, $\theta = k(\hat y - y_0)$, $C = \cos\theta$ and $S = \sin\theta$. Inside the region, $F = (x,\; -S(z - 1/k) + y_0,\; C(z - 1/k) + 1/k)$. Outside it, the part beyond the region continues along the tangent: add $C(y - \hat y)$ to the second coordinate and $S(y - \hat y)$ to the third. $\det J = 1 - kz$ inside and 1 outside.

## The algorithm

$\operatorname{cof}(J)$ is the cofactor matrix of $J$: its entry $(i, j)$ is $(-1)^{i+j}$ times the minor of $J$ without row $i$ and column $j$.

```pseudo id=main
BARR(p, n, ops)
L1  J ← I
L2  for each operation F in ops, in order do
L3      J ← J_F(p) J
L4      p ← F(p)
L5  m ← cof(J) n
L6  return p, m / |m|
```

Line L3 evaluates the Jacobian of each operation at the current point, before the point moves, so $J$ is the Jacobian of the whole chain by the chain rule.
Line L5 moves the normal; for an invertible $J$, $\operatorname{cof}(J) = \det(J)J^{-\mathsf T}$, so after line L6 this is the inverse transpose rule, with the sign of $\det J$ kept.

## Example

**Taper.** With $r(z) = 1 - 0.4z$, the point $(1, 0, 1)$ on the side of the unit cylinder moves to $(0.6, 0, 1)$, and $\det J = 0.36$.
Its normal $(1, 0, 0)$ becomes $\operatorname{cof}(J)(1, 0, 0) \propto (1, 0, 0.4)$, normalized $(0.9285, 0, 0.3714)$: the tapered side leans in, so its normal tilts up.
The naive rule $Jn = (0.6, 0, 0)$ keeps the normal horizontal, which is wrong: the tangent $(-0.4, 0, 1)$ of the tapered side is not perpendicular to it.

**Twist.** With $\theta(z) = \frac{\pi}{2}z$, the point $(1, 0, 1)$ turns to $(0, 1, 1)$ and its normal $(1, 0, 0)$ to $(0, 1, 0)$; points at $z = 0$ do not move.

**Bend.** With $k = 0.5$, $y_0 = 0$ and the region $[-2, 2]$, the point $(0, 1, 0)$ has $\theta = 0.5$ and moves to $(0, 2\sin 0.5, 2 - 2\cos 0.5) = (0, 0.9589, 0.2448)$, on the circle of radius $1/k = 2$ about $(y_0, 1/k) = (0, 2)$.
At $(0, 1, 0.5)$, $\det J = 1 - 0.5 \cdot 0.5 = 0.75$: the inner side of the bend is compressed.
The point $(0, 3, 0)$ is beyond the region and moves along the tangent at the end of the arc to $(0, 2.2232, 1.7609)$.

## Correctness

By the chain rule, after line L3 has run for the first $i$ operations, $J$ is the Jacobian of their composition at the original point.
A normal at $p$ is $a \times b$ for two tangent vectors $a$, $b$ of the surface; the map sends them to $Ja$ and $Jb$, and the identity $(Ja) \times (Jb) = \operatorname{cof}(J)(a \times b)$ holds for every 3 by 3 matrix.
So line L5 gives a vector perpendicular to the moved surface, with the orientation of the moved tangent frame.
The determinants of the three maps follow from their Jacobians; for the bend inside the region the $y, z$ block is $\begin{pmatrix} C(1 - kz) & -S \\ S(1 - kz) & C \end{pmatrix}$, with the determinant $1 - kz$.
The [proof](proofs/correctness.md) derives these and shows that the bend is continuous at the ends of the region.

## Complexity

Each operation costs $O(1)$ per point, with a 3 by 3 matrix product for line L3.
A chain of $g$ operations on $N$ points costs $\Theta(Ng)$ time.
Line L5 and the normalization cost $O(1)$ per point.
The algorithm needs $O(1)$ memory beyond the points, because each point is processed on its own.

## Properties

- **Normals are exact (proved).** The cofactor rule gives a normal of the moved surface for any smooth map, with no approximation.
- **Volume (proved).** The local volume ratio is $\det J$: $r(z)^2$ for a taper, 1 for a twist, so a twist keeps the volume, and $1 - kz$ inside a bend.
- **Fold (proved).** Inside a bend, points with $z > 1/k$ have $\det J < 0$: the far side of the bend axis is turned inside out. Keep the object below $z = 1/k$.
- **Bend is only $C^0$ at the region ends (proved).** Positions are continuous at $y_{\min}$ and $y_{\max}$, but the Jacobian jumps there unless $z = 0$, because $\det J$ changes from $1 - kz$ to 1.
- **Order matters.** A taper and a twist along the same axis commute, because a scale in $xy$ commutes with a rotation in $xy$; a bend and a twist do not.
- **Smooth, not local.** Each map acts on all of space, so it changes the whole object, not one part.

## Variants and improvements

- **Other profiles.** $r(z)$ and $\theta(z)$ can be any smooth functions, such as splines, and a taper can scale $x$ and $y$ differently.
- **Local deformations.** Barr's paper also covers deformations that act only on part of an object; a bend with a finite region is the simplest case.
- **Along a curve.** Bending onto a general space curve uses a frame along the curve, such as the [Frenet frame](/frenet-frame/) or a [rotation-minimizing frame](/rotation-minimizing-frame/), in place of the circle; [wires](/wire-deformation/) generalize this to deformations controlled by curves.
- **Lattices.** [Free-form deformation](/free-form-deformation/) gives arbitrary smooth maps at the cost of a lattice of control points.

## When to use it

Use Barr's deformations for simple, global shape changes along one axis: a tapered column, a twisted ribbon, a bent tube, a horn from a cylinder.
They are cheap and exact, and the normals come out right, so they are a good first modeling tool and a good test of a renderer's normal transform.
For changes of a part of an object, or shapes driven by control points, use [free-form deformation](/free-form-deformation/) or [cage-based deformation](/cage-based-deformation/).

## Pitfalls

- **Normals by $J$.** Moving a normal by $J$ instead of $\operatorname{cof}(J)$ or $J^{-\mathsf T}$ tilts it wrongly under any taper or bend.
- **Lost orientation.** $J^{-\mathsf T}n$ points the wrong way where $\det J < 0$; $\operatorname{cof}(J)n$ keeps the side of the moved tangent frame.
- **Jacobian at the wrong point.** In a chain, each $J_F$ must be taken at the point before that operation, as in line L3, not at the original point.
- **Bend axis.** Points beyond the bend radius, $z > 1/k$, fold over; tight bends of thick objects need $k$ small enough.
- **Region ends.** The kink in the derivative at $y_{\min}$ and $y_{\max}$ shows as a crease in the shading of a thick object; spread the bend over a larger region or blend the rate $k$ smoothly.

## Implementations

## History

Barr presented global and local deformations at SIGGRAPH 1984, as hierarchical operations for solid modeling with primitives such as superquadrics.
He gave the taper, twist and bend with their Jacobians, and the rule for moving normal vectors, so that deformed implicit and parametric surfaces could be rendered and ray traced.
Free-form deformation (Sederberg and Parry 1986) generalized the idea from closed-form maps to lattices of control points.

## References
