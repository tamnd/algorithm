---
title: Every eigenvector matrix built from the subspaces S_j gives a real gain with the wanted poles, and method 0 does not decrease the determinant
proves: [correctness]
status: full
---

Let $A \in \mathbb{R}^{n \times n}$ and $B \in \mathbb{R}^{n \times m}$ with rank $m$. Line L1 gives an orthogonal matrix $[U_0, U_1]$ and an invertible $Z \in \mathbb{R}^{m \times m}$ with $B = U_0 Z$; the columns of $U_0$ span the range of $B$, and $U_1$ has $n - m$ columns. For a number $\lambda$, let $\mathcal{S}(\lambda) = \{x \in \mathbb{C}^n : U_1^T (A - \lambda I) x = 0\}$. Line L2 computes an orthonormal basis $S_j$ of $\mathcal{S}(\lambda_j)$. Write $X = [x_1, \dots, x_n]$ and $\Lambda = \operatorname{diag}(\lambda_1, \dots, \lambda_n)$.

## Lemma 1: which eigenvector matrices are possible

Let $X$ be invertible. There is a $K \in \mathbb{C}^{m \times n}$ with $(A - BK) X = X \Lambda$ if and only if $x_j \in \mathcal{S}(\lambda_j)$ for every $j$. In that case $K$ is unique and equals $Z^{-1} U_0^T (A - X \Lambda X^{-1})$.

*Proof.* Let $M = X \Lambda X^{-1}$. The equation $(A - BK)X = X\Lambda$ is the same as $BK = A - M$, because $X$ is invertible. Since $[U_0, U_1]$ is orthogonal, this equation holds if and only if it holds after multiplication on the left by $[U_0, U_1]^T$. With $U_0^T B = Z$ and $U_1^T B = 0$, it splits into

$$Z K = U_0^T (A - M), \qquad 0 = U_1^T (A - M).$$

The first equation has the unique solution $K = Z^{-1} U_0^T (A - M)$. The second equation holds if and only if $U_1^T (A - M) X = 0$, because $X$ is invertible. Its column $j$ is $U_1^T (A x_j - \lambda_j x_j) = 0$, that is, $x_j \in \mathcal{S}(\lambda_j)$. $\square$

## Lemma 2: the dimension of the subspaces

$\operatorname{rank} [A - \lambda I, B] = m + \operatorname{rank} U_1^T (A - \lambda I)$ for every $\lambda \in \mathbb{C}$. So if $(A, B)$ is controllable, every $\mathcal{S}(\lambda)$ has dimension $m$.

*Proof.* Multiplication on the left by the invertible matrix $[U_0, U_1]^T$ does not change the rank, and gives

$$\begin{bmatrix} U_0^T (A - \lambda I) & Z \\ U_1^T (A - \lambda I) & 0 \end{bmatrix}.$$

Because $Z$ is invertible, column operations with the last $m$ columns remove the block $U_0^T (A - \lambda I)$ without changing the rank. The result is block diagonal up to the order of the blocks, with rank $m + \operatorname{rank} U_1^T(A - \lambda I)$. By the [Popov-Belevitch-Hautus test](/popov-belevitch-hautus-test/), $(A, B)$ is controllable if and only if the left side is $n$ for every $\lambda$. Then $U_1^T(A - \lambda I)$, an $(n - m) \times n$ matrix, has rank $n - m$, and its null space $\mathcal{S}(\lambda)$ has dimension $m$. $\square$

## Lemma 3: the update does not decrease the determinant

Fix all columns of $X$ except column $j$. Let $X_j$ be the matrix of the other $n - 1$ columns, assume they are independent, and let $y_j$ be a unit vector with $y_j^H x_i = 0$ for all $i \ne j$ (line L5). Among the unit vectors $x \in \mathcal{S}(\lambda_j)$, the vector $x^\ast = P y_j / \|P y_j\|$, where $P = S_j S_j^H$ is the orthogonal projector onto $\mathcal{S}(\lambda_j)$, maximizes $|\det X|$, if $P y_j \ne 0$.

*Proof.* Write any $x$ as $x = (y_j^H x) y_j + w$, with $w$ in the span of the other columns, since $y_j$ and these columns together span $\mathbb{C}^n$ and $y_j$ is orthogonal to them. The determinant is linear in column $j$ and vanishes when column $j$ is a combination of the other columns, so $\det X = (y_j^H x) \det X^{(y)}$, where $X^{(y)}$ is $X$ with column $j$ replaced by $y_j$. The factor $\det X^{(y)}$ does not depend on $x$. For a unit vector $x \in \mathcal{S}(\lambda_j)$, $x = Px$, so $y_j^H x = y_j^H P x = (P y_j)^H x$, and by the Cauchy-Schwarz inequality $|y_j^H x| \le \|P y_j\|$, with equality at $x = x^\ast$. $\square$

The old column $x_j$ is one of the admissible vectors, so the update of line L6 never decreases $|\det X|$ when only one column changes. This is the case for every real $\lambda_j$. For a complex pair the code changes two columns, $x_j$ and its conjugate, and this argument does not apply. Hadamard's inequality gives $|\det X| \le \prod_i \|x_i\| = 1$, with equality if and only if the columns are orthonormal, so for real poles the values of $|\det X|$ form a bounded nondecreasing sequence and converge. This proves nothing about the limit of $X$ itself; the code only uses it as a heuristic and keeps the matrix with the smallest $\kappa_2(X)$ that it has seen.

## Lemma 4: the gain is real

Assume that the poles are closed under conjugation, that $U_0, U_1, Z$ are real, and that for every complex pair $\lambda_k = \bar\lambda_j$ the code sets $x_k = \bar x_j$. Then $X \Lambda X^{-1}$ and $K$ are real.

*Proof.* Let $\Pi$ be the permutation matrix that swaps the columns of each complex pair and fixes the others. Then $\bar X = X \Pi$ and $\bar\Lambda = \Pi \Lambda \Pi$, with $\Pi^{-1} = \Pi$. So

$$\overline{X \Lambda X^{-1}} = X \Pi\, \Pi \Lambda \Pi\, \Pi^{-1} X^{-1} = X \Lambda X^{-1}.$$

Then $K = Z^{-1} U_0^T (A - X\Lambda X^{-1})$ is a product of real matrices. Also $\bar x_j \in \mathcal{S}(\bar\lambda_j)$ whenever $x_j \in \mathcal{S}(\lambda_j)$, because $U_1$ and $A$ are real; so the conjugate columns satisfy the condition of Lemma 1. $\square$

## Theorem

If $(A, B)$ is controllable, the poles are distinct and closed under conjugation, and the final $X$ is invertible, then the gain $K$ of line L8 is real and $(A - BK) X = X\Lambda$. So the eigenvalues of $A - BK$ are exactly $\lambda_1, \dots, \lambda_n$, with the columns of $X$ as eigenvectors.

*Proof.* Every column that the code ever stores is a vector of the form $S_j c$, from line L3 or line L6, or the conjugate of one; so $x_j \in \mathcal{S}(\lambda_j)$ for all $j$. Lemma 1 gives $(A - BK)X = X\Lambda$ for the gain of line L8, and Lemma 4 shows that it is real. An $n \times n$ matrix with $n$ independent eigenvectors for the eigenvalues $\lambda_j$ has exactly these eigenvalues. $\square$

The code raises an error if the final $\kappa_2(X)$ exceeds $10^{12}$, so it never returns a gain from a numerically singular $X$. If $(A, B)$ is not controllable and an uncontrollable eigenvalue of $A$ is not among the $\lambda_j$, no invertible $X$ with $x_j \in \mathcal{S}(\lambda_j)$ exists: by Lemma 1 it would give a gain that moves an uncontrollable eigenvalue, which the [pole placement theorem](/pole-placement-theorem/) excludes. Every $X$ the code builds is then singular, and the test reports it, up to rounding error. In floating point all equalities above hold up to rounding error; the tests check the residual $\|(A - BK) X - X \Lambda\|$ and the characteristic polynomial of $A - BK$.
