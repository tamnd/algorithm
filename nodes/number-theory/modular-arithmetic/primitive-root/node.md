---
tag: VGKN86
kind: concept
slug: primitive-root
name: Primitive root
aliases:
- generator of the multiplicative group
- primitive root modulo n
area: number-theory/modular-arithmetic
level: core
summary: An integer g whose multiplicative order modulo n equals φ(n), so that its powers run through every residue coprime to n.
prereqs: [multiplicative-order, multiplicative-group-modulo-n]
see_also: [primitive-roots-existence, cyclic-group, euler-totient, carmichael-function, discrete-logarithm-problem, diffie-hellman, number-theoretic-transform, roots-of-unity]
sources:
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1997
    locator: Section 2.4.3, Definition 2.131 and Fact 2.132 (properties of generators of Z_n^*), Example 2.133; Section 4.6, Algorithm 4.80 (finding a generator of a cyclic group) and Section 4.6.1
  - book: isbn:9780471625469
    title: Ivan Niven, Herbert S. Zuckerman and Hugh L. Montgomery, An Introduction to the Theory of Numbers, fifth edition
    locator: Section 2.8, Primitive roots and power residues
  - book: isbn:9780387973296
    title: Kenneth Ireland and Michael Rosen, A Classical Introduction to Modern Number Theory, second edition, Springer GTM 84
    locator: Chapter 4, Section 4.1, Primitive Roots and the Group Structure of U(Z/nZ)
  - paper: "Victor Shoup, Searching for primitive roots in finite fields, Mathematics of Computation 58(197), 1992"
    locator: pages 369 to 380
---

A primitive root modulo $n$ is an integer $g$, coprime to $n$, whose [multiplicative order](/multiplicative-order/) modulo $n$ is $\varphi(n)$. Equivalently, the powers $g^0, g^1, \ldots, g^{\varphi(n) - 1}$ run through every residue coprime to $n$, so $g$ generates the [multiplicative group modulo n](/multiplicative-group-modulo-n/) and that group is [cyclic](/cyclic-group/). Primitive roots exist exactly for $n = 1, 2, 4, p^k$ and $2p^k$ with $p$ an odd prime ([existence theorem](/primitive-roots-existence/)), and then there are $\varphi(\varphi(n))$ of them modulo $n$. They are the generators used in [Diffie-Hellman](/diffie-hellman/), the source of roots of unity for the [number-theoretic transform](/number-theoretic-transform/), and the base of discrete logarithms modulo a prime.

## In plain words

Pick a number and multiply it by itself again and again on a clock. You visit some positions and then return to the start of the cycle. Usually you see only some of the positions that share no factor with the clock size. A primitive root is a starting number that visits all of them before it returns. For a prime clock size, there is always such a number, and it shows that every nonzero position is a power of one number. Some clock sizes, such as 8 or 12, have no primitive root, because every cycle is too short. To check a candidate, you do not walk the full cycle. You test a few large powers, one for each prime factor of the count of positions.

## The idea

**Definition.** Let $n \ge 1$ and $\gcd(g, n) = 1$. Then $g$ is a primitive root modulo $n$ if $\operatorname{ord}_n(g) = \varphi(n)$. Since $\operatorname{ord}_n(g)$ is the number of distinct powers of $g$, this holds if and only if $\{ g^i \bmod n : 0 \le i < \varphi(n) \} = \mathbb{Z}_n^*$.

**When they exist.** $\mathbb{Z}_n^*$ is cyclic, so a primitive root exists, if and only if $n$ is $1, 2, 4, p^k$ or $2p^k$ for an odd prime $p$ and $k \ge 1$. The proof is on the page for the [existence theorem](/primitive-roots-existence/). For other $n$, the largest order of an element is the [Carmichael function](/carmichael-function/) $\lambda(n)$, which is then a proper divisor of $\varphi(n)$.

**How many.** If $g$ is a primitive root, then $g^j$ has order $\varphi(n)/\gcd(j, \varphi(n))$, so $g^j$ is a primitive root exactly when $\gcd(j, \varphi(n)) = 1$. Hence there are $\varphi(\varphi(n))$ primitive roots modulo $n$. For a prime $p$, the fraction of primitive roots in $\mathbb{Z}_p^*$ is $\varphi(p - 1)/(p - 1)$, which is at least $1/(6 \ln \ln (p - 1))$ for large $p$ (HAC, Section 4.6).

**Testing a candidate.** Let $\varphi(n) = q_1^{e_1} \cdots q_r^{e_r}$. Then $g$ is a primitive root if and only if

$$g^{\varphi(n)/q_i} \not\equiv 1 \pmod n \quad \text{for } i = 1, \ldots, r.$$

If the order $t$ of $g$ were a proper divisor of $\varphi(n)$, then $t$ would divide $\varphi(n)/q_i$ for some prime $q_i$, and that power would be 1. The test needs the factorization of $\varphi(n)$, and costs $r = O(\log n)$ [modular exponentiations](/modular-exponentiation/).

**Finding one.** Try $g = 2, 3, 4, \ldots$, or random $g$, and test each. By the density above, the expected number of random trials is $O(\log \log p)$ for a prime $p$; this is Algorithm 4.80 of HAC. The least primitive root modulo a prime is small in practice, but the proven bounds are much weaker. Under the generalized Riemann hypothesis, Shoup (1992) showed that it is $O((\log p)^6)$.

**Lifting to prime powers.** If $g$ is a primitive root modulo an odd prime $p$, then $g$ or $g + p$ is a primitive root modulo $p^2$, and a primitive root modulo $p^2$ is a primitive root modulo every $p^k$, $k \ge 2$. A primitive root modulo $2p^k$ is whichever of $g$ and $g + p^k$ is odd.

**Indices.** For a primitive root $g$ modulo $n$, each $a \in \mathbb{Z}_n^*$ is $g^i$ for exactly one $i \in [0, \varphi(n))$, called the index or the [discrete logarithm](/discrete-logarithm-problem/) of $a$ to the base $g$. The map $a \mapsto i$ turns multiplication modulo $n$ into addition modulo $\varphi(n)$, just as an ordinary logarithm turns products into sums. Computing indices is believed hard for large $p$; it is the security basis of Diffie-Hellman.

**Artin's conjecture.** Artin conjectured in 1927 that every integer $a$ that is neither $-1$ nor a perfect square is a primitive root modulo infinitely many primes; for $a = 2$, the predicted density of such primes is Artin's constant, about $0.3739558$. Hooley proved this in 1967 under the generalized Riemann hypothesis. It is not proven unconditionally for any single $a$.

## Examples

**Modulo 7.** $\varphi(7) = 6$ and $\varphi(6) = 2$. The powers of 3 are $3, 2, 6, 4, 5, 1$, so 3 is a primitive root; the other one is $3^5 \equiv 5$. The powers of 2 are $2, 4, 1$, so 2 is not.

**Modulo 13.** $\varphi(12) = 4$, and the primitive roots are $2, 6, 7, 11$. They are $2^1, 2^5, 2^7, 2^{11}$, the powers $2^j$ with $\gcd(j, 12) = 1$.

**Testing modulo 41.** $\varphi(41) = 40 = 2^3 \cdot 5$, so test $g^{20}$ and $g^8$. For $g = 2$, $2^{20} \equiv 1$; for $g = 3$, $3^{20} \equiv 40$ but $3^8 \equiv 1$; for $g = 4$ and $g = 5$, $g^{20} \equiv 1$. For $g = 6$, $6^{20} \equiv 40$ and $6^8 \equiv 10$, so 6 is the least primitive root modulo 41.

**Least primitive roots.** For the primes $3, 5, 7, 11, 13, 17, 19, 23, 41, 71, 191, 409$, the least primitive roots are $2, 2, 3, 2, 2, 3, 2, 5, 6, 7, 19, 21$.

**Prime powers and twice them.** Modulo 9 the primitive roots are 2 and 5, and modulo 25 they are $2, 3, 8, 12, 13, 17, 22, 23$. Modulo $18 = 2 \cdot 9$, the root 2 of 9 is even, so $2 + 9 = 11$ is a primitive root, as is 5. The number 14 is a primitive root modulo 29 but has order 28, not 812, modulo $29^2$, so in the lifting step $g + p = 43$ is needed.

**No primitive root.** Modulo 8, every element of $\{1, 3, 5, 7\}$ squares to 1. Modulo 12 the same holds for $\{1, 5, 7, 11\}$.

**An NTT prime.** $p = 998244353 = 119 \cdot 2^{23} + 1$, with $p - 1 = 2^{23} \cdot 7 \cdot 17$. The values $3^{(p-1)/2}$, $3^{(p-1)/7}$ and $3^{(p-1)/17}$ modulo $p$ are $p - 1$, $779057549$ and $337827833$, none equal to 1, so 3 is a primitive root, and $3^{119}$ has order $2^{23}$.

## Where it is used

- **Diffie-Hellman and ElGamal.** [Diffie-Hellman](/diffie-hellman/) and [ElGamal encryption](/elgamal-encryption/) were first described with a primitive root modulo a prime $p$. In practice, a generator of a large prime-order subgroup is often used instead, to avoid leaking the Legendre symbol of the secret.
- **Number-theoretic transform.** For a prime $p$ with $2^k \mid p - 1$ and a primitive root $g$, the element $g^{(p-1)/2^k}$ is a primitive $2^k$-th [root of unity](/roots-of-unity/), which the [NTT](/number-theoretic-transform/) needs.
- **Discrete logarithms.** [Baby-step giant-step](/baby-step-giant-step/), [Pohlig-Hellman](/pohlig-hellman/) and index calculus compute indices with respect to a primitive root.
- **Primality proofs.** By the [Lucas primality test](/lucas-primality-test/), $n$ is prime if some $g$ has order $n - 1$ modulo $n$, that is, if $n$ has a primitive root of order $n - 1$.
- **Pseudorandom generators.** A multiplicative [linear congruential generator](/linear-congruential-generator/) modulo a prime $p$ has the full period $p - 1$ when its multiplier is a primitive root, as in the Lehmer generator with $p = 2^{31} - 1$ and multiplier $16807$.
- **Decimal expansions.** $1/p$ has the longest possible period $p - 1$ when 10 is a primitive root modulo $p$, as for $p = 7, 17, 19, 23, 29, 47, 59, 61$.

## References
