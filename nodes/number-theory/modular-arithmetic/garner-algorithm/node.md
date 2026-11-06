---
tag: PHSQZC
kind: algorithm
slug: garner-algorithm
name: Garner's algorithm
aliases:
- mixed-radix CRT reconstruction
area: number-theory/modular-arithmetic
level: advanced
summary: Reconstructs the CRT solution in mixed-radix form using only small modular operations.
solves: [chinese-remainder-problem]
model: word-ram
complexity:
  vars: {t: the number of moduli, k: the number of binary digits of the largest modulus}
  time: {worst: Θ(t^2), best: Θ(t^2)}
  space: {extra: Θ(t)}
  bit_operations: {worst: O(t^2 k^2)}
properties: {deterministic: true, recursive: false}
history:
  year: 1959
  people: [Harvey L. Garner]
  note: Garner described the conversion from residues to mixed-radix digits in his paper on the residue number system for computer arithmetic.
prereqs: [chinese-remainder-theorem, modular-inverse, residue-number-system]
see_also: [chinese-remainder-problem, horner-rule, newton-interpolation, rsa-cryptosystem, number-theoretic-transform, extended-euclidean-algorithm, subproduct-tree, lagrange-interpolation]
sources:
  - paper: doi:10.1109/TEC.1959.5219515
    title: Harvey L. Garner, The residue number system, IRE Transactions on Electronic Computers EC-8 (2), 1959
    locator: pages 140 to 147 (conversion from residue to mixed-radix representation)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1997
    locator: Section 14.5.2, Garner's algorithm (Algorithm 14.71, Fact 14.72, Example 14.73 with moduli 5, 7, 11, 13 and x = 2192, Note 14.74 on efficiency, Note 14.75 on RSA decryption); Section 14.8, Notes (attribution to Garner)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.3.2, Modular arithmetic (conversion from residues to mixed-radix notation with precomputed constants c_ij)
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 2.7, Chinese remainder theorem (Algorithm 2.16 RNSToInteger, a subquadratic reconstruction) and Section 2.9, Notes and references
  - url: https://cp-algorithms.com/algebra/garners-algorithm.html
    title: Garner's algorithm, cp-algorithms
    locator: sections Mixed Radix Representation and Garner's algorithm (the constants r_ij and the O(k^2) digit computation) and Implementation of Garner's Algorithm (big numbers with 100 primes)
---

**Garner's algorithm** solves the [Chinese remainder problem](/chinese-remainder-problem/) for pairwise coprime moduli $m_1, \ldots, m_t$: from residues $v_i$ it finds the unique $x$ with $0 \le x < M = m_1 \cdots m_t$ and $x \equiv v_i \pmod{m_i}$. Instead of the classical formula of the [Chinese remainder theorem](/chinese-remainder-theorem/), which adds large multiples of $M/m_i$ and reduces modulo $M$, it computes the digits of $x$ in the *mixed radix* $(m_1, \ldots, m_t)$,
$$x = u_1 + u_2 m_1 + u_3 m_1 m_2 + \cdots + u_t m_1 \cdots m_{t-1}, \qquad 0 \le u_i < m_i,$$
one digit at a time, with arithmetic modulo $m_i$ only. When each modulus fits in a machine word, every step uses word operations, and only the final evaluation of $x$ from its digits needs [arbitrary precision](/arbitrary-precision-arithmetic/). This makes it the standard way back from a [residue number system](/residue-number-system/): in multi-modular computations, in the [number theoretic transform](/number-theoretic-transform/) with several primes, and in the two-prime case of [RSA](/rsa-cryptosystem/) decryption.

## In plain words

You know the remainders of an unknown number after division by several numbers that share no factors. You want the number itself.

Build it in stages. The first remainder already gives a number that is right for the first divisor. To also fix the second divisor, add a multiple of the first divisor: this does not spoil the first remainder. Choose how many times to add it by a small calculation that only uses the second divisor. Then add a multiple of the first two divisors multiplied together to fix the third, and so on.

The "how many times" values are the digits of the answer in a number system where each place has its own base. Every digit comes from small numbers only. The big answer is assembled once, at the end.

## The problem

**Input.** Moduli $m_1, \ldots, m_t \ge 1$, pairwise coprime, and residues $v_1, \ldots, v_t$. Usually the moduli are fixed and many residue vectors are converted.

**Output.** The unique integer $x$ with $0 \le x < M = m_1 \cdots m_t$ and $x \equiv v_i \pmod{m_i}$ for all $i$, and its mixed-radix digits $u_1, \ldots, u_t$. If the moduli are not pairwise coprime, the setup reports it.

**Representation and range.** Each residue is an integer, reduced to $\{0, \ldots, m_i - 1\}$ when used. The digits satisfy $0 \le u_i < m_i$, so each digit has the size of its modulus. Any moduli $m_i \ge 1$ are allowed, including $m_i = 1$, $m_i = 2$, powers of two and composite numbers, as long as they are pairwise coprime. The empty system, $t = 0$, has $M = 1$ and the answer $0$. Write $P_0 = 1$ and $P_i = m_1 \cdots m_i$.

**Cost model.** For moduli that fit in a word of the [word RAM](/word-ram/), each operation modulo $m_i$ costs $O(1)$ word operations with a double-width product, and the result $x$ has at most $t$ words. For moduli of $k$ binary digits in arbitrary precision, the cost is counted in bit operations, $O(k^2)$ per operation modulo $m_i$ with schoolbook arithmetic. The setup is counted separately, since it is done once for fixed moduli.

## The algorithm

The setup stores $C_i = P_{i-1}^{-1} \bmod m_i$. Digit $i$ must make $x_i = x_{i-1} + u_i P_{i-1}$ congruent to $v_i$ modulo $m_i$, so $u_i = (v_i - x_{i-1}) C_i \bmod m_i$. The value $x_{i-1} \bmod m_i$ is found from the earlier digits by [Horner's rule](/horner-rule/) modulo $m_i$, so no large number appears.

```pseudo id=main
GARNER-SETUP(m_1, ..., m_t)                    ▷ once for fixed moduli
L1  for i ← 2 to t:
L2      p ← m_1 · m_2 ⋯ m_(i−1) mod m_i            ▷ reduced after each factor
L3      (g, C_i) ← extended Euclid on (p, m_i)     ▷ C_i = P_(i−1)^(−1) mod m_i
L4      if g ≠ 1: fail                            ▷ m_i shares a factor with an earlier modulus

GARNER(v_1, ..., v_t)
L5  u_1 ← v_1 mod m_1
L6  for i ← 2 to t:
L7      s ← u_(i−1) mod m_i
L8      for j ← i − 2 downto 1:
L9          s ← (s · m_j + u_j) mod m_i            ▷ after the loop, s = x_(i−1) mod m_i
L10     u_i ← (v_i − s) · C_i mod m_i              ▷ the next mixed-radix digit
L11 x ← u_t
L12 for i ← t − 1 downto 1: x ← x · m_i + u_i      ▷ the only large numbers
L13 return x
```

Lines L5 to L10 use only residues modulo the $m_i$; the digits alone already determine $x$, and they can be used directly, for example to compare two numbers.

## Example

Take $m = (5, 7, 11, 13)$, $M = 5005$ and $v = (2, 1, 3, 8)$, as in HAC, Example 14.73. The setup gives $C_2 = 5^{-1} \bmod 7 = 3$, $C_3 = 35^{-1} \equiv 2^{-1} \equiv 6 \pmod{11}$ and $C_4 = 385^{-1} \equiv 8^{-1} \equiv 5 \pmod{13}$.

| $i$ | $m_i$ | $C_i$ | $s = x_{i-1} \bmod m_i$ (L7 to L9) | $u_i$ (L10) | $x_i = x_{i-1} + u_i P_{i-1}$ |
|---|---|---|---|---|---|
| $1$ | $5$ | | | $2$ | $2$ |
| $2$ | $7$ | $3$ | $2$ | $(1 - 2) \cdot 3 \equiv 4$ | $2 + 4 \cdot 5 = 22$ |
| $3$ | $11$ | $6$ | $4 \cdot 5 + 2 = 22 \equiv 0$ | $(3 - 0) \cdot 6 = 18 \equiv 7$ | $22 + 7 \cdot 35 = 267$ |
| $4$ | $13$ | $5$ | $(7 \cdot 7 + 4) \cdot 5 + 2 \equiv 1 \cdot 5 + 2 = 7$ | $(8 - 7) \cdot 5 = 5$ | $267 + 5 \cdot 385 = 2192$ |

So the digits are $(2, 4, 7, 5)$ and $x = 2192$. Check: $2192 = 438 \cdot 5 + 2 = 313 \cdot 7 + 1 = 199 \cdot 11 + 3 = 168 \cdot 13 + 8$. The pairs $(u_i, x_i)$ agree with the triples $(i, u, x)$ listed in HAC.

**Two moduli, as in RSA.** For $n = 3233 = 61 \cdot 53$, private exponent $d = 2753$ and ciphertext $c = 2790$, decryption modulo the primes gives $c^{53} \bmod 61 = 4$ and $c^{49} \bmod 53 = 12$, with $53 = d \bmod 60$ and $49 = d \bmod 52$. With $C_2 = 61^{-1} \bmod 53 = 20$, the one step gives $u_2 = (12 - 4) \cdot 20 \bmod 53 = 1$ and $x = 4 + 1 \cdot 61 = 65$, which is $c^d \bmod 3233$.

## Correctness

The setup succeeds exactly when $\gcd(P_{i-1}, m_i) = 1$ for every $i$, which is pairwise coprimality, and then $C_i P_{i-1} \equiv 1 \pmod{m_i}$. By induction on $i$, the partial value $x_i = u_1 + u_2 P_1 + \cdots + u_i P_{i-1}$ satisfies $0 \le x_i < P_i$ and $x_i \equiv v_j \pmod{m_j}$ for all $j \le i$. The Horner loop computes $s \equiv x_{i-1} \pmod{m_i}$. Then
$$x_i = x_{i-1} + u_i P_{i-1} \equiv s + (v_i - s) C_i P_{i-1} \equiv v_i \pmod{m_i},$$
the added term is a multiple of every earlier $m_j$, and $x_i \le (P_{i-1} - 1) + (m_i - 1) P_{i-1} = P_i - 1$. Lines L11 and L12 evaluate $x_t$ by Horner's rule. Two solutions differ by a multiple of each $m_i$, hence of $M$, so the answer in $[0, M)$ is unique. The full proof is in `proofs/correctness.md`.

## Complexity

For digit $i$, the Horner loop makes $i - 2$ multiply-add steps modulo $m_i$, and line L10 makes one more multiplication, so the digits take $t(t - 1)/2$ multiplications modulo the $m_i$ in total. The final evaluation in line L12 multiplies a number of $i$ words by one word for $i = 1, \ldots, t - 1$.

| measure | bound |
|---|---|
| multiplications modulo the $m_i$, digits | $t(t - 1)/2$ |
| setup | $(t - 1)(t - 2)/2$ multiplications and $t - 1$ inversions, done once |
| word operations, word-sized moduli | $\Theta(t^2)$: $\Theta(t^2)$ for the digits and $\Theta(t^2)$ for line L12 |
| bit operations, $k$-digit moduli | $O(t^2 k^2)$ with schoolbook arithmetic |
| stored constants | $t - 1$ values $C_i$, each smaller than its modulus |
| extra space | $\Theta(t)$ digits, plus the output $x$ |

The classical formula $x = \sum_i v_i (M/m_i) \left((M/m_i)^{-1} \bmod m_i\right) \bmod M$ also takes $\Theta(t^2)$ word operations to form the sum, but it ends with a reduction modulo the large $M$, which Garner's algorithm avoids (HAC, Note 14.74). For very many moduli, a divide-and-conquer reconstruction with product trees costs $O(M(n) \log n)$ for $M$ of $n$ binary digits, where $M(n)$ is the cost of an $n$-digit multiplication (Brent and Zimmermann, Algorithm 2.16).

## Properties

- **Deterministic and iterative.** Nested loops only, with no random choices and no recursion.
- **Small arithmetic.** The digits need only operations modulo the $m_i$; with word-sized moduli, everything except line L12 fits in words.
- **Incremental.** Adding a modulus $m_{t+1}$ adds one constant and one digit; the earlier digits do not change.
- **Mixed-radix output.** The digits give the most significant part of $x$ first in $u_t$, so two numbers in residue form can be compared, and their sign decided, from their digits without building $x$.
- **Order of moduli.** Any order works, but it changes the digits, and the setup depends on it.
- **Exact.** With $x < M$ guaranteed, there is no rounding and no final correction.

## Variants and improvements

- **Pairwise constants (Knuth; cp-algorithms).** Store $r_{ji} = m_j^{-1} \bmod m_i$ for all $j < i$, and compute $u_i = \big(\cdots((v_i - u_1) r_{1i} - u_2) r_{2i} - \cdots - u_{i-1}\big) r_{i-1,i} \bmod m_i$. This needs $t(t - 1)/2$ constants instead of $t - 1$, and the same order of work.
- **Large accumulator (HAC, Algorithm 14.71).** Keep $x_{i-1}$ as a large integer and compute $u_i = (v_i - x_{i-1}) C_i \bmod m_i$ directly. This needs a reduction of a large number by $m_i$ in every step, but no separate evaluation.
- **Two moduli (HAC, Note 14.75).** For $n = pq$, the whole algorithm is $x = v_1 + \big((v_2 - v_1) (p^{-1} \bmod q) \bmod q\big) p$. RSA implementations decrypt modulo $p$ and $q$ separately and combine the results this way, which is about four times faster than one exponentiation modulo $n$ with schoolbook arithmetic.
- **Signed results.** If the true result may be negative and $|x| < M/2$, take $x - M$ when $x \ge M/2$. Multi-modular computations of determinants, which can be negative, use this form; the [Bareiss algorithm](/bareiss-algorithm/) is the exact alternative without moduli.
- **Subquadratic reconstruction.** Split the moduli in two halves, solve each half recursively, and combine the two results with one Bezout pair, as in Algorithm 2.16 of Brent and Zimmermann, with [subproduct trees](/subproduct-tree/) for the products.
- **Moduli that are not coprime.** The general Chinese remainder problem needs gcd steps and may have no solution; see the [Chinese remainder problem](/chinese-remainder-problem/).
- **Polynomials.** For moduli $X - a_i$ over a field, the mixed-radix digits are the coefficients of the [Newton form](/newton-interpolation/) of the interpolating polynomial, and the classical formula is [Lagrange interpolation](/lagrange-interpolation/).

## When to use it

Use Garner's algorithm to convert from a residue number system with fixed moduli back to an ordinary integer, in particular when the moduli are word-sized primes: multi-modular big-integer arithmetic, [number theoretic transforms](/number-theoretic-transform/) with two or three primes whose results exceed any one prime, exact linear algebra by computing modulo many primes, and CRT-based RSA decryption. Use the mixed-radix digits alone when only comparison or sign is needed. For thousands of moduli, prefer a subquadratic product-tree method; for moduli that may share factors, use the general method of the Chinese remainder problem.

## Pitfalls

- **Pairwise coprimality.** With a shared factor, $C_i$ does not exist. The setup must check it; skipping the check gives wrong results without any error.
- **Negative intermediate values.** In line L10, $v_i - s$ can be negative. Reduce it into $[0, m_i)$ before an unsigned multiplication, or the result is wrong in C-like languages.
- **Overflow.** With word-sized $m_i$, the products in lines L9 and L10 need double-width arithmetic; $s \cdot m_j$ in line L9 also needs $m_j$ reduced modulo $m_i$ first when $m_j > m_i$.
- **Range of the true answer.** The algorithm returns the representative in $[0, M)$. If the true result can reach $M$ or be negative, choose more moduli or use the signed form.
- **Order of moduli.** The constants $C_i$ belong to one order of the moduli. Reordering the moduli without recomputing them gives wrong digits.

## Implementations

The Python version follows the main block line by line. The setup checks that the moduli are positive and pairwise coprime and stores the constants $C_i$; a second function returns the mixed-radix digits, and the main function evaluates $x$ from them. The tests check the HAC example and the RSA example, all values for several small systems, and random systems against the classical CRT formula computed with Python's `pow`: moduli $1$, $2$, powers of two, primes, composites and numbers of several hundred digits, with the values $0$, $1$ and $M - 1$. They also check that moduli with a common factor are rejected.

## History

Harvey Garner described the conversion from residues to mixed-radix digits in 1959, in his paper on the residue number system as a basis for computer arithmetic, where addition and multiplication work on each modulus separately and in parallel. Knuth discusses the method and its variants in Section 4.3.2 of *Seminumerical Algorithms*. The Handbook of Applied Cryptography (1996) gives it as Algorithm 14.71 and notes its use for RSA decryption with the two prime factors.

## References
