---
tag: AYZ9R2
kind: theorem
slug: wilson-theorem
name: Wilson's theorem
area: number-theory/modular-arithmetic
level: core
summary: An integer n ≥ 2 is prime exactly when (n − 1)! ≡ −1 (mod n); for composite n > 4 the factorial is ≡ 0.
prereqs: [modular-inverse, prime-number]
see_also: [wilsons-theorem, fermat-little-theorem, factorial-modulo-prime, multiplicative-group-modulo-n, quadratic-residue, factorial, primitive-root]
sources:
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Chapter 6, Section 6.6, Wilson's theorem (Theorem 80); Chapter 7, Section 7.6, Lagrange's proof of Fermat's and Wilson's theorems, and Section 7.7, The residue of ((p − 1)/2)!
  - book: isbn:9780471625469
    title: Ivan Niven, Herbert S. Zuckerman and Hugh L. Montgomery, An Introduction to the Theory of Numbers, fifth edition
    locator: Chapter 2, Congruences (Wilson's theorem and its converse, with the proof by pairing inverses)
  - url: "https://en.wikipedia.org/wiki/Wilson%27s_theorem"
    locator: Wikipedia, Wilson's theorem (the history from Ibn al-Haytham to Waring, Lagrange and Gauss, and Gauss's generalization)
---

Wilson's theorem says that an integer $n \ge 2$ is a [prime number](/prime-number/) if and only if $(n - 1)! \equiv -1 \pmod n$. The proof for primes pairs each factor with its [modular inverse](/modular-inverse/), so that only $1$ and $p - 1$ remain. It gives a characterization of the primes that needs no factoring, but it is useless as a test, since no method is known to compute $(n - 1)! \bmod n$ in time polynomial in $\log n$. Its value is in theory: it gives a square root of $-1$ modulo a prime $p \equiv 1 \pmod 4$, and it is the starting point for many congruences on factorials and binomial coefficients.

## Statement

**Theorem (Wilson; Lagrange).** Let $n \ge 2$. Then $n$ is prime if and only if

$$(n - 1)! \equiv -1 \pmod n.$$

Moreover, if $n$ is composite, then $(n - 1)! \equiv 0 \pmod n$ for $n \ne 4$, and $3! \equiv 2 \pmod 4$.

**Examples.** For $p = 7$: $6! = 720 = 103 \cdot 7 - 1$, so $6! \equiv -1 \pmod 7$. The pairs of inverses are $\{2, 4\}$ and $\{3, 5\}$, since $2 \cdot 4 = 8 \equiv 1$ and $3 \cdot 5 = 15 \equiv 1$, which leaves $1 \cdot 6 \equiv -1$.

For $p = 13 \equiv 1 \pmod 4$: $6! = 720 \equiv 5 \pmod{13}$, and $5^2 = 25 \equiv -1$, a square root of $-1$.

For composites: $3! \equiv 2 \pmod 4$, $5! = 120 \equiv 0 \pmod 6$ and $8! = 40320 \equiv 0 \pmod 9$. For $n = 25$, $24! \equiv 0 \pmod{25}$, by the factors 5 and 10.

For the Wilson prime 13: $12! + 1 = 479001601 = 169 \cdot 2834329$.

## In plain words

Multiply all whole numbers from 1 up to one less than a given number, and divide by the given number. When the given number is a prime, the remainder is always one less than the prime. When the given number is not a prime, this never happens: the remainder is 0, with one exception, the number 4. The reason for the prime case is that the numbers on a prime clock pair up. Each number has a partner such that their product lands on 1. Only the first and the last number are their own partners, so the whole product is the last number, which is the same as minus one.

## Proof

**If $n = p$ is prime.** For $p = 2$, $1! = 1 \equiv -1 \pmod 2$. Let $p$ be an odd prime. Each $a \in \{1, \ldots, p - 1\}$ has a unique inverse $a^{-1}$ in the same set, since $\gcd(a, p) = 1$. An element is its own inverse when $a^2 \equiv 1$, that is, $p \mid (a - 1)(a + 1)$, so, by [Euclid's lemma](/euclids-lemma/), when $a = 1$ or $a = p - 1$. The other $p - 3$ elements $2, \ldots, p - 2$ split into $(p - 3)/2$ pairs $\{a, a^{-1}\}$ with $a \ne a^{-1}$, and the product of each pair is $\equiv 1$. Hence

$$(p - 1)! \equiv 1 \cdot \prod_{\text{pairs}} (a \cdot a^{-1}) \cdot (p - 1) \equiv p - 1 \equiv -1 \pmod p.$$

**If $n$ is composite.** Write $n = ab$ with $1 < a \le b < n$.

- If $a < b$, both $a$ and $b$ are among the factors $1, \ldots, n - 1$, so $n = ab$ divides $(n - 1)!$.
- If $a = b$, then $n = a^2$. If $a > 2$, then $a < 2a < a^2 = n$, so $a$ and $2a$ are distinct factors of $(n - 1)!$, and $a \cdot 2a = 2n$ divides it. If $a = 2$, then $n = 4$ and $3! = 6 \equiv 2 \pmod 4$.

In all composite cases $(n - 1)! \not\equiv -1 \pmod n$: for $n \ne 4$ it is $\equiv 0$, and $0 \not\equiv -1$ since $n > 1$; for $n = 4$ it is $2 \not\equiv 3$. So the congruence holds exactly for primes. $\blacksquare$

**A second proof, by Lagrange.** By [Fermat's little theorem](/fermat-little-theorem/), $1, \ldots, p - 1$ are $p - 1$ distinct roots of $x^{p-1} - 1$ modulo $p$. A polynomial of degree $p - 1$ over the field $\mathbb{Z}_p$ has at most $p - 1$ roots, so $x^{p-1} - 1 \equiv (x - 1)(x - 2) \cdots (x - (p - 1))$. Comparing constant terms gives $-1 \equiv (-1)^{p-1} (p - 1)!$, which is Wilson's theorem for odd $p$.

## Consequences

- **A square root of −1.** Pair $k$ with $p - k \equiv -k$ in $(p - 1)!$. This gives $(p - 1)! \equiv (-1)^{(p-1)/2} \left( \left(\tfrac{p-1}{2}\right)! \right)^2$, so $\left( \left(\tfrac{p-1}{2}\right)! \right)^2 \equiv (-1)^{(p+1)/2} \pmod p$. For $p \equiv 1 \pmod 4$, $((p - 1)/2)!$ is a square root of $-1$, which proves that $-1$ is a [quadratic residue](/quadratic-residue/) for these primes. For $p \equiv 3 \pmod 4$, $((p - 1)/2)! \equiv \pm 1$.
- **Factorials near p.** Removing the last $k$ factors gives $(p - 1 - k)! \cdot k! \equiv (-1)^{k+1} \pmod p$. This turns a factorial close to $p$ into one of a small number, a step used when computing [factorials modulo a prime](/factorial-modulo-prime/) and binomial coefficients with [Lucas's theorem](/lucas-theorem/).
- **Gauss's generalization.** The product of all elements of the [multiplicative group modulo n](/multiplicative-group-modulo-n/) is $\equiv -1 \pmod n$ when $n$ is $2, 4, p^k$ or $2p^k$ for an odd prime $p$, and $\equiv 1$ otherwise. The proof is the same pairing: the product equals the product of the elements with $x^2 = 1$.
- **Groups in general.** In any finite abelian group, the product of all elements equals the product of the elements of order 2, and so is the identity unless there is exactly one element of order 2. Wilson's theorem is the case of the cyclic group $\mathbb{Z}_p^*$, where $-1$ is the only such element.
- **No efficient test.** Computing $(n - 1)! \bmod n$ directly takes $n - 2$ [modular multiplications](/modular-multiplication/), exponential in the length of $n$. The best known algorithms for $m! \bmod n$ take about $m^{1/2}$ operations up to logarithmic factors, still exponential. Primality is decided in practice with [Miller-Rabin](/miller-rabin/) or other tests based on Fermat's theorem.

## Tightness

The converse direction is exact: no composite $n$ satisfies the congruence, and for composite $n > 4$ the residue is 0, since $n$ divides the factorial. The only composite with a nonzero residue is $n = 4$, with $3! \equiv 2$. The modulus cannot be raised to $p^2$ in general: $(p - 1)! \equiv -1 \pmod{p^2}$ holds only for the Wilson primes, of which the only known ones are 5, 13 and 563.

## History

Ibn al-Haytham stated the result around 1000. Edward Waring published it in his *Meditationes Algebraicae* of 1770 and credited it to his student John Wilson, without a proof. Lagrange gave the first proof in 1771, including the converse; his proof by the polynomial $x^{p-1} - 1$ is the second proof above (Hardy and Wright, Section 7.6). Leibniz had also known the statement but did not publish it. Gauss stated and proved the generalization to composite moduli in the *Disquisitiones Arithmeticae* (1801).

## References
