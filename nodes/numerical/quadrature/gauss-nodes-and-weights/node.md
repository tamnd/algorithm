---
tag: V3YP1H
kind: problem
slug: gauss-nodes-and-weights
name: Computing Gaussian nodes and weights
aliases:
- Gauss quadrature node computation
- computing Gauss rules
- Gauss quadrature construction
area: numerical/quadrature
level: advanced
summary: Given a weight function and n, compute the n nodes and positive weights of its Gauss rule accurately and fast, from recurrence coefficients, moments or asymptotics.
prereqs: [gaussian-quadrature]
see_also: [golub-welsch-algorithm, gauss-legendre-quadrature, gauss-quadrature-theorem, orthogonal-polynomials, tridiagonal-eigenproblem, sturm-sequence-eigenvalue-count, newton-raphson-method, gauss-kronrod-quadrature]
sources:
  - book: isbn:9780198506720
    title: Walter Gautschi, Orthogonal Polynomials, Computation and Approximation, Oxford University Press, 2004
    locator: Chapter 2 (computing recurrence coefficients from moments, modified moments and discretizations, with conditioning) and Chapter 3, Section 3.1 (computing Gauss-type rules)
  - paper: "Gene H. Golub and John H. Welsch, Calculation of Gauss quadrature rules, Mathematics of Computation 23 (1969) 221-230"
    locator: the eigenvalue method
  - paper: "Andreas Glaser, Xiangtao Liu and Vladimir Rokhlin, A fast algorithm for the calculation of the roots of special functions, SIAM Journal on Scientific Computing 29(4) (2007) 1420-1438"
    locator: the O(n) method for Gauss rules by ODE integration and Newton steps
  - paper: "Nicholas Hale and Alex Townsend, Fast and accurate computation of Gauss-Legendre and Gauss-Jacobi quadrature nodes and weights, SIAM Journal on Scientific Computing 35(2) (2013) A652-A674"
    locator: Newton with asymptotic expansions, accuracy of the weights, comparison with Golub-Welsch
  - paper: "Ignace Bogaert, Iteration-free computation of Gauss-Legendre quadrature nodes and weights, SIAM Journal on Scientific Computing 36(3) (2014) A1008-A1026"
    locator: explicit asymptotic formulas with O(1) cost per node
  - paper: "Alex Townsend, Thomas Trogdon and Sheehan Olver, Fast computation of Gauss quadrature nodes and weights on the whole real line, IMA Journal of Numerical Analysis 36(1) (2016) 337-358"
    locator: O(n) Gauss-Hermite rules and the underflow of the weights
  - paper: "Gene H. Golub, Some modified matrix eigenvalue problems, SIAM Review 15(2) (1973) 318-334"
    locator: modified Jacobi matrices for Radau and Lobatto rules
  - book: isbn:9780122063602
    title: Philip J. Davis and Philip Rabinowitz, Methods of Numerical Integration, second edition, Academic Press, 1984
    locator: Chapter 2 (Section 2.7, Gauss rules and their computation) and Chapter 3 (Gauss-Laguerre and Gauss-Hermite rules)
---

Computing Gaussian nodes and weights is the problem of producing, for a weight function $w$ and a number $n$, the $n$ nodes and the $n$ positive weights of the [Gaussian quadrature](/gaussian-quadrature/) rule of $w$, to near machine accuracy. The nodes are the zeros of the degree-$n$ [orthogonal polynomial](/orthogonal-polynomials/) of $w$, and the weights are the Christoffel numbers. When the three-term recurrence of the polynomials is known, the problem reduces to a [symmetric tridiagonal eigenproblem](/tridiagonal-eigenproblem/) or to Newton's method on the recurrence, both in $O(n^2)$ operations; for the classical weights, asymptotic formulas bring the cost to $O(n)$.

## In plain words

A Gauss rule is a short list of points and weights. Once you have the list, integrating a function costs one evaluation per point. Making the list is the hard part: the points are the roots of a polynomial of high degree, and for some weights the smallest weights are tiny numbers that are easy to get wrong. This problem asks how to make the list fast and with every digit right. The answer depends on what you know about the weight: a formula for its orthogonal polynomials, only its moments, or nothing but the ability to evaluate it.

## Definition

**Notation.** As on all quadrature pages: $I(f) = \int_a^b f(x)\,w(x)\,dx$; $Q_n(f) = \sum_{i=1}^n w_i f(x_i)$, where $n$ counts nodes; $E_n(f) = I(f) - Q_n(f)$. The monic orthogonal polynomials of $w$ satisfy $\pi_{k+1} = (x - \alpha_k)\pi_k - \beta_k\pi_{k-1}$ with $\beta_0 = \int_a^b w$.

**Input.** A weight $w \ge 0$ on $(a, b)$, positive on a set of positive measure and with finite moments, described in one of these ways: by its recurrence coefficients $\alpha_k, \beta_k$ for $k < n$; by its moments $\mu_k = \int x^k w$ or modified moments $\int q_k w$ for $k < 2n$; or by a routine that evaluates $w$. Also $n \ge 1$.

**Output.** The nodes $x_1 < \cdots < x_n$ and the weights $w_1, \ldots, w_n > 0$ such that $Q_n(p) = I(p)$ for every polynomial $p$ of degree at most $2n - 1$. By the [Gauss quadrature theorem](/gauss-quadrature-theorem/) this output exists and is unique.

**Accuracy.** A good solution gives each node with an error of a few units of rounding relative to the scale of the interval (or to $|x_i|$), and each weight with a small relative error, even when the weights span hundreds of orders of magnitude, as for Gauss-Laguerre and Gauss-Hermite with large $n$.

## Variants

- **Classical weights.** Legendre, Chebyshev, Jacobi, Laguerre, Hermite: the recurrence coefficients are known in closed form, and asymptotic expansions of the polynomials and their zeros are available. See [Gauss-Legendre](/gauss-legendre-quadrature/), [Gauss-Jacobi](/gauss-jacobi-quadrature/), [Gauss-Laguerre](/gauss-laguerre-quadrature/), [Gauss-Hermite](/gauss-hermite-quadrature/).
- **Nonclassical weights.** The recurrence coefficients must be computed first, from moments, modified moments, or a discretization of $w$.
- **Rules with prescribed nodes.** [Gauss-Radau](/gauss-radau-quadrature/) and [Gauss-Lobatto](/gauss-lobatto-quadrature/) fix one or two endpoints; [Gauss-Kronrod](/gauss-kronrod-quadrature/) fixes the $n$ Gauss nodes and adds $n + 1$.
- **Very large $n$.** Rules with $10^5$ to $10^9$ nodes for spectral methods and for high-frequency integrals, where $O(n^2)$ is too slow.
- **Extended precision.** Rules to 30 or more digits for use in multiple-precision libraries.

## Examples

| weight $w$ on interval | $n$ | nodes | weights |
|---|---|---|---|
| $1$ on $[-1, 1]$ | 3 | $0, \pm\sqrt{3/5}$ | $\tfrac89, \tfrac59$ |
| $e^{-x^2}$ on $\mathbb{R}$ | 3 | $0, \pm\sqrt{3/2}$ | $\tfrac{2\sqrt\pi}{3}, \tfrac{\sqrt\pi}{6}$ |
| $e^{-x}$ on $[0, \infty)$ | 2 | $2 - \sqrt2, 2 + \sqrt2$ | $\tfrac{2 + \sqrt2}{4}, \tfrac{2 - \sqrt2}{4}$ |
| $(1 - x^2)^{-1/2}$ on $[-1, 1]$ | $n$ | $\cos\frac{(2i - 1)\pi}{2n}$ | $\tfrac{\pi}{n}$ each |

For Gauss-Hermite with $n = 3$, the nodes are the zeros of $H_3(x) = 8x^3 - 12x$; the weights add up to $\sqrt{\pi}$, and the rule gives $Q_3(x^2) = 2 \cdot \tfrac{\sqrt\pi}{6} \cdot \tfrac32 = \tfrac{\sqrt\pi}{2} = \int x^2 e^{-x^2}$. For Gauss-Laguerre with $n = 2$, the nodes are the zeros of $x^2 - 4x + 2$, and $Q_2(x) = \tfrac{(2+\sqrt2)(2-\sqrt2) + (2-\sqrt2)(2+\sqrt2)}{4} = 1 = \int_0^\infty x e^{-x}\,dx$. Only the Chebyshev weight has closed forms for all $n$; for the others, $n \ge 5$ or so needs computation.

The range of the weights grows quickly. For Gauss-Hermite with $n = 100$, the smallest weight is about $6 \times 10^{-79}$; for Gauss-Laguerre with $n = 100$, about $3 \times 10^{-162}$, and for a few hundred nodes the smallest Laguerre weights underflow in double precision.

## Known algorithms

| method | input | cost for all nodes and weights | notes |
|---|---|---|---|
| [Golub-Welsch](/golub-welsch-algorithm/) (1969) | $\alpha_k, \beta_k$ | $O(n^2)$ | QR or QL on the Jacobi matrix, first eigenvector components |
| Sturm bisection and Christoffel ([Gaussian quadrature](/gaussian-quadrature/)) | $\alpha_k, \beta_k$ | $O(n^2)$ | robust brackets; larger constant |
| Newton on the recurrence ([Gauss-Legendre](/gauss-legendre-quadrature/)) | $\alpha_k, \beta_k$, starting guesses | $O(n^2)$ | $O(n)$ per Newton step, a few steps per node |
| Glaser, Liu and Rokhlin (2007) | the ODE of the classical polynomial | $O(n)$ | Runge-Kutta between zeros, Taylor series for Newton |
| Hale and Townsend (2013) | Legendre, Jacobi | $O(n)$ | Newton with asymptotic expansions of $P_n$ |
| Bogaert (2014) | Legendre | $O(n)$ | explicit asymptotic formulas, no iteration |
| Townsend, Trogdon and Olver (2016) | Hermite | $O(n)$ | asymptotics on the whole real line |
| Chebyshev and modified Chebyshev algorithms | moments, modified moments | $O(n^2)$ to get $\alpha_k, \beta_k$ | then any method above (Gautschi, Chapter 2) |
| discretized Stieltjes procedure | values of $w$ | $O(nN)$ with $N$ discretization points | Gautschi, Chapter 2 |

Measured in pure Python on the implementations of this site, for Gauss-Legendre: $n = 100$ took 0.095 s by bisection, 0.014 s by Golub-Welsch and 0.004 s by bracketed Newton with symmetry; $n = 1000$ by Newton took 0.47 s. The three methods agreed on the nodes to $10^{-15}$ for $n \le 500$, and on the weights to a relative $10^{-11}$.

## Bounds

- **Output size.** Any method must write $2n$ numbers, so $\Omega(n)$ is a lower bound; the $O(n)$ methods for the classical weights are optimal up to the constant.
- **Conditioning of the nodes.** A perturbation of the recurrence coefficients by a relative $\varepsilon$ moves the eigenvalues of the Jacobi matrix by at most about $\varepsilon\|J_n\|$ (Weyl's inequality). Backward stable eigensolvers therefore give an absolute node error of order $u\|J_n\|$, with $u = 2^{-53}$. Nodes near $0$ in a long interval (Gauss-Laguerre has $\|J_n\| \approx 4n$) can lose relative accuracy this way.
- **Weights.** Newton with asymptotic formulas gives each weight to a relative accuracy of a few $u$ (Hale and Townsend 2013). The weights from an eigensolver have a guaranteed absolute accuracy of order $u\beta_0$; the measured relative accuracy on this site was much better, about $10^{-13}$ even for weights near $10^{-79}$, but it is not guaranteed.
- **Moments are a bad input.** The map from the ordinary moments $\mu_0, \ldots, \mu_{2n-1}$ to the Gauss rule is ill-conditioned, with a condition number that grows exponentially in $n$ for weights on $[0, 1]$ and $[-1, 1]$ (Gautschi, Chapter 2). With moments in double precision only a few tens of nodes can be computed. Modified moments with respect to a well-chosen polynomial basis, such as Chebyshev polynomials, can be well conditioned.

## Reductions

- **To a symmetric tridiagonal eigenproblem.** With the Jacobi matrix $J_n$, the nodes are its eigenvalues and $w_j = \beta_0 v_{1j}^2$. Any tridiagonal eigensolver that returns the first eigenvector components solves the problem.
- **To polynomial root finding with structure.** The nodes are the zeros of $\pi_n$, and the recurrence evaluates $\pi_n$ and $\pi_n'$ stably in $O(n)$; the weights follow from $w_j = 1/\sum_{k<n} p_k(x_j)^2$ or from closed forms such as $2/((1 - x_j^2)P_n'(x_j)^2)$ for Legendre.
- **From modified rules.** Radau and Lobatto rules reduce to eigenproblems for $J_n$ with a modified last row (Golub 1973), and Kronrod rules to an eigenproblem of size $2n + 1$ (Laurie 1997).
- **From moments.** Moments determine the recurrence coefficients through the Hankel matrix of moments (the Chebyshev algorithm); the reverse direction, from coefficients to moments, is easy.
- **Applying a rule on $[a, b]$.** The affine map $x \mapsto \frac{a+b}{2} + \frac{b-a}{2}x$ turns a rule for $[-1, 1]$ with $w = 1$ into a rule for $[a, b]$, so only the standard interval needs to be computed.

## Applications

- **Quadrature.** Gauss rules for smooth integrands, Gauss-Kronrod panels in [adaptive quadrature](/adaptive-quadrature/), and Gauss-Jacobi rules for endpoint singularities.
- **Spectral and spectral element methods.** Legendre-Gauss and Legendre-Gauss-Lobatto points are the collocation and quadrature points of Legendre spectral methods; very large $n$ is used for high-resolution simulations.
- **Probability and statistics.** Gauss-Hermite rules compute expectations of functions of normal random variables, for example in generalized linear mixed models.
- **Laplace transforms and special functions.** Gauss-Laguerre rules integrate against $e^{-x}$ on $[0, \infty)$.
- **Implicit Runge-Kutta methods.** Gauss, Radau IIA and Lobatto IIIA collocation methods use Gauss, Radau and Lobatto nodes as their stages.

## References
