---
tag: 0NME45
kind: concept
slug: runge-phenomenon
name: Runge phenomenon
aliases:
- Runge's phenomenon
area: numerical/interpolation-and-approximation
level: intro
summary: Polynomial interpolants at equispaced nodes can diverge near the ends of the interval as the degree grows, even for an analytic function. Chebyshev nodes remove the effect.
prereqs: [polynomial-interpolation, lebesgue-constant]
see_also: [chebyshev-nodes, chebyshev-interpolation, polynomial-interpolation-error-theorem, cubic-spline-interpolation, least-squares-approximation, gibbs-phenomenon]
sources:
  - paper: "Carl Runge, Über empirische Funktionen und die Interpolation zwischen äquidistanten Ordinaten, Zeitschrift für Mathematik und Physik 46 (1901) 224-243"
    locator: the example 1/(1 + x^2) on [-5, 5] and the curve that bounds the region of convergence
  - book: isbn:9781611975932
    title: Lloyd N. Trefethen, Approximation Theory and Approximation Practice, extended edition, SIAM, 2019
    locator: Chapter 11, Hermite integral formula; Chapter 12, Potential theory and approximation; Chapter 13, Equispaced points, Runge phenomenon; Chapter 15, Lebesgue constants
  - book: isbn:9780387953663
    title: Carl de Boor, A Practical Guide to Splines, revised edition, Springer, 2001
    locator: Chapter II, Limitations of polynomial approximation (the Runge example)
  - book: isbn:9780486624952
    title: Philip J. Davis, Interpolation and Approximation, Dover, 1975 (first published 1963)
    locator: Chapter IV, Convergence theorems for interpolatory processes (equidistant interpolation and the Runge example)
  - paper: "Rodrigo B. Platte, Lloyd N. Trefethen and Arno B. J. Kuijlaars, Impossibility of fast stable approximation of analytic functions from equispaced samples, SIAM Review 53(2) (2011) 308-318"
    locator: the theorem that a stable method from equispaced data converges at best at a root-exponential rate
  - paper: "Georg Faber, Über die interpolatorische Darstellung stetiger Funktionen, Jahresbericht der Deutschen Mathematiker-Vereinigung 23 (1914) 192-210"
    locator: the theorem that for every triangular array of nodes some continuous function has divergent interpolants
---

The Runge phenomenon is the divergence of [polynomial interpolation](/polynomial-interpolation/) at equispaced nodes near the ends of the interval as the degree grows. Runge (1901) showed it for $f(x) = 1/(1 + x^2)$ on $[-5, 5]$, a function that is analytic on the whole real line. The cause is a property of the nodes, measured by the node polynomial $\omega$ and by the [Lebesgue constant](/lebesgue-constant/) $\Lambda_n$, which grows like $2^n$ for equispaced nodes. [Chebyshev nodes](/chebyshev-nodes/) remove the effect.

## In plain words

Draw a smooth bell-shaped curve and mark evenly spaced points on it. Now find the polynomial that passes through all of them. With few points it looks fine. With more points the polynomial still hits every mark, but between the marks near the two ends it swings up and down, and the swings get larger each time you add points.

The curve is not to blame: it is smooth everywhere. The trouble comes from the even spacing, which leaves the ends of the interval with too little control over a high-degree polynomial. If you put the points closer together near the ends, in a specific pattern named after Chebyshev, the swings disappear and the polynomial gets better with every point you add. Rounding errors in a computer make the even spacing worse still.

## The idea

Notation on the interpolation pages: $f$ is a function on $[-1, 1]$, the nodes $x_0 < \cdots < x_n$ are equispaced, $x_j = -1 + 2j/n$, $p_n$ is the interpolant of degree at most $n$, and $\omega(x) = \prod_j (x - x_j)$.

**What the error formula says.** If $f \in C^{n+1}[-1, 1]$, the [interpolation error theorem](/polynomial-interpolation-error-theorem/) gives $f(x) - p_n(x) = f^{(n+1)}(\xi)\, \omega(x)/(n+1)!$. For equispaced nodes $|\omega(x)|$ is much larger near $\pm 1$ than near 0: its value at the midpoint between the first two nodes is about $2^n$ times its value at the center, up to factors polynomial in $n$. For Runge's function $f(x) = 1/(1 + 25x^2)$, the derivatives grow like $(n+1)!\, 5^{n+1}$, so the bound cannot decide whether $p_n$ converges. A finer tool is needed.

**Potential theory.** For $f$ analytic inside a contour $\Gamma$ that encloses the nodes and $x$, the Hermite integral formula gives
$$f(x) - p_n(x) = \frac{1}{2\pi i} \oint_\Gamma \frac{\omega(x)}{\omega(z)} \frac{f(z)}{z - x}\, dz.$$
As $n \to \infty$, $|\omega(z)|^{1/n} \to e^{-u(z)}$ with the logarithmic potential of the uniform distribution on $[-1, 1]$,
$$u(z) = -\frac{1}{2} \int_{-1}^{1} \log|z - t|\, dt = 1 - \operatorname{Re} \frac{(z + 1)\log(z + 1) - (z - 1)\log(z - 1)}{2}.$$
So the error at $x$ behaves like $\exp\!\big(n\,(u(z^*) - u(x))\big)$, where $z^*$ is the singularity of $f$ with the largest $u$ (the closest in the sense of the potential). The interpolants converge at $x$ when $u(x) > u(z^*)$ and diverge when $u(x) < u(z^*)$ (Trefethen, Chapters 11 to 13; the proof makes the heuristic rigorous). For Runge's function the poles are at $\pm i/5$, with $u(i/5) \approx 0.7057$, and the level curve $u = u(i/5)$ crosses the real axis at $\pm 0.72668$. So $p_n(x) \to f(x)$ for $|x| < 0.72668$ and $|p_n(x) - f(x)| \to \infty$ for $0.72668 < |x| \le 1$, apart from the nodes.

**The Runge region.** The same argument shows that equispaced interpolants converge uniformly on $[-1, 1]$ if $f$ is analytic in the closed region bounded by the level curve of $u$ through $\pm 1$. That curve crosses the imaginary axis at $\pm 0.52552i$. A function with a singularity inside this region, however mild, makes equispaced interpolation diverge somewhere in $[-1, 1]$.

**Rounding errors.** Even an entire function such as $e^x$ suffers in floating point. The Lebesgue constant of equispaced nodes satisfies $\Lambda_n \sim 2^{n+1}/(e\, n \log n)$, and a data error of size $u \approx 1.1 \times 10^{-16}$ can be magnified by $\Lambda_n$. Once $\Lambda_n u$ exceeds the truncation error, the computed interpolant gets worse with $n$, whatever the formula used to evaluate it.

**Why Chebyshev nodes cure it.** For the Chebyshev points $x_j = \cos(j\pi/n)$, the limit distribution has density $1/(\pi\sqrt{1 - x^2})$, its potential is constant on $[-1, 1]$, and $\Lambda_n \le \tfrac{2}{\pi}\log(n + 1) + 1$. Then $p_n \to f$ for every Lipschitz $f$, and geometrically fast for analytic $f$ (see [Chebyshev interpolation](/chebyshev-interpolation/)).

**Not a property of all interpolation.** For every triangular array of nodes, Faber's theorem (1914) gives a continuous $f$ whose interpolants do not converge uniformly, because $\Lambda_n \to \infty$ always. The Runge phenomenon is the stronger and practical statement that equispaced nodes fail for smooth, even analytic, functions.

## Examples

**Runge's function.** For $f(x) = 1/(1 + 25x^2)$ the maximum error on $[-1, 1]$ of the equispaced interpolant is $0.433$, $1.92$, $59.8$ and $1.05 \times 10^5$ for $n = 5, 10, 20, 40$; at Chebyshev points of the first kind it is $0.556$, $0.109$, $0.0153$ and $2.90 \times 10^{-4}$. In exact rational arithmetic, so that no rounding is involved, the pointwise error $|f(x) - p_n(x)|$ at equispaced nodes is:

| $n$ | $x = 0.01$ | $x = 0.71$ | $x = 0.76$ | $x = 0.91$ |
|---|---|---|---|---|
| 20 | $8.4 \times 10^{-5}$ | $8.4 \times 10^{-2}$ | 0.58 | 4.2 |
| 40 | $4.5 \times 10^{-7}$ | 0.12 | 0.67 | $5.7 \times 10^{2}$ |
| 60 | $1.7 \times 10^{-9}$ | 0.12 | 1.3 | $5.8 \times 10^{4}$ |
| 80 | $5.6 \times 10^{-12}$ | 0.10 | 3.9 | $5.0 \times 10^{6}$ |

At $x = 0.01$ the error falls fast; at $x = 0.71$, just inside the boundary $0.72668$, it barely moves; at $0.76$ and $0.91$, outside it, it grows, and faster the farther out the point lies.

**An entire function in floating point.** For $f(x) = e^x$, which has no singularity, the equispaced interpolant evaluated by the barycentric formula in double precision has maximum error $2.4 \times 10^{-10}$ for $n = 10$ and $8.4 \times 10^{-13}$ for $n = 20$, then $5.0 \times 10^{-7}$ for $n = 40$, $0.11$ for $n = 60$ and $1.3 \times 10^2$ for $n = 80$. In exact arithmetic these interpolants converge; the growth is rounding error magnified by $\Lambda_n$, which is about $4.7 \times 10^9$ for $n = 40$.

**Non-example: splines.** A [cubic spline](/cubic-spline-interpolation/) through the same equispaced data of Runge's function converges as $O(h^4)$ with complete or not-a-knot end conditions, because each piece depends mainly on nearby data. The phenomenon belongs to global polynomials of high degree at bad nodes, not to equispaced data as such.

## Where it is used

- **Choosing nodes.** The phenomenon is the reason that [Chebyshev nodes](/chebyshev-nodes/) and [Chebyshev interpolation](/chebyshev-interpolation/) are the default for high-degree polynomial approximation, and that [spectral methods](/spectral-methods/) use Chebyshev grids.
- **Quadrature.** [Newton-Cotes formulas](/newton-cotes-formulas/) integrate the equispaced interpolant; their weights become large and of both signs for high orders, so composite rules of low order or [Clenshaw-Curtis quadrature](/clenshaw-curtis-quadrature/) are used instead.
- **Equispaced data that cannot be moved.** When the samples are given on a uniform grid, the remedies are piecewise polynomials ([splines](/cubic-spline-interpolation/)), [least squares](/least-squares-approximation/) fits of degree about $\sqrt{n}$, and rational interpolants. Platte, Trefethen and Kuijlaars (2011) proved that no stable method can converge exponentially from equispaced samples of every analytic function; root-exponential convergence $\exp(-c\sqrt{n})$ is the best possible.
- **Teaching.** It is the standard warning against reading the error theorem as "more points always help".

## References
