---
tag: RQAHF0
kind: definition
slug: quadrature-rule
name: Quadrature rule
aliases:
- quadrature formula
- integration rule
- numerical integration formula
area: numerical/quadrature
level: intro
summary: A weighted sum of function values at chosen nodes that approximates an integral.
prereqs: [numerical-integration]
see_also: [degree-of-precision, interpolatory-quadrature, quadrature-error, composite-quadrature, newton-cotes-formulas, gaussian-quadrature, cubature-rule, trapezoidal-rule]
sources:
  - book: isbn:9780122063602
    title: Philip J. Davis and Philip Rabinowitz, Methods of Numerical Integration, second edition, Academic Press, 1984
    locator: Section 2.1, Primitive rules; Section 2.4, Compound rules; Section 2.5, Integration formulas of interpolatory type; Section 2.8, Integration rules using derivative data; Section 4.2, Roundoff error for a fixed integration rule
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 7, Numerical integration I (quadrature rules, their exactness and composite rules)
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Chapter 5, Numerical integration (Sections 5.1 to 5.3)
  - paper: "George Pólya, Über die Konvergenz von Quadraturverfahren, Mathematische Zeitschrift 37 (1933), 264-286"
    locator: the convergence theorem for sequences of quadrature rules on continuous functions
---

A quadrature rule is a fixed formula $Q_n(f) = \sum_{i=1}^n w_i f(x_i)$ that approximates an integral $I(f) = \int_a^b f(x) w(x)\,dx$ by a weighted sum of $n$ values of $f$. The points $x_i$ are the nodes and the numbers $w_i$ are the weights. Every method for [numerical integration](/numerical-integration/) in one dimension, from the [trapezoidal rule](/trapezoidal-rule/) to [Gaussian quadrature](/gaussian-quadrature/), produces a rule of this form, and its quality is measured by its [degree of exactness](/degree-of-precision/) and its [error](/quadrature-error/).

## Definition

Let $[a, b]$ be an interval with $a < b$ and let $w \ge 0$ be a weight function on it with finite moments $\int_a^b x^k w(x)\,dx$ (with $w = 1$ unless stated). Write $I(f) = \int_a^b f(x)\,w(x)\,dx$.

**Definition.** An $n$-point quadrature rule for $I$ is a list of $n \ge 1$ distinct nodes $x_1 < x_2 < \cdots < x_n$ and $n$ real weights $w_1, \ldots, w_n$. It defines the linear functional

$$Q_n(f) = \sum_{i=1}^{n} w_i\, f(x_i)$$

on all functions $f$ that are defined at the nodes. The error is $E_n(f) = I(f) - Q_n(f)$. Here $n$ always counts nodes. In almost all rules the nodes lie in $[a, b]$; we assume this below.

The following terms describe a rule.

- **Degree of exactness.** The rule has degree of exactness $d$ if $E_n(p) = 0$ for every polynomial $p$ of degree at most $d$, and $E_n(x^{d+1}) \ne 0$. By linearity it is enough to check the monomials $1, x, \ldots, x^d$. A rule with $n$ nodes has $d \le 2n - 1$ (for $w$ positive on a set of positive measure), because $E_n(p) = I(p) > 0$ for $p(x) = \prod_i (x - x_i)^2$, which has degree $2n$.
- **Closed and open.** The rule is closed if $x_1 = a$ and $x_n = b$, and open if no node is an endpoint. An open rule never evaluates $f$ at $a$ or $b$, so it applies to integrands that are infinite there.
- **Positive.** The rule is positive if every $w_i > 0$.
- **Symmetric.** For $w$ symmetric about the midpoint $c = (a + b)/2$, the rule is symmetric if the nodes are symmetric about $c$ and mirror nodes have equal weights. A symmetric rule integrates every odd power of $x - c$ exactly, so its degree of exactness is odd.
- **Interpolatory.** The rule is [interpolatory](/interpolatory-quadrature/) if $Q_n(f) = I(p)$, where $p$ is the polynomial of degree at most $n - 1$ that interpolates $f$ at the nodes. This holds if and only if $d \ge n - 1$.
- **Composite.** A [composite rule](/composite-quadrature/) cuts $[a, b]$ into $m$ subintervals of width $h = (b - a)/m$ and applies one basic rule on each.

**Change of interval.** A rule with nodes $t_i$ and weights $v_i$ on $[-1, 1]$ (with $w = 1$) gives a rule on $[a, b]$ by the affine map $x_i = \frac{a + b}{2} + \frac{b - a}{2} t_i$, $w_i = \frac{b - a}{2} v_i$. The map sends polynomials of degree $k$ to polynomials of degree $k$, so the degree of exactness does not change.

**Stability.** If each value $f(x_i)$ has an error of at most $\delta$, the computed $Q_n$ changes by at most $\delta \sum_i |w_i|$. If $d \ge 0$, then $\sum_i w_i = Q_n(1) = I(1)$, so $\sum_i |w_i| \ge I(1)$, with equality exactly when no weight is negative. Positive rules therefore amplify data errors the least. Rounding in the sum itself adds at most about $(n - 1) u \sum_i |w_i f(x_i)|$ with recursive summation, where $u$ is the unit roundoff (Davis and Rabinowitz, Section 4.2).

**Convergence of a family.** A sequence of rules $Q^{(k)}$ converges on $C[a, b]$ if $Q^{(k)}(f) \to I(f)$ for every continuous $f$. Pólya (1933) proved that this holds if and only if (i) $Q^{(k)}(p) \to I(p)$ for every polynomial $p$ and (ii) $\sup_k \sum_i |w_i^{(k)}| < \infty$. The sufficiency of (i) and (ii) has a short proof. Let $B$ be the bound in (ii), let $\varepsilon > 0$, and pick by the [Weierstrass approximation theorem](/weierstrass-approximation-theorem/) a polynomial $p$ with $\|f - p\|_\infty \le \varepsilon$. Then

$$|I(f) - Q^{(k)}(f)| \le |I(f - p)| + |I(p) - Q^{(k)}(p)| + |Q^{(k)}(p - f)| \le \varepsilon I(1) + |I(p) - Q^{(k)}(p)| + B \varepsilon,$$

and the middle term tends to 0 by (i). The necessity of (ii) follows from the uniform boundedness principle. For positive rules, (ii) follows from (i) with $p = 1$, so positive rules whose degree of exactness grows without bound converge for every continuous $f$. Gauss rules are of this kind.

## Examples and non-examples

On $[0, 1]$ with $w = 1$, the exact moments are $I(x^k) = 1/(k + 1)$. The errors on the first monomials, computed in exact rational arithmetic (for Gauss, in floating point), show the degree of exactness of each rule.

| rule | nodes | weights | $E(x^0..x^3)$ | first nonzero error | $d$ |
|---|---|---|---|---|---|
| midpoint | $\tfrac12$ | $1$ | $0, 0, \tfrac1{12}, \ldots$ | $E(x^2) = \tfrac{1}{12}$ | 1 |
| trapezoidal | $0, 1$ | $\tfrac12, \tfrac12$ | $0, 0, -\tfrac16, \ldots$ | $E(x^2) = -\tfrac16$ | 1 |
| Simpson | $0, \tfrac12, 1$ | $\tfrac16, \tfrac46, \tfrac16$ | $0, 0, 0, 0$ | $E(x^4) = -\tfrac{1}{120}$ | 3 |
| 2-point Gauss | $\tfrac12 \mp \tfrac{1}{2\sqrt3}$ | $\tfrac12, \tfrac12$ | $0, 0, 0, 0$ | $E(x^4) = \tfrac{1}{180}$ | 3 |

- **Examples.** The four rules in the table. The 2-point Gauss rule reaches $d = 3 = 2n - 1$, the largest possible degree with 2 nodes. Simpson's rule also has $d = 3$, one more than $n - 1 = 2$, because it is symmetric.
- **Example: a composite rule.** The composite trapezoidal rule with $m$ subintervals is one rule with $n = m + 1$ nodes and weights $h/2, h, \ldots, h, h/2$. Its degree of exactness is still 1.
- **Example: a Monte Carlo estimate.** For fixed sample points $x_1, \ldots, x_N$ in $[a, b]$, the estimate $\frac{b - a}{N} \sum_i f(x_i)$ is a rule with equal weights. Its degree of exactness is 0 in general.
- **Example: negative weights.** The closed [Newton-Cotes formula](/newton-cotes-formulas/) with 9 nodes has weights of both signs. It is a quadrature rule, but not a positive one, and its $\sum_i |w_i|$ exceeds $b - a$.
- **Non-example: derivative data.** The corrected trapezoidal rule $\frac{b - a}{2}(f(a) + f(b)) + \frac{(b - a)^2}{12}(f'(a) - f'(b))$ uses values of $f'$. It is a linear functional but not a quadrature rule in the sense above (Davis and Rabinowitz, Section 2.8, call it a rule using derivative data).
- **Non-example: adaptive output.** An [adaptive quadrature](/adaptive-quadrature/) code returns a weighted sum of values of $f$, but its nodes and weights depend on $f$. So the map from $f$ to the result is not linear, and it is not one fixed rule.
- **Non-example: nodes that are not distinct.** A list such as $x_1 = x_2$ with weights $w_1, w_2$ is the same functional as the 1-point rule with weight $w_1 + w_2$. The definition asks for distinct nodes so that $n$ is the true number of evaluations.

## Related definitions

- [Degree of precision](/degree-of-precision/): the degree of exactness $d$ above, in more detail.
- [Interpolatory quadrature](/interpolatory-quadrature/): rules with $d \ge n - 1$, built by integrating the interpolating polynomial.
- [Quadrature error](/quadrature-error/) and the [Peano kernel theorem](/peano-kernel-theorem/): exact formulas and bounds for $E_n(f)$.
- [Composite quadrature](/composite-quadrature/): one basic rule repeated on $m$ subintervals.
- [Gaussian quadrature](/gaussian-quadrature/): the rules with $d = 2n - 1$.
- [Cubature rule](/cubature-rule/): the same notion for integrals in several dimensions.

## References
