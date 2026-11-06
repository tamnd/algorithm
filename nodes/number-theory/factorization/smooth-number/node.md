---
tag: HRSZC6
kind: definition
slug: smooth-number
name: Smooth number
aliases:
- B-smooth number
- y-smooth integer
- y-smooth number
area: number-theory/factorization
level: core
summary: A positive integer is y-smooth (or B-smooth) when none of its prime factors is larger than y. How often numbers are smooth sets the cost of all subexponential factoring methods.
prereqs: [prime-number, fundamental-theorem-of-arithmetic]
see_also: [dickman-function, buchstab-function, factor-base, relation-collection, pollard-p-minus-1, quadratic-sieve, index-calculus, integer-factorization]
sources:
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition, Springer, 2005
    locator: Section 1.4.5, Smooth numbers, pages 48 to 49 (Definition 1.4.8, Theorem 1.4.9 of Dickman, the estimate (1.44) and the lower bound (1.45)); Section 3.3, Recognizing smooth numbers, page 128
  - paper: "E. R. Canfield, Paul Erdős and Carl Pomerance, On a problem of Oppenheim concerning factorisatio numerorum, Journal of Number Theory 17(1), 1983"
    locator: pages 1 to 28 (the estimate psi(x, x^(1/u)) = x u^(-u + o(u)))
  - paper: "Andrew Granville, Smooth numbers: computational number theory and beyond, in Algorithmic Number Theory, MSRI Publications 44, Cambridge University Press, 2008"
    locator: pages 267 to 323 (sections 1 to 4 on the counting function and its uses in factoring)
  - paper: "Adolf Hildebrand and Gérald Tenenbaum, Integers without large prime factors, Journal de Théorie des Nombres de Bordeaux 5(2), 1993"
    locator: pages 411 to 484 (a survey of the estimates for psi(x, y))
---

A positive integer is $y$-smooth, or $B$-smooth with $B = y$, when every [prime](/prime-number/) factor of it is at most $y$. The count $\Psi(x, y)$ of $y$-smooth numbers up to $x$ is the main quantity in the analysis of factoring: the [quadratic sieve](/quadratic-sieve/), the [number field sieve](/general-number-field-sieve/), [index calculus](/index-calculus/) and the [elliptic curve method](/elliptic-curve-factorization/) all wait for values to be smooth. Smooth numbers are rare when $y$ is small compared to $x$, but a smoothness bound $y = \exp(c\sqrt{\ln x \ln \ln x})$ makes them common enough, and this balance gives the [subexponential](/subexponential-time/) running times $L_x[1/2, c]$.

## Definition

**Smooth.** Let $y \ge 1$ be a real number. A positive integer $n$ is **$y$-smooth** if each prime $p \mid n$ satisfies $p \le y$. Equivalently, $P^+(n) \le y$, where $P^+(n)$ is the largest prime factor of $n$, with $P^+(1) = 1$. So $1$ is $y$-smooth for every $y$, and by the [fundamental theorem of arithmetic](/fundamental-theorem-of-arithmetic/) the $y$-smooth numbers are exactly the products $p_1^{e_1} \cdots p_k^{e_k}$ of the primes $p_1 < \cdots < p_k \le y$. In factoring, the bound is often called $B$, and a set of primes up to $B$ is a [factor base](/factor-base/).

**Powersmooth.** A positive integer $n$ is **$B$-powersmooth** if each prime power $p^e$ that divides $n$ has $p^e \le B$. A $B$-powersmooth number is $B$-smooth, and the $B$-powersmooth numbers are exactly the divisors of $\operatorname{lcm}(1, 2, \dots, B)$. [Pollard's $p - 1$ method](/pollard-p-minus-1/) with bound $B$ finds a prime $p$ exactly when $p - 1$ is $B$-powersmooth (and the other primes of $N$ are not caught at the same time).

**The counting function.** For real $x \ge 1$ and $y \ge 1$,
$$\Psi(x, y) = \#\{ 1 \le n \le x : n \text{ is } y\text{-smooth} \},$$
written $\psi(x, y)$ in Crandall and Pomerance. The ratio $u = \ln x / \ln y$, so that $y = x^{1/u}$, controls its size.

**Dickman's theorem.** For each fixed $u > 0$, $\Psi(x, x^{1/u}) \sim \rho(u)\, x$ as $x \to \infty$, where $\rho$ is the [Dickman function](/dickman-function/): $\rho(u) = 1$ for $0 \le u \le 1$, and $u \rho'(u) = -\rho(u - 1)$ for $u > 1$. So $\rho(u) = 1 - \ln u$ for $1 \le u \le 2$, and $\ln \rho(u) \sim -u \ln u$ as $u \to \infty$ (Crandall and Pomerance, Theorem 1.4.9 and (1.43)).

*Why $\rho(u) = 1 - \ln u$ on $[1, 2]$.* For $1 < u \le 2$, a number $n \le x$ fails to be $x^{1/u}$-smooth exactly when it has a prime factor $p > x^{1/u}$, and since $p^2 > x^{2/u} \ge x$, such a $p$ is unique. So $x - \Psi(x, x^{1/u}) = \sum_{x^{1/u} < p \le x} \lfloor x/p \rfloor$. By Mertens' estimate $\sum_{p \le t} 1/p = \ln \ln t + M + O(1/\ln t)$, the sum is $x(\ln \ln x - \ln \ln x^{1/u}) + o(x) = x \ln u + o(x)$. Hence $\Psi(x, x^{1/u}) = (1 - \ln u)x + o(x)$.

**Canfield, Erdős and Pomerance.** The estimate extends to $u$ that grows with $x$:
$$\Psi(x, x^{1/u}) = x\, u^{-u + o(u)}$$
uniformly as $u \to \infty$ with $u < (1 - \epsilon) \ln x / \ln \ln x$, for each fixed $\epsilon > 0$. This is the form used in the analysis of factoring.

**The consequence for subexponential methods.** Write $L_x[1/2, a] = \exp((a + o(1))\sqrt{\ln x \ln \ln x})$. If $y = L_x[1/2, a]$ with $a > 0$ fixed, then
$$u = \frac{\ln x}{\ln y} = \frac{1 + o(1)}{a}\sqrt{\frac{\ln x}{\ln \ln x}}, \qquad u \ln u = \frac{1 + o(1)}{2a}\sqrt{\ln x \ln \ln x},$$
since $\ln u = (\tfrac12 + o(1)) \ln \ln x$. So the estimate above gives
$$\frac{\Psi(x, y)}{x} = L_x[1/2, -1/(2a)].$$
A method that needs about $\pi(y)$ smooth values among numbers of size $x$ spends about $y \cdot L_x[1/2, 1/(2a)] = L_x[1/2, a + 1/(2a)]$ trials, which is smallest at $a = 1/\sqrt 2$, with cost $L_x[1/2, \sqrt 2]$. This calculation is the heart of the analyses of [Dixon's method](/dixon-random-squares/) and the [quadratic sieve](/quadratic-sieve/).

**A lower bound for all $x$.** Konyagin and Pomerance proved $\Psi(x, x^{1/u}) \ge x / (\ln x)^u$ for all $x \ge 4$ and $2 \le x^{1/u} \le x$ (Crandall and Pomerance, (1.45)). A short proof of a weaker form: the products $p_1 p_2 \cdots p_k$ of $k = \lfloor u \rfloor$ primes $p_i \le y$, in non-decreasing order, are $y$-smooth, at most $y^k \le x$, and pairwise distinct; there are at least $\pi(y)^k / k!$ of them.

## Examples and non-examples

- **5-smooth.** The 5-smooth numbers up to $100$ are $1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 18, 20, 24, 25, 27, 30, 32, 36, 40, 45, 48, 50, 54, 60, 64, 72, 75, 80, 81, 90, 96, 100$, so $\Psi(100, 5) = 34$. They are also called regular numbers or Hamming numbers. $\Psi(100, 10) = 46$.
- **2-smooth.** The 2-smooth numbers are the powers of two, so $\Psi(x, 2) = \lfloor \lg x \rfloor + 1$.
- **Smooth but not powersmooth.** $360 = 2^3 \cdot 3^2 \cdot 5$ is $5$-smooth but not $5$-powersmooth, because $2^3 = 8 > 5$; it is $9$-powersmooth. In the [$p - 1$ method](/pollard-p-minus-1/) this matters: $p = 61$ has $p - 1 = 60 = 2^2 \cdot 3 \cdot 5$, which is $5$-powersmooth, so the method finds $61$ with $B = 5$.
- **Non-example.** $202 = 2 \cdot 101$ is not $100$-smooth. Every prime $p$ is $p$-smooth but not $(p - 1)$-smooth.
- **The density at $u = 2$.** Among the numbers up to $10^6$, exactly $344{,}299$ are $1000$-smooth, a fraction $0.344$, while $\rho(2) = 1 - \ln 2 \approx 0.307$. At $u = 3$, $\Psi(10^6, 100) = 72{,}271$, a fraction $0.072$, while $\rho(3) \approx 0.0486$. The convergence in Dickman's theorem is slow, and for numbers of practical size the true density is larger than $\rho(u)$; the corrections are in Hildebrand and Tenenbaum.
- **Factoring numbers.** $9100 = 2^2 \cdot 5^2 \cdot 7 \cdot 13$ is $13$-smooth, so [trial division](/trial-division/) with bound $13$ factors it completely. The values $41^2 - 1649 = 32 = 2^5$ and $43^2 - 1649 = 200 = 2^3 \cdot 5^2$ are $5$-smooth, and their product is a square, which factors $1649 = 17 \cdot 97$ (see [congruence of squares](/congruence-of-squares/)).

## Related definitions

- **Rough numbers.** $n$ is $y$-rough if every prime factor is larger than $y$. Their count $\Phi(x, y)$ is described by the [Buchstab function](/buchstab-function/), as the smooth count is by the Dickman function.
- **Semismooth numbers.** $n$ is $(y, z)$-semismooth if all prime factors are at most $z$ and all but one are at most $y$. These are the partial relations of the large prime variation of the [quadratic sieve](/quadratic-sieve/) and of [relation collection](/relation-collection/) in general.
- **Smoothness over a factor base.** In the sieve methods, a value is smooth if it factors completely over a [factor base](/factor-base/), which may contain only part of the primes up to $B$ (for example the primes $p$ with $(N/p) = 1$).
- **Smooth polynomials and smooth ideals.** In the [number field sieve](/general-number-field-sieve/) and in [polynomial factorization over finite fields](/polynomial-factorization-over-finite-fields/), the same counting applies to norms of algebraic integers and to polynomials with all irreducible factors of small degree.
- **The largest prime factor.** $n$ is $y$-smooth if and only if $P^+(n) \le y$. The distribution of $P^+(n)$ and of the second largest factor controls the cost of [trial division](/trial-division/) (Knuth and Trabb Pardo).

## References
