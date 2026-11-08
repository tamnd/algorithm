---
tag: 82S31K
kind: theorem
slug: weierstrass-approximation-theorem
name: Weierstrass approximation theorem
aliases:
- Weierstrass theorem
- Weierstrass density theorem
area: numerical/interpolation-and-approximation
level: core
summary: Every continuous function on a closed bounded interval is a uniform limit of polynomials. Bernstein polynomials prove it, with error at most (3/2) times the modulus of continuity at n^(-1/2).
prereqs: [polynomial, approximation-theory]
see_also: [bernstein-polynomials, stone-weierstrass-theorem, minimax-approximation, chebyshev-interpolation, jackson-theorem, lebesgue-constant, runge-phenomenon, trigonometric-interpolation]
sources:
  - paper: "Karl Weierstrass, Über die analytische Darstellbarkeit sogenannter willkürlicher Functionen einer reellen Veränderlichen, Sitzungsberichte der Königlich Preussischen Akademie der Wissenschaften zu Berlin (1885) 633-639 and 789-805"
    locator: the theorem for continuous functions on an interval and its trigonometric counterpart, proved by smoothing with a heat kernel
  - paper: "Sergei N. Bernstein, Démonstration du théorème de Weierstrass fondée sur le calcul des probabilités, Communications de la Société Mathématique de Kharkow, series 2, 13 (1912) 1-2"
    locator: the proof with the polynomials now named after Bernstein
  - book: isbn:9781611975932
    title: Lloyd N. Trefethen, Approximation Theory and Approximation Practice, extended edition, SIAM, 2019
    locator: Chapter 6, Weierstrass approximation theorem
  - book: isbn:9780521295147
    title: M. J. D. Powell, Approximation Theory and Methods, Cambridge University Press, 1981
    locator: Chapter 6, The uniform convergence of polynomial approximations (the Weierstrass theorem and the Bernstein operator)
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Section 4.1, The Weierstrass theorem and Taylor's theorem
  - book: isbn:9780486624952
    title: Philip J. Davis, Interpolation and Approximation, Dover, 1975 (first published 1963)
    locator: Chapter VI, the Weierstrass theorem and Bernstein polynomials
  - paper: "Allan Pinkus, Weierstrass and approximation theory, Journal of Approximation Theory 107(1) (2000) 1-66"
    locator: the history of the theorem and of its many proofs
---

The Weierstrass approximation theorem says that polynomials can approximate any continuous function on a closed bounded interval as closely as we like, uniformly over the whole interval. It is the reason polynomials are a sound basis for numerical approximation of continuous functions. It is the starting point of approximation theory: once we know that the best error $E_n(f)$ tends to 0, the questions become how fast it does so and how to find good approximations. The proof given here, due to Bernstein, is constructive and comes with an error bound.

## Statement

Notation on the interpolation pages: $f$ is a real function on $[a, b]$, $\mathcal{P}_n$ is the space of polynomials of degree at most $n$, $\|g\|_\infty = \max_{x \in [a,b]} |g(x)|$, and $E_n(f) = \min_{p \in \mathcal{P}_n} \|f - p\|_\infty$ is the error of best approximation. The modulus of continuity of $f$ is $\omega_f(\delta) = \sup\{|f(x) - f(y)| : x, y \in [a, b],\ |x - y| \le \delta\}$.

**Theorem (Weierstrass, 1885).** Let $f$ be continuous on the closed bounded interval $[a, b]$. For every $\varepsilon > 0$ there is a polynomial $p$ with $\|f - p\|_\infty < \varepsilon$. Equivalently, $E_n(f) \to 0$ as $n \to \infty$, and the polynomials are dense in $C[a, b]$ with the maximum norm.

**Constructive form (Bernstein, 1912).** On $[0, 1]$ the Bernstein polynomials
$$B_n f(x) = \sum_{k=0}^{n} f\!\left(\frac{k}{n}\right) \binom{n}{k} x^k (1 - x)^{n-k}$$
satisfy $\|f - B_n f\|_\infty \to 0$ for every $f \in C[0, 1]$. More precisely, $\|f - B_n f\|_\infty \le \tfrac{3}{2}\, \omega_f(n^{-1/2})$ (Popoviciu's bound).

## In plain words

Take any curve you can draw on a closed stretch of the line without lifting the pen, however jagged. The theorem says that there is a polynomial whose graph stays within any distance you choose of your curve, everywhere on that stretch at once.

The polynomial may need a very high degree for a jagged curve and a tight tolerance, but it always exists. Bernstein's proof builds one by averaging the curve's values at evenly spaced points, with weights that concentrate more and more around the point being approximated.

## Proof

It suffices to treat $[0, 1]$: if $g(s) = f(a + s(b - a))$ is approximated within $\varepsilon$ by a polynomial $q(s)$ on $[0, 1]$, then $p(x) = q((x - a)/(b - a))$ is a polynomial that approximates $f$ within $\varepsilon$ on $[a, b]$.

Write $b_{n,k}(x) = \binom{n}{k} x^k (1 - x)^{n-k}$. For $x \in [0, 1]$ these are non-negative, and they are the probabilities of $k$ successes in $n$ independent trials with success probability $x$.

1. **Three moments.** By the binomial theorem, $\sum_k b_{n,k}(x) = (x + 1 - x)^n = 1$. Differentiating $(s + 1 - x)^n = \sum_k \binom{n}{k} s^k (1 - x)^{n-k}$ in $s$ once and twice and setting $s = x$ gives $\sum_k k\, b_{n,k}(x) = n x$ and $\sum_k k(k - 1)\, b_{n,k}(x) = n(n-1) x^2$. Hence
$$\sum_{k=0}^{n} \left(\frac{k}{n} - x\right)^2 b_{n,k}(x) = \frac{n(n-1)x^2 + n x}{n^2} - 2x \cdot x + x^2 = \frac{x(1 - x)}{n} \le \frac{1}{4n}.$$
2. **Split the error.** Since the weights sum to 1,
$$f(x) - B_n f(x) = \sum_{k=0}^{n} \left(f(x) - f\!\left(\tfrac{k}{n}\right)\right) b_{n,k}(x).$$
Let $\varepsilon > 0$. Because $f$ is continuous on the compact set $[0, 1]$, it is bounded, $|f| \le M$, and uniformly continuous: there is $\delta > 0$ with $|f(x) - f(y)| < \varepsilon/2$ whenever $|x - y| < \delta$.
3. **Near terms.** The terms with $|k/n - x| < \delta$ contribute at most $\tfrac{\varepsilon}{2} \sum_k b_{n,k}(x) = \tfrac{\varepsilon}{2}$ in absolute value.
4. **Far terms.** For $|k/n - x| \ge \delta$ we have $|f(x) - f(k/n)| \le 2M \le 2M (k/n - x)^2/\delta^2$, so by step 1 these terms contribute at most
$$\frac{2M}{\delta^2} \sum_{k} \left(\frac{k}{n} - x\right)^2 b_{n,k}(x) \le \frac{2M}{\delta^2} \cdot \frac{1}{4n} = \frac{M}{2 n \delta^2}.$$
5. **Conclusion.** For every $x \in [0, 1]$, $|f(x) - B_n f(x)| \le \varepsilon/2 + M/(2n\delta^2)$, and the right side does not depend on $x$. For $n > M/(\varepsilon \delta^2)$ it is less than $\varepsilon$. So $\|f - B_n f\|_\infty \to 0$, and $B_n f$ is the required polynomial. $\blacksquare$

*Popoviciu's bound.* For $\delta > 0$ and any $x, y$, $|f(x) - f(y)| \le (1 + |x - y|^2/\delta^2)\, \omega_f(\delta)$: if $|x - y| \le \delta$ this is clear, and otherwise split $[x, y]$ into $m = \lceil |x - y|/\delta \rceil \le 1 + |x - y|^2/\delta^2$ pieces of length at most $\delta$ (the inequality $m < 1 + |x-y|/\delta \le 1 + |x-y|^2/\delta^2$ uses $|x - y| > \delta$). Inserting this in step 2 and using step 1 gives $|f(x) - B_n f(x)| \le (1 + 1/(4n\delta^2))\, \omega_f(\delta)$, and $\delta = n^{-1/2}$ gives the factor $5/4$, which is below $3/2$. (Popoviciu stated the constant $3/2$; the argument above already gives $5/4$.)

## Consequences

- **Best approximations converge.** $E_n(f) \to 0$ for every continuous $f$, so the [minimax approximations](/minimax-approximation/) $p_n^*$ converge uniformly to $f$. Combined with the bound $\|f - p_n\| \le (1 + \Lambda_n) E_n(f)$ of the [Lebesgue constant](/lebesgue-constant/), interpolants converge whenever $E_n(f)$ falls faster than $\Lambda_n$ grows. For [Chebyshev interpolation](/chebyshev-interpolation/), with $\Lambda_n = O(\log n)$, this covers every Dini-Lipschitz $f$.
- **Other norms.** Since $\|g\|_{L^p} \le (b - a)^{1/p} \|g\|_\infty$ and continuous functions are dense in $L^p[a, b]$ for $1 \le p < \infty$, polynomials are dense in $L^p[a, b]$ as well. This is why orthogonal polynomial expansions converge in $L^2$.
- **Periodic functions.** Every continuous $2\pi$-periodic function is a uniform limit of trigonometric polynomials (Weierstrass proved this too; Fejér's averages of the Fourier series give a constructive proof). See [trigonometric interpolation](/trigonometric-interpolation/).
- **Generalizations.** The [Stone-Weierstrass theorem](/stone-weierstrass-theorem/) replaces polynomials on an interval by any algebra of continuous functions on a compact space that contains the constants and separates points; it gives, for example, density of multivariate polynomials on compact subsets of $\mathbb{R}^d$.
- **Rates need smoothness.** The theorem gives no rate. [Jackson's theorems](/jackson-theorem/) give $E_n(f) \le C\, \omega_f(1/n)$ on $[-1, 1]$, and faster rates when $f$ has derivatives; Bernstein's inverse theorems show that these rates characterize smoothness.

**Bernstein polynomials are slow.** For $f(x) = x^2$, $B_n f(x) - f(x) = x(1-x)/n$, so the error is exactly $1/(4n)$ even though $f$ is a polynomial. For $f(x) = |x - \tfrac12|$ the error at $x = \tfrac12$ is the mean absolute deviation of a binomial proportion:

| $n$ | $\lVert f - B_n f\rVert_\infty$ | $1/\sqrt{2\pi n}$ | Chebyshev interpolant, same $n$ |
|---|---|---|---|
| 10 | 0.1230 | 0.1262 | 0.0296 |
| 100 | 0.0398 | 0.0399 | 0.00298 |
| 1000 | 0.0126 | 0.0126 | |

The Bernstein error falls like $n^{-1/2}$, the Chebyshev interpolant's like $n^{-1}$, which is the optimal rate for this $f$. Bernstein polynomials prove the theorem and preserve shape (they are monotone and convexity preserving), but they are not used for accurate approximation; see [Bernstein polynomials](/bernstein-polynomials/).

## Tightness

- **Compactness is needed.** On an open or unbounded interval the statement fails. On $(0, 1)$, $f(x) = 1/x$ is continuous but unbounded, and no polynomial, which is bounded on $(0, 1)$, approximates it uniformly. On $\mathbb{R}$, if $\|p_n - f\|_\infty \to 0$ then $p_n - p_N$ is a bounded polynomial on $\mathbb{R}$ for a fixed large $N$ and all $n \ge N$, hence a constant $c_n$, and $f = p_N + \lim c_n$ is itself a polynomial: $\sin x$ is not a uniform limit of polynomials on $\mathbb{R}$.
- **Continuity is needed.** A uniform limit of continuous functions is continuous, so a function with a jump has $E_n(f) \ge \tfrac12 |\text{jump}|$ for every $n$.
- **No rate without more hypotheses.** For every non-increasing sequence $\varepsilon_n \to 0$ there is a continuous $f$ with $E_n(f) = \varepsilon_n$ for all $n$ (Bernstein's lethargy theorem), so no rate holds for all continuous functions.
- **Fewer monomials.** Müntz's theorem (1914) says the span of $1, x^{\lambda_1}, x^{\lambda_2}, \ldots$ with $0 < \lambda_1 < \lambda_2 < \cdots \to \infty$ is dense in $C[0, 1]$ exactly when $\sum_k 1/\lambda_k = \infty$. So the full set of powers is more than is needed, but not by much.
- **Interpolation is not enough.** The theorem does not say that interpolants at a fixed array of nodes converge; by Faber's theorem, for every array some continuous $f$ has divergent interpolants (see the [Runge phenomenon](/runge-phenomenon/)).

## History

Weierstrass proved the theorem in 1885, at the age of 70, by convolving $f$ with a Gaussian (heat) kernel and truncating the Taylor series of the result; he proved the trigonometric version in the same paper. Many proofs followed: Runge (1885-1886) by rational functions, Lebesgue (1898) by approximating $|x|$, Fejér (1900) by Cesàro means of Fourier series, Landau (1908) by a polynomial kernel, and Bernstein (1912) by the probabilistic argument above. Stone generalized the theorem in 1937 and 1948. Pinkus (2000) surveys this history.

## References
