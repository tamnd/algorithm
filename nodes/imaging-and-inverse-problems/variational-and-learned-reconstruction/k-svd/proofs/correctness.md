---
title: The K-SVD atom update is the best rank one fit on the signals that use the atom, and with an exact sparse coder the objective never increases
proves: [correctness]
status: full
---

**Setting.** $Y$ is a real $n \times N$ matrix whose columns $y_i$ are the signals. A dictionary $D$ is $n \times K$ with columns $d_k$ of norm 1. A code matrix $X$ is $K \times N$, with columns $x_i$ that have at most $s$ nonzero entries; $x^k$ denotes row $k$ of $X$. The objective is

$$F(D, X) = \|Y - DX\|_F^2 = \sum_i \|y_i - Dx_i\|^2.$$

One K-SVD iteration first replaces every $x_i$ by the output of a sparse coder, and then, for $k = 1, \dots, K$ in turn, updates $d_k$ and $x^k$ as follows. Let $\omega = \{i : x^k_i \ne 0\}$. If $\omega$ is empty, the atom may be replaced by any unit vector (the implementation uses the normalized residual of the worst represented signal). Otherwise let $E = Y - \sum_{j \ne k} d_jx^j$, let $E^R$ be the columns of $E$ with index in $\omega$, and let $\sigma_1, u_1, v_1$ be its largest singular value and a pair of singular vectors. The update sets $d_k = u_1$, $x^k_i = \sigma_1(v_1)_i$ for $i \in \omega$ (in the order of $\omega$), and leaves $x^k_i = 0$ for $i \notin \omega$.

## Lemma 1: the best rank one fit

For a real $n \times p$ matrix $E$ with largest singular value $\sigma_1$,

$$\min_{\|d\| = 1,\; w \in \mathbb{R}^p}\|E - dw^T\|_F^2 = \|E\|_F^2 - \sigma_1^2,$$

and the minimum is reached at $d = u_1$, $w = \sigma_1v_1$.

*Proof.* Fix a unit vector $d$. The function $w \mapsto \|E - dw^T\|_F^2 = \|E\|_F^2 - 2w^TE^Td + \|w\|^2$ is a convex quadratic with minimizer $w = E^Td$ and minimum $\|E\|_F^2 - \|E^Td\|^2$. Now $\|E^Td\|^2 = d^TEE^Td$, and its maximum over unit vectors $d$ is the largest eigenvalue of the symmetric matrix $EE^T$ (the Rayleigh quotient), which is $\sigma_1^2$, reached at $d = u_1$. Then $w = E^Tu_1 = \sigma_1v_1$. $\square$

## Lemma 2: the atom update does not increase the objective

Let $(D, X)$ be any pair whose codes have at most $s$ nonzeros per column, and let $(D', X')$ be the result of the update of atom $k$. Then $F(D', X') \le F(D, X)$, every column of $X'$ has at most $s$ nonzero entries, and $\|d'_k\| = 1$.

*Proof.* If $\omega$ is empty, then $x^k = 0$, so $d_k$ does not appear in $DX$, and changing it does not change $F$. Otherwise write $DX = \sum_{j \ne k}d_jx^j + d_kx^k$, so that $F(D, X) = \|E - d_kx^k\|_F^2$, and only $d_k$ and $x^k$ change. Split the columns into $\omega$ and its complement. On the complement, $x^k_i = 0$ before and after, so those columns of $E - d_kx^k$ do not change. On $\omega$, the columns form $E^R - d_k(x^k_\omega)^T$, a fit of $E^R$ by a unit vector times a row. By Lemma 1, the new pair $(u_1, \sigma_1v_1)$ gives the smallest possible value, $\|E^R\|_F^2 - \sigma_1^2$, which is at most the value of the old pair $(d_k, x^k_\omega)$. So $F$ does not increase.

The new row $x^k$ is zero outside $\omega$, so the support of each column $x_i$ either stays the same or loses entry $k$ (when $(v_1)_i = 0$). It never gains an entry, so each column still has at most $s$ nonzeros. Finally $\|u_1\| = 1$. $\square$

The restriction to $\omega$ is what keeps the sparsity: a rank one fit of the full $E$ would in general make $x^k$ dense.

## Theorem: monotone objective with an exact sparse coder

Assume the coder is exact, that is, for each $i$ it returns a minimizer of $\|y_i - Dx\|^2$ over all $x$ with at most $s$ nonzero entries. Let $F_j$ be the objective at the end of iteration $j$, and $G_j$ the objective after its coding step. Then

$$G_1 \ge F_1 \ge G_2 \ge F_2 \ge \dots \ge 0,$$

so the sequence of objective values converges.

*Proof.* At the start of iteration $j + 1$, the codes $X$ from iteration $j$ have at most $s$ nonzeros per column (Lemma 2). They are feasible for the coding problem of each column with the current $D$, so the exact coder returns a column with residual at most $\|y_i - Dx_i\|^2$. Summing over $i$ gives $G_{j+1} \le F_j$. Within an iteration, the $K$ atom updates each do not increase $F$ (Lemma 2), so $F_j \le G_j$. All values are nonnegative. A nonincreasing sequence that is bounded below converges. $\square$

The implementation's exact coder tries every support of size $\min(s, K)$ and solves least squares on it. This is exact: a support with fewer than $s$ atoms is contained in one with exactly $s$ atoms, and least squares on a larger set of columns has a residual that is not larger.

## What the theorem does not say

- It is about the values $F_j$, not about the dictionaries. The iterates need not converge, and the limit need not be a global minimizer; finding the best dictionary is NP-hard in general (Tillmann, 2015).
- It needs an exact coder. Exact sparse coding is itself NP-hard, so practical K-SVD uses orthogonal matching pursuit or another greedy coder. Then the coding step can increase the objective, and the sequence is not monotone; the page reports such increases measured on planted problems. The test file checks monotonicity only with the brute force coder on a small problem, and checks the atom update step alone with OMP codes.
- With a coder that has an error target instead of a sparsity target (code each signal until $\|y_i - Dx_i\| \le \epsilon$), the objective is a different one, and the argument above applies only to the atom update step.
