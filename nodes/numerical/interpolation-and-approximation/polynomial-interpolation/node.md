---
tag: GJDDBB
kind: problem
slug: polynomial-interpolation
name: Polynomial interpolation
aliases:
- Lagrange interpolation
- Polynomial fitting through points
- interpolating polynomial
area: numerical/interpolation-and-approximation
level: intro
summary: Given values at n + 1 distinct nodes, find the unique polynomial of degree at most n that takes them, as coefficients in a basis or as values at new points.
model: real-ram
complexity:
  vars: {n: "the degree bound, with n + 1 nodes"}
  time: {worst: O(n^2)}
prereqs: [interpolation-problem, polynomial]
see_also: [lagrange-interpolation, barycentric-interpolation, newton-interpolation, interpolating-polynomial-uniqueness, polynomial-interpolation-error-theorem, lebesgue-constant, runge-phenomenon, chebyshev-interpolation]
sources:
  - book: isbn:9781611975932
    title: Lloyd N. Trefethen, Approximation Theory and Approximation Practice, extended edition, SIAM, 2019
    locator: Chapter 5 (barycentric interpolation formula), Chapter 13 (equispaced points, Runge phenomenon) and Chapter 15 (Lebesgue constants)
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 6, Polynomial interpolation (existence, uniqueness and the error theorem)
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Section 3.1, Polynomial interpolation theory, and Section 3.2, Newton divided differences
  - book: isbn:9780521295147
    title: M. J. D. Powell, Approximation Theory and Methods, Cambridge University Press, 1981
    locator: Chapter 4, Polynomial interpolation, and Chapter 5, Divided differences
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 22, Vandermonde systems
  - paper: "V. Strassen, Die Berechnungskomplexität von elementarsymmetrischen Funktionen und von Interpolationskoeffizienten, Numerische Mathematik 20 (1973) 238-251"
    locator: the lower bound of order n log n on the number of nonscalar multiplications for the interpolation coefficients
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Chapter 10, Fast polynomial evaluation and interpolation
  - paper: doi:10.1093/imanum/24.4.547
    title: "Nicholas J. Higham, The numerical stability of barycentric Lagrange interpolation, IMA Journal of Numerical Analysis 24(4) (2004) 547-556"
    locator: the stability results for the two barycentric forms
  - paper: "Walter Gautschi and Gabriele Inglese, Lower bounds for the condition number of Vandermonde matrices, Numerische Mathematik 52 (1988) 241-250"
    locator: the exponential lower bounds for positive and for symmetric real nodes
  - paper: "Bernhard Beckermann, The condition number of real Vandermonde, Krylov and positive definite Hankel matrices, Numerische Mathematik 85 (2000) 553-577"
    locator: the exponential lower bound for every set of real nodes
---

Polynomial interpolation asks for the polynomial $p_n$ of degree at most $n$ that takes given values $y_0, \ldots, y_n$ at $n + 1$ distinct nodes $x_0, \ldots, x_n$. It is the polynomial case of the [interpolation problem](/interpolation-problem/), and it always has exactly one solution. The hard part is not existence but the choice of nodes and of the representation: at equispaced nodes the problem is badly conditioned and the interpolants of a smooth function can diverge, while at Chebyshev nodes with the [barycentric formula](/barycentric-interpolation/) it is one of the most reliable tools of numerical analysis.

## In plain words

You measure a quantity at a few places and want a formula for the values in between. A polynomial is the simplest kind of formula, because it needs only additions and multiplications. If you have a certain number of measurements, there is exactly one polynomial whose degree is one less than that number and that hits every measurement.

So the question is not whether the polynomial exists. The questions are how to compute it cheaply, how to store it, and whether it is any good between the measurements. Where you place the measurements matters a lot. Evenly spaced places can give a polynomial that swings wildly near the ends, while places that crowd toward the ends give a polynomial that stays close to the true curve.

## Definition

Notation on the interpolation pages: $f$ is a function on an interval $[a, b]$, usually $[-1, 1]$; the nodes are $x_0 < x_1 < \cdots < x_n$ (any order is allowed when only distinctness matters); the data are $y_i = f(x_i)$; $\mathcal{P}_n$ is the space of polynomials of degree at most $n$; $\omega(x) = \prod_{i=0}^{n} (x - x_i)$ is the node polynomial; $\Lambda_n$ is the [Lebesgue constant](/lebesgue-constant/) and $E_n(f) = \min_{p \in \mathcal{P}_n} \|f - p\|_\infty$ is the best approximation error. Costs count arithmetic operations on the [real RAM](/real-ram/).

**Input.** A field $K$ (in numerical work $\mathbb{R}$ or $\mathbb{C}$), nodes $x_0, \ldots, x_n \in K$ with $x_i \ne x_j$ for $i \ne j$, and values $y_0, \ldots, y_n \in K$.

**Output.** The polynomial $p_n \in \mathcal{P}_n$ with
$$p_n(x_i) = y_i \qquad (i = 0, 1, \ldots, n).$$

The output must be given in some form. The usual forms are the coefficients in the monomial basis $1, x, \ldots, x^n$, the Newton coefficients (the [divided differences](/divided-differences/) $f[x_0, \ldots, x_k]$), the barycentric weights $w_i = 1 / \prod_{j \ne i} (x_i - x_j)$ together with the data, the coefficients in the Chebyshev basis, or simply the value $p_n(t)$ at given points $t$.

**Existence and uniqueness.** For distinct nodes there is exactly one such $p_n$. Proof: the Lagrange polynomials $\ell_i(x) = \prod_{j \ne i} (x - x_j)/(x_i - x_j)$ lie in $\mathcal{P}_n$ and satisfy $\ell_i(x_k) = \delta_{ik}$, so $p_n = \sum_i y_i \ell_i$ is a solution. If $q$ is a second solution, $p_n - q \in \mathcal{P}_n$ vanishes at $n + 1$ distinct points, and a nonzero polynomial of degree at most $n$ has at most $n$ roots, so $q = p_n$. In matrix terms, the coefficient vector $c$ of $p_n$ in the monomial basis solves $V c = y$ with the [Vandermonde matrix](/vandermonde-matrix/) $V_{ij} = x_i^j$, and $\det V = \prod_{0 \le i < j \le n} (x_j - x_i) \ne 0$. The page [uniqueness of the interpolating polynomial](/interpolating-polynomial-uniqueness/) states the result as a theorem.

**Conditioning.** The map from the data $y$ to the function $p_n$ is linear. On $[a, b]$ in the maximum norm its norm is
$$\Lambda_n = \max_{x \in [a, b]} \sum_{i=0}^{n} |\ell_i(x)|,$$
so $\|p_n\|_\infty \le \Lambda_n \max_i |y_i|$, with equality for the data $y_i = \operatorname{sign} \ell_i(x^*)$ at a point $x^*$ where the maximum is reached. A perturbation of the data of size $\varepsilon$ can change $p_n$ by $\Lambda_n \varepsilon$ and no more. The same constant gives the near-best property: if $p^*$ is a best approximation of degree $n$ to $f$, then $p_n - p^*$ is the interpolant of the data $f(x_i) - p^*(x_i)$, so
$$\|f - p_n\|_\infty \le \|f - p^*\|_\infty + \Lambda_n \|f - p^*\|_\infty = (1 + \Lambda_n)\, E_n(f).$$

## Variants

- **Evaluation.** Return $p_n(t)$ at one point or at many points, with no coefficients. [Neville's algorithm](/neville-algorithm/) and the [barycentric formula](/barycentric-interpolation/) do this.
- **Coefficients in a basis.** Return the monomial, Newton or Chebyshev coefficients. The monomial basis is the worst choice in floating point on a real interval (see below).
- **Hermite data.** Some nodes repeat, and the data give derivatives there. This is [Hermite interpolation](/hermite-interpolation/), the limit of the problem when nodes merge, and the [Newton form](/newton-interpolation/) handles it with divided differences of repeated arguments.
- **Chosen nodes.** The user may pick the nodes. Then the [Chebyshev nodes](/chebyshev-nodes/) give $\Lambda_n = O(\log n)$ and the [Chebyshev interpolant](/chebyshev-interpolation/) converges for every Lipschitz $f$.
- **Exact fields.** Over $\mathbb{Q}$ or a finite field the arithmetic is exact and only the operation count matters. This is the setting of [fast interpolation](/fast-interpolation/), of [Reed-Solomon codes](/reed-solomon-code/) and of [Shamir secret sharing](/shamir-secret-sharing/).
- **Fewer unknowns than data.** If the degree must be less than $n$, the problem has no solution in general, and the usual replacement is the [least squares approximation](/least-squares-approximation/).
- **Several variables.** In $\mathbb{R}^d$ with $d \ge 2$ uniqueness depends on the geometry of the points; see [multivariate interpolation](/multivariate-interpolation/).
- **Periodic data.** Trigonometric polynomials replace algebraic ones; see [trigonometric interpolation](/trigonometric-interpolation/).

## Examples

**Four points.** The data $(-1, 2), (0, 1), (1, 2), (2, 7)$ give $n = 3$. The divided differences are $2, -1, 1, \tfrac{1}{3}$, so
$$p_3(x) = 2 - (x + 1) + (x + 1)x + \tfrac{1}{3}(x + 1)x(x - 1) = 1 - \tfrac{1}{3}x + x^2 + \tfrac{1}{3}x^3.$$
Then $p_3(3) = 18$ and $p_3(\tfrac{1}{2}) = \tfrac{9}{8}$.

**Lower degree than the bound.** The points $(0, 1), (1, 3), (2, 5)$ give $n = 2$, and the answer is $p_2(x) = 1 + 2x$, of degree 1. The problem asks for degree at most $n$, not exactly $n$.

**Non-example: a repeated abscissa.** The points $(1, 0)$ and $(1, 1)$ have no interpolant, because a function takes one value at $x = 1$. With equal values the second point adds no condition, and the solution is not unique. Repeated nodes make sense only with derivative data (Hermite interpolation).

**Node choice.** For Runge's function $f(x) = 1/(1 + 25x^2)$ on $[-1, 1]$, the maximum error of $p_n$ on a grid of 4001 points and the Lebesgue constant are:

| $n$ | error, equispaced | $\Lambda_n$, equispaced | error, Chebyshev first kind | $\Lambda_n$, Chebyshev first kind |
|---|---|---|---|---|
| 5 | 0.433 | 3.11 | 0.556 | 2.10 |
| 10 | 1.92 | 29.9 | 0.109 | 2.49 |
| 20 | 59.8 | $1.10 \times 10^4$ | 0.0153 | 2.90 |
| 40 | $1.05 \times 10^5$ | $4.69 \times 10^9$ | $2.90 \times 10^{-4}$ | 3.33 |

The equispaced interpolants diverge near the ends of the interval; this is the [Runge phenomenon](/runge-phenomenon/).

## Known algorithms

- [Lagrange interpolation](/lagrange-interpolation/): evaluates $\sum_i y_i \ell_i(t)$ directly in $\Theta(n^2)$ operations per point. Backward stable in the data.
- [Barycentric interpolation](/barycentric-interpolation/): $O(n^2)$ operations once for the weights, then $O(n)$ per point. The weights are known in closed form for Chebyshev points, so there the whole cost is $O(n)$ per point. The second form is forward stable for nodes with a small Lebesgue constant (Higham 2004).
- [Newton interpolation](/newton-interpolation/): $n(n+1)/2$ divisions and $n(n+1)$ subtractions for the divided differences, then $O(n)$ per point by nested multiplication. Adding a node costs $O(n)$.
- [Neville's algorithm](/neville-algorithm/): $\Theta(n^2)$ per point with no coefficients, and the table gives error estimates.
- Solving the Vandermonde system $V c = y$: $\Theta(n^3)$ by [Gaussian elimination](/gaussian-elimination/), or $O(n^2)$ by the Björck-Pereyra algorithm (Higham, Chapter 22).
- [Chebyshev interpolation](/chebyshev-interpolation/): at Chebyshev points of the second kind, the Chebyshev coefficients come from a discrete cosine transform in $O(n \log n)$.
- [Fast interpolation](/fast-interpolation/): over an exact field, the coefficients in $O(M(n) \log n)$ operations, where $M(n)$ is the cost of multiplying two polynomials of degree $n$; this is $O(n \log^2 n)$ with FFT multiplication. At the roots of unity it is the [inverse DFT](/inverse-discrete-fourier-transform/), $O(n \log n)$.

## Bounds

**Upper bounds.** On the real RAM, $O(n^2)$ operations give the Newton coefficients or the barycentric weights for arbitrary nodes, and $O(n \log^2 n)$ give the monomial coefficients over a field where FFT multiplication applies. The value at one point needs $O(n)$ operations once the weights are known.

**Lower bounds.** Each of the $n + 1$ data values can change the answer, so every algorithm reads all of them: $\Omega(n)$ per point. For the monomial coefficients from arbitrary nodes, Strassen (1973) proved that $\Omega(n \log n)$ nonscalar multiplications are needed in the algebraic computation model. The gap between $n \log n$ and $n \log^2 n$ is open.

**Conditioning bounds.** The condition number $\Lambda_n$ of the problem depends only on the nodes. For every set of $n + 1$ nodes in $[-1, 1]$, $\Lambda_n \ge \tfrac{2}{\pi} \log(n + 1) + 0.52$, and Chebyshev nodes give $\Lambda_n \le \tfrac{2}{\pi} \log(n + 1) + 1$, so they are within an additive constant of the best (Trefethen, Chapter 15). Equispaced nodes give $\Lambda_n \sim 2^{n+1}/(e\, n \log n)$ as $n \to \infty$. In floating point with unit roundoff $u$, no algorithm can in general guarantee an error below about $\Lambda_n u \max_i |y_i|$, since that is the effect of rounding the data. The monomial coefficients are worse still: the condition number of the Vandermonde matrix grows exponentially in $n$ for every set of real nodes (Gautschi and Inglese 1988 for positive and for symmetric nodes, Beckermann 2000 in general; see [Vandermonde matrix](/vandermonde-matrix/)).

## Reductions

- **To a linear system.** Polynomial interpolation is the Vandermonde system $V c = y$. The reduction is exact but the system is ill-conditioned, so in floating point it is used only for small $n$.
- **To and from multipoint evaluation.** Over an exact field, interpolation and [multipoint evaluation](/multipoint-evaluation/) at the same nodes have the same cost up to a constant factor, by the subproduct tree (von zur Gathen and Gerhard, Chapter 10).
- **From the DFT.** The inverse [discrete Fourier transform](/discrete-fourier-transform/) is polynomial interpolation at the $N$-th roots of unity.
- **To quadrature.** Integrating $p_n$ gives an [interpolatory quadrature](/interpolatory-quadrature/) rule with weights $\int_a^b \ell_i(x)\,dx$.

## Applications

- **Quadrature and differentiation.** Newton-Cotes, Gauss and Clenshaw-Curtis rules integrate an interpolant; finite difference formulas differentiate one.
- **Root finding.** The [secant method](/secant-method/), [Muller's method](/muller-method/) and [inverse quadratic interpolation](/inverse-quadratic-interpolation/) find the root of a low-degree interpolant.
- **Extrapolation.** [Richardson extrapolation](/richardson-extrapolation/) evaluates an interpolant in the step size at step size 0.
- **Spectral methods.** [Spectral methods](/spectral-methods/) for differential equations represent the solution by its values at Chebyshev points.
- **Coding and cryptography.** Reed-Solomon decoding and Shamir secret sharing recover a polynomial over a finite field from its values.

## References
