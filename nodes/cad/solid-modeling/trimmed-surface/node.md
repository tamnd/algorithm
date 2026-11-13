---
tag: W5MMTQ
kind: definition
slug: trimmed-surface
name: Trimmed surface
aliases:
- trimmed NURBS surface
- trimmed patch
area: cad/solid-modeling
level: core
summary: A parametric surface restricted to a region of its parameter domain bounded by trimming curves, the usual way a B-rep stores the face of a curved solid.
prereqs: [parametric-surface, nurbs, boundary-representation]
see_also: [surface-surface-intersection, tensor-product-surface, b-spline, curve-intersection, bezier-clipping, point-in-polygon, surface-tessellation, geometric-robustness-problem]
sources:
  - paper: doi:10.1145/1360612.1360678
    title: Thomas W. Sederberg, G. Thomas Finnigan, Xin Li, Hongwei Lin and Heather Ipson, Watertight trimmed NURBS, ACM Transactions on Graphics 27(3), Article 79, 2008
    locator: the introduction (the gaps between neighbor trimmed NURBS faces and why they cannot be removed in general) and the conversion of a trimmed NURBS model into a gap-free T-spline model
  - book: isbn:9783540424543
    title: Nicholas M. Patrikalakis and Takashi Maekawa, Shape Interrogation for Computer Aided Design and Manufacturing, Springer, 2002
    locator: Chapter 1, Representation of curves and surfaces, and Chapter 5, Intersection problems (the intersection curves that become trimming curves)
  - book: isbn:9781558600676
    title: Christoph M. Hoffmann, Geometric and Solid Modeling, An Introduction, Morgan Kaufmann, 1989
    locator: the chapters on curved edges and faces and on surface intersections (general locator, the chapter titles are not confirmed)
---

A trimmed surface is a [parametric surface](/parametric-surface/) $S(u, v)$, usually a [NURBS](/nurbs/) patch, that is kept only over a region $\Omega$ of its parameter rectangle. The region is bounded by closed *trimming curves* drawn in the $(u, v)$ plane: one outer loop, and one inner loop for each hole. A [boundary representation](/boundary-representation/) of a curved solid stores each face this way, because a Boolean operation or a fillet cuts a face along a curve that is not a parameter line, and the patch itself cannot be cut along such a curve. The trimming curves of two neighbor faces describe the same edge in two parameter planes, and in general they do not give the same curve in space, so a trimmed model has small gaps along its edges, and these gaps are a common source of invalid models when a model moves between two systems.

## Definition

Let $S : D \to \mathbb{R}^3$ be a regular parametric surface on the rectangle $D = [a, b] \times [c, d]$, for example a NURBS [tensor-product surface](/tensor-product-surface/) whose two directions use [B-splines](/b-spline/). A *trimming loop* is a closed curve $\gamma : [0, 1] \to D$ with $\gamma(0) = \gamma(1)$ and no self-intersection, usually a 2D B-spline or NURBS curve or a chain of such curves.

A **trimmed surface** is a pair $(S, \Omega)$ where $\Omega \subseteq D$ is a closed region bounded by a finite set of pairwise disjoint trimming loops $\gamma_0, \gamma_1, \ldots, \gamma_k$, such that:

- $\gamma_0$ is the *outer loop* and runs counterclockwise in the $(u, v)$ plane. The rectangle boundary $\partial D$ is a valid outer loop.
- $\gamma_1, \ldots, \gamma_k$ are *inner loops*. They lie inside $\gamma_0$, outside each other, and run clockwise.
- $\Omega$ is the set of points of $D$ on the left of every loop, with the loops included. So $\Omega$ is the closed disk of $\gamma_0$ minus the open disks of the inner loops.

The point set of the face is $S(\Omega)$. Its normal is $S_u \times S_v$, or the opposite vector when the face stores a reversed flag. This page uses the convention of the B-rep pages: the normal of a face points out of the solid, and each loop runs counterclockwise around that normal (the right-hand rule). With the normal $S_u \times S_v$, a loop that is counterclockwise in the $(u, v)$ plane maps to a loop that is counterclockwise around the normal in space, so the two orientation rules agree.

Each edge of the B-rep where two trimmed faces $(S_1, \Omega_1)$ and $(S_2, \Omega_2)$ meet has two *parameter curves* (often called pcurves), a part $\beta_1$ of a loop of $\Omega_1$ and a part $\beta_2$ of a loop of $\Omega_2$. Many systems also store a third curve $E$ in space. In exact arithmetic the three curves describe one curve: $S_1 \circ \beta_1 = S_2 \circ \beta_2 = E$. In a real model they are approximations of the intersection curve of the two surfaces, computed by [surface surface intersection](/surface-surface-intersection/), and they agree only within a tolerance $\tau$:

$$\max_t \left| S_1(\beta_1(t)) - S_2(\beta_2(\phi(t))) \right| \le \tau$$

for some monotone reparametrization $\phi$. The model is *watertight within* $\tau$ when every edge meets this bound. The exact intersection curve of two polynomial patches has a very high algebraic degree, while the stored trimming curves have a low fixed degree, so $\tau > 0$ in general. Sederberg and coauthors call these gaps a long-standing problem of trimmed NURBS models and give a conversion to T-splines that has none.

Point membership in a trimmed surface is a 2D question. A point $S(u, v)$ of the patch is on the face exactly when $(u, v) \in \Omega$, which a winding number or ray test against the loops decides, as in [point in polygon](/point-in-polygon/) with curved edges. A ray test meets each loop in the roots of one polynomial per curve piece, which is [curve intersection](/curve-intersection/) of the ray with a B-spline curve, for example by [Bézier clipping](/bezier-clipping/). Degenerate input is part of the definition: a point on a loop is on the face, the test must return "on" for it, and a ray through a vertex of a loop must be counted once, as in the polygon case.

## Examples and non-examples

- **A plate with a round hole.** Let $S(u, v) = (u, v, 0)$ on $D = [0, 1]^2$, with outer loop $\partial D$ and one inner loop, the circle of center $(1/2, 1/2)$ and radius $1/4$ run clockwise. A NURBS curve represents this circle exactly. The face is the unit square minus an open disk. Its area is $\iint_\Omega |S_u \times S_v| \, du \, dv = 1 - \pi / 16$.
- **A cylinder cut by a cylinder.** Take the cylinder $S(\theta, z) = (\cos \theta, \sin \theta, z)$ on $[0, 2\pi] \times [-2, 2]$ and a second cylinder $x^2 + z^2 = (1/2)^2$ that crosses it, as in a T-joint of two pipes. The face of the union on the big cylinder has an inner loop on each side, $\cos^2 \theta + z^2 = 1/4$ near $\theta = \pi / 2$ and near $\theta = 3\pi / 2$, where the second cylinder enters and leaves. These are closed curves in the $(\theta, z)$ plane that no parameter line can follow.
- **An untrimmed patch.** A Bézier or B-spline patch with $\Omega = D$ is the case $k = 0$ with outer loop $\partial D$.
- **A periodic surface.** On a full cylinder, a loop that goes once around the axis is not a closed curve in the rectangle $D$; it runs from $\theta = 0$ to $\theta = 2\pi$. Systems treat this by a seam edge on the line $\theta = 0$, which makes the loop closed in $D$, or by a domain that is a cylinder. Without one of the two, the definition above does not apply.

Non-examples:

- **Crossing loops.** If an inner loop crosses the outer loop, or two inner loops cross, the "left of every loop" rule gives no consistent region, and the face is invalid.
- **A loop with the wrong orientation.** An inner loop that runs counterclockwise defines, by the left rule, the region inside it. Together with the outer loop the region is then only the inner disk, which is not the intended face with a hole.
- **A loop outside $D$.** A trimming curve that leaves the rectangle asks for points where $S$ is not defined. Such curves come from an intersection curve that was computed past the end of a patch.

## Related definitions

- A [NURBS](/nurbs/) surface or a [tensor-product surface](/tensor-product-surface/) is the base surface $S$. Its parameter rectangle is $D$.
- A [boundary representation](/boundary-representation/) stores faces as trimmed surfaces, edges as curves with their parameter curves, and the adjacency of faces, edges and loops.
- [Surface surface intersection](/surface-surface-intersection/) computes the curves along which a Boolean operation trims two faces. Its output becomes two parameter curves and one space curve.
- [Surface tessellation](/surface-tessellation/) of a trimmed surface must triangulate $\Omega$, not $D$, and must use the same points on the edge for both neighbor faces, or the mesh has cracks along the gaps.
- An [offset surface](/offset-surface/) of a trimmed face is trimmed by the image of the same loops, as long as the offset has no self-intersection.
- The gaps are an instance of the [geometric robustness problem](/geometric-robustness-problem/): the model is consistent only within a tolerance, and algorithms that need exact incidence must treat edges as tolerance zones.

## References
