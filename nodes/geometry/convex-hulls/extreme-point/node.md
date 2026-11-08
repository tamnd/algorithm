---
tag: MS27VV
kind: definition
slug: extreme-point
name: Extreme point
aliases:
- vertex of a convex set
- extreme points
area: geometry/convex-hulls
level: intro
summary: A point of a convex set that is not a convex combination of two other distinct points of the set.
prereqs: [convex-set, convex-combination]
see_also: [convex-hull, supporting-hyperplane, support-function, facet, caratheodory-theorem, minkowski-weyl-theorem, basic-feasible-solution, fundamental-theorem-of-lp]
sources:
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 3, the definitions of convexity and the naive algorithms that find the extreme points and extreme edges of a planar set
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 3, Convex Hulls, Basic Algorithms (the extreme points problem and its relation to the convex hull problem)
  - book: isbn:9780691015866
    title: R. Tyrrell Rockafellar, Convex Analysis, Princeton University Press, 1970 (Princeton Landmarks in Mathematics edition, 1997)
    locator: Section 18, Extreme Points and Faces of Convex Sets
---

An extreme point of a [convex set](/convex-set/) $C$ is a point of $C$ that is not in the open segment between two other points of $C$. The extreme points of a finite point set are the corners of its [convex hull](/convex-hull/), and finding them is the extreme points problem, the unordered form of the [convex hull problem](/convex-hull-problem/). In linear programming the extreme points of the feasible region are the [basic feasible solutions](/basic-feasible-solution/), and an optimum is always attained at one of them when one exists.

## Definition

Let $C \subseteq \mathbb{R}^d$ be convex. A point $x \in C$ is an **extreme point** of $C$ if for all $a, b \in C$ and all $\lambda$ with $0 < \lambda < 1$,

$$x = \lambda a + (1 - \lambda) b \implies a = b = x.$$

The set of extreme points is written $\operatorname{ext}(C)$. An equivalent form: $x \in C$ is extreme if and only if $C \setminus \{x\}$ is convex.

For a finite set $P$ of points, the extreme points of $P$ are the extreme points of $\operatorname{conv}(P)$. Three facts make this the right notion for algorithms.

**Fact 1.** $\operatorname{ext}(\operatorname{conv} P) \subseteq P$.

*Proof.* Each $x \in \operatorname{conv} P$ is a [convex combination](/convex-combination/) $x = \sum_i \mu_i p_i$ of points of $P$ with all $\mu_i > 0$. If some $p_i$ differs from $x$, call it $p_1$. Then $0 < \mu_1 < 1$, and $x = \mu_1 p_1 + (1 - \mu_1) r$ with $r = \sum_{i \ge 2} \mu_i p_i / (1 - \mu_1) \in \operatorname{conv} P$. If $r = p_1$ then $x = p_1$, which is false, so $r \ne p_1$ and $x$ is not extreme. So an extreme $x$ is a combination of a single point of $P$, that is, $x \in P$. $\square$

**Fact 2.** A point $p \in P$ is an extreme point of $P$ if and only if $p \notin \operatorname{conv}(P \setminus \{p\})$.

*Proof.* If $p = \sum_i \lambda_i q_i$ with $q_i \in P \setminus \{p\}$, the argument of Fact 1 with $q_1 \ne p$ writes $p$ as a point of an open segment between two distinct points of $\operatorname{conv} P$. Conversely, let $p = \lambda a + (1 - \lambda) b$ with $a \ne b$ in $\operatorname{conv} P$ and $0 < \lambda < 1$. Write $a = \sum \alpha_q q$ and $b = \sum \beta_q q$ over $q \in P$, so $p = \sum \mu_q q$ with $\mu_q = \lambda \alpha_q + (1 - \lambda) \beta_q$. If $\mu_p = 1$, then $\alpha_p = \beta_p = 1$ and $a = b = p$, which is false. So $\mu_p < 1$ and $p = \sum_{q \ne p} \mu_q q / (1 - \mu_p) \in \operatorname{conv}(P \setminus \{p\})$. $\square$

**Fact 3.** $\operatorname{conv} P = \operatorname{conv}(\operatorname{ext} P)$.

*Proof.* Let $E = \operatorname{ext} P$, a subset of $P$ by Fact 1. Remove the points of $P \setminus E$ one at a time, and let $Q$ be the current set before a removal of $q$. By induction $\operatorname{conv} Q = \operatorname{conv} P$, so $\operatorname{ext}(\operatorname{conv} Q) = E$ and $q$ is not extreme in $Q$. By Fact 2, $q \in \operatorname{conv}(Q \setminus \{q\})$, so the removal does not change the hull. At the end the set is $E$. $\square$

Fact 3 is the finite case of Minkowski's theorem: a compact convex set in $\mathbb{R}^d$ is the convex hull of its extreme points. The Krein-Milman theorem extends it to compact convex sets in locally convex spaces, with a closure. The bounded case of the [Minkowski-Weyl theorem](/minkowski-weyl-theorem/) is the same statement for polytopes given by inequalities.

**Planar test.** In the plane, [Carathéodory's theorem](/caratheodory-theorem/) gives: $p \in P$ is not extreme if and only if $p$ lies in a closed triangle of three other points of $P$, or on a closed segment of two other points of $P$. Testing every point against every triangle with the [orientation test](/orientation-test/) finds the extreme points in $O(n^4)$ time. This is the slow reference that the fast hull algorithms are tested against.

## Examples and non-examples

- **A finite set.** Let $P = \{(0,0), (6,0), (6,4), (0,4), (3,4), (2,1), (5,2), (3,0)\}$. The extreme points are the four corners $(0,0)$, $(6,0)$, $(6,4)$, $(0,4)$. The point $(3,4)$ is the midpoint of $(0,4)$ and $(6,4)$, and $(3,0)$ is the midpoint of $(0,0)$ and $(6,0)$. The points $(2,1)$ and $(5,2)$ lie strictly inside the triangle $(0,0), (6,0), (6,4)$: for $(2,1)$ the three orientation determinants are $6$, $16$ and $2$, and for $(5,2)$ they are $12$, $4$ and $8$, all positive.
- **A disk.** Every point of the boundary circle of a closed disk is extreme, so a compact convex set can have infinitely many extreme points.
- **Non-example: a point on an edge.** The midpoint of a side of a square lies on the open segment between two corners, so it is not extreme.
- **Non-example: unbounded or open sets.** A closed half-plane, a line and an open disk have no extreme points. Minkowski's theorem needs compactness.
- **Extreme but not exposed.** A point $x$ of $C$ is *exposed* if some [supporting hyperplane](/supporting-hyperplane/) meets $C$ only at $x$. Every exposed point is extreme. The converse fails: in the stadium $\operatorname{conv}(B_1 \cup B_2)$ of the unit disks $B_1$ and $B_2$ centered at $(0,0)$ and $(2,0)$, the point $(0,1)$ is extreme, but the only supporting line there is $y = 1$, which meets the set in the whole segment from $(0,1)$ to $(2,1)$. For a polytope, extreme points, exposed points and vertices (faces of dimension 0) are the same points.
- **Extreme in a direction.** For a direction $u$, a point of $P$ that maximizes $\langle u, p \rangle$ is called extreme in direction $u$. If the maximizer is unique, it is an exposed point, hence extreme. If it is not unique, a maximizer can lie in the middle of an edge: for $P$ above and $u = (0, 1)$, the maximizers are $(0,4)$, $(3,4)$ and $(6,4)$, and $(3,4)$ is not extreme. The [support function](/support-function/) is the maximum value.

## Related definitions

- [Convex set](/convex-set/), [convex combination](/convex-combination/) and [convex hull](/convex-hull/): the setting of the definition.
- [Supporting hyperplane](/supporting-hyperplane/) and [support function](/support-function/): exposed points and extreme points in a direction.
- [Facet](/facet/): the faces of the other extreme dimension; the vertices are the faces of dimension 0.
- [Upper and lower hull](/upper-and-lower-hull/): the two chains that join the extreme points of a planar set from left to right.
- [Carathéodory's theorem](/caratheodory-theorem/): the reason why a test against triangles suffices in the plane.
- [Basic feasible solution](/basic-feasible-solution/) and the [fundamental theorem of linear programming](/fundamental-theorem-of-lp/): extreme points of a polyhedron given by inequalities.

## References
