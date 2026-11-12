---
tag: NZWWN5
kind: definition
slug: parametric-surface
name: Parametric surface
area: graphics-and-signals/curves-and-surfaces
level: intro
summary: A map S(u, v) from a domain of the plane into space. It is regular where S_u and S_v are independent; there the normal is S_u x S_v and the image is locally a smooth surface.
prereqs: [parametric-curve]
see_also: [implicit-surface, tensor-product-surface, bezier-patch, bezier-triangle, fundamental-forms, surface-curvature, surface-tessellation, polygon-mesh]
sources:
  - book: isbn:9780132125895
    title: Manfredo P. do Carmo, Differential Geometry of Curves and Surfaces, Prentice-Hall, 1976
    locator: Section 2-2, Regular Surfaces, Inverse Images of Regular Values, Section 2-3, Change of Parameters, and Section 2-4, The Tangent Plane
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: Chapter 14, Tensor Product Patches, and Chapter 19, W. Boehm, Differential Geometry II
  - book: isbn:9783540615453
    title: Les Piegl and Wayne Tiller, The NURBS Book, second edition, Springer, 1997
    locator: Chapter 8, Construction of Common Surfaces (bilinear surfaces, general cylinders, ruled surfaces and surfaces of revolution as parametric forms)
---

A parametric surface is a map $S(u, v)$ that sends each point of a region of the $(u, v)$ plane to a point of space. The image is the surface and the map is its parametrization. Most surfaces in CAD and in rendering are given in this form: [Bézier patches](/bezier-patch/), [Bézier triangles](/bezier-triangle/), B-spline and [NURBS](/nurbs/) surfaces, [surfaces of revolution](/surface-of-revolution/) and [sweeps](/sweep-surface/). A parametric form makes it easy to generate points, for example to [tessellate](/surface-tessellation/) the surface, but hard to test if a given point is on the surface. An [implicit surface](/implicit-surface/) $f(x, y, z) = 0$ has the opposite trade-off.

## Definition

Let $D \subset \mathbb{R}^2$ be a region, usually a rectangle $[a, b] \times [c, d]$ or a triangle. A parametric surface is a map

$$S : D \to \mathbb{R}^3, \qquad S(u, v) = (x(u, v),\ y(u, v),\ z(u, v)),$$

whose coordinate functions have continuous partial derivatives up to the order that the application needs (at least the first). Write $S_u = \partial S / \partial u$ and $S_v = \partial S / \partial v$.

- **Regular point.** $(u, v)$ is a regular point when $S_u$ and $S_v$ are linearly independent, which means $S_u \times S_v \neq 0$ (see the [cross product](/cross-product/)). The parametrization is regular when every point of $D$ is regular.
- **Tangent plane and normal.** At a regular point the tangent plane is the plane through $S(u, v)$ spanned by $S_u$ and $S_v$. The unit normal is $n = S_u \times S_v / |S_u \times S_v|$. Its sign depends on the order of $u$ and $v$: swapping them turns $n$ into $-n$.
- **Iso-parameter curves.** For fixed $v_0$ the map $u \mapsto S(u, v_0)$ is a [parametric curve](/parametric-curve/) on the surface, a $u$-curve. The $v$-curves are defined in the same way. The tangent of the $u$-curve is $S_u$.
- **Reparametrization.** If $\varphi : D' \to D$ is a bijection with continuous derivatives and a Jacobian determinant that is never zero, then $S \circ \varphi$ has the same image and the same tangent planes. The derivatives change by the chain rule, and the normal is multiplied by the sign of the Jacobian. Properties that do not depend on the parametrization, such as area and [curvature](/surface-curvature/), are the geometry of the surface.
- **Regular surface.** In differential geometry a regular surface is a set that is covered by regular parametrizations that are one to one and have continuous inverses (do Carmo, Section 2-2). A single parametrization can fail at a point where the set is smooth (see the sphere below), and a regular parametrization can cross itself, so the two notions are different.

Regularity is what the rest of the theory needs. At a regular point the map is locally one to one (by the inverse function theorem applied to a pair of coordinates), the [fundamental forms](/fundamental-forms/) are defined, and the surface near the point is the graph of a function over its tangent plane.

**Cost model.** For the patches of this area the cost of one point is the cost of one evaluation of $S$. A polynomial patch of degree $(m, n)$ in [Bernstein form](/bernstein-polynomials/) has $(m + 1)(n + 1)$ control points and costs $O(mn(m + n))$ operations per point by de Casteljau, or $O(mn)$ by [Horner's rule](/horner-rule/) in the monomial basis. These are worst case operation counts in the real RAM model, for one point.

## Examples and non-examples

- **The saddle.** $S(u, v) = (u, v, uv)$ on $\mathbb{R}^2$. Then $S_u = (1, 0, v)$, $S_v = (0, 1, u)$ and $S_u \times S_v = (-v, -u, 1)$, which is never zero, so the map is regular everywhere. At $(u, v) = (1, 2)$ the point is $(1, 2, 2)$, the normal direction is $(-2, -1, 1)$ and the tangent plane is $-2x - y + z = -2$. The same set is the [bilinear patch](/bilinear-interpolation/) of the four corners $(0, 0, 0)$, $(1, 0, 0)$, $(0, 1, 0)$, $(1, 1, 1)$ on $[0, 1]^2$, and the [ruled surface](/ruled-surface/) of the lines $(u, 0, 0) + v\,(0, 1, u)$.
- **Graphs.** Every function $z = f(x, y)$ with continuous derivatives gives the regular parametrization $S(u, v) = (u, v, f(u, v))$, with $S_u \times S_v = (-f_u, -f_v, 1)$. Height fields in terrain rendering are of this type.
- **The sphere, two ways.** The latitude and longitude map $S(u, v) = (\cos u \cos v,\ \cos u \sin v,\ \sin u)$ on $[-\pi/2, \pi/2] \times [0, 2\pi]$ covers the unit sphere, but $S_v = (-\cos u \sin v, \cos u \cos v, 0)$ is zero at the poles $u = \pm \pi/2$. The poles are singular points of the map, not of the sphere. The inverse stereographic map $S(u, v) = (2u,\ 2v,\ u^2 + v^2 - 1) / (1 + u^2 + v^2)$ is regular on all of $\mathbb{R}^2$ and covers the sphere except the north pole $(0, 0, 1)$. It is rational, so rational $(u, v)$ give rational points: $(u, v) = (1/2, 0)$ gives $(4/5, 0, -3/5)$. A [rational Bézier](/rational-bezier-curve/) or [NURBS](/nurbs/) patch can represent the sphere exactly for this reason, and a polynomial patch cannot.
- **Surfaces made from curves.** A [surface of revolution](/surface-of-revolution/) $(r(u) \cos v, r(u) \sin v, z(u))$, a [ruled surface](/ruled-surface/) $a(u) + v\,(b(u) - a(u))$ and a [sweep surface](/sweep-surface/) are all parametric surfaces built from one or two curves.
- **Non-example: the cone at its apex.** $S(u, v) = (u \cos v, u \sin v, u)$ has $S_v = 0$ at $u = 0$, and the set is not smooth there: no plane is tangent to the cone at the apex. A parametrization can be singular for two different reasons, a bad map (the sphere poles) or a bad set (the apex), and the derivative test alone does not tell them apart.
- **Non-example: a regular map that crosses itself.** The map of the plane onto a torus, $((3 + \cos u) \cos v, (3 + \cos u) \sin v, \sin u)$, is regular but not one to one, because it repeats with period $2\pi$ in $u$ and in $v$. On the domain $[0, 2\pi)^2$ it is one to one. A [sweep](/sweep-surface/) of a large circle along a tightly bent spine is regular in most places but crosses itself, so the image is not a regular surface.
- **Non-example: a polygon mesh.** A [polygon mesh](/polygon-mesh/) is a piecewise linear surface. Each face has a linear parametrization, but the normal jumps across edges, so the mesh as a whole is not a parametric surface with continuous derivatives. A [tessellation](/surface-tessellation/) approximates a parametric surface by such a mesh.

## Related definitions

- [Parametric curve](/parametric-curve/): the one-parameter case. Each iso-parameter line of a surface is one.
- [Implicit surface](/implicit-surface/): the zero set of $f(x, y, z)$. A parametric surface answers "give me points" in one evaluation, and an implicit surface answers "is this point inside" in one evaluation. The sphere has both forms. A general polynomial patch also has an implicit equation, but of much higher degree than the patch, so in practice systems keep one form and do not convert.
- [Tensor-product surface](/tensor-product-surface/): the parametric surfaces whose coordinates are sums of products of a basis in $u$ and a basis in $v$. [Bézier patches](/bezier-patch/) and B-spline surfaces are the main examples. A [Bézier triangle](/bezier-triangle/) uses a triangular domain instead.
- [Fundamental forms](/fundamental-forms/) and [surface curvature](/surface-curvature/): the metric and the bending of a regular parametric surface, from the first and second derivatives of $S$.
- [Surface tessellation](/surface-tessellation/) and [smooth surface from a control mesh](/surface-from-control-mesh/): the problems of going from a parametric surface to a mesh, and from a mesh back to a smooth surface.

## References
