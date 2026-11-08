---
tag: K1CWSP
kind: theorem
slug: radon-theorem
name: Radon's theorem
aliases:
- Radon partition
- Radon's lemma
- Radon point
area: geometry/convex-hulls
level: intro
summary: Any d+2 points in R^d can be split into two sets whose convex hulls intersect.
prereqs: [convex-hull, linear-independence]
see_also: [helly-theorem, caratheodory-theorem, affine-hull, vc-dimension, range-space, epsilon-net-theorem, gaussian-elimination, general-position]
sources:
  - book: isbn:9780387953748
    title: Jiri Matousek, Lectures on Discrete Geometry, Graduate Texts in Mathematics 212, Springer, 2002
    locator: Chapter 1, Section 1.3, Radon's lemma and Helly's theorem
  - paper: doi:10.1007/BF01464231
    title: Johann Radon, Mengen konvexer Körper, die einen gemeinsamen Punkt enthalten, Mathematische Annalen 83, 1921
    locator: the lemma on d+2 points and its use in the proof of Helly's theorem
  - paper: "Helge Tverberg, A generalization of Radon's theorem, Journal of the London Mathematical Society 41, 1966"
    locator: the partition of (r-1)(d+1)+1 points into r parts with a common point
  - paper: "Kenneth L. Clarkson, David Eppstein, Gary L. Miller, Carl Sturtivant and Shang-Hua Teng, Approximating center points with iterative Radon points, International Journal of Computational Geometry and Applications 6(3), 1996"
    locator: the iterated Radon point as an approximate centerpoint
---

Radon's theorem says that any $d + 2$ points in $\mathbb{R}^d$ can be split into two groups whose [convex hulls](/convex-hull/) meet. In the plane, four points always form either a triangle with the fourth point inside it, or two segments that cross. The theorem is the main step in the proof of [Helly's theorem](/helly-theorem/), it shows that half-spaces in $\mathbb{R}^d$ have [VC dimension](/vc-dimension/) $d + 1$, and the common point can be computed exactly by solving one linear system.

## Statement

**Theorem (Radon, 1921).** Let $P = \{p_1, \ldots, p_m\}$ be points in $\mathbb{R}^d$ with $m \ge d + 2$ (repeated points allowed, as a sequence). Then the index set $\{1, \ldots, m\}$ has a partition into two disjoint nonempty sets $I$ and $J$ with

$$\operatorname{conv}\{p_i : i \in I\} \cap \operatorname{conv}\{p_j : j \in J\} \ne \emptyset.$$

Such a pair $(I, J)$ is a **Radon partition**, and a point in the intersection is a **Radon point**. The theorem holds for any $d \ge 1$ and any points, with no [general position](/general-position/) assumption.

Notation: $P$ is the point set, $n = |P|$ (here $n = m$), $d$ is the dimension, and $\mathrm{orient}(p, q, r)$ is the sign of the planar orientation determinant, positive for a counterclockwise turn (see [orientation test](/orientation-test/)).

## In plain words

Take any four points on a sheet of paper. Either one of them is inside the triangle of the other three, or you can pair them up so that the two connecting segments cross. Either way, you have split the four points into two groups whose shapes overlap.

The same is true one dimension up with five points, and in general with two more points than the number of dimensions. With one point fewer it can fail: the three corners of a triangle cannot be split this way. The proof is short. It writes down a balance of weights on the points, some positive and some negative, and the point where the two sides balance is in both groups.

## Proof

Let $p_1, \ldots, p_m \in \mathbb{R}^d$ with $m \ge d + 2$.

1. **Affine dependence.** Consider the homogeneous linear system in the unknowns $\lambda_1, \ldots, \lambda_m$:
$$\sum_{i=1}^{m} \lambda_i p_i = 0, \qquad \sum_{i=1}^{m} \lambda_i = 0.$$
It has $d + 1$ equations ($d$ for the coordinates, one for the sum) and $m \ge d + 2$ unknowns, so it has a solution $\lambda \ne 0$ (a homogeneous system with more unknowns than equations has a nonzero solution, see [linear independence](/linear-independence/)).
2. **The partition.** Let $I = \{i : \lambda_i > 0\}$ and $J = \{j : \lambda_j \le 0\}$. Since $\lambda \ne 0$ and the $\lambda_i$ sum to $0$, some $\lambda_i$ is positive and some is negative. So $I$ and $J$ are both nonempty, and they partition the indices.
3. **The common point.** Let $S = \sum_{i \in I} \lambda_i > 0$. The sum condition gives $\sum_{j \in J} (-\lambda_j) = S$. The first condition gives $\sum_{i \in I} \lambda_i p_i = \sum_{j \in J} (-\lambda_j) p_j$. Divide by $S$ and let
$$x = \sum_{i \in I} \frac{\lambda_i}{S}\, p_i = \sum_{j \in J} \frac{-\lambda_j}{S}\, p_j.$$
On the left the coefficients are positive and sum to $1$, and on the right they are nonnegative and sum to $1$. So $x$ is a convex combination of the points of $I$ and also of the points of $J$, and $x$ lies in both hulls. $\blacksquare$

**Computing a Radon point.** The proof is an algorithm. Solve the system of step 1 for the first $d + 2$ points by [Gaussian elimination](/gaussian-elimination/) in $O(d^3)$ arithmetic operations, then form $I$, $J$ and $x$. With integer or rational input and exact rational arithmetic, $x$ is exact.

**Uniqueness in the plane.** If four points in the plane are in general position (no three collinear), the solution space of step 1 has dimension one, so $\lambda$ is unique up to a scalar, and the Radon partition is unique. It is a $3 + 1$ split when one point is inside the triangle of the others, and a $2 + 2$ split when the four points are in convex position, where the Radon point is the crossing of the two diagonals.

**Examples.**

- For $(0,0)$, $(4,0)$, $(0,4)$, $(1,1)$ a solution is $\lambda = (1/2, 1/4, 1/4, -1)$, so $I$ is the triangle, $J = \{(1,1)\}$, and the Radon point is $(1,1) = \tfrac12 (0,0) + \tfrac14 (4,0) + \tfrac14 (0,4)$.
- For the square $(0,0)$, $(2,0)$, $(2,2)$, $(0,2)$ a solution is $\lambda = (1, -1, 1, -1)$. The partition is the two diagonals, and the Radon point is $(1,1)$.
- In $\mathbb{R}^3$, for $o = (0,0,0)$, $e_1$, $e_2$, $e_3$ and $q = (1,1,1)$ a solution is $\lambda = (-2, 1, 1, 1, -1)$, since $e_1 + e_2 + e_3 - 2o - q = 0$ and the weights sum to $0$. Then $S = 3$, and the Radon point $(1/3, 1/3, 1/3)$ is the center of the triangle $e_1 e_2 e_3$ and lies on the segment from $o$ to $q$.

## Consequences

- **Helly's theorem.** If every $d + 1$ of $n \ge d + 1$ convex sets in $\mathbb{R}^d$ have a common point, then all of them do. The standard proof applies Radon's theorem to $d + 2$ witness points; see [Helly's theorem](/helly-theorem/).
- **VC dimension of half-spaces.** No set of $d + 2$ points in $\mathbb{R}^d$ is shattered by half-spaces: for a Radon partition $(I, J)$, suppose a half-space $H$ contains the points of $I$ and none of $J$. Then $H$ contains $\operatorname{conv} I$, and the complement of $H$, which is also convex, contains $\operatorname{conv} J$. So the two hulls are disjoint, which is false. Hence the subset $I$ is not cut out by any half-space. With $d + 1$ affinely independent points, which are shattered, the VC dimension of half-spaces is exactly $d + 1$. This bound feeds the [epsilon-net theorem](/epsilon-net-theorem/) for the [range space](/range-space/) of half-spaces.
- **Tverberg's theorem** (1966). Any $(r - 1)(d + 1) + 1$ points in $\mathbb{R}^d$ can be split into $r$ groups whose convex hulls have a common point. Radon's theorem is the case $r = 2$.
- **Centerpoints.** Clarkson, Eppstein, Miller, Sturtivant and Teng compute an approximate centerpoint by replacing groups of $d + 2$ points with their Radon point, level by level.
- **Carathéodory and Radon.** The affine dependence of step 1 is also the step that removes one point in the proof of [Carathéodory's theorem](/caratheodory-theorem/).

## Tightness

The number $d + 2$ cannot be lowered. Let $p_0, \ldots, p_d$ be $d + 1$ affinely independent points, for example the vertices of a simplex. Suppose $(I, J)$ is a partition with a common point $x = \sum_{i \in I} \alpha_i p_i = \sum_{j \in J} \beta_j p_j$, where the $\alpha_i$ and the $\beta_j$ are nonnegative and each family sums to $1$. Then $\sum_{i \in I} \alpha_i p_i - \sum_{j \in J} \beta_j p_j = 0$ with coefficient sum $1 - 1 = 0$, and the coefficients are not all zero. This is an affine dependence among affinely independent points, a contradiction. In the plane: the three corners of a triangle have no Radon partition, because a vertex is never in the opposite edge.

## History

Johann Radon proved the lemma in 1921 as the tool for his proof of Helly's theorem, which Eduard Helly had found earlier but published only in 1923. Helge Tverberg proved the generalization to $r$ parts in 1966. Radon partitions are a basic object of combinatorial convexity, and the bound on the VC dimension of half-spaces made them standard in learning theory and in the theory of epsilon-nets.

## References
