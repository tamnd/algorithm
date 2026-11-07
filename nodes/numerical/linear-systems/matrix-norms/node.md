---
tag: CCJN8A
kind: definition
slug: matrix-norms
name: Matrix norms
aliases:
- induced norm
- Frobenius norm
- operator norm
- subordinate matrix norm
- matrix p-norm
area: numerical/linear-systems
level: intro
summary: Measures of matrix size, such as the induced 1, 2, infinity norms and the Frobenius norm.
prereqs: [eigenvalue]
see_also: [condition-number, spectral-radius, singular-value-decomposition, hagers-condition-estimator, residual, neumann-series, linear-system-solving, backward-error-analysis]
sources:
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 6, Norms (Section 6.1, vector norms; Section 6.2, matrix norms, with the table of the norms subordinate to the 1, 2 and infinity vector norms and the constants that relate them; Section 6.3, the matrix p-norm)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 2.2, Vector Norms; Section 2.3, Matrix Norms (the definitions, the formulas for the 1 and infinity norms, and the inequalities between the norms)
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 3, Norms (induced matrix norms, the 1 and infinity norm formulas, the Frobenius norm, the Cauchy-Schwarz and Hölder inequalities); Lecture 5, More on the SVD (the 2-norm as the largest singular value)
  - book: isbn:9780521548236
    title: Roger A. Horn and Charles R. Johnson, Matrix Analysis, second edition, Cambridge University Press, 2013
    locator: Chapter 5, Norms for vectors and matrices (Section 5.6, matrix norms, including the bound of the spectral radius by each matrix norm and the formula for the spectral radius as a limit)
---

A matrix norm is a function that gives each matrix a size: a nonnegative number that is zero only for the zero matrix, scales with the matrix, and obeys the triangle inequality. In numerical linear algebra the important ones are the norms *induced* by a vector norm, $\|A\| = \max_{x \ne 0} \|Ax\|/\|x\|$, and the Frobenius norm. Every error bound on the pages of this area, from the [condition number](/condition-number/) $\kappa(A) = \|A\|\,\|A^{-1}\|$ to the [backward error](/backward-error-analysis/) of a computed solution, is stated in one of these norms, so the choice of the norm is part of each statement.

## Definition

**Notation.** As on the other pages of this area, $A = (a_{ij})$ is an $m \times n$ real matrix ($n \times n$ when it is square), $x \in \mathbb{R}^n$, $|A|$ is the matrix of the $|a_{ij}|$, and inequalities between matrices hold entry by entry. $\sigma_{\max}(A)$ is the largest singular value and $\rho(A)$ is the [spectral radius](/spectral-radius/).

**Vector norms.** A *norm* on $\mathbb{R}^n$ is a function $\|\cdot\|: \mathbb{R}^n \to \mathbb{R}$ such that for each $x, y \in \mathbb{R}^n$ and each $\alpha \in \mathbb{R}$:

1. $\|x\| \ge 0$, and $\|x\| = 0$ only for $x = 0$;
2. $\|\alpha x\| = |\alpha|\,\|x\|$;
3. $\|x + y\| \le \|x\| + \|y\|$.

The $p$-norms are $\|x\|_p = (\sum_i |x_i|^p)^{1/p}$ for $1 \le p < \infty$ and $\|x\|_\infty = \max_i |x_i|$. The three used in practice are $\|x\|_1 = \sum_i |x_i|$, $\|x\|_2 = (x^T x)^{1/2}$ and $\|x\|_\infty$.

**Matrix norms.** A *matrix norm* is a norm on the vector space $\mathbb{R}^{m \times n}$: the three rules above, with matrices in place of vectors. A family of matrix norms is *consistent* (or *submultiplicative*) when $\|AB\| \le \|A\|\,\|B\|$ for all matrices of compatible sizes.

**Induced norms.** For vector norms on $\mathbb{R}^n$ and $\mathbb{R}^m$, the *induced* (or *subordinate*, or *operator*) norm is

$$\|A\| = \max_{x \ne 0} \frac{\|A x\|}{\|x\|} = \max_{\|x\| = 1} \|A x\|.$$

The maximum exists because the unit sphere is compact and $x \mapsto \|Ax\|$ is continuous. An induced norm is a matrix norm, it is consistent, $\|I\| = 1$, and $\|Ax\| \le \|A\|\,\|x\|$ for each $x$. For the three $p$-norms it has a closed form:

$$\|A\|_1 = \max_{j} \sum_{i=1}^m |a_{ij}|, \qquad \|A\|_\infty = \max_{i} \sum_{j=1}^n |a_{ij}|, \qquad \|A\|_2 = \sigma_{\max}(A) = \lambda_{\max}(A^T A)^{1/2}.$$

So $\|A\|_1$ is the largest column sum of $|A|$ and $\|A\|_\infty$ is the largest row sum.

*Proof of the $\infty$-norm formula.* For $\|x\|_\infty = 1$, $|(Ax)_i| \le \sum_j |a_{ij}|\,|x_j| \le \sum_j |a_{ij}|$, so $\|A\|_\infty$ is at most the largest row sum. Let row $k$ have the largest sum, and set $x_j = \operatorname{sign}(a_{kj})$ (with $\operatorname{sign} 0 = 1$). Then $\|x\|_\infty = 1$ and $(Ax)_k = \sum_j |a_{kj}|$, so the bound is attained. The 1-norm formula follows in the same way with $x = e_j$ for the column $j$ of largest sum: for each $x$, $\|Ax\|_1 \le \sum_j |x_j| \sum_i |a_{ij}| \le \|x\|_1 \max_j \sum_i |a_{ij}|$. For the 2-norm, $\|Ax\|_2^2 = x^T (A^T A) x$, and the maximum of this [Rayleigh quotient](/rayleigh-quotient/) over unit $x$ is $\lambda_{\max}(A^T A)$ by the [spectral theorem](/spectral-theorem/). $\square$

**The Frobenius norm.** $\|A\|_F = (\sum_{i,j} a_{ij}^2)^{1/2} = (\operatorname{trace}(A^T A))^{1/2} = (\sum_k \sigma_k^2)^{1/2}$. It is the 2-norm of $A$ seen as a vector of $mn$ entries. It is consistent, because the Cauchy-Schwarz inequality gives $|(AB)_{ij}|^2 \le \|a_{i,:}\|_2^2 \|b_{:,j}\|_2^2$ and summing gives $\|AB\|_F^2 \le \|A\|_F^2 \|B\|_F^2$. It is not induced for $n \ge 2$, because $\|I_n\|_F = \sqrt n \ne 1$.

**Relations.** For $A \in \mathbb{R}^{m \times n}$ of rank $r$ (Higham, Section 6.2; Golub and Van Loan, Section 2.3):

- $\|A\|_2 \le \|A\|_F \le \sqrt r\, \|A\|_2$;
- $\frac{1}{\sqrt n}\|A\|_\infty \le \|A\|_2 \le \sqrt m\, \|A\|_\infty$ and $\frac{1}{\sqrt m}\|A\|_1 \le \|A\|_2 \le \sqrt n\, \|A\|_1$;
- $\|A\|_2 \le (\|A\|_1 \|A\|_\infty)^{1/2}$;
- $\|A^T\|_2 = \|A\|_2$ and $\|A^T\|_1 = \|A\|_\infty$;
- $\|QAZ\|_2 = \|A\|_2$ and $\|QAZ\|_F = \|A\|_F$ for orthogonal $Q$ and $Z$ (the two norms are *orthogonally invariant*);
- $\|\,|A|\,\| = \|A\|$ for the 1, $\infty$ and Frobenius norms, but only $\|A\|_2 \le \|\,|A|\,\|_2 \le \sqrt{\operatorname{rank}(A)}\,\|A\|_2$ for the 2-norm.

The first relation is $\sigma_1^2 \le \sum_k \sigma_k^2 \le r \sigma_1^2$. The third follows from $\|A\|_2^2 = \rho(A^T A) \le \|A^T A\|_1 \le \|A^T\|_1 \|A\|_1 = \|A\|_\infty \|A\|_1$, by the bound $\rho \le \|\cdot\|$ below.

**The spectral radius is a lower bound.** For a square $A$ and each consistent matrix norm, $\rho(A) \le \|A\|$. *Proof.* Let $A v = \lambda v$ with $v \ne 0$, possibly complex, and let $V$ be the matrix with each column equal to $v$. Then $A V = \lambda V$, so $|\lambda|\,\|V\| = \|AV\| \le \|A\|\,\|V\|$, and $\|V\| > 0$. An eigenvector of a real matrix may be complex; then the same argument runs in $\mathbb{C}^{n \times n}$, where the 1, 2, $\infty$ and Frobenius norms have the same formulas and are still consistent. $\square$ For a general consistent norm on real matrices the bound also holds (Horn and Johnson, Section 5.6). Conversely, for each $A$ and each $\varepsilon > 0$ there is an induced norm with $\|A\| \le \rho(A) + \varepsilon$ (Horn and Johnson, Section 5.6). This fact is the base of the convergence theory of [stationary iterations](/matrix-splitting/).

## Examples and non-examples

**A $2 \times 2$ example.** Let $A = \begin{pmatrix} 1 & -2 \\ 3 & 4 \end{pmatrix}$. The column sums of $|A|$ are $4$ and $6$, so $\|A\|_1 = 6$. The row sums are $3$ and $7$, so $\|A\|_\infty = 7$. $\|A\|_F = \sqrt{1 + 4 + 9 + 16} = \sqrt{30} \approx 5.4772$. For the 2-norm, $A^T A = \begin{pmatrix} 10 & 10 \\ 10 & 20 \end{pmatrix}$ has eigenvalues $15 \pm \sqrt{125}$, so $\|A\|_2 = (15 + 5\sqrt 5)^{1/2} \approx 5.1167$. The relations hold: $5.1167 \le 5.4772 \le \sqrt 2 \cdot 5.1167$, and $5.1167 \le \sqrt{6 \cdot 7} \approx 6.4807$. The eigenvalues of $A$ are $(5 \pm i\sqrt{15})/2$, of modulus $\sqrt{10} \approx 3.1623$, so $\rho(A) \approx 3.1623$ is below each of the four norms.

**Condition numbers in three norms.** $\det A = 10$ and $A^{-1} = \frac{1}{10}\begin{pmatrix} 4 & 2 \\ -3 & 1 \end{pmatrix}$. So $\|A^{-1}\|_1 = 0.7$ and $\|A^{-1}\|_\infty = 0.6$, and $\kappa_1(A) = 6 \cdot 0.7 = 4.2$ and $\kappa_\infty(A) = 7 \cdot 0.6 = 4.2$. In the 2-norm, $\sigma_1 \sigma_2 = |\det A| = 10$, so $\kappa_2(A) = \sigma_1/\sigma_2 = \sigma_1^2/10 = (3 + \sqrt 5)/2 \approx 2.6180$, with $\sigma_2 \approx 1.9544$. The three values differ, but by at most the factors $m$ and $n$ that the relations allow, so the norm matters only when those factors matter.

**The identity.** $\|I_n\|_p = 1$ for each induced norm, and $\|I_n\|_F = \sqrt n$.

**A rank-one matrix.** For $A = x y^T$, $\|A\|_2 = \|A\|_F = \|x\|_2 \|y\|_2$, $\|A\|_1 = \|x\|_1 \|y\|_\infty$ and $\|A\|_\infty = \|x\|_\infty \|y\|_1$.

**Non-example: the largest entry.** $\|A\|_{\max} = \max_{i,j} |a_{ij}|$ is a matrix norm, but it is not consistent. For $J = \begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix}$, $\|J\|_{\max} = 1$ but $J^2 = 2J$ has $\|J^2\|_{\max} = 2 > \|J\|_{\max}^2$. The scaled version $n \|A\|_{\max}$ is consistent on $n \times n$ matrices.

**Non-example: the spectral radius.** $\rho$ is not a norm. For $N = \begin{pmatrix} 0 & 1 \\ 0 & 0 \end{pmatrix}$, $\rho(N) = 0$ but $N \ne 0$, and with $N^T$, $\rho(N + N^T) = 1 > \rho(N) + \rho(N^T) = 0$, so the triangle inequality also fails.

**Non-example: the 2-norm of $|A|$.** For $A = \begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}$, $\|A\|_2 = \sqrt 2$ because $A^T A = 2I$, but $|A| = J$ has $\|J\|_2 = 2$. So in a componentwise bound such as $|\Delta A| \le c\,u\,|A|$, the step to a normwise bound costs a factor up to $\sqrt n$ in the 2-norm and nothing in the 1, $\infty$ and Frobenius norms.

**Cost of evaluation.** $\|A\|_1$, $\|A\|_\infty$ and $\|A\|_F$ take $O(mn)$ operations from the entries. $\|A\|_2$ needs the largest singular value, from the [SVD](/singular-value-decomposition/) or from [power iteration](/power-iteration/) on $A^T A$. The norm of an inverse, $\|A^{-1}\|_1$, is estimated from a factorization of $A$ in $O(n^2)$ flops by [Hager's estimator](/hagers-condition-estimator/), without forming $A^{-1}$.

## Related definitions

- [Condition number](/condition-number/): $\kappa(A) = \|A\|\,\|A^{-1}\|$, in a stated norm.
- [Spectral radius](/spectral-radius/): the largest eigenvalue modulus, a lower bound for each consistent norm.
- [Singular value decomposition](/singular-value-decomposition/): gives $\|A\|_2 = \sigma_1$ and $\|A\|_F = (\sum \sigma_k^2)^{1/2}$.
- [Residual](/residual/): its norm, divided by $\|A\|\,\|\hat x\| + \|b\|$, is the normwise backward error of a computed solution.
- [Neumann series](/neumann-series/): $\|E\| < 1$ in a consistent norm implies that $I - E$ is invertible.
- [Relative error](/relative-error/): the normwise relative error $\|x - \hat x\|/\|x\|$ uses a vector norm.

## References
