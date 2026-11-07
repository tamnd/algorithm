---
tag: FP385Q
kind: algorithm
slug: two-sum
name: TwoSum (Knuth)
aliases:
- Knuth's TwoSum
- 2Sum
- Moller-Knuth TwoSum
area: numerical/floating-point
level: advanced
summary: Computes s = fl(a+b) and the exact error of the addition in six floating-point operations.
model: floating-point-model
complexity:
  vars: {n: "the number of calls (each call is one addition, a fixed amount of work)"}
  time: {worst: Θ(1), average: Θ(1), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, in_place: false}
history:
  year: 1965
  people: [Ole Møller, Donald E. Knuth]
  note: Møller described the six-operation error computation in BIT in 1965; Knuth proved it for binary round to nearest in TAOCP Volume 2.
prereqs: [error-free-transformations, fast-two-sum]
see_also: [two-product, kahan-summation, neumaier-summation, double-double-arithmetic, shewchuk-expansion-sum, sterbenz-lemma, accurate-dot-product, floating-point-summation]
sources:
  - paper: "Ole Møller, Quasi double-precision in floating point addition, BIT Numerical Mathematics 5 (1965), 37-50"
    title: Ole Møller, Quasi double-precision in floating point addition
    locator: the computation of the rounding error of a sum without comparing the operands
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, Addison-Wesley, 1998
    locator: Section 4.2.2, Accuracy of floating point arithmetic (Theorem B, the exact error of a rounded sum, and its proof)
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Section 4.3.2, The 2Sum algorithm (the algorithm, its correctness theorem, and the optimality of six operations)
  - paper: doi:10.1137/030601818
    title: Takeshi Ogita, Siegfried M. Rump and Shin'ichi Oishi, Accurate sum and dot product, SIAM Journal on Scientific Computing 26(6) (2005), 1955-1988
    locator: Algorithm 3.1 (TwoSum) and its use in Sum2 and Dot2
  - paper: "Sylvie Boldo, Stef Graillat and Jean-Michel Muller, On the robustness of the 2Sum and Fast2Sum algorithms, ACM Transactions on Mathematical Software 44(1) (2017)"
    title: Sylvie Boldo, Stef Graillat and Jean-Michel Muller, On the robustness of the 2Sum and Fast2Sum algorithms
    locator: the behaviour under overflow, directed rounding and underflow
---

TwoSum computes the rounded sum $s = \mathrm{fl}(a + b)$ of two floats together with its exact rounding error $t = (a + b) - s$, using six floating-point additions and subtractions and no comparison. It is exact for all finite $a$ and $b$ in binary arithmetic with round to nearest, provided no operation overflows. It is the branch-free [error-free transformation](/error-free-transformations/) of addition, and it is the basic step of compensated summation, [double-double arithmetic](/double-double-arithmetic/) and [expansion arithmetic](/shewchuk-expansion-sum/).

## In plain words

When two numbers are added on a computer, the result is rounded, and a small piece of the true sum is lost. TwoSum finds that lost piece exactly.

It first adds the numbers as usual. Then it asks how much of each input actually made it into the result: subtracting one input from the result estimates the other, and subtracting that estimate from the result estimates the first. Each estimate differs from the real input by a little, and those two little differences, added together, are exactly the piece that was lost. Unlike the faster [Fast2Sum](/fast-two-sum/), it works no matter which input is bigger.

## The problem

**Notation.** A binary floating-point system with precision $p$ and minimal exponent $e_{\min}$ (binary64 by default, $p = 53$, $e_{\min} = -1022$), round to nearest with any symmetric tie rule (ties to even by default), unit roundoff $u = 2^{-p}$, $\mathrm{fl}(\cdot)$ for the rounded result and $\mathrm{ulp}$ as in Muller et al., Section 2.3.2; see [floating-point arithmetic](/floating-point-arithmetic/). The [standard model](/floating-point-model/) $\mathrm{fl}(a \pm b) = (a \pm b)(1 + \delta)$, $|\delta| \le u$, holds without overflow.

**Input.** Two finite floats $a$ and $b$.

**Output.** Floats $s$ and $t$ with $s = \mathrm{fl}(a + b)$ and $s + t = a + b$ exactly; moreover $|t| \le \tfrac12\mathrm{ulp}(s) \le u|s|$.

## The algorithm

```pseudo id=main
TWO-SUM(a, b)
L1  s  ← fl(a + b)
L2  a′ ← fl(s − b)                     ▷ the part of s that came from a
L3  b′ ← fl(s − a′)                    ▷ the part of s that came from b
L4  δa ← fl(a − a′)                    ▷ what a lost
L5  δb ← fl(b − b′)                    ▷ what b lost
L6  t  ← fl(δa + δb)
L7  return (s, t)
```

Lines L2 and L3 split $s$ into a part attributed to $a$ and a part attributed to $b$, with $a' + b' = s$ exactly. Lines L4 and L5 measure how far each part is from its input, and line L6 adds the two shortfalls. The theorem below shows that lines L3 to L6 are all exact; only lines L1 and L2 round.

## Example

Each row was run with Python floats (binary64) and checked with `fractions.Fraction`: in every row $s + t = a + b$ exactly.

| $a$ | $b$ | $s$ | $a'$ | $b'$ | $\delta a$ | $\delta b$ | $t$ |
|---|---|---|---|---|---|---|---|
| $2^{-60}$ | $1$ | $1$ | $0$ | $1$ | $2^{-60}$ | $0$ | $2^{-60}$ |
| $0.1$ | $0.2$ | $0.30000000000000004$ | $0.10000000000000003$ | $0.2$ | $-2^{-55}$ | $0$ | $-2^{-55}$ |
| $1$ | $0.75 \cdot 2^{-53}$ | $1$ | $1 - 2^{-53}$ | $2^{-53}$ | $2^{-53}$ | $-2^{-55}$ | $0.75 \cdot 2^{-53}$ |
| $10^{16}$ | $1.5$ | $10^{16} + 2$ | $10^{16}$ | $2$ | $0$ | $-0.5$ | $-0.5$ |

The first row has the small operand first, the case in which [Fast2Sum](/fast-two-sum/) returns $t = 0$; TwoSum recovers $2^{-60}$. In the third row neither $\delta a$ nor $\delta b$ is the error alone: line L2 rounds $1 - 0.75 \cdot 2^{-53}$ down to $1 - 2^{-53}$, so $a$ is credited with less than it contributed, and the two shortfalls $2^{-53}$ and $-2^{-55}$ add up to the true error $0.75 \cdot 2^{-53} = b$.

## Correctness

**Theorem** (Møller, 1965; Knuth, Section 4.2.2; Muller et al., Section 4.3.2). In binary arithmetic with precision $p \ge 3$, round to nearest with a symmetric tie rule, and no overflow in any of the six operations, lines L3 to L6 are exact and $s + t = a + b$, with $|t| \le \tfrac12\mathrm{ulp}(s)$.

*Proof sketch.* Let $r = (a + b) - s$. If the sum is exact, every later line is exact and $t = 0$. If $b$ has an exponent at least that of $a$, lines L1, L2 and L4 are [Fast2Sum](/fast-two-sum/) applied to $(b, a)$, so $a' = s - b$ exactly, $b' = b$, $\delta b = 0$ and $\delta a = r$. Otherwise $e_a > e_b$. Then $a' = \mathrm{fl}(a - r)$ is within $2|r| \le 2\,\mathrm{ulp}(a)$ of $a$, so $a - a'$ is a small multiple of $\tfrac12\mathrm{ulp}(a)$ and is a float; and $s - a'$ is a multiple of $\tfrac12\mathrm{ulp}(a)$ of magnitude below $2^{e_a}$ (or, when $e_b = e_a - 1$, a float by a direct check), so line L3 is exact. Then $b - b'$ is the rounding error of line L2, which is a float, and $\delta a + \delta b = a + b - (a' + b') = r$, a float, so line L6 is exact. The full case analysis is in [proofs/correctness.md](proofs/correctness.md).

What is proved and what is observed:

- **Proved**: $s + t = a + b$ for binary, precision $p \ge 3$, round to nearest with ties to even or ties away from zero, and no overflow; subnormal results are allowed, because the proof uses only the spacing of floats. No FMA is involved.
- **Observed**: the tests checked $s + t = a + b$ in exact rational arithmetic for $5 \times 10^4$ random pairs in both orders, over the whole exponent range, with close exponents, with random bit patterns and with subnormals, and $t$ always equalled `math.fsum([a, b, -s])`. An exhaustive check over all pairs of a simulated binary format with $p = 2$, $3$ and $4$ and a small exponent range, with subnormals, found no failure, so the restriction $p \ge 3$ in the proof is not needed in that range.

## Complexity

Six floating-point additions or subtractions and no branch. The dependency chain is L1, L2, L3, L5, L6 (five operations), with L4 in parallel with L3, so the latency is five additions against three for Fast2Sum. Kornerup, Lefèvre, Louvet and Muller showed that six operations are the minimum for any branch-free algorithm that uses only rounded additions and subtractions and computes the exact error for all inputs (Muller et al., Section 4.3).

## Properties

- **No precondition on the operands.** Exact for all finite inputs, in either order, with no comparison.
- **Nonoverlapping output.** $|t| \le \tfrac12\mathrm{ulp}(s)$, so $(s, t)$ is a normalized double-word number.
- **Same output as Fast2Sum with sorting.** For $|a| \ge |b|$, Fast2Sum$(a, b)$ returns the same pair, because both are exact and $s$ is the same.
- **Symmetric result.** TWO-SUM$(a, b)$ and TWO-SUM$(b, a)$ return the same $(s, t)$, although the intermediate values differ.
- **Fragile under compiler rewriting.** Algebraic simplification of $(a - (s - b)) + (b - (s - (s - b)))$ gives $0$.

## Variants and improvements

- **[Fast2Sum](/fast-two-sum/).** Three operations, exact when $e_a \ge e_b$; with a comparison and a swap it handles any order, which is faster when the branch is predictable.
- **Directed rounding.** With rounding toward $\pm\infty$ or zero the error of an addition need not be a float, so no algorithm can return it exactly; TwoSum then returns an approximation, and Boldo, Graillat and Muller bound its error.
- **Vector and SIMD versions.** Because it has no branch, TwoSum vectorizes directly and is the form used in compensated summation and dot products on SIMD hardware (Sum2 and Dot2 of Ogita, Rump and Oishi).
- **Augmented addition.** IEEE 754-2019 recommends an `augmentedAddition` operation (Clause 9.5) that returns the pair in one instruction, with ties rounded toward zero so that the pair is unique and reproducible.
- **For products.** The analogous transformation of multiplication is [TwoProduct](/two-product/), with an FMA or with [Veltkamp splitting](/veltkamp-splitting/).

## When to use it

Use TwoSum when the error of an addition is needed and the relative size of the operands is unknown: in compensated summation without a branch, in double-double and quad-double addition, in exact summation of floating-point expansions, and in verified computations. Use Fast2Sum when the order is known, for instance to renormalize a double-word result.

## Pitfalls

- **Fast-math compilation.** Options such as `-ffast-math` let the compiler reassociate the six operations and return $t = 0$.
- **Extended precision.** If intermediate results are kept in 80-bit registers, line L1 is rounded twice ([double rounding](/double-rounding/)) and $t$ is no longer the binary64 rounding error.
- **Overflow.** If $a + b$ overflows, $s = \pm\infty$ and $t$ is NaN; for $a = b = $ the largest finite binary64 number, the result is $(\infty, \mathrm{NaN})$. Boldo, Graillat and Muller analyse when one of lines L2 to L6 can overflow although $s$ is finite; this concerns only operands near the overflow threshold.
- **Directed rounding modes.** Running the algorithm with a rounding mode other than round to nearest silently gives an approximate $t$.

## Implementations

## History

Møller (1965) described how to compute the rounding error of a floating-point addition without comparing the operands, to get quasi double precision in summation. Knuth stated and proved the six-operation algorithm for binary round to nearest in Volume 2 of The Art of Computer Programming. The name TwoSum comes from Shewchuk's work on adaptive precision arithmetic (1997) and from Ogita, Rump and Oishi (2005), who used it as the building block of accurate summation and dot products. IEEE 754-2019 added the augmented operations, which make the pair a single recommended operation.

## References
