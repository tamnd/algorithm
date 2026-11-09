---
tag: 7DPCNC
kind: definition
slug: polyhedron
name: Polyhedron
aliases:
- polyhedral set
- feasible region
- convex polyhedron
area: optimization/linear-programming
level: intro
summary: Solution set of finitely many linear inequalities; the feasible region of an LP.
prereqs: [convex-set, linear-independence]
see_also: [convex-polytope, basic-feasible-solution, extreme-point, facet, minkowski-weyl-theorem, vertex-enumeration, fourier-motzkin-elimination, linear-programming-problem]
sources:
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Chapter 2, The geometry of linear programming (Section 2.1 polyhedra and convex sets, Section 2.2 extreme points, vertices and basic feasible solutions, Section 2.5 existence of extreme points)
  - book: isbn:9780387943657
    title: Günter M. Ziegler, Lectures on Polytopes, Graduate Texts in Mathematics 152, Springer, 1995
    locator: Chapter 1, Polytopes, polyhedra and cones (the main theorem for polyhedra), and Chapter 2, Faces of polytopes
  - book: isbn:9780471982326
    title: Alexander Schrijver, Theory of Linear and Integer Programming, Wiley, 1986
    locator: Chapter 8, The structure of polyhedra (faces, lineality space, characteristic cone, minimal faces and vertices)
  - paper: doi:10.1112/S0025579300002850
    title: P. McMullen, The maximum numbers of faces of a convex polytope, Mathematika 17, 179 to 184 (1970)
    locator: the upper bound theorem
---

A polyhedron is the set of points of $\mathbb{R}^n$ that satisfy a finite system of linear inequalities $Ax \le b$. It is the feasible region of every [linear program](/linear-programming-problem/), and it is a closed [convex set](/convex-set/). A bounded polyhedron is a *polytope*; by the [Minkowski-Weyl theorem](/minkowski-weyl-theorem/), polytopes are exactly the [convex hulls](/convex-polytope/) of finitely many points. The corners of a polyhedron, its vertices, are the [basic feasible solutions](/basic-feasible-solution/) on which the [simplex method](/simplex-method/) moves.

## Definition

**Polyhedron.** For $A \in \mathbb{R}^{m \times n}$ with rows $a_1^\top, \ldots, a_m^\top$ and $b \in \mathbb{R}^m$,

$$P = P(A, b) = \{ x \in \mathbb{R}^n : a_i^\top x \le b_i \text{ for } i = 1, \ldots, m \}.$$

Each set $\{x : a_i^\top x \le b_i\}$ with $a_i \ne 0$ is a closed *halfspace*, so $P$ is an intersection of finitely many halfspaces, with $m = 0$ giving $P = \mathbb{R}^n$. An equation $a^\top x = \beta$ is the pair $a^\top x \le \beta$, $-a^\top x \le -\beta$, so the feasible set $\{x : Ax = b, x \ge 0\}$ of the [standard form](/lp-standard-form/) is also a polyhedron. A *polytope* is a bounded polyhedron. A *polyhedral cone* is a polyhedron of the form $\{x : Ax \le 0\}$.

**Convexity.** If $x, y \in P$ and $0 \le \lambda \le 1$, then $a_i^\top(\lambda x + (1 - \lambda) y) = \lambda a_i^\top x + (1 - \lambda) a_i^\top y \le b_i$. So $P$ is convex. It is closed as a finite intersection of closed sets.

**Tight rows.** For $x \in P$, let $I(x) = \{ i : a_i^\top x = b_i \}$ be the set of rows that are *tight* (active) at $x$, and $A_{I(x)}$ the submatrix of those rows.

**Faces.** An inequality $w^\top x \le \delta$ is *valid* for $P$ if every point of $P$ satisfies it. A *face* of $P$ is a set $F = P \cap \{x : w^\top x = \delta\}$ for a valid inequality; $P$ itself (with $w = 0$, $\delta = 0$) and $\emptyset$ are faces. Equivalently, a nonempty face is a set $\{x \in P : a_i^\top x = b_i \text{ for } i \in J\}$ for some $J \subseteq \{1, \ldots, m\}$. The dimension of a face is the dimension of its affine hull. A face of dimension 0 is a *vertex*, of dimension 1 an *edge*, and of dimension $\dim P - 1$ a [facet](/facet/).

**Vertex.** A point $x \in P$ is a vertex exactly when $\operatorname{rank} A_{I(x)} = n$. Then $x$ is the unique solution of $A_{I(x)} x = b_{I(x)}$, and it is also an [extreme point](/extreme-point/): it is not $\lambda y + (1 - \lambda) z$ for distinct $y, z \in P$ and $0 < \lambda < 1$. The page [basic feasible solution](/basic-feasible-solution/) proves that these definitions agree. A vertex is *degenerate* if $|I(x)| > n$.

**Lineality and recession.** The *recession cone* of a nonempty $P$ is $\operatorname{rec} P = \{ d : Ad \le 0 \}$, the directions $d$ with $x + t d \in P$ for all $x \in P$ and $t \ge 0$. The *lineality space* is $\{ d : Ad = 0 \}$, the directions of the lines that $P$ contains. $P$ is *pointed* if its lineality space is $\{0\}$, that is, if $\operatorname{rank} A = n$.

**Pointed polyhedra have vertices.** A nonempty polyhedron has a vertex if and only if $\operatorname{rank} A = n$.

*Proof.* If $\operatorname{rank} A < n$, there is $d \ne 0$ with $Ad = 0$. For each $x \in P$, the points $x \pm d$ are in $P$ and $x$ is their midpoint, so $x$ is not extreme, and $P$ has no vertex. Now let $\operatorname{rank} A = n$, and pick $x \in P$ with $r = \operatorname{rank} A_{I(x)}$ as large as possible. Suppose $r < n$. Then there is $d \ne 0$ with $A_{I(x)} d = 0$. Because $\operatorname{rank} A = n$, some row has $a_k^\top d \ne 0$, and $k \notin I(x)$; replacing $d$ by $-d$ if needed, $a_k^\top d > 0$. Let $t^*$ be the smallest $t > 0$ such that $a_i^\top (x + t d) = b_i$ for some $i$ with $a_i^\top d > 0$; it exists because $k$ is such a row, and $t^* > 0$ because those rows are not tight at $x$. The point $x' = x + t^* d$ is in $P$: rows with $a_i^\top d \le 0$ stay satisfied, and the others are satisfied up to $t^*$. All rows of $I(x)$ stay tight, and a new row $i$ with $a_i^\top d > 0$ becomes tight. That row is not in the span of the rows of $I(x)$, since those rows are orthogonal to $d$ and it is not. So $\operatorname{rank} A_{I(x')} > r$, which contradicts the choice of $x$. So $r = n$ and $x$ is a vertex. $\square$

The polyhedron $\{x : Ax = b, x \ge 0\}$ contains the rows $-x_j \le 0$, which have rank $n$, so it has a vertex whenever it is nonempty.

**The number of vertices.** Each vertex is the unique solution of $A_J x = b_J$ for some set $J$ of $n$ rows with $\operatorname{rank} A_J = n$, so $P$ has at most $\binom{m}{n}$ vertices. The *upper bound theorem* of McMullen (1970) gives the exact maximum for a polytope in dimension $n$ with $m$ facets: it is reached by the polar of a cyclic polytope and grows as $\Theta(m^{\lfloor n/2 \rfloor})$ for fixed $n$. In dimension 3 the maximum is $2m - 4$.

## Examples and non-examples

**Examples.**

- *The running pentagon.* $\{x \in \mathbb{R}^2 : x_1 + x_2 \le 4,\ x_1 + 3x_2 \le 9,\ x_1 \le 3,\ x_1 \ge 0,\ x_2 \ge 0\}$ has $m = 5$ rows and 5 vertices, $(0,0)$, $(3,0)$, $(3,1)$, $(3/2, 5/2)$ and $(0,3)$, out of $\binom{5}{2} = 10$ pairs of rows. Of the other five pairs, one, $\{x_1 \le 3, x_1 \ge 0\}$, is parallel, and four meet outside $P$, for example $x_1 + x_2 = 4$ and $x_2 = 0$ at $(4, 0)$.
- *The cube* $[0, 1]^3$: $m = 6$, 8 vertices, 12 edges, 6 facets. Of the $\binom{6}{3} = 20$ triples of rows, 8 give vertices and 12 contain a parallel pair.
- *The standard simplex* $\{x \in \mathbb{R}^n : x \ge 0, \sum_j x_j \le 1\}$: $n + 1$ rows, $n + 1$ vertices.
- *A halfplane* $\{x \in \mathbb{R}^2 : x_1 \ge 0\}$ is a polyhedron with no vertex: its lineality space is the $x_2$ axis.
- *An unbounded pointed polyhedron* $\{x \in \mathbb{R}^2 : x_1 - x_2 \le 1,\ x \ge 0\}$ has the vertices $(0, 0)$ and $(1, 0)$ and the recession cone $\{d \ge 0 : d_1 \le d_2\}$.
- *The empty set*, for example $\{x : x_1 \le 0, -x_1 \le -1\}$, and *the whole space* ($m = 0$) are polyhedra.
- *A degenerate vertex.* The square pyramid with base $[-1,1]^2 \times \{0\}$ and apex $(0, 0, 1)$ has 5 facets, and its apex lies on 4 of them, more than $n = 3$.

**Non-examples.**

- The closed disk $\{x : x_1^2 + x_2^2 \le 1\}$ is convex and closed, but not the intersection of finitely many halfplanes: the boundary of such an intersection lies on finitely many lines, each line meets the circle in at most two points, and so the boundary cannot contain the whole circle.
- The open square $(0, 1)^2$ is not closed.
- The union $[0, 1] \cup [2, 3]$ is not convex.
- $\{x \in \mathbb{R}^2 : x_1 x_2 \ge 1, x \ge 0\}$ is convex and closed, but its boundary is a curve.
- The set of integer points of a polyhedron is not a polyhedron, except in trivial cases. Its convex hull is one when the data are rational; see the [integer hull](/integer-hull/).

## Related definitions

- [Convex polytope](/convex-polytope/): a bounded polyhedron, or equivalently the convex hull of finitely many points; the [Minkowski-Weyl theorem](/minkowski-weyl-theorem/) proves the equivalence and its version for cones.
- [Extreme point](/extreme-point/), [facet](/facet/) and [supporting hyperplane](/supporting-hyperplane/): the faces of a convex set in general.
- [Basic feasible solution](/basic-feasible-solution/): a vertex of a polyhedron in standard form, described by a basis.
- [Vertex enumeration](/vertex-enumeration/): list all vertices of $P(A, b)$. The opposite task, from points to inequalities, is the [convex hull problem](/convex-hull-problem/).
- [Fourier-Motzkin elimination](/fourier-motzkin-elimination/): the projection of a polyhedron to fewer coordinates is again a polyhedron.
- [Linear feasibility](/linear-feasibility/): decide whether $P(A, b)$ is empty.

## References
