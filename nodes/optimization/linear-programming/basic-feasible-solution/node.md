---
tag: KC6752
kind: concept
slug: basic-feasible-solution
name: Basic feasible solution
aliases:
- BFS
- Extreme point (basic) solution
- basic feasible solution
- extreme point
- vertex
- vertex solution
- basic solution
- basis
area: optimization/linear-programming
level: core
summary: A feasible point determined by a set of linearly independent active constraints; the vertices of the feasible region.
prereqs: [lp-standard-form, polyhedron, linear-independence]
see_also: [fundamental-theorem-of-lp, simplex-method, pivot-operation, lp-degeneracy, vertex-enumeration, extreme-point, reduced-cost, total-unimodularity]
sources:
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Section 2.2, Extreme points, vertices, and basic feasible solutions (the equivalence of the three definitions), Section 2.3, Polyhedra in standard form, and Section 2.4, Degeneracy
  - book: isbn:9783540306979
    title: Jiří Matoušek and Bernd Gärtner, Understanding and Using Linear Programming, Springer, 2007
    locator: Chapter 4, Section 4.2 (basic feasible solutions) and Section 4.4 (vertices and basic feasible solutions)
  - book: isbn:9780471982326
    title: Alexander Schrijver, Theory of Linear and Integer Programming, Wiley, 1986
    locator: Chapter 8, The structure of polyhedra (minimal faces and vertices), and Chapter 11, The simplex method
---

A basic feasible solution of a linear program in [standard form](/lp-standard-form/) $Ax = b$, $x \ge 0$ is a feasible point whose nonzero coordinates belong to a set of linearly independent columns of $A$. These points are exactly the vertices of the feasible [polyhedron](/polyhedron/), and also exactly its extreme points, so three different views, algebra, geometry and convexity, describe the same finite set. The [fundamental theorem of linear programming](/fundamental-theorem-of-lp/) says that an optimum, if one exists, is found among them, and the [simplex method](/simplex-method/) moves from one to the next.

## In plain words

The allowed region of a linear program has corners, and the best answer always sits at a corner. A corner is a point where enough of the limits are exactly met to pin the point down: in the plane, two lines that cross; in space, three planes.

The algebra gives a recipe for corners. Pick as many variables as there are equations, set all the other variables to zero, and solve the equations for the picked ones. If the solution exists, it is called basic. If all its values are also nonnegative, it is a corner of the region. There are only finitely many ways to pick, so there are only finitely many corners, and a computer can list them or walk between them.

## The idea

**Setting.** $P = \{x \in \mathbb{R}^n : Ax = b,\ x \ge 0\}$ with $A \in \mathbb{R}^{m \times n}$ of rank $m$. Write $A_j$ for column $j$ and $A_S$ for the columns with index in $S$.

**Basis and basic solution.** A *basis* is a set $B \subseteq \{1, \ldots, n\}$ of $m$ indices such that the $m \times m$ matrix $A_B$ is nonsingular. The *basic solution* of $B$ is the unique $x$ with $x_j = 0$ for $j \notin B$ and $A_B x_B = b$, that is $x_B = A_B^{-1} b$. The variables $x_j$, $j \in B$, are *basic*, the others *nonbasic*. The basic solution is a *basic feasible solution* (BFS) if also $x_B \ge 0$. It is *degenerate* if some basic variable is zero.

**Three equal definitions.** For $x \in P$ with support $S = \{ j : x_j > 0 \}$, the following are equivalent:

1. *(vertex)* the constraints that are tight at $x$ have rank $n$;
2. *(extreme point)* $x$ is not $\lambda y + (1 - \lambda) z$ for $y \ne z$ in $P$ and $0 < \lambda < 1$;
3. *(basic feasible solution)* the columns $A_S$ are linearly independent, or equivalently, $x$ is the basic solution of some basis $B \supseteq S$.

*Proof.* (1 ⇔ 3) The constraints tight at $x$ are the $m$ rows of $Ax = b$ and the rows $x_j \ge 0$ for $j \notin S$. Their matrix has rank $n$ exactly when its null space is $\{0\}$, that is, when $Ad = 0$ and $d_j = 0$ for all $j \notin S$ force $d = 0$. That says $A_S d_S = 0$ only for $d_S = 0$, which is the independence of $A_S$.

(3 ⇒ 2) Let $A_S$ be independent and $x = \lambda y + (1 - \lambda) z$ with $y, z \in P$ and $0 < \lambda < 1$. For $j \notin S$, $0 = x_j = \lambda y_j + (1 - \lambda) z_j$ with $y_j, z_j \ge 0$, so $y_j = z_j = 0$. Then $A_S y_S = b = A_S x_S$, and independence gives $y_S = x_S$. So $y = x$, and in the same way $z = x$.

(2 ⇒ 3) If $A_S$ is dependent, take $d \ne 0$ with $d_j = 0$ for $j \notin S$ and $A d = 0$. Since $x_j > 0$ on $S$, there is $\varepsilon > 0$ with $x \pm \varepsilon d \ge 0$, and $A(x \pm \varepsilon d) = b$. So $x$ is the midpoint of two distinct points of $P$ and is not extreme.

(The two forms of 3.) If $A_S$ is independent, then $|S| \le m$, and because $A$ has rank $m$, $S$ extends to a set $B$ of $m$ independent columns; $x$ satisfies $x_j = 0$ off $B$ and $A_B x_B = b$, so it is the basic solution of $B$. Conversely the support of a basic solution lies in a basis, and a subset of independent columns is independent. $\square$

**Consequences.**

- *Finitely many.* Each BFS is the basic solution of at least one basis, and there are at most $\binom{n}{m}$ bases. So $P$ has at most $\binom{n}{m}$ vertices.
- *Sparse.* A BFS has at most $m$ nonzero coordinates. This is the source of many rounding arguments, for example that an optimal vertex of a scheduling LP has few fractional values.
- *Many bases, one vertex.* A nondegenerate BFS has $|S| = m$ and exactly one basis, $B = S$. A degenerate BFS with $|S| < m$ can belong to several bases, and the simplex method can [pivot](/pivot-operation/) between them without moving; see [degeneracy](/lp-degeneracy/).
- *Adjacency.* Two bases are *adjacent* if they differ in one index. A pivot moves from a basis to an adjacent one. Two distinct BFSs of adjacent bases are the ends of an edge of $P$.
- *Exact size.* By [Cramer's rule](/cramers-rule/), each coordinate of a BFS is a ratio of two subdeterminants of $(A \mid b)$. With integer data, a BFS is integral whenever every basis has $\det A_B = \pm 1$, which is the idea behind [total unimodularity](/total-unimodularity/).

**General polyhedra.** For $P = \{x : Ax \le b\}$ in $\mathbb{R}^n$, a *basic solution* is a point where $n$ linearly independent constraints are tight (the others may be violated), and a basic feasible solution is one in $P$. By definition 1 above, the basic feasible solutions are the vertices, and a polyhedron with a line in it has none.

## Examples

**The running example in standard form.** For $\max 3x_1 + 2x_2$ subject to $x_1 + x_2 \le 4$, $x_1 + 3x_2 \le 9$, $x_1 \le 3$, $x \ge 0$, the standard form has the slacks $s_1, s_2, s_3$, so $n = 5$, $m = 3$ and $\binom{5}{3} = 10$ candidate bases. All 10 sets, with the basic solution $(x_1, x_2, s_1, s_2, s_3)$:

| basis | basic solution | status |
|---|---|---|
| $x_1, x_2, s_2$ | $(3, 1, 0, 3, 0)$ | BFS, objective 11 (optimal) |
| $x_1, x_2, s_3$ | $(3/2, 5/2, 0, 0, 3/2)$ | BFS, objective 19/2 |
| $x_1, s_1, s_2$ | $(3, 0, 1, 6, 0)$ | BFS, objective 9 |
| $x_2, s_1, s_3$ | $(0, 3, 1, 0, 3)$ | BFS, objective 6 |
| $s_1, s_2, s_3$ | $(0, 0, 4, 9, 3)$ | BFS, objective 0 |
| $x_1, x_2, s_1$ | $(3, 2, -1, 0, 0)$ | basic, not feasible |
| $x_1, s_1, s_3$ | $(9, 0, -5, 0, -6)$ | basic, not feasible |
| $x_1, s_2, s_3$ | $(4, 0, 0, 5, -1)$ | basic, not feasible |
| $x_2, s_2, s_3$ | $(0, 4, 0, -3, 3)$ | basic, not feasible |
| $x_2, s_1, s_2$ | none | $A_B$ singular: no row involves $x_1$ |

The five BFSs are the five corners of the pentagon. The four infeasible basic solutions are the crossings of two boundary lines outside the pentagon, for example $(3, 2)$ where $x_1 = 3$ meets $x_1 + 3x_2 = 9$.

**One vertex, three bases.** Change the second constraint to $x_1 + 3x_2 \le 6$. The point $(x_1, x_2) = (3, 1)$ now has $s_1 = s_2 = s_3 = 0$, its support is $\{x_1, x_2\}$ with $|S| = 2 < m = 3$, and each of the three bases $\{x_1, x_2, s_i\}$ gives this same degenerate BFS.

**A feasible point that is not basic.** In the running example, $x = (2, 1)$ with slacks $(1, 4, 1)$ has support of size 5 > 3, so its columns are dependent. It is the midpoint of $(2, 1) \pm (1, 0)$, which are both feasible.

**A polyhedron with no BFS.** $\{x \in \mathbb{R}^2 : x_1 + x_2 \le 1\}$ contains the line $x_1 + x_2 = 0$ in the direction $(1, -1)$, so no point has two independent tight constraints. In standard form, with free variables split as $x_j = x_j^+ - x_j^-$, the converted polyhedron does have BFSs, for example $x^+ = x^- = 0$, $s = 1$.

## Where it is used

- [Fundamental theorem of linear programming](/fundamental-theorem-of-lp/): if an optimum exists, some BFS is optimal.
- [Simplex method](/simplex-method/), [revised simplex](/revised-simplex-method/) and [dual simplex](/dual-simplex-method/): they store a basis and move between adjacent bases by [pivots](/pivot-operation/); the [slack form](/lp-slack-form/) is the program written for one basis.
- [Reduced costs](/reduced-cost/): computed for a basis, they test whether its BFS is optimal.
- [Vertex enumeration](/vertex-enumeration/): list all BFSs, for example by trying all $\binom{n}{m}$ bases.
- [Total unimodularity](/total-unimodularity/) and the [integrality theorem](/flow-integrality-theorem/): integral bases give integral optimal vertices, so flow LPs have integral optima.
- [LP rounding](/linear-programming-rounding/): a BFS has at most $m$ nonzero values, which bounds the number of fractional values to round.

## References
