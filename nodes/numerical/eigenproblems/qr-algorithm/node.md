---
tag: 9ACH0R
kind: algorithm
slug: qr-algorithm
name: QR algorithm
aliases:
- QR iteration
- Francis QR
- shifted QR algorithm
- Hessenberg QR algorithm
area: numerical/eigenproblems
level: core
summary: Factor A − μI = QR and form RQ + μI, again and again, on a Hessenberg matrix. With good shifts and deflation it reaches the Schur form, and so all eigenvalues, in O(n^3) flops.
solves: [eigenvalue-problem]
model: floating-point-model
complexity:
  vars: {n: "the order of A", c: "the cap maxit on QR steps per deflation"}
  time: {typical: Θ(n^3), worst: O(c n^3)}
  space: {extra: Θ(n^2)}
  flops: {eigenvalues: "10 n^3", schur: "25 n^3", hessenberg: "10 n^3 / 3"}
properties: {deterministic: true, in_place: true, recursive: false, iterative: true}
history:
  year: 1961
  people: [John G. F. Francis, Vera N. Kublanovskaya]
  note: Francis and Kublanovskaya found the QR algorithm independently in 1961; Francis also gave the Hessenberg form, shifts and the implicit double shift.
prereqs: [hessenberg-reduction, qr-decomposition, schur-decomposition, power-iteration]
see_also: [francis-double-shift-qr, wilkinson-shift, deflation, matrix-balancing, givens-rotations, subspace-iteration, rayleigh-quotient-iteration, qz-algorithm]
sources:
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 7.3 (orthogonal iteration and the unshifted QR iteration), Section 7.4 (the Hessenberg QR step), Section 7.5 (shifts, the derivation of quadratic convergence, the Francis step, the practical algorithm and its flop counts), Section 8.3 (the symmetric QR algorithm)
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 28, QR Algorithm without Shifts, and Lecture 29, QR Algorithm with Shifts (the connection with simultaneous and Rayleigh quotient iteration, the Wilkinson shift)
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Section 4.4.4 to 4.4.8 (QR iteration, making it practical, Hessenberg reduction, the implicit Q theorem, the double shift) and Section 5.3.1 (tridiagonal QR iteration)
  - book: isbn:9780898714029
    title: Beresford N. Parlett, The Symmetric Eigenvalue Problem, SIAM Classics in Applied Mathematics 20, 1998
    locator: Chapter 8, The QL and QR Algorithms (shifts, global convergence with the Wilkinson shift)
  - book: "J. H. Wilkinson, The Algebraic Eigenvalue Problem, Oxford University Press, 1965"
    title: J. H. Wilkinson, The Algebraic Eigenvalue Problem
    locator: Chapter 8, The LR and QR Algorithms (convergence and the backward error analysis)
  - paper: "J. G. F. Francis, The QR transformation: a unitary analogue to the LR transformation, parts 1 and 2, The Computer Journal 4, 1961 and 1962"
    title: "The QR transformation: a unitary analogue to the LR transformation"
    locator: Comput. J. 4(3) (1961), pp. 265 to 271, and 4(4) (1962), pp. 332 to 345
  - paper: "V. N. Kublanovskaya, On some algorithms for the solution of the complete eigenvalue problem, USSR Computational Mathematics and Mathematical Physics 1, 1963"
    title: On some algorithms for the solution of the complete eigenvalue problem
    locator: USSR Comput. Math. Math. Phys. 1(3) (1963), pp. 637 to 657 (Russian original 1961)
---

The QR algorithm computes all [eigenvalues](/eigenvalue/) of a dense square matrix $A$, and a [Schur decomposition](/schur-decomposition/) $A = Q T Q^*$ if asked. It first reduces $A$ to upper [Hessenberg form](/hessenberg-reduction/) $H$. Then it repeats one step: factor $H - \mu I = Q_k R_k$ by a [QR decomposition](/qr-decomposition/) and replace $H$ by $R_k Q_k + \mu I = Q_k^* H Q_k$. Every step is a unitary similarity, so the eigenvalues never change, and with a good shift $\mu$ the last subdiagonal entry goes to zero quadratically, or cubically for a symmetric matrix. When an entry is negligible the problem splits and the algorithm continues on the smaller part. About two to four steps per eigenvalue are typical, so the whole computation costs $O(n^3)$ flops, and it is backward stable. It is the method behind `eig` in MATLAB and LAPACK's `xHSEQR`, although its global convergence for nonsymmetric matrices has never been proved.

## In plain words

Split the matrix into a rotation part and a triangle, then multiply them back in the opposite order. The result has the same hidden stretch factors as before, but it is a little closer to a triangle, and the stretch factors of a triangle can be read off its diagonal. Done naively this is slow. Two tricks make it fast: first squeeze the matrix into a shape with zeros below the first subdiagonal, which makes each step cheap and keeps that shape; then subtract a good guess of a stretch factor before each split and add it back after, which makes the bottom corner settle in a few steps. Once the corner has settled, cut it off and continue with the rest.

## The problem

**Notation.** $A \in \mathbb C^{n \times n}$ with eigenvalues $\lambda_1, \dots, \lambda_n$, ordered by modulus $|\lambda_1| \ge \dots \ge |\lambda_n|$ when that matters. $H$ is upper Hessenberg ($h_{ij} = 0$ for $i > j + 1$), and unreduced if every $h_{i+1,i} \ne 0$. The Schur form is $A = Q T Q^*$ with $Q$ unitary and $T$ upper triangular. $u$ is the unit roundoff and $\|\cdot\|_F$ the Frobenius norm. A flop is one real operation.

Given $A$, return $T$ upper triangular and $Q$ unitary with $Q T Q^* = A + E$ and $\|E\|_F$ a small multiple of $u \|A\|_F$, together with the flag CONVERGED; or FAILED if some eigenvalue does not converge within $\mathrm{maxit}$ steps. The eigenvalues are the diagonal entries of $T$. This is the dense case of the [nonsymmetric eigenproblem](/nonsymmetric-eigenproblem/).

## The algorithm

```pseudo id=main
QR-ALGORITHM(A, maxit)
L1  (H, Q) ← HESSENBERG(A)                         ▷ A = Q H Q*, 10n³/3 flops
L2  hi ← n; its ← 0
L3  while hi > 1 do
L4      lo ← the largest l ≤ hi with |h_{l,l−1}| ≤ u (|h_{l−1,l−1}| + |h_{l,l}|), or 1; set that h_{l,l−1} ← 0
L5      if lo = hi then hi ← hi − 1; its ← 0; continue    ▷ h_{hi,hi} has converged
L6      its ← its + 1; if its > maxit then return (H, Q, FAILED)
L7      μ ← eigenvalue of H[hi−1..hi, hi−1..hi] nearer h_{hi,hi}   ▷ exceptional shift when its is a multiple of 10
L8      H[lo..hi, lo..hi] − μI = G R with Givens rotations G = G_lo ⋯ G_{hi−1}; apply Gᵢ* to rows i, i+1 of H
L9      apply each Gᵢ to columns i, i+1 of H (rows 1..i+2) and of Q; add μ back to the diagonal
L10 return (T = H, Q, CONVERGED)
```

Line L1 is [Hessenberg reduction](/hessenberg-reduction/) by Householder reflectors. Lines L3 to L9 work on the active window $H[lo..hi, lo..hi]$, an unreduced Hessenberg block; everything below row $hi$ has converged, and the entry $h_{lo, lo-1}$ is zero. Line L4 is the [deflation](/deflation/) test. Setting a tiny subdiagonal entry to zero is a perturbation of size at most $u (|h_{l-1,l-1}| + |h_{l,l}|)$, which is at the level of the rounding errors already made. Line L7 chooses the [Wilkinson shift](/wilkinson-shift/); the implementation also offers the Rayleigh shift $\mu = h_{hi,hi}$ and no shift. If ten steps pass without a deflation, an exceptional shift $\mu = h_{hi,hi} + 1.5 |h_{hi,hi-1}|$ breaks cycles like the one in Pitfalls. Lines L8 and L9 are one explicit shifted QR step, $H \leftarrow G^* H G$, written with $hi - lo$ Givens rotations: the left rotations turn the window of $H - \mu I$ into the triangle $R$, the right rotations form $R G$, which is again Hessenberg, and the shift is added back. The rotations are applied to the whole of rows $lo..hi$ and columns $lo..hi$, not only to the window, so that at the end $H$ is the triangular factor of a Schur form of the whole matrix. Production codes use the [implicit Francis double shift](/francis-double-shift-qr/) instead, which keeps a real matrix real.

## Example

Let $A = \begin{pmatrix} 1 & 2 & 3 \\ 1 & 4 & 5 \\ 0 & 1 & 6 \end{pmatrix}$, already upper Hessenberg, with the characteristic polynomial $t^3 - 11 t^2 + 27 t - 10$ (computed exactly) and the eigenvalues $0.4492308744$, $2.9154240704$ and $7.6353450551$. The table gives $|h_{32}|$ after each QR step for three choices of shift.

| step | no shift | Rayleigh shift $h_{33}$ | Wilkinson shift |
|---|---|---|---|
| 1 | 2.36e+00 | 1.59e+00 | 8.51e-02 |
| 2 | 5.72e-01 | 1.70e-01 | 6.79e-05 |
| 3 | 6.75e-02 | 5.06e-03 | 2.78e-11 |
| 4 | 9.22e-03 | 5.39e-06 | 2.79e-24 (deflated) |
| 5 | 1.36e-03 | 6.21e-12 | |
| 6 | 2.05e-04 | 8.30e-24 (deflated) | |

Without a shift the entry shrinks by about $|\lambda_3 / \lambda_2| = 0.154$ per step, the rate of [power iteration](/power-iteration/) on subspaces; this run needs 39 steps in all. With a shift the number of correct digits roughly doubles at each step. The Wilkinson shift starts closer, and with it the whole computation takes 5 steps: 4 for $\lambda = 0.449$, then 1 for the remaining $2 \times 2$ block. The diagonal of the final $T$ is $(0.4492, 2.9154, 7.6353)$, and $\|Q T Q^* - A\|_F$ is a few units of $u \|A\|_F$; the test file checks both.

## Correctness

**Invariants.** At line L3, $Q$ is unitary, $H$ is upper Hessenberg, and $Q H Q^* = A + E$, where $E$ collects the entries set to zero by line L4. Each step multiplies $H$ by a unitary $G$ on both sides, so it keeps the eigenvalues. The product $R G$ of an upper triangular matrix and a product of rotations in planes $(i, i+1)$ is Hessenberg again, so each step costs $O(n \cdot (hi - lo))$ and not $O(n^3)$. When line L10 returns, every subdiagonal entry is zero, so $T = H$ is upper triangular and $Q T Q^* = A + E$ is a Schur decomposition of a nearby matrix.

**Why it converges.** Without shifts, $A^k = (Q_1 \cdots Q_k)(R_k \cdots R_1)$, so the QR algorithm is [subspace iteration](/subspace-iteration/) on all leading subspaces at once: if $|\lambda_1| > \dots > |\lambda_n|$, then $h_{i+1, i} = O(|\lambda_{i+1}/\lambda_i|^k)$. With a shift, $(A - \mu I)^{-*} e_n$ is parallel to the last column of $Q_k$, so each step is also one step of inverse iteration on $A^*$, and the Rayleigh shift turns it into [Rayleigh quotient iteration](/rayleigh-quotient-iteration/). For the $2 \times 2$ case $H = \begin{pmatrix} a & b \\ \epsilon & d \end{pmatrix}$ with $\mu = d$, one step gives exactly $|h'_{21}| = |\epsilon|^2 |b| / (|a - d|^2 + |\epsilon|^2)$: quadratic convergence when $a \ne d$, and cubic when $|b| = |\epsilon|$, as for a Hermitian matrix with $b = \bar\epsilon$. The proof file gives these statements in full.

**Termination.** The loop always ends: each pass through line L3 either lowers $hi$ (line L5) or raises $its$, which line L6 caps. Convergence within the cap is not guaranteed. For the symmetric tridiagonal QR algorithm with the Wilkinson shift, Wilkinson (1968) proved global convergence; for nonsymmetric matrices no such theorem exists.

## Complexity

- **Reduction.** Line L1 costs $10n^3/3$ flops for $H$, $14n^3/3$ with $Q$ (exact leading terms).
- **One step.** With $m = hi - lo + 1$, a step uses $m - 1$ rotations, each applied to about $n$ entries in two rows and $n$ in two columns, and to two columns of $Q$. In real arithmetic that is about $6 n m$ flops for $H$ and $6 n m$ for $Q$ (a rotation costs 6 flops per pair of entries); complex arithmetic costs about four times as much. If only eigenvalues are wanted, rotations can be restricted to the window, and a step costs $O(m^2)$.
- **Total (typical, not proved).** The number of steps per eigenvalue is observed, not proved. In the test file, 30 random real matrices of order 4 to 12 need 3.1 complex single-shift steps per eigenvalue on average. With the Francis double shift GVL Section 7.5 estimates about $10n^3$ flops for the eigenvalues only and $25n^3$ for $Q$ and $T$, counting two steps per eigenvalue.
- **Worst case of the implementation.** At most $\mathrm{maxit}$ steps per deflation and at most $n - 1$ deflations, so $O(\mathrm{maxit} \cdot n^3)$ flops. Memory is $\Theta(n^2)$ for $H$ and $Q$.

## Properties

- **Backward stable.** The computed $\hat T$ and $\hat Q$ satisfy $\hat T = Q^*(A + E) Q$ for an exactly unitary $Q$ with $\|\hat Q - Q\|_2 = O(u)$ and $\|E\|_2 = O(u) \|A\|_2$, with constants that grow modestly with $n$ (GVL Section 7.5; Wilkinson 1965, Chapter 8). Each eigenvalue then has the error $\kappa(\lambda) \cdot O(u \|A\|)$, where $\kappa(\lambda)$ is its [condition number](/eigenvalue-condition-number/).
- **Order of eigenvalues.** Without shifts the diagonal of $T$ is ordered by decreasing modulus. With shifts the order depends on which eigenvalues the shifts find first, and it can be changed afterwards by reordering the Schur form.
- **Rates.** Linear at the ratio $|\lambda_{i+1}/\lambda_i|$ without shifts; locally quadratic with the Rayleigh or Wilkinson shift for a simple eigenvalue; locally cubic for Hermitian matrices. The test file observes median orders of 2.0 and 2.8 for the two cases.
- **In place.** $H$ overwrites $A$, and the rotations need $O(1)$ extra storage each.

## Variants and improvements

- **[Francis double shift](/francis-double-shift-qr/).** Two steps with the conjugate shifts $\mu, \bar\mu$ combined into one real step by the implicit Q theorem: compute only the first column of $(H - \mu I)(H - \bar\mu I)$, introduce a bulge with a reflector and chase it down. This keeps a real matrix real and is what LAPACK's `xLAHQR` does.
- **Multishift QR and aggressive early deflation.** Chase many small bulges at once with blocked, cache-friendly updates, and look for converged eigenvalues in a whole trailing window by computing its Schur form; this is LAPACK's `xHSEQR` for large $n$ (Braman, Byers and Mathias 2002).
- **Symmetric tridiagonal QR.** For a [tridiagonal](/tridiagonal-eigenproblem/) $T$, a step costs $O(m)$ flops, the Wilkinson shift gives proven global convergence, and all eigenvalues cost $O(n^2)$ flops; vectors cost about $6n^3$ more.
- **QZ.** The [QZ algorithm](/qz-algorithm/) applies the same idea to the pencil $A - \lambda B$ without inverting $B$.
- **[Balancing](/matrix-balancing/).** A diagonal similarity before line L1 reduces $\|A\|$ and so the absolute error bound, for badly scaled matrices.
- **The LR algorithm.** Rutishauser's earlier iteration uses $A = L R$ (LU) and $R L$; it is cheaper per step but not stable, which is why the unitary version replaced it.

## When to use it

Use it for all eigenvalues of a dense matrix that fits in memory, with or without the Schur vectors; through LAPACK it is the default in every numerical library. For a symmetric matrix, reduce to tridiagonal form and use QR, the [divide-and-conquer eigensolver](/divide-and-conquer-eigensolver/) or [MRRR](/mrrr-algorithm/), which are faster when vectors are needed. For a few eigenvalues of a large sparse matrix, use [Arnoldi](/arnoldi-iteration/) or [Lanczos](/lanczos-algorithm/) instead; they use QR internally on their small projected matrix. For the pencil $A - \lambda B$ use QZ.

## Pitfalls

- **Skipping the Hessenberg reduction.** A QR step on a full matrix costs $O(n^3)$ flops, and the total becomes $O(n^4)$. Reduce first; the Hessenberg form is kept by every step.
- **Stalling with the Rayleigh shift.** For $\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$ the Rayleigh shift is $0$, and $Q = H$, $R = I$, so the step returns $H$ unchanged. The Wilkinson shift is $\pm 1$, an exact eigenvalue, and deflates in one step. The cyclic permutation matrix of order $n \ge 3$ stalls even with the Wilkinson shift, because its trailing $2 \times 2$ block $\begin{pmatrix} 0 & 0 \\ 1 & 0 \end{pmatrix}$ gives $\mu = 0$; only the exceptional shift moves it. A code without exceptional shifts and an iteration cap can loop forever.
- **A relative deflation test without a fallback.** The test $|h_{l,l-1}| \le u(|h_{l-1,l-1}| + |h_{l,l}|)$ never passes if both diagonal entries are zero and $h_{l,l-1}$ is tiny but nonzero. The implementation falls back to $u \|H\|_F$ in that case.
- **Applying the rotations only to the window.** That is right when only eigenvalues are wanted, but then $H$ above and to the right of the window is not updated, and $Q$ and $T$ are no longer a Schur form of $A$.
- **Expecting real output from complex arithmetic.** Complex single-shift QR on a real matrix with real eigenvalues returns them with imaginary parts of order $u \|A\|$, and complex conjugate pairs come out only approximately conjugate. Use the double-shift real form when the output must be real.
- **Too small a step cap.** A matrix with a large cluster of eigenvalues, such as a perturbed Jordan block, can need dozens of steps for the first deflation. The implementation allows 100 per deflation; LAPACK allows 30 times the order of the active block in total.

## Implementations

## History

Heinz Rutishauser introduced the LR algorithm in 1958, based on his quotient-difference algorithm. In 1961 John Francis in England and Vera Kublanovskaya in the Soviet Union independently replaced the LU factorization by the QR factorization, which made the iteration stable. Francis's two papers already contain the reduction to Hessenberg form, shifts, deflation and the implicit double-shift step, and the algorithm became the standard dense eigenvalue method through the EISPACK library of the early 1970s and then LAPACK. Wilkinson proved global convergence of the symmetric tridiagonal version with his shift in 1968. In 2000 the QR algorithm was named one of the ten algorithms of the twentieth century with the greatest influence on science and engineering.

## References
