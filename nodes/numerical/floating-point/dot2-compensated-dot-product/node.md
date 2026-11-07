---
tag: 7CXZPB
kind: algorithm
slug: dot2-compensated-dot-product
name: Dot2 compensated dot product
aliases:
- Ogita-Rump-Oishi dot product
- Dot2
- compensated dot product
area: numerical/floating-point
level: research
summary: Computes the dot product as if in twice the working precision using error-free transformations.
solves: [accurate-dot-product]
model: floating-point-model
complexity:
  vars: {n: the length of the vectors}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, in_place: true}
history:
  year: 2005
  people: [Takeshi Ogita, Siegfried M. Rump, Shin'ichi Oishi]
  note: Ogita, Rump and Oishi's paper Accurate sum and dot product (SIAM Journal on Scientific Computing, 2005) introduced Sum2 and Dot2 with error bounds in terms of the condition number and showed them faster than double-double arithmetic.
prereqs: [accurate-dot-product, two-sum, two-product, error-free-transformations]
see_also: [floating-point-summation, kahan-summation, neumaier-summation, double-double-arithmetic, condition-number, fused-multiply-add, veltkamp-splitting, iterative-refinement]
sources:
  - paper: doi:10.1137/030601818
    title: Takeshi Ogita, Siegfried M. Rump and Shin'ichi Oishi, Accurate sum and dot product, SIAM Journal on Scientific Computing 26(6) (2005), 1955-1988
    locator: Section 4 (Sum2 and its error bound), Section 5 (Algorithm Dot2, its error bound in terms of u and gamma_n squared, and the condition number), Section 6 (GenDot, the generator of ill-conditioned dot products, and the timings against double-double)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 3.1 (Lemma 3.1, the theta and gamma notation) and Lemma 3.3 (rules for gamma); Section 3.1 also for the error of the ordinary inner product; Section 4.3 (compensated summation)
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Section 4.3 (TwoSum and Fast2Sum), Section 4.4 (TwoProduct by Veltkamp and Dekker or by FMA), Chapter 5 (enhanced floating-point sums, dot products and polynomial values, including the compensated dot product)
  - paper: doi:10.1007/BF01397083
    title: T. J. Dekker, A floating-point technique for extending the available precision, Numerische Mathematik 18 (1971), 224-242
    locator: the exact product by splitting (mul12) used by TwoProduct without FMA
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, Addison-Wesley, 1997
    locator: Section 4.2.2, Accuracy of Floating Point Arithmetic (Theorem B, the exact error of a sum, which is TwoSum)
---

Dot2 computes a dot product $x^{T}y = \sum_i x_i y_i$ of floating-point vectors with an error bound $u|x^{T}y| + \gamma_n^{2}\sum_i|x_i y_i|$: as accurate as if the dot product were computed with twice the working precision and then rounded once. It splits every product exactly into $h_i + r_i$ with [TwoProduct](/two-product/), accumulates the $h_i$ with [TwoSum](/two-sum/) so that every rounding error $q_i$ of the running sum is also captured exactly, adds all the small parts $q_i + r_i$ in ordinary floating point, and adds that correction to the main sum at the end. It needs only ordinary operations, no branches and no extra memory, and with an FMA it costs about $10n$ flops, five times a plain dot product; it was introduced by Ogita, Rump and Oishi in 2005.

## In plain words

When a computer multiplies two numbers and adds up the results, each step is rounded, and if the terms cancel, the small rounding errors can be larger than the answer.

Dot2 keeps the errors instead of throwing them away. A known trick returns, for each multiplication, both the rounded product and the exact amount that was rounded off; another does the same for each addition. Dot2 adds the rounded products in the usual way, adds all the rounded-off amounts in a second running total, and adds the two totals at the end. The second total is tiny and its own errors are tinier still, so the final answer is about as good as if the computer had worked with twice as many digits.

## The problem

**Notation.** A floating-point system $\mathbb{F}$ with base $\beta = 2$, precision $p$ and exponent range $[e_{\min}, e_{\max}]$; binary64 by default, with $p = 53$ and unit roundoff $u = 2^{-53}$ for round to nearest; $\mathrm{fl}(\cdot)$ is the rounded result, and the [standard model](/floating-point-model/) $\mathrm{fl}(a \circ b) = (a \circ b)(1 + \delta)$, $|\delta| \le u$, holds without underflow or overflow; $\gamma_n = nu/(1 - nu)$. See [floating-point arithmetic](/floating-point-arithmetic/) for the full notation.

**Input.** Vectors $x, y \in \mathbb{F}^{n}$.

**Output.** A float close to $x^{T}y$. The [condition number](/condition-number/) of the dot product is $\mathrm{cond}(x^{T}y) = 2\sum_i |x_i y_i| / |x^{T}y|$; a plain dot product has relative error up to about $\gamma_n \mathrm{cond}/2$ (Higham, Section 3.1), so it has no correct digit once $\mathrm{cond} > 1/(nu)$. The [accurate dot product](/accurate-dot-product/) problem asks for a smaller error; Dot2 gives the error of a computation in precision $u^{2}$.

## The algorithm

```pseudo id=main
DOT2(x, y)                                    ▷ x, y in F^n, n ≥ 1
L1  (p, s) ← TwoProduct(x_1, y_1)                 ▷ x_1 y_1 = p + s exactly
L2  for i ← 2 to n
L3      (h, r) ← TwoProduct(x_i, y_i)             ▷ x_i y_i = h + r exactly
L4      (p, q) ← TwoSum(p, h)                     ▷ p_old + h = p + q exactly
L5      s ← fl(s + fl(q + r))                     ▷ ordinary floating point
L6  return fl(p + s)
```

TwoSum is Knuth's six-operation algorithm, and TwoProduct is either two operations with an FMA, $h = \mathrm{fl}(ab)$ and $r = \mathrm{fma}(a, b, -h)$ (see [fused multiply-add](/fused-multiply-add/)), or Dekker's 17-operation product with [Veltkamp splitting](/veltkamp-splitting/). The total is $25n - 7$ flops without an FMA and $10n - 8$ with one.

## Example

Computed in Python 3.14 and checked with `fractions.Fraction`.

**A cancellation that the plain product misses.** Let $x = (1 + 2^{-30}, -1)$ and $y = (1 - 2^{-30}, 1)$, so $x^{T}y = -2^{-60}$ exactly. The plain dot product rounds $x_1y_1 = 1 - 2^{-60}$ to 0x1.0000000000000p+0 and returns $0$. Dot2: L1 gives $p = 1$ and $s = -2^{-60} \approx -8.67 \times 10^{-19}$; at $i = 2$, L3 gives $(h, r) = (-1, 0)$, L4 gives $(p, q) = (0, 0)$, L5 leaves $s = -2^{-60}$, and L6 returns $-2^{-60}$, the exact answer.

**Ill-conditioned dot products.** With a generator in the style of Ogita, Rump and Oishi's GenDot ($n = 50$, fixed seeds), the observed relative errors were:

| cond | plain dot product | Dot2 |
|---|---|---|
| $9.8 \times 10^{10}$ | $2.6 \times 10^{-6}$ | $5.8 \times 10^{-17}$ |
| $1.5 \times 10^{18}$ | $12.7$ | $1.3 \times 10^{-15}$ |
| $2.1 \times 10^{24}$ | $4.7 \times 10^{7}$ | $8.0 \times 10^{-9}$ |
| $2.8 \times 10^{31}$ | $4.0 \times 10^{14}$ | $1.4 \times 10^{-2}$ |

Dot2 is correctly rounded or nearly so up to $\mathrm{cond} \approx 10^{16}$, and loses accuracy like $u^{2}\,\mathrm{cond} \approx 1.2 \times 10^{-32}\,\mathrm{cond}$ beyond that, while the plain product loses it like $u\,\mathrm{cond}$. In every test case the error was within the proved bound below.

## Correctness

**Proved** (round to nearest, no underflow in the products, no overflow, $nu < 1$, with or without FMA):
$$|\mathrm{res} - x^{T}y| \le u\,|x^{T}y| + (1 + u)\,\gamma_n^{2} \sum_i |x_i y_i|, \qquad \frac{|\mathrm{res} - x^{T}y|}{|x^{T}y|} \le u + \tfrac12 (1 + u)\gamma_n^{2}\,\mathrm{cond}(x^{T}y).$$
The argument has three steps. The error-free transformations give the exact identity $x^{T}y = p_n + \sum_i (q_i + r_i)$. The parts are small: $\sum_i |q_i + r_i| \le \gamma_n \sum_i|x_i y_i|$, because each $q_i$ is a rounding error of a recursive sum and each $r_i$ a rounding error of a product. Summing them in floating point costs a further factor $\gamma_n$, which gives the term $\gamma_n^{2}$; the last addition adds $u|x^{T}y|$. Ogita, Rump and Oishi (Section 5) state the bound with $\gamma_n^{2}$ in place of $(1 + u)\gamma_n^{2}$. The full proof is in `proofs/correctness.md`.

**Observed.** The errors in the table are far below the bound: the bound has $\gamma_n^{2} \approx n^{2}u^{2}$, but the errors grow like $u^{2}\,\mathrm{cond}$ with a small constant, as for random rounding errors.

## Complexity

One pass over the data with $\Theta(n)$ flops and $\Theta(1)$ extra storage: $10n - 8$ flops with an FMA ($2$ for TwoProduct, $6$ for TwoSum, $2$ for the correction), or $25n - 7$ without. There are no branches, so the loop vectorizes and pipelines well. Ogita, Rump and Oishi report Dot2 faster than the same dot product in double-double arithmetic; in practice the running time is often limited by memory bandwidth, so the extra flops cost less than their count suggests. In CPython the loop is dominated by interpreter overhead (observed).

## Properties

- **Accuracy of doubled precision.** The bound is that of a computation with unit roundoff about $u^{2}$, followed by one rounding.
- **Not correctly rounded.** For $\mathrm{cond} \gtrsim 1/(nu)^{2}$ the result can have no correct digit; Dot2 is not an exact method.
- **Branch-free and portable.** It uses only $+$, $-$, $\times$ (and an optional FMA) in round to nearest; it needs no comparisons, unlike Fast2Sum-based methods.
- **Order matters little.** The bound does not depend on the order of the terms, and the algorithm is not reproducible across orders bit for bit.
- **Underflow and overflow.** Underflow in the products breaks the exactness of TwoProduct, and the bound then needs an additive term; overflow or infinite inputs give NaN in the correction even when the plain dot product would be infinite.

## Variants and improvements

- **Sum2.** The same algorithm for sums: TwoSum on the running sum and an ordinary sum of the errors (Ogita, Rump and Oishi, Section 4); Dot2 is Sum2 applied to the $2n$ parts $h_i, r_i$, rearranged.
- **DotK and SumK.** Repeating the cascade $K - 1$ times gives a result as if computed in $K$-fold precision with an error bound of the form $u|x^{T}y|$ plus a constant times $\gamma^{K}\sum|x_i y_i|$ (Ogita, Rump and Oishi, Sections 4 and 5).
- **[Double-double](/double-double-arithmetic/).** Accumulating the dot product in a double-double variable gives a similar accuracy but needs more flops and branches or renormalization.
- **Faithful and correctly rounded methods.** AccSum and NearSum (Rump, Ogita and Oishi, 2008) return a faithfully or correctly rounded result for any condition number by adapting the number of passes; the [Kulisch accumulator](/kulisch-accumulator/) computes the exact dot product.
- **Compensated Horner.** The same idea applied to [Horner's rule](/horner-rule/) gives a polynomial evaluation as if in twice the precision.

## When to use it

Use Dot2 when a dot product or sum may be ill-conditioned and twice the working precision is enough: residuals in [iterative refinement](/iterative-refinement/), geometric predicates that are nearly degenerate, and accumulation of long sums with cancellation. If the condition number can exceed $10^{30}$ in binary64, or a correctly rounded or reproducible result is required, use an adaptive method, `math.fsum` for sums, or an exact accumulator.

## Pitfalls

- **Compiler reassociation.** Options such as `-ffast-math` let the compiler simplify TwoSum to $q = 0$, which turns Dot2 back into a plain dot product.
- **Contraction.** If the compiler fuses the multiplications of Dekker's TwoProduct into FMAs, the splitting is no longer exact; use the FMA version or disable contraction.
- **Underflow.** For products below about $2^{-970}$ the error term of TwoProduct can be lost; for $x = (2^{-600}, 1)$, $y = (2^{-600}, 0)$, Dot2 returns $0$ while $x^{T}y = 2^{-1200}$, which violates the bound without an underflow term.
- **Infinities and NaN.** $\mathrm{fma}(\infty, 1, -\infty)$ is invalid: the result is NaN in C, and Python's `math.fma` raises `ValueError`. Handle nonfinite inputs separately.
- **Dekker's splitting near overflow.** Veltkamp's splitting overflows for $|a|$ above about $2^{996}$ in binary64, before the product itself would.

## Implementations

## History

Error-free transformations go back to Møller (1965) and Kahan (1965) for sums, and to Dekker (1971) for products; Knuth's TAOCP Volume 2 gave TwoSum. Compensated dot products in various forms were used for decades, but in 2005 Ogita, Rump and Oishi gave Sum2, Dot2 and their $K$-fold versions a unified treatment with error bounds in terms of the condition number and showed that they run faster than double-double arithmetic. The work became the base of later accurate and reproducible summation methods by Rump, Ogita and Oishi and of compensated algorithms for polynomial evaluation by Graillat, Langlois and Louvet.

## References
