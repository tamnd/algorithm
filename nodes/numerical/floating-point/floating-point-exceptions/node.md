---
tag: 7FWDXS
kind: concept
slug: floating-point-exceptions
name: Floating-point exceptions
aliases:
- overflow
- underflow
- invalid operation
- divide-by-zero
- inexact flag
- IEEE 754 exceptions
area: numerical/floating-point
level: core
summary: Flags and traps raised on overflow, underflow, invalid operations, division by zero and inexact results.
prereqs: [floating-point-arithmetic, ieee-754]
see_also: [special-floating-point-values, subnormal-numbers, ieee-754, rounding-modes, floating-point-model, fused-multiply-add, log-sum-exp-trick, interval-arithmetic]
sources:
  - url: https://doi.org/10.1109/IEEESTD.2019.8766229
    title: IEEE Std 754-2019, IEEE Standard for Floating-Point Arithmetic
    locator: Clause 7, Default exception handling (7.1 overview, 7.2 invalid operation, 7.3 division by zero, 7.4 overflow, 7.5 underflow, 7.6 inexact); Clause 8, Alternate exception handling attributes; Clause 6, Infinity, NaNs, and sign bit
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Section 2.5, Exceptions; Section 3.1.6, Default exception handling; Section 3.1.7, Special values; Sections 7.2.3 to 7.2.5 (detecting overflow, underflow and inexact in an implementation)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 2.3, IEEE Arithmetic; Section 27.1, Exploiting IEEE Arithmetic; Section 27.8, Avoiding Underflow and Overflow
  - paper: doi:10.1145/103162.103163
    title: "David Goldberg, What every computer scientist should know about floating-point arithmetic, ACM Computing Surveys 23(1) (1991), 5-48"
    locator: the section Special Quantities and the section Exceptions, Flags and Trap Handlers
  - url: https://people.eecs.berkeley.edu/~wkahan/ieee754status/IEEE754.PDF
    title: William Kahan, Lecture notes on the status of IEEE Standard 754 for binary floating-point arithmetic (1996)
    locator: the rationale for nonstop arithmetic with default results and sticky flags
---

A floating-point exception is an event in which an operation has no exact, finite, ordinary result to return: the result is undefined (invalid operation), infinite (division by zero), too large (overflow), too small (underflow), or not representable (inexact). [IEEE 754](/ieee-754/) defines these five exceptions and, for each, a default result that lets the computation continue, together with a sticky status flag that records that the event happened. Most programs never look at the flags and rely on the default results, which are $\pm\infty$, NaN, subnormal numbers and rounded values. The design, due to Kahan, is called nonstop arithmetic.

## In plain words

Some calculations have no good answer. Zero divided by zero has none; a number larger than the largest storable number cannot be stored; a number that is too tiny gets rounded toward zero. A computer can either stop the program when this happens or return a special value and keep going.

The floating-point standard chose to keep going. Dividing one by zero gives infinity, zero over zero gives a value called "not a number", and a result that is too large becomes infinity. Each such event also sets a flag that stays set, so a program can check at the end whether anything unusual happened. The most common event, a result that had to be rounded, is not an error at all; it has a flag too.

## The idea

**Notation.** Binary64 with round to nearest, ties to even, $p = 53$, $e_{\min} = -1022$, $e_{\max} = 1023$, $\Omega = (2 - 2^{-52})\,2^{1023}$ the largest finite number and $2^{-1022}$ the smallest normal one; see [floating-point arithmetic](/floating-point-arithmetic/) for the full notation.

**The five exceptions and their default results** (IEEE 754-2019, Clause 7).

| exception | when it is signaled | default result |
|---|---|---|
| invalid operation | no useful result exists: $0 \cdot \infty$, $\infty - \infty$, $0/0$, $\infty/\infty$, $\sqrt{x}$ for $x < 0$, $\mathrm{fma}(0, \infty, c)$, the remainder $x \bmod 0$, conversion of NaN or of an out-of-range value to an integer, ordered comparison with a NaN, any operation on a signaling NaN | a quiet NaN |
| division by zero | an exact infinite result from finite operands: $x/0$ for finite $x \ne 0$, $\log 0$ | $\pm\infty$, with the sign of the exact limit |
| overflow | the result rounded as if the exponent range were unbounded exceeds $\Omega$ in magnitude | $\pm\infty$ with round to nearest; $\pm\Omega$ or $\pm\infty$ with directed rounding, according to the direction |
| underflow | the result is tiny (nonzero and below $2^{-1022}$ in magnitude) and, in the default handling, also inexact | the rounded result, which is subnormal, $\pm 0$ or $\pm 2^{-1022}$ |
| inexact | the rounded result differs from the exact one | the rounded result (and the overflow result, after overflow) |

A NaN as input is not itself an exception: a quiet NaN propagates through arithmetic without signaling. Overflow always also signals inexact. An exact subnormal result does not raise the underflow flag in the default handling, so the flag means "accuracy may have been lost to underflow".

**Flags.** Each exception has a status flag, which is raised when the exception is signaled and stays raised until the program lowers it. A program can clear the flags, run a block of code, and test them afterwards; this is the cheap way to detect a rare problem without testing each operation. **Alternate handling** (Clause 8) lets a language offer traps, substitution of a chosen value, or an immediate transfer of control; these are optional.

**When the result is tiny.** Underflow is about tininess, and IEEE 754 lets a binary implementation detect tininess either *before rounding* (the exact result is below $2^{-1022}$) or *after rounding* (the result rounded to $p$ bits with an unbounded exponent is below $2^{-1022}$). The two differ only for exact results in $(2^{-1022}(1 - 2^{-54}), 2^{-1022})$, which round up to $2^{-1022}$.

**Why nonstop arithmetic.** A default result often gives the right final answer. With $\infty$, $1/(1 + 1/x)$ is $0$ for $x = 0$, the correct limit, with no test; a NaN that reaches the output shows that a branch of the computation was undefined, without stopping the rest; gradual underflow to [subnormal numbers](/subnormal-numbers/) keeps $x - y = 0$ equivalent to $x = y$. The [standard model](/floating-point-model/) $\mathrm{fl}(x \mathbin{op} y) = (x \mathbin{op} y)(1 + \delta)$, $|\delta| \le u$, holds exactly when no overflow and no underflow occur; the exceptions mark the operations to which it does not apply.

## Examples

Each line was run in Python 3.14 (binary64) and checked with `fractions.Fraction` where a value is exact.

**Overflow and its threshold.** With $\Omega = 1.7976931348623157 \times 10^{308}$, $\mathrm{ulp}(\Omega) = 2^{971} \approx 1.996 \times 10^{292}$, so the overflow threshold for round to nearest is $\Omega + 2^{970}$. Then `Omega + 9e291` returns $\Omega$ (inexact, no overflow) and `Omega + 1e292` returns `inf` (overflow). `1e200 * 1e200` returns `inf`, while `math.hypot(1e200, 1e200)` returns $1.414213562373095 \times 10^{200}$, because it scales before squaring (Higham, Section 27.8).

**Underflow.** `5e-324 / 2` returns $0.0$: the exact $2^{-1075}$ is a tie between $0$ and $2^{-1074}$, and ties to even gives $0$, with relative error $1$. For $a = 1 - 2^{-52}$ and $b = 2^{-1022}(1 + 2^{-52})$, the exact product is $2^{-1022}(1 - 2^{-104})$, tiny before rounding, and the result is $2^{-1022}$, not tiny after rounding: an implementation that detects tininess after rounding raises inexact only, and one that detects it before rounding also raises underflow.

**Invalid operation.** `inf - inf` and `0 * inf` return `nan`. `math.sqrt(-1)` and `math.fma(0, inf, 1.0)` raise `ValueError` in Python instead of returning NaN.

**Inexact.** $0.1 + 0.2$ is inexact: $\mathrm{Fraction}(0.1) + \mathrm{Fraction}(0.2) \ne \mathrm{Fraction}(0.1 + 0.2)$. $0.5 + 0.25$ is exact. Nearly every operation on general data raises the inexact flag; it is useful when exactness itself is the result, for example to test whether a quotient of integers is exact.

**Python is not IEEE by default.** Python maps some exceptions to Python exceptions and others to the default results:

| expression | IEEE 754 default | Python 3.14 |
|---|---|---|
| `1.0 / 0.0` | `inf`, division by zero flag | `ZeroDivisionError` |
| `1e308 * 10` | `inf`, overflow flag | `inf` |
| `1e200 ** 2` | `inf`, overflow flag | `OverflowError` |
| `math.exp(1000)` | `inf`, overflow flag | `OverflowError` |
| `math.log(0)` | `-inf`, division by zero flag | `ValueError` |
| `math.fsum([1e308, 1e308])` | `inf` | `OverflowError` (intermediate overflow) |
| `int(float('nan'))` | invalid operation | `ValueError` |

The `decimal` module implements the flags and traps of the General Decimal Arithmetic specification: in a context with no traps, `1/0` returns `Infinity` and sets `DivisionByZero`, `Infinity - Infinity` returns `NaN` and sets `InvalidOperation`, and `9e384 * 10` in a decimal64 context returns `Infinity` and sets `Overflow`, `Inexact` and `Rounded`.

## Where it is used

- **Robust numerical code.** LAPACK and the BLAS scale vectors to avoid overflow in norms, and use the fact that the default results propagate; the [log-sum-exp trick](/log-sum-exp-trick/) avoids overflow of $e^{x}$ for large $x$.
- **Fast paths with a check.** A routine can run a fast algorithm, test the overflow, underflow and invalid flags once at the end, and rerun a slower, careful version only if a flag is raised (Higham, Section 27.1).
- **Proofs of floating-point algorithms.** Error bounds and [error-free transformations](/error-free-transformations/) are stated "if no overflow occurs" or "if no underflow occurs"; the flags are the run-time test of these hypotheses.
- **[Interval arithmetic](/interval-arithmetic/) and directed rounding.** Overflow to $\Omega$ or $\infty$ according to the rounding direction is what keeps enclosures valid near the top of the range.
- **Special values.** NaN, $\pm\infty$ and signed zero, described on the page on [special floating-point values](/special-floating-point-values/), are the default results that make nonstop arithmetic possible.

## References
