---
tag: CV0X1C
kind: data-structure
slug: kulisch-accumulator
name: Kulisch accumulator
aliases:
- long accumulator
- superaccumulator
- exact dot product register
area: numerical/floating-point
level: research
summary: A fixed-point register wide enough to hold any sum of floats exactly, rounding only once at the end.
prereqs: [floating-point-summation, accurate-dot-product, ieee-754]
see_also: [reproducible-summation, shewchuk-expansion-sum, neumaier-summation, two-product, dot2-compensated-dot-product, posit-format, double-double-arithmetic]
sources:
  - paper: doi:10.1137/1028001
    title: Ulrich W. Kulisch and Willard L. Miranker, The arithmetic of the digital computer, a new approach, SIAM Review 28(1) (1986), 1-40
    locator: the exact scalar product computed in a long fixed-point accumulator and rounded once
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Chapter 5, enhanced floating-point sums and dot products (exact accumulation in a long accumulator)
  - paper: doi:10.1016/j.parco.2015.09.001
    title: Sylvain Collange, David Defour, Stef Graillat and Roman Iakymchuk, Numerical reproducibility for the parallel reduction on multi- and many-core architectures, Parallel Computing 49 (2015), 83-97
    locator: the superaccumulator with carry-save limbs and its combination with floating-point expansions (ExBLAS)
  - url: https://arxiv.org/abs/1505.05571
    title: Radford M. Neal, Fast exact summation using small and large superaccumulators, 2015
    locator: the large and small superaccumulator layouts and their measured speed against compensated summation
  - url: https://ieeexplore.ieee.org/document/8766229
    title: IEEE Std 754-2019, IEEE Standard for Floating-Point Arithmetic
    locator: Clause 9.4, the recommended reduction operations sum and dot
---

A Kulisch accumulator is a fixed-point register long enough to hold the exact value of any sum of floats or products of floats in a given format. Each float or exact product is shifted into place and added with integer arithmetic, so no rounding occurs until the end, when the register is rounded once to the nearest float. The result is the correctly rounded value of the exact sum or dot product, independent of the order of the terms. For binary64 dot products the register is about 4300 bits, which is large for hardware and cheap for software working on 64-bit words.

## In plain words

Rounding errors in a long sum come from rounding after every addition. A Kulisch accumulator avoids them by keeping every digit. It is like an enormous odometer with a place for every power of two a float can have, from the tiniest to the largest, plus some extra places on top for carries.

To add a number, find its place on the odometer and add its digits there; carries ripple upward as with any whole-number addition. Nothing ever falls off the end. When all the numbers are in, read off the leading digits and round once. The answer is the best possible float for the true sum, in any order.

## The abstract type

An accumulator $R$ represents one exact real number $\mathrm{val}(R)$, initially $0$.

- $\mathrm{ADD}(R, x)$: $\mathrm{val}(R) \leftarrow \mathrm{val}(R) + x$ for a float $x$.
- $\mathrm{ADD\text{-}PRODUCT}(R, a, b)$: $\mathrm{val}(R) \leftarrow \mathrm{val}(R) + ab$, the exact product.
- $\mathrm{ROUND}(R)$: return $\mathrm{fl}(\mathrm{val}(R))$, rounded to nearest, ties to even (or another mode).
- Optionally $\mathrm{MERGE}(R, S)$: $\mathrm{val}(R) \leftarrow \mathrm{val}(R) + \mathrm{val}(S)$, and NaN and infinity flags following IEEE 754.

The contract: after any sequence of operations, $\mathrm{val}(R)$ equals the exact sum of all terms added, as long as fewer than $2^g$ terms were added, where $g$ is the number of guard bits.

## Representation

**Notation.** binary64 with $p = 53$, $[e_{\min}, e_{\max}] = [-1022, 1023]$; every finite float is $m \cdot 2^e$ with an integer $|m| < 2^{53}$ and $e \ge -1074$. $\mathrm{fl}(\cdot)$ is round to nearest, ties to even, and $\mathrm{ulp}$ is as in Muller et al., Section 2.3.2; see [floating-point arithmetic](/floating-point-arithmetic/).

The register is an integer $V$ in two's complement, stored in $L$ limbs of 64 bits, with $\mathrm{val}(R) = V \cdot 2^{-2148}$:

- **2148 bits below the binary point.** The smallest nonzero product is $2^{-1074} \cdot 2^{-1074} = 2^{-2148}$, so every product is an integer multiple of $2^{-2148}$.
- **2048 bits above it.** Every finite product is below $2^{1024} \cdot 2^{1024} = 2^{2048}$.
- **Guard bits.** With $L = 67$ limbs (4288 bits) there are 91 bits above $2^{2048}$ and a sign bit, so up to $2^{91}$ products of any size can be added without overflow.

For sums of floats alone, 1074 fractional bits and 1024 integer bits suffice, about 2100 bits plus guard bits. Specials are kept as flags: a NaN flag, and flags for $+\infty$ and $-\infty$.

## Operations

```pseudo id=main
ADD-PRODUCT(R, a, b)                           ▷ ADD(R, x) is ADD-PRODUCT(R, x, 1)
L1  (m, e) ← (m_a·m_b, e_a + e_b)               ▷ exact: |m| < 2^106
L2  s ← e + 2148                                ▷ bit position of m in V
L3  i ← ⌊s/64⌋; chunk ← |m| · 2^(s mod 64)      ▷ spans at most 3 limbs
L4  while chunk ≠ 0 or carry ≠ 0 do             ▷ add if m > 0, subtract if m < 0
L5      R[i] ← R[i] ± (chunk mod 2^64) ± carry, with new carry or borrow; chunk ← ⌊chunk/2^64⌋; i ← i + 1

ROUND(R)
L6  V ← the signed integer in R; if V = 0 then return 0
L7  k ← bit length of |V|; d ← max(k − 53, 2148 − 1074)  ▷ keep 53 bits, but not below 2^−1074
L8  q ← ⌊|V|/2^d⌋, rounded to nearest even using bit d−1 and the bits below it
L9  return sign(V) · q · 2^(d − 2148), or ±∞ if it reaches 2^1024
```

A merge adds two registers limb by limb with one carry chain. Hardware designs keep a carry-save copy or per-limb carry flags so that an addition never waits for a long carry.

## Example

Add $10^{100}$, $1$ and $-10^{100}$. The float $10^{100}$ is $m \cdot 2^{280}$ with a 53-bit $m$, so it lands at bit $280 + 2148 = 2428$, in limbs 37 and 38. The float $1$ is bit 2148, bit 36 of limb 33. Adding $-10^{100}$ subtracts exactly what was added at limbs 37 and 38, the borrows cancel, and the register holds $V = 2^{2148}$ in limb 33 only. ROUND returns $1$; ordinary floating-point addition in this order returns $0$.

For $\sum_{i=1}^{10} \mathrm{fl}(0.1)$ the register holds $10 \cdot \mathrm{fl}(0.1) = 1 + 5.55 \times 10^{-17}$ exactly, and ROUND returns $1.0$, the float nearest the exact sum.

## Correctness

**Invariant.** After every operation, $V \cdot 2^{-2148} = \sum(\text{terms added so far})$, provided fewer than $2^{91}$ terms were added. Each term is an integer multiple of $2^{-2148}$ (L1, L2), adding the integer $m \cdot 2^{s}$ to $V$ is exactly what L3 to L5 do with carries or borrows in base $2^{64}$, and the bound on the number of terms keeps $|V| < 2^{4287}$, so the two's complement value never wraps. **Rounding.** L7 and L8 keep the 53 leading bits (fewer in the subnormal range, where the quantum is fixed at $2^{-1074}$) and round on the remaining bits, which is round to nearest, ties to even, of the exact value; L9 gives infinity exactly when the rounded value reaches $2^{1024}$. Both parts are proved in [the proof file](proofs/correctness.md), and the tests check $V$ against an exact `Fraction` after each of 500 random products, and the rounded results against `float(Fraction(...))` for random, ill-conditioned and edge-case inputs.

## Complexity

Let $L$ be the number of limbs (67 for binary64 dot products) and $n$ the number of terms.

| operation | time | note |
|---|---|---|
| ADD, ADD-PRODUCT | $O(1)$ limbs typical, $O(L)$ worst | a carry or borrow can run through all limbs |
| ROUND | $O(L)$ | find the leading limb, then a constant amount of work |
| MERGE | $O(L)$ | one limb-wise addition |
| space | $L$ words | 536 bytes for binary64 dot products |

A sum of $n$ terms costs $O(n + L)$ in the typical case. The worst case of $O(L)$ per addition happens when terms of opposite sign make the register cross zero repeatedly; carry-save limbs or lazy carry resolution remove it in practice.

## Variants

- **Sum-only accumulator.** About 2100 bits suffice for exact sums of binary64 floats, and 4288 bits for exact dot products.
- **Carry-save limbs.** Neal's and Collange et al.'s superaccumulators let each limb absorb many additions before normalizing carries, so additions are branch-free and parallel.
- **Small and large superaccumulators.** Neal combines a small accumulator indexed by exponent with a large one, reaching speeds close to plain summation for long sums.
- **Quire.** The [posit](/posit-format/) standard defines a quire, a Kulisch accumulator sized for each posit format, as part of the number system.
- **Hybrid with expansions.** ExBLAS first accumulates in a few-term floating-point expansion per thread and spills to the superaccumulator only when needed; see [reproducible summation](/reproducible-summation/) and [Shewchuk's expansions](/shewchuk-expansion-sum/).

## When to use it

Use a long accumulator when a sum or dot product must be correctly rounded or bit-for-bit reproducible across orderings and machines, regardless of conditioning: verified computing, reproducible parallel reductions, exact residuals in iterative refinement, and exactly rounded BLAS. For well-conditioned data, [compensated summation](/neumaier-summation/) or [Dot2](/dot2-compensated-dot-product/) is cheaper and usually accurate enough.

## Pitfalls

- **Guard bits.** Too few guard bits and a long sum of large terms wraps around silently; count the terms.
- **Carry chains.** A naive software accumulator can be slow on inputs that alternate in sign near zero, since each addition may carry through every limb.
- **Specials.** Infinities and NaNs cannot live in a fixed-point register; track them with flags, and remember that $\infty \cdot 0$ is NaN and $+\infty + (-\infty)$ is NaN.
- **Products that overflow in floating point.** Compute $ab$ from the integer significands, not as a float: $10^{300} \cdot 10^{300}$ overflows as a float but is held exactly in the register.
- **One rounding, not zero.** The result is correctly rounded, not exact; an exact answer needs the register itself, or an expansion read out of it.

## Implementations

## History

Kulisch argued from the 1970s that computers should provide an exact dot product as a basic operation, and with Miranker developed the theory and the long accumulator in the early 1980s; IBM offered it in the ACRITH library for System/370 and Kulisch's group built coprocessors with it. IEEE 754 did not adopt it as a required operation, but IEEE 754-2008 and 754-2019 recommend reduction operations such as `dot`. Software superaccumulators revived the idea in the 2010s for reproducible computing, and the posit standard made the quire a required part of the format.

## References
