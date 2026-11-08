---
tag: PA1GCR
kind: problem
slug: least-squares-approximation
name: Least-squares approximation
aliases:
- Least squares fitting
- Linear least squares
- least squares
- L2 approximation
area: numerical/interpolation-and-approximation
level: intro
summary: Find the member of a linear family of functions that minimizes a weighted sum or integral of squared errors against a function or data. The answer is characterized by orthogonality of the error.
prereqs: [function-approximation, least-squares-problem]
see_also: [orthogonal-polynomials, legendre-polynomials, normal-equations, qr-decomposition, hilbert-matrix, curve-fitting, chebyshev-series, minimax-approximation]
sources:
  - book: isbn:9780521295147
    title: M. J. D. Powell, Approximation Theory and Methods, Cambridge University Press, 1981
    locator: Chapter 11, Least squares approximation, and Chapter 12, Properties of orthogonal polynomials
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 9, Approximation in the 2-norm (inner product spaces, the normal equations, the Hilbert matrix and orthogonal polynomials)
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Section 4.3, The least squares approximation problem; Section 4.4, Orthogonal polynomials; Section 4.5, The least squares approximation problem (continued)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 20, The least squares problem (QR factorization, the normal equations and their accuracy)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Chapter 5, Orthogonalization and least squares
  - paper: "George E. Forsythe, Generation and use of orthogonal polynomials for data-fitting with a digital computer, Journal of the Society for Industrial and Applied Mathematics 5(2) (1957) 74-88"
    locator: the three-term recurrence for polynomials orthogonal on a discrete point set and its use for fitting
  - book: isbn:9781611975932
    title: Lloyd N. Trefethen, Approximation Theory and Approximation Practice, extended edition, SIAM, 2019
    locator: Chapter 16, Best and near-best (Theorem 16.1 on Chebyshev projection and interpolation)
---

Least-squares approximation chooses, from a linear family $V$ of functions, the member $v^*$ that minimizes the squared error $\|f - v\|_2^2$, an integral $\int_a^b |f - v|^2 w$ for a function or a sum $\sum_i w_i |y_i - v(x_i)|^2$ for data. The minimizer exists, is unique, and is characterized by the condition that the error $f - v^*$ is orthogonal to every element of $V$. With an [orthogonal basis](/orthogonal-polynomials/) the coefficients are independent inner products; with a poor basis, such as monomials, the [normal equations](/normal-equations/) are badly conditioned and must be avoided.

## In plain words

You want a simple curve, such as a straight line or a low-degree polynomial, that stays close to a function or to a cloud of measured points. You cannot make it pass through every point, so you ask for the curve that makes the total of the squared misses as small as possible. Squaring makes every miss count as positive and punishes big misses more than small ones.

The best curve has a neat geometric property: what is left over, the error, has no part that the family of curves could still remove. In the language of geometry the error is perpendicular to the family. With a well-chosen set of building blocks, each coefficient of the answer can be computed on its own, from one average of the data.

## Definition

Notation on the interpolation and approximation pages: $f$ is a function on $[a, b]$, usually $[-1, 1]$; the data are $(x_i, y_i)$ with $y_i = f(x_i)$ plus possible noise; $\mathcal{P}_n$ is the set of polynomials of degree at most $n$; costs are arithmetic operations, with the leading term.

**Input.** An inner product on real functions on $[a, b]$, either continuous
$$\langle g, h \rangle = \int_a^b g(x)\, h(x)\, w(x)\, dx \quad (w > 0 \text{ except on a null set, integrable}),$$
or discrete
$$\langle g, h \rangle = \sum_{i=1}^{m} w_i\, g(x_i)\, h(x_i) \quad (w_i > 0);$$
a function $f$ with $\|f\|_2 = \langle f, f \rangle^{1/2} < \infty$ (in the discrete case only the values $y_i = f(x_i)$ matter); and linearly independent functions $\varphi_0, \ldots, \varphi_n$ that span $V$. In the discrete case, independence means that the $m \times (n + 1)$ matrix $A_{ij} = \varphi_j(x_i)$ has full column rank, so $m \ge n + 1$; for $V = \mathcal{P}_n$ this holds when there are at least $n + 1$ distinct points.

**Output.** $v^* = \sum_j c_j \varphi_j$ that minimizes $\|f - v\|_2$ over $v \in V$.

**Theorem (characterization).** $v^* \in V$ is a minimizer if and only if $\langle f - v^*, \varphi_j \rangle = 0$ for $j = 0, \ldots, n$. The minimizer exists and is unique, and its coefficients solve the normal equations
$$G c = b, \qquad G_{jk} = \langle \varphi_k, \varphi_j \rangle, \qquad b_j = \langle f, \varphi_j \rangle.$$

*Proof.* Suppose $e = f - v^*$ is orthogonal to $V$. For any $v \in V$, $v^* - v \in V$, so $\|f - v\|_2^2 = \|e + (v^* - v)\|_2^2 = \|e\|_2^2 + \|v^* - v\|_2^2$, which is greater than $\|e\|_2^2$ unless $v = v^*$. So $v^*$ is the unique minimizer. Conversely, if $\langle e, \varphi_j \rangle = \alpha \ne 0$ for some $j$, then for small $t$ with the sign of $\alpha$, $\|e - t\varphi_j\|_2^2 = \|e\|_2^2 - 2t\alpha + t^2 \|\varphi_j\|_2^2 < \|e\|_2^2$, so $v^*$ is not a minimizer. Finally, $G$ is a Gram matrix of independent functions: $c^{T} G c = \|\sum_j c_j \varphi_j\|_2^2 > 0$ for $c \ne 0$, so $G$ is [positive definite](/positive-definite-matrix/), and $G c = b$, which is the orthogonality condition, has exactly one solution. $\blacksquare$

**Orthogonal bases.** If $\langle \varphi_j, \varphi_k \rangle = 0$ for $j \ne k$, then $G$ is diagonal and
$$c_j = \frac{\langle f, \varphi_j \rangle}{\langle \varphi_j, \varphi_j \rangle}, \qquad \|f - v^*\|_2^2 = \|f\|_2^2 - \sum_{j=0}^{n} c_j^2\, \|\varphi_j\|_2^2.$$
Each $c_j$ does not depend on $n$, so raising the degree adds terms without changing the old ones. For $V = \mathcal{P}_n$ on $[-1, 1]$ with $w = 1$ the orthogonal basis is the [Legendre polynomials](/legendre-polynomials/); with $w = (1 - x^2)^{-1/2}$ it is the [Chebyshev polynomials](/chebyshev-polynomials/), and the answer is the truncated [Chebyshev series](/chebyshev-series/).

## Variants

- **Continuous or discrete.** The continuous problem approximates a known function; the discrete problem fits data and is the matrix [least-squares problem](/least-squares-problem/) $\min_c \|W^{1/2}(Ac - y)\|_2$.
- **Polynomial, trigonometric, spline.** $V = \mathcal{P}_n$; trigonometric polynomials, where the answer is the truncated Fourier series; or splines with fixed knots, the basis of [B-spline fitting](/b-spline-fitting/).
- **Weighted.** The weight $w$ or $w_i$ puts more trust in some regions or data points; with $w_i$ equal to the inverse variance of the noise, the fit is the best linear unbiased estimate (the Gauss and Markov theorem).
- **Regularized.** Add $\lambda \|Lc\|_2^2$ to the objective ([Tikhonov regularization](/tikhonov-regularization/), [ridge regression](/ridge-regression/), [smoothing splines](/smoothing-spline/)).
- **Nonlinear least squares.** The model depends nonlinearly on its parameters, for example $c_0 e^{c_1 x}$; this needs an iteration and is outside this page.
- **Other norms.** The maximum norm gives [minimax approximation](/minimax-approximation/); the $L^1$ norm gives robust fits.

## Examples

**A line through four points.** The data $(0, 1), (1, 3), (2, 4), (3, 4)$ with $w_i = 1$ and $V = \mathcal{P}_1$ give the normal equations
$$\begin{pmatrix} 4 & 6 \\ 6 & 14 \end{pmatrix} \begin{pmatrix} c_0 \\ c_1 \end{pmatrix} = \begin{pmatrix} 12 \\ 23 \end{pmatrix},$$
with the solution $c_0 = 3/2$, $c_1 = 1$. The residuals are $-\tfrac{1}{2}, \tfrac{1}{2}, \tfrac{1}{2}, -\tfrac{1}{2}$, their sum and their sum weighted by $x_i$ are 0 (orthogonality to $1$ and to $x$), and the minimal sum of squares is 1.

**The best $L^2$ line for $e^x$ on $[-1, 1]$.** With $w = 1$ and the Legendre basis $P_0 = 1$, $P_1 = x$, $\|P_0\|^2 = 2$, $\|P_1\|^2 = 2/3$: $c_0 = \tfrac{1}{2}\int_{-1}^1 e^x\,dx = \sinh 1 \approx 1.1752$ and $c_1 = \tfrac{3}{2}\int_{-1}^1 x e^x\,dx = 3/e \approx 1.1036$. The $L^2$ error is about $0.229$ and the maximum error about $0.439$; the [minimax](/minimax-approximation/) line has maximum error $0.279$ but $L^2$ error $0.268$ (see [approximation theory](/approximation-theory/)).

**The monomial basis is a trap.** With $\varphi_j = x^j$ on $[0, 1]$ and $w = 1$, the Gram matrix is $G_{jk} = 1/(j + k + 1)$, the [Hilbert matrix](/hilbert-matrix/). Its condition number in the $\infty$-norm is $748$ for size 3, $943\,656$ for size 5 and about $3.5 \times 10^{13}$ for size 10. Fitting $e^x$ on $[0, 1]$ in $\mathcal{P}_9$ this way in double precision, with exact right-hand sides, gives coefficients with errors up to $6 \times 10^{-5}$ and a polynomial that is off by $1.7 \times 10^{-10}$, although the exact least-squares polynomial is within $2.5 \times 10^{-12}$ of $e^x$. With Legendre polynomials (shifted to $[0, 1]$) the Gram matrix is diagonal and this loss does not occur.

**A non-example.** Fitting $y = c_0 e^{c_1 x}$ is not a linear least-squares problem, because the model is not linear in $c_1$. Taking logarithms gives a linear problem for $\log y$, but its minimizer is not the least-squares fit to $y$.

## Known algorithms

For the discrete problem with $m$ points and $n + 1$ basis functions:

- [Normal equations](/normal-equations/) with [Cholesky](/cholesky-decomposition/): about $m n^2 + n^3/3$ flops. The condition number of $A^T A$ is $\kappa_2(A)^2$, so this is accurate only for a well-conditioned basis.
- [Householder QR](/householder-reflections/): about $2 m n^2 - \tfrac{2}{3} n^3$ flops; backward stable (Higham, Chapter 20). The standard method; see [QR decomposition](/qr-decomposition/).
- [Gram-Schmidt](/gram-schmidt-process/) in its modified form, or the singular value decomposition when $A$ may be rank deficient ([pseudoinverse](/pseudoinverse/)).
- Orthogonal polynomials on the data points by the three-term recurrence (Forsythe 1957): $O(mn)$ operations for a polynomial fit, with each coefficient an independent inner product.

For the continuous problem, the inner products are integrals: use an orthogonal basis and a [Gauss quadrature](/gaussian-quadrature/) rule for $\langle f, \varphi_j \rangle$, or sample at many points and solve the discrete problem.

## Bounds

- **Cost.** QR needs $\Theta(m n^2)$ operations for dense $A$; the orthogonal polynomial recurrence needs $\Theta(m n)$ for polynomial fits.
- **Accuracy.** Householder QR computes the exact solution of a problem with a relative backward error of order $m n u$ in $A$ and $y$. The sensitivity of the solution is of order $\kappa_2(A) + \kappa_2(A)^2 \tan\theta$, where $\theta$ is the angle between $y$ and the range of $A$ (Golub and Van Loan, Chapter 5; Higham, Chapter 20). The normal equations have a forward error of order $\kappa_2(A)^2 u$ even when the residual is zero.
- **Approximation.** For $V = \mathcal{P}_n$ and the Chebyshev weight, the least-squares polynomial (the truncated Chebyshev series) has maximum error at most $(4 + \tfrac{4}{\pi^2}\log(n+1)) E_n(f)$, where $E_n(f)$ is the minimax error (Trefethen, Theorem 16.1).

## Reductions

- **To a linear system.** The normal equations $Gc = b$, a symmetric positive definite system.
- **To an orthogonal factorization.** The discrete problem reduces to $A = QR$ and the triangular system $Rc = Q^T y$ ([back substitution](/back-substitution/)).
- **To interpolation.** When $m = n + 1$ and the basis is unisolvent on the points, the least-squares fit is the [interpolant](/interpolation-problem/) and the residual is zero.

## Applications

- Data fitting and [linear regression](/linear-regression/) in statistics, and [curve fitting](/curve-fitting/) of measurements.
- Spectral methods and Galerkin methods for differential equations, which are least-squares projections in an energy inner product.
- Signal processing: Fourier truncation is the $L^2$ best trigonometric approximation; least-squares filter design.
- Compression: keep the largest coefficients in an orthogonal basis.

## References
