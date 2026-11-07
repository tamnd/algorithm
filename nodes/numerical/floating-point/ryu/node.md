---
tag: JH77DH
kind: algorithm
slug: ryu
name: Ryu
aliases:
- Ryu printing
- Ryū
area: numerical/floating-point
level: advanced
summary: Always-correct shortest float printing using precomputed 128-bit multipliers.
model: floating-point-model
complexity:
  vars: {n: "the number of decimal digits of the output, at most 17 for binary64"}
  time: {worst: Θ(1), average: Θ(1), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, in_place: false}
history:
  year: 2018
  people: [Ulf Adams]
  note: Adams presented Ryu at PLDI 2018 as a fixed-width integer method for shortest output with no fallback path, faster than Grisu3 and Errol.
prereqs: [shortest-round-trip-representation, floating-point-to-decimal]
see_also: [grisu, dragon4, decimal-to-floating-point, round-to-nearest-even, ulp, ieee-754, clinger-decimal-conversion]
sources:
  - paper: doi:10.1145/3192366.3192369
    title: Ulf Adams, Ryū, fast float-to-string conversion, PLDI 2018, 270-282
    locator: Section 3, the algorithm in five steps (decoding, the rounding interval, conversion to a decimal power base with precomputed multipliers, the shortest representation, formatting), and the correctness argument for the 125-bit table entries
  - url: https://github.com/ulfjack/ryu
    title: Ulf Adams, Ryu reference implementation
    locator: ryu/d2s.c, the function d2d and the trailing-zero bookkeeping that this page follows
  - paper: doi:10.1145/3360595
    title: Ulf Adams, Ryū revisited, printf floating point conversion, Proceedings of the ACM on Programming Languages 3 (OOPSLA 2019), Article 169
    locator: the fixed-precision variant for %e and %f output
  - paper: doi:10.1145/93542.93559
    title: Guy L. Steele Jr. and Jon L. White, How to print floating-point numbers accurately, PLDI 1990, 112-126
    locator: the specification of shortest correctly rounded output (free-format printing)
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Section 4.9, radix conversion
  - url: https://ieeexplore.ieee.org/document/8766229
    title: IEEE Std 754-2019, IEEE Standard for Floating-Point Arithmetic
    locator: Clause 5.12.2, conversion of finite numbers to and from external decimal character sequences
---

Ryu turns a binary64 number into the shortest decimal string that reads back to the same number, choosing the closest such string when several have the same length. It computes the decimal digits of the two ends of the number's rounding interval at a scale where the shortest answer can be read off by dropping digits, and it gets those digits with one 64-by-128-bit multiplication by a precomputed power of 5 and a shift. Unlike [Grisu](/grisu/), it never needs a slow fallback, and unlike [Dragon4](/dragon4/) it uses no big integers. Adams showed in 2018 that the 125-bit table entries make every floor in the method exact for all binary64 inputs.

## In plain words

Every floating-point number owns a small stretch of the number line: all decimal values in that stretch read back as that number. The shortest way to print it is the decimal in the stretch with the fewest digits.

Ryu writes down both ends of the stretch and the number itself as long whole numbers of decimal digits, all with the same number of digits. It then chops the last digit off all three, over and over, for as long as the two ends still differ in what is left. When they would become equal it stops. What remains of the number itself, rounded using the last digit chopped, is the answer. The clever part is getting those long digit strings quickly: a lookup table of powers of five turns it into a single multiplication.

## The problem

**Notation.** binary64 with $p = 53$ and $[e_{\min}, e_{\max}] = [-1022, 1023]$, round to nearest, ties to even, for reading decimals back; $\mathrm{ulp}$ as in Muller et al., Section 2.3.2; see [floating-point arithmetic](/floating-point-arithmetic/). All arithmetic in the algorithm is on integers.

**Input.** A finite positive binary64 number $x$ (signs, zeros, infinities and NaNs are handled by the caller).

**Output.** Integers $d$ and $E$ with $d$ not divisible by 10, such that $d \cdot 10^E$ lies in the rounding interval $I_x$ of $x$, $d$ has the fewest digits among such decimals, and among those with that many digits $d \cdot 10^E$ is closest to $x$ (ties to an even $d$). The rounding interval $I_x$ runs from the midpoint with the predecessor of $x$ to the midpoint with its successor, and includes both ends exactly when the significand of $x$ is even; this is the [shortest round-trip representation](/shortest-round-trip-representation/).

## The algorithm

Write $x = m_2 \cdot 2^{e_2 + 2}$ with integer significand $m_2$, so that the three numbers $u \cdot 2^{e_2}$, $v \cdot 2^{e_2}$, $w \cdot 2^{e_2}$ with $u = 4m_2 - 1 - \sigma$, $v = 4m_2$, $w = 4m_2 + 2$ are the lower end of $I_x$, $x$ itself and the upper end. Here $\sigma = 0$ when $x$ is a power of two above the smallest normal, where the gap below is half the gap above, and $\sigma = 1$ otherwise.

```pseudo id=main
RYU(x)
L1  decode x into (m_2, e_2); u ← 4m_2 − 1 − σ, v ← 4m_2, w ← 4m_2 + 2; ends included iff m_2 even
L2  choose q and the starting decimal exponent E with 10^E ≤ 2^{e_2}/10 (or q = 0 when x · 10^{-E} is already an integer)
L3  (vm, vr, vp) ← (⌊u·2^{e_2}/10^E⌋, ⌊v·2^{e_2}/10^E⌋, ⌊w·2^{e_2}/10^E⌋), each by one multiply with a 125-bit table entry and a shift
L4  record whether u·2^{e_2}/10^E and v·2^{e_2}/10^E are integers (only possible for small q)
L5  if the upper end is excluded and w·2^{e_2}/10^E is an integer then vp ← vp − 1
L6  while ⌊vp/10⌋ > ⌊vm/10⌋ do: note whether the dropped digits of vm and vr are zero, keep the last dropped digit ℓ of vr, divide vm, vr, vp by 10, E ← E + 1
L7  if the lower end is included and is exactly vm · 10^E then keep dropping digits while vm mod 10 = 0
L8  if vr · 10^E is exactly halfway (ℓ = 5, all digits after it zero) and vr is even then ℓ ← 4
L9  d ← vr + 1 if ℓ ≥ 5 or (vr = vm and vm · 10^E is not in I_x), else d ← vr
L10 return (d, E)
```

Line L2 starts at a decimal scale fine enough that the rounding interval, at least $3 \cdot 2^{e_2}$ wide, spans at least 30 units, so the shortest output has at least one digit fewer than $vr$ and the loop runs at least once. Line L3 is the heart of the method: for $e_2 \ge 0$ the table holds $\lceil 2^k/5^q \rceil$, for $e_2 < 0$ it holds $5^{-e_2-q}$ truncated to 125 bits, and the floors come out exact. Lines L4, L5 and L7 handle the rare case where an end of the interval is itself a short decimal, and line L8 handles exact ties. The common case, where no end is a decimal of the current length, needs only lines L3, L6 and L9.

## Example

Take $x = 2^{-1017} \approx 7.120236347223045 \times 10^{-307}$, whose significand is even, so both ends of $I_x$ are included. Line L2 gives $E = -324$, and line L3 gives

| | $vm$ (lower end) | $vr$ ($x$) | $vp$ (upper end) |
|---|---|---|---|
| L3, $E = -324$ | 712023634722304403 | 712023634722304442 | 712023634722304521 |
| after 1 step, $E = -323$ | 71202363472230440 | 71202363472230444 | 71202363472230452 |
| after 2 steps, $E = -322$ | 7120236347223044 | 7120236347223044 | 7120236347223045 |

Now $\lfloor vp/10 \rfloor = \lfloor vm/10 \rfloor$ and the loop stops. The last dropped digit is $\ell = 4$, so plain rounding would keep $vr = 7120236347223044$. But $vr = vm$, and $vm \cdot 10^{-322}$ is below the true lower end, so line L9 takes $d = 7120236347223045$ and returns $7.120236347223045 \times 10^{-307}$, 16 digits. This is the case where printing $x$ correctly rounded to 16 significant digits, which gives $\ldots 044$, does not round-trip. For $x = 0.3$ the loop runs 17 times from $(299999999999999961, 299999999999999988, 300000000000000016)$ at $E = -18$ down to $(2, 2, 3)$ with $\ell = 9$, and returns $d = 3$, $E = -1$.

## Correctness

**Theorem.** Assume the three floors of line L3 are exact and the flags of lines L4, L5 and L7 record exactly whether the corresponding values are integers whenever that affects the output. Then RYU returns the shortest decimal in $I_x$, and the closest one to $x$ among the shortest, with ties to an even last digit.

*Proof sketch.* Let $k^\ast$ be the largest $k$ such that $I_x$ contains a multiple of $10^k$. The shortest decimals in $I_x$ are exactly the multiples of $10^{k^\ast}$ in $I_x$. Line L2 makes $10^E \le 2^{e_2}/10$, so $I_x$ spans more than 10 units of $10^E$ and $k^\ast > E$. At each step the loop condition holds exactly when the part of $I_x$ above the lower end contains a multiple of $10^{E+1}$, and line L7 covers the remaining case where the included lower end is itself that multiple; so the loops stop at $E = k^\ast$. At that scale the candidates are the integers in $I_x/10^{k^\ast}$, and the nearest to $x/10^{k^\ast} \in [vr, vr+1)$ is $vr$ or $vr + 1$; the last dropped digit and the zero flags decide which is nearer, and because the lower half of $I_x$ is never wider than the upper half, the chosen one lies in $I_x$. The full argument is in [the proof file](proofs/correctness.md).

**Proved, cited and observed.** The digit selection (lines L6 to L10) is proved here, given exact floors and flags. That 125-bit multipliers give exact floors for every binary64 input is Adams's result, established with a minimum-maximum search over all exponents (Adams 2018); the flag cutoffs ($q \le 21$ for $e_2 \ge 0$, $q < 63$ for $e_2 < 0$) follow the reference implementation. The tests check the floors in exact rationals for 1500 random inputs, compare with an exact brute-force reference on 800 random inputs and 946 edge cases, and compare with Python's `repr` on 25000 random bit patterns (seed 1); all agree.

## Complexity

$\Theta(1)$: one decode, three 64-by-128-bit multiplications, and at most about 17 rounds of the digit loop, each a few divisions by 10 of 64-bit integers (implementations remove two digits at a time with divisions by 100). The table needs 291 entries for $e_2 \ge 0$ and 326 for $e_2 < 0$, each stored in 128 bits, about 10 KB; a compact variant recomputes entries from a few stored ones.

## Properties

- **Always correct.** No input needs a fallback to big-integer arithmetic, unlike Grisu3.
- **Shortest and closest.** The output has the fewest digits that round-trip, and among those it is the nearest to $x$, so it matches Steele and White's free-format output and Python's `repr`.
- **Integer only.** No floating-point operation is used, so the result does not depend on the rounding mode or on FMA contraction.
- **Fixed work.** Running time is bounded by a small constant for every input.

## Variants and improvements

- **binary32.** The same method with 64-bit table entries and 32-bit significands; Adams checked it exhaustively over all $2^{32}$ inputs.
- **Ryu printf.** Adams's 2019 follow-up prints a fixed number of digits (the `%e` and `%f` formats) with the same multiply-and-shift idea.
- **Removing two digits at a time.** Dividing by 100 while possible halves the number of loop rounds in the common case.
- **Later methods.** Schubfach (Giulietti) and Dragonbox (Jeon) are later fixed-width methods that avoid most of the digit loop and are faster again; [Grisu](/grisu/) and [Dragon4](/dragon4/) are the earlier fast and exact methods.
- **Parsing.** The inverse problem, reading a decimal string correctly rounded, is [decimal-to-floating-point](/decimal-to-floating-point/) conversion; see also [Clinger's algorithm](/clinger-decimal-conversion/).

## When to use it

Use Ryu, or one of its successors, for any conversion of binary floating-point to text where the output must read back to the same value and should be as short as possible: JSON and other serialization, language `repr` or `toString` functions, logging and data exchange. For a fixed number of digits, use a correctly rounded fixed-precision method such as Ryu printf.

## Pitfalls

- **Rounding is not truncation.** Taking the right number of digits of $x$ correctly rounded does not always round-trip, as the example shows; the vr = vm check of line L9 is essential.
- **Boundary inclusion.** Ends of $I_x$ are included only for even significands, matching ties to even when reading back. A reader that rounds ties differently may read the output to a neighbour.
- **Asymmetric intervals.** At a power of two the gap below is half the gap above, which is the $\sigma = 0$ case; forgetting it gives outputs that read back to the predecessor.
- **Subnormals.** For subnormal $x$ the significand has no hidden bit and the exponent is fixed at the minimum; $5 \times 10^{-324}$ is the shortest output for the smallest subnormal.
- **Table generation.** The table entries must be computed exactly (ceilings for the inverse powers); an entry off by one breaks a small number of inputs that are hard to find by random testing.

## Implementations

## History

Steele and White specified shortest correctly rounded output in 1990 and gave Dragon4, which uses arbitrary-precision integers. Loitsch's Grisu (2010) used fixed-width integers but needed a fallback for about 0.5% of inputs in its exact variant Grisu3. Andrysco, Jhala and Lerner's Errol (2016) gave another fixed-width method. Ulf Adams's Ryu (PLDI 2018) was the first to combine fixed-width arithmetic with correctness for every input, with a proof that the table precision suffices. It was adopted in several language runtimes and libraries, including Microsoft's C++ standard library `to_chars`.

## References
