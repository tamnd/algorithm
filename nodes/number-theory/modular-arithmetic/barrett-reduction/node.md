---
tag: MXGY63
kind: algorithm
slug: barrett-reduction
name: Barrett reduction
aliases:
- Barrett modular reduction
area: number-theory/modular-arithmetic
level: advanced
summary: Reduces x mod n using a precomputed reciprocal approximation instead of division.
solves: [modular-multiplication]
model: word-ram
complexity:
  vars: {k: the number of binary digits of the modulus n, w: the number of binary digits in a word, M: the cost of multiplying two k-digit integers}
  time: {worst: Θ((k/w)^2), best: Θ((k/w)^2)}
  space: {extra: Θ(k/w)}
  bit_operations: {worst: O(M(k))}
  precomputation: {worst: O(M(k))}
properties: {deterministic: true, recursive: false}
history:
  year: 1986
  people: [Paul Barrett]
  note: Presented at CRYPTO '86 in a paper on fast RSA on a digital signal processor; Menezes, van Oorschot and Vanstone gave the multiprecision form with at most two corrections in 1996.
prereqs: [modular-multiplication, division-with-remainder]
see_also: [montgomery-multiplication, granlund-montgomery-division, newton-raphson-division, modular-exponentiation, binary-exponentiation, rsa-cryptosystem, number-theoretic-transform, timing-attack]
sources:
  - paper: doi:10.1007/3-540-47721-7_24
    title: Paul Barrett, Implementing the Rivest Shamir and Adleman public key encryption algorithm on a standard digital signal processor, Advances in Cryptology, CRYPTO '86, Lecture Notes in Computer Science 263
    locator: pages 311 to 323 (the reduction modulo the RSA modulus with a precomputed reciprocal)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1997
    locator: Section 14.3.3, Barrett reduction (Algorithm 14.42, Fact 14.43 that Q - 2 ≤ q3 ≤ Q, Notes 14.44 and 14.45, Example 14.46 with x = 3561 and m = 47)
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 2.4.1, Barrett's algorithm (Algorithm 2.5 BarrettDivRem, Theorem 2.4 with at most three corrections, and the cost 2M(n) with full products)
---

**Barrett reduction** computes $x \bmod n$ for a fixed modulus $n$ without a division. It stores one constant, $\mu = \lfloor 4^k/n \rfloor$ for a modulus of $k$ binary digits, and then reduces any $x < 4^k$, such as the product of two residues, with two multiplications, two shifts, one subtraction and at most two corrections by $n$. Division is several times slower than multiplication in hardware and in multiprecision libraries, so this pays off whenever many reductions use the same modulus: in [modular exponentiation](/modular-exponentiation/) for [RSA](/rsa-cryptosystem/), in the [number theoretic transform](/number-theoretic-transform/), and in hash functions with a fixed prime. Unlike [Montgomery multiplication](/montgomery-multiplication/), it works on ordinary residues and for even moduli. It is one of the two standard algorithms for [modular multiplication](/modular-multiplication/).

## In plain words

To find the remainder of a number after division by $n$, you need to know how many times $n$ fits into it. Division answers that, but division is slow.

Barrett's idea is to compute one fraction once: a scaled copy of one over $n$, rounded down to a whole number. To estimate how many times $n$ fits into a number, multiply the top part of the number by this stored value and drop the low digits, which is a shift. The estimate is never too large, and it is at most two too small.

Then multiply $n$ by the estimate and subtract it from the number. The rest is the remainder, or the remainder plus one or two extra copies of $n$, which a short check removes.

## The problem

**Input.** A modulus $n \ge 1$, given once, and then many integers $x$ with $0 \le x < 4^k$, where $k$ is the number of binary digits of $n$.

**Output.** For each $x$, the remainder $x \bmod n$ in $\{0, \ldots, n - 1\}$.

**Representation and range.** Residues modulo $n$ are the integers $0, \ldots, n - 1$ in binary. The modulus satisfies $2^{k-1} \le n < 2^k$; any $n \ge 1$ is allowed, including $n = 1$, $n = 2$, powers of two, and even moduli. The input range $x < 4^k$ includes every product $ab$ of two residues, since $(n - 1)^2 < 4^k$. The constant satisfies $2^k < \mu \le 2^{k+1}$, with equality only when $n$ is a power of two.

**Cost model.** For a single-word modulus on the [word RAM](/word-ram/) with $w$-digit words, $x$ fits in two words, and the reduction takes $O(1)$ word operations with a double-width product. For a multiprecision modulus of $k$ binary digits in [arbitrary precision](/arbitrary-precision-arithmetic/), the cost is counted in bit operations with $M(k)$ the cost of a $k$-digit multiplication, or in word operations on $k/w$ words with [schoolbook multiplication](/schoolbook-multiplication/). Shifts and subtractions cost $O(k)$ bit operations.

## The algorithm

The quotient $\lfloor x/n \rfloor$ equals $\lfloor (x/2^{k-1}) \cdot (4^k/n) / 2^{k+1} \rfloor$ exactly. Barrett reduction replaces both factors by their floors, $\lfloor x/2^{k-1} \rfloor$ (a shift) and $\mu$ (the stored constant), so the estimate needs one multiplication and one shift.

```pseudo id=main
BARRETT-SETUP(n)                              ▷ once per modulus n ≥ 1
L1  k ← number of binary digits of n            ▷ 2^(k−1) ≤ n < 2^k
L2  μ ← ⌊4^k / n⌋                               ▷ the only division

BARRETT-REDUCE(x)                             ▷ 0 ≤ x < 4^k
L3  q ← ⌊⌊x / 2^(k−1)⌋ · μ / 2^(k+1)⌋           ▷ two shifts and one product: Q − 2 ≤ q ≤ Q
L4  r ← x − q · n                               ▷ 0 ≤ r < 3n and r ≡ x (mod n)
L5  while r ≥ n: r ← r − n                      ▷ at most two passes
L6  return r

BARRETT-MULMOD(a, b)                          ▷ 0 ≤ a, b < n
L7  return BARRETT-REDUCE(a · b)
```

Here $Q = \lfloor x/n \rfloor$ is the true quotient. Line L3 never overestimates it, so $r$ in line L4 is never negative, and it underestimates by at most $2$, so line L5 makes at most two subtractions.

## Example

Take $n = 47$, as in HAC, Example 14.46. Then $k = 6$, since $32 \le 47 < 64$, and $\mu = \lfloor 4096/47 \rfloor = 87$. The input range is $0 \le x < 4096$. HAC works in base $4$, so it shifts by $4^2$ instead of $2^5$ and its intermediate values differ, but it gets the same $\mu = 87$, $q = 75$ and result $36$ for $x = 3561$.

| $n$ | $\mu$ | $x$ | $\lfloor x/2^{k-1} \rfloor$ | product with $\mu$ | $q$ (L3) | $Q = \lfloor x/n \rfloor$ | $r$ (L4) | passes of L5 | result |
|---|---|---|---|---|---|---|---|---|---|
| $47$ | $87$ | $3561$ | $111$ | $9657$ | $\lfloor 9657/128 \rfloor = 75$ | $75$ | $36$ | $0$ | $36$ |
| $47$ | $87$ | $46 \cdot 46 = 2116$ | $66$ | $5742$ | $\lfloor 5742/128 \rfloor = 44$ | $45$ | $48$ | $1$ | $1$ |
| $50$ | $81$ | $47 \cdot 49 = 2303$ | $71$ | $5751$ | $\lfloor 5751/128 \rfloor = 44$ | $46$ | $103$ | $2$ | $3$ |

For $n = 50$, again $k = 6$ and $\mu = \lfloor 4096/50 \rfloor = 81$. The last row shows that two corrections do occur, even for a product of two residues. Among all products $ab$ with $0 \le a \le b < n$ and $1 \le n < 400$, about $59\%$ need no correction, about $41\%$ need one, and only $1191$ need two.

## Correctness

Let $a = x/2^{k-1}$ and $b = 4^k/n$. Then $ab/2^{k+1} = x/n$ exactly, and line L3 computes $\lfloor \lfloor a \rfloor \lfloor b \rfloor / 2^{k+1} \rfloor$. Rounding both factors down can only lower the product, so $q \le Q$. Each factor loses less than $1$, and the other factor is at most $2^{k+1}$, because $x < 4^k$ and $n \ge 2^{k-1}$. So the product loses less than $2^{k+2}$, which is less than $2$ after division by $2^{k+1}$, and $q \ge Q - 2$. Line L4 then gives $r = (Q - q)n + (x \bmod n)$ with $Q - q \in \{0, 1, 2\}$, and line L5 removes the extra copies of $n$. The full proof is in `proofs/correctness.md`.

## Complexity

With $k$-digit operands, $\lfloor x/2^{k-1} \rfloor$ has at most $k + 1$ binary digits and $\mu$ at most $k + 2$, so line L3 is one multiplication of about $k$ by $k$ digits. The estimate $q \le Q < 2^{k+1}$ also has about $k$ digits, so line L4 is a second such multiplication. The shifts, the subtraction and the at most two corrections cost $O(k)$.

| measure | bound |
|---|---|
| multiplications per reduction | $2$, each about $k \times k$ digits |
| corrections in line L5 | at most $2$ |
| bit operations per reduction | $2M(k) + O(k)$, so $O(k^2)$ with schoolbook multiplication |
| word operations, schoolbook | $\Theta((k/w)^2)$, about $2(k/w)^2$ word products |
| single-word modulus | $O(1)$ word operations with double-width products |
| precomputation of $\mu$ | one division of $4^k$ by $n$: $O(k^2)$ schoolbook, $O(M(k))$ with [Newton's method](/newton-raphson-division/) |
| extra space | $\Theta(k/w)$ words for $\mu$ and the intermediate values |

The best and worst cases differ only in the number of corrections, so both are $\Theta((k/w)^2)$ word operations with schoolbook products. A plain division of a $2k$-digit number by a $k$-digit number has the same asymptotic cost with schoolbook arithmetic, but a much larger constant factor, and on hardware a division instruction is slower than two multiplications.

## Properties

- **Deterministic and iterative.** No random choices and no recursion; the correction loop runs at most twice.
- **Ordinary residues.** Inputs and outputs are plain residues, so no conversion is needed, unlike the Montgomery form.
- **Any modulus.** It works for even moduli and for $n = 1$, where Montgomery multiplication needs an odd $n$.
- **Never overestimates.** The quotient estimate is a lower bound, so the intermediate $r$ is never negative and unsigned arithmetic suffices.
- **Data-dependent corrections.** The number of passes in line L5 depends on $x$, which leaks timing information unless the corrections are done with masks.

## Variants and improvements

- **Base $b$ digits (HAC, Algorithm 14.42).** With a radix $b = 2^w$ and $k$ base-$b$ digits, $\mu = \lfloor b^{2k}/n \rfloor$ and $q = \lfloor \lfloor x/b^{k-1} \rfloor \mu / b^{k+1} \rfloor$. The same bound $Q - 2 \le q \le Q$ holds, and since $r < 3n < b^{k+1}$ for $b > 3$, line L4 can be computed modulo $b^{k+1}$ from the low $k + 1$ digits of $x$ and of $qn$.
- **Short products.** Only the high half of $\lfloor x/b^{k-1} \rfloor \mu$ is needed, and only the low $k + 1$ digits of $qn$. Computing only those halves saves about half of the work with schoolbook arithmetic (HAC, Note 14.45; Brent and Zimmermann, Section 2.4.1).
- **Full-precision estimate.** Without the first shift, $q = \lfloor x\mu / 4^k \rfloor$ is at most one below $Q$, at the cost of a longer product. This is the usual form for single-word moduli: with $1 < n < 2^{32}$ and $\mu = \lfloor 2^{64}/n \rfloor$, the estimate is the high word of a 64 by 64 digit product.
- **One shift instead of two (Brent and Zimmermann, Algorithm 2.5).** For a base $\beta$ and a divisor $\beta/2 < B < \beta$, take $I = \lfloor \beta^2/B \rfloor$ and $q = \lfloor \lfloor A/\beta \rfloor I / \beta \rfloor$ for $A < \beta^2$. This drops one more low digit of $A$, and needs up to three corrections; the bound is reached for $A = 1980$, $B = 36$, $\beta = 64$ (Theorem 2.4). The [Granlund-Montgomery division](/granlund-montgomery-division/) by invariant integers refines the same idea for division by a constant word.
- **FFT range.** With full products the cost is $2M(k)$. In the FFT range, the wrap-around trick lowers it to about $1.5M(k)$, and storing the forward transforms of $\mu$ and $n$ lowers it to about $M(k)$ (Brent and Zimmermann, Section 2.4.1).

## When to use it

Use Barrett reduction when many reductions share one modulus and the operands are ordinary residues: a fixed prime in a hash function or a number theoretic transform, a modulus that is even, or a computation with few products per reduction, where the conversions into and out of Montgomery form would not pay off. For long exponentiations with an odd modulus, Montgomery multiplication is usually a little faster in software, because its corrections and shifts work from the low end. For a single reduction, use ordinary division: the setup costs one division anyway.

## Pitfalls

- **Input range.** The bound on the corrections needs $x < 4^k$. A sum of several products, or a product of unreduced values, can exceed it and needs more corrections or a prior reduction.
- **Overflow of the product.** In fixed-width code, $\lfloor x/2^{k-1} \rfloor \cdot \mu$ has about $2k + 3$ binary digits. With a 64-digit word and a 32-digit modulus, it needs the high half of a 128-digit product, or a smaller modulus.
- **Power-of-two moduli.** For $n = 2^{k-1}$, $\mu = 2^{k+1}$ has one more digit than for other moduli of the same length; a fixed buffer of $k + 1$ digits overflows.
- **Timing.** A data-dependent loop in line L5 can leak secret operands in cryptographic code, as in a [timing attack](/timing-attack/). Replace it by two masked subtractions.
- **Setup per modulus.** The constant $\mu$ belongs to one modulus. Reusing it for another modulus gives wrong results without any error.

## Implementations

The Python version follows the main block line by line, with `>>` for the floors of the powers of two, and adds an exponentiation with Barrett products. Python integers have arbitrary size, so the same code serves single-word and multiprecision moduli. The tests compare it with Python's `%` and `pow` for all inputs below $4^k$ for $n < 130$, and on random inputs for moduli $1$, $2$, powers of two, primes, composites and numbers of several hundred digits, and they check that line L5 never makes more than two passes.

## History

Paul Barrett presented the method at CRYPTO '86, in a paper on an implementation of RSA on a standard digital signal processor, where a division was much slower than a multiplication. The Handbook of Applied Cryptography (1996) gave the multiprecision form with the low-digit trick of line L4 and the bound of two corrections. Brent and Zimmermann describe it as the standard method for division by a fixed divisor and analyse its cost with fast multiplication.

## References
