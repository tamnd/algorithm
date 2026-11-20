---
title: The reduced basis solution exists, its error bound is reliable and effective, and the offline-online residual is exact
proves: [correctness]
status: full
---

We assume exact arithmetic. $X = \mathbb{R}^n$ has the inner product $(u, v)_X = u^T X v$ with a symmetric positive definite matrix $X$, and the dual norm of a linear functional $\ell(v) = L^T v$ is $\|\ell\|_{X'} = \sup_{v \ne 0} \ell(v) / \|v\|_X$. For a parameter $\mu$, $a(u, v; \mu) = v^T A(\mu) u$ with $A(\mu) = \sum_{q=1}^{Q} \theta_q(\mu) A_q$, and $F(v) = F^T v$. We assume

- coercivity: $a(v, v; \mu) \ge \alpha(\mu) \|v\|_X^2$ for all $v$, with $\alpha(\mu) > 0$;
- continuity: $|a(u, v; \mu)| \le \gamma(\mu) \|u\|_X \|v\|_X$ for all $u, v$;
- a lower bound $0 < \alpha_{LB}(\mu) \le \alpha(\mu)$.

**Lemma 1 (the Riesz representer).** For a vector $R$, let $\hat{e} = X^{-1} R$. Then $\|R^T \cdot\|_{X'} = \|\hat{e}\|_X$ and $\|\hat{e}\|_X^2 = R^T X^{-1} R$.

*Proof.* $R^T v = \hat{e}^T X v = (\hat{e}, v)_X \le \|\hat{e}\|_X \|v\|_X$ by the Cauchy-Schwarz inequality, with equality for $v = \hat{e}$. And $\|\hat{e}\|_X^2 = R^T X^{-1} X X^{-1} R = R^T X^{-1} R$. $\square$

**Lemma 2 (existence).** Let $Z$ be the $n$ by $r$ matrix of line L2, with $X$-orthonormal columns. Then $A_r(\mu) = Z^T A(\mu) Z = \sum_q \theta_q(\mu) A_q^r$ is invertible, so line L5 has a unique solution $c$, and $u_r = Z c$ satisfies $a(u_r, v; \mu) = F(v)$ for all $v$ in the range $X_r$ of $Z$.

*Proof.* The sum identity holds because $Z^T(\sum_q \theta_q A_q) Z = \sum_q \theta_q Z^T A_q Z$. For $c \ne 0$, $c^T A_r c = a(Z c, Z c; \mu) \ge \alpha(\mu) \|Z c\|_X^2 = \alpha(\mu) |c|^2 > 0$, so $A_r c \ne 0$. The equation $A_r c = Z^T F$ says $(Z e_i)^T A(\mu) Z c = F^T Z e_i$ for each basis vector $Z e_i$, and by linearity for all $v \in X_r$. $\square$

Lines L1 and L2 make $X_r$ the span of the snapshots: Gram-Schmidt in the $X$ inner product keeps the span of the first $j$ vectors at each step $j$, and the snapshots are independent.

**Theorem 1 (reliability and effectivity).** Let $e = u(\mu) - u_r(\mu)$, $R = F - A(\mu) u_r$, $\hat{e} = X^{-1} R$ and $\Delta = \|\hat{e}\|_X / \alpha_{LB}(\mu)$. Then

$$\|e\|_X \le \Delta \le \frac{\gamma(\mu)}{\alpha_{LB}(\mu)} \|e\|_X .$$

*Proof.* Since $A(\mu) u = F$, we have $A(\mu) e = R$, so $a(e, v; \mu) = R^T v = (\hat{e}, v)_X$ for all $v$. With $v = e$: $\alpha(\mu) \|e\|_X^2 \le a(e, e; \mu) = (\hat{e}, e)_X \le \|\hat{e}\|_X \|e\|_X$. If $e = 0$ the first claim is clear; otherwise divide by $\|e\|_X$ to get $\|e\|_X \le \|\hat{e}\|_X / \alpha(\mu) \le \Delta$. With $v = \hat{e}$: $\|\hat{e}\|_X^2 = a(e, \hat{e}; \mu) \le \gamma(\mu) \|e\|_X \|\hat{e}\|_X$, so $\|\hat{e}\|_X \le \gamma(\mu) \|e\|_X$. Divide by $\alpha_{LB}(\mu)$. $\square$

**Lemma 3 (the offline-online residual).** The number $\rho^2$ of line L6 equals $\|\hat{e}\|_X^2$.

*Proof.* $R = F - \sum_q \theta_q \sum_j c_j A_q z_j$. By Lemma 1, $\|\hat{e}\|_X^2 = R^T X^{-1} R$. Expand the product. The term $F^T X^{-1} F$ is $G_{FF}$. Each cross term is $\theta_q c_j F^T X^{-1} A_q z_j = \theta_q c_j g_{qj}$, and it appears twice, with a minus sign, because $X^{-1}$ is symmetric. Each quadratic term is $\theta_q \theta_p c_i c_j (A_q z_i)^T X^{-1} A_p z_j = \theta_q \theta_p c_i c_j G_{qp,ij}$. These are the three sums of line L6, with the tables of line L4. $\square$

So line L7 returns the $\Delta$ of Theorem 1.

**Lemma 4 (reproduction).** If $\mu = \mu_j$ for a sample $j$, then $u_r(\mu) = u(\mu)$ and $\Delta = 0$.

*Proof.* $u(\mu_j)$ is in $X_r$. Let $w = u(\mu_j) - u_r(\mu_j) \in X_r$. By Lemma 2 and the truth equation, $a(w, v; \mu_j) = 0$ for all $v \in X_r$, in particular for $v = w$, and coercivity gives $w = 0$. Then $R = 0$ and $\Delta = 0$. $\square$

**Theorem 2 (the compliance output).** If $A(\mu)$ is symmetric, $s = F^T u$ and $s_r = F^T u_r = F_r^T c$, then $0 \le s - s_r = a(e, e; \mu) \le \|\hat{e}\|_X^2 / \alpha_{LB}(\mu)$.

*Proof.* $s - s_r = F^T e = u^T A e$ by symmetry and $A u = F$. Galerkin orthogonality (Lemma 2) gives $u_r^T A e = u_r^T R = 0$, because $Z^T R = Z^T F - A_r c = 0$. So $F^T e = (u - u_r)^T A e = a(e, e; \mu) \ge 0$. From the proof of Theorem 1, $a(e, e; \mu) = (\hat{e}, e)_X \le \|\hat{e}\|_X \|e\|_X \le \|\hat{e}\|_X^2 / \alpha(\mu) \le \|\hat{e}\|_X^2 / \alpha_{LB}(\mu)$. $\square$

**The model problem.** For $A(\mu) = K + \mu M$ with symmetric positive semidefinite $K$ and $M$ whose sum is positive definite, and $X = K + \bar{\mu} M$ with $\bar{\mu} > 0$: $v^T K v + \mu v^T M v \ge \min(1, \mu/\bar{\mu})(v^T K v + \bar{\mu} v^T M v)$ term by term, so $\alpha_{LB}(\mu) = \min(1, \mu/\bar{\mu}) \le \alpha(\mu)$. With the seminorms $|v|_K$ and $|v|_M$ and the Cauchy-Schwarz inequality, $|u^T K v + \mu u^T M v| \le |u|_K |v|_K + \mu |u|_M |v|_M \le \max(1, \mu/\bar{\mu}) (|u|_K |v|_K + \bar{\mu} |u|_M |v|_M) \le \max(1, \mu/\bar{\mu}) \|u\|_X \|v\|_X$, so $\gamma(\mu) \le \max(1, \mu/\bar{\mu})$. $\blacksquare$
