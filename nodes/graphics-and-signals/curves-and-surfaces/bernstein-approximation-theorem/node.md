---
tag: 97AGZ1
kind: theorem
slug: bernstein-approximation-theorem
name: Bernstein approximation theorem
aliases:
- Bernstein polynomial approximation
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: The Bernstein polynomials B_n f converge uniformly to each continuous f on [0, 1], with error at most |f''| / (8n) for smooth f. The rate 1/n is slow, and it cannot be improved.
prereqs: [bernstein-polynomials, weierstrass-approximation-theorem]
see_also: [weierstrass-approximation-theorem, bernstein-polynomials, bezier-curve, variation-diminishing-property, jackson-theorem, chebyshev-interpolation, binomial-distribution, law-of-large-numbers]
sources:
  - paper: "Sergei N. Bernstein, Démonstration du théorème de Weierstrass fondée sur le calcul des probabilités, Communications de la Société Mathématique de Kharkow, series 2, 13 (1912) 1-2"
    title: Démonstration du théorème de Weierstrass fondée sur le calcul des probabilités
    locator: the definition of the polynomials and the proof of uniform convergence by the law of large numbers
  - paper: "Elizaveta V. Voronovskaya, Détermination de la forme asymptotique d'approximation des fonctions par les polynômes de M. Bernstein, Comptes Rendus de l'Académie des Sciences de l'URSS (1932) 79-85"
    title: Détermination de la forme asymptotique d'approximation des fonctions par les polynômes de M. Bernstein
    locator: the asymptotic formula n (B_n f - f) to x(1 - x) f''/2
  - book: isbn:9780828403238
    title: George G. Lorentz, Bernstein Polynomials, second edition, Chelsea, 1986
    locator: Chapter 1, the convergence of the polynomials, the derivatives and the asymptotic formula
  - paper: doi:10.1016/j.cagd.2012.03.001
    title: Rida T. Farouki, The Bernstein polynomial basis, a centennial retrospective, Computer Aided Geometric Design 29(6), 379-419 (2012)
    locator: the 1912 paper, the approximation properties and the later use of the basis in CAGD
---

The Bernstein approximation theorem says that the Bernstein polynomials $B_n f(x) = \sum_{k=0}^n f(k/n) \binom{n}{k} x^k (1 - x)^{n-k}$ of a continuous function $f$ on $[0, 1]$ converge to $f$ uniformly, and it gives the rate. For a function with a bounded second derivative the error is at most $\lVert f'' \rVert / (8n)$, and by Voronovskaya's formula the factor $1/n$ is exact unless $f$ is linear. So the convergence is slow, but it is constructive and it keeps the shape of $f$. The qualitative part is the constructive proof of the [Weierstrass approximation theorem](/weierstrass-approximation-theorem/); this page is about the rates, the derivatives and the shape.

## Statement

For a function $f : [0, 1] \to \mathbb{R}$ and $n \ge 1$, let $B_n f = \sum_{k=0}^n f(k/n)\, b_{n,k}$ with $b_{n,k}(x) = \binom{n}{k} x^k (1 - x)^{n-k}$, the [Bernstein polynomials](/bernstein-polynomials/) of degree $n$. Let $\lVert g \rVert$ be the maximum of $|g|$ on $[0, 1]$, and $\omega_f(\delta) = \sup \{ |f(x) - f(y)| : |x - y| \le \delta \}$ the modulus of continuity.

**Theorem.**

(a) If $f$ is continuous, then $\lVert B_n f - f \rVert \le \frac32\, \omega_f(n^{-1/2})$, so $B_n f \to f$ uniformly.

(b) If $f \in C^2[0, 1]$, then for each $x \in [0, 1]$,
$$|B_n f(x) - f(x)| \le \frac{x (1 - x)}{2n} \lVert f'' \rVert \le \frac{\lVert f'' \rVert}{8n}.$$

(c) (Voronovskaya.) If $f \in C^2[0, 1]$, then
$$\lim_{n \to \infty} n \big(B_n f(x) - f(x)\big) = \frac{x (1 - x)}{2} f''(x),$$
uniformly in $x \in [0, 1]$.

(d) If $f \in C^1[0, 1]$, then $(B_n f)' \to f'$ uniformly.

## In plain words

To build a polynomial that follows a given curve, sample the curve at evenly spaced points and blend the samples with smooth weights that peak near each point. The theorem says that this blend gets as close to the curve as you like, everywhere at once, when you use more and more samples.

It also says how fast. With ten times more samples, the error of a smooth curve becomes about ten times smaller, and not faster, even when the curve is very simple. Other methods do much better. But the blend never adds wiggles, and its slope also follows the slope of the curve. For this reason the same weights became the basis of Bézier curves in design.

## Proof

The proof is in [the full proof](proofs/main.md). It uses the moments of the binomial distribution: for $x \in [0, 1]$ and $Y = S/n - x$ with $S$ binomial with parameters $n$ and $x$,
$$\mathbb{E}\, Y = 0, \qquad \mathbb{E}\, Y^2 = \frac{x (1 - x)}{n}, \qquad \mathbb{E}\, Y^4 = \frac{x (1 - x) \big(1 + 3 (n - 2) x (1 - x)\big)}{n^3} \le \frac{7}{16 n^2}.$$
Here $B_n f(x) = \mathbb{E} f(S/n)$.

1. **Part (a).** For $\delta > 0$, $|f(y) - f(x)| \le (1 + |y - x|/\delta)\, \omega_f(\delta)$, because $\omega_f$ is subadditive. Take the mean and use $\mathbb{E} |Y| \le (\mathbb{E}\, Y^2)^{1/2} \le 1/(2\sqrt n)$. With $\delta = n^{-1/2}$ the bound is $\frac32 \omega_f(n^{-1/2})$. This differs from the proof on the Weierstrass page, which splits the sum into near and far terms.
2. **Part (b).** By Taylor's theorem, $f(y) = f(x) + f'(x)(y - x) + R$ with $|R| \le \frac12 \lVert f'' \rVert (y - x)^2$. The mean of the linear term is 0, and the mean of $|R|$ is at most $\frac12 \lVert f'' \rVert\, x (1 - x)/n$.
3. **Part (c).** Write $R = \frac12 f''(x)(y - x)^2 + h(y)(y - x)^2$ with $|h(y)| \le \frac12 \omega_{f''}(|y - x|)$ and $|h| \le \lVert f'' \rVert$. The first term gives the limit exactly. For the second, the terms with $|Y| < \delta$ contribute at most $\frac18 \omega_{f''}(\delta)$ after multiplication by $n$, and the others at most $\lVert f'' \rVert\, n\, \mathbb{E}\, Y^4 / \delta^2 \le \frac{7 \lVert f'' \rVert}{16 n \delta^2}$, by the fourth moment.
4. **Part (d).** The derivative of a Bernstein form is $(B_n f)'(x) = \sum_{k=0}^{n-1} n \big(f(\frac{k+1}{n}) - f(\frac{k}{n})\big) b_{n-1,k}(x)$. By the mean value theorem each difference quotient is $f'(\xi_k)$ with $\xi_k$ in $(\frac kn, \frac{k+1}{n})$, an interval that contains $\frac{k}{n-1}$. So $\lVert (B_n f)' - B_{n-1}(f') \rVert \le \omega_{f'}(1/n)$, and part (a) for $f'$ ends the proof.

## Consequences

- **Shape preservation.** By the derivative formula in step 4 and its second order form $(B_n f)'' = n (n - 1) \sum_k \Delta^2 f(\frac kn)\, b_{n-2,k}$, with $\Delta^2 f(\frac kn) = f(\frac{k+2}{n}) - 2 f(\frac{k+1}{n}) + f(\frac kn)$: if $f$ is nondecreasing, so is $B_n f$, and if $f$ is convex, so is $B_n f$. More generally $B_n f$ has at most as many sign changes in $(0, 1)$ as $f$, by the [variation diminishing property](/variation-diminishing-property/).
- **One-sided error for convex functions.** If $f$ is convex, then $B_n f \ge f$, by Jensen's inequality: $B_n f(x) = \mathbb{E} f(S/n) \ge f(\mathbb{E}\, S/n) = f(x)$.
- **Linear functions are fixed.** $B_n f = f$ for $f(x) = a + bx$, by the first two moments. By (c), these are the only $C^2$ functions with $\lVert B_n f - f \rVert = o(1/n)$: if $n (B_n f - f) \to 0$ then $x (1 - x) f''(x) = 0$, so $f'' = 0$ on $(0, 1)$. This is the saturation of the method at the rate $1/n$.
- **The graph is a Bézier curve.** The graph of $B_n f$ is the [Bézier curve](/bezier-curve/) with the control points $(k/n, f(k/n))$, because $\sum_k \frac kn b_{n,k}(x) = x$. So the theorem says that the Bézier curve of the polygon inscribed in the graph of $f$ converges to that graph.
- **Probability.** The formula $B_n f(x) = \mathbb{E} f(S/n)$ makes part (a) a quantitative form of the weak [law of large numbers](/law-of-large-numbers/) for a [binomial distribution](/binomial-distribution/): $S/n$ concentrates at $x$ with spread $\sqrt{x (1 - x)/n}$.

## Tightness

- **The constant in (b) is exact.** For $f(x) = x^2$, $B_n f(x) - f(x) = x (1 - x)/n$, which is the bound of (b) with $\lVert f'' \rVert = 2$. At $x = 1/3$ the errors are $2/9$, $1/9$ and $2/45$ for $n = 1, 2, 5$.
- **The rate 1/n is real for smooth functions.** For $f(x) = \sin(\pi x)$ at $x = 1/2$, (c) gives $n (f - B_n f) \to \pi^2/8 \approx 1.2337$. The values are $1.1651$ for $n = 10$, $1.2262$ for $n = 100$ and $1.2329$ for $n = 1000$. For $f(x) = x^3$ the exact error is $B_n f(x) - f(x) = 3x^2 (1 - x)/n + x (1 - x)(1 - 2x)/n^2$, in agreement with (c), since $\frac{x (1 - x)}{2} \cdot 6x = 3x^2 (1 - x)$.
- **Much slower than the best polynomial.** For $f \in C^2$ the best approximation of degree $n$ has an error of order $\lVert f'' \rVert / n^2$ by [Jackson's theorems](/jackson-theorem/), and [Chebyshev interpolation](/chebyshev-interpolation/) of an analytic function converges geometrically. Bernstein polynomials reach only $1/n$, so they are not used to approximate functions to high accuracy.
- **Continuous functions without smoothness.** For $f(x) = |x - \frac12|$ the error at $x = \frac12$ decays like $n^{-1/2}$, the order of (a); the numbers, and the reason that continuity is needed, are on the [Weierstrass approximation theorem](/weierstrass-approximation-theorem/) page.

## History

Sergei Bernstein gave the polynomials in 1912, in a two-page note with a probabilistic proof of the Weierstrass theorem: a player wins $f(k/n)$ after $k$ successes in $n$ trials with probability $x$, and the expected gain tends to $f(x)$. Elizaveta Voronovskaya found the asymptotic formula (c) in 1932. The bound (a) with the modulus of continuity is due to Tiberiu Popoviciu (1935), with a different proof. Lorentz collected the theory in his book of 1953, with a second edition in 1986. From about 1960, de Casteljau and Bézier used the same polynomials as the basis of their curves, and the shape properties became the main reason for their use; Farouki's centennial survey of 2012 traces both lines.

## References
