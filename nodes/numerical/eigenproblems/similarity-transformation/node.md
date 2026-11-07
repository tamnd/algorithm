---
tag: RBY13N
kind: definition
slug: similarity-transformation
name: Similarity transformation
aliases:
- similar matrices
- similarity
- matrix similarity
area: numerical/eigenproblems
level: intro
summary: The map A to S⁻¹ A S for a nonsingular S. Similar matrices have the same characteristic polynomial, so the same eigenvalues with the same multiplicities.
prereqs: [eigenvalue, characteristic-polynomial]
see_also: [diagonalization, schur-decomposition, jordan-normal-form, rational-canonical-form, hessenberg-reduction, matrix-balancing, condition-number, deflation]
sources:
  - book: isbn:9780521548236
    title: Roger A. Horn and Charles R. Johnson, Matrix Analysis, second edition, Cambridge University Press, 2013
    locator: Section 1.3, Similarity; Chapter 3, Canonical forms for similarity (the Jordan form, and the similarity of a matrix and its transpose)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 7.1, Properties and Decompositions (similarity transformations, invariant subspaces and the Schur decomposition)
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 24, Eigenvalue Problems (similarity transformations and eigenvalue-revealing factorizations)
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Section 4.2, Canonical Forms
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 19, QR Factorization (the backward error of a sequence of Householder or Givens transformations)
---

A similarity transformation maps a square matrix $A$ to $B = S^{-1} A S$, where $S$ is a nonsingular matrix of the same order; $A$ and $B$ are then called similar. Similar matrices describe the same linear map in two bases, so they have the same [characteristic polynomial](/characteristic-polynomial/) and the same [eigenvalues](/eigenvalue/), and their [eigenvectors](/eigenvector/) correspond through $S$. Every dense eigenvalue method applies a sequence of similarity transformations that keeps the eigenvalues and makes the matrix simpler, and in floating point the safe ones use a unitary $S$.

## Definition

**Notation.** $\mathbb F$ is $\mathbb R$ or $\mathbb C$. $A, B \in \mathbb F^{n \times n}$ with $n \ge 1$. $S^*$ is the conjugate transpose. The condition number is $\kappa(S) = \|S\| \, \|S^{-1}\|$ in a stated norm. $u$ is the unit roundoff.

Two matrices $A, B \in \mathbb F^{n \times n}$ are **similar over $\mathbb F$** if there is a nonsingular $S \in \mathbb F^{n \times n}$ with

$$B = S^{-1} A S.$$

The map $A \mapsto S^{-1} A S$ is the **similarity transformation** with matrix $S$. Similarity is an equivalence relation: take $S = I$ for reflexivity, $S^{-1}$ for symmetry, and $S_1 S_2$ for transitivity, since $S_2^{-1}(S_1^{-1} A S_1) S_2 = (S_1 S_2)^{-1} A (S_1 S_2)$.

The transformation is **unitary** (over $\mathbb R$: **orthogonal**) when $S^* S = I$, so $B = S^* A S$, and **diagonal** when $S$ is a nonsingular diagonal matrix.

**What it keeps.** Let $B = S^{-1} A S$. Then:

1. $\det(B - \lambda I) = \det\bigl(S^{-1} (A - \lambda I) S\bigr) = \det(A - \lambda I)$ for each $\lambda$. So $A$ and $B$ have the same characteristic polynomial, the same eigenvalues with the same algebraic multiplicities, the same trace (the sum of the eigenvalues) and the same determinant (their product).
2. $A v = \lambda v$ if and only if $B (S^{-1} v) = \lambda (S^{-1} v)$, because $B S^{-1} v = S^{-1} A v$. So $\ker(B - \lambda I) = S^{-1} \ker(A - \lambda I)$, and the geometric multiplicities agree.
3. $B^k = S^{-1} A^k S$ for each $k \ge 0$, so $p(B) = S^{-1} p(A) S$ for each polynomial $p$. Hence $A$ and $B$ have the same minimal polynomial and the same rank of $(A - \lambda I)^k$ for each $\lambda$ and $k$. These ranks fix the [Jordan normal form](/jordan-normal-form/), and two complex matrices are similar exactly when they have the same Jordan form up to the order of the blocks (Horn and Johnson, Chapter 3).
4. A subspace $\mathcal X$ is invariant under $A$ ($A \mathcal X \subseteq \mathcal X$) if and only if $S^{-1} \mathcal X$ is invariant under $B$.

A unitary similarity keeps more: the 2-norm and the Frobenius norm ($\|S^* A S\|_2 = \|A\|_2$), the Hermitian property, normality, and the angles between vectors.

**In floating point.** The eigenvalues of $B$ are exactly those of $A$ only in exact arithmetic. If the computed matrix is $\hat B = B + F$, then

$$\hat B = S^{-1} (A + S F S^{-1}) S, \qquad \|S F S^{-1}\| \le \kappa(S) \, \|F\|,$$

so $\hat B$ is exactly similar to a perturbation of $A$ whose size can be $\kappa(S)$ times the error made on $B$. For a unitary $S$, $\kappa_2(S) = 1$, and a product of Householder or Givens transformations applied in floating point gives $\hat B = Q^* (A + E) Q$ with $Q$ exactly unitary and $\|E\|_2 \le p(n) \, u \, \|A\|_2$ for a modest polynomial $p$ (Higham, Chapter 19). This is why eigenvalue codes use unitary similarities, and use a nonunitary $S$ only when its entries are powers of the radix, as in [matrix balancing](/matrix-balancing/), where the scaling is exact.

## Examples and non-examples

**A similarity that diagonalizes.** Let

$$A = \begin{pmatrix} 2 & 1 \\ 0 & 3 \end{pmatrix}, \quad S = \begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix}, \quad S^{-1} = \begin{pmatrix} 1 & -1 \\ 0 & 1 \end{pmatrix}, \quad S^{-1} A S = \begin{pmatrix} 2 & 0 \\ 0 & 3 \end{pmatrix}.$$

The columns of $S$ are eigenvectors of $A$: $A (1, 0)^T = 2 (1, 0)^T$ and $A (1, 1)^T = 3 (1, 1)^T$. A similarity to a diagonal matrix is a [diagonalization](/diagonalization/).

**Same trace and determinant in a new basis.** With $A = \begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}$ and $S = \begin{pmatrix} 2 & 1 \\ 1 & 1 \end{pmatrix}$ (so $S^{-1} = \begin{pmatrix} 1 & -1 \\ -1 & 2 \end{pmatrix}$), the product is $S^{-1} A S = \begin{pmatrix} -6 & -4 \\ 16 & 11 \end{pmatrix}$. Its trace is $5$ and its determinant is $-2$, the same as for $A$.

**An ill-conditioned similarity.** Take the same $A = \begin{pmatrix} 2 & 1 \\ 0 & 3 \end{pmatrix}$ and $S = \begin{pmatrix} 1 & 1 \\ 0 & \delta \end{pmatrix}$ with $\delta = 10^{-3}$. Then $S^{-1} A S = \begin{pmatrix} 2 & \delta - 1 \\ 0 & 3 \end{pmatrix}$, which is correct, but $\kappa_2(S) \approx 2000$. An error $F = 10^{-10} e_2 e_1^T$ made on $B$ corresponds to the error $S F S^{-1}$ on $A$, whose $(1, 2)$ entry is $-10^{-7}$: one thousand times larger.

**Non-example: same eigenvalues, not similar.** $N = \begin{pmatrix} 0 & 1 \\ 0 & 0 \end{pmatrix}$ and the zero matrix both have characteristic polynomial $\lambda^2$. They are not similar, because $S^{-1} 0 S = 0 \ne N$ for each $S$. In the same way $\begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix}$ is not similar to $I$. Equal eigenvalues are necessary for similarity but not sufficient.

**Non-example: same eigenvalues and same rank.** The $3 \times 3$ matrices $I + e_1 e_2^T$ and $I + e_1 e_2^T + e_2 e_3^T$ both have the single eigenvalue $1$ and both are nonsingular. They are not similar: $A - I$ has rank 1 for the first and rank 2 for the second, and item 3 above says that this rank is kept.

**Non-example: other transformations.** The map $A \mapsto P A Q$ with two unrelated nonsingular matrices (an *equivalence*) keeps only the rank. The map $A \mapsto S^T A S$ (a *congruence*) keeps the symmetry and, by Sylvester's law of inertia, the numbers of positive, negative and zero eigenvalues of a symmetric $A$, but not the eigenvalues. Both coincide with similarity only when $Q = P^{-1}$ or $S^T = S^{-1}$.

**A matrix and its transpose.** Each square matrix is similar to its transpose (Horn and Johnson, Chapter 3), although $A^T$ and $A$ have different eigenvectors in general.

## Related definitions

- [Diagonalization](/diagonalization/): a similarity to a diagonal matrix, which exists exactly when $A$ has $n$ linearly independent eigenvectors.
- [Schur decomposition](/schur-decomposition/): a unitary similarity to an upper triangular matrix, which always exists. The [QR algorithm](/qr-algorithm/) computes it.
- [Jordan normal form](/jordan-normal-form/) and [rational canonical form](/rational-canonical-form/): canonical representatives of the similarity classes over $\mathbb C$ and over any field.
- [Hessenberg reduction](/hessenberg-reduction/) and [tridiagonalization](/tridiagonalization/): finite unitary similarities to condensed forms.
- [Matrix balancing](/matrix-balancing/): a diagonal similarity that reduces the norm before an eigenvalue computation.
- [Deflation](/deflation/): a similarity that splits off a known eigenpair.
- [Spectral theorem](/spectral-theorem/): a real symmetric matrix is orthogonally similar to a real diagonal matrix.
- [Condition number](/condition-number/): $\kappa(S)$ bounds how much a similarity can magnify errors.

## References
