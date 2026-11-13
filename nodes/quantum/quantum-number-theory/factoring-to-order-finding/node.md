---
tag: 81DQS1
kind: theorem
slug: factoring-to-order-finding
name: Factoring reduces to order finding
aliases:
- Miller's reduction
- order-finding reduction
area: quantum/quantum-number-theory
level: advanced
summary: For odd N with k >= 2 distinct prime factors, a random unit a has even order r with a^(r/2) != -1 mod N with probability at least 1 - 1/2^(k-1); then gcd(a^(r/2) - 1, N) is a factor.
prereqs: [multiplicative-order, chinese-remainder-theorem, nontrivial-square-root-of-one, cyclic-group, order-finding]
see_also: [shor-algorithm, factoring-in-bqp, integer-factorization, miller-rabin-primality-test, carmichael-function, congruence-of-squares, rsa-cryptosystem, primitive-root]
sources:
  - paper: "Gary L. Miller, Riemann's hypothesis and tests for primality, Journal of Computer and System Sciences 13(3):300-317, 1976"
    title: Gary L. Miller, Riemann's hypothesis and tests for primality
    locator: factoring N from a multiple of the orders of its units, by square roots of 1
  - paper: doi:10.1137/S0097539795293172
    title: "Peter W. Shor, Polynomial-time algorithms for prime factorization and discrete logarithms on a quantum computer, SIAM Journal on Computing 26(5):1484-1509, 1997"
    locator: the section on factoring (the reduction to order finding and the probability of a good base)
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 5.3.2 (the reduction of factoring to order finding) and Appendix 4 (the proof of the probability bound)
  - url: https://www.michaelnielsen.org/qcqi/errata/errata.pdf
    title: Errata for Nielsen and Chuang, Quantum Computation and Quantum Information
    locator: the correction of the probability bound for a good base to 1 - 1/2^(m-1)
  - paper: arxiv:1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, 2019 and later versions
    locator: Section 5.2, Reduction from factoring to period-finding
---

This theorem reduces [integer factorization](/integer-factorization/) to [order finding](/order-finding/). For an odd $N$ with at least two distinct prime factors, the order $r$ of a random unit $a$ is even with $a^{r/2} \ne -1 \pmod N$ with probability at least $1/2$, and then $\gcd(a^{r/2} - 1, N)$ is a proper factor. It is the classical half of [Shor's algorithm](/shor-algorithm/): the quantum circuit finds $r$, and this theorem turns $r$ into a factor.

## Statement

Let $N = p_1^{e_1} \cdots p_k^{e_k}$ be odd, with $k \ge 2$ distinct primes $p_i$. For a unit $a \in \mathbb{Z}_N^*$, let $r$ be its [multiplicative order](/multiplicative-order/). Call $a$ **good** if $r$ is even and $a^{r/2} \not\equiv -1 \pmod N$.

**Theorem.**

1. If $a$ is good, then $y = a^{r/2} \bmod N$ is a [nontrivial square root of 1](/nontrivial-square-root-of-one/), and $\gcd(y - 1, N)$ and $\gcd(y + 1, N)$ are proper factors of $N$.
2. For $a$ uniform in $\mathbb{Z}_N^*$,
$$\Pr[a \text{ is good}] \ge 1 - \frac{1}{2^{k-1}} \ge \frac12.$$

For a prime power $N = p^e$ with $p$ odd, no unit is good, so prime powers must be found by a classical root test first.

## In plain words

Squaring undoes signs: both one and minus one square to one. For a prime modulus these are the only numbers that square to one. For a modulus made of two or more different primes there are other ones, and each of them shares a factor with the modulus that a greatest common divisor step can find.

If you know the cycle length of the powers of a number, half that length gives a power that squares to one. Most of the time this power is one of the extra ones, not minus one. So knowing cycle lengths is enough to split the modulus, and at least half of all starting numbers work.

## Proof

**Part 1.** Since $r$ is the order and $r/2 < r$, $y \not\equiv 1$. By assumption $y \not\equiv -1$, and $y^2 = a^r \equiv 1$. So $N$ divides $y^2 - 1 = (y - 1)(y + 1)$, but $N$ divides neither factor, as $0 < y - 1 < y + 1 < N$. Then $\gcd(y - 1, N)$ is not $N$; it is not 1 either, since otherwise $N$ would divide $y + 1$. The same holds for $y + 1$. $\square$

**Part 2.** By the [Chinese remainder theorem](/chinese-remainder-theorem/), the map $a \mapsto (a \bmod p_1^{e_1}, \dots, a \bmod p_k^{e_k})$ is a bijection from $\mathbb{Z}_N^*$ to the product of the groups $G_i = \mathbb{Z}_{p_i^{e_i}}^*$. So a uniform $a$ has independent uniform components $a_i$. Each $G_i$ is [cyclic](/cyclic-group/) of order $\varphi(p_i^{e_i}) = p_i^{e_i - 1}(p_i - 1)$, which is even because $p_i$ is odd. Let $r_i$ be the order of $a_i$ in $G_i$; then $r = \operatorname{lcm}(r_1, \dots, r_k)$. Write $v(x)$ for the exponent of 2 in $x$.

*Claim A: $a$ is bad exactly when $v(r_1) = v(r_2) = \cdots = v(r_k)$.*

Suppose all $v(r_i)$ equal $d$. If $d = 0$, every $r_i$ is odd, so $r$ is odd and $a$ is bad. If $d \ge 1$, then $v(r) = d$, so $r/2$ is an odd multiple of $r_i/2$ for each $i$. In the cyclic group $G_i$, the element $a_i^{r_i/2}$ has order 2, and the only element of order 2 in a cyclic group of even order is $-1$. So $a_i^{r/2} = (-1)^{\text{odd}} = -1$ modulo each $p_i^{e_i}$, hence $a^{r/2} \equiv -1 \pmod N$ and $a$ is bad.

Suppose the $v(r_i)$ are not all equal, and let $d = \max_i v(r_i) \ge 1$. Then $v(r) = d$, so $r$ is even. Take $j$ with $v(r_j) < d$. Then $r_j$ divides $r/2$, so $a_j^{r/2} = 1$ in $G_j$. As $p_j$ is odd, $1 \ne -1$ modulo $p_j^{e_j}$, so $a^{r/2} \not\equiv -1 \pmod N$, and $a$ is good.

*Claim B: in a cyclic group $G$ of order $2^t m$ with $m$ odd and $t \ge 1$, a uniform element $x$ has $\Pr[v(\operatorname{ord} x) = j] \le 1/2$ for each $j$.*

Let $g$ generate $G$ and write $x = g^e$ with $e$ uniform in $[0, 2^t m)$. The order of $g^e$ is $2^t m / \gcd(e, 2^t m)$, so $v(\operatorname{ord} x) = t - \min(v(e), t)$. It equals $t$ exactly when $e$ is odd, which has probability $1/2$. For $u = 1, \dots, t - 1$ it equals $t - u$ with probability $2^{-(u+1)}$, and it equals 0 with probability $2^{-t}$. Each of these is at most $1/2$.

Now write $P_i(j) = \Pr[v(r_i) = j]$. By Claim A, independence and Claim B,

$$\Pr[a \text{ is bad}] = \sum_{j \ge 0} \prod_{i=1}^{k} P_i(j) \le \sum_{j \ge 0} P_1(j) \cdot \Bigl(\frac12\Bigr)^{k-1} = \frac{1}{2^{k-1}}. \qquad \blacksquare$$

**Prime powers.** For $N = p^e$, the group is cyclic, so if $r$ is even, $a^{r/2}$ is the element of order 2, which is $-1$. So no unit is good.

## Consequences

- **A randomized reduction.** An algorithm that finds orders gives a factoring algorithm with expected $O(1)$ calls per split: test $N$ for evenness, for being a perfect power and for $\gcd(a, N) > 1$, then use the order. Together with the quantum order-finding circuit this gives [factoring in BQP](/factoring-in-bqp/).
- **A multiple of the order is enough.** If only a multiple $m$ of $r$ is known, write $m = 2^s d$ with $d$ odd and square $a^d$ until the value is 1. The last value before 1 is $a^{r/2}$, so the outcome is the same as with $r$. The same method works with any multiple of the [Carmichael function](/carmichael-function/) $\lambda(N)$, for all bases at once.
- **RSA keys.** For an [RSA](/rsa-cryptosystem/) key, $ed - 1$ is a multiple of $\lambda(N)$. So whoever knows the private exponent $d$ can factor $N$ in randomized polynomial time, and computing $d$ from the public key is as hard as factoring.
- **Squares and factoring.** A nontrivial square root of 1 is a special [congruence of squares](/congruence-of-squares/) $y^2 \equiv 1^2$; the sieve methods for factoring look for the same kind of relation.
- **Primality tests.** The [Miller-Rabin test](/miller-rabin-primality-test/) uses the same squaring sequence: a nontrivial square root of 1 proves that $N$ is composite.

## Tightness

The bound $1 - 1/2^{k-1}$ is reached exactly when every $p_i \equiv 3 \pmod 4$. Then each $\varphi(p_i^{e_i})$ has exactly one factor 2, so $P_i(0) = P_i(1) = 1/2$, and the sum in the proof equals $2 \cdot 2^{-k}$. If some $p_i \equiv 1 \pmod 4$, then $P_i$ is positive at three or more values of $j$, while another $P_{i'}$ can equal $1/2$ at most at two of them, so the inequality is strict.

| N | primes | units | good units | fraction | bound |
|---|---|---|---|---|---|
| 15 | 3, 5 | 8 | 6 | 3/4 | 1/2 |
| 21 | 3, 7 | 12 | 6 | 1/2 | 1/2 |
| 105 | 3, 5, 7 | 48 | 42 | 7/8 | 3/4 |
| 231 | 3, 7, 11 | 120 | 90 | 3/4 | 3/4 |

For $N = 21$ the bad units are 1, 4 and 16 (odd order), and 5, 17 and 20 (with $a^{r/2} = 20 = -1$). The good units include 2, with $2^3 = 8$ and $\gcd(7, 21) = 7$.

The condition that $N$ is odd matters: for $N = 2^e$ with $e \ge 3$ the group of units is not cyclic, and Claim B fails. An even $N$ is split at once by the factor 2.

## History

Miller (1976) showed that computing orders, or a multiple of the orders such as $\varphi(N)$, is enough to factor $N$, using square roots of 1; his paper also gave the primality test that became the Miller-Rabin test. Shor (1994) combined this classical reduction with his quantum order-finding circuit. The first printings of Nielsen and Chuang gave $1 - 1/2^m$ for $m$ prime factors, and the published errata correct it to $1 - 1/2^{m-1}$, which is tight for $N = 21$.

## References
