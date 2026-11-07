---
tag: ADBYNC
kind: algorithm
slug: francis-double-shift-qr
name: Francis double-shift QR step
aliases:
- implicit double-shift QR
- Francis QR step
- Francis algorithm
area: numerical/eigenproblems
level: advanced
summary: One QR step of a real Hessenberg matrix with a shift pair, done in real arithmetic by chasing a 3 by 3 bulge. Repeated with deflation, it is the standard dense real eigensolver.
solves: [nonsymmetric-eigenproblem]
model: floating-point-model
complexity:
  vars: {n: "the order of A"}
  time: {per_step: O(n^2), typical: O(n^3)}
  space: {worst: Θ(n^2)}
  flops: {per_step: "10n^2", eigenvalues: "10n^3", with_q: "25n^3"}
properties: {deterministic: true, in_place: true, recursive: false, iterative: true}
history:
  year: 1961
  people: [John G. F. Francis, Vera N. Kublanovskaya, James H. Wilkinson]
  note: Francis published the QR algorithm with the implicit double shift in 1961 and 1962; Kublanovskaya found the QR iteration independently in 1961.
prereqs: [qr-algorithm, hessenberg-reduction, householder-reflections]
see_also: [schur-decomposition, nonsymmetric-eigenproblem, wilkinson-shift, deflation, matrix-balancing, implicitly-restarted-arnoldi, qz-algorithm, eigenvalue-condition-number]
sources:
  - paper: doi:10.1093/comjnl/4.3.265
    title: J. G. F. Francis, The QR transformation, a unitary analogue to the LR transformation, Part 1, The Computer Journal 4, 1961
    locator: pp. 265 to 271
  - paper: doi:10.1093/comjnl/4.4.332
    title: J. G. F. Francis, The QR transformation, Part 2, The Computer Journal 4, 1962
    locator: pp. 332 to 345 (the implicit double shift and the bulge chase)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 7.5, The Practical QR Algorithm (the implicit Q theorem, the Francis QR step, deflation and the overall flop counts)
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Section 4.4, Algorithms for the Nonsymmetric Eigenproblem (Hessenberg QR iteration and the implicit double shift)
  - book: "J. H. Wilkinson, The Algebraic Eigenvalue Problem, Oxford University Press, 1965"
    title: J. H. Wilkinson, The Algebraic Eigenvalue Problem
    locator: Chapter 8, The LR and QR Algorithms (the double-shift technique and its error analysis)
  - book: isbn:9780898716412
    title: David S. Watkins, The Matrix Eigenvalue Problem, GR and Krylov Subspace Methods, SIAM, 2007
    locator: Chapter 4, Iteration (implicit double steps, bulge chasing and convergence)
  - paper: doi:10.4169/amer.math.monthly.118.05.387
    title: David S. Watkins, Francis's algorithm, American Mathematical Monthly 118, 2011
    locator: pp. 387 to 403 (the bulge chase explained without the implicit Q theorem)
---

The Francis double-shift QR step performs two steps of the shifted [QR algorithm](/qr-algorithm/) on a real upper Hessenberg matrix $H$, with shifts $\mu_1$ and $\mu_2$ that are real or a complex conjugate pair, entirely in real arithmetic. It never forms $M = (H - \mu_1 I)(H - \mu_2 I)$. It computes only the first column of $M$, applies a $3 \times 3$ Householder reflector that creates a bulge below the subdiagonal, and chases the bulge down and out of the matrix. By the implicit Q theorem the result equals the explicit double step. One step costs about $10n^2$ flops. Repeated with the eigenvalues of the trailing $2 \times 2$ block as shifts, and with deflation, it reduces a real matrix to real [Schur form](/schur-decomposition/) in about $10n^3$ flops for eigenvalues and $25n^3$ with the Schur vectors. This is the method of LAPACK's `xHSEQR` and of MATLAB's `eig` for small and medium real matrices.

## In plain words

The shifted QR algorithm finds eigenvalues by repeating one step that keeps the eigenvalues and makes the entries under the diagonal smaller. The best shifts are guesses of eigenvalues, and for a real matrix those guesses can be complex. Complex arithmetic would cost more and would give a complex answer for a real problem.

Francis found that two steps with a complex guess and its mirror image can be done together in real arithmetic. He also found that the double step does not have to be done the obvious way. You start a small disturbance in the top-left corner, then push it down the diagonal one position at a time, and when it falls out at the bottom the step is complete. The work stays small, and the matrix keeps its shape.

## The problem

**Notation.** $A \in \mathbb{R}^{n \times n}$ with eigenvalues $\lambda_1, \dots, \lambda_n$; complex ones come in conjugate pairs. $H = Q_0^T A Q_0$ is the upper Hessenberg form from [Hessenberg reduction](/hessenberg-reduction/). *Unreduced* means that every subdiagonal entry $h_{j+1,j}$ is nonzero. The real Schur form is $A = Q T Q^T$ with $Q$ orthogonal and $T$ quasi upper triangular: block upper triangular with $1 \times 1$ blocks for real eigenvalues and $2 \times 2$ blocks for complex conjugate pairs. $u$ is the unit roundoff.

**One step.** Given an unreduced real Hessenberg $H$ and real $s, t$, the shifts $\mu_1, \mu_2$ being the roots of $z^2 - s z + t$, compute an orthogonal $Z$ with $Z e_1$ parallel to $M e_1$, $M = H^2 - s H + t I$, such that $Z^T H Z$ is again upper Hessenberg.

**The full algorithm.** Given $A$, compute $Q$ and $T$ of the real Schur form, or only the eigenvalues, by Hessenberg reduction followed by Francis steps with deflation.

## The algorithm

```pseudo id=main
FRANCIS-STEP(H, l, h, s, t)        ▷ window l..h of H, unreduced, h ≥ l + 2
L1  x ← h_ll² + h_l,l+1 h_l+1,l − s h_ll + t;  y ← h_l+1,l (h_ll + h_l+1,l+1 − s);  z ← h_l+1,l h_l+2,l+1
L2  for k ← l to h − 2 do
L3      P ← 3 × 3 Householder reflector with P (x, y, z)ᵀ = ±‖(x, y, z)‖₂ e₁
L4      H ← P H P on rows and columns k, k+1, k+2;  Q ← Q P    ▷ create, then chase, the bulge
L5      (x, y, z) ← (h_k+1,k, h_k+2,k, h_k+3,k), with z ← 0 when k = h − 2
L6  P ← 2 × 2 Householder reflector with P (x, y)ᵀ = ±‖(x, y)‖₂ e₁
L7  H ← P H P on rows and columns h − 1, h;  Q ← Q P
FRANCIS-QR(A)                        ▷ after H = Q₀ᵀ A Q₀; repeat L8 to L11 until no rows are left
L8  find the largest l ≤ h with |h_l,l−1| ≤ u (|h_l−1,l−1| + |h_ll|), and set h_l,l−1 ← 0
L9  if l = h or l = h − 1 then store the eigenvalues of the 1 × 1 or 2 × 2 block, h ← l − 1
L10 else s, t ← trace and determinant of the trailing 2 × 2 block of the window (exceptional values every 10th step)
L11     FRANCIS-STEP(H, l, h, s, t)
```

Line L1 is the first column of $M = H^2 - sH + tI$ restricted to the window; only its first three entries are nonzero because $H$ is Hessenberg. Line L4 applied at $k = l$ fills the entries $(l + 2, l)$, $(l + 3, l)$ and $(l + 3, l + 1)$, the bulge. Each later reflector zeros the two entries of column $k$ below the subdiagonal and moves the bulge one row and column down. With a Schur form wanted, the reflectors act on whole rows and columns of $H$ and on $Q$; for eigenvalues only, they act on the window. Line L9 also splits a $2 \times 2$ block with real eigenvalues by a rotation, so that $T$ has $2 \times 2$ blocks only for complex pairs. The shifts of line L10 are the two eigenvalues of the trailing $2 \times 2$ block, the double-shift analog of the [Wilkinson shift](/wilkinson-shift/). Every tenth step on the same window uses the exceptional shift of LAPACK's `xLAHQR` instead, and the implementation stops with an error after 30 steps.

## Example

The companion matrix of $z^4 - 5z^3 + 7z^2 - 5z + 6 = (z^2 + 1)(z - 2)(z - 3)$ is already upper Hessenberg:
$$H = \begin{pmatrix} 5 & -7 & 5 & -6 \\ 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \end{pmatrix}, \qquad \lambda = 3,\ 2,\ i,\ -i.$$
The trailing block $\begin{pmatrix} 0 & 0 \\ 1 & 0 \end{pmatrix}$ gives $s = t = 0$ in the first step. The subdiagonal entries before each Francis step are:

| step | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| $\lvert h_{43} \rvert$ | 1.0 | 2.2269 | 0.53055 | 0.65864 | 1.7693 | 0.52815 |
| $\lvert h_{32} \rvert$ | 1.0 | 0.26399 | 0.072807 | $7.3432 \times 10^{-4}$ | $5.1034 \times 10^{-8}$ | $1.1984 \times 10^{-15}$ |

After step 6, $|h_{32}| \le u (|h_{22}| + |h_{33}|)$, so it is set to zero, and the matrix splits into two $2 \times 2$ blocks. The trailing block is about $\begin{pmatrix} -0.4322 & 0.6815 \\ -1.742 & 0.4322 \end{pmatrix}$, with trace 0 and determinant 1, so its eigenvalues are $\pm i$. The leading block has real eigenvalues and is split by a rotation into the diagonal entries 3 and 2. The entry $h_{43}$ never converges, because it lies inside the block of a complex pair; this is how the real algorithm reports complex eigenvalues. The entry $h_{32}$ converges quadratically: $7.34 \times 10^{-4} / 0.0728^2 \approx 0.14$ and $5.10 \times 10^{-8} / (7.34 \times 10^{-4})^2 \approx 0.095$. The final $Q T Q^T$ agrees with $H$ to $6.2 \times 10^{-15}$.

For a random $40 \times 40$ matrix with Gaussian entries (seed 3), the implementation used 78 double steps, 1.95 per eigenvalue, and reproduced $A$ to $1.8 \times 10^{-14}$.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md).

1. **One step is a similarity with the right first column.** Lines L1 to L7 compute $Z^T H Z$ with $Z = P_l P_{l+1} \cdots P_{h-1}$ orthogonal and $Z e_1 = P_l e_1$ parallel to $M e_1$. The result is upper Hessenberg.
2. **Implicit Q theorem.** If $Z^T H Z$ and $W^T H W$ are both unreduced upper Hessenberg and $Z e_1 = W e_1$, then $Z = W D$ with $D = \operatorname{diag}(\pm 1)$. Hence the step equals the explicit double step $M = W R$, $H \leftarrow W^T H W$, up to signs.
3. **Equal to two single steps.** The explicit double step equals two shifted QR steps with $\mu_1$ and then $\mu_2$, done in complex arithmetic when the shifts are complex. So all theory of the shifted QR algorithm applies.
4. **Deflation is backward stable.** Setting $h_{l,l-1}$ to zero in line L8 changes $H$ by at most $u (|h_{l-1,l-1}| + |h_{ll}|)$. With orthogonal transformations elsewhere, the computed $T$ satisfies $T = \hat Q^T (A + E) \hat Q$ for an exactly orthogonal $\hat Q$ near the computed $Q$ and $\|E\|_2 \le c(n)\, u\, \|A\|_2$.
5. **Termination.** Each step is finite, and the iteration cap of line L10 bounds the number of steps per eigenvalue. Local quadratic convergence near a simple eigenvalue or a simple $2 \times 2$ block is proved. Global convergence is not proved: the cyclic permutation matrix is a fixed point of the step with the standard shifts, which is why exceptional shifts exist.

## Complexity

- **One step.** At position $k$, the reflector of order 3 acts on three rows and three columns. In the window of order $p$ this costs about $10p^2$ flops in total; with full rows and columns and $Q$, about $10n^2$ for $H$ and $10n^2$ more for $Q$. These are exact counts of the step.
- **Hessenberg reduction.** $10n^3/3$ flops, and $4n^3/3$ more to form $Q_0$.
- **Whole algorithm.** About $10n^3$ flops for eigenvalues and $25n^3$ for $T$ and $Q$ (GVL Section 7.5). These totals assume about two Francis steps per eigenvalue. That number is observed, not proved: 1.95 in the random example above, and 6 steps for 4 eigenvalues in the companion example.
- **Storage.** $H$ is overwritten by $T$ in place; $Q$ takes $n^2$ more numbers.

## Properties

- **Real arithmetic.** $s = \mu_1 + \mu_2$ and $t = \mu_1 \mu_2$ are real when the shifts are real or conjugate, so $M$ and every reflector are real.
- **Hessenberg form is kept.** Each step maps an upper Hessenberg matrix to one, so every step costs $O(n^2)$ instead of $O(n^3)$.
- **Shift-insensitive start.** A Francis step depends on the shifts only through the first column of $M$, three numbers. This makes it robust to the rounding of $M$, which the explicit form would suffer.
- **Quadratic convergence.** Near convergence, $|h_{n-1,n-2}|$ or $|h_{n,n-1}|$ is roughly squared at each step for simple eigenvalues, as in the example.
- **Backward stability.** The whole algorithm is normwise backward stable, so the error in a simple eigenvalue is about $\kappa(\lambda)\, u\, \|A\|_2$; see the [eigenvalue condition number](/eigenvalue-condition-number/).

## Variants and improvements

- **Small-bulge multishift QR** (Braman, Byers and Mathias 2002): chase many small bulges in a tight pipeline, which uses level 3 BLAS. LAPACK's `xHSEQR` uses it for large matrices, with `xLAHQR` (the classical Francis step) for small ones.
- **Aggressive early deflation** (Braman, Byers and Mathias 2002): look for negligible entries in a spike of the trailing window, not only on the subdiagonal; it often reduces the number of steps by a large factor. See [deflation](/deflation/).
- **Complex single-shift QR** for complex matrices, `xLAHQR` in complex arithmetic, where conjugate pairs need not be kept together.
- **QZ** for the [generalized eigenvalue problem](/generalized-eigenvalue-problem/): the [QZ algorithm](/qz-algorithm/) applies the same implicit double shift to a pair $(A, B)$.
- **Balancing first.** A diagonal similarity before the reduction, [matrix balancing](/matrix-balancing/), often improves accuracy and speed.
- **Symmetric case.** For symmetric tridiagonal matrices, a single real shift suffices and the step is an implicit chase of a $2 \times 2$ bulge.

## When to use it

Use the Francis algorithm, through LAPACK, for all eigenvalues of a dense real nonsymmetric matrix of order up to some thousands, and for its Schur form. It is the core of `eig` in MATLAB and NumPy. For a symmetric matrix use a [symmetric solver](/symmetric-eigenproblem/), which is cheaper and gives orthogonal eigenvectors. For a few eigenvalues of a large sparse matrix use [Arnoldi](/arnoldi-iteration/) with [implicit restarts](/implicitly-restarted-arnoldi/), which uses Francis-type steps on its small Hessenberg matrix.

## Pitfalls

- **Forming $M$ explicitly.** $H^2$ costs $O(n^3)$ and can lose accuracy when $\|H\|^2$ is large. Use only its first column.
- **Shifts with no progress.** For the cyclic permutation matrix the standard shifts are $0, 0$ and the step only changes signs. Without exceptional shifts the iteration never deflates; the implementation's test shows this.
- **Deflation criteria that are too strict or too loose.** Testing against $u \|H\|$ instead of the neighboring diagonal entries can lose relative accuracy for graded matrices. LAPACK uses the neighbor test plus a refinement by Ahues and Tisseur.
- **Reading eigenvalues from the diagonal of a quasi-triangular $T$.** Complex pairs sit in $2 \times 2$ blocks; compute their eigenvalues from the block, or standardize the block first.
- **Expecting accurate eigenvectors for close eigenvalues.** The Schur form is backward stable, but eigenvectors of nearly equal or defective eigenvalues are ill conditioned.

## Implementations

## History

Heinz Rutishauser's LR algorithm of 1955 gave the idea of iterating a factorization. John Francis, working in London, published the QR transformation in 1961 and 1962, with the shifted iteration, the reduction to Hessenberg form and the implicit double shift that keeps real matrices real. Vera Kublanovskaya found the QR iteration independently in 1961. Wilkinson analyzed its convergence and stability, and the method went into the Handbook for Automatic Computation, EISPACK and then LAPACK. Francis left numerical analysis soon after his papers and learned only decades later how widely his algorithm was used. The small-bulge multishift version and aggressive early deflation of Braman, Byers and Mathias (2002) are the main later improvements.

## References
