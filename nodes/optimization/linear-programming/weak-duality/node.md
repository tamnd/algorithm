---
tag: PCZ40E
kind: theorem
slug: weak-duality
name: Weak duality theorem
aliases:
- Weak duality
- weak duality
- weak duality theorem
area: optimization/linear-programming
level: intro
summary: Any feasible dual value bounds every feasible primal value.
prereqs: [dual-linear-program]
see_also: [strong-duality, lp-duality, complementary-slackness, farkas-lemma, lagrangian-duality, max-flow-min-cut-theorem, primal-dual-schema, dual-fitting]
sources:
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Section 4.3, The duality theorem (Theorem 4.3, weak duality, and Corollaries 4.1 and 4.2)
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 29.4, Duality (Lemma 29.8, weak linear programming duality, and Corollary 29.9)
  - book: isbn:9783540306979
    title: Jiří Matoušek and Bernd Gärtner, Understanding and Using Linear Programming, Springer, 2007
    locator: Chapter 6, Section 6.1 (the dual as the best upper bound, and the easy direction of the duality theorem)
  - book: isbn:9780716715870
    title: Vašek Chvátal, Linear Programming, W. H. Freeman, 1983
    locator: Chapter 5, The duality theorem (the upper bound from a combination of the constraints)
---

Weak duality says that the objective value of each feasible solution of the [dual linear program](/dual-linear-program/) is a bound on the objective value of each feasible solution of the primal: a lower bound for a minimization, an upper bound for a maximization. The proof is two lines of algebra. The theorem makes a dual solution a short certificate of quality: a primal solution and a dual solution with equal values are both optimal. It is the easy half of [LP duality](/lp-duality/); the hard half, that the best bound is exact, is [strong duality](/strong-duality/).

## Statement

**Theorem (symmetric form).** Let $x$ be feasible for $\max\ c^\top x$ subject to $Ax \le b$, $x \ge 0$, and let $y$ be feasible for its dual $\min\ b^\top y$ subject to $A^\top y \ge c$, $y \ge 0$. Then

$$c^\top x \le b^\top y.$$

**Theorem (equality form).** Let $x$ be feasible for $\min\ c^\top x$ subject to $Ax = b$, $x \ge 0$, and let $y$ be feasible for $\max\ b^\top y$ subject to $A^\top y \le c$. Then $b^\top y \le c^\top x$.

The same inequality, primal minimum above dual maximum, holds for every primal-dual pair built by the general rule of the [dual linear program](/dual-linear-program/) page.

**Corollaries.**

1. If $c^\top x = b^\top y$ for feasible $x$ and $y$, then $x$ and $y$ are optimal for their programs.
2. If the primal (maximization) is unbounded, the dual is infeasible. If the dual (minimization) is unbounded, the primal is infeasible.
3. If both programs are feasible, both have finite optimal values, and $\max c^\top x \le \min b^\top y$.

## In plain words

Each allowed choice of the multipliers in the dual combines the limits of the first problem into one limit on its objective. So no allowed plan of the first problem can do better than any value of the second problem. If you find a plan and a set of multipliers with the same value, neither can be improved, and you have a proof that the plan is best. If one problem can improve forever, the other cannot have any allowed choice.

## Proof

*Symmetric form.* Since $x \ge 0$ and $A^\top y \ge c$, each term of $x^\top (A^\top y - c)$ is a product of two nonnegative numbers, so $c^\top x \le (A^\top y)^\top x = y^\top A x$. Since $y \ge 0$ and $Ax \le b$, in the same way $y^\top A x \le y^\top b$. Together,

$$c^\top x \;\le\; y^\top A x \;\le\; b^\top y.$$

*Equality form.* $c^\top x - b^\top y = c^\top x - y^\top A x = (c - A^\top y)^\top x \ge 0$, because $c - A^\top y \ge 0$ and $x \ge 0$.

*General form.* For a primal minimization, write $c^\top x - b^\top y = (c - A^\top y)^\top x + y^\top (Ax - b)$. By the sign rules of the dual, each product $(c_j - A_j^\top y)\, x_j$ is nonnegative (a column constraint $\le$ pairs with $x_j \ge 0$, a $\ge$ with $x_j \le 0$, and an equation gives a zero factor), and each product $y_i\, (a_i^\top x - b_i)$ is nonnegative (a $\ge$ row pairs with $y_i \ge 0$, a $\le$ row with $y_i \le 0$, and an equation gives a zero factor). So $c^\top x \ge b^\top y$.

*Corollaries.* (1) For each feasible $x'$, $c^\top x' \le b^\top y = c^\top x$ in the symmetric form, so $x$ is optimal; the same argument applies to $y$. (2) If the dual had a feasible $y$, then $b^\top y$ would bound every primal value, so the primal would not be unbounded. (3) Each feasible $y$ bounds the primal values from above, so the supremum is finite; the [fundamental theorem](/fundamental-theorem-of-lp/) makes it a maximum, and the same holds for the dual. The bound holds for every pair, so it holds for the optima. $\blacksquare$

## Consequences

- **Certificates of optimality.** To prove that a solution is optimal, show a dual solution with the same value. The [simplex method](/simplex-method/) ends with such a pair, and the [complementary slackness](/complementary-slackness/) conditions say when the values agree.
- **Bounds in algorithms.** Any dual feasible solution bounds the optimum, so it measures how far a heuristic solution can be from optimal. [Primal-dual](/primal-dual-schema/) approximation algorithms and [dual fitting](/dual-fitting/) build such a dual to prove an approximation ratio, and [branch and bound](/land-doig-algorithm/) uses LP bounds to cut branches.
- **Combinatorial min-max inequalities.** The easy direction of every LP min-max theorem is weak duality. Each $s$-$t$ flow has value at most the capacity of each $s$-$t$ cut, and the maximum matching is at most the minimum vertex cover; the [max-flow min-cut theorem](/max-flow-min-cut-theorem/) and [König's theorem](/konig-theorem/) add equality.
- **Infeasibility from unboundedness.** Corollary 2 shows that the primal and dual cannot both be unbounded. Together with strong duality it limits the joint outcomes to the table on the [LP duality](/lp-duality/) page.

## Tightness

**The running example.** The primal is $\max 3x_1 + 2x_2$ subject to $x_1 + x_2 \le 4$, $x_1 + 3x_2 \le 9$, $x_1 \le 3$, $x \ge 0$, and its dual is $\min 4y_1 + 9y_2 + 3y_3$ subject to $y_1 + y_2 + y_3 \ge 3$, $y_1 + 3y_2 \ge 2$, $y \ge 0$. The feasible pair $x = (3, 0)$ and $y = (3, 0, 0)$ gives $9 \le 12$, a gap of 3. The pair $x = (3, 1)$ and $y = (2, 0, 1)$ gives $11 = 11$, so by corollary 1 both are optimal.

**The gap can be any size for feasible pairs.** For fixed $x$, $b^\top y$ can be made as large as wanted in this example by a large $y_2$. Weak duality says nothing about how close the bound is; only at the optima does strong duality close the gap.

**Both programs infeasible.** The converse of corollary 2 fails: an infeasible primal does not make the dual unbounded. The primal $\max x_1$ subject to $x_1 - x_2 \le -1$, $-x_1 + x_2 \le -1$, $x \ge 0$ is infeasible (the two rows add to $0 \le -2$), and its dual $\min -y_1 - y_2$ subject to $y_1 - y_2 \ge 1$, $-y_1 + y_2 \ge 0$, $y \ge 0$ is also infeasible (the two rows add to $0 \ge 1$).

**Beyond linear programs.** Weak duality holds for every [Lagrangian dual](/lagrangian-duality/), even of a nonconvex problem, because it uses only the sign of each product. For an integer program the LP dual is still a valid bound, but equality may fail; the difference is the integrality gap of the [LP relaxation](/lp-relaxation/).

## History

The inequality appears with the first statements of LP duality. In 1947 John von Neumann described the duality to George Dantzig in terms of his theory of [zero-sum games](/zero-sum-game/), and Gale, Kuhn and Tucker published the first proof of the duality theorem in 1951. Weak duality is the trivial direction of these results and of the [minimax theorem](/minimax-theorem/).

## References
