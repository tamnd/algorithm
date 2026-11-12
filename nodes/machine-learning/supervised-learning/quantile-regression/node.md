---
tag: HBFAEF
kind: algorithm
slug: quantile-regression
name: Quantile regression
aliases:
- least absolute deviations
- regression quantiles
- linear quantile regression
area: machine-learning/supervised-learning
level: advanced
summary: Fit a linear conditional quantile by minimizing the pinball loss, a linear program. Some optimal fit passes through d of the points.
solves: [regression]
model: real-ram
complexity:
  vars: {n: the number of examples, d: the number of features, p: the number of simplex pivots}
  time: {worst: O(p n (n + d))}
  space: {extra: O(n (n + d))}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1978
  people: [Roger Koenker, Gilbert Bassett]
  note: Koenker and Bassett defined regression quantiles in 1978 as the minimizers of the check loss, and proved the interpolation property.
prereqs: [linear-regression, linear-programming-problem, simplex-method]
see_also: [isotonic-regression, bland-rule, ordinary-least-squares, interior-point-method, support-vector-regression, loss-function, basic-feasible-solution]
sources:
  - paper: doi:10.2307/1913643
    title: Roger Koenker and Gilbert Bassett Jr., Regression quantiles, Econometrica 46(1), 1978
    locator: pp. 33 to 50 (the definition by the check function, the linear program, Theorem 3.1 on interpolation of d points, and the bounds on the numbers of positive and negative residuals)
  - book: isbn:9780521608275
    title: Roger Koenker, Quantile Regression, Cambridge University Press, 2005
    locator: Chapter 1 (the check function and the quantile as a minimizer), Chapter 2 (the fundamentals, including the subgradient conditions and the interpolation property) and Chapter 6 (computation by the simplex method and interior point methods)
  - paper: doi:10.1137/0710069
    title: I. Barrodale and F. D. K. Roberts, An improved algorithm for discrete l1 linear approximation, SIAM Journal on Numerical Analysis 10(5), 1973
    locator: pp. 839 to 848 (the specialized simplex method for least absolute deviations)
  - paper: doi:10.1287/moor.2.2.103
    title: Robert G. Bland, New finite pivoting rules for the simplex method, Mathematics of Operations Research 2(2), 1977
    locator: pp. 103 to 107 (the smallest index rule prevents cycling)
  - paper: "Roger W. Koenker and Vasco d'Orey, Algorithm AS 229, computing regression quantiles, Applied Statistics 36(3), 1987"
    locator: pp. 383 to 393 (the Barrodale and Roberts method for any quantile)
  - paper: "David Avis and Vašek Chvátal, Notes on Bland's pivoting rule, Mathematical Programming Study 8, 1978"
    locator: pp. 24 to 34 (exponential examples for the smallest index rule)
  - paper: doi:10.1214/ss/1030037960
    title: Stephen Portnoy and Roger Koenker, The Gaussian hare and the Laplacian tortoise, computability of squared-error versus absolute-error estimators, Statistical Science 12(4), 1997
    locator: pp. 279 to 300 (interior point methods and preprocessing for large quantile regressions)
---

Quantile regression fits a linear model $x^\top w$ to the conditional $\tau$-quantile of the response, for a level $0 < \tau < 1$, by minimizing the pinball (check) loss of the residuals. Koenker and Bassett (1978) defined it and showed that it is a [linear program](/linear-programming-problem/). With $\tau = 1/2$ it is least absolute deviations (median) regression. This page solves the linear program exactly with the [simplex method](/simplex-method/) and [Bland's rule](/bland-rule/), and shows that some optimal fit passes through $d$ of the data points.

## In plain words

Least squares draws the line that best follows the average of the response. Sometimes you want a line that follows a low or a high part of the data instead: the line below which a quarter of the points fall, or the median line.

To get the quarter line, give each point a price. A point above the line costs a quarter of its distance, and a point below the line costs three quarters of its distance. The best line under these prices has about a quarter of the points below it. The prices are straight lines in the distance, so the problem is a linear program, and the best line can be chosen to pass exactly through as many points as there are coefficients.

## The problem

The data are $n$ examples $(x_i, y_i)$ with $x_i \in \mathbb{R}^d$ (usually the first feature is the constant 1 for the intercept) and $y_i \in \mathbb{R}$. $X$ is the $n \times d$ matrix with rows $x_i^\top$. For $\tau \in [0, 1]$, the check loss is

$$\rho_\tau(r) = r\,(\tau - \mathbf{1}[r < 0]) = \begin{cases} \tau r & r \ge 0, \\ (\tau - 1) r & r < 0. \end{cases}$$

The regression quantile is any minimizer

$$\hat w \in \arg\min_{w \in \mathbb{R}^d} \sum_{i=1}^{n} \rho_\tau(y_i - x_i^\top w).$$

With only an intercept ($d = 1$, $x_i = 1$), the minimizers are exactly the sample $\tau$-quantiles of $y$. In the population, if $y$ given $x$ has a continuous distribution, the minimizer of $\mathbb{E}\,\rho_\tau(y - q)$ over $q$ is the $\tau$-quantile of $y$ given $x$. The data model is the usual one of [regression](/regression/): the pairs are drawn i.i.d., and the model assumes that the conditional quantile is linear in $x$.

**The linear program.** Split each residual into its positive and negative parts, $u_i, v_i \ge 0$, and the free vector $w$ into $w = w^+ - w^-$ with $w^+, w^- \ge 0$:

$$\min \; \tau \sum_i u_i + (1 - \tau)\sum_i v_i \quad \text{subject to} \quad X w^+ - X w^- + u - v = y, \quad w^+, w^-, u, v \ge 0 .$$

It has $n$ equality rows and $2d + 2n$ variables.

## The algorithm

The columns are numbered $w^+_1, \dots, w^+_d, w^-_1, \dots, w^-_d, u_1, \dots, u_n, v_1, \dots, v_n$. $T$ is the simplex tableau $[A \mid b]$ in the current basis, and $c$ is the cost vector.

```pseudo id=main
QUANTILE-REGRESSION(X, y, τ)               ▷ exact arithmetic, 0 ≤ τ ≤ 1
L1  T ← the rows [x_iᵀ, −x_iᵀ, e_iᵀ, −e_iᵀ | y_i] for i = 1 .. n
L2  for i ← 1 to n: if y_i < 0 then negate row i and make v_i basic, else make u_i basic
L3  loop
L4      c̄_j ← c_j − Σ_i c(basis_i) · T[i][j] for each column j     ▷ reduced costs
L5      if c̄_j ≥ 0 for each j then exit the loop                  ▷ optimal
L6      e ← the smallest j with c̄_j < 0                           ▷ Bland's rule
L7      R ← {i : T[i][e] > 0}                                     ▷ never empty, see below
L8      r ← the i in R with the least T[i][b] / T[i][e], ties to the least basis_i
L9      pivot on T[r][e]; basis_r ← e
L10 read the basic solution: basic variables from column b, the others 0
L11 return w = w⁺ − w⁻
```

Line L2 gives a feasible start at once. Row $i$ has the entry $+1$ in the column $u_i$ and $-1$ in the column $v_i$. If $y_i \ge 0$, the column $u_i$ is the unit vector $e_i$, and $u_i = y_i \ge 0$. If $y_i < 0$, the negated row has $+1$ in the column $v_i$, and $v_i = -y_i > 0$. So the basic columns form an identity matrix, the right side is non-negative, and no phase 1 is needed. The start is the fit $w = 0$.

Lines L4 to L9 are the [simplex method](/simplex-method/) on the tableau, with the smallest index rule of Bland (1977) for both the entering and the leaving variable. The rule rules out cycling, so the method stops. The loop never finds an empty set $R$, because the objective is a sum of non-negative terms: an empty $R$ would give a ray of feasible points along which the objective goes to $-\infty$.

## Example

Take six points $(x, y) = (1, 1), (2, 3), (3, 2), (4, 5), (5, 4), (6, 9)$ with an intercept, so $x_i = (1, x)$ and $d = 2$. For $\tau = 1/2$ the start is $w = 0$ with objective $\tfrac{1}{2}\sum y_i = 12$. Each pivot lowers the objective or keeps it:

| pivot | objective before | enters | leaves |
|---|---|---|---|
| 1 | 12 | $w^+_1$ | $u_1$ |
| 2 | 9 | $w^+_2$ | $u_3$ |
| 3 | 21/4 | $u_1$ | $w^+_1$ |
| 4 | 5 | $w^-_1$ | $u_5$ |
| 5 | 9/2 | $v_3$ | $w^-_1$ |
| 6 | 4 | $w^+_1$ | $u_1$ |
| 7 | 31/8 | $v_5$ | $w^+_1$ |
| 8 | 7/2 | $w^-_1$ | $u_4$ |

After 8 pivots all reduced costs are non-negative, and the objective is 3. The solution is $w^-_1 = 1/3$ and $w^+_2 = 4/3$, so the median line is

$$\hat y = -\tfrac{1}{3} + \tfrac{4}{3}x .$$

It passes through the points $(1, 1)$ and $(4, 5)$. The residuals are $(0, 2/3, -5/3, 0, -7/3, 4/3)$: two points above, two below and two on the line. The objective 3 is half of the sum of the absolute residuals, 6.

The same data at other levels give the line $\tfrac14 + \tfrac34 x$ for $\tau = 1/4$ (through the points at $x = 1$ and $x = 5$, objective $35/16$), and the line $\tfrac32 x$ for $\tau = 3/4$ (through the points at $x = 2$ and $x = 6$, objective $15/8$). Among all 15 lines through two of the points, the least objective at $\tau = 1/2$ is 3, the value that the simplex method found.

## Correctness

Three facts give correctness. The full proofs are in the correctness proof below.

1. **The linear program is the problem.** For a fixed $w$ with residual $r = y - Xw$, each feasible pair has $u - v = r$, so $u_i \ge \max(r_i, 0)$ and $v_i \ge \max(-r_i, 0)$, and the cost is at least $\sum_i \rho_\tau(r_i)$, with equality for the positive and negative parts. So the two minima are equal, and an optimal $w^+ - w^-$ is a regression quantile.
2. **The simplex method finds an optimum.** The start of line L2 is a [basic feasible solution](/basic-feasible-solution/). Bland's rule ends the loop after finitely many pivots. When all reduced costs are $\ge 0$, each feasible point has cost at least the current cost.
3. **Interpolation (Koenker and Bassett 1978, Theorem 3.1).** If $X$ has rank $d$, some optimal $w$ has zero residuals at $d$ points whose rows $x_i$ are linearly independent. The proof starts from any optimum and moves along a direction that keeps the zero residuals at zero. On that line the loss is linear near the optimum, so its slope is 0, and the move ends at a new zero residual with the same loss. Each move adds an independent row.

With an intercept column, each optimum also has at most $n\tau$ negative residuals and at most $n(1 - \tau)$ positive residuals. This is the sample quantile property in regression form.

## Complexity

Count exact arithmetic operations on a [real RAM](/real-ram/) (with rationals, each operation also grows the numbers; their size stays polynomial in the input size, because each tableau entry is a ratio of two minors of the constraint matrix).

- The tableau has $n$ rows and $2d + 2n + 1$ columns, so it uses $O(n(n + d))$ memory.
- Line L4 costs $O(n(n + d))$ as written. Line L9 updates each row once, also $O(n(n + d))$.
- So the time is $O(p \, n(n + d))$ for $p$ pivots.

The number of pivots $p$ is finite, but Bland's rule takes an exponential number of pivots on some linear programs (Avis and Chvátal 1978), so no polynomial bound holds for this method in general. For quantile regression the specialized simplex method of Barrodale and Roberts (1973), adapted to $\tau \ne 1/2$ by Koenker and d'Orey (1987), is fast in practice for $n$ up to some thousands. [Interior point methods](/interior-point-method/) solve the linear program in polynomial time, and Portnoy and Koenker (1997) combined them with preprocessing for large $n$.

## Properties

- **Exact.** With rational data, the method returns an exact optimal vertex.
- **Not unique in general.** The loss is piecewise linear, so the set of minimizers is a polyhedron and can have more than one point. With an intercept only and $n\tau$ an integer, each value between two order statistics is optimal.
- **Robust in $y$.** Moving a point far up or down without changing the sign of its residual does not change the fit: only the sign of each residual enters the optimality conditions.
- **Equivariant.** Scaling $y$ by $a > 0$ scales $\hat w$ by $a$, and adding $Xg$ to $y$ adds $g$ to $\hat w$.
- **Crossing.** Fits at two levels $\tau_1 < \tau_2$ can cross for some $x$, because each level is fitted on its own.

## Variants and improvements

- **Barrodale and Roberts.** A simplex method for the $L_1$ problem that takes several pivots in one step, the classic solver of quantile regression.
- **Parametric programming in $\tau$.** The whole family of fits for all $\tau$ has finitely many distinct solutions, and the simplex method can follow it from one $\tau$ to the next.
- **Interior point methods.** The Frisch-Newton method of Portnoy and Koenker solves large problems.
- **Penalized quantile regression.** An $L_1$ penalty $\lambda \|w\|_1$ keeps the problem a linear program, as in the [lasso](/lasso-regression/).
- **Smooth surrogates.** Gradient methods on a smoothed check loss scale to very large data, but they give an approximate answer.

## When to use it

Use quantile regression when the spread or the shape of $y$ changes with $x$, when you need a prediction interval and not only a mean, or when the errors have heavy tails, where the median fit is more stable than [ordinary least squares](/ordinary-least-squares/). Use OLS when the errors are close to Gaussian and only the mean matters: it has a closed form and is faster. For a monotone fit with no linear model, see [isotonic regression](/isotonic-regression/).

## Pitfalls

- **No feasible start for negative $y_i$.** Line L2 must negate the rows with $y_i < 0$ and make $v_i$ basic. Making $u_i$ basic in every row gives $u_i = y_i < 0$, an infeasible start.
- **A free $w$ without the split.** The simplex method needs $w \ge 0$. Without the columns $w^-$ the method finds the best fit with non-negative coefficients, which is a different problem.
- **The largest coefficient rule in floating point.** With Dantzig's rule and rounding, degenerate pivots can cycle. Line L6 uses Bland's rule, and the implementation uses exact fractions.
- **Reading a unique answer.** Software returns one vertex, but the optimum can be a whole edge or face. Report the objective, or check the uniqueness, before you interpret one coefficient.
- **Loss scaled by two.** The objective at $\tau = 1/2$ is half the sum of absolute residuals. This does not change the minimizer, but it changes reported loss values.

## Implementations

## History

Koenker and Bassett (1978) defined regression quantiles for each $\tau$ by the check function, wrote them as a linear program, and proved the interpolation property and the bounds on the numbers of positive and negative residuals. Barrodale and Roberts (1973) gave the specialized simplex method that became the standard solver. Koenker's book (2005) covers the theory and the computation.

## References
