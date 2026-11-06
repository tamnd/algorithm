---
tag: XK14YE
kind: problem
slug: modular-multiplication
name: Modular multiplication
aliases:
- computing a·b mod n quickly
area: number-theory/modular-arithmetic
level: core
summary: Given residues a and b and a modulus n, compute a·b mod n, ideally without a full division for each product.
prereqs: [congruence, division-with-remainder]
see_also: [barrett-reduction, montgomery-multiplication, modular-exponentiation, schoolbook-multiplication, karatsuba-multiplication, granlund-montgomery-division, residue-number-system, word-ram]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.3.1, The Classical Algorithms (Algorithm M, multiplication, and Algorithm D, division), and Section 4.3.3, How Fast Can We Multiply?
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1997
    locator: Section 14.3, Multiple-precision modular arithmetic (14.3.1 classical, 14.3.2 Montgomery and 14.3.3 Barrett reduction)
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 2.4, Modular multiplication (2.4.1 Barrett's algorithm, 2.4.2 Montgomery's multiplication)
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Section 9.2, Enhancements to modular arithmetic (9.2.1 Montgomery method, 9.2.2 Newton methods)
  - paper: doi:10.4007/annals.2021.193.2.4
    title: David Harvey and Joris van der Hoeven, Integer multiplication in time O(n log n), Annals of Mathematics 193(2), 2021, 563 to 617
    locator: Main theorem
---

Modular multiplication is the problem of computing $ab \bmod n$ for residues $0 \le a, b < n$. It is the inner operation of [modular exponentiation](/modular-exponentiation/), and so of RSA, Diffie-Hellman, the Miller-Rabin test and the [number-theoretic transform](/number-theoretic-transform/). The direct method multiplies and then divides by $n$, but division is the slow step, so the main algorithms ([Barrett reduction](/barrett-reduction/) and [Montgomery multiplication](/montgomery-multiplication/)) replace it by multiplications with a constant computed once per modulus. For $k$-digit arbitrary-precision operands the problem has the same cost as integer multiplication, up to a constant factor.

## In plain words

You must multiply two numbers on a clock and give the position where the product lands. The direct way is to compute the full product and then divide by the clock size, keeping only the remainder. The full product is twice as long as the inputs, so on a computer it may not fit in one machine word. Division is also much slower than multiplication, on paper and in hardware. Good methods do some preparation once for a given clock size. After that, each product needs only multiplications, additions and shifts. When you do many products with the same clock size, as in raising a number to a large power, this preparation pays back many times.

## Definition

**Input.** A modulus $n \ge 1$ and residues $a, b \in \{0, \ldots, n - 1\}$.

**Output.** The integer $r = ab \bmod n$, that is, the unique $r \in \{0, \ldots, n - 1\}$ with $r \equiv ab \pmod n$.

**Cost models.**

- *Word-sized.* On the [word RAM](/word-ram/) with $w$-digit binary words, $n < 2^w$. The product $ab$ can need $2w$ binary digits, so the question is how to reduce a double-width value, or how to avoid it, with unit-cost word operations.
- *Arbitrary precision.* The modulus $n$ has $k$ binary digits, and cost is counted in bit operations. $M(k)$ denotes the cost of multiplying two $k$-digit integers: $O(k^2)$ with [schoolbook multiplication](/schoolbook-multiplication/), $O(k^{1.585})$ with [Karatsuba multiplication](/karatsuba-multiplication/), and $O(k \log k)$ by Harvey and van der Hoeven (2021).

**Fixed modulus.** In most uses the same $n$ is used for many products. The problem then has a precomputation phase, which sees only $n$, and a query phase for each pair $(a, b)$. Only the query cost matters when the number of queries is large.

## Variants

- **Single product.** One product, no precomputation. The classical method is the best choice.
- **Many products, one modulus.** Precompute a constant for $n$. Barrett reduction stores $\mu = \lfloor 4^k / n \rfloor$; Montgomery multiplication stores $-n^{-1} \bmod 2^k$ and works on residues in a scaled form.
- **No double-width product.** Some languages have no 128-bit type. The product can be built by add-and-double, as in the example below, with $O(w)$ word operations, or with a floating-point estimate of the quotient.
- **Special moduli.** For $n = 2^k - c$ with a small $c$, such as $2^{127} - 1$ or $2^{255} - 19$, the high part of the product can be folded into the low part: $2^k \equiv c$, so $x = x_1 2^k + x_0 \equiv c x_1 + x_0$. For $n = 2^k$, reduction is a mask.
- **Many moduli.** In a [residue number system](/residue-number-system/) a large number is kept as its residues modulo several word-sized coprime moduli, and a product is one modular multiplication per modulus.
- **Modular squaring.** The case $a = b$, which with schoolbook multiplication needs about half the digit products.

## Examples

| $a$ | $b$ | $n$ | $ab$ | $ab \bmod n$ |
| --- | --- | --- | --- | --- |
| 13 | 11 | 17 | 143 | 7 |
| 123456789 | 987654321 | $10^9 + 7$ | 121932631112635269 | 259106859 |
| $n - 1$ | $n - 2$ | $2^{64} - 59$ | about $3.4 \cdot 10^{38}$ | 2 |
| $a$ | $b$ | 1 | $ab$ | 0 |

In the second row the product has 57 binary digits, so with $n$ near $2^{30}$ it fits in a 64-bit word and a single `%` is enough. In the third row $n = 2^{64} - 59$ is the largest prime below $2^{64}$, and $(n - 1)(n - 2) \equiv (-1)(-2) = 2$. The product has 128 binary digits and does not fit in a 64-bit word: this is the case that needs a wide product, Barrett or Montgomery reduction, or add-and-double.

**Add-and-double.** To compute $13 \cdot 11 \bmod 17$ without forming a product larger than $2n$, scan $b = 11 = 1011_2$ from the low bit and keep $x = 13 \cdot 2^j \bmod 17$:

| bit of $b$ | $x$ | $r$ after the step |
| --- | --- | --- |
| 1 | 13 | 13 |
| 1 | 9 | $13 + 9 = 22 \equiv 5$ |
| 0 | 1 | 5 |
| 1 | 2 | $5 + 2 = 7$ |

The result is 7, and every intermediate value is below $2n$.

## Known algorithms

- **Classical.** Compute $ab$ exactly, then divide by $n$ with [division with remainder](/division-with-remainder/) (Knuth's Algorithm D for many digits). On 64-bit hardware with $n < 2^{64}$, this is one 128-bit product and one 128-by-64 division. With arbitrary precision it costs $O(M(k))$, since division can be done in $O(M(k))$ by Newton's method.
- **[Barrett reduction](/barrett-reduction/)** (1986). Estimate the quotient as $\lfloor \lfloor x / 2^{k-1} \rfloor \mu / 2^{k+1} \rfloor$ with the stored $\mu$, subtract, and correct at most twice. Two multiplications per reduction, no division.
- **[Montgomery multiplication](/montgomery-multiplication/)** (1985). For odd $n$ and $R = 2^k > n$, compute $abR^{-1} \bmod n$ with two multiplications and a shift. Residues are kept in the form $aR \bmod n$, so the factor $R^{-1}$ cancels inside long computations.
- **Add-and-double.** Process $b$ one binary digit at a time, as in the example. It costs $O(w)$ additions and needs only $n < 2^{w-1}$; it is slow but portable.
- **Interleaved reduction.** Blakley's method (1983) folds a reduction into each step of a shift-and-add product, which keeps the partial sums below $2n$; it is common in hardware.
- **Floating-point quotient.** With $n < 2^{63}$ and a floating-point type with a 64-digit mantissa, compute $q \approx ab/n$ in floating point and $r = ab - qn$ in wrapping 64-bit integer arithmetic, then correct $r$ by $\pm n$.
- **Division by a constant.** Since $n$ is fixed, the division by $n$ can be replaced by a multiplication by a precomputed reciprocal and a shift, as in [Granlund-Montgomery division](/granlund-montgomery-division/); Barrett reduction is the multiple-precision form of the same idea.

## Bounds

**Word-sized.** With a double-width product and a double-by-single division, the cost is $O(1)$ word operations. With only single-width multiplication, Barrett or Montgomery reduction with half-words, or add-and-double with $O(w)$ operations, are the usual choices.

**Arbitrary precision, upper bound.** A product costs $M(k)$ and a division of a $2k$-digit number by a $k$-digit number costs $O(M(k))$ (Brent and Zimmermann, Chapter 1 and Section 2.4). So one modular multiplication costs $O(M(k))$, which is $O(k \log k)$ by Harvey and van der Hoeven. Barrett and Montgomery reduction each cost about two multiplications of size $k$ after an $O(M(k))$ precomputation.

**Lower bound.** Modular multiplication is at least as hard as multiplication: for $a, b < 2^k$ and $n = 2^{2k}$, $ab \bmod n = ab$. So its cost is $\Omega(M(k))$ up to a constant factor, and the two problems are equivalent. The trivial bound is $\Omega(k)$, since the output must be written.

## Reductions

- **From integer multiplication.** As in the lower bound, take a modulus larger than the product.
- **To multiplication and division.** $ab \bmod n = ab - n \lfloor ab / n \rfloor$.
- **To multiplication only, for a fixed modulus.** Barrett reduction and Montgomery reduction compute the quotient, or an equivalent, with multiplications by a constant that depends only on $n$.
- **To several word-sized products.** By the [Chinese remainder theorem](/chinese-remainder-theorem/), a product modulo $n = n_1 \cdots n_t$ with coprime $n_i$ can be done as $t$ independent products modulo the $n_i$.

## Applications

- **[Modular exponentiation](/modular-exponentiation/).** Square-and-multiply makes about $1.5 \lg e$ modular multiplications for an exponent $e$; its speed is that of modular multiplication. This is the core of [RSA](/rsa-cryptosystem/), [Diffie-Hellman](/diffie-hellman/) and the [Miller-Rabin test](/miller-rabin/).
- **[Number-theoretic transform](/number-theoretic-transform/).** Each butterfly multiplies by a root of unity modulo a word-sized prime. Montgomery or Shoup-style precomputed multiplication is used for the fixed twiddle factors.
- **Hashing.** A [polynomial rolling hash](/polynomial-rolling-hash/) multiplies by a fixed base modulo a prime such as $2^{61} - 1$, where the special form makes reduction cheap.
- **Linear algebra modulo a prime.** [Gaussian elimination](/gaussian-elimination-modular/) and [multimodular methods](/modular-methods/) do their arithmetic with word-sized primes.
- **Elliptic curve cryptography.** Field arithmetic modulo primes like $2^{255} - 19$ uses special-form reduction.

## References
