---
tag: SH6FXB
kind: problem
slug: numerical-integration
name: Numerical integration
aliases:
- numerical quadrature
- quadrature
- approximate integration
area: numerical/quadrature
level: intro
summary: Approximate the definite integral of f over [a,b] using only function evaluations.
prereqs: []
see_also: [quadrature-rule, quadrature-error, gaussian-quadrature, adaptive-quadrature, multidimensional-integration, monte-carlo-integration, improper-integration, oscillatory-integration]
sources:
  - book: isbn:9780122063602
    title: Philip J. Davis and Philip Rabinowitz, Methods of Numerical Integration, second edition, Academic Press, 1984
    locator: Chapter 1, Introduction (Sections 1.1 to 1.5 on the problem and the Riemann integral, Section 1.10 on weight functions) and Section 4.2, Roundoff error for a fixed integration rule
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Chapter 5, Numerical integration
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 7, Numerical integration I, and Chapter 10, Numerical integration II
  - book: isbn:9781611975932
    title: Lloyd N. Trefethen, Approximation Theory and Approximation Practice, extended edition, SIAM, 2019
    locator: Chapter 19, Clenshaw-Curtis and Gauss quadrature (geometric convergence for analytic integrands)
  - paper: "Erich Novak, Deterministic and Stochastic Error Bounds in Numerical Analysis, Lecture Notes in Mathematics 1349, Springer, 1988"
    locator: Chapter 1 and Chapter 2 (optimal error of deterministic and randomized integration for the classes C^r, after Bakhvalov 1959)
---

Numerical integration is the problem of computing an approximation to a definite integral $\int_a^b f(x)\,dx$ when the program can only ask for values $f(x)$ at points of its choice. Every method answers with a [quadrature rule](/quadrature-rule/), a weighted sum of function values, and the quality of the answer depends on how smooth $f$ is and how many values the method asks for. The problem is the base of [multidimensional integration](/multidimensional-integration/), of [Monte Carlo integration](/monte-carlo-integration/) and of most solvers for [initial value problems](/ode-initial-value-problem/).

## In plain words

You have a function that a program can evaluate, but you have no formula for its area. You want the area under its graph between two points. Each evaluation costs time, sometimes a lot, so you want a good answer from few evaluations.

The usual plan is to evaluate the function at some chosen points, give each value a weight, and add up. The choice of points and weights is the whole art. A smooth function lets a clever choice reach full machine accuracy with a handful of points. A function with a kink, a jump or a spike at an end needs more points, or a change of variable. No method can promise a good answer for every function, because the function can do anything between the points that you looked at.

## Definition

We use one notation on all pages of this area. The weighted integral of $f$ over an interval $[a, b]$ with a weight function $w \ge 0$ is

$$I(f) = \int_a^b f(x)\,w(x)\,dx,$$

with $w = 1$ unless stated. A [quadrature rule](/quadrature-rule/) with $n$ nodes is

$$Q_n(f) = \sum_{i=1}^{n} w_i\,f(x_i),$$

where $n$ always counts the nodes $x_i$ (not the subintervals), and the $w_i$ are the weights. The error is $E_n(f) = I(f) - Q_n(f)$. For composite rules, $[a, b]$ is cut into $m$ equal subintervals of width $h = (b - a)/m$. Adaptive methods take a tolerance $\tau$. For integrals over a region of $\mathbb{R}^s$ we write $s$ for the dimension, $N$ for the number of sample points and $\sigma^2$ for the variance of $f$.

**Input.** Real numbers $a \le b$ (or a region), a weight function $w$, a way to evaluate $f$ at any point of $[a, b]$, and either a budget of $n$ evaluations or a tolerance $\tau$.

**Output.** A number $Q$ with $|I(f) - Q|$ small, and usually an estimate of that error. A method that takes a tolerance tries to return $Q$ with $|I(f) - Q| \le \tau$ (absolute) or $\le \tau |I(f)|$ (relative), but for a black-box $f$ no method can guarantee this (see Bounds).

**Cost.** The cost model is the number of evaluations of $f$. The arithmetic of the method is counted separately. It matters only when the nodes and weights are expensive, for example for high-order Gauss rules, where the [Golub-Welsch algorithm](/golub-welsch-algorithm/) takes $O(n^2)$ operations for the nodes and weights.

**Conditioning.** If each value $f(x)$ has a relative error of at most $\epsilon$, the integral changes by at most $\epsilon\, I(|f|)$. So the relative [condition number](/condition-number/) of the problem is $\kappa = I(|f|)/|I(f)|$. An integrand that changes sign and has a small integral is ill-conditioned, and no rule can then give a small relative error in floating point.

## Variants

- **Fixed budget.** Given $n$, choose the nodes and the weights in advance. This is the setting of [Newton-Cotes formulas](/newton-cotes-formulas/), [Gaussian quadrature](/gaussian-quadrature/) and [Clenshaw-Curtis quadrature](/clenshaw-curtis-quadrature/).
- **Tolerance.** Given $\tau$, add nodes until an error estimate is below $\tau$. This is [adaptive quadrature](/adaptive-quadrature/) and [Romberg integration](/romberg-integration/).
- **Weighted integrals.** A known weight $w$ carries a singularity or the shape of an infinite interval, for example $w(x) = (1 - x)^\alpha (1 + x)^\beta$ for [Gauss-Jacobi quadrature](/gauss-jacobi-quadrature/) or $w(x) = e^{-x^2}$ on $\mathbb{R}$ for [Gauss-Hermite quadrature](/gauss-hermite-quadrature/).
- **Improper integrals.** Infinite intervals or integrands that are unbounded at an end. See [improper integration](/improper-integration/) and [tanh-sinh quadrature](/tanh-sinh-quadrature/).
- **Oscillatory integrals.** $f(x) = g(x) e^{i \omega x}$ with large $\omega$. See [oscillatory integration](/oscillatory-integration/).
- **Periodic integrands.** Over a full period, the plain [trapezoidal rule](/trapezoidal-rule/) converges geometrically for analytic $f$.
- **Many dimensions.** Integrals over $[0, 1]^s$. See [multidimensional integration](/multidimensional-integration/).
- **Tabulated data.** Only the values at fixed points are known, often equally spaced. Then the rule is fixed by the data, and the composite trapezoidal or Simpson rule is the usual choice.

## Examples

The table gives the error $E = I - Q$ of four rules on four integrands. $T_m$, $M_m$ and $S_m$ are the composite trapezoidal, midpoint and Simpson rules with $m = 4$ subintervals (5, 4 and 5 evaluations), and $G_3$ is the 3-point Gauss-Legendre rule.

| integrand, interval | exact value | $E$ for $T_4$ | $E$ for $M_4$ | $E$ for $S_4$ | $E$ for $G_3$ |
|---|---|---|---|---|---|
| $e^x$ on $[0, 1]$ | $e - 1$ | $-8.94 \times 10^{-3}$ | $4.47 \times 10^{-3}$ | $-3.70 \times 10^{-5}$ | $8.24 \times 10^{-7}$ |
| $4/(1 + x^2)$ on $[0, 1]$ | $\pi$ | $1.04 \times 10^{-2}$ | $-5.21 \times 10^{-3}$ | $2.40 \times 10^{-5}$ | $5.25 \times 10^{-4}$ |
| $\sqrt{x}$ on $[0, 1]$ | $2/3$ | $2.34 \times 10^{-2}$ | $-6.31 \times 10^{-3}$ | $1.01 \times 10^{-2}$ | $-2.51 \times 10^{-3}$ |
| $e^{\cos x}$ on $[0, 2\pi]$ | $2\pi I_0(1) \approx 7.954927$ | $-3.44 \times 10^{-2}$ | $3.44 \times 10^{-2}$ | $5.34 \times 10^{-1}$ | $-5.33 \times 10^{-1}$ |

Four lessons are in this table. For the smooth $e^x$, a rule of higher [degree of exactness](/degree-of-precision/) wins by orders of magnitude for the same number of evaluations. For $\sqrt{x}$, whose derivative is infinite at 0, all rules are poor and the higher degree helps little. For the periodic $e^{\cos x}$, the trapezoidal rule is the best of the four: with $m = 8$ its error is $-1.25 \times 10^{-6}$, and with $m = 16$ it is at the level of rounding, $8.9 \times 10^{-16}$. The trapezoidal and midpoint errors have opposite signs and a ratio near $-2$, as their error formulas predict.

## Known algorithms

- [Midpoint rule](/midpoint-rule/), [trapezoidal rule](/trapezoidal-rule/) and [Simpson's rule](/simpsons-rule/): composite rules with error $O(h^2)$, $O(h^2)$ and $O(h^4)$ for $f \in C^2$, $C^2$ and $C^4$.
- [Newton-Cotes formulas](/newton-cotes-formulas/): [interpolatory](/interpolatory-quadrature/) rules on equally spaced nodes. High orders have large weights of both signs and are unstable.
- [Gaussian quadrature](/gaussian-quadrature/): $n$ nodes, degree of exactness $2n - 1$, positive weights, error $O(\rho^{-2n})$ for $f$ analytic in a Bernstein ellipse with parameter $\rho > 1$.
- [Clenshaw-Curtis quadrature](/clenshaw-curtis-quadrature/) and [Fejér quadrature](/fejer-quadrature/): Chebyshev nodes, weights by a [fast cosine transform](/fast-dct/), in practice almost as accurate as Gauss.
- [Romberg integration](/romberg-integration/) and [Richardson extrapolation](/richardson-extrapolation/): cancel the even powers of $h$ in the trapezoidal error.
- [Adaptive quadrature](/adaptive-quadrature/) and [Gauss-Kronrod quadrature](/gauss-kronrod-quadrature/): subdivide where a local error estimate is large.
- [Tanh-sinh quadrature](/tanh-sinh-quadrature/) and [sinc quadrature](/sinc-quadrature/): a change of variable, then the trapezoidal rule. They handle endpoint singularities.
- [Monte Carlo integration](/monte-carlo-integration/) and [quasi-Monte Carlo integration](/quasi-monte-carlo-integration/): for many dimensions.

## Bounds

The bounds of this section are in the information model: an algorithm may choose each node from the values seen so far (adaption is allowed), it pays one unit per value of $f$, and its arithmetic is free. Let $F_r = \{ f \in C^r[0, 1] : |f^{(r)}(x)| \le 1 \text{ for all } x \}$ for an integer $r \ge 1$, and let $e_n$ be the smallest worst-case error over $F_r$ that an algorithm with $n$ values can reach.

**Theorem.** There are constants $0 < c_r \le C_r$ with $c_r\, n^{-r} \le e_n \le C_r\, n^{-r}$ for all $n \ge 1$.

*Upper bound.* Cut $[0, 1]$ into $m$ pieces of width $h = 1/m$. On each piece, interpolate $f$ by a polynomial of degree $r - 1$ at $r$ distinct points of the piece and integrate the polynomial. This uses $n = r m$ values. The [interpolation error theorem](/polynomial-interpolation-error-theorem/) gives $|f(x) - p(x)| = |f^{(r)}(\xi)| \prod_{j} |x - t_j| / r! \le h^r / r!$ on each piece, so the integral error is at most $h^r / r! = r^r / (r!\, n^r)$.

*Lower bound.* Run the algorithm on $f = 0$. It sees only zeros, so its nodes $x_1, \ldots, x_n$ and its output $Q$ are fixed. Cut $[0, 1]$ into $2n$ intervals of width $1/(2n)$. At most $n$ of them contain a node in their interior, so at least $n$ of them, $J_1, \ldots, J_n$, contain none. Let $\psi(t) = (t (1 - t))^{r+1}$ on $[0, 1]$ and $\psi = 0$ outside. Then $\psi \in C^r(\mathbb{R})$, because $\psi$ and its first $r$ derivatives vanish at 0 and 1. Let $K = \max |\psi^{(r)}|$ and let $g$ be the sum over $j$ of $K^{-1} (2n)^{-r} \psi(2n(x - \ell_j))$, where $\ell_j$ is the left end of $J_j$. Each term has $r$-th derivative at most 1 in absolute value, and the terms have disjoint supports, so $g$ and $-g$ are in $F_r$. Both vanish at every node, so the algorithm sees the same zeros and returns the same $Q$ for $g$, $-g$ and $0$. Now $I(g) = n \cdot K^{-1} (2n)^{-r} (2n)^{-1} \int_0^1 \psi = c_r n^{-r}$ with $c_r = \int_0^1 \psi / (2^{r+1} K)$. One of $|I(g) - Q|$ and $|I(-g) - Q|$ is at least $I(g)$. $\square$

The lower bound has a direct consequence: for a black-box $f$, no method can certify $|I(f) - Q| \le \tau$, because a bump between the nodes is invisible. Error estimates of adaptive codes are heuristics that are reliable for well-behaved integrands.

- **Randomized algorithms.** If the algorithm may use random nodes and the error is measured in root mean square, the optimal error on $F_r$ is of order $n^{-r - 1/2}$ (Bakhvalov 1959; see Novak 1988). Plain Monte Carlo, with error $\sigma n^{-1/2}$, reaches this only for $r = 0$.
- **Analytic integrands.** If $f$ is analytic inside a Bernstein ellipse $E_\rho$ around $[-1, 1]$ and bounded there, the $n$-point Gauss rule has error $O(\rho^{-2n})$ (Trefethen, Chapter 19). For a periodic $f$ analytic in a strip of half-width $\alpha$, the $n$-point trapezoidal rule has error $O(e^{-\alpha n})$ (see [trapezoidal rule](/trapezoidal-rule/)).
- **Floating point.** The computed sum $\mathrm{fl}(Q_n)$ adds rounding errors. With recursive summation the extra error is at most about $(n - 1) u \sum_i |w_i f(x_i)|$, where $u = 2^{-53}$ is the unit roundoff in double precision. With [pairwise summation](/pairwise-summation/) the factor $n - 1$ becomes $\lceil \log_2 n \rceil$, and with [Kahan summation](/kahan-summation/) it becomes about 2. Errors $\delta_i$ in the values of $f$ add at most $\sum_i |w_i|\, \delta_i$, so a rule with positive weights summing to $b - a$ is stable and a rule with large weights of both signs is not. The best relative accuracy is about $u \kappa$, where $\kappa$ is the condition number above.

## Reductions

- **To an initial value problem.** $y(x) = \int_a^x f(t)\,dt$ solves $y' = f(x)$, $y(a) = 0$. Applied to this special case, a [Runge-Kutta method](/runge-kutta-methods/) becomes a quadrature rule: the [classical fourth-order method](/classical-runge-kutta-4/) becomes Simpson's rule, and the [explicit midpoint method](/explicit-midpoint-method/) becomes the midpoint rule.
- **From an infinite interval to a finite one.** A change of variable $x = t/(1 - t)$ maps $[0, 1)$ onto $[0, \infty)$ and turns the problem into an integral over a finite interval, often with an endpoint singularity. See [improper integration](/improper-integration/).
- **From an expectation.** The mean $\mathbb{E}[g(X)]$ of a random variable $X$ with density $p$ is $I(g)$ with weight $w = p$. This is the link to [Monte Carlo integration](/monte-carlo-integration/).

## Applications

- Expectations and probabilities in statistics, including normal and Bayesian posterior integrals.
- The entries of the stiffness and mass matrices of the [finite element method](/finite-element-method/), computed element by element with Gauss rules.
- Fourier coefficients and transforms, which are integrals of oscillatory functions.
- Prices of financial options, which are integrals in many dimensions.
- Arc lengths, areas, volumes and moments in geometry and mechanics.

## References
