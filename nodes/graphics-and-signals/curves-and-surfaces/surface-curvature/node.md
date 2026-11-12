---
tag: N0S7K8
kind: concept
slug: surface-curvature
name: Surface curvature
aliases:
- Gaussian curvature
- mean curvature
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: How a surface bends at a point. The principal curvatures are the extreme normal curvatures; their product is the Gaussian curvature K and their mean is the mean curvature H.
prereqs: [fundamental-forms]
see_also: [fundamental-forms, surface-of-revolution, ruled-surface, surface-tessellation, symmetric-eigenproblem, euler-formula, polygon-mesh, frenet-frame]
sources:
  - book: isbn:9780132125895
    title: Manfredo P. do Carmo, Differential Geometry of Curves and Surfaces, Prentice-Hall, 1976
    locator: Section 3-2, The Definition of the Gauss Map and Its Fundamental Properties (principal curvatures, Euler's formula); Section 3-3, The Gauss Map in Local Coordinates (K and H from E, F, G, L, M, N); Section 4-3, The Gauss Theorem; Section 4-5, The Gauss-Bonnet Theorem and Its Applications
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: Chapter 19, W. Boehm, Differential Geometry II (normal curvature, principal curvatures, Gaussian and mean curvature of a patch)
---

Surface curvature describes how a surface bends at a point. A curve has one curvature, but a surface can bend by different amounts in different directions, so the curvature at a point is a whole function of the direction. Its maximum and minimum, the principal curvatures, sum it up, and two numbers made from them, the Gaussian curvature $K$ and the mean curvature $H$, are the ones that most applications use. All of them come from the [fundamental forms](/fundamental-forms/) of a parametrization.

## In plain words

Stand on a surface and look in one direction. Along that direction the surface curves up, curves down, or stays flat, and by some amount. Turn around, and the amount changes. On a sphere it is the same in every direction. On a cylinder it is largest around the cylinder and zero along it. On a saddle the surface curves up in one direction and down in another. The largest and the smallest amounts are the principal curvatures, and the two directions where they occur are always at right angles. Their product tells the kind of point: positive for a dome, negative for a saddle, zero for a cylinder or a plane. A surface with zero product everywhere can be made from a flat sheet without stretching. Their average is zero for a soap film, which pulls itself as small as it can.

## The idea

### Normal curvature and the principal curvatures

Let $S(u, v)$ be a regular parametric surface with unit normal $n$, first fundamental form $\mathrm{I}$ with coefficients $E, F, G$ and second fundamental form $\mathrm{II}$ with coefficients $L, M, N$. The normal curvature in the tangent direction $d$ is $k_n(d) = \mathrm{II}(d, d)/\mathrm{I}(d, d)$, the signed curvature of the normal section in that direction (see [fundamental forms](/fundamental-forms/) for the proof).

As a ratio of two quadratic forms, $k_n$ takes its extreme values at the eigenvectors of the shape operator

$$W = \mathrm{I}^{-1} \mathrm{II} = \frac{1}{EG - F^2} \begin{pmatrix} GL - FM & GM - FN \\ EM - FL & EN - FM \end{pmatrix}.$$

$W$ is self-adjoint with respect to $\mathrm{I}$, so it has two real eigenvalues $k_1 \ge k_2$, the principal curvatures, and when $k_1 \ne k_2$ its eigenvectors, the principal directions, are orthogonal on the surface. This is the 2 by 2 case of the [symmetric eigenproblem](/symmetric-eigenproblem/) in the inner product $\mathrm{I}$. With unit principal directions $e_1, e_2$ and $d = \cos \theta\, e_1 + \sin \theta\, e_2$,

$$k_n(d) = k_1 \cos^2 \theta + k_2 \sin^2 \theta,$$

which is Euler's formula. So the two principal curvatures and one direction give the normal curvature in every direction.

### Gaussian and mean curvature

$$K = k_1 k_2 = \det W = \frac{LN - M^2}{EG - F^2}, \qquad H = \frac{k_1 + k_2}{2} = \frac{\operatorname{tr} W}{2} = \frac{EN - 2FM + GL}{2(EG - F^2)},$$

and conversely $k_{1,2} = H \pm \sqrt{H^2 - K}$, where $H^2 - K = (k_1 - k_2)^2/4 \ge 0$.

- **Sign.** Replacing $n$ by $-n$ changes the signs of $L, M, N$, so $k_1, k_2$ and $H$ change sign and swap order, and $K$ does not change.
- **Kinds of points.** $K > 0$ is an elliptic point, where the surface lies on one side of its tangent plane nearby. $K < 0$ is a hyperbolic point, where it crosses the tangent plane along two directions with $k_n = 0$. $K = 0$ with $W \ne 0$ is a parabolic point, and $W = 0$ is a planar point. A point with $k_1 = k_2$ is an umbilic; on the sphere every point is one.
- **Intrinsic.** By the Gauss theorem, $K$ depends only on $E, F, G$ and their derivatives, so bending a surface without stretching keeps $K$. The cylinder and the plane both have $K = 0$ for this reason. $H$ is not intrinsic: it is $0$ for the plane and $\mp 1/(2A)$ for a cylinder of radius $A$.
- **Gauss-Bonnet.** For a closed, oriented surface, $\iint K\, dA = 2\pi \chi$, where $\chi$ is the Euler characteristic (do Carmo, Section 4-5). The sphere gives $4\pi$ with $\chi = 2$, and every torus gives $0$ with $\chi = 0$. On a [polygon mesh](/polygon-mesh/) the same total is the sum of the angle defects $2\pi - \sum(\text{angles})$ at the vertices, which equals $2\pi \chi$ exactly by [Euler's formula](/euler-formula/) $V - E + F = \chi$.

### Computing the curvatures at a point

```pseudo id=main
PRINCIPAL-CURVATURES(E, F, G, L, M, N)
L1  D ← EG − F²                              ▷ D > 0 at a regular point
L2  K ← (LN − M²) / D
L3  H ← (EN − 2FM + GL) / (2D)
L4  r ← sqrt(max(0, H² − K))
L5  return H + r, H − r
```

The cost is a constant number of operations and one square root, after the six coefficients. A principal direction for $k$ is a nonzero solution of $(W - kI) x = 0$: from the first row $x = (W_{12}, k - W_{11})$, and from the second row $x = (k - W_{22}, W_{21})$. The implementation takes the longer of the two, because one of them can vanish. At an umbilic both vanish and every direction is principal, so it returns $S_u$ and the direction orthogonal to it in the first form.

**Rounding.** $K$ and $H$ are computed with small relative error from the six coefficients. The principal curvatures are not, near an umbilic: there $H^2 - K$ is a difference of two nearly equal numbers, so its rounding error is about $\varepsilon H^2$ with $\varepsilon$ the machine epsilon, and its square root moves $k_1$ and $k_2$ by about $\sqrt \varepsilon\, |H|$. On the sphere of radius 3 in double precision, at 200 random points, the largest relative error observed was about $8 \times 10^{-16}$ for $K$ and $H$, and about $2 \times 10^{-8}$ for $k_1$ and $k_2$, which is $\sqrt \varepsilon$ in size. For the same reason the umbilic test compares $H^2 - K$ with a relative tolerance, and does not test $k_1 = k_2$.

## Examples

All charts below use the normal $S_u \times S_v / |S_u \times S_v|$, so the signs of $H$ and $k_i$ follow from it.

| surface | chart | $k_1$ | $k_2$ | $K$ | $H$ |
|---|---|---|---|---|---|
| sphere, radius $R$ | latitude $u$, longitude $v$ (normal inward) | $1/R$ | $1/R$ | $1/R^2$ | $1/R$ |
| cylinder, radius $A$ | $(A \cos u, A \sin u, v)$ (normal outward) | $0$ | $-1/A$ | $0$ | $-1/(2A)$ |
| torus $R = 3$, $a = 1$, outer equator $u = 0$ | normal into the tube | $1$ | $1/4$ | $1/4$ | $5/8$ |
| same torus, top circle $u = \pi/2$ | | $1$ | $0$ | $0$ | $1/2$ |
| same torus, inner equator $u = \pi$ | | $1$ | $-1/2$ | $-1/2$ | $1/4$ |
| saddle $(u, v, uv)$ at $(0, 0)$ | normal $(-v, -u, 1)/w$ | $1$ | $-1$ | $-1$ | $0$ |
| saddle at $(1, 1)$ | | $1/(3\sqrt 3)$ | $-1/\sqrt 3$ | $-1/9$ | $-1/(3\sqrt 3)$ |

- **The torus.** In general $k_1 = 1/a$ along the meridian circle and $k_2 = \cos u/(R + a \cos u)$ along the parallel, so $K = \cos u / (a(R + a\cos u))$. The outer half, where $\cos u > 0$, is elliptic, the inner half is hyperbolic, and the top and bottom circles are parabolic. Integrating $K\, dA = \cos u\, du\, dv$ gives $+4\pi$ over the outer half and $-4\pi$ over the inner half, which sum to $0$ as Gauss-Bonnet requires. The implementation finds these values with a product Simpson rule.
- **The saddle at the origin.** $E = G = 1$, $F = 0$, $L = N = 0$, $M = 1$, so $W = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$, with eigenvalues $\pm 1$ and eigenvectors $(1, 1)$ and $(1, -1)$. The principal directions are the diagonals, and the coordinate directions, which are straight lines on the surface, have $k_n = 0$ by Euler's formula with $\theta = 45°$. At $(1, 1)$ we have $w^2 = 3$, $K = -1/w^4 = -1/9$ and $H = -uv/w^3 = -1/(3\sqrt 3)$.
- **Minimal surfaces.** The [helicoid](/ruled-surface/) and the [catenoid](/surface-of-revolution/) have $H = 0$ everywhere, so $k_2 = -k_1$ and $K = -k_1^2 \le 0$.
- **Developable surfaces.** Cylinders, cones and tangent developables have $K = 0$ everywhere, which is why they unroll onto the plane. Every [ruled surface](/ruled-surface/) has $K \le 0$.

## Where it is used

- **Surface quality in CAD.** Designers check a surface by plotting $K$, $H$ or the principal curvatures over it as a color map, and by drawing the principal directions. Small waves that the eye misses in shaded images show as bands in these plots.
- **Machining.** A ball-end cutter of radius $\rho$ can reach a concave region only where $\rho \le 1/k$ for the largest concave principal curvature, so the principal curvatures bound the tool size.
- **Sheet material.** Surfaces with $K = 0$ can be made from flat sheet metal, paper or fabric without stretch. Design tools test $K$ to find the regions where a part must be stretched or cut.
- **Physics and shape.** Soap films are minimal surfaces with $H = 0$. A bubble or a cell membrane under pressure has constant $H$. Curvature flows, which move each point along $n$ at a speed set by $H$, smooth surfaces and meshes.
- **Tessellation and meshing.** The curvature sets how fine a mesh must be: a chord of length $h$ on a curve of curvature $k$ deviates from the curve by about $k h^2 / 8$. Adaptive [tessellation](/surface-tessellation/) uses this to put more triangles where $k_1$ is large.
- **Mesh processing.** On a [polygon mesh](/polygon-mesh/) there are no derivatives, so $K$ is estimated by the angle defect at each vertex and $H$ by discrete Laplace operators. These estimates drive feature detection, remeshing and [simplification](/mesh-simplification/).
- **Rendering.** Line drawings of 3D models use the principal curvatures and directions to place ridge and valley lines and to orient hatching strokes.

## References
