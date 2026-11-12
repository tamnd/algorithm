---
tag: R4J4XX
kind: definition
slug: surface-of-revolution
name: Surface of revolution
area: graphics-and-signals/curves-and-surfaces
level: intro
summary: The surface swept by a plane profile curve as it turns about an axis in its plane. Meridians and parallels are its lines of curvature, and K = -r''/r when the profile is in arc length.
prereqs: [parametric-surface]
see_also: [ruled-surface, sweep-surface, nurbs, rational-bezier-curve, fundamental-forms, surface-curvature, surface-tessellation, parametric-curve]
sources:
  - book: isbn:9780132125895
    title: Manfredo P. do Carmo, Differential Geometry of Curves and Surfaces, Prentice-Hall, 1976
    locator: Section 2-2, Regular Surfaces (surfaces of revolution as regular surfaces), and Section 3-3, The Gauss Map in Local Coordinates (the curvature of a surface of revolution)
  - book: isbn:9783540615453
    title: Les Piegl and Wayne Tiller, The NURBS Book, second edition, Springer, 1997
    locator: Section 8.5, The Surface of Revolution (the NURBS surface from a profile curve and the rational quadratic circle)
---

A surface of revolution is the surface that a plane curve sweeps when it turns about a straight line in its plane. The curve is the profile, the line is the axis, and every point of the profile moves on a circle about the axis. Vases, bottles, wheels, the sphere, the torus and the cone are all surfaces of revolution, and a lathe cuts exactly this shape. The rotation gives the surface a simple geometry: the first fundamental form is diagonal and the curvature depends only on the profile.

## Definition

Put the axis on the $z$ axis and the profile in the $xz$ plane as $u \mapsto (r(u), 0, z(u))$ with $r(u) \ge 0$, for $u$ in an interval $I$. The surface of revolution is

$$S(u, v) = (r(u) \cos v,\ r(u) \sin v,\ z(u)), \qquad u \in I,\ v \in [0, 2\pi].$$

The $v$-curves are the parallels, circles of radius $r(u)$ at height $z(u)$. The $u$-curves are the meridians, copies of the profile turned by the angle $v$.

**Regularity.** $S_u = (r' \cos v, r' \sin v, z')$ and $S_v = (-r \sin v, r \cos v, 0)$, so $|S_u \times S_v| = r \sqrt{r'^2 + z'^2}$. The map is regular where $r > 0$ and the profile is regular. Where the profile meets the axis, $S_v = 0$. The set is still smooth there if the profile crosses the axis at a right angle, as at the poles of a sphere, and it has a cone point if not.

**First fundamental form.** $E = r'^2 + z'^2$, $F = 0$, $G = r^2$. So the meridians and the parallels cross at right angles everywhere. The arc length of a parallel is $2\pi r(u)$, and the area is

$$A = 2\pi \int_I r(u) \sqrt{r'(u)^2 + z'(u)^2}\, du,$$

which is Pappus's rule: the length of the profile times the length of the circle that its centroid travels.

**Curvature.** Take the unit normal $n = (-z' \cos v, -z' \sin v, r') / \sqrt{E}$, which is $S_u \times S_v / |S_u \times S_v|$ for $r > 0$. The [second fundamental form](/fundamental-forms/) is $L = (r' z'' - r'' z') / \sqrt{E}$, $M = 0$, $N = r z' / \sqrt{E}$. Since $F = M = 0$, the meridians and parallels are the lines of curvature, and the principal curvatures are

$$k_1 = \frac{L}{E} = \frac{r' z'' - r'' z'}{E^{3/2}}, \qquad k_2 = \frac{N}{G} = \frac{z'}{r \sqrt{E}}.$$

The first is the curvature of the profile as a plane curve. The second is the normal curvature of the parallel. So the [Gaussian curvature](/surface-curvature/) is

$$K = k_1 k_2 = \frac{z' (r' z'' - r'' z')}{r\, (r'^2 + z'^2)^2}.$$

If the profile is in arc length, $r'^2 + z'^2 = 1$, so $r' r'' + z' z'' = 0$ and $z'(r' z'' - r'' z') = r' z' z'' - r'' z'^2 = -r'' r'^2 - r'' z'^2 = -r''$. This gives $K = -r''/r$. The sign of $K$ is the sign of $-r''$: points where the profile bends toward the axis are elliptic, and points where it bends away are hyperbolic.

### Curvature from the profile

```pseudo id=main
REVOLUTION-K(r, r′, r″, z′, z″)
L1  if r = 0 then error "point on the axis"
L2  E ← r′² + z′²
L3  if E = 0 then error "stationary profile"
L4  δ ← r′ z″ − r″ z′
L5  return z′ δ / (r E²)
```

The routine needs the profile and its first two derivatives at one $u$, and costs a constant number of arithmetic operations. It uses only $+$, $-$, $\times$ and $/$, so it is exact on rational input. A grid of $m$ values of $u$ and $n$ values of $v$ needs $m$ profile evaluations, $n$ values of $\cos$ and $\sin$, and $2mn$ multiplications, because each grid point is $(r_i c_j, r_i s_j, z_i)$. These are exact counts in the real RAM model.

## Examples and non-examples

- **The sphere.** $r = R \cos u$, $z = R \sin u$ for $u \in [-\pi/2, \pi/2]$. This profile has speed $R$, and the formula gives $K = 1/R^2$ and $k_1 = k_2 = 1/R$ with the normal above, which points into the sphere. The area is $2\pi \int R \cos u \cdot R\, du = 4\pi R^2$.
- **The torus.** $r = R + a \cos u$, $z = a \sin u$ with $R > a > 0$. Then $K = \cos u / (a (R + a \cos u))$ and $H = (R + 2a \cos u) / (2a (R + a \cos u))$ with the normal into the tube. For $R = 3$, $a = 1$: on the outer equator $u = 0$, $K = 1/4$ and $H = 5/8$; on the inner equator $u = \pi$, $K = -1/2$ and $H = 1/4$; on the top circle $u = \pi/2$, $K = 0$ and $H = 1/2$. The area is $4\pi^2 R a$, which is $12\pi^2$ here.
- **The cylinder and the cone.** $r = 2$, $z = u$ gives $r' = r'' = 0$, so $K = 0$. $r = u$, $z = 2u$ gives $r'' = z'' = 0$, so $\delta = 0$ and $K = 0$. Both are also [ruled](/ruled-surface/) and developable. The cone is singular at $u = 0$, its apex, because the profile meets the axis at an angle that is not a right angle.
- **The catenoid.** The profile $r = \cosh z$, as $(\cosh u, 0, u)$, gives $k_1 = -1/\cosh^2 u$ and $k_2 = 1/\cosh^2 u$, so $H = 0$ and $K = -1/\cosh^4 u$. It is the only minimal surface of revolution other than the plane.
- **Exact rational points.** With $\cos v = (1 - t^2)/(1 + t^2)$ and $\sin v = 2t/(1 + t^2)$, a rational profile gives rational points: the torus point with $\cos u = 3/5$, $\sin u = 4/5$, $\cos v = 0$, $\sin v = 1$ is $(0, 18/5, 4/5)$, and it satisfies $(\sqrt{x^2 + y^2} - 3)^2 + z^2 = 1$ exactly. This is why a [NURBS](/nurbs/) surface can represent a surface of revolution exactly: the profile is multiplied by a [rational quadratic](/rational-bezier-curve/) circle, which needs weights below 1, and no polynomial patch can trace a circle.
- **Non-example: a profile that crosses the axis.** If $r(u)$ changes sign, the two sides of the profile turn onto each other and the surface covers some parallels twice. Take $r \ge 0$, or cut the profile at the axis.
- **Non-example: the enclosed region.** The sphere of radius $R$ has area $4\pi R^2$; the ball it bounds has volume $4\pi R^3 / 3$. The surface is the boundary only. The volume of the region comes from a second rule of Pappus, $2\pi$ times the area of the profile region times the distance of its centroid from the axis, and it is a different quantity.
- **Non-example: a twisted profile.** If the profile does not lie in a plane through the axis, the turned copies still sweep a surface, but its meridians are not plane curves, and the formulas above do not apply. A helical [sweep](/sweep-surface/) is the usual way to model such a shape.

## Related definitions

- [Parametric curve](/parametric-curve/): the profile. The curvature $k_1$ of the meridian is its plane curvature.
- [Fundamental forms](/fundamental-forms/) and [surface curvature](/surface-curvature/): the general definitions. For a surface of revolution both forms are diagonal, so the coordinate lines are the lines of curvature.
- [Ruled surface](/ruled-surface/): the cylinder, the cone and the hyperboloid of one sheet are both ruled and surfaces of revolution.
- [Sweep surface](/sweep-surface/): a profile moved along a path. A surface of revolution is the sweep along a circle with the frame that turns with it.
- [NURBS](/nurbs/): the exact representation in CAD systems.

## References
