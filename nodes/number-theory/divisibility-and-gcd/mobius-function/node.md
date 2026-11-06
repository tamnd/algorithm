---
tag: BFV8DH
kind: definition
slug: mobius-function
name: Möbius function
aliases:
- mu function
- Möbius mu
area: number-theory/divisibility-and-gcd
level: core
summary: Mu(n) is 0 if n has a squared prime factor, else (-1)^k for k distinct primes.
prereqs: [fundamental-theorem-of-arithmetic, prime-number, divisor]
see_also: [mobius-inversion-formula, multiplicative-function, dirichlet-convolution, euler-totient, totient-divisor-sum, mobius-sieve, inclusion-exclusion-principle, prime-number-theorem]
sources:
  - book: isbn:9780387901633
    title: Tom M. Apostol, Introduction to Analytic Number Theory
    locator: Chapter 2, Section 2.2, The Möbius function (the definition and the divisor sum of mu), and Section 2.7, Dirichlet inverses and the Möbius inversion formula
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Section 16.3, The Möbius function
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Section 4.9, Phi and Mu (the definition of mu by its divisor sum and its values at prime powers)
  - url: "https://en.wikipedia.org/wiki/M%C3%B6bius_function"
    locator: lead and sections Properties and Mertens function (Möbius 1832, the divisor sum, the Dirichlet series 1/zeta(s), and the Mertens function)
---

The Möbius function $\mu(n)$ is the [multiplicative function](/multiplicative-function/) with $\mu(1) = 1$, $\mu(n) = (-1)^k$ when $n$ is a product of $k$ distinct [primes](/prime-number/), and $\mu(n) = 0$ when $n$ is divisible by the square of a prime. Its key property is $\sum_{d \mid n} \mu(d) = 0$ for every $n > 1$. That makes it the inverse of the constant function 1 under [Dirichlet convolution](/dirichlet-convolution/), which gives the [Möbius inversion formula](/mobius-inversion-formula/), and it makes $\mu(d)$ the sign in every [inclusion-exclusion](/inclusion-exclusion-principle/) over the prime divisors of a number.

## Definition

**Definition.** For a positive integer $n$,

$$\mu(n) = \begin{cases} 1 & \text{if } n = 1, \\ (-1)^k & \text{if } n = p_1 p_2 \cdots p_k \text{ with distinct primes } p_1, \ldots, p_k, \\ 0 & \text{if } p^2 \mid n \text{ for some prime } p. \end{cases}$$

The three cases cover every $n$, by the [fundamental theorem of arithmetic](/fundamental-theorem-of-arithmetic/). An integer $n$ with $\mu(n) \ne 0$ is called **squarefree**. The function is not defined at 0 or at negative integers.

**Multiplicativity.** If $\gcd(m, n) = 1$, then $mn$ is squarefree exactly when both $m$ and $n$ are, and then its prime count is the sum of the two counts, so $\mu(mn) = \mu(m) \mu(n)$. At prime powers, $\mu(p) = -1$ and $\mu(p^e) = 0$ for $e \ge 2$.

**Divisor sum.** For every positive integer $n$,

$$\sum_{d \mid n} \mu(d) = [n = 1] = \begin{cases} 1 & n = 1, \\ 0 & n > 1. \end{cases}$$

*Proof.* For $n = 1$ the sum is $\mu(1) = 1$. For $n > 1$, let $p_1, \ldots, p_k$ with $k \ge 1$ be the distinct primes that divide $n$. Only squarefree divisors contribute, and these are the products of subsets of $\{p_1, \ldots, p_k\}$. A subset of size $j$ contributes $(-1)^j$, so the sum is $\sum_{j=0}^{k} \binom{k}{j} (-1)^j = (1 - 1)^k = 0$. $\blacksquare$

Concrete Mathematics, Section 4.9, takes this identity together with $\mu(1) = 1$ as the definition of $\mu$: it fixes $\mu(n) = -\sum_{d \mid n, d < n} \mu(d)$ by induction.

**Computation.** One value $\mu(n)$ needs the factorization of $n$: [trial division](/trial-division/) gives it in $O(n^{1/2})$ divisions on the [word RAM](/word-ram/), and it can stop at the first repeated prime. All values $\mu(1), \ldots, \mu(N)$ follow in $O(N)$ word operations with the [Möbius sieve](/mobius-sieve/) or the [linear sieve](/linear-sieve/).

## Examples and non-examples

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $\mu(n)$ | 1 | $-1$ | $-1$ | 0 | $-1$ | 1 | $-1$ | 0 | 0 | 1 | $-1$ | 0 |

- $\mu(30) = \mu(2 \cdot 3 \cdot 5) = -1$, $\mu(210) = \mu(2 \cdot 3 \cdot 5 \cdot 7) = 1$ and $\mu(2310) = -1$.
- $\mu(12) = 0$ because $4 \mid 12$; $\mu(1) = 1$ although 1 has no prime factors ($k = 0$).
- Divisor sum for $n = 12$: $\mu(1) + \mu(2) + \mu(3) + \mu(4) + \mu(6) + \mu(12) = 1 - 1 - 1 + 0 + 1 + 0 = 0$.
- **Counting coprime integers.** The number of $k \le x$ with $\gcd(k, n) = 1$ is $\sum_{d \mid n} \mu(d) \lfloor x/d \rfloor$, by inclusion-exclusion over the primes of $n$. For $x = 100$ and $n = 30$: $100 - 50 - 33 - 20 + 16 + 10 + 6 - 3 = 26$. With $x = n$ this gives $\varphi(n) = \sum_{d \mid n} \mu(d)\, n/d$, the formula for [Euler's totient](/euler-totient/).
- **Counting squarefree integers.** The number of squarefree $n \le x$ is $\sum_{d \le \sqrt{x}} \mu(d) \lfloor x / d^2 \rfloor$. For $x = 100$ it is 61. As $x \to \infty$ the count is asymptotic to $6x/\pi^2$.
- **Mertens function.** $M(x) = \sum_{n \le x} \mu(n)$ has $M(10) = -1$, $M(100) = 1$ and $M(1000) = 2$.

**Non-examples and common mistakes.**

- $\mu$ is not completely multiplicative: $\mu(4) = 0$ but $\mu(2)^2 = 1$.
- $\mu$ is not the Liouville function $\lambda(n) = (-1)^{\Omega(n)}$, which counts prime factors with multiplicity and is never 0: $\lambda(4) = 1$ but $\mu(4) = 0$. The two agree exactly on squarefree $n$.
- $\mu(n)$ is not $(-1)^{\omega(n)}$, where $\omega(n)$ counts the distinct primes: $(-1)^{\omega(4)} = -1$.

## Related definitions

- **Dirichlet inverse of 1.** In the language of [Dirichlet convolution](/dirichlet-convolution/), the divisor sum says $\mu * \mathbf{1} = \varepsilon$, where $\varepsilon(n) = [n = 1]$ is the identity. This is the [Möbius inversion formula](/mobius-inversion-formula/): $g = f * \mathbf{1}$ if and only if $f = g * \mu$.
- **Totient.** $\varphi = \mu * \mathrm{id}$, equivalent to the [divisor sum of the totient](/totient-divisor-sum/) $\varphi * \mathbf{1} = \mathrm{id}$.
- **Dirichlet series.** For real part of $s$ greater than 1, $\sum_{n \ge 1} \mu(n) n^{-s} = 1/\zeta(s)$, where $\zeta$ is the Riemann zeta function. At $s = 2$ this gives the density $1/\zeta(2) = 6/\pi^2$ of the squarefree integers and of the coprime pairs.
- **Mertens function and primes.** The statement $M(x) = o(x)$ is equivalent to the [prime number theorem](/prime-number-theorem/), and the Riemann hypothesis is equivalent to $M(x) = O(x^{1/2 + \epsilon})$ for every $\epsilon > 0$. Mertens conjectured $|M(x)| < x^{1/2}$ for $x > 1$; Odlyzko and te Riele disproved it in 1985 without finding an explicit counterexample.
- **Primitive roots.** For a prime $p$, the sum of the [primitive roots](/primitive-root/) modulo $p$ is congruent to $\mu(p - 1)$ modulo $p$.
- **Generalizations.** The Möbius function of a partially ordered set generalizes $\mu$; the divisibility order on the positive integers gives the classical $\mu$, and the subset order gives the signs $(-1)^{|S|}$ of inclusion-exclusion.

## References
