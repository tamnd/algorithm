---
tag: NVQDHC
kind: theorem
slug: fundamental-theorem-of-lp
name: Fundamental theorem of linear programming
aliases:
- fundamental theorem of LP
area: optimization/linear-programming
level: core
summary: If a bounded feasible LP has an optimum, some optimal solution is a basic feasible solution.
prereqs: [basic-feasible-solution, lp-standard-form]
see_also: [linear-programming-problem, simplex-method, vertex-enumeration, polyhedron, strong-duality, lp-degeneracy]
sources:
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Section 2.5, Existence of extreme points, and Section 2.6, Optimality of extreme points
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 29.5, The initial basic feasible solution (the fundamental theorem of linear programming in the form infeasible, unbounded or a finite optimum)
  - book: isbn:9783540306979
    title: Jiří Matoušek and Bernd Gärtner, Understanding and Using Linear Programming, Springer, 2007
    locator: Chapter 4, Section 4.2 (a feasible bounded program in equational form has an optimal basic feasible solution)
  - book: isbn:9780471982326
    title: Alexander Schrijver, Theory of Linear and Integer Programming, Wiley, 1986
    locator: Chapter 8, The structure of polyhedra (minimal faces, and the optimum of a linear function over a polyhedron)
---

The fundamental theorem of linear programming says that a linear program in [standard form](/lp-standard-form/) is infeasible, unbounded, or has an optimal solution, and that in the last case some optimal solution is a [basic feasible solution](/basic-feasible-solution/). So a finite infimum is always attained, and it is attained at a vertex of the feasible [polyhedron](/polyhedron/). The theorem turns a continuous problem into a finite one: it is enough to search the finitely many bases, which is what the [simplex method](/simplex-method/) and brute-force [vertex enumeration](/vertex-enumeration/) do.

## Statement

Let $A \in \mathbb{R}^{m \times n}$ have rank $m$, let $b \in \mathbb{R}^m$ and $c \in \mathbb{R}^n$, and consider

$$\text{minimize } c^\top x \quad \text{subject to } x \in P = \{x \in \mathbb{R}^n : Ax = b,\ x \ge 0\}.$$

**Theorem.**

1. If $P \ne \emptyset$, then $P$ has a basic feasible solution.
2. If $P \ne \emptyset$ and $c^\top x$ is bounded below on $P$, then the program has an optimal solution, and some basic feasible solution is optimal.
3. Consequently exactly one of these holds: $P = \emptyset$; $\inf_{x \in P} c^\top x = -\infty$; or the minimum is attained at a basic feasible solution.

The rank condition costs nothing: if $Ax = b$ is solvable, the dependent rows can be dropped without a change of $P$. The same statements hold for a maximization, with "bounded above".

**General polyhedra.** If $P = \{x : Ax \le b\}$ with $\operatorname{rank} A = n$ (a pointed polyhedron) and $\min c^\top x$ over $P$ has an optimal solution, then some vertex of $P$ is optimal.

## In plain words

A linear program can go wrong in only two ways: no choice satisfies all the limits, or the objective can be pushed down forever. If neither happens, there is a best choice, and one of the corners of the region is a best choice.

The proof is a sliding argument. Start at any allowed point that is not a corner. Some straight line through it stays inside the region for a while. Slide along that line in the direction where the objective does not get worse, until you hit a new wall. You now touch one more wall than before. Repeat. After a bounded number of slides you are at a corner, and the corner is at least as good as where you started. So the best corner is at least as good as every point.

## Proof

**Lemma.** Let $x \in P$ and assume that $c^\top$ is bounded below on $P$. Then there is a basic feasible solution $x'$ with $c^\top x' \le c^\top x$.

*Proof.* Induction on $|S|$, where $S = \{j : x_j > 0\}$ is the support of $x$.

If the columns $A_S$ are linearly independent, $x$ is a basic feasible solution by the equivalence proved on the [basic feasible solution](/basic-feasible-solution/) page; take $x' = x$. This covers $S = \emptyset$.

Otherwise there is $d \ne 0$ with $Ad = 0$ and $d_j = 0$ for $j \notin S$. Choose the sign of $d$ as follows: if $c^\top d \ne 0$, make $c^\top d < 0$; if $c^\top d = 0$, make $d$ have a negative coordinate (one of $d$ and $-d$ has one, since $d \ne 0$). Now $c^\top d \le 0$ in both cases.

*Case $d \ge 0$.* Then $c^\top d < 0$ by the choice of sign. For each $t \ge 0$, $A(x + t d) = b$ and $x + t d \ge 0$, so $x + t d \in P$, and $c^\top (x + t d) = c^\top x + t\, c^\top d \to -\infty$. This contradicts the bound. So this case does not occur.

*Case $d_j < 0$ for some $j$.* Let

$$t^* = \min_{j : d_j < 0} \frac{x_j}{-d_j}.$$

Each $j$ with $d_j < 0$ is in $S$, so $x_j > 0$ and $t^* > 0$. Let $x'' = x + t^* d$. Then $Ax'' = b$. For $j$ with $d_j \ge 0$, $x''_j \ge x_j \ge 0$; for $j$ with $d_j < 0$, $x''_j = x_j - t^* (-d_j) \ge 0$ by the choice of $t^*$, with equality for the index that attains the minimum. So $x'' \in P$. Off $S$, $d_j = 0$ and $x''_j = 0$. So the support of $x''$ is a proper subset of $S$. Also $c^\top x'' = c^\top x + t^* c^\top d \le c^\top x$. By the induction hypothesis there is a basic feasible solution $x'$ with $c^\top x' \le c^\top x'' \le c^\top x$. $\square$

**Part 1.** Take $c = 0$, which is bounded below, and any $x \in P$. The lemma gives a basic feasible solution.

**Part 2.** By part 1, the set $V$ of basic feasible solutions is not empty, and it is finite, since each one is the basic solution of one of at most $\binom{n}{m}$ bases. Let $v^* \in V$ minimize $c^\top v$ over $V$. For each $x \in P$, the lemma gives $x' \in V$ with $c^\top x \ge c^\top x' \ge c^\top v^*$. So $v^*$ is optimal, and it is a basic feasible solution.

**Part 3.** If $P \ne \emptyset$ and $c^\top$ is not bounded below, the infimum is $-\infty$. Otherwise part 2 applies. The three cases exclude each other by their definitions.

**The general polyhedron.** Let $x$ be optimal for $\min c^\top x$ over $P = \{x : Ax \le b\}$ with $\operatorname{rank} A = n$, chosen so that the rank $r$ of the rows tight at $x$ is as large as possible. Suppose $r < n$, and take $d \ne 0$ orthogonal to all tight rows. For small $\varepsilon > 0$ both $x \pm \varepsilon d$ are in $P$, so optimality forces $c^\top d = 0$. Because $\operatorname{rank} A = n$, some row has $a_k^\top d \ne 0$; with the sign of $d$ chosen so that some row has $a_k^\top d > 0$, move from $x$ along $d$ until the first such row becomes tight. The new point is in $P$, it has the same objective value, so it is optimal, and its tight rows have rank $r + 1$, because the new row is not orthogonal to $d$. This contradicts the choice of $x$, so $r = n$ and $x$ is a vertex. $\blacksquare$

## Consequences

- **The simplex method is a finite search.** The [simplex method](/simplex-method/) searches only basic feasible solutions, and part 2 says this loses nothing. With an anti-cycling rule such as [Bland's rule](/bland-rule/) it visits each basis at most once and stops.
- **Brute force is correct.** [Vertex enumeration](/vertex-enumeration/) over all $\binom{n}{m}$ bases solves every bounded feasible LP. This is the reference solver in the tests of the LP pages.
- **Rational, small optima.** With rational data, an optimal BFS is $A_B^{-1} b$ for a basis $B$, so it is rational and, by [Cramer's rule](/cramers-rule/), its size is polynomial in the input size. This is a step of the proof that [linear programming is in P](/lp-in-p/).
- **Integral optima.** If every basis has $\det A_B = \pm 1$ and $b$ is integral, an optimal solution is integral; see [total unimodularity](/total-unimodularity/) and the [integrality theorem](/flow-integrality-theorem/) for flows.
- **Duality.** Applied to the dual, the theorem gives an optimal dual vertex, and the termination of the simplex method gives a proof of [strong duality](/strong-duality/).
- **Combinatorial rounding.** An optimal BFS has at most $m$ nonzero coordinates, which [LP rounding](/linear-programming-rounding/) uses.

## Tightness

- *Not every optimum is basic.* With the objective $\max x_1 + x_2$ on the running pentagon $x_1 + x_2 \le 4$, $x_1 + 3x_2 \le 9$, $x_1 \le 3$, $x \ge 0$, each point of the edge from $(3, 1)$ to $(3/2, 5/2)$ is optimal. The theorem promises only that *some* optimum is a vertex; an [interior point method](/interior-point-method/) returns a point inside this edge.
- *A line in the polyhedron.* $\min x_1$ over $\{x \in \mathbb{R}^2 : x_1 \ge 0\}$ has optimal value 0 on the whole line $x_1 = 0$, and no vertex. The rank condition of the general version is needed.
- *Nonlinear constraints.* $\min x_1$ subject to $x_1 x_2 \ge 1$, $x \ge 0$, is feasible and bounded below by 0, and the infimum 0 is not attained. Part 2 fails without linearity.
- *Strict inequalities.* $\min x_1$ subject to $x_1 > 0$ has infimum 0 and no optimum. Polyhedra are closed, and the proof uses this when it slides to the first wall.

**The slide on the running example.** In standard form, with $c = (-3, -2, 0, 0, 0)$ for $\max 3x_1 + 2x_2$, start at $x = (1, 1)$ with slacks $(2, 5, 2)$, so the support has size 5. The direction $d = (0, 1, -1, -3, 0)$ has $Ad = 0$ and $c^\top d = -2$; the step $t^* = \min(2/1, 5/3) = 5/3$ gives $(1, 8/3, 1/3, 0, 2)$ with support size 4. The direction $(3, -1, -2, 0, -3)$ has $c^\top d = -7$; the step $t^* = \min(\tfrac{8/3}{1}, \tfrac{1/3}{2}, \tfrac{2}{3}) = 1/6$ gives $(3/2, 5/2, 0, 0, 3/2)$, a basic feasible solution with objective $-19/2$. The proof then compares it with the other four basic feasible solutions, and the best is $(3, 1, 0, 3, 0)$ with objective $-11$.

## History

The idea that a linear objective reaches its optimum at a vertex of the feasible region is as old as the simplex method of Dantzig (1947), which moves along vertices. The name is not used in one fixed way: CLRS states as the fundamental theorem the three-way split of part 3, and other texts use it for parts 1 and 2, the existence of an optimal basic feasible solution.

## References
