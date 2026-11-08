---
tag: R30809
kind: definition
slug: convex-hull
name: Convex hull
aliases:
- convex closure
- convex envelope of a point set
area: geometry/convex-hulls
level: intro
summary: The smallest convex set containing a given set, equal to all convex combinations of its points.
prereqs: [convex-set, convex-combination]
see_also: [convex-hull-problem, convex-hull-3d, extreme-point, convex-polytope, caratheodory-theorem, affine-hull, conic-hull, separating-hyperplane-theorem]
sources:
  - book: isbn:9780691015866
    title: R. Tyrrell Rockafellar, Convex Analysis, Princeton University Press, 1970
    locator: Section 2 (the convex hull as the set of convex combinations), Section 11 (separation) and Section 17 (Carathéodory's theorem and closedness of hulls of compact sets)
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 2.1.4 (convex sets and the convex hull)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, 3rd edition, Springer, 2008
    locator: Chapter 1, Section 1.1 (the convex hull of a planar point set and its characterizations)
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 3, Convex hulls (definitions of the convex hull and extreme points)
---

The convex hull of a set $S$ is the smallest [convex set](/convex-set/) that contains $S$. For a finite set of points in the plane it is the convex polygon you get when you stretch a rubber band around all the points and let it go; its corners are points of $S$. The hull has three equivalent descriptions: the intersection of all convex sets that contain $S$, the set of all [convex combinations](/convex-combination/) of points of $S$, and, for a finite or compact $S$, the intersection of all closed half-spaces that contain $S$. Computing it is the [convex hull problem](/convex-hull-problem/) in the plane and the [3D convex hull problem](/convex-hull-3d/) in higher dimensions.

## Definition

Let $S \subseteq \mathbb{R}^d$. The *convex hull* of $S$ is

$$\mathrm{conv}(S) = \bigcap \{ C \subseteq \mathbb{R}^d : C \text{ is convex and } S \subseteq C \}.$$

An intersection of convex sets is convex, so $\mathrm{conv}(S)$ is convex, it contains $S$, and it lies inside every convex set that contains $S$. In this sense it is the smallest convex superset of $S$.

**Theorem 1 (inner description).** For every $S \subseteq \mathbb{R}^d$, $\mathrm{conv}(S)$ is the set of all convex combinations of finitely many points of $S$.

*Proof.* Let $K$ be the set of all convex combinations of points of $S$. Each point $s \in S$ is the combination of itself with weight 1, so $S \subseteq K$. $K$ is convex: given $x = \sum_i \lambda_i s_i$ and $y = \sum_j \mu_j s'_j$ in $K$ and $t \in [0, 1]$, the point $(1 - t)x + ty = \sum_i (1 - t)\lambda_i s_i + \sum_j t \mu_j s'_j$ has nonnegative weights with sum $(1 - t) + t = 1$, so it is in $K$. Hence $\mathrm{conv}(S) \subseteq K$. Conversely, every convex set $C \supseteq S$ contains all convex combinations of its own points, as shown on the [convex combination](/convex-combination/) page, so $K \subseteq C$. Taking the intersection over all such $C$ gives $K \subseteq \mathrm{conv}(S)$. $\blacksquare$

[Carathéodory's theorem](/caratheodory-theorem/) sharpens Theorem 1: each point of $\mathrm{conv}(S)$ is a convex combination of at most $d + 1$ points of $S$.

**Theorem 2 (outer description).** If $S \subseteq \mathbb{R}^d$ is compact (for example finite), then $\mathrm{conv}(S)$ is compact, and it is the intersection of all closed half-spaces $\{x : a \cdot x \le b\}$ that contain $S$.

*Proof.* By Carathéodory's theorem, $\mathrm{conv}(S)$ is the image of the compact set $S^{d+1} \times \Delta_d$ under the continuous map $(s_0, \ldots, s_d, \lambda) \mapsto \sum_i \lambda_i s_i$, where $\Delta_d$ is the set of $\lambda \in \mathbb{R}^{d+1}$ with $\lambda \ge 0$ and $\sum_i \lambda_i = 1$. So it is compact. Each closed half-space that contains $S$ is convex, so it contains $\mathrm{conv}(S)$. If $q \notin \mathrm{conv}(S)$, the [separating hyperplane theorem](/separating-hyperplane-theorem/) for a point and a closed convex set gives $a$ and $b$ with $a \cdot x \le b$ on $\mathrm{conv}(S)$ and $a \cdot q > b$, so some half-space that contains $S$ misses $q$. $\blacksquare$

For a finite set $S$, the hull is a [convex polytope](/convex-polytope/), and finitely many half-spaces, one per facet, are enough. In the plane the hull of a finite set that is not on one line is a convex polygon. Its corners are the [extreme points](/extreme-point/) of $S$: the points of $S$ that are not convex combinations of other points of $S$. Computing the hull usually means listing these corners in order around the boundary.

## Examples and non-examples

- **A finite planar set.** Let $S = \{(0,0), (4,0), (4,3), (0,3), (2,1), (1,2), (4,1), (2,3)\}$. The hull is the rectangle $[0, 4] \times [0, 3]$, and its counterclockwise corners are $(0,0), (4,0), (4,3), (0,3)$. The points $(2,1)$ and $(1,2)$ are inside. The points $(4,1)$ and $(2,3)$ are on the boundary but are not extreme: $(4,1) = \frac{2}{3}(4, 0) + \frac{1}{3}(4, 3)$. Whether such boundary points appear in the output is a choice that every hull algorithm must make and document.
- **Two points and three points.** The hull of $\{a, b\}$ is the segment $[a, b]$. The hull of three points that are not on one line is the solid triangle they span. Points on one line have a segment as hull, from the smallest to the largest point in the order along the line.
- **A circle.** The hull of the circle $\{x \in \mathbb{R}^2 : |x| = 1\}$ is the closed disk $|x| \le 1$. Every point of the circle is extreme.
- **Already convex.** If $S$ is convex, $\mathrm{conv}(S) = S$, and the converse also holds.
- **Not the hull: the union of the segments.** The union of all segments $[s, s']$ with $s, s' \in S$ is not $\mathrm{conv}(S)$ in general. For the corners of a triangle it is only the boundary of the triangle. In $\mathbb{R}^d$ one has to take combinations of $d + 1$ points at a time, and the union of the simplices with corners in $S$ is the hull by Carathéodory's theorem.
- **Hulls of closed sets need not be closed.** Let $S$ be the $x$-axis together with the point $(0, 1)$. Then $\mathrm{conv}(S)$ is the strip $\{(x, y) : 0 \le y < 1\}$ together with the point $(0, 1)$. The points $(x, 1)$ with $x \ne 0$ are limits of hull points but are not in the hull. The *closed convex hull*, the closure of $\mathrm{conv}(S)$, is the full strip $0 \le y \le 1$. Theorem 2 needs compactness for this reason.
- **Hulls of open sets are open.** Let $S$ be open and $x = \sum_i \lambda_i s_i$ with $\lambda_1 > 0$. Take an open ball $U \subseteq S$ around $s_1$. Moving $s_1$ inside $U$ moves $x$ inside the open set $x + \lambda_1 (U - s_1)$, and all these points are in $\mathrm{conv}(S)$. So $\mathrm{conv}(S)$ is open. For example, the hull of two disjoint open disks is an open stadium shape.

## Related definitions

- A [convex set](/convex-set/) equals its own hull. A [convex combination](/convex-combination/) is the building block of Theorem 1.
- An [extreme point](/extreme-point/) of a finite set is a corner of its hull, and the [convex hull problem](/convex-hull-problem/) asks for these corners in order.
- A [convex polytope](/convex-polytope/) is the hull of a finite set in $\mathbb{R}^d$, and its [facets](/facet/) give the outer description of Theorem 2.
- The [affine hull](/affine-hull/) and the [conic hull](/conic-hull/) replace convex combinations by affine and by nonnegative combinations. The [support function](/support-function/) $h_S(u) = \sup_{s \in S} u \cdot s$ describes the closed convex hull through Theorem 2.
- The [convex envelope](/convex-envelope/) of a function is the largest convex function below it. Its epigraph is the closed convex hull of the epigraph of the function. It is a different object from the hull of a point set.
- A [concave hull](/concave-hull/) is a non-convex shape that hugs a point set more closely; it has no single standard definition.

## References
