---
tag: NJ8RZY
kind: problem
slug: interpolation-problem
name: Interpolation problem
aliases:
- Data interpolation
- Function interpolation
- Lagrange interpolation problem
area: numerical/interpolation-and-approximation
level: intro
summary: Given nodes x_0, ..., x_n and values y_0, ..., y_n, find a function from a chosen family (polynomials of degree at most n, splines, trigonometric or rational functions) with value y_i at x_i.
prereqs: [polynomial, linear-system-solving]
see_also: [lagrange-interpolation, barycentric-interpolation, newton-interpolation, interpolating-polynomial-uniqueness, hermite-interpolation, cubic-spline-interpolation, lebesgue-constant, function-approximation]
sources:
  - book: isbn:9781611975932
    title: Lloyd N. Trefethen, Approximation Theory and Approximation Practice, extended edition, SIAM, 2019
    locator: Chapter 2 (Chebyshev points and interpolants), Chapter 5 (barycentric interpolation formula) and Chapter 15 (Lebesgue constants)
  - book: isbn:9780521295147
    title: M. J. D. Powell, Approximation Theory and Methods, Cambridge University Press, 1981
    locator: Chapter 4, Polynomial interpolation, and Chapter 5, Divided differences
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Chapter 3, Interpolation theory (Section 3.1, polynomial interpolation theory)
  - book: isbn:9780486624952
    title: Philip J. Davis, Interpolation and Approximation, Dover, 1975 (first published 1963)
    locator: Chapter II, Interpolation (the general linear interpolation problem and unisolvence)
  - paper: "V. Strassen, Die Berechnungskomplexität von elementarsymmetrischen Funktionen und von Interpolationskoeffizienten, Numerische Mathematik 20 (1973) 238-251"
    locator: the lower bound of order n log n on the number of nonscalar multiplications for the interpolation coefficients
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Chapter 10, Fast polynomial evaluation and interpolation
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 22, Vandermonde systems
---

The interpolation problem asks for a function from a chosen family that passes through given data points $(x_0, y_0), \ldots, (x_n, y_n)$. The family is most often the [polynomials](/polynomial/) of degree at most $n$, and then the answer exists and is unique for any distinct nodes; other families are piecewise polynomials ([splines](/cubic-spline-interpolation/)), trigonometric polynomials and rational functions. The problem is a [linear system](/linear-system-solving/) in disguise, but how it is solved decides both the cost and the accuracy in floating point.

## In plain words

You measured a quantity at a few points, or a slow program gave you a few values of a function. You want a formula that gives the same values at those points and a sensible value between them. Interpolation finds such a formula from a family that you choose in advance, such as polynomials of a fixed degree or smooth curves joined end to end.

Two questions decide whether the job is well posed. Is there exactly one member of the family that fits the data? And does a small change in the data give only a small change in the answer? For polynomials the first answer is always yes. The second answer depends strongly on where the points are: points packed near the ends of the interval behave well, and evenly spaced points can behave very badly.

## Definition

Notation on the interpolation and approximation pages: $f$ is a function on an interval $[a, b]$, usually $[-1, 1]$; the nodes are $x_0 < x_1 < \cdots < x_n$ and the data are $y_i = f(x_i)$; $p_n$ is the interpolating polynomial of degree at most $n$; $\omega(x) = \prod_{i=0}^{n} (x - x_i)$ is the node polynomial; $\Lambda_n$ is the [Lebesgue constant](/lebesgue-constant/); $E_n(f) = \min_{\deg p \le n} \|f - p\|_\infty$ is the best approximation error; $T_k$ is the [Chebyshev polynomial](/chebyshev-polynomials/) of degree $k$. Costs are counted in arithmetic operations of the [real RAM](/real-ram/), with the leading term when it is known.

**Input.** Distinct nodes $x_0, \ldots, x_n$ in $[a, b]$ (in any order), values $y_0, \ldots, y_n$, and a linear space $V$ of functions on $[a, b]$ with $\dim V = n + 1$ and a basis $\varphi_0, \ldots, \varphi_n$.

**Output.** A function $v \in V$ with
$$v(x_i) = y_i \qquad (i = 0, \ldots, n).$$

Write $v = \sum_j c_j \varphi_j$. The conditions are the linear system $A c = y$ with the collocation matrix $A_{ij} = \varphi_j(x_i)$. The problem is *unisolvent* for the nodes when it has exactly one solution for every $y$. Because $A$ is square, unisolvence holds exactly when $A$ is nonsingular, and then also exactly when the only $v \in V$ that vanishes at all nodes is $v = 0$.

**Polynomial interpolation.** For $V = \mathcal{P}_n$, the polynomials of degree at most $n$, with the monomial basis, $A$ is the [Vandermonde matrix](/vandermonde-matrix/) with $\det A = \prod_{0 \le i < j \le n} (x_j - x_i)$, which is not zero for distinct nodes. So polynomial interpolation is unisolvent for every set of $n + 1$ distinct nodes; the [uniqueness theorem](/interpolating-polynomial-uniqueness/) gives the direct proof. Its solution $p_n$ can be written down without a linear solve, in the [Lagrange form](/lagrange-interpolation/) $p_n(x) = \sum_i y_i \ell_i(x)$ with $\ell_i(x) = \prod_{j \ne i} (x - x_j)/(x_i - x_j)$.

**Conditioning.** The map from the data $y$ to the interpolant is linear. In the maximum norm on $[a, b]$, a change $\delta y$ in the data changes $p_n$ by at most $\Lambda_n \max_i |\delta y_i|$, where $\Lambda_n = \max_{x \in [a, b]} \sum_i |\ell_i(x)|$, and some $\delta y$ of size 1 attains this bound. So $\Lambda_n$ is the absolute condition number of the problem. It depends only on the nodes.

## Variants

- **Polynomial interpolation**: $V = \mathcal{P}_n$, the main case. The form of the answer is a choice: [Lagrange](/lagrange-interpolation/), [barycentric](/barycentric-interpolation/), [Newton](/newton-interpolation/) with [divided differences](/divided-differences/), or monomial coefficients.
- **Hermite interpolation**: some conditions fix derivatives, $p^{(r)}(x_i) = y_i^{(r)}$ for $r = 0, \ldots, m_i - 1$. See [Hermite interpolation](/hermite-interpolation/). When the orders of the given derivatives at a node have gaps (Birkhoff interpolation), unisolvence can fail even for polynomials.
- **Piecewise interpolation**: $V$ is a space of piecewise polynomials, for example [piecewise linear](/piecewise-linear-interpolation/) functions, [cubic Hermite splines](/cubic-hermite-spline/) or [cubic splines](/cubic-spline-interpolation/), where the extra freedom is fixed by end conditions.
- **Trigonometric interpolation**: $V$ is spanned by $1, \cos kx, \sin kx$, for periodic data; on equispaced nodes it is a [discrete Fourier transform](/discrete-fourier-transform/). See [trigonometric interpolation](/trigonometric-interpolation/).
- **Rational interpolation**: $v = p/q$ with fixed degrees; the problem is nonlinear and can fail to have a solution. See [Thiele continued fractions](/thiele-continued-fraction-interpolation/) and [rational approximation](/rational-approximation/).
- **Multivariate and scattered data**: nodes in $\mathbb{R}^d$. On a domain of $\mathbb{R}^d$ with $d \ge 2$ and an interior point, no fixed space of continuous functions of dimension at least 2 is unisolvent for all sets of distinct nodes (the Mairhuber and Curtis theorem), so methods let $V$ depend on the nodes, as [radial basis functions](/radial-basis-function-interpolation/) and [kriging](/kriging/) do. See [multivariate interpolation](/multivariate-interpolation/) and [scattered data interpolation](/scattered-data-interpolation/).
- **Exact arithmetic**: over a field such as $\mathbb{Q}$ or a finite field, interpolation is the [Chinese remainder theorem](/chinese-remainder-theorem/) for the moduli $x - x_i$, and it is used in [Reed-Solomon codes](/reed-solomon-code/) and [Shamir secret sharing](/shamir-secret-sharing/).

## Examples

**Three points.** For the nodes $0, 1, 2$ and the data $1, 3, 7$, the Vandermonde system is
$$\begin{pmatrix} 1 & 0 & 0 \\ 1 & 1 & 1 \\ 1 & 2 & 4 \end{pmatrix} \begin{pmatrix} c_0 \\ c_1 \\ c_2 \end{pmatrix} = \begin{pmatrix} 1 \\ 3 \\ 7 \end{pmatrix},$$
with the solution $c = (1, 1, 1)$, so $p_2(x) = x^2 + x + 1$. The Lagrange form gives the same polynomial: $p_2(x) = \tfrac{1}{2}(x - 1)(x - 2) - 3x(x - 2) + \tfrac{7}{2} x(x - 1)$.

**A space that is not unisolvent.** Take $V = \operatorname{span}\{1, x^2\}$ and the nodes $-1, 1$. Then $A = \begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix}$ is singular: the data $(1, 2)$ have no solution, and the data $(1, 1)$ have the solutions $c_0 + c_1 = 1$. The same space with the nodes $0, 1$ is unisolvent. So unisolvence is a property of the space and the nodes together.

**Conditioning depends on the nodes.** On $[-1, 1]$ with $n = 10$, the Lebesgue constant is about $29.9$ for equispaced nodes and about $2.42$ for the [Chebyshev points](/chebyshev-nodes/) $\cos(j\pi/10)$. At $n = 20$ the two numbers are about $1.1 \times 10^4$ and $2.87$. A data error of $10^{-6}$ can thus become an error near $10^{-2}$ in the equispaced interpolant of degree 20, and stays near $3 \times 10^{-6}$ for Chebyshev points.

## Known algorithms

For polynomial interpolation of $n + 1$ points, counted in arithmetic operations:

- [Lagrange interpolation](/lagrange-interpolation/): $O(n^2)$ per evaluation point when each $\ell_i(x)$ is formed from scratch.
- [Barycentric interpolation](/barycentric-interpolation/): $O(n^2)$ once for the weights, then $O(n)$ per evaluation point; backward stable in the second form for well-chosen nodes (Higham 2004).
- [Divided differences](/divided-differences/) and the [Newton form](/newton-interpolation/): $n(n+1)/2$ divisions and $n(n+1)$ subtractions for the coefficients, then $O(n)$ per point by a nested scheme like [Horner's rule](/horner-rule/).
- [Neville's algorithm](/neville-algorithm/): $O(n^2)$ per evaluation point, with no coefficients.
- Solving the Vandermonde system by Gaussian elimination: $O(n^3)$; the Björck and Pereyra algorithm takes $O(n^2)$ (Higham, Chapter 22). The monomial basis is badly conditioned on real intervals, so this route loses accuracy fast as $n$ grows.
- [Fast interpolation](/fast-interpolation/) with a [subproduct tree](/subproduct-tree/): $O(M(n) \log n)$ operations, where $M(n)$ is the cost of a polynomial product, so $O(n \log^2 n)$ with the FFT over a suitable field.
- [Chebyshev interpolation](/chebyshev-interpolation/) at Chebyshev points: the coefficients in the Chebyshev basis by a [fast cosine transform](/fast-dct/) in $O(n \log n)$.

For other families: [cubic spline interpolation](/cubic-spline-interpolation/) needs one [tridiagonal solve](/tridiagonal-system-solving/), $O(n)$; [trigonometric interpolation](/trigonometric-interpolation/) on equispaced nodes is an FFT, $O(n \log n)$; [radial basis function interpolation](/radial-basis-function-interpolation/) and [kriging](/kriging/) solve a dense symmetric system, $O(n^3)$.

## Bounds

- **Upper bound.** $O(M(n) \log n)$ operations for the coefficients of $p_n$ in the monomial basis from $n + 1$ values (von zur Gathen and Gerhard, Chapter 10), that is $O(n \log^2 n)$ when $M(n) = O(n \log n)$.
- **Lower bound.** Strassen (1973) proved that computing the coefficients of the interpolating polynomial needs $\Omega(n \log n)$ nonscalar multiplications and divisions in the algebraic straight-line model. So the fast algorithms are optimal up to a factor of order $\log n$ in that model.
- **Accuracy.** No algorithm can beat the conditioning: for any method the error in the computed values is in general of size $\Lambda_n$ times the error in the data. Trefethen (Chapter 15) gives $\Lambda_n \ge \tfrac{2}{\pi} \log(n + 1) + 0.52$ for every node set, $\Lambda_n \le \tfrac{2}{\pi} \log(n + 1) + 1$ for Chebyshev points, and growth like $2^{n+1}/(e\, n \log n)$ for equispaced nodes.

## Reductions

- **To a linear system.** Polynomial interpolation is the Vandermonde system above; for a general space it is $A c = y$ with the collocation matrix. This reduction is exact but often a bad way to compute, because $A$ can be far worse conditioned than the problem itself.
- **Inverse of multipoint evaluation.** Evaluation maps coefficients to values at the nodes; interpolation maps values back. Both are $O(M(n) \log n)$ by the [subproduct tree](/subproduct-tree/), see [multipoint evaluation](/multipoint-evaluation/) and the [evaluation and interpolation paradigm](/evaluation-interpolation-paradigm/).
- **Chinese remaindering.** Over a field, $p_n$ is the unique residue modulo $\omega(x)$ with $p_n \equiv y_i \pmod{x - x_i}$, so polynomial interpolation is a case of the [Chinese remainder theorem](/chinese-remainder-theorem/) in $F[x]$.

## Applications

- Tables and special functions: reading values between the entries of a table, the original use in astronomy and navigation.
- Numerical methods built on an interpolant: [interpolatory quadrature](/interpolatory-quadrature/) rules, [linear multistep methods](/linear-multistep-methods/) for ODEs, and root finders such as the [secant method](/secant-method/), [Muller's method](/muller-method/) and [inverse quadratic interpolation](/inverse-quadratic-interpolation/).
- Exact computation: the [evaluation and interpolation paradigm](/evaluation-interpolation-paradigm/) in computer algebra, [Reed-Solomon codes](/reed-solomon-code/) and [Shamir secret sharing](/shamir-secret-sharing/).
- Graphics and signals: [image resampling](/image-resampling/) with [bilinear](/bilinear-interpolation/) and [bicubic](/bicubic-interpolation/) interpolation, and smooth curves through points with splines.

## References
