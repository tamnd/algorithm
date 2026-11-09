---
tag: 1E36EE
kind: problem
slug: portfolio-optimization
name: Portfolio optimization
aliases:
- Markowitz portfolio selection
- mean-variance optimization
- mean-variance portfolio selection
area: optimization/convex-optimization
level: intro
summary: Choose asset weights trading off expected return against variance.
prereqs: [quadratic-programming, covariance-matrix]
see_also: [quadratic-programming, covariance-matrix, second-order-cone-programming, kkt-conditions, weighted-sum-method, mixed-integer-programming, online-convex-optimization, linear-programming-problem]
sources:
  - paper: doi:10.1111/j.1540-6261.1952.tb01525.x
    title: Harry Markowitz, Portfolio selection, The Journal of Finance 7(1), 1952
    locator: pages 77 to 91
  - paper: doi:10.1002/nav.3800030110
    title: Harry Markowitz, The optimization of a quadratic function subject to linear constraints, Naval Research Logistics Quarterly 3, 1956
    locator: pages 111 to 133 (the critical line algorithm)
  - paper: doi:10.2307/2296205
    title: James Tobin, Liquidity preference as behavior towards risk, The Review of Economic Studies 25(2), 1958
    locator: pages 65 to 86 (the separation theorem with a riskless asset)
  - paper: doi:10.2307/2329621
    title: Robert C. Merton, An analytic derivation of the efficient portfolio frontier, Journal of Financial and Quantitative Analysis 7(4), 1972
    locator: pages 1851 to 1872
  - paper: doi:10.1111/j.1540-6261.1964.tb02865.x
    title: William F. Sharpe, Capital asset prices, a theory of market equilibrium under conditions of risk, The Journal of Finance 19(3), 1964
    locator: pages 425 to 442
  - paper: doi:10.21314/JOR.2000.038
    title: R. Tyrrell Rockafellar and Stanislav Uryasev, Optimization of conditional value-at-risk, The Journal of Risk 2(3), 2000
    locator: pages 21 to 41
  - paper: doi:10.2469/faj.v45.n1.31
    title: Richard O. Michaud, The Markowitz optimization enigma, is optimized optimal?, Financial Analysts Journal 45(1), 1989
    locator: pages 31 to 42
  - paper: doi:10.2469/faj.v48.n5.28
    title: Fischer Black and Robert Litterman, Global portfolio optimization, Financial Analysts Journal 48(5), 1992
    locator: pages 28 to 43
  - paper: doi:10.1111/j.1467-9965.1991.tb00002.x
    title: Thomas M. Cover, Universal portfolios, Mathematical Finance 1(1), 1991
    locator: pages 1 to 29
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 4.4 (Markowitz portfolio optimization as a QP, and portfolio problems with loss risk constraints as SOCPs)
---

Portfolio optimization chooses how to split a budget among $n$ assets whose returns are random. In the mean-variance model of Markowitz (1952), each portfolio is judged by two numbers: its expected return $\mu^\top w$ and its variance $w^\top\Sigma w$, where $\mu$ is the vector of expected returns and $\Sigma$ the [covariance matrix](/covariance-matrix/). The problem is to find the portfolio with the least variance for a required expected return, or the best trade-off between the two. Because $\Sigma$ is positive semidefinite, this is a convex [quadratic program](/quadratic-programming/). Without bounds on the weights it has a closed-form solution, and the set of best portfolios, the efficient frontier, is a hyperbola. With realistic constraints, such as no short sales, it is solved by QP methods. Extensions with other risk measures lead to [second-order cone programs](/second-order-cone-programming/), linear programs and mixed-integer programs.

## In plain words

You have some money and several things to invest in. Some are likely to grow a lot but swing up and down wildly. Others grow slowly but steadily. Mixing them helps, because when one goes down another may go up, so the swings partly cancel. Portfolio optimization finds the mix with the smallest swings for the growth you want. If you ask for more growth, you must accept bigger swings. The list of all best mixes, one for each level of growth, shows the price of growth in extra risk, and you pick the point on that list that suits you.

## Definition

**Input.** A vector $\mu \in \mathbb{R}^n$ of expected returns, a positive semidefinite covariance matrix $\Sigma \in \mathbb{R}^{n \times n}$, a target return $\rho$, and a set $W$ of allowed weight vectors: $W = \mathbb{R}^n$ if short sales are allowed, or $W = \{w : w \ge 0\}$ if not.

**Problem.** The mean-variance problem is the convex QP

$$\min_{w}\ w^\top\Sigma w \quad\text{s.t.}\quad \mathbf{1}^\top w = 1, \quad \mu^\top w \ge \rho, \quad w \in W.$$

Here $w_i$ is the fraction of the budget in asset $i$. An equivalent form fixes a risk aversion $\gamma > 0$ and maximizes $\mu^\top w - \gamma\,w^\top\Sigma w$ subject to the same budget and sign constraints. As $\rho$ or $\gamma$ varies, the optimal points trace the efficient frontier.

**Output.** An optimal weight vector $w^*$, or a report that no allowed portfolio reaches the return $\rho$.

**Optimality.** All constraints are linear, so $w$ is optimal exactly when it is feasible and there are multipliers $\lambda$, $\nu \ge 0$ and $\eta \ge 0$ with

$$2\Sigma w = \lambda\mathbf{1} + \nu\mu + \eta, \qquad \nu(\mu^\top w - \rho) = 0, \qquad \eta_iw_i = 0,$$

where $\eta = 0$ if short sales are allowed. These are the [KKT conditions](/kkt-conditions/). The multiplier $\nu$ is the rate at which the least variance grows with the target return.

**The closed form.** If short sales are allowed and $\Sigma$ is positive definite, let $A = \mathbf{1}^\top\Sigma^{-1}\mathbf{1}$, $B = \mathbf{1}^\top\Sigma^{-1}\mu$, $C = \mu^\top\Sigma^{-1}\mu$ and $D = AC - B^2$. For $\rho \ge B/A$, the optimal portfolio is

$$w^* = \frac{C - B\rho}{D}\,\Sigma^{-1}\mathbf{1} + \frac{A\rho - B}{D}\,\Sigma^{-1}\mu, \qquad w^{*\top}\Sigma w^* = \frac{A\rho^2 - 2B\rho + C}{D}.$$

So every frontier portfolio is a mix of the same two portfolios, which is the two-fund theorem (Merton, 1972), and the frontier is a hyperbola in the plane of standard deviation and expected return. The global minimum-variance portfolio is $\Sigma^{-1}\mathbf{1}/A$, with variance $1/A$ and return $B/A$.

## Variants

- **A riskless asset.** With a riskless rate $r_f$, every optimal portfolio is a mix of the riskless asset and one tangency portfolio, proportional to $\Sigma^{-1}(\mu - r_f\mathbf{1})$ when short sales are allowed (Tobin, 1958). The tangency portfolio maximizes the Sharpe ratio $(\mu^\top w - r_f)/\sqrt{w^\top\Sigma w}$.
- **Maximum Sharpe ratio with constraints.** The ratio is not concave, but with $y = w/\kappa$ for a scale $\kappa > 0$ the problem becomes the convex QP $\min y^\top\Sigma y$ subject to $(\mu - r_f\mathbf{1})^\top y = 1$ and $y \ge 0$, and $w = y/\mathbf{1}^\top y$.
- **Risk as a constraint.** Maximize $\mu^\top w$ subject to $\|\Sigma^{1/2}w\| \le \sigma$, a second-order cone constraint.
- **Other risk measures.** Conditional value-at-risk over $T$ scenarios gives a linear program with $O(n + T)$ variables (Rockafellar and Uryasev, 2000). Mean absolute deviation also gives an LP.
- **Practical constraints.** Transaction costs $c^\top|w - w_0|$, bounds on sectors and turnover keep the problem a QP or an SOCP. A limit on the number of assets or minimum lot sizes make it a [mixed-integer](/mixed-integer-programming/) QP.
- **Robust and Bayesian models.** Let $\mu$ lie in an ellipsoid (an SOCP), or blend market equilibrium returns with investor views (Black and Litterman, 1992).
- **Growth-optimal portfolios.** Maximize the expected logarithm of wealth instead, which is a concave problem. In the online setting, universal portfolios (Cover, 1991) and [online convex optimization](/online-convex-optimization/) compete with the best constant mix in hindsight.

## Examples

Take three uncorrelated assets with $\mu = (1, 2, 3)$ and $\Sigma = \operatorname{diag}(1, 2, 4)$, in percent per period. Then $A = \tfrac74$, $B = \tfrac{11}{4}$, $C = \tfrac{21}{4}$ and $D = \tfrac{13}{8}$.

| target $\rho$ | short sales | $w^*$ | variance |
|---|---|---|---|
| none ($\rho \le \tfrac{11}{7}$) | either | $(\tfrac47, \tfrac27, \tfrac17)$ | $\tfrac47$ |
| 2 | either | $(\tfrac{4}{13}, \tfrac{5}{13}, \tfrac{4}{13})$ | $\tfrac{10}{13}$ |
| 5/2 | either | $(0, \tfrac12, \tfrac12)$ | $\tfrac32$ |
| 11/4 | allowed | $(-\tfrac{2}{13}, \tfrac{29}{52}, \tfrac{31}{52})$ | $\tfrac{215}{104}$ |
| 11/4 | not allowed | $(0, \tfrac14, \tfrac34)$ | $\tfrac{19}{8}$ |

The first rows follow from the closed form, and they have no negative weights, so they also solve the long-only problem. For $\rho = 2$, the variance $(A\rho^2 - 2B\rho + C)/D = \tfrac{5/4}{13/8} = \tfrac{10}{13}$ matches $\tfrac{16}{169} + 2 \cdot \tfrac{25}{169} + 4 \cdot \tfrac{16}{169}$. Above $\rho = \tfrac52$, the closed form shorts asset 1, so the long-only answer is different. For $\rho = \tfrac{11}{4}$ without short sales, the point $(0, \tfrac14, \tfrac34)$ has $2\Sigma w = (0, 1, 6)$, and

$$(0, 1, 6) = -9 \cdot (1, 1, 1) + 5 \cdot (1, 2, 3) + (4, 0, 0),$$

so the KKT conditions hold with $\lambda = -9$, $\nu = 5$ and $\eta = (4, 0, 0) \ge 0$. The dual value $\lambda + \nu\rho - \tfrac14(\lambda\mathbf{1} + \nu\mu + \eta)^\top\Sigma^{-1}(\lambda\mathbf{1} + \nu\mu + \eta)$ is $-9 + \tfrac{55}{4} - \tfrac14(0 + \tfrac12 + 9) = \tfrac{19}{8}$, equal to the variance, so the duality gap is $0$. The ban on short sales costs $\tfrac{19}{8} - \tfrac{215}{104} = \tfrac{32}{104} = \tfrac{4}{13}$ in variance. The multiplier $\nu = 5$ is the slope of the long-only frontier there: on assets 2 and 3 the variance is $2(3 - \rho)^2 + 4(\rho - 2)^2$, with derivative $5$ at $\rho = \tfrac{11}{4}$.

With $r_f = 0$, the tangency portfolio is proportional to $\Sigma^{-1}\mu = (1, 1, \tfrac34)$, that is, $(\tfrac{4}{11}, \tfrac{4}{11}, \tfrac{3}{11})$, with return $\tfrac{21}{11}$, variance $\tfrac{84}{121}$ and the Sharpe ratio $\sqrt{C} = \sqrt{21}/2$.

## Known algorithms

- **The closed form.** With only the budget and return equations, solve two linear systems with $\Sigma$, in $O(n^3)$ time for a dense matrix, or less with a factor model.
- **The critical line algorithm.** Markowitz (1956) traced the whole long-only frontier as a piecewise linear path in $w$: between breakpoints, the set of zero weights is fixed and $w$ moves linearly in $\rho$. At each breakpoint one weight enters or leaves the set. It is a parametric active-set method for QP.
- **General QP methods.** Active-set methods, primal-dual [interior-point methods](/interior-point-method/), and first-order methods such as ADMM handle bounds, sectors and transaction costs. With a factor model $\Sigma = FF^\top + \operatorname{diag}(d)$ with $k$ factors, one interior-point step costs $O(nk^2)$ instead of $O(n^3)$.
- **Branch and bound.** For cardinality and lot constraints, mixed-integer QP solvers use the convex QP as the relaxation.
- **Scenario LPs.** For CVaR, solve the LP of Rockafellar and Uryasev with the [simplex method](/simplex-method/) or an interior-point method.

## Bounds

- **Polynomial time.** The mean-variance problem with linear constraints is a convex QP, so it is solvable in polynomial time, and with rational data the optimum is rational, as in the example.
- **Unconstrained case.** The closed form needs one factorization of $\Sigma$, so $O(n^3)$ arithmetic operations for dense data.
- **Cardinality limits.** With a limit on the number of assets held, the problem is a mixed-integer QP, and no polynomial algorithm is known for it.
- **Statistical limits.** The answer is only as good as $\mu$ and $\Sigma$. The sample covariance of $T$ observations of $n$ assets has rank at most $T - 1$, so it is singular when $T \le n$, and errors in $\mu$ are amplified by the optimizer, which tends to put large weights on the assets whose returns are most overestimated (Michaud, 1989).

## Reductions

- **Portfolio selection to QP.** The definition above is a QP with $Q = 2\Sigma$.
- **Frontier to scalarization.** The frontier is the set of Pareto-optimal points of the two objectives, return and variance. Because both the objective and the constraints are convex, the [weighted-sum method](/weighted-sum-method/), the risk-aversion form, finds every frontier point.
- **Standard-deviation constraint to SOCP.** With $\Sigma = LL^\top$, $w^\top\Sigma w \le \sigma^2$ is $\|L^\top w\| \le \sigma$.
- **CVaR to LP.** $\operatorname{CVaR}_\beta$ of the loss over $T$ equally likely scenarios is $\min_t t + \frac{1}{(1 - \beta)T}\sum_s\max(0, \ell_s(w) - t)$, which is an LP after one variable per scenario.
- **Least squares.** For the closed form, minimizing $w^\top\Sigma w$ with $\Sigma = R^\top R/T$ for centered returns $R$ is a [least-squares problem](/least-squares-problem/) with linear equality constraints.

## Applications

- **Asset allocation.** Pension funds and other investors choose weights across stocks, bonds and other classes, usually with many practical constraints.
- **Asset pricing.** If all investors hold mean-variance optimal portfolios, the capital asset pricing model (Sharpe, 1964) follows, with the market portfolio as the tangency portfolio.
- **Index tracking.** Minimize the variance of the difference between the portfolio and a benchmark, a QP of the same form.
- **Risk budgeting and hedging.** Minimum-variance hedges and risk-parity portfolios use the same covariance model.
- **Beyond finance.** The same model chooses a mix of energy sources, projects or crop varieties with uncertain yields.

## References
