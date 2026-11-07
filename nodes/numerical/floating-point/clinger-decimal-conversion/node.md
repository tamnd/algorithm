---
tag: FZCTBB
kind: algorithm
slug: clinger-decimal-conversion
name: Clinger's correct decimal input
aliases:
- Clinger algorithm
- AlgorithmM
- Clinger's fast path
- How to read floating point numbers accurately
area: numerical/floating-point
level: advanced
summary: Converts decimal strings to correctly rounded floats using big-integer arithmetic when fast paths fail.
solves: [decimal-to-floating-point]
model: word-ram
complexity:
  vars: {n: "the number of decimal digits of f plus the size of the exponent e", M(n): the cost of multiplying two n-digit integers}
  time: {worst: O(n^2), average: O(n^2), best: O(1)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, in_place: false}
history:
  year: 1990
  people: [William D. Clinger]
  note: Clinger's PLDI 1990 paper, presented alongside Steele and White's paper on printing, gave the floating-point fast path, the exact AlgorithmM and the refinement AlgorithmR, and proved them correct.
prereqs: [decimal-to-floating-point, big-integer, round-to-nearest-even, floating-point-arithmetic]
see_also: [floating-point-to-decimal, dragon4, shortest-round-trip-representation, integer-division, subnormal-numbers, radix-conversion, double-rounding, ieee-754]
sources:
  - paper: doi:10.1145/93542.93557
    title: William D. Clinger, How to read floating point numbers accurately, Proceedings of the ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI), 1990, 92-101
    locator: the fast path for exact operands, AlgorithmM (exact division with a scaling loop), AlgorithmR (refinement of an approximation) and Bellerophon (extended precision with an error estimate and a fallback)
  - paper: "David M. Gay, Correctly rounded binary-decimal and decimal-binary conversions, Numerical Analysis Manuscript 90-10, AT&T Bell Laboratories, 1990"
    title: David M. Gay, Correctly rounded binary-decimal and decimal-binary conversions (1990)
    locator: strtod in dtoa.c, a floating-point first guess corrected by exact big-integer comparison with the midpoint
  - paper: doi:10.1002/spe.2984
    title: Daniel Lemire, Number parsing at a gigabyte per second, Software, Practice and Experience 51(8) (2021), 1700-1727
    locator: the Clinger fast path as the first test, the Eisel-Lemire 128-bit method, and the big-integer fallback
  - url: https://doi.org/10.1109/IEEESTD.2019.8766229
    title: IEEE Std 754-2019, IEEE Standard for Floating-Point Arithmetic
    locator: Clause 5.12.2, conversion of decimal character sequences with correct rounding; Clause 5.4.1, correctly rounded multiplication and division; Clause 7.4, overflow
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Section 4.9, Radix Conversion (4.9.2, conversion algorithms, including the decimal to binary direction)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, Addison-Wesley, 1997
    locator: Section 4.4, Radix Conversion (exact conversion of fractions with multiple-precision arithmetic)
---

Clinger's algorithm reads a decimal number $f \cdot 10^{e}$, with $f$ and $e$ integers, and returns the binary64 number nearest to it, ties to even. When $f < 2^{53}$ and $|e| \le 22$ both $f$ and $10^{|e|}$ are exact floats, and one IEEE multiplication or division gives the answer. Otherwise AlgorithmM forms the exact fraction $u/v = f \cdot 10^{e}$ with [big integers](/big-integer/), scales it by a power of two so that its integer part has exactly 53 binary digits, divides, and rounds by comparing twice the remainder with the divisor. The result is correct for every input, however many digits it has and however close it lies to a midpoint between two floats.

## In plain words

A program that reads "0.1" must find the stored binary number closest to one tenth. For short numbers there is a shortcut: the digits and the power of ten can both be stored exactly, and a single division by the machine is guaranteed to round correctly.

For long numbers or large exponents the shortcut can round twice and be off by one step. Then the algorithm writes the number as a fraction of two whole numbers, exactly, with as many digits as needed. It shifts the fraction until its whole part has the length of a stored number, divides, and looks at the remainder: less than half means round down, more than half means round up, and exactly half means pick the even neighbor. Whole-number arithmetic makes no rounding errors, so the answer is always right.

## The problem

**Notation.** Binary64 with round to nearest, ties to even: $p = 53$, $e_{\min} = -1022$, $e_{\max} = 1023$, $\mathrm{fl}(\cdot)$ for the rounded result, and $\mathrm{RN}$ for rounding to nearest even with the IEEE overflow rule; see [floating-point arithmetic](/floating-point-arithmetic/) for the full notation. The code writes $P$ for $p$, $K_{\min} = -1074$ for the exponent of the smallest subnormal $2^{-1074}$, and $K_{\max} = 1024 - 53 = 971$, so that the largest finite number is $(2^{53} - 1) 2^{971}$.

**Input.** Integers $f \ge 0$ and $e$, from a decimal string such as `-12.50e-3`, which a parser turns into $f = 1250$, $e = -5$ and a sign.

**Output.** $\mathrm{RN}(f \cdot 10^{e})$: the nearest binary64 number, the even one in a tie, $+\infty$ if the value rounds to $2^{1024}$ or more, and a subnormal or zero if it is below $2^{-1022}$. This is the correctly rounded conversion that IEEE 754-2019 Clause 5.12.2 requires and that C's `strtod` and Python's `float` provide; see [decimal to floating-point](/decimal-to-floating-point/) for the problem.

## The algorithm

```pseudo id=main
CLINGER-READ(f, e)                     ▷ integers f ≥ 0 and e; returns RN(f · 10^e) in binary64
L1  if f = 0 then return 0
L2  if f < 2^53 and |e| ≤ 22 then                   ▷ both operands are exact floats
L3      return fl(f · 10^e) if e ≥ 0, else fl(f / 10^(−e))   ▷ one IEEE operation
L4  (u, v) ← (f · 10^e, 1) if e ≥ 0, else (f, 10^(−e))       ▷ exact big integers, u/v = f · 10^e
L5  k ← len(u) − len(v) − 53                       ▷ len is the length in binary
L6  if ⌊u / (v · 2^k)⌋ ≥ 2^53 then k ← k + 1        ▷ now 2^52 ≤ u/(v · 2^k) < 2^53
L7  k ← max(k, −1074)                              ▷ subnormal results share the scale 2^(−1074)
L8  (q, r) ← divmod(u, v · 2^k)                    ▷ exact; shift u instead when k < 0
L9  if 2r > v · 2^k or (2r = v · 2^k and q is odd) then q ← q + 1   ▷ round half to even
L10 if q = 2^53 then (q, k) ← (2^52, k + 1); if k > 971 then return +∞, else return q · 2^k
```

The parser strips the sign, joins the digits before and after the point into $f$ and subtracts the number of digits after the point from the exponent; the sign is applied to the result, so `-0` gives $-0$.

Clinger's own AlgorithmM finds the scale with a loop that doubles $u$ or $v$ until the quotient has 53 binary digits; L5 and L6 replace that loop by an estimate from the lengths of $u$ and $v$, which is off by at most one.

## Example

Each value below was computed by the implementation and checked against Python's `float(s)` and against $\mathrm{RN}$ of the exact `Fraction`.

**$0.1$ on the slow path.** Forced through AlgorithmM: $u = 1$, $v = 10$, so $k = 1 - 4 - 53 = -56$ (L5). Then $\lfloor 2^{56}/10 \rfloor = 7205759403792793$, which lies in $[2^{52}, 2^{53})$, so L6 leaves $k$ alone. L8 gives $q = 7205759403792793$, $r = 6$; $2r = 12 > 10$, so L9 rounds up to $q = 7205759403792794$ = 0x1999999999999a. The result is $q \cdot 2^{-56}$ = 0x1.999999999999ap-4, the stored $0.1$. On the fast path the same value comes from one division, $1.0 / 10.0$.

**$10^{23}$, an exact tie.** Here $e = 23 > 22$, so the fast path is not allowed. $u = 10^{23}$ has length 77, so $k = 77 - 1 - 53 = 23$, and $\lfloor 10^{23}/2^{23} \rfloor = 11920928955078125 \ge 2^{53}$, so L6 sets $k = 24$. L8 gives $q = 5960464477539062$ and $r = 2^{23}$, exactly half of $2^{24}$: since $10^{23} = 2^{23} 5^{23}$ and $5^{23}$ is odd, $10^{23}$ is exactly a midpoint. $q$ is even, so L9 keeps it, and the result is $q \cdot 2^{24}$ = 0x1.52d02c7e14af6p+76, which prints as `1e+23`. A conversion that first rounds an approximation of $10^{23}$ and then decides can land on the other neighbor, which prints as `1.0000000000000001e+23`.

**Rounding twice.** For `3e23` the naive `3.0 * 1e23` multiplies by the already rounded $\mathrm{fl}(10^{23})$ and gives 0x1.fc3842bd1f071p+77, one unit below the correct 0x1.fc3842bd1f072p+77 that AlgorithmM returns. This is why the fast path stops at $10^{22}$.

**Extremes.** `9007199254740993` ($2^{53} + 1$) is a tie and goes down to $2^{53}$; `9007199254740995` goes up to $2^{53} + 4$. `1.7976931348623158e308` rounds to the largest finite number and `1.7976931348623159e308` to $+\infty$. `2.4703282292062327e-324`, just below $2^{-1075}$, gives $0$, and `2.4703282292062328e-324`, just above, gives $2^{-1074}$; here L7 clamps $k$ to $-1074$ and $q = 0$ rounds up to $1$.

## Correctness

The fast path is correct because both operands are exact: $f < 2^{53}$ is a float, and $10^{j} = 5^{j} 2^{j}$ with $5^{22} < 2^{53}$ is a float for $j \le 22$, so the single IEEE operation rounds the exact value once (IEEE 754-2019 Clause 5.4.1). For AlgorithmM, after L6 the scaled value $u/(v 2^{k})$ lies in $[2^{52}, 2^{53})$, so the two floats around $u/v$ are $q 2^{k}$ and $(q + 1) 2^{k}$, and L9 picks the nearer, or the even one in a tie, by an exact comparison of $2r$ with the divisor. When the result is subnormal, L7 moves the scale to $2^{-1074}$, the uniform spacing of the subnormals, and the same argument applies. The carry and the test $k > 971$ implement the overflow rule. The full proof is in `proofs/correctness.md`.

## Complexity

The fast path costs one floating-point operation after parsing. AlgorithmM works on integers of about $\log_2 f + 3.33|e|$ binary digits: it computes one power of ten, a constant number of shifts and comparisons, and two divisions (L6 and L8). The worst-case bound $O(n^{2})$ in the front matter assumes schoolbook division, and the best case $O(1)$ is the fast path. With schoolbook division the cost is quadratic in the number of digits $n$ of the input plus $|e|$; with fast division it is $O(M(n))$. For binary64, a reader can clamp: exponents above about $310$ plus the number of digits overflow, and exponents far below $-1075$ minus the number of digits underflow, so $|e|$ can be bounded before the big-integer work. Measured in CPython 3.14 on this machine (observed, not proved), the implementation took about $0.5$ microseconds for `12.345`, about $5$ microseconds for `12345e-300` and about $20$ microseconds for a 701-digit input.

## Properties

- **Exact.** Correct for every input length and exponent, with no tables and no assumptions about the inputs.
- **Two independent paths.** The fast path relies on IEEE rounding of one operation, AlgorithmM only on integer arithmetic; the tests check that they agree on every input where both apply.
- **Deterministic and nonrecursive.** A fixed sequence of steps; the only loop in Clinger's original, the scaling loop, is replaced here by L5 and L6.
- **Format-generic.** Changing $53$, $-1074$ and $971$ gives binary32 or binary128.

## Variants and improvements

- **AlgorithmR.** Clinger's refinement starts from a floating-point approximation $z$ and compares $f \cdot 10^{e}$ exactly with the midpoint between $z$ and a neighbor, moving $z$ by one ulp until it is correct; when $z$ is good, as it usually is, one big-integer comparison suffices.
- **Bellerophon.** Clinger's combination: try the fast path, else compute an approximation in extended precision with a bound on its error, and fall back to AlgorithmR only when the approximation is too close to a midpoint to decide.
- **Gay's strtod** (1990). A floating-point first guess, then an exact big-integer comparison of the input with the midpoint, as in AlgorithmR; the version in `dtoa.c` is used by many C libraries and by CPython.
- **The extended fast path.** If $e > 22$ but $f \cdot 10^{e - 22} < 2^{53}$, the product $f \cdot 10^{e - 22}$ is an exact integer float and one multiplication by $10^{22}$ still rounds once; for example `123e25`. Lemire's library tests this case too.
- **Eisel-Lemire** (2020, published by Lemire in 2021). Multiplies the 64-bit $f$ by a 128-bit truncated $5^{e}$ from a table and decides the rounding from the high part of the product; it fails only when the result is too close to a midpoint, and then falls back to a big-integer method. It is used in the standard libraries of Go and Rust and in several C++ libraries.
- **Long inputs.** A string with hundreds of digits can be truncated to about 768 significant digits plus a "nonzero digits follow" flag without changing the rounding, which bounds the size of the big integers.

## When to use it

Use the fast path whenever it applies; it covers most numbers written by people and by programs that print at most 15 digits with moderate exponents. Use AlgorithmM as the always-correct fallback, as a test oracle for faster methods, or alone when simplicity matters more than speed. A production reader puts Eisel-Lemire between the two, so that the big-integer path runs only for long or near-midpoint inputs.

## Pitfalls

- **Extending the fast path to $|e| > 22$.** $10^{23}$ is not a float, so $\mathrm{fl}(f \cdot \mathrm{fl}(10^{e}))$ rounds twice; `3e23` comes out one ulp low.
- **Double rounding in extended precision.** On x87 hardware with 64-bit internal precision even the fast path rounds first to 64 and then to 53 binary digits; the processor must be set to binary64 precision, or SSE2 used.
- **Midpoints need exact arithmetic.** An approximation with any fixed number of extra digits can fail for inputs that are close to a midpoint, and $10^{23}$ is exactly one; this caused wrong results in early C libraries.
- **Subnormals.** Without the clamp of L7, the quotient would keep 53 binary digits below $2^{-1022}$ and the result would be rounded twice, once by the algorithm and once by `ldexp`.
- **Huge exponents.** Computing $10^{|e|}$ for $e = 10^{9}$ is a denial-of-service risk; bound $e$ first, using the number of digits, since the result is then $0$ or $\infty$.

## Implementations

## History

Correct decimal input was required by the IEEE 754-1985 standard only within limits, and libraries of the 1980s often returned a neighbor of the correct float. In 1990 two papers at the same ACM PLDI conference settled both directions: Steele and White on printing ([Dragon4](/dragon4/)), and Clinger on reading, with the fast path, the exact AlgorithmM, the refinement AlgorithmR and the combined Bellerophon, and proofs of their correctness. In the same year Gay's technical report and his `dtoa.c` gave a widely used C implementation of both directions. The fast path survives as the first test in modern readers such as Lemire's fast_float (2021).

## References
