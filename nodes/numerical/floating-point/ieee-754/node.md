---
tag: TK8CMX
kind: definition
slug: ieee-754
name: IEEE 754 standard
aliases:
- IEEE floating-point standard
- IEEE 754-2019
- IEEE 754-2008
- IEEE 754-1985
area: numerical/floating-point
level: intro
summary: The standard that defines binary and decimal floating-point formats, their encodings, correctly rounded operations, rounding directions, special values and exceptions.
prereqs: [floating-point-arithmetic]
see_also: [floating-point-model, rounding-modes, special-floating-point-values, subnormal-numbers, floating-point-exceptions, ulp, decimal-floating-point, shortest-round-trip-representation]
sources:
  - url: https://doi.org/10.1109/IEEESTD.2019.8766229
    title: IEEE Std 754-2019, IEEE Standard for Floating-Point Arithmetic
    locator: Clause 3 (3.3 sets of floating-point data, 3.4 binary interchange format encodings, 3.6 interchange format parameters, 3.7 extended precisions); Clause 4.3 (rounding-direction attributes); Clause 5 (operations, 5.12 conversions to and from decimal character sequences); Clause 6 (infinity, NaNs and sign bit); Clause 7 (default exception handling); Clause 9 (recommended operations)
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Chapter 3, Floating-Point Formats and Environment (Section 3.1 on the IEEE 754-2008 standard and its history, the formats, the encodings and the operations)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 2.1 (floating-point number systems), Section 2.2 (model of arithmetic, Theorem 2.2) and Section 2.3 (IEEE arithmetic)
  - paper: doi:10.1145/103162.103163
    title: David Goldberg, What every computer scientist should know about floating-point arithmetic, ACM Computing Surveys 23(1) (1991), 5-48
    locator: Section 2, The IEEE Standard (formats and operations, special quantities, exceptions, flags and trap handlers)
  - url: https://people.eecs.berkeley.edu/~wkahan/ieee754status/IEEE754.PDF
    title: W. Kahan, Lecture Notes on the Status of IEEE Standard 754 for Binary Floating-Point Arithmetic (1996)
    locator: the design goals of the standard and the reasons for gradual underflow, signed zero, infinities and NaNs
---

IEEE 754 is the technical standard of the IEEE that defines [floating-point](/floating-point-arithmetic/) formats, their bit encodings, and the arithmetic on them. It requires each basic operation to return the exact result rounded to the format by a chosen [rounding mode](/rounding-modes/), and it defines [infinities, NaNs and signed zeros](/special-floating-point-values/), [subnormal numbers](/subnormal-numbers/) and five [exceptions](/floating-point-exceptions/). The first version is IEEE 754-1985, it was revised in 2008, and the current version is IEEE 754-2019. Almost all hardware since the late 1980s follows it, and a Python `float` is its binary64 format.

## Definition

**Notation.** A floating-point system $\mathbb{F}$ has base $\beta$, precision $p$ (the number of base-$\beta$ digits of the significand) and exponent range $[e_{\min}, e_{\max}]$. The default on this site is binary64, with $\beta = 2$, $p = 53$, $e_{\min} = -1022$ and $e_{\max} = 1023$. The unit roundoff is $u = \tfrac12 \beta^{1-p}$, which is $2^{-53}$ for binary64 with rounding to nearest. $\mathrm{fl}(x)$ is the value of a real $x$ rounded to $\mathbb{F}$.

**Formats (Clause 3.3).** A format is fixed by its base $\beta \in \{2, 10\}$, its precision $p$ and its largest exponent $e_{\max}$, and the standard always takes $e_{\min} = 1 - e_{\max}$. Its finite values are the numbers

$$x = (-1)^s \cdot m \cdot \beta^{e}, \qquad s \in \{0, 1\}, \quad m = d_0.d_1 d_2 \ldots d_{p-1} \ (0 \le d_i < \beta), \quad e_{\min} \le e \le e_{\max}.$$

A value is *normal* when $d_0 \neq 0$ (then $\beta^{e} \le |x| < \beta^{e+1}$) and *subnormal* when $d_0 = 0$ and $e = e_{\min}$. Each format also holds $+\infty$, $-\infty$, quiet NaNs and signaling NaNs. Zero has two encodings, $+0$ and $-0$, which compare equal.

**The binary interchange formats (Clauses 3.4 and 3.6).** A binary format of width $k$ stores three fields: a sign bit $S$, a biased exponent $E$ of $w$ bits, and a trailing significand $T$ of $t = p - 1$ bits. The leading bit $d_0$ is not stored. The bias is $e_{\max}$. The value of the word is

$$v = \begin{cases} (-1)^S \, 2^{E - e_{\max}} \, (1 + T \cdot 2^{-t}) & 1 \le E \le 2^w - 2 \quad \text{(normal)}, \\ (-1)^S \, 2^{e_{\min}} \, (T \cdot 2^{-t}) & E = 0 \quad \text{(zero or subnormal)}, \\ (-1)^S \, \infty & E = 2^w - 1, \ T = 0, \\ \text{NaN} & E = 2^w - 1, \ T \neq 0. \end{cases}$$

| format | width $k$ | $w$ | $p$ | $e_{\max}$ | $u$ (round to nearest) | largest finite | smallest normal | smallest subnormal |
|---|---|---|---|---|---|---|---|---|
| binary16 | 16 | 5 | 11 | 15 | $2^{-11}$ | 65504 | $2^{-14}$ | $2^{-24}$ |
| binary32 | 32 | 8 | 24 | 127 | $2^{-24}$ | $(2 - 2^{-23}) 2^{127}$ | $2^{-126}$ | $2^{-149}$ |
| binary64 | 64 | 11 | 53 | 1023 | $2^{-53}$ | $(2 - 2^{-52}) 2^{1023}$ | $2^{-1022}$ | $2^{-1074}$ |
| binary128 | 128 | 15 | 113 | 16383 | $2^{-113}$ | $(2 - 2^{-112}) 2^{16383}$ | $2^{-16382}$ | $2^{-16494}$ |

The decimal formats decimal32, decimal64 and decimal128 have $p = 7, 16, 34$ and $e_{\max} = 96, 384, 6144$. They have two encodings of the significand (Clause 3.5); see [decimal floating point](/decimal-floating-point/).

The encoding is chosen so that, for two non-negative finite values, the order of the values is the order of the words read as unsigned integers. So the next float above a positive $x$ has the word of $x$ plus one, and the number of floats between two positive values is the difference of their words.

**Operations (Clause 5).** The standard requires addition, subtraction, multiplication, division, square root, [fused multiply-add](/fused-multiply-add/), remainder, conversions between formats and to and from integers, and comparisons. Each one of them "computes the infinitely precise result and then rounds it" to the destination format: with $\circ$ the active rounding function,

$$\mathrm{fl}(x \mathbin{op} y) = \circ(x \mathbin{op} y) \quad \text{for } op \in \{+, -, \times, /\}, \qquad \mathrm{fl}(\sqrt{x}) = \circ(\sqrt{x}).$$

This property is called *correct rounding*. It makes each result a function of the inputs and the rounding direction only, so the same program on two conforming machines gives the same bits, if the compiler keeps the order of the operations and the formats (Clause 11).

**Rounding directions (Clause 4.3).** There are five: roundTiesToEven (the default for binary formats, see [round to nearest, ties to even](/round-to-nearest-even/)), roundTiesToAway, roundTowardPositive, roundTowardNegative and roundTowardZero. The last three are the directed roundings used by [interval arithmetic](/interval-arithmetic/). See [rounding modes](/rounding-modes/).

**Special values and exceptions (Clauses 6 and 7).** Overflow gives $\pm\infty$ in the default round to nearest. An invalid operation such as $0/0$, $\infty - \infty$ or $\sqrt{-1}$ gives a quiet NaN. The five exceptions are invalid operation, division by zero, overflow, underflow and inexact. By default each one sets a status flag and the computation goes on with a defined result.

**Conversions to and from decimal (Clause 5.12).** Conversion between a binary format and a decimal character string is correctly rounded up to a large number of digits. For a binary format of precision $p$, the standard defines $P_{\min} = 1 + \lceil p \log_{10} 2 \rceil$ significant decimal digits, which is 9 for binary32 and 17 for binary64. A conversion to a string with $P_{\min}$ digits and back recovers the same value. The [shortest round-trip string](/shortest-round-trip-representation/) is often shorter.

**Recommended, not required (Clause 9).** The standard recommends correctly rounded elementary functions such as $\exp$, $\log$ and $\sin$, but does not require them. Common math libraries do not round them correctly in all cases, so their results can differ between systems. See [correctly rounded functions](/correctly-rounded-functions/).

### What follows from the definition

From correct rounding in round to nearest, each real $x$ in the normal range satisfies $\mathrm{fl}(x) = x(1 + \delta)$ with $|\delta| \le u$ (Higham, Theorem 2.2; the bound is proved, and it needs no underflow and no overflow). So each basic operation on normal results obeys the [standard model](/floating-point-model/) $\mathrm{fl}(x \mathbin{op} y) = (x \mathbin{op} y)(1 + \delta)$, $|\delta| \le u$. The [error-free transformations](/error-free-transformations/), such as [TwoSum](/two-sum/), depend on more than this model: they use the fact that the result is the exact rounding.

### Versions

IEEE 754-1985 defined binary formats only. IEEE 854-1987 gave a radix-independent version. IEEE 754-2008 merged the two, added the decimal formats, binary16 and binary128 as interchange formats, the fused multiply-add, and roundTiesToAway. IEEE 754-2019 is a minor revision: it adds the augmented operations (Clause 9.5, which return a sum or product and its rounding error) and new minimum and maximum operations, and it fixes errors. W. Kahan was the main architect of the 1985 standard, and he received the Turing Award in 1989 in part for this work.

## Examples and non-examples

**The number 1.0 in binary64.** The word is `0x3FF0000000000000`: $S = 0$, $E = 1023$, $T = 0$, so $v = 2^{0} \cdot 1 = 1$. The next word `0x3FF0000000000001` holds $1 + 2^{-52}$, so the gap above 1 is $2^{-52} = 2u$, which is [machine epsilon](/machine-epsilon/).

**The number 0.1 is not in $\mathbb{F}$.** The literal `0.1` rounds to the word `0x3FB999999999999A`: $S = 0$, $E = 1019$ (so $e = -4$), $T = \texttt{0x999999999999A}$. Its exact value is

$$\mathrm{fl}(0.1) = \frac{3602879701896397}{2^{55}} = 0.1000000000000000055511151231257827\ldots,$$

and $\mathrm{fl}(0.1) - 0.1 = 1/(10 \cdot 2^{54}) \approx 5.55 \times 10^{-18}$. The relative error is $2^{-54} \approx 5.55 \times 10^{-17}$, below $u = 2^{-53} \approx 1.11 \times 10^{-16}$. In binary32 the literal rounds to `0x3DCCCCCD`, that is $13421773/2^{27} = 0.100000001490116\ldots$, and in binary16 to `0x2E66`, that is $0.0999755859375$.

**0.1 + 0.2.** The exact sum of the two stored values exceeds $0.3$ by $3/180143985094819840 \approx 1.67 \times 10^{-17}$. Correct rounding of this exact sum gives `0x3FD3333333333334`, printed as `0.30000000000000004`. The literal `0.3` rounds to `0x3FD3333333333333`. The two results differ by one [ulp](/ulp/). The operation is correct: each step is correctly rounded, and the difference comes from the rounding of the inputs.

**The extreme values of binary64.**

| value | word | Python `float.hex` |
|---|---|---|
| smallest subnormal $2^{-1074} \approx 4.94 \times 10^{-324}$ | `0x0000000000000001` | `0x0.0000000000001p-1022` |
| smallest normal $2^{-1022} \approx 2.23 \times 10^{-308}$ | `0x0010000000000000` | `0x1.0000000000000p-1022` |
| largest finite $\approx 1.80 \times 10^{308}$ | `0x7FEFFFFFFFFFFFFF` | `0x1.fffffffffffffp+1023` |
| $+\infty$ | `0x7FF0000000000000` | `inf` |
| a quiet NaN | `0x7FF8000000000000` | `nan` |
| $-0$ | `0x8000000000000000` | `-0x0.0p+0` |

There are $2 (2^{11} - 1) 2^{52} = 18437736874454810624$ words with a finite value (each zero counted twice) and $2 (2^{52} - 1) = 9007199254740990$ NaN words.

**Overflow.** In Python, `1e308 * 10` gives `inf`, and `inf - inf` gives `nan`. These are the default results of Clause 7 for overflow and for an invalid operation.

**Non-examples.**

- bfloat16 is not an IEEE 754 interchange format. It has the layout of the upper half of binary32 ($w = 8$, $p = 8$), but the standard does not define it. See [bfloat16](/bfloat16/).
- [Posits](/posit-format/) and the [logarithmic number system](/logarithmic-number-system/) are other number formats. They do not follow IEEE 754.
- A mode that flushes subnormal results to zero (the FTZ and DAZ modes of many processors) does not conform. The standard requires gradual underflow.
- The 80-bit format of the x87 unit is not an interchange format. The standard allows it as an extended precision format (Clause 3.7). When a compiler keeps intermediate results in it, the result of an expression can differ from the binary64 result, by [double rounding](/double-rounding/).
- The standard does not fix the result of `exp(x)` or `sin(x)`. Two conforming systems can return values that differ by one ulp.

## Related definitions

- [Floating-point arithmetic](/floating-point-arithmetic/): the general number systems of which IEEE 754 fixes particular members.
- [Standard model of floating-point arithmetic](/floating-point-model/): the error model that correct rounding implies.
- [Rounding modes](/rounding-modes/) and [round to nearest, ties to even](/round-to-nearest-even/): the five rounding-direction attributes.
- [Infinities, NaN and signed zero](/special-floating-point-values/), [subnormal numbers](/subnormal-numbers/) and [floating-point exceptions](/floating-point-exceptions/): the parts of the standard that handle the edges of the range.
- [Unit in the last place](/ulp/) and [machine epsilon](/machine-epsilon/): the spacing of the floats.
- [Fused multiply-add](/fused-multiply-add/): the one operation with three inputs that the 2008 revision made required.
- [Shortest round-trip representation](/shortest-round-trip-representation/): how to print a float with the fewest decimal digits.

## References
