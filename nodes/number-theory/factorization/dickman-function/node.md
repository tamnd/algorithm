---
tag: 2JVP6F
kind: concept
slug: dickman-function
name: Dickman function
aliases:
- Dickman rho function
area: number-theory/factorization
level: research
summary: The function rho(u) with rho = 1 on [0, 1] and u rho'(u) = -rho(u - 1). About rho(u) x of the integers up to x are x^(1/u)-smooth, which sets the cost of sieve and group factoring methods.
prereqs: [smooth-number, prime-number-theorem]
see_also: [smooth-number, buchstab-function, quadratic-sieve, pollard-p-minus-1, elliptic-curve-factorization, relation-collection, subexponential-time, integer-factorization]
sources:
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition, Springer, 2005
    locator: Section 1.4.5, Smooth numbers, pages 48 to 49 (Theorem 1.4.9 of Dickman, rho(u) = 1 - ln u on [1, 2], and ln rho(u) ~ -u ln u as (1.43)); Section 7.4.1, pages 338 to 339 (the ECM parameter choice)
  - paper: "Karl Dickman, On the frequency of numbers containing prime factors of a certain relative magnitude, Arkiv för Matematik, Astronomi och Fysik 22A(10), 1930"
    locator: pages 1 to 14 (the limit density and the equation for rho)
  - paper: "Donald E. Knuth and Luis Trabb Pardo, Analysis of a simple factorization algorithm, Theoretical Computer Science 3(3), 1976"
    locator: pages 321 to 348 (the distribution of the largest prime factors, the function rho, and its numerical values)
  - paper: "Adolf Hildebrand and Gérald Tenenbaum, Integers without large prime factors, Journal de Théorie des Nombres de Bordeaux 5(2), 1993"
    locator: pages 411 to 484 (the Dickman function, its asymptotic expansion, and the range of validity of psi(x, y) ~ rho(u) x)
  - paper: "Andrew Granville, Smooth numbers: computational number theory and beyond, in Algorithmic Number Theory, MSRI Publications 44, Cambridge University Press, 2008"
    locator: pages 267 to 323 (sections 1 to 4, rho and its use in the analysis of factoring algorithms)
---

The Dickman function $\rho(u)$ gives the density of [smooth numbers](/smooth-number/): for each fixed $u > 0$, the number $\Psi(x, x^{1/u})$ of integers $n \le x$ with no prime factor above $x^{1/u}$ satisfies $\Psi(x, x^{1/u}) \sim \rho(u)\, x$ as $x \to \infty$. It is the continuous function with $\rho(u) = 1$ for $0 \le u \le 1$ and $u\rho'(u) = -\rho(u - 1)$ for $u > 1$, so $\rho(u) = 1 - \ln u$ on $[1, 2]$, and it has no closed form beyond that. It falls quickly, roughly like $u^{-u}$. The running time of every factoring method that waits for a smooth number, from [Pollard's $p - 1$](/pollard-p-minus-1/) and [ECM](/elliptic-curve-factorization/) to the [quadratic sieve](/quadratic-sieve/), is a trade between the cost of a trial and the chance $\rho(u)$ that it succeeds.

## In plain words

Pick a large number at random and look at its largest prime factor. Measure its size by the number of digits, as a fraction of the digits of the whole number. The Dickman function tells how likely it is that this fraction is at most one half, one third, one quarter, and so on.

All numbers pass the test "at most the whole". About 31 percent of numbers have every prime factor below their square root, about 5 percent below their cube root, and about half a percent below their fourth root. The chance falls very fast as the allowed part shrinks.

Fast factoring methods need numbers whose prime factors are all small, and they find them by trying many numbers. This function says how many they must try.

## The idea

**Definition.** $\rho : [0, \infty) \to \mathbb{R}$ is the unique continuous function with $\rho(u) = 1$ on $[0, 1]$ and, for $u > 1$,
$$u\rho'(u) = -\rho(u - 1), \qquad \text{equivalently} \qquad u\rho(u) = \int_{u-1}^{u} \rho(t)\, dt.$$
The integral form follows from the differential one: both sides equal $1$ at $u = 1$, and the derivative of the right side is $\rho(u) - \rho(u - 1) = \rho(u) + u\rho'(u)$, the derivative of the left side. On each interval $[k, k + 1]$ the equation gives $\rho$ from its values on $[k - 1, k]$, so $\rho$ exists and is unique.

**Dickman's theorem** (Crandall and Pomerance, Theorem 1.4.9). For each fixed $u > 0$, $\Psi(x, x^{1/u}) \sim \rho(u)\,x$ as $x \to \infty$. Equivalently, $\rho(u)$ is the limiting probability that the largest prime factor of a random integer up to $x$ is at most $x^{1/u}$.

**Why this equation.** A heuristic count shows where it comes from. Let $y = x^{1/u}$ and sum $\ln n = \sum_{p^k \mid n} \ln p$ over the $y$-smooth $n \le x$. The left side is about $\Psi(x, y)\ln x \approx \rho(u)\,x \ln x$, since most such $n$ are near $x$ in size. On the right, each prime $p \le y$ contributes $\ln p$ times the number of smooth $m \le x/p$, which is about $\rho(u - \ln p/\ln y)\,x/p$. By the [prime number theorem](/prime-number-theorem/), the sum over $p$ of $(\ln p)/p$ behaves like an integral with density $1$ in $s = \ln p$, so the right side is about $x\int_0^{\ln y} \rho(u - s/\ln y)\, ds = x \ln y \int_{u-1}^{u} \rho(t)\,dt$. Dividing by $x\ln y$ gives $u\rho(u) = \int_{u-1}^u \rho(t)\,dt$. The standard proof makes this count rigorous.

**On $[1, 2]$.** There $\rho(u - 1) = 1$, so $\rho'(u) = -1/u$ and $\rho(u) = 1 - \ln u$. The smooth number page derives the same value directly by counting the numbers with one prime factor above $\sqrt x$. On $[2, 3]$ the solution already involves the dilogarithm, and no closed form in elementary functions is known for $u > 2$.

**Basic properties.** These follow from the integral form.

- *Positive.* If $\rho > 0$ on $[0, u)$, then $u\rho(u) = \int_{u-1}^u \rho > 0$. By continuity $\rho > 0$ everywhere.
- *Decreasing.* $\rho'(u) = -\rho(u - 1)/u < 0$ for $u > 1$, so $\rho$ is strictly decreasing on $[1, \infty)$.
- *A simple upper bound.* Since $\rho$ is nonincreasing, $u\rho(u) = \int_{u-1}^u \rho \le \rho(u - 1)$, so $\rho(u) \le \rho(u - 1)/u$. Applying this $\lfloor u \rfloor$ times gives $\rho(u) \le 1/(u(u - 1)\cdots(u - \lfloor u \rfloor + 1)) \le 1/\lfloor u \rfloor!$.
- *Asymptotics.* $\ln \rho(u) \sim -u\ln u$ as $u \to \infty$, so $\rho(u) = u^{-u + o(u)}$ (Crandall and Pomerance, (1.43)). More precisely, $\rho(u) = \exp\big(-u(\ln u + \ln \ln u - 1 + o(1))\big)$, by de Bruijn; Hildebrand and Tenenbaum give the full expansion.

**Beyond fixed $u$.** Factoring needs $u$ that grows with $x$. Canfield, Erdős and Pomerance showed $\Psi(x, x^{1/u}) = x\,u^{-u + o(u)}$ uniformly for $u < (1 - \epsilon)\ln x/\ln \ln x$, the same rate as $\rho(u)$; see the [smooth number](/smooth-number/) page. The related function for numbers with no small prime factors is the [Buchstab function](/buchstab-function/).

**Computing $\rho$.** The integral form is stable: all terms are positive, so the relative error stays small even when $\rho(u)$ is tiny. On a grid with step $h$, the trapezoidal rule for $\int_{u-1}^u \rho$ gives each new value $\rho(u)$ from the $1/h$ values before it, with error $O(h^2)$. Steps $h = 1/1000$ and $h = 1/2000$ with one Richardson step give the values below to about ten digits. Subtracting the integral of $\rho(t - 1)/t$ from $\rho(u - h)$ instead loses all relative accuracy near $u = 10$, where $\rho$ is about $10^{-11}$.

## Examples

**Values.** Computed by the method above; $\rho(1.5)$ and $\rho(2)$ are $1 - \ln 1.5$ and $1 - \ln 2$ exactly.

| $u$ | $\rho(u)$ | $u^{-u}$ | $1/\lfloor u \rfloor!$ |
|---|---|---|---|
| 1.5 | 0.594535 | 0.544 | 1 |
| 2 | 0.306853 | 0.25 | 0.5 |
| 3 | 0.0486084 | 0.0370 | 0.167 |
| 4 | 0.00491093 | 0.00391 | 0.0417 |
| 5 | 0.000354725 | 0.00032 | 0.00833 |
| 6 | 1.96497 · 10^-5 | 2.14 · 10^-5 | 0.00139 |
| 8 | 3.23207 · 10^-8 | 5.96 · 10^-8 | 2.48 · 10^-5 |
| 10 | 2.77017 · 10^-11 | 10^-10 | 2.76 · 10^-7 |

For small $u$ the guess $u^{-u}$ is too small; from $u = 6$ on it is too large, and for large $u$ the ratio $u^{-u}/\rho(u)$ grows without bound, as the term $u \ln \ln u$ in the exponent shows.

**Actual counts.** For $x = 10^7$, counting the $n \le x$ by their largest prime factor gives:

| $u$ | $y = x^{1/u}$ | $\Psi(x, y)$ | $\Psi(x, y)/x$ | $\rho(u)$ |
|---|---|---|---|---|
| 2 | 3162.3 | 3,362,157 | 0.336 | 0.307 |
| 3 | 215.4 | 665,196 | 0.0665 | 0.0486 |
| 4 | 56.2 | 115,696 | 0.0116 | 0.00491 |
| 5 | 25.1 | 28,434 | 0.00284 | 0.000355 |

The limit is approached slowly, and for numbers of practical size the true density is larger than $\rho(u)$, more so for large $u$. This is why estimates with $\rho$ are pessimistic in practice.

**The largest prime factor.** The average of $\ln P(n)/\ln n$, with $P(n)$ the largest prime factor of $n$, tends to $\int_0^\infty \rho(t)/(1 + t)^2\, dt \approx 0.62433$, the Golomb Dickman constant (Knuth and Trabb Pardo). So the largest prime factor of a random number has on average about 62 percent of its digits.

## Where it is used

- **Group methods.** [Pollard's $p - 1$ method](/pollard-p-minus-1/) with bound $B$ finds $p$ when $p - 1$ is $B$-smooth, which happens for a fraction about $\rho(\ln p/\ln B)$ of primes. [ECM](/elliptic-curve-factorization/) succeeds on a curve with about the same probability for its group order near $p$; balancing the cost $B$ against $1/\rho$ gives $B = L_p[1/2, \sqrt 2/2]$ and the total $L_p[1/2, \sqrt 2]$ (Crandall and Pomerance, Section 7.4.1).
- **Sieve methods.** In the [quadratic sieve](/quadratic-sieve/) the values are near $x = M\sqrt N$, and a factor base bound $B = x^{1/u}$ makes a fraction about $u^{-u}$ of them smooth. The method needs about $\pi(B)$ [relations](/relation-collection/), so the cost is about $B \cdot u^u$ trials, and the best $u$ gives $L_N[1/2, 1]$. The same balance, with smoothness of two values at once, gives the $L_N[1/3, \cdot]$ of the [number field sieve](/general-number-field-sieve/).
- **Trial division.** Knuth and Trabb Pardo used $\rho$ and its relatives to find the distribution of the time that [trial division](/trial-division/) takes to factor a random number completely, which is set by the second largest prime factor.
- **Discrete logarithms.** Index calculus methods have the same balance between the size of the factor base and the chance of smoothness.
- **Large prime variations.** The density of numbers with one prime factor between $B$ and $B^v$ and the rest below $B$ is a similar integral of $\rho$, which tells how many extra relations the large prime variations give.

## References
