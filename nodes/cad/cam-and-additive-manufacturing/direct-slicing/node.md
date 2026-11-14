---
tag: YQA8PY
kind: algorithm
slug: direct-slicing
name: Direct slicing of CAD models
aliases:
- CAD-based slicing
area: cad/cam-and-additive-manufacturing
level: advanced
summary: Cuts the exact CAD solid by each layer plane instead of a triangle mesh, so the layer contours are exact curves and the only error is the one chosen for the printer path.
solves: [slicing-for-additive-manufacturing]
model: real-ram
complexity:
  vars: {k: number of layers, t: number of nodes of the CSG tree, n: total number of polygon vertices over all layers}
  time: {conic_trees: O(k t), polygons: O(t n)}
  space: {extra: O(t + n)}
properties: {deterministic: true, recursive: true, exact: true}
history:
  year: 1992
  people: [Sashidhar Guduri, Richard H. Crawford, Joseph J. Beaman, Ron Jamieson, Herbert Hacker]
  note: Guduri, Crawford and Beaman sliced CSG solids of quadrics into exact contours in 1992 and 1993. Jamieson and Hacker (1995) sliced the B-rep inside the CAD system and named the method.
prereqs: [constructive-solid-geometry, triangle-mesh-slicing]
see_also: [boundary-representation, nurbs, surface-surface-intersection, implicit-surface, slicing-for-additive-manufacturing, adaptive-slicing, staircase-effect, curved-layer-printing]
sources:
  - paper: "Sashidhar Guduri, Richard H. Crawford and Joseph J. Beaman, A method to generate exact contour files for solid freeform fabrication, Solid Freeform Fabrication Symposium 1992, University of Texas at Austin, 95 to 101"
    locator: exact contours of CSG solids built from quadric primitives
  - paper: "Sashidhar Guduri, Richard H. Crawford and Joseph J. Beaman, Direct generation of contour files from constructive solid geometry representations, Solid Freeform Fabrication Symposium 1993, University of Texas at Austin, 291 to 302"
    locator: the contours of a layer computed from the CSG tree without a tessellation (general locator)
  - paper: doi:10.1108/13552549510086826
    title: Ron Jamieson and Herbert Hacker, Direct slicing of CAD models for rapid prototyping, Rapid Prototyping Journal 1(2), 1995, 4 to 12
    locator: slicing the B-rep model inside the CAD system, with the plane section of each face, instead of an STL file
  - paper: doi:10.1016/j.cad.2004.06.014
    title: Binil Starly, Alan Lau, Wei Sun, Wing Lau and Tom Bradbury, Direct slicing of STEP based NURBS models for layered manufacturing, Computer-Aided Design 37(4), 2005, 387 to 397
    locator: the contours of NURBS faces read from a STEP file, computed by ray casting along raster lines, with adaptive layer thickness
---

Direct slicing computes the layers of a part for additive manufacturing from the exact CAD model, not from a triangle mesh. The usual chain exports the solid as an STL mesh and then cuts the triangles with the layer planes, as in [triangle mesh slicing](/triangle-mesh-slicing/). The mesh only touches the true surface at its vertices, so every contour inherits the chord error of the export, and this error is fixed in 3D before anyone knows the layer height. Direct slicing intersects each layer plane with the true faces of the model. For a solid made of planes, spheres, cylinders and cones the section of each face is an exact conic with rational coefficients, and the layer is the same Boolean expression of these conics. For NURBS faces the section is a curve that a numerical method computes to a tolerance that the user sets per layer. Guduri, Crawford and Beaman (1992) did this for CSG solids of quadrics, and Jamieson and Hacker (1995) did it for the B-rep inside a CAD system. This page gives the exact version for a CSG tree of quadrics, proves that the section of the tree is the tree of the sections, and bounds the error of the polygon that is finally sent to the printer.

## In plain words

To print a part, the printer needs its outline on each layer. The common way first turns the smooth part into many small flat triangles, then cuts the triangles. The triangles are a little off the real surface, so every outline is a little off too, and nothing later can fix it.

Direct slicing skips the triangles. It asks the CAD model itself where each layer crosses the surface. For a ball or a round hole the answer is an exact circle or oval. The outline only becomes straight segments at the very end, and the program picks as many segments as it needs to stay within the error that the user allows on that layer.

## The problem

A solid is given as a CSG tree ([constructive solid geometry](/constructive-solid-geometry/)). Each leaf is a quadric half-space: a symmetric $4 \times 4$ matrix $Q$, with the solid $\{p : \hat p^{\mathsf T} Q \hat p \le 0\}$ for $\hat p = (x, y, z, 1)$. Each inner node is a union, an intersection or a difference of its two children. A ball of center $c$ and radius $R$ is $|p - c|^2 - R^2 \le 0$. An infinite cylinder through the point $q$ with axis direction $a$ and radius $r$ is
$$|p - q|^2 - \frac{((p - q) \cdot a)^2}{|a|^2} - r^2 \le 0,$$
and a half-space $n \cdot p \le d$ is a quadric with no quadratic part. All input numbers are rational.

Given the tree $T$, the layer heights $Z_1 < \dots < Z_k$ and a tolerance tol, the task is to give, for each layer, the exact set $S(T) \cap \{z = Z_i\}$, and a set of polygons for the printer whose distance from the true contours is at most tol.

## The algorithm

Substitute $z = Z$ in the quadric. The result is a conic $\bar p^{\mathsf T} M \bar p \le 0$ with $\bar p = (x, y, 1)$ and a symmetric $3 \times 3$ matrix $M$. The upper left $2 \times 2$ block $A$ of $M$ is the same as in $Q$, the last column picks up $Q_{i3} Z + Q_{i4}$, and the corner is $Q_{33} Z^2 + 2 Q_{34} Z + Q_{44}$. With rational $Q$ and $Z$ these are rational numbers, computed without error.

```pseudo id=main
DIRECT-SLICE(T, Z, tol)
L1  for each leaf Q of T: M_Q ← SECTION(Q, Z)        ▷ exact rational conic
L2  T_Z ← T with each leaf Q replaced by M_Q          ▷ the exact layer
L3  contours ← empty list
L4  for each leaf M of T_Z do
L5      (kind, c, f_c) ← CLASSIFY(M)
L6      if kind = ellipse then P ← POLYLINE(M, tol)
L7          append the runs of vertices v of P with CLASSIFY-POINT(T_Z, v, M) = on
L8  return T_Z, contours

CLASSIFY(M)                       ▷ A = 2×2 block, b = (M13, M23), f₀ = M33
L9  if det A = 0 then return parabolic
L10 c ← −A⁻¹ b; f_c ← f₀ + b·c       ▷ the value of the conic at its center
L11 if A is positive definite then return ellipse, point or empty as f_c <, =, > 0
L12 return hyperbola, line pair or complement

POLYLINE(M, tol)                  ▷ a ≥ b semi-axes, e₁, e₂ unit axes
L13 n ← max(3, ⌈π / arccos(1 − tol/a)⌉)
L14 return c + a cos(2πj/n) e₁ + b sin(2πj/n) e₂ for j = 0 … n−1
```

Lines L1 and L2 are the whole exact part: the layer is the tree $T_Z$, and a point $(x, y)$ is in the layer if and only if the same Boolean expression of the signs of the conics says so. CLASSIFY finds the center $c$ where the gradient of the conic vanishes, and the value $f_c$ there. If the block $A$ is positive definite and $f_c < 0$, the leaf is an ellipse with squared semi-axes $-f_c/\lambda_1$ and $-f_c/\lambda_2$, where $\lambda_1, \lambda_2$ are the eigenvalues of $A$. The type, the center, $f_c$, $\det A$ and $\operatorname{tr} A$ are exact. The semi-axes and their directions need square roots, so only they are floats.

POLYLINE is the only step that approximates. It places $n$ vertices on the ellipse, and $n$ is the least number of vertices for which the chord error $a(1 - \cos(\pi/n))$ is at most tol. Line L7 trims the polygon of one leaf to the boundary of the layer. A vertex is kept when it is on the boundary of $T_Z$ with that leaf forced to "on", with the three valued rules: a union is in if one side is in, an intersection is out if one side is out, and a difference is an intersection with the complement, which swaps in and out.

A general CAD model is a [B-rep](/boundary-representation/) whose faces are planes, quadrics, tori and [NURBS](/nurbs/) patches. The same plan applies face by face: the section of a plane or a quadric face is a line or a conic, trimmed to the face boundary, and the section of a NURBS face is a curve that a [surface-surface intersection](/surface-surface-intersection/) method traces to a tolerance. The pieces are then linked into loops by their end points.

## Example

A ball of radius 10 at the origin has a straight hole of radius 2 drilled through it. The hole has the axis direction $a = (3, 0, 4)$ through the origin, so it leans $36.87°$ from the vertical. The tree is $T = \text{ball} \setminus \text{cylinder}$. Slice it at $Z = 4$ with tol $= 0.01$.

Line L1 gives two conics. For the ball, $M = \operatorname{diag}(1, 1, -84)$: the circle $x^2 + y^2 \le 84$, which is $R^2 - Z^2 = 100 - 16$. For the cylinder, $|a|^2 = 25$ and
$$M = \begin{pmatrix} 16/25 & 0 & -48/25 \\ 0 & 1 & 0 \\ -48/25 & 0 & 44/25 \end{pmatrix},$$
which is $16 x^2 + 25 y^2 - 96 x + 44 \le 0$ after multiplying by 25.

| leaf | kind | center $c$ | $f_c$ | $\det A$ | squared semi-axes |
|---|---|---|---|---|---|
| ball | ellipse | $(0, 0)$ | $-84$ | 1 | 84 and 84 |
| cylinder | ellipse | $(3, 0)$ | $-4$ | $16/25$ | $25/4$ and $4$ |

The cylinder gives the ellipse $(x - 3)^2/6.25 + y^2/4 \le 1$, with semi-axes 2.5 along $x$ and 2 along $y$. The closed form agrees: the axis meets the plane at $t = Z/a_z = 1$, at $(3, 0, 4)$, and a cylinder of radius $r$ cut by a plane at angle gives the semi-axes $r$ and $r|a|/|a_z| = 2 \cdot 5/4 = 2.5$. All the numbers in the table are exact fractions.

The point $(3, 0)$ is in the hole: the ball conic is $-75 \le 0$ and the cylinder conic is $-100/25 = -4 \le 0$, so the difference says out. The point $(7, 0)$ has the scaled cylinder value $16 \cdot 49 - 96 \cdot 7 + 44 = 156 > 0$ and the ball value $49 - 84 < 0$, so it is in the layer.

Line L13 gives $n = 68$ for the outer circle ($a = \sqrt{84} \approx 9.165$) and $n = 36$ for the hole ($a = 2.5$). The hole lies inside the disk, so all the vertices of both polygons are "on", and the result is two closed loops. On the next layer only the numbers $Z$ change in line L1, and the error stays at most 0.01 on every layer.

**The same ball as a mesh.** A UV sphere of radius 10 with 16 rings and 32 segments is within about 0.096 of the true sphere in 3D. Slice it at $z = 2.5$: the section is a regular 32-gon with circumradius 9.641 and inradius 9.595, while the true circle has radius $\sqrt{93.75} \approx 9.682$. The contour is off by up to 0.088. At $z = -9.95$, near the pole, the true radius is 0.999 and the mesh section has radius at most 0.508, so the contour is off by 0.49: the surface is almost flat there, and a small error in height becomes a large error in the layer. The direct section at $z = 2.5$ is $x^2 + y^2 \le 375/4$, exactly.

## Correctness

Three facts make the method correct. First, substituting $z = Z$ in $\hat p^{\mathsf T} Q \hat p$ gives $\bar p^{\mathsf T} M \bar p$ term by term, so each leaf conic is the exact section of its leaf. Second, the section by a plane commutes with union, intersection and difference: $(A \cup B) \cap \Pi = (A \cap \Pi) \cup (B \cap \Pi)$, and the same for the other two. By induction on the tree, $T_Z$ describes exactly the section of the solid. Third, the polygon of POLYLINE is the affine image of a regular $n$-gon inscribed in the unit circle. Pairing each point of the circle with the point of the $n$-gon on the same ray moves it by a factor between $\cos(\pi/n)$ and 1. The affine map stretches no vector by more than $a$, so the Hausdorff distance between the polygon and the ellipse is at most $a(1 - \cos(\pi/n)) \le \text{tol}$.

One caveat: CAD kernels use regularized Boolean operations, and regularization does not commute with the section. At a plane that only touches a face, the exact section can have a lower dimension part, such as the single point $x^2 + y^2 \le 0$ at the pole of a ball. The regularized layer drops it. The trimming of line L7 is a float test, and near a point where two conics cross, a kept run ends up to one edge before the crossing. The full proof is in [the correctness proof](proofs/correctness.md).

**What the tests check.** They compare the sphere section with $r^2 = R^2 - (Z - c_z)^2$ and the cylinder section with the semi-axes $r$ and $r|a|/|a_z|$ on random rational input, exactly. They compare the 2D membership with the 3D membership on random trees and points, and they measure the Hausdorff distance of the polygons against tol.

## Complexity

For one layer, line L1 does a fixed number of exact operations per leaf, so the conic tree costs $O(t)$, and $k$ layers cost $O(k t)$. The rational numbers grow with the size of the input fractions and of $Z$, not with the number of layers, because each layer starts again from $Q$. Testing one point against $T_Z$ costs $O(t)$.

The polygon of an ellipse with largest semi-axis $a$ has $n = \lceil \pi / \arccos(1 - \text{tol}/a) \rceil \approx \pi \sqrt{a / (2\,\text{tol})}$ vertices, because $1 - \cos x \approx x^2/2$. A tolerance 10 times smaller needs about $\sqrt{10} \approx 3.2$ times more vertices: for $a = \sqrt{93.75}$ the counts are 22, 70 and 219 for tol 0.1, 0.01 and 0.001. Trimming tests each vertex against the tree, so $n$ output vertices over all layers cost $O(t n)$. A mesh slicer runs in time linear in the number of triangles, but the mesh must be fine everywhere to be accurate on the worst layer.

For NURBS faces the cost depends on the intersection method and the tolerance, and no simple bound covers it.

## Properties

- **No tessellation error.** The layer is the exact section of the model. For quadric solids it is exact in rational arithmetic.
- **Error chosen per layer.** The only approximation is the polygon output, with an error bound that the user sets, and it can change from layer to layer.
- **No mesh repair.** The input is a valid solid, so the gaps, flipped triangles and self intersections of bad STL files do not occur.
- **Depends on the CAD kernel.** The slicer needs the CAD model or a STEP file, and a surface intersection routine for each face type.
- **Boundary cases.** At a plane that touches a face, the exact section can contain points or curves of lower dimension, which regularization removes.

## Variants and improvements

- **B-rep slicing.** Jamieson and Hacker (1995) cut each face of the B-rep inside the CAD system, which gives the section curves of planes, quadrics and spline faces.
- **NURBS by ray casting.** Starly and coauthors (2005) read NURBS faces from a STEP file and compute the contours as raster lines with [ray casting](/ray-casting/), together with adaptive layer heights.
- **Adaptive direct slicing.** The exact model gives the surface normal at each contour point, so the cusp height of [adaptive slicing](/adaptive-slicing/) can be computed from the true surface instead of from triangle normals.
- **Implicit and volume models.** A model given as an [implicit surface](/implicit-surface/) or a signed distance field is sliced by contouring each plane of the field, for example with [marching squares](/marching-squares/).
- **Curved layers.** When the layers are not planes, the same idea cuts the model with a family of surfaces. See [curved layer printing](/curved-layer-printing/).

## When to use it

Use direct slicing when the CAD model is available and the surface quality matters: large parts with gently sloped faces, where the error of the mesh near the flat regions shows on the layers, or parts for which a fine STL file would be very large. It also helps when the mesh export produces bad geometry. Use mesh slicing when only a mesh exists (scans, models from other tools), when the slicer must accept any input, or when the printer software only reads STL.

## Pitfalls

- **Calling NURBS slicing exact.** The section of a NURBS face is not a closed form curve. It is computed numerically to a tolerance. Direct slicing removes the error of the tessellation, not every error.
- **Float conics.** Computing the conic coefficients in floats loses the exact type at tangent planes. A sphere cut at its pole can come out as a tiny ellipse or as empty.
- **Ignoring regularization.** Point and curve parts of a section at a tangent plane must be removed before the path planner sees them.
- **Too few vertices for the large axis.** The vertex count must use the largest semi-axis. Using the smaller one breaks the bound on long thin ellipses, for example the section of a steep cylinder.
- **Trimming by samples.** A trimmed polygon run ends at a vertex near the crossing of two conics, not at the crossing. Compute the crossing points when the corners must be sharp.

## Implementations

## History

Guduri, Crawford and Beaman (1992, 1993) described the exact contours of CSG solids built from quadric primitives at the Solid Freeform Fabrication Symposium in Austin. Jamieson and Hacker (1995) sliced the B-rep inside the CAD system and avoided the STL file, which gave the method its name. Later work moved the method to exchange formats: Starly, Lau, Sun, Lau and Bradbury (2005) sliced NURBS models read from STEP files. Most printer software still slices meshes, because the input is usually an STL or 3MF file.

## References
