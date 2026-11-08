---
tag: M6H41M
kind: algorithm
slug: romberg-integration
name: Romberg integration
aliases:
- Romberg's method
- Romberg quadrature
- Romberg table
area: numerical/quadrature
level: advanced
summary: Apply Richardson extrapolation to trapezoid estimates on successively halved step sizes.
solves: [numerical-integration]
model: real-ram
complexity:
  vars: {K: "the number of halvings (levels)", τ: "the tolerance"}
  time: {worst: Θ(2^K), average: Θ(2^K), best: Θ(2^K)}
  space: {extra: Θ(K^2)}
properties: {deterministic: true, recursive: false}
prereqs: [trapezoidal-rule, richardson-extrapolation, euler-maclaurin-formula]
see_also: [simpsons-rule, newton-cotes-formulas, adaptive-quadrature, gaussian-quadrature, clenshaw-curtis-quadrature, bulirsch-stoer-method, neville-algorithm, quadrature-error]
sources:
  - paper: "Werner Romberg, Vereinfachte numerische Integration, Det Kongelige Norske Videnskabers Selskab Forhandlinger 28, 1955, 30-36"
    locator: the original description of the table
  - paper: "F. L. Bauer, H. Rutishauser and E. Stiefel, New aspects in numerical quadrature, in Experimental Arithmetic, High Speed Computing and Mathematics, Proceedings of Symposia in Applied Mathematics 15, American Mathematical Society, 1963, 199-218"
    locator: the positivity of the weights and the error theory of the Romberg table
  - book: isbn:9780122063602
    title: Philip J. Davis and Philip Rabinowitz, Methods of Numerical Integration, second edition, Academic Press, 1984
    locator: Section 6.3, Romberg integration; Section 2.9, Integration of periodic functions (the Euler-Maclaurin formula); Section 1.15, Extrapolation and speed-up
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Chapter 5, Section 5.4, Asymptotic error formulas and their applications (Richardson extrapolation and Romberg integration)
  - paper: doi:10.1137/130932132
    title: Lloyd N. Trefethen and J. A. C. Weideman, The exponentially convergent trapezoidal rule, SIAM Review 56(3), 2014, 385-458
    locator: Section 2 (the Euler-Maclaurin view and why extrapolation does nothing for periodic integrands)
---

Romberg integration computes the composite [trapezoidal rule](/trapezoidal-rule/) with $1, 2, 4, \ldots, 2^K$ subintervals, reusing every old function value, and then applies [Richardson extrapolation](/richardson-extrapolation/) in powers of $h^2$ to the results. The outcome is a triangular table $R[i, k]$ whose column $k$ has degree of exactness $2k + 1$ and error $O(h_i^{2k+2})$ for smooth $f$; column 1 is [Simpson's rule](/simpsons-rule/) and column 2 is Boole's rule. For analytic integrands the diagonal $R[K, K]$ converges faster than any power of the number $2^K + 1$ of evaluations, and the difference of consecutive diagonal entries gives an error estimate to stop on a tolerance $\tau$.

## In plain words

Start with the crudest trapezoid: one slanted line from one end to the other. Then halve the step: the new estimate needs only the function values at the new middle points, the old ones are kept. Keep halving.

The trapezoid errors shrink by about four each time the step is halved, in a predictable pattern. Richardson's trick uses that pattern: two neighbouring estimates combine into one whose error shrinks by about sixteen per halving. Two of those combine into one shrinking by sixty-four, and so on. The table of all these combinations fills in row by row. When two diagonal entries agree to the tolerance, stop. For smooth functions this reaches full machine accuracy with a few dozen function values.

## The problem

The input is a function $f$, an interval $[a, b]$, a tolerance $\tau \ge 0$, a minimum level $K_0$ and a maximum level $K_{\max}$. With $h_i = (b - a)/2^i$, the output is $R[K, K]$ from the table

$$R[i, 0] = T(h_i), \qquad R[i, k] = R[i, k-1] + \frac{R[i, k-1] - R[i-1, k-1]}{4^k - 1} \quad (1 \le k \le i),$$

where $T(h)$ is the composite trapezoidal rule with step $h$ and $K$ is the first level $i \ge K_0$ with $|R[i, i] - R[i-1, i-1]| \le \tau$, or $K_{\max}$. Also returned is the estimate $|R[K, K] - R[K-1, K-1]|$. The integral is $I(f) = \int_a^b f(x)\,dx$, and the cost is counted in evaluations of $f$.

## The algorithm

```pseudo id=main
ROMBERG(f, a, b, τ, K_max, K_0)
L1  h ← b − a
L2  R[0, 0] ← h · (f(a) + f(b)) / 2
L3  for i ← 1 to K_max do
L4      h ← h / 2
L5      R[i, 0] ← R[i−1, 0] / 2 + h · Σ_{j=1..2^(i−1)} f(a + (2j − 1) h)    ▷ new nodes only
L6      for k ← 1 to i do
L7          R[i, k] ← R[i, k−1] + (R[i, k−1] − R[i−1, k−1]) / (4^k − 1)
L8      if i ≥ K_0 and |R[i, i] − R[i−1, i−1]| ≤ τ then return R[i, i]
L9  return R[K_max, K_max]
```

Line L5 is the halving identity $T(h/2) = \tfrac12 T(h) + \tfrac{h}{2} \sum f(\text{midpoints})$, so each level evaluates $f$ only at the $2^{i-1}$ new points. Line L7 is one Richardson step with $p_k = 2k$. The minimum level $K_0$ in line L8 guards against stopping on agreement that comes from too few samples.

## Example

For $f(x) = e^x$ on $[0, 1]$, with $I = e - 1 = 1.7182818285$, the table is:

| $i$ | $h_i$ | $R[i,0]$ | $R[i,1]$ | $R[i,2]$ | $R[i,3]$ | $R[i,4]$ |
|---|---|---|---|---|---|---|
| 0 | 1 | 1.8591409142 | | | | |
| 1 | 1/2 | 1.7539310925 | 1.7188611519 | | | |
| 2 | 1/4 | 1.7272219046 | 1.7183188419 | 1.7182826879 | | |
| 3 | 1/8 | 1.7205185922 | 1.7182841547 | 1.7182818422 | 1.7182818288 | |
| 4 | 1/16 | 1.7188411286 | 1.7182819741 | 1.7182818287 | 1.7182818285 | 1.7182818285 |

The errors of the diagonal entries are $-1.41 \times 10^{-1}$, $-5.79 \times 10^{-4}$, $-8.59 \times 10^{-7}$, $-3.35 \times 10^{-10}$ and $-3.33 \times 10^{-14}$. With $\tau = 10^{-12}$ the algorithm stops at level $K = 5$ after $2^5 + 1 = 33$ evaluations, with error $2.2 \times 10^{-16}$ and estimate $3.3 \times 10^{-14}$. The trapezoidal rule alone would need about $10^6$ subintervals for that accuracy. Down each column the errors fall by factors near $4$, $16$ and $64$, the orders $h^2$, $h^4$ and $h^6$. For $4/(1 + x^2)$ on $[0, 1]$ the run stops at level 7 with the value of $\pi$ correct to all printed digits.

## Correctness

The full proof is in the correctness file. Main points:

- **Column 0.** Line L5 gives $R[i, 0] = T(h_i)$ exactly, by the halving identity.
- **Combination coefficients.** $R[i, k]$ is a fixed combination $\sum_{l=0}^k \gamma_l T(2^l h_i)$ whose coefficients sum to 1 and annihilate the sequences $h^2, h^4, \ldots, h^{2k}$, but not $h^{2k+2}$.
- **Order (proved).** By the [Euler-Maclaurin formula](/euler-maclaurin-formula/), $T(h) = I + \sum_{j=1}^k c_j h^{2j} + O(h^{2k+2})$ for $f \in C^{2k+2}[a, b]$. Hence $R[i, k] - I = O(h_i^{2k+2})$, with an explicit constant times $\max|f^{(2k+2)}|$.
- **Degree of exactness (proved).** $R[i, k]$ is exact for polynomials of degree at most $2k + 1$ and not for $x^{2k+2}$, so $R[K, K]$ has degree $2K + 1$ with $2^K + 1$ nodes.
- **Positivity (cited).** All weights of every $R[i, k]$ are positive (Bauer, Rutishauser and Stiefel 1963), so the table is stable and each column converges for every Riemann integrable $f$.
- **The estimate.** $|R[K, K] - R[K-1, K-1]|$ is an asymptotic estimate of the error of $R[K-1, K-1]$ and so, for smooth $f$, an overestimate of the error of $R[K, K]$. It is not a bound.

## Complexity

- **Evaluations.** $2^K + 1$ when the run stops at level $K$, exactly the nodes of $T(h_K)$; nothing is evaluated twice.
- **Arithmetic and memory.** $O(2^K)$ operations for the sums and $O(K^2)$ for the table. Keeping only two rows reduces memory to $O(K)$; the implementation keeps the whole table for inspection.
- **Work for a tolerance.** For $f$ analytic on a neighbourhood of $[a, b]$ the diagonal converges superalgebraically in the number of nodes, and a few levels beyond the first agreement suffice. For $f \in C^r$ with $r$ fixed, the columns beyond $k \approx r/2$ do not help, and the rate is that of column $\lfloor (r - 2)/2 \rfloor$.
- **Floating point.** The weights are positive and sum to $b - a$, so rounding errors in the values of $f$ are not amplified, and the sums in line L5 can use `math.fsum`. The table differences in line L7 subtract nearly equal numbers late in the table; this costs a few units of roundoff, which is why $\tau$ should not be set below about $10^{-14}$ times the integral.

## Properties

- **Nested.** Every level reuses all earlier values. Romberg is the classical example of a nested high-order rule.
- **Not Gauss-optimal.** $R[K, K]$ has degree $2K + 1$ with $2^K + 1$ nodes, while a Gauss rule reaches degree $2^{K+1} + 1$ with the same number. Romberg's advantages are nesting and the free error estimate, not efficiency per node.
- **Columns 1 and 2 are Newton-Cotes rules.** $R[i, 1]$ is the composite Simpson rule on $2^i$ subintervals, and $R[i, 2]$ the composite Boole rule. Columns 3 and higher are not Newton-Cotes rules; unlike the Newton-Cotes rules with 9 or more points, their weights stay positive.
- **Global, not adaptive.** All levels refine the whole interval uniformly.

## Variants and improvements

- **Other step sequences.** Bulirsch's sequence $h, h/2, h/3, h/4, h/6, h/8, \ldots$ needs fewer evaluations per level, at the price of losing the simple halving identity; the extrapolation is then done with [Neville's algorithm](/neville-algorithm/) in $h^2$.
- **Rational extrapolation.** Replacing polynomial by rational extrapolation in $h^2$, as in the [Bulirsch-Stoer method](/bulirsch-stoer-method/), helps when $f$ has a nearby complex singularity.
- **Extrapolating the midpoint rule.** The midpoint rule has the same kind of expansion. Combined with the trapezoidal rule by $T(h/2) = \tfrac12(T(h) + M(h))$ it gives the same table.
- **Adaptive Romberg.** Apply a few Romberg levels on each subinterval of an [adaptive quadrature](/adaptive-quadrature/) scheme, which handles local difficulties.
- **Singular integrands.** With an algebraic endpoint singularity $x^\beta$, the trapezoidal expansion has extra terms in $h^{1+\beta+j}$; extrapolating with those exponents (generalized Romberg) restores fast convergence.

## When to use it

Romberg integration suits smooth, nonperiodic integrands on a finite interval when a nested rule with a built-in error estimate is wanted and $f$ is cheap enough that $2^K + 1$ evaluations are acceptable, or when the trapezoidal values are already available, for example from a simulation at halved step sizes. For the same accuracy per evaluation, [Gauss-Legendre quadrature](/gauss-legendre-quadrature/) or [Clenshaw-Curtis quadrature](/clenshaw-curtis-quadrature/) are better, and [adaptive quadrature](/adaptive-quadrature/) is better for integrands with local features.

## Pitfalls

- **Periodic integrands.** For $e^{\cos x}$ on $[0, 2\pi]$, $R[4, 0] = T(2\pi/16)$ is correct to $10^{-15}$, but $R[4, 4]$ has error $2.8 \times 10^{-4}$, because the extrapolation mixes in the poor coarse rows. For a smooth periodic function over a period, use the trapezoidal rule alone; the Euler-Maclaurin coefficients all vanish and there is nothing to extrapolate.
- **Endpoint singularities.** For $\sqrt{x}$ on $[0, 1]$ the expansion contains $h^{3/2}$, and at $K = 10$ the errors are $6.3 \times 10^{-6}$ for $R[10, 0]$ and $2.1 \times 10^{-6}$ for $R[10, 10]$: a factor of 3 for 1025 evaluations. Use a change of variable such as [tanh-sinh quadrature](/tanh-sinh-quadrature/) or a Gauss-Jacobi rule instead.
- **Kinks and jumps.** A kink inside the interval reduces every column to order $h^2$ with irregular errors. For $|x - 1/\sqrt{2}|$ the diagonal is no better than column 0. (A kink at $1/3$ is a curiosity: its trapezoidal errors are exactly $\tfrac29 \cdot 4^{-i}$, because $1/3$ has a periodic binary expansion, and column 1 is exact.)
- **Early stopping.** $\sin^2(2\pi x)$ vanishes at $0$, $\tfrac12$ and $1$, so $R[0, 0] = R[1, 1] = 0$ although the integral is $\tfrac12$. Require a few levels before testing, as $K_0$ does.
- **Too small a tolerance.** Asking for $\tau$ below the rounding level makes the loop run to $K_{\max}$ and spend $2^{K_{\max}}$ evaluations without gaining accuracy.

## Implementations

## History

Werner Romberg published the method in 1955 in the proceedings of the Royal Norwegian Society of Sciences, as a simplification of extrapolation methods for the trapezoidal rule. The idea of extrapolating in $h^2$ goes back to Richardson (1911, 1927), and Huygens used a similar combination for $\pi$ in 1654. Bauer, Rutishauser and Stiefel (1963) gave the error theory and proved that the weights stay positive. Romberg integration was the standard automatic integrator of the 1960s, before adaptive Gauss-Kronrod codes such as QUADPACK replaced it.

## References
