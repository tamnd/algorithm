---
tag: V08SST
kind: theorem
slug: caratheodory-theorem
name: Carathéodory's theorem
aliases:
- Caratheodory theorem
- Caratheodory's theorem on convex hulls
area: geometry/convex-hulls
level: intro
summary: Any point in the convex hull of a set in R^d is a convex combination of at most d+1 points of the set.
prereqs: [convex-hull, convex-combination, linear-independence]
see_also: [radon-theorem, helly-theorem, conic-hull, affine-hull, convex-polytope, simplex-method, minkowski-weyl-theorem]
sources:
  - paper: doi:10.1007/BF01449883
    title: Constantin Carathéodory, Über den Variabilitätsbereich der Koeffizienten von Potenzreihen, die gegebene Werte nicht annehmen, Mathematische Annalen 64, 1907
    locator: the statement on points of the convex hull of a set as convex combinations of at most d+1 of its points
  - book: isbn:9780387953748
    title: Jiří Matoušek, Lectures on Discrete Geometry, Springer, 2002
    locator: Chapter 1, Convexity (Carathéodory's theorem and its proof by affine dependence)
  - book: isbn:9780691015866
    title: R. Tyrrell Rockafellar, Convex Analysis, Princeton University Press, 1970
    locator: Section 17, Carathéodory's theorem (the versions for convex hulls and for cones)
---

Carathéodory's theorem says that if a point lies in the [convex hull](/convex-hull/) of a set $S \subseteq \mathbb{R}^d$, then it is a [convex combination](/convex-combination/) of at most $d + 1$ points of $S$, and these points can be taken affinely independent. So the convex hull of a set in the plane is the union of the triangles with corners in the set, and in space the union of the tetrahedra. The bound $d + 1$ depends only on the dimension, not on the size of $S$. The cone version says that a vector in the [conic hull](/conic-hull/) of $S$ is a nonnegative combination of at most $d$ linearly independent vectors of $S$.

## Statement

For a set $S \subseteq \mathbb{R}^d$, $\mathrm{conv}(S)$ is the set of all convex combinations $\sum_{i=1}^m \lambda_i s_i$ with $m \ge 1$, $s_i \in S$, $\lambda_i \ge 0$ and $\sum_i \lambda_i = 1$. Points $s_1, \ldots, s_m$ are *affinely independent* if $s_2 - s_1, \ldots, s_m - s_1$ are [linearly independent](/linear-independence/); then $m \le d + 1$.

**Theorem (Carathéodory, 1907).** Let $S \subseteq \mathbb{R}^d$ and $x \in \mathrm{conv}(S)$. Then there are affinely independent points $s_1, \ldots, s_m \in S$, with $m \le d + 1$, and $\lambda_1, \ldots, \lambda_m > 0$ with $\sum_i \lambda_i = 1$, such that $x = \sum_i \lambda_i s_i$. So

$$\mathrm{conv}(S) = \bigcup \{\mathrm{conv}(T) : T \subseteq S,\ |T| \le d + 1\}.$$

**Theorem (cone version).** Let $S \subseteq \mathbb{R}^d$ and let $x \ne 0$ be a nonnegative combination of vectors of $S$. Then $x = \sum_{i=1}^m \mu_i s_i$ with $\mu_i > 0$ and $s_1, \ldots, s_m \in S$ linearly independent, so $m \le d$.

## In plain words

Take some points and the region they enclose when you wrap them tightly. Pick any spot in that region. In the plane, you can always find three of the points that form a triangle around the spot. You never need more than three, however many points there are. In space you need four points, the corners of a pyramid with a triangular base. In general you need one more point than the number of directions in the space.

The reason is simple. If a spot is a weighted mix of too many points, the points are not spread out enough: you can shift weight between them without moving the spot. Shift until one weight reaches zero and drop that point. Repeat until few enough points remain.

## Proof

*Convex hull version.* Since $x \in \mathrm{conv}(S)$, it is a convex combination of finitely many points of $S$. Among all ways to write $x = \sum_{i=1}^m \lambda_i s_i$ as a convex combination with $s_i \in S$, choose one with $m$ smallest. Then all $\lambda_i > 0$, since a zero weight could be dropped. We show that $s_1, \ldots, s_m$ are affinely independent, which gives $m \le d + 1$, because $\mathbb{R}^d$ has at most $d$ linearly independent vectors.

Suppose they are affinely dependent. Then $s_2 - s_1, \ldots, s_m - s_1$ are linearly dependent: $\sum_{i=2}^m \alpha_i (s_i - s_1) = 0$ with some $\alpha_i \ne 0$. Put $\mu_i = \alpha_i$ for $i \ge 2$ and $\mu_1 = -\sum_{i \ge 2} \alpha_i$. Then

$$\sum_{i=1}^m \mu_i s_i = 0, \qquad \sum_{i=1}^m \mu_i = 0, \qquad \mu \ne 0.$$

Since the $\mu_i$ sum to 0 and are not all 0, some $\mu_i > 0$. Let

$$t = \min\{\lambda_i / \mu_i : \mu_i > 0\} > 0,$$

reached at an index $j$, and put $\lambda'_i = \lambda_i - t \mu_i$. For $\mu_i \le 0$, $\lambda'_i \ge \lambda_i > 0$. For $\mu_i > 0$, $\lambda'_i \ge 0$ by the choice of $t$, and $\lambda'_j = 0$. Also $\sum_i \lambda'_i = \sum_i \lambda_i - t \sum_i \mu_i = 1$ and $\sum_i \lambda'_i s_i = x - t \cdot 0 = x$. So $x$ is a convex combination of the $m - 1$ points $s_i$ with $i \ne j$, against the choice of $m$. $\square$

*Cone version.* Choose $x = \sum_{i=1}^m \mu_i s_i$ with $\mu_i > 0$ and $m$ smallest; $m \ge 1$ because $x \ne 0$. If the $s_i$ are linearly dependent, $\sum_i \alpha_i s_i = 0$ with $\alpha \ne 0$, and replacing $\alpha$ by $-\alpha$ if needed, some $\alpha_i > 0$. With $t = \min\{\mu_i / \alpha_i : \alpha_i > 0\}$ the weights $\mu_i - t \alpha_i$ are nonnegative, one of them is 0, and they still give $x$. This contradicts the choice of $m$. So the $s_i$ are linearly independent, and $m \le d$. $\blacksquare$

*Example of the reduction step.* In the plane, $x = (1, 1)$ is the average of the four corners $s_1 = (0,0)$, $s_2 = (2,0)$, $s_3 = (2,2)$, $s_4 = (0,2)$ of a square, with all $\lambda_i = 1/4$. Four points in the plane are affinely dependent: $s_1 - s_2 + s_3 - s_4 = 0$, so $\mu = (1, -1, 1, -1)$. Then $t = \min\{(1/4)/1, (1/4)/1\} = 1/4$, and $\lambda' = (0, 1/2, 0, 1/2)$: $x = \frac{1}{2}(2, 0) + \frac{1}{2}(0, 2)$, a combination of two points.

## Consequences

- **The planar hull is a union of triangles.** For a finite set $S$ in the plane, each point of $\mathrm{conv}(S)$ lies in a triangle (possibly flat) with corners in $S$. So a point $q$ is in the hull exactly when it is in one of these triangles. This gives the slow but simple membership test of the [convex hull problem](/convex-hull-problem/): a point of $S$ is not a vertex of the hull exactly when it lies in a triangle of three other points of $S$, or on a segment between two of them.
- **Compactness.** If $S$ is compact, $\mathrm{conv}(S)$ is compact: it is the image of the compact set $S^{d+1} \times \Delta_d$, where $\Delta_d$ is the set of weight vectors, under the continuous map $(s, \lambda) \mapsto \sum_i \lambda_i s_i$.
- **Basic solutions in linear programming.** If the system $Ax = b$, $x \ge 0$ with $A \in \mathbb{R}^{m \times n}$ has a solution, then $b$ is in the cone of the columns of $A$, and the cone version gives a solution whose nonzero entries belong to linearly independent columns. This is the existence of a basic feasible solution, the starting point of the [simplex method](/simplex-method/).
- **Helly and Radon.** Carathéodory's theorem, [Radon's theorem](/radon-theorem/) and [Helly's theorem](/helly-theorem/) are the three classical results on convex sets whose constants depend only on the dimension, and each has a proof by affine dependence of $d + 2$ points.

## Tightness

The number $d + 1$ cannot be lowered. Let $v_0, \ldots, v_d$ be affinely independent, for example $0$ and the unit vectors, and let $x$ be their average. A convex combination of a proper subset of the $v_i$ lies on a proper face of the simplex, where some barycentric coordinate is 0, but every barycentric coordinate of $x$ is $1/(d+1)$. So $x$ needs all $d + 1$ points.

Several results change the setting.

- **Interior points (Steinitz).** A point in the interior of $\mathrm{conv}(S)$ lies in the interior of the convex hull of at most $2d$ points of $S$, and $2d$ is needed for the center of a cross-polytope.
- **Colorful version (Bárány, 1982).** If $x$ lies in the convex hull of each of $d + 1$ sets $S_0, \ldots, S_d$, then it lies in the convex hull of a set with one point from each $S_i$.
- **Approximate version.** If $S$ lies in the unit ball, each point of $\mathrm{conv}(S)$ is within distance $\varepsilon$ of an average of $O(1 / \varepsilon^2)$ points of $S$, a bound that does not depend on $d$. The proof samples points of $S$ at random with the weights $\lambda_i$.

## History

Constantin Carathéodory proved the theorem in 1907, in a paper on the coefficients of power series. Ernst Steinitz added the interior version in 1913. The proof by affine dependence given here is the standard one in textbooks such as Rockafellar's and Matoušek's. Imre Bárány proved the colorful version in 1982, and it became a basic tool for Tverberg-type theorems.

## References
