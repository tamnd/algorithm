---
tag: PHVDFD
kind: algorithm
slug: grisu
name: Grisu
aliases:
- Grisu3
- Grisu2
- Loitsch's algorithm
area: numerical/floating-point
level: advanced
summary: Fast shortest float printing using 64-bit integers, falling back to exact code when it cannot decide.
solves: [floating-point-to-decimal]
model: word-ram
complexity:
  vars: {n: "the number of digits produced (at most 17 for binary64)"}
  time: {worst: O(n), average: O(n), best: O(n)}
  space: {extra: O(1)}
properties: {deterministic: true, recursive: false, in_place: false}
history:
  year: 2010
  people: [Florian Loitsch]
  note: Loitsch presented Grisu, Grisu2 and Grisu3 at PLDI 2010; Grisu3 with a big-integer fallback became the number printer of the V8 JavaScript engine through the double-conversion library.
prereqs: [floating-point-to-decimal, dragon4, ulp, floating-point-arithmetic]
see_also: [ryu, dragon4, shortest-round-trip-representation, clinger-decimal-conversion, decimal-to-floating-point, double-double-arithmetic, round-to-nearest-even, subnormal-numbers]
sources:
  - paper: doi:10.1145/1806596.1806623
    title: Florian Loitsch, Printing floating-point numbers quickly and accurately with integers, Proceedings of PLDI 2010, 233-243
    locator: the do-it-yourself floating-point type, the cached powers of ten and the target exponent range, Grisu, Grisu2 (digit generation from the upper boundary), Grisu3 (the unsafe interval, round-weed and the failure report), and the measured failure rate of about 0.5 percent
  - url: https://github.com/google/double-conversion
    title: Google, double-conversion, the C++ library used by V8 for binary-decimal conversion
    locator: fast-dtoa.cc (Grisu3 with DigitGen and RoundWeed), cached-powers.cc (the table of 87 powers of ten), and bignum-dtoa.cc (the exact fallback)
  - paper: doi:10.1145/93542.93559
    title: Guy L. Steele Jr. and Jon L. White, How to print floating-point numbers accurately, Proceedings of PLDI 1990, 112-126
    locator: the free-format output that Grisu3 reproduces, and the Dragon4 fallback
  - paper: doi:10.1145/3192366.3192369
    title: Ulf Adams, Ryu, fast float-to-string conversion, Proceedings of PLDI 2018, 270-282
    locator: the comparison with Grisu3 and the method without a fallback
  - paper: doi:10.1145/2837614.2837654
    title: Marc Andrysco, Ranjit Jhala and Sorin Lerner, Printing floating-point numbers, a faster, always correct method, Proceedings of POPL 2016, 555-567
    locator: Errol, which replaces the 64-bit approximation by double-double arithmetic to avoid a fallback
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Section 4.9, Radix Conversion (4.9.2, conversion algorithms)
---

Grisu prints a binary64 number as the shortest decimal string that reads back to it, using only 64-bit integer arithmetic and a table of 87 cached powers of ten. It multiplies $x$ and the two ends of its rounding interval by a cached power $10^{K}$ chosen so that the products have a few integer digits, then produces digits from the upper end with shifts and divisions by powers of ten. Grisu3, the version on this page, keeps track of the error of the 64-bit products, accepts its answer only when it can prove that the answer is the shortest and the nearest, and otherwise reports failure, which happens for about $0.5\%$ of inputs; a big-integer method such as [Dragon4](/dragon4/) then handles them. On the inputs it accepts it is several times faster than Dragon4.

## In plain words

Printing a stored number in the shortest exact way needs care, and the careful methods use very long whole numbers, which are slow. Grisu does the same job with ordinary 64-bit numbers, which a processor handles in one step.

Ordinary numbers are not exact, so Grisu knows its answer could be slightly off. It keeps a small safety margin around everything it computes. If the answer is well inside the margin, it is guaranteed right and Grisu returns it. If the answer is too close to the edge to be sure, Grisu says so, and a slower exact method takes over. That happens for about one number in two hundred.

## The problem

**Notation.** Binary64 with round to nearest, ties to even, $p = 53$; for a finite $x > 0$, $x = f \cdot 2^{e}$, with neighbors $x^{\pm}$ and midpoints $M^{-} = (x^{-} + x)/2$, $M^{+} = (x + x^{+})/2$. The rounding interval $R$ has ends $M^{\pm}$, closed when $f$ is even. A "DIY float" is a pair $(f, e)$ of a 64-bit integer and an exponent with value $f \cdot 2^{e}$. See [floating-point arithmetic](/floating-point-arithmetic/) for the full notation.

**Input.** A finite float $x > 0$.

**Output.** Either digits $N$ and an exponent $t$ such that $y = N \cdot 10^{t}$ lies in $R$, no number with fewer significant digits lies in $R$, and $y$ is the nearest to $x$ among the numbers of its length in $R$; or "fail". The problem is shortest round-trip [floating-point to decimal](/floating-point-to-decimal/) conversion.

## The algorithm

```pseudo id=main
GRISU3(x)                                     ▷ x > 0 finite; 64-bit integers only
L1  (f, e) ← DECODE(x)                                         ▷ x = f · 2^e
L2  M+ ← (2f + 1) · 2^(e−1);  M− ← (2f − 1) · 2^(e−1), or (4f − 1) · 2^(e−2) below a power of two   ▷ exact
L3  pick a cached 10^K ≈ (c_f, c_e) with −60 ≤ e_w + c_e + 64 ≤ −32          ▷ table of 87 entries
L4  w ← ⌊x · c⌉;  high ← ⌊M+ · c⌉;  low ← ⌊M− · c⌉            ▷ upper 64 bits of 128-bit products; error < 1
L5  too_low ← low − 1;  too_high ← high + 1;  unsafe ← too_high − too_low   ▷ surely contains the scaled R
L6  produce decimal digits of too_high from the left: integer part, then fraction part ×10 per digit
L7      after each digit, rest ← too_high − (digits so far); stop when rest < unsafe   ▷ shortest length found
L8  while the candidate is above w + 1 and the next lower candidate is ≥ too_low and nearer to w + 1: decrement the last digit
L9  if the next lower candidate would be nearer to w − 1 (and ≥ too_low): return fail      ▷ nearest is ambiguous
L10 if 2 ≤ rest ≤ unsafe − 4 (in current units) return (digits, κ − K), else return fail   ▷ certainly inside R
```

The scaling makes the integer part of $\mathit{too\_high}$ fit in 32 bits (binary exponent between $-60$ and $-32$), so the integer digits come from 32-bit divisions and the fraction digits from multiplying by $10$ and shifting. In the fraction phase every quantity, including the error unit, is multiplied by $10$ at each digit, so all comparisons stay exact in integers. Grisu2 is L1 to L7 with the returned candidate taken as it is: always correct (it reads back to $x$) but not always shortest. The fallback in the implementation is an exact search with rationals; any exact shortest method works.

## Example

The values were computed by the implementation and checked with `fractions.Fraction`.

**$x = \mathrm{fl}(0.3)$.** $f = 5404319552844595$, $e = -54$. The cached power is $10^{4}$, exactly $\mathtt{0x9c40000000000000} \cdot 2^{-50}$, and the products have binary exponent $e_2 = -51$, so the unit is $2^{-51}$ and one is $2^{51}$. L4 gives $w = 6755399441055743750$, $\mathit{high} = 6755399441055744375$ and $\mathit{low} = 6755399441055743125$; so $\mathit{too\_high} = 3000 \cdot 2^{51} + 376$ and $\mathit{unsafe} = 1252$. The integer part of $\mathit{too\_high}$ is $3000$. After the first digit $3$, the rest is $376 < 1252$, so the length is one digit and the candidate is $3000 \cdot 2^{51}$, that is $0.3$. In L8 the candidate is above $w + 1$ ($\mathit{too\_high} - w = 626$, so it is $250$ units above $w$), but the next lower candidate, $2000 \cdot 2^{51}$, is far below $\mathit{too\_low}$, so nothing changes; L9 does not fire, and L10 accepts since $2 \le 376 \le 1248$. After the digit, $\kappa = 3$, so the output is `3` with exponent $\kappa - K = 3 - 4 = -1$, that is $3 \cdot 10^{-1}$.

**Failures.** For $\mathrm{fl}(10^{23})$, the shortest string `1e+23` is exactly $M^{+}$, the closed upper end of $R$; it lies in the band of width $2$ units next to $\mathit{too\_high}$ that the 64-bit computation cannot resolve, so L10 rejects it and the exact fallback prints `1e+23`. For $2^{50} + \tfrac14$, the two shortest candidates `...624.2` and `...624.3` are at exactly the same distance from $x$, so L9 cannot pick one and Grisu3 fails; the fallback picks the even digit.

**Rate.** For $30000$ random bit patterns with a fixed seed, Grisu3 failed on $0.5\%$ (the run in the tests); over $100000$ patterns the rate was $0.508\%$, in line with Loitsch's measurement. Every accepted result was identical to Python's `repr`, and a sample was checked exactly with rationals.

## Correctness

Each 64-bit product is within one unit of the exact scaled value: the cached power has error at most half a unit in its last place, and rounding the product adds at most half a unit. Widening the computed interval by one unit on each side therefore gives an "unsafe" interval that surely contains the scaled $R$, and shrinking by two units would give a "safe" interval surely inside it. Digit generation from the upper end of the unsafe interval stops at the coarsest power of ten that has a multiple in the unsafe interval; since that interval contains $R$, no shorter number is in $R$. The weeding step moves the candidate toward $w$ and returns it only if it is the nearest multiple for every possible position of the exact $w$ in $[w - 1, w + 1]$ and if it lies in the safe interval; then it is in $R$, as short as possible, and nearest. The full proof, including the fallback and the bound that all quantities stay below $2^{64}$, is in `proofs/correctness.md`.

## Complexity

Grisu3 does a table lookup, three 64 by 64 multiplications with 128-bit results, and one step per digit with a 32-bit division or a multiplication by $10$ and a shift: $O(n)$ word operations with $n \le 17$, and no memory allocation. The table has 87 entries of 10 bytes (a 64-bit significand and a 16-bit exponent). The fallback costs as much as a big-integer method on about $0.5\%$ of inputs. In C, Loitsch measured Grisu3 at several times the speed of Gay's dtoa; in the Python implementation here (observed, not proved) Grisu3 took about $5$ microseconds per number against about $16$ for the rational fallback.

## Properties

- **Certified or silent.** Grisu3 never returns a wrong answer; it returns the shortest, nearest digits or fails. Grisu2 never fails but is not always shortest; it always reads back to $x$.
- **Fixed size.** All arithmetic is on 64-bit integers, so it runs in constant memory and is easy to port.
- **Digits from the upper end.** Digits are generated from $\mathit{too\_high}$ downward, then adjusted toward $x$; Dragon4 generates digits of $x$ itself.
- **Ties are left to the fallback.** When two shortest candidates are equally near, or the shortest is exactly an end of $R$, Grisu3 fails, so the fallback decides the tie rule.

## Variants and improvements

- **Grisu (the first version).** Generates the digits of the scaled $x$ with enough extra precision that the output reads back correctly, without trying to be shortest.
- **Grisu2.** The version without weeding; it is always correct, gives the shortest string for most binary64 inputs, and needs no fallback. RapidJSON and other JSON libraries used it.
- **Grisu-Exact.** Junekey Jeon's variant, which makes the Grisu approach exact for every input by a more careful choice of the precision and the cached powers; it led to Dragonbox.
- **Errol** (Andrysco, Jhala and Lerner, 2016). Replaces the 64-bit approximations by [double-double](/double-double-arithmetic/) arithmetic and proves offline that no input needs a fallback.
- **[Ryu](/ryu/)** (Adams, 2018). Uses 128-bit products against a table of powers of five sized so that the scaled interval ends are always exact enough; it needs no fallback and is faster than Grisu3. Schubfach and Dragonbox are later methods of the same kind.

## When to use it

Use Grisu3 with an exact fallback when an implementation already exists, as in V8 and the double-conversion library. For new code, Ryu, Schubfach or Dragonbox are faster and need no fallback. Grisu2 is reasonable when the shortest string is a preference rather than a requirement, for example when writing logs.

## Pitfalls

- **Dropping the fallback.** Grisu3 alone fails on about one input in two hundred; returning its candidate anyway can print a string that is not shortest, or not nearest.
- **The lower boundary below powers of two.** As in every shortest printer, $M^{-}$ is closer below a power of two; using the symmetric formula prints some powers of two wrongly.
- **Error accounting.** The margins of one unit per product, and two and four units in the final test, come from the error analysis; tightening them without a proof gives rare wrong outputs.
- **Overflow of 64-bit quantities.** The choice of the target exponent range keeps every quantity below $2^{64}$; a different range needs the analysis redone.
- **Table generation.** The cached powers must be the correctly rounded 64-bit significands of $10^{K}$; a table computed with floating-point arithmetic is wrong for large $|K|$.

## Implementations

## History

Before 2010, correct shortest printing meant Steele and White's Dragon4 or Gay's dtoa, both with big integers. Florian Loitsch's PLDI 2010 paper showed how far 64-bit integers go: Grisu with extra precision, Grisu2 for nearly shortest output, and Grisu3 with a proof that its accepted results are optimal and a measured failure rate of about $0.5\%$. The V8 JavaScript engine adopted Grisu3 with a big-integer fallback through Google's double-conversion library, and other runtimes followed. Errol (2016) and Ryu (2018) then removed the need for a fallback.

## References
