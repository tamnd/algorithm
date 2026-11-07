---
tag: MRZTGB
kind: problem
slug: floating-point-product-error
name: Exact floating-point product error
aliases:
- error of a floating-point product
- exact product as two floats
- TwoProduct problem
area: numerical/floating-point
level: advanced
summary: Given floats a and b, find the rounded product and its exact error.
prereqs: [floating-point-model, error-free-transformations, fused-multiply-add]
see_also: [two-product, veltkamp-splitting, double-double-arithmetic, accurate-dot-product, dot2-compensated-dot-product, fast-two-sum, two-sum, floating-point-division]
sources:
  - paper: doi:10.1007/BF01397083
    title: T. J. Dekker, A floating-point technique for extending the available precision, Numerische Mathematik 18 (1971), 224-242
    locator: the exact product of two floats as a sum of two floats, computed with splitting (mul12)
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Section 4.4, Computing the Error of a Product (4.4.1 with an FMA, 4.4.2 Veltkamp splitting and Dekker's product, and the condition on the exponents)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 2.6, Fused Multiply-Add Operation (the error model of the FMA and its use for exact products)
  - paper: doi:10.1137/030601818
    title: Takeshi Ogita, Siegfried M. Rump and Shin'ichi Oishi, Accurate sum and dot product, SIAM Journal on Scientific Computing 26(6) (2005), 1955-1988
    locator: TwoProduct as the building block of the compensated dot product Dot2
  - url: https://doi.org/10.1109/IEEESTD.2019.8766229
    title: IEEE Std 754-2019, IEEE Standard for Floating-Point Arithmetic
    locator: Clause 5.4.1, fusedMultiplyAdd (the operation that makes the error computable in one step)
---

The exact product error problem asks, for floats $a$ and $b$, for the rounded product $\pi = \mathrm{fl}(ab)$ and the float $\rho$ with $ab = \pi + \rho$ exactly. In binary arithmetic with round to nearest, such a $\rho$ exists whenever the product does not underflow too far, because $ab$ has at most $2p$ significant bits. With a [fused multiply-add](/fused-multiply-add/) it costs two operations, $\rho = \mathrm{fma}(a, b, -\pi)$; without one, Dekker's product (1971) computes it with [Veltkamp splitting](/veltkamp-splitting/) in $17$ operations. It is, with the exact sum of [TwoSum](/two-sum/), one of the two basic [error-free transformations](/error-free-transformations/), and the base of [double-double](/double-double-arithmetic/) multiplication and of compensated dot products.

## In plain words

When a computer multiplies two numbers, the exact answer usually has about twice as many digits as it can keep, so it rounds. The rounding throws away the second half of the digits.

This problem asks for that lost half as a second stored number, so that the rounded product plus the lost part equal the exact product with nothing missing. That is always possible, as long as the numbers are not so tiny that the lost part falls below the smallest number the machine can store. Some processors do it in two steps with a special instruction; others need a cleverer method of seventeen steps.

## Definition

**Notation.** A binary floating-point system with precision $p$ and minimal exponent $e_{\min}$ (binary64: $p = 53$, $e_{\min} = -1022$), round to nearest, $u = 2^{-p}$, $\mathrm{fl}(\cdot)$ for the rounded result and $\mathrm{ulp}$ as in Muller et al., Section 2.3.2; see [floating-point arithmetic](/floating-point-arithmetic/). For a nonzero float $x$, $e_x$ is its exponent.

**Input.** Finite floats $a$ and $b$.

**Output.** Floats $\pi$ and $\rho$ with $\pi = \mathrm{fl}(ab)$ and $\pi + \rho = ab$, or a report that no such $\rho$ exists.

**Existence (proved).** If $e_a + e_b \ge e_{\min} + p - 1$ and $ab$ does not overflow, then $\rho = ab - \pi$ is a float, and $|\rho| \le \tfrac12\mathrm{ulp}(\pi) \le u|\pi|$. Write $a = M_a 2^{e_a - p + 1}$ and $b = M_b 2^{e_b - p + 1}$ with integers $|M_a|, |M_b| < 2^{p}$; then $ab$ and $\pi$ are integer multiples of $2^{e_a + e_b - 2p + 2}$, $|ab - \pi| \le 2^{e_a + e_b - p + 1}$, so $\rho$ is a multiple of that unit with at most $p$ significant bits. The full proof is on the [fused multiply-add](/fused-multiply-add/) page. The same argument works for any rounding mode, since a directed rounding still gives $|ab - \pi| < \mathrm{ulp}(\pi)$ and $\rho$ fits in $p$ bits (Muller et al., Section 4.4).

## Variants

- **Without an FMA.** Only additions and multiplications rounded to nearest are available; this is the setting of Dekker's algorithm.
- **The rounded result and its error for an FMA.** For $r = \mathrm{fma}(a, b, c)$, the error $ab + c - r$ need not be a float, but it is a sum of two floats; Boldo and Muller's ErrFma computes them.
- **Products of several factors.** $x_1 x_2 \cdots x_n$ exactly as an expansion of floats, by repeated exact products and sums ([Shewchuk expansions](/shewchuk-expansion-sum/)).
- **Residuals.** For a quotient or a square root, $a - qb$ and $a - s^{2}$ are exact under similar conditions; these are the related problems behind [floating-point division](/floating-point-division/) by Newton iteration.
- **Decimal formats.** In radix 10 the product of two $p$-digit numbers has at most $2p$ digits, and the same statement holds with $\beta = 10$.

## Examples

Each line was computed in Python 3.14 with `math.fma` and checked exactly with `fractions.Fraction`.

| $a$ | $b$ | $\pi = \mathrm{fl}(ab)$ | $\rho$ |
|---|---|---|---|
| $0.1$ | $0.1$ | $0.010000000000000002$ (0x1.47ae147ae147cp-7) | $-8.326672684688674 \times 10^{-19}$ (-0x1.eb851eb851eb8p-61) |
| $1 + 2^{-30}$ | $1 - 2^{-30}$ | $1$ | $-2^{-60}$ |
| $3$ | $\mathrm{fl}(1/3)$ | $1$ | $-2^{-54}$ |
| $10^{300}$ | $10^{-300}$ | $1$ | $7.756385209041318 \times 10^{-17}$ |

In every row Dekker's 17-operation product returned the same pair as the FMA. For $100000$ random pairs with exponents in $[-400, 400]$, Dekker's product was exact every time.

**No solution.** For $a = b = 2^{-520}(1 + 2^{-52})$, $e_a + e_b = -1040 < e_{\min} + p - 1 = -970$. The product is $2^{-1040} + 2^{-1091} + 2^{-1144}$, $\pi$ is the subnormal $2^{-1040}$, and the error $2^{-1091} + 2^{-1144}$ is not a float; the FMA returns $\rho = 0$.

## Known algorithms

- **With an FMA** ([TwoProduct](/two-product/) in the form 2MultFMA): $\pi \leftarrow \mathrm{fl}(ab)$, $\rho \leftarrow \mathrm{fma}(a, b, -\pi)$. Two operations, exact under the existence condition (Muller et al., Section 4.4.1).
- **Dekker's product** (1971): split $a = a_h + a_\ell$ and $b = b_h + b_\ell$ into halves of at most $\lceil p/2 \rceil$ and $\lfloor p/2 \rfloor$ bits with [Veltkamp splitting](/veltkamp-splitting/) ($c = \mathrm{fl}((2^{\lceil p/2\rceil} + 1)a)$, $a_h = \mathrm{fl}(c - \mathrm{fl}(c - a))$, $a_\ell = \mathrm{fl}(a - a_h)$), so that the four partial products are exact, and compute $\rho = \mathrm{fl}(\mathrm{fl}(\mathrm{fl}(\mathrm{fl}(a_h b_h - \pi) + a_h b_\ell) + a_\ell b_h) + a_\ell b_\ell)$. Seventeen operations, exact in binary with round to nearest, no overflow in the splitting and the existence condition (Muller et al., Section 4.4.2).
- **Integer arithmetic.** Multiply the integer significands $M_a M_b$ exactly in $2p$ bits and split the result; used when floating-point operations are slow or rounding cannot be trusted.
- **A wider format.** If a format with at least $2p$ bits of precision is available (binary128 for binary64), $\mathrm{fl}_{128}(ab)$ is exact and $\rho = \mathrm{fl}(\mathrm{fl}_{128}(ab) - \pi)$.

## Bounds

- **Size of the error.** $|\rho| \le \tfrac12\mathrm{ulp}(\pi) \le u|\pi|$ with round to nearest.
- **Cost.** Two floating-point operations with an FMA; seventeen with Dekker's method; both have constant cost, with the FMA version also shorter in latency (two dependent operations).
- **Range of validity.** The FMA version needs only the exponent condition and no overflow. Dekker's splitting multiplies by $2^{27} + 1$ and overflows for $|a|$ above about $2^{996}$: in Python, splitting $1.5 \cdot 2^{1000}$ returns NaN.

## Reductions

- **To Veltkamp splitting.** Without an FMA, the exact product reduces to splitting each operand into two halves whose products are exact.
- **Double-word multiplication reduces to it.** The product of double-word numbers is the exact product of the high parts plus low-order terms ([double-double arithmetic](/double-double-arithmetic/)).
- **Compensated dot products reduce to it and to TwoSum.** [Dot2](/dot2-compensated-dot-product/) applies an exact product to each term and an exact sum to each accumulation.
- **Exact residuals reduce to it.** $a - qb$ for $q = \mathrm{fl}(a/b)$ is $\mathrm{fma}(-q, b, a)$, an exact-product computation in which the leading term cancels.

## Applications

- **Compensated algorithms.** [Accurate dot products](/accurate-dot-product/), compensated Horner evaluation and accurate sums of products (Ogita, Rump and Oishi, 2005).
- **Extended precision.** Double-double and quad-double libraries, and the final steps of [correctly rounded functions](/correctly-rounded-functions/).
- **Division and square root.** Correctly rounded quotients and roots in software by Newton or Goldschmidt iterations and exact residuals.
- **Exact geometric predicates.** Determinants of small integer-like matrices computed exactly with floating-point expansions.
- **Testing.** Exact products give an independent check of a multiplication unit or of a library's rounding.

## References
