---
tag: YNMZJH
kind: problem
slug: shortest-round-trip-representation
name: Shortest round-trip decimal representation
aliases:
- shortest representation
- shortest uniquely identifying decimal
- free-format output
area: numerical/floating-point
level: core
summary: Find the shortest decimal string that reads back to the same float.
prereqs: [floating-point-to-decimal, decimal-to-floating-point, ulp, round-to-nearest-even]
see_also: [ryu, dragon4, grisu, clinger-decimal-conversion, ieee-754, subnormal-numbers, floating-point-arithmetic]
sources:
  - paper: doi:10.1145/93542.93559
    title: Guy L. Steele Jr. and Jon L. White, How to print floating-point numbers accurately, Proceedings of PLDI 1990, 112-126
    locator: the free-format output problem (shortest output that reads back correctly) and its solution by FPP and Dragon4
  - paper: "David W. Matula, In-and-out conversions, Communications of the ACM 11(1) (1968), 47-50"
    title: David W. Matula, In-and-out conversions (1968)
    locator: the number of digits needed for a base conversion to be one-to-one
  - paper: doi:10.1145/103162.103163
    title: David Goldberg, What every computer scientist should know about floating-point arithmetic, ACM Computing Surveys 23(1) (1991), 5-48
    locator: Theorem 15 (17 decimal digits recover a binary64 number, and 9 a binary32 number) and the discussion of binary to decimal conversion
  - paper: doi:10.1145/3192366.3192369
    title: Ulf Adams, Ryu, fast float-to-string conversion, Proceedings of PLDI 2018, 270-282
    locator: the problem statement (shortest, then closest, with the rounding interval of round to nearest even) and the survey of earlier algorithms
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Section 4.9, Radix Conversion (4.9.1, conditions on the formats, the number of digits needed for an invertible conversion)
  - url: https://doi.org/10.1109/IEEESTD.2019.8766229
    title: IEEE Std 754-2019, IEEE Standard for Floating-Point Arithmetic
    locator: Clause 5.12.2, External decimal character sequences representing finite numbers (enough digits to recover the float)
---

The shortest round-trip problem asks, for a finite binary float $x$, for a decimal number with the fewest significant digits that converts back to exactly $x$ under correctly rounded decimal-to-binary conversion. Among the shortest such decimals, the usual rule picks the one closest to $x$. In binary64 the answer always has at most 17 significant digits, by Matula's theorem, and it is what Python's `repr`, JavaScript's `Number.prototype.toString` and Java's `Double.toString` (since JDK 19) print.

## In plain words

A computer stores a number like 0.1 in binary, and the stored value is not exactly 0.1 but a number very close to it. When the number is printed, writing all its exact decimal digits would take dozens of digits and confuse everyone. Writing too few digits is worse: two different stored numbers could then print the same, and reading the text back would give the wrong one.

The goal is the middle ground. Print the fewest digits such that reading the text back gives exactly the same stored number. For the stored 0.1 that is just "0.1", even though the stored value is not exactly one tenth. If several strings of that length work, print the one closest to the stored value.

## Definition

**Notation.** A binary floating-point system $\mathbb{F}$ with precision $p$ and exponent range $[e_{\min}, e_{\max}]$, binary64 by default ($p = 53$, $e_{\min} = -1022$). The reader uses round to nearest, ties to even, written $\mathrm{fl}(\cdot)$; [ulp](/ulp/) is as in Muller et al., Section 2.3.2 (Goldberg's definition extended to the reals). $u = 2^{-p}$.

**The rounding interval.** For a finite positive $x \in \mathbb{F}$ with neighbours $x^- < x < x^+$ in $\mathbb{F}$ (with $x^+ = 2^{e_{\max}+1}$ for the largest float, the value at which rounding overflows), let

$$R(x) = \{\, r \in \mathbb{R} : \mathrm{fl}(r) = x \,\},$$

which is the interval from $m^- = (x^- + x)/2$ to $m^+ = (x + x^+)/2$, closed at both ends if the significand of $x$ is even and open at both ends if it is odd. Negative $x$ are handled by symmetry, and $\pm 0$, $\pm\infty$ and NaN are printed by fixed rules.

**The problem.** Given $x$, find integers $d \ge 1$ and $k$ and a decimal $D = c \cdot 10^{k}$ with $c$ an integer of exactly $d$ digits (no trailing zeros), such that $D \in R(x)$ and $d$ is minimal. Among the minimal choices, output the $D$ that minimizes $|D - x|$; if two are equally close, a fixed tie rule decides (Ryu takes the one with an even last digit).

The output format (where the decimal point goes, when to use exponent notation) is a separate choice; Python's `repr` uses exponent notation when the decimal exponent of the leading digit is below $-4$ or at least $16$.

## Variants

- **Shortest without the closest rule.** Any shortest $D \in R(x)$; the closest rule makes the answer unique except for exact ties. A related weaker goal, met by Grisu2, is a string that reads back correctly and is usually, but not always, the shortest.
- **Fixed precision.** Print exactly $n$ significant digits, correctly rounded (`%.17g`). The result reads back to $x$ when $n \ge 17$, but it is not the shortest.
- **Other formats.** For binary32 the bound is 9 digits, for binary16 it is 5, for binary128 it is 36; the same problem is posed for each [IEEE 754](/ieee-754/) format.
- **Other readers.** If the reader rounds differently (toward zero, or ties away), $R(x)$ changes, and so does the answer. Steele and White parametrize the algorithm by the reader's rounding.
- **The reverse direction.** Decimal-to-binary conversion with correct rounding ([decimal to floating-point](/decimal-to-floating-point/), [Clinger's algorithm](/clinger-decimal-conversion/)) is the reader that defines $R(x)$.
- **Shortest decimal in an interval.** The general question: given rationals $a < b$, find the decimal with fewest digits in $[a, b]$. The float problem is the case $[a, b] = R(x)$.

## Examples

Each row was produced in Python 3.14 and checked with `decimal.Decimal(x)`, which prints the exact value.

| float $x$ | exact value of $x$ (abridged) | shortest (`repr`) | digits |
|---|---|---|---|
| `0.1` | $0.1000000000000000055511151231257827\ldots$ | `0.1` | 1 |
| `0.3` | $0.2999999999999999888977697537484345\ldots$ | `0.3` | 1 |
| `0.1 + 0.2` | $0.3000000000000000444089209850062616\ldots$ | `0.30000000000000004` | 17 |
| `1e23` | $99999999999999991611392$ | `1e+23` | 1 |
| `2.0**-1074` | $4.9406564584124654\ldots \times 10^{-324}$ | `5e-324` | 1 |
| `2.0**53 + 2` | $9007199254740994$ | `9007199254740994.0` | 16 |
| largest float | $1.7976931348623157081\ldots \times 10^{308}$ | `1.7976931348623157e+308` | 17 |

**The shortest string need not be the correctly rounded one.** For $x = 2^{-1017}$, whose exact value begins $7.1202363472230444258\ldots \times 10^{-307}$, the correctly rounded 16-digit decimal is $7.120236347223044 \times 10^{-307}$, but it lies $4.26 \times 10^{-323}$ below $x$, while the gap to the predecessor is only half as large as the gap to the successor, because $x$ is a power of two: $m^-$ is $3.95 \times 10^{-323}$ below $x$. So that decimal reads back to $x^-$. The 16-digit decimal $7.120236347223045 \times 10^{-307}$ is $5.74 \times 10^{-323}$ above $x$, inside the upper half-gap of $7.9 \times 10^{-323}$, and it is the answer; an algorithm that tries `%.{n}e` for increasing $n$ would print 17 digits instead.

**How long the answers are.** Over $10^5$ random 64-bit patterns that encode finite nonzero floats (seed 1), the shortest representation had 17 digits for 45%, 16 for 49%, 15 for 5.4%, and fewer for the rest. For $10^5$ floats uniform in $[1, 2)$, 78% needed 17 digits, because the floats there are spaced $2^{-52} \approx 2.2 \times 10^{-16}$ apart, closer than the 16-digit decimals ($10^{-15}$).

## Known algorithms

| algorithm | year | method | always shortest and closest |
|---|---|---|---|
| [Dragon4](/dragon4/) (Steele and White) | 1990 | exact big-integer digit generation with the interval bounds scaled alongside | yes |
| Gay's `dtoa` | 1990 | floating-point fast path, big-integer fallback | yes |
| Burger and Dybvig | 1996 | Dragon4 with a fast estimate of the decimal exponent | yes |
| [Grisu](/grisu/) 2 and 3 (Loitsch) | 2010 | 64-bit integers and cached powers of ten; Grisu3 detects the about 0.5% of inputs it cannot decide and falls back | Grisu3 with fallback |
| Errol (Andrysco, Jhala and Lerner) | 2016 | double-double arithmetic instead of big integers | yes |
| [Ryu](/ryu/) (Adams) | 2018 | precomputed 128-bit approximations of powers of five, no fallback | yes |
| Schubfach (Giulietti), Dragonbox (Jeon) | 2020 | like Ryu, with fewer digit-removal steps | yes |

The structure is shared: compute $m^-$, $x$ and $m^+$ scaled by a power of ten, then remove trailing digits while the interval still contains a candidate, and finally round the last digit toward $x$.

## Bounds

**Theorem** (Matula, 1968; Goldberg, Theorem 15). If $10^{n-1} > 2^p$, every finite $x \in \mathbb{F}$ has a decimal of at most $n$ significant digits in $R(x)$. For binary64 ($p = 53$) this gives $n = 17$; for binary32 ($p = 24$), $n = 9$.

*Proof.* Let $x > 0$ be normal, with $2^e \le x < 2^{e+1}$. The distance from $x$ to the nearer end of $R(x)$ is at least $2^{e-p-1}$: it equals $2^{e-p-1}$ on the lower side when $x = 2^e$ and $2^{e-p}$ otherwise. In both cases it is at least $x \cdot 2^{-p-1}$, because $x = 2^e$ in the first case and $x < 2^{e+1}$ in the second. Let $10^{k-1} \le x < 10^k$. The $n$-digit decimals near $x$ are spaced $10^{k-n} \le x \cdot 10^{1-n}$ apart, so the nearest one, $D$, satisfies $|D - x| \le \tfrac12 x \cdot 10^{1-n} < \tfrac12 x \cdot 2^{-p} = x \cdot 2^{-p-1}$, using $10^{n-1} > 2^p$. So $D$ lies strictly inside $R(x)$. For subnormal $x$ the half-gap is $2^{e_{\min}-p}$ on both sides and $x < 2^{e_{\min}}$, so the same inequality holds. $\square$

**The bound is attained.** $0.1 + 0.2$ needs 17 digits: the 16-digit decimals nearest to it, $0.3000000000000000$ and $0.3000000000000001$, read back to $0.3$, the float just below it, and to the float just above it, whose shortest form is `0.3000000000000001`. Since $10^{15} < 2^{53}$, the theorem does not give 16 digits, and such examples exist.

**The reverse bound.** Any decimal of at most 15 significant digits survives a conversion to binary64 and back to 15 digits (Goldberg, Theorem 15, and Muller et al., Section 4.9.1), since $2^{53-1} > 10^{15}$; this is why `DBL_DIG` is 15.

**Cost.** With precomputed tables of 128-bit approximations of powers of five, as in Ryu, the shortest representation of a binary64 number is found with a constant number of 64-by-128-bit multiplications and at most 17 digit-removal steps; exact methods with big integers need integers of about $|e| + p$ bits, up to about 1100 bits for binary64.

## Reductions

- **To interval search.** The problem is the shortest decimal in $R(x)$; with integers $\ell$, $c$, $h$ representing $m^-$, $x$, $m^+$ scaled by $2^a 10^b$, it reduces to stripping common decimal digits from $\ell$ and $h$ (Ryu's and Dragon4's digit loop).
- **From correct reading.** The problem is only well posed once the reader is fixed. It assumes a correctly rounding reader, so its correctness depends on decimal-to-binary conversion ([Clinger](/clinger-decimal-conversion/), Gay); with a reader that is not correctly rounded, the shortest string can read back to a neighbour.
- **From fixed-precision printing.** Trying $n = 1, 2, \ldots, 17$ digits with a correctly rounded fixed-precision printer and testing each by reading back gives a correct but non-minimal answer, as the example $2^{-1017}$ shows: it finds the shortest correctly rounded string, which can be one digit longer.

## Applications

- **Language runtimes.** Python's `repr` and `str` (since 3.1), JavaScript's `Number.prototype.toString` (required by ECMAScript), Java's `Double.toString` (fixed in JDK 19), Go's `strconv.FormatFloat` with precision $-1$, and Rust's `Display` for `f64` print the shortest round-trip string.
- **Serialization.** JSON, CSV and other text formats can carry floats exactly without hexadecimal notation, and the output stays short and readable.
- **Testing and debugging.** Two floats are equal exactly when their shortest strings are equal, so test expectations can be written in decimal without losing bits.
- **Reproducibility.** Configuration files and logs that store shortest round-trip strings reproduce the same binary values on reading.

## References
