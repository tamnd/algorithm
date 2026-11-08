---
tag: W6G1K4
kind: algorithm
slug: sparse-grid-quadrature
name: Sparse grid quadrature
aliases:
- Smolyak quadrature
- Smolyak construction
- Smolyak cubature
- sparse grid cubature
area: numerical/quadrature
level: research
summary: Combines tensor-product rules in the Smolyak manner to reduce the cost growth with dimension.
solves: [numerical-integration]
model: real-ram
complexity:
  vars: {s: "the dimension", l: "the level above the minimum, l = q - s", N: "the number of distinct points, at most 2^(l+1) (l + s)^(s-1)"}
  time: {worst: "O(s 1.5^s 2^l (l + s)^(s-1))", average: "O(s 1.5^s 2^l (l + s)^(s-1))", best: "O(s 1.5^s 2^l (l + s)^(s-1))"}
  space: {extra: Θ(s N)}
properties: {deterministic: true, recursive: false}
prereqs: [product-quadrature, clenshaw-curtis-quadrature]
see_also: [smolyak-sparse-grids, multidimensional-integration, curse-of-dimensionality, quasi-monte-carlo-integration, monte-carlo-integration, cubature-rule, degree-of-precision, tensor-product-interpolation]
sources:
  - paper: "Sergey A. Smolyak, Quadrature and interpolation formulas for tensor products of certain classes of functions, Soviet Mathematics Doklady 4, 1963, 240-243"
    locator: the construction of multivariate formulas from differences of one-dimensional ones
  - paper: "Erich Novak and Klaus Ritter, High dimensional integration of smooth functions over cubes, Numerische Mathematik 75, 1996, 79-97"
    locator: Smolyak rules from Clenshaw-Curtis formulas, exactness for total degree 2(q - d) + 1, and the error bound for mixed smoothness
  - paper: "Thomas Gerstner and Michael Griebel, Numerical integration using sparse grids, Numerical Algorithms 18, 1998, 209-232"
    locator: the combination formula, point counts for nested rules, and comparisons with Monte Carlo and quasi-Monte Carlo
  - paper: "Grzegorz W. Wasilkowski and Henryk Woźniakowski, Explicit cost bounds of algorithms for multivariate tensor product problems, Journal of Complexity 11, 1995, 1-56"
    locator: the representation A(q, d) as a sum of tensor products of differences, and cost bounds
  - paper: "Hans-Joachim Bungartz and Michael Griebel, Sparse grids, Acta Numerica 13, 2004, 147-269"
    locator: survey of sparse grid approximation and quadrature, including the dimension adaptive and hierarchical forms
---

Sparse grid quadrature, or Smolyak quadrature, builds a rule for $I(f) = \int_{[0,1]^s} f$ from a nested family $U^1, U^2, \ldots$ of one-dimensional rules. A [product rule](/product-quadrature/) $U^{i}\otimes\cdots\otimes U^{i}$ needs $m_i^s$ points; Smolyak's rule instead combines many small and lopsided product rules,

$$A(q, s) = \sum_{q - s + 1 \le |\mathbf i| \le q} (-1)^{q - |\mathbf i|} \binom{s - 1}{q - |\mathbf i|}\, U^{i_1} \otimes \cdots \otimes U^{i_s},$$

so that high resolution in one variable is paired only with low resolution in the others. With [Clenshaw-Curtis](/clenshaw-curtis-quadrature/) rules of $1, 3, 5, 9, 17, \ldots$ points, $A(q, s)$ uses $O(2^\ell \ell^{s-1})$ points for $\ell = q - s$ instead of $(2^\ell + 1)^s$, is exact for all polynomials of total degree at most $2\ell + 1$, and for functions with bounded mixed derivatives of order $r$ has error $O(N^{-r} (\log N)^{(s-1)(r+1)})$. Smolyak introduced the construction in 1963.

## In plain words

To integrate over a square or a cube, the obvious approach is a grid: take good points in each direction and use all combinations. In many dimensions that explodes, because the count is multiplied by the same factor once per direction.

A sparse grid keeps only the combinations that matter. Fine detail along one direction is combined with coarse detail along the others, never with fine detail along all of them at once, because for smooth functions the joint fine detail contributes very little. The rule is a signed sum of several small grids, some added and some subtracted, arranged so that the overlaps cancel. The number of points then grows only a little faster than in one dimension, and smooth integrands are still integrated very accurately.

## The problem

Given an oracle for $f$ on a box $[a, b] \subset \mathbb{R}^s$, smooth in the sense of bounded mixed derivatives, and a tolerance $\tau$, approximate $I(f) = \int_{[a, b]} f$. The dimension $s$ is moderate, from 2 to a few dozen. Cost is counted in evaluations of $f$; the nodes and weights cost extra work that does not involve $f$ and can be reused. See [multidimensional integration](/multidimensional-integration/).

## The algorithm

```pseudo id=main
SMOLYAK(f, s, q, U)                        ▷ q ≥ s; U^1, U^2, ... nested rules on [0, 1]
L1  W ← empty map from points to weights
L2  for each i ∈ ℕ^s with all i_j ≥ 1 and max(s, q − s + 1) ≤ |i| ≤ q do
L3      κ ← (−1)^(q − |i|) · binom(s − 1, q − |i|)
L4      for each node (x_1, ..., x_s) of U^{i_1} × ... × U^{i_s}, with weights v_1, ..., v_s do
L5          W[x] ← W[x] + κ · v_1 ⋯ v_s
L6  return Σ_{x ∈ W} W[x] · f(x)
```

Line L2 enumerates the multi-indices with an odometer, without recursion. The one-dimensional rules are the midpoint rule for $i = 1$ and Clenshaw-Curtis with $m_i = 2^{i-1} + 1$ points for $i \ge 2$, nested, so that the many component grids share points; line L5 merges equal points by an exact key, the fraction $j / (m_i - 1)$ of the Chebyshev angle, and line L6 evaluates $f$ once per distinct point. On a box $[a, b]$ the points are mapped affinely and the result multiplied by the volume. A second family, equispaced closed Newton-Cotes rules with the same nesting and exact rational weights, lets the tests run in exact arithmetic.

## Example

For $s = 2$ and $q = 3$, the combination formula has three terms: $U^1 \otimes U^2 + U^2 \otimes U^1 - U^1 \otimes U^1$, where $U^1$ is the midpoint rule and $U^2$ is Simpson's rule on $0, \tfrac12, 1$ with weights $\tfrac16, \tfrac23, \tfrac16$. The two lopsided grids are a vertical and a horizontal line of three points through the centre. Adding them and subtracting the centre point once more leaves 5 points:

| point | weight |
|---|---|
| $(\tfrac12, \tfrac12)$ | $\tfrac23 + \tfrac23 - 1 = \tfrac13$ |
| $(\tfrac12, 0)$, $(\tfrac12, 1)$, $(0, \tfrac12)$, $(1, \tfrac12)$ | $\tfrac16$ each |

The rule is exact for every polynomial of total degree at most 3, which the $3 \times 3$ product Simpson rule achieves with 9 points; it misses $x_1^2 x_2^2$ by $\tfrac{1}{144}$. On $\int_0^1\!\int_0^2 \cos(x + y)\,dy\,dx$ the errors for $q = 2, \ldots, 8$, with 1, 5, 13, 29, 65, 145 and 321 points, are $2.7 \times 10^{-2}$, $1.3 \times 10^{-4}$, $3.6 \times 10^{-5}$, $3.4 \times 10^{-7}$, $7.8 \times 10^{-10}$, $3.8 \times 10^{-13}$ and $2.8 \times 10^{-17}$.

In higher dimensions, for $\int_{[0,1]^s} \exp\big(\frac1s\sum_j x_j\big)\,dx$, against the root mean square error $\sigma/\sqrt N$ of [Monte Carlo](/monte-carlo-integration/) with the same $N$:

| $s$ | $\ell$ | points $N$ | sparse grid error | Monte Carlo RMS | $\sum \lvert w \rvert$ |
|---|---|---|---|---|---|
| 5 | 1 | 11 | $4.1 \times 10^{-5}$ | $6.5 \times 10^{-2}$ | 2.33 |
| 5 | 2 | 61 | $4.6 \times 10^{-8}$ | $2.8 \times 10^{-2}$ | 6.56 |
| 5 | 3 | 241 | $6.9 \times 10^{-12}$ | $1.4 \times 10^{-2}$ | 11.9 |
| 5 | 5 | 2433 | $4.0 \times 10^{-15}$ | $4.4 \times 10^{-3}$ | 35.3 |
| 10 | 1 | 21 | $1.2 \times 10^{-5}$ | $3.3 \times 10^{-2}$ | 5.67 |
| 10 | 2 | 221 | $1.2 \times 10^{-8}$ | $1.0 \times 10^{-2}$ | 19.7 |
| 10 | 3 | 1581 | $7.0 \times 10^{-12}$ | $3.8 \times 10^{-3}$ | 60.1 |
| 10 | 4 | 8801 | $1.6 \times 10^{-13}$ | $1.6 \times 10^{-3}$ | 154 |

In five dimensions the product of 3-point Clenshaw-Curtis rules has 243 points and error $4.6 \times 10^{-6}$, against $6.9 \times 10^{-12}$ for the 241-point sparse grid; the 5-point product rule has 3125 points and error $1.1 \times 10^{-10}$.

## Correctness

The full proof is in the correctness file. With $\Delta^i = U^i - U^{i-1}$ and $U^0 = 0$, the Smolyak rule is defined as $A(q, s) = \sum_{|\mathbf i| \le q} \Delta^{i_1} \otimes \cdots \otimes \Delta^{i_s}$; expanding the differences and an alternating binomial identity give the combination formula of lines L2 and L3 (Lemma 2, proved). Merging equal points does not change the value (Lemma 3). Proved there as well:

- **Exactness.** If each $U^i$ is exact for degree $2i - 1$, then $A(q, s)$ is exact for all polynomials of total degree $\le 2(q - s) + 1$. For a monomial the differences $\Delta^i x^k$ vanish above the first exact level, the sum over $|\mathbf i| \le q$ covers a full box of the remaining indices, and it telescopes to the exact product of one-dimensional integrals. The rules used here have $m_i \ge 2i - 1$ symmetric nodes, so they qualify, and $x_1^2 x_2^2$ for $s = 2$, $q = 3$ shows that the bound can be attained.
- **Size.** For nested rules the number of distinct points is $\sum_{|\mathbf i| \le q} \prod_j n_{i_j}$, $n_i$ the new points at level $i$, which is at most $2^{\ell + 1}\binom{\ell + s - 1}{s - 1}$.

The error rate for mixed smoothness is cited (Novak and Ritter 1996; Gerstner and Griebel 1998).

## Complexity

The number of evaluations is the number $N(q, s)$ of distinct points: 1, 5, 13, 29, 65, 145 for $s = 2$; 1, 7, 25, 69, 177, 441 for $s = 3$; 1, 21, 221, 1581, 8801 for $s = 10$, for $\ell = 0, 1, \ldots$. For fixed $s$ this is $O(2^\ell \ell^{s-1})$, against $(2^\ell + 1)^s$ for the product rule of the same one-dimensional resolution; for fixed $\ell$ and growing $s$ it is polynomial in $s$, about $2^\ell s^\ell / \ell!$. Building the weights touches every point of every component grid, at most $(3/2)^s\, 2^{\ell+1}\binom{\ell + s - 1}{s - 1}$ of them with $O(s)$ work each, and the map of weights takes $O(sN)$ memory. For functions with bounded mixed derivatives of order $r$, the error is $O(N^{-r}(\log N)^{(s-1)(r+1)})$ (asymptotic, cited), so the cost for tolerance $\tau$ is about $\tau^{-1/r}$ up to logarithmic factors, compared with $\tau^{-s/r}$ for a product rule and $\sigma^2 \tau^{-2}$ for Monte Carlo.

## Properties

- **Exact for total degree $2\ell + 1$** with $O(2^\ell \ell^{s-1})$ points; product rules reach the same total degree only with about $(\ell + 1)^s$ points.
- **Negative weights.** The coefficients of the combination formula alternate in sign, and $\sum |w|$ grows with $\ell$ and $s$ (35 at $s = 5$, $\ell = 5$; 154 at $s = 10$, $\ell = 4$). The rule is less stable than a positive one, and it can return a negative value for a positive integrand.
- **Nested in the level.** $A(q, s)$ and $A(q + 1, s)$ share all points of the former when the one-dimensional rules are nested, so $|A(q + 1, s)f - A(q, s)f|$ is a cheap error estimate.
- **Anisotropic sensitivity.** All coordinates are treated alike; functions whose variation lies in a few coordinates or in low order interactions benefit most.
- **Deterministic.** No randomness and no statistical error bars, unlike [Monte Carlo](/monte-carlo-integration/) and randomized [quasi-Monte Carlo](/quasi-monte-carlo-integration/).

## Variants and improvements

- **Other one-dimensional families.** Gauss-Patterson (nested, higher degree), Gauss-Legendre (not nested, more points), [Gauss-Hermite](/gauss-hermite-quadrature/) or Genz-Keister rules for Gaussian weights, and slowly growing variants with $m_i$ chosen to raise the degree by 2 per level.
- **Dimension adaptive sparse grids.** Gerstner and Griebel (2003) choose the set of multi-indices greedily from the size of the differences $\Delta^{\mathbf i} f$, which favours the important coordinates and interactions.
- **Anisotropic sparse grids.** Weighted level sums $\sum_j \gamma_j i_j \le q$ for known coordinate importance.
- **Hierarchical form.** Writing $f$ in hierarchical surplus coefficients gives the same quadrature and an interpolant at the same points; see [Smolyak sparse grid interpolation](/smolyak-sparse-grids/).
- **Combination technique.** The same alternating sum, applied to solutions of PDEs on anisotropic full grids, is the combination technique of Griebel, Schneider and Zenger.

## When to use it

- Smooth integrands in moderate dimension, from about 3 to a few dozen, where tensor products are too expensive and Monte Carlo too slow, as in uncertainty quantification with smooth parameter dependence and in some option pricing problems.
- When a deterministic rule with a polynomial exactness guarantee and nested error estimates is wanted.
- Not for integrands with kinks, jumps or features not aligned with the axes, where the mixed smoothness is missing; [quasi-Monte Carlo](/quasi-monte-carlo-integration/) or [Monte Carlo](/monte-carlo-integration/) are more robust there. Not in very high dimension unless the effective dimension is low.

## Pitfalls

- **Kinks along diagonals.** For $\int_{[0,1]^3} \max(x_1 + x_2 + x_3 - \tfrac32, 0)\,dx = 0.203125$, the errors with 7, 25, 69, 177, 441, 1073 and 2561 points are $4.7 \times 10^{-2}$, $4.6 \times 10^{-2}$, $3.7 \times 10^{-2}$, $1.6 \times 10^{-2}$, $1.6 \times 10^{-3}$, $1.3 \times 10^{-2}$ and $3.2 \times 10^{-4}$: slow and not even monotone.
- **Negative results for positive integrands.** With negative weights, a peaked positive integrand can give a negative or wildly wrong value at low levels; use the difference between levels as an error indicator before trusting a result.
- **Cancellation.** The values $W[x] f(x)$ partly cancel, with $\sum |w|$ in the dozens or hundreds, so noise in $f$ is amplified by that factor.
- **Not merging nested points.** Evaluating each component grid separately multiplies the cost by a large factor, and computing the shared nodes by different formulas at different levels makes them differ in the last bit, so that they no longer merge; the implementation computes each node from its reduced key.
- **Confusing the level.** Conventions differ: some texts use $|\mathbf i| \le q$ with $q \ge s$ as here, others the level $\ell = q - s \ge 0$, others start indices at 0.

## Implementations

## History

Sergey Smolyak introduced the construction in 1963 for quadrature and interpolation of tensor product function classes, with error bounds that depend only logarithmically on the dimension through the level. Wasilkowski and Woźniakowski (1995) derived explicit cost bounds, and Novak and Ritter (1996) analysed Smolyak rules built from Clenshaw-Curtis formulas, proving exactness for total degree $2(q - d) + 1$ and the rate for mixed smoothness. Gerstner and Griebel (1998) gave the efficient combination formula, point counts and numerical comparisons with Monte Carlo and quasi-Monte Carlo, and in 2003 the dimension adaptive variant. Zenger's sparse grids for PDEs (1991) and the survey of Bungartz and Griebel (2004) connect the quadrature with sparse grid approximation more broadly.

## References
