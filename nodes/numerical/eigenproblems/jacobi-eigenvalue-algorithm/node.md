---
tag: HTTEGG
kind: algorithm
slug: jacobi-eigenvalue-algorithm
name: Jacobi eigenvalue algorithm
aliases:
- Jacobi rotation method
- Jacobi method for eigenvalues
- cyclic Jacobi method
area: numerical/eigenproblems
level: core
summary: Plane rotations J^T A J that each zero one off-diagonal entry of a symmetric matrix. Repeated sweeps drive A to diagonal form, quadratically in the end, with high relative accuracy.
solves: [symmetric-eigenproblem]
model: floating-point-model
complexity:
  vars: {n: "the order of A", s: "the number of sweeps"}
  time: {worst: O(s n^3)}
  space: {extra: Θ(n^2)}
  flops: {worst: "3 s n^3", with_vectors: "6 s n^3"}
properties: {deterministic: true, in_place: true, recursive: false, iterative: true}
history:
  year: 1846
  people: [Carl Gustav Jacob Jacobi, Heinz Rutishauser, Peter Henrici, James Demmel, Krešimir Veselić]
  note: Jacobi diagonalized symmetric systems by rotations in 1846; the method was revived for computers around 1950 and analysed by Henrici, Forsythe and Wilkinson.
prereqs: [givens-rotations, symmetric-eigenproblem, spectral-theorem]
see_also: [qr-algorithm, tridiagonalization, weyls-inequality, gershgorin-circle-theorem, singular-value-decomposition, positive-definite-matrix, divide-and-conquer-eigensolver, mrrr-algorithm]
sources:
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 8.5, Jacobi Methods (the symmetric Schur decomposition of a 2 by 2 block, classical and cyclic Jacobi, error analysis, one-sided and parallel Jacobi)
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Section 5.3.5, Jacobi's Method, and Section 5.4.3 on high relative accuracy
  - book: isbn:9780898714029
    title: Beresford N. Parlett, The Symmetric Eigenvalue Problem, SIAM Classics in Applied Mathematics 20, 1998
    locator: Chapter 9, Jacobi Methods
  - paper: doi:10.1515/crll.1846.30.51
    title: C. G. J. Jacobi, Über ein leichtes Verfahren die in der Theorie der Säcularstörungen vorkommenden Gleichungen numerisch aufzulösen, Journal für die reine und angewandte Mathematik 30, 1846
    locator: pp. 51 to 94
  - paper: doi:10.1137/0613074
    title: James Demmel and Krešimir Veselić, Jacobi's method is more accurate than QR, SIAM Journal on Matrix Analysis and Applications 13(4), 1992
    locator: Sections 2 to 4 (relative accuracy for scaled positive definite matrices)
  - paper: "G. E. Forsythe and P. Henrici, The cyclic Jacobi method for computing the principal values of a complex matrix, Transactions of the American Mathematical Society 94, 1960, pp. 1 to 23"
    title: G. E. Forsythe and P. Henrici, The cyclic Jacobi method for computing the principal values of a complex matrix
    locator: the convergence proof for the cyclic order with restricted angles
  - paper: "P. Henrici, On the speed of convergence of cyclic and quasicyclic Jacobi methods for computing eigenvalues of Hermitian matrices, Journal of the Society for Industrial and Applied Mathematics 6, 1958, pp. 144 to 162"
    title: P. Henrici, On the speed of convergence of cyclic and quasicyclic Jacobi methods
    locator: the quadratic convergence theorem for distinct eigenvalues
---

The Jacobi eigenvalue algorithm computes all eigenvalues and eigenvectors of a real symmetric matrix $A$ by a sequence of plane rotations $A \leftarrow J^T A J$, each chosen to make one off-diagonal pair $a_{pq} = a_{qp}$ zero. A later rotation can make a zeroed entry nonzero again, but the squared off-diagonal norm $\operatorname{off}(A)^2$ drops by exactly $2 a_{pq}^2$ at each step, and the cyclic method converges quadratically in the end. It is several times slower than the tridiagonal [QR algorithm](/qr-algorithm/), but it is simple, highly parallel, and it computes small eigenvalues of graded positive definite matrices with high relative accuracy, which the QR algorithm does not.

## In plain words

A symmetric matrix can be turned by rotations into a diagonal one, and then its diagonal holds the eigenvalues. The method does not find the full rotation at once. It looks at one pair of rows and columns at a time and turns them by the angle that clears the pair's off-diagonal entry. This undoes some earlier work, but the total size of everything off the diagonal always shrinks.

The method goes through all pairs in a fixed order, again and again. Each round is called a sweep. After a few sweeps the off-diagonal part is tiny, and from then on each sweep roughly squares it. The product of all rotations holds the eigenvectors.

## The problem

**Notation.** $A = A^T \in \mathbb{R}^{n \times n}$ with eigenvalues $\lambda_1 \ge \dots \ge \lambda_n$; $\operatorname{off}(A) = (\sum_{i \ne j} a_{ij}^2)^{1/2}$; $J = J(p, q, \theta)$ is the rotation in the $(p, q)$ plane with $J_{pp} = J_{qq} = c$, $J_{pq} = s$, $J_{qp} = -s$; $u$ is the unit roundoff.

Given $A$, compute an orthogonal $V$ and a diagonal $\Lambda$ with $A V = V \Lambda$ up to rounding errors. This is the [symmetric eigenproblem](/symmetric-eigenproblem/); the [spectral theorem](/spectral-theorem/) says that the answer exists.

## The algorithm

```pseudo id=main
JACOBI(A, tol)                                   ▷ A symmetric, overwritten
L1  V ← I
L2  for sweep ← 1, 2, … do
L3      for p ← 1 to n − 1 do for q ← p + 1 to n do
L4          if |a_pq| ≤ tol · sqrt(|a_pp a_qq|) then skip this pair
L5          τ ← (a_qq − a_pp) / (2 a_pq);  t ← sign(τ) / (|τ| + sqrt(1 + τ²));  c ← 1 / sqrt(1 + t²);  s ← t c
L6          A ← Jᵀ A J;  V ← V J            ▷ only rows and columns p, q change; a_pq ← 0
L7      if no pair was rotated in this sweep then exit the loop
L8  return the diagonal of A and V
```

Line L5 takes the root $t = \tan\theta$ of smaller modulus of $t^2 + 2\tau t - 1 = 0$, so $|\theta| \le \pi/4$. The small angle is needed for the convergence proof and keeps the diagonal entries from swapping. Line L6 needs only these formulas, with $r \ne p, q$:
$$a_{pp} \leftarrow a_{pp} - t a_{pq}, \quad a_{qq} \leftarrow a_{qq} + t a_{pq}, \quad a_{pq} \leftarrow 0, \quad a_{rp} \leftarrow c\, a_{rp} - s\, a_{rq}, \quad a_{rq} \leftarrow s\, a_{rp} + c\, a_{rq}.$$
The threshold of line L4 is relative to the diagonal, as in Demmel and Veselić (1992); it gives the high relative accuracy described below. The classical method of Jacobi instead rotates on the entry of largest modulus, at a search cost of $O(n^2)$ per rotation.

## Example

Take
$$A = \begin{pmatrix} 4 & -2 & 2 \\ -2 & 3 & 1 \\ 2 & 1 & 5 \end{pmatrix}, \qquad \operatorname{off}(A) = \sqrt{18} \approx 4.242641.$$
The first rotation, for $(p, q) = (1, 2)$, has $\tau = 0.25$, $t = 0.780776$, $c = 0.788205$ and $s = 0.615412$. It gives
$$\begin{pmatrix} 5.561553 & 0 & 0.960999 \\ 0 & 1.438447 & 2.019030 \\ 0.960999 & 2.019030 & 5 \end{pmatrix}.$$
The values of $\operatorname{off}(A)$ after sweeps 1 to 4 are $1.712672$, $0.038096$, $1.06 \times 10^{-9}$ and $1.7 \times 10^{-41}$; sweep 5 rotates nothing. The convergence is quadratic or faster. Ten rotations give the diagonal $(6.640023, 0.495336, 4.864641)$, whose sum is $12 = \operatorname{tr} A$ and whose product is $16 = \det A$. The exact characteristic polynomial changes sign within a relative distance of $10^{-13}$ of each computed value.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md).

1. **One rotation.** The choice of line L5 makes $b_{pq} = 0$ in $B = J^T A J$, and gives $b_{pp} = a_{pp} - t a_{pq}$ and $b_{qq} = a_{qq} + t a_{pq}$.
2. **The off-diagonal norm decreases.** $\operatorname{off}(B)^2 = \operatorname{off}(A)^2 - 2 a_{pq}^2$, because rotations keep the Frobenius norm and the norm of each pair $(a_{rp}, a_{rq})$.
3. **Classical rate.** On the largest entry, $\operatorname{off}(B)^2 \le (1 - 1/N)\operatorname{off}(A)^2$ with $N = n(n-1)/2$: at least linear convergence.
4. **Cyclic convergence.** Forsythe and Henrici (1960) proved that the cyclic order with $|\theta| \le \pi/4$ converges. Henrici (1958) and Wilkinson (1962) proved that it is quadratic per sweep for distinct eigenvalues, and Schönhage (1964) did so for multiple eigenvalues.
5. **What the diagonal means.** For $A^{(k)} = V_k^T A V_k$, the sorted diagonal is within $\operatorname{off}(A^{(k)})$ of the sorted eigenvalues, by [Weyl's inequality](/weyls-inequality/), and each column of $V_k$ has a residual at most $\operatorname{off}(A^{(k)})$. The [Gershgorin theorem](/gershgorin-circle-theorem/) with diagonal scaling shows that a well separated diagonal entry is in fact correct to second order in the off-diagonal entries.

## Complexity

- **Per rotation.** The row and column update costs $6n$ flops, plus $6n$ for $V$.
- **Per sweep.** $N = n(n-1)/2$ rotations cost about $3n^3$ flops, or $6n^3$ with the eigenvectors. These counts are exact up to lower-order terms.
- **Number of sweeps.** This number is observed, not proved: 4 to 10 sweeps for double precision, growing slowly with $n$. The implementation needs 5, 6, 7 and 7 sweeps for random symmetric matrices of order 5, 10, 20 and 30.
- **Comparison.** With 6 to 10 sweeps, Jacobi costs $20n^3$ to $60n^3$ flops with vectors. Tridiagonalization followed by QR costs about $9n^3$ with vectors and $4n^3/3$ without, so Jacobi is slower by a factor of 3 to 10 on one processor.
- **Space.** $A$ and $V$, that is $2n^2$ numbers, with $O(1)$ extra.

## Properties

- **Iterative, in place, and backward stable** in the normwise sense: the computed eigenvalues are those of $A + E$ with $\|E\| = O(u\|A\|)$ per sweep.
- **High relative accuracy.** For $A = D H D$ positive definite, with $D$ diagonal and $H$ with unit diagonal, Demmel and Veselić (1992) proved relative errors of order $u \max_k \kappa(H_k)$ for the eigenvalues, where $H_k$ is the same scaling of the $k$-th iterate. They observed that $\max_k \kappa(H_k)$ stays near $\kappa(H)$. QR-based methods only give errors of order $u \|A\|$, which can be larger than the small eigenvalues.
- **Orthogonal eigenvectors** to working accuracy, since $V$ is a product of rotations: $\|V^T V - I\| = O(s n u)$ for $s$ sweeps.
- **Parallel.** The $n/2$ rotations on disjoint pairs commute and can be done at the same time.

## Variants and improvements

- **Classical Jacobi.** Jacobi's own choice, the largest entry, is the best per rotation but needs a search; row maxima make the search cheaper.
- **Threshold Jacobi.** Skip entries below a threshold that is lowered from sweep to sweep (Rutishauser's Handbook procedure).
- **One-sided Jacobi (Hestenes).** Orthogonalize the columns of a matrix $G$ by rotations from the right; this computes the [singular value decomposition](/singular-value-decomposition/) of $G$, and the eigenvalues of $G^T G$, without forming $G^T G$. Preconditioned with a QR factorization, it is the method of Drmač and Veselić (2008) in LAPACK `xGEJSV`.
- **Parallel orderings.** Round-robin orderings of the pairs (Brent and Luk, 1985) for systolic arrays and multiprocessors.
- **Block Jacobi.** Diagonalize $b \times b$ blocks instead of $2 \times 2$ ones, for cache use.
- **Nonsymmetric and complex versions.** Unitary rotations for Hermitian matrices are direct. Norm-reducing methods for normal and general matrices exist but are rarely used.

## When to use it

Use Jacobi when you need small eigenvalues or singular values of a graded or scaled matrix to high relative accuracy, when the matrix is already nearly diagonal (a few sweeps then suffice, for example when updating the eigenvectors of a slowly changing matrix), or on hardware where its parallelism matters. For a general dense symmetric matrix on one processor, use [tridiagonalization](/tridiagonalization/) followed by QR, [divide and conquer](/divide-and-conquer-eigensolver/) or [MRRR](/mrrr-algorithm/).

## Pitfalls

- **Computing the angle by $\tan 2\theta = 2 a_{pq} / (a_{qq} - a_{pp})$ and trigonometric functions.** This is slower and less accurate. Use the root $t$ of line L5 and the update $a_{pp} - t a_{pq}$.
- **The larger root.** It also zeroes $a_{pq}$, but it gives $|\theta| > \pi/4$, and the convergence proofs fail.
- **An absolute stopping test.** Stopping when $\operatorname{off}(A) \le u\|A\|_F$ loses the relative accuracy of tiny eigenvalues. The test of line L4 compares $a_{pq}$ with $\sqrt{|a_{pp} a_{qq}|}$.
- **Updating only one triangle without care.** The formulas of line L6 read $a_{rp}$ and $a_{rq}$ before they write them; keep the old values in temporaries.
- **Nonsymmetric input.** The method assumes $a_{pq} = a_{qp}$. For a nonsymmetric matrix, rotations do not converge to a triangular form.

## Implementations

## History

Jacobi published the method in 1846 to compute the secular perturbations of planetary orbits, rotating on the largest entry and computing by hand. It was rediscovered for electronic computers around 1950, by Goldstine, Murray and von Neumann among others. Henrici (1958) and Forsythe and Henrici (1960) proved the convergence of the cyclic version, and Wilkinson (1962) and Schönhage (1964) its quadratic rate. Rutishauser's 1966 procedure in the Handbook for Automatic Computation became the standard code. In the 1960s Householder tridiagonalization with QR replaced Jacobi as the main dense method. Demmel and Veselić's 1992 paper on relative accuracy gave it a new role. The one-sided form is now the most accurate SVD method in LAPACK.

## References
