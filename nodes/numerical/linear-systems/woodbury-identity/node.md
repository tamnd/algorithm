---
tag: NKHFA0
kind: theorem
slug: woodbury-identity
name: Woodbury matrix identity
aliases:
- matrix inversion lemma
- Sherman-Morrison-Woodbury formula
- low-rank update formula
area: numerical/linear-systems
level: core
summary: Gives (A + UCV)^-1 in terms of A^-1 and a smaller k x k inverse.
prereqs: [sherman-morrison-formula, schur-complement]
see_also: [kalman-filter, bfgs, tikhonov-regularization, lup-solve, determinant, domain-decomposition, iterative-refinement, positive-definite-matrix]
sources:
  - paper: doi:10.1137/1031049
    title: William W. Hager, Updating the inverse of a matrix, SIAM Review 31(2), 1989
    locator: the Woodbury formula, its derivation from a bordered matrix, its history and applications
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 2.1, Basic Ideas from Linear Algebra (the Sherman-Morrison-Woodbury formula)
  - book: isbn:9780521548236
    title: Roger A. Horn and Charles R. Johnson, Matrix Analysis, second edition, Cambridge University Press, 2013
    locator: Section 0.7.4, Rank-one and low-rank updates of the inverse; Section 0.8.5, Schur complements and determinantal formulae
---

The Woodbury identity gives the inverse of a matrix changed by a rank-$k$ term: for $A \in \mathbb{R}^{n \times n}$ and $C \in \mathbb{R}^{k \times k}$ nonsingular, $U \in \mathbb{R}^{n \times k}$ and $V \in \mathbb{R}^{k \times n}$,

$$(A + U C V)^{-1} = A^{-1} - A^{-1} U \left(C^{-1} + V A^{-1} U\right)^{-1} V A^{-1},$$

whenever the $k \times k$ matrix $C^{-1} + V A^{-1} U$ is nonsingular. For $k \ll n$ this replaces a new $n \times n$ factorization by $k$ solves with $A$ and a $k \times k$ system. The [Sherman-Morrison formula](/sherman-morrison-formula/) is the case $k = 1$, $C = 1$.

## Statement

**Theorem.** Let $A \in \mathbb{R}^{n \times n}$ and $C \in \mathbb{R}^{k \times k}$ be nonsingular, $U \in \mathbb{R}^{n \times k}$, $V \in \mathbb{R}^{k \times n}$, and let $K = C^{-1} + V A^{-1} U$ (the *capacitance matrix*). Then

1. $\det(A + U C V) = \det A \cdot \det C \cdot \det K$;
2. $A + U C V$ is nonsingular if and only if $K$ is;
3. in that case $(A + U C V)^{-1} = A^{-1} - A^{-1} U K^{-1} V A^{-1}$, and the solution of $(A + U C V) x = b$ is $x = y - Z K^{-1} V y$ with $A y = b$ and $A Z = U$.

## In plain words

If a matrix changes by a few vector products at once, you can still reuse what you know about the old matrix. The correction needs one quick solve for each of the few directions of change, and one small system whose size is the number of directions, not the size of the matrix. The small system decides everything: if it can be solved, so can the new big one, and if it is singular, the change made the big matrix singular too.

## Proof

Consider the bordered matrix

$$M = \begin{pmatrix} A & U \\ V & -C^{-1} \end{pmatrix} \in \mathbb{R}^{(n+k) \times (n+k)}.$$

Its [Schur complement](/schur-complement/) of $A$ is $S_A = -C^{-1} - V A^{-1} U = -K$, and its Schur complement of the block $-C^{-1}$ is $S_C = A - U(-C^{-1})^{-1} V = A + U C V$.

**Part 1.** By the determinant formula for each of the two Schur complements, $\det M = \det A \cdot \det(-K) = \det(-C^{-1}) \cdot \det(A + U C V)$. Since $\det(-K) = (-1)^k \det K$ and $\det(-C^{-1}) = (-1)^k/\det C$, this gives $\det(A + U C V) = \det A \cdot \det C \cdot \det K$.

**Part 2.** $\det A \ne 0$ and $\det C \ne 0$, so part 1 gives the equivalence.

**Part 3.** Assume $K$ is nonsingular, so $M$ is nonsingular. The inverse of a block matrix in terms of the Schur complement of its leading block has lower right block $S_A^{-1}$ and upper left block $A^{-1} + A^{-1} U S_A^{-1} V A^{-1}$; in terms of the Schur complement of its trailing block, the upper left block is $S_C^{-1}$. Both describe the same block of $M^{-1}$, so

$$(A + U C V)^{-1} = S_C^{-1} = A^{-1} + A^{-1} U (-K)^{-1} V A^{-1} = A^{-1} - A^{-1} U K^{-1} V A^{-1}.$$

The formula for $x$ is this inverse applied to $b$, with $y = A^{-1} b$ and $Z = A^{-1} U$. $\blacksquare$

A direct check is also short: multiplying $(A + U C V)$ by the right side gives $I + U C V A^{-1} - U(I + C V A^{-1} U) K^{-1} V A^{-1} = I + U C V A^{-1} - U C K K^{-1} V A^{-1} = I$, using $I + C V A^{-1} U = C K$.

## Consequences

**Cost.** With a factorization of $A$, computing $Z = A^{-1} U$ takes $k$ solves, $2 k n^2$ flops with LU factors; forming $K = C^{-1} + V Z$ takes $2 k^2 n$ flops plus the inverse of $C$; factoring $K$ takes $2k^3/3$; and each right side then costs one solve with $A$, a product with $V$ and $Z$, and a $k \times k$ solve, $2n^2 + 4 k n + 2k^2$ flops. For $k \ll n$ this is far below the $2n^3/3$ of refactoring.

**A worked example.** Let $A = 2 I_3$, $C = I_2$, $U = \begin{pmatrix} 1 & 0 \\ 0 & 1 \\ 1 & 1 \end{pmatrix}$ and $V = U^T$, so that $A + U C V = \begin{pmatrix} 3 & 0 & 1 \\ 0 & 3 & 1 \\ 1 & 1 & 4 \end{pmatrix}$. Then $K = I + \tfrac12 U^T U = \begin{pmatrix} 2 & \tfrac12 \\ \tfrac12 & 2 \end{pmatrix}$, $\det K = 15/4$, $K^{-1} = \tfrac{1}{15}\begin{pmatrix} 8 & -2 \\ -2 & 8 \end{pmatrix}$, and the identity gives $(A + U C V)^{-1} = \tfrac12 I - \tfrac14 U K^{-1} U^T$. Its $(1,1)$ entry is $\tfrac12 - \tfrac14 \cdot \tfrac{8}{15} = \tfrac{11}{30}$ and its $(3,3)$ entry is $\tfrac12 - \tfrac14 \cdot \tfrac{12}{15} = \tfrac{3}{10}$, which match the direct inverse. Part 1 gives $\det = 8 \cdot 1 \cdot \tfrac{15}{4} = 30$.

**Applications.**

- *Low rank plus diagonal.* Covariance models $D + W W^T$ in factor analysis and Gaussian processes, and preconditioners of that form, are inverted in $O(n k^2)$ with $A = D$.
- *Regularized least squares with few rows.* For $X \in \mathbb{R}^{m \times p}$ with $m \ll p$, the identity gives $(X^T X + \lambda I_p)^{-1} X^T = X^T (X X^T + \lambda I_m)^{-1}$, so [Tikhonov regularization](/tikhonov-regularization/) needs an $m \times m$ solve instead of a $p \times p$ one.
- *Kalman filter.* The covariance update and the information-form update of the [Kalman filter](/kalman-filter/) are two sides of the identity, with $k$ the number of measurements.
- *Quasi-Newton methods.* The BFGS update of the inverse Hessian is the identity with $k = 2$ ([BFGS](/bfgs/)); limited-memory variants keep the factors $U$, $V$ instead of the matrix.
- *Capacitance matrix methods.* A fast solver for a simple domain is combined with a correction of rank equal to the number of boundary points that differ, which is how the identity enters [domain decomposition](/domain-decomposition/).

**Numerical behavior.** As with the rank-one formula, the identity is exact but its floating-point use can be inaccurate when $K$ is ill conditioned relative to $A + U C V$, or when $A$ is much worse conditioned than $A + U C V$. The error comes from the solves with $A$ and with $K$; there is no general bound that makes it backward stable. Refactoring after a number of updates, or one step of [iterative refinement](/iterative-refinement/) with the true matrix, are the usual safeguards. For symmetric positive definite $A$ and $C$, $K$ is symmetric positive definite and can be factored by Cholesky.

## Tightness

- **$K$ singular means $A + U C V$ singular.** For $A = I_n$, $C = I_k$, $U = -V^T$ with $V V^T = I_k$, $K = I_k - V V^T = 0$, and $A + U C V = I - V^T V$ is the projector onto the complement of the row space of $V$, which is singular.
- **$C$ singular.** The identity uses $C^{-1}$. If $C$ is singular, write $U C V = (U C) V$ and use the form $(A + U' V)^{-1} = A^{-1} - A^{-1} U'(I + V A^{-1} U')^{-1} V A^{-1}$ with $U' = U C$, which needs no inverse of $C$.
- **$A$ singular.** The identity has no meaning, although $A + U C V$ may be nonsingular; then a different splitting must be chosen.

## History

Woodbury's Princeton memorandum of 1950 gave the rank-$k$ formula, at the same time as Sherman and Morrison's rank-one formula for a change of one entry. Hager (1989) traces earlier forms, among them Duncan (1944) and Guttman (1946), and surveys the uses in statistics, structural mechanics, networks and optimization. In control and signal processing the identity is known as the matrix inversion lemma.

## References
