---
title: LUP-SOLVE solves A x = b, and its result has a componentwise backward error of at most γ_3n P^T |L||U|
proves: [correctness, termination]
status: full
---

$A$ is a nonsingular $n \times n$ matrix with $P A = L U$, $L$ unit lower triangular, $U$ upper triangular with nonzero diagonal, and row $i$ of $P A$ equal to row $\pi_i$ of $A$, so $(P b)_i = b_{\pi_i}$. The algorithm stops, because each loop has a fixed length.

## Exact arithmetic

**Claim 1.** After the loop of line L1, $L y = P b$.

*Proof.* By induction on $i$ we show: after iteration $i$, the first $i$ equations of $L y = P b$ hold, that is $\sum_{j \le k} l_{kj} y_j = b_{\pi_k}$ for $k \le i$, and $y_1, \ldots, y_i$ do not change later. The case $i = 0$ is empty. In iteration $i$, line L2 sets $y_i = b_{\pi_i} - \sum_{j < i} l_{ij} y_j$, which is equation $i$ because $l_{ii} = 1$, and it writes no other entry. $\square$

**Claim 2.** After the loop of line L3, $U x = y$.

*Proof.* By induction on the number $n - i + 1$ of passes: after the pass for $i$, equations $k = i, \ldots, n$ of $U x = y$ hold, that is $\sum_{j \ge k} u_{kj} x_j = y_k$. In the pass for $i$, the values $x_{i+1}, \ldots, x_n$ are fixed, and line L4 sets $x_i = (y_i - \sum_{j > i} u_{ij} x_j)/u_{ii}$, which is defined because $u_{ii} \ne 0$ and is exactly equation $i$. $\square$

**Theorem.** LUP-SOLVE returns the solution of $A x = b$.

*Proof.* By the claims, $P A x = L U x = L y = P b$. $P$ is a permutation matrix, so it is invertible, and $A x = b$. Since $A$ is nonsingular, this $x$ is the unique solution. $\blacksquare$

## Floating point

Assume the standard model, $|\delta| \le u$ for each operation, and $3 n u < 1$. Let $\hat L$, $\hat U$ be the factors computed by the LUP decomposition, with the permutation $P$ that it chose, so that

$$\hat L \hat U = P A + \Delta A_1, \qquad |\Delta A_1| \le \gamma_n |\hat L|\,|\hat U| \tag{1}$$

(Higham, Theorem 9.3; the proof is on the page of LUP decomposition).

**Step 1: the substitutions.** Line L2 evaluates $y_i = c - \sum_{j<i} a_j b_j$ with $c = b_{\pi_i}$; line L4 evaluates the same kind of expression and divides it by $u_{ii}$. By Higham, Lemma 8.4, the computed value of $(c - \sum_{j=1}^{k-1} a_j b_j)/b_k$ satisfies $b_k \hat y (1 + \theta_k) = c - \sum_{j=1}^{k-1} a_j b_j (1 + \theta_j)$ with each $|\theta_j| \le \gamma_k$, in any order of the sum. Moving each factor $1 + \theta$ onto the matrix entry gives, for the whole forward and back substitution,

$$(\hat L + \Delta L)\hat y = P b, \quad |\Delta L| \le \gamma_n |\hat L|, \qquad (\hat U + \Delta U)\hat x = \hat y, \quad |\Delta U| \le \gamma_n |\hat U|. \tag{2}$$

This is Higham, Theorem 8.5. The permutation of $b$ is exact.

**Step 2: combine.** From (2),

$$P b = (\hat L + \Delta L)(\hat U + \Delta U)\hat x = (\hat L \hat U + \Delta L\, \hat U + \hat L\, \Delta U + \Delta L\, \Delta U)\hat x.$$

Insert (1): $P b = (P A + E)\hat x$ with $E = \Delta A_1 + \Delta L\, \hat U + \hat L\, \Delta U + \Delta L\, \Delta U$. Each term is bounded entry by entry:

$$|E| \le \gamma_n |\hat L||\hat U| + \gamma_n |\hat L||\hat U| + \gamma_n |\hat L||\hat U| + \gamma_n^2 |\hat L||\hat U| = (3\gamma_n + \gamma_n^2)\,|\hat L|\,|\hat U|.$$

**Step 3: the constant.** For $j, k \ge 1$ with $(j + k) u < 1$, $\gamma_j + \gamma_k + \gamma_j \gamma_k \le \gamma_{j+k}$ (Higham, Lemma 3.3). With $j = k = n$ it gives $2\gamma_n + \gamma_n^2 \le \gamma_{2n}$, and with $j = 2n$, $k = n$ it gives $\gamma_{2n} + \gamma_n \le \gamma_{3n}$. So $3\gamma_n + \gamma_n^2 = (2\gamma_n + \gamma_n^2) + \gamma_n \le \gamma_{2n} + \gamma_n \le \gamma_{3n}$.

**Step 4: undo the permutation.** Multiply $P b = (P A + E)\hat x$ by $P^T = P^{-1}$: $b = (A + \Delta A)\hat x$ with $\Delta A = P^T E$, and $|\Delta A| = P^T |E| \le \gamma_{3n} P^T |\hat L|\,|\hat U|$, because a permutation only moves entries. $\blacksquare$

**Residual form.** The theorem says $r = b - A \hat x = \Delta A\, \hat x$, so $|P r| \le \gamma_{3n} |\hat L|\,|\hat U|\,|\hat x|$ entry by entry. The tests of the implementation check this inequality in exact rational arithmetic for each computed solution.
