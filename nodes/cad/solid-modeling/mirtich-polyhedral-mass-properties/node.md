---
tag: JVZRYG
kind: algorithm
slug: mirtich-polyhedral-mass-properties
name: Mirtich's polyhedral mass properties
aliases:
- Mirtich algorithm
area: cad/solid-modeling
level: advanced
summary: Computes the exact volume, centroid and inertia of a polyhedron by reducing volume integrals to face integrals and then to line integrals by Green's theorem.
solves: [mass-properties-of-solids]
model: real-ram
complexity:
  vars: {n: the total number of vertices over all faces (twice the number of edges)}
  time: {worst: Θ(n)}
  space: {extra: Θ(1)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1996
  people: [Brian Mirtich]
  note: Mirtich published the three-step reduction and a C program in the Journal of Graphics Tools in 1996, for use in rigid body simulation.
prereqs: [mass-properties-of-solids, boundary-representation, shoelace-formula]
see_also: [polygon-area, numerical-integration, gaussian-quadrature, monte-carlo-integration, polygon-mesh, csg-ray-casting]
sources:
  - paper: doi:10.1080/10867651.1996.10487458
    title: Brian Mirtich, Fast and accurate computation of polyhedral mass properties, Journal of Graphics Tools 1(2), 31 to 50, 1996
    locator: the whole paper (the reduction to face integrals, the projection to a coordinate plane, the Green's theorem step and the code)
  - paper: doi:10.1109/MCG.1984.6429334
    title: S. Lien and J. T. Kajiya, A symbolic method for calculating the integral properties of arbitrary nonconvex polyhedra, IEEE Computer Graphics and Applications 4(10), 35 to 42, 1984
    locator: the whole paper (the sum of signed tetrahedra)
  - paper: doi:10.1145/358628.358643
    title: Yong Tsui Lee and Aristides A. G. Requicha, Algorithms for computing the volume and other integral properties of solids, I, Known methods and open issues, Communications of the ACM 25(9), 635 to 641, 1982
    locator: the whole paper (the survey of integration methods, including the reduction to boundary integrals)
---

Mirtich's algorithm computes the volume, the center of mass and the inertia tensor of a uniform solid polyhedron from its [boundary representation](/boundary-representation/). It reduces each volume integral to a sum of integrals over the faces with the divergence theorem, then reduces each face integral to an integral over the projection of the face onto a coordinate plane, and then reduces that to a sum over the edges with Green's theorem. It solves the [mass properties problem](/mass-properties-of-solids/) for polyhedra in $\Theta(n)$ arithmetic operations, where $n$ is the number of face vertices. The results are exact when the arithmetic is exact.

## In plain words

To find the weight and the balance point of a solid, you must add up tiny pieces of the inside. A polyhedron is given only by its faces, so the method never looks at the inside. A theorem from calculus says that some sums over the inside are equal to sums over the outer skin. So the method visits each face one time.

A face is a flat polygon at an angle. The method lays it flat onto the floor or onto a wall, whichever gives the biggest shadow, and corrects for the tilt. A second theorem then turns the sum over the flat shadow into a sum along its edges. Each edge adds a short formula of the two corner coordinates. So the method is a loop over the faces and a loop over the edges of each face, with no division into small pieces.

## The problem

The input is a closed polyhedral surface: a list of planar faces, each a list of vertices $p_0, \ldots, p_{k-1}$ in $\mathbb{R}^3$. The vertices of each face are in counterclockwise order seen from outside, so the outward normal follows the right-hand rule. The surface bounds a solid $V$ with constant density $\rho$. The output is

- the volume $T_0 = \int_V 1 \, dV$ and the mass $m = \rho T_0$;
- the first moments $T_x = \int_V x \, dV$, $T_y$, $T_z$, and the center of mass $r = (T_x, T_y, T_z)/T_0$;
- the second moments $T_{x^2} = \int_V x^2 \, dV$, $T_{y^2}$, $T_{z^2}$ and the products $T_{xy} = \int_V xy \, dV$, $T_{yz}$, $T_{zx}$;
- the inertia tensor about $r$. Its diagonal entry is $J_{xx} = \rho (T_{y^2} + T_{z^2}) - m (r_y^2 + r_z^2)$, and its off-diagonal entry is $J_{xy} = -(\rho T_{xy} - m r_x r_y)$. The other entries follow by a cyclic shift of $x, y, z$.

The last line is the parallel axis theorem: the tensor about the origin, minus the tensor of a point mass $m$ at $r$.

## The algorithm

Write $\hat n$ for the unit outward normal of a face $f$ and $w$ for the constant with $\hat n \cdot p + w = 0$ on the plane of $f$. Three identities do the work.

1. **Divergence theorem.** For a vector field $F$, $\int_V \nabla \cdot F \, dV = \sum_f \int_f F \cdot \hat n \, dA$. The fields $(x, 0, 0)$, $(x^2/2, 0, 0)$, $(x^3/3, 0, 0)$ and $(x^2 y/2, 0, 0)$ give $T_0 = \sum_f \hat n_x \int_f x \, dA$, $T_x = \frac{1}{2} \sum_f \hat n_x \int_f x^2 \, dA$, $T_{x^2} = \frac{1}{3} \sum_f \hat n_x \int_f x^3 \, dA$ and $T_{xy} = \frac{1}{2} \sum_f \hat n_x \int_f x^2 y \, dA$. The same holds with $x, y, z$ shifted cyclically.
2. **Projection.** Pick the coordinate $\gamma$ with the largest $|\hat n_\gamma|$ and let $\alpha, \beta$ be the next two in the cyclic order $x, y, z$. On the face, $\gamma = -(\hat n_\alpha \alpha + \hat n_\beta \beta + w)/\hat n_\gamma$, and $dA = d\alpha \, d\beta / |\hat n_\gamma|$. So a face integral of a polynomial becomes a combination of the *projection integrals* $P_{pq} = \int_\Pi \alpha^p \beta^q \, d\alpha \, d\beta$ over the projected polygon $\Pi$, with $p + q \le 3$.
3. **Green's theorem.** $P_{pq} = \frac{1}{p+1} \oint_{\partial \Pi} \alpha^{p+1} \beta^q \, d\beta$. On a straight edge the line integral of a polynomial has a closed form in the two end points. For $P_{00}$ it is the [shoelace formula](/shoelace-formula/).

```pseudo id=main
MIRTICH(faces)                         ▷ closed surface, faces counterclockwise from outside
L1  T0 ← 0, T1 ← (0, 0, 0), T2 ← (0, 0, 0), TP ← (0, 0, 0)
L2  for each face f = (p0, ..., pk−1) do
L3      n ← the Newell normal of f, w ← −n · p0       ▷ n is outward, |n| = 2 · area(f)
L4      γ ← the axis with the largest |nγ|, (α, β) ← the next two axes in cyclic order
L5      P ← the ten projection integrals P00, ..., P03 of f on the (α, β) plane, by sums over the edges
L6      F ← the twelve face integrals of f, from P, n and w, with γ = −(nα α + nβ β + w)/nγ
L7      add the terms of f to T0, T1, T2 and TP, by the divergence theorem
L8  return T0, T1/2, T2/3, TP/2

MASS(faces, ρ)
L9  m ← ρ T0, r ← T1/T0, J ← the tensor about r by the parallel axis theorem
```

Line L3 does not normalize the normal. Every face integral in line L7 is multiplied by a normal component and divided by a power of $n_\gamma$ in the same degree, so the length of $n$ cancels. This keeps the whole computation in the field of the input coordinates: with rational input there is no square root. Line L5 uses the signed projection integrals: the projected polygon is counterclockwise exactly when $n_\gamma > 0$, because $(\alpha, \beta, \gamma)$ is a cyclic order. Dividing by the signed $n_\gamma$ in line L6 then gives the factor $1/|\hat n_\gamma|$ of step 2.

## Example

Take the tetrahedron with vertices $O = (0, 0, 0)$, $A = (2, 0, 0)$, $B = (0, 3, 0)$ and $C = (0, 0, 4)$. Its four faces, each counterclockwise from outside, give these values.

| face | Newell normal $n$ | $w$ | $\gamma$ | $P_{00}$ | term of $T_0$ | terms of $T_1$ |
|---|---|---|---|---|---|---|
| $O B A$ | $(0, 0, -6)$ | $0$ | $z$ | $-3$ | $0$ | $(0, 0, 0)$ |
| $O A C$ | $(0, -8, 0)$ | $0$ | $y$ | $-4$ | $0$ | $(0, 0, 0)$ |
| $O C B$ | $(-12, 0, 0)$ | $0$ | $x$ | $-6$ | $0$ | $(0, 0, 0)$ |
| $A B C$ | $(12, 8, 6)$ | $-24$ | $x$ | $6$ | $4$ | $(4, 6, 8)$ |

On each of the first three faces one coordinate is $0$ and the normal points along that axis, so every term vanishes. The face $ABC$ projects onto the $(y, z)$ plane as the triangle $(3, 0), (0, 4), (0, 0)$, counterclockwise, with area $P_{00} = 6$, $\int y = 6$ and $\int z = 8$. On the face, $x = (24 - 8y - 6z)/12$, so $\int_\Pi x \, dy \, dz = (24 \cdot 6 - 8 \cdot 6 - 6 \cdot 8)/12 = 4$. That is the volume $T_0 = 4$, which agrees with $\det(A, B, C)/6 = 24/6$.

Line L8 halves $T_1$ to $(2, 3, 4)$, so the center of mass is $r = (1/2, 3/4, 1)$, the mean of the four vertices. The second moments are $T_2 = (8/5, 18/5, 32/5)$ and $TP = (T_{xy}, T_{yz}, T_{zx}) = (6/5, 12/5, 8/5)$. With $\rho = 1$, line L9 gives the inertia tensor about $r$:

$$J = \begin{pmatrix} 15/4 & 3/10 & 2/5 \\ 3/10 & 3 & 3/5 \\ 2/5 & 3/5 & 39/20 \end{pmatrix}.$$

For instance $J_{xx} = 18/5 + 32/5 - 4 (9/16 + 1) = 10 - 25/4 = 15/4$.

## Correctness

The three identities are exact, so the algorithm returns the exact integrals when the arithmetic is exact. Step 1 is the divergence theorem applied to a polynomial field on a polyhedron. Step 2 is the change of variables from a planar face to its projection, which is one to one because $\hat n_\gamma \ne 0$. Step 3 is Green's theorem on a polygon, and the edge formulas are the exact integrals of a polynomial along a segment. The [full proof](proofs/correctness.md) derives the edge formulas and the signs.

## Complexity

For a face of $k$ vertices, lines L3 and L5 cost $\Theta(k)$ arithmetic operations, and lines L4, L6 and L7 cost $O(1)$. The total is $\Theta(n)$, where $n$ is the sum of the face sizes, which is twice the number of edges. The extra space is $\Theta(1)$: the algorithm keeps only the running sums. This holds in the [real RAM](/real-ram/). In exact rational arithmetic each operation costs more, but the count of operations is the same.

No algorithm can do better than $\Omega(n)$ in general. On a triangle mesh the volume depends on every vertex: if an algorithm does not read one coordinate, moving that vertex a little along the coordinate axis changes the volume but not the answer.

## Properties

- **Exact.** With integer or rational coordinates every step is a ring operation or a division by $n_\gamma \ne 0$. So the results are exact rationals. With integer coordinates, $6 T_0$, $24 T_x$, $120 T_{x^2}$ and $120 T_{xy}$ are integers, because each equals a sum of signed tetrahedra (see Variants) with those denominators.
- **Signed.** If every face is reversed, every result changes sign. The volume is positive exactly when the faces are oriented outward.
- **Works on non-convex solids and solids with holes.** Nothing in the method uses convexity. A face may be any simple planar polygon, and a solid may have through holes and cavities, as long as the surface is closed and consistently oriented.
- **Winding number.** For a closed surface that intersects itself, the sums give $\int \omega(p) g(p) \, dp$, where $\omega$ is the [winding number](/generalized-winding-number/) of the surface around $p$. They are the integrals over the solid only when $\omega$ is $0$ or $1$ everywhere.
- **Independent of the origin, in exact arithmetic.** In floating point, moving the solid far from the origin causes [cancellation](/catastrophic-cancellation/) in the third-degree terms. Translate the vertices so that one vertex is at the origin first.

## Variants and improvements

- **Signed tetrahedra.** Fan each face into triangles and add, for each triangle $(a, b, c)$, the signed tetrahedron with the origin: volume $\det(a, b, c)/6$, first moment $\frac{V}{4}(a + b + c)$, and $\int x_i x_j \, dV = \frac{V}{20}\left(\sum_v v_i v_j + s_i s_j\right)$, where the sum is over $a, b, c$ and $s = a + b + c$. This is the method of Lien and Kajiya (1984). It gives the same results and is the brute force of the tests. It needs a triangulation of each face.
- **Higher moments and polynomial densities.** The same three steps work for any polynomial integrand. A density $\rho(x, y, z)$ of degree $d$ needs projection integrals of degree up to $d + 3$.
- **Planar regions.** In the plane, Green's theorem alone gives the area and moments of a polygon. The area is the [shoelace formula](/shoelace-formula/) of the [polygon area](/polygon-area/) page.
- **Curved solids.** For a B-rep with curved faces there is no closed form. Apply [Gaussian quadrature](/gaussian-quadrature/) to the face integrals of step 1, or use [Monte Carlo integration](/monte-carlo-integration/) with [CSG ray casting](/csg-ray-casting/) or point classification.

## When to use it

Use it to get the mass properties of a mesh or a polyhedral B-rep: for a rigid body simulation, for the center of gravity of a part, or to check the volume of a Boolean result. It needs a closed, consistently oriented surface with planar faces. For a triangle mesh the signed tetrahedra are shorter to code and as fast. For a mesh with holes in the surface or bad orientation, repair it first ([mesh repair](/mesh-repair-problem/)), or use the generalized winding number.

## Pitfalls

- **A fixed projection axis.** If line L4 always takes $\gamma = z$, a face parallel to the $z$ axis has $n_z = 0$, and line L6 divides by zero. In floating point a face that is nearly vertical loses all accuracy. Line L4 must take the axis with the largest $|n_\gamma|$, so that $|\hat n_\gamma| \ge 1/\sqrt{3}$.
- **Inconsistent orientation.** Line L3 takes the normal from the vertex order. One face in the wrong order adds its terms with the wrong sign, and the result is wrong with no warning. Orient all faces outward before line L2, and test that $T_0 > 0$.
- **Inertia about the wrong point.** Lines L1 to L8 give moments about the origin. Line L9 must subtract the point mass term $m(r_y^2 + r_z^2)$ to get the tensor about the center of mass. The off-diagonal entries are $-\int xy$, not $+\int xy$.
- **Non-planar faces.** Line L6 assumes that the whole face lies in the plane of line L3. A face of a scanned mesh with four slightly non-coplanar vertices breaks this. Triangulate such faces first.
- **Normalizing the normal.** Making $n$ a unit vector in line L3 needs a square root. It adds rounding error in floating point and leaves the rationals in exact arithmetic. It is not needed, because the length cancels.

## Implementations

## History

Lee and Requicha surveyed the methods for the volume and the moments of solids in 1982, and Lien and Kajiya gave the sum of signed tetrahedra for non-convex polyhedra in 1984. Brian Mirtich published the reduction by projection and Green's theorem in the Journal of Graphics Tools in 1996, with a C program. It was written for the dynamics of rigid bodies in simulation, where the inertia tensor of each body is needed.

## References
