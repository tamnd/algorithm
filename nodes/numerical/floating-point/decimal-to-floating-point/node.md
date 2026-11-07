---
tag: WDK18J
kind: problem
slug: decimal-to-floating-point
name: Decimal to floating-point conversion
aliases:
- string to float conversion
- correct decimal input
- strtod
area: numerical/floating-point
level: core
summary: Parse a decimal string into the correctly rounded binary float.
prereqs: [floating-point-arithmetic, round-to-nearest-even, radix-conversion]
see_also: [clinger-decimal-conversion, floating-point-to-decimal, shortest-round-trip-representation, decimal-floating-point, big-integer, subnormal-numbers, round-to-nearest-even, ieee-754]
sources:
  - paper: doi:10.1145/93542.93557
    title: William D. Clinger, How to read floating point numbers accurately, Proceedings of the ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI), 1990, 92-101
    locator: the fast path for short inputs, AlgorithmM with big integers, and the refinement AlgorithmR that starts from a floating-point approximation
  - paper: "David M. Gay, Correctly rounded binary-decimal and decimal-binary conversions, Numerical Analysis Manuscript 90-10, AT&T Bell Laboratories, 1990"
    title: David M. Gay, Correctly rounded binary-decimal and decimal-binary conversions (1990)
    locator: the decimal to binary algorithm of strtod in dtoa.c, with a floating-point first guess and a big-integer correction
  - paper: doi:10.1002/spe.2984
    title: Daniel Lemire, Number parsing at a gigabyte per second, Software, Practice and Experience 51(8) (2021), 1700-1727
    locator: the Eisel-Lemire algorithm (a 128-bit product with a table of powers of five, and the fallback when the result is too close to a midpoint)
  - url: https://doi.org/10.1109/IEEESTD.2019.8766229
    title: IEEE Std 754-2019, IEEE Standard for Floating-Point Arithmetic
    locator: Clause 5.12, Details of conversion between floating-point data and external character sequences (5.12.2, decimal character sequences for finite numbers, correct rounding)
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Section 3.1.5, Conversions to and from string representations; Section 4.9, Radix Conversion (4.9.1 conditions on the formats, 4.9.2 conversion algorithms)
---

Decimal to floating-point conversion takes a decimal string such as `0.1` or `6.02214076e23` and returns the binary float nearest to the exact value of the string. Most short inputs can be converted with one correctly rounded floating-point operation, but some need the exact comparison of the decimal value with a midpoint between two floats, and that comparison can need hundreds of digits. Clinger (1990) and Gay (1990) gave the first correct and fast algorithms; the Eisel-Lemire method (2020) is the fast method now used by many language runtimes. The inverse problem is [floating-point to decimal](/floating-point-to-decimal/) conversion.

## In plain words

A computer stores numbers in base two, and people write them in base ten. Most decimal numbers, even $0.1$, have no exact base-two form, so the computer must pick the nearest number it can store. Picking it is easy most of the time.

The hard cases are the numbers that lie almost exactly halfway between two numbers the computer can store. To decide which side they are on, the program may have to look at every digit of a very long input. A correct program must get these cases right too, or the same text can be read as two different numbers by two programs.

## Definition

**Notation.** Binary64 with round to nearest, ties to even, $p = 53$, $e_{\min} = -1022$, $e_{\max} = 1023$, and $\mathrm{fl}(\cdot)$ the rounded value; see [floating-point arithmetic](/floating-point-arithmetic/) for the full notation.

**Input.** A decimal string, which denotes a rational number $v = \pm\, d \cdot 10^{k}$, with $d$ a nonnegative integer (the digits, without the decimal point) and $k$ an integer (the exponent, adjusted for the position of the point). The string may have any number of digits.

**Output.** The float $\mathrm{fl}(v)$: the element of binary64 nearest to $v$, with ties to the float with an even last bit. If $|v| \ge (2 - 2^{-53})\,2^{1023}$ the result is $\pm\infty$ (overflow); if $|v|$ is below the normal range the result is the nearest [subnormal](/subnormal-numbers/) or $\pm 0$. The sign of a zero result is the sign of the string.

The output is a function of $v$ alone. IEEE 754 requires correct rounding for inputs up to a limit on the number of significant digits that is at least $20$ for binary64, and recommends it without a limit (Clause 5.12.2).

## Variants

- **Other rounding modes.** Round toward $0$, $+\infty$ or $-\infty$ under the current rounding attribute; the algorithms change only in the final decision.
- **Other formats.** binary32, binary16, [bfloat16](/bfloat16/) or binary128 as the target; the method is the same with different $p$ and exponent range.
- **Bounded input length.** If the input has at most $19$ significant digits, $d$ fits in a 64-bit integer, which many fast algorithms assume; longer inputs are truncated with a sticky flag and sent to a slow path when the truncation matters.
- **Hexadecimal input.** A string such as `0x1.999999999999ap-4` denotes a dyadic rational, and conversion is exact unless the string has more than $p$ bits; no big integers are needed.
- **Decimal targets.** Conversion to a [decimal floating-point](/decimal-floating-point/) format is a rounding of a decimal string to $p$ digits, with no change of base.

## Examples

Each input was converted with Python's `float()` (which is correctly rounded) and the result checked against the exact rational value with `fractions.Fraction`.

| input | result | bit pattern | remark |
|---|---|---|---|
| `0.1` | $0.1000000000000000055511\ldots$ | 0x3FB999999999999A | not exact; error $5.55 \times 10^{-18}$ |
| `9007199254740993` | $9007199254740992$ | 0x4340000000000000 | $2^{53} + 1$ is a tie; ties to even |
| `9007199254740993.0000000000000001` | $9007199254740994$ | 0x4340000000000001 | just above the tie; the last digit decides |
| `1e23` | $99999999999999991611392$ | 0x44B52D02C7E14AF6 | $10^{23}$ is not a float |
| `1.7976931348623158e308` | largest finite | 0x7FEFFFFFFFFFFFFF | below the overflow threshold |
| `1.7976931348623159e308` | $+\infty$ | 0x7FF0000000000000 | above $(2 - 2^{-53})2^{1023} = 1.7976931348623158079\ldots \times 10^{308}$ |
| `2.2250738585072011e-308` | largest subnormal | 0x000FFFFFFFFFFFFF | the input that hung PHP's parser in 2011 (Java's hung on the neighbor ending in 012) |
| `2.4703282292062328e-324` | $2^{-1074}$ | 0x0000000000000001 | just above half of the smallest subnormal |
| `2.4703282292062327e-324` | $0$ | 0x0000000000000000 | just below $2^{-1075} = 2.4703282292062327208\ldots \times 10^{-324}$ |

**The naive method is wrong.** Computing $d \cdot 10^{k}$ with floating-point operations, as `d * 10.0**k` or `d / 10.0**(-k)`, rounds more than once. In a test of $20000$ random inputs with $d < 10^{15}$ and $-40 \le k \le 40$, it gave a wrong result for $2758$ of them; for example `176600039647804e-26` gives $1.7660003964780398 \times 10^{-12}$ instead of $1.76600039647804 \times 10^{-12}$. The fast path below avoids this by restricting $d$ and $k$.

## Known algorithms

- **The fast path** (Clinger, 1990). If $d \le 2^{53}$ and $|k| \le 22$, then $d$ and $10^{|k|}$ are exact floats ($5^{22} < 2^{53}$), and $\mathrm{fl}(d \cdot 10^{k})$ or $\mathrm{fl}(d / 10^{-k})$ is one correctly rounded operation on exact operands, so it is the correct result. This is proved, assuming the floating-point unit rounds correctly to binary64 (no extended precision). A test of $20000$ random inputs in this range found no error, as it must. It covers most inputs met in practice.
- **[Clinger's AlgorithmM and AlgorithmR](/clinger-decimal-conversion/).** AlgorithmM computes the integer quotient of $d \cdot 10^{k}$ by a power of two with [big integers](/big-integer/) and rounds it; AlgorithmR starts from a floating-point approximation and corrects it by comparing $v$ with the midpoint above or below, exactly, with big integers.
- **Gay's strtod** (1990). A floating-point first guess, then a big-integer test of the error and a correction by one ulp; this is the `dtoa.c` code that CPython and many C libraries use.
- **Eisel-Lemire** (2020; Lemire, 2021). Multiply the 64-bit $d$ by a 128-bit approximation of $5^{k}$ from a table, take the leading bits, and round. If the discarded bits show that the result might be within the approximation error of a midpoint, fall back to a slow exact method; this is rare for random inputs. It is used by Go, Rust and others, and by `fast_float` in C++ (`std::from_chars`).
- **Exact rational rounding.** Form $v$ as a fraction $a/b$ of big integers, find the exponent $e$ with $2^{e} \le v < 2^{e+1}$, compute $q = \lfloor v \cdot 2^{p - 1 - e} \rfloor$ and the remainder, and round. This is simple and always correct, and it is the reference for testing the others; its cost grows with the length of the input and with $|k|$.

## Bounds

- **Digits that matter.** A midpoint between two adjacent binary64 numbers is an odd multiple of a power of two, so its decimal expansion is finite. In the binade $[2^{-1022}, 2^{-1021})$ the midpoints are $m \cdot 2^{-1075}$ with $m$ odd and $2^{53} < m < 2^{54}$, and they have $768$ significant decimal digits. An input that agrees with such a midpoint in its first $767$ digits cannot be rounded without reading the next one, so no algorithm can bound the number of digits it examines below that.
- **Cost.** For inputs of $n$ digits, the exact methods do a few multiplications and comparisons of big integers with $O(n + |k|)$ digits; the fast paths cost $O(n)$ to read the digits and $O(1)$ more.
- **Round trip.** $17$ significant decimal digits always identify a binary64 number uniquely, so the output of a correct conversion in the other direction with $17$ digits converts back to the same float; any decimal string of at most $15$ significant digits survives decimal to binary64 to decimal. These are the theorems of Matula and Goldberg for the base conversion (Muller et al., Section 4.9.1).

## Reductions

- **To a comparison with a midpoint.** Given a candidate float $f$ with $f \le v < f^{+}$, the correct result is decided by the sign of $v - (f + f^{+})/2$. With $v = d \cdot 10^{k}$ and the midpoint $m \cdot 2^{j}$, after multiplying both sides by the denominators this is a comparison of two big integers, so the problem reduces to one big-integer comparison once a candidate within one ulp is known.
- **To [radix conversion](/radix-conversion/).** In general, conversion from base $10$ to base $2$ with rounding to $p$ digits.
- **From the inverse problem.** A correct [floating-point to decimal](/floating-point-to-decimal/) conversion with enough digits, followed by this one, must return the original float; the pair is tested together in practice.

## Applications

- **Parsing text formats.** JSON, CSV and configuration files store numbers in decimal; a correct parser makes the same file give the same floats on every system. Parsing speed matters here, which is why the Eisel-Lemire method was adopted.
- **Compilers.** A floating-point literal in source code must become the same bit pattern on every compiler; C, Java and most languages require or recommend correct rounding.
- **Reproducibility.** A program that prints its floats with $17$ digits, or with the [shortest round-trip representation](/shortest-round-trip-representation/), can read them back exactly.
- **Security.** A parser that loops on hard inputs, as in the 2011 case above, is a denial-of-service bug.

## References
