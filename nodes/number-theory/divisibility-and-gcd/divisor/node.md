---
tag: DRRA5H
kind: definition
slug: divisor
name: Divisor
aliases:
- factor
- proper divisor
area: number-theory/divisibility-and-gcd
level: intro
summary: An integer d that divides n; a proper divisor is one other than 1 and n.
prereqs: [divisibility]
see_also: [divisor-function, enumerating-divisors, prime-number, greatest-common-divisor, fundamental-theorem-of-arithmetic, trial-division]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.1, Elementary number-theoretic notions (divisors, trivial divisors and factors)
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Chapter 1, Section 1.1 (divisors), and Chapter 16 (the functions d(n) and sigma(n) from the factorization)
  - book: isbn:9780387901633
    title: Tom M. Apostol, Introduction to Analytic Number Theory
    locator: Chapter 1, Section 1.2 (divisors), and Chapter 2, Section 2.13 (the divisor functions)
---

A divisor of an integer $n$ is an integer $d$ that [divides](/divisibility/) $n$, that is, $n = kd$ for some integer $k$. The positive divisors of a positive integer come in pairs $d$ and $n/d$, one of them at most $\sqrt n$, which is why [trial division](/trial-division/) up to $\sqrt n$ finds them all. Through the [fundamental theorem of arithmetic](/fundamental-theorem-of-arithmetic/), the divisors of $n$ are exactly the products of the prime powers of $n$ with smaller or equal exponents. The words "proper" and "nontrivial" divisor have two conventions, given below.

## Definition

Let $n$ be an integer. An integer $d$ is a **divisor** (or **factor**) of $n$ if $d \mid n$, that is, if $n = kd$ for some integer $k$. For $n \ne 0$, the integer $n / d$ is the **complementary divisor** of $d$.

For $n \ge 1$ we write

$$\mathcal{D}(n) = \{ d \in \mathbb{Z} : d \ge 1, \ d \mid n \}$$

for the set of **positive divisors**. Number theory uses positive divisors unless it says otherwise: the negative divisors of $n$ are the numbers $-d$ with $d \in \mathcal{D}(n)$. The number of positive divisors is $\tau(n) = |\mathcal{D}(n)|$, also written $d(n)$, and their sum is $\sigma(n)$. The page [divisor function](/divisor-function/) covers these functions.

**Trivial, proper and nontrivial divisors.** The divisors $\pm 1$ and $\pm n$ are the **trivial divisors** of $n$. Two conventions for "proper" are in use:

- A **proper divisor** of $n \ge 1$ is a positive divisor $d \ne n$. This is the convention of perfect numbers and aliquot sums: $n$ is perfect when it is the sum of its proper divisors.
- Some books, CLRS among them, call a positive divisor $d$ with $1 < d < n$ a **nontrivial** (or proper) divisor, and use the word "factor" for it.

So $1$ is a proper divisor of $12$ in the first convention but not in the second. A page that uses the word says which convention it means. A positive integer $n > 1$ with no nontrivial divisor is a [prime number](/prime-number/).

**The divisors of zero.** Each integer divides $0$, so $0$ has infinitely many divisors. For $n \ne 0$, each divisor satisfies $1 \le |d| \le |n|$ (if $n = kd$ with $n \ne 0$ then $k \ne 0$, so $|n| = |k| \, |d| \ge |d|$), so the set of divisors is finite. Signs do not matter: $d \mid n$ if and only if $|d| \mid |n|$, so $\mathcal{D}(-n) = \mathcal{D}(n)$ when the definition is extended to $n \le -1$.

### The pairing $d \leftrightarrow n/d$

Let $n \ge 1$. The map $d \mapsto n/d$ sends $\mathcal{D}(n)$ to itself, because $n = (n/d) \cdot d$ shows that $n/d$ is a positive divisor too. The map is its own inverse, so it is a bijection. Three facts follow.

1. **One of each pair is small.** If $d \le n/d$ then $d^2 \le n$, so $d \le \sqrt n$. So each pair $\{d, n/d\}$ has an element at most $\sqrt n$, and a scan of $1, 2, \ldots, \lfloor \sqrt n \rfloor$ finds every divisor of $n$ together with its partner.
2. **A bound on the count.** Each divisor is $d$ or $n/d$ for some $d \le \sqrt n$, so $\tau(n) \le 2 \lfloor \sqrt n \rfloor$.
3. **Odd count means square.** A divisor is its own partner exactly when $d = n/d$, that is, $d^2 = n$. The other divisors fall into pairs of two distinct elements. So $\tau(n)$ is odd if and only if $n$ is a perfect square.

### Divisors from the prime factorization

Let $n = p_1^{e_1} p_2^{e_2} \cdots p_r^{e_r}$ with distinct primes $p_i$ and exponents $e_i \ge 1$.

**Claim.** The positive divisors of $n$ are exactly the numbers $p_1^{f_1} \cdots p_r^{f_r}$ with $0 \le f_i \le e_i$ for each $i$, and different exponent vectors give different divisors. So $\tau(n) = \prod_{i=1}^{r} (e_i + 1)$.

*Proof.* Each such product divides $n$: the quotient is $p_1^{e_1 - f_1} \cdots p_r^{e_r - f_r}$, an integer. Conversely, let $d \mid n$ with $d \ge 1$, so $n = dk$ with $k \ge 1$. A prime $p$ that divides $d$ divides $n$, so by [Euclid's lemma](/euclids-lemma/) it is one of the $p_i$. So $d = \prod p_i^{f_i}$ and $k = \prod p_i^{g_i}$ with $f_i, g_i \ge 0$, and $n = \prod p_i^{f_i + g_i}$. By the uniqueness part of the [fundamental theorem of arithmetic](/fundamental-theorem-of-arithmetic/), $f_i + g_i = e_i$, so $f_i \le e_i$. Two different exponent vectors give two different numbers, again by uniqueness. The number of vectors is $\prod (e_i + 1)$. $\square$

The page [enumerating divisors](/enumerating-divisors/) turns this claim into an algorithm that lists the divisors in time proportional to their number.

## Examples and non-examples

| $n$ | factorization | positive divisors | $\tau(n)$ | sum of proper divisors ($d \ne n$) |
|---|---|---|---|---|
| 1 | (empty) | 1 | 1 | 0 |
| 12 | $2^2 \cdot 3$ | 1, 2, 3, 4, 6, 12 | 6 | 16 |
| 28 | $2^2 \cdot 7$ | 1, 2, 4, 7, 14, 28 | 6 | 28 |
| 36 | $2^2 \cdot 3^2$ | 1, 2, 3, 4, 6, 9, 12, 18, 36 | 9 | 55 |
| 60 | $2^2 \cdot 3 \cdot 5$ | 1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60 | 12 | 108 |
| 97 | $97$ | 1, 97 | 2 | 1 |

- The divisors of $12$ pair up as $(1, 12)$, $(2, 6)$, $(3, 4)$. Each pair has one element at most $\sqrt{12} \approx 3.46$.
- $36$ is a square, and $6$ is its own partner. So $\tau(36) = 9$ is odd. From the factorization, $\tau(36) = (2+1)(2+1) = 9$.
- $28$ is a perfect number: its proper divisors in the first convention sum to $28$.
- $97$ is prime: its only positive divisors are $1$ and itself, so it has no nontrivial divisor.
- The divisors of $-12$ are $\pm 1, \pm 2, \pm 3, \pm 4, \pm 6, \pm 12$, the same as those of $12$ with both signs.

**Non-examples.**

- $5$ is not a divisor of $12$: $12 = 2 \cdot 5 + 2$, with remainder $2$.
- $24$ is not a divisor of $12$, because a divisor of a non-zero $n$ is at most $|n|$ in absolute value. It is a multiple of $12$.
- $0$ is a divisor of no integer except $0$.
- $2.5$ is not a divisor of $5$ in the sense of this page, although $5 = 2 \cdot 2.5$: divisors and the factor $k$ are integers.

## Related definitions

- [Divisibility](/divisibility/): the relation $d \mid n$ itself.
- [Divisor function](/divisor-function/): $\tau(n)$, $\sigma(n)$ and $\sigma_k(n)$.
- [Enumerating divisors](/enumerating-divisors/): the problem of listing $\mathcal{D}(n)$.
- [Greatest common divisor](/greatest-common-divisor/): the largest common element of $\mathcal{D}(a)$ and $\mathcal{D}(b)$.
- [Prime number](/prime-number/): an integer $n > 1$ with $\mathcal{D}(n) = \{1, n\}$.
- [Trial division](/trial-division/): finds a divisor by the pairing argument above.
- [Fundamental theorem of arithmetic](/fundamental-theorem-of-arithmetic/): the factorization that describes all divisors.

## References
