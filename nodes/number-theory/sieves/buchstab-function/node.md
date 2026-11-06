---
tag: 4M2FJG
kind: definition
slug: buchstab-function
name: Buchstab function
aliases:
- Buchstab's function
- Buchstab omega function
area: number-theory/sieves
level: research
summary: omega(u) = 1/u on [1, 2] and (u omega(u))' = omega(u - 1) after. The count of n <= x with all prime factors above x^(1/u) is about omega(u) x / log(x^(1/u)).
prereqs: [legendre-phi-function, prime-number-theorem, sieve-theory]
see_also: [dickman-function, smooth-number, legendre-phi-function, sieve-theory, selberg-sieve, brun-sieve, meissel-lehmer-algorithm, prime-counting-function]
sources:
  - paper: "A. A. Buchstab, Asymptotic estimates of a general number-theoretic function (in Russian, with a German summary), Matematicheskii Sbornik 2(44), 1937, pages 1239 to 1246"
    locator: the asymptotic formula for the number of integers free of small prime factors, with the function omega
  - paper: "N. G. de Bruijn, On the number of uncancelled elements in the sieve of Eratosthenes, Proceedings of the Koninklijke Nederlandse Akademie van Wetenschappen 53, 1950, pages 803 to 812"
    locator: uniform estimates for the sieve count and properties of omega
  - book: isbn:9780821898543
    title: Gérald Tenenbaum, Introduction to Analytic and Probabilistic Number Theory, third edition, American Mathematical Society, Graduate Studies in Mathematics 163, 2015
    locator: Part III, Chapter 6, Integers free of small prime factors (pp. 557 to 590)
  - url: https://arxiv.org/abs/2607.21883
    title: Andreas Weingartner, Explicit bounds for Buchstab's function, arXiv preprint, 2026
    locator: the introduction, which recalls Buchstab's theorem and the definition of omega
---

The Buchstab function $\omega(u)$ describes how many integers have no small prime factors. It is the continuous function on $u \ge 1$ given by $\omega(u) = 1/u$ for $1 \le u \le 2$ and by the delay differential equation $(u\,\omega(u))' = \omega(u - 1)$ for $u > 2$. Buchstab proved in 1937 that the number of $n \le x$ whose prime factors all exceed $y = x^{1/u}$ is asymptotic to $\omega(u)\, x / \log y$ for each fixed $u > 1$. As $u$ grows, $\omega(u)$ tends to $e^{-\gamma} = 0.5614594\ldots$ very fast, in agreement with Mertens' product $\prod_{p \le y}(1 - 1/p) \sim e^{-\gamma}/\log y$.

## Definition

**Rough numbers.** For $x \ge 1$ and $y \ge 1$ let

$$\Phi(x, y) = \#\{\, 1 \le n \le x : p \mid n \Rightarrow p > y \,\},$$

the number of $y$-rough integers up to $x$ (the integer 1 counts). If $p_a \le y < p_{a+1}$, then $\Phi(x, y)$ equals [Legendre's](/legendre-phi-function/) $\varphi(x, a)$.

**The function.** The Buchstab function is the unique function $\omega : [1, \infty) \to \mathbb{R}$ that is continuous on $(1, \infty)$ and satisfies

$$\omega(u) = \frac{1}{u} \quad (1 \le u \le 2), \qquad \frac{d}{du}\big(u\, \omega(u)\big) = \omega(u - 1) \quad (u > 2),$$

the derivative being one sided at the integers. Equivalently, for $u \ge 2$,

$$u\, \omega(u) = 1 + \int_1^{u - 1} \omega(t)\, dt.$$

The integral form determines $\omega$ on $[k, k+1]$ from its values on $[1, k]$, one unit interval at a time, which is also how it is computed.

**Buchstab's theorem.** For every fixed $u > 1$,

$$\Phi\big(x, x^{1/u}\big) \sim \omega(u)\, \frac{x}{\log x^{1/u}} = u\, \omega(u)\, \frac{x}{\log x} \qquad (x \to \infty).$$

For $1 < u \le 2$ this is the [prime number theorem](/prime-number-theorem/): the $y$-rough numbers up to $x \le y^2$ are 1 and the primes in $(y, x]$, so $\Phi(x, y) = 1 + \pi(x) - \pi(y)$. For larger $u$ the equation comes from Buchstab's identity: sorting the $n$ counted by $\Phi(x, y)$ by their least prime factor $p$ gives

$$\Phi(x, y) = \Phi(x, z) + \sum_{y < p \le z} \Phi\Big(\frac{x}{p}, p^{-}\Big) \qquad (y < z),$$

where $\Phi(x/p, p^{-})$ counts $m \le x/p$ whose prime factors are all at least $p$. Inserting the asymptotic for the smaller ranges and replacing the sum over primes by an integral with the prime number theorem gives the integral equation for $\omega$.

## Examples and non-examples

- **The first pieces in closed form.** On $[2, 3]$, $u\,\omega(u) = 1 + \int_1^{u-1} dt/t = 1 + \log(u - 1)$, so $\omega(u) = (1 + \log(u - 1))/u$ and $\omega(3) = (1 + \log 2)/3 = 0.5643824$. On $[3, 4]$ the formula already needs the dilogarithm, and beyond that one computes numerically.
- **Values.** Solving the integral equation on a grid of step $10^{-4}$ with the trapezoidal rule gives

  | $u$ | 1.5 | 2 | 2.5 | 3 | 3.5 | 4 | 5 | 6 |
  |---|---|---|---|---|---|---|---|---|
  | $\omega(u)$ | 0.6666667 | 0.5 | 0.5621860 | 0.5643824 | 0.5608289 | 0.5614582 | 0.5614545 | 0.5614597 |

  and the grid values on $[2, 3]$ agree with the closed form to about $10^{-10}$.
- **The maximum.** On $[2, 3]$, $\omega'(u) = 0$ exactly when $(u - 1)\log(u - 1) = 1$, that is $u = 1 + 1/W(1) = 2.7632228$, where $W$ is the Lambert function. The maximum value is $W(1) = 0.5671433$, the omega constant. This is the largest value of $\omega$ on $[2, \infty)$.
- **Fast oscillating convergence.** The largest deviation $|\omega(u) - e^{-\gamma}|$ on $[k, k+1]$ is about $6.1 \cdot 10^{-2}$, $2.9 \cdot 10^{-3}$, $6.2 \cdot 10^{-5}$, $5.0 \cdot 10^{-6}$, $2.0 \cdot 10^{-7}$, $2.7 \cdot 10^{-9}$ for $k = 2, \ldots, 7$, and the sign of $\omega(u) - e^{-\gamma}$ keeps changing. The decay is faster than exponential.
- **Counts at $x = 10^7$.** With $y = x^{1/u}$, the normalized counts $\Phi(x, y) \log y / x$ are

  | $u$ | $y$ | $\Phi(10^7, y)$ | $\Phi \log y / x$ | $\omega(u)$ |
  |---|---|---|---|---|
  | 1.5 | 46415.89 | 659783 | 0.70896 | 0.66667 |
  | 2.5 | 630.96 | 851658 | 0.54908 | 0.56219 |
  | 3 | 215.44 | 1039400 | 0.55844 | 0.56438 |
  | 4 | 56.23 | 1360693 | 0.54829 | 0.56146 |
  | 5 | 25.12 | 1635877 | 0.52734 | 0.56146 |

  The asymptotic is approached slowly. At $u = 1.5$ the excess is that of $\pi(x)\log x / x = 1.063$ at $x = 10^7$, and at $u = 5$ the sifting bound $y = 25$ is too small for the limit to show.
- **Non-example: fixed $y$.** If $y$ stays fixed while $x \to \infty$, then $\Phi(x, y) \sim x \prod_{p \le y}(1 - 1/p)$, and the right normalization involves this product rather than $\omega$. For example $\Phi(x, 2)$ counts the odd numbers, which is $\lceil x/2 \rceil$. Buchstab's theorem needs $y \to \infty$ with $u$ fixed. The two regimes match as $u \to \infty$ because $\log y \prod_{p \le y}(1 - 1/p) \to e^{-\gamma}$, which is Mertens' theorem, and $\omega(u) \to e^{-\gamma}$.
- **Non-example: smoothness at 2.** The function $\omega$ is continuous but not differentiable at $u = 2$. From the left, $\omega'(2) = -1/4$. From the right, $(u\omega)' = \omega(1) = 1$ gives $\omega'(2^{+}) = 1/4$. At each later integer the derivative is continuous, but a higher derivative is not.
- **Non-example: the Dickman function.** The [Dickman function](/dickman-function/) $\rho$ satisfies a similar delay equation, $u\rho'(u) = -\rho(u - 1)$ with $\rho = 1$ on $[0, 1]$, but it counts the opposite set: integers whose prime factors are all at most $x^{1/u}$. It tends to 0 faster than any exponential, while $\omega$ tends to a positive constant.

## Related definitions

- **Legendre's phi function.** $\varphi(x, a) = \Phi(x, p_a)$ is the exact count. The [Meissel-Lehmer algorithm](/meissel-lehmer-algorithm/) evaluates it, and Buchstab's identity is its recursion $\varphi(x, a) = \varphi(x, a - 1) - \varphi(x/p_a, a - 1)$ written in terms of least prime factors.
- **Smooth numbers and the Dickman function.** The [smooth numbers](/smooth-number/) are the complement viewpoint. Here $\Psi(x, y)$ counts $n \le x$ whose prime factors are at most $y$, and $\Psi(x, x^{1/u}) \sim \rho(u) x$.
- **Sieve functions.** In [sieve theory](/sieve-theory/) the sifted count of a set of integers is compared with $X\prod_{p<z}(1 - g(p))$. For the integers themselves the exact asymptotic ratio is $e^{\gamma}\omega(u)$, with $z = x^{1/u}$. The upper and lower bound functions $F$ and $f$ of the linear sieve satisfy delay equations of the same Buchstab type.
- **The prime counting function.** The [prime counting function](/prime-counting-function/) is the case $1 < u \le 2$ of $\Phi$, up to the term $1 + \pi(y)$.

## References
