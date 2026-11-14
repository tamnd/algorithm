---
tag: 1K4XZJ
kind: definition
slug: silhouette-curve-of-a-surface
name: Silhouette curve of a surface
aliases:
- contour generator
- surface silhouette
area: cad/surface-interrogation-and-design
level: core
summary: The curve on a surface where the normal is perpendicular to the view or pull direction, computed as an intersection and used for drawings, draft and parting lines.
prereqs: [parametric-surface, implicit-surface]
see_also: [silhouette-edge, isophote, parting-line-generation, draft-angle-analysis, hidden-line-removal, surface-surface-intersection, fundamental-forms, pinhole-camera-model]
sources:
  - book: isbn:9780521632515
    title: Roberto Cipolla and Peter Giblin, Visual Motion of Curves and Surfaces, Cambridge University Press, 2000
    locator: Chapter 3, Views of curves and surfaces (the contour generator and the apparent contour of a smooth surface; general locator inside the chapter)
  - paper: doi:10.1068/p130321
    title: Jan J. Koenderink, What does the occluding contour tell us about solid shape?, Perception 13(3), 321 to 330, 1984
    locator: the whole paper (the theorem that relates the curvature of the outline to the Gaussian curvature of the surface)
  - paper: doi:10.1145/344779.345074
    title: Aaron Hertzmann and Denis Zorin, Illustrating smooth surfaces, Proceedings of SIGGRAPH 2000, 517 to 526, 2000
    locator: the part on the contour generator of a smooth surface as the zero set of the normal times the vector from the eye (general locator)
---

The silhouette curve of a surface, also called its contour generator, is the set of points where a line of sight touches the surface. For a parallel view along a direction $d$ it is where the normal is perpendicular to $d$, and for an eye at a point $e$ it is where the normal is perpendicular to the line from the eye. In a picture, the image of this curve is the outline of the smooth part of the surface. In molding, the pull direction takes the place of the view direction, and the silhouette is where the draft is zero, so it is the natural candidate for the parting line.

## Definition

Let $x(u, v)$ be a regular [parametric surface](/parametric-surface/) on a domain $D$, of class $C^2$, with normal $n = x_u \times x_v$ and unit normal $N = n / |n|$.

**Parallel view.** For a view direction $d \ne 0$, put $g(u, v) = n(u, v) \cdot d$. The *silhouette* for $d$ is

$$C_d = \{\, x(u, v) : g(u, v) = 0 \,\}.$$

**Central view.** For an eye $e$ that is not on the surface, put $g_e(u, v) = n(u, v) \cdot (x(u, v) - e)$. The *silhouette* for $e$ is $C_e = \{ x(u, v) : g_e(u, v) = 0 \}$. A point with $N \cdot (e - x) > 0$ faces the eye, a point with $N \cdot (e - x) < 0$ faces away, and the silhouette lies between the two parts.

**Implicit surfaces.** For an [implicit surface](/implicit-surface/) $F = 0$ with $\nabla F \ne 0$, the normal is $\nabla F$, and the silhouette is the intersection of the surface with the surface $\nabla F \cdot d = 0$, or with $\nabla F(x) \cdot (x - e) = 0$ for an eye. For a polynomial $F$ of degree $m$, these have degree $m - 1$ and $m$. For a polynomial patch of degree $p$ in $u$ and $q$ in $v$, $n$ has degree at most $2p - 1$ in $u$ and $2q - 1$ in $v$, so $C_d$ is the image of a plane algebraic curve $g = 0$ in the domain. In both cases the silhouette is computed by an intersection method.

The *apparent contour*, or outline, is the image of the silhouette under the projection along $d$, or from $e$.

**Regular points.** The zero sets of $n \cdot d$ and $N \cdot d$ are the same, and at a zero, $\nabla (n \cdot d) = |n| \, \nabla (N \cdot d)$. At a point of $C_d$, the vector $d$ is tangent, so $d = a x_u + b x_v$. With the coefficients $h_{11} = -N_u \cdot x_u$, $h_{12} = -N_u \cdot x_v = -N_v \cdot x_u$ and $h_{22} = -N_v \cdot x_v$ of the [second fundamental form](/fundamental-forms/) $\mathrm{II}$,

$$\nabla (N \cdot d) = (N_u \cdot d, \; N_v \cdot d) = -\begin{pmatrix} h_{11} & h_{12} \\ h_{12} & h_{22} \end{pmatrix} \begin{pmatrix} a \\ b \end{pmatrix}.$$

So the gradient vanishes exactly when $d$ is in the kernel of the second fundamental form, $\mathrm{II}(d, \cdot) = 0$. That needs $h_{11} h_{22} - h_{12}^2 = 0$, so the Gaussian curvature is $0$ at the point. Away from such points, the implicit function theorem shows that $C_d$ is a regular $C^1$ curve. The same holds for $C_e$, with $x - e$ in place of $d$, because $\partial_u (N \cdot (x - e)) = N_u \cdot (x - e) + N \cdot x_u = N_u \cdot (x - e)$.

**Tangent of the silhouette.** Along $C_d$ with unit tangent $t$, $N \cdot d = 0$, so $0 = dN(t) \cdot d = -\mathrm{II}(t, d)$. The tangent of the silhouette is *conjugate* to the view direction. If $\mathrm{II}(d, d) \ne 0$, then $t$ is not parallel to $d$, so the projection along $d$ maps $t$ to a vector that is not zero, and the outline is a regular curve at that point. Where $\mathrm{II}(d, d) = 0$, the line of sight is an asymptotic direction, $t$ can be parallel to $d$, and the outline can have a cusp or end there.

**Curvature of the outline.** Koenderink proved that, at a point of the silhouette, the Gaussian curvature is a positive multiple of the product of the curvature of the outline and the normal curvature of the surface along the line of sight. So at a visible point, where that normal curvature is not negative, a convex part of the outline comes from a part of the surface with positive Gaussian curvature, and a concave part from negative curvature (cited, not proved here).

## Examples and non-examples

- **Sphere, parallel view.** For the sphere $|x| = r$ about the origin, $n$ is parallel to $x$, and $C_d$ is the great circle $x \cdot d = 0$.
- **Sphere, central view.** For an eye at distance $D > r$ from the center, $x \cdot (x - e) = 0$ gives $x \cdot e = r^2$, the small circle of radius $r \sqrt{1 - r^2 / D^2}$. It tends to the great circle as $D \to \infty$, and the eye sees less than half of the sphere.
- **Cylinder, side view.** For the cylinder $y^2 + z^2 = 1$ seen along $d = (0, 0, 1)$, $n = (0, y, z)$ and $C_d$ is the two lines $z = 0$, $y = \pm 1$.
- **Cylinder, end view (non-example of a curve).** Seen along its axis $d = (1, 0, 0)$, every normal is perpendicular to $d$, so the whole cylinder is its own silhouette. Here the Gaussian curvature is $0$ and $d$ is in the kernel of $\mathrm{II}$ at every point, the case that the regularity test excludes.
- **Torus, top view.** For the torus $x = ((R + r \cos \varphi) \cos \theta, (R + r \cos \varphi) \sin \theta, r \sin \varphi)$ with $R > r$, the unit normal is $N = (\cos \varphi \cos \theta, \cos \varphi \sin \theta, \sin \varphi)$. Along the axis $d = (0, 0, 1)$, $N \cdot d = \sin \varphi = 0$ gives the outer and the inner equator, two circles.
- **Torus, side view (a singular point).** Along $d = (1, 0, 0)$, $N \cdot d = \cos \varphi \cos \theta = 0$ gives the two meridian circles $\theta = \pm \pi/2$ and the top and bottom circles $\varphi = \pm \pi/2$. They cross at four points, where the gradient $(-\sin \varphi \cos \theta, -\cos \varphi \sin \theta)$ is zero. These points are on the circles of zero Gaussian curvature, and $d$ is the direction of the circle there, which is in the kernel of $\mathrm{II}$.
- **Mold, pull direction.** For a sphere pulled along $d$, the silhouette is the equator, which is the parting line of a mold in two halves. The [draft angle](/draft-angle-analysis/) of a point is $90^\circ$ minus the angle between $N$ and $d$, so the silhouette is the set of points with zero draft.
- **Non-example, edges.** The boundary curves of a patch and the sharp edges between patches can be part of the outline of a picture, but they are not on the silhouette curve, which is defined only on the smooth part of the surface. The [silhouette edges](/silhouette-edge/) of a polygon mesh are the discrete counterpart, where the faces on the two sides of an edge face the eye and face away.

## Related definitions

- **Isophote.** The [isophote](/isophote/) of level $0$ for the light direction $d$ is the silhouette for the parallel view along $d$.
- **Apparent contour.** The image of the silhouette in the picture, as defined above. [Hidden line removal](/hidden-line-removal/) draws the visible part of it, and the [pinhole camera model](/pinhole-camera-model/) gives the central projection.
- **Parting line.** [Parting line generation](/parting-line-generation/) starts from the silhouette in the pull direction and adjusts it to give a parting line that is flat and has no undercut.
- **Silhouette as an intersection.** For an implicit surface, the silhouette is a [surface surface intersection](/surface-surface-intersection/) of the surface with the surface $\nabla F \cdot d = 0$.

## References
