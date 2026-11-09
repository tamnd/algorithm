---
tag: 5YZQTA
kind: definition
slug: dual-linear-program
name: Dual linear program
aliases:
- dual LP
- dual problem
- primal-dual pair
area: optimization/linear-programming
level: intro
summary: The LP obtained by swapping constraint and variable roles in a primal LP.
prereqs: [linear-programming-problem, lp-standard-form]
see_also: [weak-duality, strong-duality, lp-duality, complementary-slackness, shadow-price, farkas-lemma, lagrangian-duality, dual-simplex-method]
sources:
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Section 4.1, Motivation, and Section 4.2, The dual problem (the table of primal and dual rules, the dual of the dual, and the invariance under equivalent transformations)
  - book: isbn:9783540306979
    title: Jiří Matoušek and Bernd Gärtner, Understanding and Using Linear Programming, Springer, 2007
    locator: Chapter 6, Duality of linear programming (Section 6.1 the duality theorem, Section 6.2 dualization for everyone)
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 29.4, Duality (the dual of a program in standard form)
  - book: isbn:9780716715870
    title: Vašek Chvátal, Linear Programming, W. H. Freeman, 1983
    locator: Chapter 5, The duality theorem (the dual problem as the problem of the best upper bound)
---

The dual of a linear program is a second linear program with one variable for each constraint of the first (the *primal*) and one constraint for each primal variable. Its feasible solutions are the vectors of multipliers that combine the primal constraints into a bound on the primal objective, and its objective asks for the best such bound. The two programs are tied by [weak duality](/weak-duality/), [strong duality](/strong-duality/) and [complementary slackness](/complementary-slackness/), and the optimal dual variables are the [shadow prices](/shadow-price/) of the primal constraints.

## Definition

Let $A \in \mathbb{R}^{m \times n}$ with rows $a_i^\top$ and columns $A_j$, $b \in \mathbb{R}^m$ and $c \in \mathbb{R}^n$.

**Symmetric form.** The dual of the inequality [standard form](/lp-standard-form/) is

$$\text{(P)}\quad \max\ c^\top x \ \ \text{s.t.}\ \ Ax \le b,\ x \ge 0 \qquad\qquad \text{(D)}\quad \min\ b^\top y \ \ \text{s.t.}\ \ A^\top y \ge c,\ y \ge 0.$$

**Equality form.** The dual of the equality standard form, the default form of these pages, is

$$\text{(P)}\quad \min\ c^\top x \ \ \text{s.t.}\ \ Ax = b,\ x \ge 0 \qquad\qquad \text{(D)}\quad \max\ b^\top y \ \ \text{s.t.}\ \ A^\top y \le c,\ y \text{ free}.$$

**General rule.** For a primal minimization $\min c^\top x$ with any mix of row types and sign conditions, the dual is $\max b^\top y$, with one variable $y_i$ per row and one constraint per column, as in this table:

| primal (minimize $c^\top x$) | dual (maximize $b^\top y$) |
|---|---|
| row $a_i^\top x \ge b_i$ | $y_i \ge 0$ |
| row $a_i^\top x \le b_i$ | $y_i \le 0$ |
| row $a_i^\top x = b_i$ | $y_i$ free |
| $x_j \ge 0$ | column $A_j^\top y \le c_j$ |
| $x_j \le 0$ | column $A_j^\top y \ge c_j$ |
| $x_j$ free | column $A_j^\top y = c_j$ |

For a primal maximization, read the table from right to left: the dual of a maximization is the minimization in the left column, with the roles of the two columns swapped. The two forms above are the special cases with all rows of one type and all $x_j \ge 0$.

**Where the rule comes from.** For a minimization, the dual asks for multipliers $y$ that make $y^\top A x \le c^\top x$ hold for every feasible $x$ while $y^\top A x \ge y^\top b$ holds at the same time. The sign of $y_i$ must keep the direction of row $i$: a multiplier on a $\ge$ row must be nonnegative, and on an equation it may have either sign. The bound $y^\top A x \le c^\top x$ must hold for each allowed sign of $x_j$, which gives the column constraint. Then each feasible $x$ has $c^\top x \ge y^\top A x \ge b^\top y$, and the dual looks for the largest such lower bound. This is the proof of weak duality, read backwards. The same rule is the [Lagrangian dual](/lagrangian-duality/) of the program: $\max_y \min_x \big(c^\top x + y^\top (b - Ax)\big)$, with the inner minimum over the sign conditions of $x$, is finite exactly when $y$ satisfies the column constraints, and then it equals $b^\top y$.

**The dual of the dual is the primal.** Write (D) of the symmetric form as a maximization: $\max\ (-b)^\top y$ subject to $(-A^\top) y \le -c$, $y \ge 0$. Its dual by the symmetric rule is $\min\ (-c)^\top x$ subject to $(-A^\top)^\top x \ge -b$, $x \ge 0$, which is $\max c^\top x$ subject to $Ax \le b$, $x \ge 0$. The table is symmetric in the same way for the general rule.

**Invariance.** If a primal is converted to an equivalent program by the rules of [standard form](/lp-standard-form/) (splitting a free variable, adding slacks, replacing an equation by two inequalities), the dual of the new program is equivalent to the dual of the old one: it has the same optimal value, and it is feasible or unbounded exactly when the old one is. So "the dual" is well defined up to such changes of form.

## Examples and non-examples

**The running example.** The primal is $\max 3x_1 + 2x_2$ subject to $x_1 + x_2 \le 4$, $x_1 + 3x_2 \le 9$, $x_1 \le 3$, $x \ge 0$. Its dual is

$$\min\ 4y_1 + 9y_2 + 3y_3 \quad \text{s.t.} \quad y_1 + y_2 + y_3 \ge 3,\quad y_1 + 3y_2 \ge 2,\quad y \ge 0.$$

The dual feasible region is unbounded and has four vertices, $(3, 0, 0)$, $(0, 3, 0)$, $(2, 0, 1)$ and $(0, 2/3, 7/3)$, with objective values 12, 27, 11 and 13. The minimum 11 at $y^* = (2, 0, 1)$ equals the primal maximum 11 at $x^* = (3, 1)$. Each dual vertex is a bound: the vertex $(3, 0, 0)$ says "three times the first row" and proves $3x_1 + 2x_2 \le 3x_1 + 3x_2 \le 12$.

**A mixed program.** Minimize $2x_1 + 3x_2 - x_3$ subject to

$$x_1 + x_2 + x_3 \ge 2, \qquad x_1 - x_3 = 1, \qquad x_2 + 2x_3 \le 4, \qquad x_1 \ge 0,\ x_2 \text{ free},\ x_3 \le 0.$$

By the table the dual has $y_1 \ge 0$, $y_2$ free, $y_3 \le 0$, and one constraint per column:

$$\max\ 2y_1 + y_2 + 4y_3 \quad \text{s.t.} \quad y_1 + y_2 \le 2,\quad y_1 + y_3 = 3,\quad y_1 - y_2 + 2y_3 \ge -1.$$

The primal optimum is $x^* = (1, 1, 0)$ with value 5, and the dual optimum is $y^* = (3, -1, 0)$, also with value 5. The equality $y_1 + y_3 = 3$ comes from the free variable $x_2$, and the $\ge$ in the last row comes from $x_3 \le 0$.

**The standard form of the running example.** With slacks, $A = \begin{pmatrix} 1 & 1 & 1 & 0 & 0 \\ 1 & 3 & 0 & 1 & 0 \\ 1 & 0 & 0 & 0 & 1 \end{pmatrix}$, $b = (4, 9, 3)$ and $c = (-3, -2, 0, 0, 0)$ for a minimization. The dual $\max b^\top y$, $A^\top y \le c$ has free $y$, but the slack columns give $y_i \le 0$. Its optimum is $y = (-2, 0, -1)$ with value $-11$: the same solution as before with the signs that the minimization brings.

**Graph examples.** The dual of the [maximum flow LP](/max-flow-linear-program/) is a fractional minimum cut. The dual of the [shortest path LP](/shortest-paths-lp-formulation/) is a minimum cost flow of one unit. The dual of the [minimum cost flow LP](/min-cost-flow-lp-formulation/) has one potential per node, and its constraints say that the [reduced costs](/potential-function-reduced-costs/) are nonnegative.

**Non-examples.**

- *The polar of a polytope.* The polar dual of a polytope swaps vertices and facets. It is a different construction, not the dual LP.
- *The dual of an integer program.* Dropping the integrality conditions and taking the LP dual gives a bound for the [LP relaxation](/lp-relaxation/), not an exact dual of the integer program; the two optimal values can differ by the [integrality gap](/integrality-gap/). An exact dual needs [subadditive duality](/subadditive-duality/).
- *Using the wrong sign.* For $\min x_1$ subject to $x_1 \le 5$, $x_1 \ge 0$, a careless dual "$\max 5y$, $y \le 1$, $y \ge 0$" has value 5, which is not a lower bound on the primal optimum 0. The table gives $y \le 0$ for a $\le$ row of a minimization, and then the dual optimum is 0.

## Related definitions

- [Weak duality](/weak-duality/): each dual feasible value bounds each primal feasible value.
- [Strong duality](/strong-duality/) and [LP duality](/lp-duality/): the optimal values are equal when either program has an optimum, and the list of the possible cases.
- [Complementary slackness](/complementary-slackness/): the conditions under which a feasible pair is optimal.
- [Shadow price](/shadow-price/) and [reduced cost](/reduced-cost/): the optimal dual variables and the dual slacks, read from a basis.
- [Farkas' lemma](/farkas-lemma/): the dual of a feasibility problem gives a certificate of infeasibility.
- [Lagrangian duality](/lagrangian-duality/): the same construction for convex programs, where strong duality needs a constraint qualification.
- [Dual simplex method](/dual-simplex-method/): the simplex method run on the dual, through the primal tableau.

## References
