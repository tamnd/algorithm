---
tag: WCHJ4Y
kind: algorithm
slug: qz-algorithm
name: QZ algorithm
aliases:
- generalized Schur algorithm
- Moler-Stewart algorithm
area: numerical/eigenproblems
level: advanced
summary: Computes the generalized Schur form Q* A Z = S, Q* B Z = T of a pencil with unitary Q, Z and triangular S, T, by QR-type steps that never invert B. Backward stable; handles singular B.
solves: [generalized-eigenvalue-problem]
model: floating-point-model
complexity:
  vars: {n: "the order of A and B"}
  time: {worst: O(n^3)}
  space: {extra: Θ(n^2)}
  flops: {eigenvalues: "30 n^3", with_q_and_z: "66 n^3", reduction: "8 n^3"}
properties: {deterministic: true, in_place: true, recursive: false, iterative: true}
history:
  year: 1973
  people: [Cleve B. Moler, G. W. Stewart]
  note: Moler and Stewart published the QZ algorithm in 1973 as the analogue of Francis's QR algorithm for the pencil A − λB.
prereqs: [generalized-eigenvalue-problem, qr-algorithm, givens-rotations]
see_also: [schur-decomposition, hessenberg-reduction, francis-double-shift-qr, wilkinson-shift, deflation, eigenvalue-condition-number, matrix-balancing, backward-error-analysis]
sources:
  - paper: doi:10.1137/0710024
    title: C. B. Moler and G. W. Stewart, An algorithm for generalized matrix eigenvalue problems, SIAM Journal on Numerical Analysis 10(2), 1973
    locator: pp. 241 to 256 (Hessenberg-triangular reduction, the double-shift QZ step, deflation of infinite eigenvalues)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 7.7, The Generalized Eigenvalue Problem (7.7.2 the generalized Schur decomposition, 7.7.4 Hessenberg-triangular form, 7.7.5 deflation, 7.7.6 the QZ step, and the flop counts)
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Section 4.5, Other Nonsymmetric Eigenvalue Problems (regular pencils, the generalized Schur form and QZ)
  - book: isbn:9780898715033
    title: G. W. Stewart, Matrix Algorithms, Volume II, Eigensystems, SIAM, 2001
    locator: Chapter 2, Section 4, The Generalized Eigenvalue Problem (the QZ algorithm and its backward stability)
  - book: isbn:9780898714715
    title: Zhaojun Bai, James Demmel, Jack Dongarra, Axel Ruhe and Henk van der Vorst (editors), Templates for the Solution of Algebraic Eigenvalue Problems, SIAM, 2000
    locator: Section 8.4, Direct Methods (QZ for dense generalized non-Hermitian problems)
  - paper: "D. S. Watkins and L. Elsner, Theory of decomposition and bulge-chasing algorithms for the generalized eigenvalue problem, SIAM Journal on Matrix Analysis and Applications 15(3), 1994"
    title: Theory of decomposition and bulge-chasing algorithms for the generalized eigenvalue problem
    locator: SIAM J. Matrix Anal. Appl. 15(3) (1994), pp. 943 to 967
---

The QZ algorithm solves the [generalized eigenvalue problem](/generalized-eigenvalue-problem/) $A x = \lambda B x$ for dense square matrices. It computes unitary $Q$ and $Z$ such that $S = Q^* A Z$ and $T = Q^* B Z$ are both upper triangular, the generalized [Schur form](/schur-decomposition/); the eigenvalues are then the ratios $\lambda_i = s_{ii} / t_{ii}$, with $t_{ii} = 0$ meaning an infinite eigenvalue. It is the [QR algorithm](/qr-algorithm/) applied implicitly to $A B^{-1}$ (and to $B^{-1} A$) without ever forming the inverse: after a reduction to Hessenberg-triangular form, each step chases a bulge down the pencil with rotations from both sides, using only unitary transformations, so the result is backward stable for the pair $(A, B)$ even when $B$ is singular or badly conditioned. It costs about $30 n^3$ flops for the eigenvalues and $66 n^3$ with $Q$ and $Z$ (counts for the real double-shift version).

## In plain words

Sometimes a problem asks not for the special numbers of one table but for the special numbers of a pair of tables, where one table's stretching is compared with the other's. One could divide one table by the other and solve the usual problem, but if the second table is nearly flat the division blows up the errors. The QZ algorithm never divides. It turns both tables at once, from the left and from the right, by the same rigid turns, until both have only zeros below the diagonal. Then each special number is a ratio of two diagonal entries, and a zero at the bottom of the ratio is an answer at infinity.

## The problem

**Notation.** $A, B \in \mathbb C^{n \times n}$, the pencil $A - \lambda B$. The generalized Schur form is $Q^* A Z = S$, $Q^* B Z = T$ with $Q$, $Z$ unitary and $S$, $T$ upper triangular; on this page $S$ and $T$ play the role of the triangular factor $T$ of the ordinary Schur form $A = Q T Q^*$. During the iteration $H$ is upper Hessenberg and $T$ upper triangular, with $Q^* A Z = H$ and $Q^* B Z = T$ at every moment. Eigenvalues are pairs $(\alpha_i, \beta_i) = (s_{ii}, t_{ii})$, standing for $\lambda_i = \alpha_i / \beta_i$. $u$ is the unit roundoff and $\varepsilon = 2u$ the machine epsilon used in the deflation tests.

**Input.** Two square matrices of order $n$. The pencil is regular when $\det(A - \lambda B)$ is not identically zero; then it has $n$ eigenvalues counting infinite ones, and $n - \deg \det(A - \lambda B)$ of them are infinite.

**Output.** $Q$, $Z$, $S$, $T$ with $Q^* (A + E) Z = S$ and $Q^* (B + F) Z = T$, where $E$ and $F$ are the deflation perturbations described in the Correctness section; in floating point $\|E\| = O(u \|A\|)$ and $\|F\| = O(u \|B\|)$. For a singular pencil some pair $(\alpha_i, \beta_i)$ is $(0, 0)$ up to rounding, and the other pairs are not determined by the pencil.

## The algorithm

```pseudo id=main
QZ(A, B)
L1  (H, T, Q, Z) ← Hessenberg-triangular reduction of (A, B)   ▷ Q*AZ = H Hessenberg, Q*BZ = T triangular
L2  hi ← n
L3  while hi > 1 do
L4      set each h_{k,k−1} with |h_{k,k−1}| ≤ ε (|h_{k−1,k−1}| + |h_{kk}|) to 0
L5      if h_{hi,hi−1} = 0 then hi ← hi − 1; continue          ▷ deflate a converged 1 × 1 block
L6      lo ← least index with h_{k,k−1} ≠ 0 for lo < k ≤ hi; set each t_kk, lo ≤ k ≤ hi, with |t_kk| ≤ ε ‖T‖_F to 0
L7      if t_kk = 0 for some lo ≤ k ≤ hi then chase the zero up to t_{lo,lo} and zero h_{lo+1,lo}; continue   ▷ infinite eigenvalue
L8      μ ← eigenvalue of the trailing 2 × 2 pencil nearer to h_{hi,hi} / t_{hi,hi}   ▷ the shift
L9      apply from the left the rotation G with G (h_{lo,lo} − μ t_{lo,lo}, h_{lo+1,lo})ᵀ = (r, 0)ᵀ
L10     for k ← lo to hi − 1: zero t_{k+1,k} by a rotation of columns k, k+1, then h_{k+2,k} by a rotation of rows k+1, k+2   ▷ chase the bulge
L11 return (S, T, Q, Z) ← (H, T, Q, Z);  αᵢ ← s_ii,  βᵢ ← t_ii
```

Every rotation acts on both $H$ and $T$: a rotation $G$ of rows updates $H \leftarrow G H$, $T \leftarrow G T$ and $Q \leftarrow Q G^*$, and a rotation $R$ of columns updates $H \leftarrow H R$, $T \leftarrow T R$ and $Z \leftarrow Z R$, so $Q^* A Z = H$ and $Q^* B Z = T$ hold throughout. Line L1 first triangularizes $B$ by rotations of rows, then removes the entries of $H$ below the subdiagonal column by column; each such row rotation creates one entry below the diagonal of $T$, which a column rotation removes without disturbing $H$ (GVL Algorithm 7.7.1). The vector in line L9 is $(H T^{-1} - \mu I) e_1$ scaled by $t_{lo,lo}$, so the step is a shifted QR step on $H T^{-1}$ done implicitly. The implementation uses complex arithmetic and single shifts; the real version of Moler and Stewart uses double shifts as in [Francis's algorithm](/francis-double-shift-qr/) to keep real data real.

## Example

**An infinite eigenvalue.** Let

$$A = \begin{pmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 10 \end{pmatrix}, \qquad B = \begin{pmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 0 \end{pmatrix}.$$

Then $\det(A - \lambda B) = 10 \lambda^2 + 9 \lambda - 3$, computed exactly in rational arithmetic, which has degree 2, so there are two finite eigenvalues $(-9 \pm \sqrt{201})/20 = 0.258872$ and $-1.158872$ and one infinite eigenvalue. Line L1 gives

$$H = \begin{pmatrix} 1 & -3 & 2 \\ 8.062258 & -11.659265 & 9.426640 \\ 0 & 0.248069 & -0.372104 \end{pmatrix}, \qquad T = \begin{pmatrix} 1 & 0 & 0 \\ 0 & 0 & 0.496139 \\ 0 & 0 & -0.868243 \end{pmatrix},$$

with $t_{22} = 0$ exactly, as it must be since $B$ has rank 2. Line L7 chases this zero to $t_{11}$ and zeroes $h_{21}$, which splits off the pair $(\alpha_1, \beta_1) = (12.041595, 0)$, the infinite eigenvalue. The remaining $2 \times 2$ block converges in one QZ step, because the shift of line L8 is then an exact eigenvalue: $|h_{32}|$ drops to $2.8 \times 10^{-17}$, and the pairs $(1.098313, -0.947743)$ and $(-0.226836, -0.876245)$ give $\lambda = -1.158872$ and $0.258872$.

**Quadratic convergence.** For a random $6 \times 6$ pencil with entries uniform in $[-1, 1]$ (seed 1 of the tests), the method takes 16 QZ steps for 6 eigenvalues. While the bottom eigenvalue converges, $|h_{65}|$ runs $0.12$, $0.068$, $0.054$, $4.1 \times 10^{-4}$, $9.7 \times 10^{-9}$, $1.5 \times 10^{-18}$: each value is roughly the square of the previous one once the shift is close. These numbers come from the implementation and are checked by its tests.

## Correctness

The full proofs are in [proofs/correctness.md](proofs/correctness.md); the argument, in exact arithmetic apart from the deflations:

- **The invariant.** Each operation is a rotation of two rows applied to both $H$ and $T$ (with $Q \leftarrow Q G^*$) or of two columns applied to both (with $Z \leftarrow Z R$). So $Q$, $Z$ stay unitary and $Q^* A Z = H$, $Q^* B Z = T$ hold, except for the entries that line L4 and line L6 set to zero.
- **The structure.** Line L1 produces Hessenberg $H$ and triangular $T$. The bulge chase of lines L9 and L10 and the zero chase of line L7 restore this structure after every rotation: each rotation creates exactly one nonzero entry outside it, and the next rotation removes it.
- **Deflation.** A zero $h_{k,k-1}$ splits the pencil into two independent pencils; a zero $t_{lo,lo}$ is an infinite eigenvalue, and after the chase, $h_{lo+1,lo} = 0$ splits it off. Each subdiagonal position is set to zero at most once, and each such entry is at most $2 \varepsilon \|A\|_F$ in size, so $\|E\|_F \le 2 (n - 1) \, \varepsilon \, \|A\|_F$ to first order. The diagonal entries of $T$ set to zero are each at most $\varepsilon \|B\|_F$ in size, and there are at most $n$ of them per deflation, so $\|F\|_F \le n (n - 1) \, \varepsilon \, \|B\|_F$, a crude bound that is far from attained in practice.
- **Termination.** Each pass either deflates, which happens at most $n - 1$ times, or takes a QZ step, of which there are at most $30n$ (the cap of the implementation). So the loop ends, and on success $H$ and $T$ are upper triangular.
- **Convergence (cited).** By the implicit Q theorem for pencils, the step of lines L9 and L10 is one step of the shifted QR algorithm applied to $H T^{-1}$ and to $T^{-1} H$ (GVL Section 7.7; Watkins and Elsner 1994). Hence the convergence theory of the shifted QR algorithm carries over: quadratic local convergence of $h_{hi,hi-1}$ to zero for a simple eigenvalue with the shift of line L8, and no proof of global convergence, as for the QR algorithm.

**Backward stability (cited).** In floating point, the computed $S$, $T$ are the exact generalized Schur form of $(A + E, B + F)$ with $\|E\|_2 \approx u \|A\|_2$ and $\|F\|_2 \approx u \|B\|_2$, up to modest constants depending on $n$, and the computed $Q$, $Z$ are within $O(u)$ of unitary (Moler and Stewart 1973; GVL Section 7.7). The tests observe $\|A - Q S Z^*\|_F / \|A\|_F$, $\|B - Q T Z^*\|_F / \|B\|_F$ and the departure from unitarity all below $3.4 \, n u$ over 200 random pencils. The eigenvalues themselves can still be inaccurate when they are ill conditioned; the natural measure is the chordal distance between $(\alpha, \beta)$ pairs (Stewart and Sun, Chapter VI).

## Complexity

**Flops (cited, real double-shift QZ).** The Hessenberg-triangular reduction costs about $8 n^3$ flops, and with the usual assumption of about two QZ steps per eigenvalue the whole algorithm costs about $30 n^3$ flops for the eigenvalues alone and $66 n^3$ with $Q$ and $Z$ (GVL Section 7.7). These counts rest on the typical number of steps, not a proved bound.

**Steps (observed).** Over 200 random pencils of order 2 to 9 the implementation took 2.3 complex QZ steps per eigenvalue on average and at most 3.5. Each step on an active block of order $m$ costs $O(n m)$ flops when $Q$ and $Z$ are accumulated, and the cap of $30n$ steps makes the worst case $O(n^3)$ for the implementation.

**Space.** In place in $A$ and $B$, plus $Q$ and $Z$ when wanted.

## Properties

- **No inversion of $B$.** Only unitary transformations are used, so a singular or ill conditioned $B$ causes no instability; infinite eigenvalues appear as $\beta_i = 0$.
- **Backward stable** for the pair $(A, B)$ jointly, which is the right notion: the errors are relative to $\|A\|$ and $\|B\|$ separately.
- **Symmetric in A and B.** Swapping $A$ and $B$ swaps $\alpha$ and $\beta$, so zero and infinite eigenvalues are treated alike.
- **Reduces to QR.** With $B = I$ the iterates are those of the [QR algorithm](/qr-algorithm/) with $Q = Z$.
- **Does not preserve symmetry.** For symmetric $A$ and positive definite $B$, the Cholesky-based reduction to a standard symmetric problem is cheaper and keeps the structure.

## Variants and improvements

- **Double-shift real QZ.** Moler and Stewart's original version uses two shifts from the trailing $2 \times 2$ pencil and $3 \times 3$ Householder reflectors, so that complex conjugate pairs are computed in real arithmetic, and ends with a quasi-triangular $S$.
- **Multishift and aggressive early deflation.** Kågström and Kressner (2006) carry over the small-bulge multishift and aggressive early deflation techniques of the QR algorithm, giving the LAPACK 3.x routine xHGEQZ its block-oriented speed.
- **Balancing.** Ward's balancing scales the rows and columns of $A$ and $B$ by two diagonal matrices before QZ, the pencil analogue of [matrix balancing](/matrix-balancing/) (LAPACK xGGBAL).
- **Reordering.** Swapping adjacent diagonal blocks of $(S, T)$ by unitary transformations moves selected eigenvalues to the top, giving deflating subspaces, as needed in control theory (LAPACK xTGSEN).
- **The QZ algorithm for singular pencils.** For singular pencils the GUPTRI algorithm of Demmel and Kågström first extracts the singular part of the Kronecker canonical form.

## When to use it

Use QZ for dense generalized eigenproblems $A x = \lambda B x$ when $B$ may be singular or ill conditioned, when no symmetry is available, or when the deflating subspaces are wanted, for example in descriptor systems, the polynomial eigenvalue problem after linearization, and the solution of algebraic Riccati equations. When $B$ is well conditioned and speed matters, forming $B^{-1} A$ and running the QR algorithm is cheaper but loses accuracy in proportion to the condition number of $B$. For symmetric $A$ with positive definite $B$, use the Cholesky reduction and a symmetric solver; for large sparse pencils, use shift-and-invert Krylov methods.

## Pitfalls

- **Reading ratios too early.** Do not divide $\alpha_i / \beta_i$ when $\beta_i$ is tiny; report the pair, or the chordal value, since a tiny $\beta_i$ may be an infinite eigenvalue perturbed by rounding.
- **Singular pencils.** If $\det(A - \lambda B) \equiv 0$, QZ still runs, but every computed eigenvalue can be arbitrary, because a backward perturbation of size $u$ can move them anywhere; a pair with $\alpha_i \approx \beta_i \approx 0$ is the warning sign.
- **Negligible diagonal entries of T.** A test that is too strict leaves a tiny $t_{kk}$ in place, and the shift $h_{kk} / t_{kk}$ becomes huge and slows convergence; a test that is too loose creates spurious infinite eigenvalues.
- **Inverting B.** Forming $B^{-1} A$ to save time gives errors of size $u \, \kappa(B) \, \|A\|$, which can be far worse than QZ.
- **Shift without exceptional shifts.** As for the QR algorithm, rare cycles occur; the implementation uses an ad hoc shift every 11 steps without deflation.

## Implementations

## History

Cleve Moler and G. W. Stewart published the QZ algorithm in 1973, extending Francis's implicitly shifted QR algorithm to pencils by applying different unitary transformations on the left and the right; it went into EISPACK as qzhes, qzit, qzval and qzvec, and later into LAPACK. Linda Kaufman's LZ algorithm of 1974 used stabilized elementary transformations instead. Watkins and Elsner (1994) gave a general theory of bulge-chasing algorithms for the pencil, and Kågström and Kressner (2006) brought in multishift steps and aggressive early deflation.

## References
