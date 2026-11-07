---
tag: GQ2TAR
kind: concept
slug: correctly-rounded-functions
name: Correctly rounded functions
aliases:
- correct rounding
- correctly rounded elementary functions
- CR functions
area: numerical/floating-point
level: advanced
summary: Elementary functions whose result is the exact value rounded once to the nearest float.
prereqs: [floating-point-arithmetic, rounding-modes, ulp]
see_also: [table-maker-dilemma, correctly-rounded-elementary-functions, cody-waite-range-reduction, payne-hanek-argument-reduction, double-double-arithmetic, ieee-754, decimal-to-floating-point, fused-multiply-add]
sources:
  - url: https://doi.org/10.1109/IEEESTD.2019.8766229
    title: IEEE Std 754-2019, IEEE Standard for Floating-Point Arithmetic
    locator: Clause 5.4.1 (squareRoot and the basic operations, required to be correctly rounded); Clause 9.2 (recommended correctly rounded functions such as exp, log, sin and pow)
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Chapter 10, Evaluating Floating-Point Elementary Functions (range reduction, polynomial approximation, the table maker's dilemma and correct rounding)
  - paper: "Abraham Ziv, Fast evaluation of elementary mathematical functions with correctly rounded last bit, ACM Transactions on Mathematical Software 17(3) (1991), 410-423"
    title: Abraham Ziv, Fast evaluation of elementary mathematical functions with correctly rounded last bit (1991)
    locator: the strategy of evaluating with increasing precision until the rounding is decided
  - paper: "Vincent Lefevre and Jean-Michel Muller, Worst cases for correct rounding of the elementary functions in double precision, Proceedings of the 15th IEEE Symposium on Computer Arithmetic (ARITH 15), 2001, 111-118"
    title: Vincent Lefevre and Jean-Michel Muller, Worst cases for correct rounding of the elementary functions in double precision (2001)
    locator: the hardest-to-round binary64 inputs of exp, log and other functions, and the precision they require
  - paper: doi:10.1145/3747840
    title: "Nicolas Brisebarre, Guillaume Hanrot, Jean-Michel Muller and Paul Zimmermann, Correctly rounded evaluation of a function: why, how, and at what cost?, ACM Computing Surveys (2025)"
    locator: a survey of the reasons for correct rounding, the methods (Ziv's strategy, worst cases) and the libraries (CRlibm, CORE-MATH, RLIBM)
  - url: https://core-math.gitlabpages.inria.fr/
    title: The CORE-MATH project, correctly rounded mathematical functions
    locator: correctly rounded implementations of the C mathematical functions in binary32 and binary64
---

A function $f$ is *correctly rounded* in a floating-point format if, for every input float $x$, it returns $\circ(f(x))$, the exact real value $f(x)$ rounded once by the current [rounding mode](/rounding-modes/). IEEE 754 has required this of addition, multiplication, division, square root and FMA since 1985 (FMA since 2008); for $\exp$, $\log$, $\sin$, $\mathrm{pow}$ and the other elementary functions it is only recommended (Clause 9.2), because guaranteeing it is hard: the value must be computed accurately enough to decide which side of a rounding boundary it lies on, and the required accuracy is set by the [table maker's dilemma](/table-maker-dilemma/). Libraries such as CRlibm and CORE-MATH show that it can be done at a cost close to that of ordinary libraries, and C23 reserves names with the prefix `cr_` for such functions.

## In plain words

A computer can store only some numbers. When the true answer of a calculation lies between two of them, the best possible result is the stored number nearest to the true answer. A function that always returns that number is called correctly rounded.

For adding and multiplying, every modern computer does this. For functions such as the exponential or the sine, most math libraries are very close but not perfect: once in a while they return the neighbor of the best number. The difference is tiny, but it means two computers can disagree, and some mathematical properties of the function can break. Getting it right every time is possible but needs care for the rare inputs whose answer lies extremely close to halfway between two stored numbers.

## The idea

**Notation.** A binary format with precision $p$ (binary64, $p = 53$, by default), round to nearest with ties to even unless stated, $\circ$ for the rounding function of the current mode, $u = 2^{-p}$ and $\mathrm{ulp}$ as in Muller et al., Section 2.3.2. See [floating-point arithmetic](/floating-point-arithmetic/).

**Definition.** An implementation $\hat{f}$ of $f$ is

- *correctly rounded* if $\hat{f}(x) = \circ(f(x))$ for every float $x$ in the domain; with round to nearest this means $|\hat{f}(x) - f(x)| \le \tfrac12\mathrm{ulp}(f(x))$ with ties broken by the rule of the mode;
- *faithful* if $\hat{f}(x)$ is one of the two floats that bracket $f(x)$ (and equals $f(x)$ when it is a float), an error below $1$ ulp;
- accurate to *$k$ ulps* if $|\hat{f}(x) - f(x)| \le k \cdot \mathrm{ulp}(f(x))$.

Most libraries aim for an error below $1$ ulp, which is faithful rounding or close to it, without a proof.

**What correct rounding gives.** These hold for every correctly rounded implementation, in any rounding mode, because $\circ$ is monotone and depends only on the real value:

- *Reproducibility.* All correctly rounded implementations return the same bits, on every platform and in every language.
- *Monotonicity.* If $f$ is nondecreasing on an interval, so is $\hat{f}$ on the floats of that interval.
- *Symmetry and exact values.* If $f$ is odd, $\hat{f}(-x) = -\hat{f}(x)$ in the symmetric modes (to nearest and toward zero); if $f(x)$ is a float, $\hat{f}(x) = f(x)$.
- *Error bounds.* In the [standard model](/floating-point-model/) the function behaves like a basic operation: $\hat{f}(x) = f(x)(1 + \delta)$ with $|\delta| \le u$ when the result is normal, so rounding error analyses can treat it as one operation.
- *Interval arithmetic.* With directed rounding, a correctly rounded function gives the tightest possible enclosure.

**How it is computed.** An approximation $y$ with a proved error bound $|y - f(x)| \le \varepsilon|f(x)|$ decides the rounding if the whole interval $[y - \varepsilon|y|, y + \varepsilon|y|]$, enlarged slightly for safety, contains no rounding boundary (a midpoint between floats for round to nearest, a float for the directed modes). Ziv's strategy (1991) first computes $y$ with a precision slightly above $p$, for example with [double-double arithmetic](/double-double-arithmetic/), which decides the rounding for almost all inputs; when the test fails, it recomputes with higher precision, and so on. The loop ends if the precision eventually exceeds the distance from $f(x)$ to the nearest boundary; that distance is positive for $\exp$, $\log$, $\sin$ and similar functions at all inputs except a few known exact cases (for example $\exp(0) = 1$, $\log(1) = 0$; for $x \ne 0$ rational, $\exp(x)$ is irrational by the Lindemann-Weierstrass theorem, so it is never a float or a midpoint). The worst cases found by exhaustive search (Lefèvre and Muller, 2001) bound the precision needed, so a library can stop at a fixed precision with a proof. Range reduction, by [Cody-Waite](/cody-waite-range-reduction/) or [Payne-Hanek](/payne-hanek-argument-reduction/), must be accurate to the same level.

**Exact cases.** Functions with many exact or midpoint results, such as $\mathrm{pow}$ ($\mathrm{pow}(9, 0.5) = 3$), $\log_2$ at powers of two, and $\mathrm{hypot}$, need a separate test for them, since no precision decides a value that is exactly a midpoint.

## Examples

These were run with Python 3.14 on macOS 15, whose `math.exp` and `math.log` call the system math library, with references computed with `decimal` at $60$ significant digits and rounded to binary64 with `fractions.Fraction` (a correct rounding of the 60-digit value is the correct rounding of $f(x)$ unless $f(x)$ is within $10^{-60}$ relative of a midpoint, which none of these is).

**A library that is not correctly rounded.** For $100000$ random $x$ in $[-700, 700]$, `math.exp(x)` differed from the correctly rounded value in $149$ cases, about $0.15\%$, and in each the result was the neighbor of the correct one. For $x$ = 0x1.41df019e3279cp+9 $= 643.7422368761504$, the exact $e^{x}$ lies $0.49958$ ulp above the float 0x1.a6c56304c0275p+928, so its correct rounding is that float; the library returned the next float up, 0x1.a6c56304c0276p+928, at $0.50042$ ulp from $e^{x}$. The library error is just over half an ulp, as expected of a good library, but the result is the wrong neighbor.

**Close to the midpoint.** For $y = 13477.09331206735$, $\log y$ lies $0.49995$ ulp above the float 0x1.3047a739be059p+3, only $5.3 \times 10^{-5}$ ulp from the midpoint, and `math.log` returned the neighbor 0x1.3047a739be05ap+3. To decide this case an approximation needs a relative accuracy of about $2^{-66}$. In $100000$ random positive binary64 inputs `math.log` misrounded only this one.

**Required operations.** `math.sqrt`, `math.fma` and the four basic operations are correctly rounded on IEEE 754 hardware; for $100000$ random $x$, `math.sqrt(x)` was the float nearest to $\sqrt{x}$ every time, checked by squaring the neighboring midpoints in exact rational arithmetic.

## Where it is used

- **The basic operations.** IEEE 754 requires correct rounding of $+$, $-$, $\times$, $/$, $\sqrt{\ }$, FMA, conversions between formats, and conversions between binary and decimal within stated limits; see [decimal to floating-point](/decimal-to-floating-point/) conversion.
- **Correctly rounded libraries.** CRlibm (ENS Lyon, 2000s) provided correctly rounded binary64 functions with proofs; the CORE-MATH project (since 2022) provides correctly rounded binary32 and binary64 versions of the C mathematical functions, and some of its code has been adopted by C libraries. The RLIBM project generates correctly rounded functions for small formats by polynomial fitting with linear programming. The problem of building them is the [correctly rounded elementary functions](/correctly-rounded-elementary-functions/) problem.
- **Reproducible computation.** Climate models, distributed simulations and consensus systems need bitwise-identical results across machines; correctly rounded functions are the only library functions that guarantee it.
- **Testing other libraries.** A correctly rounded implementation, or a multiple-precision one like MPFR, is the reference against which the errors of fast libraries are measured in ulps.
- **Language standards.** C23 reserves the identifiers `cr_exp`, `cr_log` and so on for correctly rounded versions of the functions in `<math.h>`.

## References
