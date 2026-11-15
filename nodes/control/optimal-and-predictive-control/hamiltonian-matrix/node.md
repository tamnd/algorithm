---
tag: PK49RX
kind: definition
slug: hamiltonian-matrix
name: Hamiltonian matrix
aliases:
- Hamiltonian matrix of the Riccati equation
area: control/optimal-and-predictive-control
level: advanced
summary: The 2n by 2n matrix [A, -BR^(-1)B^T; -Q, -A^T], whose stable invariant subspace gives the stabilizing Riccati solution.
prereqs: [continuous-algebraic-riccati-equation, eigenvalue]
see_also: [schur-method-riccati, stabilizing-riccati-solution-theorem, continuous-algebraic-riccati-equation, control-hamiltonian, costate, hamiltonian-systems, schur-decomposition, symplectic-integrators]
sources:
  - paper: doi:10.1109/TAC.1979.1102178
    title: Alan J. Laub, A Schur method for solving algebraic Riccati equations, IEEE Transactions on Automatic Control 24(6), 913-921, 1979
    locator: the Hamiltonian matrix of the CARE, its eigenvalue symmetry, and the solution from the stable invariant subspace
  - paper: doi:10.1016/0024-3795(81)90086-0
    title: Chris Paige and Charles Van Loan, A Schur decomposition for Hamiltonian matrices, Linear Algebra and its Applications 41, 11-32, 1981
    locator: the Hamiltonian Schur form under a symplectic orthogonal similarity, for matrices with no eigenvalue on the imaginary axis
  - book: isbn:9780198537953
    title: Peter Lancaster and Leiba Rodman, Algebraic Riccati Equations, Clarendon Press, Oxford, 1995
    locator: the correspondence between solutions of the Riccati equation and invariant subspaces of the Hamiltonian matrix
  - book: isbn:0134565673
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: Chapter 13, Algebraic Riccati Equations
---

The Hamiltonian matrix of the [continuous-time algebraic Riccati equation](/continuous-algebraic-riccati-equation/) $A^T P + P A - P B R^{-1} B^T P + Q = 0$ is the $2n \times 2n$ matrix

$$H = \begin{bmatrix} A & -B R^{-1} B^T \\ -Q & -A^T \end{bmatrix}.$$

It turns the quadratic matrix equation into a linear eigenvalue problem: $P$ solves the CARE exactly when the columns of $\begin{bmatrix} I \\ P \end{bmatrix}$ span an invariant subspace of $H$. Its eigenvalues are symmetric about the imaginary axis. Under the hypotheses of the [stabilizing solution theorem](/stabilizing-riccati-solution-theorem/), none of them lies on the axis, so exactly $n$ are in the open left half plane. A basis $\begin{bmatrix} X_1 \\ X_2 \end{bmatrix}$ of their invariant subspace gives the stabilizing solution $P = X_2 X_1^{-1}$. The [Schur method](/schur-method-riccati/) computes that basis. The name comes from the general class of Hamiltonian matrices, defined below, to which $H$ belongs; that class is also the matrix form of linear [Hamiltonian systems](/hamiltonian-systems/) in mechanics.

## Definition

Let $J = \begin{bmatrix} 0 & I_n \\ -I_n & 0 \end{bmatrix}$. A real matrix $H \in \mathbb{R}^{2n \times 2n}$ is *Hamiltonian* if $J H$ is symmetric, that is, $H^T J + J H = 0$.

**Block form.** Write $H = \begin{bmatrix} A & G \\ F & D \end{bmatrix}$ with $n \times n$ blocks. Then $J H = \begin{bmatrix} F & D \\ -A & -G \end{bmatrix}$, which is symmetric if and only if $F = F^T$, $G = G^T$ and $D = -A^T$. So the Hamiltonian matrices are exactly the matrices

$$H = \begin{bmatrix} A & G \\ F & -A^T \end{bmatrix}, \qquad G = G^T, \quad F = F^T.$$

The *Hamiltonian matrix of the CARE* is the case $G = -B R^{-1} B^T$ and $F = -Q$. In this area, the name refers to that matrix unless the text says otherwise.

**Origin in the LQR problem.** The [Pontryagin maximum principle](/pontryagin-maximum-principle/) for the LQR cost gives the state and [costate](/costate/) equations $\dot x = A x - B R^{-1} B^T \lambda$ and $\dot\lambda = -Q x - A^T \lambda$ (with the costate scaled so that $u = -R^{-1} B^T \lambda$). So $H$ is the coefficient matrix of the joint system in $(x, \lambda)$, and the optimal solution satisfies $\lambda = P x$.

**Eigenvalue symmetry.** From $(J H)^T = J H$ and $J^T = -J = J^{-1}$, one gets $H^T = J H J$, so $H^T = -J H J^{-1}$ is similar to $-H$. Hence $\lambda$ is an eigenvalue of $H$ if and only if $-\lambda$ is, with the same multiplicity. Since $H$ is real, $\bar\lambda$ is an eigenvalue too. So the spectrum is symmetric under $\lambda \mapsto -\bar\lambda$, the reflection in the imaginary axis, and also under $\lambda \mapsto -\lambda$ and $\lambda \mapsto \bar\lambda$.

**Riccati solutions and invariant subspaces.** For symmetric $P$, with $G = B R^{-1} B^T$,

$$H \begin{bmatrix} I \\ P \end{bmatrix} = \begin{bmatrix} A - G P \\ -Q - A^T P \end{bmatrix}, \qquad \begin{bmatrix} I \\ P \end{bmatrix} (A - G P) = \begin{bmatrix} A - G P \\ P A - P G P \end{bmatrix}.$$

The two are equal if and only if $P$ solves the CARE. Then the subspace is invariant, and the eigenvalues of $H$ on it are those of the closed loop matrix $A - G P$. Conversely, if $\begin{bmatrix} X_1 \\ X_2 \end{bmatrix}$ spans an $n$-dimensional invariant subspace and $X_1$ is invertible, then $\begin{bmatrix} I \\ X_2 X_1^{-1} \end{bmatrix}$ spans the same subspace, and $X_2 X_1^{-1}$ solves the CARE, provided it is symmetric.

**No eigenvalue on the imaginary axis.** Let $(A, B)$ be stabilizable, $(Q^{1/2}, A)$ detectable, and $R > 0$. Suppose $H \begin{bmatrix} x \\ y \end{bmatrix} = i \omega \begin{bmatrix} x \\ y \end{bmatrix}$ with $\omega$ real. The two block rows are $A x - G y = i \omega x$ and $-Q x - A^T y = i \omega y$. Multiply the first by $y^*$ on the left, take the conjugate transpose of the second and multiply it by $x$ on the right, and add. The terms $y^* A x$ and $\pm i \omega\, y^* x$ cancel, and what is left is

$$y^* G y + x^* Q x = 0.$$

Both terms are at least 0, so $B^T y = 0$ and $Q^{1/2} x = 0$. Then $A x = i \omega x$ with $Q^{1/2} x = 0$, so $x = 0$ by the [PBH test](/popov-belevitch-hautus-test/) for detectability. Also $y^* A = i \omega\, y^*$ with $y^* B = 0$, so $y = 0$ by the PBH test for stabilizability. So no eigenvector exists, and $H$ has no eigenvalue on the imaginary axis. By the symmetry, $n$ eigenvalues are in each open half plane.

**The stable subspace is Lagrangian.** Let the columns of $X \in \mathbb{C}^{2n \times n}$ span the invariant subspace of the $n$ eigenvalues in the open left half plane, so $H X = X \Lambda$ with $\Lambda$ Hurwitz. Let $M = X^* J X$, which satisfies $M^* = -M$. The matrix $X^* J H X = M \Lambda$ is Hermitian because $J H$ is symmetric, so $M \Lambda = \Lambda^* M^* = -\Lambda^* M$. That is the Lyapunov equation $\Lambda^* M + M \Lambda = 0$ with $\Lambda$ Hurwitz, whose only solution is $M = 0$. With $X = \begin{bmatrix} X_1 \\ X_2 \end{bmatrix}$, $M = X_1^* X_2 - X_2^* X_1 = 0$, so $X_1^* X_2$ is Hermitian. When $X_1$ is invertible, this gives $X_2 X_1^{-1} = X_1^{-*} (X_1^* X_2) X_1^{-1}$ Hermitian, and real for a real basis. The invertibility of $X_1$ is part of the [stabilizing solution theorem](/stabilizing-riccati-solution-theorem/).

## Examples and non-examples

**Scalar.** For $n = m = 1$, $H = \begin{bmatrix} a & -b^2 / r \\ -q & -a \end{bmatrix}$, with eigenvalues $\pm \mu$, $\mu = \sqrt{a^2 + b^2 q / r}$. For the eigenvalue $-\mu$, the first row gives $(a + \mu) x = (b^2 / r) y$, so $y / x = r (a + \mu) / b^2$. That is the stabilizing solution $p$ of the scalar CARE. For $a = b = q = r = 1$, $H = \begin{bmatrix} 1 & -1 \\ -1 & -1 \end{bmatrix}$, $\mu = \sqrt 2$ and $p = 1 + \sqrt 2$.

**Double integrator.** With $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$, $Q = I$ and $R = 1$,

$$H = \begin{bmatrix} 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & -1 \\ -1 & 0 & 0 & 0 \\ 0 & -1 & -1 & 0 \end{bmatrix}, \qquad \det(s I - H) = s^4 - s^2 + 1 = (s^2 + \sqrt 3\, s + 1)(s^2 - \sqrt 3\, s + 1).$$

The eigenvalues are $\pm \sqrt 3 / 2 \pm i / 2$, four points placed symmetrically about both axes. The stable pair $-\sqrt 3 / 2 \pm i / 2$ is the spectrum of the optimal closed loop, and its invariant subspace gives $P = \begin{bmatrix} \sqrt 3 & 1 \\ 1 & \sqrt 3 \end{bmatrix}$. The unstable pair gives the other real solution $\begin{bmatrix} -\sqrt 3 & 1 \\ 1 & -\sqrt 3 \end{bmatrix}$.

**Eigenvalues on the axis.** For $a = 0$, $b = r = 1$ and $q = 0$, $H = \begin{bmatrix} 0 & -1 \\ 0 & 0 \end{bmatrix}$ has the double eigenvalue 0, on the imaginary axis. Detectability fails, and the CARE $-p^2 = 0$ has no stabilizing solution.

**Hamiltonian, but not from an LQR problem.** $H = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}$ is Hamiltonian ($G = -1$ and $F = 1$ are symmetric), with eigenvalues $\pm i$. It is the Hamiltonian matrix of the scalar data $a = 0$, $b = r = 1$ and $q = -1$, which violates $Q \ge 0$. It is also the matrix of the harmonic oscillator $\dot x = -y$, $\dot y = x$. So a Hamiltonian matrix can have all its eigenvalues on the axis, and the no-axis result needs the LQR hypotheses.

**Not Hamiltonian.** The identity $I_2$ is not Hamiltonian: $J I_2 = J$ is skew, not symmetric, and the eigenvalues $1, 1$ are not mirrored by $-1, -1$. The matrix $\begin{bmatrix} A & G \\ F & -A^T \end{bmatrix}$ with a nonsymmetric $G$ is not Hamiltonian either, even though its diagonal blocks have the right form.

## Related definitions

- **Symplectic matrices.** $S$ is symplectic if $S^T J S = J$. If $H$ is Hamiltonian, $e^{H t}$ is symplectic for every $t$, which is why [symplectic integrators](/symplectic-integrators/) suit Hamiltonian systems. The [DARE](/discrete-algebraic-riccati-equation/) uses a symplectic matrix, with eigenvalues in pairs $\lambda$ and $1 / \bar\lambda$, in the place of $H$.
- **Hamiltonian Schur form.** If $H$ has no eigenvalue on the imaginary axis, there is a matrix $U$ that is both orthogonal and symplectic with $U^T H U = \begin{bmatrix} T & W \\ 0 & -T^T \end{bmatrix}$, $T$ upper quasi-triangular (Paige and Van Loan 1981). A method that keeps this structure in floating point would give eigenvalues that are exactly mirrored. The usual [Schur method](/schur-method-riccati/) uses the general [Schur decomposition](/schur-decomposition/) instead, which ignores the structure.
- **Skew-Hamiltonian matrices**, with $J H$ skew-symmetric. The square of a Hamiltonian matrix is skew-Hamiltonian, which some structure-preserving eigenvalue methods use.
- **Control Hamiltonian.** The scalar function $\mathcal{H}(x, u, \lambda)$ of the maximum principle ([control Hamiltonian](/control-hamiltonian/)). For the LQR problem, minimizing it over $u$ and writing the state and costate equations gives the linear system with matrix $H$.
- **Extended Hamiltonian pencil.** The $(2n + m) \times (2n + m)$ pencil that keeps $B$ and $R$ apart, so that $R^{-1}$ is never formed. It is solved with the [QZ algorithm](/qz-algorithm/).

## References
