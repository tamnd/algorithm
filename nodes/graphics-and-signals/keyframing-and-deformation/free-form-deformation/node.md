---
tag: 5QACBN
kind: algorithm
slug: free-form-deformation
name: Free-form deformation
aliases:
- Sederberg-Parry deformation
- lattice deformation
area: graphics-and-signals/keyframing-and-deformation
level: core
summary: Embed an object in a trivariate Bezier lattice and move its points with the lattice control points, so that any shape deforms smoothly.
solves: [shape-deformation]
model: real-ram
complexity:
  vars: {N: "the number of points to deform", l: "the lattice degree along S", m: "the lattice degree along T", n: "the lattice degree along U"}
  time: {per_point: "Θ(l m n)", all: "Θ(N l m n)"}
  space: {extra: "Θ(l m n)"}
properties: {deterministic: true, exact: true, online: true, recursive: false}
prereqs: [bezier-curve, tensor-product-surface]
see_also: [extended-free-form-deformation, barr-global-deformations, cage-based-deformation, wire-deformation, shape-deformation, de-casteljau-algorithm, bezier-patch, b-spline]
sources:
  - paper: doi:10.1145/15886.15903
    title: "Thomas W. Sederberg and Scott R. Parry, Free-form deformation of solid geometric models, SIGGRAPH 86, Computer Graphics 20(4), 151-160, 1986"
    locator: the whole paper (the parallelepiped lattice, the local coordinates, the trivariate Bernstein polynomial, the volume change and the continuity across the lattice boundary)
  - paper: doi:10.1145/97879.97900
    title: "Sabine Coquillart, Extended free-form deformation: a sculpturing tool for 3D geometric modeling, SIGGRAPH 90, Computer Graphics 24(4), 187-196, 1990"
    locator: the whole paper (lattices that are not parallelepipeds)
---

Free-form deformation (FFD) bends space, and with it any object that lies in that space.
The object sits inside a box with a grid of control points, the lattice.
Each point of the object gets its coordinates in the box once, and its new position is a trivariate Bernstein polynomial of those coordinates with the moved control points as coefficients.
Thomas Sederberg and Scott Parry (1986) introduced the method.
It works for polygon meshes, parametric surfaces and point clouds alike, because it moves points and does not care what they belong to.

## In plain words

Put a soft object inside a block of clear jelly.
Grab the jelly at a few marked points and pull them.
The jelly bends, and the object bends with it, smoothly and without tears.
FFD is that jelly.
The marked points are the control points of a grid that fills a box around the object.
At the start each point of the object is told where it sits in the box, as three numbers between 0 and 1.
When the control points move, each object point takes a weighted mix of all the control points, with weights that depend only on those three numbers.
If no control point moves, every point stays where it is.

## The problem

The input is a lattice and a set of points.
The lattice is a parallelepiped with the corner $X_0$ and the edge vectors $S$, $T$ and $U$, and the degrees $l$, $m$ and $n$.
It has the $(l + 1)(m + 1)(n + 1)$ control points $P_{ijk}$, which start at the regular grid

$$P_{ijk} = X_0 + \frac{i}{l}S + \frac{j}{m}T + \frac{k}{n}U$$

and are then moved by the user.
The output is the new position $X'$ of each point $X$.
Points inside the lattice should move smoothly with the control points, and the map should be the identity while the lattice is at rest.

## The algorithm

$B_i^l(s) = \binom{l}{i}(1 - s)^{l - i}s^i$ is the Bernstein polynomial of degree $l$.

```pseudo id=main
FFD(X, X_0, S, T, U, P)
L1  s ← (T × U)·(X - X_0) / ((T × U)·S)
L2  t ← (S × U)·(X - X_0) / ((S × U)·T)
L3  u ← (S × T)·(X - X_0) / ((S × T)·U)
L4  if s, t or u is outside [0, 1] then return X
L5  X' ← 0
L6  for i ← 0..l, j ← 0..m, k ← 0..n do X' ← X' + B_i^l(s) B_j^m(t) B_k^n(u) P_ijk
L7  return X'
```

Lines L1 to L3 compute the local coordinates, the unique $(s, t, u)$ with $X = X_0 + sS + tT + uU$.
Each is a dot product with a fixed vector, so they can be computed once per point and kept while the user edits the lattice.
Line L4 leaves the points outside the lattice where they are.
Line L6 evaluates the Bezier volume; the de Casteljau algorithm applied along each of the three directions gives the same result.

## Example

Take the unit cube as the lattice, with $l = m = n = 2$, so it has 27 control points on the grid with spacing $1/2$.
Move only the center control point $P_{111}$ from $(1/2, 1/2, 1/2)$ to $(1/2, 1/2, 1)$.
Its weight at the center of the cube is $B_1^2(1/2)^3 = (1/2)^3 = 1/8$, so the center point moves up by $1/8$ of $1/2$, to $(1/2, 1/2, 9/16)$.
At $(1/4, 1/4, 1/4)$ the weight is $B_1^2(1/4)^3 = (3/8)^3 = 27/512$, and the point moves to $(1/4, 1/4, 283/1024)$.
The corners of the cube do not move, because every Bernstein weight of an inner control point is 0 there.
The Jacobian at $(1/2, 1/2, 1/4)$ is $\operatorname{diag}(1, 1, 9/8)$: the region below the moved control point is stretched up by $12.5\%$ in volume, and the region above it is compressed.
The implementation reproduces these numbers exactly with `fractions.Fraction`.

## Correctness

The Bernstein polynomials satisfy $\sum_i B_i^l(s) = 1$ and $\sum_i \frac{i}{l} B_i^l(s) = s$.
With the control points at rest, line L6 gives $X_0 + sS + tT + uU$, which is $X$ by lines L1 to L3.
So the rest lattice gives the identity, exactly in rational arithmetic.
The same two identities show that an affine map $A$ applied to every control point gives $X' = A(X)$ for every point inside the lattice.
The Jacobian of the map is $J = \frac{\partial X'}{\partial(s, t, u)}\,\frac{\partial(s, t, u)}{\partial X}$, where the rows of the second factor are the three vectors of lines L1 to L3; the volume of a deformed region $V$ is $\int_V |\det J|\,dX$, a statement Sederberg and Parry use to control the volume.
The [proof](proofs/correctness.md) gives these arguments and the continuity across the lattice boundary.

## Complexity

Lines L1 to L4 take $O(1)$ time.
The Bernstein values take $O(l + m + n)$ time, and line L6 takes $\Theta(lmn)$ time, so one point costs $\Theta(lmn)$ and $N$ points cost $\Theta(N\,lmn)$.
The lattice holds $\Theta(lmn)$ control points.
The weights of each point can be stored once, which makes each later edit a sparse matrix product, but the dense weights cost $\Theta(N\,lmn)$ memory.

## Properties

- **Identity at rest (proved).** The rest lattice gives $X' = X$, by the linear precision of the Bernstein basis.
- **Affine invariance (proved).** Moving the lattice by an affine map moves the object by the same map.
- **Smooth inside (proved).** The map is a polynomial of degree $l + m + n$ in $X$ inside the lattice, so it is $C^\infty$ there.
- **Boundary continuity (proved).** The map is continuous across a face of the lattice if the control points on that face are at rest, and $C^k$ if the $k + 1$ outer layers of control points at that face are at rest.
- **Not interpolating.** A point at a control point does not follow it: only the corners of the lattice are interpolated.
- **No volume guarantee.** The volume changes by $\det J$, which can be negative: a lattice folded too far turns the object inside out.

## Variants and improvements

- **Other lattice shapes.** [Extended free-form deformation](/extended-free-form-deformation/) (Coquillart 1990) joins Bezier volumes of other shapes, such as cylinders, and finds the local coordinates by Newton iteration.
- **B-spline lattices.** A [B-spline](/b-spline/) volume instead of a Bezier volume makes each control point act only on nearby cells, so large lattices stay local and cheap.
- **Direct manipulation.** The user drags a point of the object, and a least squares solve finds the control point moves that put it there.
- **Cages.** [Cage-based deformation](/cage-based-deformation/) replaces the box by a coarse mesh around the object and the Bernstein weights by [generalized barycentric coordinates](/generalized-barycentric-coordinates/).
- **Simple global maps.** [Barr's global deformations](/barr-global-deformations/) taper, twist and bend with a closed form and no lattice.

## When to use it

Use FFD to shape an object with a few handles when its own representation is detailed, mixed, or not editable, such as a dense mesh or a point cloud.
It is the right tool for broad, smooth changes of shape: bulges, bends, squashes.
For a shape that should follow a coarse mesh around it, prefer [cage-based deformation](/cage-based-deformation/), whose cage can fit the object closely.
For a deformation along a curve, such as a wrinkle or a lip, use [wires](/wire-deformation/).
For deformations that should keep the local detail of a surface rigid, use a surface method such as [Laplacian surface editing](/laplacian-surface-editing/) or [as-rigid-as-possible deformation](/as-rigid-as-possible-deformation/).

## Pitfalls

- **Points outside the lattice.** They do not move, so a lattice that cuts through an object tears it unless the boundary layers of control points stay at rest.
- **Folding.** A control point moved past its neighbours can make $\det J < 0$ and turn part of the object inside out; check the sign of $\det J$ if this matters.
- **Normals.** Transform normals with the inverse transpose of $J$, not with $J$, as for [Barr's deformations](/barr-global-deformations/).
- **Polygon meshes.** FFD moves vertices only, so large curvature on large triangles shows as facets; refine the mesh first.
- **Degree.** A high degree makes each control point act on the whole lattice; for local control, raise the number of cells with a spline lattice, not the degree.

## Implementations

## History

Sederberg and Parry presented FFD at SIGGRAPH 1986 as a tool for solid modeling.
They took the lattice from Bezier volumes and showed that the method keeps the algebraic form of the object (a deformed polynomial surface stays polynomial), and that the volume change is the Jacobian determinant.
Barr's global deformations of 1984 were the earlier closed-form space deformations.
Coquillart (1990) extended the lattice to other shapes, and later work moved from lattices to cages and to surface-based methods.

## References
