---
tag: DG2M92
kind: problem
slug: sylvester-equation
name: Sylvester equation
aliases:
- AX + XB = C
- Sylvester matrix equation
area: numerical/linear-systems
level: advanced
summary: Solve the matrix equation AX + XB = C for X.
model: floating-point-model
complexity:
  vars: {m: "the order of A", n: "the order of B"}
  time: {worst: "Θ(m^3 + n^3)"}
prereqs: [linear-system-solving, schur-decomposition, kronecker-product]
see_also: [lyapunov-equation, qr-algorithm, hessenberg-reduction, triangular-system-solving, condition-number, adi-method, eigenvalue-problem, residual]
sources:
  - paper: doi:10.1145/361573.361582
    title: Richard H. Bartels and G. W. Stewart, Algorithm 432, Solution of the matrix equation AX + XB = C, Communications of the ACM 15(9), 1972
    locator: reduction of A and B to real Schur form and the solution of the quasi-triangular equation by substitution
  - paper: doi:10.1109/TAC.1979.1102170
    title: Gene H. Golub, Stephen Nash and Charles F. Van Loan, A Hessenberg-Schur method for the problem AX + XB = C, IEEE Transactions on Automatic Control 24(6), 1979
    locator: reducing the larger matrix only to Hessenberg form, and the operation counts compared with Bartels-Stewart
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 16, The Sylvester Equation (solvability, the Bartels-Stewart method, the residual bound, the backward error and its difference from the relative residual, and the condition number)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 7.6, Invariant Subspace Computations (the Sylvester equation, its solution through Schur forms, and its role in block diagonalization)
  - paper: doi:10.1137/130912839
    title: Valeria Simoncini, Computational methods for linear matrix equations, SIAM Review 58(3), 2016
    locator: the survey of direct and iterative methods for Sylvester and Lyapunov equations, including low-rank methods for large sparse coefficients
---

The Sylvester equation asks for $X \in \mathbb{R}^{m \times n}$ with
$$A X + X B = C, \qquad A \in \mathbb{R}^{m \times m},\; B \in \mathbb{R}^{n \times n},\; C \in \mathbb{R}^{m \times n}.$$
It is a linear system of $m n$ equations in $m n$ unknowns, uniquely solvable exactly when no eigenvalue of $A$ is the negative of an eigenvalue of $B$. Solving it as a Kronecker system would cost $O(m^3 n^3)$; the Bartels-Stewart algorithm reduces $A$ and $B$ to Schur form and solves in $O(m^3 + n^3)$ flops. It appears in block diagonalization of matrices, in control theory through its special case, the [Lyapunov equation](/lyapunov-equation/), and in the perturbation theory of invariant subspaces.

## In plain words

Ordinary linear equations ask for an unknown vector that a matrix sends to a given vector. Here the unknown is a whole table of numbers, and it is multiplied by one matrix from the left and by another from the right, and the two results are added. It is still a linear problem, just a very large one if written out in full. The trick is to rotate both matrices into triangular form first; then the table can be filled in one column at a time, like back substitution.

## Definition

**Notation.** $\Lambda(A) = \{\lambda_i\}$ and $\Lambda(B) = \{\mu_j\}$ are the spectra, $\mathrm{vec}(X)$ stacks the columns of $X$, $\otimes$ is the [Kronecker product](/kronecker-product/), $\|\cdot\|_F$ the Frobenius norm, $u = 2^{-53}$, and $\hat X$ a computed solution with residual $R = C - (A\hat X + \hat X B)$.

**Input.** $A$, $B$, $C$ as above.

**Output.** $X$ with $A X + X B = C$.

**Kronecker form.** $\mathrm{vec}(A X + X B) = (I_n \otimes A + B^T \otimes I_m)\,\mathrm{vec}(X)$. The matrix $T = I_n \otimes A + B^T \otimes I_m$ of order $mn$ has eigenvalues $\lambda_i + \mu_j$. Hence:

**Theorem (solvability).** The equation has a unique solution for every $C$ if and only if $\lambda_i + \mu_j \ne 0$ for all $i$, $j$, that is, $\Lambda(A) \cap \Lambda(-B) = \emptyset$.

**Separation and condition.** The quantity $\mathrm{sep}(A, -B) = \sigma_{\min}(T) = \min_{X \ne 0} \|A X + X B\|_F/\|X\|_F$ measures how close the equation is to singular. Always $\mathrm{sep}(A, -B) \le \min_{i,j}|\lambda_i + \mu_j|$, with equality for normal $A$ and $B$, but it can be far smaller for nonnormal matrices. A relative perturbation of size $\varepsilon$ in $C$ changes $X$ by up to $\varepsilon \|C\|_F/\mathrm{sep}(A, -B)$; Higham (Chapter 16) gives the full condition number for perturbations in $A$, $B$ and $C$.

## Variants

- **$A X - X B = C$.** The classical form; solvable iff $\Lambda(A) \cap \Lambda(B) = \emptyset$. Replace $B$ by $-B$.
- **The Lyapunov equation** $A X + X A^T = -Q$, the case $B = A^T$, $C = -Q$ symmetric, and the discrete (Stein) equation $A X A^T - X = -Q$; see [Lyapunov equation](/lyapunov-equation/).
- **Generalized Sylvester equation** $A X D + E X B = C$, solved through the generalized Schur (QZ) forms.
- **Coupled Sylvester equations** $A X - Y B = C$, $D X - Y E = F$, which arise in computing deflating subspaces.
- **Large sparse coefficients with low-rank $C$.** Then $X$ is often numerically of low rank and is computed as a factor $Z Z^T$ or $Z W^T$ (Simoncini, 2016).

## Examples

**A small exact case.** With $A = \begin{pmatrix} 1 & 2 \\ 0 & 3 \end{pmatrix}$, $B = \begin{pmatrix} 1 & 0 \\ 1 & 2 \end{pmatrix}$, $C = I_2$: $\Lambda(A) = \{1, 3\}$ and $\Lambda(B) = \{1, 2\}$, all sums are nonzero, and the unique solution is
$$X = \begin{pmatrix} 37/60 & -2/15 \\ -1/20 & 1/5 \end{pmatrix},$$
which is checked by computing $A X = \begin{pmatrix} 31/60 & 4/15 \\ -3/20 & 3/5 \end{pmatrix}$ and $X B = \begin{pmatrix} 29/60 & -4/15 \\ 3/20 & 2/5 \end{pmatrix}$.

**A singular case.** $A = (1)$, $B = (-1)$: $A X + X B = 0$ for every $X$, so $C \ne 0$ has no solution and $C = 0$ has infinitely many.

**Block diagonalization.** If $M = \begin{pmatrix} A & C \\ 0 & -B \end{pmatrix}$ with $\Lambda(A) \cap \Lambda(-B) = \emptyset$, the solution of $A X + X B = -C$ gives $\begin{pmatrix} I & X \\ 0 & I \end{pmatrix}^{-1} M \begin{pmatrix} I & X \\ 0 & I \end{pmatrix} = \mathrm{diag}(A, -B)$. When $\mathrm{sep}$ is small, $X$ is large and the similarity is ill conditioned.

## Known algorithms

- **Kronecker system.** Gaussian elimination on $T$: $\tfrac23 (mn)^3$ flops and $(mn)^2$ storage. Only for tiny sizes or as a reference.
- **Bartels-Stewart (1972).** Compute real Schur forms $A = U R U^T$ and $B = V S V^T$ by the [QR algorithm](/qr-algorithm/), set $F = U^T C V$, solve the quasi-triangular equation $R Y + Y S = F$ column by column (each column, or pair of columns for a $2 \times 2$ block of $S$, is a quasi-triangular system with matrix $R + s_{jj} I$), and return $X = U Y V^T$. The Schur forms cost about $25 m^3$ and $25 n^3$ flops with the orthogonal factors, and the rest $O(m^2 n + m n^2)$.
- **Hessenberg-Schur (Golub, Nash and Van Loan, 1979).** Reduce the larger of $A$ and $B$ only to [Hessenberg form](/hessenberg-reduction/), which is cheaper than Schur form, and solve Hessenberg systems for the columns; this saves work when $m \gg n$ or $n \gg m$.
- **Recursive blocked algorithms.** Split the triangular equation into blocks to use matrix multiplication (level 3 BLAS); this is how modern libraries reach high speed.
- **Iterative and low-rank methods.** For large sparse $A$, $B$ and low-rank $C$: [ADI](/adi-method/) iterations with shifts, rational Krylov and extended Krylov projection, which produce $X \approx Z W^T$.

## Bounds

- **Lower bound.** The input has $m^2 + n^2 + mn$ entries, so $\Omega(m^2 + n^2 + mn)$ time is needed; the Schur-based methods are $O(m^3 + n^3)$, matching dense eigenvalue computation. No method is known that beats matrix multiplication exponents for general dense $A$, $B$.
- **Residual (proved).** The Bartels-Stewart solution satisfies $\|R\|_F \le c_{m,n}\, u\, (\|A\|_F + \|B\|_F)\, \|\hat X\|_F$ for a modest constant $c_{m,n}$ (Higham, Chapter 16): the relative residual is small.
- **Backward error (worst case).** Unlike a linear system, a small relative residual does not imply a small backward error in $(A, B, C)$, because the perturbations of $A$ and $B$ must keep their structure; the ratio between the two can be as large as a quantity involving the singular values of $\hat X$, so it is large when $\hat X$ is ill conditioned and $A$, $B$ are of very different norms (Higham, Chapter 16). Bartels-Stewart is therefore not backward stable in general, though it is in practice for most inputs.
- **Forward error.** $\|\hat X - X\|_F/\|X\|_F$ is bounded by the condition number times the backward error; with $\mathrm{sep}$ alone, about $u(\|A\|_F + \|B\|_F)/\mathrm{sep}(A, -B)$ to first order.

## Reductions

- **To a linear system:** the Kronecker form above, of order $mn$.
- **From the Lyapunov equation:** $B = A^T$, and the solution is symmetric when $C$ is.
- **To the eigenvalue problem:** a solution of $A X + X B = -C$ is equivalent to the invariant subspace $\mathrm{range}\begin{pmatrix} X \\ I \end{pmatrix}$ of $\begin{pmatrix} A & C \\ 0 & -B \end{pmatrix}$, and methods based on the matrix sign function compute $X$ from that block matrix.
- **From invariant subspace perturbation:** the first-order change of an invariant subspace under a perturbation solves a Sylvester equation with the two diagonal blocks of a Schur form, which is why $\mathrm{sep}$ appears in the condition of invariant subspaces (Golub and Van Loan, Section 7.6).

## Applications

- Stability analysis, Gramians and model reduction in control, through the Lyapunov special case.
- Block diagonalization and the computation of matrix functions by the Schur-Parlett method, where the off-diagonal blocks of $f(T)$ solve Sylvester equations.
- Separable PDEs on rectangles: the 5-point Laplacian system on an $m \times n$ grid is $T_m X + X T_n = F$ with $T_k = \mathrm{tridiag}(-1, 2, -1)$, and $T = I_n \otimes T_m + T_n \otimes I_m$ is the 2D Laplacian matrix; fast Poisson solvers diagonalize both $T_m$ and $T_n$.
- Eigenvector and invariant subspace refinement, and the observer design problem $A X - X F = G C$ in control.

## References
