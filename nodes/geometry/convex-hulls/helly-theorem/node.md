---
tag: CT6YW9
kind: theorem
slug: helly-theorem
name: Helly's theorem
aliases:
- Helly's theorem on convex sets
- Helly theorem
- Helly's intersection theorem
area: geometry/convex-hulls
level: core
summary: If every d+1 members of a finite family of convex sets in R^d intersect, the whole family intersects.
prereqs: [convex-set, radon-theorem]
see_also: [caratheodory-theorem, helly-property-intervals, lp-type-problem, seidel-linear-programming, minimum-enclosing-circle, linear-feasibility, interval-piercing, convex-hull]
sources:
  - book: isbn:9780387953748
    title: Jiri Matousek, Lectures on Discrete Geometry, Graduate Texts in Mathematics 212, Springer, 2002
    locator: Chapter 1, Section 1.3, Radon's lemma and Helly's theorem, and Chapter 1, Section 1.4, centerpoints
  - paper: "Eduard Helly, Über Mengen konvexer Körper mit gemeinsamen Punkten, Jahresbericht der Deutschen Mathematiker-Vereinigung 32, 1923"
    locator: the theorem for convex sets in n dimensions
  - paper: doi:10.1007/BF01464231
    title: Johann Radon, Mengen konvexer Körper, die einen gemeinsamen Punkt enthalten, Mathematische Annalen 83, 1921
    locator: the first published proof of Helly's theorem, by the partition lemma
  - paper: "Ludwig Danzer, Branko Grünbaum and Victor Klee, Helly's theorem and its relatives, in Convexity, Proceedings of Symposia in Pure Mathematics 7, American Mathematical Society, 1963"
    locator: the survey of variants, including the infinite version and the colorful and fractional forms that followed
---

Helly's theorem says that for convex sets in $\mathbb{R}^d$, a common point of the whole family is guaranteed by common points of all its small subfamilies: if every $d + 1$ of the sets intersect, all of them intersect. On the line this is the familiar fact that pairwise intersecting intervals share a point. The theorem turns a global question into many local ones of fixed size, which is why it underlies the combinatorial dimension of linear programming and other [LP-type problems](/lp-type-problem/), the existence of centerpoints, and many piercing and covering results.

## Statement

**Theorem (Helly, 1913).** Let $C_1, \ldots, C_m$ be convex sets in $\mathbb{R}^d$ with $m \ge d + 1$. If every $d + 1$ of them have a common point, then

$$C_1 \cap C_2 \cap \cdots \cap C_m \ne \emptyset.$$

The sets need not be closed or bounded, and no [general position](/general-position/) is assumed. Repeated sets are allowed.

**Theorem (infinite version).** Let $\mathcal{F}$ be a family, possibly infinite, of compact convex sets in $\mathbb{R}^d$. If every $d + 1$ members of $\mathcal{F}$ have a common point, then all members of $\mathcal{F}$ have a common point.

Notation: $d$ is the dimension, $m$ the number of sets, and a family is a list of sets. For the consequences below, $P$ is a finite point set with $n = |P|$, and a closed half-space is a set $\{x : \langle a, x \rangle \le b\}$ with $a \ne 0$.

## In plain words

Suppose you have many convex shapes, such as discs, triangles or half-planes, drawn on a sheet of paper. You want to know if one point lies in all of them. Helly's theorem says that it is enough to look at three shapes at a time. If every choice of three shapes has a point in common, then there is a point in all of them.

In space the number is four, and in general it is one more than the number of dimensions. On a line it is two: if every two intervals overlap, there is a point in all the intervals.

The shapes must be convex. For shapes with holes or several pieces, every small group can overlap while the whole family has no common point.

## Proof

**Finite version.** Induction on $m$. For $m = d + 1$ the hypothesis is the claim. Let $m \ge d + 2$ and assume the theorem for $m - 1$ sets.

1. **Points that miss one set.** For each $i \in \{1, \ldots, m\}$, the family without $C_i$ has $m - 1 \ge d + 1$ sets, and every $d + 1$ of them intersect. By the induction hypothesis there is a point
$$p_i \in \bigcap_{j \ne i} C_j.$$
2. **Radon partition.** The $m \ge d + 2$ points $p_1, \ldots, p_m$ (some may be equal) have, by [Radon's theorem](/radon-theorem/), a partition of the indices into nonempty sets $I$ and $J$ and a point
$$x \in \operatorname{conv}\{p_i : i \in I\} \cap \operatorname{conv}\{p_j : j \in J\}.$$
3. **$x$ is in every set.** Fix $k$. If $k \in I$, then $k \notin J$, so every $p_j$ with $j \in J$ lies in $C_k$ by step 1. $C_k$ is convex, so it contains $\operatorname{conv}\{p_j : j \in J\}$, and hence $x \in C_k$. If $k \in J$, the same argument with $I$ gives $x \in C_k$.

So $x$ lies in all $m$ sets, which completes the induction.

**Infinite version.** By the finite version, every finite subfamily of $\mathcal{F}$ has a common point. Fix one member $K \in \mathcal{F}$. The sets $K \cap C$ for $C \in \mathcal{F}$ are closed subsets of the compact set $K$, and every finite number of them intersect. A family of closed subsets of a compact set with this finite intersection property has a nonempty intersection. So $\bigcap \mathcal{F} \ne \emptyset$. $\blacksquare$

## Consequences

- **Intervals.** For $d = 1$: if every two intervals of a finite family on the line intersect, all of them do. Directly, the largest left end point is at most the smallest right end point, and that point is common. See [the Helly property of intervals](/helly-property-intervals/) and [interval piercing](/interval-piercing/).
- **Infeasible linear systems.** If a system of $m$ linear inequalities in $d$ variables has no solution, then some $d + 1$ of the inequalities already have no solution. Apply the theorem to the $m$ half-spaces. This is a finite certificate of [infeasibility](/linear-feasibility/), of size independent of $m$.
- **Combinatorial dimension of linear programming.** Let a linear program $\min \langle c, x \rangle$ over $m$ half-spaces in $\mathbb{R}^d$ be feasible with optimum value $v$. Add the convex set $\{x : \langle c, x \rangle < v\}$. The $m + 1$ sets have no common point, so some $d + 1$ of them have none. These must include the added set, because any $d + 1$ constraints alone are feasible. So some $d$ constraints alone have optimum at least $v$, and so exactly $v$. This bound on the size of a basis is what makes linear programming an [LP-type problem](/lp-type-problem/) of combinatorial dimension $d$, and it drives [Seidel's algorithm](/seidel-linear-programming/) and Clarkson's algorithms.
- **Enclosing balls.** A finite set $P \subset \mathbb{R}^d$ fits in a closed ball of radius $r$ exactly when every $d + 1$ points of $P$ do. Apply the theorem to the balls of radius $r$ centred at the points of $P$: a common point is the centre of a ball of radius $r$ that contains $P$. So the [minimum enclosing ball](/minimum-enclosing-circle/) is fixed by at most $d + 1$ points of $P$.
- **Centerpoints.** For every finite $P \subset \mathbb{R}^d$ with $n$ points there is a point $c$ such that every closed half-space containing $c$ contains at least $n / (d + 1)$ points of $P$. Proof: let the family be the hulls $\operatorname{conv} Q$ of all $Q \subseteq P$ with $|Q| > dn/(d+1)$. Each such $Q$ misses fewer than $n/(d+1)$ points, so any $d + 1$ of them miss fewer than $n$ points together and share a point of $P$. By the theorem there is a point $c$ in all these hulls. If a closed half-space $H \ni c$ had fewer than $n/(d+1)$ points, the open complement of $H$ would hold a set $Q$ with $|Q| > dn/(d+1)$, and $c \in \operatorname{conv} Q$ would lie in that open complement, a contradiction.
- **Stronger forms.** The colorful Helly theorem (Lovász, published by Bárány in 1982): if $d + 1$ finite families are given and every choice of one set from each family intersects, then one of the families has a common point. The fractional Helly theorem (Katchalski and Liu, 1979): if a positive fraction of the $(d+1)$-subfamilies intersect, then a positive fraction of the sets have a common point. Both are proved in Matoušek's book.

## Tightness

- **$d + 1$ cannot be lowered to $d$.** The $d + 1$ facets of a simplex in $\mathbb{R}^d$ are convex. Any $d$ of them share the vertex opposite the missing facet, but all $d + 1$ have no common point. In the plane: the three sides of a triangle meet pairwise at the corners, but no point is on all three sides.
- **Convexity is needed.** On the line, the sets $\{0, 1\}$, $\{1, 2\}$ and $\{0, 2\}$ meet pairwise, but no point is in all three.
- **Compactness is needed in the infinite version.** The closed half-lines $[i, \infty)$ for $i = 1, 2, \ldots$ are convex and every finite subfamily intersects, but no point is in all of them. Boundedness alone does not help either: the open intervals $(0, 1/i)$ have the same behavior. In both examples $d + 1 = 2$ sets always intersect, so only the missing compactness breaks the conclusion.

## History

Eduard Helly proved the theorem in 1913 and told Johann Radon about it. Radon published the first proof in 1921, using the partition lemma now called [Radon's theorem](/radon-theorem/). Helly's own paper appeared in 1923, and Dénes König gave another proof in 1922. Danzer, Grünbaum and Klee surveyed the many relatives of the theorem in 1963. In computational geometry the theorem became the base of the analysis of linear programming in fixed dimension and of LP-type problems in the 1980s and 1990s.

## References
