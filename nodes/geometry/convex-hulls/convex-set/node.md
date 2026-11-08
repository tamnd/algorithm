---
tag: FREJH4
kind: definition
slug: convex-set
name: Convex set
aliases:
- convex region
- convexity
area: geometry/convex-hulls
level: intro
summary: A set that contains the segment between any two of its points.
prereqs: [point-and-vector]
see_also: [convex-combination, convex-hull, convex-polygon, convex-function, half-plane-intersection, separating-hyperplane-theorem, extreme-point, helly-theorem]
sources:
  - book: isbn:9780691015866
    title: R. Tyrrell Rockafellar, Convex Analysis, Princeton University Press, 1970
    locator: Section 2, Convex sets and cones (definition and closure under intersection), and Section 3, The algebra of convex sets
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 2.1.4 (convex sets), Section 2.2 (examples) and Section 2.3 (operations that preserve convexity)
  - book: isbn:9780387953748
    title: Jiří Matoušek, Lectures on Discrete Geometry, Springer, 2002
    locator: Chapter 1, Convexity
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, 3rd edition, Springer, 2008
    locator: Chapter 1, Section 1.1 (convex sets and the convex hull of a planar point set)
---

A convex set is a set of points that contains the whole segment between any two of its points. Disks, triangles, half-planes, lines and the solid cube are convex; a ring, a crescent and the letter L are not. Convexity is the property behind most results in this sub-area: the [convex hull](/convex-hull/) of a point set is the smallest convex set that contains it, and each algorithm for hulls computes the boundary of that set.

## Definition

A set $C \subseteq \mathbb{R}^d$ is *convex* if for all $x, y \in C$ and all $t \in [0, 1]$,

$$(1 - t)\, x + t\, y \in C.$$

The points $(1 - t) x + t y$ for $t \in [0, 1]$ form the closed segment $[x, y]$, so the condition says $[x, y] \subseteq C$ for all $x, y \in C$. The empty set and one-point sets are convex because the condition has no case that fails.

The definition uses only addition and multiplication by reals, so it makes sense in any real vector space. This sub-area uses $\mathbb{R}^2$ and $\mathbb{R}^3$, with the occasional $\mathbb{R}^d$.

**Basic facts.** Each fact follows from the definition in one or two lines.

1. *Intersections.* If each $C_i$ in a family (finite or infinite) is convex, then $\bigcap_i C_i$ is convex: if $x, y$ are in all $C_i$, then $[x, y]$ is in all $C_i$.
2. *Affine images and preimages.* If $f(x) = Ax + b$ and $C$ is convex, then $f(C)$ and $f^{-1}(C)$ are convex, because $f((1 - t)x + ty) = (1 - t) f(x) + t f(y)$.
3. *Sums and scaling.* The [Minkowski sum](/minkowski-sum/) $C + D = \{c + e : c \in C, e \in D\}$ and the scaled set $\lambda C$ of convex sets are convex.
4. *Closure and interior.* The closure and the interior of a convex set are convex.
5. *All convex combinations.* A convex set contains every [convex combination](/convex-combination/) $\sum_i \lambda_i x_i$ of finitely many of its points, not only the combinations of two points. The proof is by induction on the number of points and is on the convex combination page.

Fact 1 gives the [convex hull](/convex-hull/) of a set $S$ as the intersection of all convex sets that contain $S$. Facts 1 and 2 show that each half-space $\{x : a \cdot x \le b\}$ and each intersection of half-spaces is convex, which is why [half-plane intersection](/half-plane-intersection/) produces a convex polygon.

## Examples and non-examples

**Convex.**

- A half-plane $\{(x, y) : 2x + 3y \le 6\}$. The function $(x, y) \mapsto 2x + 3y$ is linear, so on a segment it takes values between the values at the ends. The same argument covers half-spaces in $\mathbb{R}^d$ and, by Fact 1, any polyhedron $\{x : Ax \le b\}$.
- A disk $\{x : |x - c| \le r\}$. For $x, y$ in the disk, $|(1 - t)x + ty - c| = |(1 - t)(x - c) + t(y - c)| \le (1 - t) r + t r = r$ by the triangle inequality. Every ball for every norm is convex in the same way.
- A line, a ray, a segment, a linear or affine subspace, and the whole space.
- The solid triangle with corners $(0, 0)$, $(6, 0)$, $(0, 6)$. It is the intersection of the three half-planes $x \ge 0$, $y \ge 0$ and $x + y \le 6$.
- The [epigraph](/epigraph/) of a [convex function](/convex-function/), the set of points on or above its graph. A function is convex exactly when its epigraph is a convex set.

**Not convex.**

- The ring $\{x \in \mathbb{R}^2 : 1 \le |x| \le 3\}$. The points $(2, 0)$ and $(-2, 0)$ are in it, but their midpoint $(0, 0)$ is not.
- The union of two disjoint disks. A segment from one disk to the other leaves the union.
- An L-shaped region such as $[0, 2] \times [0, 1] \cup [0, 1] \times [0, 2]$. The points $(2, 0)$ and $(0, 2)$ are in it, and so is their midpoint $(1, 1)$, so this pair does not show anything. The pair $(2, 1)$ and $(1, 2)$ does: their midpoint $(\frac{3}{2}, \frac{3}{2})$ is in neither rectangle. One good pair proves nothing, but one bad pair proves that the set is not convex.
- A finite set of two or more points, such as $\{(0, 0), (1, 0)\}$: the midpoint $(\frac{1}{2}, 0)$ is missing. In the same way the integer points $\mathbb{Z}^2$ do not form a convex set.
- The boundary of a convex set with nonempty interior, for example the circle $|x| = 1$: the midpoint of $(1, 0)$ and $(-1, 0)$ is the center.

**A test for polygons.** A simple polygon with corners $v_1, \ldots, v_n$ in counterclockwise order bounds a convex region exactly when every corner turns left or goes straight: $\mathrm{orient}(v_{i-1}, v_i, v_{i+1}) \ge 0$ for each $i$, indices modulo $n$, where $\mathrm{orient}$ is the [orientation test](/orientation-test/). With integer coordinates this is exact. For the corners $(0, 0)$, $(4, 0)$, $(4, 3)$, $(2, 1)$, $(0, 3)$ the value at $(2, 1)$ is $\mathrm{orient}((4, 3), (2, 1), (0, 3)) = (-2)(0) - (-2)(-4) = -8 < 0$, a right turn, and the region is not convex. The test needs the polygon to be simple: a star drawn as a five-pointed self-crossing path turns left at every corner but does not bound a convex region.

## Related definitions

- A [convex combination](/convex-combination/) is a weighted average with nonnegative weights; convex sets are the sets closed under it.
- The [convex hull](/convex-hull/) of $S$ is the smallest convex set that contains $S$.
- An [extreme point](/extreme-point/) of a convex set is a point that is not in the open segment between two other points of the set. A compact convex set is the convex hull of its extreme points (Krein-Milman in general, Minkowski in finite dimension).
- A [supporting hyperplane](/supporting-hyperplane/) touches a closed convex set at a boundary point and has the set on one side. The [separating hyperplane theorem](/separating-hyperplane-theorem/) says that two disjoint convex sets can be split by a hyperplane, under conditions given on that page.
- A [convex polygon](/convex-polygon/) is a polygon whose region is convex, and a [convex polytope](/convex-polytope/) is the convex hull of finitely many points in $\mathbb{R}^d$.
- A [convex function](/convex-function/) is a function whose epigraph is a convex set.
- [Helly's theorem](/helly-theorem/) is about the intersection pattern of convex sets: if every $d + 1$ sets of a finite family of convex sets in $\mathbb{R}^d$ meet, then all of them meet.
- An [affine hull](/affine-hull/) and a [conic hull](/conic-hull/) are the analogues of the convex hull for affine and for nonnegative combinations.

## References
