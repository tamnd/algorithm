---
tag: YRCKGK
kind: concept
slug: interpolatory-quadrature
name: Interpolatory quadrature
aliases:
- interpolatory quadrature rules
- interpolatory rule
- quadrature of interpolatory type
area: numerical/quadrature
level: core
summary: A rule obtained by integrating the polynomial that interpolates f at the nodes.
prereqs: [quadrature-rule, degree-of-precision, lagrange-interpolation]
see_also: [newton-cotes-formulas, gaussian-quadrature, clenshaw-curtis-quadrature, fejer-quadrature, gauss-quadrature-theorem, lebesgue-constant, runge-phenomenon, quadrature-error]
sources:
  - book: isbn:9780122063602
    title: Philip J. Davis and Philip Rabinowitz, Methods of Numerical Integration, second edition, Academic Press, 1984
    locator: Section 2.5, Integration formulas of interpolatory type; Section 2.7, Integration rules of Gauss type
  - book: isbn:9781611975932
    title: Lloyd N. Trefethen, Approximation Theory and Approximation Practice, extended edition, SIAM, 2019
    locator: Chapter 19, Clenshaw-Curtis and Gauss quadrature (interpolatory rules, the bound through best approximation, and the comparison of Newton-Cotes, Clenshaw-Curtis and Gauss)
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 7, Numerical integration I (Newton-Cotes formulae as interpolatory rules, and the Runge phenomenon revisited), and Chapter 10, Numerical integration II
  - book: isbn:9780198506720
    title: Walter Gautschi, Orthogonal Polynomials, Computation and Approximation, Oxford University Press, 2004
    locator: Section 1.4, Quadrature rules (interpolatory rules and the theorem of Jacobi on the degree of exactness)
  - paper: "George Pólya, Über die Konvergenz von Quadraturverfahren, Mathematische Zeitschrift 37 (1933), 264-286"
    locator: the divergence of the Newton-Cotes rules for some analytic integrands
---

An interpolatory quadrature rule takes $n$ distinct nodes, interpolates $f$ at them by the polynomial of degree at most $n - 1$, and returns the exact integral of that polynomial. Its weights are the integrals of the [Lagrange basis polynomials](/lagrange-interpolation/), and a [quadrature rule](/quadrature-rule/) with $n$ nodes is interpolatory exactly when its [degree of exactness](/degree-of-precision/) is at least $n - 1$. The [Newton-Cotes formulas](/newton-cotes-formulas/), [Clenshaw-Curtis quadrature](/clenshaw-curtis-quadrature/) and [Gaussian quadrature](/gaussian-quadrature/) are all interpolatory; they differ only in the choice of nodes.

## In plain words

You know the function at a few points and want its area. Draw the unique smooth polynomial curve that passes through all those points, and take the exact area under that curve. That is an interpolatory rule.

The area under the curve is a fixed weighted sum of the known values, so the weights can be computed once and reused for every function. If the function itself is a polynomial of low enough degree, the curve is the function, and the rule is exact. The choice of points matters a lot. Equally spaced points make the curve swing wildly near the ends when there are many of them, and the weights then grow huge with mixed signs. Points that crowd toward the ends, or the special points of Gauss, keep the weights positive and the answers good.

## The idea

Fix an interval $[a, b]$, a weight $w \ge 0$ with finite moments $\mu_k = \int_a^b x^k w(x)\,dx$, and write $I(f) = \int_a^b f(x) w(x)\,dx$. Let $x_1, \ldots, x_n$ be distinct nodes and let

$$\ell_i(x) = \prod_{j \ne i} \frac{x - x_j}{x_i - x_j}, \qquad \omega(x) = \prod_{j=1}^{n} (x - x_j).$$

The interpolant of $f$ of degree at most $n - 1$ is $p(x) = \sum_i f(x_i) \ell_i(x)$, so

$$Q_n(f) = I(p) = \sum_{i=1}^{n} w_i f(x_i), \qquad w_i = I(\ell_i).$$

**Theorem 1 (characterization).** A rule with nodes $x_1, \ldots, x_n$ is interpolatory if and only if it is exact for all polynomials of degree at most $n - 1$.

*Proof.* If the rule is interpolatory and $\deg f \le n - 1$, then the interpolant of $f$ is $f$ itself, so $Q_n(f) = I(f)$. Conversely, if the rule is exact on degree $n - 1$, apply it to $\ell_i$, which has degree $n - 1$ and satisfies $\ell_i(x_j) = [i = j]$: then $w_i = Q_n(\ell_i) = I(\ell_i)$. $\square$

**The moment equations.** Equivalently, the weights solve the Vandermonde system $\sum_{i=1}^n w_i x_i^k = \mu_k$ for $k = 0, \ldots, n - 1$. The [Vandermonde matrix](/vandermonde-matrix/) is nonsingular for distinct nodes, so the weights exist and are unique. Solving it in floating point is ill-conditioned for large $n$; in practice one uses exact formulas (Newton-Cotes), a cosine transform (Clenshaw-Curtis) or an eigenvalue problem ([Golub-Welsch](/golub-welsch-algorithm/)).

**Theorem 2 (error).** If $f \in C^n[a, b]$, then

$$E_n(f) = I(f) - Q_n(f) = \int_a^b f[x_1, \ldots, x_n, x]\, \omega(x)\, w(x)\,dx, \qquad |E_n(f)| \le \frac{\max |f^{(n)}|}{n!} \int_a^b |\omega(x)|\, w(x)\,dx.$$

*Proof.* The Newton form of the [interpolation error](/polynomial-interpolation-error-theorem/) is $f(x) - p(x) = f[x_1, \ldots, x_n, x]\,\omega(x)$. Integrate against $w$. Each divided difference of order $n$ equals $f^{(n)}(\zeta)/n!$ for some $\zeta \in [a, b]$, which gives the bound. $\square$

**Theorem 3 (higher degree, Jacobi).** Let $0 \le k \le n$. An interpolatory rule is exact for all polynomials of degree at most $n - 1 + k$ if and only if $I(q\,\omega) = 0$ for every polynomial $q$ of degree at most $k - 1$.

*Proof.* Let $\deg p \le n - 1 + k$. Divide by $\omega$: $p = q \omega + r$ with $\deg q \le k - 1$ and $\deg r \le n - 1$. Since $\omega(x_i) = 0$, $Q_n(p) = Q_n(r) = I(r)$ by Theorem 1. So $E_n(p) = I(p) - I(r) = I(q \omega)$, and the rule is exact on this degree if and only if $I(q\omega) = 0$ for all such $q$. Every $q$ of degree at most $k - 1$ occurs, with $p = q \omega$. $\square$

With $k = n$, $\omega$ must be orthogonal to all polynomials of degree below $n$, so the nodes are the zeros of the $n$-th [orthogonal polynomial](/orthogonal-polynomials/) for $w$: this is the [Gauss quadrature theorem](/gauss-quadrature-theorem/). The case $k = n + 1$ is impossible, since $q = \omega$ would give $I(\omega^2) = 0$. For a weight symmetric about the midpoint and symmetric nodes, $\omega$ is odd or even about the midpoint. For odd $n$ it is odd, so $I(\omega) = 0$ and the degree rises from $n - 1$ to $n$. This is why Simpson's rule with 3 nodes has degree 3.

**Theorem 4 (best approximation bound).** Let $p^*$ be a best approximation of degree $n - 1$ to $f$ in the maximum norm, with error $\varepsilon_{n-1}(f) = \|f - p^*\|_\infty$. Then

$$|E_n(f)| \le \Big( \mu_0 + \sum_{i=1}^n |w_i| \Big)\, \varepsilon_{n-1}(f).$$

*Proof.* $Q_n(p^*) = I(p^*)$, so $E_n(f) = I(f - p^*) - Q_n(f - p^*)$, and the two terms are at most $\mu_0 \varepsilon_{n-1}$ and $\sum_i |w_i| \varepsilon_{n-1}$. $\square$

So two things decide the quality of an interpolatory rule: how well $f$ can be approximated by polynomials, which depends only on $f$ ([Jackson theorems](/jackson-theorem/), [Chebyshev series](/chebyshev-series/)), and the size of $\sum_i |w_i|$, which depends only on the nodes. If all weights are positive, $\sum_i |w_i| = \mu_0$, the smallest possible value. In general $\sum_i |w_i| = \sum_i |I(\ell_i)| \le \mu_0 \Lambda_n$, where $\Lambda_n$ is the [Lebesgue constant](/lebesgue-constant/) of the nodes.

## Examples

**A rule with a zero weight.** On $[0, 1]$ with nodes $0, \tfrac13, 1$, the moment equations give the weights $w = (0, \tfrac34, \tfrac14)$. The errors on $1, x, x^2$ are 0, and $E(x^3) = -\tfrac{1}{36}$, so $d = 2 = n - 1$. The node 0 gets weight 0. The rule is the 2-point Gauss-Radau rule with nodes $\tfrac13$ and $1$, which already has degree $2 = 2 \cdot 2 - 2$.

**Simpson's rule.** Nodes $0, \tfrac12, 1$ on $[0, 1]$ give $w = (\tfrac16, \tfrac46, \tfrac16)$. Here $\omega(x) = x(x - \tfrac12)(x - 1)$ is odd about $\tfrac12$, so $I(\omega) = 0$ and Theorem 3 with $k = 1$ gives $d = 3$.

**Equally spaced against Chebyshev nodes.** For the Runge function $f(x) = 1/(1 + 25 x^2)$ on $[-1, 1]$, with $I(f) = \tfrac25 \arctan 5 \approx 0.549360$, compare the closed [Newton-Cotes](/newton-cotes-formulas/) rule (equally spaced nodes, weights from exact rational arithmetic) with [Clenshaw-Curtis](/clenshaw-curtis-quadrature/) (nodes $\cos(j\pi/(n - 1))$):

| $n$ | Newton-Cotes error | Newton-Cotes $\sum \lvert w_i \rvert$ | Clenshaw-Curtis error | Clenshaw-Curtis $\sum \lvert w_i \rvert$ |
|---|---|---|---|---|
| 5 | $7.46 \times 10^{-2}$ | 2.000 | $-3.35 \times 10^{-1}$ | 2 |
| 9 | $2.49 \times 10^{-1}$ | 2.902 | $-5.52 \times 10^{-2}$ | 2 |
| 13 | $6.12 \times 10^{-1}$ | 15.06 | $-1.08 \times 10^{-2}$ | 2 |
| 17 | $1.80$ | 116.9 | $-2.20 \times 10^{-3}$ | 2 |
| 21 | $5.92$ | 1088 | $-4.48 \times 10^{-4}$ | 2 |
| 25 | $2.10 \times 10^{1}$ | 11250 | $-9.16 \times 10^{-5}$ | 2 |

Both families are interpolatory and $f$ is analytic on $[-1, 1]$. The Newton-Cotes rules diverge, as Pólya (1933) proved for such integrands: the interpolant shows the [Runge phenomenon](/runge-phenomenon/), and the weights have mixed signs with $\sum |w_i|$ growing exponentially. The Clenshaw-Curtis weights are positive, so $\sum |w_i| = 2$, and Theorem 4 gives geometric convergence at the rate of the Chebyshev approximation of $f$.

## Where it is used

- [Newton-Cotes formulas](/newton-cotes-formulas/): equally spaced nodes, including the [trapezoidal rule](/trapezoidal-rule/), [Simpson's rule](/simpsons-rule/) and the [midpoint rule](/midpoint-rule/).
- [Clenshaw-Curtis quadrature](/clenshaw-curtis-quadrature/) and [Fejér quadrature](/fejer-quadrature/): Chebyshev nodes, positive weights, computed with a [fast cosine transform](/fast-dct/).
- [Gaussian quadrature](/gaussian-quadrature/), [Gauss-Radau](/gauss-radau-quadrature/) and [Gauss-Lobatto](/gauss-lobatto-quadrature/) rules: the nodes make $\omega$ orthogonal to as many polynomials as possible (Theorem 3).
- [Gauss-Kronrod quadrature](/gauss-kronrod-quadrature/): adds nodes to a Gauss rule and keeps the rule interpolatory with a higher degree.
- Product integration for weights $w$ that carry a singularity or an oscillation, such as [Filon quadrature](/filon-quadrature/), where the weights $I(\ell_i)$ are computed for that $w$.
- [Product quadrature](/product-quadrature/) in several dimensions: a tensor product of interpolatory rules is exact on the tensor product of their polynomial spaces.
- The analysis of [quadrature error](/quadrature-error/) and the [Peano kernel theorem](/peano-kernel-theorem/), which use Theorem 2 and the degree of exactness.

## References
