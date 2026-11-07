---
title: The Thomas algorithm computes the solution of a tridiagonal system whose leading principal minors are nonzero
proves: [correctness, termination]
status: full
---

$A$ is tridiagonal of order $n$, with subdiagonal $a_2, \ldots, a_n$, diagonal $b_1, \ldots, b_n$ and superdiagonal $c_1, \ldots, c_{n-1}$. Let $A_k = A_{1:k,1:k}$ and $\delta_k = \det A_k$, with $\delta_0 = 1$. The loops have fixed lengths, so the algorithm stops; it stops early, at line L3 or L6, exactly when some pivot is zero.

**Lemma 1 (the pivots).** If $\delta_1, \ldots, \delta_{k-1}$ are nonzero, then lines L1 to L4 compute $u_1, \ldots, u_k$ with $u_i = \delta_i/\delta_{i-1}$ for $i \le k$.

*Proof.* Expanding $\det A_i$ along its last row gives the three-term recurrence $\delta_i = b_i \delta_{i-1} - a_i c_{i-1} \delta_{i-2}$ for $i \ge 2$, with $\delta_1 = b_1$. For $i = 1$, $u_1 = b_1 = \delta_1/\delta_0$. For $i \ge 2$, assume $u_{i-1} = \delta_{i-1}/\delta_{i-2}$, which is nonzero. Line L3 gives $l_i = a_i/u_{i-1}$ and line L4 gives

$$u_i = b_i - \frac{a_i c_{i-1}}{u_{i-1}} = b_i - \frac{a_i c_{i-1} \delta_{i-2}}{\delta_{i-1}} = \frac{b_i \delta_{i-1} - a_i c_{i-1}\delta_{i-2}}{\delta_{i-1}} = \frac{\delta_i}{\delta_{i-1}}. \qquad \square$$

So no division by zero occurs if and only if $\delta_1, \ldots, \delta_{n-1}$ are nonzero, and $u_n \ne 0$ if and only if moreover $\det A = \delta_n \ne 0$.

**Lemma 2 (the factorization).** If all pivots are nonzero, then $A = L U$, where $L$ is unit lower bidiagonal with $L_{i,i-1} = l_i$ and $U$ is upper bidiagonal with $U_{ii} = u_i$ and $U_{i,i+1} = c_i$.

*Proof.* The product $L U$ is tridiagonal. Its entry $(1,1)$ is $u_1 = b_1$. For $i \ge 2$, row $i$ of $L$ has $l_i$ in column $i - 1$ and $1$ in column $i$, so $(L U)_{i,i-1} = l_i u_{i-1} = a_i$, $(L U)_{ii} = l_i c_{i-1} + u_i = b_i$ by line L4, and $(L U)_{i,i+1} = c_i$. $\square$

**Lemma 3 (the sweeps).** Line L5 computes the solution $y$ of $L y = d$, and lines L6 and L7 compute the solution $x$ of $U x = y$.

*Proof.* Row $i$ of $L y = d$ is $l_i y_{i-1} + y_i = d_i$ (with no first term for $i = 1$), which is lines L1 and L5. Row $i$ of $U x = y$ is $u_i x_i + c_i x_{i+1} = y_i$ (with no second term for $i = n$). Going from $i = n$ down to $1$, $x_{i+1}$ is known when $x_i$ is computed, and lines L6 and L7 solve row $i$ for $x_i$, which is possible because $u_i \ne 0$. $\square$

**Theorem.** If $\delta_1, \ldots, \delta_n$ are nonzero, THOMAS returns the unique solution of $A x = d$; otherwise it stops at the first zero pivot.

*Proof.* By Lemmas 2 and 3, $A x = L U x = L y = d$, and $A$ is nonsingular because $\delta_n \ne 0$. The second claim is Lemma 1. $\blacksquare$

**Diagonal dominance gives nonzero pivots.** Suppose $A$ is strictly diagonally dominant by rows: $|b_i| > |a_i| + |c_i|$ for all $i$, with $a_1 = c_n = 0$. Then $|u_i| > |c_i|$ for all $i$, so no pivot is zero. Indeed $|u_1| = |b_1| > |c_1|$. If $|u_{i-1}| > |c_{i-1}|$, then $|l_i c_{i-1}| = |a_i|\,|c_{i-1}|/|u_{i-1}| \le |a_i|$, so $|u_i| \ge |b_i| - |l_i c_{i-1}| \ge |b_i| - |a_i| > |c_i|$. The same induction shows $|l_i| \le |a_i|/|u_{i-1}|$ stays bounded, and that the pivots satisfy $|u_i| \le |b_i| + |a_i|$.

**Floating point.** Each computed quantity is one operation or one fused pair: $\hat l_i = (a_i/\hat u_{i-1})(1 + \epsilon_1)$, $\hat u_i = (b_i - \hat l_i c_{i-1}(1 + \epsilon_2))(1 + \epsilon_3)$, and similarly for $\hat y_i$ and $\hat x_i$, with $|\epsilon_j| \le u$. Moving these factors onto the entries of $\hat L$ and $\hat U$ gives the bound $|\Delta A| \le f(u)|\hat L||\hat U|$ with $f(u) = 4u + 3u^2 + u^3$ stated on the page (Higham, Section 9.6). The tests check the resulting residual inequality $|d - A\hat x| \le f(u)\,|\hat L|\,|\hat U|\,|\hat x|$ exactly.
