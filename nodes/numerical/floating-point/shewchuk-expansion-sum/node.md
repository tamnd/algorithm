---
tag: A734Z5
kind: algorithm
slug: shewchuk-expansion-sum
name: Shewchuk expansion arithmetic
aliases:
- adaptive exact summation
- Priest arithmetic
- floating-point expansions
- Grow-Expansion
- msum
area: numerical/floating-point
level: research
summary: Represents results exactly as nonoverlapping expansions of floats, with adaptive precision.
model: floating-point-model
complexity:
  vars: {n: "the number of summands", m: "the largest length of the expansion, at most min(n, 2098) for binary64"}
  time: {worst: Θ(n·m), average: Θ(n·m), best: Θ(n)}
  space: {extra: Θ(m)}
properties: {deterministic: true, recursive: false, in_place: false}
history:
  year: 1997
  people: [Jonathan Richard Shewchuk, Douglas M. Priest]
  note: Priest introduced arbitrary-precision arithmetic on sums of floats in 1991. Shewchuk's 1997 paper gave the nonoverlapping expansions, Grow-Expansion and the adaptive geometric predicates, and Raymond Hettinger's 2005 recipe became Python's math.fsum.
prereqs: [two-sum, fast-two-sum, error-free-transformations]
see_also: [kahan-summation, neumaier-summation, kulisch-accumulator, reproducible-summation, double-double-arithmetic, floating-point-summation, orientation-test, accurate-dot-product]
sources:
  - paper: doi:10.1007/PL00009321
    title: Jonathan Richard Shewchuk, Adaptive precision floating-point arithmetic and fast robust geometric predicates, Discrete and Computational Geometry 18(3) (1997), 305-363
    locator: Section 2, arbitrary precision floating-point arithmetic (nonoverlapping expansions, Grow-Expansion with its Theorem 10, Expansion-Sum, Fast-Expansion-Sum, compression); Section 4, the adaptive orientation and incircle predicates
  - paper: doi:10.1109/ARITH.1991.145549
    title: Douglas M. Priest, Algorithms for arbitrary precision floating point arithmetic, 10th IEEE Symposium on Computer Arithmetic (ARITH 1991), 132-143
    locator: sums of floating-point numbers as an exact representation, and the renormalization of such sums
  - url: https://code.activestate.com/recipes/393090/
    title: Raymond Hettinger, Binary floating point summation accurate to full precision, Python Cookbook recipe 393090 (2005)
    locator: the msum loop that keeps a list of nonoverlapping partials, and the final correctly rounded sum
  - url: https://github.com/python/cpython/blob/main/Modules/mathmodule.c
    title: CPython, Modules/mathmodule.c, math_fsum
    locator: the partials loop, the handling of infinities, NaNs and intermediate overflow, and the half-way correction at the end
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Section 5.3, computing sums more accurately; Chapter 14, extending the precision (floating-point expansions)
---

Shewchuk's expansion arithmetic represents a real number exactly as an *expansion*, an unevaluated sum $e_1 + e_2 + \cdots + e_m$ of floats whose binary digits do not overlap, stored from the smallest component to the largest. Adding one float to an expansion takes one pass of [TwoSum](/two-sum/) through the components, and the result is again an exact nonoverlapping expansion. Summing a sequence this way gives its exact value. One more short pass rounds that value correctly. This is the algorithm behind Python's `math.fsum`. In Shewchuk's geometric predicates, the same expansions give exact answers at the cost of only as much precision as each input needs.

## In plain words

Picture a running total kept as a short stack of numbers, each one far smaller than the one above it, so that their digits never collide. To add a new number, you combine it with the smallest piece first. Whatever cannot be written exactly at that size is kept as a new small piece, and you move up. Nothing is ever thrown away, so the stack always holds the exact total. When you are done, you read off the total from the top piece down, and stop as soon as the remaining pieces are too small to change the rounded answer.

## The problem

Given floats $x_1, \ldots, x_n$, represent $S = \sum_i x_i$ exactly with floats only, and return $\mathrm{fl}(S)$, the correctly rounded value. The floats $x_i$ may cancel arbitrarily. For example, $10^{100} + 1 - 10^{100} = 1$, while recursive summation returns 0. [Kahan](/kahan-summation/) and [Neumaier](/neumaier-summation/) summation reduce the error, but they do not remove it. A [Kulisch accumulator](/kulisch-accumulator/) is exact, but it uses a 4288-bit register whatever the data. Expansions are exact and use only as many floats as the data needs.

**Definitions.** For a nonzero float $x$, let $\epsilon(x)$ be the value of its lowest nonzero bit, the largest power of two that divides $x$. Two floats $a$ and $b$ are *nonoverlapping* if one of them is zero or if $|a| < \epsilon(b)$ or $|b| < \epsilon(a)$. This means that the highest bit of the smaller one is below the lowest bit of the larger one. An *expansion* is a list $e_1, \ldots, e_m$ of nonzero floats with $|e_k| < \epsilon(e_{k+1})$ for each $k$. Its value is $\sum_k e_k$.

## The algorithm

```pseudo id=main
SHEWCHUK-SUM(x₁, …, xₙ)
L1  e ← ()                                      ▷ an expansion, smallest component first
L2  for i ← 1 to n
L3      Q ← x_i;  h ← ()
L4      for each component y of e, smallest first
L5          (Q, t) ← TWO-SUM(Q, y)              ▷ Q + t = old Q + y exactly
L6          if t ≠ 0 then append t to h
L7      if Q ≠ 0 then append Q to h;  e ← h     ▷ GROW-EXPANSION: Σe = x₁ + ⋯ + x_i exactly
L8  s ← e_m;  t ← 0;  j ← m                     ▷ round: start at the largest component
L9  while j > 1: j ← j − 1;  (s, t) ← FAST-TWO-SUM(s, e_j);  if t ≠ 0 then break
L10 if t ≠ 0 and j > 1 and sign(t) = sign(e_{j−1}) and fl(s + 2t) − s = 2t then s ← fl(s + 2t)
L11 return s
```

Lines L3 to L7 are Shewchuk's Grow-Expansion. Line L5 can also be written as a comparison followed by [Fast2Sum](/fast-two-sum/), which is what `math.fsum` does. Lines L8 to L11 round the expansion. They add components from the top down while the additions are exact. At the first inexact addition, the sum $s$ is the nearest float to the part seen so far, and the error $t$ is at least as large as everything below. The only remaining question is a tie. If $t$ is exactly half the gap to the next float in its direction, the components below decide which way to round, and line L10 moves $s$ one step when they push past the midpoint.

## Example

Sum $0.1 + 0.2 + 0.3$, where each constant means its binary64 value. Recursive summation gives $0.6000000000000001$.

| after adding | expansion (smallest first) |
|---|---|
| $0.1$ | `0x1.999999999999ap-4` |
| $0.2$ | `-0x1p-55`, `0x1.3333333333334p-2` |
| $0.3$ | `0x1p-55`, `0x1.3333333333333p-1` |

When $0.2$ is added, TwoSum rounds $0.1 + 0.2$ to $0.30000000000000004$ and keeps the error $-2^{-55}$. When $0.3$ is added, the error $-2^{-55}$ is combined first, as the smallest component, and the result is again exact. The final expansion says that the exact sum is $\mathrm{fl}(0.6) + 2^{-55}$. In the rounding pass, $\mathrm{fl}(0.6) + 2^{-55}$ rounds to $\mathrm{fl}(0.6)$ with $t = 2^{-55}$. That is not a tie, because half an ulp of $0.6$ is $2^{-54}$. So the result is $0.6$, the correctly rounded value.

A tie case: for $1 + 2^{-53} + 2^{-106}$ the expansion is $(2^{-106}, 2^{-53}, 1)$. In line L9, $1 + 2^{-53}$ is a tie and rounds to $1$ with $t = 2^{-53}$. The next component $2^{-106}$ has the same sign, and $1 + 2t = 1 + 2^{-52}$ is a float. So line L10 returns $1 + 2^{-52}$, which is correct because the exact sum lies just above the midpoint. Recursive summation returns $1$.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It assumes binary floating point with round to nearest, ties to even for the final result, and no overflow. It holds with underflow.

- **Exactness (proved).** TwoSum is exact, so each pass of L3 to L7 keeps $\sum e = x_1 + \cdots + x_i$.
- **Nonoverlap (proved).** Each $t$ in L5 is a multiple of the smaller of the lowest bits of its two inputs, and it is smaller than the lowest bit of the new $Q$. An induction on the components then shows that the output of Grow-Expansion is again an expansion. This is Shewchuk's Theorem 10, and it holds for any tie rule.
- **Correct rounding (proved).** In an expansion each component exceeds the sum of all smaller ones in magnitude. So the top-down additions in L9 have their larger operand first, which makes Fast2Sum exact. At the first nonzero error $t$, the rest $R$ of the expansion satisfies $|R| < \epsilon(e_j) \le |t|$, and $R$ has the sign of its top component. If $|t|$ is less than half the gap, $s$ is already $\mathrm{fl}(S)$. If $|t|$ is exactly half the gap, $R$ breaks the tie, and L10 performs the step exactly when it should.

## Complexity

Adding $x_i$ costs one TwoSum, which is 6 floating-point operations, per component of the current expansion. The rounding pass costs at most one Fast2Sum per component. The expansion length is the parameter that matters. Every component has its own range of bit positions, and binary64 has 2098 bit positions from $2^{-1074}$ to $2^{1023}$, so $m \le \min(n, 2098)$. On typical data $m$ stays small, often only a few components, so the cost is a small multiple of $n$. The worst case is $\Theta(nm)$, and the best case, with the expansion of length 1 throughout, is $\Theta(n)$. The extra space is the expansion, $\Theta(m)$.

## Properties

- **Exact.** The expansion is the exact sum, not an approximation, whatever the cancellation.
- **Correctly rounded and order independent.** The returned value is $\mathrm{fl}(S)$. It depends only on the multiset of inputs, so it is also reproducible.
- **Adaptive.** The cost grows with the spread of the data, not with the width of the format, unlike a [Kulisch accumulator](/kulisch-accumulator/).
- **Floats only.** It needs nothing but floating-point addition and comparison, with no integer tricks and no extended precision.
- **Sensitive to the arithmetic.** It needs correctly rounded binary addition in round to nearest. Double rounding on x87 or reassociation by the compiler breaks TwoSum, and with it everything else.

## Variants and improvements

- **Expansion-Sum and Fast-Expansion-Sum.** Shewchuk adds two expansions of lengths $m$ and $k$ by growing one with each component of the other, in $O(mk)$, or by merging them by magnitude and making one pass of TwoSum in $O(m + k)$. The second needs round to even for its nonoverlap guarantee.
- **Scale-Expansion.** Multiplies an expansion by a float, using [TwoProduct](/two-product/) on each component. With Expansion-Sum this gives exact products of expansions.
- **Compression.** Renormalize an expansion so that its largest component approximates the whole value to within one ulp. Then the top component alone is a good approximation.
- **Adaptive predicates.** Shewchuk's orientation and incircle tests compute a floating-point approximation, and an error bound for it, first. They extend to longer expansions only when the sign is uncertain. This makes exact [orientation tests](/orientation-test/) nearly as fast as plain floating point on typical inputs.
- **Fixed-length expansions.** [Double-double arithmetic](/double-double-arithmetic/) and quad-double arithmetic keep 2 or 4 components and drop the rest. That gives fixed extra precision instead of exactness.
- **Exponent bins.** Neal's superaccumulator and the [reproducible summation](/reproducible-summation/) methods replace the adaptive list with a fixed set of bins.

## When to use it

Use it when a sum must be correctly rounded, or exact for a decision, and the data does not justify a full long accumulator. Examples are `math.fsum`, exact geometric predicates, the residual computation in iterative refinement, and test oracles for other summation algorithms. For large vectors where speed matters more than the last bit, prefer [Kahan summation](/kahan-summation/) or a compensated sum such as Sum2.

## Pitfalls

- **Dropping zeros incorrectly.** Line L6 must drop zero errors. Otherwise the list grows needlessly, and the zero components break the nonoverlap test used by later steps.
- **Wrong order.** Grow-Expansion must visit components from smallest to largest, and the rounding pass from largest to smallest. Reversing either breaks the proofs.
- **Rounding by summing the components.** Adding up the components naively can be off in the last place. The half-way correction of L10 is needed.
- **Intermediate overflow.** A partial sum can overflow even when the final sum is finite, for example in $1.7 \times 10^{308} + 1.7 \times 10^{308} - 1.7 \times 10^{308}$. `math.fsum` raises `OverflowError` in this case, and so does the Python implementation here.
- **Python's built-in `sum`.** Since Python 3.12, `sum` of floats uses compensated summation, so it is no longer a plain recursive sum to compare against.

## Implementations

## History

Dekker (1971) and Knuth's TwoSum showed that the error of a floating-point addition is itself a float. Douglas Priest's 1991 paper and 1992 thesis built arbitrary-precision arithmetic on sums of floats, using a renormalization step to keep them well formed. Jonathan Shewchuk's 1997 paper introduced the nonoverlapping condition, proved that Grow-Expansion and Fast-Expansion-Sum preserve it, and used expansions to make Delaunay triangulation robust with adaptive predicates. Raymond Hettinger published the msum recipe in 2005. It combines Grow-Expansion with a correctly rounded final step, and it entered Python 2.6 as `math.fsum` in 2008.

## References
