---
title: Cholesky's algorithm finds the factor exactly when A is positive definite, and is backward stable
proves: [correctness, termination]
status: full
---

Notation: $A$ is a real symmetric $n \times n$ matrix, $A_j$ is its leading $j \times j$ block, $R_j$ is the leading $j \times j$ block of the computed $R$, $u$ is the unit roundoff and $\gamma_m = m u / (1 - m u)$. The algorithm stops: line L1 runs $n$ times and each inner loop has a fixed length.

## Exact arithmetic

**Invariant $I(j)$.** After the pass of line L1 for $j$: for all $1 \le k \le j$ and $k \le i \le n$,
$$a_{ki} = \sum_{l=1}^{k} r_{lk} r_{li}, \qquad r_{kk} > 0.$$

*Initialization.* $I(0)$ is empty and true.

*Maintenance.* Assume $I(j - 1)$ and that line L3 does not return. Line L2 gives $s = a_{jj} - \sum_{k<j} r_{kj}^2 > 0$, and line L4 gives $r_{jj} = \sqrt s > 0$, so $a_{jj} = \sum_{k \le j} r_{kj}^2$. For $i > j$, line L6 gives $r_{jj} r_{ji} = a_{ji} - \sum_{k<j} r_{kj} r_{ki}$, so $a_{ji} = \sum_{k \le j} r_{kj} r_{ki}$. With $I(j - 1)$ this is $I(j)$.

*At the end.* $I(n)$ says $(R^T R)_{ki} = \sum_{l \le \min(k, i)} r_{lk} r_{li} = a_{ki}$ for $k \le i$, since $r_{lk} = 0$ for $l > k$. Both sides are symmetric, so $R^T R = A$.

**Lemma 1.** Assume $I(j - 1)$. Then the value $s$ of line L2 at step $j$ is $s = \det A_j / \det(R_{j-1})^2$ (with $\det R_0 = 1$), and $\det R_{j-1} > 0$.

*Proof.* Let $c = (r_{1j}, \ldots, r_{j-1, j})^T$. By $I(j - 1)$, $A_j = \begin{pmatrix} R_{j-1}^T R_{j-1} & R_{j-1}^T c \\ c^T R_{j-1} & a_{jj} \end{pmatrix}$. Multiply out to check that
$$A_j = \begin{pmatrix} R_{j-1}^T & 0 \\ c^T & 1 \end{pmatrix} \begin{pmatrix} R_{j-1} & c \\ 0 & s \end{pmatrix}, \qquad s = a_{jj} - c^T c:$$
the block $(2, 2)$ of the product is $c^T c + s = a_{jj}$, and the other blocks are those of $A_j$. Both factors are triangular, so $\det A_j = \det(R_{j-1}) \cdot \det(R_{j-1}) \cdot s$. $R_{j-1}$ is triangular with positive diagonal, so $\det R_{j-1} > 0$. $\square$

**Theorem 2.** (a) If $A$ is positive definite, the algorithm returns $R$ upper triangular with positive diagonal and $R^T R = A$. (b) If it returns NOT-POSITIVE-DEFINITE, then $A$ is not positive definite. (c) The factor is unique, and $A = R^T R$ with such an $R$ implies that $A$ is positive definite.

*Proof.* (a) For $z \in \mathbb{R}^j$, $z \ne 0$, put $\tilde z = (z, 0, \ldots, 0) \in \mathbb{R}^n$. Then $z^T A_j z = \tilde z^T A \tilde z > 0$, so $A_j$ is positive definite, its eigenvalues are positive and $\det A_j > 0$. By Lemma 1 and induction on $j$, $s > 0$ at each step, so line L3 never returns, and $I(n)$ gives $R^T R = A$.

(b) If line L3 returns at step $j$, then $s \le 0$, and Lemma 1 gives $\det A_j \le 0$. By the argument of (a), $A$ is then not positive definite.

(c) Let $S$ be upper triangular with positive diagonal and $S^T S = A$. Entry $(j, i)$, $i \ge j$, of $S^T S = A$ reads $a_{ji} = \sum_{k \le j} s_{kj} s_{ki}$. By induction on $j$, rows $1, \ldots, j - 1$ of $S$ and $R$ agree; then $s_{jj}^2 = a_{jj} - \sum_{k<j} s_{kj}^2$ is the value of line L2, and $s_{jj} > 0$ forces $s_{jj} = r_{jj}$; the entries $s_{ji}$, $i > j$, then solve the same equation as line L6. So $S = R$. Finally, if $A = R^T R$ with $R$ nonsingular, then $z^T A z = \|R z\|_2^2 > 0$ for $z \ne 0$. $\square$

## Floating point

Assume the [standard model](/floating-point-model/) $\mathrm{fl}(a \circ b) = (a \circ b)(1 + \delta)$, $\mathrm{fl}(\sqrt a) = \sqrt a (1 + \delta)$, $|\delta| \le u$, no underflow or overflow, and $(3n + 1) u < 1$. We use two facts: a product of $m$ factors $(1 + \delta_k)^{\pm 1}$ is $1 + \theta$ with $|\theta| \le \gamma_m$ (Higham, Lemma 3.1; proved on the [back substitution](/back-substitution/) proof page), and $\gamma_a + \gamma_b + \gamma_a \gamma_b \le \gamma_{a+b}$ (Higham, Lemma 3.3).

**Theorem 3.** If the algorithm runs to completion, then $\hat R^T \hat R = A + \Delta A$ with $|\Delta A| \le \gamma_{n+1} |\hat R^T| \, |\hat R|$.

*Proof.* Fix $j$. *Off the diagonal* ($i > j$): line L6 computes $m = j - 1$ products, $m$ subtractions in order and one division. As in the proof of Theorem 3 for back substitution, unrolling the roundings and dividing by the factors of the subtractions gives
$$\hat r_{jj} \hat r_{ji} (1 + \theta_0) + \sum_{k<j} \hat r_{kj} \hat r_{ki} (1 + \theta_k) = a_{ji},$$
with $|\theta_0| \le \gamma_{m+1} = \gamma_j$ and $|\theta_k| \le \gamma_m$. So $|a_{ji} - \sum_{k \le j} \hat r_{kj} \hat r_{ki}| \le \gamma_j \sum_{k \le j} |\hat r_{kj}| |\hat r_{ki}|$.

*On the diagonal*: line L2 gives $\hat s (1 + \theta_0') + \sum_{k<j} \hat r_{kj}^2 (1 + \theta_k') = a_{jj}$ with $m$ factors in $\theta_0'$ and at most $m$ in each $\theta_k'$. Line L4 gives $\hat r_{jj} = \sqrt{\hat s} (1 + \delta)$, so $\hat s = \hat r_{jj}^2 (1 + \delta)^{-2}$. Then the factor of $\hat r_{jj}^2$ is a product of $m + 2 = j + 1$ terms, and $|a_{jj} - \sum_{k \le j} \hat r_{kj}^2| \le \gamma_{j+1} \sum_{k \le j} \hat r_{kj}^2$.

Set $\Delta A = \hat R^T \hat R - A$; it is symmetric, its entry $(j, i)$, $i \ge j$, is bounded as above, and $\gamma_j \le \gamma_{j+1} \le \gamma_{n+1}$. $\square$

**Theorem 4.** The solution computed by CHOLESKY-SOLVE satisfies $(A + \Delta A')\hat x = b$ with $|\Delta A'| \le \gamma_{3n+1} |\hat R^T| \, |\hat R|$.

*Proof.* By the backward error of [substitution](/back-substitution/), the computed $\hat y$ and $\hat x$ satisfy $(\hat R^T + E_1)\hat y = b$ and $(\hat R + E_2)\hat x = \hat y$ with $|E_1| \le \gamma_n |\hat R^T|$ and $|E_2| \le \gamma_n |\hat R|$. So $(\hat R^T + E_1)(\hat R + E_2)\hat x = b$, and
$$\Delta A' = \Delta A + E_1 \hat R + \hat R^T E_2 + E_1 E_2, \qquad |\Delta A'| \le (\gamma_{n+1} + 2 \gamma_n + \gamma_n^2) |\hat R^T| \, |\hat R|.$$
By the second fact, $2 \gamma_n + \gamma_n^2 \le \gamma_{2n}$ and $\gamma_{n+1} + \gamma_{2n} \le \gamma_{3n+1}$. $\blacksquare$
