---
tag: 17AMFE
kind: algorithm
slug: dragon4
name: Dragon4 (Steele-White)
aliases:
- Steele-White algorithm
- Steele and White free-format printing
- Dragon4 free-format algorithm
- Burger-Dybvig free-format printing
area: numerical/floating-point
level: advanced
summary: Exact big-integer digit generation for shortest float printing.
solves: [floating-point-to-decimal]
model: word-ram
complexity:
  vars: {n: "the number of digits produced (at most 17 for binary64)", L: the length of the scaled integers in machine words}
  time: {worst: O(L^2 + n L), average: O(L^2 + n L), best: O(n L)}
  space: {extra: O(L)}
properties: {deterministic: true, recursive: false, in_place: false}
history:
  year: 1990
  people: [Guy L. Steele Jr., Jon L. White]
  note: Steele and White published FPP and Dragon4 at PLDI 1990, years after the work on printing in Lisp systems at MIT; Burger and Dybvig (1996) gave the simplified formulation with integer setup by cases and a fast exponent estimate.
prereqs: [floating-point-to-decimal, big-integer, ulp, floating-point-arithmetic]
see_also: [grisu, ryu, shortest-round-trip-representation, clinger-decimal-conversion, decimal-to-floating-point, radix-conversion, round-to-nearest-even, subnormal-numbers]
sources:
  - paper: doi:10.1145/93542.93559
    title: Guy L. Steele Jr. and Jon L. White, How to print floating-point numbers accurately, Proceedings of the ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI), 1990, 112-126
    locator: the algorithms FPP and Dragon4, free-format and fixed-format output, and the termination conditions on the remainder and the scaled gaps
  - paper: doi:10.1145/231379.231397
    title: Robert G. Burger and R. Kent Dybvig, Printing floating-point numbers quickly and accurately, Proceedings of PLDI 1996, 108-116
    locator: the free-format algorithm with exact integers, the four setup cases for r, s, m+ and m-, and the estimate of the decimal exponent
  - paper: "David M. Gay, Correctly rounded binary-decimal and decimal-binary conversions, Numerical Analysis Manuscript 90-10, AT&T Bell Laboratories, 1990"
    title: David M. Gay, Correctly rounded binary-decimal and decimal-binary conversions (1990)
    locator: dtoa mode 0 (shortest round trip), with floating-point fast paths in front of the big-integer digit loop
  - paper: doi:10.1145/1806596.1806623
    title: Florian Loitsch, Printing floating-point numbers quickly and accurately with integers, Proceedings of PLDI 2010, 233-243
    locator: the comparison with Dragon4 and its use as the fallback of Grisu3
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Section 4.9, Radix Conversion (4.9.1 conditions on the formats, 4.9.2 conversion algorithms)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, Addison-Wesley, 1997
    locator: Section 4.4, Radix Conversion (conversion of fractions by repeated multiplication with exact arithmetic)
---

Dragon4 prints a binary float $x$ as the shortest decimal string that reads back to $x$, and among the shortest strings the one nearest to $x$. It writes $x$ and the half-gaps to its two neighbors as fractions $r/s$, $m^{+}/s$ and $m^{-}/s$ with exact [big integers](/big-integer/), scales them by the right power of ten, and produces digits by multiplying by ten and dividing, stopping at the first digit at which the truncated or the incremented number lies in the rounding interval of $x$. Because every step is exact, the result is correct for every float, including subnormals, powers of two and the largest finite number. Faster methods such as [Grisu](/grisu/) and [Ryu](/ryu/) give the same output; Grisu3 uses Dragon4 as its fallback.

## In plain words

Each stored binary number stands for a small range of real numbers: everything that would be rounded to it when read. To print the number, we want the shortest decimal that falls in that range, so that reading it back gives the same stored number.

Dragon4 produces the decimal digits one at a time, from the left, the way long division does, with whole numbers so that nothing is rounded along the way. After each digit it asks two questions: if I stop here, is the number I have printed inside the range? And if I stop here but add one to the last digit, is that inside? As soon as one answer is yes, it stops. If both are yes, it picks whichever is closer to the stored number.

## The problem

**Notation.** Binary64 with round to nearest, ties to even, $p = 53$; for a finite $x > 0$, $x = m \cdot 2^{q}$ with integers $m < 2^{53}$ and $q \ge -1074$, and $x^{-}$, $x^{+}$ are the neighbors of $x$ (with $x^{+} = 2^{1024}$ for the largest finite number). The half-gaps are $g^{-} = (x - x^{-})/2$ and $g^{+} = (x^{+} - x)/2$; they are $\tfrac12\mathrm{ulp}(x)$, with the ulp of Muller et al., Section 2.3.2, except below a power of two, where $g^{-} = g^{+}/2$. See [floating-point arithmetic](/floating-point-arithmetic/) for the full notation.

**Input.** A finite float $x > 0$. Zero, the sign, infinities and NaN are handled by the caller.

**Output.** Digits $d_1 d_2 \ldots d_n$ and an exponent $k$, meaning $y = 0.d_1 d_2 \ldots d_n \times 10^{k}$, such that $y$ lies in the rounding interval $R = [x - g^{-}, x + g^{+}]$ (closed when $m$ is even, open when $m$ is odd, matching a reader that rounds ties to even), $n$ is as small as possible, and $y$ is the nearest to $x$ among the $n$-digit numbers in $R$, ties to an even last digit. This is the free-format output of Steele and White and the output of Python's `repr`; see [floating-point to decimal](/floating-point-to-decimal/) for the problem.

## The algorithm

```pseudo id=main
DRAGON4(x)                                     ▷ x > 0 finite; output 0.d1 d2 ... dn × 10^k
L1  (m, q) ← DECOMPOSE(x);  incl ← (m is even)            ▷ x = m · 2^q exactly
L2  set integers r, s, m+, m− with r/s = x, m+/s = g+, m−/s = g−   ▷ four cases: q ≥ 0 or not, power of two or not
L3  k ← ⌊e2 · 0.30103⌋ − 1 where 2^e2 ≤ x < 2^(e2+1); scale s by 10^k (or r, m+, m− by 10^(−k))
L4  while r + m+ > s, or (incl and r + m+ = s):  s ← 10 s;  k ← k + 1   ▷ now R lies below 10^k
L5  loop:  r ← 10 r;  m+ ← 10 m+;  m− ← 10 m−
L6      d ← ⌊r / s⌋;  r ← r mod s                              ▷ next digit and remainder
L7      low ← r < m− (or ≤ if incl);  high ← r + m+ > s (or ≥ if incl)
L8      if not low and not high then emit d and repeat the loop
L9      if low and high then d ← d + 1 when 2r > s, or 2r = s and d is odd;  else if high then d ← d + 1
L10     emit d and return the digits and k
```

The four cases of L2 (Burger and Dybvig's table) are: for $q \ge 0$, $(r, s, m^{+}, m^{-}) = (2m2^{q}, 2, 2^{q}, 2^{q})$, or $(4m2^{q}, 4, 2^{q+1}, 2^{q})$ when $m = 2^{52}$; for $q < 0$, $(2m, 2^{1-q}, 1, 1)$, or $(4m, 2^{2-q}, 2, 1)$ when $m = 2^{52}$ and $q > -1074$. The factor $2$ or $4$ keeps the half-gaps integral.

## Example

The traces were computed by the implementation and checked with `fractions.Fraction`.

**$x = \mathrm{fl}(0.3)$.** Here $m = 5404319552844595$ = 0x13333333333333 (odd, so $R$ is open), $q = -54$, and $x = 0.299999999999999988897769753748\ldots$. L2 gives $r = 2m$, $s = 2^{55}$, $m^{\pm} = 1$. With $e_2 = -2$, L3 estimates $k = \lfloor -0.60206 \rfloor - 1 = -2$ and multiplies $r$ and $m^{\pm}$ by $100$. L4 runs twice: $(r + m^{+})/s \approx 30$ and then $3$ exceed $1$, so $k$ becomes $0$, and now $(r + m^{+})/s \approx 0.3 < 1$. In the first pass of the loop, L6 gives $d = 2$ with $r/s = 0.99999999999999988898\ldots$ and $m^{\pm}/s = 2.776 \times 10^{-16}$. `low` is false ($0.2$ is far below $x$), but `high` is true: $r/s + m^{+}/s > 1$, that is $0.3 < x + g^{+}$. L9 increments $d$, and the output is the digit `3` with $k = 0$, that is $0.3$. The first digit computed was $2$; the termination test is what turns it into the shortest answer.

**A tie between two shortest strings.** For $x = 2^{50} + \tfrac14 = 1125899906842624.25$ (exactly), the gaps are $\tfrac18$ on each side and $m$ is odd. No 16-digit decimal ($\ldots 624$ or $\ldots 625$) is inside $R = (\ldots 624.125, \ldots 624.375)$, so 17 digits are needed, and both $\ldots 624.2$ and $\ldots 624.3$ are inside, at distance $0.05$ each. Here $2r = s$, $d = 2$ is even, and Dragon4 prints `1125899906842624.2`, as `repr` does; $2^{50} + \tfrac34$ prints as `...624.8`.

**Edge cases.** $2^{-1074}$ prints as `5e-324`: its rounding interval $(2.47, 7.41) \times 10^{-324}$ contains five one-digit numbers and $5$ is the nearest. $\mathrm{fl}(10^{23})$ prints as `1e+23` because $10^{23}$ lies on the closed end of its interval (it is exactly the midpoint to the neighbor, and $m$ is even). The largest finite number prints as `1.7976931348623157e+308`, with the upper gap measured to $2^{1024}$.

For $20000$ random bit patterns (fixed seed) and all subnormals $m \cdot 2^{-1074}$ with $m < 3000$, the output formatted in the style of `repr` was identical to Python's `repr`.

## Correctness

Three facts make it work. First, the setup is exact: $r/s = x$ and $m^{\pm}/s$ are the half-gaps, and after the scaling of L3 and L4 every number in the rounding interval $R$ is below $10^{k}$, with $k$ the least such exponent. Second, the loop keeps the invariant $x \cdot 10^{j - k} = D_{j} + r/s$, where $D_{j}$ is the integer formed by the first $j$ digits, and the gaps are scaled the same way; so `low` says that the truncation $D_{j} 10^{k - j}$ is in $R$ and `high` says that $(D_{j} + 1)10^{k - j}$ is in $R$. Third, $R$ contains a number with at most $j$ significant digits exactly when it contains one of these two multiples of $10^{k-j}$, since $R$ is an interval around $x$ below $10^{k}$. Hence the loop stops at the shortest length, the output lies in $R$, and the comparison of $2r$ with $s$ picks the nearest candidate. A subtle case is the subnormal $2 \cdot 2^{-1074}$, whose interval straddles $10^{-323}$; it is handled there. The full proof is in `proofs/correctness.md`.

## Complexity

The integers have at most about $1100$ binary digits for binary64 (for $q$ near $-1074$, $s \approx 2^{1075}$, and for $x$ near the top, $r \approx 2^{1025}$), so $L \le 18$ words of 64 binary digits. Computing $10^{|k|}$ and scaling costs $O(L^{2})$ with schoolbook multiplication. Each digit costs a multiplication by $10$ of three integers and a division whose quotient is a single digit, which is $O(L)$; at most $17$ digits are produced. In CPython 3.14 (observed, not proved) the implementation took about $3$ to $5$ microseconds per number, roughly ten times slower than the C code behind `repr`.

## Properties

- **Exact.** No floating-point operation after L1, so the result is independent of the machine's rounding mode and extended precision.
- **Shortest and nearest.** The output is the free-format output of Steele and White; with ties to even, it equals Python's `repr`, JavaScript's `Number.prototype.toString` digits, and the output of Ryu.
- **Left to right.** Digits come out one at a time, so the loop can stop early or feed a fixed-format variant.
- **Format-generic.** Changing $p$, the minimal exponent and the base handles binary32, binary128 and other radices.

## Variants and improvements

- **Fixed-format output.** Steele and White's fixed-format mode stops at a given digit position and rounds the last digit correctly; `printf("%.17g")` and Python's `'%.17g'` need this mode. Gay's dtoa has both modes.
- **FPP and (FP)³.** Steele and White's paper builds Dragon4 in steps from the fixed-point printer FPP, through a floating-point version, to the free-format Dragon4.
- **Burger and Dybvig (1996).** The formulation used here: integer setup by four cases, and an estimate $k \approx \lceil \log_{10} x \rceil$ from the exponent, which removes Dragon4's loop of repeated scaling by ten; they also treat readers whose rule for ties is unknown, by using the open interval.
- **Gay's dtoa** (1990). Fast paths in floating-point arithmetic when they are provably safe, and the big-integer loop otherwise; it was the standard C implementation for two decades and is used in CPython.
- **Grisu, Ryu, Schubfach, Dragonbox.** Table-based methods with 64-bit or 128-bit integers that avoid big integers. [Grisu3](/grisu/) falls back to Dragon4 for about $0.5\%$ of inputs; [Ryu](/ryu/) needs no fallback.

## When to use it

Use Dragon4 when correctness and simplicity matter more than speed: as the reference implementation that tests faster printers, as the fallback behind Grisu, for unusual formats or radices without precomputed tables, and for fixed-format output with many digits. When printing speed matters, as in JSON serialization, use Ryu or a similar table-based method.

## Pitfalls

- **The asymmetric gap.** Below a power of two the lower neighbor is twice as close; using the same gap on both sides makes $2^{64}$ print as `1.844674407370955e+19`, which reads back as its lower neighbor; with that bug, 255 of the 2045 normal powers of two from $2^{-1021}$ to $2^{1023}$ print wrongly.
- **Open or closed interval.** The ends of $R$ belong to it only when $m$ is even; using the closed interval for odd $m$ prints strings that read back to the neighbor.
- **The exponent estimate.** A floating-point $\log_{10}$ can be off near powers of ten; the estimate must be provably not too high, or the first digit can be zero, and a fixup loop like L4 must follow.
- **Performance of big integers.** Scaling by $10^{300}$ is slow in a naive implementation; precomputed powers or a faster method are worth it in hot paths.
- **Subnormals.** Their interval is wide in relative terms and can straddle a power of ten (as for $2 \cdot 2^{-1074}$); testing only normal numbers misses this.

## Implementations

## History

Printing floats correctly was a known problem in Lisp systems, whose readers and printers had to agree; Jon L White worked on it for MacLisp at MIT in the 1970s, and Steele and White's paper at PLDI 1990, which had circulated in draft for years, gave the first published algorithms with proofs: FPP for fixed point and Dragon4 for free-format floating point. Clinger's paper on the reverse direction, [reading](/clinger-decimal-conversion/), appeared in the same proceedings, and Gay's dtoa followed the same year. Burger and Dybvig (1996) simplified and sped up the free-format algorithm. Loitsch's Grisu (2010) and Adams's Ryu (2018) replaced big integers in most runtimes, but Dragon4 remains the reference.

## References
