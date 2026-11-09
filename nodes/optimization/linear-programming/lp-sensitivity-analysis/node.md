---
tag: RKTX2B
kind: concept
slug: lp-sensitivity-analysis
name: Sensitivity analysis of linear programs
aliases:
- LP sensitivity
- sensitivity analysis
- postoptimal analysis
- ranging
area: optimization/linear-programming
level: advanced
summary: How the optimum changes when coefficients or right-hand sides change.
prereqs: [shadow-price, reduced-cost]
see_also: [parametric-linear-programming, dual-simplex-method, simplex-method, basic-feasible-solution, lp-degeneracy, complementary-slackness, revised-simplex-method, land-doig-algorithm]
sources:
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Section 5.1, Local sensitivity analysis (a new variable, a new constraint, changes in b, changes in c, changes in a nonbasic column), and Sections 5.2 and 5.4 (global dependence on b and on c)
  - book: isbn:9780716715870
    title: Vašek Chvátal, Linear Programming, W. H. Freeman, 1983
    locator: Chapter 10, Sensitivity analysis
  - book: isbn:9780471982326
    title: Alexander Schrijver, Theory of Linear and Integer Programming, Wiley, 1986
    locator: Chapter 10, Section 10.4 (sensitivity analysis)
---

Sensitivity analysis asks how the optimal solution and the optimal value of a linear program change when its data change: a right-hand side, an objective coefficient, a new variable or a new constraint. Its main tool is the optimal basis. A basis stays optimal as long as two sets of linear inequalities hold, primal feasibility of the basic solution and nonnegativity of the [reduced costs](/reduced-cost/), and each change of one number moves these inequalities in a simple way. So for each number of the input, one can compute the range in which the current basis stays optimal and the rate at which the value changes in that range, the [shadow price](/shadow-price/) or the reduced cost. Outside the range, one pivot step of the [simplex](/simplex-method/) or [dual simplex](/dual-simplex-method/) method, started from the old basis, finds the new optimum.

## In plain words

You solved a planning problem, and now the numbers move: a supplier offers more material, a price drops, a new product is proposed. Solving everything again works, but it hides the structure. The best plan comes with a list of which limits are binding. That list stays the same for a while as a number changes, and while it does, the profit changes at a fixed rate. Sensitivity analysis computes, for each number, how far it can move before the list changes, and that fixed rate. Past the edge, a few cheap steps from the old plan find the new one.

## The idea

**Setting.** $\min c^\top x$ subject to $Ax = b$, $x \ge 0$, with an optimal basis $B$. Write $x_B = A_B^{-1} b$, $y^\top = c_B^\top A_B^{-1}$ and $\bar c^\top = c^\top - y^\top A$. The basis $B$ is optimal exactly when

$$\text{(feasibility)}\quad A_B^{-1} b \ge 0 \qquad\text{and}\qquad \text{(optimality)}\quad \bar c \ge 0.$$

The first condition does not involve $c$, and the second does not involve $b$. This split is what makes the analysis simple.

**A change in a right-hand side.** Replace $b$ by $b + \delta e_i$. Optimality does not change. Feasibility becomes $x_B + \delta\, A_B^{-1} e_i \ge 0$, one inequality in $\delta$ per basic variable, so the set of good $\delta$ is an interval $[\delta_-, \delta_+]$ that contains 0. In it, the value is $c^\top x + \delta y_i$: $y_i$ is the [shadow price](/shadow-price/). Past the interval, some basic variable turns negative, the basis is still dual feasible, and the [dual simplex method](/dual-simplex-method/) restores feasibility.

**A change in the cost of a nonbasic variable.** Replace $c_j$ by $c_j + \delta$ for $j \notin B$. Only $\bar c_j$ changes, to $\bar c_j + \delta$. So the basis stays optimal for $\delta \ge -\bar c_j$: the reduced cost is how much $c_j$ must fall before $x_j$ is worth using. Past that, $x_j$ enters by a primal simplex pivot.

**A change in the cost of a basic variable.** Replace $c_j$ by $c_j + \delta$ for $j$ the basic variable of row $\ell$. Then $y$ changes, and every nonbasic reduced cost becomes $\bar c_k - \delta\, (A_B^{-1} A_k)_\ell$. The basis stays optimal while all of these are nonnegative, again an interval of $\delta$. Feasibility does not change.

**A new variable.** Add a column $A_{n+1}$ with cost $c_{n+1}$. The old basis is still feasible. It stays optimal if $\bar c_{n+1} = c_{n+1} - y^\top A_{n+1} \ge 0$. Otherwise the new variable enters, and the primal simplex continues from the old basis. This is the step of [column generation](/column-generation/).

**A new constraint.** If the old optimum satisfies it, the old optimum is still optimal. Otherwise, add the row with a new slack variable in the basis: the new basis is dual feasible but primal infeasible, and the dual simplex method continues. This is how [cutting planes](/branch-and-cut/) and [branch and bound](/land-doig-algorithm/) re-solve LPs quickly.

**Global picture.** Over all $b$, the optimal value is a piecewise linear convex function of $b$ for a minimization; over all $c$, it is piecewise linear and concave. The pieces correspond to bases. [Parametric linear programming](/parametric-linear-programming/) traces these functions along a line.

## Examples

The running example is $\max 3x_1 + 2x_2$ subject to $x_1 + x_2 \le b_1 = 4$, $x_1 + 3x_2 \le b_2 = 9$, $x_1 \le b_3 = 3$, $x \ge 0$. The optimal basis is $\{x_1, x_2, s_2\}$, with $x^* = (3, 1)$, slack $s_2 = 3$, value 11, and shadow prices $y = (2, 0, 1)$. In this basis, $x_1 = b_3$, $x_2 = b_1 - b_3$ and $s_2 = b_2 - 3 b_1 + 2 b_3$.

**Ranges of the right-hand sides.** The basic variables stay nonnegative exactly when $b_3 \ge 0$, $b_1 \ge b_3$ and $b_2 - 3b_1 + 2b_3 \ge 0$. Changing one value at a time:

| data | range | value in the range |
|---|---|---|
| $b_1$ | $3 \le b_1 \le 5$ | $11 + 2(b_1 - 4)$ |
| $b_2$ | $b_2 \ge 6$ | $11$ |
| $b_3$ | $3/2 \le b_3 \le 4$ | $11 + (b_3 - 3)$ |

At $b_1 = 5$, $s_2$ reaches 0. For $b_1 > 5$, the dual simplex method pivots $s_2$ out and $s_1$ in, and the value stays at 13, with shadow price 0 for row 1.

**Ranges of the costs.** The point $(3, 1)$ stays optimal while the objective vector $(c_1, c_2)$ lies in the cone spanned by the normals $(1, 1)$ and $(1, 0)$ of the two tight rows, that is $c_1 \ge c_2 \ge 0$. With $c_2 = 2$ fixed, the range is $c_1 \ge 2$. With $c_1 = 3$ fixed, it is $0 \le c_2 \le 3$. At $c_2 = 3$ the objective is parallel to row 1, and every point of the edge from $(3, 1)$ to $(3/2, 5/2)$ is optimal.

**A new product.** A third product with profit $p$ uses one unit of row 1 and two units of row 2. Its reduced cost, for the maximization, is $p - y^\top (1, 2, 0) = p - 2$. For $p = 3/2$ it is negative, and the plan does not change. For $p = 4$ it is $2 > 0$, so the product enters; the simplex method from the old basis reaches the new optimum $(x_1, x_2, x_3) = (0, 0, 4)$ with value 16.

**A new constraint.** Add $x_2 \le 1/2$. The old optimum violates it. One dual simplex pivot gives $(3, 1/2)$ with value 10.

## Where it is used

- Reports of LP solvers: for each constraint, the shadow price and the range of its right-hand side; for each variable, the reduced cost and the range of its cost.
- Warm starts: [branch and bound](/land-doig-algorithm/) and [branch and cut](/branch-and-cut/) change a bound or add a cut, then re-solve with the [dual simplex method](/dual-simplex-method/) from the parent's basis.
- [Column generation](/column-generation/): each new column is tested by its reduced cost.
- [Parametric linear programming](/parametric-linear-programming/): follows the changes past the ranges, basis after basis.
- Simultaneous changes: the 100 percent rule of Bradley, Hax and Magnanti allows several changes at once if the sum of the fractions of their ranges used is at most one.

**Pitfalls.** The ranges belong to the basis, not to the optimal point. At a degenerate optimum, several bases describe the same point, and different solvers can report different ranges and different shadow prices; a range can then have width 0 on one side, while the optimal value still changes smoothly on that side. Ranges for one number at a time say nothing about joint changes, except through rules such as the 100 percent rule. And for integer programs, LP sensitivity analysis describes only the [LP relaxation](/lp-relaxation/).

## References
