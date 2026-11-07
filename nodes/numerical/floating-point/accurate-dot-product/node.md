---
tag: FVVKHC
kind: problem
slug: accurate-dot-product
name: Accurate dot product
aliases:
- compensated dot product
- accurate inner product
area: numerical/floating-point
level: core
summary: Compute the inner product of two float vectors with error close to that of working in doubled precision.
prereqs: [dot-product, floating-point-model, condition-number, floating-point-summation]
see_also: [dot2-compensated-dot-product, two-product, two-sum, error-free-transformations, kulisch-accumulator, double-double-arithmetic, iterative-refinement, reproducible-summation]
sources:
  - paper: doi:10.1137/030601818
    title: Takeshi Ogita, Siegfried M. Rump and Shin'ichi Oishi, Accurate sum and dot product, SIAM Journal on Scientific Computing 26(6) (2005), 1955-1988
    locator: the condition number of a dot product, the algorithms Dot2 and DotK and their error bounds, and the generator of ill-conditioned dot products used in the experiments
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 3.1, Inner and Outer Products (the bound gamma_n times the sum of the absolute products); Section 27.10, Extended and Mixed Precision BLAS
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Section 5.1.2 (classical error bounds for dot products); Section 5.4, Compensated Dot Products; Section 4.4, Accurate Computation of the Product of Two Numbers
  - paper: "Claude-Pierre Jeannerod and Siegfried M. Rump, Improved error bounds for inner products in floating-point arithmetic, SIAM Journal on Matrix Analysis and Applications 34(2) (2013), 338-344"
    title: Jeannerod and Rump, Improved error bounds for inner products in floating-point arithmetic (2013)
    locator: the bound n u times the sum of the absolute products for round to nearest
---

The accurate dot product problem asks for $s = \sum_{i=1}^{n} x_i y_i$, for two vectors of floating-point numbers, with an error that is as small as if the sum were computed in twice the working precision and then rounded. The plain loop has an error that grows with $n$ and with the cancellation in the sum, and a dot product with cancellation can lose every digit. With [error-free transformations](/error-free-transformations/), the [Dot2 algorithm](/dot2-compensated-dot-product/) of Ogita, Rump and Oishi meets the target in about $25n$ floating-point operations without [FMA](/fused-multiply-add/) and fewer with it. An exact long accumulator gives the correctly rounded result.

## In plain words

A dot product multiplies two lists of numbers entry by entry and adds the products. On a computer each product and each partial sum is rounded. When the products are large and have mixed signs, they cancel, and the rounding errors made on the large products can be as large as the small true answer. The plain loop can then return a result with no correct digit.

An accurate dot product keeps the rounding errors instead of throwing them away. The error of each product and of each addition can be computed exactly with a few extra operations. Those errors are added up on the side and put back at the end. The result is as good as if the computer had worked with twice as many digits.

## Definition

**Notation.** Binary64 with round to nearest, unit roundoff $u = 2^{-53}$, $\gamma_n = nu/(1 - nu)$ and the [standard model](/floating-point-model/); see [floating-point arithmetic](/floating-point-arithmetic/) for the full notation.

**Input.** Vectors $x, y \in \mathbb{F}^n$.

**Output.** A float $\hat s$ that approximates $s = x^{T}y = \sum_i x_i y_i$.

**Condition number.** Following Ogita, Rump and Oishi,

$$\mathrm{cond}(x^{T}y) = \frac{2\sum_i |x_i y_i|}{|x^{T}y|} = \frac{2\,|x|^{T}|y|}{|x^{T}y|},$$

the [condition number](/condition-number/) of $s$ with respect to relative perturbations of the $x_i$ and $y_i$. It is at least $2$, and it is large exactly when the products cancel.

**Goal.** "Accurate" means a result with the error bound of a computation in precision $u^2$ followed by one rounding to the working precision:

$$|\hat s - s| \le u|s| + c_n u^2 \sum_i |x_i y_i|, \qquad\text{that is,}\qquad \frac{|\hat s - s|}{|s|} \le u + \tfrac12 c_n u^2 \,\mathrm{cond}(x^{T}y),$$

with a modest $c_n$ (for Dot2, $c_n u^2 = \gamma_n^2$). The relative error is then of order $u$ while $\mathrm{cond} \lesssim 1/(nu)$, which is about $10^{14}$ for $n = 100$ in binary64, and it degrades smoothly beyond.

## Variants

- **K-fold precision.** The result should have the error of a computation in precision $u^K$ followed by a rounding: $|\hat s - s| \le (u + O(u^2))|s| + O(n u)^K \sum_i|x_i y_i|$. The algorithm DotK of Ogita, Rump and Oishi does this.
- **Faithful rounding.** $\hat s$ is one of the two floats next to $s$ (or $s$ itself if it is a float), whatever the condition number.
- **Correct rounding.** $\hat s = \mathrm{fl}(s)$ in a given rounding mode. This is what an exact accumulator, or [`math.fsum`](/floating-point-summation/) applied to the exact products, gives.
- **Reproducible dot product.** The result must not depend on the order of the terms or the number of processors; see [reproducible summation](/reproducible-summation/).
- **Summation.** With $y_i = 1$ the problem is the accurate [summation](/floating-point-summation/) problem.

## Examples

**A dot product with full cancellation.** Let $x = (1 + 2^{-30},\ 1,\ -2^{-29})$ and $y = (1 + 2^{-30},\ -1,\ 1)$. The exact value is

$$s = (1 + 2^{-30})^2 - 1 - 2^{-29} = 1 + 2^{-29} + 2^{-60} - 1 - 2^{-29} = 2^{-60} \approx 8.67 \times 10^{-19},$$

and $\mathrm{cond} = 2(2 + 2^{-28} + 2^{-60})/2^{-60} \approx 2^{62} \approx 4.6 \times 10^{18}$. The plain loop and Dot2 run as follows ($p$ is the running sum and, for Dot2, $\sigma$ the running sum of the errors).

| step | product, exact | plain loop $p$ | Dot2 $p$ | Dot2 $\sigma$ |
|---|---|---|---|---|
| 1 | $1 + 2^{-29} + 2^{-60}$ | $1 + 2^{-29}$ | $1 + 2^{-29}$ | $2^{-60}$ |
| 2 | $-1$ | $2^{-29}$ | $2^{-29}$ | $2^{-60}$ |
| 3 | $-2^{-29}$ | $0$ | $0$ | $2^{-60}$ |
| result | | $0$ | | $0 + 2^{-60} = 2^{-60}$ |

The plain loop loses $2^{-60}$ when it rounds the first product, and returns $0$: relative error $1$. Dot2 keeps the error $2^{-60}$ of the first product, computed exactly by [TwoProduct](/two-product/), and returns the exact value. `math.sumprod` (Python 3.12 and later) also returns $2^{-60}$ here.

**Ill-conditioned random data.** For $n = 100$, vectors with prescribed cancellation (half of the pairs random, the other half chosen to cancel the running sum) give, in one run with a fixed seed:

| $\mathrm{cond}$ | plain loop, relative error | Dot2, relative error |
|---|---|---|
| $1.3 \times 10^{2}$ | $1.4 \times 10^{-15}$ | $4.8 \times 10^{-17}$ |
| $5.6 \times 10^{7}$ | $2.9 \times 10^{-9}$ | $2.6 \times 10^{-17}$ |
| $2.9 \times 10^{14}$ | $1.3 \times 10^{-2}$ | $4.5 \times 10^{-17}$ |
| $1.7 \times 10^{21}$ | $2.2 \times 10^{4}$ | $4.1 \times 10^{-12}$ |

These are observations, not bounds. The plain loop's error grows like $\mathrm{cond} \cdot u$; Dot2 stays at the level $u \approx 1.1 \times 10^{-16}$ until $\mathrm{cond}$ is near $1/u$ and then grows like $\mathrm{cond} \cdot u^2$, well below its proved bound $u + \tfrac12\gamma_{100}^2\,\mathrm{cond} \approx 10^{-7}$ for the last row.

## Known algorithms

| algorithm | idea | error (proved, round to nearest, no underflow or overflow) | cost |
|---|---|---|---|
| plain loop | $p \leftarrow \mathrm{fl}(p + \mathrm{fl}(x_i y_i))$ | $\gamma_n \sum\lvert x_i y_i\rvert$ | $2n$ flops |
| plain loop with FMA | $p \leftarrow \mathrm{fl}(x_i y_i + p)$ | $\gamma_n \sum\lvert x_i y_i\rvert$ | $n$ FMAs |
| pairwise | sum the products as a balanced tree | $\gamma_{\lceil \log_2 n\rceil + 1} \sum\lvert x_i y_i\rvert$ | $2n$ flops |
| [Dot2](/dot2-compensated-dot-product/) | [TwoProduct](/two-product/) and [TwoSum](/two-sum/) on each term, errors summed on the side | $u\lvert s\rvert + \gamma_n^2 \sum\lvert x_i y_i\rvert$ | $25n - 7$ flops without FMA, about $10n$ with FMA |
| DotK | $K - 1$ passes of error-free summation | $(u + O(u^2))\lvert s\rvert + O(nu)^K \sum\lvert x_i y_i\rvert$ | $O(Kn)$ |
| [double-double](/double-double-arithmetic/) accumulation | accumulate in a pair of floats | about $u\lvert s\rvert + O(nu^2) \sum\lvert x_i y_i\rvert$ | about $20n$ to $30n$ flops |
| TwoProduct, then exact summation | $2n$ exact parts summed by `math.fsum` or a [Shewchuk expansion](/shewchuk-expansion-sum/) | correctly rounded | $O(n)$ typical, more for wide exponent spreads |
| [long accumulator](/kulisch-accumulator/) | a fixed-point register that covers the whole exponent range | correctly rounded | $O(n)$, a wide register |

The first row is the classical bound of Higham, Section 3.1. With round to nearest the bound improves to $nu\sum|x_i y_i|$, without the denominator of $\gamma_n$ (Jeannerod and Rump, 2013). The Dot2 bound is the theorem of Ogita, Rump and Oishi (2005). TwoProduct is exact only when $x_i y_i$ does not underflow, so the bounds of the compensated rows assume that no product is below about $2^{-970}$ in magnitude in binary64; with gradual underflow the extra error is at most a small multiple of $n$ times the smallest subnormal.

## Bounds

- **Lower bound.** Every algorithm must read all $2n$ inputs, so the cost is $\Omega(n)$. A correctly rounded result is possible in $O(n)$ operations, with a long accumulator of about 4300 bits for binary64.
- **The plain loop in practice.** The proved constant grows like $n$; for random data the observed error grows like $\sqrt{n}\,u\sum|x_i y_i|$, an observation that a probabilistic model explains but that is not a bound for a given input.
- **No fixed-precision method is accurate for every condition number.** A bound of the form $u + c\,u^2\,\mathrm{cond}$ is useless once $\mathrm{cond} > 1/u^2$; only faithful or correct rounding methods remove the dependence on $\mathrm{cond}$, and their cost then depends on the data (number of passes, or the width of the accumulator).

## Reductions

- **To summation.** TwoProduct splits each $x_i y_i$ into $h_i + r_i$ exactly, so the dot product is the exact sum of the $2n$ floats $h_1, r_1, \ldots, h_n, r_n$. Any accurate summation algorithm then gives an accurate dot product with the same guarantee, and a correctly rounded sum gives a correctly rounded dot product.
- **From summation.** Summation is the dot product with $y = (1, \ldots, 1)$, so the two problems are equivalent up to the cost of TwoProduct.
- **Matrix products and residuals.** Each entry of a matrix product, and each entry of a residual $b - Ax$, is a dot product; accurate dot products give accurate matrix products and residuals entry by entry.

## Applications

- **Residuals in [iterative refinement](/iterative-refinement/).** The [residual](/residual/) $r = b - A\hat x$ must be computed more accurately than the working precision for refinement to give a solution accurate to working precision; an accurate dot product does this without a wider format (Higham, Chapter 12).
- **Polynomial evaluation.** The compensated [Horner's rule](/horner-rule/) evaluates $\sum a_i x^i$ with the accuracy of doubled precision, by the same idea (Muller et al., Section 5.5).
- **Geometric predicates.** Orientation and in-circle tests are signs of small determinants, which are dot products with heavy cancellation; an accurate or exact dot product gives the correct sign.
- **Extended and mixed precision BLAS.** The XBLAS library computes dot products internally in double-double (Higham, Section 27.10).
- **Verified computation.** Error bounds for linear systems computed with interval or verified methods need residuals with small, rigorously bounded errors.

## References
