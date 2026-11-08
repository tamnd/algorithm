---
tag: 3S7CV6
kind: problem
slug: function-approximation
name: Function approximation
aliases:
- Approximating functions
- approximation of functions
- best approximation problem
area: numerical/interpolation-and-approximation
level: intro
summary: Given a function f on an interval, a family of simple functions and a norm, find a member of the family whose distance from f is as small as possible, or below a given tolerance.
prereqs: [interpolation-problem, polynomial]
see_also: [approximation-theory, minimax-approximation, least-squares-approximation, chebyshev-interpolation, remez-algorithm, rational-approximation, curve-fitting, lebesgue-constant]
sources:
  - book: isbn:9781611975932
    title: Lloyd N. Trefethen, Approximation Theory and Approximation Practice, extended edition, SIAM, 2019
    locator: Chapter 7 (convergence for differentiable functions, Theorem 7.2), Chapter 8 (convergence for analytic functions, Theorem 8.2), Chapter 10 (best approximation) and Chapter 16 (best and near-best)
  - book: isbn:9780521295147
    title: M. J. D. Powell, Approximation Theory and Methods, Cambridge University Press, 1981
    locator: Chapter 1 (the approximation problem and existence of best approximations), Chapters 7 and 8 (minimax approximation and the exchange algorithm), Chapter 11 (least squares approximation) and Chapter 17 (the uniform boundedness theorem and the norms of projections)
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Chapter 4, Approximation of functions (Sections 4.2 to 4.7, minimax, least squares and near-minimax approximation)
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 8 (polynomial approximation in the maximum norm) and Chapter 9 (approximation in the 2-norm)
---

Function approximation is the problem of replacing a function $f$ by a member of a family of simple functions, such as polynomials of degree at most $n$, splines or rational functions, so that the error in a chosen norm is as small as possible or below a given tolerance. It is how a math library computes $e^x$, how a solver represents an unknown solution, and how a slow model is replaced by a fast surrogate. Unlike the [interpolation problem](/interpolation-problem/), the answer is judged by its error over the whole interval, not by its values at given points.

## In plain words

You have a function that is slow to compute, or known only through a program that returns its values. You want a short formula that stays close to it everywhere on an interval. You fix the kind of formula in advance, for example a polynomial of a given degree, and you fix how you measure closeness: the largest error at any point, or an average error. The task is to find the formula of that kind that is closest, or one that is close enough.

Smooth functions are easy: a low degree already gives errors near the limits of the computer. Functions with corners need many more terms. A good method also needs few values of the function, since each value can be costly.

## Definition

Notation on the interpolation and approximation pages: $f$ is a function on $[a, b]$, usually $[-1, 1]$; $\mathcal{P}_n$ is the set of polynomials of degree at most $n$; $E_n(f) = \min_{p \in \mathcal{P}_n} \|f - p\|_\infty$ is the best approximation error; $\Lambda_n$ is the [Lebesgue constant](/lebesgue-constant/) of a set of nodes; $T_k$ is the [Chebyshev polynomial](/chebyshev-polynomials/) of degree $k$.

**Input.** A function $f$ on $[a, b]$, given either explicitly or as a procedure that returns $f(x)$ for any $x$; a family $V$ of approximants; a norm $\|\cdot\|$ on functions on $[a, b]$; and either a size parameter (the degree $n$, or the numbers $m, n$ of a rational function, or a number of knots) or a tolerance $\varepsilon > 0$.

**Output.** One of:

- *best approximation*: $v^* \in V$ with $\|f - v^*\| = \inf_{v \in V} \|f - v\|$;
- *near-best approximation*: $v \in V$ with $\|f - v\| \le C \inf_{v' \in V} \|f - v'\|$ for a stated factor $C$;
- *tolerance form*: some $v$ in the smallest family of a nested sequence $V_0 \subset V_1 \subset \cdots$ with $\|f - v\| \le \varepsilon$.

The costs are the arithmetic operations and, when $f$ is a procedure, the number of evaluations of $f$. For a linear subspace $V$ of finite dimension a best approximation always exists; it is unique in a strictly convex norm such as $L^2$, and unique in the maximum norm for $V = \mathcal{P}_n$ ([approximation theory](/approximation-theory/), properties 2 and 3).

## Variants

- **Minimax (uniform) approximation**: the norm is $\|g\|_\infty = \max_{[a, b]} |g|$, or a weighted maximum $\max |g|/|w|$, for example $w = f$ for relative error. See [minimax approximation](/minimax-approximation/) and the [Remez algorithm](/remez-algorithm/).
- **Least squares**: the norm is $\|g\|_2 = (\int_a^b |g|^2 w)^{1/2}$, or a sum over data points. See [least-squares approximation](/least-squares-approximation/) and [orthogonal polynomials](/orthogonal-polynomials/).
- **$L^1$ approximation**: the norm is $\int |g|$; the best approximation is robust to outliers in the discrete case (Powell, Chapters 14 and 15).
- **Near-best by interpolation or truncation**: [Chebyshev interpolation](/chebyshev-interpolation/) and truncated [Chebyshev series](/chebyshev-series/) cost far less than the best approximation and lose only a small factor.
- **Nonlinear families**: [rational approximation](/rational-approximation/), [Padé approximation](/pade-approximation/) (best near one point), and splines with free knots.
- **Discrete data**: $f$ is known only at fixed points, possibly with noise; this is [curve fitting](/curve-fitting/).
- **Several variables**: tensor products, [sparse grids](/smolyak-sparse-grids/), [radial basis functions](/radial-basis-function-interpolation/).

## Examples

**$e^x$ on $[-1, 1]$.** The interpolant of degree $n$ in the [Chebyshev points](/chebyshev-nodes/) $\cos(j\pi/n)$ has these maximum errors:

| $n$ | 2 | 4 | 6 | 8 | 10 | 12 | 14 |
|---|---|---|---|---|---|---|---|
| error | $7.9 \times 10^{-2}$ | $1.1 \times 10^{-3}$ | $6.4 \times 10^{-6}$ | $2.2 \times 10^{-8}$ | $5.0 \times 10^{-11}$ | $8.0 \times 10^{-14}$ | $2.7 \times 10^{-15}$ |

At degree 14 the error is at the level of rounding in double precision. The fall is faster than geometric because $e^x$ is entire. For $n = 1$ the best approximation is $1.2643 + 1.1752\,x$ with error $0.2788$ (see [approximation theory](/approximation-theory/)).

**The Runge function.** For $f(x) = 1/(1 + 25 x^2)$, the Chebyshev interpolant has the errors $1.8 \times 10^{-2}$, $3.4 \times 10^{-4}$, $1.2 \times 10^{-7}$ and $1.6 \times 10^{-14}$ at $n = 20, 40, 80, 160$. The ratio between consecutive errors at $n = 40$ and $n = 80$ corresponds to the factor $\rho^{-40}$ with $\rho = (1 + \sqrt{26})/5 \approx 1.22$, as the theory for analytic functions predicts.

**$|x|$.** The Chebyshev interpolant has the error $0.0373$ at $n = 16$, $0.0149$ at $n = 40$ and $0.00373$ at $n = 160$: the error falls only like $0.6/n$. The best error behaves like $0.2802/n$. A tolerance of $10^{-6}$ would need a degree in the hundreds of thousands; a piecewise or rational approximant with a break at 0 is the right tool here.

**A non-example.** "Find the polynomial of degree 3 that agrees with $f$ at $0, 1, 2, 3$" is an [interpolation problem](/interpolation-problem/), not an approximation problem: it puts no condition on the error between or beyond the nodes, and for a bad choice of nodes that error can be large.

## Known algorithms

- [Chebyshev interpolation](/chebyshev-interpolation/): $n + 1$ evaluations of $f$ and $O(n \log n)$ operations by the [fast cosine transform](/fast-dct/) (or $O(n^2)$ directly), with error at most $(1 + \Lambda_n) E_n(f)$, where $\Lambda_n \le \tfrac{2}{\pi}\log(n+1) + 1$.
- [Chebyshev series](/chebyshev-series/) truncation: the projection onto $\mathcal{P}_n$ in the Chebyshev weighted norm; near-best in the maximum norm with a factor of order $\log n$.
- [Remez algorithm](/remez-algorithm/): the minimax polynomial or rational function by exchange of reference points, with quadratic convergence for smooth $f$; each step solves a linear system of size $n + 2$ and searches for the extrema of the error.
- [Least squares](/least-squares-approximation/) by [orthogonal polynomials](/orthogonal-polynomials/) or by a [QR decomposition](/qr-decomposition/) of a discrete problem.
- [Chebyshev economization](/chebyshev-economization/): lower the degree of a given polynomial with a known small loss.
- [Padé approximation](/pade-approximation/) and [rational approximation](/rational-approximation/) for functions with poles or singularities.
- Splines: [cubic spline interpolation](/cubic-spline-interpolation/), [smoothing splines](/smoothing-spline/) and [B-spline fitting](/b-spline-fitting/), with $O(h^4)$ error for $f \in C^4$ on a mesh of width $h$.

## Bounds

All bounds below are proved theorems for polynomials on $[-1, 1]$.

- **Near-best factor.** For interpolation at nodes with Lebesgue constant $\Lambda_n$, $\|f - p_n\|_\infty \le (1 + \Lambda_n) E_n(f)$. No linear projection onto $\mathcal{P}_n$ has a norm below order $\log n$ (the lower bound on $\Lambda_n$, and for general projections the theorem of Kharshiladze and Lozinski; Powell, Chapter 17), so a factor of order $\log n$ is the best possible for linear methods.
- **Smooth functions.** If $f, \ldots, f^{(\nu-1)}$ are absolutely continuous and $f^{(\nu)}$ has bounded variation $V$, then for $n > \nu$ the Chebyshev interpolant satisfies $\|f - p_n\|_\infty \le 4V/(\pi \nu (n - \nu)^\nu)$ (Trefethen, Theorem 7.2).
- **Analytic functions.** If $f$ is analytic in the open Bernstein ellipse $E_\rho$ with foci $\pm 1$ and semiaxis sum $\rho > 1$, and $|f| \le M$ there, then the Chebyshev interpolant satisfies $\|f - p_n\|_\infty \le 4M\rho^{-n}/(\rho - 1)$ (Trefethen, Theorem 8.2).
- **Lower bounds.** [Jackson's theorem](/jackson-theorem/) and Bernstein's inverse theorems show that for the class $\{f : \|f^{(k)}\|_\infty \le 1\}$ the worst-case $E_n(f)$ is of order $n^{-k}$, not smaller; the [Kolmogorov width](/kolmogorov-width/) shows that no other $n$-dimensional linear space does better than polynomials by more than a constant factor for such a class.

## Reductions

- **To interpolation.** Near-best approximation reduces to interpolation at good nodes, with the loss factor $1 + \Lambda_n$.
- **To linear algebra.** Discrete least squares is a [least-squares problem](/least-squares-problem/) $\min \|Ac - y\|_2$; each Remez step is a square linear system; discrete minimax approximation on a finite set is a linear program.
- **From quadrature and differential equations.** [Interpolatory quadrature](/interpolatory-quadrature/) integrates an approximant; spectral methods approximate the unknown solution by a Chebyshev series.

## Applications

- Elementary and special functions in math libraries: a minimax polynomial or rational function on a small interval after [range reduction](/cody-waite-range-reduction/), evaluated with [Horner's rule](/horner-rule/).
- Surrogate models of expensive simulations, and response surfaces in design.
- Representations of functions in numerical software: Chebyshev expansions in spectral methods, splines in graphics and CAD.
- Signal processing: filter design by the [Remez algorithm](/remez-algorithm/) (the Parks and McClellan method).

## References
