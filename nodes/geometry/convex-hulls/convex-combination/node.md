---
tag: 32D9RE
kind: definition
slug: convex-combination
name: Convex combination
aliases:
- convex combination of points
- weighted average
- barycentric combination
area: geometry/convex-hulls
level: intro
summary: A weighted sum of points with non-negative weights summing to one.
prereqs: [point-and-vector]
see_also: [convex-set, convex-hull, affine-hull, conic-hull, caratheodory-theorem, jensens-inequality, expected-value, oriented-triangle-area]
sources:
  - book: isbn:9780691015866
    title: R. Tyrrell Rockafellar, Convex Analysis, Princeton University Press, 1970
    locator: Section 2, Convex sets and cones (convex combinations and the theorem that a convex set contains all convex combinations of its points)
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 2.1.4 (convex combinations and the convex hull)
  - book: isbn:9780387953748
    title: Jiří Matoušek, Lectures on Discrete Geometry, Springer, 2002
    locator: Chapter 1, Convexity
---

A convex combination of points $x_1, \ldots, x_m$ is a weighted average $\lambda_1 x_1 + \cdots + \lambda_m x_m$ whose weights are nonnegative and add up to 1. The convex combinations of two points fill the segment between them, those of three points fill the triangle, and those of any finite set fill its [convex hull](/convex-hull/). The weights also have a probability reading: a convex combination is the [expected value](/expected-value/) of a random point that equals $x_i$ with probability $\lambda_i$.

## Definition

Let $x_1, \ldots, x_m \in \mathbb{R}^d$ with $m \ge 1$. A *convex combination* of them is a point

$$x = \sum_{i=1}^m \lambda_i x_i \quad\text{with}\quad \lambda_i \ge 0 \text{ for all } i \quad\text{and}\quad \sum_{i=1}^m \lambda_i = 1.$$

The numbers $\lambda_i$ are the *weights* or *coefficients*. The sum is always finite. For $m = 2$ the convex combinations are the points $(1 - t) x_1 + t x_2$ with $t \in [0, 1]$, the segment $[x_1, x_2]$.

The two conditions on the weights give four kinds of combination, from the most to the least restricted:

| weights | name | set of all such combinations |
| --- | --- | --- |
| $\lambda_i \ge 0$, $\sum \lambda_i = 1$ | convex combination | [convex hull](/convex-hull/) |
| any real $\lambda_i$, $\sum \lambda_i = 1$ | affine combination | [affine hull](/affine-hull/) |
| $\lambda_i \ge 0$ | conic (nonnegative) combination | [conic hull](/conic-hull/) |
| any real $\lambda_i$ | linear combination | linear span |

**Proposition.** A set $C \subseteq \mathbb{R}^d$ is [convex](/convex-set/) if and only if it contains every convex combination of finitely many of its points.

*Proof.* If $C$ contains all convex combinations, it contains those with $m = 2$, which is the definition of convexity. For the converse, let $C$ be convex; we show by induction on $m$ that each convex combination $x = \sum_{i=1}^m \lambda_i x_i$ of points of $C$ is in $C$. For $m = 1$, $x = x_1$. Let $m \ge 2$. If $\lambda_m = 1$, the other weights are 0 and $x = x_m \in C$. Otherwise put $\sigma = 1 - \lambda_m > 0$ and

$$y = \sum_{i=1}^{m-1} \frac{\lambda_i}{\sigma} x_i.$$

The weights $\lambda_i / \sigma$ are nonnegative and add up to $(1 - \lambda_m)/\sigma = 1$, so $y$ is a convex combination of $m - 1$ points of $C$ and $y \in C$ by induction. Then $x = \sigma y + \lambda_m x_m = (1 - \lambda_m) y + \lambda_m x_m$ is a point of the segment $[y, x_m] \subseteq C$. $\blacksquare$

**Combinations of combinations.** If each $y_j = \sum_i \lambda_{ji} x_i$ is a convex combination of $x_1, \ldots, x_m$ and $z = \sum_j \mu_j y_j$ is a convex combination of the $y_j$, then $z = \sum_i \big(\sum_j \mu_j \lambda_{ji}\big) x_i$, and the new weights are nonnegative and add up to $\sum_j \mu_j \sum_i \lambda_{ji} = 1$. So the set of convex combinations of a fixed set of points is itself convex, which is half of the proof that it is the [convex hull](/convex-hull/).

**Barycentric coordinates.** If $a, b, c$ are the corners of a nondegenerate triangle in the plane, each point $p$ of the plane has unique weights $(\alpha, \beta, \gamma)$ with $\alpha + \beta + \gamma = 1$ and $p = \alpha a + \beta b + \gamma c$. They are ratios of [oriented triangle areas](/oriented-triangle-area/):

$$\alpha = \frac{\mathrm{orient}(p, b, c)}{\mathrm{orient}(a, b, c)}, \qquad \beta = \frac{\mathrm{orient}(a, p, c)}{\mathrm{orient}(a, b, c)}, \qquad \gamma = \frac{\mathrm{orient}(a, b, p)}{\mathrm{orient}(a, b, c)}.$$

The point $p$ is a convex combination of $a, b, c$, which means it lies in the closed triangle, exactly when all three are $\ge 0$. With integer coordinates the three signs give an exact test, and the weights are exact rationals.

## Examples and non-examples

- **A worked triangle.** Let $a = (0, 0)$, $b = (6, 0)$, $c = (0, 6)$ and $p = (1, 2)$. Then $\mathrm{orient}(a, b, c) = 36$, $\mathrm{orient}(p, b, c) = 18$, $\mathrm{orient}(a, p, c) = 6$ and $\mathrm{orient}(a, b, p) = 12$. So $(\alpha, \beta, \gamma) = (\frac{1}{2}, \frac{1}{6}, \frac{1}{3})$, and indeed $\frac{1}{6}(6, 0) + \frac{1}{3}(0, 6) = (1, 2)$. All weights are positive, so $p$ is inside the triangle.
- **A point outside.** For $q = (5, 3)$ and the same triangle, $\mathrm{orient}(q, b, c) = -12$, so $\alpha = -\frac{1}{3}$, $\beta = \frac{5}{6}$, $\gamma = \frac{1}{2}$. This is an affine combination of $a, b, c$, but not a convex one, and $q$ lies outside the triangle, beyond the edge $bc$.
- **The centroid.** With all weights $\frac{1}{m}$, the combination is the centroid $\frac{1}{m} \sum_i x_i$. The centroid of $(0,0)$, $(6,0)$, $(0,6)$ is $(2, 2)$.
- **Many representations.** The center $(1, 1)$ of the square with corners $(0,0)$, $(2,0)$, $(2,2)$, $(0,2)$ is the combination with all weights $\frac{1}{4}$, and also $\frac{1}{2}(2, 0) + \frac{1}{2}(0, 2)$, and also $\frac{1}{2}(0, 0) + \frac{1}{2}(2, 2)$. Weights are unique only when the points are affinely independent. [Carathéodory's theorem](/caratheodory-theorem/) says that $d + 1$ affinely independent points are always enough.
- **Not a convex combination: weights that do not add up to 1.** $2 \cdot (1, 0) = (2, 0)$ uses the weight 2 alone. It is a conic combination of $(1, 0)$, and the conic combinations of one nonzero vector form a ray, not a point.
- **Not a convex combination: an infinite sum.** The definition uses finitely many points. Integrals against a probability measure, such as the center of mass of a solid body, are the continuous analogue and also land in the closed convex hull, but they are not convex combinations in the sense above.

## Related definitions

- A set is [convex](/convex-set/) exactly when it is closed under convex combinations, as proved above.
- The [convex hull](/convex-hull/) of a set is the set of all convex combinations of its points, the [affine hull](/affine-hull/) uses affine combinations, and the [conic hull](/conic-hull/) uses nonnegative combinations.
- [Carathéodory's theorem](/caratheodory-theorem/) bounds the number of points needed in a convex combination in $\mathbb{R}^d$ by $d + 1$.
- [Jensen's inequality](/jensens-inequality/) says that a [convex function](/convex-function/) $f$ satisfies $f(\sum_i \lambda_i x_i) \le \sum_i \lambda_i f(x_i)$ for each convex combination. With $\lambda_i$ read as probabilities it is $f(\mathbb{E}[X]) \le \mathbb{E}[f(X)]$.
- An [extreme point](/extreme-point/) of a convex set is a point that is not a convex combination of other points of the set.

## References
