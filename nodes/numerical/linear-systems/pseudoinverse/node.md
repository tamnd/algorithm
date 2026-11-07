---
tag: 3QHN5A
kind: concept
slug: pseudoinverse
name: Moore-Penrose pseudoinverse
aliases:
- Moore-Penrose inverse
- generalized inverse
- pseudo-inverse
area: numerical/linear-systems
level: core
summary: A generalized inverse A+ giving the minimum-norm least-squares solution x = A+ b.
prereqs: [singular-value-decomposition, least-squares-problem]
see_also: [normal-equations, qr-decomposition, rank-revealing-factorization, tikhonov-regularization, condition-number, matrix-inversion, residual, matrix-norms]
sources:
  - paper: doi:10.1017/S0305004100030401
    title: Roger Penrose, A generalized inverse for matrices, Mathematical Proceedings of the Cambridge Philosophical Society 51(3), 1955
    locator: the four equations that define the generalized inverse uniquely, and its use for the best approximate solution of linear equations
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 5.5, The Rank-Deficient Least Squares Problem (the minimum-norm solution, the pseudoinverse through the SVD, and numerical rank)
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 11, Least Squares Problems (the pseudoinverse of a full rank matrix and the solution by QR and SVD)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 20, The Least Squares Problem (perturbation theory with the pseudoinverse and the rank-deficient case)
---

The Moore-Penrose pseudoinverse of a matrix $A \in \mathbb{R}^{m \times n}$ is the unique $A^+ \in \mathbb{R}^{n \times m}$ that satisfies
$$A A^+ A = A, \qquad A^+ A A^+ = A^+, \qquad (A A^+)^T = A A^+, \qquad (A^+ A)^T = A^+ A.$$
It exists for every matrix, square or not, of any rank, and equals $A^{-1}$ when $A$ is invertible. Its use is $x = A^+ b$: among all least squares solutions of $A x \approx b$, this is the one of smallest 2-norm. In computation it is a definition, not a method: one solves with an SVD or a rank-revealing QR and does not form $A^+$.

## In plain words

An ordinary inverse undoes a matrix, but many matrices cannot be undone: they are not square, or they squash some directions to nothing. The pseudoinverse does the best that can be done. It undoes the matrix on the directions it does not squash, and sends everything else to zero. Applied to a right side that has no exact solution, it returns the answer that comes closest, and if many answers come equally close, it picks the shortest one.

## The idea

**Notation.** $A \in \mathbb{R}^{m \times n}$ of rank $r$, with singular value decomposition $A = U \Sigma V^T$, singular values $\sigma_1 \ge \cdots \ge \sigma_r > 0$, and $u = 2^{-53}$. The general notation of this area ($A$, $b$, $x$, $\hat{x}$, $r = b - A\hat{x}$, $\kappa$) is on the page [linear system solving](/linear-system-solving/).

**Through the SVD.** With $\Sigma^+ \in \mathbb{R}^{n \times m}$ the diagonal matrix with entries $1/\sigma_1, \ldots, 1/\sigma_r$ and zeros elsewhere,
$$A^+ = V \Sigma^+ U^T = \sum_{i=1}^{r} \frac{1}{\sigma_i} v_i u_i^T.$$
The four Penrose equations are checked directly, and they determine $A^+$ uniquely (if $X$ and $Y$ both satisfy them, a short chain of substitutions using the four equations gives $X = X A Y = Y$; Penrose 1955). So $A^+$ inverts $A$ on its row space, maps the orthogonal complement of the range to $0$, $A A^+$ is the orthogonal projector onto $\mathrm{range}(A)$ and $A^+ A$ the orthogonal projector onto $\mathrm{range}(A^T)$.

**Minimum-norm least squares.** For every $b$, the vector $x^+ = A^+ b$ minimizes $\|b - A x\|_2$, and among all minimizers it has the smallest $\|x\|_2$. In the SVD basis, $\|b - A x\|_2^2 = \sum_{i \le r} (u_i^T b - \sigma_i v_i^T x)^2 + \sum_{i > r} (u_i^T b)^2$, so the minimizers are exactly the $x$ with $v_i^T x = u_i^T b/\sigma_i$ for $i \le r$, and the components $v_i^T x$ for $i > r$ are free; setting them to zero gives $x^+$.

**Special forms.** If $A$ has full column rank, $A^+ = (A^T A)^{-1} A^T$, the matrix of the [normal equations](/normal-equations/), and $A^+ = R^{-1} Q^T$ from a thin [QR decomposition](/qr-decomposition/) $A = Q R$. If $A$ has full row rank, $A^+ = A^T (A A^T)^{-1}$. For a nonzero column vector $a$, $a^+ = a^T/\|a\|_2^2$. Also $A^+ = \lim_{\lambda \to 0^+} (A^T A + \lambda I)^{-1} A^T$, the limit of [Tikhonov regularization](/tikhonov-regularization/).

**Norm and conditioning.** $\|A^+\|_2 = 1/\sigma_r$, and $\kappa_2(A) = \|A\|_2 \|A^+\|_2 = \sigma_1/\sigma_r$ is the condition number used for least squares and for rank-deficient problems.

**Discontinuity and numerical rank.** $A^+$ is a continuous function of $A$ only where the rank does not change. For $A_\varepsilon = \mathrm{diag}(1, \varepsilon)$, $A_\varepsilon^+ = \mathrm{diag}(1, 1/\varepsilon)$, which blows up as $\varepsilon \to 0$, while $A_0^+ = \mathrm{diag}(1, 0)$. In floating point every matrix is a rounding error away from full rank, so the computed pseudoinverse is useful only after a decision about the rank: drop the singular values below a threshold $\tau$, such as $\tau = \max(m, n)\, u\, \sigma_1$, and use the truncated $A_\tau^+ = \sum_{\sigma_i > \tau} v_i u_i^T/\sigma_i$. When the rank is preserved, perturbations behave well: Wedin (1973) bounds $\|B^+ - A^+\|_2$ by a small constant times $\|A^+\|_2\,\|B^+\|_2\,\|B - A\|_2$ for $\mathrm{rank}\, B = \mathrm{rank}\, A$.

**Computation.**
- *SVD.* $x^+ = \sum_{i \le r} (u_i^T b/\sigma_i)\, v_i$. A Golub-Kahan SVD costs $O(m n^2)$ flops for $m \ge n$, and is backward stable: the computed singular values are exact for $A + E$ with $\|E\|_2 \le c(m,n)\,u\,\|A\|_2$.
- *Rank-revealing QR.* A [rank-revealing factorization](/rank-revealing-factorization/) $A \Pi = Q R$ gives a basic least squares solution with at most $r$ nonzeros in $O(m n r)$ flops; a further orthogonal reduction of the trailing block (a complete orthogonal decomposition) gives the minimum-norm solution.
- *Never form $A^+$ to solve.* Forming $A^+$ and multiplying costs more and is less accurate, as with the ordinary inverse.

## Examples

**A rank-one square matrix.** $A = \begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix} = 2\, w w^T$ with $w = (1, 1)^T/\sqrt2$, so $A^+ = \tfrac12 w w^T = \tfrac14\begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix}$. For $b = (1, 3)^T$ there is no solution; the least squares solutions are the line $x_1 + x_2 = 2$, and $A^+ b = (1, 1)^T$ is the point of it closest to the origin.

**Full column rank.** For $A = \begin{pmatrix} 1 & 0 \\ 0 & 1 \\ 1 & 1 \end{pmatrix}$, $A^T A = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$ and
$$A^+ = (A^T A)^{-1} A^T = \frac13\begin{pmatrix} 2 & -1 & 1 \\ -1 & 2 & 1 \end{pmatrix},$$
a left inverse: $A^+ A = I_2$, while $A A^+$ is the projector onto the plane $\mathrm{range}(A)$.

**The zero matrix and vectors.** $0_{m \times n}^+ = 0_{n \times m}$. For $a = (3, 4)^T$, $a^+ = (3, 4)/25$.

**Rules that fail.** $(A B)^+ \ne B^+ A^+$ in general: for $A = (1 \;\; 1)$ and $B = (1, 0)^T$, $A B = 1$ and $(AB)^+ = 1$, but $B^+ A^+ = (1 \;\; 0)\,(\tfrac12, \tfrac12)^T = \tfrac12$. Also $A^+$ is not a polynomial or rational function of the entries of $A$ across rank changes, as the $\mathrm{diag}(1, \varepsilon)$ example shows.

## Where it is used

- **Rank-deficient and underdetermined least squares.** $x^+ = A^+ b$ is the standard answer when $A$ lacks full rank, computed by the SVD or by complete orthogonal decomposition (Golub and Van Loan, Section 5.5).
- **Perturbation theory.** Bounds for least squares solutions and residuals are stated with $\|A^+\|_2$ and $\kappa_2(A) = \|A\|_2\|A^+\|_2$ (Higham, Chapter 20).
- **Regularization of ill-posed problems.** The truncated SVD solution $A_\tau^+ b$ and the Tikhonov solution are two filters applied to the terms $u_i^T b/\sigma_i$ of $A^+ b$.
- **Statistics and signal processing.** Ordinary least squares fits, projections onto subspaces ($A A^+$), and the minimum-norm solutions of underdetermined systems in control and robotics.
- **Generalized inverses.** Weaker inverses satisfy only some of the four equations, for instance $A X A = A$ alone; the Drazin inverse serves square matrices in the theory of singular systems of differential equations.

## References
