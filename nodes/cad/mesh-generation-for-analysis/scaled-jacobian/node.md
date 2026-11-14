---
tag: ECBX02
kind: definition
slug: scaled-jacobian
name: Scaled Jacobian
aliases:
- scaled Jacobian quality
area: cad/mesh-generation-for-analysis
level: core
summary: The determinant of the element Jacobian at a corner divided by the product of the edge lengths there, 1 for a cube and at most 0 for an inverted element.
prereqs: [determinant, hadamard-bound, bilinear-interpolation]
see_also: [mesh-quality-measures, radius-edge-ratio, sliver-tetrahedron, hexahedral-mesh-generation, mesh-untangling, optimization-based-mesh-smoothing, structured-grid-generation, finite-element-method]
sources:
  - paper: doi:10.1137/S1064827500371499
    title: Patrick M. Knupp, Algebraic mesh quality metrics, SIAM Journal on Scientific Computing 23(1), 2001, 193 to 218
    locator: the Jacobian matrices at the corners of triangles, quadrilaterals, tetrahedra and hexahedra as the basis of quality metrics, and their invariance under scaling and rotation (general locator)
  - paper: doi:10.1016/0045-7825(90)90004-6
    title: Patrick M. Knupp, On the invertibility of the isoparametric map, Computer Methods in Applied Mechanics and Engineering 78(3), 1990, 313 to 329
    locator: positive corner Jacobians make the bilinear map of a quadrilateral invertible, but not the trilinear map of a hexahedron
  - paper: "Jonathan Richard Shewchuk, What is a good linear element? Interpolation, conditioning, and quality measures, Proceedings of the 11th International Meshing Roundtable, Sandia National Laboratories, 2002, 115 to 126"
    locator: quality measures for tetrahedra and what each one detects (general locator)
---

The scaled Jacobian of a mesh element is the determinant of the edge vectors at a corner divided by the product of their lengths, minimized over the corners. It is 1 for a square or a cube corner, it is near 0 for a flat or badly skewed element, and it is negative when the element is inverted. Hexahedral and quadrilateral meshers report it first, because a non-positive value means that the element map is not invertible and the [finite element](/finite-element-method/) computation fails.

## Definition

**Corner value.** Let $p$ be a corner of an element in $\mathbb{R}^d$, $d = 2$ or $3$, and let $e_1, \ldots, e_d$ be the vectors from $p$ along the $d$ element edges at $p$, in the order that gives a positive [determinant](/determinant/) for a correctly oriented element. The corner value is

$$J_p = \frac{\det(e_1, \ldots, e_d)}{|e_1| \cdots |e_d|} = \det\left( \frac{e_1}{|e_1|}, \ldots, \frac{e_d}{|e_d|} \right).$$

For a triangle or a quadrilateral, $J_p = \sin \theta_p$, where $\theta_p$ is the interior angle at $p$, and it is negative at a reflex corner. The name comes from the element map. The bilinear map of a quadrilateral, the trilinear map of a hexahedron and the linear map of a simplex all have the edge vectors $e_i$ as the columns of their Jacobian matrix at the corner $p$. So $\det(e_1, \ldots, e_d)$ is the Jacobian there, and $J_p$ is that Jacobian scaled by the edge lengths.

**Element value.** For a quadrilateral or a hexahedron, $\mathrm{SJ} = \min_p J_p$ over the 4 or 8 corners. A simplex needs a normalization, because the regular simplex does not have right angles. For a triangle, $\mathrm{SJ} = \frac{2}{\sqrt{3}} \min_p J_p$. For a tetrahedron, $\mathrm{SJ} = \sqrt{2} \min_p J_p$. Codes differ in these constants, so a reported value needs its convention.

**As a quality measure.** Larger is better. For quadrilaterals and hexahedra the range is $[-1, 1]$ with ideal value 1, reached exactly by rectangles and boxes. For triangles the range is $[-2/\sqrt{3}, 1]$ and for tetrahedra $[-\sqrt{2}, 1]$, with ideal value 1, reached exactly by the regular simplex. The measure detects inversion (a value at most 0) and angular distortion: skew, flat corners and slivers. It does not detect stretching. A $1 \times 1 \times 100$ box has $\mathrm{SJ} = 1$, so the measure is used with an aspect ratio or an edge ratio. It is one of the [mesh quality measures](/mesh-quality-measures/).

**Range of a corner value.** By the [Hadamard bound](/hadamard-bound/), $|\det(e_1, \ldots, e_d)| \le |e_1| \cdots |e_d|$, with equality for nonzero vectors if and only if they are pairwise orthogonal. So $-1 \le J_p \le 1$, and $J_p = 1$ if and only if the edges at $p$ are orthogonal and positively ordered. A box has orthogonal edges at every corner, so its value is 1, and a quadrilateral or a hexahedron with every corner value 1 has right angles everywhere and is a rectangle or a box.

**Invariance.** A translation does not change the edge vectors. A rotation $Q$ has $\det Q = 1$ and keeps lengths, so $\det(Q e_1, \ldots, Q e_d) = \det(e_1, \ldots, e_d)$. Scaling one edge vector $e_i$ by $s > 0$ multiplies the determinant and the product of lengths by $s$. So $J_p$ is invariant under translations, rotations, uniform scaling, and independent scaling of the edges at the corner. A reflection changes the sign of every $J_p$, which is how the measure detects inversion. A shear or a general affine map changes the value.

**Theorem (positivity of the bilinear map).** Let a quadrilateral $p_{00}, p_{10}, p_{11}, p_{01}$ have the bilinear map $x(u, v) = (1-u)(1-v) p_{00} + u(1-v) p_{10} + u v\, p_{11} + (1-u) v\, p_{01}$ on $[0, 1]^2$. If the four corner Jacobians are positive, then $\det Dx(u, v) > 0$ everywhere on the square.

*Proof.* Here $x_u = A + v B$ and $x_v = C + u B$, with $A = p_{10} - p_{00}$, $C = p_{01} - p_{00}$ and $B = p_{11} - p_{10} - p_{01} + p_{00}$. So $\det(x_u, x_v) = \det(A, C) + u \det(A, B) + v \det(B, C) + u v \det(B, B)$, and $\det(B, B) = 0$. The Jacobian is an affine function of $(u, v)$, so its minimum over the square is at a corner. At the corners it equals the corner Jacobians, which are positive. $\blacksquare$

So for a quadrilateral, $\mathrm{SJ} > 0$ if and only if the bilinear map is invertible, which is the case for a strictly convex quadrilateral. The same claim fails for the trilinear hexahedron: its Jacobian is a polynomial of higher degree, and Knupp showed that positive Jacobians at the 8 corners do not guarantee a positive Jacobian inside. So a positive hexahedral $\mathrm{SJ}$ is a necessary check, not a proof of validity.

**Theorem (the tetrahedron normalization).** For every positively oriented tetrahedron, $\min_p J_p \le 1/\sqrt{2}$, with equality if and only if the tetrahedron is regular. So $\mathrm{SJ} = \sqrt{2} \min_p J_p \le 1$.

*Proof.* At a corner $p$, let $\alpha$, $\beta$, $\gamma$ be the three face angles, that is, the angles between pairs of edges at $p$, with $\alpha$ opposite $e_1$ and so on. The Gram matrix of the unit edge vectors has determinant $J_p^2 = 1 - \cos^2 \alpha - \cos^2 \beta - \cos^2 \gamma + 2 \cos \alpha \cos \beta \cos \gamma$. With $s = (\alpha + \beta + \gamma)/2$,

$$J_p^2 = 4 \sin s \, \sin(s - \alpha) \sin(s - \beta) \sin(s - \gamma).$$

To check this, write $2 \sin s \sin(s - \alpha) = \cos \alpha - \cos(\beta + \gamma)$ and $2 \sin(s - \beta) \sin(s - \gamma) = \cos(\beta - \gamma) - \cos \alpha$. With $P = \cos \beta \cos \gamma$ and $Q = \sin \beta \sin \gamma$, the product is $(\cos \alpha - P + Q)(P + Q - \cos \alpha) = Q^2 - (\cos \alpha - P)^2$, and $Q^2 = (1 - \cos^2 \beta)(1 - \cos^2 \gamma)$ expands to the Gram determinant.

The 12 face angles of a tetrahedron are the angles of its 4 triangular faces, so they add up to $4 \pi$. The 4 corner sums $2s$ have the mean $\pi$, so some corner has $s \le \pi / 2$. At that corner, each face angle is less than the sum of the other two, so $s - \alpha$, $s - \beta$, $s - \gamma$ are in $(0, \pi)$. The function $\log \sin$ is concave on $(0, \pi)$, and the three numbers have the mean $s/3$. By [Jensen's inequality](/jensens-inequality/), $\sin(s - \alpha) \sin(s - \beta) \sin(s - \gamma) \le \sin^3(s/3)$. So $J_p^2 \le 4 \sin s \sin^3(s / 3)$. On $(0, \pi / 2]$ both factors increase, so $J_p^2 \le 4 \cdot 1 \cdot (1/2)^3 = 1/2$, and the inequality is strict when $s < \pi / 2$.

Now suppose that $\min_p J_p \ge 1/\sqrt{2}$. No corner can have $s < \pi/2$. Since the mean of the corner sums is $\pi$, every corner has $s = \pi/2$. Equality in Jensen's inequality at every corner forces $\alpha = \beta = \gamma = \pi / 3$. Then all four faces are equilateral, all edges are equal, and the tetrahedron is regular. The regular tetrahedron has $J_p^2 = 1 - 3/4 + 2/8 = 1/2$ at every corner, so equality holds. $\blacksquare$

For a triangle the same holds with a short proof: the smallest angle is at most $60°$, so $\min_p \sin \theta_p \le \sin 60° = \sqrt{3}/2$, with equality only for the equilateral triangle. A single corner of a simplex can still have $J_p = 1$: the tetrahedron $(0,0,0), (1,0,0), (0,1,0), (0,0,1)$ has corner values $1, \frac{1}{2}, \frac{1}{2}, \frac{1}{2}$. That is why the element value takes the minimum.

For a tetrahedron with the even orderings of the corners, every corner determinant equals $6V$, with $V$ the signed volume. So $\mathrm{SJ} = 6 \sqrt{2}\, V / \max_p (|e_1| |e_2| |e_3|)_p$ for $V > 0$. The value is 0 exactly when the volume is 0, whatever the edge lengths are, which is why it detects slivers.

## Examples and non-examples

**Quadrilaterals and hexahedra.**

- The unit cube: every corner has three orthogonal unit edges, so $J_p = \det I = 1$ and $\mathrm{SJ} = 1$. The $1 \times 1 \times 100$ box also has $\mathrm{SJ} = 1$.
- The parallelepiped with a $60°$ angle in its base, $(x, y, z) \mapsto (x + y/2, \sqrt{3} y / 2, z)$ applied to the cube: every corner value is $\sin 60° \approx 0.866$.
- The trapezoid $(0,0), (4,0), (3,1), (1,1)$: all four corners have angle $45°$ or $135°$, so $\mathrm{SJ} = \sin 45° \approx 0.707$.
- Non-example, a dart: $(0,0), (3,0), (1,1), (0,3)$. The corner at $(1,1)$ is reflex, with interior angle about $216.9°$ and $J_p = -0.6$. The bilinear map of this quadrilateral folds over itself.
- Non-example, a dented cube: the unit cube with the vertex $(1,1,1)$ moved to $(0.5, 0.5, 0.5)$. The moved corner has $J_p \approx -0.770$ and its three neighbors have $J_p \approx 0.577$, so $\mathrm{SJ} < 0$ and the element is inverted near that corner.

**Tetrahedra.**

- The regular tetrahedron: $\mathrm{SJ} = 1$.
- The corner tetrahedron $(0,0,0), (1,0,0), (0,1,0), (0,0,1)$: $\mathrm{SJ} = \sqrt{2}/2 \approx 0.707$.
- The sliver $T_{0.01}$ of the [radius-edge ratio](/radius-edge-ratio/) page, four nearly cocircular and coplanar points: every corner value is about $0.020$, so $\mathrm{SJ} \approx 0.028$, while its radius-edge ratio is a good $0.707$.
- The cap with apex at height $0.1$ over an equilateral triangle inscribed in the unit circle: the corner values are about $0.086$ at the base and $0.256$ at the apex, so $\mathrm{SJ} \approx 0.122$.

## Related definitions

- [Mesh quality measures](/mesh-quality-measures/): the other measures, with their ranges and the defects they detect.
- [Radius-edge ratio](/radius-edge-ratio/): bounded by Delaunay refinement, but blind to slivers. The scaled Jacobian sees them.
- [Sliver tetrahedron](/sliver-tetrahedron/): the flat element with good edges, whose scaled Jacobian is near 0.
- [Mesh untangling](/mesh-untangling/): moves vertices until every corner value is positive.
- [Optimization-based mesh smoothing](/optimization-based-mesh-smoothing/): maximizes the worst value, often the scaled Jacobian, over the elements around a vertex.
- [Hexahedral mesh generation](/hexahedral-mesh-generation/) and [structured grid generation](/structured-grid-generation/): the settings in which a minimum scaled Jacobian is the first number to check.

## References
