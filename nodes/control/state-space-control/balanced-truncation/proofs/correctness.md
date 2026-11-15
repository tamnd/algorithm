---
title: The square root method returns a balanced reduced model with gramians diag(sigma_1, ..., sigma_r), and its error obeys the twice-the-tail bound
proves: [correctness]
status: full
---

Let $A \in \mathbb{R}^{n \times n}$ be Hurwitz, $B \in \mathbb{R}^{n \times m}$, $C \in \mathbb{R}^{p \times n}$ and $D \in \mathbb{R}^{p \times m}$, with $G(s) = C (sI - A)^{-1} B + D$. The gramians are the unique solutions of

$$A W_c + W_c A^T + B B^T = 0, \qquad A^T W_o + W_o A + C^T C = 0.$$

They are symmetric positive semidefinite, because $W_c = \int_0^\infty e^{At} B B^T e^{A^T t}\, dt$ and $W_o = \int_0^\infty e^{A^T t} C^T C e^{At}\, dt$ (see [Lyapunov equation](/lyapunov-equation/)). The algorithm takes any square factors $L_c, L_o \in \mathbb{R}^{n \times n}$ with $W_c = L_c L_c^T$ and $W_o = L_o L_o^T$, and a singular value decomposition

$$M = L_o^T L_c = U \Sigma V^T, \qquad \Sigma = \operatorname{diag}(\sigma_1, \dots, \sigma_n), \quad \sigma_1 \ge \dots \ge \sigma_n \ge 0,$$

with $U$ and $V$ orthogonal. For $1 \le r \le n$ with $\sigma_r > 0$, let $U_r$ and $V_r$ be the first $r$ columns of $U$ and $V$, $\Sigma_r = \operatorname{diag}(\sigma_1, \dots, \sigma_r)$, and

$$T_r = L_c V_r \Sigma_r^{-1/2}, \quad W_r = L_o U_r \Sigma_r^{-1/2}, \quad A_r = W_r^T A T_r, \quad B_r = W_r^T B, \quad C_r = C T_r, \quad D_r = D.$$

## Lemma 1: the sigma_i are the Hankel singular values

$\sigma_i^2$ are the eigenvalues of $W_c W_o$, so the $\sigma_i$ do not depend on the choice of factors.

*Proof.* $W_c W_o = L_c (L_c^T L_o L_o^T)$. For square matrices $X$ and $Y$, $XY$ and $YX$ have the same characteristic polynomial. With $X = L_c$ and $Y = L_c^T L_o L_o^T$, $YX = L_c^T L_o L_o^T L_c = M^T M = V \Sigma^2 V^T$, whose eigenvalues are $\sigma_1^2, \dots, \sigma_n^2$. $\square$

## Lemma 2: the two singular vector identities

$M V_r = U_r \Sigma_r$ and $M^T U_r = V_r \Sigma_r$.

*Proof.* $M V = U \Sigma V^T V = U \Sigma$ and $M^T U = V \Sigma U^T U = V \Sigma$. Take the first $r$ columns. $\square$

## Lemma 3: the projection is oblique and exact on its range

$W_r^T T_r = I_r$, so $\Pi = T_r W_r^T$ is a projection and $(A_r, B_r, C_r)$ is the Petrov-Galerkin projection of $(A, B, C)$ onto $\operatorname{im} T_r$ along $\ker W_r^T$.

*Proof.* $W_r^T T_r = \Sigma_r^{-1/2} U_r^T L_o^T L_c V_r \Sigma_r^{-1/2} = \Sigma_r^{-1/2} U_r^T M V_r \Sigma_r^{-1/2} = \Sigma_r^{-1/2} U_r^T U_r \Sigma_r \Sigma_r^{-1/2} = I_r$, by Lemma 2. $\square$

## Lemma 4: the gramians act on the projection bases by Sigma_r

$W_c W_r = T_r \Sigma_r$ and $W_o T_r = W_r \Sigma_r$.

*Proof.* $W_c W_r = L_c L_c^T L_o U_r \Sigma_r^{-1/2} = L_c M^T U_r \Sigma_r^{-1/2} = L_c V_r \Sigma_r \Sigma_r^{-1/2} = T_r \Sigma_r$. In the same way, $W_o T_r = L_o L_o^T L_c V_r \Sigma_r^{-1/2} = L_o M V_r \Sigma_r^{-1/2} = L_o U_r \Sigma_r^{1/2} = W_r \Sigma_r$. Both use Lemma 2. $\square$

## Theorem 1: the reduced model is balanced

$A_r \Sigma_r + \Sigma_r A_r^T + B_r B_r^T = 0$ and $A_r^T \Sigma_r + \Sigma_r A_r + C_r^T C_r = 0$.

*Proof.* Multiply the controllability equation on the left by $W_r^T$ and on the right by $W_r$:

$$W_r^T A (W_c W_r) + (W_r^T W_c) A^T W_r + W_r^T B B^T W_r = 0.$$

By Lemma 4, $W_c W_r = T_r \Sigma_r$, and its transpose is $W_r^T W_c = \Sigma_r T_r^T$. So the left side is $A_r \Sigma_r + \Sigma_r A_r^T + B_r B_r^T$. Multiply the observability equation on the left by $T_r^T$ and on the right by $T_r$, and use $W_o T_r = W_r \Sigma_r$ and $T_r^T W_o = \Sigma_r W_r^T$:

$$T_r^T A^T W_r \Sigma_r + \Sigma_r W_r^T A T_r + T_r^T C^T C T_r = A_r^T \Sigma_r + \Sigma_r A_r + C_r^T C_r = 0. \qquad \square$$

If $A_r$ is Hurwitz, the gramians of the reduced model are the unique solutions of these equations, so both are $\Sigma_r$. The reduced model is then balanced, and its Hankel singular values are $\sigma_1, \dots, \sigma_r$.

## Theorem 2: the reduced model is the truncation of a balanced realization

Assume $\sigma_n > 0$ (the realization is minimal). Let $T = L_c V \Sigma^{-1/2}$. Then $T^{-1} = \Sigma^{-1/2} U^T L_o^T$, the realization $(T^{-1} A T, T^{-1} B, C T)$ is balanced with both gramians equal to $\Sigma$, and $(A_r, B_r, C_r)$ is its leading $r \times r$, $r \times m$ and $p \times r$ block.

*Proof.* Lemma 3 with $r = n$ gives $(\Sigma^{-1/2} U^T L_o^T) T = I$, so this is the inverse. The new gramians are $T^{-1} W_c T^{-T}$ and $T^T W_o T$. Lemma 4 with $r = n$ gives $W_c W_n = T \Sigma$, where $W_n^T = T^{-1}$. So $T^{-1} W_c T^{-T} = T^{-1} (W_c W_n) = T^{-1} T \Sigma = \Sigma$, and $T^T W_o T = T^T W_n \Sigma = \Sigma$. The first $r$ columns of $T$ are $T_r$ and the first $r$ rows of $T^{-1}$ are $W_r^T$, so the leading blocks are $W_r^T A T_r$, $W_r^T B$ and $C T_r$. $\square$

## Theorem 3: stability and the error bound

Assume $\sigma_n > 0$ and $\sigma_r > \sigma_{r+1}$. Then $A_r$ is Hurwitz, and

$$\sigma_{r+1} \le \|G - G_r\|_{\mathcal{H}_\infty} \le 2 \sum_{k} \tau_k,$$

where $\tau_1 > \tau_2 > \dots$ are the distinct values among $\sigma_{r+1}, \dots, \sigma_n$.

*Proof.* By Theorem 2, $G_r$ is the truncation of a balanced realization of $G$. The [balanced truncation error bound](/balanced-truncation-error-bound/) theorem gives both claims for such a truncation; its proof is on that page. The lower bound holds for every model of order $r$, not only for this one. $\square$

## The checks in the implementation

The implementation raises `ValueError` when $0 < r < n$ and $\sigma_r - \sigma_{r+1} \le \text{rtol} \cdot \sigma_1$, because then the hypothesis of Theorem 3 fails or cannot be decided in floating point. It also raises when $\sigma_r = 0$, because $\Sigma_r^{-1/2}$ does not exist. The function `error_bound` counts two computed values as one distinct value when they differ by at most $\text{rtol} \cdot \sigma_1$. In exact arithmetic this is the bound of Theorem 3. In floating point, values that are equal in exact arithmetic come out with a small difference, and without the grouping the bound would count them twice and be up to twice too large.

For a realization that is not minimal ($\sigma_n = 0$), Theorem 1 still holds, because its proof does not use $\sigma_n > 0$. The tests check this case on a system with one uncontrollable state.
