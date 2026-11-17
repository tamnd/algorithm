---
tag: B6HGFM
kind: algorithm
slug: as-rigid-as-possible-shape-interpolation
name: As-rigid-as-possible shape interpolation
aliases:
- ARAP shape interpolation
area: graphics-and-signals/keyframing-and-deformation
level: advanced
summary: Morph between two compatible triangulations by interpolating the rotation and stretch of each triangle separately and solving for a consistent mesh.
model: real-ram
complexity:
  vars: {n: "the number of vertices", m: "the number of triangles"}
  time: {build: "O(n^3 + m)", query: "O(n^2 + m)"}
  space: {extra: "Θ(n^2)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
prereqs: [least-squares-problem, singular-value-decomposition]
see_also: [as-rigid-as-possible-shape-manipulation, as-rigid-as-possible-deformation, arap-parameterization, beier-neely-morphing, keyframe-interpolation, cholesky-decomposition, delaunay-triangulation, kabsch-algorithm]
sources:
  - paper: doi:10.1145/344779.344859
    title: "Marc Alexa, Daniel Cohen-Or and David Levin, As-rigid-as-possible shape interpolation, SIGGRAPH 2000, 157-164"
    locator: "Section 2 (the decomposition of each affine map, equation 5 for A(t), the quadratic energy of equation 8 with one fixed vertex, and the symmetric variant of Section 2.3) and Section 3 (compatible dissections)"
  - paper: doi:10.1145/1377980.1377993
    title: "William Baxter, Pascal Barla and Ken-ichi Anjyo, Rigid shape interpolation using normal equations, NPAR 2008, 59-64"
    locator: the choice of consistent rotation angles for neighbouring triangles, and the normal equations that are factored once
---

As-rigid-as-possible shape interpolation morphs one 2D shape into another when both are triangulated with the same triangles.
For each triangle it takes the affine map from the source triangle to the target triangle, splits it into a rotation and a stretch, and interpolates the angle of the rotation and the entries of the stretch separately.
The interpolated triangles do not fit together, so the vertices at each time are the least squares fit to them.
Marc Alexa, Daniel Cohen-Or and David Levin (2000) introduced the method.
It avoids the shrinking and the kinks of linear interpolation of the vertices, because a triangle that only turns keeps its shape and area at every time.

## In plain words

Picture a cartoon arm drawn as a mesh of small triangles, first held down and then raised.
If every corner moves in a straight line to its new place, the arm shrinks in the middle of the move, as if it were made of rubber.
This method looks at each small triangle instead.
It asks how much the triangle turns and how much it is stretched, and makes it turn and stretch a little at a time.
Those little triangles no longer fit together, like tiles cut a bit wrong.
So the method finds the mesh that comes closest to all of them at once.
That mesh turns the arm as a whole, and the arm keeps its size.

## The problem

The input is a source shape $P = (p_1, \dots, p_n)$ and a target shape $Q = (q_1, \dots, q_n)$ of points in the plane, a list of triangles on the vertex indices that triangulates both shapes, and a time $t \in [0, 1]$.
The two triangulations must be compatible: the same triangles, with the same orientation, in both shapes.
The output is the shape $V(t) = (v_1(t), \dots, v_n(t))$, with $V(0) = P$ and $V(1) = Q$.
The shapes in between should keep each triangle as close to a rotated and gradually stretched copy of itself as possible.

For a triangle $f = (i, j, k)$, $A_f$ is the 2 by 2 matrix with $A_f(p_j - p_i) = q_j - q_i$ and $A_f(p_k - p_i) = q_k - q_i$, the linear part of the affine map of the triangle.
In the same way, $B_f(V)$ is the linear part of the map from the source triangle to the triangle $f$ of $V$; it is linear in $V$.

## The algorithm

$R(\theta)$ is the rotation by $\theta$.
The polar decomposition of a 2 by 2 matrix $A$ with $\det A > 0$ is $A = R(\gamma)S$ with $S$ symmetric positive definite; in 2D it has the closed form $\gamma = \operatorname{atan2}(a_{21} - a_{12}, a_{11} + a_{22})$ and $S = R(\gamma)^{\mathsf T}A$.

```pseudo id=main
ARAP-INTERPOLATION(P, Q, triangles)               ▷ build, once
L1  for each triangle f do
L2      A_f ← the linear part of the map from triangle f of P to triangle f of Q
L3      (R(γ_f), S_f) ← polar(A_f)
L4  walk over neighbouring triangles: γ_g ← γ_g + 2πk with |γ_g - γ_f| ≤ π
L5  H ← the matrix of Σ_f |B_f(V)|²_F, without vertex 1      ▷ does not depend on t
AT(t)                                               ▷ query, for each frame
L6  A_f(t) ← R(t γ_f) ((1 - t) I + t S_f) for each triangle f
L7  v_1(t) ← (1 - t) p_1 + t q_1
L8  for each coordinate x and y: solve H z = b(t) for the free vertices
L9  return V(t)
```

Lines L1 to L3 compute the matrices and their polar decompositions.
Line L4 makes the angles consistent, as Baxter, Barla and Anjyo (2008) propose: the polar decomposition gives angles in $(-\pi, \pi]$, and two neighbouring triangles that both turn by about 180 degrees could get the angles $+3.1$ and $-3.1$ and turn in opposite directions.
Line L5 builds the normal equations of the energy

$$E(V) = \sum_f \bigl\lVert B_f(V) - A_f(t)\bigr\rVert_F^2,$$

which Alexa et al. minimize at each time.
Each entry of $B_f(V)$ depends only on the $x$ coordinates or only on the $y$ coordinates of $V$, so the energy splits into an $x$ part and a $y$ part with the same matrix $H$.
Fixing $v_1$ removes the free translation, and $H$ is then positive definite for a connected triangulation.
Only the right side $b(t)$ of line L8 depends on $t$, so $H$ is factored once and each frame costs two solves.

## Example

**One triangle.** Let $P = ((0, 0), (1, 0), (0, 1))$ and $Q = ((0, 0), (0, 2), (-1, 0))$.
Line L2 gives $A = \begin{pmatrix} 0 & -1 \\ 2 & 0 \end{pmatrix}$, and line L3 gives $\gamma = \operatorname{atan2}(3, 0) = \pi/2$ and $S = \operatorname{diag}(2, 1)$: the triangle is stretched by 2 along $x$ and turned by 90 degrees.
At $t = 0.5$, line L6 gives $A(0.5) = R(\pi/4)\operatorname{diag}(1.5, 1)$.
With one triangle the fit is exact, so $V(0.5) = ((0, 0), (1.06066, 1.06066), (-0.70711, 0.70711))$, with the area $0.75$.
Linear interpolation of the vertices gives $((0, 0), (0.5, 1), (-0.5, 0.5))$, with the area $0.375$, less than both the source area $0.5$ and the target area $1$.
The area of the interpolated triangle is $\frac12\det A(t) = \frac12(1 + t)$, which grows steadily from $0.5$ to $1$.

**A turn by almost 180 degrees.** Let $Q$ be a 3 by 3 grid of vertices with 8 triangles, turned by $3$ radians.
Every $A_f$ is $R(3)$, so the interpolation turns the grid rigidly, and $V(0.5)$ is the grid turned by $1.5$ radians, with the full area.
Linear interpolation of the vertices maps the grid by $\frac12(I + R(3))$, whose determinant is $\frac12(1 + \cos 3) = 0.005$, so the grid at $t = 0.5$ has only 0.5 percent of its area.

**Consistent angles.** On a strip of four triangles with the angles $3.0, -3.1, 3.05, -3.0$ from line L3, line L4 adds $2\pi$ to the second and the fourth, which gives $3.0, 3.183, 3.05, 3.283$.
All four triangles then turn the same way.

## Correctness

The matrix path of line L6 starts at $A_f(0) = I$ and ends at $A_f(1) = R(\gamma_f)S_f = A_f$.
At $t = 0$, the source shape has $B_f = I$ for every triangle, so it has the energy 0, and with $v_1(0) = p_1$ it is the only minimizer; so $V(0) = P$.
At $t = 1$, the target shape has the energy 0 in the same way, so $V(1) = Q$.

If the target is a rigid motion of the source by the angle $\theta \in (-\pi, \pi)$, every $A_f$ is $R(\theta)$, every $S_f$ is $I$, and the path is $R(t\theta)$.
The shape $P$ turned by $t\theta$ about $p_1$ and moved to $v_1(t)$ fits every triangle exactly, so the morph is rigid.

If $\det A_f > 0$, then $S_f$ is positive definite, so $(1 - t)I + tS_f$ is positive definite and $\det A_f(t) > 0$ for all $t$: each target triangle keeps its orientation.
The least squares fit of line L8 can still flip a triangle, because it only approximates the targets.
The [proof](proofs/correctness.md) gives the details, including why $H$ is positive definite for a connected triangulation.

## Complexity

Lines L1 to L4 take $\Theta(m)$ time for $m$ triangles.
$H$ has one row and column per free vertex and a nonzero entry for each edge of the triangulation, so it is sparse, with $O(n + m)$ nonzero entries.
The implementation stores $H$ as a dense matrix and inverts it once, at the cost $O(n^3)$ and $\Theta(n^2)$ memory, and then each frame costs $O(n^2 + m)$.
With a sparse [Cholesky factorization](/cholesky-decomposition/) of $H$, as in practice, the factor is computed once and each frame costs two sparse triangular solves, close to linear in $n$ for planar meshes with a good ordering.

## Properties

- **Exact ends.** $V(0) = P$ and $V(1) = Q$.
- **Rigid motions are kept.** A target that is a rotation and a translation of the source gives a rigid morph.
- **Triangle orientations are kept in the targets.** Each $A_f(t)$ has a positive determinant when $A_f$ has.
- **Not symmetric.** Interpolating from $Q$ to $P$ at the time $1 - t$ does not give the same shapes in general, because the decomposition depends on which shape is the source. Alexa et al. give a symmetric variant.
- **Translation by one vertex.** The motion of the whole shape is set by the path of the fixed vertex; a different choice of the fixed vertex moves the shapes by a translation that depends on $t$.
- **Smooth in $t$.** For fixed angles, $V(t)$ is an analytic function of $t$, because the right side of line L8 is.

## Variants and improvements

- **Other matrix paths.** Alexa et al. also consider the decomposition $A = R_\alpha D R_\beta$ from the [singular value decomposition](/singular-value-decomposition/), and they prefer the symmetric polar form because the singular value form behaves worse.
- **Symmetric variant.** Alexa et al. (Section 2.3) give a variant of the energy that treats the two shapes in the same way, so that the morph from $Q$ to $P$ is the reverse of the morph from $P$ to $Q$.
- **Consistent angles.** Baxter, Barla and Anjyo (2008) make the angles of neighbouring triangles consistent and write the energy as normal equations that are factored once, which makes the interpolation interactive. They also interpolate more than two shapes.
- **Three dimensions.** The same construction works for compatible tetrahedral meshes, with the polar decomposition of 3 by 3 matrices and rotations interpolated as quaternions, for example by [slerp](/spherical-linear-interpolation/).
- **Compatible triangulations.** If the two shapes are given only as outlines, a compatible triangulation of both must be built first, often with added interior vertices. Alexa et al. do this with compatible dissections.

## When to use it

Use as-rigid-as-possible shape interpolation to morph the outline of a 2D character or object between two poses, as in cartoon in-betweening, when both poses can be triangulated with the same triangles.
It is the right tool when parts of the shape turn by large angles, where linear interpolation shrinks them.
For images rather than shapes, use a warp such as [Beier-Neely morphing](/beier-neely-morphing/), which needs only line correspondences and no triangulation.
For an interactive deformation of one shape by handles, use [as-rigid-as-possible shape manipulation](/as-rigid-as-possible-shape-manipulation/) instead: it fits a shape to handle positions, while this method blends between two given shapes.
The [as-rigid-as-possible deformation](/as-rigid-as-possible-deformation/) of surfaces and the [ARAP parameterization](/arap-parameterization/) of a surface onto the plane use the same idea of local rotations, but they alternate local fits and a global solve and are not interpolations between two shapes.

## Pitfalls

- **Incompatible triangulations.** The method needs the same triangles in both shapes. A triangle that is flipped in the target has $\det A_f < 0$, and its path passes through a degenerate triangle.
- **Inconsistent angles.** Without line L4, two neighbours that turn by about 180 degrees can turn in opposite directions, and the fit tears the mesh in the middle of the morph.
- **Turns beyond 180 degrees.** The polar decomposition only sees the angle modulo $2\pi$. A shape that should spin more than half a turn needs the extra turns added to the angles by hand.
- **Thin triangles.** Long thin triangles in the source make $A_f$ sensitive to small moves of the vertices. A good triangulation of the source helps.
- **The fixed vertex.** The path of vertex 1 is a straight line; if the whole shape should move on an arc, move the result by a rigid motion of its own.

## Implementations

## History

Alexa, Cohen-Or and Levin presented the method at SIGGRAPH 2000, with compatible triangulations of the two shapes made from compatible dissections, and with examples in 2D and 3D.
Earlier shape morphs interpolated vertices or the intrinsic data of polygons, such as edge lengths and angles.
Baxter, Barla and Anjyo (2008) made the angles consistent, wrote the energy as normal equations, and extended the method to more than two shapes.
The idea of fitting a mesh to local rotations later led to as-rigid-as-possible shape manipulation and surface deformation.

## References
