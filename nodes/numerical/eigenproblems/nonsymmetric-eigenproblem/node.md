---
tag: ZKTWNC
kind: problem
slug: nonsymmetric-eigenproblem
name: Nonsymmetric eigenproblem
aliases:
- general eigenproblem
- unsymmetric eigenvalue problem
- nonsymmetric eigenvalue problem
area: numerical/eigenproblems
level: core
summary: Compute the eigenvalues, and if asked a Schur form or eigenvectors, of a general square matrix. The eigenvalues may be complex, defective and badly conditioned.
model: floating-point-model
complexity:
  vars: {n: "the order of A"}
  time: {worst: O(n^3)}
  flops: {eigenvalues: "10 n^3", schur: "25 n^3"}
prereqs: [eigenvalue-problem, schur-decomposition, backward-error-analysis]
see_also: [qr-algorithm, francis-double-shift-qr, hessenberg-reduction, matrix-balancing, eigenvalue-condition-number, pseudospectrum, bauer-fike-theorem, arnoldi-iteration]
sources:
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Chapter 7, Unsymmetric Eigenvalue Problems (Section 7.1 properties and the real Schur form, Section 7.2 perturbation theory, Sections 7.4 and 7.5 the Hessenberg QR algorithm and its cost, Section 7.6 invariant subspaces and eigenvectors)
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lectures 24 to 29 (eigenvalue problems, overview of algorithms, reduction to Hessenberg form, QR algorithm)
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Chapter 4, Nonsymmetric Eigenvalue Problems (Section 4.2 canonical forms, Section 4.3 perturbation theory, Section 4.4 algorithms)
  - book: "J. H. Wilkinson, The Algebraic Eigenvalue Problem, Oxford University Press, 1965"
    title: J. H. Wilkinson, The Algebraic Eigenvalue Problem
    locator: Chapter 2 (perturbation theory, the condition numbers 1/|s_i|) and Chapter 8 (the LR and QR algorithms)
  - paper: "F. L. Bauer and C. T. Fike, Norms and exclusion theorems, Numerische Mathematik 2, 1960"
    title: Norms and exclusion theorems
    locator: Numer. Math. 2 (1960), pp. 137 to 141
  - paper: "Karen Braman, Ralph Byers and Roy Mathias, The multishift QR algorithm. Part II: Aggressive early deflation, SIAM Journal on Matrix Analysis and Applications 23, 2002"
    title: "The multishift QR algorithm. Part II: Aggressive early deflation"
    locator: SIAM J. Matrix Anal. Appl. 23(4) (2002), pp. 948 to 973
  - paper: "Jess Banks, Jorge Garza-Vargas, Archit Kulkarni and Nikhil Srivastava, Pseudospectral shattering, the sign function, and diagonalization in nearly matrix multiplication time, Foundations of Computational Mathematics 23, 2023"
    title: Pseudospectral shattering, the sign function, and diagonalization in nearly matrix multiplication time
    locator: the main theorem (randomized backward-approximate diagonalization)
---

The nonsymmetric eigenproblem asks for the [eigenvalues](/eigenvalue/) of a general square matrix $A$, with no symmetry assumed, and often for a [Schur decomposition](/schur-decomposition/) $A = Q T Q^*$ or for eigenvectors as well. It is harder than the [symmetric eigenproblem](/symmetric-eigenproblem/) in three ways: the eigenvalues of a real matrix can be complex, the matrix may have no basis of eigenvectors, and an eigenvalue can move by far more than the perturbation of the matrix. The standard dense method, [Hessenberg reduction](/hessenberg-reduction/) followed by the shifted [QR algorithm](/qr-algorithm/), is backward stable and costs about $10n^3$ flops for the eigenvalues, but its convergence is observed rather than proved, and the accuracy of what it returns is limited by the conditioning of each eigenvalue.

## In plain words

A square table of numbers acts on arrows by stretching and turning them. For a symmetric table there are always enough special directions that are only stretched, they are at right angles to each other, and small changes in the table only change the stretch amounts a little. For a general table none of this holds. Some stretch amounts are complex numbers, which describe a turn as well as a stretch. Special directions can almost coincide or even merge, and then a tiny change in the table can move a stretch amount a lot. Good methods give the exact answer for a table that is wrong only in the last digits; how close that is to the true answer depends on the table.

## Definition

**Notation.** $A \in \mathbb C^{n \times n}$, often real, with eigenvalues $\lambda_1, \dots, \lambda_n$ counted with multiplicity and ordered by modulus, $|\lambda_1| \ge \dots \ge |\lambda_n|$. A right eigenvector $x$ satisfies $A x = \lambda x$ and a left eigenvector $y$ satisfies $y^* A = \lambda y^*$. The Schur form is $A = Q T Q^*$ with $Q$ unitary and $T$ upper triangular; $H$ denotes an upper Hessenberg matrix. $u$ is the unit roundoff and $\kappa_2(V) = \|V\|_2 \|V^{-1}\|_2$.

**The exact problem.** Input: $A$. Output: the roots $\lambda_1, \dots, \lambda_n$ of $\det(t I - A)$; optionally a Schur decomposition, or, when $A$ is [diagonalizable](/diagonalization/), a nonsingular $V$ with $A = V \Lambda V^{-1}$. For a real $A$ the output is usually the real Schur form $A = Q T Q^T$ with $Q$ real orthogonal and $T$ real and block upper triangular with $1 \times 1$ blocks for real eigenvalues and $2 \times 2$ blocks for complex conjugate pairs. It exists for every real $A$ (GVL Section 7.4) and avoids complex arithmetic.

**The floating-point problem.** Return a computed $\hat T$ (triangular, or quasi-triangular in the real case) and optionally $\hat Q$ such that $\hat T = Q^* (A + E) Q$ for an exactly unitary $Q$ with $\|\hat Q - Q\|_2 \le c(n) u$ and $\|E\|_2 \le c(n) u \|A\|_2$, where $c(n)$ is a modest polynomial. The computed eigenvalues are the diagonal entries (or block eigenvalues) of $\hat T$. This is the backward stability that the Hessenberg QR algorithm achieves (GVL Section 7.5; Wilkinson 1965, Chapter 8).

**The conditioning of one eigenvalue.** For a simple eigenvalue $\lambda$ with right and left eigenvectors $x$ and $y$, and a perturbation $A + \epsilon F$,

$$\lambda(\epsilon) = \lambda + \epsilon \, \frac{y^* F x}{y^* x} + O(\epsilon^2), \qquad \kappa(\lambda) = \frac{\|x\|_2 \|y\|_2}{|y^* x|} \ge 1 .$$

So the [eigenvalue condition number](/eigenvalue-condition-number/) $\kappa(\lambda)$ is the secant of the angle between the left and right eigenvectors. It equals 1 for every eigenvalue of a normal matrix and can be arbitrarily large otherwise. The first-order forward error of a backward stable method is $\kappa(\lambda) \, c(n) \, u \, \|A\|_2$.

## Variants

- **Eigenvalues only.** About $10n^3$ flops (typical) by Hessenberg reduction and Francis QR, without accumulating $Q$.
- **Schur form.** About $25n^3$ flops (typical) with $Q$ and $T$. The Schur vectors span nested invariant subspaces and are computed stably, even for defective matrices.
- **Eigenvectors.** From the Schur form, the eigenvectors of $T$ by back substitution, then multiplied by $Q$ (LAPACK `xTREVC`). They are accurate only when the eigenvalue is well separated, and for a defective eigenvalue they do not form a basis.
- **Invariant subspaces.** Reorder the Schur form so that a chosen cluster of eigenvalues comes first (LAPACK `xTRSEN`); the first columns of $Q$ then span the invariant subspace, which is better conditioned than the individual eigenvectors of the cluster.
- **A few eigenvalues of a large sparse $A$.** Use products $x \mapsto A x$ only: the [Arnoldi iteration](/arnoldi-iteration/), [implicitly restarted Arnoldi](/implicitly-restarted-arnoldi/) (ARPACK), shift-and-invert, and [power iteration](/power-iteration/) for the dominant eigenvalue.
- **Structured cases.** Nonnegative matrices ([Perron-Frobenius theorem](/perron-frobenius-theorem/)), stochastic matrices of a [Markov chain](/markov-chain/), companion matrices from [polynomial root finding](/polynomial-root-finding/), and the [generalized problem](/generalized-eigenvalue-problem/) $A x = \lambda B x$ solved by the [QZ algorithm](/qz-algorithm/).

## Examples

**Complex eigenvalues of a real matrix.** $\begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}$ has eigenvalues $\pm i$. It is already in real Schur form: one $2 \times 2$ block. No real arithmetic method can make it triangular.

**A companion matrix and its condition numbers.** $A = \begin{pmatrix} 6 & -11 & 6 \\ 1 & 0 & 0 \\ 0 & 1 & 0 \end{pmatrix}$ has the characteristic polynomial $(t - 1)(t - 2)(t - 3)$. The right eigenvector of $\lambda$ is $x = (\lambda^2, \lambda, 1)^T$, and the left eigenvectors are $(-1, 5, -6)$, $(-2, 8, -6)$ and $(-3, 9, -6)$. So $\kappa(1) = 6.82$, $\kappa(2) = 23.37$ and $\kappa(3) = 17.85$. Changing $a_{11}$ from 6 to $6 + \epsilon$ moves the eigenvalues by $0.5\epsilon$, $-4\epsilon$ and $4.5\epsilon$ to first order, which is $\epsilon \, y_1 x_1 / (y^* x)$ for each; a numerical root of the perturbed cubic with $\epsilon = 10^{-6}$ confirms these values to five digits, and their sum is $\epsilon$, the change of the trace.

**A nonnormal $2 \times 2$ matrix.** $A = \begin{pmatrix} 1 & 100 \\ 0 & 2 \end{pmatrix}$ has the eigenvalue 1 with $x = e_1$ and $y = (1, -100)^T$, so $\kappa(1) = \sqrt{10001} \approx 100$. Putting $\epsilon = 10^{-8}$ in position $(2, 1)$ moves the eigenvalue 1 to $1 - 0.99999 \times 10^{-6}$, a change 100 times larger than $\epsilon$.

**A defective matrix.** The $10 \times 10$ Jordan block $J_{10}(0)$ with $10^{-10}$ added in position $(10, 1)$ has the characteristic polynomial $t^{10} - 10^{-10}$, so all ten eigenvalues have modulus $0.1$. A perturbation of size $\epsilon$ moves a defective eigenvalue of index $m$ by about $\epsilon^{1/m}$.

**A matrix on which plain shifts stall.** The cyclic permutation matrix with ones in positions $(i + 1, i)$ and $(1, n)$ is upper Hessenberg and unitary, with eigenvalues the $n$-th roots of unity. With the Rayleigh shift $h_{nn} = 0$, one QR step returns the same matrix, so unshifted and Rayleigh-shifted QR make no progress. Practical codes apply an exceptional shift after about 10 iterations without deflation.

## Known algorithms

| algorithm | what it computes | cost (leading term) | status of the count |
|---|---|---|---|
| [matrix balancing](/matrix-balancing/) | a diagonal similarity that reduces $\|A\|$ | $O(n^2)$ per sweep | a few sweeps, observed |
| [Hessenberg reduction](/hessenberg-reduction/) | $H = Q_0^* A Q_0$ | $10n^3/3$ flops, $14n^3/3$ with $Q_0$ | exact count |
| [QR algorithm](/qr-algorithm/) with the [Francis double shift](/francis-double-shift-qr/) | real Schur form | about $10n^3$ in total for eigenvalues, $25n^3$ with $Q$ and $T$ (GVL Section 7.5) | typical: assumes about 2 iterations per eigenvalue |
| multishift QR with aggressive early deflation | real Schur form | same order, faster in practice (Braman, Byers and Mathias 2002) | typical |
| triangular back substitution | eigenvectors of $T$, then $Q$ times them | $O(n^3)$ | exact |
| [inverse iteration](/inverse-iteration/) | one eigenvector for a computed eigenvalue | $O(n^2)$ per step on $H$ | one or two steps, typical |
| [Arnoldi](/arnoldi-iteration/) and [implicitly restarted Arnoldi](/implicitly-restarted-arnoldi/) | a few eigenpairs of a large sparse $A$ | matrix-vector products plus $O(n k^2)$ per restart | depends on the spectrum |
| Banks, Garza-Vargas, Kulkarni and Srivastava (2023) | an approximate diagonalization | $O(T_{MM}(n) \log^2(n/\delta))$ arithmetic operations, randomized | proved, in floating point with $O(\log^4(n/\delta) \log n)$ bits of precision |

## Bounds

- **No finite algorithm.** Every monic polynomial is the characteristic polynomial of its companion matrix, so by the [Abel-Ruffini theorem](/abel-ruffini-theorem/) no method with finitely many arithmetic operations and radicals solves the problem for all $n \ge 5$.
- **Convergence of QR.** For the symmetric tridiagonal QR algorithm with the [Wilkinson shift](/wilkinson-shift/), global convergence is proved. For the nonsymmetric QR algorithm with Francis shifts, no global convergence proof is known, and there are matrices on which it cycles without exceptional shifts. The $O(n^3)$ total is a count based on the observed number of iterations per eigenvalue, about 2 for the Francis double shift.
- **[Bauer-Fike](/bauer-fike-theorem/).** If $A = V \Lambda V^{-1}$ is diagonalizable and $\mu$ is an eigenvalue of $A + E$, then $\min_i |\mu - \lambda_i| \le \kappa_p(V) \, \|E\|_p$ for every $p$-norm with $1 \le p \le \infty$ (Bauer and Fike 1960). For a normal $A$, $\kappa_2(V) = 1$.
- **Defective eigenvalues.** If $\lambda$ has a Jordan block of size $m$, perturbations of size $\epsilon$ can move it by a quantity of order $\epsilon^{1/m}$, and the Jordan example shows that this is attained.
- **Backward error is the right goal.** The Hessenberg QR algorithm returns the exact Schur form of $A + E$ with $\|E\|_2 \le c(n) u \|A\|_2$. No method can guarantee a forward error better than about $\kappa(\lambda) u \|A\|$ for all inputs, because the input itself is known only to rounding accuracy.
- **Nonnormality.** The departure from normality $\Delta(A) = (\|A\|_F^2 - \sum_i |\lambda_i|^2)^{1/2}$ is the Frobenius norm of the strictly upper part of any Schur factor $T$ (Henrici 1962). When it is large, the eigenvalues alone say little about $\|A^k\|$ or $\|e^{tA}\|$, and the [pseudospectrum](/pseudospectrum/) is the better description.

## Reductions

- **To Hessenberg form.** A unitary similarity reduces $A$ to upper Hessenberg $H$ in $10n^3/3$ flops; all later QR steps then cost $O(n^2)$ each and keep the Hessenberg form.
- **Splitting by permutation.** A symmetric permutation $P^T A P$ is block upper triangular with irreducible diagonal blocks, one for each [strongly connected component](/strongly-connected-components/) of the graph of $A$, and the eigenvalues are those of the blocks. Balancing codes find the isolated eigenvalues this way before scaling.
- **Polynomial roots.** The roots of a monic polynomial are the eigenvalues of its [companion matrix](/companion-matrix-method/), which is the way MATLAB's `roots` computes them.
- **Generalized problem.** If $B$ is nonsingular and well conditioned, $A x = \lambda B x$ is the standard problem for $B^{-1} A$. In general it is solved by QZ without inverting $B$.
- **Eigenvalues and singular values.** $z$ is an eigenvalue of $A$ exactly when $\sigma_{\min}(A - z I) = 0$; the $\epsilon$-pseudospectrum is the set where $\sigma_{\min}(A - zI) \le \epsilon$.
- **Characteristic polynomial.** For exact or rational input, computing $\det(tI - A)$ by a [characteristic polynomial algorithm](/characteristic-polynomial-computation/) and isolating its roots is exact. In floating point it is unstable and is not used.

## Applications

Stability of linear and linearized dynamical systems, where $x' = A x$ is stable when every eigenvalue has negative real part and $x_{k+1} = A x_k$ when every eigenvalue is inside the unit disc; control design by pole placement; stationary distributions and mixing of Markov chains; population models with nonnegative matrices; [PageRank](/pagerank/) and [eigenvector centrality](/eigenvector-centrality/) on directed graphs; the roots of polynomials; and the analysis of iterative methods through the [spectral radius](/spectral-radius/). In fluid mechanics and other strongly nonnormal problems, the eigenvalues predict the long-time behaviour, and pseudospectra explain the transient growth.

## References
