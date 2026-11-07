---
title: The normal equations method returns the least squares solution, and its forward error is of order u kappa_2(A)^2
proves: [correctness, termination]
status: full
---

$A \in \mathbb{R}^{m \times n}$ has $m \ge n$ and full column rank, and $b \in \mathbb{R}^m$. Every loop of the algorithm has a fixed length, so it stops.

## Exact arithmetic

**Claim 1.** $x$ minimizes $\|b - A x\|_2$ if and only if $A^T A x = A^T b$, and the minimizer is unique.

*Proof.* Let $r = b - A x$. For each $y \in \mathbb{R}^n$,

$$\|b - A(x + y)\|_2^2 = (r - A y)^T (r - A y) = \|r\|_2^2 - 2 y^T A^T r + \|A y\|_2^2.$$

If $A^T r = 0$, the right side is $\|r\|_2^2 + \|A y\|_2^2 \ge \|r\|_2^2$, with equality only when $A y = 0$, that is $y = 0$ because the columns of $A$ are independent. So $x$ is the unique minimizer. If $A^T r \ne 0$, take $y = t A^T r$ with $t > 0$ small: the right side is $\|r\|_2^2 - 2t\|A^T r\|_2^2 + t^2 \|A A^T r\|_2^2 < \|r\|_2^2$, so $x$ is not a minimizer. $\square$

**Claim 2.** $C = A^T A$ is symmetric positive definite, so line L3 succeeds and returns an upper triangular $R$ with positive diagonal and $R^T R = C$.

*Proof.* $C^T = A^T A = C$, and $v^T C v = \|A v\|_2^2 > 0$ for $v \ne 0$. The column Cholesky algorithm computes, for $j = 1, \ldots, n$, $r_{jj} = (c_{jj} - \sum_{k<j} r_{kj}^2)^{1/2}$ and $r_{ji} = (c_{ji} - \sum_{k<j} r_{kj} r_{ki})/r_{jj}$ for $i > j$. By induction on $j$, the first $j - 1$ rows of $R$ satisfy the first $j - 1$ rows of $R^T R = C$, and the pivot $c_{jj} - \sum_{k<j} r_{kj}^2$ equals the Schur complement $s_j$ of the leading $(j-1) \times (j-1)$ block in the leading $j \times j$ block of $C$. That block is positive definite, so $\det$ of it is the product of the positive leading pivots times $s_j$, and $s_j > 0$. So no pivot is $\le 0$ and the square roots are real and positive. $\square$

**Theorem.** NORMAL-EQUATIONS returns the least squares solution.

*Proof.* Lines L4 and L5 solve $R^T y = d$ and $R x = y$, which are possible because the diagonal of $R$ is positive. Then $C x = R^T R x = R^T y = d$, so $A^T A x = A^T b$, and by Claim 1 $x$ is the unique minimizer. $\blacksquare$

## Floating point

Assume the standard model with unit roundoff $u$ and $m u < 1$. Write $\| \cdot \|$ for the 2-norm.

**Step 1: forming $C$ and $d$.** Each $\hat c_{ij}$ is an inner product of length $m$, so $|\hat c_{ij} - c_{ij}| \le \gamma_m \sum_k |a_{ki}||a_{kj}|$ (Higham, Section 3.1). Hence $\hat C = C + E_1$ with $|E_1| \le \gamma_m |A|^T |A|$, and in the same way $\hat d = d + f$ with $|f| \le \gamma_m |A|^T |b|$. For a nonnegative matrix the 2-norm is monotone in the entries, and $\| |A| \| \le \|A\|_F \le \sqrt n \|A\|$, so

$$\|E_1\| \le n \gamma_m \|A\|^2, \qquad \|f\| \le \sqrt n \gamma_m \|A\|\,\|b\|.$$

**Step 2: the Cholesky solve.** If the Cholesky factorization of $\hat C$ runs to completion, the computed $\hat x$ satisfies $(\hat C + E_2)\hat x = \hat d$ with $|E_2| \le \gamma_{3n+1} |\hat R^T||\hat R|$ (Higham, Chapter 10). Since $\| |\hat R^T||\hat R| \| \le n \|\hat R\|^2$ and $\|\hat R\|^2 = \|\hat R^T \hat R\| \le \|\hat C\|(1 + O(n u))$, this gives $\|E_2\| \le c_n u \|C\| + O(u^2)$ with $c_n = O(n^2)$.

**Step 3: perturbation.** So $(C + E)\hat x = d + f$ with $E = E_1 + E_2$, $\|E\| \le \epsilon_1 \|A\|^2$, $\epsilon_1 = (n m + c_n) u + O(u^2)$, using $\|C\| = \|A\|^2$. Subtracting $C x = d$ gives $C(\hat x - x) = f - E\hat x$, and $\|C^{-1}\| = 1/\sigma_n^2$, so

$$\|\hat x - x\| \le \frac{1}{\sigma_n^2}\bigl(\epsilon_1 \|A\|^2 \|\hat x\| + \sqrt n \gamma_m \|A\|\,\|b\|\bigr), \qquad \frac{\|\hat x - x\|}{\|\hat x\|} \le \kappa_2(A)^2 \left(\epsilon_1 + \sqrt n \gamma_m \frac{\|b\|}{\|A\|\,\|\hat x\|}\right).$$

The bound is in terms of $\|\hat x\|$; if the right side is below $1/2$, then $\|\hat x\| \le 2\|x\|$ and the same bound holds relative to $\|x\|$ with an extra factor $2$. This is the bound stated on the page, with $c_{m,n} = O(m n + n^2)$. $\blacksquare$

**Termination of Cholesky.** If $\hat C$ is positive definite, the column algorithm completes in floating point whenever $c'_n u\, \kappa_2(\hat C) < 1$ for a modest $c'_n$ (Higham, Chapter 10). When $\kappa_2(A)^2 u$ is of order one this can fail, and the implementation then raises `NotFullRank` instead of returning a value.

**What the tests check.** The tests compare $\hat x$ with the exact rational least squares solution and assert $\|\hat x - x\|_\infty/\|x\|_\infty \le 4(m+n) n u\, \kappa_1(A^T A)(1 + \|b\|_1/(\|A\|_1\|x\|_\infty))$, which has the form of Step 3 with the 1-norm quantities, computed exactly, in place of the 2-norm ones; $\kappa_2(A)^2 = \kappa_2(A^T A) \le \kappa_1(A^T A)$ for the symmetric matrix $A^T A$.
