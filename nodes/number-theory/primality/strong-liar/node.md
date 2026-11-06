---
tag: KPG4XY
kind: concept
slug: strong-liar
name: Strong liar
aliases:
- strong liar to primality
- Miller-Rabin liar
area: number-theory/primality
level: core
summary: A base a for which an odd composite n passes the Miller-Rabin check. For n > 9 at most a quarter of the units modulo n are strong liars, so each round errs with probability below 1/4.
prereqs: [strong-pseudoprime, multiplicative-group-modulo-n, subgroup]
see_also: [miller-rabin, miller-rabin-error-bound, compositeness-witness, deterministic-miller-rabin-bases, euler-jacobi-pseudoprime, carmichael-number, nontrivial-square-root-of-one, solovay-strassen]
sources:
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Section 3.5 (Theorem 3.5.4, Lemmas 3.5.8 and 3.5.9 and the proof of Theorem 3.5.4), Section 3.5.1 (Theorems 3.5.11 and 3.5.12), and Exercise 3.15
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography
    locator: Chapter 4, Section 4.2.3 (Definition 4.21, Example 4.22, Fact 4.23, Remark 4.26, Example 4.27, Remark 4.28) and Section 4.2.4 (Fact 4.30, Example 4.31, Fact 4.32)
---

A strong liar for an odd composite number $n$ is a base $a$ for which $n$ passes the check of the [Miller-Rabin test](/miller-rabin/), so that $n$ is a [strong pseudoprime](/strong-pseudoprime/) to the base $a$. The bases that are not liars are the strong witnesses, and each of them proves that $n$ is composite. The key fact is the Monier-Rabin theorem: for $n > 9$, at most a quarter of the units modulo $n$ are strong liars, so a random base exposes $n$ with probability above $3/4$.

## In plain words

A test for primes checks one base at a time. For a composite number, most bases make the check fail and show that the number is composite. A few bases let the composite pass; they lie about it. A strong liar is such a base for the Miller-Rabin check, which is the strictest of the common checks. Every composite number has some liars, at least the two trivial bases, but never many: fewer than one base in four. So a test that picks bases at random catches every composite number quickly, and each new base cuts the chance of a mistake by a factor of four or more.

## The idea

**Definition** (HAC Definition 4.21). Let $n$ be odd and composite, and write $n - 1 = 2^s t$ with $t$ odd. An integer $a$ with $1 \le a \le n - 1$ is a **strong liar** for $n$ if
$$a^t \equiv 1 \pmod n \quad \text{or} \quad a^{2^i t} \equiv -1 \pmod n \text{ for some } 0 \le i < s.$$
Otherwise $a$ is a **strong witness** for $n$, a kind of [compositeness witness](/compositeness-witness/). Write $\mathcal{S}(n)$ for the set of strong liars and $S(n)$ for its size (Crandall and Pomerance, (3.5)). Each strong liar is a unit, since $a^{n-1} \equiv 1$. The bases $1$ and $n - 1$ are always liars, because $(n-1)^t \equiv -1$ for odd $t$.

**Inclusions** (HAC Fact 4.30). Each strong liar is an Euler liar (a base that fools the [Solovay-Strassen test](/solovay-strassen/)), and each Euler liar is a Fermat liar. If $n \equiv 3 \pmod 4$, the strong liars and the Euler liars are the same set (HAC Fact 4.32).

**Not a subgroup.** The Fermat liars and the Euler liars form [subgroups](/subgroup/) of the [group of units](/multiplicative-group-modulo-n/) $\mathbb{Z}_n^*$. The strong liars need not: the product of two strong liars is often a strong liar, but not always (HAC Remark 4.28). Among the 2217 odd composites below 6000, 264 have a set $\mathcal{S}(n)$ that is not closed under products, and each of them is $\equiv 1 \pmod 4$, as the case $n \equiv 3 \pmod 4$ requires.

**A subgroup that contains them** (Crandall and Pomerance, Lemma 3.5.8). Let $\nu = \nu(n)$ be the largest integer such that $2^\nu$ divides $p - 1$ for every prime $p \mid n$, and let $m = 2^{\nu - 1} t$. Every strong liar satisfies $a^m \equiv \pm 1 \pmod n$. *Proof.* If $a^t \equiv 1$, then $a^m \equiv 1$. Otherwise $a^{2^i t} \equiv -1$ for some $i$. For each prime $p \mid n$, the order of $a$ modulo $p$ is then divisible by exactly $2^{i+1}$ and divides $p - 1$, so $i + 1 \le \nu$, and $a^m = (a^{2^i t})^{2^{\nu - 1 - i}}$ is $-1$ if $i + 1 = \nu$ and $1$ otherwise. $\square$ The set $\bar{\mathcal{S}}(n) = \{a : a^m \equiv \pm 1\}$ is a subgroup, and Lemma 3.5.9 counts it with the [Chinese remainder theorem](/chinese-remainder-theorem/):
$$|\bar{\mathcal{S}}(n)| = 2 \cdot 2^{(\nu - 1) \omega(n)} \prod_{p \mid n} \gcd(t, p - 1),$$
where $\omega(n)$ is the number of distinct prime factors of $n$.

**Exact count** (Monier; Crandall and Pomerance, Exercise 3.15).
$$S(n) = \left(1 + \frac{2^{\nu \omega(n)} - 1}{2^{\omega(n)} - 1}\right) \prod_{p \mid n} \gcd(t, p - 1).$$
The formula agrees with a direct count for every odd composite $n < 6000$.

**The Monier-Rabin bound** (Crandall and Pomerance, Theorem 3.5.4; HAC Fact 4.23). For every odd composite $n > 9$, $S(n) \le \varphi(n)/4$. The proof bounds the larger set $\bar{\mathcal{S}}(n)$: each factor $(p - 1)/(2^{\nu - 1} \gcd(t, p - 1))$ is even, which gives $\varphi(n)/|\bar{\mathcal{S}}(n)| \ge 4$ when $n$ has three or more prime factors. Two prime factors with $n$ not squarefree give at least 6. For $n = pq$ with $p < q$, either $2^{\nu + 1} \mid q - 1$, or $q - 1 \nmid n - 1$ forces an odd prime to divide $q - 1$ more often than $n - 1$; either way the ratio is at least 4. For $n = p^k$ with $k \ge 2$ the ratio is $p^{k-1} \ge 5$, except for $n = 9$. The bound gives the error $4^{-k}$ of $k$ rounds of Miller-Rabin; see [the error bound](/miller-rabin-error-bound/).

**Most composites have far fewer.** The bound $\varphi(n)/4$ is the worst case. For most $n$ the number of strong liars is much smaller (HAC Remark 4.26), and for some $n$ it is the minimum of 2.

## Examples

**$n = 65 = 5 \cdot 13$** (HAC Example 4.31). Of the 48 units, 16 are Fermat liars, 8 are Euler liars and 6 are strong liars: $\mathcal{S}(65) = \{1, 8, 18, 47, 57, 64\}$. Here $64 = 2^6$, so $t = 1$ and $\nu = 2$, and Monier's formula gives $(1 + 15/3) \cdot 1 = 6$. The set is not closed: $8 \cdot 18 = 144 \equiv 14 \pmod{65}$, and $14$ is an Euler liar but not a strong liar.

**$n = 91 = 7 \cdot 13$** (HAC Example 4.22). There are 18 strong liars, $\{1, 9, 10, 12, 16, 17, 22, 29, 38, 53, 62, 69, 74, 75, 79, 81, 82, 90\}$, out of $\varphi(91) = 72$, so the bound $\varphi(n)/4$ is attained. With $90 = 2 \cdot 45$, $\nu = 1$ and $\gcd(45, 6) = \gcd(45, 12) = 3$, the formula gives $(1 + 3/3) \cdot 9 = 18$. Below 6000 the bound is attained only by $15 = 3 \cdot 5$, $91 = 7 \cdot 13$, $703 = 19 \cdot 37$ and $1891 = 31 \cdot 61$, each of the form $p(2p - 1)$.

**$n = 561 = 3 \cdot 11 \cdot 17$.** This [Carmichael number](/carmichael-number/) has all 320 units as Fermat liars, but only 80 Euler liars and 10 strong liars. With $560 = 2^4 \cdot 35$ and $p - 1 = 2, 10, 16$, $\nu = 1$, $\omega = 3$, and the formula gives $(1 + 7/7) \cdot (1 \cdot 5 \cdot 1) = 10$.

**Few liars** (HAC Example 4.27). For $n = 105 = 3 \cdot 5 \cdot 7$ the only strong liars are $1$ and $104$. The same holds for every product of the first $k \ge 2$ odd primes, such as $15$, $1155$ and $15015$.

**The exception $n = 9$.** $8 = 2^3 \cdot 1$, and the strong liars are $1$ and $8$. That is $2$ out of $\varphi(9) = 6$, more than a quarter, which is why Theorem 3.5.4 needs $n > 9$; it is still less than a quarter of the $8$ values in $[1, 8]$.

## Where it is used

- **Error of Miller-Rabin.** A random base in $[2, n - 2]$ is a strong liar with probability at most $(\varphi(n)/4 - 2)/(n - 3) < 1/4$ for $n > 9$, so $k$ independent rounds err with probability below $4^{-k}$ on every odd composite. See [Miller-Rabin](/miller-rabin/) and [the error bound](/miller-rabin-error-bound/).
- **Deterministic bases.** A list of bases that contains a strong witness for every odd composite below a bound gives a deterministic test below that bound; see [deterministic Miller-Rabin bases](/deterministic-miller-rabin-bases/). No finite list works for all $n$: there are infinitely many odd composites whose least witness exceeds $(\ln n)^{1/(3 \ln \ln \ln n)}$ (Crandall and Pomerance, Theorem 3.5.11).
- **Miller's test under ERH.** If the extended Riemann hypothesis holds, every odd composite $n$ has a strong witness below $2 (\ln n)^2$ (Crandall and Pomerance, Theorem 3.5.12, from Bach). Testing all those bases decides primality in deterministic polynomial time, on that hypothesis.
- **Factoring from a witness.** When a witness $a$ gives $x = a^{2^i t}$ with $x^2 \equiv 1$ and $x \not\equiv \pm 1$, $x$ is a [nontrivial square root of one](/nontrivial-square-root-of-one/), and $\gcd(x - 1, n)$ is a proper factor of $n$ (HAC, discussion after Algorithm 4.24).
- **Random prime generation.** Because random composites have few strong liars, one round of Miller-Rabin on a random large candidate errs far less often than $1/4$; see [random prime generation](/random-prime-generation/).

## References
