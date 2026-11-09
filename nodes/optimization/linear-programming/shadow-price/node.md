---
tag: X2MAEE
kind: concept
slug: shadow-price
name: Shadow price
aliases:
- dual value
- dual price
- marginal value
- marginal cost
area: optimization/linear-programming
level: core
summary: 'Optimal dual variable: the rate at which the optimum improves per unit increase of a resource.'
prereqs: [dual-linear-program, strong-duality]
see_also: [lp-sensitivity-analysis, reduced-cost, complementary-slackness, parametric-linear-programming, lagrangian-duality, column-generation, kkt-conditions, lp-duality]
sources:
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Section 4.4, Optimal dual variables as marginal costs, and Section 5.2, Global dependence on the right-hand side vector (the optimal value is a piecewise linear concave or convex function of b)
  - book: isbn:9780716715870
    title: Vašek Chvátal, Linear Programming, W. H. Freeman, 1983
    locator: Chapter 5, The duality theorem (the economic significance of the dual variables)
  - book: isbn:9780471982326
    title: Alexander Schrijver, Theory of Linear and Integer Programming, Wiley, 1986
    locator: Chapter 10, Section 10.4 (sensitivity analysis, and the change of the optimal value with the right-hand side)
---

The shadow price of a constraint in a linear program is the value of its variable in an optimal [dual](/dual-linear-program/) solution. It measures how much the optimal value would rise if the right-hand side of the constraint grew by one unit, as long as the change is small enough that the same basis stays optimal. A constraint that is not tight at the optimum has shadow price zero. In economic terms, the shadow price of a resource is the most it is worth paying for one more unit of it. Shadow prices are the main output of [sensitivity analysis](/lp-sensitivity-analysis/), and they are what [column generation](/column-generation/) uses to price new columns.

## In plain words

Suppose you plan production with limited machines, labor and material, and you have found the best plan. Now ask: if I had one more hour of a machine, how much more profit could I make? That amount is the shadow price of the machine. A machine that is already idle at the best plan has a shadow price of zero, since more of it would not help. The shadow prices come for free with the best plan, as the solution of the partner problem. They hold only for small changes; after a point, a different limit becomes the bottleneck, and the price changes.

## The idea

**Setting.** Take $\max c^\top x$ subject to $Ax \le b$, $x \ge 0$, with dual $\min b^\top y$ subject to $A^\top y \ge c$, $y \ge 0$. Write $z^*(b)$ for the optimal value as a function of the right-hand side $b$.

**Definition.** A *shadow price* of constraint $i$ is the value $y^*_i$ in an optimal dual solution $y^*$. For a minimization in equality form, $\min c^\top x$, $Ax = b$, $x \ge 0$, the shadow prices are an optimal $y$ of $\max b^\top y$, $A^\top y \le c$; at an optimal basis $B$ they are $y^\top = c_B^\top A_B^{-1}$, the simplex multipliers of the [reduced cost](/reduced-cost/) page.

**The optimal value is piecewise linear.** Assume the dual feasible set $D = \{y \ge 0 : A^\top y \ge c\}$ is not empty. It does not depend on $b$, and it has finitely many vertices $y^{(1)}, \ldots, y^{(K)}$, since it lies in $y \ge 0$. By [strong duality](/strong-duality/) and the [fundamental theorem](/fundamental-theorem-of-lp/), for every $b$ for which the primal is feasible,

$$z^*(b) = \min_{y \in D} b^\top y = \min_{k = 1, \ldots, K} b^\top y^{(k)}.$$

(The dual is bounded below for such $b$, by weak duality, so the minimum is at a vertex.) So $z^*$ is the minimum of finitely many linear functions of $b$: it is piecewise linear and concave on the set of $b$ where the primal is feasible.

**Shadow prices are slopes.** If the dual optimum $y^*$ at $b$ is unique, then $b^\top y^* < b^\top y^{(k)}$ for every other vertex, and these strict inequalities survive a small change of $b$. So near $b$,

$$z^*(b + \delta e_i) = z^*(b) + \delta\, y^*_i,$$

and $y^*_i = \partial z^* / \partial b_i$. If the dual optimum is not unique, which happens when the primal optimum is degenerate, $z^*$ has a kink at $b$. Then each optimal dual solution is a *supergradient*: $z^*(b') \le z^*(b) + (b' - b)^\top y^*$ for all $b'$. The right derivative in the direction $e_i$ is the smallest $y_i$ over the optimal dual solutions, and the left derivative is the largest.

**Complementary slackness.** By [complementary slackness](/complementary-slackness/), a constraint with slack at the optimum has $y^*_i = 0$: a resource that is not used up has no value at the margin. A positive shadow price means that the constraint is tight.

**Signs.** In a maximization with $\le$ rows, shadow prices are nonnegative: more resource never hurts. In a minimization with $\ge$ rows (requirements), they are nonnegative too, and give the extra cost per unit of extra requirement. For equations they can have either sign. Solvers report them with their own sign conventions, which should be checked.

## Examples

**The running example.** $\max 3x_1 + 2x_2$ subject to $x_1 + x_2 \le 4$, $x_1 + 3x_2 \le 9$, $x_1 \le 3$, $x \ge 0$ has the optimum $x^* = (3, 1)$ with value 11 and the unique dual optimum $y^* = (2, 0, 1)$.

- *Row 1, price 2.* Raising $b_1 = 4$ to $4 + \delta$ moves the optimum to $(3, 1 + \delta)$, with value $11 + 2\delta$, for $-1 \le \delta \le 1$.
- *Row 2, price 0.* At the optimum $x_1 + 3x_2 = 6 < 9$, so the row is slack, and small changes of $b_2$ do not change the value.
- *Row 3, price 1.* Raising $b_3 = 3$ to $3 + \delta$ moves the optimum to $(3 + \delta, 1 - \delta)$, with value $11 + \delta$, for $-3/2 \le \delta \le 1$.

**The whole value function of $b_1$.** With $b_2 = 9$ and $b_3 = 3$ fixed, exact computation over all vertices gives

$$z^*(b_1) = \begin{cases} 3 b_1 & 0 \le b_1 \le 3, \\ 2 b_1 + 3 & 3 \le b_1 \le 5, \\ 13 & b_1 \ge 5. \end{cases}$$

The slopes 3, 2 and 0 are the shadow prices of row 1 for the three optimal bases, and they decrease, as concavity requires. At $b_1 = 3$ the optimum $(3, 0)$ is degenerate (three rows are tight), the dual optimum is not unique, and the shadow price is any number between the right slope 2 and the left slope 3. At $b_1 = 5$ the price falls to 0, because row 2 becomes the bottleneck.

**Max flow.** In the [maximum flow LP](/max-flow-linear-program/), an optimal dual solution can be taken to be the indicator of the arcs of one minimum cut, so its shadow prices are 1 on those arcs and 0 on the others. If there are several minimum cuts, one more unit of capacity on an arc raises the maximum flow only when the arc lies in every minimum cut. This is the kink of the previous example: the right derivative is the smallest shadow price over all optimal dual solutions.

## Where it is used

- [Sensitivity analysis](/lp-sensitivity-analysis/): shadow prices and their ranges answer "what if a resource changes" without solving again.
- [Column generation](/column-generation/) and [Dantzig-Wolfe decomposition](/dantzig-wolfe-decomposition/): the master problem's shadow prices price the candidate columns in the subproblem.
- [Lagrangian relaxation](/lagrangian-duality/): Lagrange multipliers play the role of shadow prices for constraints moved into the objective, and the [KKT conditions](/kkt-conditions/) carry the same meaning for nonlinear programs.
- Economics: Kantorovich called them objectively determined valuations, and Koopmans used them as efficiency prices. In electricity markets, locational marginal prices are the shadow prices of the power balance constraints at each node of a dispatch LP.
- Decisions: buy one more unit of a resource only if its market price is below its shadow price; the [parametric](/parametric-linear-programming/) analysis tells how many units the price holds for.

## References
