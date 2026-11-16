---
tag: 6AAEHY
kind: definition
slug: limit-surface
name: Limit surface
aliases:
- friction limit surface
area: robotics/grasping-and-manipulation
level: advanced
summary: The boundary of the set of friction wrenches that a planar support can apply to an object sliding on it, often approximated by an ellipsoid.
prereqs: [wrench, rigid-body-twist, convex-set]
see_also: [quasi-static-pushing, mason-voting-theorem, friction-cone, instant-center-of-velocity, support-function, grasp-wrench-space, fixture-planning, numerical-integration]
sources:
  - paper: doi:10.1016/0043-1648(91)90104-3
    title: Suresh Goyal, Andy Ruina and Jim Papadopoulos, Planar sliding with dry friction. Part 1. Limit surface and moment function, Wear 143(2), 307-330, 1991
    locator: the whole paper (the limit surface of a planar support, its convexity, and the twist as a normal to it)
  - paper: "Sukhan Lee and Mark R. Cutkosky, Fixture planning with friction, ASME Journal of Engineering for Industry 113(3), 320-327, 1991"
    locator: the whole paper (the ellipsoid approximation of the limit surface)
  - paper: doi:10.1109/IROS.1992.587370
    title: Kevin M. Lynch, Hitoshi Maekawa and Kazuo Tanie, Manipulation and active sensing by pushing using tactile feedback, IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 1992
    locator: the whole paper (pushing with an ellipsoidal limit surface, with the motion of the object in closed form)
  - book: isbn:9780262133968
    title: Matthew T. Mason, Mechanics of Robotic Manipulation, MIT Press, 2001
    locator: Chapter 6, Section 6.6 (planar sliding)
---

The limit surface of an object that slides on a flat support is a closed surface in the three-dimensional space of planar [wrenches](/wrench/) $(m, f_x, f_y)$. It bounds the set of all friction wrenches that the support can apply to the object. When the object slides with a given [twist](/rigid-body-twist/), the friction wrench is on the surface, and the twist is normal to the surface there. This page defines the surface. [Quasi-static pushing](/quasi-static-pushing/) is the model of motion that uses it to predict how a pushed object moves, and [Mason's voting theorem](/mason-voting-theorem/) gives the sense of rotation of a pushed object without it.

## Definition

An object lies on a horizontal plane. The support presses on it with a pressure distribution $p(r) \ge 0$ over the contact region $R$, with total normal force $N = \int_R p\, dA$. Friction is Coulomb friction with coefficient $\mu$, the same in every direction. Moments are taken about a reference point in the plane, usually the center of pressure. A wrench is written moment first: $w = (m, f_x, f_y)$.

When the object moves with the planar twist $\xi = (\omega, v_x, v_y)$, the point $r$ of the support region has the velocity $v(r) = (v_x - \omega r_y,\ v_y + \omega r_x)$. Where $v(r) \ne 0$, the support applies the friction force $-\mu\, p(r)\, v(r) / \lvert v(r) \rvert$ per unit area. The friction wrench of the motion is

$$w(\xi) = \int_R \mu\, p(r) \left( -\operatorname{cross}(r, \hat v(r)),\ -\hat v(r) \right) dA, \qquad \hat v = v / \lvert v \rvert,$$

with $\operatorname{cross}(a, b) = a_x b_y - a_y b_x$. Over the points where $v(r) = 0$, a set of measure zero for a twist that is not zero, the friction force can be anything in the friction disc, so it does not change the integral.

The *limit surface* is the set $\{w(\xi) : \xi \ne 0\}$. The wrench $w(\xi)$ does not change when $\xi$ is multiplied by a positive number, so the surface is the image of the sphere of twist directions. The set it bounds contains every friction wrench that the support can apply: the wrenches strictly inside it are the ones the support can apply without slipping.

The following properties are theorems (Goyal, Ruina and Papadopoulos 1991).

- **Convex.** The limit surface is the boundary of a convex set that contains the origin.
- **Symmetric.** $w(-\xi) = -w(\xi)$, so the surface is symmetric about the origin.
- **Maximum dissipation.** For every motion $\xi$, the wrench $w(\xi)$ maximizes the dissipated power $-\xi \cdot w$ over all wrenches $w$ in the set. So $-\xi$ is an outward normal of the limit surface at $w(\xi)$. Many authors draw the surface for the wrench $-w$ that a pusher must apply to keep the object sliding; for that wrench the twist $\xi$ itself is the outward normal. Where the surface is smooth, the normal gives the direction of the twist from the wrench.
- **Facets and vertices.** If the support is a finite set of points, the surface has flat facets and edges. The twists that rotate about a support point map to a whole set of wrenches, a facet of the surface, because the friction at that point can be anything in its disc.

The support function of the set is $h(\xi) = \max_w (-\xi \cdot w) = \int_R \mu\, p(r)\, \lvert v(r) \rvert\, dA$, the frictional power. It is a convex, positively homogeneous function of $\xi$, and the set bounded by the limit surface is the set it defines.

**The ellipsoid approximation.** Lee and Cutkosky (1991) replace the surface by the ellipsoid

$$\left(\frac{f_x}{f_{\max}}\right)^2 + \left(\frac{f_y}{f_{\max}}\right)^2 + \left(\frac{m}{m_{\max}}\right)^2 = 1,$$

with $f_{\max} = \mu N$, the friction force of a pure translation, and $m_{\max} = \mu \int_R p(r)\, \lvert r \rvert\, dA$, the friction moment of a pure rotation about the reference point. The normal of the ellipsoid gives the twist $\xi \propto (m / m_{\max}^2,\ f_x / f_{\max}^2,\ f_y / f_{\max}^2)$ in closed form. The approximation is a heuristic: it is exact at the two kinds of motion that fix $f_{\max}$ and $m_{\max}$, and in between its error depends on the pressure distribution.

## Examples and non-examples

**A uniform disc.** A disc of radius $\rho$ with uniform pressure $p = N / (\pi \rho^2)$, with moments about its center. Pure translation gives $f = \mu N$ opposite to the velocity and $m = 0$. Pure rotation about the center gives

$$m_{\max} = \mu \int_0^\rho \frac{N}{\pi \rho^2}\, r \cdot 2\pi r\, dr = \frac{2}{3} \mu N \rho.$$

By symmetry the surface is a surface of revolution about the moment axis. It passes through $(\pm \frac{2}{3}\mu N \rho, 0, 0)$ and through the circle of radius $\mu N$ in the plane $m = 0$. The ellipsoid with these axes is close to it but not equal to it. With $\mu = N = \rho = 1$, a rotation about a point on the rim gives the friction wrench $(m, f) \approx (-0.283,\ 0.849)$ in size, by numerical integration on a 400 by 400 polar grid (a measurement). The left side of the ellipsoid equation is then 0.90, not 1, so the exact surface lies about 5 percent inside the ellipsoid in that direction.

**Two support points.** A bar that rests on two points, each with normal force $N/2$, at $(\pm a, 0)$. The friction force at each point can be any force of size at most $\mu N / 2$, so the set of friction wrenches is the Minkowski sum of two flat discs in wrench space, one for each point. Its boundary, the limit surface, has a flat facet for each sense of rotation about each support point, four in all, joined by curved pieces. It is convex but not smooth, and the ellipsoid misses its edges.

**Non-example: the friction cone.** The [friction cone](/friction-cone/) of a point contact bounds the forces at one contact as a function of the normal force. The limit surface bounds the total wrench over a support region for a fixed normal load. The first lives in the space of forces at a point, the second in the space of planar wrenches.

**Non-example: anisotropic friction.** If the friction coefficient depends on the direction of sliding, the friction force at a point is no longer opposite to the velocity, and the definition above does not apply as written. A limit surface can still be defined, but the properties above need other proofs.

## Related definitions

- **Moment function.** The moment of friction about the reference point, as a function of the center of rotation of the motion. Goyal, Ruina and Papadopoulos study it together with the limit surface.
- **Center of rotation.** A planar twist with $\omega \ne 0$ is a rotation about the point $(-v_y / \omega,\ v_x / \omega)$, its [instant center](/instant-center-of-velocity/). The twist directions are the centers of rotation together with the pure translations, so the limit surface can be drawn as a function of the center of rotation.
- **Center of friction.** The point $\int \mu\, p\, r\, dA / \int \mu\, p\, dA$. With uniform $\mu$ it is the center of pressure. Under a pure translation the friction force acts through it. It is the point that [Mason's voting theorem](/mason-voting-theorem/) uses.
- **Wrench space of a grasp.** The [grasp wrench space](/grasp-wrench-space/) is the set of wrenches that fingers can apply. A limit surface is the same kind of object for a distributed support.

## References
