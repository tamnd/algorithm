---
tag: DKHXH7
kind: definition
slug: implicit-surface
name: Implicit surface
aliases:
- level set surface
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: The set of points where a function of space takes one value, f(x) = c. Where the gradient is not zero there, it is a smooth surface with normal along the gradient.
prereqs: [gradient]
see_also: [signed-distance-function, isosurface-extraction, parametric-surface, surface-curvature, level-set-method, sphere-tracing, poisson-surface-reconstruction, polygon-mesh]
sources:
  - book: isbn:9781558602335
    title: Jules Bloomenthal (editor), with Chandrajit Bajaj, Jim Blinn, Marie-Paule Cani, Alyn Rockwood, Brian Wyvill and Geoff Wyvill, Introduction to Implicit Surfaces, Morgan Kaufmann, 1997
    locator: Chapter 1, The Geometry of Implicit Surfaces, Chapter 4, Surface Tiling, and Chapter 6, Blending
  - paper: doi:10.1145/357306.357310
    title: James F. Blinn, A generalization of algebraic surface drawing, ACM Transactions on Graphics 1(3), 235 to 256, 1982
    locator: the definition F(x, y, z) = 0, and the sums of Gaussian densities (blobby molecules)
  - paper: doi:10.1016/j.cagd.2005.06.005
    title: Ron Goldman, Curvature formulas for implicit curves and surfaces, Computer Aided Geometric Design 22(7), 632 to 658, 2005
    locator: the formulas for the Gaussian and mean curvature of an implicit surface in terms of the gradient and the Hessian
---

An implicit surface is the set of points $x$ in space where a function $f : \mathbb{R}^3 \to \mathbb{R}$ has one given value, $f(x) = c$; usually $c = 0$. The function does not list the points of the surface. It only tells, for each point of space, on which side of the surface the point is, by the sign of $f(x) - c$. That makes the inside test, blends and Boolean operations easy, and it makes it hard to list points on the surface, which is the opposite of a [parametric surface](/parametric-surface/). A [signed distance function](/signed-distance-function/) is the special case where $|f(x)|$ is the distance to the surface. Programs draw implicit surfaces by [isosurface extraction](/isosurface-extraction/) into a [polygon mesh](/polygon-mesh/), or by root finding along rays.

## Definition

**Level set.** Let $U \subseteq \mathbb{R}^3$ be open, $f : U \to \mathbb{R}$ continuous, and $c \in \mathbb{R}$. The level set, or isosurface, of $f$ at $c$ is
$$S = f^{-1}(c) = \{x \in U : f(x) = c\}.$$
Replacing $f$ by $f - c$ gives $c = 0$, so the rest of this page uses the zero set $S = \{f = 0\}$. This page takes $f < 0$ as the inside and $f > 0$ as the outside, as on the signed distance page; some authors use the opposite sign, and blobby models often use $f > c$ for the inside.

**Regular surface.** Let $f$ be continuously differentiable. A value is regular when the [gradient](/gradient/) $\nabla f$ is not zero at any point of $S$. If 0 is a regular value, then by the implicit function theorem each point of $S$ has a neighborhood in which $S$ is the graph of a smooth function of two of the coordinates. So $S$ is a smooth 2-manifold without border, and it is a closed subset of $U$. If $U = \mathbb{R}^3$ and $S$ is bounded, then $S$ is compact, it is the boundary of the solid $\{f \le 0\}$, and it is orientable.

**Normal and curvature.** At a regular point, the unit normal that points to the outside is
$$n(x) = \frac{\nabla f(x)}{\lVert \nabla f(x) \rVert}.$$
With $H_f$ the Hessian matrix of second derivatives, the mean curvature and the Gaussian curvature are, for a twice differentiable $f$,
$$\kappa_H = \tfrac12 \operatorname{div}\!\left(\frac{\nabla f}{\lVert \nabla f \rVert}\right), \qquad \kappa_G = -\frac{1}{\lVert \nabla f \rVert^4} \det \begin{pmatrix} H_f & \nabla f \\ \nabla f^{\mathsf T} & 0 \end{pmatrix}.$$
These are the formulas collected by Goldman; with this sign of $n$ a sphere has $\kappa_H = 1/r > 0$. [Surface curvature](/surface-curvature/) gives the same values from a parametrization.

**Scaling.** The set $S$ does not change if $f$ is multiplied by a positive function, so many functions describe the same surface. The values of $f$ away from $S$ have no meaning unless more is asked, such as $\lVert \nabla f \rVert = 1$ for a signed distance function. Near a regular point, the distance to $S$ is about $|f(x)| / \lVert \nabla f(x) \rVert$, a first order estimate that many algorithms use.

**Operations.** With the sign convention above, for two functions $f$ and $g$ with solids $A = \{f \le 0\}$ and $B = \{g \le 0\}$: $\min(f, g)$ gives $A \cup B$, $\max(f, g)$ gives $A \cap B$, and $-f$ gives the closure of the complement of $A$. The new zero sets are exact, but $\min$ and $\max$ have creases where $f = g$, and the result of $\min$ or $\max$ of two signed distance functions is in general only a bound on the distance. Smooth blends replace $\min$ by a smooth function of $f$ and $g$.

**Sampled functions.** In imaging and simulation, $f$ is known only at the nodes of a grid, for example the density values of a CT scan. The surface is then the level set of an interpolant, such as the trilinear interpolant in each cell or the piecewise linear one on tetrahedra, and the choice of interpolant decides the surface between the nodes. This is the input of [marching cubes](/marching-cubes/).

## Examples and non-examples

**Implicit surfaces.**

- **Sphere.** $f(x) = \lVert x - m \rVert^2 - r^2$. Then $\nabla f = 2 (x - m)$, which is not zero on $S$, so 0 is regular. The Hessian is $2I$, and $\det \begin{pmatrix} 2I & g \\ g^{\mathsf T} & 0 \end{pmatrix} = 8 \cdot (-g^{\mathsf T} g / 2) = -4 \lVert g \rVert^2$ for $g = \nabla f$, so $\kappa_G = 4 \lVert g \rVert^2 / \lVert g \rVert^4 = 1 / r^2$, as it must be.
- **Plane.** $f(x) = u \cdot x - d$ with $u \ne 0$. It has $\kappa_H = \kappa_G = 0$, and for a unit $u$ it is a signed distance function.
- **Torus.** $f(x, y, z) = (x^2 + y^2 + z^2 + R^2 - r^2)^2 - 4 R^2 (x^2 + y^2)$ for $R > r > 0$, a polynomial of degree 4. Its zero set is the torus with tube radius $r$ around a circle of radius $R$, and 0 is a regular value. The sign is negative inside the tube.
- **Quadrics and algebraic surfaces.** $f(x) = x^{\mathsf T} A x + b^{\mathsf T} x + c$ gives ellipsoids, hyperboloids and paraboloids; any polynomial $f$ gives an algebraic surface, of degree equal to the degree of $f$.
- **Blobby objects.** Blinn modeled molecules with $f(x) = T - \sum_i b_i e^{-a_i \lVert x - m_i \rVert^2}$, a threshold minus a sum of Gaussian bumps. Two spheres that come close merge smoothly into one surface. Metaballs and soft objects use bumps with bounded support instead.
- **Fitted surfaces.** [Poisson surface reconstruction](/poisson-surface-reconstruction/) fits a smooth indicator function to oriented points and takes a level set; radial basis function fits are another method of the same kind.

**Non-examples, or not regular.**

- $f(x) = (\lVert x \rVert^2 - 1)^2$. The zero set is the unit sphere, but $\nabla f = 0$ on it, so 0 is not a regular value. The function does not change sign at the surface, so the inside test, the normal and sign-based root finding all fail, although the set is a fine surface.
- The cone $f(x, y, z) = x^2 + y^2 - z^2$. The gradient is zero at the origin, which is on $S$, and near the origin the set is two cones that touch at a point. It is not a 2-manifold there.
- $f(x, y, z) = x y$. The zero set is two planes that cross along the $z$ axis, which is not a 2-manifold on the axis.
- $f(x) = \lVert x \rVert^2 + 1$. The zero set is empty. A level set can be empty, or have many parts, with no warning from the formula.
- A [parametric surface](/parametric-surface/) $s(u, v)$, such as a Bézier patch. It is given by a map, not by an equation; turning it into an implicit equation (implicitization) is possible for polynomial patches but gives polynomials of high degree.

## Related definitions

- **[Signed distance function](/signed-distance-function/).** An implicit function with $|f|$ equal to the distance to $S$; it has $\lVert \nabla f \rVert = 1$ where it is differentiable, which lets [sphere tracing](/sphere-tracing/) take safe steps along a ray.
- **[Isosurface extraction](/isosurface-extraction/).** The problem of building a mesh of a level set from samples on a grid, solved by [marching cubes](/marching-cubes/), [marching tetrahedra](/marching-tetrahedra/) and [dual contouring](/dual-contouring/).
- **[Level set method](/level-set-method/).** Moves a surface in time by evolving the implicit function by a partial differential equation, so that changes of topology need no special care.
- **[Ray marching](/ray-marching/).** Finds the first zero of $f$ along a ray by steps and a sign test; for a general $f$ the step must be small, or bounds from [interval arithmetic](/interval-arithmetic/) are needed.
- **Implicit curve.** The planar version $\{f(x, y) = 0\}$, whose extraction from a grid is [marching squares](/marching-squares/).

## References
