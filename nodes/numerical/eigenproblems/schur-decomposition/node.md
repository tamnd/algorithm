---
tag: TN48EM
kind: theorem
slug: schur-decomposition
name: Schur decomposition
aliases:
- Schur form
- Schur triangularization
- unitary triangularization
- real Schur form
area: numerical/eigenproblems
level: advanced
summary: Every complex square matrix is A = Q T Q* with Q unitary and T upper triangular, the eigenvalues on the diagonal of T in any chosen order. A real matrix has a real form with 2 by 2 blocks.
prereqs: [similarity-transformation, eigenvalue, eigenvector]
see_also: [qr-algorithm, spectral-theorem, jordan-normal-form, hessenberg-reduction, nonsymmetric-eigenproblem, qz-algorithm, francis-double-shift-qr, deflation]
sources:
  - book: isbn:9780521548236
    title: Roger A. Horn and Charles R. Johnson, Matrix Analysis, second edition, Cambridge University Press, 2013
    locator: Section 2.3, Unitary triangularizations (Schur's theorem and the real Schur form)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 7.1.3 (the Schur decomposition), Section 7.4.1 (the real Schur decomposition), Section 7.6 (invariant subspace computations and reordering)
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 24, Eigenvalue Problems (Schur factorization and why eigenvalue algorithms aim for it)
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Section 4.2, Canonical Forms (Jordan and Schur forms, and why the Schur form is the one computed)
  - paper: "Issai Schur, Über die charakteristischen Wurzeln einer linearen Substitution mit einer Anwendung auf die Theorie der Integralgleichungen, Mathematische Annalen 66, 1909"
    title: Über die charakteristischen Wurzeln einer linearen Substitution mit einer Anwendung auf die Theorie der Integralgleichungen
    locator: Math. Ann. 66 (1909), pp. 488 to 510
  - paper: "P. Henrici, Bounds for iterates, inverses, spectral variation and fields of values of non-normal matrices, Numerische Mathematik 4, 1962"
    title: Bounds for iterates, inverses, spectral variation and fields of values of non-normal matrices
    locator: Numer. Math. 4 (1962), pp. 24 to 40
---

The Schur decomposition writes any complex square matrix as $A = Q T Q^*$ with $Q$ unitary and $T$ upper triangular. The diagonal of $T$ holds the [eigenvalues](/eigenvalue/) of $A$, and they can be put in any order. Unlike diagonalization, it exists for every matrix, defective or not, and unlike the [Jordan normal form](/jordan-normal-form/) it uses only a unitary [similarity](/similarity-transformation/), so it can be computed stably: the [QR algorithm](/qr-algorithm/) returns the Schur form of a matrix within $O(u)\|A\|$ of $A$. The first $k$ columns of $Q$ span an invariant subspace for the first $k$ diagonal entries. A real matrix has a real Schur form $A = Q T Q^T$ with $Q$ real orthogonal and $T$ block upper triangular with $1 \times 1$ and $2 \times 2$ diagonal blocks, the latter carrying the complex conjugate pairs. For a normal matrix, and in particular a Hermitian one, $T$ is diagonal and the theorem becomes the [spectral theorem](/spectral-theorem/).

## Statement

**Notation.** $A \in \mathbb C^{n \times n}$, $A^*$ its conjugate transpose, and $\lambda_1, \dots, \lambda_n$ its eigenvalues, repeated by algebraic multiplicity, in any order chosen in advance.

**Theorem (complex Schur form; Schur 1909).** There is a unitary $Q$ and an upper triangular $T$ with

$$A = Q T Q^*, \qquad t_{ii} = \lambda_i \quad (i = 1, \dots, n).$$

For each $k$, $\operatorname{span}\{q_1, \dots, q_k\}$ is an invariant subspace of $A$: $A Q_k = Q_k T_{11}$ with $Q_k = [q_1, \dots, q_k]$ and $T_{11}$ the leading $k \times k$ block of $T$.

**Theorem (real Schur form).** If $A \in \mathbb R^{n \times n}$, there is a real orthogonal $Q$ with

$$A = Q T Q^T, \qquad T = \begin{pmatrix} R_{11} & R_{12} & \cdots & R_{1m} \\ 0 & R_{22} & \cdots & R_{2m} \\ \vdots & & \ddots & \vdots \\ 0 & 0 & \cdots & R_{mm} \end{pmatrix},$$

where each $R_{ii}$ is either $1 \times 1$ (a real eigenvalue) or $2 \times 2$ with a pair of complex conjugate eigenvalues $\alpha \pm i\beta$, $\beta \ne 0$.

**Corollary (normal matrices).** $T$ is diagonal if and only if $A$ is normal, $A^* A = A A^*$. More precisely, writing $T = D + N$ with $D$ diagonal and $N$ strictly upper triangular, $\|N\|_F^2 = \|A\|_F^2 - \sum_i |\lambda_i|^2$ for every Schur form (Henrici's departure from normality).

## In plain words

Any square table of numbers can be turned, by a rotation of the coordinate system that keeps lengths and angles, into a table with nothing below the main diagonal. The numbers on the diagonal are then exactly the special values of the table, in whatever order we like. The first direction found is stretched without leaving its line, the first two directions span a flat piece that the table maps into itself, and so on. Because only rotations are used, small errors in the computation stay small, which is why computer programs aim for this form.

## Proof

*Complex form, by induction on $n$.* For $n = 1$ take $Q = (1)$. Let $n \ge 2$. The characteristic polynomial has the root $\lambda_1$ (the fundamental theorem of algebra), so there is a unit vector $q_1$ with $A q_1 = \lambda_1 q_1$. Complete it to a unitary matrix $U = [q_1, W]$, for example by Gram-Schmidt on $q_1, e_1, \dots, e_n$. Then

$$U^* A U = \begin{pmatrix} q_1^* A q_1 & q_1^* A W \\ W^* A q_1 & W^* A W \end{pmatrix} = \begin{pmatrix} \lambda_1 & b^* \\ 0 & A_2 \end{pmatrix},$$

because $W^* A q_1 = \lambda_1 W^* q_1 = 0$. The characteristic polynomial of this block triangular matrix is $(\lambda_1 - z)\det(A_2 - z I)$, so the eigenvalues of $A_2$ are $\lambda_2, \dots, \lambda_n$. By the induction hypothesis $A_2 = Q_2 T_2 Q_2^*$ with $T_2$ upper triangular and diagonal $\lambda_2, \dots, \lambda_n$. Put $Q = U \operatorname{diag}(1, Q_2)$, a product of unitary matrices. Then

$$Q^* A Q = \begin{pmatrix} 1 & 0 \\ 0 & Q_2^* \end{pmatrix} \begin{pmatrix} \lambda_1 & b^* \\ 0 & A_2 \end{pmatrix} \begin{pmatrix} 1 & 0 \\ 0 & Q_2 \end{pmatrix} = \begin{pmatrix} \lambda_1 & b^* Q_2 \\ 0 & T_2 \end{pmatrix},$$

which is upper triangular with the required diagonal. The invariant subspace claim follows from $A Q = Q T$: since $T$ is upper triangular, $A q_k = \sum_{l \le k} t_{lk} q_l$.

*Real form, by induction on $n$.* If $A$ has a real eigenvalue, take a real unit eigenvector (a real singular matrix $A - \lambda I$ has a real null vector) and proceed as above with real orthogonal matrices. Otherwise let $\lambda = \alpha + i\beta$ with $\beta \ne 0$ be an eigenvalue with eigenvector $z = x + i y$, $x, y \in \mathbb R^n$. Taking real and imaginary parts of $A z = \lambda z$ gives

$$A [x, y] = [x, y] \begin{pmatrix} \alpha & \beta \\ -\beta & \alpha \end{pmatrix}.$$

The vectors $x$ and $y$ are linearly independent: if $y = c x$ with $c$ real (or $x = 0$), then $z$ is a complex multiple of a real vector $w$, and $A w = \lambda w$ with $A w$ real forces $\lambda$ real. So $\operatorname{span}\{x, y\}$ is a 2-dimensional real invariant subspace. Let $V_1 \in \mathbb R^{n \times 2}$ be an orthonormal basis of it and complete it to a real orthogonal $V = [V_1, V_2]$. Then $A V_1 = V_1 R_{11}$ for a real $2 \times 2$ matrix $R_{11}$ similar to $\begin{pmatrix} \alpha & \beta \\ -\beta & \alpha \end{pmatrix}$, whose eigenvalues are $\alpha \pm i\beta$, and $V^T A V = \begin{pmatrix} R_{11} & * \\ 0 & A_2 \end{pmatrix}$ because $V_2^T A V_1 = V_2^T V_1 R_{11} = 0$. Apply the induction hypothesis to the real matrix $A_2$ of order $n - 2$.

*Normal matrices.* If $A$ is normal, so is $T = Q^* A Q$. Compare the $(1, 1)$ entries of $T^* T$ and $T T^*$: $|t_{11}|^2 = \sum_j |t_{1j}|^2$, so $t_{1j} = 0$ for $j > 1$. Repeating with the next diagonal entry shows that $T$ is diagonal. Conversely a diagonal $T$ is normal, and so is $Q T Q^*$. For the formula, $\|A\|_F = \|T\|_F$ because the Frobenius norm is unitarily invariant, and $\|T\|_F^2 = \sum |\lambda_i|^2 + \|N\|_F^2$. $\blacksquare$

## Consequences

- **The target of eigenvalue algorithms.** The QR algorithm computes a sequence of unitary similarities that converge to a Schur form; in floating point it returns $\hat Q$ and $\hat T$ with $\hat Q \hat T \hat Q^* = A + E$ and $\|E\|_2 = O(u)\|A\|_2$ (GVL Section 7.5). The [Francis double-shift QR](/francis-double-shift-qr/) algorithm computes the real Schur form of a real matrix in real arithmetic.
- **Invariant subspaces and reordering.** Swapping adjacent diagonal blocks by a unitary similarity (Bai and Demmel 1993) moves any chosen set of eigenvalues to the top, so the leading columns of $Q$ give an orthonormal basis of the invariant subspace for that set; this is how stable subspaces of control problems and Riccati equations are computed (GVL Section 7.6).
- **Matrix functions and equations.** $f(A) = Q f(T) Q^*$ reduces matrix functions to triangular ones (the Schur-Parlett algorithm), and the Bartels-Stewart method solves the Sylvester equation $A X - X B = C$ through the Schur forms of $A$ and $B$.
- **Spectral theorem and trace identities.** For Hermitian $A$, $T = Q^* A Q$ is Hermitian and triangular, hence diagonal and real. In general $\operatorname{tr} A = \sum \lambda_i$ and $\det A = \prod \lambda_i$ can be read off $T$, and Cayley-Hamilton follows from $p(T) = 0$ for triangular $T$.
- **Nonnormality.** Henrici's $\|N\|_F$ measures how far $A$ is from normal; it controls the distance of the eigenvalues of $A + E$ from those of $A$ when $A$ is not diagonalizable, and the growth of $\|A^k\|$ and $\|e^{tA}\|$.

**Example.** $A = \begin{pmatrix} 3 & 1 \\ -1 & 1 \end{pmatrix}$ has the double eigenvalue $2$ ($\operatorname{tr} A = 4$, $\det A = 4$) and only one eigenvector, $q_1 = (1, -1)^T / \sqrt 2$, so it is not diagonalizable. With $q_2 = (1, 1)^T / \sqrt 2$, $Q = [q_1, q_2]$ gives $T = Q^T A Q = \begin{pmatrix} 2 & 2 \\ 0 & 2 \end{pmatrix}$, since $A q_1 = 2 q_1$, $q_1^T A q_2 = 2$ and $q_2^T A q_2 = 2$. Henrici's formula checks: $\|A\|_F^2 - |2|^2 - |2|^2 = 12 - 8 = 4 = |t_{12}|^2$.

## Tightness

- **$T$ is not unique.** Changing the order of the eigenvalues changes the strictly upper part, and for a fixed order the columns of $Q$ can be multiplied by unit scalars $e^{i\phi_k}$, which changes $t_{lk}$ by $e^{i(\phi_k - \phi_l)}$. Only $\|N\|_F$ is the same for all Schur forms.
- **Triangular, not diagonal.** For a non-normal matrix no unitary similarity gives a diagonal matrix, by the corollary; diagonalization needs a non-unitary similarity, which may be ill conditioned, and does not exist at all for defective matrices like the example.
- **Real arithmetic needs the $2 \times 2$ blocks.** $\begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}$ has eigenvalues $\pm i$, so no real similarity makes it triangular.
- **Stability, compared with Jordan.** $\begin{pmatrix} 0 & 1 \\ \epsilon & 0 \end{pmatrix}$ has the Jordan form $\begin{pmatrix} 0 & 1 \\ 0 & 0 \end{pmatrix}$ for $\epsilon = 0$ and $\operatorname{diag}(\sqrt\epsilon, -\sqrt\epsilon)$ for $\epsilon > 0$, a jump, while its Schur forms vary continuously with $\epsilon$ for a fixed ordering of the eigenvalues.

## History

Issai Schur proved in 1909 that every matrix is unitarily similar to a triangular matrix, in a paper on the characteristic roots of linear substitutions, and used it to bound $\sum |\lambda_i|^2$ by $\sum |a_{ij}|^2$, with equality exactly for normal matrices. The real form appears in Murnaghan and Wintner (1931). Francis (1961) and Kublanovskaya (1961) found that the QR iteration converges to a Schur form, and from then on the Schur form, rather than the Jordan form, became the computed canonical form. Henrici named the departure from normality in 1962.

## References
