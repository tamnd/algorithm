---
title: Householder QR returns the least squares solution when X has full column rank
proves: [correctness, termination]
status: full
---

Let $X \in \mathbb{R}^{n \times d}$ with $n \ge d$ and $\operatorname{rank} X = d$, and let $y \in \mathbb{R}^n$. We prove that OLS-QR returns the unique minimizer of $f(w) = \|y - Xw\|_2^2$. Arithmetic is exact in this proof.

**Lemma 1 (the minimizer is unique).** $f$ has exactly one minimizer, the solution of $X^\top X w = X^\top y$.

*Proof.* $f(w) = w^\top X^\top X w - 2 y^\top X w + y^\top y$ is a quadratic with Hessian $2X^\top X$. For $u \ne 0$, $u^\top X^\top X u = \|Xu\|^2 > 0$ because the columns of $X$ are independent. So $X^\top X$ is positive definite, $f$ is strictly convex, and its only stationary point $X^\top X w = X^\top y$ is the unique minimizer. $\square$

**Lemma 2 (one reflection).** Let $a \in \mathbb{R}^m$ with $a \ne 0$, let $\alpha = -\operatorname{sign}(a_1)\|a\|$ with $\operatorname{sign}(0) = 1$, let $v = a - \alpha e_1$ and $H = I - 2vv^\top / v^\top v$. Then $v \ne 0$, $H$ is symmetric and orthogonal, and $Ha = \alpha e_1$.

*Proof.* $v_1 = a_1 - \alpha = a_1 + \operatorname{sign}(a_1)\|a\|$, and $|v_1| = |a_1| + \|a\| > 0$, so $v \ne 0$ and $H$ is defined. $H^\top = H$ is clear, and $H^2 = I - 4vv^\top/v^\top v + 4v(v^\top v)v^\top/(v^\top v)^2 = I$, so $H^\top H = I$. For the last claim, $v^\top v = \|a\|^2 - 2\alpha a_1 + \alpha^2 = 2(\|a\|^2 - \alpha a_1)$, because $\alpha^2 = \|a\|^2$, and $v^\top a = \|a\|^2 - \alpha a_1$. So $2v^\top a / v^\top v = 1$ and $Ha = a - v = \alpha e_1$. $\square$

Lines L5 and L6 compute $H$ times a vector as $u - (2v^\top u / v^\top v)v$, which is exactly $Hu$.

**Invariant.** Let $A^{(k)}$ and $b^{(k)}$ be the values of $A$ and $b$ after $k$ passes of the loop of line L2, with $A^{(0)} = X$ and $b^{(0)} = y$. Then for $0 \le k \le d$:

1. there is an orthogonal $Q_k$ with $A^{(k)} = Q_k^\top X$ and $b^{(k)} = Q_k^\top y$, and
2. for each column $j \le k$, the entries $A^{(k)}[i][j]$ with $i > j$ are 0.

*Proof by induction.* For $k = 0$, take $Q_0 = I$; part 2 is empty. Assume the invariant after $k - 1$ passes. Let $a = A^{(k-1)}[k..n][k]$. First, $a \ne 0$. By part 2, the first $k - 1$ columns of $A^{(k-1)}$ are upper triangular with diagonal entries $\alpha_1, \dots, \alpha_{k-1}$, which are nonzero by Lemma 2. If $a = 0$, the first $k$ columns of $A^{(k-1)}$ would have nonzero entries only in rows $1$ to $k - 1$, so they would be dependent. But $A^{(k-1)} = Q_{k-1}^\top X$ has rank $d$, a contradiction. So line L3 finds a nonzero norm and does not stop. Let $\hat H_k$ be the reflection of Lemma 2 for $a$, and $H_k = \operatorname{diag}(I_{k-1}, \hat H_k)$, which is orthogonal and symmetric. Lines L5 and L6 replace the rows $k$ to $n$ of the columns $k$ to $d$ of $A$, and of $b$, by $\hat H_k$ times them. The columns $1$ to $k - 1$ are not changed, but in the rows $k$ to $n$ they are zero by part 2, and $\hat H_k 0 = 0$. So $A^{(k)} = H_k A^{(k-1)}$ and $b^{(k)} = H_k b^{(k-1)}$, and part 1 holds with $Q_k = Q_{k-1}H_k$. Column $k$ of $A^{(k)}$ is zero below row $k$ by Lemma 2, and columns $j < k$ keep their zeros, so part 2 holds. $\square$

**Termination.** The loop of line L2 has $d$ passes, each with a finite number of operations, and line L7 is $d$ steps of back substitution. By the invariant, no pass stops at line L3 when $X$ has rank $d$.

**Theorem.** OLS-QR returns the unique minimizer of $\|y - Xw\|^2$.

*Proof.* After $d$ passes, let $Q = Q_d$, $R = A^{(d)} = Q^\top X$ and $c = b^{(d)} = Q^\top y$. By part 2 of the invariant, $R = \binom{R_1}{0}$ with $R_1$ upper triangular of size $d \times d$, and its diagonal entries are $\alpha_1, \dots, \alpha_d \ne 0$, so $R_1$ is nonsingular. Write $c = \binom{c_1}{c_2}$ with $c_1 \in \mathbb{R}^d$. Since $Q^\top$ is orthogonal, for each $w$,

$$\|y - Xw\|^2 = \|Q^\top y - Q^\top X w\|^2 = \|c_1 - R_1 w\|^2 + \|c_2\|^2 \ge \|c_2\|^2 ,$$

with equality exactly when $R_1 w = c_1$. Line L7 solves this nonsingular triangular system, so line L8 returns the $w$ that reaches the lower bound, which is the unique minimizer of Lemma 1. The minimum value is $\|c_2\|^2$, the sum of the squares of $b[d+1..n]$. $\blacksquare$
