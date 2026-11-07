---
tag: BYQ57F
kind: technique
slug: deflation
name: Deflation
aliases:
- matrix deflation
- eigenvalue deflation
area: numerical/eigenproblems
level: core
summary: Removing a known eigenpair, or a negligible coupling, from an eigenproblem so that the rest of the spectrum can be computed from a smaller or modified matrix.
prereqs: [eigenvalue, eigenvector, similarity-transformation]
see_also: [power-iteration, qr-algorithm, householder-reflections, schur-decomposition, implicitly-restarted-arnoldi, divide-and-conquer-eigensolver, subspace-iteration, wilkinson-shift]
sources:
  - book: "J. H. Wilkinson, The Algebraic Eigenvalue Problem, Oxford University Press, 1965"
    title: J. H. Wilkinson, The Algebraic Eigenvalue Problem
    locator: Chapter 9, Iterative Methods (the sections on deflation by similarity, Hotelling and Wielandt deflation, and their numerical stability)
  - book: isbn:9781611970722
    title: Yousef Saad, Numerical Methods for Large Eigenvalue Problems, revised edition, SIAM Classics in Applied Mathematics 66, 2011
    locator: Section 4.2, Deflation Techniques (Wielandt deflation, the optimality of Schur-Wielandt deflation, deflation with several vectors)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 7.5.1 (deflation in the Hessenberg QR iteration) and Section 7.4 (decoupling a block triangular form)
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Section 4.4 (deflation in the QR algorithm) and Section 5.3.3 (deflation in divide and conquer)
  - paper: doi:10.1137/S0895479801384585
    title: Karen Braman, Ralph Byers and Roy Mathias, The multishift QR algorithm. Part II, Aggressive early deflation, SIAM Journal on Matrix Analysis and Applications 23(4), 2002
    locator: pp. 948 to 973
---

Deflation is the step that removes an eigenvalue that is already known from an eigenvalue problem, so that an algorithm can go on to the others without finding the known one again. The basic form uses a similarity to bring $A$ to the block triangular form $\begin{pmatrix} \lambda_1 & b^* \\ 0 & A_2 \end{pmatrix}$ and continues with the smaller $A_2$. Other forms subtract a rank-one matrix, which keeps the size but moves $\lambda_1$ to a harmless value, or restrict the iteration to a subspace orthogonal to the converged vectors. The same word names the decision, inside the [QR algorithm](/qr-algorithm/) and other iterations, to treat a tiny entry as zero and split the problem into independent parts.

## In plain words

Many eigenvalue methods find one eigenvalue at a time, and they find the same dominant one again if you just run them again. Deflation stops this. Once you know one eigenvalue and its eigenvector, you change the matrix so that this eigenvalue is out of the way, either by cutting the matrix down by one row and one column, or by moving the found eigenvalue to zero. Then the method finds the next one.

The second meaning is about splitting. When an iteration makes an entry that links two parts of a matrix very small, you can set it to zero. The error that this makes is about as small as a rounding error. After that, each part is solved on its own, which is faster.

## When it applies

- **An eigenpair is known.** $A v_1 = \lambda_1 v_1$ with $v_1 \ne 0$, computed by the [power iteration](/power-iteration/), [inverse iteration](/inverse-iteration/) or a Krylov method. The deflation is exact if the eigenpair is exact. If the pair has a residual $r = A v_1 - \lambda_1 v_1$ with $\|v_1\|_2 = 1$, the deflated problem is exact for a matrix within $\|r\|_2$ of $A$.
- **An invariant subspace is known.** $A V_1 = V_1 \Lambda_1$ with $V_1 \in \mathbb{C}^{n \times p}$ of full rank. Every result below has a block form with $p$ columns.
- **A coupling entry is negligible.** In a Hessenberg or tridiagonal iteration, $|h_{k+1,k}|$ is of the order of $u$ times the neighbouring diagonal entries, so setting it to zero is a backward error of order $u\|A\|$. In a structured problem, such as the secular equation of [divide and conquer](/divide-and-conquer-eigensolver/), a component $z_i$ or the difference of two poles can be negligible in the same way.

It does not apply in this simple form when the known eigenvalue is defective, or so ill conditioned that its computed eigenvector carries a large error ([eigenvalue condition number](/eigenvalue-condition-number/)). The deflated matrix then inherits that error.

## The template

**Notation.** $A \in \mathbb{C}^{n \times n}$ with eigenvalues $\lambda_1, \dots, \lambda_n$, a known eigenpair $(\lambda_1, v_1)$ with $\|v_1\|_2 = 1$, and $u$ the unit roundoff.

1. **Deflation by similarity.** Choose a unitary $P$ with $P v_1 = \alpha e_1$, $|\alpha| = 1$, for example a [Householder reflector](/householder-reflections/). Then $P A P^* e_1 = \lambda_1 e_1$, so
$$P A P^* = \begin{pmatrix} \lambda_1 & b^* \\ 0 & A_2 \end{pmatrix}, \qquad \det(zI - A) = (z - \lambda_1)\det(zI - A_2),$$
and $A_2$ of order $n - 1$ has the eigenvalues $\lambda_2, \dots, \lambda_n$. Continue with $A_2$. Repeating this builds the [Schur decomposition](/schur-decomposition/) column by column. An eigenvector $w$ of $A_2$ for $\lambda_i \ne \lambda_1$ gives the eigenvector $P^* \begin{pmatrix} \gamma \\ w \end{pmatrix}$ of $A$ with $\gamma = b^* w / (\lambda_i - \lambda_1)$.
2. **Deflation by a rank-one change (Wielandt).** For any vector $x$, the matrix $B = A - v_1 x^*$ has the eigenvalues
$$\lambda_1 - x^* v_1, \ \lambda_2, \ \dots, \ \lambda_n \qquad \text{(Brauer 1952).}$$
*Proof.* Take any nonsingular $S$ with first column $v_1$. Then $S^{-1} A S$ has first column $\lambda_1 e_1$, and $S^{-1} v_1 x^* S = e_1 (x^* S)$ is nonzero only in its first row. So $S^{-1} B S$ is block upper triangular, with the $(1,1)$ entry $\lambda_1 - x^* v_1$ and the same trailing block as $S^{-1} A S$. $\square$ With $x^* v_1 = \lambda_1$ the known eigenvalue moves to 0. Hotelling's choice $x = \bar\lambda_1 v_1$ is the natural one for Hermitian $A$, where it keeps all the other eigenvectors. Wielandt's choice $x^* = e_i^* A / (v_1)_i$, row $i$ of $A$ scaled, makes row $i$ of $B$ zero, so that row and column $i$ can be dropped.
3. **Deflation by orthogonal projection (locking).** Keep the iteration orthogonal to the converged vectors: in the power or [subspace iteration](/subspace-iteration/), multiply by $(I - V_1 V_1^*) A$, or orthogonalize each new vector against $V_1$. With an orthonormal Schur basis $V_1$, this is the Schur-Wielandt deflation of Saad, Section 4.2, which keeps the remaining eigenvalues and is well conditioned.
4. **Deflation by splitting.** In the Hessenberg QR iteration, after each step test
$$|h_{k+1,k}| \le u \, (|h_{kk}| + |h_{k+1,k+1}|).$$
If it holds, set $h_{k+1,k} = 0$. The matrix is then block upper triangular, and the two diagonal blocks are treated separately. The error is a perturbation of norm at most $u\|H\|_F$, so it is backward stable.

## Classic examples

- **Similarity, $3 \times 3$.** $A = \begin{pmatrix} 3 & 1 & -1 \\ -1 & 5 & 1 \\ -2 & 2 & 4 \end{pmatrix}$ has the eigenpairs $(2, (1,0,1))$, $(4, (1,1,0))$ and $(6, (0,1,1))$. With $v_1 = (0, 1, 1)/\sqrt{2}$ and the Householder reflector $P$ that maps $v_1$ to $-e_1$,
$$P A P = \begin{pmatrix} 6 & -2.207107 & -0.792893 \\ 0 & 1.939340 & 0.353553 \\ 0 & -0.353553 & 4.060660 \end{pmatrix}.$$
The trailing block has trace 6 and determinant 8, so its eigenvalues are 4 and 2.
- **Wielandt, $2 \times 2$.** $A = \begin{pmatrix} 4 & 1 \\ 2 & 3 \end{pmatrix}$ has $\lambda_1 = 5$ with $v_1 = (1, 1)^T$ (not normalized, with $x^* v_1 = 5$). With $x^* = $ row 1 of $A$ $= (4, 1)$, $B = A - v_1 x^* = \begin{pmatrix} 0 & 0 \\ -2 & 2 \end{pmatrix}$, whose eigenvalues are 0 and 2. Row 1 of $B$ is zero, as Wielandt's choice promises.
- **Hotelling with the power iteration.** For the Toeplitz matrix $T = \operatorname{tridiag}(-1, 2, -1)$ of order 4, with $\lambda_1 = 3.618034$ and its unit eigenvector $v_1$, the power iteration on $T - \lambda_1 v_1 v_1^T$ converges to $\lambda_2 = 2.618034$. The error of the Rayleigh quotient is $4.7 \times 10^{-6}$ after 10 steps and $1.3 \times 10^{-11}$ after 20. That is a factor of 0.279 per step, which is $(\lambda_3/\lambda_2)^2 = (1.381966/2.618034)^2$, as the theory of the power iteration predicts for the deflated matrix.
- **Deflation in the QR algorithm.** Each time a subdiagonal entry of the Hessenberg iterate passes the test of step 4, one eigenvalue (a $1 \times 1$ block) or a complex pair (a $2 \times 2$ block) is found, and the iteration works on the remaining active window. With the [Wilkinson shift](/wilkinson-shift/), one to two steps per eigenvalue are typical; this count is observed, not proved.
- **Aggressive early deflation.** Braman, Byers and Mathias (2002) compute a Schur form of a trailing window of the Hessenberg matrix and test the spike of entries that couples it to the rest. They often find many negligible entries before any subdiagonal entry is small. This is the main reason why the modern LAPACK QR code `xHSEQR` is fast.
- **Divide and conquer.** In the symmetric rank-one update $D + \rho z z^T$, a tiny component $z_i$ leaves $d_i$ as an eigenvalue, and two equal poles $d_i = d_j$ can be merged by a rotation. Both cases are removed before the secular equation is solved.
- **Implicit restarts.** In the [implicitly restarted Arnoldi method](/implicitly-restarted-arnoldi/), converged Ritz vectors are "locked" (kept and no longer updated), and unwanted converged ones are "purged".

## Variations

- **Block deflation.** For an invariant subspace with orthonormal basis $V_1$ and $\Lambda_1 = V_1^* A V_1$, complete $V_1$ to a unitary $[V_1, V_2]$. Then $V_2^* A V_2$ has the remaining eigenvalues.
- **Rank-one deflation that keeps sparsity.** Do not form $A - v_1 x^*$; apply it as $y \mapsto A y - v_1 (x^* y)$. The cost is one product with $A$ and $O(n)$ more flops.
- **Deflation by shifting a known eigenvalue away.** For Hermitian $A$, $A + \sigma v_1 v_1^*$ moves $\lambda_1$ to $\lambda_1 + \sigma$. This is used to remove a known null space, for example the constant vector of a graph Laplacian.
- **Deflation in linear solvers.** Deflated CG and deflated GMRES remove the small eigenvalues that slow down a Krylov solver by projecting them out. The idea is the same, but the purpose is a faster linear solve.
- **Polynomial deflation.** Dividing a computed root out of a polynomial is the same idea for the roots of a polynomial. Wilkinson showed that it is stable if the roots are removed in increasing order of modulus, and that the computed roots should be refined on the original polynomial.

## Pitfalls

- **Errors accumulate in repeated deflation.** An eigenvector error of size $\varepsilon$ gives a perturbation of order $|\lambda_1| \varepsilon$ in the Hotelling or Wielandt matrix. After $m$ deflations the later eigenvalues carry the sum of the earlier errors. Refine each deflated result on the original $A$, for example by a few steps of [inverse iteration](/inverse-iteration/).
- **Hotelling for a non-Hermitian matrix.** By Brauer's theorem, $A - \lambda_1 v_1 v_1^*$ still has the eigenvalues $0, \lambda_2, \dots, \lambda_n$, but its eigenvectors are not those of $A$. They must be mapped back with $v_i = w_i + \gamma_i v_1$, $\gamma_i = (x^* w_i)/(\lambda_i - \lambda_1)$.
- **Wielandt with a tiny component.** Wielandt's choice divides by $(v_1)_i$; choose $i$ with $|(v_1)_i|$ largest, or the row will be badly scaled.
- **Forming dense rank-one updates of sparse matrices.** $A - v_1 x^*$ is dense; it wastes memory and time. Apply it implicitly.
- **A stopping test that is too loose.** Setting $h_{k+1,k}$ to zero when it is only small relative to $\|H\|$, not to its neighbours, is still normwise backward stable, but it can lose the relative accuracy of tiny eigenvalues of graded matrices. A stricter test is due to Ahues and Tisseur (1997) and is used in LAPACK.
- **Deflating an eigenvalue that has not converged.** A pair with a large residual leaves a large error in the deflated matrix. Deflate only when the residual is of order $u\|A\|$, or keep the pair in the active window.

## Exercises

1. Show that the vector $\begin{pmatrix} \gamma \\ w \end{pmatrix}$ with $\gamma = b^* w / (\lambda_i - \lambda_1)$ is an eigenvector of $\begin{pmatrix} \lambda_1 & b^* \\ 0 & A_2 \end{pmatrix}$ when $A_2 w = \lambda_i w$ and $\lambda_i \ne \lambda_1$.
2. Show that for Hermitian $A$ and $x = \lambda_1 v_1$, every eigenvector $v_i$ of $A$ with $i \ge 2$ is also an eigenvector of $A - \lambda_1 v_1 v_1^*$. Give a $2 \times 2$ nonsymmetric example where this fails.
3. Prove the bound: if $\|A v_1 - \lambda_1 v_1\|_2 = \rho$ with $\|v_1\|_2 = 1$, then deflation by the similarity of step 1 gives a matrix $P A P^*$ whose first column is $\lambda_1 e_1$ up to a vector of norm $\rho$. Deduce that $A_2$ has the remaining eigenvalues of a matrix $A + E$ with $\|E\|_2 \le \rho$.
4. For the QR test $|h_{k+1,k}| \le u(|h_{kk}| + |h_{k+1,k+1}|)$, show that setting $h_{k+1,k}$ to zero is a perturbation $E$ with $\|E\|_F \le u\|H\|_F \sqrt{2}$.
5. Apply Wielandt deflation with $i = 2$ to the $3 \times 3$ example above and $v_1 = (0, 1, 1)^T$. Check that the remaining $2 \times 2$ block, obtained by deleting row and column 2, has the eigenvalues 2 and 4.

## References
