---
tag: AFETH4
kind: definition
slug: dirichlet-convolution
name: Dirichlet convolution
aliases:
- Dirichlet product
area: number-theory/divisibility-and-gcd
level: advanced
summary: The product (f * g)(n) = sum of f(d) g(n/d) over divisors d of n.
prereqs: [divisor, multiplicative-function]
see_also: [mobius-inversion-formula, mobius-function, divisor-function, euler-totient, dirichlet-hyperbola-method, multiplicative-functions-up-to-n, linear-sieve, totient-divisor-sum]
sources:
  - book: isbn:9780387901633
    title: Tom M. Apostol, Introduction to Analytic Number Theory
    locator: Chapter 2, Arithmetical functions and Dirichlet multiplication (the Dirichlet product, Dirichlet inverses, the Möbius inversion formula, multiplicative functions); Chapter 11 (Dirichlet series and their products)
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Chapter 16 (arithmetical functions and the Möbius formula) and Chapter 17 (generating functions of arithmetical functions, Dirichlet series)
---

Dirichlet convolution is the product of two arithmetic functions $f, g$ defined on the positive integers by $(f * g)(n) = \sum_{d \mid n} f(d) \, g(n/d)$. It turns the set of arithmetic functions into a commutative ring, in which the Möbius function is the inverse of the constant function $1$; this one fact is the [Möbius inversion formula](/mobius-inversion-formula/). Many classical identities are convolutions: the number of divisors is $1 * 1$, the sum of divisors is $\mathrm{id} * 1$, and Gauss's identity $\sum_{d \mid n} \varphi(d) = n$ says $\varphi * 1 = \mathrm{id}$. Under the map to Dirichlet series $\sum f(n) n^{-s}$, convolution becomes ordinary multiplication, which is the origin of the name.

## Definition

An **arithmetic function** is a function $f : \mathbb{Z}_{\ge 1} \to \mathbb{C}$ (or into any commutative ring). The **Dirichlet convolution** of $f$ and $g$ is the arithmetic function

$$(f * g)(n) = \sum_{d \mid n} f(d) \, g\!\left(\frac{n}{d}\right) = \sum_{ab = n} f(a) \, g(b),$$

where the first sum runs over the positive divisors $d$ of $n$ and the second over ordered pairs of positive integers with product $n$.

**Notation.** $\mathbf{1}(n) = 1$ for all $n$; $\mathrm{id}(n) = n$ and $\mathrm{id}_k(n) = n^k$; $\varepsilon(n) = 1$ if $n = 1$ and $0$ otherwise; $\mu$ is the [Möbius function](/mobius-function/), $\varphi$ the [Euler totient](/euler-totient/), $d$ and $\sigma_k$ the [divisor functions](/divisor-function/).

**Algebraic properties.** For all arithmetic functions $f, g, h$:

1. *Commutative*: $f * g = g * f$, since the pairs $(a, b)$ with $ab = n$ are symmetric.
2. *Associative*: $((f * g) * h)(n) = \sum_{abc = n} f(a) g(b) h(c) = (f * (g * h))(n)$.
3. *Distributive* over pointwise addition: $f * (g + h) = f * g + f * h$.
4. *Identity*: $\varepsilon * f = f$, because only $d = 1$ contributes.
5. *Inverses*: $f$ has an inverse $f^{-1}$ with $f * f^{-1} = \varepsilon$ if and only if $f(1)$ is invertible ($f(1) \ne 0$ over $\mathbb{C}$). It is given by $f^{-1}(1) = 1/f(1)$ and, for $n > 1$,
$$f^{-1}(n) = -\frac{1}{f(1)} \sum_{d \mid n, \; d < n} f\!\left(\frac{n}{d}\right) f^{-1}(d).$$
*Proof.* The equation $(f * f^{-1})(n) = \varepsilon(n)$ reads $f(1) f^{-1}(1) = 1$ for $n = 1$, and for $n > 1$ it reads $f(1) f^{-1}(n) + \sum_{d \mid n, d < n} f(n/d) f^{-1}(d) = 0$. These determine $f^{-1}(n)$ from the values at proper divisors, by induction on $n$, exactly when $f(1)$ is invertible. $\square$

So the arithmetic functions form a commutative ring with unit $\varepsilon$, and it has no zero divisors: if $f * g = 0$, take the smallest $m$ with $f(m) \ne 0$ and $n$ with $g(n) \ne 0$; then $(f * g)(mn) = f(m) g(n) \ne 0$.

**Multiplicative functions.** If $f$ and $g$ are [multiplicative](/multiplicative-function/), so is $f * g$: for coprime $m, n$, each divisor of $mn$ is uniquely $d_1 d_2$ with $d_1 \mid m$, $d_2 \mid n$, so the sum factors. The inverse of a multiplicative function is multiplicative. So the multiplicative functions form a group under $*$, and $f * g$ is determined by its values at prime powers:

$$(f * g)(p^e) = \sum_{i = 0}^{e} f(p^i) \, g(p^{e - i}).$$

**Dirichlet series.** If $F(s) = \sum_{n \ge 1} f(n) n^{-s}$ and $G(s) = \sum g(n) n^{-s}$ converge absolutely, then $F(s) G(s) = \sum (f * g)(n) n^{-s}$, because $a^{-s} b^{-s} = (ab)^{-s}$ and collecting terms with $ab = n$ gives the convolution. With $\zeta(s) = \sum n^{-s}$, the series of $\mathbf{1}$, this gives $\sum d(n) n^{-s} = \zeta(s)^2$ and $\sum \mu(n) n^{-s} = 1/\zeta(s)$.

**Computing.** All values of $f * g$ up to $N$ cost $\sum_{a \le N} \lfloor N/a \rfloor = O(N \log N)$ multiplications, by iterating over $a$ and over the multiples $ab \le N$ ([harmonic series](/harmonic-series/)). When $f * g$ is multiplicative, a [linear sieve](/linear-sieve/) gives all values in $O(N)$ from the prime power formula; see [multiplicative functions up to n](/multiplicative-functions-up-to-n/). The partial sums $\sum_{n \le x} (f * g)(n)$ can often be found much faster with the [Dirichlet hyperbola method](/dirichlet-hyperbola-method/).

## Examples and non-examples

| identity | in words | value at $n = 12$ |
|---|---|---|
| $\mathbf{1} * \mathbf{1} = d$ | each divisor counts $1$ | $6$ |
| $\mathrm{id} * \mathbf{1} = \sigma$ | sum of divisors | $28$ |
| $\mathrm{id}_k * \mathbf{1} = \sigma_k$ | sum of $k$-th powers of divisors | $\sigma_2(12) = 210$ |
| $\mu * \mathbf{1} = \varepsilon$ | $\sum_{d \mid n} \mu(d) = 0$ for $n > 1$ | $0$ |
| $\varphi * \mathbf{1} = \mathrm{id}$ | Gauss: $\sum_{d \mid n} \varphi(d) = n$ | $12$ |
| $\mu * \mathrm{id} = \varphi$ | $\varphi(n) = \sum_{d \mid n} \mu(d) \, n/d$ | $4$ |
| $\lambda * \mathbf{1} = $ indicator of squares | $\lambda$ is Liouville's function | $0$ |
| $\Lambda * \mathbf{1} = \log$ | $\Lambda$ is von Mangoldt's function | $\log 12$ |

**Gauss's identity at $n = 12$.** The divisors are $1, 2, 3, 4, 6, 12$, and $\varphi(1) + \varphi(2) + \varphi(3) + \varphi(4) + \varphi(6) + \varphi(12) = 1 + 1 + 2 + 2 + 2 + 4 = 12$. The fractions $h/12$ for $h = 1, \ldots, 12$, reduced, have denominators $d \mid 12$, and exactly $\varphi(d)$ of them have denominator $d$. See [totient divisor sum](/totient-divisor-sum/).

**Möbius inversion.** From $\mu * \mathbf{1} = \varepsilon$: if $g = f * \mathbf{1}$, then $f = g * \mu$. For example $\sigma * \mu = \mathrm{id}$ and $d * \mu = \mathbf{1}$. This is the [Möbius inversion formula](/mobius-inversion-formula/), and $\mu = \mathbf{1}^{-1}$ by the inverse formula above.

**An inverse.** The inverse of $d = \mathbf{1} * \mathbf{1}$ is $\mu * \mu$, with values $1, -2, -2, 1, -2, 4, -2, 0, 1, 4, -2, -2$ for $n = 1, \ldots, 12$. At a prime power, $(\mu * \mu)(p) = -2$, $(\mu * \mu)(p^2) = 1$ and $(\mu * \mu)(p^e) = 0$ for $e \ge 3$.

**Non-example: the pointwise product.** $(fg)(n) = f(n) g(n)$ is a different product. For instance $\mathbf{1} \cdot \mathbf{1} = \mathbf{1}$, but $\mathbf{1} * \mathbf{1} = d$.

**Non-example: the additive convolution.** $\sum_{a + b = n} f(a) g(b)$ is the convolution of ordinary power series and of sequences; it matches the product of generating functions $\sum f(n) x^n$, not of Dirichlet series.

**Non-example: no inverse.** $\mathrm{id} - \varepsilon$, which is $0$ at $n = 1$ and $n$ elsewhere, has no Dirichlet inverse, because its value at $1$ is $0$.

## Related definitions

- **[Möbius function](/mobius-function/) and [Möbius inversion](/mobius-inversion-formula/).** $\mu$ is the Dirichlet inverse of $\mathbf{1}$, and inversion is convolution with $\mu$.
- **[Multiplicative function](/multiplicative-function/).** The functions closed under $*$ whose values are fixed by prime powers; completely multiplicative $f$ have inverse $\mu f$.
- **Bell series.** For multiplicative $f$ and a prime $p$, $f_p(x) = \sum_{e \ge 0} f(p^e) x^e$. Then $(f * g)_p = f_p \, g_p$, so convolution of multiplicative functions becomes multiplication of power series, one prime at a time.
- **Unitary convolution.** $\sum_{d \mid n, \gcd(d, n/d) = 1} f(d) g(n/d)$, a variant over unitary divisors, with its own Möbius function.
- **Divisor sums.** $f * \mathbf{1}$ is the summatory function over divisors, $\sum_{d \mid n} f(d)$. Its partial sums $\sum_{n \le x} (f * \mathbf{1})(n) = \sum_{d \le x} f(d) \lfloor x/d \rfloor$ lead to the [divisor summatory function](/divisor-summatory-function/) for $f = \mathbf{1}$.

## References
