---
tag: 5JCA6Q
kind: algorithm
slug: gram-schmidt-process
name: Gram-Schmidt process
aliases:
- Gram-Schmidt orthogonalization
- modified Gram-Schmidt
- classical Gram-Schmidt
- MGS
- CGS
area: numerical/linear-systems
level: core
summary: Orthonormalize columns of A, yielding the QR factorization.
model: floating-point-model
complexity:
  vars: {m: "the number of rows of A", n: "the number of columns of A (n ≤ m)"}
  time: {worst: Θ(m n^2)}
  space: {extra: Θ(n^2)}
  flops: {worst: "2 m n^2 + O(m n)"}
properties: {deterministic: true, in_place: true, recursive: false, iterative: false}
prereqs: [qr-decomposition, matrix-norms, condition-number]
see_also: [householder-reflections, givens-rotations, least-squares-problem, arnoldi-iteration, gmres, lanczos-algorithm, orthogonal-polynomials, krylov-subspace]
sources:
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 19.8, Gram-Schmidt Orthogonalization (Theorem 19.13, the backward error and the loss of orthogonality of MGS; the equivalence with Householder QR)
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 7, QR Factorization (classical Gram-Schmidt); Lecture 8, Gram-Schmidt Orthogonalization (modified Gram-Schmidt and its operation count); Lecture 9, MATLAB (the loss of orthogonality experiment)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 5.2, The QR Factorization (the classical and modified Gram-Schmidt algorithms, their work and accuracy)
  - book: isbn:9780898713602
    title: Åke Björck, Numerical Methods for Least Squares Problems, SIAM, 1996
    locator: Section 2.4, Gram-Schmidt Orthogonalization (loss of orthogonality, reorthogonalization, MGS for least squares)
  - paper: doi:10.1007/BF01934122
    title: Åke Björck, Solving linear least squares problems by Gram-Schmidt orthogonalization, BIT 7, 1967
    locator: pp. 1 to 21 (the bound of order u κ_2(A) on the loss of orthogonality of MGS, and the stable least squares solver)
  - paper: doi:10.1137/0613015
    title: Åke Björck and Christopher C. Paige, Loss and recapture of orthogonality in the modified Gram-Schmidt algorithm, SIAM Journal on Matrix Analysis and Applications 13(1), 1992
    locator: pp. 176 to 190 (MGS is numerically equivalent to Householder QR on the matrix with n zero rows on top of A)
  - paper: doi:10.1007/s00211-005-0615-4
    title: Luc Giraud, Julien Langou, Miroslav Rozložník and Jasper van den Eshof, Rounding error analysis of the classical Gram-Schmidt orthogonalization process, Numerische Mathematik 101, 2005
    locator: pp. 87 to 100 (the loss of orthogonality of CGS is of order u κ_2(A)^2, and CGS2 keeps it at order u)
  - paper: doi:10.1007/BF01449770
    title: Erhard Schmidt, Zur Theorie der linearen und nichtlinearen Integralgleichungen, Mathematische Annalen 63, 1907
    locator: pp. 433 to 476 (the orthogonalization of a sequence of functions)
---

The Gram-Schmidt process turns the columns $a_1, \ldots, a_n$ of an $m \times n$ matrix $A$ of full column rank into orthonormal vectors $q_1, \ldots, q_n$ with $\operatorname{span}\{q_1, \ldots, q_j\} = \operatorname{span}\{a_1, \ldots, a_j\}$ for every $j$. Recording the coefficients gives the thin [QR factorization](/qr-decomposition/) $A = Q R$, with $R$ upper triangular with positive diagonal. Classical Gram-Schmidt (CGS) and modified Gram-Schmidt (MGS) are identical in exact arithmetic and cost $2 m n^2$ flops, but differ in floating point: both give a small residual $A - \hat Q \hat R$, while the loss of orthogonality $\|I - \hat Q^T \hat Q\|_2$ is of order $u \kappa_2(A)$ for MGS and of order $u \kappa_2(A)^2$ for CGS. CGS repeated once (CGS2) is orthogonal to working precision. Gram-Schmidt is the orthogonalization inside [Arnoldi](/arnoldi-iteration/) and [GMRES](/gmres/).

## In plain words

Start with a list of directions that are independent but may point almost the same way. Take the first one and scale it to length one. For the second, remove the part that points along the first, and scale what is left. For the third, remove the parts along the first two, and so on. Each new vector is at right angles to all the earlier ones, and together they reach exactly the same set of directions as the original list.

On a computer, removing the parts one at a time from the running remainder (the modified version) is much more reliable than computing all parts from the original vector (the classical version). The two only differ in rounding, but the difference matters when the starting vectors are nearly parallel.

## The problem

**Notation.** $A = [a_1, \ldots, a_n] \in \mathbb{R}^{m \times n}$ with $m \ge n$ and rank $n$. $\kappa_2(A) = \sigma_{\max}(A) / \sigma_{\min}(A)$, $u = 2^{-53}$ and $\gamma_k = k u/(1 - k u)$, as in [solving linear systems](/linear-system-solving/). Hats denote computed quantities. The loss of orthogonality is $\|I - \hat Q^T \hat Q\|_2$.

Input: $A$. Output: $Q \in \mathbb{R}^{m \times n}$ with orthonormal columns and an upper triangular $R \in \mathbb{R}^{n \times n}$ with $r_{jj} > 0$ and $A = Q R$. If some $a_j$ lies in the span of the earlier columns, the process meets $r_{jj} = 0$ and reports rank deficiency.

## The algorithm

MGS orthogonalizes against $q_j$ as soon as $q_j$ is known, updating all later columns. The column $a_k$ is overwritten by its running remainder, so after step $j$ it is orthogonal to $q_1, \ldots, q_j$.

```pseudo id=main
MGS(A)                                     ▷ A = [a₁ … aₙ] is overwritten
L1  for j ← 1 to n do
L2      r_jj ← ‖a_j‖₂
L3      if r_jj = 0 then fail (rank deficient)
L4      q_j ← a_j / r_jj
L5      for k ← j + 1 to n do
L6          r_jk ← q_jᵀ a_k                   ▷ a_k is already orthogonal to q₁ … q_{j−1}
L7          a_k ← a_k − r_jk q_j
L8  return (Q, R)
```

CGS computes all coefficients of column $j$ from the original $a_j$:

```pseudo id=cgs
CGS(A)
C1  for j ← 1 to n do
C2      r_ij ← q_iᵀ a_j  for i = 1, …, j − 1    ▷ one product Q_{j−1}ᵀ a_j
C3      v ← a_j − Σ_{i<j} r_ij q_i
C4      r_jj ← ‖v‖₂; if r_jj = 0 then fail
C5      q_j ← v / r_jj
```

In exact arithmetic $q_i^T a_k$ equals $q_i^T (a_k - \sum_{l < i} r_{lk} q_l)$, because the $q_l$ are orthogonal to $q_i$. So lines L6 and C2 compute the same numbers. In floating point the computed $q_l$ are not exactly orthogonal, and MGS projects out the errors made in earlier steps, while CGS does not. **CGS2** repeats lines C2 and C3 once on $v$ and adds the new coefficients to $R$.

## Example

For
$$A = \begin{pmatrix} 1 & 3 & 5 \\ 2 & 3 & 1 \\ 2 & 0 & 1 \end{pmatrix}:$$
$r_{11} = \|(1, 2, 2)\|_2 = 3$ and $q_1 = (1, 2, 2)/3$. Then $r_{12} = q_1^T a_2 = 3$ and $a_2 - 3 q_1 = (2, 1, -2)$, so $r_{22} = 3$ and $q_2 = (2, 1, -2)/3$. For the third column, $r_{13} = 3$ and $r_{23} = 3$, and the remainder $(2, -2, 1)$ gives $r_{33} = 3$. So
$$Q = \frac13 \begin{pmatrix} 1 & 2 & 2 \\ 2 & 1 & -2 \\ 2 & -2 & 1 \end{pmatrix}, \qquad R = \begin{pmatrix} 3 & 3 & 3 \\ 0 & 3 & 3 \\ 0 & 0 & 3 \end{pmatrix}.$$

**Loss of orthogonality.** The Läuchli matrix $A = \begin{pmatrix} 1 & 1 & 1 \\ \varepsilon & 0 & 0 \\ 0 & \varepsilon & 0 \\ 0 & 0 & \varepsilon \end{pmatrix}$ with $\varepsilon = 10^{-8}$ has $\kappa_2(A) \approx \sqrt 3 / \varepsilon \approx 1.7 \times 10^{8}$. Since $\varepsilon^2 < u$, $\mathrm{fl}(1 + \varepsilon^2) = 1$. In binary64, CGS returns $\hat q_2^T \hat q_3 = 0.5$: the vectors are 60 degrees apart, a complete loss of orthogonality. MGS returns $\hat q_2^T \hat q_3 \approx 10^{-16}$ and $\hat q_1^T \hat q_3 \approx -4.1 \times 10^{-9}$, consistent with the $u \kappa_2(A) \approx 1.9 \times 10^{-8}$ bound. CGS2 gives $\|I - \hat Q^T \hat Q\|_2 \approx 3 \times 10^{-17}$. On the [Hilbert matrix](/hilbert-matrix/) $H_8$ ($\kappa_2 \approx 1.5 \times 10^{10}$), the loss is $1.0$ for CGS, $3.9 \times 10^{-7}$ for MGS and $2.6 \times 10^{-16}$ for CGS2.

## Correctness

The proofs are in `proofs/correctness.md` and `proofs/complexity.md`.

1. **Exact arithmetic (proved).** If $A$ has rank $n$, MGS and CGS never fail and return the same $Q$ and $R$, with $Q^T Q = I$, $A = Q R$, $r_{jj} > 0$ and $\operatorname{span}\{q_1, \ldots, q_j\} = \operatorname{span}\{a_1, \ldots, a_j\}$. This thin QR factorization with positive diagonal is unique. If $a_j \in \operatorname{span}\{a_1, \ldots, a_{j-1}\}$ for the first such $j$, both fail at step $j$. Moreover, $r_{jj}^2 = \det G_j / \det G_{j-1}$ where $G_j$ is the leading $j \times j$ block of $A^T A$, which the tests use as an exact oracle.
2. **Backward error of the factorization (cited).** Both MGS and CGS give $\hat Q \hat R = A + \Delta A$ with $\|\Delta a_j\|_2 \le c_{m,n} u \|a_j\|_2$ for every column (Higham, Section 19.8; for CGS, Giraud et al. 2005). The residual is never the problem.
3. **Loss of orthogonality of MGS (Björck 1967, cited).** If $c_2 u \kappa_2(A) < 1$, then $\|I - \hat Q^T \hat Q\|_2 \le c_1 u \kappa_2(A) / (1 - c_2 u \kappa_2(A))$, with $c_1, c_2$ depending only on $m$ and $n$. This is a worst-case bound, and it is attained up to a constant, as the Läuchli example shows.
4. **MGS is Householder in disguise (Björck and Paige 1992, cited).** MGS on $A$ performs, in floating point, the same computation as [Householder QR](/householder-reflections/) on $\begin{pmatrix} 0_n \\ A \end{pmatrix}$. So $\hat R$ from MGS is as accurate as the $R$ of Householder QR, and products with $\hat Q$ can be made backward stable if $\hat Q$ is applied in the right way. This is why MGS gives a stable [least squares](/least-squares-problem/) solver when $b$ is treated as column $n + 1$ (Björck 1967).
5. **CGS (Giraud et al. 2005, cited).** If $c u \kappa_2(A)^2 < 1$, then $\|I - \hat Q^T \hat Q\|_2 = O(u \kappa_2(A)^2)$; for larger $\kappa_2(A)$ nothing is guaranteed, and $\hat Q$ can be far from orthogonal (Läuchli). CGS2 gives $\|I - \hat Q^T \hat Q\|_2 = O(u)$ whenever $c u \kappa_2(A) < 1$ ("twice is enough", Kahan and Parlett; Giraud et al.).

## Complexity

| quantity | cost |
|---|---|
| MGS or CGS, $m \times n$ | $2 m n^2 + O(m n)$ flops and $n$ square roots (proved) |
| CGS2 | $4 m n^2 + O(m n)$ flops |
| Householder QR, for comparison | $2 m n^2 - \tfrac23 n^3$ flops, or $4 m n^2 - \tfrac43 n^3$ with $Q$ formed explicitly |
| storage | $A$ overwritten by $Q$, plus $R$: $n^2/2$ numbers |

The flop counts of MGS and CGS are equal, but their memory access differs. CGS step $j$ is two matrix-vector products, $Q_{j-1}^T a_j$ and $Q_{j-1} r$, which can be blocked (BLAS-2 or, for blocks of columns, BLAS-3) and need one global reduction per column on a distributed machine. MGS step $j$ is a sequence of $n - j$ dot products and vector updates (BLAS-1), each a separate reduction. On parallel machines this communication, not the flop count, dominates, which is why CGS2 is the usual choice in parallel [GMRES](/gmres/) and Arnoldi codes.

## Properties

- **Exact arithmetic equivalence.** CGS, MGS and CGS2 compute the same $Q$ and $R$ in exact arithmetic.
- **Column order matters.** $q_j$ depends only on $a_1, \ldots, a_j$, so Gram-Schmidt processes columns one at a time, which suits [Arnoldi](/arnoldi-iteration/), where the next column is not known in advance. Householder QR does not produce $q_j$ until it is applied to $e_j$.
- **Thin factor only.** Gram-Schmidt gives $Q$ with $n$ columns; it does not give an orthonormal basis of the orthogonal complement, unlike Householder QR.
- **In place.** $A$ can be overwritten by $Q$.

## Variants and improvements

- **CGS2 and selective reorthogonalization.** Repeat the projection, always or only when $\|v\|_2$ drops below a fraction (for example $1/\sqrt 2$, Daniel, Gragg, Kaufman and Stewart 1976) of the norm before projection.
- **Column pivoting.** Choose as next column the remaining one with the largest remainder norm. This gives a rank-revealing factorization ([rank-revealing factorization](/rank-revealing-factorization/)) and handles rank deficiency.
- **Block Gram-Schmidt.** Orthogonalize blocks of $s$ columns, with an inner QR for each block; the variants BCGS2 and block MGS trade stability for BLAS-3 speed.
- **Low-synchronization variants.** One reduction per column with a lagged normalization, used in exascale GMRES.
- **Weighted inner products.** Replace $q^T v$ by $q^T W v$; with polynomials and $\int_0^1$ this generates the [orthogonal polynomials](/orthogonal-polynomials/).

## When to use it

Use MGS or CGS2 when the columns arrive one at a time, as in Krylov methods ([Arnoldi](/arnoldi-iteration/), [GMRES](/gmres/), [Lanczos](/lanczos-algorithm/) with reorthogonalization), or when the explicit thin $Q$ is wanted and $\kappa_2(A)$ is moderate. For a general QR of a given matrix, or a least squares solve, [Householder reflections](/householder-reflections/) are the default: they give an orthogonal $Q$ to working precision regardless of $\kappa_2(A)$. Use CGS alone only when $\kappa_2(A)$ is known to be small or when the next step tolerates nonorthogonality.

## Pitfalls

- **Classical Gram-Schmidt on ill-conditioned data.** The loss of orthogonality grows like $u \kappa_2(A)^2$ and can reach $O(1)$, as in the Läuchli example; reorthogonalize.
- **Using $\hat Q^T b$ from MGS for least squares.** With $\hat Q$ not orthogonal, $x = \hat R^{-1} \hat Q^T b$ is not backward stable. Instead, append $b$ as an extra column and use the last column of $R$ (Björck 1967), as the implementation does.
- **Testing rank by $r_{jj} = 0$.** In floating point a dependent column gives $r_{jj}$ of order $u \|a_j\|$, not zero. Compare $r_{jj}$ with a tolerance, or use a [rank-revealing factorization](/rank-revealing-factorization/).
- **Normal equations instead.** Computing $R$ from the [Cholesky decomposition](/cholesky-decomposition/) of $A^T A$ squares the condition number; it is the same error as using CGS without reorthogonalization.

## Implementations

## History

Laplace used the process in 1812 in a least squares context, without the name. Gram (1883) orthogonalized functions for least squares approximation, and Schmidt (1907) stated the recursion for sequences of functions in his work on integral equations. The numerical difference between the classical and modified forms was observed by Rice (1966) in experiments and explained by Björck (1967), who proved the $u \kappa_2(A)$ bound for MGS. Björck and Paige (1992) showed the equivalence with Householder QR, and Giraud, Langou, Rozložník and van den Eshof (2005) proved the $u \kappa_2(A)^2$ bound for CGS and the stability of CGS2. Leon, Björck and Gander (2013) give the full history.

## References
