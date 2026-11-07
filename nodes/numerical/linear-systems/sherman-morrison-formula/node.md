---
tag: 83BRZ0
kind: theorem
slug: sherman-morrison-formula
name: Sherman-Morrison formula
aliases:
- rank-one update formula
- matrix determinant lemma
- Bartlett's formula
area: numerical/linear-systems
level: core
summary: Gives the inverse of A + u v^T from A^-1 in O(n^2) time.
prereqs: [matrix-inversion, schur-complement]
see_also: [woodbury-identity, lup-solve, thomas-algorithm, bfgs, kalman-filter, iterative-refinement, determinant, cyclic-reduction]
sources:
  - paper: doi:10.1214/aoms/1177729893
    title: Jack Sherman and Winifred J. Morrison, Adjustment of an inverse matrix corresponding to a change in one element of a given matrix, Annals of Mathematical Statistics 21(1), 1950
    locator: the formula for a change in a single entry
  - paper: doi:10.1137/1031049
    title: William W. Hager, Updating the inverse of a matrix, SIAM Review 31(2), 1989
    locator: the Sherman-Morrison and Woodbury formulas, their history, and applications to statistics, networks, optimization and partial differential equations
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 2.1, Basic Ideas from Linear Algebra (the Sherman-Morrison-Woodbury formula)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 14, Matrix Inversion (the formula is used in the inversion and updating context; the reasons for solving rather than inverting)
---

The Sherman-Morrison formula expresses the inverse of a rank-one change of a matrix in terms of the inverse of the original: if $A$ is nonsingular and $1 + v^T A^{-1} u \ne 0$, then

$$(A + u v^T)^{-1} = A^{-1} - \frac{A^{-1} u\, v^T A^{-1}}{1 + v^T A^{-1} u}.$$

In practice it is used for solving, not inverting: with a factorization of $A$ at hand, the system $(A + u v^T) x = b$ costs two solves with $A$ and $O(n)$ more work, instead of a new $O(n^3)$ factorization. The [Woodbury identity](/woodbury-identity/) is the same statement for a rank-$k$ change.

## Statement

**Theorem.** Let $A \in \mathbb{R}^{n \times n}$ be nonsingular and $u, v \in \mathbb{R}^n$. Then

1. $\det(A + u v^T) = (1 + v^T A^{-1} u)\det A$ (the matrix determinant lemma);
2. $A + u v^T$ is nonsingular if and only if $1 + v^T A^{-1} u \ne 0$;
3. in that case its inverse is given by the formula above, and for each $b$ the solution of $(A + u v^T) x = b$ is
$$x = y - \frac{v^T y}{1 + v^T z}\, z, \qquad A y = b, \quad A z = u.$$

The same holds over $\mathbb{C}$ with $v^T$ replaced by $v^*$ if desired, and over any field.

## In plain words

Suppose you already know how to undo a matrix, and the matrix changes by the simplest possible amount: one column vector times one row vector, for instance a single entry or a single row. Then you do not need to start over. Undoing the new matrix is the old undoing plus a correction built from two quick solves, and one number tells whether the new matrix can be undone at all. If that number is zero, the change has made the matrix singular. If it is small, the answer is fragile.

## Proof

Let $z = A^{-1} u$, $w^T = v^T A^{-1}$ and $\delta = 1 + v^T A^{-1} u = 1 + v^T z$.

**Part 1.** Consider the bordered matrix $M = \begin{pmatrix} A & u \\ -v^T & 1 \end{pmatrix}$. Taking the [Schur complement](/schur-complement/) of $A$, $\det M = \det A \cdot (1 + v^T A^{-1} u)$. Taking the Schur complement of the $1 \times 1$ block $(1)$, $\det M = 1 \cdot \det(A - u \cdot 1^{-1} \cdot (-v^T)) = \det(A + u v^T)$. Equating the two gives part 1.

**Part 2.** Since $\det A \ne 0$, part 1 shows that $\det(A + u v^T) \ne 0$ exactly when $\delta \ne 0$.

**Part 3.** Assume $\delta \ne 0$ and let $X = A^{-1} - z w^T/\delta$. Then

$$(A + u v^T) X = I + u w^T - \frac{u w^T}{\delta} - \frac{u (v^T z) w^T}{\delta} = I + u w^T\left(1 - \frac{1 + v^T z}{\delta}\right) = I,$$

using $A z = u$, $A A^{-1} = I$ and $v^T A^{-1} = w^T$. A one-sided inverse of a square matrix is its inverse, so $X = (A + u v^T)^{-1}$. Applying $X$ to $b$ gives $X b = y - z (w^T b)/\delta$ with $y = A^{-1} b$, and $w^T b = v^T A^{-1} b = v^T y$. $\blacksquare$

## Consequences

**Solving with an updated matrix.** Given an [LUP decomposition](/lup-decomposition/) of $A$, part 3 costs two [LUP solves](/lup-solve/), $2(2n^2 - n)$ flops, plus two inner products and one vector update, about $4n^2$ flops in all. Several right sides with the same $u$ share $z$, so each further solve costs $2n^2 + 4n$. A sequence of $k$ updates can be handled by keeping the vectors $z_j$ and applying the formula recursively, at $O(k n^2 + k^2 n)$ cost, until refactoring is cheaper.

**A worked example.** Let $A = \begin{pmatrix} 2 & 1 \\ 1 & 3 \end{pmatrix}$, $u = e_1$, $v = e_2$, so that $A + u v^T = \begin{pmatrix} 2 & 2 \\ 1 & 3 \end{pmatrix}$ changes only the entry $(1, 2)$. Then $A^{-1} = \tfrac15 \begin{pmatrix} 3 & -1 \\ -1 & 2 \end{pmatrix}$, $z = A^{-1} e_1 = (\tfrac35, -\tfrac15)^T$, $w^T = e_2^T A^{-1} = (-\tfrac15, \tfrac25)$ and $\delta = 1 + z_2 = \tfrac45$. The formula gives

$$A^{-1} - \frac{z w^T}{\delta} = \frac15\begin{pmatrix} 3 & -1 \\ -1 & 2 \end{pmatrix} - \frac54 \cdot \frac{1}{25}\begin{pmatrix} -3 & 6 \\ 1 & -2 \end{pmatrix} = \begin{pmatrix} \tfrac34 & -\tfrac12 \\ -\tfrac14 & \tfrac12 \end{pmatrix},$$

which is the inverse of $\begin{pmatrix} 2 & 2 \\ 1 & 3 \end{pmatrix}$, and $\det = 5 \cdot \tfrac45 = 4$.

**Applications.**

- *Changing one entry, row or column.* $a_{ij} \mathrel{+}= \tau$ is $u = \tau e_i$, $v = e_j$; changing row $i$ by $r^T$ is $u = e_i$, $v = r$. This is the original use of Sherman and Morrison, and the basis of the product-form update in the simplex method.
- *Quasi-Newton methods.* Broyden's method updates an approximate Jacobian by rank one, and the formula updates its inverse directly; [BFGS](/bfgs/) applies it twice for its rank-two update.
- *Cyclic tridiagonal systems.* A periodic tridiagonal matrix is a tridiagonal matrix plus a rank-one corner correction, so two runs of the [Thomas algorithm](/thomas-algorithm/) and the formula solve it in $O(n)$.
- *Statistics.* Adding or deleting one observation in least squares changes $A^T A$ by $\pm a a^T$; leave-one-out residuals have the closed form $r_i/(1 - h_{ii})$ with $h_{ii}$ the leverage, by the same formula. Recursive least squares and the [Kalman filter](/kalman-filter/) update are rank-one or rank-$k$ instances.

**Numerical behavior.** The formula is exact, but its floating-point use inherits two sources of error: the solves with $A$, which are accurate to about $u\,\kappa(A)$, and the division by $\delta$. If $|\delta|$ is small compared with $|v^T z|$, the update suffers cancellation, and the computed $x$ can be inaccurate even when $A + u v^T$ is well conditioned; conversely, when $A$ is ill conditioned and the update cures it, the formula still pays for $\kappa(A)$. These are worst-case effects, not a proved instability for every input. A common safeguard is to monitor $|\delta|$ relative to $1 + |v^T z|$, to apply one step of [iterative refinement](/iterative-refinement/) with the true matrix, or to refactor.

## Tightness

- **The condition $\delta \ne 0$ cannot be dropped.** For $A = I$ and $u = -v = e_1$, $\delta = 1 - 1 = 0$ and $A + u v^T = I - e_1 e_1^T$ is singular.
- **The hypothesis that $A$ is nonsingular is needed for the formula, not for the conclusion.** $A = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}$ is singular, yet $A + e_2 e_2^T = I$ is not; the formula has no meaning here, because $A^{-1}$ does not exist.
- **Rank one is the limit of this form.** For a change of rank $k > 1$, the scalar $\delta$ becomes the $k \times k$ matrix $I + V^T A^{-1} U$ of the [Woodbury identity](/woodbury-identity/), which must be inverted.

## History

The formula for a change in one entry was published by Sherman and Morrison (an abstract in 1949 and the paper in 1950), and Bartlett (1951) gave the general rank-one form $u v^T$. Woodbury's 1950 report extended it to rank $k$. Hager (1989) traces earlier appearances, including work by Duncan (1944) and Guttman (1946), and surveys the applications.

## References
