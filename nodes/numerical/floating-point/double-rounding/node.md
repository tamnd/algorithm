---
tag: 79643R
kind: concept
slug: double-rounding
name: Double rounding
aliases:
- double rounding error
area: numerical/floating-point
level: core
summary: Rounding a value twice, first to an intermediate precision, which can differ from a single correct rounding.
prereqs: [floating-point-arithmetic, round-to-nearest-even, rounding-modes]
see_also: [round-to-nearest-even, rounding-modes, bfloat16, decimal-to-floating-point, fused-multiply-add, correctly-rounded-functions, ieee-754, ulp]
sources:
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Section 3.2, On the Possible Hidden Use of a Higher Internal Precision (double rounding, x87 extended precision); Section 4.7.3, Double Roundings in Division; Section 7.8.1, A Software Algorithm Around Double Rounding
  - paper: "Samuel A. Figueroa, When is double rounding innocuous?, ACM SIGNUM Newsletter 30(3) (1995), 21-26"
    title: Samuel A. Figueroa, When is double rounding innocuous? (1995)
    locator: the theorem that double rounding through precision q is innocuous for the basic operations on p-bit operands when q is at least 2p + 2
  - paper: "Sylvie Boldo and Guillaume Melquiond, Emulation of FMA and correctly rounded sums: proved algorithms using rounding to odd, IEEE Transactions on Computers 57(4) (2008), 462-471"
    title: Sylvie Boldo and Guillaume Melquiond, Emulation of FMA and correctly rounded sums, proved algorithms using rounding to odd (2008)
    locator: rounding to odd and the theorem that rounding to odd at precision p + 2 or more followed by rounding to nearest at precision p is a correct rounding
  - paper: doi:10.1145/103162.103163
    title: "David Goldberg, What every computer scientist should know about floating-point arithmetic, ACM Computing Surveys 23(1) (1991), 5-48"
    locator: the section on languages and compilers (extended precision and double rounding)
---

Double rounding happens when an exact result is first rounded to a precision $q$ and then to a smaller precision $p$. The two roundings together can differ from a single rounding to $p$: when the exact value lies just above or below a midpoint between two $p$-digit numbers, the first rounding can land exactly on that midpoint, and the second then breaks the artificial tie in the wrong direction. The x87 floating-point unit, which computed in 64-bit precision and stored in binary64, is the classic source; conversions through an intermediate format are another. Double rounding is harmless when $q \ge 2p + 2$ for the basic operations, and rounding to odd at the first step removes the problem for any $q \ge p + 2$.

## In plain words

Rounding a number once to the nearest whole number is safe. Rounding it in two steps is not always the same. Round $1.49$ to one decimal place and you get $1.5$; round that to a whole number and you get $2$. But $1.49$ is nearer to $1$.

Computers make this mistake when they compute with extra digits and then store the result with fewer digits. Most of the time the answer is the same. Once in a few thousand operations it is off by one in the last place, and the result differs from that of a machine that rounds once. The fix is either to keep many extra digits, or to make the first rounding leave a mark that tells the second rounding which way to go.

## The idea

**Notation.** Binary arithmetic, $\mathrm{RN}_p(x)$ the rounding of a real $x$ to the nearest number with $p$ significant bits, ties to even, and $\mathrm{ulp}_p(x) = 2^{e - p + 1}$ for $2^{e} \le |x| < 2^{e+1}$, with an unbounded exponent range. This is the ulp of Muller et al., Section 2.3.2; see [floating-point arithmetic](/floating-point-arithmetic/) for the full notation.

**The failure.** Let $q > p$. Every $p$-bit number and every midpoint between two consecutive $p$-bit numbers is a $q$-bit number. Suppose $x$ is slightly above such a midpoint $m$, with $x - m < \tfrac12\mathrm{ulp}_q(x)$. Then $\mathrm{RN}_q(x) = m$, and $\mathrm{RN}_p(m)$ is a tie, which goes to the even neighbor; if that is the lower one, the result is below $m$, while $\mathrm{RN}_p(x)$ is above. The symmetric case is just below a midpoint. This is the only way the two can differ.

**Theorem (error of double rounding).** For every real $x$ and $q > p$,

$$|\mathrm{RN}_p(\mathrm{RN}_q(x)) - x| \le \tfrac12\left(1 + 2^{p - q}\right)\mathrm{ulp}_p(x),$$

and $\mathrm{RN}_p(\mathrm{RN}_q(x))$ is one of the two $p$-bit neighbors of $x$.

*Proof.* Assume $x > 0$ and let $y = \mathrm{RN}_q(x)$, so $|y - x| \le \tfrac12\mathrm{ulp}_q(x) = \tfrac12 2^{p-q}\mathrm{ulp}_p(x)$. Let $a \le x < b$ be the two consecutive $p$-bit numbers around $x$ (if $x$ is a $p$-bit number, it is a $q$-bit number too, $y = x$ and both roundings are exact). Since $a$ and $b$ are $q$-bit numbers and $y$ is a nearest $q$-bit number, $a \le y \le b$. So $\mathrm{RN}_p(y) \in \{a, b\}$, which is the second claim. If $y = b$ then the result is $b$ and the error is $|y - x| \le \tfrac12 2^{p-q}\mathrm{ulp}_p(x)$. Otherwise $a \le y < b$ lie in one binade, $\mathrm{ulp}_p(y) = \mathrm{ulp}_p(x)$, and $|\mathrm{RN}_p(y) - x| \le |\mathrm{RN}_p(y) - y| + |y - x| \le \tfrac12\mathrm{ulp}_p(x) + \tfrac12 2^{p - q}\mathrm{ulp}_p(x)$. $\blacksquare$

So double rounding is a [faithful rounding](/correctly-rounded-functions/) with an error slightly above half an ulp, and in terms of the unit roundoff $u = 2^{-p}$ the relative error is at most $u(1 + 2^{p-q})$. For binary64 through the 64-bit x87 format this is $2^{-53}(1 + 2^{-11})$. The [standard model](/floating-point-model/) holds with this slightly larger $u$, so most error analyses survive; what is lost is correct rounding, and with it the [error-free transformations](/error-free-transformations/) and bit-for-bit reproducibility.

**When it is innocuous.** Figueroa (1995) proved that if $a$ and $b$ are $p$-bit numbers and $x$ is the exact $a + b$, $a - b$, $a \times b$, $a / b$ or $\sqrt{a}$, then $\mathrm{RN}_p(\mathrm{RN}_q(x)) = \mathrm{RN}_p(x)$ whenever $q \ge 2p + 2$. The reason is that such an $x$ cannot be too close to a midpoint without being on it. binary32 operations computed in binary64 and rounded back ($53 \ge 2 \cdot 24 + 2$) are therefore correctly rounded; binary64 operations computed in the x87 format ($64 < 108$) are not.

**Rounding to odd.** Let $\mathrm{RO}_q(x)$ be $x$ if $x$ is a $q$-bit number, and otherwise the one of its two $q$-bit neighbors whose last bit is $1$.

*Theorem (Boldo and Melquiond, 2008).* If $q \ge p + 2$, then $\mathrm{RN}_p(\mathrm{RO}_q(x)) = \mathrm{RN}_p(x)$ for every real $x$.

*Proof.* Since $q \ge p + 2$, each $p$-bit number and each midpoint between consecutive $p$-bit numbers is a $q$-bit number whose last bit (at precision $q$) is $0$. If $x$ is a $q$-bit number the claim is trivial. Otherwise $x$ lies strictly between two consecutive $q$-bit numbers $c < x < c^{+}$, exactly one of which has last bit $1$, and $\mathrm{RO}_q(x)$ is that one, so it is not a $p$-bit number or a midpoint. No $p$-bit number or midpoint lies strictly between $c$ and $c^{+}$, so $x$ and $\mathrm{RO}_q(x)$ lie in the same closed interval between consecutive "breakpoints" (the $p$-bit numbers and the midpoints), and neither is a breakpoint. $\mathrm{RN}_p$ is constant on the open interval between two consecutive breakpoints, so the two results agree. $\blacksquare$

Rounding to odd is easy to implement (truncate and set the last bit to the OR of the discarded bits, the "sticky" bit), and it is what makes several FMA emulations and correctly rounded sums of three numbers work.

## Examples

Every claim below was checked with exact rational arithmetic (`fractions.Fraction`).

**A sum, through 64 bits.** Let $x = 1 + 2^{-53} + 2^{-105}$, the exact sum of the binary64 numbers $1$ and $2^{-53}(1 + 2^{-52})$. It lies just above the midpoint $1 + 2^{-53}$ between $1$ and $1 + 2^{-52}$, so $\mathrm{RN}_{53}(x) = 1 + 2^{-52}$. But $\mathrm{RN}_{64}(x) = 1 + 2^{-53}$, because $2^{-105}$ is far below half of $\mathrm{ulp}_{64}(1) = 2^{-63}$, and $\mathrm{RN}_{53}(1 + 2^{-53}) = 1$ by ties to even. An x87 unit in its default mode returns $1$. With rounding to odd at 64 bits, $\mathrm{RO}_{64}(x) = 1 + 2^{-53} + 2^{-63}$ and the second rounding gives $1 + 2^{-52}$, the correct result.

**A product, through 64 bits.** For $a$ = 0x1.63aa70ccdbedep+0 and $b$ = 0x1.6e0a7506e44ecp+0, the correctly rounded product is 0x1.fc8c3483c32c3p+0 and the double-rounded one is 0x1.fc8c3483c32c2p+0. Among $200000$ random products of binary64 numbers in $[1, 2)$, $39$ differed, a rate near $2^{-12}$, which matches the chance that the exact product falls within $\tfrac12\mathrm{ulp}_{64}$ of a 53-bit midpoint. Python, which rounds once to binary64, returns the correct product.

**A decimal string, through binary64 to binary32.** The decimal `1.0000000596046448` is slightly above $1 + 2^{-24} = 1.000000059604644775390625$, the midpoint between the binary32 numbers $1$ and $1 + 2^{-23}$. The nearest binary32 number is $1 + 2^{-23} = 1.0000001192092896$. Parsing the string to binary64 first gives exactly $1 + 2^{-24}$ (the string is within $2.5 \times 10^{-17}$ of it, less than half a binary64 ulp), and rounding that to binary32 is a tie that goes to $1$. So a `strtof` written as `(float)strtod(s)` is wrong for this input. The same trap applies to the conversion of binary64 to [bfloat16](/bfloat16/) through binary32.

**Rare failures at a wide gap.** In $20000$ random reals with 81 bits, rounding to 53 bits and then to 24 bits never differed from one rounding to 24 bits; this is an observation, since for arbitrary reals the failure is possible (the decimal example above is one) but its chance is only about $2^{-30}$ per input. Rounding to odd at 26 bits followed by rounding to 24 bits never differed either, and that is the theorem.

## Where it is used

- **The x87 unit and extended precision.** Compilers for 32-bit x86 kept intermediates in 80-bit registers, so the same C program could give different results with and without optimization. Setting the precision control to 53 bits removes double rounding for normal results but not for subnormal ones, because the exponent range stays wide (Muller et al., Section 3.2). SSE2 arithmetic, the default on x86-64, rounds once.
- **Language rules.** C's `FLT_EVAL_METHOD` reports whether intermediates are kept wider, and Java's original `strictfp` keyword forced binary64 behavior; Java 17 made strict semantics the default. [IEEE 754](/ieee-754/)-2019, Clause 10, lets a language define the precision used for expressions.
- **Narrow formats.** Operations on binary16 or [bfloat16](/bfloat16/) operands computed in binary32 and rounded back are correctly rounded, since $24 \ge 2 \cdot 11 + 2$ and $24 \ge 2 \cdot 8 + 2$. The conversion of an arbitrary binary64 value to binary16 or bfloat16 through binary32 is not covered by that theorem and can be wrong, as in the decimal example above.
- **Emulation.** A [fused multiply-add](/fused-multiply-add/) computed as `(double)((long double)a*b + c)`, or binary32 FMA through binary64, needs a rounding to odd at the wide step to be correct.
- **Conversions.** [Decimal to floating-point](/decimal-to-floating-point/) conversion to a narrow format must round once from the decimal value.

## References
