---
tag: 845A4C
kind: concept
slug: floating-point-arithmetic
name: Floating-point arithmetic
aliases:
- IEEE 754
- finite-precision arithmetic
- floating-point number system
- floating point
area: numerical/floating-point
level: intro
summary: Finite-precision arithmetic on numbers stored as significand times power of a base.
prereqs: [positional-number-system, radix]
see_also: [floating-point-model, ieee-754, rounding-modes, ulp, machine-epsilon, subnormal-numbers, catastrophic-cancellation, error-free-transformations]
sources:
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 2, Floating Point Arithmetic (Section 2.1 the number system and Theorem 2.2 on the error of rounding, Section 2.3 IEEE arithmetic)
  - book: isbn:9783319765259
    title: Jean-Michel Muller, Nicolas Brunie, Florent de Dinechin, Claude-Pierre Jeannerod, Mioara Joldes, Vincent Lefevre, Guillaume Melquiond, Nathalie Revol and Serge Torres, Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Chapter 2, Definitions and Basic Notions (Sections 2.1 Floating-Point Numbers, 2.2 Rounding, 2.3.2 The ulp function, 2.6 Lost and Preserved Properties of Real Arithmetic); Section 3.1, The IEEE 754-2008 Standard
  - url: https://doi.org/10.1109/IEEESTD.2019.8766229
    title: IEEE Std 754-2019, IEEE Standard for Floating-Point Arithmetic
    locator: Clause 3 (formats; Clause 3.6, interchange format parameters), Clause 4.3 (rounding-direction attributes), Clause 5.1 and 5.4 (correctly rounded operations)
  - paper: doi:10.1145/103162.103163
    title: "David Goldberg, What every computer scientist should know about floating-point arithmetic, ACM Computing Surveys 23(1) (1991), 5-48"
    locator: the sections Rounding Error (ulps and relative error) and The IEEE Standard
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.2.1, Single-Precision Calculations, and Section 4.2.2, Accuracy of Floating Point Arithmetic
---

Floating-point arithmetic is arithmetic on a finite set of numbers of the form $\pm m \cdot \beta^{q}$, where the [radix](/radix/) $\beta$ and the number of digits of the integer $m$ are fixed, and where each operation returns its exact result rounded to a member of the set. It gives a large range of magnitudes with a fixed relative accuracy, so that $10^{-300}$ and $10^{300}$ are both stored with about 16 significant decimal digits in the usual 64-bit format. The [IEEE 754](/ieee-754/) standard fixes the formats, the [rounding modes](/rounding-modes/) and the [special values](/special-floating-point-values/) that almost all current hardware uses. The price of the finite set is rounding error: the operations are not exact, and some laws of real arithmetic, such as associativity, fail.

## In plain words

A computer cannot store every real number, so it keeps a fixed number of significant digits and a separate scale, like the scientific notation 6.022 times ten to the 23rd. The digits say what the number is, and the scale says where the point goes. Because the point "floats" with the scale, tiny and huge numbers keep the same number of correct digits.

After each operation, the exact answer is usually not one of the numbers that the computer can store. The machine then picks the nearest one that it can store. This small change is the rounding error. One rounding error is tiny, but many of them can add up, and a subtraction of two close numbers can make the earlier errors large. Most of the pages of this sub-area are about how to control these errors, or how to get rid of them.

## The idea

### Notation

All pages of this sub-area use the same notation. $\mathbb{F}$ is a floating-point system with base $\beta \ge 2$, precision $p \ge 2$ and exponent range $[e_{\min}, e_{\max}]$. The default is binary64 (double precision, the Python `float`): $\beta = 2$, $p = 53$, $e_{\min} = -1022$, $e_{\max} = 1023$. $\mathrm{fl}(x)$ is the value of $\mathbb{F}$ that a real $x$ rounds to, and $\mathrm{fl}(x \mathbin{op} y)$ is the computed result of an operation. The unit roundoff is $u = \tfrac12 \beta^{1-p}$, which is $2^{-53}$ for binary64 with rounding to nearest. [Machine epsilon](/machine-epsilon/) is $\varepsilon = \beta^{1-p} = 2u$, the gap between $1$ and the next larger float; where a page uses $\varepsilon$ it says so. The [standard model](/floating-point-model/) is $\mathrm{fl}(x \mathbin{op} y) = (x \mathbin{op} y)(1 + \delta)$ with $|\delta| \le u$, when no underflow or overflow occurs. For a real $x \ne 0$ with $\beta^{e} \le |x| < \beta^{e+1}$, the [ulp](/ulp/) is $\mathrm{ulp}(x) = \beta^{\max(e, e_{\min}) - p + 1}$, the definition that Muller et al. use in Section 2.3.2 (Goldberg's definition, extended to all reals). Finally $\gamma_n = nu/(1 - nu)$ for $nu < 1$.

### The numbers

A finite member of $\mathbb{F}$ is a number

$$x = (-1)^s \cdot M \cdot \beta^{e - p + 1}, \qquad s \in \{0, 1\}, \quad M \in \mathbb{Z}, \quad 0 \le M \le \beta^{p} - 1, \quad e_{\min} \le e \le e_{\max}.$$

$M$ is the integral significand and $e$ is the exponent. Many pairs $(M, e)$ give the same $x$; the representation is *normalized* when $M \ge \beta^{p-1}$, and then $\beta^{e} \le |x| < \beta^{e+1}$. A nonzero $x$ that has no normalized representation has $e = e_{\min}$ and $M < \beta^{p-1}$; it is [subnormal](/subnormal-numbers/). In a binade $[\beta^{e}, \beta^{e+1})$ with $e \ge e_{\min}$ the floats are equally spaced, with gap $\beta^{e-p+1} = \mathrm{ulp}(x)$, and the gap grows by a factor $\beta$ from one binade to the next. So the absolute spacing changes with the magnitude, and the relative spacing stays between $\beta^{-p}$ and $\beta^{1-p}$.

The common binary formats of IEEE 754-2019 (Clause 3.6) are below. The values are exact powers of two or their stated decimal roundings.

| format | $p$ | $e_{\min}$ | $e_{\max}$ | $u$ | largest finite | smallest normal | smallest subnormal |
|---|---|---|---|---|---|---|---|
| binary16 | 11 | $-14$ | 15 | $2^{-11}$ | 65504 | $2^{-14}$ | $2^{-24}$ |
| binary32 | 24 | $-126$ | 127 | $2^{-24}$ | $(2 - 2^{-23}) 2^{127} \approx 3.40 \times 10^{38}$ | $2^{-126} \approx 1.18 \times 10^{-38}$ | $2^{-149} \approx 1.40 \times 10^{-45}$ |
| binary64 | 53 | $-1022$ | 1023 | $2^{-53}$ | $(2 - 2^{-52}) 2^{1023} \approx 1.80 \times 10^{308}$ | $2^{-1022} \approx 2.23 \times 10^{-308}$ | $2^{-1074} \approx 4.94 \times 10^{-324}$ |

A binary64 value is stored in 64 bits: 1 sign bit, 11 bits of biased exponent $E = e + 1023$, and the 52 low bits of $M$ (the leading bit of a normal $M$ is implicit). $E = 0$ codes zero and the subnormals, and $E = 2047$ codes the infinities and NaNs.

### Rounding

A rounding function maps each real to a member of $\mathbb{F}$ (or to an infinity on overflow). IEEE 754-2019 (Clause 4.3) defines five: [round to nearest, ties to even](/round-to-nearest-even/) (the default), round to nearest with ties away from zero, and the three directed roundings toward $+\infty$, toward $-\infty$ and toward zero. An operation is *correctly rounded* when its result is the exact real result, rounded once by the current rounding function. IEEE 754 requires correct rounding for $+$, $-$, $\times$, $/$, the square root and the [fused multiply-add](/fused-multiply-add/) (Clause 5.4.1), and for the conversions between formats.

**The error of one rounding.** Let $x$ be a real with $\beta^{e} \le |x| < \beta^{e+1}$ and $e_{\min} \le e \le e_{\max}$, and let $\mathrm{fl}$ round to nearest. If $|x|$ is at most the largest finite float, then

$$\mathrm{fl}(x) = x(1 + \delta), \qquad |\delta| \le u.$$

*Proof.* The members of $\mathbb{F}$ in $[\beta^{e}, \beta^{e+1}]$ are the numbers $k \beta^{e-p+1}$ for the integers $k$ from $\beta^{p-1}$ to $\beta^{p}$ (the last one is $\beta^{e+1}$, which is in $\mathbb{F}$ when $e < e_{\max}$; when $e = e_{\max}$ the bound on $|x|$ keeps $|x|$ at most the largest float $(\beta^{p}-1)\beta^{e-p+1}$). So $|x|$ lies between two neighbours at distance $\beta^{e-p+1}$, and the nearest one is at distance at most $\tfrac12 \beta^{e-p+1}$. Hence $|\mathrm{fl}(x) - x| \le \tfrac12 \beta^{e-p+1} = \tfrac12 \beta^{1-p} \beta^{e} \le u |x|$. Set $\delta = (\mathrm{fl}(x) - x)/x$. $\square$

This is Theorem 2.2 of Higham. With a directed rounding the same argument gives $|\delta| < \beta^{1-p} = 2u$. In the subnormal range the absolute error is still at most $\tfrac12 \beta^{e_{\min}-p+1}$, but the relative error can be large (for example, $\mathrm{fl}(3 \cdot 2^{-1076}) = 2^{-1074}$ has relative error $1/3$, and $\mathrm{fl}(2^{-1075}) = 0$ has relative error $1$), so the bound needs the assumption "no underflow".

### Special values

IEEE 754 adds $+0$ and $-0$ (equal under comparison, but $1/(+0) = +\infty$ and $1/(-0) = -\infty$), $+\infty$ and $-\infty$, and NaN ("not a number") for results such as $0/0$ and $\sqrt{-1}$. Each NaN compares unequal to everything, itself included. An operation that cannot return an exact result raises one of five [exception flags](/floating-point-exceptions/): invalid operation, division by zero, overflow, underflow and inexact.

### What changes from real arithmetic

- Addition and multiplication are commutative, but not associative: in binary64, $(0.1 + 0.2) + 0.3 = 0.6000000000000001$ and $0.1 + (0.2 + 0.3) = 0.6$.
- The distributive law fails, and $x + y = x$ can hold for $y \ne 0$ ($10^{16} + 1 = 10^{16}$ in binary64).
- A subtraction of two close values is exact (the [Sterbenz lemma](/sterbenz-lemma/)), but it exposes the errors that the two values already had: this is [catastrophic cancellation](/catastrophic-cancellation/).
- Monotonicity survives: if $x \le y$ then $\mathrm{fl}(x) \le \mathrm{fl}(y)$, and so $a \le b$ gives $\mathrm{fl}(a + c) \le \mathrm{fl}(b + c)$ (Muller et al., Section 2.6).
- The error of a rounded sum or product is itself a float in most cases, and cheap [error-free transformations](/error-free-transformations/) compute it exactly.

## Examples

**The decimal 0.1.** The decimal $0.1$ has no finite binary expansion. In binary64 it rounds to $0x3FB999999999999A$, whose exact value is

$$0.1000000000000000055511151231257827021181583404541015625,$$

with relative error about $5.55 \times 10^{-17} \approx 0.5u$. In binary32 it rounds to $0x3DCCCCCD$, which is $0.100000001490116119384765625$.

**A sum that is not 0.3.** $\mathrm{fl}(0.1 + 0.2)$ is $0.3000000000000000444\ldots$, and the float nearest to $0.3$ is $0.2999999999999999888\ldots$. They are neighbours, one ulp ($2^{-54}$) apart, so `0.1 + 0.2 == 0.3` is false in Python and in C.

**Bit patterns.** $1.0$ is $0x3FF0000000000000$ (sign 0, biased exponent $1023$, fraction 0). $-0.0$ is $0x8000000000000000$. $+\infty$ is $0x7FF0000000000000$, and the quiet NaN that Python makes is $0x7FF8000000000000$. The largest finite float $1.7976931348623157 \times 10^{308}$ is $0x7FEFFFFFFFFFFFFF$, the smallest normal $2.2250738585072014 \times 10^{-308}$ is $0x0010000000000000$, and the smallest subnormal $5 \times 10^{-324}$ (exactly $2^{-1074}$) is $0x0000000000000001$.

**Spacing.** $\mathrm{ulp}(1) = 2^{-52}$ and $\mathrm{ulp}(2^{53}) = 2$. So $2^{53} + 1$ is not a binary64 number: it is a tie between $2^{53}$ and $2^{53} + 2$, and ties to even returns $2^{53}$. This is why a binary64 value holds each integer exactly only up to $2^{53}$.

**A non-example: fixed point.** A 64-bit fixed-point number with 32 fraction bits has the same absolute spacing $2^{-32}$ everywhere. It holds $10^{-12}$ with no correct significant digit and cannot hold $10^{12}$ at all, while binary64 holds both with relative error at most $2^{-53}$.

## Where it is used

- Almost all scientific, engineering and graphics code computes in binary64 or binary32; machine learning also uses binary16 and [bfloat16](/bfloat16/).
- The [standard model](/floating-point-model/) turns the rounding rule into an algebraic tool for [backward error analysis](/backward-error-analysis/) and [forward error analysis](/forward-error-analysis/).
- [Floating-point summation](/floating-point-summation/), the [accurate dot product](/accurate-dot-product/) and [double-double arithmetic](/double-double-arithmetic/) recover accuracy that plain rounding loses.
- Conversion between binary floats and decimal text is its own problem: [decimal to floating-point](/decimal-to-floating-point/) and [floating-point to decimal](/floating-point-to-decimal/).
- Money and other decimal data use [decimal floating-point](/decimal-floating-point/), and when a fixed precision is not enough, programs use [arbitrary-precision arithmetic](/arbitrary-precision-arithmetic/).

## References
