---
tag: Y34RMM
kind: theorem
slug: fermat-little-theorem
name: Fermat's little theorem
aliases:
- Fermat's theorem
area: number-theory/modular-arithmetic
level: intro
summary: If p is prime and p does not divide a, then a^(p-1) ≡ 1 (mod p).
prereqs: [congruence, prime-number, euclids-lemma]
see_also: [euler-theorem, lagranges-theorem-group-theory, fermat-primality-test, carmichael-number, fermat-pseudoprime, modular-inverse, primitive-root, wilson-theorem]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.3, Modular arithmetic (Lagrange's theorem), Section 31.6, Powers of an element (Euler's theorem and Fermat's theorem), and Section 31.8, Primality testing (pseudoprimes and Carmichael numbers)
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Chapter 6, Fermat's theorem and its consequences
  - book: isbn:9780521516440
    title: Victor Shoup, A Computational Introduction to Number Theory and Algebra, second edition
    locator: Section 2.7, Euler's theorem and Fermat's little theorem
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 2.4.3, Fact 2.127 (Fermat's theorem and the reduction of exponents modulo p − 1)
  - url: https://en.wikipedia.org/wiki/Fermat%27s_little_theorem
    title: Fermat's little theorem, Wikipedia
    locator: section History (Fermat's letter to Frénicle de Bessy of 18 October 1640, Euler's published proof of 1736, Leibniz's unpublished proof)
---

Fermat's little theorem says that for a [prime](/prime-number/) $p$ and an integer $a$ that $p$ does not divide, $a^{p-1} \equiv 1 \pmod p$. Equivalently, $a^p \equiv a \pmod p$ for every integer $a$. It is the base of the [Fermat primality test](/fermat-primality-test/) and of [Miller-Rabin](/miller-rabin/), it gives the [modular inverse](/modular-inverse/) modulo a prime as $a^{p-2}$, and it lets exponents be reduced modulo $p - 1$. It is the prime case of [Euler's theorem](/euler-theorem/), and both follow from [Lagrange's theorem](/lagranges-theorem-group-theory/) for groups.

## Statement

**Theorem (Fermat).** Let $p$ be a prime number and $a$ an integer with $p \nmid a$. Then

$$a^{p-1} \equiv 1 \pmod p.$$

**Equivalent form.** For each prime $p$ and each integer $a$,

$$a^{p} \equiv a \pmod p.$$

The two forms are equivalent. If $p \nmid a$, multiply the first form by $a$ to get the second. Conversely, if $a^p \equiv a$ and $p \nmid a$, then $\gcd(a, p) = 1$, and $a$ can be cancelled from $a \cdot a^{p-1} \equiv a \cdot 1$ by the cancellation rule of [congruences](/congruence/). If $p \mid a$, both sides of the second form are $0$ modulo $p$, while the first form fails, since $a^{p-1} \equiv 0$.

**Reduction of exponents.** If $p \nmid a$ and $s \equiv t \pmod{p - 1}$ with $s, t \ge 0$, then $a^s \equiv a^t \pmod p$. Write $s = t + k(p-1)$ with $k \ge 0$ (or swap $s$ and $t$); then $a^s = a^t (a^{p-1})^k \equiv a^t$.

## In plain words

Take a prime number and any whole number that the prime does not divide. Multiply the number by itself one time fewer than the prime, and divide by the prime. The remainder is always one.

The reason is a reshuffle. Multiply each of the nonzero remainders by the number. You get the same remainders again, only in another order. So the product of all of them does not change, and the extra factor that the multiplication brought in must act like one.

This fact makes large powers cheap modulo a prime, gives a quick way to divide modulo a prime, and gives a fast test that catches most numbers that are not prime.

## Proof

Two proofs follow. The first uses only cancellation of congruences; the second uses the binomial theorem and proves the form $a^p \equiv a$.

**Proof by permutation of residues.** Let $p \nmid a$. Consider the $p - 1$ numbers

$$a \cdot 1,\ a \cdot 2,\ \ldots,\ a \cdot (p - 1) \pmod p.$$

1. None of them is $0$ modulo $p$. If $p \mid a i$ with $1 \le i \le p - 1$, then by [Euclid's lemma](/euclids-lemma/) $p \mid a$ or $p \mid i$, and both are false.
2. No two of them are congruent. If $a i \equiv a j \pmod p$ with $1 \le i, j \le p - 1$, then $p \mid a(i - j)$, so $p \mid i - j$ by Euclid's lemma, and since $|i - j| < p$, $i = j$.
3. So the residues of $a, 2a, \ldots, (p-1)a$ are $p - 1$ distinct nonzero residues, which means they are $1, 2, \ldots, p - 1$ in some order. The products of the two lists are congruent:
$$a^{p-1} \cdot (p - 1)! \equiv (p - 1)! \pmod p.$$
4. The prime $p$ divides none of $1, 2, \ldots, p - 1$, so by Euclid's lemma it does not divide $(p - 1)!$, and $\gcd((p-1)!, p) = 1$. Cancel $(p - 1)!$ to get $a^{p-1} \equiv 1 \pmod p$. $\square$

**Proof by the binomial theorem.** We prove $a^p \equiv a \pmod p$ for all integers $a$.

1. For $0 < k < p$, the prime $p$ divides the binomial coefficient $\binom{p}{k}$. Indeed $k! \, (p - k)! \binom{p}{k} = p!$, so $p$ divides the left side. Each factor of $k!$ and of $(p-k)!$ is between $1$ and $p - 1$, so by Euclid's lemma $p$ divides neither $k!$ nor $(p-k)!$. Hence $p \mid \binom{p}{k}$.
2. By the binomial theorem, $(b + 1)^p = b^p + \sum_{k=1}^{p-1} \binom{p}{k} b^k + 1 \equiv b^p + 1 \pmod p$ for each integer $b$.
3. Induction on $a \ge 0$. For $a = 0$, $0^p = 0$. If $a^p \equiv a$, then by step 2, $(a + 1)^p \equiv a^p + 1 \equiv a + 1$.
4. For $a < 0$, choose $c \ge 0$ with $c \equiv a \pmod p$. Then $a^p \equiv c^p \equiv c \equiv a$. $\blacksquare$

**The group view.** The nonzero residues modulo $p$ form a group under multiplication with $p - 1$ elements, the [multiplicative group modulo p](/multiplicative-group-modulo-n/). By [Lagrange's theorem](/lagranges-theorem-group-theory/), the order of each element divides $p - 1$, so $a^{p-1} = 1$ in the group. The same argument with $\varphi(n)$ in place of $p - 1$ proves [Euler's theorem](/euler-theorem/).

## Consequences

- **Inverses modulo a prime.** If $p \nmid a$, then $a \cdot a^{p-2} \equiv 1$, so $a^{-1} \equiv a^{p-2} \pmod p$. With [binary exponentiation](/binary-exponentiation/) this costs $O(\log p)$ multiplications. For $p = 7$ and $a = 3$: $3^5 = 243 \equiv 5$, and $3 \cdot 5 = 15 \equiv 1 \pmod 7$.
- **Small exponents.** To compute $a^e \bmod p$ with a huge $e$, first replace $e$ by $e \bmod (p - 1)$ when $p \nmid a$.
- **Primality testing.** If $a^{n-1} \not\equiv 1 \pmod n$ for some $a$ with $\gcd(a, n) = 1$, then $n$ is composite. This is the [Fermat primality test](/fermat-primality-test/). The [Miller-Rabin test](/miller-rabin/) strengthens it with square roots of $1$.
- **[Euler's criterion](/euler-criterion/).** For an odd prime $p$, $a^{(p-1)/2} \equiv \pm 1$, and the sign tells whether $a$ is a [quadratic residue](/quadratic-residue/).
- **Orders.** The [multiplicative order](/multiplicative-order/) of $a$ modulo $p$ divides $p - 1$. This bounds the search for [primitive roots](/primitive-root/) and is the base of [Pollard's p − 1 method](/pollard-p-minus-1/).
- **Finite fields.** In $\mathbb{F}_p$, the polynomial $x^p - x$ has every element as a root, so $x^p - x = \prod_{c \in \mathbb{F}_p} (x - c)$. This is used in polynomial factorization over finite fields.

## Tightness

**The hypothesis $p \nmid a$ is needed in the first form.** For $a = p$, $a^{p-1} \equiv 0 \pmod p$.

**The exponent $p - 1$ cannot be lowered for all $a$ at once.** Each prime has a [primitive root](/primitive-root/), an element of order exactly $p - 1$. For $p = 7$, the powers $3^1, \ldots, 3^6$ are $3, 2, 6, 4, 5, 1$ modulo $7$, so no exponent $k$ with $1 \le k < 6$ gives $3^k \equiv 1$. The existence of primitive roots is proved on [existence of primitive roots](/primitive-roots-existence/).

**Primality is needed.** Modulo $4$, $3^{3} = 27 \equiv 3$, not $1$. For composite moduli the right exponent is $\varphi(n)$ ([Euler's theorem](/euler-theorem/)) or the [Carmichael function](/carmichael-function/) $\lambda(n)$.

**The converse is false.** The composite number $341 = 11 \cdot 31$ satisfies $2^{340} \equiv 1 \pmod{341}$, so it is a [Fermat pseudoprime](/fermat-pseudoprime/) to base $2$. Base $3$ exposes it: $3^{340} \equiv 56 \pmod{341}$. Worse, the [Carmichael number](/carmichael-number/) $561 = 3 \cdot 11 \cdot 17$ satisfies $a^{560} \equiv 1 \pmod{561}$ for every $a$ coprime to $561$, so no coprime base exposes it. This is why the Fermat test alone is not a proof of primality.

## History

Pierre de Fermat stated the theorem in a letter to Frénicle de Bessy dated 18 October 1640, without a proof. Leonhard Euler gave the first published proof, in a paper presented to the Saint Petersburg Academy in 1736; Leibniz had found a similar proof earlier but did not publish it. Euler later generalized the result to composite moduli, which is [Euler's theorem](/euler-theorem/). Hardy and Wright (Chapter 6) give the theorem and its consequences, and the Wikipedia article gives the history with references.

## References
