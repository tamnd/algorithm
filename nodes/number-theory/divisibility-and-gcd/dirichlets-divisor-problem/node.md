---
tag: 9M01SN
kind: problem
slug: dirichlets-divisor-problem
name: Dirichlet's divisor problem
aliases:
- divisor problem
- error term of the divisor sum
area: number-theory/divisibility-and-gcd
level: research
summary: Determine the error term in the asymptotics of the divisor summatory function.
prereqs: [divisor-summatory-function, dirichlet-hyperbola-method]
see_also: [lattice-point-counting, divisor-function, prime-number-theorem, dirichlet-convolution, harmonic-series, divisor-count-sieve, multiplicative-function, euler-totient]
sources:
  - book: isbn:9780198533696
    title: E. C. Titchmarsh, The Theory of the Riemann Zeta-Function, second edition, revised by D. R. Heath-Brown
    locator: Chapter 12, Divisor problems (the Voronoi bound, the Omega theorem, the mean square, and the exponent-pair method)
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Chapter 18, Section 18.2, The average order of d(n) (Dirichlet's theorem with error O(x^(1/2)))
  - paper: "G. H. Hardy, On Dirichlet's divisor problem, Proceedings of the London Mathematical Society (2) 15, 1916"
    locator: pages 1 to 25
  - paper: "M. N. Huxley, Exponential sums and lattice points III, Proceedings of the London Mathematical Society (3) 87, 2003"
    locator: pages 591 to 609 (the exponent 131/416 for the divisor and circle problems)
  - paper: "Jean Bourgain and Nigel Watt, Mean square of zeta function, circle problem and divisor problem revisited, arXiv:1709.04340, 2017"
    locator: abstract and comments (the claimed exponent 517/1648; the preprint was withdrawn in 2023)
  - url: "https://en.wikipedia.org/wiki/Divisor_summatory_function"
    locator: Wikipedia, Divisor summatory function, section Dirichlet's divisor problem (the table of exponents)
---

Dirichlet's divisor problem asks for the true size of the error term $\Delta(x)$ in

$$D(x) = \sum_{n \le x} d(n) = x \ln x + (2\gamma - 1) x + \Delta(x),$$

where $d(n)$ is the number of divisors of $n$ and $\gamma$ is the Euler-Mascheroni constant. Dirichlet proved $\Delta(x) = O(x^{1/2})$ in 1849 with the [hyperbola method](/dirichlet-hyperbola-method/); Voronoi lowered the exponent to $1/3$, Hardy proved that it cannot go below $1/4$, and the conjecture is that $\Delta(x) = O(x^{1/4 + \varepsilon})$ for every $\varepsilon > 0$. The best established exponent is Huxley's $131/416 \approx 0.3149$ from 2003. The problem is the hyperbola twin of the Gauss circle problem, and progress on both comes from bounds on exponential sums.

## In plain words

Add up the number of divisors of every whole number up to some limit. A simple formula predicts this total very well, and the question is how far the true total can drift from the formula.

The total counts grid points under a curved line, and the formula is essentially the area under that line. The error comes from the points near the curve, which sometimes fall just inside and sometimes just outside. If they behaved like coin flips, the error would be about the fourth root of the limit. It is known that the error does reach that size infinitely often, and that it never grows faster than roughly the cube root. Closing the gap between the fourth root and the cube root has been open for more than a century.

## Definition

For real $x \ge 1$ let $D(x) = \sum_{n \le x} d(n)$, the number of pairs of positive integers $(a, b)$ with $ab \le x$, the [divisor summatory function](/divisor-summatory-function/), and

$$\Delta(x) = D(x) - x \ln x - (2\gamma - 1) x.$$

Let $\theta$ be the infimum of the exponents $\alpha$ such that $\Delta(x) = O(x^{\alpha})$ as $x \to \infty$.

**The problem.** Determine $\theta$, and more precisely the order of $\Delta(x)$. Known: $1/4 \le \theta \le 131/416$. **Conjecture:** $\theta = 1/4$.

Some authors write the main term as $x \ln x + (2\gamma - 1)x + \tfrac14$, because $\Delta(x)$ has mean value $1/4$; the constant does not change $\theta$.

## Variants

- **The Gauss circle problem.** $N(r) = \#\{ (a, b) \in \mathbb{Z}^2 : a^2 + b^2 \le r^2 \} = \pi r^2 + P(r)$. With $x = r^2$, the conjectured and best known exponents for $P$ in terms of $x$ are the same as for $\Delta$: Huxley's $131/416$ covers both.
- **Piltz divisor problem.** For $d_k(n)$, the number of ordered factorizations of $n$ into $k$ factors, $\sum_{n \le x} d_k(n) = x P_{k-1}(\ln x) + \Delta_k(x)$ with a polynomial $P_{k-1}$ of degree $k - 1$; the exponent $\alpha_k$ of $\Delta_k$ is conjectured to be $(k - 1)/(2k)$. The Lindelöf hypothesis for the Riemann zeta function is equivalent to $\alpha_k \le 1/2$ for every $k$.
- **Mean values.** Instead of the maximum of $|\Delta|$, the moments $\int_1^X \Delta(x)^k \, dx$.
- **Sign changes and distribution.** How often $\Delta(x)$ changes sign, and the distribution of $\Delta(x)/x^{1/4}$.
- **Other weights.** Error terms of $\sum_{n \le x} \sigma(n)$, of $\sum_{n \le x} \varphi(n)$ and of other sums of [multiplicative functions](/multiplicative-function/) built from the divisor function.
- **Computation.** Compute $\Delta(x)$ exactly for very large $x$, which needs $D(x)$ exactly.

## Examples

**Small values.** $D(10) = 27$ and $10 \ln 10 + (2\gamma - 1) \cdot 10 = 24.57$, so $\Delta(10) = 2.43$.

**Large values.** Exact values of $D(10^k)$ give

| $x$ | $\Delta(x)$ | $\Delta(x)/x^{1/4}$ | $x^{1/3}$ |
|---|---|---|---|
| $10^4$ | 20.28 | 2.03 | 21.5 |
| $10^6$ | 92.11 | 2.91 | 100 |
| $10^8$ | 360.62 | 3.61 | 464 |
| $10^{10}$ | 622.57 | 1.97 | 2154 |
| $10^{12}$ | 3354.39 | 3.35 | 10000 |
| $10^{14}$ | 9083.47 | 2.87 | 46416 |

The ratio $\Delta(x)/x^{1/4}$ stays of moderate size, as the conjecture predicts, while $x^{1/3}$ pulls away.

**Mean and mean square.** Over $1 \le x \le 2 \cdot 10^6$, the average of $\Delta(x)$ is $0.249$, close to $1/4$, and $\int_1^X \Delta(x)^2 \, dx / X^{3/2}$ is $0.648$, close to Cramér's constant $\zeta(3/2)^4 / (6\pi^2 \zeta(3)) = 0.6543$.

## Known algorithms

The problem is a question of proof, and the known results are bounds, each from a new method for exponential sums.

| year | author | $\theta \le$ | value |
|---|---|---|---|
| 1849 | Dirichlet | $1/2$ | 0.5 |
| 1903 | Voronoi | $1/3$ | 0.3333 |
| 1922 | van der Corput | $33/100$ | 0.33 |
| 1928 | van der Corput | $27/82$ | 0.3293 |
| 1950, 1953 | Chih; Richert | $15/46$ | 0.3261 |
| 1982 | Kolesnik | $35/108$ | 0.3241 |
| 1988 | Iwaniec and Mozzochi | $7/22$ | 0.3182 |
| 2003 | Huxley | $131/416$ | 0.3149 |
| 2017 (withdrawn) | Bourgain and Watt | $517/1648$ | 0.3137 |

**Dirichlet: the hyperbola.** The symmetric count $D(x) = 2 \sum_{n \le \sqrt x} \lfloor x/n \rfloor - \lfloor \sqrt x \rfloor^2$ and $\lfloor t \rfloor = t + O(1)$ give $O(\sqrt x)$ directly.

**The sawtooth sum.** Writing $\lfloor t \rfloor = t - \tfrac12 - \psi(t)$ with $\psi(t) = \{t\} - \tfrac12$, the same identity gives

$$\Delta(x) = -2 \sum_{n \le \sqrt x} \psi\!\left(\frac{x}{n}\right) + O(1).$$

So $\theta$ is decided by cancellation in a sum of $\sqrt x$ sawtooth values: with no cancellation the sum is $O(\sqrt x)$, and random signs would give about $x^{1/4}$. Expanding $\psi$ in a Fourier series turns the problem into bounds for exponential sums $\sum e(h x / n)$.

**Voronoi: the summation formula.** Voronoi expressed $\Delta$ as a series of Bessel functions; truncated, it reads

$$\Delta(x) = \frac14 + \frac{x^{1/4}}{\pi \sqrt 2} \sum_{n \le N} \frac{d(n)}{n^{3/4}} \cos\!\left(4\pi\sqrt{nx} - \frac{\pi}{4}\right) + O\!\left(x^{1/2 + \varepsilon} N^{-1/2}\right),$$

and bounding the sum gives $\Delta(x) = O(x^{1/3} \log x)$. The factor $x^{1/4}$ in front is the source of the conjecture.

**Exponential sums.** Van der Corput's method of exponent pairs, the Bombieri-Iwaniec method (1986) and Huxley's refinement of it, the discrete Hardy-Littlewood method, produced the later exponents. Bourgain and Watt announced $517/1648$ in 2017, with new estimates for the first spacing problem of the Bombieri-Iwaniec method, but the preprint was withdrawn in 2023 because of gaps in the proofs, so $131/416$ remains the best established bound.

**Computation of $\Delta(x)$.** Exact values for large $x$ come from computing $D(x)$ with the hyperbola method in $O(\sqrt x)$ steps, or with Sladkey's convex-hull method in $O(x^{1/3})$ steps.

## Bounds

- **Upper.** $\Delta(x) = O(x^{131/416 + \varepsilon})$ (Huxley 2003, with a power of $\log x$ instead of $x^{\varepsilon}$).
- **Lower.** Hardy (1916): $\Delta(x) = \Omega(x^{1/4})$, and more precisely $\Delta(x) > K x^{1/4}$ and $\Delta(x) < -K x^{1/4}$ for arbitrarily large $x$, for some constant $K > 0$. Later work, by Hafner (1981) and Soundararajan (2003), improved the lower bound by powers of $\log x$ and $\log \log x$. So $\theta \ge 1/4$, and $\Delta(x) = O(x^{1/4})$ itself is false.
- **Mean square.** Cramér (1922): $\int_1^X \Delta(x)^2 \, dx = c X^{3/2} + O(X^{5/4 + \varepsilon})$ with $c = \frac{1}{6\pi^2} \sum_{n \ge 1} \frac{d(n)^2}{n^{3/2}} = \frac{\zeta(3/2)^4}{6\pi^2 \zeta(3)}$; Tong (1956) improved the error to $O(X \log^5 X)$. So $\Delta(x)$ is of size $x^{1/4}$ on average, which supports the conjecture.
- **Distribution.** Heath-Brown (1992): $\Delta(x)/x^{1/4}$ has a limiting distribution, with a density, which is not Gaussian.

## Reductions

- **Lattice points under a hyperbola.** $D(x)$ is the number of lattice points in $\{a, b \ge 1, ab \le x\}$, and $\Delta(x)$ is the difference between this count and a smoothed area; see [lattice point counting](/lattice-point-counting/).
- **To exponential sums.** The sawtooth formula reduces bounds for $\Delta$ to bounds for $\sum_{n \le \sqrt x} \psi(x/n)$, and so to sums $\sum_{n} e(hx/n)$ over short ranges; each improvement on such sums improves $\theta$.
- **To the circle problem.** Both problems reduce to the same type of sums of $\psi$ along a convex curve, $\sum \psi(f(n))$ with $f$ of a given smoothness, which is why their exponents move together.
- **To the zeta function.** By Perron's formula, $D(x) = \frac{1}{2\pi i} \int \zeta(s)^2 x^s \frac{ds}{s}$, and $\Delta$ comes from moving the line of integration left of the double pole at $s = 1$; bounds on $\zeta$ on the critical line give bounds on $\Delta$, and the mean square of $\Delta$ is linked to the fourth moment of $\zeta$.

## Applications

- **A test bed for exponential sum methods.** Most methods for bounding exponential sums, from van der Corput to Bombieri-Iwaniec and Huxley, were first measured by the exponent they give for the divisor and circle problems.
- **Error terms in other counting problems.** Sums of $d(n)$ appear in the analysis of [divisor count sieves](/divisor-count-sieve/), in averages over $\gcd$ and lcm, and in counting matrices and lattices; their error terms inherit the exponent $\theta$.
- **Zeta function moments.** The mean square of $\Delta$ and the fourth power moment of $\zeta(1/2 + it)$ are proved with the same tools, and results transfer between them.
- **Numerical experiments.** Exact values of $\Delta(x)$ for large $x$ test the conjectures on its growth and distribution.

## References
