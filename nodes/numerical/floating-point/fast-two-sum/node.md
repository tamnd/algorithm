---
tag: R9EM9Q
kind: algorithm
slug: fast-two-sum
name: Fast2Sum (Dekker)
aliases:
- Dekker's Fast2Sum
- Fast2Sum
- FastTwoSum
- quick-two-sum
area: numerical/floating-point
level: advanced
summary: Exact error of an addition in three operations, valid when the exponent of a is at least that of b.
model: floating-point-model
complexity:
  vars: {n: "the number of calls (each call is one addition, a fixed amount of work)"}
  time: {worst: Θ(1), average: Θ(1), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, in_place: false}
history:
  year: 1971
  people: [Theodorus J. Dekker]
  note: Dekker stated and proved the algorithm in his 1971 paper on extending the available precision. Kahan's compensated summation (1965) already computes the same correction term inside its loop.
prereqs: [floating-point-model, error-free-transformations, ulp]
see_also: [two-sum, kahan-summation, neumaier-summation, double-double-arithmetic, sterbenz-lemma, two-product, shewchuk-expansion-sum, floating-point-summation]
sources:
  - paper: doi:10.1007/BF01397083
    title: T. J. Dekker, A floating-point technique for extending the available precision, Numerische Mathematik 18 (1971), 224-242
    locator: the exact sum of two floats with the larger one first, and its proof
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Section 4.3.1, The Fast2Sum algorithm (Algorithm 4.3 and Theorem 4.3, including the condition on the exponents and on the radix)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, Addison-Wesley, 1998
    locator: Section 4.2.2, Accuracy of floating point arithmetic (the exact error of a sum when the first operand is the larger)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 4.3, Compensated Summation (the correction term of Kahan's method and its exactness)
  - paper: doi:10.1145/363707.363723
    title: W. Kahan, Pracniques, further remarks on reducing truncation errors, Communications of the ACM 8(1) (1965), 40
    locator: compensated summation, whose correction step is Fast2Sum
---

Fast2Sum computes the rounded sum $s = \mathrm{fl}(a + b)$ of two floats together with its exact rounding error $t = (a + b) - s$, using three floating-point operations and no branch. It is exact under round to nearest in binary when the exponent of $a$ is at least that of $b$, which holds in particular when $|a| \ge |b|$. It is the cheapest [error-free transformation](/error-free-transformations/) for addition and the inner step of [compensated summation](/kahan-summation/) and [double-double arithmetic](/double-double-arithmetic/); when the order of the operands is unknown, [TwoSum](/two-sum/) does the same job in six operations without the condition.

## In plain words

When a computer adds a big number and a small one, the small one's last digits often fall off the end and are lost. Fast2Sum gets those lost digits back.

It adds the two numbers as usual. Then it subtracts the big number from the result, which tells how much of the small number actually got in. Subtracting that from the small number leaves exactly the part that was lost. Three steps give the rounded sum and the exact leftover, so the two together equal the true sum with nothing missing. The trick needs the first number to be the larger one; if it is not, the leftover can come out wrong.

## The problem

**Notation.** A binary floating-point system with precision $p$ (binary64 by default, $p = 53$, $e_{\min} = -1022$), round to nearest with any tie rule, unit roundoff $u = 2^{-p}$, $\mathrm{fl}(\cdot)$ for the rounded result and $\mathrm{ulp}$ as in Muller et al., Section 2.3.2; see [floating-point arithmetic](/floating-point-arithmetic/). For a float $x$, $e_x$ is its exponent, $\lfloor \log_2 |x| \rfloor$ for normal $x$ and $e_{\min}$ for zero and subnormals.

**Input.** Two finite floats $a$ and $b$ with $e_a \ge e_b$, such that $a + b$ does not overflow.

**Output.** Floats $s$ and $t$ with $s = \mathrm{fl}(a + b)$ and $s + t = a + b$ exactly.

## The algorithm

```pseudo id=main
FAST-TWO-SUM(a, b)                     ▷ requires e_a ≥ e_b
L1  s ← fl(a + b)
L2  z ← fl(s − a)                      ▷ exact: the part of b that s absorbed
L3  t ← fl(b − z)                      ▷ exact: the part of b that was lost
L4  return (s, t)
```

Line L2 measures how much of $b$ made it into $s$. Under the hypothesis this difference is a float, so it is computed without error, and line L3 subtracts it from $b$ to leave the rounding error of line L1, which is again a float.

## Example

Each row was run with Python floats (binary64) and checked with `fractions.Fraction`: in every row $s + t = a + b$ exactly. Values in hex are `float.hex` output.

| $a$ | $b$ | $s$ | $z$ | $t$ |
|---|---|---|---|---|
| $1$ | 0x1.0000000000001p-53 $= 2^{-53} + 2^{-105}$ | 0x1.0000000000001p+0 | 0x1p-52 | $-\texttt{0x1.ffffffffffffep-54} = -2^{-53} + 2^{-105}$ |
| $0.2$ = 0x1.999999999999ap-3 | $0.1$ | $0.30000000000000004$ = 0x1.3333333333334p-2 | 0x1.999999999999cp-4 | $-2^{-55}$ |
| $10^{16}$ | $1.5$ | $10000000000000002$ | $2$ | $-0.5$ |
| $1$ | $1.5$ | $2.5$ | $1.5$ | $0$ |

In the first row $b$ is a little more than half an ulp of $1$, so $s$ rounds up to $1 + 2^{-52}$; the error $t$ is negative and a little less than half an ulp. In the third row the spacing of floats near $10^{16}$ is $2$, the exact sum $10^{16} + 1.5$ rounds to $10^{16} + 2$, and the error is $-0.5$. The last row has $|a| < |b|$ but equal exponents, which the hypothesis allows.

**When the hypothesis fails.** For $a = 2^{-60}$ and $b = 1$, line L1 gives $s = 1$, line L2 gives $z = \mathrm{fl}(1 - 2^{-60}) = 1$, and line L3 gives $t = 0$, so $s + t = 1 \ne a + b$: the lost part $2^{-60}$ is not recovered. Swapping the operands gives $t = 2^{-60}$.

## Correctness

**Theorem** (Dekker, 1971; Muller et al., Theorem 4.3). In binary arithmetic with round to nearest (any tie rule), if $e_a \ge e_b$ and no overflow occurs, then $z = s - a$ and $t = b - z$ exactly, so $s + t = a + b$, and $|t| \le \tfrac12\mathrm{ulp}(s) \le u|s|$.

*Proof sketch.* Let $U = 2^{e_b - p + 1}$, the spacing of floats at the exponent of $b$; $a$, $b$, $a + b$ and $s$ are all integer multiples of $U$. Since $a$ is itself a float near $a + b$, rounding to nearest gives $|s - (a + b)| \le |b|$, so $|s - a| \le 2|b|$. If $|a + b| \le 2^{e_b + 1}$, the sum is exact and $t = 0$. Otherwise $s$ is a multiple of $2U$; if $e_a > e_b$ so is $a$, and $s - a$ is a multiple of $2U$ below $2^{e_b + 2}$ in magnitude, hence a float; if $e_a = e_b$, $a$ and $b$ have the same sign, the error of line L1 is $0$ or $\pm U$, and $|s - a| \le 2^{e_b + 1}$, again a float. So line L2 is exact. Then $b - z = (a + b) - s$ is a multiple of $U$ with magnitude at most $|b|$, so it is a float and line L3 is exact. The full proof is in `proofs/correctness.md`.

What is proved and what is not:

- **Proved**: the identity $s + t = a + b$ for binary (more generally radix $2$ or $3$, Muller et al., Section 4.3.1), round to nearest with any tie rule, $e_a \ge e_b$, and no overflow. Underflow does not matter, because the proof uses only the spacing of floats, which is uniform among subnormals. An FMA is not needed and does not change the result.
- **Observed**: the implementation's tests run a large number of random pairs over the whole exponent range, with close and equal exponents in either order, and check $s + t = a + b$ in exact rational arithmetic; no failure occurred, and $t$ always equalled `math.fsum([a, b, -s])`.

## Complexity

Three floating-point additions or subtractions, each depending on the one before, and $O(1)$ extra space. The latency is that of three dependent additions. TwoSum needs six operations; Fast2Sum with a comparison and swap needs three operations and a branch or two selects.

## Properties

- **Exact under its hypothesis.** $s + t = a + b$ with no rounding error at all, and $s$ is the ordinary rounded sum.
- **Nonoverlapping output.** $|t| \le \tfrac12\mathrm{ulp}(s)$, so $t$ is below the last bit of $s$ and $(s, t)$ is a normalized double-word number, which is what [double-double arithmetic](/double-double-arithmetic/) needs to renormalize.
- **Sign of zero.** If $a + b$ is exact, $t = b - b$ is $+0$ in round to nearest, whatever the signs of $a$ and $b$.
- **Branch-free.** No comparison is made; the caller is responsible for the order of the operands.
- **Fragile under compiler rewriting.** An optimizer that treats floating-point addition as associative simplifies $b - ((a + b) - a)$ to $0$.

## Variants and improvements

- **With a comparison.** `if |a| < |b|: swap(a, b)` before line L1 makes Fast2Sum valid for all inputs; on pipelined processors a mispredicted branch can cost more than the three extra operations of TwoSum (Muller et al., Section 4.3.2).
- **[TwoSum](/two-sum/)** (Møller 1965, Knuth). Six operations, no condition on the operands, exact in binary with round to nearest.
- **Inside other algorithms.** Kahan's compensated summation computes $c = (t - s) - y$, which is the negated Fast2Sum error when the running sum dominates the next term; [Neumaier's variant](/neumaier-summation/) swaps the roles when it does not. Double-double addition uses TwoSum for the main sum and Fast2Sum to renormalize, and [expansion arithmetic](/shewchuk-expansion-sum/) uses both.
- **Directed rounding.** With rounding toward $\pm\infty$ or zero the error of a sum need not be a float: for $a = 1$ and $b = -2^{-200}$, rounding down gives $s = 1 - 2^{-53}$, and $(a + b) - s = 2^{-53} - 2^{-200}$ needs $147$ significant bits. Fast2Sum then returns only an approximation of the error (Muller et al., Section 4.3.1).

## When to use it

Use Fast2Sum when the order of magnitude of the operands is known in advance: renormalizing a double-word number, adding a small correction to a large accumulator, or summing terms sorted by decreasing magnitude. Use TwoSum when the order is unknown and branches are expensive, and [Sterbenz's lemma](/sterbenz-lemma/) when only a subtraction of nearby numbers is needed.

## Pitfalls

- **The operands in the wrong order.** If $e_a < e_b$, the error can be lost entirely, as in the example with $a = 2^{-60}$, $b = 1$; nothing signals the failure.
- **Compiler optimizations.** Options such as `-ffast-math` or `-fassociative-math` allow the compiler to reduce $t$ to $0$. Extended precision of intermediate results (x87 registers) can also break exactness through [double rounding](/double-rounding/).
- **Overflow.** If $a + b$ overflows, $s = \pm\infty$ and $t$ is infinite or NaN; for $a = b = $ the largest finite binary64 number, the result is $(\infty, -\infty)$.
- **Radix 10.** The theorem needs radix $2$ or $3$; it fails in decimal arithmetic, so it does not carry over to [decimal floating-point](/decimal-floating-point/) types.

## Implementations

## History

Kahan's compensated summation (1965) contains the correction step of Fast2Sum without stating it as a separate algorithm. Dekker (1971) isolated it, proved that it is exact in binary when $|a| \ge |b|$, and used it with his exact product to build double-length arithmetic. Knuth gives the result in TAOCP Volume 2, Section 4.2.2. The weaker condition on exponents and the analysis for other radices and rounding modes are presented in Muller et al., Section 4.3.1.

## References
