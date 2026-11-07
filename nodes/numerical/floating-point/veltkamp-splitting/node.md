---
tag: Z6SW6X
kind: algorithm
slug: veltkamp-splitting
name: Veltkamp splitting
aliases:
- Veltkamp's splitting
- Dekker splitting
area: numerical/floating-point
level: advanced
summary: Splits a floating-point number into two halves with fewer significant bits, enabling exact products.
model: floating-point-model
complexity:
  vars: {n: "the number of calls (each call splits one float with a fixed amount of work)"}
  time: {worst: Θ(1), average: Θ(1), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, in_place: false}
history:
  year: 1971
  people: [G. W. Veltkamp, T. J. Dekker]
  note: Veltkamp devised the split; Dekker published it with credit to him in his 1971 paper on extending the available precision.
prereqs: [error-free-transformations, floating-point-model, ulp]
see_also: [two-product, two-sum, fused-multiply-add, double-double-arithmetic, accurate-dot-product, sterbenz-lemma, fast-two-sum]
sources:
  - paper: doi:10.1007/BF01397083
    title: T. J. Dekker, A floating-point technique for extending the available precision, Numerische Mathematik 18 (1971), 224-242
    locator: the splitting procedure inside mul12, credited to G. W. Veltkamp
  - paper: doi:10.1145/103162.103163
    title: David Goldberg, What every computer scientist should know about floating-point arithmetic, ACM Computing Surveys 23(1) (1991), 5-48
    locator: Theorem 6 (splitting x into two halves of about p/2 digits) and its proof
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Section 4.4.1, Veltkamp splitting (the algorithm and the theorem on the sizes of the two parts)
  - paper: doi:10.1007/11814771_6
    title: Sylvie Boldo, Pitfalls of a full floating-point proof, example on the formal proof of the Veltkamp/Dekker algorithms, IJCAR 2006, LNCS 4130, 52-66
    locator: the formal proof of the splitting, including the bound on the low part
---

Veltkamp splitting writes a float $a$ as an exact sum $a = a_h + a_l$ of two floats whose significands are each about half as long as that of $a$. It takes one multiplication by the constant $C = 2^s + 1$ and three subtractions or additions, with no branch and no access to the bit pattern. For binary64 with $s = 27$, both parts fit in 26 bits, so the product of any two parts of two numbers is exact. That is what [Dekker's product](/two-product/) needs to compute the exact rounding error of a multiplication on hardware without a [fused multiply-add](/fused-multiply-add/).

## In plain words

A computer multiplication of two full-length numbers gives a result twice as long as fits, so part of it is thrown away. If each number is first cut into a front half and a back half, every product of two halves is short enough to keep in full.

Veltkamp's trick does the cutting with ordinary arithmetic. It multiplies the number by a constant slightly bigger than a power of two, which pushes the number's back digits off the end. Subtracting the original back out then leaves the front half, rounded. The back half is whatever is left over when the front half is taken away from the original, and that subtraction loses nothing.

## The problem

**Notation.** A binary floating-point system $F$ with precision $p$ and exponent range $[e_{\min}, e_{\max}]$ (binary64 by default, $p = 53$), round to nearest with a symmetric tie rule (ties to even by default), unit roundoff $u = 2^{-p}$, $\mathrm{fl}(\cdot)$ for the rounded result and $\mathrm{ulp}$ as in Muller et al., Section 2.3.2; see [floating-point arithmetic](/floating-point-arithmetic/). The [standard model](/floating-point-model/) holds without underflow or overflow.

**Input.** A finite float $a$ and an integer split point $s$ with $1 \le s \le p - 1$ (for binary64, $s = 27$).

**Output.** Floats $a_h$ and $a_l$ with $a_h + a_l = a$ exactly, where $a_h$ is a multiple of $2^s\,\mathrm{ulp}(a)$ (so it has at most $p - s$ significant bits) and $|a_l| \le 2^{s-1}\,\mathrm{ulp}(a)$ (so it has at most $s - 1$ significant bits when $s \ge 2$).

## The algorithm

```pseudo id=main
VELTKAMP-SPLIT(a, s)
L1  C   ← 2^s + 1                     ▷ 134217729 for binary64 with s = 27
L2  γ   ← fl(C · a)                   ▷ a scaled up; its last s bits are rounded away
L3  δ   ← fl(a − γ)                   ▷ about −2^s · a, on the coarse grid
L4  a_h ← fl(γ + δ)                   ▷ a rounded to p − s bits
L5  a_l ← fl(a − a_h)                 ▷ exact: the remainder
L6  return (a_h, a_l)
```

Line L2 computes $(2^s + 1)a$, a number about $2^s$ times larger than $a$, so its unit in the last place is about $2^s\,\mathrm{ulp}(a)$. Line L3 cancels the scaled copy back down; the result lands on that coarse grid. Line L4 adds the two coarse numbers, and the sum is $a$ rounded to the nearest multiple of $2^s\,\mathrm{ulp}(a)$. Line L5 is exact because $a_h$ is close to $a$.

## Example

Take $a = \pi$ in binary64, $a = \texttt{0x1.921fb54442d18p+1}$, with $s = 27$ and $C = 134217729$. Every value below was computed with Python floats and checked with `fractions.Fraction`.

| line | value | hexadecimal |
|---|---|---|
| L2 $\gamma$ | $421657431.40790576$ | `0x1.921fb57686c83p+28` |
| L3 $\delta$ | $-421657428.2663131$ | `-0x1.921fb54442d18p+28` |
| L4 $a_h$ | $3.1415926814079285$ | `0x1.921fb58000000p+1` |
| L5 $a_l$ | $-2.781813535079891 \times 10^{-8}$ | `-0x1.dde9740000000p-26` |

The high part has 26 significant bits and the low part has 23. Here $\delta$ happens to equal $-2^{27}a$ exactly, and $a_h$ is $\pi$ rounded up at bit 26, so $a_l$ is negative. For $a = 0.1$ the split gives $a_h = \texttt{0x1.9999998p-4}$ and $a_l = \texttt{0x1.99999ap-32}$, with 26 and 24 significant bits.

## Correctness

**Theorem.** Let the radix be 2, the rounding round to nearest with a symmetric tie rule, $1 \le s \le p - 1$, and $a$ a nonzero float such that no operation overflows and $a$ is normal. Then $a_h + a_l = a$ exactly, $a_h$ is a multiple of $2^s\,\mathrm{ulp}(a)$ with $|a_h| \le 2^{e_a + 1}$, and $|a_l| \le 2^{s-1}\,\mathrm{ulp}(a)$, where $e_a$ is the exponent of $a$.

*Proof sketch.* Scale so that $1 \le a < 2$, and write $q = \mathrm{ulp}(a) = 2^{1-p}$ and $\sigma = 2^s$. Since $Ca \ge \sigma + 1$ lies in a binade whose spacing is at least $\sigma q$, $\gamma$ is a multiple of $\sigma q$. The difference $\gamma - a$ lies in $[\sigma, 2\sigma]$, a range where the floats are spaced at most $\sigma q$ apart and include every multiple of $\sigma q$; so rounding it to nearest gives a multiple of $\sigma q$, and $\gamma + \delta$, a multiple of $\sigma q$ near $a$, is $a$ rounded to the nearest multiple of $\sigma q$. That number lies in $[1, 2]$ and has at most $p - s$ significant bits, so line L4 is exact. Then $a - a_h$ is a multiple of $q$ of size at most $\sigma q/2$, hence a float, and line L5 is exact. The full proof, with the case where $\gamma$ moves up a binade, is in [the proof file](proofs/correctness.md).

**Proved and observed.** The theorem is proved for binary round to nearest, without overflow, for normal $a$. The tests also observe exact splits for subnormal $a$ (5000 random values, seed 5); Boldo (2006) gives a formal proof that covers underflow. Directed rounding is not covered.

## Complexity

One multiplication and three additions or subtractions, $\Theta(1)$ time and $\Theta(1)$ extra space per call. The constant $C$ is computed once. Splitting both factors of a product costs 8 operations, which is most of the 17 operations of [Dekker's product](/two-product/).

## Properties

- **Exact.** $a = a_h + a_l$ holds with no error at all, not merely to within a rounding error.
- **Branch free.** No comparison, no bit manipulation and no access to the exponent; it runs on any machine with correctly rounded multiplication and addition.
- **Short parts.** For $s = \lceil p/2 \rceil$ the parts have at most $\lfloor p/2 \rfloor$ and $\lceil p/2 \rceil - 1$ bits, so in binary64 (26 and 26) any product $x_h y_h$, $x_h y_l$, $x_l y_h$ or $x_l y_l$ needs at most 52 bits and is exact.
- **Sign trick.** The low part may have the opposite sign to $a$, as in the $\pi$ example. That is what lets 53 bits fit into $26 + 26$: the sign carries the missing bit.
- **Rounded, not truncated.** $a_h$ is $a$ rounded to nearest at bit $p - s$, not $a$ with its trailing bits cleared.

## Variants and improvements

- **Bit masking.** Clearing the low 27 bits of the significand gives $a_h$ with 26 bits and $a_l = a - a_h$ with up to 27 bits. That is too long for exact products of two low parts, and it needs integer access to the representation.
- **Fused multiply-add.** With an [FMA](/fused-multiply-add/) no split is needed: $\mathrm{fl}(ab)$ and $\mathrm{fma}(a, b, -\mathrm{fl}(ab))$ give the product and its error in two operations; see [two-product](/two-product/).
- **Any split point.** Other values of $s$ split $a$ into $p - s$ and $s - 1$ bits. These are used in [double-double arithmetic](/double-double-arithmetic/) and in table-based argument reduction, where a constant such as $\pi/2$ is stored in short pieces so that products with small integers are exact.
- **Other radices.** Dekker's paper and Boldo's formal proof treat general radix; outside radix 2 the low part may need $s$ digits, not $s - 1$.

## When to use it

Use Veltkamp splitting to build [Dekker's product](/two-product/) or an [accurate dot product](/accurate-dot-product/) where no fused multiply-add is available or where its speed cannot be relied on, and whenever a float must be written exactly as a sum of shorter pieces. On hardware with a fast FMA, the two-operation FMA product is better.

## Pitfalls

- **Contraction into an FMA.** If a compiler fuses lines L2 and L3 into $\mathrm{fma}(-C, a, a)$, then $\delta = -2^s a$ exactly, $a_h = a$ and $a_l = 0$, and the split silently does nothing. Code that relies on the split must disable floating-point contraction (for example `-ffp-contract=off` in C).
- **Overflow.** $C a$ overflows when $|a|$ is about $2^{996}$ or more in binary64 ($2^{1024}/2^{28}$); then $a_h$ and $a_l$ are NaN. Scale $a$ down by a power of two first and scale the parts back.
- **Extended intermediate precision.** On x87 hardware with 64-bit intermediate significands, $\gamma$ is not rounded to 53 bits and the parts come out with the wrong lengths. Evaluate in true binary64, as SSE2 does.
- **Wrong constant.** $C$ must be $2^s + 1$ exactly. For binary32, $p = 24$ and $s = 12$ give $C = 4097$.

## Implementations

## History

Dekker's 1971 paper, which introduced the double-length operations later called double-double arithmetic, attributes the splitting method used in its multiplication routine to G. W. Veltkamp. Goldberg's 1991 survey restated it as Theorem 6, with a proof for radix 2 and even precision in other radices. The remark that in radix 2 the low part fits in $s - 1$ bits, one fewer than the obvious count, is what makes the 53-bit product exact with 26-bit halves. Boldo verified the algorithm, including underflow, in the Coq proof assistant in 2006.

## References
