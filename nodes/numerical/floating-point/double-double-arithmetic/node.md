---
tag: M6Q84G
kind: technique
slug: double-double-arithmetic
name: Double-double arithmetic
aliases:
- double-double
- double-word arithmetic
- double-length floating-point arithmetic
area: numerical/floating-point
level: advanced
summary: Represents a number as an unevaluated sum of two doubles, giving about twice the precision.
prereqs: [error-free-transformations, two-sum, fast-two-sum, two-product]
see_also: [shewchuk-expansion-sum, veltkamp-splitting, fused-multiply-add, accurate-dot-product, correctly-rounded-functions, kahan-summation, interval-arithmetic, floating-point-summation]
sources:
  - paper: doi:10.1007/BF01397083
    title: T. J. Dekker, A floating-point technique for extending the available precision, Numerische Mathematik 18 (1971), 224-242
    locator: double-length addition, multiplication, division and square root built from exact sums and products (add2, mul2, div2, sqrt2)
  - paper: doi:10.1145/3121432
    title: Mioara Joldes, Jean-Michel Muller and Valentina Popescu, Tight and rigorous error bounds for basic building blocks of double-word arithmetic, ACM Transactions on Mathematical Software 44(2) (2017)
    locator: the double-word addition, multiplication and division algorithms, their relative error bounds of order u^2, and examples showing that the bounds are nearly attained
  - paper: doi:10.1145/3484514
    title: Jean-Michel Muller and Laurence Rideau, Formalization of double-word arithmetic, and comments on Tight and rigorous error bounds for basic building blocks of double-word arithmetic, ACM Transactions on Mathematical Software 48(1) (2022)
    locator: the formal proofs of the 2017 bounds and the improved bounds (3u^2 for both accurate additions)
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Chapter 14, Extending the Precision (double-word and expansion arithmetic); Section 4.3, Exact addition (Fast2Sum and 2Sum); Section 4.4, Computing the error of a product
  - paper: "Yozo Hida, Xiaoye S. Li and David H. Bailey, Algorithms for quad-double precision floating point arithmetic, Proceedings of the 15th IEEE Symposium on Computer Arithmetic (ARITH 15), 2001, 155-162"
    title: Yozo Hida, Xiaoye S. Li and David H. Bailey, Algorithms for quad-double precision floating point arithmetic (2001)
    locator: the QD library, with double-double and quad-double types, and the sloppy and accurate additions
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, Addison-Wesley, 1998
    locator: Section 4.2.3, Double-Precision Calculations
---

Double-double arithmetic represents a real number as an unevaluated sum $x_h + x_\ell$ of two binary64 floats with $|x_\ell| \le \tfrac12\mathrm{ulp}(x_h)$, which gives about $106$ bits of precision with ordinary hardware. Each operation is built from [error-free transformations](/error-free-transformations/): [TwoSum](/two-sum/) and [TwoProduct](/two-product/) compute the main term and its exact error, a few floating-point operations add the lower-order terms, and [Fast2Sum](/fast-two-sum/) renormalizes the pair. Dekker (1971) introduced it; the QD library (Hida, Li and Bailey, 2001) made it widely available, and Joldes, Muller and Popescu (2017) proved relative error bounds near $3u^2$ for addition and $4u^2$ to $5u^2$ for multiplication. It is the standard way to get extra precision for a few critical steps, such as correctly rounded elementary functions or accurate residuals, without a multiple-precision library.

## In plain words

A double-precision number holds about 16 decimal digits. Sometimes that is not enough, for example to check whether a result is right in its last digit. Double-double arithmetic keeps each number as two doubles: a main part and a small correction that holds the digits that did not fit. Together they hold about 32 digits.

To add or multiply such pairs, the method uses tricks that compute the exact rounding error of an ordinary addition or multiplication. It adds the errors and the small parts together, then tidies the pair so the correction is again small. Each operation costs ten to twenty ordinary operations, far cheaper than general high-precision software.

## When it applies

**Notation.** Binary64 with round to nearest, ties to even, $p = 53$, $u = 2^{-53}$, $\mathrm{fl}(\cdot)$ for the rounded result, $\mathrm{ulp}$ as in Muller et al., Section 2.3.2, and the [standard model](/floating-point-model/); see [floating-point arithmetic](/floating-point-arithmetic/). A *double-word number* is a pair $(x_h, x_\ell)$ of floats with $x_h = \mathrm{fl}(x_h + x_\ell)$; its value is $x_h + x_\ell$.

Use it when

- a computation needs somewhat more than $53$ bits, and $106$ are enough;
- the exponent range of binary64 is enough (a double-word number has the same range, and its low part underflows earlier);
- the machine rounds to nearest in binary64 without extended intermediate precision, and the compiler does not reassociate floating-point expressions;
- an FMA is available, ideally, so that TwoProduct costs two operations instead of seventeen with [Veltkamp splitting](/veltkamp-splitting/).

**Precision.** For a double-word number, $|x_\ell| \le \tfrac12\mathrm{ulp}(x_h) \le u|x_h|$. Every real in the range is within relative distance about $u^2 = 2^{-106}$ of a double-word number, so an operation whose relative error is $c\,u^2$ behaves like an operation of a format with precision about $106$; it is not a format with fixed precision, because $x_\ell$ can be much smaller than $\tfrac12\mathrm{ulp}(x_h)$: $1 + 2^{-200}$ is represented exactly.

## The template

```pseudo id=main
DW-OP(x, y)                        ▷ x = (xh, xl), y = (yh, yl) double-word numbers
L1  (s, e) ← EFT(xh, yh)                ▷ hole: TwoSum for +, TwoProduct for ×
L2  e ← fl(e + LOW(xh, xl, yh, yl))     ▷ hole: the low-order terms; xl + yl, or xh·yl + xl·yh
L3  (zh, zl) ← FAST-TWO-SUM(s, e)       ▷ renormalize: |zl| ≤ ½ ulp(zh)
L4  return (zh, zl)
```

The holes are the error-free transformation of the leading terms, the low-order terms kept, and the number of renormalizations. Line L3 is exact under the hypothesis of Fast2Sum, which holds because $|e|$ is much smaller than $|s|$ except after cancellation, when $s$ is small and the pair is still correct.

## Classic examples

Written in the notation of Joldes, Muller and Popescu (2017); TwoSum, Fast2Sum and TwoProduct are the error-free transformations.

**Accurate addition** (AccurateDWPlusDW):

1. $(s_h, s_\ell) \leftarrow \mathrm{TwoSum}(x_h, y_h)$; $(t_h, t_\ell) \leftarrow \mathrm{TwoSum}(x_\ell, y_\ell)$
2. $c \leftarrow \mathrm{fl}(s_\ell + t_h)$; $(v_h, v_\ell) \leftarrow \mathrm{Fast2Sum}(s_h, c)$
3. $w \leftarrow \mathrm{fl}(t_\ell + v_\ell)$; $(z_h, z_\ell) \leftarrow \mathrm{Fast2Sum}(v_h, w)$

$20$ operations; relative error at most $3u^2$ (Muller and Rideau, 2022, improving the 2017 bound).

**Sloppy addition**: $(s, e) \leftarrow \mathrm{TwoSum}(x_h, y_h)$, $e \leftarrow \mathrm{fl}(e + \mathrm{fl}(x_\ell + y_\ell))$, $(z_h, z_\ell) \leftarrow \mathrm{Fast2Sum}(s, e)$. $11$ operations; accurate when $x$ and $y$ have the same sign, but with no relative error bound when they cancel.

**Multiplication with an FMA** (in the style of DWTimesDW): $(c_h, c_{\ell 1}) \leftarrow \mathrm{TwoProduct}(x_h, y_h)$, $t \leftarrow \mathrm{fl}(x_h y_\ell)$, $c_{\ell 2} \leftarrow \mathrm{fma}(x_\ell, y_h, t)$, $c_{\ell 3} \leftarrow \mathrm{fl}(c_{\ell 1} + c_{\ell 2})$, $(z_h, z_\ell) \leftarrow \mathrm{Fast2Sum}(c_h, c_{\ell 3})$. Eight operations; relative error bounds between $4u^2$ and $5u^2$ for the published variants; the product $x_\ell y_\ell$ is below the error and is dropped.

**Division by a float** (Dekker): $q_h \leftarrow \mathrm{fl}(x_h / y)$, $(p, \pi) \leftarrow \mathrm{TwoProduct}(q_h, y)$, $r \leftarrow \mathrm{fl}(\mathrm{fl}(\mathrm{fl}(x_h - p) - \pi) + x_\ell)$, $q_\ell \leftarrow \mathrm{fl}(r / y)$, $(z_h, z_\ell) \leftarrow \mathrm{Fast2Sum}(q_h, q_\ell)$. This is one Newton correction of the quotient using an exact residual.

**Checked runs.** In Python with binary64 floats, `math.fma` and `fractions.Fraction` as the reference, over $100000$ random pairs of double-word numbers, half of them chosen to cancel to between $40$ and $110$ bits:

- the accurate addition had a largest relative error of $1.97u^2$, within $3u^2$;
- the FMA multiplication had a largest relative error of $3.68u^2$, within the published bounds;
- the sloppy addition had a relative error of $1.1 \times 10^{19}\,u^2 \approx 1.4 \times 10^{-13}$ for $x = (-\texttt{0x1.45445899589ccp+2}, -\texttt{0x1.ff9da156eb005p-52})$ and $y = (\texttt{0x1.45445899589cdp+2}, -\texttt{0x1.fff91af117dcep-52})$: the high parts cancel to $2^{-50}$, $\mathrm{fl}(x_\ell + y_\ell)$ is inexact, and its rounding error, about $5 \times 10^{-32}$, is large next to the true sum $3.5665 \times 10^{-19}$. The accurate addition returned the exact sum, which here is a float.

**Values.** $\mathrm{dd}(1/10) = (0.1, -5.551115123125783 \times 10^{-18})$ and $\mathrm{dd}(1/3) = (0.3333333333333333, 1.850371707708594 \times 10^{-17})$. Summing $\sum_{k=0}^{30} 1/k!$ in double-double, with division by a float and the accurate addition, gives $e$ as $(2.718281828459045, 1.4456468917292502 \times 10^{-16})$ with relative error $7.8 \times 10^{-34} \approx 0.06u^2$; `math.e` has relative error $5.3 \times 10^{-17}$.

## Variations

- **Quad-double and triple-double.** Four (or three) floats give about $212$ (or $159$) bits; the QD library provides quad-double, and CRlibm used triple-double for the last step of [correctly rounded functions](/correctly-rounded-functions/).
- **Floating-point expansions.** [Shewchuk's expansions](/shewchuk-expansion-sum/) and Priest's arithmetic let the number of terms grow as needed, which gives exact results for sums and products of floats, as in robust geometric predicates.
- **Double-word with one float operand.** Operations such as DWPlusFP and DWTimesFP are cheaper and have smaller bounds; compensated algorithms such as [Dot2](/accurate-dot-product/) and compensated Horner use them implicitly.
- **Hardware-specific formats.** The `long double` of IBM PowerPC compilers (IBM extended double) is a double-double type; `__float128` and binary128 replace it on newer systems.
- **Other base formats.** The same construction with binary32 gives float-float arithmetic, used on GPUs without fast binary64.

## Pitfalls

- **Sloppy addition with cancellation.** As in the example, it can lose all but $40$ or so bits; use the accurate addition unless the signs are known to agree.
- **Compiler and hardware settings.** Reassociation (`-ffast-math`), x87 extended registers and [double rounding](/double-rounding/) break the error-free transformations. FMA contraction is usually harmless for the products but can change TwoSum.
- **Range.** Overflow happens at the binary64 limit, and in TwoProduct even slightly before it; the low part underflows for results below about $2^{-969}$, so the precision drops gradually near the bottom of the range.
- **Non-normalized input.** The algorithms assume $|x_\ell| \le \tfrac12\mathrm{ulp}(x_h)$; feeding pairs that overlap (for example $(1, 1)$) voids the bounds.
- **Not a real format.** There is no fixed epsilon, special values are handled only through the high part, and functions such as comparisons, rounding to integer and printing must look at both parts.

## Exercises

1. Prove that if $(x_h, x_\ell)$ is a double-word number then $|x_\ell| \le \tfrac12 \mathrm{ulp}(x_h) \le u|x_h|$.
2. Show that the sloppy addition is exact to within $O(u^2)$ relative error when $x_h, x_\ell, y_h, y_\ell$ are all nonnegative.
3. Implement the accurate addition and the FMA multiplication, and test them against `fractions.Fraction` with cancelling inputs; record the largest error in units of $u^2$.
4. Use double-double arithmetic to compute $\mathrm{fl}(\pi)$ and its error from Machin's formula $\pi = 16\arctan(1/5) - 4\arctan(1/239)$, and compare with a 40-digit value.

## References
