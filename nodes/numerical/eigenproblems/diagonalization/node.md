---
tag: A9SXXF
kind: concept
slug: diagonalization
name: Diagonalization
aliases:
- eigendecomposition
- spectral decomposition
- eigenvalue decomposition
area: numerical/eigenproblems
level: intro
summary: Writing A = V Λ V⁻¹ with Λ diagonal, possible exactly when A has n independent eigenvectors. In floating point it is only as reliable as the condition number of V.
prereqs: [eigenvalue, eigenvector, linear-independence]
see_also: [similarity-transformation, spectral-theorem, schur-decomposition, jordan-normal-form, bauer-fike-theorem, eigenvalue-problem, singular-value-decomposition]
sources:
  - book: isbn:9780521548236
    title: Roger A. Horn and Charles R. Johnson, Matrix Analysis, second edition, Cambridge University Press, 2013
    locator: Section 1.3 (similarity and diagonalizability, and the simultaneous diagonalization of commuting matrices) and Section 2.5 (normal matrices)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 7.1 (diagonalizable matrices and the Schur decomposition) and Chapter 9 (functions of matrices, the eigenvector approach and its sensitivity)
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 24 (eigenvalue decomposition, defective and diagonalizable matrices, unitary diagonalization)
---

Diagonalization writes a square matrix $A \in \mathbb{C}^{n \times n}$ as $A = V \Lambda V^{-1}$, with $\Lambda = \operatorname{diag}(\lambda_1, \dots, \lambda_n)$ the [eigenvalues](/eigenvalue/) and the columns of the nonsingular matrix $V$ the matching [eigenvectors](/eigenvector/). It exists exactly when $A$ has $n$ linearly independent eigenvectors; such an $A$ is *diagonalizable* and the others are *defective*. With $V$ unitary, it exists exactly when $A$ is normal, which is the [spectral theorem](/spectral-theorem/). In floating point the factorization is only as reliable as the condition number $\kappa(V)$, so numerical codes prefer the [Schur decomposition](/schur-decomposition/).

## In plain words

Some matrices act in a very simple way once you look at them along the right axes. Along each special axis the matrix only stretches by a fixed amount. If there are enough special axes to describe every vector, you can split any vector into parts along them, stretch each part, and add the parts back. That is all the matrix does. Writing the matrix this way is diagonalization.

It makes repeated products easy, since stretching many times only raises each stretch amount to a power. Some matrices do not have enough special axes and cannot be written this way. When the special axes are almost parallel, the split into parts uses huge numbers that cancel, and rounding errors grow by the same large factor.

## The idea

**When it exists.** For $A \in \mathbb{C}^{n \times n}$ the following are equivalent: (a) $A = V \Lambda V^{-1}$ with $\Lambda$ diagonal; (b) $A$ has $n$ linearly independent eigenvectors; (c) for each eigenvalue, the geometric multiplicity equals the algebraic multiplicity. *Proof.* (a) to (b): $A V = V \Lambda$ says $A v_i = \lambda_i v_i$ column by column, and $V$ nonsingular means its columns are independent. (b) to (a): put the eigenvectors in $V$ and read $A V = V \Lambda$ backwards. (b) and (c): eigenvectors of distinct eigenvalues are independent, so bases of the eigenspaces together give an independent set whose size is the sum of the geometric multiplicities. This sum is $n$ if and only if each geometric multiplicity equals its algebraic one, since geometric is at most algebraic and the algebraic ones add up to $n$. $\square$ In particular, $n$ distinct eigenvalues imply diagonalizable.

**Uniqueness.** $\Lambda$ is unique up to the order of its entries. $V$ is not: each column can be scaled by a nonzero number, and inside an eigenspace of dimension above 1 any basis works.

**Unitary diagonalization.** $A = Q \Lambda Q^*$ with $Q$ unitary if and only if $A$ is normal ($A^* A = A A^*$). Hermitian matrices are normal, with real $\Lambda$; real symmetric matrices have $A = Q \Lambda Q^T$ with $Q$ real orthogonal. *Proof sketch.* Every $A$ has a Schur form $A = Q T Q^*$ with $T$ upper triangular. If $A$ is normal, so is $T$; comparing the $(1,1)$ entries of $T^* T$ and $T T^*$ gives $|t_{11}|^2 = \sum_j |t_{1j}|^2$, so the rest of the first row is zero, and induction on $n$ makes $T$ diagonal. Conversely, $Q \Lambda Q^*$ commutes with its adjoint because diagonal matrices commute. $\square$

**What it is for.** If $A = V \Lambda V^{-1}$, then $A^k = V \Lambda^k V^{-1}$ for every integer $k \ge 0$, and more generally $f(A) = V f(\Lambda) V^{-1}$ for a function $f$ defined on the spectrum, for example $e^{tA} = V e^{t\Lambda} V^{-1}$. The linear recurrence $x_{k+1} = A x_k$ becomes $n$ scalar recurrences in the coordinates $y = V^{-1} x$, and the ODE $x' = Ax$ becomes $n$ scalar ODEs. Two diagonalizable matrices can be diagonalized by the same $V$ if and only if they commute (Horn and Johnson, Section 1.3).

**Defective matrices are rare but real.** Each matrix is a limit of diagonalizable ones: perturb the diagonal of a Schur form $T$ by amounts of size at most $\varepsilon$ so that the diagonal entries become distinct; then $Q (T + D) Q^*$ is diagonalizable and within $\varepsilon$ of $A$. So in floating point almost every computed matrix is diagonalizable. That does not help: near a defective matrix, $\kappa(V)$ is huge. The exact structure of a defective matrix is the [Jordan normal form](/jordan-normal-form/), which is not continuous in the entries and is not computed in floating point.

**Sensitivity.** The [Bauer-Fike theorem](/bauer-fike-theorem/) says that each eigenvalue of $A + E$ lies within $\kappa_p(V) \|E\|_p$ of an eigenvalue of $A$, where $\kappa_p(V) = \|V\|_p \|V^{-1}\|_p$. For a normal matrix $\kappa_2(V) = 1$. Forming $V f(\Lambda) V^{-1}$ in floating point gives an error of order $\kappa(V) u \|f(\Lambda)\|$ (Golub and Van Loan, Chapter 9), so diagonalization is a good way to compute $f(A)$ only when $V$ is well conditioned. Backward stable algorithms produce a Schur form, whose $Q$ is unitary up to rounding, and recover $V$ from it only when asked.

## Examples

**A 2 by 2 matrix.** For $A = \begin{pmatrix} 4 & 1 \\ 2 & 3 \end{pmatrix}$,
$$V = \begin{pmatrix} 1 & 1 \\ 1 & -2 \end{pmatrix}, \quad \Lambda = \begin{pmatrix} 5 & 0 \\ 0 & 2 \end{pmatrix}, \quad V^{-1} = \frac13 \begin{pmatrix} 2 & 1 \\ 1 & -1 \end{pmatrix}.$$
Then $A^k = \frac13 \begin{pmatrix} 2 \cdot 5^k + 2^k & 5^k - 2^k \\ 2 \cdot 5^k - 2 \cdot 2^k & 5^k + 2 \cdot 2^k \end{pmatrix}$. For $k = 10$ this is $\begin{pmatrix} 6510758 & 3254867 \\ 6509734 & 3255891 \end{pmatrix}$, the same as ten matrix products.

**Fibonacci numbers.** $F = \begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}$ has the eigenvalues $\varphi = (1 + \sqrt5)/2$ and $\psi = (1 - \sqrt5)/2$, which are distinct, so $F$ is diagonalizable. The $(1,2)$ entry of $F^k = V \operatorname{diag}(\varphi^k, \psi^k) V^{-1}$ is the Binet formula $(\varphi^k - \psi^k)/\sqrt5$.

**Non-example: a Jordan block.** $J = \begin{pmatrix} 2 & 1 \\ 0 & 2 \end{pmatrix}$ has only the eigenvectors $c e_1$, so it is defective. Its powers are $J^k = \begin{pmatrix} 2^k & k 2^{k-1} \\ 0 & 2^k \end{pmatrix}$, and the factor $k$ cannot come from a diagonal $\Lambda^k$.

**Nearly defective: ill-conditioned V.** $A = \begin{pmatrix} 1 & 1 \\ 0 & 1 + \delta \end{pmatrix}$ with $\delta = 10^{-6}$ has the eigenvectors $(1, 0)^T$ and $(1, \delta)^T$, at an angle of about $10^{-6}$. With unit columns, $\kappa_2(V) \approx 2 / \delta = 2 \times 10^6$. Forming the $(1,2)$ entry of $V \Lambda V^{-1}$ in IEEE double gives $0.9999999998835847$ instead of 1, an error of $1.16 \times 10^{-10}$, which is of the order $\kappa_2(V) u$.

**Non-example of unitary diagonalization.** The $2 \times 2$ example above is diagonalizable but not normal: $V$ has the angle $\arccos(-1/\sqrt{10})$ between its columns, not a right angle, and no unitary $V$ exists.

## Where it is used

- **Matrix functions and dynamics.** Powers, exponentials and square roots of a well-conditioned diagonalizable matrix; the decoupling of linear ODEs and recurrences into modes.
- **Symmetric problems.** For real symmetric matrices the orthogonal diagonalization $A = Q \Lambda Q^T$ is the output of the [symmetric eigenproblem](/symmetric-eigenproblem/) solvers ([Jacobi](/jacobi-eigenvalue-algorithm/), [divide and conquer](/divide-and-conquer-eigensolver/), tridiagonal QR) and is computed in a backward stable way.
- **Perturbation theory.** $\kappa(V)$ is the constant of the Bauer-Fike theorem and enters convergence bounds of Krylov methods such as [GMRES](/gmres/).
- **Quadratic forms and statistics.** Principal axes of an ellipsoid $x^T A x = 1$, principal components of a covariance matrix.
- **Exact computation.** Over the rationals, diagonalizability is decided exactly from the [minimal polynomial](/minimal-polynomial-computation/): $A$ is diagonalizable over $\mathbb{C}$ if and only if its minimal polynomial has no repeated roots.

## References
