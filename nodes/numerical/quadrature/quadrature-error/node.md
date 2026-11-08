---
tag: G4YC1H
kind: concept
slug: quadrature-error
name: Quadrature error
aliases:
- truncation error of quadrature
- quadrature remainder
- error of a quadrature rule
area: numerical/quadrature
level: core
summary: The gap between the exact integral and the quadrature sum, bounded through derivatives of f.
prereqs: [quadrature-rule, degree-of-precision]
see_also: [peano-kernel-theorem, interpolatory-quadrature, richardson-extrapolation, euler-maclaurin-formula, gauss-kronrod-quadrature, adaptive-quadrature, floating-point-summation, monte-carlo-integration]
sources:
  - book: isbn:9780122063602
    title: Philip J. Davis and Philip Rabinowitz, Methods of Numerical Integration, second edition, Academic Press, 1984
    locator: Chapter 4, Error analysis (Section 4.2, Roundoff error for a fixed rule; Section 4.3, Truncation error; Section 4.6, Analytic functions; Section 4.9, Practical error estimation)
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 7, Numerical integration I (error of the Newton-Cotes and composite rules), and Chapter 10, Numerical integration II (Gauss rules and their error)
  - book: isbn:9781611975932
    title: Lloyd N. Trefethen, Approximation Theory and Approximation Practice, extended edition, SIAM, 2019
    locator: Chapter 8 (Chebyshev coefficients of analytic functions) and Chapter 19, Theorem 19.3 (error of Gauss and Clenshaw-Curtis quadrature for analytic integrands)
  - paper: doi:10.1137/1025003
    title: J. N. Lyness, When not to use an automatic quadrature routine, SIAM Review 25(1), 1983, 63-87
    locator: the limits of error estimates computed from samples of f
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 4, Summation (error bounds for recursive, pairwise and compensated summation)
---

The quadrature error of a rule $Q_n$ on an integrand $f$ is $E_n(f) = I(f) - Q_n(f)$, the gap between the exact integral and the weighted sum. It is a linear functional of $f$ that vanishes on polynomials up to the [degree of exactness](/degree-of-precision/) $d$, and every classical error formula comes from that fact: $|E_n(f)|$ is bounded by a constant times a derivative of $f$, by a best approximation error, or, for analytic $f$, by a geometric term. In a computer the error also has a rounding part, and in practice it is estimated from the samples, which no method can do with certainty.

## In plain words

A quadrature rule looks at a function in a few places and guesses the area. The error is how far the guess is from the true area.

If the function is a simple polynomial that the rule handles exactly, the error is zero. For other functions, the error is small when the function is close to such a polynomial, which is the case when it is smooth and the points are close together. That is why error formulas contain a high derivative of the function and a power of the spacing between points. Rounding in the computer adds a second, usually much smaller error. Finally, a program never knows the true area, so it estimates its own error by comparing two guesses. That works for well behaved functions but can be fooled, because the program sees only finitely many values.

## The idea

Throughout, $I(f) = \int_a^b f(x) w(x)\,dx$ with $w = 1$ unless stated, $Q_n(f) = \sum_{i=1}^n w_i f(x_i)$, and $E_n(f) = I(f) - Q_n(f)$. Composite rules use $h = (b - a)/m$ with $m$ subintervals.

**Linearity and exactness.** $E_n(\alpha f + \beta g) = \alpha E_n(f) + \beta E_n(g)$, and $E_n(p) = 0$ for every polynomial of degree at most $d$. So for every such $p$,

$$|E_n(f)| = |E_n(f - p)| \le \Big( \int_a^b w + \sum_i |w_i| \Big) \|f - p\|_\infty.$$

Taking the best $p$ gives the bound by the best approximation error of degree $d$. Three families of error results follow, and they differ in what they assume and what they deliver.

**1. Derivative formulas (proved, exact for every $f$ in the class).** Expand $f$ by Taylor's theorem around a point of each panel. The polynomial part is integrated exactly, and the remainder gives the error. The [Peano kernel theorem](/peano-kernel-theorem/) makes this precise: if $E_n(p) = 0$ for degree $k$ and $f \in C^{k+1}[a, b]$, then

$$E_n(f) = \int_a^b K_k(t)\, f^{(k+1)}(t)\,dt, \qquad K_k(t) = \frac{1}{k!}\, E_n\big( (x - t)_+^k \big),$$

where $E_n$ acts on the variable $x$. If $K_k$ does not change sign, then $E_n(f) = c\, f^{(k+1)}(\xi)$ with $c = E_n(x^{k+1})/(k+1)!$. Standard cases, each for $f \in C^r[a, b]$ with the stated $r$:

| rule | $d$ | $r$ | error $E(f)$, with some $\xi \in [a, b]$ |
|---|---|---|---|
| composite [midpoint](/midpoint-rule/) | 1 | 2 | $\frac{(b - a) h^2}{24} f''(\xi)$ |
| composite [trapezoidal](/trapezoidal-rule/) | 1 | 2 | $-\frac{(b - a) h^2}{12} f''(\xi)$ |
| composite [Simpson](/simpsons-rule/), $m$ even | 3 | 4 | $-\frac{(b - a) h^4}{180} f^{(4)}(\xi)$ |
| composite Boole, $m$ a multiple of 4 | 5 | 6 | $-\frac{2 (b - a) h^6}{945} f^{(6)}(\xi)$ |
| $n$-point [Gauss-Legendre](/gauss-legendre-quadrature/) | $2n - 1$ | $2n$ | $\frac{(b - a)^{2n+1} (n!)^4}{(2n + 1)\, ((2n)!)^3} f^{(2n)}(\xi)$ |

For an [interpolatory rule](/interpolatory-quadrature/) with $n$ nodes, the general bound is $|E_n(f)| \le \frac{\max|f^{(n)}|}{n!} \int_a^b |\omega(x)| w(x)\,dx$ with $\omega(x) = \prod_i (x - x_i)$.

**2. Asymptotic expansions (proved as $h \to 0$, a statement about the leading term).** For the composite trapezoidal rule and $f \in C^{2K+2}[a, b]$, the [Euler-Maclaurin formula](/euler-maclaurin-formula/) gives

$$E(f) = -\sum_{k=1}^{K} \frac{B_{2k}\, h^{2k}}{(2k)!} \big( f^{(2k-1)}(b) - f^{(2k-1)}(a) \big) + O(h^{2K+2}),$$

with Bernoulli numbers $B_{2k}$. The expansion is what [Richardson extrapolation](/richardson-extrapolation/) and [Romberg integration](/romberg-integration/) exploit. It also says when a rule is better than its formula: for a periodic $f$ over a period, all the end terms cancel.

**3. Analytic integrands (proved, geometric rates).** If $f$ is analytic in the Bernstein ellipse $E_\rho$ with foci $\pm 1$ and semi-axis sum $\rho > 1$, and $|f| \le M$ there, its Chebyshev coefficients satisfy $|a_k| \le 2 M \rho^{-k}$ (Trefethen 2019, Theorem 8.1), so truncating the Chebyshev series after degree $d$ leaves at most $2 M \rho^{-d}/(\rho - 1)$. For a rule on $[-1, 1]$ with positive weights, $\int w + \sum |w_i| = 4$, and the bound above gives

$$|E_n(f)| \le \frac{8 M \rho^{-d}}{\rho - 1}.$$

For Gauss with $d = 2n - 1$ this is $O(\rho^{-2n})$; Trefethen's Theorem 19.3 gives the sharper constant $\frac{64}{15} M \rho^{-2n}/(\rho^2 - 1)$. For the periodic trapezoidal rule with $f$ analytic and bounded by $M$ in the strip $|\operatorname{Im} z| < \alpha$, the error is at most $4 \pi M/(e^{\alpha m} - 1)$ (Trefethen and Weideman 2014, Theorem 3.2).

**Low smoothness.** When the hypotheses fail, the rate is set by the singularity, not by $d$. For $\sqrt{x}$ on $[0, 1]$ the trapezoidal errors at $m = 16, 32, 64, 128$ are $3.09 \times 10^{-3}$, $1.11 \times 10^{-3}$, $3.96 \times 10^{-4}$ and $1.41 \times 10^{-4}$, ratios near $2^{3/2} = 2.83$, so the error is $O(h^{3/2})$ and a higher order rule would not do better. For a jump the error is $O(h)$ unless a node falls on the jump.

**Random rules (probabilistic).** For [Monte Carlo integration](/monte-carlo-integration/) with $N$ independent uniform points, $E$ is a random variable with mean 0 and standard deviation $\sigma/\sqrt{N}$, where $\sigma^2$ is the variance of $f$. Statements about it are of the form "with probability at least $1 - \delta$", from the [Chebyshev inequality](/chebyshev-inequality/) or, asymptotically, the [central limit theorem](/central-limit-theorem/).

**Rounding error.** Suppose the computed values satisfy $\hat f_i = f(x_i)(1 + \epsilon_i)$ with $|\epsilon_i| \le \eta$, and weights and products are rounded with unit roundoff $u$. With recursive summation the computed sum satisfies

$$|\mathrm{fl}(Q_n) - Q_n| \le \big( \eta + (n + 1) u \big)(1 + O(\eta + n u)) \sum_{i=1}^n |w_i f(x_i)|$$

(Higham 2002, Chapter 4, with the extra $u$ for the product). With compensated or `math.fsum` summation the term $(n + 1) u$ drops to a small multiple of $u$, independent of $n$. Two consequences: the rounding error is negligible beside the truncation error unless the latter is near $\eta$, and it is amplified by $\sum |w_i f(x_i)| / |I(f)|$, which is large when the weights have mixed signs (high-order [Newton-Cotes](/newton-cotes-formulas/)) or when $f$ changes sign and $I(f)$ is small by cancellation.

**Error estimates from the samples.** A program cannot evaluate a derivative bound, so it estimates $E$ by comparing two rules:

- The difference of two rules of different order, as in [Gauss-Kronrod quadrature](/gauss-kronrod-quadrature/), estimates the error of the lower order rule and is used as a cautious estimate for the higher one.
- The difference of one rule at $h$ and $h/2$, divided by $2^p - 1$ for a rule of order $p$, estimates the error of the finer rule when the asymptotic expansion holds. This is the principle of [adaptive quadrature](/adaptive-quadrature/).

Such estimates are asymptotic: they are right for smooth $f$ and small $h$ and can be wrong otherwise. In fact no estimate can be certain. **Proposition.** Let $A$ be any deterministic method that evaluates $f$ at most $N$ times, each point chosen from the earlier values, and returns a number. For every $f_0$ and every $c$ there is a $C^\infty$ function $f_1$ on which $A$ returns the same result while $I(f_1) - I(f_0) = c$. *Proof.* Run $A$ on $f_0$; it queries some points $y_1, \ldots, y_N$. Let $g$ be a smooth bump supported in an open interval of $(a, b)$ that contains no $y_j$, scaled so that $\int g\,w = c$ (possible if $w > 0$ on that interval). Set $f_1 = f_0 + g$. Then $f_1(y_j) = f_0(y_j)$, so $A$ makes the same queries, receives the same values and returns the same output. $\square$ Lyness (1983) discusses what this means for automatic integrators.

## Examples

**An estimate that works.** For $e^x$ on $[0, 1]$, compare the composite Simpson rules $S_m$ and $S_{2m}$. The estimate $(S_{2m} - S_m)/15$ of $I - S_{2m}$:

| $m$ | true error of $S_{2m}$ | estimate | ratio |
|---|---|---|---|
| 4 | $-2.3262 \times 10^{-6}$ | $-2.3125 \times 10^{-6}$ | 1.0060 |
| 8 | $-1.4559 \times 10^{-7}$ | $-1.4538 \times 10^{-7}$ | 1.0015 |
| 16 | $-9.1027 \times 10^{-9}$ | $-9.0993 \times 10^{-9}$ | 1.0004 |
| 32 | $-5.6897 \times 10^{-10}$ | $-5.6892 \times 10^{-10}$ | 1.0001 |

The ratio tends to 1 at the rate of the next term in the expansion, $O(h^2)$.

**An estimate that is fooled.** Let $g(x) = e^x + \sin^2(8 \pi x)$ on $[0, 1]$. The added term vanishes at every node of $S_4$ and $S_8$, so both rules return the same values as for $e^x$, the estimate is $-1.5 \times 10^{-7}$, and the true error is about $0.5$, since $\int_0^1 \sin^2(8\pi x)\,dx = \tfrac12$. This is the proposition above in a concrete form.

**Rounding.** The 11-point closed Newton-Cotes rule has weights of mixed sign with $\sum |w_i| \approx 3.06 (b - a)$, so it amplifies errors in the values of $f$ about three times more than a rule with positive weights; at 21 points the factor is above 500.

## Where it is used

- Choosing a rule and a step for a tolerance $\tau$: the derivative formulas give a sufficient $m$, as on the pages of the [trapezoidal](/trapezoidal-rule/), [midpoint](/midpoint-rule/) and [Simpson](/simpsons-rule/) rules.
- [Adaptive quadrature](/adaptive-quadrature/) and [Gauss-Kronrod quadrature](/gauss-kronrod-quadrature/): local error estimates decide where to subdivide.
- [Richardson extrapolation](/richardson-extrapolation/) and [Romberg integration](/romberg-integration/): the asymptotic expansion is used to cancel error terms.
- The [Peano kernel theorem](/peano-kernel-theorem/): sharp constants for any linear rule.
- The [Koksma-Hlawka inequality](/koksma-hlawka-inequality/): the deterministic error bound for [quasi-Monte Carlo integration](/quasi-monte-carlo-integration/), in place of derivatives.
- Comparing rules: the [Newton-Cotes](/newton-cotes-formulas/), [Clenshaw-Curtis](/clenshaw-curtis-quadrature/) and [Gauss](/gaussian-quadrature/) families are compared through the best approximation bound and $\sum |w_i|$.

## References
