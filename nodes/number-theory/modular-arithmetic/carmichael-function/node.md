---
tag: S21972
kind: concept
slug: carmichael-function
name: Carmichael function
aliases:
- lambda function
- reduced totient
area: number-theory/modular-arithmetic
level: advanced
summary: The exponent of the multiplicative group mod n, the smallest m with a^m ≡ 1 for all coprime a.
prereqs: [euler-totient, multiplicative-order, chinese-remainder-theorem]
see_also: [euler-theorem, carmichael-number, primitive-root, cyclic-group, rsa-cryptosystem, miller-rabin, multiplicative-group-modulo-n, binary-exponentiation]
sources:
  - book: isbn:9780521516440
    title: Victor Shoup, A Computational Introduction to Number Theory and Algebra, second edition
    locator: Section 6.5, the exponent of an abelian group (Theorems 6.39, 6.40 and 6.41, Example 6.67); Section 7.5, Theorem 7.28 (the structure of Z_(p^e)^*); Section 10.4 (the formula for λ(n) and factoring n from a multiple of λ(n)) and Section 10.5 (attribution to Miller)
  - url: https://www.rfc-editor.org/rfc/rfc8017
    title: "K. Moriarty, B. Kaliski, J. Jonsson and A. Rusch, PKCS #1, RSA Cryptography Specifications Version 2.2, RFC 8017, 2016"
    locator: Section 3.1 (λ(n) as the least common multiple of r_i - 1) and Section 3.2 (the private exponent d with e d ≡ 1 mod λ(n))
  - url: https://en.wikipedia.org/wiki/Carmichael_function
    title: Carmichael function, Wikipedia
    locator: lead (defined by Carmichael in 1910), sections Carmichael's theorems, Exponential cycle length, Average value and Minimal order (Erdős, Pomerance and Schmutz, 1991)
---

The **Carmichael function** $\lambda(n)$ is the smallest positive integer $m$ with $a^m \equiv 1 \pmod n$ for every $a$ [coprime](/coprime-integers/) to $n$. In group terms, it is the *exponent* of the [multiplicative group](/multiplicative-group-modulo-n/) $\mathbb{Z}_n^*$: the least common multiple of the [orders](/multiplicative-order/) of its elements. It divides the [Euler totient](/euler-totient/) $\varphi(n)$, which is the order of the group, and it can be much smaller; the two are equal exactly when $\mathbb{Z}_n^*$ is [cyclic](/cyclic-group/), that is, when $n$ has a [primitive root](/primitive-root/). So $\lambda(n)$ is the sharp form of [Euler's theorem](/euler-theorem/). It gives the smallest valid private exponent modulus in [RSA](/rsa-cryptosystem/), the criterion for [Carmichael numbers](/carmichael-number/), and, like $\varphi(n)$, it is easy to compute from the factorization of $n$ and as hard to compute as factoring without it.

## In plain words

Take a clock with $n$ positions and look only at the numbers that share no factor with $n$. If you multiply such a number by itself again and again, you come back to one after some steps. Different numbers need different numbers of steps.

The Carmichael function of $n$ is the smallest step count that brings every one of these numbers back to one at the same time. Euler's totient is also such a count, but often a larger one. The two agree when one number visits all the others before it returns to one. When they differ, the Carmichael function gives the tighter bound.

## The idea

**Definition.** For $n \ge 1$, $\lambda(n)$ is the least $m \ge 1$ with $a^m \equiv 1 \pmod n$ for all $a$ with $\gcd(a, n) = 1$. So $\lambda(1) = \lambda(2) = 1$.

**Basic facts** (Shoup, Section 6.5). Let $G = \mathbb{Z}_n^*$.

- For an integer $k$, $a^k \equiv 1$ for all $a \in G$ if and only if $\lambda(n) \mid k$. The set of such $k$ is a subgroup of $\mathbb{Z}$, so it is $\lambda(n)\mathbb{Z}$.
- The order of each element divides $\lambda(n)$, and $\lambda(n) \mid \varphi(n) = |G|$ by [Lagrange's theorem](/lagranges-theorem-group-theory/).
- *Some element has order exactly $\lambda(n)$* (Shoup, Theorem 6.41). So $\lambda(n)$ is also the largest order of an element, and $G$ is cyclic if and only if $\lambda(n) = \varphi(n)$.

**Formula.** By the [Chinese remainder theorem](/chinese-remainder-theorem/), $\mathbb{Z}_n^* \cong \prod_i \mathbb{Z}_{p_i^{e_i}}^*$ for $n = \prod_i p_i^{e_i}$, and the exponent of a product is the least common multiple of the exponents (Shoup, Theorem 6.40). The groups modulo prime powers are cyclic, except for powers of $2$ from $8$ on (Shoup, Theorem 7.28). This gives

$$\lambda(p^e) = \begin{cases} p^{e-1}(p - 1) & \text{for odd } p, \text{ or } p = 2 \text{ and } e \le 2, \\ 2^{e-2} & \text{for } p = 2 \text{ and } e \ge 3, \end{cases} \qquad \lambda(n) = \operatorname{lcm}_i \lambda(p_i^{e_i}).$$

For $e \ge 3$, the group modulo $2^e$ is $\{\pm 5^k\}$, a product of a group of order $2$ and a cyclic group of order $2^{e-2}$. As a consequence, $\lambda(n) = \varphi(n)$ exactly for $n = 1, 2, 4, p^e$ and $2p^e$ with $p$ an odd prime.

**Reduction of exponents.** For $\gcd(a, n) = 1$, $a^k \equiv a^{k \bmod \lambda(n)} \pmod n$, which is the best reduction that works for all $a$. For every $a$, coprime or not, $a^{r + \lambda(n)} \equiv a^r \pmod n$ for all $r$ at least the largest exponent $e_i$ in the factorization of $n$. In particular, $a^{\lambda(n) + 1} \equiv a$ for all $a$ when $n$ is squarefree, which is why RSA decryption works even for messages that share a factor with the modulus.

**Computation.** With the factorization of $n$, the formula gives $\lambda(n)$ in time polynomial in $\log n$. Without it, computing $\lambda(n)$ is as hard as factoring: from $n$ and any nonzero multiple $f$ of $\lambda(n)$, a randomized algorithm in the style of [Miller-Rabin](/miller-rabin/) splits $n$ with probability at least $1/2$ per trial. Write $f = 2^h t$ with $t$ odd, choose a random $a$, and look at $a^t, a^{2t}, \ldots$; the last term before the first $1$ gives a square root of $1$ other than $\pm 1$ often enough, and its gcd with $n$ is a proper factor (Shoup, Section 10.4, after Miller).

**Size.** Since $\lambda(n)$ is a least common multiple of numbers $p - 1$, it is small when these share large factors. For example $\lambda(65520) = 12$, while $\varphi(65520) = 13824$. Erdős, Pomerance and Schmutz (1991) proved that $\lambda(n)$ is usually close to $n$ divided by a factor of the size $(\log n)^{\log \log \log n}$, and that it can be as small as a power of $\log n$ with exponent growing like $\log \log \log n$.

## Examples

| $n$ | factorization | $\lambda(n)$ | $\varphi(n)$ | cyclic |
|---|---|---|---|---|
| $8$ | $2^3$ | $2$ | $4$ | no |
| $12$ | $2^2 \cdot 3$ | $\operatorname{lcm}(2, 2) = 2$ | $4$ | no |
| $15$ | $3 \cdot 5$ | $\operatorname{lcm}(2, 4) = 4$ | $8$ | no |
| $32$ | $2^5$ | $8$ | $16$ | no |
| $18$ | $2 \cdot 3^2$ | $6$ | $6$ | yes |
| $561$ | $3 \cdot 11 \cdot 17$ | $\operatorname{lcm}(2, 10, 16) = 80$ | $320$ | no |
| $3233$ | $53 \cdot 61$ | $\operatorname{lcm}(52, 60) = 780$ | $3120$ | no |

- **Element orders.** The orders of the eight units modulo $15$ are $1, 2, 2, 2, 4, 4, 4, 4$. Their maximum and their least common multiple are both $4 = \lambda(15)$, and no unit has order $8$, so $\mathbb{Z}_{15}^*$ is not cyclic (Shoup, Example 6.67).
- **Carmichael numbers.** A composite $n$ is a Carmichael number when $a^{n-1} \equiv 1$ for all units $a$, that is, when $\lambda(n) \mid n - 1$. For $561$, $\lambda(561) = 80$ divides $560$.
- **RSA.** For $n = 3233 = 53 \cdot 61$ and $e = 17$, the private exponent modulo $\lambda(n) = 780$ is $d = 413$, while modulo $\varphi(n) = 3120$ it is $2753$. Both decrypt the ciphertext $2790$ to $65$.
- **Non-squarefree moduli.** Modulo $12$, $2^{\lambda(12) + 1} = 2^3 = 8 \not\equiv 2$, so the rule $a^{\lambda(n) + 1} \equiv a$ needs a squarefree $n$. With $r = 2$, the largest exponent in $12 = 2^2 \cdot 3$, the rule $a^{r + \lambda(n)} \equiv a^r$ holds: $2^4 = 16 \equiv 4 = 2^2$.

## Where it is used

- **RSA.** PKCS #1 (RFC 8017) defines the private exponent by $e d \equiv 1 \pmod{\lambda(n)}$. This gives the smallest valid $d$, and every $d$ that works for all messages is congruent to it modulo $\lambda(n)$.
- **Primality testing.** Carmichael numbers, the composites that every Fermat test with a unit base passes, are exactly the composites with $\lambda(n) \mid n - 1$ (Korselt's criterion in the language of $\lambda$). This is why the [Fermat test](/fermat-primality-test/) is replaced by Miller-Rabin.
- **Factoring from a key.** The algorithm that splits $n$ from a multiple of $\lambda(n)$ shows that an RSA private exponent $d$, with $e d - 1$ a multiple of $\lambda(n)$, reveals the factors of $n$.
- **Exponent reduction.** In a computation of $a^k \bmod n$ with a huge $k$, such as a tower of exponents, $k$ may be reduced modulo $\lambda(n)$, with the correction for non-coprime $a$ above. Then [binary exponentiation](/binary-exponentiation/) works with the smaller exponent.
- **Periods.** The period of the sequence $a, a^2, a^3, \ldots \bmod n$ for a unit $a$ divides $\lambda(n)$, which bounds the period of multiplicative [linear congruential generators](/linear-congruential-generator/) and of decimal expansions of fractions with denominator $n$ coprime to $10$.

## References
