---
tag: P2DD1D
kind: definition
slug: special-floating-point-values
name: Infinities, NaN and signed zero
aliases:
- NaN
- signed zero
- infinity
- not a number
- negative zero
area: numerical/floating-point
level: intro
summary: The IEEE 754 values that are not finite nonzero numbers. Plus and minus infinity stand for overflow and division by zero, NaN for an invalid result, and the two zeros keep a sign.
prereqs: [ieee-754]
see_also: [floating-point-exceptions, subnormal-numbers, ieee-754, rounding-modes, interval-arithmetic, log-sum-exp-trick, floating-point-arithmetic, ulp]
sources:
  - url: https://doi.org/10.1109/IEEESTD.2019.8766229
    title: IEEE Std 754-2019, IEEE Standard for Floating-Point Arithmetic
    locator: Clause 3.4 (encodings of infinities and NaNs); Clause 5.10 (totalOrder); Clause 5.11 (comparison predicates and the unordered relation); Clause 6.1 (infinity arithmetic), 6.2 (operations with NaNs, 6.2.1 quiet and signaling NaN encodings), 6.3 (the sign bit); Clause 7.2 and 7.3 (invalid operation, division by zero); Clause 9.2.1 (special values of the recommended functions); Clause 9.6 (minimum and maximum operations)
  - paper: doi:10.1145/103162.103163
    title: David Goldberg, What every computer scientist should know about floating-point arithmetic, ACM Computing Surveys 23(1) (1991), 5-48
    locator: Section 2.2, Special Quantities (NaNs, infinity, signed zero, denormalized numbers)
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Chapter 3, the parts of Section 3.1 on infinities, NaNs and signed zeros in IEEE 754-2008, and on comparisons
  - paper: "W. Kahan, Branch cuts for complex elementary functions, or much ado about nothing's sign bit, in A. Iserles and M. J. D. Powell (eds.), The State of the Art in Numerical Analysis, Clarendon Press, Oxford, 1987, 165-211"
    title: W. Kahan, Branch cuts for complex elementary functions, or much ado about nothing's sign bit
    locator: the use of the sign of zero to choose the side of a branch cut
---

The [IEEE 754](/ieee-754/) formats hold, besides the finite nonzero numbers, the special values $+\infty$, $-\infty$, NaN ("not a number") and two zeros, $+0$ and $-0$. An infinity is the result of an overflow or of a division of a nonzero number by zero, a NaN is the result of an invalid operation such as $0/0$, and the sign of a zero records the side from which a result went to zero. With these values each operation has a defined result, so a program can go on after an [exception](/floating-point-exceptions/) and test the result later.

## Definition

**Notation.** A floating-point system $\mathbb{F}$ has base $\beta$, precision $p$ and exponent range $[e_{\min}, e_{\max}]$; the default is binary64 ($\beta = 2$, $p = 53$, $e_{\min} = -1022$, $e_{\max} = 1023$), with 11 exponent bits and 52 trailing significand bits. $\mathrm{fl}(\cdot)$ is the rounded result, and $\Omega$ is the largest finite float.

**Encodings (Clauses 3.4 and 6.2.1).** In a binary format, the exponent field with all bits 1 marks a special value:

| value | sign $S$ | exponent field $E$ | trailing significand $T$ | binary64 word |
|---|---|---|---|---|
| $+0$ | 0 | 0 | 0 | `0x0000000000000000` |
| $-0$ | 1 | 0 | 0 | `0x8000000000000000` |
| $+\infty$ | 0 | all 1 | 0 | `0x7FF0000000000000` |
| $-\infty$ | 1 | all 1 | 0 | `0xFFF0000000000000` |
| quiet NaN | any | all 1 | first bit 1 | for example `0x7FF8000000000000` |
| signaling NaN | any | all 1 | first bit 0, rest not all 0 | for example `0x7FF4000000000001` |

The other bits of $T$ in a NaN are its *payload*. The standard recommends that an operation with a NaN input return a NaN with the payload of one of the inputs.

**Infinity arithmetic (Clause 6.1).** The infinities follow the limits of real arithmetic: for finite $x$, $\infty + x = \infty$, $\infty \times x = \pm\infty$ for $x \neq 0$, $x / \infty = \pm 0$, and $\sqrt{+\infty} = +\infty$. These operations are exact and signal no exception. An infinity arises from an operation on finite operands in two ways only:

- *overflow* (Clause 7.4): the result, rounded as if the exponent range had no upper limit, exceeds $\Omega$; in round to nearest the default result is $\pm\infty$, for example for $\Omega \times 2$;
- *division by zero* (Clause 7.3): $x / 0$ for a finite nonzero $x$, with result $\pm\infty$; also $\log(0) = -\infty$ in the recommended functions.

**Invalid operations (Clause 7.2).** These give a quiet NaN by default: $\infty - \infty$, $0 \times \infty$, $0/0$, $\infty/\infty$, $\sqrt{x}$ for $x < 0$, $\mathrm{fma}(0, \infty, c)$, $\mathrm{remainder}(x, 0)$ and $\mathrm{remainder}(\infty, y)$, a conversion of a NaN or an infinity to an integer format, and an arithmetic operation on a signaling NaN (copying, negation, absolute value and copySign do not signal).

**Comparisons (Clause 5.11).** Four relations are possible between two values: less, equal, greater and *unordered*. A NaN is unordered with each value, itself included. So $x = x$ is false and $x \neq x$ is true when $x$ is a NaN, and $x < y$, $x > y$, $x \le y$ and $x \ge y$ are all false when either one is a NaN. The two zeros are equal: $+0 = -0$ is true.

**The sign of zero (Clause 6.3).** A product or quotient has the exclusive OR of the signs of the operands, also when it is zero: $(-1) \times 0 = -0$. A sum of two zeros of opposite sign, and a sum $x + (-x)$ with $x$ finite, is $+0$ in each rounding mode except roundTowardNegative, where it is $-0$. $\sqrt{-0} = -0$. The sign of zero is visible through division, $1/(+0) = +\infty$ and $1/(-0) = -\infty$, and through functions with a branch cut such as $\operatorname{atan2}$ and the complex logarithm.

**Facts that follow.** If a computation on finite operands returns a NaN, an invalid operation occurred in it. A NaN does not disappear in the arithmetic operations: each one with a NaN operand returns a NaN. Some recommended functions do return a number for a NaN operand where the result is the same for each value of it: $\mathrm{pow}(x, 0) = 1$ and $\mathrm{hypot}(\pm\infty, \text{NaN}) = +\infty$ (Clause 9.2.1).

## Examples and non-examples

The examples run in Python 3, whose `float` is binary64.

**NaN.** `nan = float("nan")`; then `nan == nan` is `False`, `nan != nan` is `True`, and `nan < 1.0` and `nan > 1.0` are both `False`. `math.inf - math.inf`, `0 * math.inf` and `math.inf / math.inf` all give `nan`. On an ARM processor the NaN that the hardware makes is `0x7FF8000000000000`; on an x86 processor it is `0xFFF8000000000000`, with the sign bit set. The standard does not fix the sign of a NaN.

**Signaling NaN.** The word `0x7FF4000000000001` is a signaling NaN. After `s + 0.0`, the word is `0x7FFC000000000001`: the arithmetic set the quiet bit and kept the payload.

**Signed zero.** `0.0 == -0.0` is `True`, but `math.copysign(1.0, -0.0)` is `-1.0`. The product `-1e-300 * 1e-300` underflows to `-0.0`. `1.0 - 1.0` is `0.0`, `-0.0 + -0.0` is `-0.0`, and `-0.0 + 0.0` is `0.0`. `math.atan2(0.0, -1.0)` is $\pi$, and `math.atan2(-0.0, -1.0)` is $-\pi$: the sign of zero selects the side of the cut along the negative real axis.

**Infinity.** `1e308 * 10` gives `inf`, `-1e308 * 10` gives `-inf`, and `1 / math.inf` gives `0.0`. `math.inf > 1.7976931348623157e308` is `True`.

**Where Python differs from the default IEEE 754 results.** Python raises an exception where IEEE 754 by default returns a special value and sets a flag: `1 / 0.0` raises `ZeroDivisionError` (IEEE 754 gives $+\infty$), `math.sqrt(-1.0)` raises `ValueError` (NaN), and `math.exp(1000)` raises `OverflowError` ($+\infty$). The basic multiplication does not raise: `1e308 * 10` is `inf`. Also `math.fsum([-0.0, -0.0])` returns `0.0`, where an IEEE sum of the two zeros is $-0$.

**Pitfalls (non-examples of a total order).**

- `min(nan, 1.0)` is `nan` but `min(1.0, nan)` is `1.0`. The built-in `min` compares with `<`, which is false for NaN, so the result depends on the order of the arguments. IEEE 754-2019 defines `minimum` (which returns NaN if an input is NaN) and `minimumNumber` (which ignores a quiet NaN) in Clause 9.6 for this reason.
- `sorted([3.0, nan, 1.0, 2.0])` returns `[3.0, nan, 1.0, 2.0]`, not a sorted list, because a sort needs a total order. Clause 5.10 defines `totalOrder`, in which $-\text{NaN} < -\infty < \cdots < -0 < +0 < \cdots < +\infty < +\text{NaN}$; sort by it, or remove the NaNs first.
- `x == 0.0` does not tell the two zeros apart; use `math.copysign(1.0, x)`.
- `nan in [nan]` is `True` in Python, because list membership tests identity first. It is not a NaN comparison.
- An infinity is not an error value in all code. In [interval arithmetic](/interval-arithmetic/) an endpoint $\pm\infty$ is a correct bound, and in the [log-sum-exp trick](/log-sum-exp-trick/) $\log 0 = -\infty$ is a correct result.

## Related definitions

- [IEEE 754](/ieee-754/): the standard that defines these values.
- [Floating-point exceptions](/floating-point-exceptions/): invalid operation, division by zero and overflow, which produce them, with their flags.
- [Subnormal numbers](/subnormal-numbers/): the values between zero and the smallest normal number.
- [Rounding modes](/rounding-modes/): the mode decides the sign of an exact zero sum, and whether overflow gives $\infty$ or $\Omega$.
- [Unit in the last place](/ulp/): `math.ulp` returns `inf` for an infinity and `nan` for a NaN.

## References
