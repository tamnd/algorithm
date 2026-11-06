---
tag: YJH8R4
kind: definition
slug: multiplicative-function
name: Multiplicative function
aliases:
- multiplicative arithmetic function
area: number-theory/divisibility-and-gcd
level: core
summary: An arithmetic function f with f(mn) = f(m)f(n) whenever gcd(m, n) = 1.
prereqs: [coprime-integers, fundamental-theorem-of-arithmetic, divisor]
see_also: [dirichlet-convolution, mobius-function, euler-totient, divisor-function, mobius-inversion-formula, multiplicative-functions-up-to-n, linear-sieve, totient-divisor-sum]
sources:
  - book: isbn:9780387901633
    title: Tom M. Apostol, Introduction to Analytic Number Theory
    locator: Chapter 2, Section 2.9, Multiplicative functions, and Section 2.10, Multiplicative functions and Dirichlet multiplication
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Section 4.9, Phi and Mu (multiplicative functions, their values at prime powers, and the divisor sums of multiplicative functions)
  - url: "https://en.wikipedia.org/wiki/Multiplicative_function"
    locator: lead and section Examples (the definition with f(1) = 1, completely multiplicative functions, and the list of examples)
---

A multiplicative function is an arithmetic function $f$, defined on the positive integers, with $f(1) = 1$ and $f(mn) = f(m) f(n)$ whenever $m$ and $n$ are [coprime](/coprime-integers/). By the [fundamental theorem of arithmetic](/fundamental-theorem-of-arithmetic/), such a function is fixed by its values at prime powers: $f(n) = \prod f(p^{e})$ over the prime powers $p^e$ that exactly divide $n$. [Euler's totient](/euler-totient/), the [Möbius function](/mobius-function/) and the [divisor functions](/divisor-function/) are multiplicative, and [Dirichlet convolution](/dirichlet-convolution/) of multiplicative functions is again multiplicative. This is why their values have product formulas, and why a [linear sieve](/linear-sieve/) can compute all of them up to $N$ in $O(N)$ operations.

## Definition

An **arithmetic function** is a function $f$ from the positive integers to the complex numbers.

**Definition.** An arithmetic function $f$ is **multiplicative** if $f(1) = 1$ and

$$f(mn) = f(m)\, f(n) \quad \text{for all positive integers } m, n \text{ with } \gcd(m, n) = 1.$$

It is **completely multiplicative** (or totally multiplicative) if $f(1) = 1$ and $f(mn) = f(m) f(n)$ for all positive $m$ and $n$.

The condition $f(1) = 1$ excludes only the zero function: if $f(mn) = f(m) f(n)$ for coprime pairs and $f(n) \ne 0$ for some $n$, then $f(n) = f(n \cdot 1) = f(n) f(1)$ gives $f(1) = 1$. Apostol states the definition as "$f$ is not identically zero" with the product rule; the two forms are equivalent.

**Values at prime powers.** If $n = p_1^{e_1} \cdots p_r^{e_r}$ with distinct primes $p_i$, then the prime powers $p_i^{e_i}$ are pairwise coprime, so by induction on $r$

$$f(n) = f(p_1^{e_1}) \cdots f(p_r^{e_r}).$$

Conversely, any choice of values $f(p^e)$ for the prime powers, extended by this formula and $f(1) = 1$, gives a multiplicative function, because the factorization is unique. A completely multiplicative function is fixed by its values at primes alone: $f(p^e) = f(p)^e$.

**Divisor sums and convolution.** If $f$ and $g$ are multiplicative, then so is their Dirichlet convolution $(f * g)(n) = \sum_{d \mid n} f(d)\, g(n/d)$. The reason: for coprime $m$ and $n$, the map $(d_1, d_2) \mapsto d_1 d_2$ is a bijection from pairs of divisors $d_1 \mid m$, $d_2 \mid n$ onto the divisors of $mn$, and $\gcd(d_1, d_2) = \gcd(m/d_1, n/d_2) = 1$. Hence

$$(f * g)(mn) = \sum_{d_1 \mid m} \sum_{d_2 \mid n} f(d_1) f(d_2)\, g(m/d_1)\, g(n/d_2) = (f * g)(m)\, (f * g)(n).$$

In particular, $F(n) = \sum_{d \mid n} f(d)$ is multiplicative when $f$ is, with $F(p^e) = 1 + f(p) + \cdots + f(p^e)$.

## Examples and non-examples

**Examples.** The table gives values at a few arguments; each column satisfies $f(72) = f(8) f(9)$ and $f(24) = f(8) f(3)$, since 8 is coprime to 9 and to 3.

| function | definition | value at $p^e$ | completely multiplicative? | $f(12)$ | $f(72)$ |
| --- | --- | --- | --- | --- | --- |
| $\varepsilon$ | 1 at $n = 1$, else 0 | 0 for $e \ge 1$ | yes | 0 | 0 |
| $\mathbf{1}$ | 1 | 1 | yes | 1 | 1 |
| $\mathrm{id}_k$ | $n^k$ | $p^{ek}$ | yes | $12^k$ | $72^k$ |
| $\lambda$ (Liouville) | $(-1)^{\Omega(n)}$, $\Omega$ = number of prime factors with multiplicity | $(-1)^e$ | yes | $-1$ | $-1$ |
| $\tau = \sigma_0$ | number of divisors | $e + 1$ | no | 6 | 12 |
| $\sigma = \sigma_1$ | sum of divisors | $(p^{e+1} - 1)/(p - 1)$ | no | 28 | 195 |
| $\varphi$ | [Euler's totient](/euler-totient/) | $p^{e-1}(p - 1)$ | no | 4 | 24 |
| $\mu$ | [Möbius function](/mobius-function/) | $-1$ if $e = 1$, 0 if $e \ge 2$ | no | 0 | 0 |
| $2^{\omega(n)}$ | $\omega$ = number of distinct prime factors | 2 | no | 4 | 4 |
| $n \mapsto \gcd(n, m)$ | for a fixed $m \ge 1$ | $p^{\min(e, v_p(m))}$ | no | for $m = 12$: 12 | for $m = 12$: 12 |
| $s(n)$ | number of $x \bmod n$ with $x^2 \equiv 1$ | see below | no | 4 | 8 |

For the last row, $s(2) = 1$, $s(4) = 2$, $s(2^e) = 4$ for $e \ge 3$, and $s(p^e) = 2$ for odd $p$; by the [Chinese remainder theorem](/chinese-remainder-theorem/) the solutions modulo coprime moduli combine, which is the multiplicative property. The modulo 12 solutions are $1, 5, 7, 11$.

The totient shows the difference between the two notions: $\varphi(4) = 2$ but $\varphi(2)^2 = 1$, so $\varphi$ is multiplicative but not completely multiplicative. The divisor sum identities $\varphi * \mathbf{1} = \mathrm{id}$ (the [divisor sum of the totient](/totient-divisor-sum/)), $\mu * \mathbf{1} = \varepsilon$, $\mathbf{1} * \mathbf{1} = \tau$ and $\mathrm{id} * \mathbf{1} = \sigma$ show multiplicativity of the right side from that of the left.

**Non-examples.**

- $f(n) = 2n$: $f(1) = 2 \ne 1$, and $f(mn) = 2mn \ne 4mn = f(m) f(n)$.
- $\omega(n)$, the number of distinct prime factors: it is **additive**, $\omega(mn) = \omega(m) + \omega(n)$ for coprime $m$ and $n$, so $2^{\omega(n)}$ is multiplicative but $\omega$ itself is not. Similarly $\log n$ is completely additive.
- The von Mangoldt function $\Lambda(n)$, equal to $\log p$ if $n = p^e$ with $e \ge 1$ and 0 otherwise: $\Lambda(1) = 0$, and $\Lambda(6) = 0 \ne \Lambda(2) \Lambda(3)$.
- $f(n) = n + 1$: $f(1) = 2$, and $f(6) = 7 \ne f(2) f(3) = 12$.
- The sum of two multiplicative functions is usually not multiplicative: $(\varphi + \mathbf{1})(1) = 2$. The pointwise product of two multiplicative functions is multiplicative, and so is the Dirichlet convolution.

## Related definitions

- **[Dirichlet convolution](/dirichlet-convolution/).** The multiplicative functions form a group under Dirichlet convolution, with identity $\varepsilon$. The Dirichlet inverse of a multiplicative function is multiplicative; for example, the inverse of $\mathbf{1}$ is $\mu$, which is the [Möbius inversion formula](/mobius-inversion-formula/). Apostol proves this in Section 2.10.
- **Completely multiplicative functions** have Dirichlet inverse $\mu f$; for example, the inverse of $\mathrm{id}_k$ is $\mu(n) n^k$.
- **Additive functions** satisfy $f(mn) = f(m) + f(n)$ for coprime $m$ and $n$; if $f$ is additive, $c^{f(n)}$ is multiplicative.
- **Computation.** Given $f(p^e)$ in $O(1)$ time, all values $f(1), \ldots, f(N)$ follow in $O(N)$ word operations with a [linear sieve](/linear-sieve/), which tracks the smallest prime factor and its exponent; see [multiplicative functions up to n](/multiplicative-functions-up-to-n/). A single value $f(n)$ needs the factorization of $n$, by [trial division](/trial-division/) or a [factorization](/integer-factorization/) method.
- **Summation.** Sums $\sum_{n \le N} f(n)$ of multiplicative functions use convolution identities, as in the [Dirichlet hyperbola method](/dirichlet-hyperbola-method/).

## References
