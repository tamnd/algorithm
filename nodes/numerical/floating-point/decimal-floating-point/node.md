---
tag: NP4BWA
kind: definition
slug: decimal-floating-point
name: Decimal floating-point
aliases:
- IEEE 754 decimal formats
- DFP
- decimal64
area: numerical/floating-point
level: core
summary: IEEE 754 formats with base-10 significands, exact for decimal fractions such as 0.1.
prereqs: [floating-point-arithmetic, ieee-754]
see_also: [floating-point-model, decimal-to-floating-point, floating-point-to-decimal, rounding-modes, ulp, radix, positional-number-system, bfloat16]
sources:
  - url: https://doi.org/10.1109/IEEESTD.2019.8766229
    title: IEEE Std 754-2019, IEEE Standard for Floating-Point Arithmetic
    locator: Clause 3.3 (sets of floating-point data, cohorts and the quantum); Clause 3.5 (decimal interchange format encodings, DPD and BID); Clause 3.6 (the parameters of decimal32, decimal64 and decimal128); Clause 5.2 (decimal exponent calculation, the preferred exponent)
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Section 2.7.2, A Case for Radix 10; Section 3.1.1, Formats (the decimal formats and their two encodings); Section 3.4.7, Decimal Arithmetic; Section 7.3.1, Decimal Addition
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 2.1, Floating-Point Number System (Theorem 2.2 for any base); Section 2.7, Choice of Base and Distribution of Numbers (wobbling precision)
  - paper: "Mike F. Cowlishaw, Decimal floating-point: algorism for computers, Proceedings of the 16th IEEE Symposium on Computer Arithmetic (ARITH-16), 2003, 104-111"
    title: Mike F. Cowlishaw, Decimal floating-point, algorism for computers (2003)
    locator: the case for decimal arithmetic in commercial computation and the arithmetic that became the decimal part of IEEE 754-2008
  - url: https://docs.python.org/3/library/decimal.html
    title: Python documentation, decimal, Decimal fixed point and floating point arithmetic
    locator: contexts (precision, Emax, Emin, rounding), quantize, and the significance of trailing zeros
---

Decimal floating-point is floating-point arithmetic with base $\beta = 10$: each number is an integer significand of at most $p$ decimal digits times a power of ten. Decimal fractions such as $0.1$ and $0.01$ are then exact, and the results agree with hand calculation and with the rules of finance and law, which binary64 cannot do. [IEEE 754](/ieee-754/)-2008 added three decimal interchange formats, decimal32, decimal64 and decimal128, with two encodings each. Decimal formats keep trailing zeros: $1.0$ and $1.00$ are different members of one cohort, with the same value.

## Definition

**Notation.** A floating-point system $\mathbb{F}$ has base $\beta$, precision $p$ and exponent range $[e_{\min}, e_{\max}]$; $u = \tfrac12\beta^{1-p}$ is the unit roundoff for rounding to nearest, and $\mathrm{fl}(\cdot)$ is the rounded value (see [floating-point arithmetic](/floating-point-arithmetic/)).

**A decimal floating-point format** is a system with $\beta = 10$. In the integer-significand form of IEEE 754 (Clause 3.3), a finite number is

$$v = (-1)^{s} \cdot c \cdot 10^{q}, \qquad 0 \le c \le 10^{p} - 1, \qquad e_{\min} - p + 1 \le q \le e_{\max} - p + 1,$$

with $e_{\min} = 1 - e_{\max}$. The integer $c$ is the coefficient and $10^{q}$ is the *quantum*. The other values are $\pm\infty$ and quiet and signaling NaNs, as in binary.

**Cohorts.** Unlike a binary format, a decimal format does not normalize: the set of pairs $(c, q)$ with the same value $v$ is the *cohort* of $v$. For example $1 = 1 \cdot 10^{0} = 10 \cdot 10^{-1} = 100 \cdot 10^{-2}$, which print as `1`, `1.0` and `1.00`. They compare equal, but the exponent is kept and carries information (the number of significant decimal places). Each operation has a *preferred exponent* for its result: for an exact addition, the smaller of the two exponents; for an exact multiplication, the sum of the two exponents (Clause 5.2).

**The three interchange formats** (Clause 3.6):

| | decimal32 | decimal64 | decimal128 |
|---|---|---|---|
| storage | 32 bits | 64 bits | 128 bits |
| precision $p$ (digits) | 7 | 16 | 34 |
| $e_{\max}$ | 96 | 384 | 6144 |
| $e_{\min}$ | $-95$ | $-383$ | $-6143$ |
| exponent bias (for $q$) | 101 | 398 | 6176 |
| unit roundoff $u = \tfrac12 10^{1-p}$ | $5 \times 10^{-7}$ | $5 \times 10^{-16}$ | $5 \times 10^{-34}$ |
| largest finite | $9.999999 \times 10^{96}$ | $9.999999999999999 \times 10^{384}$ | $(10^{34} - 1)\,10^{6111}$ |
| smallest normal | $10^{-95}$ | $10^{-383}$ | $10^{-6143}$ |
| smallest subnormal | $10^{-101}$ | $10^{-398}$ | $10^{-6176}$ |

**Encodings** (Clause 3.5). A decimal word has a sign bit, a combination field and a trailing significand field. The standard defines two ways to store $c$:

- **BID** (binary integer decimal): $c$ is stored as a binary integer. For decimal64, if $c < 2^{53}$ the word is the sign, the 10-bit biased exponent $q + 398$ and the 53-bit $c$; otherwise the word starts with the bits `11` after the sign, then the exponent, then the low 51 bits of $c$, with an implicit prefix `100`. Software implementations (the Intel library) use BID because binary integer arithmetic is fast.
- **DPD** (densely packed decimal): the trailing field stores groups of three digits in 10-bit declets ($1000$ of the $1024$ patterns are used), and the combination field holds the leading digit. IBM's POWER and z hardware use DPD.

Both encodings represent exactly the same set of values, and an implementation must document which one it uses.

**Arithmetic.** The operations are correctly rounded, as in binary, with the same [rounding modes](/rounding-modes/) (round to nearest with ties to even is the default; IEEE 754-2019 also requires roundTiesToAway for decimal). So the [standard model](/floating-point-model/) holds with $u = \tfrac12 10^{1-p}$ when no underflow or overflow occurs (Higham, Theorem 2.2, holds for every base).

## Examples and non-examples

Each line was run with Python's `decimal` module, in a decimal64 context (`prec=16`, `Emax=384`, `Emin=-383`, ties to even), and compared with binary64 floats.

| expression | decimal64 | binary64 |
|---|---|---|
| $0.1 + 0.2 = 0.3$ | true | false ($0.30000000000000004$) |
| $0.01$ added $100$ times | $1.00$ | $1.0000000000000007$ |
| $2.675$ rounded to 2 places, ties to even | $2.68$ | $2.67$ (the stored value is $2.67499999999999982\ldots$) |
| $(1/3) \cdot 3$ | $0.9999999999999999$ | $1.0$ |
| $1.1 + 2.2$ | $3.3$ | $3.3000000000000003$ |
| $2.50 \times 2$ | $5.00$ (exponent $-2$ kept) | $5.0$ |

- **Decimal fractions are exact.** Every decimal number with at most 16 significant digits and an exponent in range is a decimal64 value; this is the main reason for the format. In binary64 the decimal $0.1$ is stored as $0.1000000000000000055511151231257827\ldots$.
- **Other fractions are not.** $1/3$ is rounded in decimal as in binary, and $(1/3) \cdot 3$ is not $1$ in decimal64. Decimal arithmetic removes representation errors of decimal input, not rounding errors.
- **Trailing zeros are kept.** $2.50 \times 2$ gives $5.00$, with the preferred exponent $-2$. A money computation keeps its number of cents without an explicit rescaling; `quantize` sets the quantum explicitly.
- **BID encodings.** The decimal64 value $1 = 1 \cdot 10^{0}$ has biased exponent $398$ and the word 0x31C0000000000001; $0.1 = 1 \cdot 10^{-1}$ is 0x31A0000000000001; $9999999999999999 \cdot 10^{369}$, the largest finite value, needs the long form and is 0x77FB86F26FC0FFFF; the smallest subnormal $10^{-398}$ is 0x0000000000000001.
- **Wobbling precision.** The spacing of decimal64 values is constant on each decade $[10^{e}, 10^{e+1})$, so the relative spacing varies by a factor of $10$ across the decade, against $2$ for binary. The bound $u = 5 \times 10^{-16}$ is reached just above $10^{e}$, while near $9.99 \times 10^{e}$ the relative error of rounding is at most $5 \times 10^{-17}$ (Higham, Section 2.7).
- **Non-example: a midpoint outside the interval.** With $p = 3$ and round to nearest, $a = 5.01$ and $b = 5.02$ give $\mathrm{fl}(a + b) = 10.0$ and $\mathrm{fl}(10.0/2) = 5.00 < a$. In base $2$ the computed midpoint $\mathrm{fl}(\mathrm{fl}(a + b)/2)$ always lies in $[a, b]$ when there is no overflow; in base $10$ it need not.
- **Non-example: binary fixed point with a decimal scale.** Storing cents as integers (a scaled binary integer) also makes decimal fractions exact, but it is fixed point: the scale is chosen once, and there is no rounding to a precision.

## Related definitions

- [Floating-point arithmetic](/floating-point-arithmetic/): the general definition, for any base, and the binary formats.
- [IEEE 754](/ieee-754/): the standard that defines the decimal interchange formats, since its 2008 revision; IEEE 854-1987 had allowed base 10 before.
- [Radix](/radix/) and [positional number systems](/positional-number-system/): the choice of base. The base $10$ makes conversion to and from decimal strings exact and fast, while binary needs the algorithms of [decimal to floating-point](/decimal-to-floating-point/) and [floating-point to decimal](/floating-point-to-decimal/) conversion.
- [ulp](/ulp/): in decimal, $\mathrm{ulp}(v) = 10^{q}$ for a value with full $p$-digit coefficient, and the quantum generalizes it to all members of a cohort.
- [Rounding modes](/rounding-modes/): decimal adds the requirement of roundTiesToAway, the rounding used in many commercial rules.

## References
