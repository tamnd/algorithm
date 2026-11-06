---
tag: XNH1YD
kind: concept
slug: euler-totient
name: Euler's totient function
aliases:
- phi function
- Euler phi
area: number-theory/modular-arithmetic
level: core
summary: Phi(n) counts the integers in 1..n coprime to n.
prereqs: [congruence, greatest-common-divisor, coprime-integers, fundamental-theorem-of-arithmetic]
see_also: [euler-theorem, multiplicative-group-modulo-n, carmichael-function, totient-divisor-sum, euler-phi-sieve, multiplicative-function, chinese-remainder-theorem, rsa-cryptosystem]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.3, Modular arithmetic (the size of Z_n^* is phi(n), the product formula over the primes dividing n)
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Chapter 5 (Euler's function and the sum over divisors), Chapter 16 (phi as an arithmetical function), and Chapter 18 (the order of magnitude and the average order of phi)
  - book: isbn:9780521516440
    title: Victor Shoup, A Computational Introduction to Number Theory and Algebra, second edition
    locator: Section 2.6, Euler's phi function, and Section 10.4, Factoring and computing Euler's phi function
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Section 4.9, Phi and Mu
  - url: https://en.wikipedia.org/wiki/Euler%27s_totient_function
    title: Euler's totient function, Wikipedia
    locator: section History and naming (Euler 1763, Gauss's notation, Sylvester's word totient)
---

Euler's totient function $\varphi(n)$ counts the integers $k$ with $1 \le k \le n$ that are [coprime](/coprime-integers/) to $n$. It is the number of residue classes modulo $n$ that have a [modular inverse](/modular-inverse/), so it is the size of the [multiplicative group modulo n](/multiplicative-group-modulo-n/), and it is the exponent in [Euler's theorem](/euler-theorem/) $a^{\varphi(n)} \equiv 1 \pmod n$. From the prime factorization of $n$ it follows from the product formula $\varphi(n) = n \prod_{p \mid n} (1 - 1/p)$. Without the factorization no fast method is known, and for $n = pq$ computing $\varphi(n)$ is as hard as factoring $n$, which the [RSA cryptosystem](/rsa-cryptosystem/) relies on.

## In plain words

Pick a whole number. Now count the numbers from one up to it that share no common factor with it, other than one. That count is the totient.

For a prime, every smaller number shares no factor with it, so the count is the prime minus one. For twelve, only one, five, seven and eleven qualify, so the count is four.

The count matters because these are exactly the numbers that you can divide by when you compute with remainders. It also tells you after how many steps the powers of such a number come back to one. You can compute the totient fast if you know the prime factors of the number. Without them, nobody knows a fast way.

## The idea

**Definition.** For an integer $n \ge 1$,

$$\varphi(n) = \#\{k \in \mathbb{Z} : 1 \le k \le n,\ \gcd(k, n) = 1\}.$$

So $\varphi(1) = 1$, since $\gcd(1, 1) = 1$. For $n \ge 2$, $k = n$ is never counted, and $\varphi(n)$ is also the number of residues in $0$ to $n - 1$ that are coprime to $n$, which is $|(\mathbb{Z}/n\mathbb{Z})^*|$. The residues coprime to $n$ are exactly the invertible ones: if $\gcd(a, n) = 1$, [Bézout's identity](/bezouts-identity/) gives $ax + ny = 1$, so $ax \equiv 1$; and if $ax \equiv 1$, then $ax - ny = 1$ for some $y$, so each common divisor of $a$ and $n$ divides $1$.

**Primes and prime powers.** For a prime $p$ and $k \ge 1$, the integers in $1$ to $p^k$ that are not coprime to $p^k$ are the multiples of $p$, and there are $p^{k-1}$ of them. So

$$\varphi(p^k) = p^k - p^{k-1} = p^{k-1}(p - 1), \qquad \varphi(p) = p - 1.$$

**Multiplicativity.** If $\gcd(m, n) = 1$, then $\varphi(mn) = \varphi(m)\varphi(n)$.

*Proof.* By the [Chinese remainder theorem](/chinese-remainder-theorem/), the map $x \mapsto (x \bmod m, x \bmod n)$ is a bijection from $\{0, \ldots, mn - 1\}$ to $\{0, \ldots, m - 1\} \times \{0, \ldots, n - 1\}$. An integer $x$ is coprime to $mn$ if and only if it is coprime to $m$ and to $n$, since a prime divides $mn$ exactly when it divides $m$ or $n$ ([Euclid's lemma](/euclids-lemma/)). And $\gcd(x, m) = \gcd(x \bmod m, m)$. So the bijection maps the residues coprime to $mn$ exactly onto the pairs of a residue coprime to $m$ and a residue coprime to $n$. Counting both sides gives $\varphi(mn) = \varphi(m)\varphi(n)$. $\square$

So $\varphi$ is a [multiplicative function](/multiplicative-function/), though not completely multiplicative: $\varphi(4) = 2 \ne \varphi(2)^2 = 1$.

**The product formula.** If $n = p_1^{k_1} \cdots p_r^{k_r}$ is the [prime factorization](/fundamental-theorem-of-arithmetic/) of $n$ with distinct primes $p_i$ and $k_i \ge 1$, multiplicativity and the prime-power case give

$$\varphi(n) = \prod_{i=1}^{r} p_i^{k_i - 1}(p_i - 1) = n \prod_{p \mid n} \left(1 - \frac{1}{p}\right).$$

The same formula follows from inclusion and exclusion. For distinct primes $q_1, \ldots, q_j$ that divide $n$, exactly $n / (q_1 \cdots q_j)$ of the integers in $1$ to $n$ are divisible by all of them. So the number of integers divisible by none of the $p_i$ is $\sum_{S \subseteq \{1, \ldots, r\}} (-1)^{|S|} n / \prod_{i \in S} p_i$, and this sum factors as $n \prod_i (1 - 1/p_i)$.

**Gauss's divisor sum.** For each $n \ge 1$,

$$\sum_{d \mid n} \varphi(d) = n.$$

*Proof.* Sort the integers $k$ in $1$ to $n$ by $g = \gcd(k, n)$. Write $k = g j$; then $\gcd(j, n/g) = 1$ and $1 \le j \le n/g$, and each such $j$ gives a $k$ with $\gcd(k, n) = g$. So exactly $\varphi(n/g)$ integers have gcd $g$. Summing over the divisors $g$ of $n$ counts all $n$ integers once, and $n/g$ runs over the divisors of $n$ as $g$ does. $\square$

The page [totient divisor sum](/totient-divisor-sum/) covers this identity, and [Möbius inversion](/mobius-inversion-formula/) turns it into $\varphi(n) = \sum_{d \mid n} \mu(d) \, n/d$.

**Other facts.**

- $\varphi(n) = n - 1$ if and only if $n$ is prime, for $n \ge 2$: a composite $n$ has a divisor $d$ with $1 < d < n$, which is not counted.
- $\varphi(n)$ is even for $n \ge 3$: if $n$ has an odd prime factor $p$, then $p - 1$ is an even factor of $\varphi(n)$; otherwise $n = 2^k$ with $k \ge 2$ and $\varphi(n) = 2^{k-1}$.
- The size of $\varphi(n)/n$ is $\prod_{p \mid n}(1 - 1/p)$. It can be small, but only slowly: $\varphi(n) \ge c \, n / \ln \ln n$ for some constant $c > 0$ and all $n \ge 3$. Hardy and Wright (Chapter 18) prove that $\liminf \varphi(n) \ln \ln n / n = e^{-\gamma}$, where $\gamma$ is the Euler-Mascheroni constant.
- The average order is $\sum_{k \le N} \varphi(k) = \frac{3}{\pi^2} N^2 + O(N \log N)$ (Hardy and Wright, Chapter 18). So about $6/\pi^2 \approx 61$ percent of the residues are units on average, which is also the probability that two random integers are coprime.

**Computing $\varphi(n)$.**

- *From a factorization.* Apply the product formula, with integer arithmetic: start with $r = n$, and for each prime $p \mid n$ replace $r$ by $r / p \cdot (p - 1)$. The division is exact at each step. With [trial division](/trial-division/) to find the primes, this takes $O(n^{1/2})$ divisions.
- *For all $n \le N$.* A sieve computes the whole table in $O(N \log \log N)$ time, or $O(N)$ with the [linear sieve](/linear-sieve/); see [Euler phi sieve](/euler-phi-sieve/) and [totient values up to n](/totient-values-up-to-n/).
- *Without a factorization.* For $n = pq$ with distinct primes, $\varphi(n) = n - (p + q) + 1$. So from $n$ and $\varphi(n)$ one gets $p + q = n - \varphi(n) + 1$ and then $p$ and $q$ as the roots of $x^2 - (p + q)x + n$. Thus computing $\varphi$ of an RSA modulus is as hard as factoring it. For general $n$, Shoup (Section 10.4) shows that $\varphi(n)$ gives a randomized polynomial-time factoring algorithm.

## Examples

The first values:

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $\varphi(n)$ | 1 | 1 | 2 | 2 | 4 | 2 | 6 | 4 | 6 | 4 | 10 | 4 | 12 | 6 | 8 | 8 |

- $\varphi(36)$: $36 = 2^2 \cdot 3^2$, so $\varphi(36) = 36 \cdot \frac12 \cdot \frac23 = 12$. The units are $1, 5, 7, 11, 13, 17, 19, 23, 25, 29, 31, 35$.
- $\varphi(1000) = 1000 \cdot \frac12 \cdot \frac45 = 400$, so $40$ percent of the residues modulo $1000$ are invertible.
- $\varphi(64) = 32$: half of the residues modulo a power of two, the odd ones, are units.
- $\varphi(97) = 96$, since $97$ is prime.
- **Divisor sum.** For $n = 12$: $\varphi(1) + \varphi(2) + \varphi(3) + \varphi(4) + \varphi(6) + \varphi(12) = 1 + 1 + 2 + 2 + 2 + 4 = 12$.
- **RSA.** For $n = 3233 = 61 \cdot 53$, $\varphi(n) = 60 \cdot 52 = 3120$. Conversely, from $n = 3233$ and $\varphi(n) = 3120$: $p + q = 3233 - 3120 + 1 = 114$, and the roots of $x^2 - 114x + 3233$ are $61$ and $53$.
- **Average.** $\sum_{k=1}^{1000} \varphi(k) = 304192$, against $3 \cdot 1000^2 / \pi^2 \approx 303964$.
- **A small value.** Below $10^4$, the smallest ratio $\varphi(n)/n$ is at $n = 2310 = 2 \cdot 3 \cdot 5 \cdot 7 \cdot 11$, with $\varphi(2310)/2310 = 480/2310 \approx 0.208$. The ratio is smallest at products of the first primes.

## Where it is used

- [Euler's theorem](/euler-theorem/): $a^{\varphi(n)} \equiv 1 \pmod n$ for $\gcd(a, n) = 1$, which reduces exponents modulo $\varphi(n)$.
- [RSA](/rsa-cryptosystem/): the private exponent is the inverse of the public one modulo $\varphi(n)$ (or modulo the [Carmichael function](/carmichael-function/) $\lambda(n)$, which divides it).
- [Multiplicative group modulo n](/multiplicative-group-modulo-n/): its order is $\varphi(n)$, so the order of each element divides $\varphi(n)$ by [Lagrange's theorem](/lagranges-theorem-group-theory/).
- [Primitive roots](/primitive-root/): when they exist modulo $n$, there are exactly $\varphi(\varphi(n))$ of them.
- Counting: the number of reduced fractions in $(0, 1]$ with denominator $n$ is $\varphi(n)$, so the [Farey sequence](/farey-sequence/) of order $N$ has $1 + \sum_{k \le N} \varphi(k)$ terms.
- [Cyclic groups](/cyclic-group/): a cyclic group of order $n$ has exactly $\varphi(n)$ generators, and $\varphi(d)$ elements of each order $d \mid n$.

## References
