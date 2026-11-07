---
tag: PT81CC
kind: problem
slug: floating-point-to-decimal
name: Floating-point to decimal conversion
aliases:
- binary to decimal conversion
- float printing
- dtoa
area: numerical/floating-point
level: core
summary: Print a binary float as a decimal string.
prereqs: [floating-point-arithmetic, ulp, radix-conversion]
see_also: [shortest-round-trip-representation, dragon4, grisu, ryu, decimal-to-floating-point, big-integer, decimal-floating-point, round-to-nearest-even]
sources:
  - paper: doi:10.1145/93542.93559
    title: Guy L. Steele Jr. and Jon L. White, How to print floating-point numbers accurately, Proceedings of the ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI), 1990, 112-126
    locator: the free-format (shortest) and fixed-format printing problems, and the algorithms FPP and Dragon4
  - paper: "David M. Gay, Correctly rounded binary-decimal and decimal-binary conversions, Numerical Analysis Manuscript 90-10, AT&T Bell Laboratories, 1990"
    title: David M. Gay, Correctly rounded binary-decimal and decimal-binary conversions (1990)
    locator: the dtoa modes (shortest round trip and a fixed number of digits) with a floating-point fast path and a big-integer fallback
  - paper: doi:10.1145/1806596.1806623
    title: Florian Loitsch, Printing floating-point numbers quickly and accurately with integers, Proceedings of PLDI 2010, 233-243
    locator: Grisu2 and Grisu3, and the fraction of inputs for which Grisu3 reports failure
  - paper: doi:10.1145/3192366.3192369
    title: Ulf Adams, Ryu, fast float-to-string conversion, Proceedings of PLDI 2018, 270-282
    locator: the shortest round-trip conversion with precomputed powers of five and no fallback
  - paper: "David W. Matula, In-and-out conversions, Communications of the ACM 11(1) (1968), 47-50"
    title: David W. Matula, In-and-out conversions (1968)
    locator: the number of digits needed for a base conversion to be invertible
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Section 3.1.5, Conversions to and from string representations; Section 4.9, Radix Conversion (4.9.1 conditions on the formats, 4.9.2 conversion algorithms)
  - url: https://doi.org/10.1109/IEEESTD.2019.8766229
    title: IEEE Std 754-2019, IEEE Standard for Floating-Point Arithmetic
    locator: Clause 5.12, Details of conversion between floating-point data and external character sequences (5.12.2 and the requirement that enough digits recover the float)
---

Floating-point to decimal conversion takes a binary float and produces a decimal string. Three versions of the problem are common: print a given number of significant digits, correctly rounded (`printf("%.17g")`); print the shortest string that converts back to the same float (Python's `repr`, JavaScript's `Number.prototype.toString`); or print the exact value, which always has a finite decimal expansion. The shortest form was solved by Steele and White (1990) with [Dragon4](/dragon4/), and made fast by [Grisu](/grisu/) (Loitsch, 2010) and [Ryu](/ryu/) (Adams, 2018). The inverse problem is [decimal to floating-point](/decimal-to-floating-point/) conversion, and the two together give exact round trips.

## In plain words

A computer stores a number such as $0.1$ in base two, and the stored number is not exactly $0.1$: written out in full in base ten it has 55 digits. To show it to a person, the computer must choose how many digits to print.

Printing too few digits loses information: two different stored numbers can print the same. Printing all of them is exact but long and unhelpful. The usual choice is the shortest string that, when read back, gives exactly the same stored number. For the stored $0.1$, that string is "0.1". Finding the shortest string quickly and correctly for every number is the hard part.

## Definition

**Notation.** Binary64 with round to nearest, ties to even, $p = 53$; for a positive float $x$, $x^{-}$ and $x^{+}$ are its neighbors, and $\mathrm{ulp}$ is as in Muller et al., Section 2.3.2; see [floating-point arithmetic](/floating-point-arithmetic/) for the full notation.

**Input.** A finite float $x$ (sign, zero, infinities and NaN are handled separately).

**Output**, in one of three forms:

1. **Fixed precision.** For a given $k \ge 1$, the decimal $d \cdot 10^{e}$ with $10^{k-1} \le d < 10^{k}$ nearest to $x$ (ties to even), that is, $x$ correctly rounded to $k$ significant digits. Fixed-point formats (a given number of digits after the point) are the same with $e$ fixed.
2. **Shortest round trip.** The decimal $d \cdot 10^{e}$ with the fewest significant digits that lies in the rounding interval of $x$, the set of reals that round to $x$:
$$R(x) = \left[\tfrac{x^{-} + x}{2},\ \tfrac{x + x^{+}}{2}\right] \ \text{if the last bit of } x \text{ is } 0, \qquad \text{the open interval otherwise}.$$
Among several shortest candidates, the one nearest to $x$ is chosen (this is Steele and White's free-format output with the closest-digit rule; Ryu and Python's `repr` make the same choice).
3. **Exact.** All digits of $x$. Since $x = m \cdot 2^{q}$, with $q < 0$, equals $m \cdot 5^{-q} \cdot 10^{q}$, the expansion is finite.

## Variants

- **Bounded output length.** C's `printf` with a precision, and IEEE 754's requirement that conversions with enough digits be correctly rounded and recoverable (Clause 5.12.2).
- **Shortest without the nearest rule.** Any shortest string in $R(x)$; the strings can differ in the last digit, and the reading back still gives $x$.
- **Other formats.** binary32 needs at most $9$ digits for a round trip, binary128 at most $36$; [decimal floating-point](/decimal-floating-point/) formats need no conversion of base, only formatting of the coefficient.
- **Other output bases.** Hexadecimal output (`float.hex`) is exact and short, since $16$ is a power of $2$.

## Examples

Each line was produced by Python 3.14 (`repr` is shortest round trip; `%.17g` and `%.15g` are fixed precision) and checked with `decimal.Decimal(x)`, which gives the exact value.

| float | shortest (`repr`) | 17 digits | 15 digits |
|---|---|---|---|
| $\mathrm{fl}(0.1)$ | `0.1` | `0.10000000000000001` | `0.1` |
| $\mathrm{fl}(0.1) + \mathrm{fl}(0.2)$ | `0.30000000000000004` | `0.30000000000000004` | `0.3` |
| $\mathrm{fl}(1/3)$ | `0.3333333333333333` | `0.33333333333333331` | `0.333333333333333` |
| $\mathrm{fl}(10^{23})$ | `1e+23` | `9.9999999999999992e+22` | `1e+23` |
| $2^{63}$ | `9.223372036854776e+18` | `9.2233720368547758e+18` | `9.22337203685478e+18` |
| $2^{-1074}$ | `5e-324` | `4.9406564584124654e-324` | `4.94065645841247e-324` |
| largest finite | `1.7976931348623157e+308` | `1.7976931348623157e+308` | `1.79769313486232e+308` |

- **Exact values are long.** The stored $0.1$ is exactly $0.1000000000000000055511151231257827021181583404541015625$, with 55 significant digits; $2^{-1074}$ has 751 significant digits.
- **Fifteen digits are not enough.** `%.15g` prints $\mathrm{fl}(0.1) + \mathrm{fl}(0.2)$ as `0.3`, which reads back as a different float, $\mathrm{fl}(0.3)$.
- **Shortest is not "15 or 17".** `repr` prints $2^{63}$ with 16 digits and $2^{-1074}$ with 1. For $100000$ random binary64 bit patterns, the shortest output had 17 significant digits for $45.3\%$, 16 for $48.8\%$, 15 for $5.3\%$ and fewer for the rest.
- **Ties in fixed precision.** `'%.0f' % 0.5` is `0` and `'%.0f' % 2.5` is `2` (exact ties, to even), but `'%.2f' % 2.675` is `2.67`, because the stored value is $2.67499999999999982236\ldots$, not a tie.

## Known algorithms

- **Exact big-integer methods.** Write $x = m \cdot 2^{q}$ and generate digits of the fraction $m \cdot 2^{q}/10^{e}$ by repeated multiplication by $10$ and integer division, with [big integers](/big-integer/). Steele and White's FPP and [Dragon4](/dragon4/) do this, keeping the half-gaps $(x - x^{-})/2$ and $(x^{+} - x)/2$ scaled the same way, and stop at the first digit at which the output is inside $R(x)$; this gives the shortest output. The cost is a few big-integer operations per digit, with integers of up to about 1100 bits for binary64.
- **Gay's dtoa** (1990). The same problem with floating-point fast paths for common cases and big integers otherwise; modes for shortest and for a fixed number of digits. CPython's `repr` uses it.
- **[Grisu](/grisu/)** (Loitsch, 2010). Uses a 64-bit approximation of $x \cdot 10^{-k}$ from a table of cached powers of ten (a "do-it-yourself floating point" with 64-bit integers) and generates digits with integer arithmetic. Grisu3 gives the shortest output for about $99.5\%$ of binary64 inputs and detects the others, which then go to a big-integer method.
- **[Ryu](/ryu/)** (Adams, 2018). Computes the bounds of $R(x)$ scaled by a power of ten with 128-bit products against a table of powers of five, then removes trailing digits; it is shortest and correct for all inputs without a fallback. Schubfach (Giulietti) and Dragonbox (Jeon) are later methods of the same kind.
- **Fixed precision with big integers.** Compute $\lfloor x \cdot 10^{k - 1 - e}\rfloor$ and the remainder exactly and round; Ryu has a fixed-precision variant (Ryu printf) based on tables.

## Bounds

- **Seventeen digits suffice for binary64.** If $10^{k-1} > 2^{p}$, that is $k \ge 1 + \lceil p \log_{10} 2\rceil$, then two different floats always differ in their $k$-digit correct roundings, so $k$ digits always round trip; for $p = 53$ this gives $k = 17$ (Matula, 1968). For binary32 it gives $9$.
- **And are sometimes necessary.** The output for $\mathrm{fl}(0.1) + \mathrm{fl}(0.2)$ needs 17 digits, so no shorter fixed length works for all binary64 values.
- **Fifteen digits survive the other direction.** Any decimal with at most $15$ significant digits converts to binary64 and back to $15$ digits unchanged, since $10^{15} < 2^{52}$ (Muller et al., Section 4.9.1).
- **Exact output length.** The exact decimal value of a binary64 number has at most $767$ significant digits; the maximum is reached by subnormals and small normals such as $(2^{53} - 1)\,2^{-1074}$.
- **Cost.** Shortest output with table-based methods costs $O(1)$ word operations per conversion (a few 128-bit products and the digit loop), with tables of a few kilobytes; big-integer methods cost more for large and small exponents.

## Reductions

- **Shortest output to an interval problem.** Find the decimal with the fewest digits in $R(x)$, an interval whose endpoints are the midpoints to the neighbors. Scaling $R(x)$ by $10^{-e}$ for the right $e$ makes it a search for the integer with the most trailing zeros in an interval.
- **To [radix conversion](/radix-conversion/).** Exact output is base conversion of the integer $m \cdot 5^{-q}$, for $q < 0$, or of $m \cdot 2^{q}$.
- **Round-trip correctness.** The output of a shortest method is correct if and only if a correct [decimal to floating-point](/decimal-to-floating-point/) conversion returns $x$ and no shorter string does; this is how implementations are tested.

## Applications

- **Printing and serialization.** JSON, CSV and log files store floats as text; the [shortest round-trip representation](/shortest-round-trip-representation/) keeps the files short and the values exact. JavaScript, Python, Go, Rust and Java (since JDK 19) print shortest round-trip strings by default.
- **Debugging.** `repr` shows that $0.1 + 0.2$ is not $0.3$, which `%.15g` would hide.
- **Reproducible results.** A program that writes its floats with 17 digits or in shortest form can be restarted from its output with identical state.
- **Speed.** Conversion of numbers to text is a bottleneck in data-heavy programs, which is why Grisu and Ryu replaced big-integer methods in many runtimes.

## References
