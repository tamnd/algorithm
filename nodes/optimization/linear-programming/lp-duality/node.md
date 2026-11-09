---
tag: SVBFN1
kind: theorem
slug: lp-duality
name: Linear programming duality
aliases:
- duality theorem
- LP duality
- linear programming duality theorem
area: optimization/linear-programming
level: core
summary: Every LP has a dual LP whose optimum matches the primal optimum when both are feasible and bounded.
prereqs: [weak-duality, strong-duality]
see_also: [dual-linear-program, complementary-slackness, farkas-lemma, shadow-price, dual-simplex-method, good-characterization, minimax-theorem, lagrangian-duality]
sources:
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Section 4.3, The duality theorem (the table of the possible combinations of primal and dual outcomes)
  - book: isbn:9783540306979
    title: Jiří Matoušek and Bernd Gärtner, Understanding and Using Linear Programming, Springer, 2007
    locator: Chapter 6, Section 6.1 (the duality theorem with its four cases)
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 29.4, Duality
  - book: isbn:9780471982326
    title: Alexander Schrijver, Theory of Linear and Integer Programming, Wiley, 1986
    locator: Chapter 7, Section 7.4 (the duality theorem of linear programming) and its corollaries
---

The duality theorem of linear programming joins [weak duality](/weak-duality/) and [strong duality](/strong-duality/) into one statement about a primal program and its [dual](/dual-linear-program/): the two have equal optimal values whenever either has an optimum, and the only other joint outcomes are "one unbounded, the other infeasible" and "both infeasible". This page states the full classification, gives an example of each case, and lists what the theorem implies for algorithms and for combinatorics.

## Statement

Let (P) be a linear program and (D) its dual. For the symmetric pair these are

$$\text{(P)}\quad \max\ c^\top x \ \ \text{s.t.}\ \ Ax \le b,\ x \ge 0 \qquad\qquad \text{(D)}\quad \min\ b^\top y \ \ \text{s.t.}\ \ A^\top y \ge c,\ y \ge 0.$$

Each program, by the [fundamental theorem](/fundamental-theorem-of-lp/), is in exactly one of the states *optimal* (it has an optimal solution), *unbounded* or *infeasible*.

**Theorem (LP duality).** Exactly one of the following holds.

1. Both (P) and (D) have optimal solutions, and $\max c^\top x = \min b^\top y$.
2. (P) is unbounded and (D) is infeasible.
3. (P) is infeasible and (D) is unbounded.
4. Both (P) and (D) are infeasible.

In a table, with "yes" for the possible combinations:

| | (D) optimal | (D) unbounded | (D) infeasible |
|---|---|---|---|
| **(P) optimal** | yes, equal values | no | no |
| **(P) unbounded** | no | no | yes |
| **(P) infeasible** | no | yes | yes |

The theorem holds for every primal-dual pair built by the general rule of the [dual](/dual-linear-program/) page, since the dual of the dual is the primal and equivalent programs have equivalent duals.

## In plain words

Every linear program comes with a partner program that searches for the best proven bound on its value. The two are tied in a strict way. If either one has a best answer, so does the other, and the two best values are equal. If one can improve forever, the other has no allowed choice at all. And it can happen that neither has any allowed choice. No other combination is possible.

## Proof

*Row "optimal".* If (P) has an optimal solution, part 1 of [strong duality](/strong-duality/) gives an optimal solution of (D) with the same value. So (D) is optimal, and the other two entries of the row are impossible.

*Column "optimal".* If (D) has an optimal solution, apply strong duality to (D), whose dual is (P). So (P) is optimal, and the entries "(P) unbounded, (D) optimal" and "(P) infeasible, (D) optimal" are impossible.

*Entry "both unbounded".* If (P) is unbounded, it is feasible, and by [weak duality](/weak-duality/) a feasible $y$ of (D) would bound every value of (P). So (D) is infeasible, and "both unbounded" is impossible.

*The remaining entries.* "(P) unbounded, (D) infeasible", "(P) infeasible, (D) unbounded" and "both infeasible" are possible, by the examples below. So the four cases of the theorem are exactly the possible ones, and they exclude each other because each program is in only one state. $\blacksquare$

**A useful reformulation.** If (P) is infeasible and (D) is feasible, then (D) is unbounded. Indeed, (D) cannot be optimal by the column "optimal", and a feasible program that is not optimal is unbounded by the fundamental theorem. In the same way, if (P) is feasible and (D) is infeasible, then (P) is unbounded.

## Consequences

- **Short certificates for every outcome.** An optimal $x$ is certified by a dual $y$ with the same value. Infeasibility of (P) is certified by a [Farkas](/farkas-lemma/) vector, which is a ray of (D). Unboundedness of (P) is certified by a feasible point and a ray $d \ge 0$ with $Ad \le 0$ and $c^\top d > 0$. Each certificate can be checked by arithmetic, so each outcome is in NP, and LP is a [good characterization](/good-characterization/).
- **Optimization reduces to feasibility.** The optimal pairs are the solutions of one linear system: primal feasibility, dual feasibility and $c^\top x \ge b^\top y$. See [linear feasibility](/linear-feasibility/).
- **Algorithms that work on both sides.** The [dual simplex method](/dual-simplex-method/) keeps a dual feasible basis and searches for primal feasibility. [Interior point methods](/interior-point-method/) follow both programs at once and stop when the duality gap is small. The [primal-dual schema](/primal-dual-schema/) for approximation algorithms grows a dual solution to pay for a primal one.
- **Min-max theorems.** The [max-flow min-cut theorem](/max-flow-min-cut-theorem/), [König's theorem](/konig-theorem/) and von Neumann's [minimax theorem](/minimax-theorem/) are case 1 for special LPs.
- **Prices and sensitivity.** The optimal dual is the vector of [shadow prices](/shadow-price/), and the pair satisfies [complementary slackness](/complementary-slackness/).

## Tightness

The four possible cases each occur.

1. *Both optimal.* (P) $\max 3x_1 + 2x_2$ subject to $x_1 + x_2 \le 4$, $x_1 + 3x_2 \le 9$, $x_1 \le 3$, $x \ge 0$ has the optimum $(3, 1)$ with value 11, and (D) $\min 4y_1 + 9y_2 + 3y_3$ subject to $y_1 + y_2 + y_3 \ge 3$, $y_1 + 3y_2 \ge 2$, $y \ge 0$ has the optimum $(2, 0, 1)$ with value 11.
2. *(P) unbounded, (D) infeasible.* (P) $\max x_1 + x_2$ subject to $x_1 - x_2 \le 1$, $x \ge 0$ is unbounded along the ray $(1, 1)$. (D) $\min y$ subject to $y \ge 1$, $-y \ge 1$, $y \ge 0$ is infeasible.
3. *(P) infeasible, (D) unbounded.* (P) $\max x_1$ subject to $x_1 \le -1$, $x_1 \ge 0$ is infeasible. (D) $\min -y$ subject to $y \ge 1$, $y \ge 0$ is unbounded as $y \to \infty$.
4. *Both infeasible.* (P) $\max x_1$ subject to $x_1 - x_2 \le -1$, $-x_1 + x_2 \le -1$, $x \ge 0$: the two rows add to $0 \le -2$. (D) $\min -y_1 - y_2$ subject to $y_1 - y_2 \ge 1$, $-y_1 + y_2 \ge 0$, $y \ge 0$: the two rows add to $0 \ge 1$.

**Beyond linear programs.** For convex programs, case 1 needs a constraint qualification: without one the optimal values can differ or the dual optimum may not be attained; see [Lagrangian duality](/lagrangian-duality/). For integer programs, case 1 fails in general, since the LP dual gives only the value of the [LP relaxation](/lp-relaxation/).

## History

Von Neumann stated the duality theorem in 1947, in a conversation with Dantzig and an unpublished note, by analogy with his [minimax theorem](/minimax-theorem/) for zero-sum games of 1928. Gale, Kuhn and Tucker gave the first published proof in 1951. The table of the four outcomes is now standard in textbooks, for example in Bertsimas and Tsitsiklis.

## References
