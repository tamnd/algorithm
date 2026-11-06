---
tag: 8K64HH
kind: theorem
slug: euler-theorem
name: Euler's theorem
aliases:
- Euler-Fermat theorem
area: number-theory/modular-arithmetic
level: core
summary: If gcd(a, n) = 1 then a^phi(n) ≡ 1 (mod n).
prereqs: [euler-totient, fermat-little-theorem, congruence, coprime-integers]
see_also: [lagranges-theorem-group-theory, carmichael-function, multiplicative-group-modulo-n, multiplicative-order, modular-inverse, rsa-cryptosystem, binary-exponentiation, chinese-remainder-theorem]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.3, Modular arithmetic (groups modulo n and Lagrange's theorem), Section 31.6, Powers of an element (Euler's theorem), and Section 31.7, The RSA public-key cryptosystem (the correctness of RSA)
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Chapter 6, Fermat's theorem and its consequences (Fermat's theorem in Euler's form, for a modulus m and a coprime to m)
  - book: isbn:9780521516440
    title: Victor Shoup, A Computational Introduction to Number Theory and Algebra, second edition
    locator: Section 2.7, Euler's theorem and Fermat's little theorem
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 2.4.3, Fact 2.126 (Euler's theorem and the reduction of exponents modulo phi(n) for a product of distinct primes)
  - url: https://en.wikipedia.org/wiki/Euler%27s_theorem
    title: Euler's theorem, Wikipedia
    locator: section History (Euler's 1736 proof of Fermat's theorem and his 1763 proof of the general case)
---

Euler's theorem says that if an integer $a$ is [coprime](/coprime-integers/) to a positive integer $n$, then $a^{\varphi(n)} \equiv 1 \pmod n$, where $\varphi$ is [Euler's totient function](/euler-totient/). It extends [Fermat's little theorem](/fermat-little-theorem/) from primes to all moduli, and it is the reason that exponents can be reduced modulo $\varphi(n)$. It proves that [RSA](/rsa-cryptosystem/) decryption inverts encryption, and it gives the inverse $a^{-1} \equiv a^{\varphi(n) - 1}$. In group terms it is [Lagrange's theorem](/lagranges-theorem-group-theory/) applied to the [multiplicative group modulo n](/multiplicative-group-modulo-n/).

## Statement

**Theorem (Euler).** Let $n \ge 1$ and let $a$ be an integer with $\gcd(a, n) = 1$. Then

$$a^{\varphi(n)} \equiv 1 \pmod n.$$

**Corollary (reduction of exponents).** If $\gcd(a, n) = 1$ and $s \equiv t \pmod{\varphi(n)}$ with $s, t \ge 0$, then $a^s \equiv a^t \pmod n$.

**Corollary (orders).** If $\gcd(a, n) = 1$, the [multiplicative order](/multiplicative-order/) of $a$ modulo $n$, the least $d \ge 1$ with $a^d \equiv 1$, divides $\varphi(n)$.

**Extension to all bases.** Let $n = \prod p_i^{e_i}$ and $E = \max_i e_i$ (with $E = 0$ for $n = 1$). For every integer $a$ and every $k \ge E$,

$$a^{k + \varphi(n)} \equiv a^{k} \pmod n.$$

For $n = 1$ every statement is trivial, since all integers are congruent modulo $1$.

## In plain words

Pick a modulus, and a number that shares no factor with it. Count how many numbers below the modulus share no factor with it; call that count the totient. Raise the number to the power of the totient, and divide by the modulus. The remainder is always one.

So the powers of the number, read modulo the modulus, repeat with a period that divides the totient. To find a huge power, you only need the exponent modulo the totient.

Fermat's little theorem is the special case of a prime modulus, where the totient is one less than the prime. The proof is the same reshuffle of remainders: multiplying all the invertible remainders by the number only reorders them.

## Proof

**Proof by permutation of the reduced residues.** Let $r_1, \ldots, r_k$ with $k = \varphi(n)$ be the integers in $1$ to $n$ that are coprime to $n$, a *reduced residue system*.

1. Each $a r_i$ is coprime to $n$. A prime that divides $n$ and $a r_i$ divides $a$ or $r_i$ by [Euclid's lemma](/euclids-lemma/), and both are coprime to $n$.
2. So $a r_i \bmod n$ is coprime to $n$, because $\gcd(a r_i \bmod n, n) = \gcd(a r_i, n) = 1$. Thus it equals some $r_j$ (for $n = 1$, the single residue is $r_1 = 1 \equiv 0$, and the claim is trivial).
3. The map $i \mapsto j$ is injective. If $a r_i \equiv a r_{i'} \pmod n$, then $n \mid a(r_i - r_{i'})$, and since $\gcd(a, n) = 1$, $n \mid r_i - r_{i'}$ by the cancellation rule for [congruences](/congruence/). Both are in $1$ to $n$, so $r_i = r_{i'}$.
4. An injective map of a finite set to itself is a bijection, so $a r_1, \ldots, a r_k$ are congruent to $r_1, \ldots, r_k$ in some order. Multiply all of them:
$$a^{k} \, r_1 r_2 \cdots r_k \equiv r_1 r_2 \cdots r_k \pmod n.$$
5. The product $R = r_1 \cdots r_k$ is coprime to $n$, by step 1 applied to each factor. So $R$ can be cancelled, and $a^{\varphi(n)} \equiv 1 \pmod n$. $\square$

**Proof by Lagrange's theorem.** The residues coprime to $n$ form a group $(\mathbb{Z}/n\mathbb{Z})^*$ under multiplication, of order $\varphi(n)$. The powers of $a$ form a subgroup whose order is the order $d$ of $a$. By [Lagrange's theorem](/lagranges-theorem-group-theory/), $d \mid \varphi(n)$, so $a^{\varphi(n)} = (a^d)^{\varphi(n)/d} = 1$. $\square$

**The corollaries.** For the reduction of exponents, let $s = t + q \varphi(n)$ with $q \ge 0$ (else swap $s$ and $t$); then $a^s = a^t (a^{\varphi(n)})^q \equiv a^t$. For the order $d$ of $a$, write $\varphi(n) = qd + r$ with $0 \le r < d$; then $1 \equiv a^{\varphi(n)} = (a^d)^q a^r \equiv a^r$, so $r = 0$ by the minimality of $d$.

**Proof of the extension.** Fix a prime power $p^e$ that exactly divides $n$; then $e \le E \le k$.

- If $p \mid a$, then $p^k \mid a^k$, and $p^e \mid p^k$, so both $a^k$ and $a^{k + \varphi(n)}$ are $\equiv 0 \pmod{p^e}$.
- If $p \nmid a$, then $\gcd(a, p^e) = 1$, and the theorem for the modulus $p^e$ gives $a^{\varphi(p^e)} \equiv 1 \pmod{p^e}$. Since $\varphi$ is multiplicative, $\varphi(p^e) \mid \varphi(n)$, so $a^{\varphi(n)} \equiv 1$ and $a^{k + \varphi(n)} \equiv a^k \pmod{p^e}$.

So $p^e$ divides $a^{k + \varphi(n)} - a^k$ for each prime power $p^e$ in $n$. These prime powers are pairwise coprime, so their product $n$ divides it too. $\blacksquare$

## Consequences

- **Exponent reduction.** The last digit of $7^{222}$: $\gcd(7, 10) = 1$ and $\varphi(10) = 4$, and $222 \equiv 2 \pmod 4$, so $7^{222} \equiv 7^2 = 49 \equiv 9 \pmod{10}$.
- **Inverses.** If $\gcd(a, n) = 1$, then $a^{-1} \equiv a^{\varphi(n) - 1} \pmod n$, computed by [binary exponentiation](/binary-exponentiation/). This needs $\varphi(n)$, so for a general $n$ the [extended Euclidean algorithm](/extended-euclidean-algorithm/) is the better method for a [modular inverse](/modular-inverse/).
- **RSA.** Let $n = pq$ and $ed \equiv 1 \pmod{\varphi(n)}$. For a message $m$ with $\gcd(m, n) = 1$, $(m^e)^d = m^{1 + q\varphi(n)} \equiv m \pmod n$. For $n = 3233 = 61 \cdot 53$, $\varphi(n) = 3120$, $e = 17$ and $d = 2753$ (since $17 \cdot 2753 = 46801 = 15 \cdot 3120 + 1$): the message $65$ encrypts to $65^{17} \bmod 3233 = 2790$, and $2790^{2753} \bmod 3233 = 65$. Messages that share a factor with $n$ are also decrypted correctly, because $n$ is square-free; this follows from the extension with $E = 1$, or from Fermat's theorem modulo $p$ and $q$ and the [Chinese remainder theorem](/chinese-remainder-theorem/).
- **Periods of decimal fractions.** If $\gcd(10, n) = 1$, the decimal expansion of $1/n$ is purely periodic, and its period is the order of $10$ modulo $n$, which divides $\varphi(n)$.
- **Orders and generators.** The order of each unit divides $\varphi(n)$. A unit of order exactly $\varphi(n)$ is a [primitive root](/primitive-root/).

## Tightness

**Coprimality is needed.** For $n = 4$ and $a = 2$, $2^{\varphi(4)} = 2^2 = 4 \equiv 0 \pmod 4$. If $\gcd(a, n) = g > 1$, then every power $a^j$ with $j \ge 1$ is divisible by $g$, so no positive power is $\equiv 1$. The extension shows what survives: $2^{k + 4} \equiv 2^k \pmod{12}$ for $k \ge 2$, for example $2^6 = 64 \equiv 4 = 2^2$.

**The exponent $\varphi(n)$ is not always the least one.** The least exponent that works for all units is the [Carmichael function](/carmichael-function/) $\lambda(n)$, which divides $\varphi(n)$. Modulo $8$, the four units $1, 3, 5, 7$ all satisfy $a^2 \equiv 1$, so $\lambda(8) = 2 < \varphi(8) = 4$. Modulo $12$, also $a^2 \equiv 1$ for the units $1, 5, 7, 11$, while $\varphi(12) = 4$.

**When it is tight.** The exponent $\varphi(n)$ is the least one that works for all units exactly when some unit has order $\varphi(n)$, that is, when $n$ has a [primitive root](/primitive-root/). This holds for $n = 1, 2, 4, p^k$ and $2p^k$ with $p$ an odd prime, and only for these ([existence of primitive roots](/primitive-roots-existence/)).

## History

Euler published a proof of Fermat's little theorem in 1736, and he proved the general form for composite moduli in a paper of 1763, in which he also introduced the function now written $\varphi(n)$ (Wikipedia, section History). The theorem is often called the Euler-Fermat theorem. The proof through Lagrange's theorem treats the theorem as a fact about the group of units modulo n; it is the proof that CLRS gives (Sections 31.3 and 31.6).

## References
