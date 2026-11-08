---
tag: 41WKP4
kind: definition
slug: degree-of-precision
name: Degree of precision
aliases:
- degree of exactness
- algebraic degree of precision
- polynomial degree of exactness
- order of precision
area: numerical/quadrature
level: core
summary: The largest d such that a rule integrates every polynomial of degree at most d exactly. An n-node rule can reach d = n - 1 by its weights, and never passes 2n - 1 for a positive weight.
prereqs: [quadrature-rule]
see_also: [quadrature-rule, interpolatory-quadrature, gauss-quadrature-theorem, newton-cotes-formulas, peano-kernel-theorem, composite-quadrature, quadrature-error, cubature-rule]
sources:
  - book: isbn:9780122063602
    title: Philip J. Davis and Philip Rabinowitz, Methods of Numerical Integration, second edition, Academic Press, 1984
    locator: Chapter 1 (rules of interpolatory type and the degree of precision) and Chapter 4, Error analysis (Peano kernels and the convergence of rules)
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Chapter 5, Sections 5.1 to 5.3 (degree of precision of the trapezoidal, Simpson, Newton-Cotes and Gauss rules)
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 7, Numerical integration I (Newton-Cotes formulae and their exactness) and Chapter 10, Numerical integration II (Gauss quadrature and the bound 2n - 1)
  - paper: "George Pólya, Über die Konvergenz von Quadraturverfahren, Mathematische Zeitschrift 37 (1933) 264-286"
    locator: the convergence theorem for sequences of quadrature rules on C[a, b] and the divergence of Newton-Cotes rules
---

The degree of precision of a [quadrature rule](/quadrature-rule/) is the largest integer $d$ such that the rule gives the exact integral of every polynomial of degree at most $d$. It is the main measure of the quality of a rule on smooth functions: a rule with degree $d$ has an error that depends only on $f^{(d+1)}$, through the [Peano kernel theorem](/peano-kernel-theorem/). An $n$-node rule can always reach $d \ge n - 1$ by the choice of its weights ([interpolatory quadrature](/interpolatory-quadrature/)), and it can never pass $d = 2n - 1$ when the weight function is positive, a bound that [Gaussian quadrature](/gauss-quadrature-theorem/) reaches.

## Definition

Let $w \ge 0$ be a weight function on an interval $[a, b]$, finite or infinite, with $\int_a^b w > 0$ and finite moments $\int_a^b |x|^k w(x)\,dx$ for all $k$. Write $I(f) = \int_a^b f(x)\,w(x)\,dx$ ($w = 1$ unless stated). A rule with $n$ nodes is

$$Q_n(f) = \sum_{i=1}^{n} w_i\, f(x_i), \qquad E_n(f) = I(f) - Q_n(f),$$

with real weights $w_i$ and distinct nodes $x_i$. Let $\mathcal{P}_k$ be the set of real polynomials of degree at most $k$. The rule has **degree of precision** $d$ if

$$E_n(p) = 0 \ \text{ for all } p \in \mathcal{P}_d, \qquad \text{and} \qquad E_n(p) \ne 0 \ \text{ for some } p \in \mathcal{P}_{d+1}.$$

If $E_n(1) \ne 0$, the rule is exact for no polynomial except $0$, and we set $d = -1$.

**Test by monomials.** $E_n$ is linear and $\{1, x, \ldots, x^k\}$ is a basis of $\mathcal{P}_k$. So $d$ is the largest $k$ with $E_n(x^j) = 0$ for $j = 0, 1, \ldots, k$, and then $E_n(x^{d+1}) \ne 0$. In exact arithmetic this needs only $d + 2$ checks.

**Invariance under an affine map.** If $x = \alpha + \beta t$ with $\beta \ne 0$ maps $[c, e]$ onto $[a, b]$ and $w = 1$, the mapped rule has nodes $\alpha + \beta t_i$ and weights $|\beta| v_i$. Since $p(\alpha + \beta t)$ has the same degree as $p$, the mapped rule has the same degree of precision. So a rule's degree can be computed once on $[0, 1]$ or $[-1, 1]$.

**The error constant.** If the degree is $d$, the number

$$C = \frac{E_n(x^{d+1})}{(d+1)!}$$

is the error constant of the rule on that interval. When the Peano kernel of order $d + 1$ does not change sign, $E_n(f) = C\, f^{(d+1)}(\xi)$ for some $\xi \in (a, b)$ and each $f \in C^{d+1}[a, b]$.

**The two bounds.** Let $x_1, \ldots, x_n$ be distinct.

- *Lower bound.* There are unique weights with $d \ge n - 1$. The conditions $\sum_i w_i x_i^k = I(x^k)$, $k = 0, \ldots, n - 1$, are a linear system whose matrix is the transposed [Vandermonde matrix](/vandermonde-matrix/) of the nodes, which is nonsingular for distinct nodes. The solution is $w_i = I(\ell_i)$, with $\ell_i$ the Lagrange basis polynomials.
- *Upper bound.* If $w \ge 0$ with $\int w > 0$ on an interval, then $d \le 2n - 1$. Take $p(x) = \prod_{i=1}^n (x - x_i)^2 \in \mathcal{P}_{2n}$. Then $Q_n(p) = 0$, while $I(p) > 0$ because $p > 0$ except at $n$ points. So $E_n(p) \ne 0$.

The [Gauss quadrature theorem](/gauss-quadrature-theorem/) shows that $d = 2n - 1$ is reached, for exactly one choice of nodes.

## Examples and non-examples

On $[0, 1]$ with $w = 1$, the errors $E(x^k)$ in rational arithmetic are:

| rule | nodes | weights | $E(x^0), \ldots, E(x^5)$ | $d$ | $C$ |
|---|---|---|---|---|---|
| midpoint | $\tfrac12$ | $1$ | $0, 0, \tfrac1{12}, \tfrac18, \tfrac{11}{80}, \tfrac{13}{96}$ | 1 | $\tfrac{1}{24}$ |
| trapezoid | $0, 1$ | $\tfrac12, \tfrac12$ | $0, 0, -\tfrac16, -\tfrac14, -\tfrac{3}{10}, -\tfrac13$ | 1 | $-\tfrac1{12}$ |
| Simpson | $0, \tfrac12, 1$ | $\tfrac16, \tfrac23, \tfrac16$ | $0, 0, 0, 0, -\tfrac1{120}, -\tfrac1{48}$ | 3 | $-\tfrac1{2880}$ |
| Simpson's 3/8 | $0, \tfrac13, \tfrac23, 1$ | $\tfrac18, \tfrac38, \tfrac38, \tfrac18$ | $0, 0, 0, 0, -\tfrac1{270}, -\tfrac1{108}$ | 3 | $-\tfrac1{6480}$ |
| interpolatory on $0, \tfrac13, 1$ | $0, \tfrac13, 1$ | $0, \tfrac34, \tfrac14$ | $0, 0, 0, -\tfrac1{36}, -\tfrac{8}{135}, -\tfrac{7}{81}$ | 2 | $-\tfrac1{216}$ |

- **Symmetry gains one degree.** Simpson's rule has 3 nodes, so interpolation gives $d \ge 2$; the nodes and weights are symmetric about $\tfrac12$, so $E((x - \tfrac12)^3) = 0$ too, and $d = 3$. The 4-node 3/8 rule gets no such gain: it has $d = 3 = n - 1$, the same as Simpson with one node more, and only a smaller error constant ($-\tfrac1{6480}$ against $-\tfrac1{2880}$). In general a closed [Newton-Cotes rule](/newton-cotes-formulas/) with $n$ nodes has $d = n$ when $n$ is odd and $d = n - 1$ when $n$ is even.
- **The last row** is the interpolatory rule on $\{0, \tfrac13, 1\}$. Its weight at $0$ is $0$, so it is in fact the 2-node rule on $\tfrac13, 1$ with weights $\tfrac34, \tfrac14$, of degree $2 = 2n - 2$. This is the right-sided [Gauss-Radau rule](/gauss-radau-quadrature/) with $n = 2$.
- **Gauss-type rules.** With $n$ nodes: [Gauss](/gaussian-quadrature/) $2n - 1$, [Gauss-Radau](/gauss-radau-quadrature/) $2n - 2$, [Gauss-Lobatto](/gauss-lobatto-quadrature/) $2n - 3$. A [Gauss-Kronrod](/gauss-kronrod-quadrature/) rule with $2m + 1$ nodes built on the $m$-node Gauss-Legendre rule has $d = 3m + 1$ for even $m$ and $3m + 2$ for odd $m$. [Clenshaw-Curtis](/clenshaw-curtis-quadrature/) with $n$ nodes has $d = n - 1$ for even $n$ and $d = n$ for odd $n$.
- **Composite rules.** The [composite](/composite-quadrature/) Simpson rule on $m \ge 2$ panels still has $d = 3$: it integrates cubics exactly, but not every quartic. Its accuracy comes from the small panels, not from a high degree.
- **Non-example: equal weights at random nodes.** Monte Carlo with $Q(f) = \frac{b-a}{n}\sum f(x_i)$ has $d = 0$ for almost all node sets: it is exact on constants only. Its error is controlled by the variance of $f$, not by derivatives.
- **Non-example: a high degree is not a good rule.** The closed Newton-Cotes rule with 21 equally spaced nodes on $[0, 1]$ has $d = 21$, but some weights are negative and $\sum |w_i| = 544.18$. Rounding errors in the values $f(x_i)$ are amplified by this factor, and Pólya (1933) showed that the Newton-Cotes rules do not converge for every continuous $f$ as $n \to \infty$. For comparison, $\sum|w_i| = 1.45$ for 9 nodes and $3.06$ for 11 nodes.
- **Non-example: degree on the wrong class.** The $m$-point [trapezoidal rule](/trapezoidal-rule/) on a period has algebraic degree 1, but it is exact for all trigonometric polynomials $e^{ikx}$ with $|k| < m$. For periodic $f$, this trigonometric degree is the right measure.

**Convergence and the degree.** Let $Q^{(n)}$ be rules on a finite $[a, b]$ with degrees $d_n \to \infty$. If $\sup_n \sum_i |w_i^{(n)}| = L < \infty$, then $Q^{(n)}(f) \to I(f)$ for every $f \in C[a, b]$. *Proof.* Given $\varepsilon > 0$, the Weierstrass theorem gives a polynomial $p$ with $\max|f - p| \le \varepsilon$. For $n$ with $d_n \ge \deg p$, $E^{(n)}(p) = 0$, so $|E^{(n)}(f)| = |E^{(n)}(f - p)| \le (\int_a^b w + L)\,\varepsilon$. $\square$ Rules with positive weights and $d_n \ge 0$ have $\sum_i |w_i| = \sum_i w_i = I(1)$, so the condition holds for Gauss and Clenshaw-Curtis rules. Pólya proved that the condition is also necessary (Pólya 1933; Davis and Rabinowitz, Chapter 4).

**Floating point.** The definition is exact. When nodes or weights are rounded, $E_n(x^k)$ is of order $u \sum_i |w_i||x_i|^k$ for $k \le d$ instead of $0$, with $u = 2^{-53}$. A numerical test of the degree must therefore compare $|E_n(x^k)|$ with this size, not with $0$, or use rational arithmetic when the nodes are rational, as in the table above.

## Related definitions

- [Quadrature rule](/quadrature-rule/) and [interpolatory quadrature](/interpolatory-quadrature/): the objects to which the degree applies, and the rules that reach $d \ge n - 1$.
- [Quadrature error](/quadrature-error/) and the [Peano kernel theorem](/peano-kernel-theorem/): for $f \in C^{d+1}$ the error of a rule of degree $d$ is $\int K(t) f^{(d+1)}(t)\,dt$.
- [Gauss quadrature theorem](/gauss-quadrature-theorem/): the maximal degree $2n - 1$ and the rules that reach it.
- [Cubature rule](/cubature-rule/): the same notion in several variables, with total degree.
- [Composite quadrature](/composite-quadrature/): a basic rule of degree $d$ gives the rate $h^{d+1}$.

## References
