---
tag: K72EMJ
kind: algorithm
slug: golub-kahan-svd-algorithm
name: Golub-Kahan SVD algorithm
aliases:
- Golub-Reinsch SVD
- Golub-Kahan-Reinsch algorithm
- bidiagonal QR SVD
area: numerical/eigenproblems
level: advanced
summary: Reduce A to upper bidiagonal form with Householder reflectors, then run implicitly shifted QR steps on the bidiagonal matrix until it is diagonal. The standard dense SVD method.
solves: [singular-value-decomposition]
model: floating-point-model
complexity:
  vars: {m: "the number of rows, m ≥ n", n: "the number of columns"}
  time: {worst: O(m n^2), typical: O(m n^2)}
  space: {worst: Θ(m n)}
  flops: {values: "4 m n^2 - 4 n^3 / 3", thin_with_vectors: "14 m n^2 + 8 n^3", per_step_values: "30 n"}
properties: {deterministic: true, in_place: true, recursive: false, iterative: true}
history:
  year: 1965
  people: [Gene H. Golub, William Kahan, Christian Reinsch]
  note: Golub and Kahan proposed bidiagonalization for the SVD in 1965; Golub and Reinsch gave the implicit shifted QR step on the bidiagonal matrix and the Algol program in 1970.
prereqs: [singular-value-decomposition, householder-reflections, givens-rotations]
see_also: [qr-algorithm, wilkinson-shift, dqds-algorithm, symmetric-eigenproblem, francis-double-shift-qr, jacobi-eigenvalue-algorithm, pseudoinverse, least-squares-problem]
sources:
  - paper: doi:10.1137/0702016
    title: G. Golub and W. Kahan, Calculating the singular values and pseudo-inverse of a matrix, SIAM Journal on Numerical Analysis Series B 2, 1965
    locator: pp. 205 to 224 (bidiagonalization by Householder transformations)
  - paper: doi:10.1007/BF02163027
    title: G. H. Golub and C. Reinsch, Singular value decomposition and least squares solutions, Numerische Mathematik 14, 1970
    locator: pp. 403 to 420 (the shifted QR step on the bidiagonal matrix, zero diagonal entries, the Algol procedure)
  - paper: doi:10.1137/0911052
    title: J. Demmel and W. Kahan, Accurate singular values of bidiagonal matrices, SIAM Journal on Scientific and Statistical Computing 11, 1990
    locator: pp. 873 to 912 (zero-shift QR, relative accuracy, convergence criteria)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 8.6, Computing the SVD (bidiagonalization, the Golub-Kahan step, zero diagonal entries, the flop table)
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 31, Computing the SVD (bidiagonalization and its cost, the link to the symmetric eigenproblem)
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Section 5.4, Algorithms for the Singular Value Decomposition (QR iteration and its variants, high relative accuracy)
---

The Golub-Kahan SVD algorithm computes the [singular value decomposition](/singular-value-decomposition/) $A = U \Sigma V^T$ of a dense real $m \times n$ matrix in two phases. First, Householder reflectors applied alternately from the left and the right reduce $A$ to an upper bidiagonal matrix $B = U_B^T A V_B$ in $4mn^2 - 4n^3/3$ flops. Second, implicitly shifted QR steps on $B$, each a chase of one bulge with Givens rotations, drive the superdiagonal to zero. Each step is the symmetric [QR algorithm](/qr-algorithm/) with a [Wilkinson shift](/wilkinson-shift/) applied to $B^T B$, but done without ever forming $B^T B$. The second phase costs $O(n^2)$ flops for the singular values alone and is backward stable. LAPACK's `xGESVD` uses this method, with `xBDSQR` for the bidiagonal phase.

## In plain words

The singular values of a matrix tell how much it stretches space in each of a set of perpendicular directions. Finding them directly is hard, so the algorithm first simplifies the matrix. Reflections from both sides, which do not change the singular values, clear everything except the main diagonal and the line just above it.

The second phase works on this thin matrix. Each pass starts a small disturbance at the top, pushes it down to the bottom with small rotations, and shrinks the entries above the diagonal, the last ones fastest. When an entry above the diagonal becomes negligible, the problem splits into two smaller ones. When none are left, the diagonal holds the singular values.

## The problem

**Notation.** $A \in \mathbb{R}^{m \times n}$ with $m \ge n$; for $m < n$, apply the algorithm to $A^T$. Singular values are ordered $\sigma_1 \ge \sigma_2 \ge \dots \ge \sigma_n \ge 0$. $B$ is upper bidiagonal with diagonal $d_1, \dots, d_n$ and superdiagonal $e_1, \dots, e_{n-1}$, $e_i = b_{i,i+1}$. $B$ is *unreduced* if every $e_i$ is nonzero. $u$ is the unit roundoff.

**Input.** A dense $A$.

**Output.** $\sigma_1, \dots, \sigma_n$ and, if wanted, $U \in \mathbb{R}^{m \times n}$ with orthonormal columns and an orthogonal $V \in \mathbb{R}^{n \times n}$ with $A = U \operatorname{diag}(\sigma) V^T$.

## The algorithm

```pseudo id=main
GOLUB-KAHAN-SVD(A)
L1  B ← U_Bᵀ A V_B, upper bidiagonal, by Householder reflectors from the left and right; U ← U_B, V ← V_B
L2  repeat: set e_i ← 0 for every i with |e_i| ≤ u (|d_i| + |d_i+1|)
L3      find the last unreduced block B[p..q] with q > p; if there is none, go to L11
L4      if some d_k = 0 in the block then zero row k (or column q) by Givens rotations, and go to L2
L5      μ ← eigenvalue of the trailing 2 × 2 block of B[p..q]ᵀ B[p..q] closer to d_q² + e_q−1²
        ▷ the Golub-Kahan step, lines L6 to L10
L6      y ← d_p² − μ;  z ← d_p e_p
L7      for k ← p to q − 1 do
L8          G ← rotation on columns k, k+1 with (y, z) G = (r, 0);  B ← B G;  V ← V G
L9          y ← b_kk;  z ← b_k+1,k;  G ← rotation on rows k, k+1 that zeros z;  B ← Gᵀ B;  U ← U G
L10         if k < q − 1 then y ← b_k,k+1;  z ← b_k,k+2
L11 make every d_i ≥ 0 by negating the matching column of V, sort, and return U, (d_i), V
```

Line L1 alternates two reflectors. The one from the left zeros column $k$ below the diagonal; the one from the right zeros row $k$ to the right of the superdiagonal. The right reflectors never touch column 1, so $V e_1 = e_1$. Line L6 is the first column of $B^T B - \mu I$, restricted to its two nonzero entries. The rotation of line L8 at $k = p$ creates a bulge at position $(p + 1, p)$. Line L9 moves it to $(k, k + 2)$, and the next L8 moves it to $(k + 2, k + 1)$, until it leaves the block at the bottom. Line L4 handles a zero diagonal entry: then $B$ is singular, the shifted step may make no progress, and a sweep of rotations from the left moves the superdiagonal entry of row $k$ to the right until it disappears, after which $e_k = 0$ and the block splits.

## Example

Take
$$A = \begin{pmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 10 \\ 1 & 0 & 1 \end{pmatrix}.$$
Bidiagonalization gives, rounded to five digits,
$$B = \begin{pmatrix} -8.18535 & 15.30194 & 0 \\ 0 & -2.08303 & -0.09756 \\ 0 & 0 & 0.70867 \end{pmatrix}.$$
The superdiagonal before each Golub-Kahan step was:

| step | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| $\lvert e_1 \rvert$ | 15.30 | $4.917 \times 10^{-2}$ | $7.792 \times 10^{-5}$ | $1.235 \times 10^{-7}$ |
| $\lvert e_2 \rvert$ | $9.756 \times 10^{-2}$ | $4.189 \times 10^{-3}$ | $1.542 \times 10^{-9}$ | 0 |

The shift aims at the last singular value, so $e_2$ converges fast: from $4.2 \times 10^{-3}$ to $1.5 \times 10^{-9}$ in one step, faster than quadratic. After step 3, $e_2$ is negligible and is set to zero. Step 4 runs on the remaining $2 \times 2$ block, where the shift is an exact singular value squared, and $e_1$ vanishes. While the shift was aimed at $e_2$, $e_1$ decreased only linearly. Four steps produced
$$\sigma_1 = 17.450895584636637, \quad \sigma_2 = 0.9869391657365866, \quad \sigma_3 = 0.7015656613921291.$$
Two exact checks with fractions: $\sigma_1^2 + \sigma_2^2 + \sigma_3^2 = \operatorname{tr}(A^T A) = 306$, and $\sigma_1^2 \sigma_2^2 \sigma_3^2 = \det(A^T A)$, both to rounding.

For random Gaussian matrices (seed 3) of sizes $40 \times 30$, $30 \times 40$ and $50 \times 50$, the implementation used 57, 60 and 92 steps, about 1.9 per singular value. Residuals were below $1.2 \times 10^{-14}$, and the orthogonality errors of $U$ and $V$ were below $4.5 \times 10^{-15}$.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md).

1. **Bidiagonalization.** Line L1 produces $B = U_B^T A V_B$ with $U_B$, $V_B$ orthogonal, so $A$ and $B$ have the same singular values.
2. **The step is implicit QR on $B^T B$.** Let $Z$ be the product of the right rotations in lines L8. Then $Z e_1$ is parallel to $(B^T B - \mu I) e_1$, and the new bidiagonal is $\bar B = W^T B Z$ with $\bar B^T \bar B = Z^T (B^T B) Z$ tridiagonal. By the implicit Q theorem, $\bar B^T \bar B$ is the result of one shifted QR step on the tridiagonal $B^T B$, up to signs.
3. **Splitting.** If $e_i = 0$, $B$ is the direct sum of two bidiagonal blocks, and its singular values are the union of theirs. If $d_k = 0$, the rotations of line L4 produce a zero row or column without changing the singular values.
4. **Result.** When every $e_i = 0$, $B = \operatorname{diag}(d_i)$, and the sign changes and sorting of line L11 give a valid SVD.
5. **Termination.** Each step and each sweep of line L4 is finite. The implementation stops after $40n$ steps. Local cubic convergence of the shifted step, in the generic case, follows from the symmetric QR algorithm with the Wilkinson shift. Global convergence of the Wilkinson-shifted symmetric tridiagonal QR algorithm is proved (Wilkinson 1968), and it carries over to $B^T B$.
6. **Stability.** The computed factors satisfy $A + E = \hat U \hat \Sigma \hat V^T$ with $\hat U$, $\hat V$ exactly orthogonal near the computed ones and $\|E\|_2 \le c(m, n)\, u\, \|A\|_2$. By [Weyl's inequality](/weyls-inequality/) for singular values, $|\hat \sigma_i - \sigma_i| \le c(m, n)\, u\, \sigma_1$.

## Complexity

- **Bidiagonalization.** $4mn^2 - 4n^3/3$ flops for $B$ alone. This is an exact leading-term count, proved by summing the reflector costs.
- **Bidiagonal QR, values only.** A step on a block of order $p$ applies $2(p - 1)$ rotations to $B$, about $30p$ flops, so the second phase costs $O(n^2)$ flops in practice. That rests on about two steps per singular value, which is observed, not proved: 1.9 in the random tests above.
- **With vectors.** Each step adds $6m$ flops per rotation for $U$ and $6n$ for $V$, so the iteration costs about $6mn^2 + 6n^3$ more with two steps per value. The totals are about $14mn^2 + 8n^3$ for $\Sigma$, the thin $U$ and $V$, and $4m^2n + 8mn^2 + 9n^3$ with the full $U$ (GVL Section 8.6). These totals are typical, not worst-case bounds.
- **R-bidiagonalization.** For $m \ge 5n/3$ it is cheaper to compute $A = QR$ first and bidiagonalize $R$: $2mn^2 + 2n^3$ flops instead of $4mn^2 - 4n^3/3$.
- **Storage.** $B$ overwrites $A$; $U$ and $V$ need $mn + n^2$ numbers.

## Properties

- **No cross product.** The algorithm never forms $A^T A$, whose eigenvalues $\sigma_i^2$ lose all accuracy below $\sqrt{u}\, \sigma_1$. Small singular values are as accurate as backward stability allows.
- **Backward stable** in the normwise sense; the absolute error in every singular value is about $u\, \sigma_1$.
- **Quadratic or cubic convergence.** Near convergence, $e_{q-1}$ is roughly cubed per step in the generic case, as for the symmetric QR algorithm with a Wilkinson shift.
- **Deterministic and in place**, with all work in real arithmetic.

## Variants and improvements

- **Zero-shift QR and relative accuracy** (Demmel and Kahan 1990). A step with $\mu = 0$ can be done without any subtraction, so it computes all singular values of a bidiagonal matrix to high relative accuracy, even tiny ones. LAPACK's `xBDSQR` switches to it when the shift would spoil small singular values.
- **dqds** (Fernando and Parlett 1994). For singular values only, the [dqds algorithm](/dqds-algorithm/) is faster and also relatively accurate; LAPACK's `xBDSQR` calls it when no vectors are wanted.
- **Divide and conquer** for the bidiagonal SVD with vectors, LAPACK's `xBDSDC` and `xGESDD`, uses the [secular equation](/secular-equation/), like the [divide-and-conquer eigensolver](/divide-and-conquer-eigensolver/). It is usually much faster than QR when vectors are needed.
- **One-sided Jacobi** (Hestenes, Demmel and Veselić) gives high relative accuracy for some classes of matrices; see the [Jacobi eigenvalue algorithm](/jacobi-eigenvalue-algorithm/).
- **Blocked bidiagonalization** (`xGEBRD`) does half of the bidiagonalization flops in matrix-matrix products.
- **Lanczos (Golub-Kahan) bidiagonalization** for large sparse matrices builds $B$ one column at a time from products with $A$ and $A^T$, a Krylov method.

## When to use it

Use it, through LAPACK `xGESVD`, when you need the full SVD of a dense matrix, or singular values for rank decisions, [least squares](/least-squares-problem/), [pseudoinverses](/pseudoinverse/) and principal component analysis. When vectors are needed for large $n$, `xGESDD` (divide and conquer) is usually faster. For a few singular triplets of a large sparse matrix, use Lanczos bidiagonalization or randomized methods.

## Pitfalls

- **Forming $A^T A$** and calling a symmetric eigensolver squares the condition number and loses small singular values. The bidiagonal phase avoids this.
- **Ignoring zero diagonal entries.** If $d_k = 0$ the shifted step can stall and a deflation test on $e$ never fires. Line L4 is required, and the test must be scaled sensibly (here $|d_k| \le u \|B\|$).
- **Deflation tests and relative accuracy.** The test $|e_i| \le u (|d_i| + |d_{i+1}|)$ is fine for backward stability, but graded bidiagonals need the Demmel-Kahan tests to keep relative accuracy.
- **Sign and order.** The iteration may leave negative $d_i$ in any order; fix the signs through $V$ and sort the triplets, as in line L11.
- **Full $U$ when the thin one suffices.** For $m \gg n$, the full $m \times m$ matrix $U$ costs $4m^2n$ flops and $m^2$ storage.

## Implementations

## History

Gene Golub and William Kahan showed in 1965 how to reduce a matrix to bidiagonal form with Householder transformations, which made the SVD computable without forming $A^T A$. Golub and Christian Reinsch published the shifted QR iteration on the bidiagonal matrix in 1970, with an Algol procedure in the Handbook for Automatic Computation that became the basis of EISPACK and LINPACK SVD codes. Tony Chan's R-bidiagonalization (1982), the zero-shift QR of James Demmel and Kahan (1990), Fernando and Parlett's dqds (1994) and Gu and Eisenstat's divide and conquer (1995) shaped the LAPACK SVD routines.

## References
