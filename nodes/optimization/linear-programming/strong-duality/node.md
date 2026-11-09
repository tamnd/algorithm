---
tag: AK6PWF
kind: theorem
slug: strong-duality
name: Strong duality theorem
aliases:
- Strong duality
- strong duality
- duality theorem of linear programming
area: optimization/linear-programming
level: core
summary: If primal and dual are both feasible, their optimal values are equal.
prereqs: [weak-duality, farkas-lemma]
see_also: [lp-duality, complementary-slackness, dual-linear-program, simplex-method, shadow-price, minimax-theorem, max-flow-min-cut-theorem, lagrangian-duality]
sources:
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Section 4.3, The duality theorem (Theorem 4.4, proved from the simplex method), and Section 4.6, Farkas' lemma and linear inequalities (the second proof)
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 29.4, Duality (Theorem 29.10, linear programming duality, proved from the final slack form of SIMPLEX)
  - book: isbn:9783540306979
    title: Jiří Matoušek and Bernd Gärtner, Understanding and Using Linear Programming, Springer, 2007
    locator: Chapter 6, Section 6.3 (a proof from the simplex method) and Section 6.4 (a proof from the Farkas lemma)
  - book: isbn:9780471982326
    title: Alexander Schrijver, Theory of Linear and Integer Programming, Wiley, 1986
    locator: Chapter 7, Fundamental concepts and results on polyhedra, linear inequalities and linear programming (the duality theorem as a corollary of the Farkas lemma)
---

The strong duality theorem says that if a linear program has an optimal solution, then its [dual](/dual-linear-program/) also has one, and the two optimal values are equal. Together with [weak duality](/weak-duality/), it shows that the best bound that a combination of the constraints can prove is exactly the optimum. So every optimal solution of a linear program has a short proof of optimality, and optimization reduces to [feasibility](/linear-feasibility/). Many min-max theorems of combinatorics, such as [max-flow min-cut](/max-flow-min-cut-theorem/) and the [minimax theorem](/minimax-theorem/) for zero-sum games, are strong duality for a special LP.

## Statement

Consider the symmetric pair

$$\text{(P)}\quad \max\ c^\top x \ \ \text{s.t.}\ \ Ax \le b,\ x \ge 0 \qquad\qquad \text{(D)}\quad \min\ b^\top y \ \ \text{s.t.}\ \ A^\top y \ge c,\ y \ge 0.$$

**Theorem.**

1. If (P) has an optimal solution $x^*$, then (D) has an optimal solution $y^*$, and $c^\top x^* = b^\top y^*$.
2. If (P) and (D) are both feasible, then both have optimal solutions, and $\max c^\top x = \min b^\top y$.

Because the dual of (D) is (P), part 1 also holds with the roles exchanged. The same statements hold for the equality pair $\min c^\top x$, $Ax = b$, $x \ge 0$ and $\max b^\top y$, $A^\top y \le c$, and for every pair built by the general rule, since each LP is equivalent to a symmetric one and equivalent programs have equivalent duals.

## In plain words

The dual of a linear program looks for the best bound on the objective that can be built by adding up the constraints with nonnegative weights. Weak duality says that each such bound is safe. Strong duality says that no gap is left: if the problem has a best value, some choice of weights proves exactly that value. So whoever claims a plan is optimal can always back the claim with a short list of weights that anyone can check by multiplication and addition.

## Proof

The proof uses [Farkas' lemma](/farkas-lemma/) in this form: a system $Mz \le q$ has no solution if and only if there is $u \ge 0$ with $u^\top M = 0$ and $u^\top q < 0$.

*Part 1.* Let $\gamma = c^\top x^*$ be the optimal value of (P). It is enough to find $y$ with

$$A^\top y \ge c, \qquad b^\top y \le \gamma, \qquad y \ge 0,$$

because such a $y$ is dual feasible, and weak duality gives $b^\top y \ge \gamma$, so $b^\top y = \gamma$ and $y$ is optimal.

Suppose that no such $y$ exists. Write the system as $Mz \le q$ with rows $-A^\top y \le -c$, $b^\top y \le \gamma$ and $-y \le 0$. Farkas' lemma gives multipliers $x \ge 0$ (for the first block), $t \ge 0$ (for the second row) and $w \ge 0$ (for the third block) with

$$-Ax + t\, b - w = 0 \qquad\text{and}\qquad -c^\top x + t \gamma < 0.$$

The first equation says $Ax = t b - w \le t b$. The second says $c^\top x > t \gamma$.

*Case $t > 0$.* Then $x / t \ge 0$ and $A (x / t) \le b$, so $x / t$ is feasible for (P), and $c^\top (x / t) > \gamma$. This contradicts the optimality of $\gamma$.

*Case $t = 0$.* Then $Ax \le 0$, $x \ge 0$ and $c^\top x > 0$. For each $s \ge 0$, the point $x^* + s x$ satisfies $A(x^* + s x) \le b$ and $x^* + s x \ge 0$, and its value $\gamma + s\, c^\top x$ grows without bound. This again contradicts the optimality of $\gamma$.

So the system has a solution, and part 1 holds.

*Part 2.* Let $\bar y$ be feasible for (D). By weak duality, $c^\top x \le b^\top \bar y$ for every feasible $x$, so (P) is feasible and bounded above. By the [fundamental theorem of linear programming](/fundamental-theorem-of-lp/), (P) has an optimal solution, and part 1 gives the rest. $\blacksquare$

**A second proof, from the simplex method.** Run the [simplex method](/simplex-method/) with an anti-cycling rule on the equality form $\min c^\top x$, $Ax = b$, $x \ge 0$. It stops at a basis $B$ whose [reduced costs](/reduced-cost/) $c^\top - c_B^\top A_B^{-1} A$ are all nonnegative. Put $y^\top = c_B^\top A_B^{-1}$. Then $A^\top y \le c$, so $y$ is dual feasible, and $b^\top y = c_B^\top A_B^{-1} b = c_B^\top x_B = c^\top x$. This proof is constructive, but it needs the termination of the simplex method.

## Consequences

- **The joint outcomes.** Strong and weak duality together leave four possible pairs of outcomes: both optimal with equal values; primal unbounded and dual infeasible; primal infeasible and dual unbounded; both infeasible. The [LP duality](/lp-duality/) page lists them with examples.
- **Optimality conditions.** A feasible pair $(x, y)$ is optimal if and only if $c^\top x = b^\top y$, which is equivalent to [complementary slackness](/complementary-slackness/).
- **Optimization as feasibility.** The optimal solutions of (P) and (D) are exactly the solutions of the one system $Ax \le b$, $x \ge 0$, $A^\top y \ge c$, $y \ge 0$, $c^\top x \ge b^\top y$. So an algorithm for [linear feasibility](/linear-feasibility/) also solves optimization, and the problem is in $\text{NP} \cap \text{coNP}$ (a [good characterization](/good-characterization/)) before any polynomial algorithm is known.
- **Prices.** The optimal dual variables are the [shadow prices](/shadow-price/): the rate at which the optimal value changes with each right-hand side.
- **Min-max theorems.** The [max-flow min-cut theorem](/max-flow-min-cut-theorem/), [König's theorem](/konig-theorem/), the [minimax theorem](/minimax-theorem/) and [Menger's theorem](/menger-theorem/) follow from strong duality for a suitable LP, together with the integrality of its vertices.

## Tightness

**The running example.** For $\max 3x_1 + 2x_2$ subject to $x_1 + x_2 \le 4$, $x_1 + 3x_2 \le 9$, $x_1 \le 3$, $x \ge 0$, the primal optimum $x^* = (3, 1)$ and the dual optimum $y^* = (2, 0, 1)$ both have value 11. The weights $y^*$ prove the bound: $2(x_1 + x_2) + 1 \cdot x_1 = 3x_1 + 2x_2 \le 2 \cdot 4 + 3 = 11$.

**Feasibility is needed.** If (P) is feasible and (D) is not, (P) is unbounded and there is no optimal value to match. If both are infeasible, for example (P) $\max x_1$ subject to $x_1 - x_2 \le -1$, $-x_1 + x_2 \le -1$, $x \ge 0$, nothing can be said.

**Integer programs.** For $\max x$ subject to $2x \le 1$, $x \ge 0$ and $x$ integer, the optimum is 0. The LP dual $\min y$ subject to $2y \ge 1$, $y \ge 0$ has optimum $1/2$, the value of the [LP relaxation](/lp-relaxation/). The gap is not closed. An exact duality for integer programs needs [subadditive duality](/subadditive-duality/).

**Convex programs.** For nonlinear convex programs, the [Lagrangian dual](/lagrangian-duality/) can have a gap or an optimum that is not attained unless a condition such as Slater's holds. For $\min x$ subject to $x^2 \le 0$, the primal optimum is 0, and the dual function $\min_x (x + \lambda x^2) = -1/(4\lambda)$ tends to 0 as $\lambda \to \infty$ but never reaches it. Linear constraints need no such condition.

## History

George Dantzig described the simplex method in 1947 and discussed it with John von Neumann in October of that year. Von Neumann saw at once the connection with his theory of [zero-sum games](/zero-sum-game/) and stated the duality theorem in an unpublished note. David Gale, Harold Kuhn and Albert Tucker published the first rigorous proof in 1951, in the Cowles Commission volume *Activity Analysis of Production and Allocation*. The proof from [Farkas' lemma](/farkas-lemma/) (1902) is the standard modern one; the proof from the simplex method is the one in CLRS and in Dantzig's own book.

## References
