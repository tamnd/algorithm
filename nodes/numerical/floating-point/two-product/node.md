---
tag: Q0TV83
kind: algorithm
slug: two-product
name: TwoProduct (Dekker)
aliases:
- Dekker's product
- TwoProd
- 2MultFMA
area: numerical/floating-point
level: advanced
summary: Computes a product and its exact rounding error as an unevaluated sum of two floats.
model: floating-point-model
complexity:
  vars: {n: "the number of calls (each call is one multiplication, a fixed amount of work)"}
  time: {worst: Θ(1), average: Θ(1), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, in_place: false}
history:
  year: 1971
  people: [T. J. Dekker, G. W. Veltkamp]
  note: Dekker published the exact product, built on Veltkamp's splitting, as mul12 in his 1971 paper on double-length arithmetic.
prereqs: [error-free-transformations, veltkamp-splitting, fused-multiply-add]
see_also: [two-sum, accurate-dot-product, dot2-compensated-dot-product, double-double-arithmetic, floating-point-product-error, horner-rule, fast-two-sum]
sources:
  - paper: doi:10.1007/BF01397083
    title: T. J. Dekker, A floating-point technique for extending the available precision, Numerische Mathematik 18 (1971), 224-242
    locator: the procedure mul12 and its exactness theorem
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Section 4.4, accurate computation of the product of two floating-point numbers (2MultFMA, Veltkamp splitting and Dekker's product, and the condition e_a + e_b >= e_min + p - 1)
  - paper: doi:10.1137/030601818
    title: Takeshi Ogita, Siegfried M. Rump and Shin'ichi Oishi, Accurate sum and dot product, SIAM Journal on Scientific Computing 26(6) (2005), 1955-1988
    locator: Section 3, the algorithms Split and TwoProduct and their use in Dot2
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 2.6, the fused multiply-add operation, and the notes to Chapter 4 on Dekker's double-length techniques
  - url: https://ieeexplore.ieee.org/document/8766229
    title: IEEE Std 754-2019, IEEE Standard for Floating-Point Arithmetic
    locator: Clause 5.4.1, fusedMultiplyAdd
---

TwoProduct computes the rounded product $x = \mathrm{fl}(ab)$ of two floats together with its exact rounding error $y = ab - x$, so that $ab = x + y$ holds exactly. Dekker's version uses only multiplication and addition: it cuts both factors into halves with [Veltkamp splitting](/veltkamp-splitting/), multiplies the halves exactly, and subtracts the pieces from $x$ in an order where every subtraction is exact, 17 operations in all. With a [fused multiply-add](/fused-multiply-add/) the same pair takes two operations, $x = \mathrm{fl}(ab)$ and $y = \mathrm{fma}(a, b, -x)$. Both are exact as long as nothing overflows and the exponents of $a$ and $b$ are not too small, and together with [TwoSum](/two-sum/) they are the basic [error-free transformations](/error-free-transformations/).

## In plain words

Multiplying two numbers of 53 binary digits gives a number of up to 106 digits, and the computer keeps only the first 53. TwoProduct recovers the other half.

Without special hardware it works the way long multiplication on paper does. Each number is cut into a front half and a back half. Products of halves are short enough to compute exactly. Starting from the rounded product, it takes away the front times front, then the two mixed products, then back times back. What remains is exactly the part that rounding threw away. With a fused multiply-add instruction, which multiplies and adds with a single rounding, one extra instruction gives that part directly.

## The problem

**Notation.** A binary floating-point system $F$ with precision $p \ge 4$ and exponent range $[e_{\min}, e_{\max}]$ (binary64 by default, $p = 53$, $e_{\min} = -1022$), round to nearest with a symmetric tie rule (ties to even by default), unit roundoff $u = 2^{-p}$, $\mathrm{fl}(\cdot)$ for the rounded result and $\mathrm{ulp}$ as in Muller et al., Section 2.3.2; see [floating-point arithmetic](/floating-point-arithmetic/). The [standard model](/floating-point-model/) holds without underflow or overflow. $e_a$ denotes the exponent of $a$, so $2^{e_a} \le |a| < 2^{e_a + 1}$.

**Input.** Two finite floats $a$ and $b$.

**Output.** Floats $x$ and $y$ with $x = \mathrm{fl}(ab)$ and $x + y = ab$ exactly; then $|y| \le \tfrac12\mathrm{ulp}(x) \le u|x|$.

## The algorithm

```pseudo id=main
TWO-PRODUCT(a, b)
L1  x ← fl(a · b)
L2  (a_h, a_l) ← VELTKAMP-SPLIT(a, ⌈p/2⌉)          ▷ 4 operations, a = a_h + a_l
L3  (b_h, b_l) ← VELTKAMP-SPLIT(b, ⌈p/2⌉)          ▷ 4 operations, b = b_h + b_l
L4  t₁ ← fl(fl(a_h · b_h) − x)                      ▷ both operations exact
L5  t₂ ← fl(t₁ + fl(a_h · b_l))                     ▷ exact
L6  t₃ ← fl(t₂ + fl(a_l · b_h))                     ▷ exact
L7  y  ← fl(t₃ + fl(a_l · b_l))                     ▷ exact: y = ab − x
L8  return (x, y)
```

Line L1 is the only line that rounds apart from the splits. The products of halves in lines L4 to L7 have at most $p$ significant bits and are exact. The order matters: subtracting the largest piece first makes $t_1$ small, and each later partial result is a small multiple of a fine enough unit to be a float. The FMA variant replaces lines L2 to L7 by $y \leftarrow \mathrm{fma}(a, b, -x)$.

## Example

Every row was run with Python floats (binary64) and checked with `fractions.Fraction`; in every row $x + y = ab$ exactly and the FMA variant returns the same $y$.

| $a$ | $b$ | $x$ | $y$ |
|---|---|---|---|
| $0.1$ | $0.1$ | $0.010000000000000002$ | $-8.326672684688674 \times 10^{-19}$ |
| $1 + 2^{-52}$ | $1 + 2^{-52}$ | $1 + 2^{-51}$ | $2^{-104}$ |
| $3$ | $\mathrm{fl}(1/3)$ | $1$ | $-2^{-54}$ |
| $\pi$ | $e$ | $8.539734222673566$ | $3.119184308355765 \times 10^{-16}$ |

For $a = b = 1 + 2^{-52}$ the intermediate values are $t_1 = -2^{-51}$, $t_2 = -2^{-52}$ and $t_3 = 0$, and the last line adds $a_l b_l = 2^{-104}$, the square of the low part.

## Correctness

**Theorem.** In binary with round to nearest and $p \ge 4$, let $a$ and $b$ be normal floats with $e_a + e_b \ge e_{\min} + p - 1$, and suppose no operation overflows (in particular $(2^{\lceil p/2 \rceil} + 1)a$ and $(2^{\lceil p/2 \rceil} + 1)b$ do not). Then Dekker's algorithm returns $x = \mathrm{fl}(ab)$ and $y = ab - x$ exactly. Under the same exponent condition and without overflow of $ab$, the FMA variant returns the same $y$, for any tie rule.

*Proof sketch.* Scale so that $a, b \in [1, 2)$ and let $q = 2^{1-p}$, $s = \lceil p/2 \rceil$. By the splitting theorem, $a_h$ and $b_h$ are multiples of $2^s q$ with at most $p - s$ bits, and $a_l$, $b_l$ are multiples of $q$ with at most $s - 1$ bits, so the four products of halves fit in $p$ bits. Then $t_1 = a_h b_h - x$ is a multiple of $q$ with $|t_1| \le (2^{s+1} + 2) q$; $t_2$ and $t_3$ are multiples of $2^{s+1-p}q$ with $|t_2| \le (2^s + 2)q$ and $|t_3| \le 2q$; and $y = ab - x$ is a multiple of $q^2$ with $|y| \le q$. Each of these is an integer of at most $p$ bits times a power of two, so each is a float and each line is exact. The exponent condition makes the smallest unit, $2^{e_a + e_b + 2 - 2p}$, at least the subnormal spacing $2^{e_{\min} - p + 1}$. For the FMA, $ab - x$ is a float by the same count, and an FMA returns a representable exact result unchanged. The full proof is in [the proof file](proofs/correctness.md).

**Proved and observed.** The theorem is proved for binary round to nearest with $p \ge 4$, no overflow and the exponent condition. For binary64 the condition reads $e_a + e_b \ge -970$. When it fails the error may not be representable: for $a = b = 2^{-500}(1 + 2^{-52})$ the error is $2^{-1104}$, below the smallest subnormal, and both versions return $y = 0$. The tests observe exactness for every pair of significands with $p = 2$ to $6$ in a simulated format (the proof covers $p \ge 4$), and for 20000 random binary64 pairs with seed 1971.

## Complexity

Dekker's algorithm takes 17 floating-point operations: 1 for $x$, 4 for each split, 4 products of halves and 4 additions, with $\Theta(1)$ time and extra space per call. The FMA variant takes 2. Both are branch free.

## Properties

- **Exact.** $ab = x + y$ with no error; $y$ is the rounding error of the product, not an estimate.
- **Error bound.** $|y| \le \tfrac12\mathrm{ulp}(x) \le u|x|$, so $(x, y)$ is a normalized double-length result.
- **No comparison.** Unlike [Fast2Sum](/fast-two-sum/) there is no ordering condition on the inputs.
- **Robust to the tie rule.** The FMA variant needs only that $x$ is a faithful rounding; then $ab - x$ is representable and the FMA returns it.
- **Depends on rounding to nearest for the split.** Dekker's version relies on [Veltkamp splitting](/veltkamp-splitting/), which is proved for round to nearest.

## Variants and improvements

- **FMA version (2MultFMA).** $x = \mathrm{fl}(ab)$, $y = \mathrm{fma}(a, b, -x)$. It is the preferred form on any processor with a hardware [fused multiply-add](/fused-multiply-add/), which IEEE 754-2008 and 754-2019 require as an operation.
- **Presplit constants.** If $b$ is a constant used many times, such as a coefficient in [Horner's rule](/horner-rule/), split it once and reuse $(b_h, b_l)$; each product then costs 13 operations.
- **Squares.** For $a^2$ the split is done once and the two mixed products are equal, so $t_2 + 2 a_h a_l$ replaces two lines.
- **Accurate dot products and polynomials.** TwoProduct with [TwoSum](/two-sum/) gives Ogita, Rump and Oishi's [Dot2](/dot2-compensated-dot-product/) and the compensated Horner scheme, both as accurate as if computed in twice the working precision.
- **Double-double multiplication.** In [double-double arithmetic](/double-double-arithmetic/) the high parts are multiplied with TwoProduct and the cross terms are added in ordinary arithmetic.

## When to use it

Use TwoProduct whenever the exact error of a product is needed: compensated dot products and polynomial evaluation, double-double and multiple-component arithmetic, exact geometric predicates, and residual computations in [iterative refinement](/iterative-refinement/). Prefer the FMA form wherever FMA is in hardware; use Dekker's form for portability to machines or languages without a fast FMA, or for code that must not depend on it.

## Pitfalls

- **Small exponents.** If $e_a + e_b < e_{\min} + p - 1$, the error may underflow and $y$ is wrong, often zero. Scale the inputs by a power of two when they may be tiny.
- **Overflow in the split.** In binary64, $134217729\,a$ overflows for $|a|$ about $2^{996}$ or more, and $y$ becomes NaN even when $ab$ is moderate; for $a = 2^{1000}$ and $b = 2^{-1000}$, Dekker's version returns $y = \mathrm{NaN}$ while the FMA version returns $y = 0$.
- **Compiler contraction.** If a compiler contracts lines of the split or of L4 to L7 into FMAs, the intermediate results change and the error can be wrong. Disable contraction (for example `-ffp-contract=off`) for Dekker's version, or use the explicit FMA variant.
- **Software FMA.** Where FMA is emulated in software, as on some older platforms, the 2-operation variant can be far slower than the 17-operation one.
- **Extended precision.** On x87 with 64-bit intermediate significands, $x$ is double rounded and the split goes wrong; use SSE2 or another true binary64 evaluation.

## Implementations

## History

Dekker's 1971 paper gave algorithms for double-length addition and multiplication in ordinary floating-point arithmetic. Its mul12 procedure is the exact product above, built on a splitting method that Dekker credits to G. W. Veltkamp. The fused multiply-add of the IBM RS/6000 in 1990 made the two-operation form possible, and IEEE 754-2008 made FMA a required operation. Ogita, Rump and Oishi's 2005 paper used the name TwoProduct and built accurate dot products on it.

## References
