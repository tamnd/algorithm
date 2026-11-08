---
tag: 6N3RZF
kind: concept
slug: chebyshev-nodes
name: Chebyshev nodes
aliases:
- Chebyshev points
- Chebyshev zeros
- Chebyshev-Lobatto points
- Chebyshev extreme points
area: numerical/interpolation-and-approximation
level: core
summary: The zeros of T_(n+1) or the extrema of T_n on [-1, 1], clustered near the ends. Interpolation there has a Lebesgue constant of order log n and converges for every Lipschitz function.
prereqs: [chebyshev-polynomials, interpolation-problem]
see_also: [chebyshev-polynomials, chebyshev-interpolation, lebesgue-constant, runge-phenomenon, barycentric-interpolation, clenshaw-curtis-quadrature, polynomial-interpolation-error-theorem, interpolation-problem]
sources:
  - book: isbn:9781611975932
    title: Lloyd N. Trefethen, Approximation Theory and Approximation Practice, extended edition, SIAM, 2019
    locator: Chapter 2 (Chebyshev points and interpolants), Chapter 5 (the barycentric weights for Chebyshev points), Chapter 12 (potential theory and the arcsine density), Chapter 13 (equispaced points and the Runge phenomenon) and Chapter 15 (Lebesgue constants, Theorem 15.2)
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 8, Polynomial approximation in the maximum norm (Chebyshev polynomials and the choice of interpolation points that minimizes the node polynomial)
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Section 4.7, Near-minimax approximations (interpolation at the Chebyshev zeros)
  - book: isbn:9780849303555
    title: J. C. Mason and D. C. Handscomb, Chebyshev Polynomials, Chapman and Hall/CRC, 2003
    locator: Chapter 6, Chebyshev interpolation (interpolation at the zeros and extrema, and the Lebesgue constants)
  - paper: "Jean-Paul Berrut and Lloyd N. Trefethen, Barycentric Lagrange interpolation, SIAM Review 46(3), 501-517, 2004, doi:10.1137/S0036144502417715"
    locator: Section 5, the explicit barycentric weights for Chebyshev points of the first and second kinds
---

Chebyshev nodes are the points on $[-1, 1]$ obtained by projecting equally spaced points on the upper half of the unit circle down to the real axis. They come in two families: the zeros of the [Chebyshev polynomial](/chebyshev-polynomials/) $T_{n+1}$ (first kind) and the extrema of $T_n$ (second kind). Both cluster near $\pm 1$ with the density $1/(\pi\sqrt{1 - x^2})$. Interpolation at these points is nearly optimal. The Lebesgue constant grows only like $\tfrac{2}{\pi}\log n$, while at equally spaced points it grows like $2^n$, so the [Runge phenomenon](/runge-phenomenon/) does not occur.

## In plain words

If you fit a polynomial through many evenly spaced points, the curve can swing wildly near the ends of the interval, even when the function is smooth. Moving the points closer together near the ends fixes this.

Chebyshev nodes do this in a natural way. Draw a half circle over the interval, mark points at equal angles along it, and drop each one straight down. The dropped points are close together near the ends and spread out in the middle. Through such points a polynomial follows a smooth function closely, and the fit improves steadily as you add points. They are also easy to compute, and the formula for the curve through them is very simple.

## The idea

Notation on the interpolation and approximation pages: $f$ is a function on $[-1, 1]$; the nodes are $x_0, \ldots, x_n$ with data $y_i = f(x_i)$; $p_n$ is the interpolating polynomial of degree at most $n$; $\omega(x) = \prod_{i=0}^{n} (x - x_i)$ is the node polynomial; $\Lambda_n$ is the [Lebesgue constant](/lebesgue-constant/); $E_n(f)$ is the best approximation error; $T_k$ are the [Chebyshev polynomials](/chebyshev-polynomials/).

**The two families.** For $n + 1$ nodes:

- *First kind* (Chebyshev zeros, Chebyshev-Gauss points): $x_j = \cos\big((2j + 1)\pi / (2n + 2)\big)$, $j = 0, \ldots, n$, the zeros of $T_{n+1}$. All lie in the open interval.
- *Second kind* (Chebyshev extreme points, Chebyshev-Gauss-Lobatto points): $x_j = \cos(j\pi/n)$, $j = 0, \ldots, n$, the extrema of $T_n$, including $\pm 1$. They are nested: the points for $n$ are among those for $2n$.

Both are listed in decreasing order by these formulas. On $[a, b]$ map them by $x \mapsto \tfrac{a + b}{2} + \tfrac{b - a}{2} x$.

**Why they work: the node polynomial.** The [interpolation error theorem](/polynomial-interpolation-error-theorem/) says that for $f \in C^{n+1}[-1, 1]$ and $x \in [-1, 1]$,
$$f(x) - p_n(x) = \frac{f^{(n+1)}(\xi_x)}{(n+1)!}\, \omega(x)$$
for some $\xi_x \in (-1, 1)$. At the first-kind points, $\omega = 2^{-n} T_{n+1}$, so $\|\omega\|_\infty = 2^{-n}$, and by the minimax property of $T_{n+1}$ no other set of $n + 1$ nodes has a smaller $\|\omega\|_\infty$. This gives the proved bound
$$\|f - p_n\|_\infty \le \frac{\|f^{(n+1)}\|_\infty}{2^n (n+1)!}.$$
At the second-kind points, $\omega(x) = 2^{1-n}(x^2 - 1) U_{n-1}(x)$, since $U_{n-1}$ has leading coefficient $2^{n-1}$; with $x = \cos t$ this is $-2^{1-n} \sin t \sin(nt)$, so $\|\omega\|_\infty \le 2^{1-n}$.

**Why they work: the Lebesgue constant.** A bound through $f^{(n+1)}$ is useless for functions that are only a few times differentiable. The robust measure is the Lebesgue constant $\Lambda_n = \max_x \sum_j |\ell_j(x)|$, which gives $\|f - p_n\|_\infty \le (1 + \Lambda_n) E_n(f)$ for every continuous $f$. These bounds are proved (Trefethen, Theorem 15.2):

- for the second-kind points, $\Lambda_n \le \tfrac{2}{\pi} \log(n + 1) + 1$;
- for any set of $n + 1$ nodes, $\Lambda_n \ge \tfrac{2}{\pi} \log(n + 1) + 0.52125$;
- for equispaced points, $\Lambda_n > 2^{n-2}/n^2$, and asymptotically $\Lambda_n \sim 2^{n+1}/(e\, n \log n)$.

So Chebyshev points are within an additive constant of the best possible, and the first-kind points behave in the same way. With the bound on $E_n(f)$ from [Jackson's theorem](/jackson-theorem/), interpolation at Chebyshev points converges for every Lipschitz continuous $f$, at the rate $O(n^{-k})$ when $f^{(k-1)}$ is absolutely continuous and $f^{(k)}$ has bounded variation, and geometrically for analytic $f$ (Trefethen, Theorems 7.2 and 8.2).

**Why they work: potential theory.** As $n \to \infty$, both families are distributed with the arcsine density $1/(\pi\sqrt{1 - x^2})$, the equilibrium distribution of electric charge on $[-1, 1]$. For any node family with this limit density, $\|\omega\|_\infty^{1/n} \to 1/2$, the capacity of the interval and the smallest possible limit, and $|\omega|$ is of about the same size all across the interval. Equispaced points have the uniform density, and $|\omega|^{1/n}$ is much larger near the ends than in the middle (Trefethen, Chapter 12). Near $\pm 1$ the spacing of Chebyshev points is about $\pi^2/(2n^2)$, against $\pi/n$ at the center.

**Simple barycentric weights.** For the [barycentric formula](/barycentric-interpolation/)
$$p_n(x) = \frac{\sum_j w_j y_j/(x - x_j)}{\sum_j w_j/(x - x_j)},$$
the weights can be scaled to $w_j = (-1)^j \sin\big((2j + 1)\pi/(2n + 2)\big)$ for the first kind, and to $w_j = (-1)^j \delta_j$ with $\delta_0 = \delta_n = \tfrac{1}{2}$ and $\delta_j = 1$ otherwise for the second kind (Berrut and Trefethen 2004, Section 5). So evaluation costs $O(n)$ operations per point with no setup, and the formula is stable in floating point because $\Lambda_n$ is small.

**Computing the points.** In floating point, $\cos(j\pi/n)$ for $j$ near $n/2$ does not give exactly 0 or exactly symmetric values. The equivalent form $x_j = \sin\big(\pi(n - 2j)/(2n)\big)$ is exactly antisymmetric and gives $x_{n/2} = 0$. Either form has an absolute error of a few units of $10^{-16}$, harmless for interpolation.

**What they do not do.** They do not minimize the interpolation error for a given $f$, and they do not minimize $\Lambda_n$ exactly. The nodes that minimize $\Lambda_n$ were characterized by Kilgore and by de Boor and Pinkus in 1978 (the Bernstein and Erdős conjecture); they improve on the Chebyshev points only in the additive constant. The best approximation $p^*$ is in general not an interpolant at Chebyshev points either, but the factor is small: at the second-kind points $\Lambda_n < 4$ for $n \le 100$, so $1 + \Lambda_n < 5$.

## Examples

**Five points.** For $n = 4$, the second-kind points are $1, \tfrac{\sqrt{2}}{2}, 0, -\tfrac{\sqrt{2}}{2}, -1$, and the first-kind points are $\cos(\pi/10), \cos(3\pi/10), 0, -\cos(3\pi/10), -\cos(\pi/10) \approx \pm 0.9511, \pm 0.5878, 0$.

**Node polynomial size.** Measured by sampling on a fine grid:

| $n$ | equispaced $\|\omega\|_\infty$ | first kind $\|\omega\|_\infty$ | second kind $\|\omega\|_\infty$ |
|---|---|---|---|
| 5 | $6.9 \times 10^{-2}$ | $3.13 \times 10^{-2} = 2^{-5}$ | $6.25 \times 10^{-2} = 2^{-4}$ |
| 10 | $8.5 \times 10^{-3}$ | $9.77 \times 10^{-4} = 2^{-10}$ | $1.93 \times 10^{-3}$ |
| 20 | $2.3 \times 10^{-4}$ | $9.54 \times 10^{-7} = 2^{-20}$ | $1.90 \times 10^{-6}$ |

The ratio of the equispaced to the first-kind value is about 9 at $n = 10$ and about 245 at $n = 20$, and it grows exponentially.

**Lebesgue constants.** Measured by sampling on a fine grid:

| $n$ | 5 | 10 | 20 |
|---|---|---|---|
| equispaced | 3.11 | 29.9 | 10987 |
| first kind | 2.10 | 2.49 | 2.90 |
| second kind | 1.99 | 2.42 | 2.87 |

**The Runge function.** For $f(x) = 1/(1 + 25 x^2)$, the maximum interpolation error on a fine grid is:

| $n$ | equispaced | first kind | second kind |
|---|---|---|---|
| 10 | 1.92 | 0.109 | 0.132 |
| 20 | 59.8 | 0.0153 | 0.0177 |
| 40 | (diverges) | | $3.4 \times 10^{-4}$ |
| 80 | | | $1.2 \times 10^{-7}$ |

The Chebyshev errors fall like $\rho^{-n}$ with $\rho = (1 + \sqrt{26})/5 \approx 1.22$, set by the poles at $\pm i/5$; the equispaced errors grow without bound.

## Where it is used

- [Chebyshev interpolation](/chebyshev-interpolation/) and the Chebfun system: functions are represented by their values at second-kind points, and coefficients come from the [discrete cosine transform](/discrete-cosine-transform/).
- [Clenshaw-Curtis quadrature](/clenshaw-curtis-quadrature/) uses second-kind points and [Fejér quadrature](/fejer-quadrature/) uses first-kind points.
- Spectral collocation methods for differential equations, where the clustering at the ends resolves boundary layers.
- Starting references for the [Remez algorithm](/remez-algorithm/), and nodes for near-minimax approximation in math libraries.
- [Chebyshev economization](/chebyshev-economization/) and the [Chebyshev iteration](/chebyshev-iteration/) use the same polynomials and their zeros.

## References
