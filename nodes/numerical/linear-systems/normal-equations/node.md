---
tag: FJBYRZ
kind: algorithm
slug: normal-equations
name: Normal equations
aliases:
- A^T A x = A^T b
- Normal equations method
- method of normal equations
- Cholesky least squares
area: numerical/linear-systems
level: core
summary: Solve A^T A x = A^T b for least squares; fast but squares the condition number.
solves: [least-squares-problem]
model: floating-point-model
complexity:
  vars: {m: "the number of rows of A", n: "the number of columns of A, with 1 <= n <= m"}
  time: {worst: Θ(m n^2), best: Θ(m n^2)}
  space: {extra: Θ(n^2)}
  flops: {worst: "m n^2 + n^3/3"}
properties: {deterministic: true, in_place: false, recursive: false}
prereqs: [least-squares-problem, cholesky-decomposition, condition-number]
see_also: [qr-decomposition, singular-value-decomposition, pseudoinverse, tikhonov-regularization, positive-definite-matrix, iterative-refinement, conjugate-gradient-method, triangular-system-solving]
sources:
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 20, The Least Squares Problem (Section 20.1, perturbation theory; Section 20.4, the normal equations and their forward error; Section 20.6, the seminormal equations); Chapter 10, Cholesky factorization (the backward error of the Cholesky solve)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 5.3, The Full-Rank Least Squares Problem (the method of normal equations, its flop count, its accuracy compared with Householder QR, and the Läuchli example)
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 11, Least Squares Problems (the normal equations, QR and SVD methods); Lecture 18, Conditioning of Least Squares Problems; Lecture 19, Stability of Least Squares Algorithms (the normal equations are unstable)
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Section 3.2, Matrix Factorizations That Solve the Linear Least Squares Problem (normal equations); Section 3.3, Perturbation Theory for the Least Squares Problem
  - paper: doi:10.1007/BF01436075
    title: Gene H. Golub, Numerical methods for solving linear least squares problems, Numerische Mathematik 7, 1965
    locator: the case for Householder QR instead of the normal equations
---

The method of normal equations solves the [least squares problem](/least-squares-problem/) $\min_x \|b - A x\|_2$, for $A \in \mathbb{R}^{m \times n}$ of full column rank, by forming the $n \times n$ matrix $C = A^T A$ and the vector $d = A^T b$ and solving $C x = d$ by [Cholesky factorization](/cholesky-decomposition/). It costs about $m n^2 + n^3/3$ flops, about half of [Householder QR](/qr-decomposition/) when $m \gg n$. Its weakness is that $\kappa_2(A^T A) = \kappa_2(A)^2$: the computed solution has a forward error of order $\kappa_2(A)^2 u$ even when the residual is zero, and Cholesky can break down once $\kappa_2(A)$ reaches about $u^{-1/2} \approx 10^8$.

## In plain words

To fit a model to more data than unknowns, you look for the coefficients that make the misfit as small as possible. At the best fit, the leftover misfit points in a direction that no change of the coefficients can reach. Writing that down gives a small square system with one equation per unknown, and this square system is symmetric and positive, so it has a fast and simple solver. The catch is that building the small system multiplies the data by itself. Any near dependence between the columns becomes twice as bad, and about half of the reliable digits can be lost before the solver even starts.

## The problem

Given $A \in \mathbb{R}^{m \times n}$ with $m \ge n$ and $\operatorname{rank}(A) = n$, and $b \in \mathbb{R}^m$, find the unique $x$ that minimizes $\|b - A x\|_2$.

**Notation.** $x$ is the exact solution, $\hat x$ the computed one, $r = b - A x$ the optimal residual. $\kappa_2(A) = \sigma_1/\sigma_n$ is the ratio of the largest and smallest singular values, $u = 2^{-53}$ is the unit roundoff of binary64, and $\gamma_k = k u/(1 - k u)$. The general notation of this area is on the page [linear system solving](/linear-system-solving/).

**Why the normal equations hold.** For each $y$, $\|b - A(x + y)\|_2^2 = \|r\|_2^2 - 2 y^T A^T r + \|A y\|_2^2$. If $A^T r = 0$, the middle term vanishes and $x$ is a minimizer; since $A$ has full column rank, $\|A y\|_2 > 0$ for $y \ne 0$, so it is the only one. Conversely, at a minimizer the derivative $-2 A^T r$ must vanish. So $x$ is the least squares solution if and only if $A^T A x = A^T b$. The matrix $C = A^T A$ is symmetric, and $v^T C v = \|A v\|_2^2 > 0$ for $v \ne 0$, so it is [positive definite](/positive-definite-matrix/).

## The algorithm

```pseudo id=main
NORMAL-EQUATIONS(A, b)                        ▷ A is m × n, m ≥ n, full column rank
L1  C ← A^T A                                 ▷ only the lower triangle: c_ij = Σ_k a_ki a_kj, i ≥ j
L2  d ← A^T b
L3  R ← CHOLESKY(C)                           ▷ R^T R = C; report "not full rank" if a pivot is ≤ 0
L4  solve R^T y = d by forward substitution
L5  solve R x = y by back substitution; return x
```

Line L1 computes only the $n(n+1)/2$ entries on and below the diagonal and mirrors them. Line L3 is the column-oriented Cholesky factorization; a pivot that is zero or negative in floating point means that the computed $C$ is not numerically positive definite, and the method stops. Lines L4 and L5 are two [triangular solves](/triangular-system-solving/).

## Example

**A line fit.** Fit $y = x_1 + x_2 t$ to the points $(1, 1)$, $(2, 2)$, $(3, 2)$. Then

$$A = \begin{pmatrix} 1 & 1 \\ 1 & 2 \\ 1 & 3 \end{pmatrix}, \quad b = \begin{pmatrix} 1 \\ 2 \\ 2 \end{pmatrix}, \quad C = \begin{pmatrix} 3 & 6 \\ 6 & 14 \end{pmatrix}, \quad d = \begin{pmatrix} 5 \\ 11 \end{pmatrix}.$$

Line L3 gives $r_{11} = \sqrt3$, $r_{12} = 6/\sqrt3 = 2\sqrt3$, $r_{22} = \sqrt{14 - 12} = \sqrt2$. Line L4 gives $y_1 = 5/\sqrt3$, $y_2 = (11 - 2\sqrt3 \cdot 5/\sqrt3)/\sqrt2 = 1/\sqrt2$. Line L5 gives $x_2 = 1/2$ and $x_1 = (5/\sqrt3 - 2\sqrt3 \cdot \tfrac12)/\sqrt3 = 2/3$. The residual is $r = b - A x = (-\tfrac16, \tfrac13, -\tfrac16)^T$, and $A^T r = 0$ as the theory requires.

**The Läuchli matrix.** For

$$A = \begin{pmatrix} 1 & 1 \\ \varepsilon & 0 \\ 0 & \varepsilon \end{pmatrix}, \qquad A^T A = \begin{pmatrix} 1 + \varepsilon^2 & 1 \\ 1 & 1 + \varepsilon^2 \end{pmatrix},$$

with $\varepsilon = 10^{-8}$, $\varepsilon^2 = 10^{-16} < u$, so $\mathrm{fl}(1 + \varepsilon^2) = 1$ and the computed $C$ is the singular matrix of all ones. Line L3 finds the pivot $1 - 1 = 0$ and stops. Yet $\kappa_2(A) = \sqrt{2 + \varepsilon^2}/\varepsilon \approx 1.4 \cdot 10^8$, well below $u^{-1}$, and Householder QR solves the problem with $b = (2, \varepsilon, \varepsilon)^T$ to a relative error of order $10^{-8}$ or better. The information was lost in line L1, before any solving.

**Polynomial fitting.** Fit a polynomial of degree $n - 1$ at the $21$ points $t_i = i/20$, with $A_{ij} = t_i^{j}$ and $b$ chosen so that $x = (1, \ldots, 1)$ with zero residual. The table gives the relative forward error in the $\infty$-norm, against the exact rational solution, for the normal equations and for Householder QR in binary64 (observed values; $\kappa_2(A)$ computed in 80-digit decimal arithmetic).

| $n$ | $\kappa_2(A)$ | normal equations | Householder QR |
|---|---|---|---|
| 4 | $1.1 \cdot 10^2$ | $5.0 \cdot 10^{-13}$ | $2.0 \cdot 10^{-15}$ |
| 6 | $3.3 \cdot 10^3$ | $1.2 \cdot 10^{-10}$ | $1.8 \cdot 10^{-14}$ |
| 8 | $1.1 \cdot 10^5$ | $2.8 \cdot 10^{-7}$ | $1.2 \cdot 10^{-12}$ |
| 10 | $3.7 \cdot 10^6$ | $2.4 \cdot 10^{-4}$ | $4.0 \cdot 10^{-10}$ |
| 12 | $1.5 \cdot 10^8$ | $3.1 \cdot 10^{-1}$ | $3.6 \cdot 10^{-9}$ |

The normal equations lose about $2 \log_{10}\kappa_2(A)$ digits and QR about $\log_{10}\kappa_2(A)$, as the bounds below predict.

## Correctness

**Exact arithmetic.** $C$ is positive definite, so Cholesky succeeds and $R$ has a positive diagonal. Lines L4 and L5 give $R^T R x = d$, that is $A^T A x = A^T b$, and by the argument of The problem this $x$ is the unique least squares solution. The details are in [the proof](proofs/correctness.md).

**Floating point (proved, Higham, Section 20.4).** In the [standard model](/floating-point-model/), line L1 gives $\hat C = C + E_1$ with $|E_1| \le \gamma_m |A|^T |A|$ and line L2 gives $\hat d = d + f$ with $|f| \le \gamma_m |A|^T |b|$. If Cholesky runs to completion, the solve gives $(\hat C + E_2)\hat x = \hat d$ with $\|E_2\|_2 \le c_n u \|\hat C\|_2$, where $c_n$ is a low-degree polynomial in $n$ (Higham, Chapter 10). Since $\| |A| \|_2 \le \sqrt n \|A\|_2$, all three perturbations are of order $m n u$ relative to $\|A\|_2^2$ and $\|A\|_2\|b\|_2$, and the perturbation bound for the square system $C x = d$ gives, to first order,

$$\frac{\|x - \hat x\|_2}{\|x\|_2} \lesssim c_{m,n}\, u\, \kappa_2(A)^2 \left(1 + \frac{\|b\|_2}{\|A\|_2 \|x\|_2}\right),$$

with $c_{m,n}$ of order $m n + n^2$. This is a worst-case bound; the table above shows that the factor $\kappa_2(A)^2$ is really seen. For comparison, a backward stable method such as Householder QR has a forward error of order $u\,(\kappa_2(A) + \kappa_2(A)^2 \tan\theta / \eta)$, where $\theta$ is the angle between $b$ and its projection $A x$, and $\eta = \|A\|_2\|x\|_2/\|A x\|_2 \ge 1$ (Trefethen and Bau, Lecture 18). When the residual is small, QR is much better; when $\tan\theta$ is of order one or larger, both errors are of order $\kappa_2(A)^2 u$.

**Breakdown.** Cholesky succeeds in floating point if $c_n u\, \kappa_2(\hat C) < 1$ for a modest $c_n$ (Higham, Chapter 10). Since $\kappa_2(C) = \kappa_2(A)^2$, the method is safe when $\kappa_2(A)$ is well below $u^{-1/2} \approx 10^8$, and the Läuchli example shows that it can fail at that size.

**Not backward stable.** Higham (Section 20.4) and Trefethen and Bau (Lecture 19) show that the computed $\hat x$ is in general not the exact least squares solution for a nearby $A + \Delta A$ with $\|\Delta A\| = O(u)\|A\|$. The Cholesky stage is backward stable for $C$, but the formation of $C$ is not backward stable for $A$.

## Complexity

Line L1 computes $n(n+1)/2$ inner products of length $m$, $m n^2 + O(m n)$ flops. Line L2 costs $2 m n$, line L3 $n^3/3 + O(n^2)$, and lines L4 and L5 $2 n^2$. The total is $m n^2 + n^3/3$ to leading order, against $2 m n^2 - 2n^3/3$ for Householder QR. For $m \gg n$ the normal equations are about twice as fast; for $m = n$ they cost $4n^3/3$ against $4n^3/3$, no gain. The storage is the $n \times n$ array $C$, overwritten by $R$, and $A$ is read once in a stream. Line L1 is a symmetric rank-$k$ update (`xSYRK`), a matrix-matrix operation that runs near the peak flop rate, and it can be accumulated row by row when $A$ is too big for memory or arrives as a stream.

## Properties

- **Speed and simplicity.** One pass over $A$, then a small dense problem.
- **The condition number is squared**, in the bound and in practice, regardless of the residual.
- **Not backward stable**, but the error is within the bound above whenever Cholesky completes.
- **Sparse friendly in part.** If $A$ is sparse, $A^T A$ is often sparse too and can be factored by sparse Cholesky, but a single dense row of $A$ makes $A^T A$ dense.
- **Updating.** Adding a row $a^T$ to $A$ adds $a a^T$ to $C$ and $a\, b_i$ to $d$, so the normal equations can be accumulated incrementally.

## Variants and improvements

- **Seminormal equations.** Compute $R$ by QR but solve $R^T R x = A^T b$ without storing $Q$. With one step of [iterative refinement](/iterative-refinement/) in the same precision (corrected seminormal equations), the accuracy is close to that of QR for many problems (Higham, Section 20.6).
- **Higher precision for $C$.** Forming $C$ and $d$ in double the working precision removes the error of line L1, but not the squared condition number of the system that Cholesky then solves.
- **Weighted and regularized forms.** Weighted least squares solves $A^T W A x = A^T W b$; [Tikhonov regularization](/tikhonov-regularization/) solves $(A^T A + \lambda^2 I) x = A^T b$, whose condition number is at most $(\sigma_1^2 + \lambda^2)/\lambda^2$.
- **Iterative methods.** CGLS and LSQR apply the [conjugate gradient method](/conjugate-gradient-method/) to the normal equations without forming $A^T A$, using only products with $A$ and $A^T$. Their convergence depends on $\kappa_2(A)^2$ as well, and LSQR is the more stable of the two in floating point (Paige and Saunders, 1982).
- **Augmented system.** The $(m + n) \times (m + n)$ symmetric indefinite system $\begin{pmatrix} I & A \\ A^T & 0 \end{pmatrix}\begin{pmatrix} r \\ x \end{pmatrix} = \begin{pmatrix} b \\ 0 \end{pmatrix}$ avoids forming $A^T A$; with suitable scaling its solution by a stable method is backward stable.

## When to use it

Use the normal equations when $\kappa_2(A)$ is known to be modest (say below $10^4$ in binary64, so that $\kappa_2(A)^2 u$ is below $10^{-8}$), when $m \gg n$ and speed matters, or when the data arrive as a stream and only $C$ and $d$ can be kept. They are standard in statistics for well-conditioned designs. When the columns of $A$ are nearly dependent, when $A$ is a polynomial or Vandermonde design, or when the residual is small and full accuracy is needed, use [QR](/qr-decomposition/), or the [SVD](/singular-value-decomposition/) if $A$ may be rank deficient.

## Pitfalls

- **Forming $A^T A$ loses information.** Entries of $A$ below $\sqrt u$ times the column norms disappear in line L1, as in the Läuchli matrix.
- **Breakdown is a symptom.** A failed Cholesky in line L3 means that $\kappa_2(A)$ is near $u^{-1/2}$ or $A$ is rank deficient; switching to QR or the SVD is the fix, not adding a tiny shift, which silently regularizes the problem.
- **Scaling the columns.** Column scaling changes $\kappa_2(A)$ and the computed solution. Equilibrating the columns to unit norm is cheap and often reduces $\kappa_2(A)$, and it costs nothing in the exact solution beyond rescaling.
- **The residual by subtraction.** Computing $\|r\|_2^2$ as $b^T b - x^T d$ cancels badly when the residual is small; compute $r = b - A\hat x$ directly.
- **Rank deficiency is not detected reliably.** In floating point a rank-deficient $A$ can give a positive but tiny pivot, and the method then returns a large, meaningless $\hat x$ instead of failing.

## Implementations

## History

Gauss and Legendre derived the normal equations in the early nineteenth century for the adjustment of astronomical and geodetic observations, and Gauss solved them by elimination; Cholesky's square-root method, used by the French army geodesists, was published by Benoit in 1924. The numerical objection came in the 1960s: Läuchli (1961) gave the example above, and Golub (1965) proposed Householder QR for least squares, which avoids forming $A^T A$. The modern error analysis is summarized by Higham (Chapter 20) and Björck's monograph on least squares.

## References
