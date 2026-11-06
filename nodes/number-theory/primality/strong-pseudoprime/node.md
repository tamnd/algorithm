---
tag: 7KV5K7
kind: definition
slug: strong-pseudoprime
name: Strong pseudoprime
aliases:
- spsp
- strong pseudoprime to the base a
area: number-theory/primality
level: core
summary: An odd composite n that passes the Miller-Rabin check for a given base a. With n-1 = 2^s t and t odd, either a^t = 1 or a^(2^i t) = -1 modulo n for some i < s.
prereqs: [pseudoprime, nontrivial-square-root-of-one, fermat-little-theorem]
see_also: [strong-liar, miller-rabin, deterministic-miller-rabin-bases, euler-jacobi-pseudoprime, fermat-pseudoprime, carmichael-number, baillie-psw, probable-prime]
sources:
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Section 3.5 (Theorem 3.5.1, Algorithm 3.5.2, Definition 3.5.3, Theorem 3.5.4) and Section 3.5.1 (Theorems 3.5.10 to 3.5.12)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography
    locator: Chapter 4, Section 4.2.3 (Fact 4.20, Definition 4.21, Example 4.22, Fact 4.23, Definition 4.29, Table 4.1) and Section 4.2.4 (Fact 4.30, Fact 4.32)
---

A strong pseudoprime to the base $a$ is an odd composite number $n$ that passes the strong probable prime test for $a$, the check at the heart of the [Miller-Rabin test](/miller-rabin/). The test looks at the sequence $a^t, a^{2t}, \ldots, a^{2^s t}$ modulo $n$, where $n - 1 = 2^s t$ with $t$ odd, and asks that it behave as it must for a prime. Strong pseudoprimes are much rarer than [Fermat pseudoprimes](/fermat-pseudoprime/), and unlike them no composite is a strong pseudoprime to all bases.

## Definition

Let $n$ be an odd composite number, write $n - 1 = 2^s t$ with $t$ odd, and let $a$ be an integer. Then $n$ is a **strong pseudoprime to the base $a$** if
$$a^t \equiv 1 \pmod n \quad \text{or} \quad a^{2^i t} \equiv -1 \pmod n \text{ for some } i \text{ with } 0 \le i < s$$
(Crandall and Pomerance, Definition 3.5.3; HAC Definition 4.21). The base $a$ is then a [strong liar](/strong-liar/) for $n$. If $n$ is odd and satisfies the condition, prime or not, $n$ is a *strong probable prime* to the base $a$.

**Why primes pass** (Crandall and Pomerance, Theorem 3.5.1; HAC Fact 4.20). Let $n$ be an odd prime with $n \nmid a$. By [Fermat's little theorem](/fermat-little-theorem/), the last term $a^{2^s t} = a^{n-1}$ of the sequence is $1$. If $a^t \not\equiv 1$, let $i < s$ be the last index with $a^{2^i t} \not\equiv 1$. Then $x = a^{2^i t}$ satisfies $x^2 \equiv 1$, and modulo a prime the only square roots of $1$ are $\pm 1$, so $x \equiv -1$. $\square$ A composite $n$ fails the condition exactly when the sequence starts away from $1$ and reaches $1$ without passing through $-1$, which exposes a [nontrivial square root of one](/nontrivial-square-root-of-one/), or when it never reaches $1$, so that the Fermat test also fails.

**Relations to other pseudoprimes.** For each odd composite $n$ and each base $a$:

- If $n$ is a strong pseudoprime to the base $a$, it is an [Euler-Jacobi pseudoprime](/euler-jacobi-pseudoprime/) to the base $a$, and so a Fermat pseudoprime to the base $a$ (HAC Fact 4.30).
- If $n \equiv 3 \pmod 4$, then $n$ is a strong pseudoprime to the base $a$ exactly when it is an Euler-Jacobi pseudoprime to the base $a$ (HAC Fact 4.32).
- For $n > 9$, at most $\varphi(n)/4$ residues $a$ modulo $n$ make $n$ a strong pseudoprime (Crandall and Pomerance, Theorem 3.5.4, due to Monier and to Rabin). So there is no strong analogue of [Carmichael numbers](/carmichael-number/).

**Infinitely many.** For each prime $p > 5$, $n = (4^p + 1)/5$ is a strong pseudoprime to the base 2 (Crandall and Pomerance, Theorem 3.5.10). It is composite by the identity $4^p + 1 = (2^p - 2^{(p+1)/2} + 1)(2^p + 2^{(p+1)/2} + 1)$, and $2^{2p} \equiv -1 \pmod n$ gives the condition.

**Least witness.** Let $W(n)$ be the least base $a$ for which an odd composite $n$ is not a strong pseudoprime. There are infinitely many $n$ with $W(n) > (\ln n)^{1/(3 \ln \ln \ln n)}$ (Theorem 3.5.11, from Alford, Granville and Pomerance), so no fixed set of bases works for every $n$. If the extended Riemann hypothesis holds, $W(n) < 2 (\ln n)^2$ for every odd composite $n$ (Theorem 3.5.12, from Bach); this conditional bound is the basis of Miller's deterministic test.

## Examples and non-examples

**Examples.**

- $2047 = 23 \cdot 89$ is the smallest strong pseudoprime to the base 2. Here $2046 = 2 \cdot 1023$ and $2^{1023} \equiv 1 \pmod{2047}$, because $2^{11} = 2048 \equiv 1$.
- The strong pseudoprimes to the base 2 below $10^5$ are $2047, 3277, 4033, 4681, 8321, 15841, 29341, 42799, 49141, 52633, 65281, 74665, 80581, 85489, 88357, 90751$. There are 16 of them, against 78 Fermat pseudoprimes to the base 2. Below $10^6$ there are 46. Three of the 16, namely $15841$, $29341$ and $52633$, are Carmichael numbers.
- $3277 = 29 \cdot 113 = (4^7 + 1)/5$ and $838861 = 397 \cdot 2113 = (4^{11} + 1)/5$ come from the family above.
- $91 = 7 \cdot 13$ is a strong pseudoprime to the bases 9 and 10: $90 = 2 \cdot 45$, $9^{45} \equiv 1$ and $10^{45} \equiv -1 \pmod{91}$. Its strong liars are $1, 9, 10, 12, 16, 17, 22, 29, 38, 53, 62, 69, 74, 75, 79, 81, 82, 90$, which is $18 = \varphi(91)/4$ of them, so the bound $\varphi(n)/4$ is attained (HAC Example 4.22).
- **Smallest strong pseudoprimes to the first $t$ primes** (HAC Definition 4.29 and Table 4.1). Write $\psi_t$ for the smallest composite that is a strong pseudoprime to each of the first $t$ prime bases. Every odd $n < \psi_t$ that passes those $t$ bases is prime; the page on [deterministic bases](/deterministic-miller-rabin-bases/) builds on this.

| $t$ | bases | $\psi_t$ | factors |
|---|---|---|---|
| 1 | 2 | 2047 | $23 \cdot 89$ |
| 2 | 2, 3 | 1373653 | $829 \cdot 1657$ |
| 3 | 2, 3, 5 | 25326001 | $2251 \cdot 11251$ |
| 4 | 2, 3, 5, 7 | 3215031751 | $151 \cdot 751 \cdot 28351$ |
| 5 | 2 to 11 | 2152302898747 | |
| 6 | 2 to 13 | 3474749660383 | |
| 7 and 8 | 2 to 17, 2 to 19 | 341550071728321 | |

The values for $t = 1, 2, 3$ agree with an exhaustive search over all odd composites up to $\psi_3$.

**Non-examples.**

- $341 = 11 \cdot 31$ is a Fermat pseudoprime to the base 2 but not a strong one: $340 = 2^2 \cdot 85$, $2^{85} \equiv 32$ and $2^{170} \equiv 1 \pmod{341}$. So $32$ is a nontrivial square root of $1$ modulo 341, and $\gcd(32 - 1, 341) = 31$ is a factor.
- $561 = 3 \cdot 11 \cdot 17$ is a Carmichael number but not a strong pseudoprime to the base 2: $560 = 2^4 \cdot 35$, and the sequence $2^{35}, 2^{70}, 2^{140}, 2^{280}$ is $263, 166, 67, 1$ modulo 561, which reaches $1$ without passing through $560$.
- $105 = 3 \cdot 5 \cdot 7$ is a strong pseudoprime to no base except $1$ and $104$ (HAC Example 4.27).
- An odd prime is never a strong pseudoprime, because the definition asks for $n$ composite; it is a strong probable prime to every base it does not divide.

## Related definitions

- **[Strong liar](/strong-liar/).** A base $a$ for which $n$ is a strong pseudoprime; the set of strong liars and its size $S(n)$.
- **Strong probable prime.** An odd $n$, prime or composite, that satisfies the condition; see [probable prime](/probable-prime/). The test is due to Artjuhov (1966 and 1967) and was rediscovered by Selfridge, who named it (Crandall and Pomerance, Section 3.5).
- **[Fermat pseudoprime](/fermat-pseudoprime/)** and **[Euler-Jacobi pseudoprime](/euler-jacobi-pseudoprime/).** The weaker notions; every strong pseudoprime to the base $a$ is both.
- **[Miller-Rabin test](/miller-rabin/).** The randomized test that checks the condition for random bases; by the bound $\varphi(n)/4$ each round misses a composite with probability below $1/4$.
- **[Baillie-PSW test](/baillie-psw/).** A strong probable prime test to the base 2 followed by a strong Lucas test. A composite passes only if it is a pseudoprime of both kinds at once.

## References
