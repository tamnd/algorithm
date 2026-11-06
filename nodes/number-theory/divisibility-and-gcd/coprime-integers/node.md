---
tag: SHY5EB
kind: definition
slug: coprime-integers
name: Coprime integers
aliases:
- relatively prime
- coprime
area: number-theory/divisibility-and-gcd
level: intro
summary: Integers a and b are coprime when gcd(a, b) = 1.
prereqs: [divisibility, greatest-common-divisor]
see_also: [bezouts-identity, euclids-lemma, euler-totient, modular-inverse, counting-coprime-pairs, reducing-fractions, euclidean-algorithm]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.1, Elementary number-theoretic notions (relatively prime integers, pairwise relatively prime, and the theorem that gcd(a, p) = gcd(b, p) = 1 gives gcd(ab, p) = 1)
  - book: isbn:9780387901633
    title: Tom M. Apostol, Introduction to Analytic Number Theory
    locator: Chapter 1, Section 1.3, Greatest common divisor (relatively prime integers and the consequences of Bezout's identity)
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Chapter 18 (the average order of phi(n) and the probability that two integers are coprime)
---

Two integers $a$ and $b$ are coprime, or relatively prime, when their [greatest common divisor](/greatest-common-divisor/) is $1$: the only integers that [divide](/divisibility/) both are $1$ and $-1$. Coprimality is the condition of most theorems of elementary number theory: it makes $a$ invertible modulo $b$, it lets a divisor of a product be split between the factors, and it is what a fraction in lowest terms has. The [Euclidean algorithm](/euclidean-algorithm/) tests it in $O(\log \min(|a|, |b|))$ division steps.

## Definition

Let $a$ and $b$ be integers. Then $a$ and $b$ are **coprime** (or **relatively prime**, or $a$ is **prime to** $b$) if

$$\gcd(a, b) = 1.$$

Some books write $a \perp b$. The definition is symmetric in $a$ and $b$, and it depends only on $|a|$ and $|b|$.

**Zero.** By the usual convention $\gcd(a, 0) = |a|$ and $\gcd(0, 0) = 0$. So $a$ and $0$ are coprime if and only if $a = \pm 1$, and $0$ is not coprime to itself.

**Several integers.** Integers $a_1, \ldots, a_k$ are **coprime as a set** (or *mutually coprime*) if $\gcd(a_1, \ldots, a_k) = 1$. They are **pairwise coprime** if $\gcd(a_i, a_j) = 1$ for each $i \ne j$. Pairwise coprime implies coprime as a set when $k \ge 2$, but not conversely: $\gcd(6, 10, 15) = 1$, while $\gcd(6, 10) = 2$, $\gcd(10, 15) = 5$ and $\gcd(6, 15) = 3$. The [Chinese remainder theorem](/chinese-remainder-theorem/) needs pairwise coprime moduli.

### Equivalent conditions

For integers $a$ and $b$, not both zero, these statements are equivalent.

1. $\gcd(a, b) = 1$.
2. There are integers $x$ and $y$ with $ax + by = 1$.
3. No prime $p$ divides both $a$ and $b$.

*Proof.* (1) gives (2) by [Bézout's identity](/bezouts-identity/). (2) gives (3): if $p \mid a$ and $p \mid b$, then $p \mid ax + by = 1$, which is false for $p \ge 2$. (3) gives (1): let $g = \gcd(a, b)$. Since $a$ and $b$ are not both zero, $g \ge 1$. If $g > 1$, then $g$ has a prime factor $p$, and $p$ divides both $a$ and $b$, against (3). So $g = 1$. $\square$

When $b \ge 2$, a fourth condition is equivalent: $a$ has an inverse modulo $b$, an integer $x$ with $ax \equiv 1 \pmod b$. This is condition 2 read modulo $b$. The page [modular inverse](/modular-inverse/) computes $x$ with the [extended Euclidean algorithm](/extended-euclidean-algorithm/).

### Basic properties

Let $a$, $b$, $c$ and $m$ be integers.

1. **Products of coprime numbers.** If $\gcd(a, m) = \gcd(b, m) = 1$, then $\gcd(ab, m) = 1$. Proof: from $ax + my = 1$ and $bu + mv = 1$, multiply to get $ab(xu) + m(axv + ybu + ymv) = 1$, and use condition 2.
2. **Gauss's lemma.** If $a \mid bc$ and $\gcd(a, b) = 1$, then $a \mid c$. Proof: from $ax + by = 1$ we get $c = acx + bcy$. Both terms are multiples of $a$, the second because $a \mid bc$. So $a \mid c$. With $a$ prime this is [Euclid's lemma](/euclids-lemma/).
3. **Coprime divisors multiply.** If $a \mid c$, $b \mid c$ and $\gcd(a, b) = 1$, then $ab \mid c$. Proof: write $c = ak$. Then $b \mid ak$ and $\gcd(b, a) = 1$, so $b \mid k$ by property 2, and $ab \mid ak = c$.
4. **Dividing out the gcd.** If $g = \gcd(a, b) \ge 1$, then $a/g$ and $b/g$ are coprime. Proof: $ax + by = g$ for some $x, y$, so $(a/g)x + (b/g)y = 1$. This is how a fraction is put in lowest terms ([reducing fractions](/reducing-fractions/)).
5. **Shifts.** $\gcd(a, b) = \gcd(a, b + ka)$ for each integer $k$, because a common divisor of two of the numbers $a$, $b$, $b + ka$ divides the third. So $\gcd(n, n + 1) = \gcd(n, 1) = 1$: consecutive integers are coprime.

### Density

Coprime pairs are common. Let $C(N)$ be the number of pairs $(a, b)$ with $1 \le a, b \le N$ and $\gcd(a, b) = 1$. Then

$$C(N) = \frac{6}{\pi^2} N^2 + O(N \log N),$$

so the fraction of coprime pairs tends to $6/\pi^2 \approx 0.6079$. Hardy and Wright prove this in Chapter 18 through the average order of [Euler's totient](/euler-totient/). A heuristic reading: a prime $p$ divides both numbers with "probability" $1/p^2$, and $\prod_p (1 - 1/p^2) = 1/\zeta(2) = 6/\pi^2$. The page [counting coprime pairs](/counting-coprime-pairs/) computes $C(N)$ exactly.

## Examples and non-examples

| $a$ | $b$ | $\gcd(a, b)$ | coprime? | a witness $ax + by = 1$, or a common prime |
|---|---|---|---|---|
| 35 | 64 | 1 | yes | $35 \cdot 11 + 64 \cdot (-6) = 1$ |
| 8 | 9 | 1 | yes | $8 \cdot (-1) + 9 \cdot 1 = 1$ (consecutive) |
| 832040 | 514229 | 1 | yes | consecutive Fibonacci numbers $F_{30}, F_{29}$ |
| $-7$ | 10 | 1 | yes | $(-7) \cdot (-3) + 10 \cdot (-2) = 1$ |
| 1 | 0 | 1 | yes | $1 \cdot 1 + 0 \cdot 0 = 1$ |
| 91 | 35 | 7 | no | $7$ divides both |
| 6 | 15 | 3 | no | $3$ divides both |
| 0 | 0 | 0 | no | every integer divides both |
| 12 | 0 | 12 | no | $2$ divides both |

- $2^{10} = 1024$ and $3^7 = 2187$ are coprime, because no prime divides both (condition 3).
- The totient counts coprime residues: of $1, \ldots, 12$, the numbers coprime to $12$ are $1, 5, 7, 11$, so $\varphi(12) = 4$.
- For $N = 1000$ there are $C(1000) = 608{,}383$ coprime pairs, a fraction of $0.608383$, against $6/\pi^2 \approx 0.607927$.

**Non-example of a false rule.** Coprimality is not transitive: $\gcd(6, 35) = 1$ and $\gcd(35, 4) = 1$, but $\gcd(6, 4) = 2$.

## Related definitions

- [Greatest common divisor](/greatest-common-divisor/): coprime means that it is $1$.
- [Bézout's identity](/bezouts-identity/): gives condition 2.
- [Euclid's lemma](/euclids-lemma/): Gauss's lemma for a prime divisor.
- [Euler's totient](/euler-totient/): the number of residues coprime to $n$.
- [Modular inverse](/modular-inverse/): exists exactly for residues coprime to the modulus.
- [Reducing fractions](/reducing-fractions/): a fraction $p/q$ is in lowest terms when $\gcd(p, q) = 1$.
- [Farey sequence](/farey-sequence/): the reduced fractions with bounded denominator, all built from coprime pairs.

## References
