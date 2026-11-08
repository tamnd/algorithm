---
tag: TMNJEX
kind: definition
slug: affine-hull
name: Affine hull
aliases:
- affine span
- affine closure
area: geometry/convex-hulls
level: intro
summary: The smallest affine subspace containing a set, built from affine combinations.
prereqs: [convex-combination, linear-independence, rank]
see_also: [convex-hull, conic-hull, general-position, gaussian-elimination, caratheodory-theorem, convex-polytope, beneath-beyond, convex-hull-3d]
sources:
  - book: isbn:9780691015866
    title: R. Tyrrell Rockafellar, Convex Analysis, Princeton University Press, 1970
    locator: Section 1, Affine sets (affine sets as translates of subspaces, affine hulls, affine independence and dimension), and Section 6 (relative interiors)
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 2.1.2 (affine sets) and Section 2.1.3 (affine dimension and relative interior)
  - book: isbn:9780387953748
    title: Jiří Matoušek, Lectures on Discrete Geometry, Springer, 2002
    locator: Chapter 1, Convexity (affine combinations, affine dependence and affine hulls)
---

The affine hull of a set $S \subseteq \mathbb{R}^d$ is the smallest flat (point, line, plane or higher analogue) that contains $S$. The affine hull of two distinct points is the line through them, that of three points not on one line is the plane through them, and that of a full-dimensional set is the whole space. Its dimension is the *dimension* of $S$. Hull algorithms use it to detect inputs that are flat, for example points in $\mathbb{R}^3$ that all lie in one plane, and to find a starting simplex of affinely independent points.

## Definition

An *affine combination* of points $x_1, \ldots, x_m \in \mathbb{R}^d$ is a point $\sum_{i=1}^m \lambda_i x_i$ with real weights such that $\sum_{i=1}^m \lambda_i = 1$. The weights may be negative; this is the difference from a [convex combination](/convex-combination/).

A set $A \subseteq \mathbb{R}^d$ is an *affine set* (a *flat*) if it contains every affine combination of two of its points, that is, the whole line through any two of its points. The *affine hull* of $S$ is

$$\mathrm{aff}(S) = \bigcap \{ A : A \text{ is affine and } S \subseteq A \} = \Big\{ \sum_{i=1}^m \lambda_i s_i : m \ge 1,\ s_i \in S,\ \sum_i \lambda_i = 1 \Big\}.$$

The two descriptions agree by the same argument as for the [convex hull](/convex-hull/): the set of affine combinations is affine and contains $S$, and an affine set contains all affine combinations of its points (induction on $m$, as for convex combinations, but with no sign condition). For $S = \emptyset$ the affine hull is empty.

**Translates of subspaces.** A nonempty set $A$ is affine if and only if $A = p + L$ for a linear subspace $L$ and any $p \in A$, and then $L = A - p$ does not depend on $p$. The *dimension* of $A$ is $\dim L$. For nonempty $S$ and any $s_0 \in S$,

$$\mathrm{aff}(S) = s_0 + \mathrm{span}\{ s - s_0 : s \in S \}, \qquad \dim S := \dim \mathrm{aff}(S) = \mathrm{rank}\{ s - s_0 : s \in S \}.$$

The identity holds because $\sum_i \lambda_i s_i = s_0 + \sum_i \lambda_i (s_i - s_0)$ when $\sum_i \lambda_i = 1$, and each $s_0 + \sum_i \mu_i (s_i - s_0)$ is the affine combination with weights $\mu_i$ on $s_i$ and $1 - \sum_i \mu_i$ on $s_0$.

**Affine independence.** Points $x_0, \ldots, x_k$ are *affinely independent* if the only solution of $\sum_i \lambda_i x_i = 0$ with $\sum_i \lambda_i = 0$ is $\lambda = 0$. Equivalent forms: the vectors $x_1 - x_0, \ldots, x_k - x_0$ are [linearly independent](/linear-independence/); the lifted vectors $(x_i, 1) \in \mathbb{R}^{d+1}$ are linearly independent; no $x_i$ is an affine combination of the others. At most $d + 1$ points of $\mathbb{R}^d$ are affinely independent, and $\dim S$ is one less than the largest number of affinely independent points in $S$. Each point of $\mathrm{aff}(x_0, \ldots, x_k)$ has unique affine weights exactly when $x_0, \ldots, x_k$ are affinely independent.

**Computing it exactly.** For a finite set with integer or rational coordinates, run [Gaussian elimination](/gaussian-elimination/) over the rationals on the difference vectors $s - s_0$. The pivot rows give a basis of the direction space $L$, and the points whose rows were independent when they arrived form a maximal affinely independent subset. This takes $O(n d^2)$ arithmetic operations for $n$ points in $\mathbb{R}^d$, with no rounding. A 3D hull algorithm such as [beneath-beyond](/beneath-beyond/) does the same with orientation signs: it looks for two distinct points, then a third not on their line, then a fourth not in their plane, and reports a lower-dimensional input if the search fails.

**Relative interior.** The *relative interior* of a convex set $C$ is its interior inside $\mathrm{aff}(C)$. A segment in $\mathbb{R}^3$ has empty interior but its relative interior is the open segment. Every nonempty convex set in $\mathbb{R}^d$ has a nonempty relative interior, which is why the faces of a [convex polytope](/convex-polytope/) are described by their relative interiors.

## Examples and non-examples

- **Five points on a plane in space.** Take $(1,0,0)$, $(0,1,0)$, $(0,0,1)$, $(1,1,-1)$ and $(2,-1,0)$ in $\mathbb{R}^3$, with $s_0 = (1,0,0)$. The differences are $(-1,1,0)$, $(-1,0,1)$, $(0,1,-1)$ and $(1,-1,0)$. Elimination keeps the first two and reduces the other two to 0: $(0,1,-1) = (-1,1,0) - (-1,0,1)$ and $(1,-1,0) = -(-1,1,0)$. So the rank is 2, the affine hull is the plane $x + y + z = 1$ (each point has coordinate sum 1), and the set has dimension 2. Its linear span is all of $\mathbb{R}^3$, which shows that the affine hull and the span are different.
- **Two points.** $\mathrm{aff}(\{a, b\})$ with $a \ne b$ is the full line $\{(1 - t) a + t b : t \in \mathbb{R}\}$, while the convex hull is only the segment $t \in [0, 1]$.
- **A circle in space.** The circle $\{(x, y, 5) : x^2 + y^2 = 1\}$ has the plane $z = 5$ as affine hull, so it is 2-dimensional although it is a curve. The affine dimension measures the smallest flat, not the intrinsic dimension of a curve or surface.
- **Not affine: a segment, a half-plane, a disk.** Each is convex but does not contain the whole line through two of its points.
- **Not affine: two parallel lines.** The union of the lines $y = 0$ and $y = 1$ is not affine, because the line through $(0, 0)$ and $(0, 1)$ leaves the union. A single line moved off the origin, such as $y = 1$, is affine; affine sets do not need to contain the origin.
- **A full-dimensional set.** Any set in $\mathbb{R}^d$ that contains $d + 1$ affinely independent points, for example a ball or the corners of a simplex, has $\mathbb{R}^d$ as its affine hull.

## Related definitions

- The [convex hull](/convex-hull/) uses convex combinations, the affine hull affine combinations, the [conic hull](/conic-hull/) nonnegative combinations, and the linear span all combinations. So $\mathrm{conv}(S) \subseteq \mathrm{aff}(S)$ and $\mathrm{cone}(S) \subseteq \mathrm{span}(S)$.
- The *dimension* of a convex set or a polytope is the dimension of its affine hull. A $d$-[polytope](/convex-polytope/) is a polytope of dimension $d$.
- [General position](/general-position/) asks for affine independence of every small enough subset: no three points on a line in the plane, no four on a plane in space.
- [Carathéodory's theorem](/caratheodory-theorem/) writes each point of $\mathrm{conv}(S)$ with affinely independent points of $S$.
- The [rank](/rank/) of the matrix of difference vectors equals the dimension of the affine hull.

## References
