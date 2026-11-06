---
tag: FZE2NP
kind: definition
slug: pseudoprime
name: Pseudoprime
aliases:
- psp
- base-a pseudoprime
area: number-theory/primality
level: intro
summary: A composite number that passes a given primality test for some base, so that the test takes it for a prime.
prereqs: [prime-number, probable-prime, fermat-little-theorem]
see_also: [fermat-pseudoprime, euler-jacobi-pseudoprime, strong-pseudoprime, carmichael-number, strong-liar, baillie-psw, deterministic-miller-rabin-bases, compositeness-witness]
sources:
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Section 3.4 (Theorems 3.4.2, 3.4.4 and 3.4.7), Section 3.5 (Definition 3.5.3, Theorem 3.5.4), Section 3.6.1 (Definitions 3.6.2 and 3.6.4) and Exercise 3.41
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography
    locator: Chapter 4, Definitions 4.7, 4.15, 4.21 and 4.29, Table 4.1 and Fact 4.30
  - paper: doi:10.1090/S0025-5718-1980-0572872-7
    title: Carl Pomerance, J. L. Selfridge and Samuel S. Wagstaff Jr., The pseudoprimes to 25·10^9, Mathematics of Computation 35 (1980)
    locator: pages 1003 to 1026
---

A pseudoprime is a composite number that passes a [primality test](/primality-testing/) that every [prime](/prime-number/) passes, for a given base or parameter. The test then calls it a [probable prime](/probable-prime/), and the answer is wrong. The word always goes with a test: there are [Fermat pseudoprimes](/fermat-pseudoprime/), [Euler-Jacobi pseudoprimes](/euler-jacobi-pseudoprime/), [strong pseudoprimes](/strong-pseudoprime/), Lucas pseudoprimes and others, and without a qualifier "pseudoprime base $a$" means the Fermat kind. Pseudoprimes are rare, and this is why fast probabilistic tests work.

## Definition

Let $P(n, a)$ be a property of an integer $n \ge 2$ and a parameter $a$ such that $P(p, a)$ holds for each prime $p$ and each parameter $a$ allowed for $p$. A **pseudoprime for $P$ with parameter $a$** is a composite $n$ for which $P(n, a)$ holds. Equivalently, it is a composite probable prime for the test that checks $P$. For a composite $n$, the parameters $a$ with $P(n, a)$ are the *liars* for $n$ and the others are the [witnesses](/compositeness-witness/).

The standard families, for a composite $n$ and an integer $a$:

| Name | Condition on $n$ and $a$ | Holds for each prime because of |
|---|---|---|
| Fermat pseudoprime base $a$ | $a^{n-1} \equiv 1 \pmod n$ | [Fermat's little theorem](/fermat-little-theorem/) |
| Euler-Jacobi pseudoprime base $a$ | $n$ odd, $\gcd(a, n) = 1$, $a^{(n-1)/2} \equiv \left(\frac{a}{n}\right) \pmod n$ | [Euler's criterion](/euler-criterion/) and the [Jacobi symbol](/jacobi-symbol/) |
| Strong pseudoprime base $a$ | $n$ odd, $n - 1 = 2^s t$ with $t$ odd, $a^t \equiv 1$ or $a^{2^i t} \equiv -1 \pmod n$ for some $0 \le i < s$ | the only square roots of $1$ modulo a prime are $\pm 1$ |
| Lucas pseudoprime for $x^2 - ax + b$ | $\Delta = a^2 - 4b$ not a square, $\gcd(n, 2b\Delta) = 1$, $U_{n - (\Delta/n)} \equiv 0 \pmod n$ | Crandall and Pomerance, Theorem 3.6.3 |
| Fibonacci pseudoprime | the Lucas case $a = 1$, $b = -1$, so $U_j$ is the $j$-th Fibonacci number | the same theorem |

Here $(U_j)$ is the Lucas sequence with $U_0 = 0$, $U_1 = 1$ and $U_j = aU_{j-1} - bU_{j-2}$, and $(\Delta/n)$ is the Jacobi symbol. The Handbook of Applied Cryptography (Definitions 4.7, 4.15 and 4.21) restricts the first three families to odd $n$ and $1 \le a \le n - 1$; Crandall and Pomerance (Section 3.4.1) use the base range $1 < a < n - 1$ for the matching probable prime tests, because $a = 1$ and $a = n - 1$ make every odd $n$ pass.

**Inclusions.** For odd composite $n$ and $\gcd(a, n) = 1$, each strong pseudoprime base $a$ is an Euler-Jacobi pseudoprime base $a$, and each Euler-Jacobi pseudoprime base $a$ is a Fermat pseudoprime base $a$ (HAC Fact 4.30). The second inclusion follows by squaring, since $\left(\frac{a}{n}\right)^2 = 1$.

**Infinitely many for each base** (Crandall and Pomerance, Theorem 3.4.4). For each integer $a \ge 2$ there are infinitely many Fermat pseudoprimes base $a$. *Proof.* Let $p$ be an odd prime that does not divide $a^2 - 1$; all but finitely many primes qualify. Put

$$n = \frac{a^{2p} - 1}{a^2 - 1} = \frac{a^p - 1}{a - 1} \cdot \frac{a^p + 1}{a + 1}.$$

Both factors are integers greater than 1, so $n$ is composite. By Fermat's little theorem $a^{2p} \equiv a^2 \pmod p$, so $p$ divides $a^{2p} - a^2 = (a^2 - 1)(n - 1)$, and since $p \nmid a^2 - 1$, $p \mid n - 1$. Also $n - 1 = a^2 + a^4 + \cdots + a^{2p-2}$ is a sum of $p - 1$ terms of the same parity, and $p - 1$ is even, so $n - 1$ is even. Hence $2p \mid n - 1$, so $a^{2p} - 1$ divides $a^{n-1} - 1$, and $n$ divides $a^{2p} - 1$. So $a^{n-1} \equiv 1 \pmod n$. Different primes $p$ give different $n$, because $n$ grows with $p$. $\square$ For $a = 2$ and $p = 5$ this gives $n = 341$.

## Examples and non-examples

**Examples.**

- $341 = 11 \cdot 31$ is the smallest Fermat pseudoprime base 2. $91 = 7 \cdot 13$ is the smallest Fermat pseudoprime base 3.
- $1105 = 5 \cdot 13 \cdot 17$ is the smallest Fermat pseudoprime to both bases 2 and 3. It is a [Carmichael number](/carmichael-number/), a Fermat pseudoprime to each base coprime to it.
- $2047 = 23 \cdot 89$ is the smallest strong pseudoprime base 2. The smallest strong pseudoprimes to all of the first $t$ prime bases, $\psi_t$, are $2047$, $1373653$, $25326001$, $3215031751$ for $t = 1, 2, 3, 4$ (HAC Table 4.1).
- $323 = 17 \cdot 19$ is the smallest Fibonacci pseudoprime coprime to 10 (Crandall and Pomerance, Section 3.6.1).

The counts of odd composites $n < 10^5$ of each kind, against $9592$ primes below $10^5$:

| Kind | base 2 | base 3 | base 5 |
|---|---|---|---|
| Fermat pseudoprime | 78 | 76 | 66 |
| Strong pseudoprime | 16 | 23 | 16 |

In the same range there are 36 Euler-Jacobi pseudoprimes base 2, 50 Fibonacci pseudoprimes coprime to 10, and 16 Carmichael numbers. Below $10^6$ there are 245 Fermat and 46 strong pseudoprimes base 2.

**Non-examples.**

- A prime is never a pseudoprime, by definition. A probable prime is a pseudoprime only when it is composite.
- $341$ is not a Fermat pseudoprime base 3 ($3^{340} \equiv 56 \pmod{341}$), and not a strong pseudoprime base 2 ($2^{85} \equiv 32$, $2^{170} \equiv 1$). $91$ is not a Fermat pseudoprime base 2.
- $561$ is a Fermat pseudoprime to each base coprime to it, but not a strong pseudoprime base 2. No odd composite $n > 9$ is a strong pseudoprime to more than $\varphi(n)/4$ of the residues modulo $n$ (Crandall and Pomerance, Theorem 3.5.4), so the strong test has no analogue of Carmichael numbers.
- The three strong pseudoprimes base 2 below $10^6$ that are also Fibonacci pseudoprimes are $252601$, $741751$ and $873181$, and all three are $\equiv 1 \pmod 5$. No number $n \equiv \pm 2 \pmod 5$ is known that is both a Fermat pseudoprime base 2 and a Fibonacci pseudoprime. Pomerance, Selfridge and Wagstaff offer a prize of 620 dollars for an example or a proof that none exists (Crandall and Pomerance, Exercise 3.41). This open problem is the basis of the [Baillie-PSW](/baillie-psw/) test.

## Related definitions

- **[Probable prime](/probable-prime/).** A number that passes the test, prime or not.
- **[Compositeness witness](/compositeness-witness/) and [strong liar](/strong-liar/).** The bases that expose a composite, and those that do not.
- **[Carmichael number](/carmichael-number/).** A composite that is a Fermat pseudoprime to each base coprime to it. There are infinitely many (Alford, Granville and Pomerance; Crandall and Pomerance, Theorem 3.4.7).
- **Density.** For each fixed $a \ge 2$, the number of Fermat pseudoprimes base $a$ up to $x$ is $o(\pi(x))$, where $\pi$ is the [prime-counting function](/prime-counting-function/) (Crandall and Pomerance, Theorem 3.4.2). So among the probable primes base $a$ up to $x$, the fraction that is composite tends to 0.
- **[Deterministic Miller-Rabin bases](/deterministic-miller-rabin-bases/).** The values $\psi_t$ give ranges in which a fixed set of strong tests has no pseudoprime and so decides primality.

## References
