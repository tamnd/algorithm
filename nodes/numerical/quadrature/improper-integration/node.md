---
tag: 2PC2NH
kind: problem
slug: improper-integration
name: Improper integration
aliases:
- infinite-interval integration
- singular integrals
- improper integral
- integration with endpoint singularities
area: numerical/quadrature
level: core
summary: Compute an integral over an infinite interval, or of a function that is unbounded near an endpoint, from values of the function. Transform it to a smooth one, or use a rule built for the singularity.
prereqs: [quadrature-rule, composite-quadrature]
see_also: [tanh-sinh-quadrature, gauss-jacobi-quadrature, gauss-laguerre-quadrature, gauss-hermite-quadrature, adaptive-quadrature, sinc-quadrature, product-quadrature, oscillatory-integration]
sources:
  - book: isbn:9780122063602
    title: Philip J. Davis and Philip Rabinowitz, Methods of Numerical Integration, second edition, Academic Press, 1984
    locator: Chapter 2 (the sections on improper integrands over a finite interval) and Chapter 3, Approximate integration over infinite intervals
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Chapter 5, Section 5.6, Singular integrals (change of variables, Gaussian quadrature with a weight, and the truncation of infinite intervals)
  - paper: doi:10.2977/prims/1195192451
    title: "Hidetosi Takahasi and Masatake Mori, Double exponential formulas for numerical integration, Publications of the Research Institute for Mathematical Sciences, Kyoto University 9(3) (1974) 721-741"
    locator: the tanh-sinh transformation and its rate for integrands with endpoint singularities
  - paper: doi:10.1137/130932132
    title: "Lloyd N. Trefethen and J. A. C. Weideman, The exponentially convergent trapezoidal rule, SIAM Review 56(3) (2014) 385-458"
    locator: the sections on the trapezoidal rule over the real line and on double exponential and other changes of variables
  - book: isbn:9783540125532
    title: Robert Piessens, Elise de Doncker-Kapenga, Christoph W. Überhuber and David K. Kahaner, QUADPACK, A Subroutine Package for Automatic Integration, Springer, 1983
    locator: the routines QAGS (adaptive with epsilon extrapolation for endpoint singularities), QAGI (infinite intervals by the map x = a + (1 - t)/t) and QAWS (algebraic and logarithmic endpoint weights)
  - paper: "Masaaki Sugihara, Optimality of the double exponential formula, functional analysis approach, Numerische Mathematik 75(3) (1997) 379-395"
    locator: the optimality of double exponential transformations in spaces of analytic functions
---

Improper integration is the problem of computing an integral whose interval is infinite, or whose integrand is unbounded near an endpoint, from values of the integrand at points that the algorithm chooses. A plain rule such as the [composite trapezoidal rule](/composite-quadrature/) fails on such integrals: it cannot cover an infinite interval, it cannot evaluate $f$ at a singular endpoint, and near a singularity its rate collapses. The standard cures are a change of variables that makes the integrand smooth, a [Gaussian rule](/gaussian-quadrature/) whose weight function holds the singular or decaying factor, and the double exponential ([tanh-sinh](/tanh-sinh-quadrature/)) transformation, which handles both cases at once.

## In plain words

Some areas under a curve are finite even though the curve goes up to infinity at one end, or the region goes on forever to the right. The usual recipe, cut the interval into equal pieces and add up small trapezoids, breaks down here. You cannot cut an infinite interval into finitely many equal pieces. At an end where the curve goes to infinity, you cannot even compute the height. Near such an end, the trapezoids fit badly, so adding more pieces helps very little. The fixes rewrite the problem. One fix stretches the variable so that the infinite curve becomes a tame one. Another builds the bad part of the curve into the formula itself, so that only the tame part is sampled.

## Definition

**Notation.** As on all quadrature pages: $I(f) = \int_a^b f(x)\,w(x)\,dx$ (with $w = 1$ unless stated), a rule $Q_n(f) = \sum_{i=1}^n w_i f(x_i)$ with $n$ nodes, the error $E_n(f) = I(f) - Q_n(f)$, and the tolerance $\tau$.

Let $-\infty \le a < b \le \infty$ and let $f$ be continuous on the open interval $(a, b)$. The integral is **improper** if $a = -\infty$, or $b = \infty$, or $f$ is unbounded near $a$ or near $b$. It is defined as a limit,

$$\int_a^b f(x)\,dx = \lim_{\alpha \downarrow a,\ \beta \uparrow b} \int_\alpha^\beta f(x)\,dx,$$

when the limit exists and is finite, with $\alpha$ and $\beta$ moving independently. It **converges absolutely** if $\int_a^b |f| < \infty$. An unbounded point inside $(a, b)$ is reduced to two endpoint cases by splitting the interval there.

**The computational problem.** The input is an oracle that returns $f(x)$ for each $x$ in the open interval $(a, b)$, the endpoints $a, b$, and a tolerance $\tau > 0$; often also a description of the behaviour at the ends, such as $f(x) = (x - a)^\alpha g(x)$ with known $\alpha > -1$ and smooth $g$, or $f(x) = e^{-x} g(x)$. The output is a number $\hat I$ with $|\hat I - I(f)| \le \tau$, or an estimate $\hat E$ of the error. The cost is the number of evaluations of $f$.

## Variants

- **Infinite interval.** $[a, \infty)$ or $(-\infty, \infty)$ with $f$ decaying: exponentially ($e^{-x}$, $e^{-x^2}$) or only algebraically ($1/(1 + x^2)$).
- **Algebraic endpoint singularity.** $f(x) = (x - a)^\alpha g(x)$ with $-1 < \alpha < 0$ (unbounded) or $\alpha > 0$ not an integer (bounded, but with an unbounded derivative, such as $\sqrt{x}$).
- **Logarithmic endpoint singularity.** $f(x) = \log(x - a)\, g(x)$.
- **Known weight.** $I(f) = \int_a^b g(x) w(x)\,dx$ with a singular or decaying weight $w$ given in closed form and a smooth $g$. This is the setting of [Gauss-Jacobi](/gauss-jacobi-quadrature/), [Gauss-Laguerre](/gauss-laguerre-quadrature/) and [Gauss-Hermite](/gauss-hermite-quadrature/) rules and of [product quadrature](/product-quadrature/).
- **Conditionally convergent.** $\int_0^\infty \frac{\sin x}{x}\,dx = \frac{\pi}{2}$ converges, but not absolutely. Truncating at $L$ leaves an error of order $1/L$ that oscillates in sign; see [oscillatory integration](/oscillatory-integration/).
- **Cauchy principal value.** $\mathrm{PV}\int_{-1}^1 \frac{g(x)}{x}\,dx$ with a non-integrable singularity inside, defined by a symmetric limit. It needs its own methods and is not covered here.

## Examples

Each line gives the exact value and what some methods do. The errors are $I - \hat I$.

- $\int_0^1 x^{-1/2}\,dx = 2$. The composite midpoint rule never evaluates $f(0)$, but with $m = 4, 16, 64, 256, 1024$ panels its errors are $0.301$, $0.151$, $0.0756$, $0.0378$, $0.0189$: the rate is $h^{1/2}$, so 10 correct digits would need about $10^{20}$ panels. The tanh-sinh rule with step $h = 1, 0.5, 0.25$ and $9$, $19$, $37$ nodes has errors $-4.5 \times 10^{-3}$, $-4.6 \times 10^{-7}$, $-3.1 \times 10^{-15}$.
- $\int_0^1 \log x\,dx = -1$. The composite midpoint errors for $m = 4, 16, 64, 256, 1024$ are $-8.4 \times 10^{-2}$, $-2.2 \times 10^{-2}$, $-5.4 \times 10^{-3}$, $-1.4 \times 10^{-3}$, $-3.4 \times 10^{-4}$: rate $h$.
- $\int_0^1 x^{-1/2}\cos x\,dx = 1.8090484758\ldots$. The substitution $x = t^2$ gives $2\int_0^1 \cos(t^2)\,dt$, with an entire integrand. [Gauss-Legendre](/gauss-legendre-quadrature/) with $n = 2, 4, 8$ nodes then has errors $-2.7 \times 10^{-3}$, $-4.9 \times 10^{-7}$, $-4.4 \times 10^{-14}$. The same rules on the original integrand have errors $0.349$, $0.194$, $0.103$, and halving the error needs twice the nodes.
- $\int_0^\infty \frac{dx}{1 + x^2} = \frac{\pi}{2}$. Truncation at $L$ loses $\frac{\pi}{2} - \arctan L \approx 1/L$, which is $0.0997$, $0.0100$, $0.0010$ for $L = 10, 100, 1000$. The map $x = t/(1 - t)$ gives $\int_0^1 \frac{dt}{(1-t)^2 + t^2}$, analytic on $[0, 1]$, and Gauss-Legendre with $n = 4, 8, 16, 32$ has errors $2.2 \times 10^{-3}$, $1.9 \times 10^{-6}$, $1.5 \times 10^{-12}$, $-6.7 \times 10^{-16}$.
- $\int_{-\infty}^\infty e^{-x^2}\,dx = \sqrt{\pi}$. The [trapezoidal rule](/trapezoidal-rule/) $h\sum_{k} e^{-(kh)^2}$, cut at $|kh| \le 6$, has errors $-1.8 \times 10^{-4}$, $-8.5 \times 10^{-8}$, $-2.2 \times 10^{-16}$ for $h = 1, 0.75, 0.5$ with 13, 17 and 25 nodes. The error of the untruncated sum is about $2\sqrt{\pi}\,e^{-\pi^2/h^2}$ (Trefethen and Weideman 2014).
- $\int_0^\infty x^{1/2} e^{-x}\,dx = \Gamma(3/2) = \sqrt{\pi}/2$. Gauss-Laguerre with weight $e^{-x}$ samples $g(x) = \sqrt{x}$, which is not smooth at $0$, so it converges slowly. Generalized Gauss-Laguerre with weight $x^{1/2}e^{-x}$ and $g = 1$ is exact with one node.

## Known algorithms

- **Change of variables, then a standard rule.** $x = a + t^2$ removes $(x - a)^{-1/2}$; $x = a + t^q$ removes $(x - a)^{p/q - 1}$; $x = a + (1 - t)/t$ or $x = a + t/(1 - t)$ maps $[a, \infty)$ to a finite interval. Afterwards use [Gauss-Legendre](/gauss-legendre-quadrature/), [Clenshaw-Curtis](/clenshaw-curtis-quadrature/) or an [adaptive](/adaptive-quadrature/) rule. Cost: the evaluations of the chosen rule.
- **Gaussian rules with the singular weight.** [Gauss-Jacobi](/gauss-jacobi-quadrature/) for $(1 - x)^\alpha (1 + x)^\beta$, [Gauss-Laguerre](/gauss-laguerre-quadrature/) for $x^\alpha e^{-x}$, [Gauss-Hermite](/gauss-hermite-quadrature/) for $e^{-x^2}$. Geometric convergence when the remaining factor $g$ is analytic; $O(n^2)$ work for the nodes and weights by the [Golub-Welsch algorithm](/golub-welsch-algorithm/), or $O(n)$ by asymptotic methods.
- **[Tanh-sinh quadrature](/tanh-sinh-quadrature/)** (Takahasi and Mori 1974). The substitution $x = \tanh(\tfrac{\pi}{2}\sinh t)$ maps $(-1, 1)$ to the real line and makes the new integrand decay double exponentially; the trapezoidal rule in $t$ then converges at a rate of about $\exp(-c\,n/\log n)$ for integrands analytic inside the interval, even with algebraic endpoint singularities. Variants $x = e^{\pi \sinh t/2}$ and $x = \exp(t - e^{-t})$ handle $[0, \infty)$.
- **[Sinc quadrature](/sinc-quadrature/)** with single exponential maps, rate about $\exp(-c\sqrt{n})$.
- **Adaptive with extrapolation.** QUADPACK's QAGS refines the panels next to the singular end and accelerates the sequence of results with Wynn's epsilon algorithm; QAGI first maps $[a, \infty)$ to $(0, 1]$ by $x = a + (1 - t)/t$.
- **Truncation.** Replace $\int_a^\infty$ by $\int_a^L$ with a tail bound $\int_L^\infty |f| \le \tau/2$, then integrate the proper integral to $\tau/2$. This works only when a tail bound is known.
- **Singularity subtraction.** Write $f = (f - s) + s$, where $s$ has the same singular behaviour and a known integral, and integrate the smoother $f - s$ numerically.

## Bounds

**No guarantee from samples alone.** Let $\mathcal{F}$ be the set of continuous functions on $(a, b)$ with a convergent integral. No algorithm that uses finitely many values of $f$ can return $\hat I$ with $|\hat I - I(f)| \le \tau$ for each $f \in \mathcal{F}$. *Proof.* Run the algorithm on $f_0 = 0$; it evaluates $f$ at some points $x_1, \ldots, x_k$ (possibly chosen adaptively) and returns some $\hat I$. Let $\phi \ge 0$ be a continuous bump with support in an interval of $(a, b)$ that contains none of the $x_j$, scaled so that $\int \phi = 3\tau$. The algorithm sees the same values on $f_1 = \phi$ as on $f_0$, so it makes the same choices and returns the same $\hat I$. Since $I(f_1) - I(f_0) = 3\tau$, the error is more than $\tau$ for $f_0$ or for $f_1$. $\square$ The same argument works for proper integrals; it shows that every guarantee needs a class of functions, such as bounds on derivatives or analyticity in a known region.

**Rates under hypotheses.**

- If $f = w g$ with a Gauss weight $w$ and $g$ analytic in the Bernstein ellipse $E_\rho$ of the (finite) interval and bounded by $M$ there, the $n$-node Gaussian rule for $w$ has error $O(M\rho^{-2n})$ (see the [Gauss quadrature theorem](/gauss-quadrature-theorem/) and [Gauss-Legendre quadrature](/gauss-legendre-quadrature/)). For Laguerre and Hermite weights on infinite intervals the convergence is slower, subgeometric in general.
- For $f = (x - a)^\alpha g$ with $g$ smooth and $-1 < \alpha < 0$, a composite rule of any fixed degree on a uniform mesh has error of order $h^{1 + \alpha}$, as in the example $x^{-1/2}$ (rate $h^{1/2}$). Geometrically graded meshes, as built by [adaptive quadrature](/adaptive-quadrature/), restore an algebraic rate in the number of evaluations.
- For the trapezoidal rule on $(-\infty, \infty)$ with $f$ analytic in the strip $|\operatorname{Im} x| < a$ and integrable along its lines, the error of the infinite sum is $O(e^{-2\pi a/h})$ (Trefethen and Weideman 2014). Tanh-sinh inherits from this its rate of about $\exp(-c\,n/\log n)$; Sugihara (1997) showed that double exponential transformations are optimal in a precise sense for certain classes of analytic functions.

**Floating point.** Near a singular endpoint, the nodes of a transformed rule crowd toward $a$. If $a \ne 0$, a node $a + \delta$ with $\delta$ below $u|a|$ rounds to $a$, and $f(a)$ is infinite. Store the distance to the nearest endpoint, $\delta$, and evaluate $f$ in a form that uses it, for example $g(\delta) = f(a + \delta)$ with $\delta$ computed directly from the transformation. The weights of tanh-sinh decay double exponentially, so the sum must stop once the terms underflow, not when $f$ overflows.

## Reductions

- **To a proper integral.** A substitution $x = \phi(t)$ with $\phi$ smooth and monotone gives $\int_a^b f = \int_c^d f(\phi(t))\phi'(t)\,dt$. It costs nothing in evaluations; it helps when the new integrand is smooth. For $f = (x - a)^{-1/2} g(x)$, the choice $x = a + t^2$ gives $2 g(a + t^2)$, which is as smooth as $g$.
- **To a weighted Gaussian rule.** Factor out the singular part as a weight: $\int_0^1 x^\alpha g(x)\,dx$ is a Gauss-Jacobi integral for $g$ after the map $x = (1 + y)/2$.
- **Interior singularities to endpoint ones.** Split at the known singular point $c$: $\int_a^b = \int_a^c + \int_c^b$.

## Applications

- Expected values under the normal distribution, $\int_{-\infty}^\infty g(x)e^{-x^2/2}\,dx$, in statistics and uncertainty quantification: Gauss-Hermite.
- Laplace transforms and the Gamma function, $\int_0^\infty x^{s-1}e^{-x}\,dx$: Gauss-Laguerre.
- Boundary element methods, with logarithmic and $1/r$ kernels at the endpoints of panels: product rules and changes of variables.
- Fourier integrals over $[0, \infty)$ in signal processing: [oscillatory integration](/oscillatory-integration/) combined with the map of the infinite interval.

## References
