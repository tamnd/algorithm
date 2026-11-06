---
tag: 5PCVSY
kind: definition
slug: divisor-function
name: Divisor function
aliases:
- sigma function
- tau function
- sum-of-divisors function
area: number-theory/divisibility-and-gcd
level: core
summary: Sigma_k(n) sums the k-th powers of divisors of n; tau(n) counts them.
prereqs: [divisor, fundamental-theorem-of-arithmetic, multiplicative-function]
see_also: [divisor-summatory-function, enumerating-divisors, dirichlet-convolution, divisor-count-sieve, divisor-function-up-to-n, dirichlets-divisor-problem, euler-totient, mobius-inversion-formula]
sources:
  - book: isbn:9780387901633
    title: Tom M. Apostol, Introduction to Analytic Number Theory
    locator: Chapter 2, Section 2.13, The divisor functions sigma_alpha(n); Chapter 3, the average order of d(n) and of sigma_alpha(n)
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Chapter 16 (the functions d(n) and sigma(n), perfect numbers) and Chapter 18 (the order of magnitude of d(n) and sigma(n))
  - paper: "Guy Robin, Grandes valeurs de la fonction somme des diviseurs et hypothese de Riemann, Journal de Mathematiques Pures et Appliquees 63, 1984"
    locator: pages 187 to 213
---

The divisor function $\sigma_k(n)$ is the sum of the $k$-th powers of the positive [divisors](/divisor/) of $n$. Two cases have their own names: $\sigma_0(n) = d(n) = \tau(n)$ counts the divisors, and $\sigma_1(n) = \sigma(n)$ adds them up. Both are [multiplicative functions](/multiplicative-function/), so they are computed from the prime factorization by a product of simple factors, such as $d(n) = \prod (e_i + 1)$. They grow irregularly: $d(n) = 2$ for each prime, yet $d(n)$ exceeds every power of $\log n$ infinitely often, while on average $d(n)$ is about $\ln n$. The sum $\sigma(n)$ defines perfect, abundant and deficient numbers, and its largest values are tied to the Riemann hypothesis.

## Definition

For an integer $n \ge 1$ and a real (or complex) number $k$, the **divisor function** is

$$\sigma_k(n) = \sum_{d \mid n, \; d \ge 1} d^k.$$

The **number of divisors** is $d(n) = \tau(n) = \sigma_0(n)$, and the **sum of divisors** is $\sigma(n) = \sigma_1(n)$. The functions are defined on positive integers only; $0$ has infinitely many divisors, and $d(-n)$, when it is used, means $d(|n|)$. The *aliquot sum* $s(n) = \sigma(n) - n$ adds the proper divisors.

**Formula from the factorization.** If $n = p_1^{e_1} p_2^{e_2} \cdots p_r^{e_r}$ with distinct primes $p_i$, then

$$d(n) = \prod_{i=1}^{r} (e_i + 1), \qquad \sigma(n) = \prod_{i=1}^{r} \frac{p_i^{e_i + 1} - 1}{p_i - 1}, \qquad \sigma_k(n) = \prod_{i=1}^{r} \left(1 + p_i^k + p_i^{2k} + \cdots + p_i^{e_i k}\right).$$

*Proof.* By the [fundamental theorem of arithmetic](/fundamental-theorem-of-arithmetic/), the positive divisors of $n$ are exactly the numbers $p_1^{f_1} \cdots p_r^{f_r}$ with $0 \le f_i \le e_i$, each written once ([divisor](/divisor/)). So

$$\sigma_k(n) = \sum_{f_1 = 0}^{e_1} \cdots \sum_{f_r = 0}^{e_r} p_1^{f_1 k} \cdots p_r^{f_r k} = \prod_{i=1}^{r} \sum_{f = 0}^{e_i} p_i^{f k},$$

by expanding the product. For $k = 0$ each inner sum is $e_i + 1$, and for $k = 1$ it is a geometric sum. $\square$

**Multiplicativity.** If $\gcd(m, n) = 1$, then $\sigma_k(mn) = \sigma_k(m) \sigma_k(n)$, because $m$ and $n$ share no prime, so the product formula for $mn$ splits into the factors for $m$ and for $n$. The function is not *completely* multiplicative: $d(4) = 3$ but $d(2)^2 = 4$.

**As a Dirichlet convolution.** $\sigma_k = \mathrm{id}_k * \mathbf{1}$, where $\mathrm{id}_k(n) = n^k$ and $\mathbf{1}(n) = 1$, and $d = \mathbf{1} * \mathbf{1}$ ([Dirichlet convolution](/dirichlet-convolution/)). In terms of Dirichlet series, $\sum_{n \ge 1} \sigma_k(n) n^{-s} = \zeta(s) \zeta(s - k)$. By [Möbius inversion](/mobius-inversion-formula/), $n^k = \sum_{d \mid n} \mu(n/d) \sigma_k(d)$.

**Elementary properties.** For $n \ge 1$:

- $d(n) \le 2\sqrt n$, because the divisors pair up as $d$ and $n/d$ with one of them at most $\sqrt n$; and $d(n)$ is odd if and only if $n$ is a perfect square, since only then is a divisor paired with itself.
- $\sigma(n)$ is odd if and only if $n$ is a square or twice a square. Each odd prime power $p^e$ contributes the factor $1 + p + \cdots + p^e$, a sum of $e + 1$ odd terms, which is odd exactly when $e$ is even; the factor for $2^e$ is always odd.
- $\sigma(n) \ge n + 1$ for $n \ge 2$, with equality exactly when $n$ is prime; and $d(n) = 2$ exactly when $n$ is prime.
- $\sigma_{-k}(n) = \sigma_k(n) / n^k$, by the pairing $d \leftrightarrow n/d$. The ratio $\sigma(n)/n = \sigma_{-1}(n)$ is the *abundancy* of $n$.

**Size.**

- *Average order.* $\sum_{n \le x} d(n) = x \ln x + (2\gamma - 1) x + O(\sqrt x)$, where $\gamma \approx 0.5772$ is Euler's constant, so $d(n)$ is $\ln n$ on average. This is the [divisor summatory function](/divisor-summatory-function/), and the error term is [Dirichlet's divisor problem](/dirichlets-divisor-problem/). Also $\sum_{n \le x} \sigma(n) = \frac{\pi^2}{12} x^2 + O(x \log x)$.
- *Maximal order of $d$.* For each $\varepsilon > 0$, $d(n) = O(n^\varepsilon)$; more precisely $\limsup \frac{\ln d(n) \cdot \ln \ln n}{\ln n} = \ln 2$ (Wigert). So $d(n)$ is smaller than every power of $n$, but larger than every power of $\ln n$ infinitely often.
- *Maximal order of $\sigma$.* $\limsup \frac{\sigma(n)}{n \ln \ln n} = e^\gamma$ (Gronwall). Robin proved that the inequality $\sigma(n) < e^\gamma n \ln \ln n$ holds for every $n > 5040$ if and only if the Riemann hypothesis is true. For $3 \le n \le 5040$ it fails 26 times, the last time at $n = 5040$.

## Examples and non-examples

| $n$ | factorization | divisors | $d(n)$ | $\sigma(n)$ | $\sigma(n) - 2n$ |
|---|---|---|---|---|---|
| 1 | $1$ | 1 | 1 | 1 | $-1$ |
| 7 | $7$ | 1, 7 | 2 | 8 | $-6$ |
| 12 | $2^2 \cdot 3$ | 1, 2, 3, 4, 6, 12 | 6 | 28 | $4$ |
| 28 | $2^2 \cdot 7$ | 1, 2, 4, 7, 14, 28 | 6 | 56 | $0$ |
| 36 | $2^2 \cdot 3^2$ | 1, 2, 3, 4, 6, 9, 12, 18, 36 | 9 | 91 | $19$ |
| 60 | $2^2 \cdot 3 \cdot 5$ | twelve divisors | 12 | 168 | $48$ |

**By the formula.** $60 = 2^2 \cdot 3 \cdot 5$ gives $d(60) = 3 \cdot 2 \cdot 2 = 12$ and $\sigma(60) = 7 \cdot 4 \cdot 6 = 168$. For $\sigma_2$: $\sigma_2(12) = (1 + 4 + 16)(1 + 9) = 210$, and indeed $1 + 4 + 9 + 16 + 36 + 144 = 210$.

**Perfect, abundant and deficient numbers.** $n$ is *perfect* if $\sigma(n) = 2n$, *abundant* if $\sigma(n) > 2n$ and *deficient* if $\sigma(n) < 2n$. The perfect numbers below $10^5$ are $6$, $28$, $496$ and $8128$. By the Euclid-Euler theorem, an even number is perfect if and only if it is $2^{p-1}(2^p - 1)$ with $2^p - 1$ prime; whether an odd perfect number exists is an open problem. Primes and prime powers are deficient; $12$ is the smallest abundant number.

**Many divisors.** The number below $1000$ with the most divisors is $840 = 2^3 \cdot 3 \cdot 5 \cdot 7$, with $d(840) = 4 \cdot 2 \cdot 2 \cdot 2 = 32$. Below $10^5$ the record is $d(83160) = 128$, and $720720 = 2^4 \cdot 3^2 \cdot 5 \cdot 7 \cdot 11 \cdot 13$ has $5 \cdot 3 \cdot 2^4 = 240$ divisors. The numbers with more divisors than any smaller number are the *highly composite numbers*.

**Non-example: not completely multiplicative.** $\sigma(4) = 7$, but $\sigma(2) \sigma(2) = 9$; the rule $\sigma(mn) = \sigma(m)\sigma(n)$ needs $\gcd(m, n) = 1$.

**Non-example: zero.** $\sigma_k(0)$ and $d(0)$ are not defined, since every positive integer divides $0$.

## Related definitions

- **[Divisor](/divisor/).** The set of positive divisors $D(n)$, whose size is $d(n)$. Listing them is the [enumerating divisors](/enumerating-divisors/) problem.
- **[Multiplicative function](/multiplicative-function/).** A function with $f(mn) = f(m) f(n)$ for coprime $m, n$; $d$, $\sigma_k$, the [Euler totient](/euler-totient/) $\varphi$ and the [Möbius function](/mobius-function/) are the basic examples.
- **[Divisor summatory function](/divisor-summatory-function/).** $D(x) = \sum_{n \le x} d(n)$, the number of lattice points under the hyperbola $uv = x$, computed in $O(\sqrt x)$ by the [Dirichlet hyperbola method](/dirichlet-hyperbola-method/).
- **Tables for all $n \le N$.** The values $d(n)$ or $\sigma(n)$ for all $n$ up to $N$ come from a [divisor count sieve](/divisor-count-sieve/), from the [divisor function up to n](/divisor-function-up-to-n/), or from a [linear sieve](/linear-sieve/) for multiplicative functions, in $O(N \log N)$ or $O(N)$ time.
- **Unitary and other variants.** $\sigma^*(n)$ sums the unitary divisors $d$ with $\gcd(d, n/d) = 1$, and $d_k(n)$ counts the ways to write $n$ as an ordered product of $k$ factors, so $d_2 = d$.

## References
