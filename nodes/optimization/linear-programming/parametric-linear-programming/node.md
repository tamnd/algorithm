---
tag: SF3F4C
kind: problem
slug: parametric-linear-programming
name: Parametric linear programming
aliases:
- parametric LP
- parametric programming
- parametric simplex
area: optimization/linear-programming
level: advanced
summary: Solve an LP whose coefficients vary linearly with a parameter and track the optimal basis as it changes.
prereqs: [lp-sensitivity-analysis]
see_also: [lp-sensitivity-analysis, shadow-price, reduced-cost, simplex-method, dual-simplex-method, smoothed-simplex-analysis, parametric-max-flow-problem, klee-minty-cube]
sources:
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Section 5.5, Parametric programming (the optimal cost as a piecewise linear concave function of the parameter, and the parametric simplex method)
  - paper: doi:10.1002/nav.3800020106
    title: Saul Gass and Thomas Saaty, The computational algorithm for the parametric objective function, Naval Research Logistics Quarterly 2, 39 to 45 (1955)
    locator: the parametric simplex method for an objective that depends linearly on one parameter
  - paper: doi:10.1007/BF01581642
    title: Katta G. Murty, Computational complexity of parametric linear programming, Mathematical Programming 19, 213 to 219 (1980)
    locator: a family of parametric LPs with exponentially many breakpoints
---

Parametric linear programming asks for the optimal solutions of a whole family of linear programs, in which the objective or the right-hand side depends linearly on a real parameter $\lambda$. The answer is a finite list of breakpoints $\lambda_1 < \cdots < \lambda_K$ and, between two breakpoints, one optimal basis. The optimal value is a piecewise linear function of $\lambda$, convex or concave depending on the case. The parametric simplex method finds all pieces with one pivot per breakpoint, so it extends [sensitivity analysis](/lp-sensitivity-analysis/) from one range to the whole line. The number of breakpoints can be exponential, and its average behavior is the core of the [smoothed analysis](/smoothed-simplex-analysis/) of the simplex method.

## In plain words

Sometimes one number of a planning problem is not known, or you want to see the effect of every possible value: the price of a product, the size of a budget, a weight between two goals. Parametric linear programming answers the problem for all values at once. The best plan does not change smoothly. It stays fixed for a while, then jumps to a new plan at a switching point, and the profit changes at a constant rate between the switching points. The method starts with the best plan for one value, finds where it stops being best, makes one swap there, and repeats.

## Definition

**Cost parametric.** Given $A \in \mathbb{Q}^{m \times n}$, $b \in \mathbb{Q}^m$, $c, d \in \mathbb{Q}^n$ and an interval $\Lambda$ of real numbers, let

$$z(\lambda) = \min\ \{ (c + \lambda d)^\top x \;:\; Ax = b,\ x \ge 0 \}, \qquad \lambda \in \Lambda.$$

**Right-hand side parametric.** Given $g \in \mathbb{Q}^m$, let $w(\lambda) = \min\, \{ c^\top x : Ax = b + \lambda g,\ x \ge 0 \}$.

**Output.** Breakpoints $\lambda_1 < \cdots < \lambda_K$ in $\Lambda$ and, for each interval between two consecutive breakpoints (and the two end intervals), a basis that is optimal for every $\lambda$ in it, or a statement that the program is infeasible or unbounded there.

**Shape of the answer.** For a fixed basis $B$, the conditions "feasible" ($A_B^{-1} b \ge 0$) and "optimal" (reduced costs $c + \lambda d - A^\top A_B^{-\top}(c_B + \lambda d_B) \ge 0$) are linear in $\lambda$ in the cost case, so each basis is optimal on a closed interval. Since $z(\lambda)$ is the minimum over the finitely many vertices of the fixed feasible region of linear functions of $\lambda$, $z$ is piecewise linear and concave where it is finite. In the right-hand side case the feasible region moves, but the dual feasible region is fixed, and the same argument on the dual makes $w$ piecewise linear and convex.

## Variants

- **Both sides at once.** If $\lambda$ appears in both $c$ and $b$, the value is still piecewise in $\lambda$, but each piece is quadratic, and the function need not be convex or concave.
- **Parametric matrix entries.** If $\lambda$ appears in $A$, the basic solutions are rational functions of $\lambda$, and the analysis is much harder.
- **Several parameters.** In multiparametric LP, the parameter is a vector, and the parameter space splits into polyhedral *critical regions*, one per optimal basis. This is used in explicit model predictive control.
- **Bicriteria LP.** Minimizing $c^\top x$ and $d^\top x$ at once: the Pareto optimal values are traced by the cost parametric problem with weights $(1, \lambda)$.
- **Network special cases.** [Parametric max flow](/parametric-max-flow-problem/) with capacities that move monotonically in $\lambda$ has at most $n - 1$ breakpoints, all found in the time of one push-relabel max flow (Gallo, Grigoriadis and Tarjan, 1989). Parametric shortest paths and parametric min cost flow can have $n^{\Theta(\log n)}$ breakpoints (Carstensen, 1983).

## Examples

**Cost parametric.** On the running pentagon $x_1 + x_2 \le 4$, $x_1 + 3x_2 \le 9$, $x_1 \le 3$, $x \ge 0$, maximize $3x_1 + \lambda x_2$ for all real $\lambda$. A vertex is optimal while $(3, \lambda)$ lies in the cone of the outer normals of its tight rows:

| interval | optimal vertex | value |
|---|---|---|
| $\lambda \le 0$ | $(3, 0)$ | $9$ |
| $0 \le \lambda \le 3$ | $(3, 1)$ | $9 + \lambda$ |
| $3 \le \lambda \le 9$ | $(3/2, 5/2)$ | $9/2 + 5\lambda/2$ |
| $\lambda \ge 9$ | $(0, 3)$ | $3\lambda$ |

The breakpoints are 0, 3 and 9. At each one, the objective is parallel to an edge, and the whole edge is optimal. The slopes $0, 1, 5/2, 3$ increase, so the value is convex, as a maximum of linear functions must be. At $\lambda = 2$ this is the running example, with value 11.

**Right-hand side parametric.** With the objective $3x_1 + 2x_2$ and $b_1 = \lambda$, the value is $3\lambda$ for $0 \le \lambda \le 3$, $2\lambda + 3$ for $3 \le \lambda \le 5$ and $13$ for $\lambda \ge 5$, and the program is infeasible for $\lambda < 0$. The slopes are the [shadow prices](/shadow-price/) of row 1 in the three bases.

## Known algorithms

**The parametric simplex method** (Gass and Saaty, 1955) for the cost case:

1. Find an optimal basis $B$ for $\lambda = \lambda_{\text{start}}$, with the [simplex method](/simplex-method/).
2. The reduced costs are $\bar c_j(\lambda) = \bar c_j + \lambda \bar d_j$ for the nonbasic $j$. The basis stays optimal up to $\lambda^* = \min \{ -\bar c_j / \bar d_j : \bar d_j < 0 \}$, the first $\lambda$ at which a reduced cost reaches 0.
3. At $\lambda^*$, let the variable $j$ that attains the minimum enter the basis by a primal pivot with the [ratio test](/ratio-test/). If no variable can leave, the program is unbounded for $\lambda > \lambda^*$. Otherwise the new basis is optimal on an interval that starts at $\lambda^*$.
4. Repeat until no $\bar d_j < 0$ remains.

Each breakpoint costs one pivot, $O(mn)$ arithmetic operations with a tableau. The right-hand side case is the same on the dual, with [dual simplex](/dual-simplex-method/) pivots. Under degeneracy, one breakpoint can need several pivots, and an anti-cycling rule is needed.

**Self-dual parametric simplex.** Dantzig's self-dual method adds $\lambda$ times a positive vector to both $b$ and $c$, so that the slack basis is optimal for large $\lambda$, and then lowers $\lambda$ to 0. It solves an ordinary LP without a phase 1.

**The shadow vertex rule.** The cost parametric method visits the vertices of $P$ whose images are vertices of the projection of $P$ to the plane spanned by $c$ and $d$. Used as a pivot rule for ordinary LP, it is the *shadow vertex* simplex method of the [smoothed analysis](/smoothed-simplex-analysis/) of Spielman and Teng, who bounded the expected size of this two-dimensional shadow.

## Bounds

- **Upper bound.** Each basis is optimal on one interval, so the number of breakpoints is at most the number of bases, $\binom{n}{m}$.
- **Exponential lower bound.** Murty (1980) gave parametric LPs whose number of breakpoints is exponential in $n$, built in the style of the [Klee-Minty cube](/klee-minty-cube/). So the parametric simplex method, and the shadow vertex pivot rule, are exponential in the worst case.
- **Smoothed and average bounds.** Under random perturbation of the data, the expected number of breakpoints is polynomial in $m$, $n$ and the inverse of the perturbation size (Spielman and Teng). Earlier average case analyses by Borgwardt used the same rule.
- **Special structure.** Monotone parametric max flow has at most $n - 1$ breakpoints. Parametric shortest path and min cost flow have $n^{\Theta(\log n)}$ in the worst case (Carstensen, 1983; Gusfield, 1980).

## Reductions

- **Cost and right-hand side.** The cost parametric problem for (P) is the right-hand side parametric problem for its [dual](/dual-linear-program/), so one algorithm handles both.
- **Bicriteria to parametric.** The lower left boundary of the image $\{(c^\top x, d^\top x) : x \in P\}$ is traced by the cost parametric problem with weights $(1, \lambda)$, $\lambda \ge 0$.
- **Sensitivity analysis.** The first interval around the starting value is the range computed in [sensitivity analysis](/lp-sensitivity-analysis/); the parametric method continues past it.

## Applications

- Trade-off curves between two objectives, such as cost and risk.
- What-if analysis over the whole range of an uncertain price or capacity.
- Ratio problems: maximizing $c^\top x / d^\top x$ by searching for $\lambda$ with $\max (c - \lambda d)^\top x = 0$, as in Dinkelbach's method and in densest subgraph via [parametric max flow](/parametric-max-flow-problem/).
- Solving ordinary LPs by the self-dual parametric method.
- Explicit model predictive control, through multiparametric programming.

## References
