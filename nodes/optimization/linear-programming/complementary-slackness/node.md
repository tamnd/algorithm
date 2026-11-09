---
tag: AFFVTS
kind: theorem
slug: complementary-slackness
name: Complementary slackness
aliases:
- complementary slackness conditions
- complementary slackness theorem
area: optimization/linear-programming
level: core
summary: Primal and dual optimal solutions satisfy zero products between variables and their dual slacks.
prereqs: [strong-duality]
see_also: [kkt-conditions, primal-dual-schema, hungarian-algorithm, central-path, reduced-cost, shadow-price, shortest-path-optimality-conditions, lp-duality]
sources:
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Section 4.3, The duality theorem (Theorem 4.5, complementary slackness, and the examples after it)
  - book: isbn:9780716715870
    title: Vašek Chvátal, Linear Programming, W. H. Freeman, 1983
    locator: Chapter 5, The duality theorem (the complementary slackness theorem and its use to check optimality)
  - book: isbn:9783540306979
    title: Jiří Matoušek and Bernd Gärtner, Understanding and Using Linear Programming, Springer, 2007
    locator: Chapter 6, Section 6.1 and Section 6.2 (complementary slackness as a consequence of the duality theorem)
  - book: isbn:9780486402581
    title: Christos H. Papadimitriou and Kenneth Steiglitz, Combinatorial Optimization, Algorithms and Complexity, Dover, 1998
    locator: Chapter 3, Section 3.4 (complementary slackness) and Chapter 5, the primal-dual algorithm
---

Complementary slackness is the condition that tells when a feasible primal solution and a feasible [dual](/dual-linear-program/) solution are both optimal: for each constraint, either the constraint is tight or its dual variable is zero, and for each variable, either it is zero or its dual constraint is tight. It turns the single equation $c^\top x = b^\top y$ of [strong duality](/strong-duality/) into many small equations, one per pair of a constraint and a variable. This is the form that algorithms use: the [Hungarian algorithm](/hungarian-algorithm/) and the [primal-dual schema](/primal-dual-schema/) keep it true while they search for feasibility, and [interior point methods](/interior-point-method/) relax it and drive the relaxation to zero.

## Statement

Consider the symmetric pair

$$\text{(P)}\quad \max\ c^\top x \ \ \text{s.t.}\ \ Ax \le b,\ x \ge 0 \qquad\qquad \text{(D)}\quad \min\ b^\top y \ \ \text{s.t.}\ \ A^\top y \ge c,\ y \ge 0,$$

with rows $a_i^\top$ and columns $A_j$ of $A$.

**Theorem.** Let $x$ be feasible for (P) and $y$ feasible for (D). Then $x$ and $y$ are both optimal if and only if

$$y_i \,\big(b_i - a_i^\top x\big) = 0 \quad \text{for } i = 1, \ldots, m, \qquad\qquad x_j \,\big(A_j^\top y - c_j\big) = 0 \quad \text{for } j = 1, \ldots, n.$$

In words: if a primal constraint has slack, its dual variable is zero, and if a dual constraint has slack, its primal variable is zero.

**Equality form.** For $\min c^\top x$, $Ax = b$, $x \ge 0$ and $\max b^\top y$, $A^\top y \le c$, the conditions are $x_j\,(c_j - A_j^\top y) = 0$ for all $j$. The factor $c_j - A_j^\top y$ is the [reduced cost](/reduced-cost/) of $x_j$ with respect to $y$; the rows are equations and add no condition.

**General form.** For any primal-dual pair, the condition is that every product of a primal constraint's slack with its dual variable, and of a dual constraint's slack with its primal variable, is zero.

## In plain words

Think of the dual variables as prices for the limited resources of the first problem. At an optimum, a resource that is not used up has price zero, since more of it would not help. And an activity that is actually used earns exactly what its resources cost at those prices; an activity that would lose money at those prices is not used at all. A plan and a set of prices that obey both rules, and are each allowed, are both best.

## Proof

Let $x$ and $y$ be feasible. Write the chain of [weak duality](/weak-duality/) as

$$b^\top y - c^\top x \;=\; \underbrace{y^\top (b - Ax)}_{=\ \sum_i y_i (b_i - a_i^\top x)} \;+\; \underbrace{x^\top (A^\top y - c)}_{=\ \sum_j x_j (A_j^\top y - c_j)}.$$

Every term of both sums is a product of two nonnegative numbers, by feasibility. So the gap $b^\top y - c^\top x$ is zero exactly when every term is zero.

(If.) If all the products are zero, then $c^\top x = b^\top y$, and by weak duality both are optimal.

(Only if.) If both are optimal, [strong duality](/strong-duality/) gives $c^\top x = b^\top y$, so the gap is zero, and every product is zero. $\blacksquare$

The "if" direction uses only weak duality. The "only if" direction needs strong duality.

## Consequences

- **Recovering the dual from a primal optimum.** Given an optimal $x$, complementary slackness gives linear equations for $y$: $y_i = 0$ for each row with slack, and $A_j^\top y = c_j$ for each $j$ with $x_j > 0$. For a nondegenerate vertex these equations determine $y$ uniquely.
- **Checking a claimed optimum.** To test whether a feasible $x$ is optimal, solve those equations; $x$ is optimal if and only if some solution $y$ is dual feasible. The examples below do this.
- **Primal-dual algorithms.** The [Hungarian algorithm](/hungarian-algorithm/) for the [assignment problem](/assignment-problem/), the primal-dual method of Papadimitriou and Steiglitz, and the [primal-dual schema](/primal-dual-schema/) for approximation keep a dual feasible $y$ and a primal $x$ that satisfies complementary slackness, and move toward primal feasibility. Approximation algorithms use *relaxed* conditions, such as $x_j > 0 \Rightarrow A_j^\top y \ge c_j / \alpha$, to prove a ratio $\alpha$.
- **Interior point methods.** The [central path](/central-path/) replaces each condition $x_j s_j = 0$, where $s$ is the dual slack, by $x_j s_j = \mu$, and lets $\mu \to 0$.
- **KKT conditions.** For a linear program, the [Karush-Kuhn-Tucker conditions](/kkt-conditions/) are primal feasibility, dual feasibility and complementary slackness.
- **Network optimality.** In a minimum cost flow, an arc with positive [reduced cost](/potential-function-reduced-costs/) carries no flow and an arc with negative reduced cost is full. In a shortest path problem, every arc of a shortest path is tight, $d(v) = d(u) + w(u, v)$; see [shortest path optimality conditions](/shortest-path-optimality-conditions/). In max flow, every arc across a minimum cut is saturated.
- **Strict complementarity.** If both programs have optimal solutions, some optimal pair has, for each product, exactly one factor zero (Goldman and Tucker, 1956). Interior point methods converge to such a pair.

## Tightness

**Finding the dual of the running example.** The primal is $\max 3x_1 + 2x_2$ subject to $x_1 + x_2 \le 4$, $x_1 + 3x_2 \le 9$, $x_1 \le 3$, $x \ge 0$. At $x = (3, 1)$ the slacks are $(0, 3, 0)$, so $y_2 = 0$. Both $x_1$ and $x_2$ are positive, so both dual constraints are tight: $y_1 + y_2 + y_3 = 3$ and $y_1 + 3y_2 = 2$. This gives $y = (2, 0, 1)$, which is dual feasible. So $(3, 1)$ is optimal, and the value is $4 \cdot 2 + 3 \cdot 1 = 11$.

**Rejecting a vertex that is not optimal.** At $x = (3/2, 5/2)$ the slacks are $(0, 0, 3/2)$, so $y_3 = 0$, and $y_1 + y_2 = 3$, $y_1 + 3y_2 = 2$ give $y = (7/2, -1/2, 0)$. The only candidate has $y_2 < 0$, so it is not dual feasible, and $(3/2, 5/2)$ is not optimal.

**Both factors can be zero.** Change the second row to $x_1 + 3x_2 \le 6$. Then $(3, 1)$ is still optimal with value 11, but now all three slacks are zero (a degenerate vertex). The dual optima form the segment from $(2, 0, 1)$ to $(0, 2/3, 7/3)$. At $y = (2, 0, 1)$ the second row has slack 0 and $y_2 = 0$: both factors are zero. At the midpoint $y = (1, 1/3, 5/3)$ every $y_i$ is positive, and this pair is strictly complementary. So the conditions do not say "exactly one factor is zero", and a degenerate primal vertex can have many dual optima.

**Feasibility is part of the condition.** The products can all be zero for points that are not feasible. In the running example, $x = 0$ and $y = 0$ make every product zero, but $y = 0$ violates $y_1 + y_2 + y_3 \ge 3$, and $x = 0$ is not optimal.

## History

Complementary slackness appears in the duality work of Gale, Kuhn and Tucker (1951) and, for nonlinear programs, in the conditions of Kuhn and Tucker (1951) and the earlier thesis of Karush (1939). Goldman and Tucker proved the existence of a strictly complementary optimal pair in 1956. The economic reading, with dual variables as prices of resources, goes back to Kantorovich and Koopmans.

## References
