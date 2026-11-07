---
tag: Y0XTDM
kind: problem
slug: least-squares-problem
name: Linear least squares
aliases:
- Least squares problem
- linear least squares
- linear regression fitting
- overdetermined linear system
- LLS
area: numerical/linear-systems
level: core
summary: Minimize ||Ax - b||_2 for an overdetermined or rank-deficient A.
model: floating-point-model
complexity:
  vars: {m: "the number of rows of A", n: "the number of columns of A (n ≤ m)"}
  time: {worst: O(m n^2)}
  flops: {worst: "2 m n^2 - 2n^3/3 + O(m n)"}
prereqs: [linear-system-solving, matrix-norms, condition-number]
see_also: [normal-equations, householder-reflections, gram-schmidt-process, givens-rotations, pseudoinverse, singular-value-decomposition, tikhonov-regularization, least-squares-approximation]
sources:
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 20, The Least Squares Problem (Section 20.1, perturbation theory, Theorem 20.1; Section 20.2, solution by QR factorization, Theorem 20.3; Section 20.3, MGS; Section 20.4, the normal equations; Section 20.5, iterative refinement; Section 20.7, backward error)
  - book: isbn:9780898713602
    title: Åke Björck, Numerical Methods for Least Squares Problems, SIAM, 1996
    locator: Chapter 1, Mathematical and Statistical Properties of Least Squares Solutions; Chapter 2, Basic Numerical Methods
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 11, Least Squares Problems; Lecture 18, Conditioning of Least Squares Problems (Theorem 18.1); Lecture 19, Stability of Least Squares Algorithms
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 5.3, The Full-Rank Least Squares Problem; Section 5.4, Other Orthogonal Factorizations; Section 5.5, The Rank-Deficient Least Squares Problem
  - paper: doi:10.1007/BF01436075
    title: Gene H. Golub, Numerical methods for solving linear least squares problems, Numerische Mathematik 7, 1965
    locator: pp. 206 to 216 (Householder QR for least squares, avoiding the normal equations)
  - paper: doi:10.1007/BF01933494
    title: Per-Åke Wedin, Perturbation theory for pseudo-inverses, BIT 13, 1973
    locator: pp. 217 to 232 (the κ^2 tan θ term in the sensitivity of the solution)
  - paper: "Bo Waldén, Rune Karlsson and Ji-guang Sun, Optimal backward perturbation bounds for the linear least squares problem, Numerical Linear Algebra with Applications 2(3), 1995"
    locator: pp. 271 to 286 (the exact normwise backward error of an approximate least squares solution)
  - book: "Carl Friedrich Gauss, Theoria motus corporum coelestium in sectionibus conicis solem ambientium, Perthes and Besser, Hamburg, 1809"
    locator: Book 2, Section 3 (the method of least squares and its probabilistic justification)
---

The linear least squares problem asks, for an $m \times n$ matrix $A$ with $m \ge n$ and a vector $b \in \mathbb{R}^m$, for $x \in \mathbb{R}^n$ minimizing $\|b - A x\|_2$. It is the standard way to fit a model with $n$ parameters to $m$ noisy observations. A minimizer always exists, it is unique exactly when $A$ has full column rank, and it is characterized by the orthogonality of the residual to the columns of $A$, that is by the [normal equations](/normal-equations/) $A^T A x = A^T b$. The numerical question is which way of computing $x$ keeps the error near what the conditioning allows, which here depends on $\kappa_2(A)$, on $\kappa_2(A)^2$ and on the size of the residual.

## In plain words

When there are more equations than unknowns, there is usually no exact solution: measurements disagree a little. Least squares picks the answer that makes the total of the squared misfits as small as possible. Geometrically, the best fit is the point in the space of possible predictions that is closest to the data, and the misfit then points straight away from that space.

Fitting a straight line through scattered points is the simplest case. The method is easy to state, but on a computer the obvious formula squares the sensitivity to rounding, so careful codes use orthogonal transformations instead.

## Definition

**Notation.** As in [solving linear systems](/linear-system-solving/): $u = 2^{-53}$, hats for computed quantities. $A \in \mathbb{R}^{m \times n}$, $m \ge n$, $b \in \mathbb{R}^m$, $r = b - A x$ the residual, $\kappa_2(A) = \sigma_{\max}(A) / \sigma_{\min}(A)$, $A^+$ the [pseudoinverse](/pseudoinverse/). For the exact solution $x$, $\theta \in [0, \pi/2]$ is the angle between $b$ and $\operatorname{range}(A)$, so $\sin \theta = \|r\|_2 / \|b\|_2$, and $\eta = \|A\|_2 \|x\|_2 / \|A x\|_2 \in [1, \kappa_2(A)]$.

**Input:** $A$ and $b$. **Output:** $x$ minimizing $\|b - A x\|_2$; if $A$ is rank deficient, the minimizer of least 2-norm, $x = A^+ b$.

Facts, all standard (Björck, Chapter 1):

1. **Characterization.** $x$ is a minimizer if and only if $A^T (b - A x) = 0$. Proof: for any $y$, $\|b - A(x + y)\|_2^2 = \|r\|_2^2 - 2 y^T A^T r + \|A y\|_2^2$, which is at least $\|r\|_2^2$ for all $y$ exactly when $A^T r = 0$.
2. **Uniqueness.** If $\operatorname{rank} A = n$, then $A^T A$ is positive definite and $x = (A^T A)^{-1} A^T b$ is unique. The residual $r$ and the fitted vector $A x$ are unique in every case.
3. **QR form.** If $A = Q R$ with $Q \in \mathbb{R}^{m \times n}$ orthonormal and $R$ nonsingular, then $x = R^{-1} Q^T b$ and $\|r\|_2 = \|(I - Q Q^T) b\|_2$.
4. **Sensitivity (Trefethen and Bau, Theorem 18.1; Wedin 1973).** For $A$ of full rank and $\theta < \pi/2$, the relative condition number of $x$ is $\kappa_2(A) / (\eta \cos \theta)$ with respect to $b$ and
$$\kappa_2(A) + \frac{\kappa_2(A)^2 \tan \theta}{\eta}$$
with respect to $A$. So a small residual ($\theta$ near 0) gives sensitivity $\kappa_2(A)$, as for a square system, while a large residual brings in $\kappa_2(A)^2$. Higham, Theorem 20.1, gives the corresponding normwise bound for simultaneous perturbations of $A$ and $b$.
5. **Backward error.** For an approximate $y$, the smallest $\|\Delta A\|_F$ that makes $y$ an exact least squares solution of $(A + \Delta A, b)$ has a closed form (Waldén, Karlsson and Sun 1995; Higham, Section 20.7). Unlike for square systems, $\|b - A y\|_2$ alone does not measure it, since the optimal residual is not zero.

## Variants

- **Rank-deficient problems.** Seek $x = A^+ b$, via the [SVD](/singular-value-decomposition/) or a [rank-revealing factorization](/rank-revealing-factorization/) with a rank tolerance.
- **Underdetermined problems** ($m < n$, full row rank): the minimum-norm solution of $A x = b$, $x = A^T (A A^T)^{-1} b$, computed from a QR factorization of $A^T$.
- **Weighted and generalized least squares.** Minimize $\|W^{1/2}(b - A x)\|_2$, or the Gauss-Markov model with a covariance matrix.
- **Regularized problems.** [Tikhonov regularization](/tikhonov-regularization/) (ridge regression) minimizes $\|b - A x\|_2^2 + \lambda^2 \|x\|_2^2$, which is an ordinary least squares problem for $\begin{pmatrix} A \\ \lambda I \end{pmatrix}$.
- **Constrained problems.** Equality constraints $C x = d$ (LSE), nonnegativity (NNLS), bounds.
- **Total least squares.** Errors in $A$ too; solved with the SVD of $[A \; b]$.
- **Sparse and large problems.** Solved by sparse QR or by iterative methods on the normal equations (CGLS, LSQR) or by row projections ([Kaczmarz](/kaczmarz-method/)).
- **Other norms.** $\ell_1$ and $\ell_\infty$ fits are linear programs; nonlinear least squares is solved by sequences of linear ones (Gauss-Newton).

## Examples

- **A line through three points.** Fit $y = x_0 + x_1 t$ to $(0, 1)$, $(1, 2)$, $(2, 4)$: $A = \begin{pmatrix} 1 & 0 \\ 1 & 1 \\ 1 & 2 \end{pmatrix}$, $b = (1, 2, 4)$. The normal equations $\begin{pmatrix} 3 & 3 \\ 3 & 5 \end{pmatrix} x = \begin{pmatrix} 7 \\ 10 \end{pmatrix}$ give $x = (5/6, 3/2)$ and $r = (1/6, -1/3, 1/6)$, and indeed $A^T r = 0$. The implementation of [Gram-Schmidt](/gram-schmidt-process/) reproduces these numbers to within $10^{-14}$.
- **Normal equations destroy information.** For the Läuchli matrix $A = \begin{pmatrix} 1 & 1 & 1 \\ \varepsilon & 0 & 0 \\ 0 & \varepsilon & 0 \\ 0 & 0 & \varepsilon \end{pmatrix}$ with $\varepsilon = 10^{-8}$, $A$ has full rank and $\kappa_2(A) \approx 1.7 \times 10^8$, so $u \kappa_2(A) \approx 2 \times 10^{-8}$ and QR methods solve the problem with about 8 correct digits. But $A^T A$ has diagonal entries $1 + \varepsilon^2$, which round to $1$: the computed $A^T A$ is the all-ones matrix, exactly singular, and the [Cholesky decomposition](/cholesky-decomposition/) breaks down.
- **Polynomial fitting.** Fitting a polynomial of degree $n - 1$ in the monomial basis on many equally spaced points in $[0, 1]$ gives $A^T A / m \approx H_n$, the [Hilbert matrix](/hilbert-matrix/), with $\kappa_2(H_{10}) \approx 1.6 \times 10^{13}$. QR on $A$ works with $\kappa_2(A) \approx \kappa_2(H_n)^{1/2}$; better still is an [orthogonal polynomial](/orthogonal-polynomials/) basis.
- **Zero residual.** If $b \in \operatorname{range}(A)$, then $\theta = 0$ and the problem is as well conditioned as a square system with matrix $A$; the normal equations are still worse, with forward error of order $u \kappa_2(A)^2$.

## Known algorithms

| method | flops (leading term) | stability |
|---|---|---|
| [Normal equations](/normal-equations/) with [Cholesky](/cholesky-decomposition/) | $m n^2 + n^3/3$ | not backward stable; forward error of order $u \kappa_2(A)^2$ even when the residual is small (Higham, Section 20.4) |
| [Householder](/householder-reflections/) QR | $2 m n^2 - 2n^3/3$ | backward stable: $\hat x$ solves a problem with $\|\Delta a_j\|_2 \le \gamma_{c m n} \|a_j\|_2$ and a small $\Delta b$ (Higham, Theorem 20.3) |
| [Givens](/givens-rotations/) QR | $3 m n^2 - n^3$ | backward stable; preferred for sparse or structured $A$ and for updating |
| [MGS](/gram-schmidt-process/) on $[A \; b]$ | $2 m n^2$ | backward stable for $x$ (Björck 1967), although $\hat Q$ is not orthogonal |
| [SVD](/singular-value-decomposition/) | about $2 m n^2 + 11 n^3$ (R-SVD, Golub and Van Loan) | backward stable; handles rank deficiency |
| QR with column pivoting | $4 m n r - 2 r^2 (m + n) + 4 r^3/3$ for rank $r$ | reliable rank decisions in practice |
| CGLS or LSQR | two matvecs per step | iterative; the convergence depends on $\kappa_2(A)$, not on its square in exact arithmetic |
| [Iterative refinement](/iterative-refinement/) on the augmented system | $O(m n)$ per step after a QR | recovers accuracy for large residuals (Björck 1967) |

The forward error of every backward stable method is bounded by about $u$ times the condition number of fact 4. So for small residuals QR beats the normal equations by a factor $\kappa_2(A)$; for large residuals ($\tan \theta \gtrsim 1$) both errors are of order $u \kappa_2(A)^2$, and the faster normal equations are acceptable if $A^T A$ can be formed without breaking down.

## Bounds

Reading the input takes $\Omega(m n)$ time. Householder QR solves the dense problem in $O(m n^2)$ flops; with fast matrix multiplication the exponent of $n$ can be reduced, but no practical code does so. When $m \gg n$, randomized sketching (Rokhlin and Tygert 2008; Avron, Maymounkov and Toledo 2010) reduces the cost to $O(m n \log m + n^3)$ for a backward stable solution, using the sketch to precondition LSQR.

## Reductions

- **To a square system.** The augmented system $\begin{pmatrix} I & A \\ A^T & 0 \end{pmatrix} \begin{pmatrix} r \\ x \end{pmatrix} = \begin{pmatrix} b \\ 0 \end{pmatrix}$ is a symmetric indefinite linear system of order $m + n$ that is equivalent to fact 1. Scaling the identity block by $\alpha \approx \sigma_{\min}(A)/\sqrt 2$ minimizes its condition number (Björck 1967). The normal equations are the Schur complement of this system.
- **From a square system.** If $m = n$ and $A$ is nonsingular, the least squares solution is the solution of $A x = b$, so [solving linear systems](/linear-system-solving/) is the special case with zero residual.
- **To orthogonal factorization.** Facts 2 and 3 reduce the problem to a [QR decomposition](/qr-decomposition/) and a [back substitution](/back-substitution/).

## Applications

Linear regression and the general linear model in statistics ([linear regression](/linear-regression/), [ridge regression](/ridge-regression/)); data fitting and [least squares approximation](/least-squares-approximation/) of functions; geodesy and GPS positioning, which motivated Gauss; parameter estimation in control and signal processing, including adaptive filters; the inner step of Gauss-Newton methods for nonlinear least squares; and the projection steps of Krylov solvers such as [GMRES](/gmres/), which solve a small least squares problem at each step.

## References
